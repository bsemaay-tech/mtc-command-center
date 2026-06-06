"""
MTC Backtest Runner.

Bar-by-bar simulation engine matching MTC Section 4-5 logic flow.
"""

import logging
from typing import Optional, Dict, Any, Tuple
from datetime import datetime
from pathlib import Path
import pandas as pd
import numpy as np

from .mtc_state import MTCState, Position, Trade, Direction, ExitReason, QTY_PRECISION
from .indicators import atr
from ..config.defaults import MTCConfig
from ..modules.confirmation_layer import ConfirmationLayer
from ..modules.signals.base import SignalPlugin, NullSignal
from ..modules.signals.range_filter import RangeFilterHybridSignal
from ..modules.signals.supertrend import SupertrendSignal
from ..modules.filters.base import CompositeFilter, PassThroughFilter
from ..modules.filters.htf_trend_filter import HTFTrendFilter
from ..modules.filters.macd_hub_filter import MacdHubFilter
from ..modules.filters.ma_filter import MAFilter, MASlopeFilter
from ..modules.filters.mcginley_filter import McGinleyFilter
from ..modules.filters.range_regime_filter import RangeRegimeFilter
from ..modules.filters.volume_filter import VolumeFilter, ATRVolatilityFilter
from ..modules.risk.sl_calculator import SLCalculator
from ..modules.risk.tp_calculator import TPCalculator, BreakEvenCalculator, TrailingStopCalculator
from ..modules.risk.position_sizer import PositionSizer

logger = logging.getLogger(__name__)


class MTCRunner:
    _MARGIN_CALL_MAINT_MULT: float = 1.104
    """
    MTC Backtest Engine.
    
    Runs bar-by-bar simulation matching MASTER_TEMPLATE_CORE.pine logic:
    1. Generate raw signals (Section 4)
    2. Apply filters (Section 3)
    3. Apply guards
    4. Determine final signals
    5. Process exits (SL/TP/BE/Trailing)
    6. Process entries
    7. Update state
    """
    
    def __init__(self, config: MTCConfig):
        """
        Initialize MTC runner.
        
        Args:
            config: MTC strategy configuration
        """
        self.config = config
        self._validate_unsupported_config()
        # Keep mintick centralized for sizing/slippage consistency.
        self.mintick = float(config.strategy.mintick)
        
        # Initialize state
        self.state = MTCState(initial_capital=config.strategy.initial_capital)
        
        # Initialize signal plugin
        self.signal_plugin = self._create_signal_plugin()
        
        # Initialize filters
        self.filter_chain = self._create_filter_chain()
        
        # Initialize risk components
        self.sl_calc = SLCalculator(
            mode=config.stop_loss.mode,
            atr_len=config.stop_loss.atr_len,
            atr_mult=config.stop_loss.atr_mult,
            percent=config.stop_loss.percent,
            swing_lookback=config.stop_loss.swing_lookback,
            swing_atr_len=config.stop_loss.swing_atr_len,
            swing_atr_mult=config.stop_loss.swing_atr_mult,
            swing_basis=config.stop_loss.swing_basis,
        )
        
        self.tp_calc = TPCalculator(
            mode=config.take_profit.mode,
            atr_len=config.take_profit.atr_len,
            atr_mult=config.take_profit.atr_mult,
            percent=config.take_profit.percent,
            rr=config.take_profit.rr,
            use_multi_tp=config.multi_tp.enabled,
            tp1_rr=config.multi_tp.tp1_rr,
            tp1_pct=config.multi_tp.tp1_pct,
            tp2_rr=config.multi_tp.tp2_rr,
        )
        
        self.be_calc = BreakEvenCalculator(
            enabled=config.break_even.enabled,
            trigger_rr=config.break_even.rr,
            buffer_r=config.break_even.buffer_r,
        )
        
        self.trail_calc = TrailingStopCalculator(
            enabled=config.trailing.enabled,
            start_r=config.trailing.start_r,
            dist_r=config.trailing.dist_r,
        )
        
        self.sizer = PositionSizer(
            risk_long_pct=config.risk.risk_long_percent,
            risk_short_pct=config.risk.risk_short_percent,
            max_leverage=config.risk.max_leverage_cap,
            mintick=self.mintick,
        )
        
        # Warmup tracking
        self.warmup_bars = 20  # Pine minimum safety warmup

        # First-eval-bar edge gate (reset in run())
        self._first_eval_entry_done = False
        self._ts_series_calendar: Optional[pd.Series] = None
        self._active_df: Optional[pd.DataFrame] = None
        # Per-bar entry diagnostics (exported in debug signals).
        self._last_entry_diag: Dict[str, Any] = {}
        self._same_bar_exit_tp1_fill_bar: Optional[int] = None
        self._same_bar_exit_trail_active_start: Optional[bool] = None
        self._same_bar_exit_trailing_stop: Optional[float] = None
        self._same_bar_exit_trail_start_hit: Optional[bool] = None
        self._margin_call_lock = False
        self._entry_attempted_prev_bar = False
        # Pine-style guard loss streak tracking:
        # update at most once per bar from latest closed trade.
        self._guard_loss_streak = 0
        self._guard_last_closed_count = 0
        self._guard_last_exit_bar = -999999
        self._pending_consec_daily_reset = False

    def _validate_unsupported_config(self) -> None:
        """Fail fast for toggles that are config-visible but not engine-implemented."""
        unsupported: list[str] = []
        c = self.config

        # These knobs are exposed in config/UI but not enforced in runner logic yet.
        if c.strategy.pyramiding != 1:
            unsupported.append("strategy.pyramiding != 1")
        if c.trade.max_pyramid_positions != 1:
            unsupported.append("trade.max_pyramid_positions != 1")
        if c.trade.same_bar_reentry_max_per_bar != 1:
            unsupported.append("trade.same_bar_reentry_max_per_bar != 1")

        if unsupported:
            unsupported_text = ", ".join(unsupported)
            raise NotImplementedError(
                f"Unsupported config toggle(s) enabled: {unsupported_text}. "
                "Disable these options or implement the corresponding FP item first."
            )

    def _reset_daily_guards(self) -> None:
        """Reset per-day guard counters/state for a new run."""
        self._daily_key = None
        self._daily_start_balance = float(self.state.balance)
        self._daily_entry_count = 0
        self._guard_loss_streak = 0
        self._guard_last_closed_count = 0
        self._guard_last_exit_bar = -999999
        self._pending_consec_daily_reset = False

    def _reset_guard_recovery(self) -> None:
        """Reset guard-recovery runtime state for a new run."""
        self._recovery_bars = 0
        self._recovery_signals = 0
        self._virtual_recovery: Optional[Dict[str, Any]] = None

    def _try_guard_recovery(
        self,
        bar_index: int,
        bar: Dict[str, float],
        df: pd.DataFrame,
        long_candidate: bool,
        short_candidate: bool,
    ) -> bool:
        """
        Attempt recovery override when guards block entries.

        Returns True when this bar should bypass guard blocking.
        """
        gc = self.config.guards
        if not gc.use_guard_recovery:
            return False

        has_candidate = bool(long_candidate or short_candidate)
        mode = gc.guard_recovery_mode

        if mode == "Manual":
            return False  # Manual recovery: no auto-resume in backtest

        if mode == "Bars":
            if has_candidate:
                self._recovery_bars += 1
            if self._recovery_bars >= gc.guard_recovery_bars:
                self._recovery_bars = 0
                return True
            return False

        if mode == "Signals":
            if has_candidate:
                self._recovery_signals += 1
            if self._recovery_signals >= gc.guard_recovery_signals:
                self._recovery_signals = 0
                return True
            return False

        # Virtual Trade mode (baseline): simulate 1R trade and recover on virtual TP.
        if mode == "Virtual Trade":
            if self._virtual_recovery is None and has_candidate:
                direction = Direction.LONG if long_candidate else Direction.SHORT
                entry = float(bar["close"])
                sl = None
                if self.config.stop_loss.enabled:
                    sl = self.sl_calc.calculate(
                        df,
                        bar_index,
                        "long" if direction == Direction.LONG else "short",
                        entry,
                        atr_cache=self._atr_cache,
                    )
                if sl is None:
                    sl = entry * (0.99 if direction == Direction.LONG else 1.01)
                risk = max(self.mintick, abs(entry - float(sl)))
                tp = entry + risk if direction == Direction.LONG else entry - risk
                self._virtual_recovery = {
                    "opened_bar": bar_index,
                    "direction": direction,
                    "sl": float(sl),
                    "tp": float(tp),
                }

            vr = self._virtual_recovery
            if vr is None or bar_index <= int(vr["opened_bar"]):
                return False

            is_long = vr["direction"] == Direction.LONG
            high = float(bar["high"])
            low = float(bar["low"])
            tp_hit = high >= float(vr["tp"]) if is_long else low <= float(vr["tp"])
            sl_hit = low <= float(vr["sl"]) if is_long else high >= float(vr["sl"])
            if tp_hit:
                self._virtual_recovery = None
                return True
            if sl_hit:
                self._virtual_recovery = None
            return False

        return False

    def _roll_daily_guards(self, cur_ts: Optional[pd.Timestamp]) -> None:
        """Rotate day-boundary counters when timestamp day changes."""
        if cur_ts is None:
            return
        cur_day = cur_ts.date()
        if self._daily_key != cur_day:
            self._daily_key = cur_day
            self._daily_start_balance = float(self.state.balance)
            self._daily_entry_count = 0
            if self.config.guards.consec_loss_reset_daily:
                self._guard_loss_streak = 0
                self.state.consecutive_losses = 0
                self._pending_consec_daily_reset = False

    def _refresh_guard_loss_streak_from_trades(self, bar_idx: Optional[int] = None) -> bool:
        """
        Sync Pine-style consecutive-loss streak from closed trades.

        Pine logic updates streak when `strategy.closedtrades` count changes and
        uses only the latest closed trade's profit sign for that update.
        Returns True if an update was applied.
        """
        closed_count = len(self.state.trades)
        if closed_count == self._guard_last_closed_count or closed_count <= 0:
            return False
        last_trade = self.state.trades[-1]
        if bar_idx is not None:
            self._guard_last_exit_bar = int(bar_idx)
        if float(last_trade.pnl) < 0.0:
            self._guard_loss_streak += 1
        else:
            self._guard_loss_streak = 0
        self._guard_last_closed_count = closed_count
        self.state.consecutive_losses = self._guard_loss_streak
        return True

    def _daily_loss_percent(self) -> float:
        """Daily realized loss percentage from day-start balance."""
        if self._daily_start_balance <= 0:
            return 0.0
        return max(0.0, ((self._daily_start_balance - float(self.state.balance)) / self._daily_start_balance) * 100.0)

    def _position_mae_percent(self, bar: Dict[str, float]) -> float:
        """Current-bar max adverse excursion percent for active position."""
        if not self.state.in_position or self.state.position is None:
            return 0.0
        entry_price = float(self.state.position.entry_price)
        if entry_price <= 0:
            return 0.0
        if self.state.is_long:
            adverse_move = max(0.0, entry_price - float(bar["low"]))
        else:
            adverse_move = max(0.0, float(bar["high"]) - entry_price)
        return (adverse_move / entry_price) * 100.0

    def _evaluate_entry_guards(
        self,
        *,
        bar_idx: int,
        bar: Dict[str, float],
        can_trade_window: bool,
        in_position_for_mae: bool,
        long_candidate: bool,
        short_candidate: bool,
        allow_recovery: bool,
    ) -> tuple[bool, Optional[float], Optional[float], Optional[bool], str]:
        """
        Evaluate stateful entry guards against the current runner state.

        This helper is used both before exits (bar-start snapshot semantics)
        and after a full close on the same bar so same-bar reentry paths can
        see updated drawdown / daily-loss / cooldown state.
        """
        guard_allow = True
        guard_eq_now_dbg: Optional[float] = None
        guard_eq_ma_dbg: Optional[float] = None
        guard_eq_ok_dbg: Optional[bool] = None
        blocked_reason = ""

        if self.config.guards.use_dd_guard:
            if self.state.max_drawdown >= self.config.guards.dd_guard_pct:
                guard_allow = False
                blocked_reason = "dd_guard"
        if guard_allow and self.config.guards.use_consec_loss_guard:
            if self._guard_loss_streak >= self.config.guards.consec_loss_max:
                guard_allow = False
                blocked_reason = "consec_loss_guard"
        if guard_allow and self.config.guards.use_cooldown_guard:
            bars_since_last = bar_idx - self._guard_last_exit_bar
            if bars_since_last < self.config.guards.cooldown_bars:
                guard_allow = False
                blocked_reason = "cooldown_guard"
        if guard_allow and self.config.guards.use_eq_curve_guard:
            ma_len = int(self.config.guards.eq_curve_ma_len)
            if ma_len > 0:
                eq_now = self._current_equity_mark_to_market(float(bar["close"]))
                guard_eq_now_dbg = float(eq_now)
                guard_eq_ok_dbg = True
                if ma_len == 1:
                    eq_ma = eq_now
                    guard_eq_ma_dbg = float(eq_ma)
                    if eq_now < eq_ma:
                        guard_eq_ok_dbg = False
                        guard_allow = False
                        blocked_reason = "eq_curve_guard"
                else:
                    need_hist = ma_len - 1
                    if len(self.state.equity_curve) >= need_hist:
                        hist = self.state.equity_curve[-need_hist:] if need_hist > 0 else []
                        eq_ma = (sum(hist) + eq_now) / float(ma_len)
                        guard_eq_ma_dbg = float(eq_ma)
                        if eq_now < eq_ma:
                            guard_eq_ok_dbg = False
                            guard_allow = False
                            blocked_reason = "eq_curve_guard"
        if guard_allow and self.config.risk.use_daily_loss_limit:
            if self._daily_loss_percent() >= self.config.risk.max_daily_loss_percent:
                guard_allow = False
                blocked_reason = "daily_loss_limit"
        if guard_allow and self.config.risk.use_max_trades_per_day:
            if self._daily_entry_count >= self.config.risk.max_trades_per_day:
                guard_allow = False
                blocked_reason = "max_trades_per_day"
        if guard_allow and self.config.guards.use_mae_guard and in_position_for_mae:
            if self._position_mae_percent(bar) >= self.config.guards.mae_max_pct:
                guard_allow = False
                blocked_reason = "mae_guard"

        if self._pending_consec_daily_reset:
            self._guard_loss_streak = 0
            self.state.consecutive_losses = 0
            self._pending_consec_daily_reset = False

        if allow_recovery and (not guard_allow) and can_trade_window:
            if self._try_guard_recovery(
                bar_index=bar_idx,
                bar=bar,
                df=self._active_df,
                long_candidate=bool(long_candidate),
                short_candidate=bool(short_candidate),
            ):
                guard_allow = True
                blocked_reason = ""

        return guard_allow, guard_eq_now_dbg, guard_eq_ma_dbg, guard_eq_ok_dbg, blocked_reason

    def _should_exit_on_filter_block(
        self,
        bar_index: int,
        filter_details: Dict[str, Tuple[pd.Series, pd.Series]],
        is_long: bool,
    ) -> bool:
        """Evaluate global or granular filter-block exits for current position side."""
        c = self.config
        selected: list[str] = []
        if c.exit_filter_block.exit_on_ma_block:
            selected.append("MA_Filter")
        if c.exit_filter_block.exit_on_ma_slope_block:
            selected.append("MA_Slope_Filter")
        if c.exit_filter_block.exit_on_mcginley_block:
            selected.append("McGinley_Filter")
        if c.exit_filter_block.exit_on_htf_trend_block:
            selected.append("HTF_Trend_Filter")
        if c.exit_filter_block.exit_on_vol_part_block:
            selected.append("Volume_Filter")
        if c.exit_filter_block.exit_on_atr_vol_block:
            selected.append("ATR_Vol_Filter")
        if c.exit_filter_block.exit_on_range_block:
            selected.append("Range_Regime_Filter")

        if not selected:
            if not c.trade.exit_on_filter_block:
                return False
            selected = list(filter_details.keys())

        for name in selected:
            pair = filter_details.get(name)
            if pair is None:
                continue
            f_long, f_short = pair
            allow_side = bool(f_long.iloc[bar_index]) if is_long else bool(f_short.iloc[bar_index])
            if not allow_side:
                return True
        return False

    @staticmethod
    def _is_day_change(i: int, ts_series: Optional[pd.Series]) -> bool:
        """Return True on the first bar of a new calendar day (Pine ta.change(time(\"D\")))."""
        if ts_series is None or i <= 0 or i >= len(ts_series):
            return False
        cur = pd.Timestamp(ts_series.iloc[i])
        prev = pd.Timestamp(ts_series.iloc[i - 1])
        return cur.date() != prev.date()

    @staticmethod
    def _is_week_change(i: int, ts_series: Optional[pd.Series]) -> bool:
        """Return True on the first bar of a new ISO week (Pine ta.change(time(\"W\")))."""
        if ts_series is None or i <= 0 or i >= len(ts_series):
            return False
        cur = pd.Timestamp(ts_series.iloc[i]).isocalendar()
        prev = pd.Timestamp(ts_series.iloc[i - 1]).isocalendar()
        return (cur.year, cur.week) != (prev.year, prev.week)

    @staticmethod
    def _is_end_of_day(i: int, ts_series: Optional[pd.Series]) -> bool:
        """Return True when the current bar is the last available bar of its UTC day."""
        if ts_series is None or i < 0 or i >= len(ts_series):
            return False
        if i == len(ts_series) - 1:
            return True
        cur = pd.Timestamp(ts_series.iloc[i])
        nxt = pd.Timestamp(ts_series.iloc[i + 1])
        return cur.date() != nxt.date()

    @staticmethod
    def _is_end_of_week(i: int, ts_series: Optional[pd.Series]) -> bool:
        """Return True when the current bar is the last available bar of its ISO week."""
        if ts_series is None or i < 0 or i >= len(ts_series):
            return False
        if i == len(ts_series) - 1:
            return True
        cur = pd.Timestamp(ts_series.iloc[i]).isocalendar()
        nxt = pd.Timestamp(ts_series.iloc[i + 1]).isocalendar()
        return (cur.year, cur.week) != (nxt.year, nxt.week)

    def _time_stop_would_trigger(self, bar_idx: int, mark_price: float) -> bool:
        """Evaluate whether time-stop condition is true on this bar for current position."""
        time_stop_active = (
            self.config.time_stop.enabled
            or self.config.time_stop.use_bars
            or self.config.time_stop.eod
            or self.config.time_stop.eow
        )
        if not time_stop_active or not self.state.in_position or self.state.position is None:
            return False
        pos = self.state.position
        bars_in_pos = bar_idx - pos.entry_bar
        bar_limit_met = (
            (self.config.time_stop.enabled or self.config.time_stop.use_bars)
            and bars_in_pos >= self.config.time_stop.bars
        )
        eod_condition = self.config.time_stop.eod and self._is_day_change(bar_idx, self._ts_series_calendar)
        eow_condition = self.config.time_stop.eow and self._is_week_change(bar_idx, self._ts_series_calendar)
        cond = self.config.time_stop.condition
        unrealized = pos.unrealized_pnl(mark_price)
        condition_met = (
            cond == "Always"
            or (cond == "Profit Only" and unrealized > 0)
            or (cond == "Loss Only" and unrealized < 0)
        )
        return condition_met and (bar_limit_met or eod_condition or eow_condition)

    # RMA convergence constants -------------------------------------------
    # RMA(n) retains ~(1-1/n)^k of its initial seed after k bars.
    # To reduce seed influence to <1 %, we need k ≥ n·ln(100) ≈ 4.6·n.
    # We use 5× as a round, safe multiplier and clamp to [200, 2000] bars
    # so that very small or very large ATR lengths remain practical.
    _RMA_CONVERGENCE_MULT: int = 5
    _WARMUP_FLOOR: int = 200
    _WARMUP_CEIL: int = 2000

    def _compute_warmup_bars(self) -> int:
        """
        Compute dynamic warmup bars similar to Pine warmup gate,
        **with RMA convergence clamp**.

        Two-stage approach:
        1. Collect raw indicator lookback lengths (Pine-compatible).
        2. Multiply every RMA-based lookback by ``_RMA_CONVERGENCE_MULT``
           so the exponential seed decays to <1 %.  Final value is clamped
           to [_WARMUP_FLOOR, _WARMUP_CEIL].
        """
        c = self.config

        # --- Stage 1: raw lookback candidates (non-RMA) ---
        raw_candidates: list[int] = [20]

        # Filters (SMA/EMA: converge quickly, no multiplier needed)
        if c.filters.use_ma_filter:
            raw_candidates.append(int(c.filters.ma_length))
        if c.filters.use_ma_slope_filter:
            raw_candidates.append(int(c.filters.ma_slope_len))
        if c.filters.use_volume_filter:
            raw_candidates.append(int(c.filters.vol_filter_len))
        if c.filters.use_atr_vol_filter:
            raw_candidates.append(int(max(c.filters.atr_vol_len, c.filters.atr_vol_smooth_len)))
        if c.filters.use_mcginley_filter:
            raw_candidates.append(int(c.filters.mcginley_len))
        if c.filters.use_macd_filter:
            raw_candidates.append(int(max(c.filters.macd_fast_len, c.filters.macd_slow_len, c.filters.macd_signal_len)))
        range_regime_enabled = c.filters.use_range_filters or c.filters.use_range_regime_filter
        if range_regime_enabled:
            raw_candidates.append(14)

        # Swing SL lookback (not RMA-based)
        if c.stop_loss.mode in ("Swing+ATR", "SWING_ATR"):
            raw_candidates.append(int(c.stop_loss.swing_lookback + 1))

        # --- Stage 2: RMA-based lookbacks (need convergence multiplier) ---
        rma_candidates: list[int] = []

        # Supertrend ATR (RMA inside ATR)
        if c.signal_mode == "Supertrend":
            rma_candidates.append(int(c.supertrend.atr_len))
        elif c.signal_mode in ("Range Filter Hybrid", "Range Filter Hybrid (ADX+Chop+BB)"):
            rma_candidates.append(int(max(c.range_filter.rsi_len, c.range_filter.bb_len)))

        # SL / TP / Trailing ATR lengths
        if c.stop_loss.enabled:
            rma_candidates.append(int(c.stop_loss.atr_len))
            if c.stop_loss.mode in ("Swing+ATR", "SWING_ATR"):
                rma_candidates.append(int(c.stop_loss.swing_atr_len))
        if c.take_profit.enabled:
            rma_candidates.append(int(c.take_profit.atr_len))
        if c.trailing.enabled:
            rma_candidates.append(int(c.trailing.atr_len))

        # Apply convergence multiplier to RMA candidates
        scaled_rma = [n * self._RMA_CONVERGENCE_MULT for n in rma_candidates]

        all_candidates = raw_candidates + scaled_rma
        warmup = max(all_candidates) if all_candidates else 20

        # Clamp to [FLOOR, CEIL]
        warmup = max(self._WARMUP_FLOOR, min(warmup, self._WARMUP_CEIL))
        return int(warmup)
    
    def _use_close_fill_contract(self) -> bool:
        """Return True when parity mode enforces close-based exit checks."""
        return self.config.parity.enabled and self.config.parity.fill_contract == "close"

    def _stop_reason_for_position(self, pos) -> ExitReason:
        if getattr(pos, "trailing_active", False):
            return ExitReason.TRAIL
        if getattr(pos, "be_triggered", False):
            return ExitReason.BE
        return ExitReason.SL
    
    def _long_stop_hit(self, low: float, close: float, stop_price: float) -> bool:
        if self._use_close_fill_contract():
            return close <= stop_price
        return low <= stop_price
    
    def _short_stop_hit(self, high: float, close: float, stop_price: float) -> bool:
        if self._use_close_fill_contract():
            return close >= stop_price
        return high >= stop_price
    
    def _long_tp_hit(self, high: float, close: float, tp_price: float) -> bool:
        if self._use_close_fill_contract():
            return close >= tp_price
        return high >= tp_price
    
    def _short_tp_hit(self, low: float, close: float, tp_price: float) -> bool:
        if self._use_close_fill_contract():
            return close <= tp_price
        return low <= tp_price

    def _tv_high_first(self, bar: Dict) -> bool:
        """
        TradingView historical intrabar path heuristic (no bar magnifier):
        open -> (nearest extreme first) -> other extreme -> close.
        """
        d_high = abs(float(bar['open']) - float(bar['high']))
        d_low = abs(float(bar['open']) - float(bar['low']))
        return d_high <= d_low

    def _apply_slippage(self, price: float, is_buy: bool) -> float:
        """Apply slippage ticks to price."""
        if self.config.strategy.slippage_ticks <= 0:
            return price
        
        # Pine slippage is in ticks; align with configured mintick.
        tick_size = self.mintick
        slip_val = self.config.strategy.slippage_ticks * tick_size
        return price + slip_val if is_buy else price - slip_val

    def _margin_ratio(self, direction: Direction | str) -> float:
        """Return margin ratio (0..1) for side, mirroring Pine strategy() margin settings."""
        if isinstance(direction, Direction):
            is_long = direction == Direction.LONG
        else:
            is_long = str(direction).lower().startswith("long")
        pct = (
            self.config.strategy.margin_long_percent
            if is_long
            else self.config.strategy.margin_short_percent
        )
        return max(float(pct) / 100.0, 1e-9)

    def _margin_call_maint_mult(self, direction: Direction | str) -> float:
        if isinstance(direction, Direction):
            is_long = direction == Direction.LONG
        else:
            is_long = str(direction).lower().startswith("long")
        return self._MARGIN_CALL_MAINT_MULT if is_long else 0.97

    def _current_equity_mark_to_market(self, mark_price: float) -> float:
        """Current strategy equity using realized balance + open PnL at mark price."""
        if self.state.in_position and self.state.position is not None:
            pos = self.state.position
            # Pine parity: entry commission affects strategy.equity immediately on entry.
            # We model this on mark-to-market equity by subtracting the remaining
            # (not-yet-realized in balance) entry commission for open quantity.
            pending_entry_commission = (
                float(pos.entry_price)
                * abs(float(pos.quantity))
                * (float(self.config.strategy.commission_percent) / 100.0)
            )
            return float(
                self.state.balance
                + pos.unrealized_pnl(mark_price)
                - pending_entry_commission
            )
        return float(self.state.balance)

    def _margin_required(self, notional: float, direction: Direction | str) -> float:
        """Required margin for a side and notional."""
        return max(0.0, float(notional)) * self._margin_ratio(direction)

    def _can_afford_margin(
        self,
        *,
        post_notional: float,
        direction: Direction | str,
        mark_price: float,
    ) -> bool:
        """
        Entry affordability gate.

        TradingView parity: the broker emulator can still accept a fresh entry
        that is near/through the margin threshold and then liquidate it on a
        later bar via margin-call handling. A strict `equity >= required`
        pre-entry block suppresses real TV trades in deep drawdown tails.
        """
        equity_now = self._current_equity_mark_to_market(mark_price)
        return equity_now > 0.0



    def _is_margin_call(self, mark_price: float) -> bool:
        """
        Forced liquidation trigger.

        Approximation of TV rule: margin call when current equity <= required margin.
        """
        if not self.state.in_position or self.state.position is None:
            return False
        pos = self.state.position
        notional = abs(float(pos.quantity)) * max(float(mark_price), self.mintick)
        equity_now = self._current_equity_mark_to_market(mark_price)
        required = self._margin_required(notional, pos.direction) * self._margin_call_maint_mult(pos.direction)
        return equity_now <= required

    @staticmethod
    def _truncate_toward_zero(value: float, step: float) -> float:
        """TradingView-like truncation toward zero with quantity step support."""
        s = max(float(step), 1e-12)
        return float(np.trunc(float(value) / s) * s)

    @staticmethod
    def _infer_qty_step(qty: float) -> float:
        """
        Infer quantity precision step from observed position size.

        TV uses symbol min contract size. We infer a practical step from current qty
        precision and clamp to a sane minimum for crypto-style symbols.
        """
        q = abs(float(qty))
        if q <= 0:
            return 1e-6
        txt = f"{q:.12f}".rstrip("0").rstrip(".")
        if "." not in txt:
            return 1.0
        dec = len(txt.split(".", 1)[1])
        dec = max(0, min(dec, 8))
        return max(10.0 ** (-dec), 1e-6)

    def _margin_call_liquidation_qty(self, mark_price: float) -> float:
        """
        Compute margin-call liquidation quantity using TV broker-emulator style math.

        TV does partial liquidation on margin call:
          MoneyLost = AvailableFunds / MarginRatio
          CoverUnits = trunc(MoneyLost / Price, min_contract_step)
          Liquidate  = abs(CoverUnits) * 4
        """
        if not self.state.in_position or self.state.position is None:
            return 0.0

        pos = self.state.position
        qty_abs = abs(float(pos.quantity))
        if qty_abs <= 0:
            return 0.0

        px = max(float(mark_price), self.mintick)
        mr = self._margin_ratio(pos.direction)
        if mr <= 0:
            return qty_abs

        # Current position value and equity at mark.
        mvs = qty_abs * px
        equity_now = self._current_equity_mark_to_market(px)
        margin = mvs * mr * self._margin_call_maint_mult(pos.direction)
        if equity_now > margin:
            return 0.0

        available_funds = equity_now - margin
        money_lost = available_funds / mr
        raw_cover_units = money_lost / px

        qty_step = self._infer_qty_step(qty_abs)
        cover_units = self._truncate_toward_zero(raw_cover_units, qty_step)
        liq_qty = abs(cover_units) * 4.0
        liq_qty = self._truncate_toward_zero(liq_qty, qty_step)
        if liq_qty <= 0:
            # Keep liquidation minimal but non-zero to avoid over-liquidating.
            liq_qty = min(qty_abs, qty_step * 4.0)
        return min(qty_abs, liq_qty)

    def _is_capital_exhausted(self, mark_price: float) -> bool:
        """
        Dynamic entry-capital guard aligned with Pine FIX MARGIN-5 semantics.

        Fresh entries should be blocked only when current equity is non-positive,
        or when max tradable notional (equity * leverage cap) cannot finance even
        the minimum tradable quantity step at the current market price.
        """
        px = max(float(mark_price), self.mintick)
        equity_now = float(self.state.balance if not self.state.in_position else self.state.equity)
        if equity_now <= 0.0:
            return True

        min_qty = QTY_PRECISION
        if self.state.in_position and self.state.position is not None:
            pos_qty = abs(float(self.state.position.quantity))
            if pos_qty > 0:
                min_qty = max(self._infer_qty_step(pos_qty), QTY_PRECISION)

        min_tradable_notional = min_qty * px
        max_tradable_notional = max(equity_now, 0.0) * float(self.config.risk.max_leverage_cap)
        return max_tradable_notional < min_tradable_notional
    
    def _create_signal_plugin(self) -> SignalPlugin:
        """Create signal plugin based on configuration."""
        if self.config.signal_mode == "Supertrend":
            return SupertrendSignal(
                atr_len=self.config.supertrend.atr_len,
                factor=self.config.supertrend.factor,
                use_wicks=self.config.supertrend.use_wicks,
                use_ha=self.config.supertrend.use_ha,
            )
        elif self.config.signal_mode in ("Range Filter Hybrid", "Range Filter Hybrid (ADX+Chop+BB)"):
            rf = self.config.range_filter
            return RangeFilterHybridSignal(
                adx_trend_threshold=rf.adx_trend_threshold,
                adx_range_threshold=rf.adx_range_threshold,
                chop_trend_threshold=rf.chop_trend_threshold,
                chop_range_threshold=rf.chop_range_threshold,
                rsi_len=rf.rsi_len,
                rsi_oversold=rf.rsi_oversold,
                rsi_overbought=rf.rsi_overbought,
                bb_len=rf.bb_len,
                bb_mult=rf.bb_mult,
                use_bb_filter=rf.use_bb_filter,
            )
        else:
            return NullSignal()
    
    def _create_filter_chain(self) -> CompositeFilter:
        """Create filter chain based on configuration."""
        chain = CompositeFilter()
        
        # MA Filter
        if self.config.filters.use_ma_filter:
            chain.add_filter(MAFilter(
                enabled=True,
                ma_type=self.config.filters.ma_type,
                length=self.config.filters.ma_length,
                use_htf=self.config.filters.ma_use_higher_timeframe,
                htf_timeframe=self.config.filters.ma_htf_timeframe,
            ))

        # MA Slope Filter
        if self.config.filters.use_ma_slope_filter:
            chain.add_filter(MASlopeFilter(
                enabled=True,
                ma_type=self.config.filters.ma_type,
                length=self.config.filters.ma_slope_len,
                min_slope_pct=self.config.filters.ma_slope_min_pct,
            ))
        
        # Volume Filter
        if self.config.filters.use_volume_filter:
            chain.add_filter(VolumeFilter(
                enabled=True,
                length=self.config.filters.vol_filter_len,
                mult=self.config.filters.vol_filter_mult,
            ))
        
        # ATR Volatility Filter
        if self.config.filters.use_atr_vol_filter:
            chain.add_filter(ATRVolatilityFilter(
                enabled=True,
                atr_len=self.config.filters.atr_vol_len,
                smooth_len=self.config.filters.atr_vol_smooth_len,
                floor_mult=self.config.filters.atr_vol_floor_mult,
            ))

        # McGinley Filter
        if self.config.filters.use_mcginley_filter:
            chain.add_filter(McGinleyFilter(
                enabled=True,
                length=self.config.filters.mcginley_len,
                k=self.config.filters.mcginley_k,
                use_htf=self.config.filters.use_mcginley_htf,
                htf_timeframe=self.config.filters.mcginley_htf_timeframe,
            ))

        # MACD Hub Filter
        if self.config.filters.use_macd_filter:
            chain.add_filter(MacdHubFilter(
                enabled=True,
                gate_mode=self.config.filters.macd_gate_mode,
                source=self.config.filters.macd_source,
                fast_len=self.config.filters.macd_fast_len,
                slow_len=self.config.filters.macd_slow_len,
                signal_len=self.config.filters.macd_signal_len,
                distance_pct=self.config.filters.macd_distance_pct,
                htf_timeframe=self.config.filters.macd_htf_timeframe,
                use_htf_bias=self.config.filters.macd_use_htf_bias,
            ))

        # Range Regime Filter
        range_regime_enabled = self.config.filters.use_range_filters or self.config.filters.use_range_regime_filter
        if range_regime_enabled:
            # Pine parity: prefer explicit hysteresis thresholds (on/off).
            # Keep backward-compat fallback for older case files.
            adx_off = float(self.config.filters.range_regime_adx_off)
            chop_off = float(self.config.filters.range_regime_chop_off)
            adx_on = float(self.config.filters.range_regime_adx_on)
            chop_on = float(self.config.filters.range_regime_chop_on)

            if adx_on == 25.0 and self.config.filters.range_regime_adx_min != 20.0:
                adx_off = float(self.config.filters.range_regime_adx_min)
            if chop_off == 62.0 and self.config.filters.range_regime_chop_max != 62.0:
                chop_off = float(self.config.filters.range_regime_chop_max)

            chain.add_filter(RangeRegimeFilter(
                enabled=True,
                adx_on=adx_on,
                adx_off=adx_off,
                chop_on=chop_on,
                chop_off=chop_off,
                hold_bars=self.config.filters.range_regime_hold_bars,
                agg_mode=self.config.filters.range_agg_mode,
                min_pass=self.config.filters.range_min_pass,
                adx_len=self.config.filters.range_regime_adx_len,
                chop_len=self.config.filters.range_regime_chop_len,
            ))

        # HTF Trend Filter
        if self.config.filters.use_htf_trend_filter:
            chain.add_filter(HTFTrendFilter(
                enabled=True,
                timeframe=self.config.filters.htf_trend_timeframe,
                ma_type=self.config.filters.htf_trend_ma_type,
                ma_len=self.config.filters.htf_trend_ma_len,
                buffer_pct=self.config.filters.htf_trend_buffer_pct,
            ))
        
        return chain
    
    def run(
        self,
        df: pd.DataFrame,
        warmup_bars: Optional[int] = None,
        progress_callback: Optional[callable] = None,
        eval_start: Optional[datetime] = None,
        eval_end: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Run backtest simulation.
        
        Args:
            df: OHLCV DataFrame
            warmup_bars: Bars to skip for indicator warmup (None -> dynamic Pine-like warmup)
            progress_callback: Optional callback(current_bar, total_bars)
            eval_start: Optional UTC datetime start for evaluation window
            eval_end: Optional UTC datetime end for evaluation window
            
        Returns:
            Dict with results:
            - metrics: Performance metrics dict
            - trades: List of Trade objects
            - equity_curve: List of equity values
            - signals: List of signal records
        """
        import time
        start_time = time.time()

        eval_start_ts = None
        eval_end_ts = None
        if eval_start is not None:
            eval_start_ts = pd.Timestamp(eval_start)
            eval_start_ts = eval_start_ts.tz_localize("UTC") if eval_start_ts.tzinfo is None else eval_start_ts.tz_convert("UTC")
        if eval_end is not None:
            eval_end_ts = pd.Timestamp(eval_end)
            eval_end_ts = eval_end_ts.tz_localize("UTC") if eval_end_ts.tzinfo is None else eval_end_ts.tz_convert("UTC")
        
        # Reset state
        self.state.reset()
        self._active_df = df
        self.state.initial_capital = self.config.strategy.initial_capital
        self.state.balance = self.config.strategy.initial_capital
        self.state.equity = self.config.strategy.initial_capital
        self._first_eval_entry_done = False
        self._pending_entry_direction: Optional[Direction] = None
        self._same_bar_exit_tp1_fill_bar = None
        self._same_bar_exit_trail_active_start = None
        self._same_bar_exit_trailing_stop = None
        self._same_bar_exit_trail_start_hit = None
        self._margin_call_lock = False
        self._entry_attempted_prev_bar = False
        self._reset_daily_guards()
        self._reset_guard_recovery()
        resolved_warmup = self._compute_warmup_bars() if warmup_bars is None else int(warmup_bars)
        self.warmup_bars = resolved_warmup
        
        # Pre-calculate signals for all bars
        logger.info("Pre-calculating signals...")
        long_raw, short_raw = self.signal_plugin.generate(df)
        get_debug_series = getattr(self.signal_plugin, "get_debug_series", None)
        signal_debug_series = get_debug_series(df) if callable(get_debug_series) else {}
        
        # Pre-calculate filter outputs
        logger.info("Pre-calculating filters...")
        allow_long, allow_short, filter_details = self.filter_chain.apply_with_details(df)
        
        # Pre-compute ATR series (avoid per-entry recomputation)
        logger.info("Pre-computing ATR cache...")
        _t_precompute = time.perf_counter()
        self._atr_cache = {}
        atr_lengths = set()
        if self.config.stop_loss.enabled:
            atr_lengths.add(self.config.stop_loss.atr_len)
            atr_lengths.add(self.config.stop_loss.swing_atr_len)
        if self.config.take_profit.enabled:
            atr_lengths.add(self.config.take_profit.atr_len)
        for atr_len in atr_lengths:
            self._atr_cache[atr_len] = atr(df['high'], df['low'], df['close'], atr_len)

        self._confirmation = (
            ConfirmationLayer(df, self.config.confirmation, self.mintick)
            if self.config.confirmation.enabled else None
        )
        
        # Pre-convert timestamps (avoid per-bar pd.Timestamp construction)
        _ts_series = pd.to_datetime(df['timestamp'], utc=True) if 'timestamp' in df.columns else None
        _ts_series_calendar = _ts_series
        if _ts_series is not None:
            try:
                _ts_series_calendar = _ts_series.dt.tz_convert(self.config.time_stop.timezone)
            except Exception:
                _ts_series_calendar = _ts_series
        self._ts_series_calendar = _ts_series_calendar
        _precompute_time = time.perf_counter() - _t_precompute
        
        # Run bar-by-bar simulation
        logger.info(f"Running simulation on {len(df)} bars...")
        
        # Signal-mode multi-entry tracking (Pine parity)
        current_entries_long = 0
        current_entries_short = 0
        last_entry_bar = -999999
        prev_entry_long_signal = False
        prev_entry_short_signal = False
        
        _t_loop = time.perf_counter()
        for i in range(len(df)):
            self.state.bar_index = i
            self.state.current_time = _ts_series.iloc[i] if _ts_series is not None else None
            
            # Get current bar data
            bar = {
                'open': df['open'].iloc[i],
                'high': df['high'].iloc[i],
                'low': df['low'].iloc[i],
                'close': df['close'].iloc[i],
                'volume': df['volume'].iloc[i],
            }
            
            # Skip warmup period
            if i < resolved_warmup:
                self.state.update_equity(self.state.balance)
                continue
            
            self.state.warmup_complete = True

            # --- Preroll / Eval Window Classification ---
            # Bars are classified into:
            #   in_preroll: before eval_start — indicators run, trading gated
            #   in_eval:    eval_start <= ts <= eval_end — full trading
            #
            # preroll_mode controls trading during preroll:
            #   "warmup_only" (DEFAULT): NO trading at all — engine stays FLAT.
            #     Eval window always starts from clean FLAT state (TV parity).
            #   "trade": preroll bars allow trading (legacy/research mode).
            #     Positions may carry into eval window.
            cur_ts = _ts_series.iloc[i] if _ts_series is not None else None
            cur_ts_calendar = _ts_series_calendar.iloc[i] if _ts_series_calendar is not None else cur_ts
            self._roll_daily_guards(cur_ts_calendar)
            in_preroll = False
            in_eval = True
            if eval_start_ts is not None and cur_ts is not None:
                in_preroll = cur_ts < eval_start_ts
                in_eval = not in_preroll
            entered_eval_from_preroll = False
            if eval_start_ts is not None and cur_ts is not None and i > 0:
                prev_ts = _ts_series.iloc[i - 1] if _ts_series is not None else None
                entered_eval_from_preroll = (
                    prev_ts is not None
                    and prev_ts < eval_start_ts
                    and cur_ts >= eval_start_ts
                )

            # Preroll warmup-only gate: skip ALL trading actions
            preroll_warmup_only = (
                in_preroll
                and self.config.parity.preroll_mode == "warmup_only"
            )
            if preroll_warmup_only:
                # Indicators/signals/filters already computed above (pre-loop).
                # DO NOT mutate position state. Engine stays FLAT.
                # Advance stateful modules so their internal state matches TV's
                # accumulated history from bar 0 of the chart.
                if self._confirmation is not None:
                    _pr_lr = bool(long_raw.iloc[i]) if not pd.isna(long_raw.iloc[i]) else False
                    _pr_sr = bool(short_raw.iloc[i]) if not pd.isna(short_raw.iloc[i]) else False
                    self._confirmation.step(i=i, pos_size=0.0, long_raw=_pr_lr, short_raw=_pr_sr)
                # Still record debug row if enabled.
                if self.config.parity.export_debug_csv:
                    self.state.record_signal(
                        long_raw=False, short_raw=False,
                        allow_long=True, allow_short=True,
                        long_final=False, short_final=False,
                        guard_allow=True,
                        final_long_entry=False, final_short_entry=False,
                        blocked_filters_long="", blocked_filters_short="",
                        blocked_filters="",
                        exit_reason=None,
                        pos_side="FLAT", open_legs=0,
                        entry_price=None, sl_price=None,
                        be_triggered=False, trailing_active=False,
                        can_trade=False,
                        in_position_start_bar=False,
                        in_position_after_exits=False,
                        exit_fired=False, exited_this_bar=False,
                        can_attempt_entry=False,
                        same_bar_reentry_allowed=False,
                        blocked_reason="PREROLL_WARMUP_ONLY",
                        in_preroll=True, in_eval=False,
                    )
                self.state.update_equity(self.state.balance)
                continue

            # --- trade_start gate ---
            # can_trade_window determines if entries/exits are allowed:
            #   warmup_only (already handled above with `continue`)
            #   trade: preroll bars CAN trade, positions may carry over
            if eval_start_ts is not None and cur_ts is not None:
                if self.config.parity.preroll_mode == "trade":
                    # In trade mode, trading is allowed even during preroll.
                    # Trades from preroll are excluded from eval metrics later.
                    can_trade_window = True
                else:
                    # warmup_only never reaches here (continue'd above),
                    # but as safety fallback, block trading before eval_start.
                    can_trade_window = cur_ts >= eval_start_ts
            else:
                can_trade_window = True

            if (
                entered_eval_from_preroll
                and self.config.parity.preroll_mode == "warmup_only"
                and self._confirmation is not None
            ):
                _ev_lr = bool(long_raw.iloc[i]) if not pd.isna(long_raw.iloc[i]) else False
                _ev_sr = bool(short_raw.iloc[i]) if not pd.isna(short_raw.iloc[i]) else False
                self._confirmation.align_wait_state_on_eval_start(
                    i=i,
                    long_raw=_ev_lr,
                    short_raw=_ev_sr,
                )

            # Snapshot bar-start position state before any close/exit logic.
            in_position_start_bar = self.state.in_position
            is_long_start_bar = self.state.is_long
            is_short_start_bar = self.state.is_short
            if self.config.risk.risk_equity_mode == "Initial":
                bar_start_risk_equity = self.state.initial_capital
            else:
                bar_start_risk_equity = float(self.state.balance)
                if in_position_start_bar and self.state.position is not None:
                    bar_start_risk_equity -= (
                        float(self.state.position.entry_price)
                        * abs(float(self.state.position.quantity))
                        * (float(self.config.strategy.commission_percent) / 100.0)
                    )

            if self._entry_attempted_prev_bar and not in_position_start_bar:
                # Pine parity: rejected entry attempts are diagnostic only.
                # They must not permanently lock the engine.
                pass
            self._entry_attempted_prev_bar = False

            # --- Eval window boundary: force-flatten carried position ---
            # When preroll_mode="trade" and close_open_at_eval_start=True,
            # if we just crossed into eval window with an open position,
            # close it so eval starts FLAT.
            if (in_eval and self.state.in_position
                    and self.config.parity.preroll_mode == "trade"
                    and self.config.parity.close_open_at_eval_start
                    and eval_start_ts is not None and cur_ts is not None):
                # Check if previous bar was preroll
                prev_ts = _ts_series.iloc[i - 1] if i > 0 and _ts_series is not None else None
                if prev_ts is not None and prev_ts < eval_start_ts:
                    self.state.close_position(
                        exit_price=bar['close'],
                        exit_reason=ExitReason.EVAL_START_FLATTEN,
                        commission_pct=self.config.strategy.commission_percent,
                    )

            if not in_position_start_bar:
                current_entries_long = 0
                current_entries_short = 0
            
            # Get signals for this bar
            long_signal_raw = long_raw.iloc[i] if not pd.isna(long_raw.iloc[i]) else False
            short_signal_raw = short_raw.iloc[i] if not pd.isna(short_raw.iloc[i]) else False
            prev_long_raw = long_raw.iloc[i - 1] if i > 0 and not pd.isna(long_raw.iloc[i - 1]) else False
            prev_short_raw = short_raw.iloc[i - 1] if i > 0 and not pd.isna(short_raw.iloc[i - 1]) else False
            
            # Get filter outputs
            filter_long = allow_long.iloc[i] if not pd.isna(allow_long.iloc[i]) else True
            filter_short = allow_short.iloc[i] if not pd.isna(allow_short.iloc[i]) else True
            
            # Pine parity: confirmation emits the entry signal first; entry
            # mode edge shaping is applied to the confirmed pulses/levels.
            entry_long_signal = bool(long_signal_raw)
            entry_short_signal = bool(short_signal_raw)
            conf_waiting_long = False
            conf_waiting_short = False
            if self._confirmation is not None:
                pos_size_start = 1.0 if is_long_start_bar else (-1.0 if is_short_start_bar else 0.0)
                conf_step = self._confirmation.step(
                    i=i,
                    pos_size=pos_size_start,
                    long_raw=bool(long_signal_raw),
                    short_raw=bool(short_signal_raw),
                )
                entry_long_signal = conf_step.long_confirmed
                entry_short_signal = conf_step.short_confirmed
                conf_waiting_long = conf_step.waiting_long
                conf_waiting_short = conf_step.waiting_short

            if self.config.trade.entry_mode == "Edge":
                long_edge = bool(entry_long_signal and not prev_entry_long_signal)
                short_edge = bool(entry_short_signal and not prev_entry_short_signal)
            else:
                long_edge = bool(entry_long_signal)
                short_edge = bool(entry_short_signal)

            # Apply filters after confirmation/entry pulse shaping.
            long_filtered = long_edge and filter_long
            short_filtered = short_edge and filter_short
            
            # Pine parity: regime lock gates against previous bar's tracked
            # confirmed-signal direction, not the current bar update.
            prev_signal_direction = self.state.last_signal_direction

            # Update signal direction tracker on confirmed signal pulses/levels,
            # independent from entry_mode edge shaping.
            long_signal_confirmed = bool(entry_long_signal)
            short_signal_confirmed = bool(entry_short_signal)

            if long_signal_confirmed and not short_signal_confirmed:
                self.state.last_signal_direction = Direction.LONG
            elif short_signal_confirmed and not long_signal_confirmed:
                self.state.last_signal_direction = Direction.SHORT

            # Apply regime lock
            if self.config.trade.use_regime_lock:
                # Pine L3518-L3519: gate against lastSignalDir_tracked[1]
                if prev_signal_direction == Direction.LONG:
                    long_filtered = False
                elif prev_signal_direction == Direction.SHORT:
                    short_filtered = False

            # Edge-mode pending queue when allow_flip=False:
            # queue opposite RAW edge while position is open; the queued
            # signal must still pass current-bar filters/guards when flat.
            if self.config.trade.entry_mode == "Edge":
                if self.config.trade.allow_flip:
                    self._pending_entry_direction = None
                else:
                    if long_edge:
                        if in_position_start_bar and is_short_start_bar:
                            self._pending_entry_direction = Direction.LONG
                        elif self._pending_entry_direction == Direction.SHORT:
                            self._pending_entry_direction = None
                    if short_edge:
                        if in_position_start_bar and is_long_start_bar:
                            self._pending_entry_direction = Direction.SHORT
                        elif self._pending_entry_direction == Direction.LONG:
                            self._pending_entry_direction = None

            # Bring closed-trade dependent guard counters up to date for this bar.
            self._refresh_guard_loss_streak_from_trades(i)
            guard_allow, guard_eq_now_dbg, guard_eq_ma_dbg, guard_eq_ok_dbg, blocked_reason = (
                self._evaluate_entry_guards(
                    bar_idx=i,
                    bar=bar,
                    can_trade_window=can_trade_window,
                    in_position_for_mae=in_position_start_bar,
                    long_candidate=bool(long_filtered),
                    short_candidate=bool(short_filtered),
                    allow_recovery=not in_position_start_bar,
                )
            )

            # Per-filter block diagnostics
            blocked_long = []
            blocked_short = []
            for filter_name, (filter_long_series, filter_short_series) in filter_details.items():
                f_long = filter_long_series.iloc[i] if not pd.isna(filter_long_series.iloc[i]) else True
                f_short = filter_short_series.iloc[i] if not pd.isna(filter_short_series.iloc[i]) else True
                if not bool(f_long):
                    blocked_long.append(filter_name)
                if not bool(f_short):
                    blocked_short.append(filter_name)
            if self.config.confirmation.enabled:
                if not bool(entry_long_signal):
                    blocked_long.append("confirmation_layer")
                if not bool(entry_short_signal):
                    blocked_short.append("confirmation_layer")
            
            # Process exits first (if in position)
            # Pine parity: opposite-signal exit uses RAW signals (not filtered)
            # to prevent position lock-in when filters toggle. See CORE.pine L3584.
            exit_reason = None
            self._same_bar_exit_tp1_fill_bar = None
            self._same_bar_exit_trail_active_start = None
            self._same_bar_exit_trailing_stop = None
            self._same_bar_exit_trail_start_hit = None
            if self.state.in_position and can_trade_window:
                exit_reason = self._process_exits(
                    bar, df, i, long_filtered, short_filtered,
                    long_raw=bool(long_signal_raw),
                    short_raw=bool(short_signal_raw),
                )
            # Pine parity nuance:
            # - After a PARTIAL margin call, TV may still close the remaining leg
            #   via bar-close discretionary exits on the same bar.
            # - We therefore clear exit_reason only for partial margin-call bars.
            if self.state.in_position and exit_reason == ExitReason.MARGIN_CALL.value:
                exit_reason = None

            if self.state.in_position and can_trade_window and exit_reason is None:
                if self._should_exit_on_filter_block(
                    bar_index=i,
                    filter_details=filter_details,
                    is_long=self.state.is_long,
                ):
                    self.state.close_position(
                        exit_price=self._apply_slippage(bar["close"], not self.state.is_long),
                        exit_reason=ExitReason.FILTER_BLOCK,
                        commission_pct=self.config.strategy.commission_percent,
                    )
                    exit_reason = ExitReason.FILTER_BLOCK.value

            # Time Stop (Pine parity): one gate for bar-limit + EOD/EOW.
            time_stop_active = (
                self.config.time_stop.enabled
                or self.config.time_stop.use_bars
                or self.config.time_stop.eod
                or self.config.time_stop.eow
            )
            if (self.state.in_position and can_trade_window and exit_reason is None
                    and time_stop_active):
                bars_in_pos = i - self.state.position.entry_bar
                bar_limit_met = (
                    (self.config.time_stop.enabled or self.config.time_stop.use_bars)
                    and bars_in_pos >= self.config.time_stop.bars
                )
                eod_condition = self.config.time_stop.eod and self._is_day_change(i, _ts_series_calendar)
                eow_condition = self.config.time_stop.eow and self._is_week_change(i, _ts_series_calendar)
                cond = self.config.time_stop.condition
                unrealized = self.state.position.unrealized_pnl(bar["close"])
                condition_met = (
                    cond == "Always"
                    or (cond == "Profit Only" and unrealized > 0)
                    or (cond == "Loss Only" and unrealized < 0)
                )
                if condition_met and (bar_limit_met or eod_condition or eow_condition):
                    boundary_exit = (eod_condition or eow_condition) and i > 0
                    exit_price = float(df["close"].iloc[i - 1]) if boundary_exit else float(bar["close"])
                    saved_bar_index = self.state.bar_index
                    saved_current_time = self.state.current_time
                    if boundary_exit:
                        self.state.bar_index = i - 1
                        self.state.current_time = _ts_series.iloc[i - 1] if _ts_series is not None else saved_current_time
                    try:
                        self.state.close_position(
                            exit_price=self._apply_slippage(exit_price, not self.state.is_long),
                            exit_reason=ExitReason.TIME_STOP,
                            commission_pct=self.config.strategy.commission_percent,
                        )
                    finally:
                        self.state.bar_index = saved_bar_index
                        self.state.current_time = saved_current_time
                    exit_reason = ExitReason.TIME_STOP.value

            # Pine-like guard streak refresh after this bar's closes, so entries
            # on the same bar can be blocked if a new losing close just occurred.
            if self._refresh_guard_loss_streak_from_trades(i):
                if guard_allow and self.config.guards.use_consec_loss_guard:
                    if self._guard_loss_streak >= self.config.guards.consec_loss_max:
                        guard_allow = False
                        blocked_reason = "consec_loss_guard"

            # Signal-mode multi-entry gates must use bar-start position snapshot.
            # Pine computes canOpen* with inPosition/isLong captured before
            # any close/exit requests in that bar.
            capital_exhausted = (not self.state.in_position) and self._is_capital_exhausted(float(bar["close"]))

            allow_signal_mode_entry_long = True
            allow_signal_mode_entry_short = True
            if self.config.trade.entry_mode == "Signal":
                if in_position_start_bar and is_long_start_bar:
                    if current_entries_long >= self.config.trade.signal_mode_max_entries:
                        allow_signal_mode_entry_long = False
                    elif current_entries_long > 0 and (i - last_entry_bar) < self.config.trade.signal_mode_cooldown_bars:
                        allow_signal_mode_entry_long = False
                if in_position_start_bar and is_short_start_bar:
                    if current_entries_short >= self.config.trade.signal_mode_max_entries:
                        allow_signal_mode_entry_short = False
                    elif current_entries_short > 0 and (i - last_entry_bar) < self.config.trade.signal_mode_cooldown_bars:
                        allow_signal_mode_entry_short = False

            # Final entry gates are evaluated from bar-start state (Pine parity).
            pending_long_signal = False
            pending_short_signal = False
            if self.config.trade.entry_mode == "Edge" and not self.config.trade.allow_flip and not in_position_start_bar:
                pending_long_signal = (
                    self._pending_entry_direction == Direction.LONG
                    and bool(filter_long)
                )
                pending_short_signal = (
                    self._pending_entry_direction == Direction.SHORT
                    and bool(filter_short)
                )
                if self.config.trade.use_regime_lock:
                    if prev_signal_direction == Direction.LONG:
                        pending_long_signal = False
                    elif prev_signal_direction == Direction.SHORT:
                        pending_short_signal = False

            edge_pyramid_ok_long = (
                self.config.trade.entry_mode == "Edge"
                and is_long_start_bar
                and current_entries_long < self.config.trade.max_pyramid_positions
            )
            edge_pyramid_ok_short = (
                self.config.trade.entry_mode == "Edge"
                and is_short_start_bar
                and current_entries_short < self.config.trade.max_pyramid_positions
            )

            long_edge_eff = bool(long_filtered or pending_long_signal)
            short_edge_eff = bool(short_filtered or pending_short_signal)

            # Pine parity: canOpenLong/canOpenShort are computed from bar-start
            # position state before any exit on the same bar.
            long_final = (
                long_edge_eff
                and can_trade_window
                and (not self._margin_call_lock)
                and (not capital_exhausted)
                and self.config.trade.enable_long
                and guard_allow
                and (
                    (not in_position_start_bar)
                    or (
                        self.config.trade.allow_flip
                        and self.config.trade.exit_on_opposite_signal
                        and is_short_start_bar
                    )
                    or (
                        in_position_start_bar
                        and is_long_start_bar
                        and (edge_pyramid_ok_long or allow_signal_mode_entry_long)
                    )
                )
            )
            short_final = (
                short_edge_eff
                and can_trade_window
                and (not self._margin_call_lock)
                and (not capital_exhausted)
                and self.config.trade.enable_short
                and guard_allow
                and (
                    (not in_position_start_bar)
                    or (
                        self.config.trade.allow_flip
                        and self.config.trade.exit_on_opposite_signal
                        and is_long_start_bar
                    )
                    or (
                        in_position_start_bar
                        and is_short_start_bar
                        and (edge_pyramid_ok_short or allow_signal_mode_entry_short)
                    )
                )
            )

            # ---- PHASE 5: ENTRY GATE (same-bar re-entry) ----
            # Per-bar evaluation order (Pine parity contract):
            #   1. Snapshot bar-start state (in_position, is_long, is_short)
            #   2. Process exits (SL/TP/Trail/OppSignal/FilterBlock)
            #   3. Time stop
            #   4. Signal-mode multi-entry gates
            #   5. Final entry gates + same-bar re-entry check  <-- HERE
            #   6. Process entries
            #
            # Pine parity: TradingView's process_orders_on_close=true allows
            # exit + re-entry on the SAME bar.  When a position was closed
            # during exit processing on this bar, we allow a new entry if
            # config.trade.allow_same_bar_reentry is True.
            final_long_entry = False
            final_short_entry = False

            # Detect if an exit just occurred on this bar
            in_position_after_exits = self.state.in_position
            exited_this_bar = (in_position_start_bar and not in_position_after_exits)

            # Same-bar re-entry gate (config-driven, default: allow).
            #
            # Pine parity nuance:
            # - OPP_SIGNAL can reverse on the same bar when allow_flip is ON.
            # - TIME_STOP / FILTER_BLOCK are discretionary close paths
            #   that should not auto-reopen on the same bar.
            # - TRAIL can still re-enter on the same bar in TV exports
            #   when process_orders_on_close is enabled.
            # - Intrabar SL/TP/BE exits can still allow same-bar re-entry.
            _BAR_CLOSE_EXITS_NO_REENTRY = {
                "FILTER_BLOCK", "TIME_STOP",
                "MANUAL", "EVAL_START_FLATTEN", "MARGIN CALL",
            }
            same_bar_reentry_allowed = False
            opp_signal_flip_reentry = (
                exit_reason == ExitReason.OPP_SIGNAL.value
                and self.config.trade.allow_flip
                and self.config.trade.exit_on_opposite_signal
            )
            if exited_this_bar and self.config.trade.allow_same_bar_reentry:
                if self.config.trade.same_bar_reentry_requires_exit and exit_reason is None:
                    blocked_reason = "reentry_no_exit_reason"
                elif self.config.confirmation.enabled and self.config.confirmation.gate_only_when_flat:
                    # TV parity: when confirmation is configured to operate
                    # only while flat, same-bar reopen does not occur after an
                    # exit that started the bar in-position.  Reusing the raw
                    # level signal here creates artificial churn.
                    blocked_reason = "conf_flat_no_same_bar_reentry"
                elif exit_reason == ExitReason.OPP_SIGNAL.value and not opp_signal_flip_reentry:
                    blocked_reason = "bar_close_exit_no_reentry"
                elif exit_reason in _BAR_CLOSE_EXITS_NO_REENTRY:
                    blocked_reason = "bar_close_exit_no_reentry"
                else:
                    same_bar_reentry_allowed = True
            if (
                self._confirmation is not None
                and exited_this_bar
                and self.config.confirmation.enabled
                and self.config.confirmation.gate_only_when_flat
                and not same_bar_reentry_allowed
            ):
                self._confirmation.defer_flat_event(
                    long_event=bool(long_signal_raw and not prev_long_raw),
                    short_event=bool(short_signal_raw and not prev_short_raw),
                    source_bar=i,
                )
            # When same-bar re-entry is allowed, the signal-mode entry counters
            # were computed from bar-start state (when we were still in the old
            # position).  A same-bar re-entry is a FRESH entry, not a pyramid
            # add-on, so the multi-entry quota must not block it.
            # Re-evaluate long_final/short_final WITHOUT signal-mode gate.
            if same_bar_reentry_allowed:
                (
                    same_bar_guard_allow,
                    _same_bar_guard_eq_now_dbg,
                    _same_bar_guard_eq_ma_dbg,
                    _same_bar_guard_eq_ok_dbg,
                    same_bar_guard_blocked_reason,
                ) = self._evaluate_entry_guards(
                    bar_idx=i,
                    bar=bar,
                    can_trade_window=can_trade_window,
                    in_position_for_mae=False,
                    long_candidate=bool(long_filtered),
                    short_candidate=bool(short_filtered),
                    allow_recovery=False,
                )
                long_final = (
                    can_trade_window
                    and (not self._margin_call_lock)
                    and (not capital_exhausted)
                    and long_filtered
                    and self.config.trade.enable_long
                    and same_bar_guard_allow
                )
                short_final = (
                    can_trade_window
                    and (not self._margin_call_lock)
                    and (not capital_exhausted)
                    and short_filtered
                    and self.config.trade.enable_short
                    and same_bar_guard_allow
                )
                # Pine parity: same-bar risk exits (SL/TP/BE) can reopen into
                # the opposite direction on the same bar because TradingView
                # computes current `strategy.position_size` after the exit path.
                # The no-flip rule only blocks OPP_SIGNAL reversals, which are
                # already excluded above via _BAR_CLOSE_EXITS_NO_REENTRY.
                # Reset entry counters since we're starting a fresh position
                current_entries_long = 0
                current_entries_short = 0
                # TRAIL same-bar re-entry can be reversal-only in specific TV paths.
                if exit_reason == "TRAIL":
                    if is_long_start_bar:
                        long_final = False
                    elif is_short_start_bar:
                        short_final = False
                # TV export parity nuance:
                # for TRAIL exits, same-direction same-bar re-entry can still occur
                # only when trailing was already active at the START of the bar.
                # If trailing both activates and exits on the same bar, TV does
                # not reopen immediately; the fresh entry appears on the next bar.
                if exit_reason == "TRAIL":
                    trail_was_active_start = bool(self._same_bar_exit_trail_active_start)
                    trail_start_hit = bool(self._same_bar_exit_trail_start_hit)
                    if trail_was_active_start and trail_start_hit and is_long_start_bar and bool(long_filtered):
                        long_final = (
                            can_trade_window
                            and (not self._margin_call_lock)
                            and (not capital_exhausted)
                            and self.config.trade.enable_long
                            and same_bar_guard_allow
                        )
                    elif trail_was_active_start and trail_start_hit and is_short_start_bar and bool(short_filtered):
                        short_final = (
                            can_trade_window
                            and (not self._margin_call_lock)
                            and (not capital_exhausted)
                            and self.config.trade.enable_short
                            and same_bar_guard_allow
                        )
            else:
                same_bar_guard_allow = guard_allow
                same_bar_guard_blocked_reason = blocked_reason

            # Determine can_attempt_entry
            if not in_position_start_bar:
                # Was flat at bar start -> normal entry path
                can_attempt_entry = can_trade_window
                if not can_attempt_entry:
                    blocked_reason = "outside_trade_window"
            elif exited_this_bar and same_bar_reentry_allowed:
                # Exited this bar AND re-entry is allowed
                can_attempt_entry = can_trade_window
                if not can_attempt_entry:
                    blocked_reason = "outside_trade_window"
                elif not (long_final or short_final):
                    can_attempt_entry = False
                    if capital_exhausted:
                        blocked_reason = "capital_exhaustion"
                    elif self._margin_call_lock:
                        blocked_reason = "margin_call_lock"
                    elif not same_bar_guard_allow:
                        blocked_reason = same_bar_guard_blocked_reason or "guard_blocked_after_exit"
                    else:
                        blocked_reason = "no_signal_after_exit"
            elif in_position_start_bar and self.config.trade.entry_mode == "Signal" and not exited_this_bar:
                # In position, no exit -> pyramiding / add-on (Signal mode)
                can_attempt_entry = can_trade_window and (
                    (is_long_start_bar and long_final) or
                    (is_short_start_bar and short_final)
                )
                if not can_attempt_entry:
                    blocked_reason = "in_position_no_addon"
            else:
                # In position, no exit, Edge mode or other -> blocked
                can_attempt_entry = False
                blocked_reason = "in_position_blocked"

            # First-bar edge gate: on the first tradable eval bar, block
            # entry unless an actual edge transition occurred this bar.
            # TradingView does not enter on a level signal that was already
            # active when the backtest starts.
            if (can_attempt_entry
                    and self.config.trade.first_bar_requires_edge
                    and not self._first_eval_entry_done
                    and in_eval):
                has_edge = (
                    (bool(entry_long_signal) and not bool(prev_entry_long_signal))
                    or (bool(entry_short_signal) and not bool(prev_entry_short_signal))
                )
                if not has_edge:
                    can_attempt_entry = False
                    blocked_reason = "first_bar_no_edge"

            # Reset per-bar entry diagnostics before entry attempt.
            self._last_entry_diag = {}
            if can_attempt_entry:
                final_long_entry, final_short_entry = self._process_entries(
                    bar,
                    df,
                    i,
                    long_final,
                    short_final,
                    bar_start_risk_equity=bar_start_risk_equity,
                )
                if final_long_entry or final_short_entry:
                    self._first_eval_entry_done = True
                    if (not in_position_start_bar) or exited_this_bar:
                        self._daily_entry_count += 1
                        self._entry_attempted_prev_bar = True
                if final_long_entry:
                    current_entries_long += 1
                    if not self.state.in_position or self.state.is_long:
                        current_entries_short = 0
                    last_entry_bar = i
                    if self._pending_entry_direction == Direction.LONG:
                        self._pending_entry_direction = None
                if final_short_entry:
                    current_entries_short += 1
                    if not self.state.in_position or self.state.is_short:
                        current_entries_long = 0
                    last_entry_bar = i
                    if self._pending_entry_direction == Direction.SHORT:
                        self._pending_entry_direction = None
            
            # Record signals for parity/debug
            if self.config.parity.export_debug_csv:
                pos = self.state.position
                pos_qty_dbg = abs(float(pos.quantity)) if pos else 0.0
                pos_notional_dbg = pos_qty_dbg * float(bar["close"]) if pos else 0.0
                pos_equity_dbg = self._current_equity_mark_to_market(float(bar["close"])) if pos else float(self.state.balance)
                pos_margin_required_dbg = (
                    self._margin_required(pos_notional_dbg, pos.direction)
                    if pos else 0.0
                )
                pos_margin_call_dbg = self._is_margin_call(float(bar["close"])) if pos else False
                pos_margin_liq_qty_dbg = self._margin_call_liquidation_qty(float(bar["close"])) if pos else 0.0
                signal_debug_point = {}
                for key, series in signal_debug_series.items():
                    try:
                        val = series.iloc[i]
                    except Exception:
                        continue
                    signal_debug_point[f"sig_{key}"] = None if pd.isna(val) else val
                self.state.record_signal(
                    long_raw=long_signal_raw,
                    short_raw=short_signal_raw,
                    allow_long=filter_long,
                    allow_short=filter_short,
                    entry_signal_long=entry_long_signal,
                    entry_signal_short=entry_short_signal,
                    conf_waiting_long=conf_waiting_long,
                    conf_waiting_short=conf_waiting_short,
                    conf_long_level=(conf_step.long_level if self._confirmation is not None else None),
                    conf_short_level=(conf_step.short_level if self._confirmation is not None else None),
                    conf_wait_long_start_bar=(conf_step.wait_long_start_bar if self._confirmation is not None else None),
                    conf_wait_short_start_bar=(conf_step.wait_short_start_bar if self._confirmation is not None else None),
                    conf_last_swing_high=(conf_step.last_swing_high if self._confirmation is not None else None),
                    conf_last_swing_low=(conf_step.last_swing_low if self._confirmation is not None else None),
                    long_final=long_final,
                    short_final=short_final,
                    guard_allow=(same_bar_guard_allow if exited_this_bar and same_bar_reentry_allowed else guard_allow),
                    final_long_entry=final_long_entry,
                    final_short_entry=final_short_entry,
                    blocked_filters_long="|".join(blocked_long),
                    blocked_filters_short="|".join(blocked_short),
                    blocked_filters="|".join(sorted(set(blocked_long + blocked_short))),
                    exit_reason=exit_reason,
                    # --- Position state ---
                    pos_side=(
                        "LONG" if self.state.is_long else
                        ("SHORT" if self.state.is_short else "FLAT")
                    ),
                    open_legs=current_entries_long + current_entries_short,
                    entry_price=pos.entry_price if pos else None,
                    sl_price=pos.sl_price if pos else None,
                    be_triggered=pos.be_triggered if pos else False,
                    trailing_active=pos.trailing_active if pos else False,
                    pos_trailing_stop=pos.trailing_stop if pos else None,
                    pos_tp1_filled=pos.tp1_filled if pos else False,
                    pos_tp1_fill_bar=pos.tp1_fill_bar if pos else None,
                    pos_qty=pos_qty_dbg,
                    pos_notional_close=pos_notional_dbg,
                    pos_equity_close=pos_equity_dbg,
                    pos_required_margin_close=pos_margin_required_dbg,
                    pos_margin_call_close=pos_margin_call_dbg,
                    pos_margin_liq_qty_close=pos_margin_liq_qty_dbg,
                    same_bar_exit_tp1_fill_bar=self._same_bar_exit_tp1_fill_bar,
                    same_bar_exit_trail_active_start=self._same_bar_exit_trail_active_start,
                    same_bar_exit_trailing_stop=self._same_bar_exit_trailing_stop,
                    same_bar_exit_trail_start_hit=self._same_bar_exit_trail_start_hit,
                    can_trade=can_trade_window,
                    # --- STEP 1: Same-bar re-entry debug columns ---
                    in_position_start_bar=in_position_start_bar,
                    in_position_after_exits=in_position_after_exits,
                    exit_fired=exited_this_bar,
                    exited_this_bar=exited_this_bar,
                    can_attempt_entry=can_attempt_entry,
                    same_bar_reentry_allowed=same_bar_reentry_allowed,
                    capital_exhausted=capital_exhausted,
                    margin_call_lock=self._margin_call_lock,
                    blocked_reason=blocked_reason,
                    entry_diag_reason=self._last_entry_diag.get("entry_diag_reason", ""),
                    entry_diag_direction=self._last_entry_diag.get("entry_diag_direction", ""),
                    entry_diag_qty=self._last_entry_diag.get("entry_diag_qty", 0.0),
                    entry_diag_post_notional=self._last_entry_diag.get("entry_diag_post_notional", 0.0),
                    entry_diag_equity_now=self._last_entry_diag.get("entry_diag_equity_now", 0.0),
                    entry_diag_margin_required=self._last_entry_diag.get("entry_diag_margin_required", 0.0),
                    guard_eq_now=guard_eq_now_dbg,
                    guard_eq_ma=guard_eq_ma_dbg,
                    guard_eq_ok=guard_eq_ok_dbg,
                    in_preroll=in_preroll,
                    in_eval=in_eval,
                    **signal_debug_point,
                )
            prev_entry_long_signal = bool(entry_long_signal)
            prev_entry_short_signal = bool(entry_short_signal)
            
            # Update equity exactly once per bar.
            # In-position bars include unrealized PnL; flat bars use realized balance.
            if self.state.in_position:
                unrealized = self.state.position.unrealized_pnl(float(bar["close"]))
                self.state.update_equity(self.state.balance + unrealized)
            else:
                self.state.update_equity(self.state.balance)
            
            if progress_callback and i % 100 == 0:
                progress_callback(i, len(df))
        
        _loop_time = time.perf_counter() - _t_loop
        
        # Close any open position at end.
        #
        # Current TV exports used for parity include a terminal MANUAL close
        # at evaluation-window end, so parity mode enforces this behavior.
        close_open_at_end_eff = (
            self.config.strategy.close_open_at_end
            or (
                self.config.parity.enabled
                and self.config.parity.force_terminal_manual_close
                and eval_end_ts is not None
            )
        )
        if self.state.in_position and close_open_at_end_eff:
            self.state.close_position(
                exit_price=df['close'].iloc[-1],
                exit_reason=ExitReason.MANUAL,
                commission_pct=self.config.strategy.commission_percent,
            )
        
        runtime = time.time() - start_time

        trades_eval = self._filter_trades_for_eval_window(
            self.state.trades,
            eval_start=eval_start_ts,
            eval_end=eval_end_ts,
        )
        
        # Compile results
        results = {
            'metrics': self.state.get_metrics(trades=trades_eval),
            'trades': trades_eval,
            'trades_all': self.state.trades,
            'equity_curve': self.state.equity_curve,
            'drawdown_curve': self.state.drawdown_curve,
            'signal_history': self.state.signal_history,
            'runtime_seconds': runtime,
            'bar_count': len(df),
            'warmup_bars': resolved_warmup,
            'eval_start': eval_start_ts,
            'eval_end': eval_end_ts,
        }
        
        if self.config.parity.export_debug_csv:
            _t_export = time.perf_counter()
            results['debug_exports'] = self._export_debug_csv(
                export_trades=results['trades'],
                eval_start=eval_start_ts,
                eval_end=eval_end_ts,
            )
            _export_time = time.perf_counter() - _t_export
        else:
            _export_time = 0.0
        
        # Print profiling timers
        print(f"\n{'='*50}")
        print(f"PERFORMANCE PROFILING")
        print(f"{'='*50}")
        print(f"PRECOMPUTE_TIME = {_precompute_time:.3f} sec")
        print(f"MAIN_LOOP_TIME  = {_loop_time:.3f} sec")
        print(f"DEBUG_EXPORT_TIME = {_export_time:.3f} sec")
        print(f"TOTAL_TIME      = {runtime:.3f} sec")
        print(f"{'='*50}\n")
        
        logger.info(
            "Backtest complete in %.2fs: total_trades=%d eval_trades=%d",
            runtime,
            len(self.state.trades),
            len(results['trades']),
        )
        
        return results
    
    def _trade_overlaps_eval_window(
        self,
        trade: Trade,
        eval_start: Optional[pd.Timestamp],
        eval_end: Optional[pd.Timestamp],
    ) -> bool:
        """Return True if trade interval overlaps evaluation window."""
        if trade.entry_time is None or trade.exit_time is None:
            return False
        t0 = pd.Timestamp(trade.entry_time)
        t1 = pd.Timestamp(trade.exit_time)
        t0 = t0.tz_localize("UTC") if t0.tzinfo is None else t0.tz_convert("UTC")
        t1 = t1.tz_localize("UTC") if t1.tzinfo is None else t1.tz_convert("UTC")
        if eval_start is not None and t1 < eval_start:
            return False
        if eval_end is not None and t0 > eval_end:
            return False
        return True

    def _filter_trades_for_eval_window(
        self,
        trades: list[Trade],
        eval_start: Optional[pd.Timestamp],
        eval_end: Optional[pd.Timestamp],
    ) -> list[Trade]:
        """Filter trades by overlap with evaluation window."""
        if eval_start is None and eval_end is None:
            return trades
        return [t for t in trades if self._trade_overlaps_eval_window(t, eval_start, eval_end)]

    def _export_debug_csv(
        self,
        export_trades: Optional[list[Trade]] = None,
        eval_start: Optional[pd.Timestamp] = None,
        eval_end: Optional[pd.Timestamp] = None,
    ) -> Dict[str, str]:
        """
        Export deterministic parity debug CSVs with unique timestamps and robust retry logic.
        
        Returns:
            Dict with exported file paths.
        """
        import uuid
        from datetime import datetime
        debug_dir = Path(self.config.parity.debug_dir)
        try:
            debug_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to create debug directory {debug_dir}: {e}")
            return {}
        
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        short_id = str(uuid.uuid4())[:8]
        trades_filename = f"debug_python_trades_{timestamp_str}_{short_id}.csv"
        signals_filename = f"debug_python_signals_{timestamp_str}_{short_id}.csv"
        
        trades_path = debug_dir / trades_filename
        signals_path = debug_dir / signals_filename
        
        trade_source = export_trades if export_trades is not None else self.state.trades
        
        def _safe_write_csv(df: pd.DataFrame, path: Path) -> str:
            try:
                df.to_csv(path, index=False)
                return str(path)
            except PermissionError:
                logger.warning(f"Permission denied for {path}. Retrying with suffix...")
                retry_path = path.with_name(f"{path.stem}_retry1{path.suffix}")
                try:
                    df.to_csv(retry_path, index=False)
                    return str(retry_path)
                except Exception as e:
                    logger.error(f"Failed to write debug CSV to {retry_path} after retry: {e}")
                    return f"FAILED: {path.name}"
            except Exception as e:
                logger.error(f"Failed to write debug CSV to {path}: {e}")
                return f"FAILED: {path.name}"

        # Trade-level export
        trade_rows = []
        for t in trade_source:
            trade_rows.append({
                "timestamp": t.entry_time,
                "entry_timestamp": t.entry_time,
                "exit_timestamp": t.exit_time,
                "side": t.direction.value.upper() if hasattr(t.direction, "value") else str(t.direction),
                "entry_price": t.entry_price,
                "exit_price": t.exit_price,
                "qty": t.quantity,
                "pnl": t.pnl,
                "pnl_pct": t.pnl_pct,
                "reason": t.exit_reason.value if hasattr(t.exit_reason, "value") else str(t.exit_reason),
                "bar_index": t.entry_bar,
                "exit_bar_index": t.exit_bar,
            })
        
        start_time_trades = datetime.now()
        exported_trades_path = _safe_write_csv(pd.DataFrame(trade_rows), trades_path)
        
        # Signal-level export
        signal_rows = []
        base_signal_cols = [
            "timestamp",
            "bar_index",
            "longSignal_raw",
            "shortSignal_raw",
            "allowLong",
            "allowShort",
            "guardAllow",
            "longSignal",
            "shortSignal",
            "finalLongEntry",
            "finalShortEntry",
            "blockedFilters",
            "blockedFiltersLong",
            "blockedFiltersShort",
            "exitReason",
            "pos_side",
            "open_legs",
            "entry_price",
            "sl_price",
            "be_triggered",
            "trailing_active",
            "pos_trailing_stop",
            "same_bar_exit_trailing_stop",
            "same_bar_exit_trail_start_hit",
            "can_trade",
            "in_position_start_bar",
            "in_position_after_exits",
            "exit_fired",
            "exited_this_bar",
            "can_attempt_entry",
            "same_bar_reentry_allowed",
            "blocked_reason",
            "entry_diag_reason",
            "entry_diag_direction",
            "entry_diag_qty",
            "entry_diag_post_notional",
            "entry_diag_equity_now",
            "entry_diag_margin_required",
            "guard_eq_now",
            "guard_eq_ma",
            "guard_eq_ok",
            "in_preroll",
            "in_eval",
        ]
        extra_signal_keys = []
        for s in self.state.signal_history:
            for key in s.keys():
                if key in {
                    "timestamp",
                    "bar_index",
                    "long_signal_raw",
                    "short_signal_raw",
                    "allow_long",
                    "allow_short",
                    "guard_allow",
                    "long_signal",
                    "short_signal",
                    "final_long_entry",
                    "final_short_entry",
                    "blocked_filters",
                    "blocked_filters_long",
                    "blocked_filters_short",
                    "exit_reason",
                }:
                    continue
                if key not in {
                    "pos_side",
                    "open_legs",
                    "entry_price",
                    "sl_price",
                    "be_triggered",
                    "trailing_active",
                    "pos_trailing_stop",
                    "same_bar_exit_trailing_stop",
                    "same_bar_exit_trail_start_hit",
                    "can_trade",
                    "in_position_start_bar",
                    "in_position_after_exits",
                    "exit_fired",
                    "exited_this_bar",
                    "can_attempt_entry",
                    "same_bar_reentry_allowed",
                    "blocked_reason",
                    "entry_diag_reason",
                    "entry_diag_direction",
                    "entry_diag_qty",
                    "entry_diag_post_notional",
                    "entry_diag_equity_now",
                    "entry_diag_margin_required",
                    "guard_eq_now",
                    "guard_eq_ma",
                    "guard_eq_ok",
                    "in_preroll",
                    "in_eval",
                } and key not in extra_signal_keys:
                    extra_signal_keys.append(key)

        for s in self.state.signal_history:
            ts = s.get("timestamp")
            if ts is not None:
                ts_utc = pd.Timestamp(ts)
                ts_utc = ts_utc.tz_localize("UTC") if ts_utc.tzinfo is None else ts_utc.tz_convert("UTC")
                if eval_start is not None and ts_utc < eval_start:
                    continue
                if eval_end is not None and ts_utc > eval_end:
                    continue
            row = {
                "timestamp": s.get("timestamp"),
                "bar_index": s.get("bar_index"),
                "longSignal_raw": s.get("long_signal_raw", False),
                "shortSignal_raw": s.get("short_signal_raw", False),
                "allowLong": s.get("allow_long", True),
                "allowShort": s.get("allow_short", True),
                "guardAllow": s.get("guard_allow", True),
                "longSignal": s.get("long_signal", False),
                "shortSignal": s.get("short_signal", False),
                "finalLongEntry": s.get("final_long_entry", False),
                "finalShortEntry": s.get("final_short_entry", False),
                "blockedFilters": s.get("blocked_filters", ""),
                "blockedFiltersLong": s.get("blocked_filters_long", ""),
                "blockedFiltersShort": s.get("blocked_filters_short", ""),
                "exitReason": s.get("exit_reason"),
                # Position state columns
                "pos_side": s.get("pos_side", "FLAT"),
                "open_legs": s.get("open_legs", 0),
                "entry_price": s.get("entry_price"),
                "sl_price": s.get("sl_price"),
                "be_triggered": s.get("be_triggered", False),
                "trailing_active": s.get("trailing_active", False),
                "pos_trailing_stop": s.get("pos_trailing_stop"),
                "same_bar_exit_trailing_stop": s.get("same_bar_exit_trailing_stop"),
                "same_bar_exit_trail_start_hit": s.get("same_bar_exit_trail_start_hit"),
                "can_trade": s.get("can_trade", True),
                # Same-bar re-entry debug columns
                "in_position_start_bar": s.get("in_position_start_bar", False),
                "in_position_after_exits": s.get("in_position_after_exits", False),
                "exit_fired": s.get("exit_fired", False),
                "exited_this_bar": s.get("exited_this_bar", False),
                "can_attempt_entry": s.get("can_attempt_entry", False),
                "same_bar_reentry_allowed": s.get("same_bar_reentry_allowed", False),
                "blocked_reason": s.get("blocked_reason", ""),
                # Entry diagnostics (attempted-entry bars)
                "entry_diag_reason": s.get("entry_diag_reason", ""),
                "entry_diag_direction": s.get("entry_diag_direction", ""),
                "entry_diag_qty": s.get("entry_diag_qty", 0.0),
                "entry_diag_post_notional": s.get("entry_diag_post_notional", 0.0),
                "entry_diag_equity_now": s.get("entry_diag_equity_now", 0.0),
                "entry_diag_margin_required": s.get("entry_diag_margin_required", 0.0),
                "guard_eq_now": s.get("guard_eq_now"),
                "guard_eq_ma": s.get("guard_eq_ma"),
                "guard_eq_ok": s.get("guard_eq_ok"),
                # Preroll / eval window debug columns
                "in_preroll": s.get("in_preroll", False),
                "in_eval": s.get("in_eval", True),
            }
            for key in extra_signal_keys:
                row[key] = s.get(key)
            signal_rows.append(row)

        signal_df = pd.DataFrame(signal_rows)
        ordered_cols = [c for c in base_signal_cols if c in signal_df.columns] + [
            c for c in extra_signal_keys if c in signal_df.columns
        ]
        signal_df = signal_df.reindex(columns=ordered_cols)
        exported_signals_path = _safe_write_csv(signal_df, signals_path)
        
        logger.info(f"Debug parity CSV exported to {debug_dir} (Trades: {len(trade_rows)}, Signals: {len(signal_rows)})")
        return {
            "debug_python_trades": exported_trades_path,
            "debug_python_signals": exported_signals_path,
        }
    
    def _process_exits(
        self,
        bar: Dict,
        df: pd.DataFrame,
        bar_idx: int,
        long_signal: bool,
        short_signal: bool,
        long_raw: bool = False,
        short_raw: bool = False,
    ) -> Optional[str]:
        """
        Process exits using deterministic fill contract matching TradingView.

        ===================================================================
        FILL CONTRACT (Pine Parity)
        ===================================================================
        TradingView's strategy engine processes orders in two categories:

        A) INTRABAR ORDERS — strategy.exit(stop=X, limit=Y)
           - SL/TP are standing stop/limit orders
           - Checked against current bar's OHLC (touch: H/L, close: C)
           - Fill at the EXACT stop/limit price (+ slippage)
           - When SL and TP both hit same bar, _tv_high_first() determines
             intrabar path: open -> nearest extreme -> other extreme -> close

        B) BAR-CLOSE ORDERS — strategy.close()
           - OPP_SIGNAL, FILTER_BLOCK, TRAIL, TIME_STOP
           - Fill at bar close price (+ slippage)

        ===================================================================
        EVALUATION ORDER (per bar)
        ===================================================================
        1) Update position extremes (highest/lowest for trailing)
        2) SL/TP intrabar conflict detection (both touched this bar?)
        3) SL check — fill at SL price; deferred if TP reached first
        4) TP checks — TP1 (partial), then TP2/single; fill at TP price
        5) Deferred SL — after TP partial, close remaining at SL price
        6) OPP_SIGNAL exit (bar close, uses RAW signals - Pine L3583)
        7) BE update — move SL to breakeven (for NEXT bar's SL check)
        8) Trail activation + trail stop recompute (for NEXT bar)
        9) Trail exit check — fill at bar close (strategy.close)

        Notes:
        - Steps 7-8 update levels for the NEXT bar. They do NOT affect
          the SL/TP checks on the CURRENT bar (steps 3-5).
        - Trail exit (step 9) uses the trail stop computed THIS bar
          (after extreme update in step 1), matching Pine L4238.
        - TP1 is a partial close; if position remains open, steps 6-9
          continue evaluating the remaining leg.
        ===================================================================
        """
        pos = self.state.position
        if not pos:
            return None

        is_long = pos.is_long()
        trail_active_start = bool(pos.trailing_active)
        trail_stop_start = float(pos.trailing_stop) if (trail_active_start and pos.trailing_stop is not None) else None
        current_price = bar['close']
        high = bar['high']
        low = bar['low']
        side = "long" if is_long else "short"

        # Update position extremes
        pos.update_extremes(high, low)

        # Pine parity exit priority (matches CORE.pine closeRequestedThisBar guard):
        # 1) OPP_SIGNAL (strategy.close at close, uses RAW signals - Pine L3583)
        # 2) FILTER_BLOCK (strategy.close at close - Pine L3625)
        # 3) TIME_STOP (strategy.close at close - Pine L3712)
        # 4) SL/TP (strategy.exit stop/limit - processed by TV engine)
        # 5) TRAIL (strategy.close at close - Pine L4238)
        # 6) BE (strategy.exit update - Pine L4169)

        close_requested = False

        # PRIORITY FIX: SL/TP (Intrabar) must be checked BEFORE Bar-Close exits (OPP/TRAIL)
        high_first = self._tv_high_first(bar)
        tp_first_if_conflict = (is_long and high_first) or ((not is_long) and (not high_first))
        sl_deferred = False

        # Detect SL/TP same-bar conflict for intrabar sequencing.
        sl_hit = False
        if pos.sl_price and self.config.stop_loss.enabled:
            sl_hit = self._long_stop_hit(low, current_price, pos.sl_price) if is_long else self._short_stop_hit(high, current_price, pos.sl_price)

        tp_any_hit_for_conflict = False
        if self.config.take_profit.enabled:
            if self.config.multi_tp.enabled and (not pos.tp1_filled) and (pos.tp1_price is not None):
                tp_any_hit_for_conflict = self._long_tp_hit(high, current_price, pos.tp1_price) if is_long else self._short_tp_hit(low, current_price, pos.tp1_price)
            else:
                tp_conf_price = pos.tp2_price if pos.tp1_filled else pos.tp_price
                if tp_conf_price is not None:
                    tp_any_hit_for_conflict = self._long_tp_hit(high, current_price, tp_conf_price) if is_long else self._short_tp_hit(low, current_price, tp_conf_price)

        # 1) Static stop-loss hit (strategy.exit stop order - fills at SL price)
        if pos.sl_price and self.config.stop_loss.enabled and sl_hit:
            if tp_any_hit_for_conflict and tp_first_if_conflict:
                # Defer SL after TP processing when intrabar path reaches TP side first.
                sl_deferred = True
            elif is_long:
                sl_fill = self._apply_slippage(pos.sl_price, False)  # Sell
                stop_reason = self._stop_reason_for_position(pos)
                # Pine parity: with Multi-TP ON, TP1/TP2 bracket exits each carry stop.
                # A stop hit can therefore realize two closed trades (TP1 leg + remainder).
                if (
                    self.config.take_profit.enabled
                    and self.config.multi_tp.enabled
                    and not pos.tp1_filled
                    and pos.tp1_price is not None
                    and pos.tp2_price is not None
                ):
                    leg1_qty = min(pos.quantity, pos.initial_quantity * (self.tp_calc.tp1_pct / 100.0))
                    leg2_qty = max(0.0, pos.quantity - leg1_qty)
                    if leg1_qty > 0:
                        self.state.close_position(
                            exit_price=sl_fill,
                            exit_reason=stop_reason,
                            quantity=leg1_qty,
                            commission_pct=self.config.strategy.commission_percent,
                        )
                    if leg2_qty > 0 and self.state.in_position:
                        self.state.close_position(
                            exit_price=sl_fill,
                            exit_reason=stop_reason,
                            quantity=leg2_qty,
                            commission_pct=self.config.strategy.commission_percent,
                        )
                else:
                    self.state.close_position(
                        exit_price=sl_fill,
                        exit_reason=stop_reason,
                        commission_pct=self.config.strategy.commission_percent,
                    )
                return stop_reason.value
            else:
                sl_fill = self._apply_slippage(pos.sl_price, True)  # Buy
                stop_reason = self._stop_reason_for_position(pos)
                if (
                    self.config.take_profit.enabled
                    and self.config.multi_tp.enabled
                    and not pos.tp1_filled
                    and pos.tp1_price is not None
                    and pos.tp2_price is not None
                ):
                    leg1_qty = min(pos.quantity, pos.initial_quantity * (self.tp_calc.tp1_pct / 100.0))
                    leg2_qty = max(0.0, pos.quantity - leg1_qty)
                    if leg1_qty > 0:
                        self.state.close_position(
                            exit_price=sl_fill,
                            exit_reason=stop_reason,
                            quantity=leg1_qty,
                            commission_pct=self.config.strategy.commission_percent,
                        )
                    if leg2_qty > 0 and self.state.in_position:
                        self.state.close_position(
                            exit_price=sl_fill,
                            exit_reason=stop_reason,
                            quantity=leg2_qty,
                            commission_pct=self.config.strategy.commission_percent,
                        )
                else:
                    self.state.close_position(
                        exit_price=sl_fill,
                        exit_reason=stop_reason,
                        commission_pct=self.config.strategy.commission_percent,
                    )
                return stop_reason.value

        # 2) Take-profit checks (strategy.exit limit order - fills at TP price)
        tp1_hit_this_bar = False
        partial_exit_reason: Optional[str] = None
        if not pos.tp1_filled and pos.tp1_price and self.config.multi_tp.enabled:
            if is_long and self._long_tp_hit(high, current_price, pos.tp1_price):
                close_qty = pos.initial_quantity * (self.tp_calc.tp1_pct / 100)
                self.state.close_position(
                    exit_price=self._apply_slippage(pos.tp1_price, False),
                    exit_reason=ExitReason.TP1,
                    quantity=close_qty,
                    commission_pct=self.config.strategy.commission_percent,
                )
                pos.tp1_filled = True
                pos.tp1_fill_bar = bar_idx
                tp1_hit_this_bar = True
                partial_exit_reason = ExitReason.TP1.value
            if (not is_long) and self._short_tp_hit(low, current_price, pos.tp1_price):
                close_qty = pos.initial_quantity * (self.tp_calc.tp1_pct / 100)
                self.state.close_position(
                    exit_price=self._apply_slippage(pos.tp1_price, True),
                    exit_reason=ExitReason.TP1,
                    quantity=close_qty,
                    commission_pct=self.config.strategy.commission_percent,
                )
                pos.tp1_filled = True
                pos.tp1_fill_bar = bar_idx
                tp1_hit_this_bar = True
                partial_exit_reason = ExitReason.TP1.value

        tp_price = pos.tp2_price if pos.tp1_filled else pos.tp_price
        if tp_price and self.config.take_profit.enabled:
            if is_long and self._long_tp_hit(high, current_price, tp_price):
                self.state.close_position(
                    exit_price=self._apply_slippage(tp_price, False),
                    exit_reason=ExitReason.TP2 if pos.tp1_filled else ExitReason.TP,
                    commission_pct=self.config.strategy.commission_percent,
                )
                return ExitReason.TP2.value if pos.tp1_filled else ExitReason.TP.value
            if (not is_long) and self._short_tp_hit(low, current_price, tp_price):
                self.state.close_position(
                    exit_price=self._apply_slippage(tp_price, True),
                    exit_reason=ExitReason.TP2 if pos.tp1_filled else ExitReason.TP,
                    commission_pct=self.config.strategy.commission_percent,
                )
                return ExitReason.TP2.value if pos.tp1_filled else ExitReason.TP.value

        # Deferred SL handling:
        # when TP side is reached first on this bar, apply stop to remaining size
        # only if position is still open after TP processing.
        if sl_deferred and self.state.in_position and pos.sl_price and self.config.stop_loss.enabled:
            stop_reason = self._stop_reason_for_position(pos)
            sl_fill = self._apply_slippage(pos.sl_price, not is_long)
            self.state.close_position(
                exit_price=sl_fill,
                exit_reason=stop_reason,
                commission_pct=self.config.strategy.commission_percent,
            )
            return stop_reason.value

        # Do not return early on TP1 partial fills.
        # Pine keeps evaluating the remaining position on the same bar
        # (e.g., TP1 + TRAIL can happen within one candle).
        if tp1_hit_this_bar and not self.state.in_position:
            return ExitReason.TP1.value

        # 3) Margin call (TV-like partial liquidation).
        #
        # Pine broker emulator can trigger margin call intrabar (first point where
        # equity <= required margin), not only at close. In touch mode, probe the
        # intrabar path and use the first trigger price; otherwise use bar close.
        margin_mark_price = current_price
        if self.config.parity.fill_contract == "touch":
            o = float(bar["open"])
            h = float(high)
            l = float(low)
            c = float(current_price)
            if high_first:
                intrabar_path = (o, h, l, c)
            else:
                intrabar_path = (o, l, h, c)
            for px_probe in intrabar_path:
                if self._is_margin_call(px_probe):
                    margin_mark_price = px_probe
                    break

        margin_liq_qty = self._margin_call_liquidation_qty(margin_mark_price)
        if margin_liq_qty > 0:
            self._margin_call_lock = True
            # TradingView broker emulator liquidates only the computed margin-call
            # quantity (can be partial). Remaining size may continue and be closed
            # by other exit paths on the same/later bars.
            close_qty = margin_liq_qty
            self.state.close_position(
                exit_price=self._apply_slippage(margin_mark_price, not is_long),
                exit_reason=ExitReason.MARGIN_CALL,
                quantity=close_qty,
                commission_pct=self.config.strategy.commission_percent,
            )
            if not self.state.in_position:
                return ExitReason.MARGIN_CALL.value
            # Partial margin call: keep evaluating this bar so TIME_STOP / OPP_SIGNAL
            # can close the remaining leg, matching TV's multi-exit behavior.
            partial_exit_reason = ExitReason.MARGIN_CALL.value

        # 4) Opposite-signal exits (uses RAW signals for parity - Pine L3583-3616)
        # Executed at Bar Close (market order)
        if self.config.trade.exit_on_opposite_signal and not close_requested:
            if is_long and short_raw:
                self.state.close_position(
                    exit_price=self._apply_slippage(current_price, False),
                    exit_reason=ExitReason.OPP_SIGNAL,
                    commission_pct=self.config.strategy.commission_percent,
                )
                return ExitReason.OPP_SIGNAL.value
            if (not is_long) and long_raw:
                self.state.close_position(
                    exit_price=self._apply_slippage(current_price, True),
                    exit_reason=ExitReason.OPP_SIGNAL,
                    commission_pct=self.config.strategy.commission_percent,
                )
                return ExitReason.OPP_SIGNAL.value

        # 5) Break-even updates (Pine order: BE block runs before trailing block)
        # Pine gate is `if ... and not trailActive` where `trailActive` is previous state.
        be_armed_this_bar = False
        if not pos.be_triggered and self.be_calc.enabled and not pos.trailing_active:
            if self.be_calc.should_trigger(
                pos.entry_price, pos.sl_base_price or pos.sl_price,
                high if is_long else low, side,
            ):
                pos.be_triggered = True
                pos.sl_price = self.be_calc.calculate_be_price(
                    pos.entry_price,
                    pos.sl_base_price or pos.sl_price, side,
                )
                be_armed_this_bar = True

        # 6) Trailing updates (activation + stop recompute)
        if self.trail_calc.enabled and not pos.trailing_active:
            if self.trail_calc.should_activate(
                pos.entry_price, pos.sl_base_price or pos.sl_price,
                high if is_long else low, side,
            ):
                pos.trailing_active = True

        if pos.trailing_active:
            pos.trailing_stop = self.trail_calc.calculate_trailing_stop(
                pos.entry_price,
                pos.sl_base_price or pos.sl_price,
                pos.highest_price, pos.lowest_price, side,
            )

        # 7) Trailing stop exit check (Pine L4238: strategy.close at close price)
        if pos.trailing_active and pos.trailing_stop and not close_requested:
            if is_long and self._long_stop_hit(low, current_price, pos.trailing_stop):
                start_stop_hit = (
                    trail_stop_start is not None
                    and self._long_stop_hit(low, current_price, trail_stop_start)
                )
                trail_fill = self._apply_slippage(current_price, False)
                self._same_bar_exit_tp1_fill_bar = pos.tp1_fill_bar
                self._same_bar_exit_trail_active_start = trail_active_start
                self._same_bar_exit_trailing_stop = float(pos.trailing_stop)
                self._same_bar_exit_trail_start_hit = bool(start_stop_hit)
                if (
                    self.config.take_profit.enabled
                    and self.config.multi_tp.enabled
                    and not pos.tp1_filled
                    and pos.tp1_price is not None
                    and pos.tp2_price is not None
                ):
                    leg1_qty = min(pos.quantity, pos.initial_quantity * (self.tp_calc.tp1_pct / 100.0))
                    leg2_qty = max(0.0, pos.quantity - leg1_qty)
                    if leg1_qty > 0:
                        self.state.close_position(
                            exit_price=trail_fill,
                            exit_reason=ExitReason.TRAIL,
                            quantity=leg1_qty,
                            commission_pct=self.config.strategy.commission_percent,
                        )
                    if leg2_qty > 0 and self.state.in_position:
                        self.state.close_position(
                            exit_price=trail_fill,
                            exit_reason=ExitReason.TRAIL,
                            quantity=leg2_qty,
                            commission_pct=self.config.strategy.commission_percent,
                        )
                else:
                    self.state.close_position(
                        exit_price=trail_fill,
                        exit_reason=ExitReason.TRAIL,
                        commission_pct=self.config.strategy.commission_percent,
                    )
                return ExitReason.TRAIL.value
            if (not is_long) and self._short_stop_hit(high, current_price, pos.trailing_stop):
                start_stop_hit = (
                    trail_stop_start is not None
                    and self._short_stop_hit(high, current_price, trail_stop_start)
                )
                trail_fill = self._apply_slippage(current_price, True)
                self._same_bar_exit_tp1_fill_bar = pos.tp1_fill_bar
                self._same_bar_exit_trail_active_start = trail_active_start
                self._same_bar_exit_trailing_stop = float(pos.trailing_stop)
                self._same_bar_exit_trail_start_hit = bool(start_stop_hit)
                if (
                    self.config.take_profit.enabled
                    and self.config.multi_tp.enabled
                    and not pos.tp1_filled
                    and pos.tp1_price is not None
                    and pos.tp2_price is not None
                ):
                    leg1_qty = min(pos.quantity, pos.initial_quantity * (self.tp_calc.tp1_pct / 100.0))
                    leg2_qty = max(0.0, pos.quantity - leg1_qty)
                    if leg1_qty > 0:
                        self.state.close_position(
                            exit_price=trail_fill,
                            exit_reason=ExitReason.TRAIL,
                            quantity=leg1_qty,
                            commission_pct=self.config.strategy.commission_percent,
                        )
                    if leg2_qty > 0 and self.state.in_position:
                        self.state.close_position(
                            exit_price=trail_fill,
                            exit_reason=ExitReason.TRAIL,
                            quantity=leg2_qty,
                            commission_pct=self.config.strategy.commission_percent,
                        )
                else:
                    self.state.close_position(
                        exit_price=trail_fill,
                        exit_reason=ExitReason.TRAIL,
                        commission_pct=self.config.strategy.commission_percent,
                    )
                return ExitReason.TRAIL.value

        return partial_exit_reason
    
    def _process_entries(
        self,
        bar: Dict,
        df: pd.DataFrame,
        bar_idx: int,
        long_signal: bool,
        short_signal: bool,
        bar_start_risk_equity: Optional[float] = None,
    ) -> Tuple[bool, bool]:
        """Process entry signals."""
        entry_price = bar['close']
        direction = None
        self._last_entry_diag = {
            "entry_diag_direction": "",
            "entry_diag_qty": 0.0,
            "entry_diag_post_notional": 0.0,
            "entry_diag_equity_now": 0.0,
            "entry_diag_margin_required": 0.0,
            "entry_diag_reason": "",
        }
        
        if long_signal:
            direction = Direction.LONG
        elif short_signal:
            direction = Direction.SHORT
        else:
            self._last_entry_diag["entry_diag_reason"] = "no_direction_signal"
            return False, False
        self._last_entry_diag["entry_diag_direction"] = direction.value

        # In signal-mode multi-entry, only same-direction add-ons are allowed.
        if self.state.in_position:
            if (direction == Direction.LONG and not self.state.is_long) or (direction == Direction.SHORT and not self.state.is_short):
                self._last_entry_diag["entry_diag_reason"] = "opposite_in_position"
                return False, False
        
        # Calculate SL
        sl_price = None
        if self.config.stop_loss.enabled:
            sl_price = self.sl_calc.calculate(
                df, bar_idx,
                "long" if direction == Direction.LONG else "short",
                entry_price,
                atr_cache=self._atr_cache,
            )
        
        # Calculate TP
        tp_price = None
        tp1_price = None
        tp2_price = None
        
        if self.config.take_profit.enabled:
            if self.config.multi_tp.enabled:
                tp1_price, tp2_price, _ = self.tp_calc.calculate_multi(
                    df, bar_idx,
                    "long" if direction == Direction.LONG else "short",
                    entry_price, sl_price,
                    atr_cache=self._atr_cache,
                )
            else:
                tp_price = self.tp_calc.calculate(
                    df, bar_idx,
                    "long" if direction == Direction.LONG else "short",
                    entry_price, sl_price,
                    atr_cache=self._atr_cache,
                )
        
        # Calculate position size
        risk_equity = (
            bar_start_risk_equity
            if bar_start_risk_equity is not None
            else (
                self.state.initial_capital
                if self.config.risk.risk_equity_mode == "Initial"
                else self.state.balance
            )
        )
        risk_equity = max(0.0, float(risk_equity))

        if sl_price:
            quantity = self.sizer.calculate(
                risk_equity,
                entry_price,
                sl_price,
                "long" if direction == Direction.LONG else "short"
            )
        else:
            risk_pct_dir = (
                self.config.risk.risk_long_percent
                if direction == Direction.LONG
                else self.config.risk.risk_short_percent
            )
            quantity = self.sizer.calculate_fallback(
                risk_equity,
                entry_price,
                self.config.risk.fallback_qty_pct,
                risk_pct=risk_pct_dir,
            )

        # Pine parity: aggregate notional cap is applied to TOTAL same-direction exposure.
        # Enforce remaining notional room after existing position notional.
        entry_safe = max(float(entry_price), self.mintick)
        same_dir_open = self.state.in_position and (
            (direction == Direction.LONG and self.state.is_long) or
            (direction == Direction.SHORT and self.state.is_short)
        )
        pos_ref_price = self.state.position.entry_price if same_dir_open else entry_price
        open_notional = (self.state.position.quantity * pos_ref_price) if same_dir_open else 0.0
        max_notional = risk_equity * self.config.risk.max_leverage_cap
        remaining_notional = max(0.0, max_notional - open_notional)
        max_qty_by_remaining = remaining_notional / entry_safe
        quantity = min(quantity, max_qty_by_remaining)

        if self.config.risk.use_notional_hard_assert and quantity > 0:
            post_total_notional = open_notional + (quantity * entry_safe)
            assert_eps = self.mintick * entry_safe
            if post_total_notional > max_notional + assert_eps:
                quantity = 0.0

        # TradingView export uses symbol contract precision; for BTC perpetual
        # parity runs here, executed quantity is effectively truncated to 6 decimals.
        quantity = self._truncate_toward_zero(quantity, 1e-6)

        if quantity <= 0:
            self._last_entry_diag["entry_diag_reason"] = "qty_non_positive"
            return False, False

        # Broker-emulator margin affordability gate (TV parity).
        # Use mark-price notional at entry bar close.
        open_qty_same_dir = self.state.position.quantity if same_dir_open else 0.0
        post_notional_mark = (open_qty_same_dir + quantity) * entry_safe
        equity_now = self._current_equity_mark_to_market(entry_price)
        margin_required = self._margin_required(post_notional_mark, direction)
        self._last_entry_diag["entry_diag_qty"] = float(quantity)
        self._last_entry_diag["entry_diag_post_notional"] = float(post_notional_mark)
        self._last_entry_diag["entry_diag_equity_now"] = float(equity_now)
        self._last_entry_diag["entry_diag_margin_required"] = float(margin_required)
        if not self._can_afford_margin(
            post_notional=post_notional_mark,
            direction=direction,
            mark_price=entry_price,
        ):
            self._last_entry_diag["entry_diag_reason"] = "margin_affordability"
            return False, False
        
        if self.state.in_position:
            # Add to existing same-direction position (aggregated average).
            pos = self.state.position
            old_qty = pos.quantity
            new_qty = self._truncate_toward_zero(old_qty + quantity, 1e-6)
            if new_qty <= 0:
                self._last_entry_diag["entry_diag_reason"] = "add_qty_non_positive"
                return False, False
            pos.entry_price = ((pos.entry_price * old_qty) + (entry_price * quantity)) / new_qty
            pos.quantity = new_qty
            pos.initial_quantity = new_qty
            # Pine parity (v2.2.0 update):
            # - Keep existing BE/trailing ownership state on same-direction add.
            # - Preserve existing TP levels unless currently NA.
            # - Keep SL monotonic (long=max, short=min) when new SL exists.
            if pos.tp_price is None:
                pos.tp_price = tp_price
            if pos.tp1_price is None:
                pos.tp1_price = tp1_price
            if pos.tp2_price is None:
                pos.tp2_price = tp2_price
            if pos.sl_base_price is None:
                pos.sl_base_price = sl_price
            if sl_price is not None:
                if pos.sl_price is None:
                    pos.sl_price = sl_price
                elif direction == Direction.LONG:
                    pos.sl_price = max(pos.sl_price, sl_price)
                else:
                    pos.sl_price = min(pos.sl_price, sl_price)
            if pos.sl_price is not None:
                pos.r_distance = abs(pos.entry_price - pos.sl_price)
            self.state.last_entry_direction = direction
            self.state.last_trade_bar = bar_idx
            self.state.entry_events += 1
            logger.debug(
                f"Added {direction.value} @ {entry_price:.2f}, "
                f"add_qty={quantity:.4f}, total_qty={new_qty:.4f}"
            )
        else:
            # Open fresh position.
            self.state.open_position(
                direction=direction,
                entry_price=self._apply_slippage(entry_price, direction == Direction.LONG),
                quantity=quantity,
                sl_price=sl_price,
                tp_price=tp_price,
                tp1_price=tp1_price,
                tp2_price=tp2_price,
            )
            logger.debug(
                f"Opened {direction.value} @ {entry_price:.2f}, "
                f"qty={quantity:.4f}, SL={f'{sl_price:.2f}' if sl_price else 'None'}"
            )
        self._last_entry_diag["entry_diag_reason"] = "entered"
        
        return direction == Direction.LONG, direction == Direction.SHORT


def run_backtest(
    df: pd.DataFrame,
    config: Optional[MTCConfig] = None,
    warmup_bars: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Convenience function to run a backtest.
    
    Args:
        df: OHLCV DataFrame
        config: MTC configuration (uses defaults if None)
        warmup_bars: Indicator warmup period
        
    Returns:
        Backtest results dict
    """
    if config is None:
        config = MTCConfig()
    
    runner = MTCRunner(config)
    return runner.run(df, warmup_bars=warmup_bars)
