"""
MTC Default Configuration Parameters.

This module defines all MTC strategy default parameters matching
the MASTER_TEMPLATE_CORE.pine v2.2.0-LibRefactor defaults.
"""

from typing import Literal
from pydantic import BaseModel, Field, field_validator


class SupertrendConfig(BaseModel):
    """Supertrend signal module parameters."""
    
    atr_len: int = Field(default=21, ge=1, description="ATR length for Supertrend")
    factor: float = Field(default=4.0, ge=0.1, description="Supertrend factor/multiplier")
    use_wicks: bool = Field(default=True, description="Use High/Low instead of Close")
    use_ha: bool = Field(default=True, description="Use Heikin Ashi candles")


class RangeFilterConfig(BaseModel):
    """Range Filter Hybrid signal module parameters."""
    
    adx_trend_threshold: int = Field(default=25, ge=15, le=50)
    adx_range_threshold: int = Field(default=20, ge=10, le=30)
    chop_trend_threshold: int = Field(default=50, ge=30, le=70)
    chop_range_threshold: int = Field(default=62, ge=50, le=80)
    rsi_len: int = Field(default=14, ge=5, le=50)
    rsi_oversold: int = Field(default=30, ge=10, le=40)
    rsi_overbought: int = Field(default=70, ge=60, le=90)
    bb_len: int = Field(default=20, ge=10, le=50)
    bb_mult: float = Field(default=2.0, ge=1.0, le=3.0)
    use_bb_filter: bool = Field(default=True)


class ConfirmationConfig(BaseModel):
    """Confirmation Layer (swing break + momentum validation)."""

    enabled: bool = Field(default=False)
    # Legacy simplified fields retained for backward compatibility with older
    # configs/tests. Pine-parity runtime uses the explicit fields below.
    swing_lookback: int = Field(default=5, ge=2)
    momentum_len: int = Field(default=10, ge=1)
    momentum_threshold_pct: float = Field(default=0.0, ge=0.0)
    p_left: int = Field(default=7, ge=1)
    p_right: int = Field(default=7, ge=1)
    require_close_beyond: bool = Field(default=True)
    confirm_timeout_bars: int = Field(default=200, ge=1)
    min_wait_bars: int = Field(default=1, ge=0)
    gate_only_when_flat: bool = Field(default=False)
    dynamic_level_while_waiting: bool = Field(default=False)
    dyn_update_mode: Literal["ANY", "TIGHTEN_ONLY"] = Field(default="TIGHTEN_ONLY")
    defer_break_on_level_update: bool = Field(default=True)
    refresh_on_new_raw_signal: bool = Field(default=True)
    raw_event_mode: Literal["EDGE", "LEVEL"] = Field(default="EDGE")
    bar_close_only: bool = Field(default=True)
    require_raw_still_true: bool = Field(default=False)
    break_buffer_ticks: int = Field(default=0, ge=0)
    max_swing_distance_pct: float = Field(default=0.0, ge=0.0)
    max_pivot_age_bars: int = Field(default=0, ge=0)
    same_bar_tie_rule: Literal["LONG_WINS", "SHORT_WINS", "IGNORE"] = Field(default="LONG_WINS")
    use_momentum: bool = Field(default=False)
    momentum_mode: Literal["ATR_BODY", "ROC_1"] = Field(default="ATR_BODY")
    atr_len: int = Field(default=14, ge=1)
    mom_atr_mult: float = Field(default=0.30, ge=0.0)
    roc_min_pct: float = Field(default=0.15, ge=0.0)
    use_session_filter: bool = Field(default=False)
    session: str = Field(default="0000-2359")


class StopLossConfig(BaseModel):
    """Stop Loss configuration."""
    
    enabled: bool = Field(default=True, alias="use_sl")
    mode: Literal["ATR", "%", "Swing+ATR", "SWING_ATR"] = Field(default="ATR")
    atr_len: int = Field(default=14, ge=1)
    atr_mult: float = Field(default=4.0, ge=0.1)
    percent: float = Field(default=1.0, ge=0.1, description="SL % distance")
    
    # Swing SL settings
    swing_basis: Literal["Wick", "Body"] = Field(default="Wick")
    swing_lookback: int = Field(default=20, ge=1)
    swing_atr_len: int = Field(default=14, ge=1)
    swing_atr_mult: float = Field(default=0.5, ge=0.0)


class TakeProfitConfig(BaseModel):
    """Take Profit configuration."""
    
    enabled: bool = Field(default=True, alias="use_tp")
    mode: Literal["ATR", "%", "R"] = Field(default="ATR")
    atr_len: int = Field(default=14, ge=1)
    atr_mult: float = Field(default=3.0, ge=0.1)
    percent: float = Field(default=2.0, ge=0.1)
    rr: float = Field(default=2.0, ge=0.1, description="R-multiple for TP")


class BreakEvenConfig(BaseModel):
    """Break-Even configuration."""
    
    enabled: bool = Field(default=True, alias="use_break_even")
    rr: float = Field(default=1.0, ge=0.1, description="BE trigger R-multiple")
    buffer_r: float = Field(default=0.1, ge=0.0, description="BE buffer R-multiple")


class MultiTPConfig(BaseModel):
    """Multi-TP (2 targets) configuration."""
    
    enabled: bool = Field(default=True, alias="use_multi_tp")
    tp1_rr: float = Field(default=3.0, ge=0.1, description="TP1 R-multiple")
    tp1_pct: float = Field(default=50.0, ge=1, le=99, description="TP1 close %")
    tp2_rr: float = Field(default=5.5, ge=0.1, description="TP2 R-multiple")


class TrailingConfig(BaseModel):
    """Trailing Stop configuration."""
    
    enabled: bool = Field(default=True, alias="use_trailing")
    atr_len: int = Field(default=14, ge=1)
    start_r: float = Field(default=2.5, ge=0.1, description="Start after R-multiple")
    dist_r: float = Field(default=2.0, ge=0.1, description="Trail distance R-multiple")


class RiskConfig(BaseModel):
    """Risk management configuration."""
    
    risk_long_percent: float = Field(default=4.0, ge=0.01, description="Risk per long trade %")
    risk_short_percent: float = Field(default=3.0, ge=0.01, description="Risk per short trade %")
    max_leverage_cap: float = Field(default=5.0, ge=1.0, description="Max leverage limit")
    fallback_qty_pct: float = Field(default=5.0, ge=0.1, le=100.0)
    risk_equity_mode: Literal["Initial", "Realized"] = Field(default="Initial")
    use_notional_hard_assert: bool = Field(default=False)
    
    use_daily_loss_limit: bool = Field(default=False)
    max_daily_loss_percent: float = Field(default=5.0, ge=0.1)
    
    use_max_trades_per_day: bool = Field(default=False)
    max_trades_per_day: int = Field(default=5, ge=1)


class FilterConfig(BaseModel):
    """Filter configuration."""
    
    # MA Filter
    use_ma_filter: bool = Field(default=False)
    ma_type: Literal["SMA", "EMA", "DEMA", "TEMA", "RMA", "WMA", "VWMA", "KAMA"] = "EMA"
    ma_length: int = Field(default=200, ge=1)
    ma_use_higher_timeframe: bool = Field(default=False, description="Use HTF for MA calculation")
    ma_htf_timeframe: str = Field(default="60", description="HTF timeframe for MA filter")

    # MA Slope Filter
    use_ma_slope_filter: bool = Field(default=False)
    ma_slope_len: int = Field(default=200, ge=1)
    ma_slope_min_pct: float = Field(default=0.005, ge=0.0)
    
    # Volume Filter
    use_volume_filter: bool = Field(default=False)
    vol_filter_len: int = Field(default=50, ge=1)
    vol_filter_mult: float = Field(default=0.5, ge=0.1)
    
    # ATR Volatility Floor
    use_atr_vol_filter: bool = Field(default=False)
    atr_vol_len: int = Field(default=14, ge=1)
    atr_vol_smooth_len: int = Field(default=100, ge=2)
    atr_vol_floor_mult: float = Field(default=1.2, ge=0.1)

    # McGinley Dynamic Filter
    use_mcginley_filter: bool = Field(default=False)
    mcginley_len: int = Field(default=5, ge=1)
    mcginley_k: float = Field(default=0.6, gt=0.0)
    use_mcginley_htf: bool = Field(default=False)
    mcginley_htf_timeframe: str = Field(default="60")
    
    # HTF Trend Filter
    use_htf_trend_filter: bool = Field(default=False)
    htf_trend_timeframe: str = Field(default="240")
    htf_trend_ma_type: Literal["SMA", "EMA", "RMA", "WMA", "KAMA"] = "EMA"
    htf_trend_ma_len: int = Field(default=100, ge=1)
    htf_trend_buffer_pct: float = Field(default=0.1, ge=0.0)

    # MACD Filter Hub
    use_macd_filter: bool = Field(default=False)
    macd_gate_mode: Literal["Regime", "Cross-State", "Histogram", "Distance", "HTF Bias", "STANDARD", "PPO_NORM"] = Field(default="Regime")
    macd_source: Literal["close", "open", "hl2", "hlc3", "ohlc4"] = Field(default="close", description="Price source for MACD calculation")
    macd_fast_len: int = Field(default=12, ge=1)
    macd_slow_len: int = Field(default=26, ge=2)
    macd_signal_len: int = Field(default=9, ge=1)
    macd_distance_pct: float = Field(default=0.0, ge=0.0)
    macd_htf_timeframe: str = Field(default="240")
    macd_use_htf_bias: bool = Field(default=False, description="Enable HTF bias (regime) gating for STANDARD/PPO_NORM/other modes")

    @field_validator("htf_trend_timeframe", "macd_htf_timeframe", "mcginley_htf_timeframe", "ma_htf_timeframe", "adx_htf_timeframe", "chop_htf_timeframe", mode="before")
    @classmethod
    def _coerce_timeframe_to_str(cls, v):
        """JSON may contain int timeframes (e.g. 240 instead of '240')."""
        if isinstance(v, (int, float)):
            return str(int(v))
        return v

    # Range Regime Filter (ADX + Chop + hold bars, Pine-like hysteresis)
    use_range_filters: bool = Field(default=False)
    use_range_regime_filter: bool = Field(default=False)
    range_regime_adx_on: float = Field(default=25.0, ge=0.0)
    range_regime_adx_off: float = Field(default=20.0, ge=0.0)
    range_regime_chop_on: float = Field(default=50.0, ge=0.0)
    range_regime_chop_off: float = Field(default=62.0, ge=0.0)
    # Backward-compat aliases used by older case manifests.
    range_regime_adx_min: float = Field(default=20.0, ge=0.0)
    range_regime_chop_max: float = Field(default=62.0, ge=0.0)
    range_regime_hold_bars: int = Field(default=8, ge=0)
    range_agg_mode: Literal["AND", "COUNT"] = Field(default="AND")
    range_min_pass: int = Field(default=2, ge=1)
    # ADX / Choppiness indicator lengths (Pine: i_adxLen, i_chopLen)
    range_regime_adx_len: int = Field(default=14, ge=1, description="ADX indicator length")
    range_regime_chop_len: int = Field(default=14, ge=1, description="Choppiness indicator length")
    # ADX HTF
    adx_use_higher_timeframe: bool = Field(default=False, description="Use HTF for ADX calculation")
    adx_htf_timeframe: str = Field(default="240", description="HTF timeframe for ADX filter")
    # Chop HTF
    chop_use_higher_timeframe: bool = Field(default=False, description="Use HTF for Choppiness calculation")
    chop_htf_timeframe: str = Field(default="240", description="HTF timeframe for Choppiness filter")


class GuardConfig(BaseModel):
    """Guard filters configuration."""
    
    # Max Drawdown Guard
    use_dd_guard: bool = Field(default=False)
    dd_guard_pct: float = Field(default=10.0, ge=0.1)
    
    # Consecutive Loss Guard
    use_consec_loss_guard: bool = Field(default=False)
    consec_loss_max: int = Field(default=3, ge=1)
    # Pine default is ON (legacy behavior): reset loss streak at day boundary.
    consec_loss_reset_daily: bool = Field(default=True)
    
    # Cooldown Guard
    use_cooldown_guard: bool = Field(default=False)
    cooldown_bars: int = Field(default=5, ge=1)
    
    # Equity Curve Filter
    use_eq_curve_guard: bool = Field(default=False)
    eq_curve_ma_len: int = Field(default=5, ge=5)
    
    # MAE Guard
    use_mae_guard: bool = Field(default=False)
    mae_max_pct: float = Field(default=2.0, ge=0.1)

    # Guard Recovery (bars/signals/virtual trade)
    use_guard_recovery: bool = Field(default=False)
    guard_recovery_mode: Literal["Bars", "Signals", "Virtual Trade", "Manual"] = Field(default="Bars")
    guard_recovery_bars: int = Field(default=3, ge=1)
    guard_recovery_signals: int = Field(default=2, ge=1)


class TimeStopConfig(BaseModel):
    """Time Stop (Position Duration Exit) configuration."""

    enabled: bool = Field(default=False, description="Exit after specified duration")
    use_bars: bool = Field(default=False, description="Enable bar-count exit (Position Duration Bars)")
    bars: int = Field(default=50, ge=1, description="Exit after this many bars")
    eod: bool = Field(default=False, description="Exit at end of day")
    eow: bool = Field(default=False, description="Exit at end of week")
    condition: Literal["Always", "Profit Only", "Loss Only"] = Field(default="Always")
    timezone: str = Field(
        default="UTC",
        description="Calendar timezone for EOD/EOW detection (e.g., Europe/London)",
    )


class ExitFilterBlockConfig(BaseModel):
    """Per-filter granular exit triggers (Pine grpExitFilterBlock)."""

    exit_on_ma_block: bool = Field(default=False)
    exit_on_ma_slope_block: bool = Field(default=False)
    exit_on_mcginley_block: bool = Field(default=False)
    exit_on_htf_trend_block: bool = Field(default=False)
    exit_on_vol_part_block: bool = Field(default=False, alias="exit_on_vol_block")
    exit_on_atr_vol_block: bool = Field(default=False)
    exit_on_range_block: bool = Field(default=False)


class TradeConfig(BaseModel):
    """Trade direction and entry configuration."""

    enable_long: bool = Field(default=True)
    enable_short: bool = Field(default=True)
    allow_flip: bool = Field(default=True)
    exit_on_opposite_signal: bool = Field(default=False)
    exit_on_filter_block: bool = Field(default=False)
    use_regime_lock: bool = Field(default=False)
    entry_mode: Literal["Edge", "Signal"] = Field(default="Signal")

    # Pyramiding
    max_pyramid_positions: int = Field(default=1, ge=1, le=5)
    signal_mode_max_entries: int = Field(default=1, ge=1, le=3)
    signal_mode_cooldown_bars: int = Field(default=10, ge=1)

    # Same-bar re-entry (Pine parity: process_orders_on_close=true)
    # When True, if a position exits during bar processing, a new entry
    # is allowed on the SAME bar.  This matches TradingView's behavior
    # where strategy.close() + strategy.entry() execute in one bar.
    allow_same_bar_reentry: bool = Field(
        default=True,
        description="Allow new entry on a bar where an exit just occurred",
    )
    same_bar_reentry_requires_exit: bool = Field(
        default=True,
        description="Re-entry only when an actual exit fired this bar (not just flat)",
    )
    same_bar_reentry_max_per_bar: int = Field(
        default=1, ge=1, le=3,
        description="Max new entries allowed per bar after an exit",
    )

    # First-bar edge gate (TV parity):
    # TradingView appears to require an edge transition (direction change)
    # before placing the first entry when a backtest starts.  Level signals
    # that are already active at backtest start do NOT trigger an entry.
    first_bar_requires_edge: bool = Field(
        default=False,
        description="Block first eval-bar entry unless an edge transition occurs",
    )


class StrategyConfig(BaseModel):
    """Strategy-level configuration."""

    initial_capital: float = Field(default=10000.0, ge=100.0)
    # TradingView strategy() defaults in MASTER_TEMPLATE_CORE.pine:
    # margin_long=1, margin_short=1
    margin_long_percent: float = Field(default=1.0, gt=0.0, le=100.0)
    margin_short_percent: float = Field(default=1.0, gt=0.0, le=100.0)
    commission_percent: float = Field(default=0.04, ge=0.0)
    slippage_ticks: int = Field(default=5, ge=0)
    mintick: float = Field(
        default=0.1,
        gt=0.0,
        description="Instrument minimum tick size used for slippage/sizing parity",
    )
    pyramiding: int = Field(default=1, ge=1)
    close_open_at_end: bool = Field(
        default=False,
        description=(
            "Close any open position at backtest end with MANUAL exit. "
            "When False (default), open positions are left as-is (TV parity)."
        ),
    )


class ParityConfig(BaseModel):
    """Deterministic parity configuration for Pine vs Python alignment."""

    enabled: bool = Field(
        default=False,
        description="Enable strict Pine parity mode and deterministic fill contract",
    )
    fill_contract: Literal["touch", "close"] = Field(
        default="touch",
        description="Exit detection mode: touch=OHLC touch rules, close=close-based exits",
    )
    export_debug_csv: bool = Field(
        default=False,
        description="Export debug_python_trades.csv and debug_python_signals.csv after run",
    )
    debug_dir: str = Field(default="debug", description="Debug export directory")
    preroll_days: int = Field(
        default=90,
        ge=0,
        description=(
            "Default preroll days for indicator warmup. RMA-based indicators "
            "(ATR, Supertrend) need long history to converge with TradingView. "
            "90 days ≈ 8640 bars @15m — sufficient for RMA convergence."
        ),
    )
    preroll_mode: Literal["warmup_only", "trade"] = Field(
        default="warmup_only",
        description=(
            "How preroll bars are handled:\n"
            "  warmup_only (DEFAULT): indicators compute normally but NO trading "
            "    actions occur — engine stays FLAT throughout preroll. Eval window "
            "    always starts from a clean FLAT state (TradingView parity).\n"
            "  trade: preroll bars allow trading (legacy/research mode). Positions "
            "    may carry into the eval window."
        ),
    )
    close_open_at_eval_start: bool = Field(
        default=True,
        description=(
            "Only relevant when preroll_mode='trade'. If True and a position is "
            "open when the eval window starts, force-close it with reason "
            "EVAL_START_FLATTEN so the eval window begins FLAT."
        ),
    )
    force_terminal_manual_close: bool = Field(
        default=True,
        description=(
            "When parity mode is enabled, force-close any still-open position at "
            "eval-window end with MANUAL. Keep True for the locked parity suite; "
            "set False only for workbook variants whose TV export omits terminal "
            "open-trade flattening."
        ),
    )


class MTCConfig(BaseModel):
    """
    Complete MTC Strategy Configuration.
    
    Mirrors all inputs from MASTER_TEMPLATE_CORE.pine v2.2.0-LibRefactor.
    """
    
    # Signal mode selection
    # NOTE: Pine default is "Range Filter Hybrid (ADX+Chop+BB)" but that module
    # is NOT yet implemented in Python. Using "Supertrend" as Python default.
    # Change to match Pine once Range Filter is ported.
    signal_mode: Literal["Supertrend", "Range Filter Hybrid", "Range Filter Hybrid (ADX+Chop+BB)", "None"] = "Supertrend"
    
    # Module configs
    supertrend: SupertrendConfig = Field(default_factory=SupertrendConfig)
    range_filter: RangeFilterConfig = Field(default_factory=RangeFilterConfig)
    confirmation: ConfirmationConfig = Field(default_factory=ConfirmationConfig)
    
    # Trade settings
    trade: TradeConfig = Field(default_factory=TradeConfig)

    # Time Stop
    time_stop: TimeStopConfig = Field(default_factory=TimeStopConfig)

    # Per-filter exit triggers
    exit_filter_block: ExitFilterBlockConfig = Field(default_factory=ExitFilterBlockConfig)

    # Risk management
    risk: RiskConfig = Field(default_factory=RiskConfig)
    
    # SL/TP/BE/Multi-TP/Trailing
    stop_loss: StopLossConfig = Field(default_factory=StopLossConfig)
    take_profit: TakeProfitConfig = Field(default_factory=TakeProfitConfig)
    break_even: BreakEvenConfig = Field(default_factory=BreakEvenConfig)
    multi_tp: MultiTPConfig = Field(default_factory=MultiTPConfig)
    trailing: TrailingConfig = Field(default_factory=TrailingConfig)
    
    # Filters & Guards
    filters: FilterConfig = Field(default_factory=FilterConfig)
    guards: GuardConfig = Field(default_factory=GuardConfig)
    
    # Strategy settings
    strategy: StrategyConfig = Field(default_factory=StrategyConfig)
    
    # Pine↔Python parity controls
    parity: ParityConfig = Field(default_factory=ParityConfig)
    
    class Config:
        populate_by_name = True


def get_default_config() -> MTCConfig:
    """Get default MTC configuration matching Pine Script defaults."""
    return MTCConfig()


def config_to_dict(config: MTCConfig) -> dict:
    """Convert config to flat dictionary for optimization."""
    return config.model_dump()


def dict_to_config(d: dict) -> MTCConfig:
    """Create config from flat dictionary."""
    return MTCConfig.model_validate(d)
