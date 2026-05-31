from __future__ import annotations
from __future__ import annotations

from collections import deque
import math
from typing import Iterable

from mtc_v2.core.config import SIGNAL_MODE_RANGE_FILTER, SIGNAL_MODE_SUPERTREND, resolve_config
from mtc_v2.core.confirmation import (
    AdvancedConfirmationState,
    finalize_advanced_confirmation_signal,
    build_advanced_confirmation_state,
    snapshot_advanced_confirmation_state,
)
from mtc_v2.core.exits import (
    AtrTracker,
    PriceExitHit,
    build_working_exit_book,
    calc_sl,
    disable_active_target_exits,
    evaluate_price_exit,
    find_swing_reference,
    sync_working_exit_stops,
    update_protective_stop_owner,
)
from mtc_v2.core.gates import (
    GATE_MA_FILTER,
    GATE_MA_SLOPE_FILTER,
    GATE_MCGINLEY_FILTER,
    GATE_VOLUME_FILTER,
    GATE_ADX_FILTER,
    GATE_CHOP_FILTER,
    GATE_ATR_VOL_FLOOR,
    GATE_MACD_REGIME,
    GATE_MACD_CROSS,
    GATE_MACD_HIST,
    GATE_MACD_ZERO_DIST,
    GATE_CANDLE_PATTERN,
    GATE_LEVEL_PROXIMITY,
    GATE_HTF_TREND,
    GATE_MACD_HTF_BIAS,
    GATE_MOMENTUM_FILTER,
    GATE_SESSION,
    evaluate_ma_filter,
    evaluate_ma_slope_filter,
    evaluate_mcginley_filter,
    evaluate_volume_filter,
    evaluate_adx_filter,
    evaluate_chop_filter,
    evaluate_atr_vol_floor,
    evaluate_macd_regime,
    evaluate_macd_cross,
    evaluate_macd_hist,
    evaluate_macd_zero_dist,
    evaluate_candle_pattern_gate,
    evaluate_level_proximity_gate,
    evaluate_htf_trend_filter,
    evaluate_macd_htf_bias,
    evaluate_momentum_filter,
    evaluate_session_filter,
)
from mtc_v2.core.indicators import IndicatorSnapshot, SupertrendIndicatorSnapshot
from mtc_v2.core.instrument import InstrumentMetadata
from mtc_v2.core.ma import (
    HtfMovingAverageTracker,
    McGinleyTracker,
    MovingAverageTracker,
    VolumeSmaTracker,
    AdxTracker,
    ChoppinessTracker,
    AtrVolFloorTracker,
    MacdTracker,
)
from mtc_v2.core.position_manager import POSITION_SIDE_LONG, POSITION_SIDE_SHORT, PositionManager
from mtc_v2.core.position_sizer import PositionSizer
from mtc_v2.core.types import Bar, EntryDecision, GateResult, HtfSnapshot, PortfolioState, RawSignal
from mtc_v2.signals.range_filter import RangeFilterSignal
from mtc_v2.signals.supertrend import SupertrendSignal


def resolve_price_source(bar: "Bar", source: str) -> float:
    """Resolve a Pine-style price source name to a float value for the given bar."""
    mapping = {
        "close":  bar.close,
        "open":   bar.open,
        "hl2":    (bar.high + bar.low) / 2.0,
        "hlc3":   (bar.high + bar.low + bar.close) / 3.0,
        "ohlc4":  (bar.open + bar.high + bar.low + bar.close) / 4.0,
    }
    if source not in mapping:
        raise ValueError(f"Unknown price source: {source!r}")
    return mapping[source]


REASON_SIGNAL_CONFLICT = "signal_conflict"
REASON_EXIT_OPP_SIGNAL = "opp_signal"
REASON_EXIT_FILTER_BLOCK = "filter_block"
REASON_EXIT_TIME_STOP = "time_stop"
REASON_EXIT_EOD = "eod"
REASON_EXIT_EOW = "eow"
REASON_EXIT_GUARD = "guard_blocked"
FILL_POLICY_DECISION_BAR_CLOSE = "decision_bar_close"
EXIT_BEFORE_ENTRY_PLACEHOLDER = "future_position_manager_exit_before_entry"
SAME_BAR_REENTRY_OWNER = "future_position_manager_same_bar_reentry"
REASON_EXIT_MARGIN_CALL = "margin_call"


class Runner:
    """Parity-first MTC_V2 runner, extended through the L18 confirm transform."""

    def __init__(self, config: dict[str, object]) -> None:
        self.config = resolve_config(config)
        self.execution_profile_id = str(self.config["execution_profile_id"])
        self.fill_policy_id = FILL_POLICY_DECISION_BAR_CLOSE
        self.exit_before_entry_policy = EXIT_BEFORE_ENTRY_PLACEHOLDER
        self.same_bar_reentry_owner = SAME_BAR_REENTRY_OWNER
        self.allow_flip = bool(self.config["allow_flip"])
        self._override_adx_values = None
        self._override_chop_values = None
        self._override_macd_htf_line = None
        self._override_htf_trend_line = None
        self._override_ma_filter_line = None
        self._override_mcginley_line = None
        self.regime_lock = bool(self.config["regime_lock"])
        self.initial_capital = float(self.config["initial_capital"])
        self.margin_long_pct = float(self.config["margin_long_pct"])
        self.margin_short_pct = float(self.config["margin_short_pct"])
        self.max_leverage_cap = float(self.config["max_leverage_cap"])
        self.tw_audit_semantics_mode = str(self.config.get("tw_audit_semantics_mode", "off"))
        self.tw_reversal_reentry_mode = str(self.config.get("tw_reversal_reentry_mode", "local"))
        self.tw_reversal_reentry_delay_bars = int(self.config.get("tw_reversal_reentry_delay_bars", 0))
        self.tw_margin_call_mode = str(self.config.get("tw_margin_call_mode", "off"))
        self.tw_margin_call_split_entries = bool(self.config.get("tw_margin_call_split_entries", False))
        self.tw_be_semantics_mode = str(self.config.get("tw_be_semantics_mode", "local"))
        self.tw_trailing_semantics_mode = str(self.config.get("tw_trailing_semantics_mode", "local"))
        self.instrument = InstrumentMetadata.from_config(self.config)
        self.state = PortfolioState(
            initial_capital=self.initial_capital,
            equity=self.initial_capital,
            execution_profile_id=self.execution_profile_id,
            instrument=self.instrument,
        )
        signal_mode = str(self.config["signal_mode"])
        if signal_mode == SIGNAL_MODE_RANGE_FILTER:
            self.signal_producer = RangeFilterSignal(self.config)
        elif signal_mode == SIGNAL_MODE_SUPERTREND:
            self.signal_producer = SupertrendSignal(self.config)
        else:
            raise ValueError(f"Unsupported signal_mode: {signal_mode}")
        self.position_manager = PositionManager(
            enable_long=bool(self.config["enable_long"]),
            enable_short=bool(self.config["enable_short"]),
            regime_lock=self.regime_lock,
            max_entries=int(self.config["max_entries"]),
            cooldown_bars=int(self.config["cooldown_bars"]),
            contract_multiplier=self.instrument.contract_multiplier,
            qty_step=self.instrument.qty_step,
        )
        self.position_sizer = PositionSizer(self.config)
        self.ma_filter_tracker = MovingAverageTracker(
            length=int(self.config["ma_length"]),
            ma_type=str(self.config["ma_type"]),
            enabled=bool(self.config["use_ma_filter"]),
        )
        self.ma_slope_tracker = MovingAverageTracker(
            length=int(self.config["ma_slope_len"]),
            ma_type=str(self.config["ma_type"]),
            enabled=bool(self.config["use_ma_slope_filter"]),
        )
        self.mcginley_tracker = McGinleyTracker(
            length=int(self.config["mcginley_length"]),
            enabled=bool(self.config["use_mcginley_filter"]),
        )
        self.vol_sma_tracker = VolumeSmaTracker(
            length=int(self.config["vol_sma_length"]),
            enabled=bool(self.config["use_volume_filter"]),
        )
        self.adx_tracker = AdxTracker(
            length=int(self.config["adx_length"]),
            enabled=bool(self.config["use_adx_filter"]),
        )
        self.chop_tracker = ChoppinessTracker(
            length=int(self.config["chop_length"]),
            enabled=bool(self.config["use_chop_filter"]),
        )
        self.atr_vol_floor_tracker = AtrVolFloorTracker(
            fast_length=int(self.config["atr_vol_floor_fast_len"]),
            baseline_length=int(self.config["atr_vol_floor_baseline_len"]),
            enabled=bool(self.config["use_atr_vol_floor"]),
        )
        self.macd_tracker = MacdTracker(
            fast_len=int(self.config["macd_fast_len"]),
            slow_len=int(self.config["macd_slow_len"]),
            sig_len=int(self.config["macd_sig_len"]),
            enabled=(
                bool(self.config["use_macd_regime_filter"])
                or bool(self.config["use_macd_cross_filter"])
                or bool(self.config["use_macd_hist_filter"])
                or bool(self.config["use_macd_zero_dist_filter"])
            ),
        )
        self._htf_trend_tracker = HtfMovingAverageTracker(
            length=int(self.config["htf_trend_ma_len"]),
            ma_type=str(self.config["htf_trend_ma_type"]),
            enabled=bool(self.config["use_htf_trend_filter"]),
        )
        # MACD HTF Bias: separate MACD tracker fed with HTF close values
        self._macd_htf_tracker = MacdTracker(
            fast_len=int(self.config["macd_fast_len"]),
            slow_len=int(self.config["macd_slow_len"]),
            sig_len=int(self.config["macd_sig_len"]),
            enabled=bool(self.config.get("use_macd_htf_bias", False)),
        )
        # Momentum Filter ATR (RMA, same formula as atr_vol_floor fast-side)
        self.momentum_atr_tracker = AtrVolFloorTracker(
            fast_length=int(self.config["momentum_atr_len"]),
            baseline_length=int(self.config["momentum_atr_len"]),  # unused
            enabled=bool(self.config.get("use_momentum_filter", False)),
        )

        self.stop_atr_tracker = AtrTracker(
            length=int(self.config["sl_atr_len"]),
            enabled=bool(self.config["use_sl"] and self.config["use_sl_atr"]),
            snapshot_kind="stop",
        )
        self.swing_sl_atr_tracker = AtrTracker(
            length=int(self.config["sl_swing_atr_len"]),
            enabled=bool(self.config["use_sl"] and self.config["use_sl_swing_atr"]),
            snapshot_kind="stop",
        )
        self.tp_atr_tracker = AtrTracker(
            length=int(self.config["tp_atr_len"]),
            enabled=bool(self.config["tp_mode"] == "ATR"),
            snapshot_kind="tp",
        )
        self.trail_atr_tracker = AtrTracker(
            length=int(self.config["trail_atr_len"]),
            enabled=bool(self.config["use_trailing"]),
            snapshot_kind="stop",
        )
        self._swing_history: deque[Bar] = deque(maxlen=max(int(self.config["sl_swing_lookback"]), 1))
        self._level_prox_history: deque[Bar] = deque(
            maxlen=max(int(self.config.get("level_proximity_lookback", 50)), 1)
        )
        self._candle_history: deque[Bar] = deque(
            maxlen=max(int(self.config.get("candle_pattern_lookback", 5)) + 1, 2)
        )
        self._prev_bar: Bar | None = None

        # L14-L18 state
        self._l15_bars_since_entry: int = 0
        self._l16_day_open_equity: float | None = None
        self._l16_trades_today: int = 0
        self._l16_last_trade_day: str | None = None
        self._l16_equity_peak: float = self.initial_capital
        self._l16_consec_loss_count: int = 0
        self._l16_equity_history: list[float] = []
        self._l16_equity_sma: float | None = None
        # L16 MAE guard
        self._l16_mae_current: float = 0.0
        self._l16_mae_last: float = 0.0
        # L16 Trade cooldown after exit
        self._l16_last_exit_bar_index: int | None = None
        # TradingView execution-parity research state (default-off).
        self._tw_last_protective_exit_bar_index: int | None = None
        self._tw_pending_reentry_side: str | None = None
        self._tw_pending_reentry_reason: str | None = None
        self._tw_pending_open_side: str | None = None
        self._tw_pending_open_reason: str | None = None
        # L16 guard recovery
        self._l16_guard_recovery_active: bool = False
        self._l16_guard_recovery_bars_rem: int = 0
        self._l16_guard_recovery_signals_rem: int = 0
        # L18 confirmation transform
        self._l18_confirm_direction: int = 0  # 1=long, -1=short, 0=none
        self._l18_confirm_bars_count: int = 0
        self._l18_long_armed: bool = False
        self._l18_short_armed: bool = False
        self._l18_prev_raw_long: bool = False
        self._l18_prev_raw_short: bool = False
        # L18b confirmation port scaffold
        self._l18b_state: AdvancedConfirmationState = build_advanced_confirmation_state()
        self._l18b_snapshot = snapshot_advanced_confirmation_state(
            self._l18b_state,
            enabled=bool(self.config.get("use_l18b_confirmation", False)),
        )

        # HTF data lookup (set once per run() call when htf_data is provided;
        # preserved across bar-by-bar run() calls when htf_data=None)
        self._htf_data: dict = {}

        # Track last seen HTF OHLCV to step HTF indicators only on edges
        self._last_adx_htf_key = None
        self._last_chop_htf_key = None

        # L21 Level Retest
        self._l21_waiting: bool = False
        self._l21_pending_side: int = 0   # 1=long, -1=short
        self._l21_break_level: float = 0.0
        self._l21_bars_waiting: int = 0
        # allow_flip=False: pending entry deferred from the opp_signal bar
        self._deferred_flip_side: int = 0  # 1=long, -1=short, 0=none

        self.state.warmup_bars = max(
            self.signal_producer.warmup_bars_required,
            self._gate_warmup_bars_required(),
            self.stop_atr_tracker.warmup_bars_required,
            self.swing_sl_atr_tracker.warmup_bars_required,
            self.tp_atr_tracker.warmup_bars_required,
            self.trail_atr_tracker.warmup_bars_required,
            int(self.config["sl_swing_lookback"]) if bool(self.config["use_sl"] and self.config["use_sl_swing_atr"]) else 0,
        )

    def run(
        self,
        bars: Iterable[Bar],
        htf_data: "dict | None" = None,
    ) -> list[RawSignal]:
        """Run the strategy over a sequence of bars.

        Parameters
        ----------
        bars :
            Iterable of ``Bar`` objects (LTF, in chronological order).
        htf_data :
            Optional ``dict`` mapping ``pd.Timestamp`` â†’ HTF OHLCV dict (or
            ``None`` for warmup bars).  Built by
            ``mtc_v2.core.htf.build_htf_lookup()``.  When provided, each bar
            loop iteration will expose an ``HtfSnapshot`` for HTF-aware gate
            functions (Tasks 1â€“6).
        """
        if htf_data is not None:
            self._htf_data = htf_data
        outputs: list[RawSignal] = []
        _first_bar: Bar | None = None
        for bar in bars:
            if _first_bar is None:
                _first_bar = bar
            self.state.current_bar_index = bar.bar_index
            self.state.block_new_entries_this_bar = False
            self.state.opened_this_bar_reason = None
            self.state.closed_this_bar_reason = None
            self.state.exit_events_this_bar = []
            self.state.last_exit_qty = 0.0
            self.state.last_exit_id = None
            self.state.last_exit_was_partial = False

            sizing_equity_snapshot = self._frozen_sizing_equity_snapshot(bar)
            self.state.last_sizing_equity_snapshot = sizing_equity_snapshot
            self._maybe_execute_tw_pending_open_entry(bar=bar, sizing_equity_snapshot=sizing_equity_snapshot)

            raw = self.signal_producer.calculate(bar)
            raw = finalize_advanced_confirmation_signal(
                raw,
                bar=bar,
                state=self._l18b_state,
                enabled=bool(self.config.get("use_l18b_confirmation", False)),
            )
            self._l18b_snapshot = snapshot_advanced_confirmation_state(
                self._l18b_state,
                enabled=bool(self.config.get("use_l18b_confirmation", False)),
            )
            # Build HTF snapshot for this bar (used by HTF-aware gate functions).
            htf_snap = HtfSnapshot.from_dict(self._htf_data.get(bar.timestamp))
            # Update HTF trend tracker with prior-closed HTF close
            if bool(self.config["use_htf_trend_filter"]):
                self._htf_trend_tracker.update(htf_snap.close if htf_snap.is_ready else None)
            # Update MACD HTF bias tracker with prior-closed HTF close (no dedup â€” every bar)
            if bool(self.config.get("use_macd_htf_bias", False)) and self._bar_is_valid(bar) and htf_snap.is_ready:
                self._macd_htf_tracker.update(htf_snap.close)
            ma_filter_line, ma_slope_line, mcginley_line, vol_sma, adx, chop, fast_atr, base_atr, macd_line, macd_sig, macd_hist, prev_macd_hist, momentum_atr = self._update_gate_indicators(bar, htf_snap=htf_snap)
            gate_results = self._evaluate_entry_gates(
                bar=bar,
                prev_bar=self._prev_bar,
                close=bar.close,
                volume=bar.volume,
                high=bar.high,
                low=bar.low,
                ma_filter_line=ma_filter_line,
                ma_slope_line=ma_slope_line,
                ma_slope_prev_line=self.ma_slope_tracker.prev_line,
                mcginley_line=mcginley_line,
                vol_sma=vol_sma,
                adx=adx,
                chop=chop,
                fast_atr=fast_atr,
                baseline_atr=base_atr,
                macd_line=macd_line,
                macd_signal=macd_sig,
                macd_hist=macd_hist,
                prev_macd_hist=prev_macd_hist,
                momentum_atr=momentum_atr,
            )
            # Inject HTF trend gate (evaluated after tracker is updated each bar)
            if bool(self.config["use_htf_trend_filter"]):
                gate_results[GATE_HTF_TREND] = evaluate_htf_trend_filter(
                    close=bar.close,
                    htf_snap=htf_snap,
                    ma_type=str(self.config["htf_trend_ma_type"]),
                    ma_len=int(self.config["htf_trend_ma_len"]),
                    buffer_pct=float(self.config["htf_trend_buffer_pct"]),
                    _tracker=self._htf_trend_tracker,
                )
            else:
                gate_results[GATE_HTF_TREND] = GateResult(
                    gate_name=GATE_HTF_TREND,
                    long_ok=True,
                    short_ok=True,
                    value=None,
                    category="filter",
                )
            _htf_trend_ov = self._override_series_value(self._override_htf_trend_line, bar.bar_index)
            if bool(self.config["use_htf_trend_filter"]) and _htf_trend_ov is not None:
                _buf = float(self.config["htf_trend_buffer_pct"]) / 100.0
                gate_results[GATE_HTF_TREND] = GateResult(
                    gate_name=GATE_HTF_TREND,
                    long_ok=float(bar.close) > _htf_trend_ov * (1.0 - _buf),
                    short_ok=float(bar.close) < _htf_trend_ov * (1.0 + _buf),
                    value=float(_htf_trend_ov),
                    category="filter",
                )
            # Inject MACD HTF bias gate (evaluated after HTF tracker update each bar)
            gate_results[GATE_MACD_HTF_BIAS] = evaluate_macd_htf_bias(
                use_macd_htf_bias=bool(self.config.get("use_macd_htf_bias", False)),
                macd_htf_line=self._macd_htf_tracker.macd_line,
            )
            _macd_htf_ov = self._override_series_value(self._override_macd_htf_line, bar.bar_index)
            if bool(self.config.get("use_macd_htf_bias", False)) and _macd_htf_ov is not None:
                gate_results[GATE_MACD_HTF_BIAS] = GateResult(
                    gate_name=GATE_MACD_HTF_BIAS,
                    long_ok=float(_macd_htf_ov) > 0.0,
                    short_ok=float(_macd_htf_ov) < 0.0,
                    value=float(_macd_htf_ov),
                    category="filter",
                )
            self.state.gate_results = gate_results
            gated = self._apply_entry_gates(raw, gate_results)
            self.state.gated_long = gated.long
            self.state.gated_short = gated.short
            signal_indicator_snapshot = self._signal_indicator_snapshot(raw)
            stop_indicator_snapshot = self.stop_atr_tracker.update(bar)
            self.swing_sl_atr_tracker.update(bar)
            tp_indicator_snapshot = self.tp_atr_tracker.update(bar)
            self.trail_atr_tracker.update(bar)
            self.state.indicator_snapshot = IndicatorSnapshot(
                supertrend=signal_indicator_snapshot,
                atr_stop=stop_indicator_snapshot,
                atr_tp=tp_indicator_snapshot,
            )

            warmup_blocks_entry = (
                not self.state.indicator_snapshot.supertrend.warmup_ready
                or (bar.bar_index < self.state.warmup_bars - 1)
                # Mirror Pine l12_filters_ready: block entries until HTF MA line is non-na
                or (
                    bool(self.config["use_htf_trend_filter"])
                    and self._override_series_value(self._override_htf_trend_line, bar.bar_index) is None
                    and not self._htf_trend_tracker.ready
                )
                # When use_ma_mtf=True, block until the HTF-fed MA filter line is ready
                or (
                    bool(self.config.get("use_ma_filter", False))
                    and bool(self.config.get("use_ma_mtf", False))
                    and self._override_series_value(self._override_ma_filter_line, bar.bar_index) is None
                    and self.ma_filter_tracker.line is None
                )
                # When use_macd_htf_bias=True, block until HTF MACD line is ready
                or (
                    bool(self.config.get("use_macd_htf_bias", False))
                    and self._override_series_value(self._override_macd_htf_line, bar.bar_index) is None
                    and self._macd_htf_tracker.macd_line is None
                )
                # When ADX/Chop use HTF, block until their HTF-fed values are ready
                or (
                    bool(self.config.get("use_adx_filter", False))
                    and bool(self.config.get("adx_use_higher_timeframe", False))
                    and self._override_series_value(self._override_adx_values, bar.bar_index) is None
                    and self.adx_tracker.adx is None
                )
                or (
                    bool(self.config.get("use_chop_filter", False))
                    and bool(self.config.get("chop_use_higher_timeframe", False))
                    and self._override_series_value(self._override_chop_values, bar.bar_index) is None
                    and self.chop_tracker.chop is None
                )
                or (
                    bool(self.config.get("use_mcginley_filter", False))
                    and bool(self.config.get("mcginley_use_higher_timeframe", False))
                    and self._override_series_value(self._override_mcginley_line, bar.bar_index) is None
                    and self.mcginley_tracker.line is None
                )
            )
            price_exit_blocks_entry = not self._entry_ready()

            if raw.long and raw.short:
                raw = RawSignal(
                    False,
                    False,
                    REASON_SIGNAL_CONFLICT,
                    direction=raw.direction,
                    line=raw.line,
                )
                gated = RawSignal(
                    False,
                    False,
                    REASON_SIGNAL_CONFLICT,
                    direction=gated.direction,
                    line=gated.line,
                )
                self.state.gated_long = False
                self.state.gated_short = False

            candidate_side = self._candidate_side(raw)
            gated_candidate_side = self._candidate_side(gated)

            # Deferred flip entry (allow_flip=False): when opp_signal bar blocked the
            # opposite-direction entry, replay it next bar if flat and no fresh signal.
            if self._deferred_flip_side != 0:
                if (
                    self.state.position is None
                    and not gated.long
                    and not gated.short
                    and not warmup_blocks_entry
                ):
                    _rep_ok = all(
                        gate.long_ok if self._deferred_flip_side == 1 else gate.short_ok
                        for gate in gate_results.values()
                    )
                    _def_long = self._deferred_flip_side == 1 and _rep_ok
                    _def_short = self._deferred_flip_side == -1 and _rep_ok
                    raw = RawSignal(_def_long, _def_short, raw.reason, direction=raw.direction, line=raw.line)
                    gated = raw
                    self.state.gated_long = gated.long
                    self.state.gated_short = gated.short
                    candidate_side = self._candidate_side(raw)
                    gated_candidate_side = self._candidate_side(gated)
                    self._deferred_flip_side = 0
                else:
                    self._deferred_flip_side = 0  # cancel: position open, fresh signal, or warmup

            if (
                self.regime_lock
                and candidate_side is not None
                and self.state.regime_lock_side is not None
                and candidate_side != self.state.regime_lock_side
            ):
                self.state.regime_lock_side = None

            entry_blocked_by_exit = False
            if self.state.position is not None:
                update_protective_stop_owner(
                    self.config,
                    position=self.state.position,
                    bar=bar,
                    prev_bar=self._prev_bar,
                    price_tick=self.instrument.price_tick,
                    trail_atr=self.trail_atr_tracker.atr,
                )
                sync_working_exit_stops(self.state.position)

                price_exit_blocked_entry = False
                continue_price_loop = True
                if self.tw_audit_semantics_mode == "research" and self.tw_margin_call_mode == "tradingview":
                    self._apply_tw_margin_call_semantics(bar=bar)
                while self.state.position is not None and continue_price_loop:
                    continue_price_loop = False
                    price_exit = evaluate_price_exit(self.config, bar=bar, position=self.state.position)
                    if price_exit.hit and price_exit.fill_price is not None and price_exit.reason is not None:
                        self.position_manager.close_position(
                            bar=bar,
                            exit_price=price_exit.fill_price,
                            reason=price_exit.reason,
                            state=self.state,
                            exit_pct=price_exit.exit_pct,
                            exit_id=price_exit.exit_id,
                            is_pessimistic=price_exit.is_pessimistic,
                        )
                        if (
                            self.state.position is not None
                            and bool(getattr(price_exit, "cancel_remaining_targets_after_fill", False))
                        ):
                            disable_active_target_exits(self.state.position)
                        # Future TW execution parity work will branch from this owner
                        # to model margin-call splitting and protective-exit reentry delay.
                        self._remember_tw_protective_exit(bar=bar, reason=price_exit.reason)
                        price_exit_blocked_entry = True
                        entry_blocked_by_exit = True
                        continue_price_loop = (
                            self.state.position is not None and price_exit.continue_evaluation_this_bar
                        )

                if (
                    bool(self.config["exit_on_opposite_signal"])
                    and self.state.position is not None
                    and candidate_side is not None
                    and candidate_side != self.state.position.side
                ):
                    self.position_manager.close_position(
                        bar=bar,
                        exit_price=bar.close,
                        reason=REASON_EXIT_OPP_SIGNAL,
                        state=self.state,
                    )
                    entry_blocked_by_exit = not self.allow_flip
                    self._remember_tw_protective_exit(bar=bar, reason=REASON_EXIT_OPP_SIGNAL)
                elif price_exit_blocked_entry:
                    entry_blocked_by_exit = True

                # --- L14: FILTER_BLOCK EXIT ---
                if (
                    self.state.position is not None
                    and not entry_blocked_by_exit
                    and self.state.closed_this_bar_reason is None
                ):
                    pos = self.state.position
                    gr = self.state.gate_results
                    cfg = self.config
                    filter_blocked = False
                    is_long_pos = pos.side == POSITION_SIDE_LONG
                    if bool(cfg["exit_on_ma_block"]):
                        ok = gr[GATE_MA_FILTER].long_ok if is_long_pos else gr[GATE_MA_FILTER].short_ok
                        if not ok:
                            filter_blocked = True
                    if not filter_blocked and bool(cfg["exit_on_ma_slope_block"]):
                        ok = gr[GATE_MA_SLOPE_FILTER].long_ok if is_long_pos else gr[GATE_MA_SLOPE_FILTER].short_ok
                        if not ok:
                            filter_blocked = True
                    if not filter_blocked and bool(cfg["exit_on_mcginley_block"]):
                        ok = gr[GATE_MCGINLEY_FILTER].long_ok if is_long_pos else gr[GATE_MCGINLEY_FILTER].short_ok
                        if not ok:
                            filter_blocked = True
                    if not filter_blocked and bool(cfg["exit_on_vol_block"]):
                        ok = gr[GATE_VOLUME_FILTER].long_ok if is_long_pos else gr[GATE_VOLUME_FILTER].short_ok
                        if not ok:
                            filter_blocked = True
                    if not filter_blocked and bool(cfg["exit_on_atr_vol_block"]):
                        ok = gr[GATE_ATR_VOL_FLOOR].long_ok if is_long_pos else gr[GATE_ATR_VOL_FLOOR].short_ok
                        if not ok:
                            filter_blocked = True
                    if not filter_blocked and bool(cfg["exit_on_range_block"]):
                        adx_ok = gr[GATE_ADX_FILTER].long_ok if is_long_pos else gr[GATE_ADX_FILTER].short_ok
                        chop_ok = gr[GATE_CHOP_FILTER].long_ok if is_long_pos else gr[GATE_CHOP_FILTER].short_ok
                        if not adx_ok or not chop_ok:
                            filter_blocked = True
                    if not filter_blocked and bool(cfg["exit_on_candle_pattern_block"]):
                        ok = gr[GATE_CANDLE_PATTERN].long_ok if is_long_pos else gr[GATE_CANDLE_PATTERN].short_ok
                        if not ok:
                            filter_blocked = True
                    if not filter_blocked and bool(cfg["exit_on_level_prox_block"]):
                        ok = gr[GATE_LEVEL_PROXIMITY].long_ok if is_long_pos else gr[GATE_LEVEL_PROXIMITY].short_ok
                        if not ok:
                            filter_blocked = True
                    if not filter_blocked and bool(cfg["exit_on_htf_trend_block"]):
                        ok = gr[GATE_HTF_TREND].long_ok if is_long_pos else gr[GATE_HTF_TREND].short_ok
                        if not ok:
                            filter_blocked = True
                    if filter_blocked:
                        self.position_manager.close_position(
                            bar=bar,
                            exit_price=bar.close,
                            reason=REASON_EXIT_FILTER_BLOCK,
                            state=self.state,
                        )
                        self._remember_tw_protective_exit(bar=bar, reason=REASON_EXIT_FILTER_BLOCK)
                        entry_blocked_by_exit = True

                # --- L15: TIME-BASED EXITS ---
                if (
                    self.state.position is not None
                    and self.state.closed_this_bar_reason is None
                ):
                    # bars_since_entry
                    entry_bar = self.state.position.entry_bar
                    self._l15_bars_since_entry = bar.bar_index - entry_bar

                    time_exit_reason: str | None = None
                    if bool(self.config["use_time_stop"]):
                        cond = str(self.config["time_stop_condition"])
                        last_pnl = self.state.last_realized_pnl
                        cond_ok = (
                            cond == "Always"
                            or (cond == "Profit Only" and last_pnl >= 0.0)
                            or (cond == "Loss Only" and last_pnl < 0.0)
                        )
                        if self._l15_bars_since_entry >= int(self.config["time_stop_bars"]) and cond_ok:
                            time_exit_reason = REASON_EXIT_TIME_STOP
                    if time_exit_reason is None and bool(self.config["time_stop_eod"]):
                        # EOD: fires on the first bar of a new calendar day
                        day_str_l15 = bar.timestamp.strftime("%Y%m%d")
                        if self._l16_last_trade_day is not None and day_str_l15 != self._l16_last_trade_day:
                            time_exit_reason = REASON_EXIT_EOD
                    if time_exit_reason is None and bool(self.config["time_stop_eow"]):
                        # EOW: Friday bar with hour >= 21 UTC (matches Pine's closing-hour check)
                        if bar.timestamp.weekday() == 4 and bar.timestamp.hour >= 21:
                            time_exit_reason = REASON_EXIT_EOW
                    if time_exit_reason is not None:
                        self.position_manager.close_position(
                            bar=bar,
                            exit_price=bar.close,
                            reason=time_exit_reason,
                            state=self.state,
                        )
                        self._remember_tw_protective_exit(bar=bar, reason=time_exit_reason)
                        entry_blocked_by_exit = True
                else:
                    self._l15_bars_since_entry = 0

            # --- L16: GUARDS ---
            if not warmup_blocks_entry:
                realized_equity = self.state.initial_capital + self.state.realized_equity
                day_str = bar.timestamp.strftime("%Y%m%d")

                # MAE tracking: update running MAE for open position BEFORE exits are evaluated
                # (position may have been closed above; record it if so)
                if self.state.position is not None:
                    pos16 = self.state.position
                    if pos16.entry_price is not None and pos16.entry_price > 0.0:
                        if pos16.side == POSITION_SIDE_LONG:
                            adverse = max(pos16.entry_price - bar.low, 0.0)
                        else:
                            adverse = max(bar.high - pos16.entry_price, 0.0)
                        mae_pct_now = adverse / pos16.entry_price * 100.0
                        self._l16_mae_current = max(self._l16_mae_current, mae_pct_now)
                # Capture MAE when position closed this bar
                if self.state.closed_this_bar_reason is not None and self.state.position is None:
                    self._l16_mae_last = self._l16_mae_current
                    self._l16_mae_current = 0.0

                # Update equity peak
                if realized_equity > self._l16_equity_peak:
                    self._l16_equity_peak = realized_equity

                # Track consecutive losses â€” only on full close (SAP-06)
                if self.state.closed_this_bar_reason is not None and self.state.position is None:
                    if self.state.last_realized_pnl < 0.0:
                        self._l16_consec_loss_count += 1
                    else:
                        self._l16_consec_loss_count = 0

                # Day reset
                if self._l16_last_trade_day != day_str:
                    self._l16_trades_today = 0
                    self._l16_day_open_equity = realized_equity
                    self._l16_last_trade_day = day_str

                if self.state.closed_this_bar_reason is not None:
                    self._l16_trades_today += 1

                # Equity curve SMA
                if self.state.closed_this_bar_reason is not None and self.state.position is None:
                    self._l16_equity_history.append(realized_equity)
                    ma_len = int(self.config["equity_ma_length"])
                    if len(self._l16_equity_history) > ma_len:
                        self._l16_equity_history = self._l16_equity_history[-ma_len:]
                    if len(self._l16_equity_history) >= ma_len:
                        self._l16_equity_sma = sum(self._l16_equity_history) / ma_len

                # Trade cooldown: record bar index of last full position close
                if self.state.closed_this_bar_reason is not None and self.state.position is None:
                    self._l16_last_exit_bar_index = bar.bar_index

                # Canonical guard order: daily_loss â†’ max_trades â†’ max_drawdown â†’ consec_loss â†’ equity_curve â†’ mae
                daily_loss_ok = (
                    not bool(self.config["use_daily_loss_limit"])
                    or self._l16_day_open_equity is None
                    or self._l16_day_open_equity <= 0.0
                    or (self._l16_day_open_equity - realized_equity) / self._l16_day_open_equity * 100.0
                    < float(self.config["max_daily_loss_pct"])
                )
                max_trades_ok = (
                    not bool(self.config["use_max_trades_per_day"])
                    or self._l16_trades_today < int(self.config["max_trades_per_day"])
                )
                max_dd_ok = (
                    not bool(self.config["use_max_drawdown_guard"])
                    or self._l16_equity_peak <= 0.0
                    or (self._l16_equity_peak - realized_equity) / self._l16_equity_peak * 100.0
                    < float(self.config["max_drawdown_pct"])
                )
                consec_loss_ok = (
                    not bool(self.config["use_consecutive_loss_halt"])
                    or self._l16_consec_loss_count < int(self.config["max_consecutive_losses"])
                )
                ec_ok = (
                    not bool(self.config["use_equity_curve_filter"])
                    or self._l16_equity_sma is None
                    or realized_equity >= self._l16_equity_sma
                )
                mae_ok = (
                    not bool(self.config["use_mae_guard"])
                    or self._l16_mae_last <= float(self.config["max_mae_pct"])
                )
                guard_blocked_raw = not (daily_loss_ok and max_trades_ok and max_dd_ok
                                         and consec_loss_ok and ec_ok and mae_ok)

                # Guard Recovery (SAP-02)
                if bool(self.config["use_guard_recovery"]):
                    if guard_blocked_raw and not self._l16_guard_recovery_active:
                        # New breach: activate recovery lock
                        self._l16_guard_recovery_active = True
                        self._l16_guard_recovery_bars_rem = int(self.config["guard_recovery_bars"])
                        self._l16_guard_recovery_signals_rem = int(self.config["guard_recovery_signals"])
                    if self._l16_guard_recovery_active:
                        recovery_mode = str(self.config["guard_recovery_mode"])
                        if recovery_mode == "Bars":
                            # Countdown runs unconditionally (breach-agnostic)
                            self._l16_guard_recovery_bars_rem = max(0, self._l16_guard_recovery_bars_rem - 1)
                            if self._l16_guard_recovery_bars_rem <= 0:
                                self._force_reset_guard_state(realized_equity)
                                self._l16_guard_recovery_active = False
                        # Signals mode: countdown deferred below after gated candidate is evaluated

                trade_cooldown_blocked = (
                    bool(self.config.get("use_trade_cooldown", False))
                    and self._l16_last_exit_bar_index is not None
                    and (bar.bar_index - self._l16_last_exit_bar_index) < int(self.config["cooldown_bars_after_exit"])
                )
                guard_blocked = guard_blocked_raw or (
                    bool(self.config["use_guard_recovery"]) and self._l16_guard_recovery_active
                ) or trade_cooldown_blocked
            else:
                guard_blocked = False

            # --- L18: CONFIRMATION TRANSFORM ---
            # BUG-01 fix: track RAW signal direction (pre-gate), not gated
            # This matches Pine's `l18_raw_dir = long_raw ? 1 : short_raw ? -1 : 0`
            if bool(self.config["use_confirm_transform"]) and not warmup_blocks_entry:
                raw_dir = 1 if raw.long else (-1 if raw.short else 0)
                confirm_bars_cfg = int(self.config["confirm_bars"])
                # Pine: `if l18_new_dir != 0 and l18_new_dir != l18_confirm_direction_state`
                # raw_dir=0 (no signal) never triggers the direction-change branch.
                if raw_dir != 0 and raw_dir != self._l18_confirm_direction:
                    self._l18_confirm_direction = raw_dir
                    self._l18_confirm_bars_count = 1
                    self._l18_long_armed = False
                    self._l18_short_armed = False
                elif self._l18_confirm_direction != 0:
                    # Pine: `else if l18_confirm_direction_state != 0` — keep counting
                    self._l18_confirm_bars_count += 1
                # refresh_on_new_raw runs unconditionally after if/else, matching Pine structure.
                # Resets count=0 when a NEW pulse fires on the direction-change bar, preventing
                # same-bar arming (pulse-producer semantics; with Supertrend this yields 0 trades).
                if bool(self.config["refresh_on_new_raw"]):
                    if raw.long and not self._l18_prev_raw_long and self._l18_confirm_direction == 1:
                        self._l18_confirm_bars_count = 0
                    elif raw.short and not self._l18_prev_raw_short and self._l18_confirm_direction == -1:
                        self._l18_confirm_bars_count = 0
                # SAP-05: confirm_close_crosses â€” runs unconditionally (matches Pine structure).
                # Pine line 1372: cross_ok is computed OUTSIDE the if/else, so it also applies
                # on direction-change bars. Failure resets count to 0 on any bar.
                if bool(self.config["confirm_close_crosses"]) and raw.line is not None and self._l18_confirm_direction != 0:
                    if self._l18_confirm_direction == 1:
                        cross_ok = bar.close > raw.line
                    else:
                        cross_ok = bar.close < raw.line
                    if not cross_ok:
                        self._l18_confirm_bars_count = 0
                        self._l18_long_armed = False
                        self._l18_short_armed = False
                if self._l18_confirm_bars_count >= confirm_bars_cfg:
                    raw_still = (self._l18_confirm_direction == 1 and raw.long) or (self._l18_confirm_direction == -1 and raw.short)
                    if not bool(self.config["require_raw_still_true"]) or raw_still:
                        if self._l18_confirm_direction == 1:
                            self._l18_long_armed = True
                        elif self._l18_confirm_direction == -1:
                            self._l18_short_armed = True
                # Pine line 1738-1739: l18_long_final = l18_long_confirmed AND individual gate flags
                # (NOT short_gated/long_gated which also require raw.long/short=True).
                # For pulse-only producers like Supertrend, raw.short=False on hold bars,
                # so the count-up confirmation bar has no raw pulse — gated.short=False there.
                # Using gate_results directly (without requiring raw signal) matches Pine.
                _gate_long_ok = all(gr.long_ok for gr in gate_results.values())
                _gate_short_ok = all(gr.short_ok for gr in gate_results.values())
                confirmed_long = self._l18_long_armed and _gate_long_ok
                confirmed_short = self._l18_short_armed and _gate_short_ok
                # one-shot fire reset — matches Pine lines 1724-1733
                if confirmed_long:
                    self._l18_long_armed = False
                    self._l18_confirm_bars_count = 0
                    self._l18_confirm_direction = 0
                if confirmed_short:
                    self._l18_short_armed = False
                    self._l18_confirm_bars_count = 0
                    self._l18_confirm_direction = 0
                from mtc_v2.core.types import RawSignal as _RS
                gated = _RS(
                    long=confirmed_long,
                    short=confirmed_short,
                    reason=gated.reason,
                    direction=gated.direction,
                    line=gated.line,
                )

            # --- L21: LEVEL RETEST TRANSFORM ---
            if bool(self.config["use_level_retest"]) and self.state.position is None:
                from mtc_v2.core.types import RawSignal as _RS
                retest_timeout = int(self.config["retest_timeout_bars"])
                buffer_pct = float(self.config["retest_buffer_pct"])

                if not self._l21_waiting and (gated.long or gated.short):
                    self._l21_waiting = True
                    self._l21_pending_side = 1 if gated.long else -1
                    self._l21_break_level = gated.line if gated.line is not None else bar.close
                    self._l21_bars_waiting = 0
                    gated = _RS(long=False, short=False, direction=gated.direction, line=gated.line, reason=gated.reason)
                
                elif self._l21_waiting:
                    self._l21_bars_waiting += 1
                    opp = (self._l21_pending_side == 1 and gated.short) or (self._l21_pending_side == -1 and gated.long)
                    if opp or self._l21_bars_waiting >= retest_timeout:
                        self._l21_waiting = False
                        self._l21_pending_side = 0
                        gated = _RS(long=False, short=False, direction=gated.direction, line=gated.line, reason=gated.reason)
                    elif self._l21_break_level > 0:
                        dist_pct = abs(bar.close - self._l21_break_level) / self._l21_break_level * 100.0
                        if dist_pct <= buffer_pct:
                            gated = _RS(long=(self._l21_pending_side == 1), short=(self._l21_pending_side == -1), direction=gated.direction, line=gated.line, reason=gated.reason)
                            self._l21_waiting = False
                            self._l21_pending_side = 0
                        else:
                            gated = _RS(long=False, short=False, direction=gated.direction, line=gated.line, reason=gated.reason)
            
            if self.state.position is None and self.state.closed_this_bar_reason is not None:
                self._l21_waiting = False
                self._l21_pending_side = 0
                self._l21_bars_waiting = 0

            # Mirror Pine 1805: deferred flip is set from the post-L18/L21 final candidate.
            # When L21 is active, it suppresses gated to False on the opp-exit bar,
            # so no deferred flip fires — matching Pine's l21_final_candidate=0 behaviour.
            if (
                not self.allow_flip
                and self.state.position is None
                and self.state.closed_this_bar_reason == REASON_EXIT_OPP_SIGNAL
            ):
                if gated.long:
                    self._deferred_flip_side = 1
                elif gated.short:
                    self._deferred_flip_side = -1

            # Guard recovery: signals mode – count post-transform candidate (unconditional, breach-agnostic)
            if (
                bool(self.config.get("use_guard_recovery", False))
                and self._l16_guard_recovery_active
                and str(self.config.get("guard_recovery_mode", "Bars")) == "Signals"
            ):
                if gated.long or gated.short:
                    self._l16_guard_recovery_signals_rem = max(0, self._l16_guard_recovery_signals_rem - 1)
                if self._l16_guard_recovery_signals_rem <= 0:
                    _realized_eq = self.state.initial_capital + self.state.realized_equity
                    self._force_reset_guard_state(_realized_eq)
                    self._l16_guard_recovery_active = False
                    guard_blocked = False

            self.state.block_new_entries_this_bar = warmup_blocks_entry or price_exit_blocks_entry or entry_blocked_by_exit or guard_blocked
            if (
                self.tw_audit_semantics_mode == "research"
                and self.tw_reversal_reentry_mode == "carry_to_next_bar_after_protective_exit"
                and self.state.position is None
                and self.state.closed_this_bar_reason is not None
                and self._tw_should_defer_reentry_after_protective_exit(bar=bar)
            ):
                if gated.long != gated.short:
                    self._tw_pending_reentry_side = POSITION_SIDE_LONG if gated.long else POSITION_SIDE_SHORT
                    self._tw_pending_reentry_reason = gated.reason

            decision = self._tw_pending_or_live_entry_decision(raw=gated)
            if (
                decision.can_open
                and decision.side is not None
                and self._tw_should_queue_next_bar_open_entry(bar=bar)
            ):
                self._tw_pending_open_side = decision.side
                self._tw_pending_open_reason = decision.reason
                decision = EntryDecision(False)
            if (
                decision.can_open
                and decision.side is not None
                and self._tw_should_queue_next_bar_close_entry(bar=bar)
            ):
                self._tw_pending_reentry_side = decision.side
                self._tw_pending_reentry_reason = decision.reason
                decision = EntryDecision(False)
            if decision.can_open and decision.side is not None and self._tw_should_defer_reentry_after_protective_exit(bar=bar):
                decision = EntryDecision(False)
            entry_blocked_by_capital = False
            if decision.can_open and decision.side is not None:
                is_long = decision.side == POSITION_SIDE_LONG
                entry_stop_price = self._entry_stop_price(bar=bar, entry_price=bar.close, is_long=is_long)
                entry_qty = self.position_sizer.calc_qty(
                    bar.close,
                    entry_stop_price,
                    sizing_equity_snapshot,
                    is_long,
                    self.instrument,
                    existing_position=self.state.position,
                )
                entry_blocked_by_capital = entry_qty > 0.0 and self._entry_blocked_by_capital(
                    entry_price=bar.close,
                    side=decision.side,
                    qty=entry_qty,
                    sizing_equity=sizing_equity_snapshot,
                )
                if entry_qty > 0.0 and not entry_blocked_by_capital:
                    initial_risk = self._initial_risk_for_entry(entry_price=bar.close, stop_price=entry_stop_price)
                    next_book_version = 1
                    completed_exit_ids: set[str] = set()
                    if self.state.position is not None and self.state.position.side == decision.side:
                        next_book_version = self.state.position.working_exit_book_version + 1
                        completed_exit_ids = set(self.state.position.completed_exit_ids)
                    active_tp_price, working_exits = build_working_exit_book(
                        self.config,
                        entry_price=bar.close,
                        is_long=is_long,
                        price_tick=self.instrument.price_tick,
                        atr_value=self.tp_atr_tracker.atr,
                        initial_risk_per_unit=initial_risk,
                        book_version=next_book_version,
                        completed_exit_ids=completed_exit_ids,
                    )
                    self.position_manager.open_position(
                        bar=bar,
                        side=decision.side,
                        qty=entry_qty,
                        state=self.state,
                        reason=decision.reason,
                        active_stop_price=entry_stop_price,
                        active_tp_price=active_tp_price,
                        working_exits=working_exits,
                    )
                    if self._tw_pending_reentry_side == decision.side:
                        self._tw_pending_reentry_side = None
                        self._tw_pending_reentry_reason = None

            self.state.block_new_entries_this_bar = (
                warmup_blocks_entry
                or price_exit_blocks_entry
                or entry_blocked_by_exit
                or entry_blocked_by_capital
                or self.state.position is not None
            )
            outputs.append(gated)
            self._swing_history.append(bar)
            self._level_prox_history.append(bar)
            self._candle_history.append(bar)
            self._prev_bar = bar
            self._l18_prev_raw_long = raw.long
            self._l18_prev_raw_short = raw.short
        # --- L24: DEBUG METADATA ---
        if bool(self.config.get("debug_mode", False)):
            self._debug_metadata = {
                "execution_profile_id": EXECUTION_PROFILE_RAW_CLOSE_ONLY,
                "tw_audit_semantics_mode": self.tw_audit_semantics_mode,
                "tw_reversal_reentry_mode": self.tw_reversal_reentry_mode,
                "tw_reversal_reentry_delay_bars": self.tw_reversal_reentry_delay_bars,
                "tw_margin_call_mode": self.tw_margin_call_mode,
                "tw_margin_call_split_entries": self.tw_margin_call_split_entries,
                "tw_be_semantics_mode": self.tw_be_semantics_mode,
                "tw_trailing_semantics_mode": self.tw_trailing_semantics_mode,
                "lifecycle_id": self.state.next_position_lifecycle_id - 1,
                "warmup_bars": self.state.warmup_bars,
                "warmup_seed_provenance": "preroll",
                "effective_history_start": str(_first_bar.timestamp) if _first_bar is not None else "",
            }

        return outputs

    def get_debug_metadata(self) -> dict[str, object]:
        """Return debug metadata populated after the last run() call (L24).

        Only populated when debug_mode=True. Returns empty dict otherwise.
        """
        return getattr(self, "_debug_metadata", {})

    def _gate_warmup_bars_required(self) -> int:
        ma_filter_warmup = int(self.config["ma_length"]) if bool(self.config["use_ma_filter"]) else 0
        ma_slope_warmup = (int(self.config["ma_slope_len"]) + 1) if bool(self.config["use_ma_slope_filter"]) else 0
        mcginley_warmup = int(self.config["mcginley_length"]) if bool(self.config["use_mcginley_filter"]) else 0
        vol_warmup = int(self.config["vol_sma_length"]) if bool(self.config["use_volume_filter"]) else 0
        adx_warmup = int(self.config["adx_length"]) * 2 if bool(self.config["use_adx_filter"]) else 0
        chop_warmup = int(self.config["chop_length"]) if bool(self.config["use_chop_filter"]) else 0
        atr_floor_warmup = (int(self.config["atr_vol_floor_fast_len"]) + int(self.config["atr_vol_floor_baseline_len"])) if bool(self.config["use_atr_vol_floor"]) else 0
        macd_warmup = (int(self.config["macd_slow_len"]) + int(self.config["macd_sig_len"])) if self.macd_tracker.enabled else 0
        level_prox_warmup = int(self.config["level_proximity_lookback"]) if bool(self.config["use_level_proximity_gate"]) else 0
        candle_warmup = 1 if bool(self.config["use_candle_pattern_gate"]) else 0
        return max(ma_filter_warmup, ma_slope_warmup, mcginley_warmup, vol_warmup, adx_warmup, chop_warmup, atr_floor_warmup, macd_warmup, level_prox_warmup, candle_warmup)

    def _update_gate_indicators(self, bar: Bar, htf_snap: "HtfSnapshot | None" = None) -> tuple:
        if self._bar_is_valid(bar):
            # When use_ma_mtf=True use the prior-closed HTF close to drive the MA filter
            # tracker (matches Pine's request.security HTF MA path).
            if bool(self.config.get("use_ma_mtf", False)):
                _ov_ma = self._override_series_value(self._override_ma_filter_line, bar.bar_index)
                if _ov_ma is not None:
                    ma_f = float(_ov_ma)
                elif htf_snap is not None and htf_snap.is_ready:
                    ma_f = self.ma_filter_tracker.update(htf_snap.close)
                else:
                    ma_f = self.ma_filter_tracker.line
            else:
                ma_f = self.ma_filter_tracker.update(bar.close)
            ma_s = self.ma_slope_tracker.update(bar.close)
            _ov_mcginley = self._override_series_value(self._override_mcginley_line, bar.bar_index)
            if _ov_mcginley is not None:
                mg = float(_ov_mcginley)
            # McGinley: use prior-closed HTF close when mcginley_use_higher_timeframe=True
            elif bool(self.config.get("use_mcginley_filter", False)) and bool(self.config.get("mcginley_use_higher_timeframe", False)):
                if htf_snap is not None and htf_snap.is_ready:
                    mg = self.mcginley_tracker.update(htf_snap.close)
                else:
                    mg = self.mcginley_tracker.line
            else:
                mg = self.mcginley_tracker.update(bar.close)
            vol_sma = self.vol_sma_tracker.update(bar.volume)
            # ADX: use prior-closed HTF h/l/c when adx_use_higher_timeframe=True
            if bool(self.config.get("use_adx_filter", False)) and bool(self.config.get("adx_use_higher_timeframe", False)):
                if self._override_adx_values is not None:
                    val = self._override_adx_values.get(bar.bar_index)
                    adx = float(val) if val is not None else self.adx_tracker.adx
                elif htf_snap is not None and htf_snap.is_ready:
                    adx = self.adx_tracker.update(htf_snap.high, htf_snap.low, htf_snap.close)
                else:
                    adx = self.adx_tracker.adx
            else:
                adx = self.adx_tracker.update(bar.high, bar.low, bar.close)

            # CHOP: use prior-closed HTF h/l/c when chop_use_higher_timeframe=True
            if bool(self.config.get("use_chop_filter", False)) and bool(self.config.get("chop_use_higher_timeframe", False)):
                if self._override_chop_values is not None:
                    val = self._override_chop_values.get(bar.bar_index)
                    chop = float(val) if val is not None else self.chop_tracker.chop
                elif htf_snap is not None and htf_snap.is_ready:
                    chop = self.chop_tracker.update(htf_snap.high, htf_snap.low, htf_snap.close)
                else:
                    chop = self.chop_tracker.chop
            else:
                chop = self.chop_tracker.update(bar.high, bar.low, bar.close)
                chop = self.chop_tracker.update(bar.high, bar.low, bar.close)
            fast_atr, base_atr = self.atr_vol_floor_tracker.update(bar.high, bar.low, bar.close)
            macd_src = resolve_price_source(bar, str(self.config.get("macd_source", "close")))
            macd_line, macd_sig, macd_hist, prev_macd_hist = self.macd_tracker.update(macd_src)
            momentum_atr, _ = self.momentum_atr_tracker.update(bar.high, bar.low, bar.close)
        else:
            ma_f = self.ma_filter_tracker.line
            ma_s = self.ma_slope_tracker.line
            mg = self.mcginley_tracker.line
            vol_sma = self.vol_sma_tracker.sma
            adx = self.adx_tracker.adx
            chop = self.chop_tracker.chop
            fast_atr = self.atr_vol_floor_tracker.fast_atr
            base_atr = self.atr_vol_floor_tracker.baseline_atr
            macd_line = self.macd_tracker.macd_line
            macd_sig = self.macd_tracker.macd_signal
            macd_hist = self.macd_tracker.macd_hist
            prev_macd_hist = self.macd_tracker.prev_macd_hist
            momentum_atr = self.momentum_atr_tracker.fast_atr
        return ma_f, ma_s, mg, vol_sma, adx, chop, fast_atr, base_atr, macd_line, macd_sig, macd_hist, prev_macd_hist, momentum_atr

    def _evaluate_entry_gates(
        self,
        *,
        close: float,
        volume: float,
        high: float,
        low: float,
        ma_filter_line: float | None,
        ma_slope_line: float | None,
        ma_slope_prev_line: float | None,
        mcginley_line: float | None,
        vol_sma: float | None,
        adx: float | None,
        chop: float | None,
        fast_atr: float | None,
        baseline_atr: float | None,
        macd_line: float | None,
        macd_signal: float | None,
        macd_hist: float | None,
        prev_macd_hist: float | None,
        momentum_atr: float | None = None,
        bar: "Bar | None" = None,
        prev_bar: "Bar | None" = None,
    ) -> dict[str, object]:
        return {
            GATE_MA_FILTER: evaluate_ma_filter(self.config, close=close, ma_line=ma_filter_line),
            GATE_MA_SLOPE_FILTER: evaluate_ma_slope_filter(self.config, ma_line=ma_slope_line, prev_ma_line=ma_slope_prev_line),
            GATE_MCGINLEY_FILTER: evaluate_mcginley_filter(self.config, close=close, mcginley_line=mcginley_line),
            GATE_VOLUME_FILTER: evaluate_volume_filter(self.config, volume=volume, vol_sma=vol_sma),
            GATE_ADX_FILTER: evaluate_adx_filter(self.config, adx=adx),
            GATE_CHOP_FILTER: evaluate_chop_filter(self.config, chop=chop),
            GATE_ATR_VOL_FLOOR: evaluate_atr_vol_floor(self.config, atr=fast_atr, baseline_atr=baseline_atr),
            GATE_MACD_REGIME: evaluate_macd_regime(self.config, macd_line=macd_line),
            GATE_MACD_CROSS: evaluate_macd_cross(self.config, macd_line=macd_line, macd_signal=macd_signal),
            GATE_MACD_HIST: evaluate_macd_hist(self.config, macd_hist=macd_hist, prev_macd_hist=prev_macd_hist),
            GATE_MACD_ZERO_DIST: evaluate_macd_zero_dist(self.config, macd_line=macd_line),
            GATE_CANDLE_PATTERN: evaluate_candle_pattern_gate(
                self.config,
                recent_bars=list(self._candle_history),
            ),
            GATE_LEVEL_PROXIMITY: evaluate_level_proximity_gate(
                self.config,
                close=float(close),
                recent_highs=[b.high for b in self._level_prox_history],
                recent_lows=[b.low for b in self._level_prox_history],
            ),
            GATE_MOMENTUM_FILTER: evaluate_momentum_filter(
                self.config,
                bar_close=float(bar.close) if bar is not None else float(close),
                bar_open=float(bar.open) if bar is not None else float(close),
                prev_close=float(prev_bar.close) if prev_bar is not None else None,
                momentum_atr=momentum_atr,
            ),
            GATE_SESSION: evaluate_session_filter(
                self.config,
                bar_timestamp=bar.timestamp if bar is not None else None,
            ),
        }

    @staticmethod
    def _apply_entry_gates(raw: RawSignal, gate_results: dict[str, object]) -> RawSignal:
        long_ok = raw.long
        short_ok = raw.short
        for gate in gate_results.values():
            long_ok = long_ok and gate.long_ok
            short_ok = short_ok and gate.short_ok
        return RawSignal(
            long=long_ok,
            short=short_ok,
            reason=raw.reason,
            direction=raw.direction,
            line=raw.line,
        )

    def _entry_stop_price(self, *, bar: Bar, entry_price: float, is_long: bool) -> float | None:
        swing_reference = None
        if bool(self.config["use_sl"] and self.config["use_sl_swing_atr"]):
            swing_reference = find_swing_reference(
                self._swing_history,
                is_long=is_long,
                lookback=int(self.config["sl_swing_lookback"]),
                basis=str(self.config["sl_swing_basis"]),
            )

        return calc_sl(
            self.config,
            bar=bar,
            entry_price=entry_price,
            is_long=is_long,
            price_tick=self.instrument.price_tick,
            atr_value=self.stop_atr_tracker.atr,
            swing_reference=swing_reference,
            swing_atr_value=self.swing_sl_atr_tracker.atr,
        )

    def _entry_ready(self) -> bool:
        if not bool(self.config["use_sl"]):
            sl_ready = True
        elif bool(self.config["use_sl_atr"]):
            sl_ready = self.stop_atr_tracker.valid_bar and self.stop_atr_tracker.warmup_ready
        elif bool(self.config["use_sl_percent"]):
            sl_ready = True
        else:
            swing_ref_ready = len(self._swing_history) >= int(self.config["sl_swing_lookback"])
            sl_ready = (
                self.swing_sl_atr_tracker.valid_bar
                and self.swing_sl_atr_tracker.warmup_ready
                and swing_ref_ready
            )

        tp_mode = str(self.config["tp_mode"])
        if tp_mode == "None":
            tp_ready = True
        elif tp_mode == "ATR":
            tp_ready = self.tp_atr_tracker.valid_bar and self.tp_atr_tracker.warmup_ready
        elif tp_mode in {"Percent"}:
            tp_ready = True
        else:
            tp_ready = bool(self.config["use_sl"]) and sl_ready

        return sl_ready and tp_ready

    def _remember_tw_protective_exit(self, *, bar: Bar, reason: str) -> None:
        if reason != REASON_EXIT_OPP_SIGNAL:
            self._tw_last_protective_exit_bar_index = bar.bar_index

    def _tw_should_defer_reentry_after_protective_exit(self, *, bar: Bar) -> bool:
        if self.tw_audit_semantics_mode != "research":
            return False
        if self.tw_reversal_reentry_mode not in {
            "delay_after_protective_exit",
            "carry_to_next_bar_after_protective_exit",
        }:
            return False
        if self.tw_reversal_reentry_delay_bars <= 0:
            return False
        if self._tw_last_protective_exit_bar_index is None:
            return False
        bars_since_exit = bar.bar_index - self._tw_last_protective_exit_bar_index
        if self.tw_reversal_reentry_mode == "carry_to_next_bar_after_protective_exit":
            return bars_since_exit < self.tw_reversal_reentry_delay_bars
        return bars_since_exit <= self.tw_reversal_reentry_delay_bars

    def _tw_should_queue_next_bar_open_entry(self, *, bar: Bar) -> bool:
        if self.tw_audit_semantics_mode != "research":
            return False
        if self.tw_reversal_reentry_mode != "next_bar_open_after_protective_exit_signal":
            return False
        if self.tw_reversal_reentry_delay_bars <= 0:
            return False
        if self._tw_last_protective_exit_bar_index is None:
            return False
        bars_since_exit = bar.bar_index - self._tw_last_protective_exit_bar_index
        return 0 < bars_since_exit <= self.tw_reversal_reentry_delay_bars

    def _tw_should_queue_next_bar_close_entry(self, *, bar: Bar) -> bool:
        if self.tw_audit_semantics_mode != "research":
            return False
        if self.tw_reversal_reentry_mode != "next_bar_close_after_protective_exit_signal":
            return False
        if self.tw_reversal_reentry_delay_bars <= 0:
            return False
        if self._tw_last_protective_exit_bar_index is None:
            return False
        bars_since_exit = bar.bar_index - self._tw_last_protective_exit_bar_index
        return 0 < bars_since_exit <= self.tw_reversal_reentry_delay_bars

    def _maybe_execute_tw_pending_open_entry(self, *, bar: Bar, sizing_equity_snapshot: float) -> None:
        if self.tw_audit_semantics_mode != "research":
            return
        if self.tw_reversal_reentry_mode != "next_bar_open_after_protective_exit_signal":
            return
        if self.state.position is not None:
            return
        if self._tw_pending_open_side is None:
            return

        pending_side = self._tw_pending_open_side
        pending_reason = self._tw_pending_open_reason
        self._tw_pending_open_side = None
        self._tw_pending_open_reason = None

        is_long = pending_side == POSITION_SIDE_LONG
        entry_price = float(bar.open)
        entry_stop_price = self._entry_stop_price(bar=bar, entry_price=entry_price, is_long=is_long)
        entry_qty = self.position_sizer.calc_qty(
            entry_price,
            entry_stop_price,
            sizing_equity_snapshot,
            is_long,
            self.instrument,
            existing_position=self.state.position,
        )
        if entry_qty <= 0.0:
            return
        if self._entry_blocked_by_capital(
            entry_price=entry_price,
            side=pending_side,
            qty=entry_qty,
            sizing_equity=sizing_equity_snapshot,
        ):
            return

        initial_risk = self._initial_risk_for_entry(entry_price=entry_price, stop_price=entry_stop_price)
        active_tp_price, working_exits = build_working_exit_book(
            self.config,
            entry_price=entry_price,
            is_long=is_long,
            price_tick=self.instrument.price_tick,
            atr_value=self.tp_atr_tracker.atr,
            initial_risk_per_unit=initial_risk,
            book_version=1,
            completed_exit_ids=set(),
        )
        self.position_manager.open_position(
            bar=bar,
            side=pending_side,
            qty=entry_qty,
            state=self.state,
            reason=pending_reason,
            active_stop_price=entry_stop_price,
            active_tp_price=active_tp_price,
            working_exits=working_exits,
            fill_price=entry_price,
        )

    def _tw_pending_or_live_entry_decision(self, *, raw: RawSignal) -> EntryDecision:
        if (
            self.tw_audit_semantics_mode == "research"
            and self.tw_reversal_reentry_mode in {
                "carry_to_next_bar_after_protective_exit",
                "next_bar_close_after_protective_exit_signal",
            }
            and self.state.position is None
            and self._tw_pending_reentry_side is not None
            and self.state.closed_this_bar_reason is None
        ):
            return EntryDecision(
                True,
                side=self._tw_pending_reentry_side,
                reason=self._tw_pending_reentry_reason,
            )
        return self.position_manager.can_open_raw_signal(raw=raw, state=self.state)

    def _apply_tw_margin_call_semantics(self, *, bar: Bar) -> None:
        if self.state.position is None:
            return
        checkpoints = self._tw_margin_call_checkpoints(bar=bar)
        for checkpoint_price in checkpoints:
            if self.state.position is None:
                return
            exit_pct = self._tw_margin_call_exit_pct(mark_price=checkpoint_price)
            if exit_pct <= 0.0:
                continue
            self.position_manager.close_position(
                bar=bar,
                exit_price=checkpoint_price,
                reason=REASON_EXIT_MARGIN_CALL,
                state=self.state,
                exit_pct=exit_pct,
                exit_id=REASON_EXIT_MARGIN_CALL,
            )

    def _tw_margin_call_checkpoints(self, *, bar: Bar) -> list[float]:
        position = self.state.position
        if position is None:
            return []
        checkpoints: list[float] = [bar.open]
        if position.side == POSITION_SIDE_LONG:
            adverse_extreme = bar.low
            if adverse_extreme < checkpoints[-1]:
                checkpoints.append(adverse_extreme)
        else:
            adverse_extreme = bar.high
            if adverse_extreme > checkpoints[-1]:
                checkpoints.append(adverse_extreme)
        return checkpoints

    def _tw_margin_call_exit_pct(self, *, mark_price: float) -> float:
        position = self.state.position
        if position is None or position.qty <= 0.0:
            return 0.0
        margin_pct = self.margin_long_pct if position.side == POSITION_SIDE_LONG else self.margin_short_pct
        margin_frac = margin_pct / 100.0
        if margin_frac <= 0.0:
            return 0.0
        if position.side == POSITION_SIDE_LONG:
            unrealized = (mark_price - position.avg_entry_price) * position.qty * self.instrument.contract_multiplier
        else:
            unrealized = (position.avg_entry_price - mark_price) * position.qty * self.instrument.contract_multiplier
        equity_at_mark = self.state.initial_capital + self.state.realized_equity + unrealized
        required_margin = mark_price * position.qty * self.instrument.contract_multiplier * margin_frac
        deficit = required_margin - equity_at_mark
        if deficit <= 0.0:
            return 0.0
        # TradingView appears to liquidate ~4x the minimum under-margined amount.
        liquidation_qty = (deficit * 4.0) / (mark_price * self.instrument.contract_multiplier * margin_frac)
        liquidation_qty = min(position.qty, max(0.0, liquidation_qty))
        reference_qty = (
            position.working_exit_reference_qty
            if position.working_exit_reference_qty > 0.0
            else position.qty
        )
        if reference_qty <= 0.0:
            return 0.0
        return liquidation_qty / reference_qty

    @staticmethod
    def _initial_risk_for_entry(*, entry_price: float, stop_price: float | None) -> float | None:
        if stop_price is None:
            return None
        return abs(entry_price - stop_price)

    def _entry_blocked_by_capital(
        self, *, entry_price: float, side: str, qty: float, sizing_equity: float
    ) -> bool:
        if qty <= 0.0:
            return False

        margin_pct = self.margin_long_pct if side == POSITION_SIDE_LONG else self.margin_short_pct
        existing_qty = 0.0
        if self.state.position is not None and self.state.position.side == side:
            existing_qty = self.state.position.qty
        required_margin = (
            entry_price
            * (existing_qty + qty)
            * self.instrument.contract_multiplier
            * (margin_pct / 100.0)
        )
        # Use sizing_equity Ã— max_leverage_cap as the threshold, not self.state.equity.
        # PositionSizer.calc_qty already caps qty so that:
        #   qty â‰¤ (sizing_equity Ã— max_leverage_cap) / (price Ã— contract_mult)
        # Therefore required_margin â‰¤ sizing_equity Ã— max_leverage_cap.
        # Using self.state.equity would cause false blocks when equity drops after a
        # same-bar close (flip scenario) while qty was sized from the pre-close snapshot.
        return (sizing_equity * self.max_leverage_cap) < required_margin

    def _frozen_sizing_equity_snapshot(self, bar: Bar) -> float:
        realized_equity_value = self.state.initial_capital + self.state.realized_equity
        unrealized_pnl = 0.0
        if self.state.position is not None:
            mark_basis = self.state.position.avg_entry_price
            if self.state.position.side == POSITION_SIDE_LONG:
                unrealized_pnl = (
                    (bar.open - mark_basis)
                    * self.state.position.qty
                    * self.instrument.contract_multiplier
                )
            else:
                unrealized_pnl = (
                    (mark_basis - bar.open)
                    * self.state.position.qty
                    * self.instrument.contract_multiplier
                )
        self.state.unrealized_pnl = unrealized_pnl
        self.state.equity = realized_equity_value + unrealized_pnl
        # Sizing is fixed to realized equity snapshots; unrealized PnL remains
        # available for diagnostics/account state but no longer changes qty.
        return realized_equity_value

    @staticmethod
    def _candidate_side(raw: RawSignal) -> str | None:
        if raw.long == raw.short:
            return None
        return POSITION_SIDE_LONG if raw.long else POSITION_SIDE_SHORT

    def _force_reset_guard_state(self, realized_equity: float) -> None:
        """Force-reset the 4 self-blocking guard states so breach auto-clears after recovery."""
        self._l16_equity_peak = realized_equity
        self._l16_consec_loss_count = 0
        self._l16_mae_last = 0.0
        if self._l16_equity_sma is not None:
            self._l16_equity_sma = realized_equity * 0.999

    def set_gate_overrides(
        self,
        adx_map: dict[int, float] | None = None,
        chop_map: dict[int, float] | None = None,
        macd_htf_line_map: dict[int, float] | None = None,
        htf_trend_line_map: dict[int, float] | None = None,
        ma_filter_line_map: dict[int, float] | None = None,
        mcginley_line_map: dict[int, float] | None = None,
    ) -> None:
        self._override_adx_values = adx_map
        self._override_chop_values = chop_map
        self._override_macd_htf_line = macd_htf_line_map
        self._override_htf_trend_line = htf_trend_line_map
        self._override_ma_filter_line = ma_filter_line_map
        self._override_mcginley_line = mcginley_line_map

    @staticmethod
    def _override_series_value(series_map: dict[int, float] | None, bar_index: int) -> float | None:
        if series_map is None:
            return None
        value = series_map.get(bar_index)
        if value is None:
            return None
        return float(value)
    def _bar_is_valid(self, bar: Bar) -> bool:
        prices = (bar.open, bar.high, bar.low, bar.close)
        if not all(math.isfinite(price) for price in prices):
            return False
        if bar.high < bar.low:
            return False
        if bar.open < bar.low or bar.open > bar.high:
            return False
        if bar.close < bar.low or bar.close > bar.high:
            return False
        return True

    def _signal_indicator_snapshot(self, raw: RawSignal) -> SupertrendIndicatorSnapshot:
        indicator_snapshot = getattr(self.signal_producer, "indicator_snapshot", None)
        if callable(indicator_snapshot):
            snapshot = indicator_snapshot()
            if hasattr(snapshot, "supertrend"):
                return snapshot.supertrend
            if isinstance(snapshot, dict):
                return SupertrendIndicatorSnapshot(
                    line=snapshot.get("filter_line", raw.line),
                    direction=snapshot.get("direction", raw.direction),
                    valid_bar=raw.direction is not None or raw.line is not None,
                    warmup_ready=raw.direction is not None,
                )

        return SupertrendIndicatorSnapshot(
            line=raw.line,
            direction=raw.direction,
            valid_bar=raw.direction is not None or raw.line is not None,
            warmup_ready=raw.direction is not None,
        )

    def run_parity_rows(self, bars: Iterable[Bar]) -> list[str]:
        bar_list = list(bars)
        parity_config = {
            key: value
            for key, value in self.config.items()
            if key not in {"use_tp", "use_tp_single_atr", "use_tp_single_pct", "use_tp_single_r", "use_tp_multi"}
        }
        parity_runner = Runner(parity_config)
        return self.format_parity_rows(bar_list, parity_runner.run(bar_list))

    def run_l4_parity_rows(self, bars: Iterable[Bar]) -> list[str]:
        rows: list[str] = []
        for bar in bars:
            raw = self.run([bar])[0]
            rows.append(self.format_l4_parity_row(bar, raw, self.state))
        return rows

    @staticmethod
    def format_raw_signals(signals: Iterable[RawSignal]) -> list[str]:
        rows: list[str] = []
        for index, signal in enumerate(signals):
            pulse = "LONG" if signal.long else "SHORT" if signal.short else "-"
            direction = "na" if signal.direction is None else str(signal.direction)
            line = "na" if signal.line is None else f"{signal.line:.4f}"
            rows.append(
                f"{index:02d} | pulse={pulse:<5} | dir={direction:>2} | line={line:>8} | reason={signal.reason}"
            )
        return rows

    @staticmethod
    def format_parity_rows(bars: Iterable[Bar], signals: Iterable[RawSignal]) -> list[str]:
        bar_list = list(bars)
        signal_list = list(signals)

        if len(bar_list) != len(signal_list):
            raise ValueError("bars and signals length mismatch")

        rows: list[str] = []
        for bar, signal in zip(bar_list, signal_list):
            close = f"{bar.close:.2f}" if math.isfinite(bar.close) else "na"
            direction = "na" if signal.direction is None else str(signal.direction)
            rows.append(
                f"{bar.bar_index:02d} | c={close:>5} | d={direction:>2} | L={int(signal.long)} | S={int(signal.short)} | r={signal.reason}"
            )
        return rows

    @staticmethod
    def format_l4_parity_row(bar: Bar, signal: RawSignal, state: PortfolioState) -> str:
        supertrend_line = Runner._format_optional_float(state.indicator_snapshot.supertrend.line)
        direction = "na" if signal.direction is None else str(signal.direction)

        if state.position is None:
            position_side = "flat"
            entry_price = "na"
            avg_entry_price = "na"
            entry_bar = "na"
            qty = "0.0000"
            active_stop_price = "na"
            active_tp_price = "na"
            entry_count = "0"
            lifecycle_id = "0"
            book_version = "0"
        else:
            position_side = state.position.side
            entry_price = Runner._format_optional_float(state.position.entry_price)
            avg_entry_price = Runner._format_optional_float(state.position.avg_entry_price)
            entry_bar = f"{state.position.entry_bar:02d}"
            qty = f"{state.position.qty:.4f}"
            active_stop_price = Runner._format_optional_float(state.position.active_stop_price)
            active_tp_price = Runner._format_optional_float(state.position.active_tp_price)
            entry_count = str(len([leg for leg in state.position.entry_legs if leg.qty > 0.0]))
            lifecycle_id = str(state.position.lifecycle_id)
            book_version = str(state.position.working_exit_book_version)

        exit_reason = state.closed_this_bar_reason or "na"
        exit_bar = f"{bar.bar_index:02d}" if state.closed_this_bar_reason is not None else "na"
        exit_price = (
            Runner._format_optional_float(state.last_exit_price)
            if state.closed_this_bar_reason is not None
            else "na"
        )
        pessimistic = "1" if state.last_exit_was_pessimistic else "0"

        return (
            f"{bar.bar_index:02d} | ts={bar.timestamp.isoformat()} | c={bar.close:.4f} | "
            f"st={supertrend_line} | d={direction:>2} | L={int(signal.long)} | S={int(signal.short)} | "
            f"pos={position_side:<5} | ep={entry_price} | aep={avg_entry_price} | eb={entry_bar} | q={qty} | "
            f"ec={entry_count} | lc={lifecycle_id} | bv={book_version} | "
            f"sp={active_stop_price} | tp={active_tp_price} | xr={exit_reason} | xb={exit_bar} | xp={exit_price} | ps={pessimistic}"
        )

    @staticmethod
    def _format_optional_float(value: float | None) -> str:
        if value is None or not math.isfinite(value):
            return "na"
        return f"{value:.4f}"





