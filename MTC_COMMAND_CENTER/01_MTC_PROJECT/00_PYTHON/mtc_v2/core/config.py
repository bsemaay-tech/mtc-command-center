from __future__ import annotations

import math
from typing import Any


SIGNAL_MODE_SUPERTREND = "Supertrend"
SIGNAL_MODE_RANGE_FILTER = "Range Filter"
SUPPORTED_SIGNAL_MODES = {SIGNAL_MODE_SUPERTREND, SIGNAL_MODE_RANGE_FILTER}
EXECUTION_PROFILE_RAW_CLOSE_ONLY = "raw_close_only_v1"
EXECUTION_PROFILE_CLOSE_ONLY_DETERMINISTIC = "close_only_deterministic_v2"
SUPPORTED_EXECUTION_PROFILES = {
    EXECUTION_PROFILE_RAW_CLOSE_ONLY,
    EXECUTION_PROFILE_CLOSE_ONLY_DETERMINISTIC,
}
SUPPORTED_MA_TYPES = {"EMA", "SMA", "WMA", "RMA"}

TP_MODE_NONE = "None"
TP_MODE_ATR = "ATR"
TP_MODE_PERCENT = "Percent"
TP_MODE_R = "R"
TP_MODE_MULTI = "Multi-TP"

SL_BASIS_WICK = "Wick"
SL_BASIS_CLOSE = "Close"


DEFAULT_CONFIG: dict[str, object] = {
    "enable_long": True,
    "enable_short": True,
    "allow_flip": True,
    "regime_lock": False,
    "max_entries": 1,
    "cooldown_bars": 0,
    "warmup_bars_override": None,
    "debug_mode": False,
    "signal_mode": SIGNAL_MODE_SUPERTREND,
    "st_atr_len": 21,
    "st_factor": 4.0,
    "st_use_wicks": False,
    "st_use_ha": False,
    "rf_range": 1000.0,
    "instrument_symbol": "UNKNOWN",
    "instrument_point_value": 1.0,
    "instrument_price_tick": 0.01,
    "instrument_qty_step": 1.0,
    "instrument_min_qty": 0.0,
    "instrument_min_notional": 0.0,
    "instrument_contract_multiplier": 1.0,
    "initial_capital": 1_000_000_000_000.0,
    # Broker margin defaults are auto-derived from max_leverage_cap unless
    # explicit values are passed in config/export overrides.
    "margin_long_pct": 100.0,
    "margin_short_pct": 100.0,
    "execution_profile_id": EXECUTION_PROFILE_CLOSE_ONLY_DETERMINISTIC,
    # TradingView execution-parity research knobs (default-off; no runtime impact
    # until semantic owners are implemented).
    "tw_audit_semantics_mode": "off",
    "tw_reversal_reentry_mode": "local",
    "tw_reversal_reentry_delay_bars": 0,
    "tw_margin_call_mode": "off",
    "tw_margin_call_split_entries": False,
    "tw_be_semantics_mode": "local",
    "tw_trailing_semantics_mode": "local",
    "fixed_qty": 1.0,
    "risk_per_long_pct": 1.0,
    "risk_per_short_pct": 1.0,
    "fallback_size_pct": 10.0,
    "max_leverage_cap": 1.0,
    "equity_source": "Realized",
    "use_notional_assert": False,
    "use_ma_filter": False,
    "ma_type": "EMA",
    "ma_length": 200,
    "use_ma_mtf": False,
    "ma_htf_timeframe": "60",
    # L12 — HTF Trend Filter
    "use_htf_trend_filter": False,
    "htf_trend_timeframe": "240",
    "htf_trend_ma_type": "EMA",
    "htf_trend_ma_len": 100,
    "htf_trend_buffer_pct": 0.1,
    "use_ma_slope_filter": False,
    "ma_slope_len": 200,
    "ma_slope_min_pct": 0.005,
    "use_mcginley_filter": False,
    "mcginley_length": 200,
    "mcginley_use_higher_timeframe": False,
    "mcginley_htf_timeframe": "240",
    "use_volume_filter": False,
    "vol_sma_length": 20,
    "vol_sma_mult": 1.0,
    "use_adx_filter": False,
    "adx_length": 14,
    "adx_threshold": 25.0,
    "adx_use_higher_timeframe": False,
    "adx_htf_timeframe": "240",
    "use_chop_filter": False,
    "chop_length": 14,
    "chop_threshold": 61.8,
    "chop_use_higher_timeframe": False,
    "chop_htf_timeframe": "240",
    "use_atr_vol_floor": False,
    "atr_vol_floor_fast_len": 14,
    "atr_vol_floor_baseline_len": 100,
    "atr_vol_floor_mult": 0.5,
    "use_macd_regime_filter": False,
    "use_macd_cross_filter": False,
    "use_macd_hist_filter": False,
    "macd_hist_mode": "POSITIVE",
    "use_macd_zero_dist_filter": False,
    "macd_zero_dist_min": 0.0,
    "macd_fast_len": 12,
    "macd_slow_len": 26,
    "macd_sig_len": 9,
    "macd_source": "close",
    "use_macd_htf_bias": False,
    "macd_htf_timeframe": "240",
    # L12 — Momentum Filter
    "use_momentum_filter": False,
    "momentum_mode": "ATR_BODY",
    "momentum_atr_len": 14,
    "momentum_atr_mult": 0.30,
    "momentum_roc_min_pct": 0.15,
    # L12 — Session Filter
    "use_session_filter": False,
    "session_name": "New York",
    "session_custom_string": "0930-1600:America/New_York",
    # L13 - Opposite Signal Exit
    "exit_on_opposite_signal": True,
    # L14 - Filter Block Exits
    # Architecture requires "exit_on_filter_block" as a master toggle.
    # DEFERRED: master toggle enforcement is pending Pine-side implementation.
    # Current behaviour: each sub-toggle works independently (master toggle not enforced).
    # "exit_on_filter_block": False,  # placeholder — not yet enforced as master gate
    "exit_on_ma_block": False,
    "exit_on_ma_slope_block": False,
    "exit_on_mcginley_block": False,
    "exit_on_htf_trend_block": False,
    "exit_on_vol_block": False,
    "exit_on_atr_vol_block": False,
    "exit_on_range_block": False,     # ADX/Chop range-regime bloklarinin OR'u
    "exit_on_candle_pattern_block": False,
    "exit_on_level_prox_block": False,
    # L22 - Candle Pattern Gate
    "use_candle_pattern_gate": False,
    "candle_pattern_lookback": 5,
    # L20 - Level Proximity Gate
    "use_level_proximity_gate": False,
    "level_proximity_threshold_pct": 0.5,
    "level_proximity_lookback": 50,
    # L15 - Time-based Exits
    "use_time_stop": False,
    "time_stop_bars": 50,
    "time_stop_condition": "Always",  # Always | Profit Only | Loss Only
    "time_stop_eod": False,
    "time_stop_eow": False,
    # L16 - Guards
    "use_daily_loss_limit": False,
    "max_daily_loss_pct": 2.0,
    "use_max_trades_per_day": False,
    "max_trades_per_day": 3,
    "use_max_drawdown_guard": False,
    "max_drawdown_pct": 10.0,
    "use_consecutive_loss_halt": False,
    "max_consecutive_losses": 3,
    "use_equity_curve_filter": False,
    "equity_ma_length": 20,
    "use_mae_guard": False,
    "max_mae_pct": 2.0,
    # L16 - Trade Cooldown After Exit
    "use_trade_cooldown": False,
    "cooldown_bars_after_exit": 5,
    # L16 - Guard Recovery
    "use_guard_recovery": False,
    "guard_recovery_mode": "Bars",    # "Bars" | "Signals"
    "guard_recovery_bars": 20,
    "guard_recovery_signals": 2,
    # L18 - Confirmation Transform
    "use_confirm_transform": False,
    "confirm_bars": 1,
    "confirm_close_crosses": True,
    # L18b - Advanced Confirmation (V1 swing-break + momentum port scaffold)
    "use_l18b_confirmation": False,
    "l18b_swing_left": 2,
    "l18b_swing_right": 2,
    "l18b_timeout_bars": 20,
    "l18b_min_wait_bars": 1,
    "l18b_dynamic_level_while_waiting": False,
    "l18b_require_close_beyond": True,
    "l18b_close_buffer_pct": 0.0,
    "l18b_raw_event_mode": "EDGE",
    "l18b_tie_rule": "IGNORE",
    "l18b_use_momentum": True,
    "l18b_momentum_mode": "ATR_BODY",
    "l18b_confirm_session_filter": False,
    "l18b_refresh_on_new_raw": False,
    # L18b - Advanced Confirmation options
    "require_raw_still_true": False,  # raw must be active on confirmation bar
    "refresh_on_new_raw": False,      # reset count on new raw same-direction signal
    # L21 - Level Retest Transform
    "use_level_retest": False,
    "retest_timeout_bars": 50,
    "retest_buffer_pct": 0.1,
    # SL/TP
    "use_sl": True,
    "use_sl_atr": True,
    "use_sl_percent": False,
    "use_sl_swing_atr": False,
    "sl_atr_len": 14,
    "sl_atr_mult": 2.0,
    "sl_percent": 1.0,
    "sl_swing_basis": SL_BASIS_WICK,
    "sl_swing_lookback": 20,
    "sl_swing_atr_len": 14,
    "sl_swing_atr_mult": 0.5,
    "tp_mode": TP_MODE_NONE,
    "tp_atr_len": 14,
    "tp_atr_mult": 3.0,
    "tp_percent": 3.0,
    "tp_r_multiple": 2.0,
    "tp1_r_multiple": 3.0,
    "tp1_close_pct": 50.0,
    "tp2_r_multiple": 5.5,
    # L25 - WunderTrading
    "wt_enter_long_code":   "",
    "wt_exit_long_code":    "",
    "wt_enter_short_code":  "",
    "wt_exit_short_code":   "",
    "wt_exit_all_code":     "",
    "wt_order_type":        "market",
    "wt_amount_type":       "quote",
    "wt_amount":            100.0,
    "wt_leverage":          1,
    "wt_use_tp":            False,
    "wt_use_sl":            False,
    "wt_reduce_only":       True,
    "wt_place_cond_orders": False,
    "use_break_even": False,
    "be_trigger_r": 1.0,
    "be_buffer_r": 0.1,
    "use_trailing": False,
    "trail_atr_len": 14,
    "trail_start_r": 2.0,
    "trail_distance_atr_mult": 1.0,
}


def validate_config(config: dict[str, object]) -> None:
    required_keys = set(DEFAULT_CONFIG.keys())
    unknown = set(config.keys()) - required_keys
    if unknown:
        raise ValueError(f"Unknown config keys: {sorted(unknown)}")

    merged = resolve_config(config, validate=False)

    _require_bool(merged, "enable_long")
    _require_bool(merged, "enable_short")
    _require_bool(merged, "allow_flip")
    _require_bool(merged, "regime_lock")
    _require_optional_int(merged, "warmup_bars_override")
    _require_bool(merged, "debug_mode")
    _require_int(merged, "max_entries", minimum=1)
    _require_int(merged, "cooldown_bars", minimum=0)
    _require_str(merged, "signal_mode")
    _require_int(merged, "st_atr_len", minimum=1)
    _require_number(merged, "st_factor", greater_than=0.0)
    _require_bool(merged, "st_use_wicks")
    _require_bool(merged, "st_use_ha")
    _require_number(merged, "rf_range", greater_than=0.0)
    _require_str(merged, "instrument_symbol")
    _require_number(merged, "instrument_point_value", greater_than=0.0)
    _require_number(merged, "instrument_price_tick", greater_than=0.0)
    _require_number(merged, "instrument_qty_step", greater_than=0.0)
    _require_number(merged, "instrument_min_qty", minimum=0.0)
    _require_number(merged, "instrument_min_notional", minimum=0.0)
    _require_number(merged, "instrument_contract_multiplier", greater_than=0.0)
    _require_number(merged, "initial_capital", greater_than=0.0)
    _require_number(merged, "margin_long_pct", greater_than=0.0)
    _require_number(merged, "margin_short_pct", greater_than=0.0)
    _require_str(merged, "execution_profile_id")
    _require_str(merged, "tw_audit_semantics_mode")
    _require_str(merged, "tw_reversal_reentry_mode")
    _require_int(merged, "tw_reversal_reentry_delay_bars", minimum=0)
    _require_str(merged, "tw_margin_call_mode")
    _require_bool(merged, "tw_margin_call_split_entries")
    _require_str(merged, "tw_be_semantics_mode")
    _require_str(merged, "tw_trailing_semantics_mode")
    _require_number(merged, "fixed_qty", greater_than=0.0)
    _require_number(merged, "risk_per_long_pct", minimum=0.0)
    _require_number(merged, "risk_per_short_pct", minimum=0.0)
    _require_number(merged, "fallback_size_pct", minimum=0.0)
    _require_number(merged, "max_leverage_cap", greater_than=0.0)
    _require_bool(merged, "use_notional_assert")
    _require_bool(merged, "use_ma_filter")
    _require_str(merged, "ma_type")
    _require_int(merged, "ma_length", minimum=1)
    _require_bool(merged, "use_ma_mtf")
    _require_str(merged, "ma_htf_timeframe")
    # L12 — HTF Trend Filter
    _require_bool(merged, "use_htf_trend_filter")
    _require_str(merged, "htf_trend_timeframe")
    _require_str(merged, "htf_trend_ma_type")
    _require_int(merged, "htf_trend_ma_len", minimum=1)
    _require_number(merged, "htf_trend_buffer_pct", minimum=0.0)
    _require_bool(merged, "use_ma_slope_filter")
    _require_int(merged, "ma_slope_len", minimum=1)
    _require_number(merged, "ma_slope_min_pct", minimum=0.0)
    _require_bool(merged, "use_mcginley_filter")
    _require_int(merged, "mcginley_length", minimum=1)
    _require_bool(merged, "mcginley_use_higher_timeframe")
    _require_str(merged, "mcginley_htf_timeframe")
    _require_bool(merged, "use_volume_filter")
    _require_int(merged, "vol_sma_length", minimum=1)
    _require_number(merged, "vol_sma_mult", minimum=0.0)
    _require_bool(merged, "use_adx_filter")
    _require_int(merged, "adx_length", minimum=1)
    _require_number(merged, "adx_threshold", minimum=0.0)
    _require_bool(merged, "adx_use_higher_timeframe")
    _require_str(merged, "adx_htf_timeframe")
    _require_bool(merged, "use_chop_filter")
    _require_int(merged, "chop_length", minimum=2)
    _require_number(merged, "chop_threshold", minimum=0.0)
    _require_bool(merged, "chop_use_higher_timeframe")
    _require_str(merged, "chop_htf_timeframe")
    _require_bool(merged, "use_atr_vol_floor")
    _require_int(merged, "atr_vol_floor_fast_len", minimum=1)
    _require_int(merged, "atr_vol_floor_baseline_len", minimum=1)
    _require_number(merged, "atr_vol_floor_mult", minimum=0.0)
    _require_bool(merged, "use_macd_regime_filter")
    _require_bool(merged, "use_macd_cross_filter")
    _require_bool(merged, "use_macd_hist_filter")
    _require_str(merged, "macd_hist_mode")
    _require_bool(merged, "use_macd_zero_dist_filter")
    _require_number(merged, "macd_zero_dist_min", minimum=0.0)
    _require_int(merged, "macd_fast_len", minimum=1)
    _require_int(merged, "macd_slow_len", minimum=1)
    _require_int(merged, "macd_sig_len", minimum=1)
    _VALID_MACD_SOURCES = {"close", "open", "hl2", "hlc3", "ohlc4"}
    if str(merged["macd_source"]) not in _VALID_MACD_SOURCES:
        raise ValueError(f"macd_source must be one of: {sorted(_VALID_MACD_SOURCES)}")
    _require_bool(merged, "use_macd_htf_bias")
    # L12 — Momentum Filter
    _require_bool(merged, "use_momentum_filter")
    _require_str(merged, "momentum_mode")
    _require_int(merged, "momentum_atr_len", minimum=1)
    _require_number(merged, "momentum_atr_mult", minimum=0.0)
    _require_number(merged, "momentum_roc_min_pct", minimum=0.0)
    if merged["momentum_mode"] not in {"ATR_BODY", "ROC"}:
        raise ValueError("momentum_mode must be 'ATR_BODY' or 'ROC'")
    # L12 — Session Filter
    _require_bool(merged, "use_session_filter")
    _require_str(merged, "session_name")
    _require_str(merged, "session_custom_string")
    _VALID_SESSIONS = {"New York", "London", "Asia", "Sydney", "Custom"}
    if merged["session_name"] not in _VALID_SESSIONS:
        raise ValueError(f"session_name must be one of: {sorted(_VALID_SESSIONS)}")
    # L14
    _require_bool(merged, "exit_on_ma_block")
    _require_bool(merged, "exit_on_ma_slope_block")
    _require_bool(merged, "exit_on_mcginley_block")
    _require_bool(merged, "exit_on_htf_trend_block")
    _require_bool(merged, "exit_on_vol_block")
    _require_bool(merged, "exit_on_atr_vol_block")
    _require_bool(merged, "exit_on_range_block")
    _require_bool(merged, "exit_on_candle_pattern_block")
    _require_bool(merged, "exit_on_level_prox_block")
    _require_bool(merged, "use_candle_pattern_gate")
    _require_bool(merged, "use_level_proximity_gate")
    _require_number(merged, "level_proximity_threshold_pct", minimum=0.0)
    _require_int(merged, "level_proximity_lookback", minimum=1)
    # L15
    _require_bool(merged, "use_time_stop")
    _require_int(merged, "time_stop_bars", minimum=1)
    _require_str(merged, "time_stop_condition")
    _require_bool(merged, "time_stop_eod")
    _require_bool(merged, "time_stop_eow")
    # L16
    _require_bool(merged, "use_daily_loss_limit")
    _require_number(merged, "max_daily_loss_pct", minimum=0.0)
    _require_bool(merged, "use_max_trades_per_day")
    _require_int(merged, "max_trades_per_day", minimum=1)
    _require_bool(merged, "use_max_drawdown_guard")
    _require_number(merged, "max_drawdown_pct", minimum=0.0)
    _require_bool(merged, "use_consecutive_loss_halt")
    _require_int(merged, "max_consecutive_losses", minimum=1)
    _require_bool(merged, "use_equity_curve_filter")
    _require_int(merged, "equity_ma_length", minimum=1)
    _require_bool(merged, "use_mae_guard")
    _require_number(merged, "max_mae_pct", minimum=0.0)
    # L16 - Trade Cooldown
    _require_bool(merged, "use_trade_cooldown")
    _require_int(merged, "cooldown_bars_after_exit", minimum=1)
    _require_bool(merged, "use_guard_recovery")
    _require_str(merged, "guard_recovery_mode")
    _require_int(merged, "guard_recovery_bars", minimum=1)
    _require_int(merged, "guard_recovery_signals", minimum=1)
    # L18
    _require_bool(merged, "use_confirm_transform")
    _require_int(merged, "confirm_bars", minimum=1)
    _require_bool(merged, "confirm_close_crosses")
    # L18b
    _require_bool(merged, "use_l18b_confirmation")
    _require_int(merged, "l18b_swing_left", minimum=1)
    _require_int(merged, "l18b_swing_right", minimum=1)
    _require_int(merged, "l18b_timeout_bars", minimum=1)
    _require_int(merged, "l18b_min_wait_bars", minimum=0)
    _require_bool(merged, "l18b_dynamic_level_while_waiting")
    _require_bool(merged, "l18b_require_close_beyond")
    _require_number(merged, "l18b_close_buffer_pct", minimum=0.0)
    _require_str(merged, "l18b_raw_event_mode")
    _require_str(merged, "l18b_tie_rule")
    _require_bool(merged, "l18b_use_momentum")
    _require_str(merged, "l18b_momentum_mode")
    _require_bool(merged, "l18b_confirm_session_filter")
    _require_bool(merged, "l18b_refresh_on_new_raw")
    _require_bool(merged, "require_raw_still_true")
    _require_bool(merged, "refresh_on_new_raw")
    # L21
    _require_bool(merged, "use_level_retest")
    _require_int(merged, "retest_timeout_bars", minimum=1)
    _require_number(merged, "retest_buffer_pct", minimum=0.0)
    # SL/TP
    _require_bool(merged, "use_sl")
    _require_bool(merged, "use_sl_atr")
    _require_bool(merged, "use_sl_percent")
    _require_bool(merged, "use_sl_swing_atr")
    _require_int(merged, "sl_atr_len", minimum=1)
    _require_number(merged, "sl_atr_mult", greater_than=0.0)
    _require_number(merged, "sl_percent", greater_than=0.0)
    _require_str(merged, "sl_swing_basis")
    _require_int(merged, "sl_swing_lookback", minimum=1)
    _require_int(merged, "sl_swing_atr_len", minimum=1)
    _require_number(merged, "sl_swing_atr_mult", greater_than=0.0)
    _require_str(merged, "tp_mode")
    _require_int(merged, "tp_atr_len", minimum=1)
    _require_number(merged, "tp_atr_mult", greater_than=0.0)
    _require_number(merged, "tp_percent", greater_than=0.0)
    _require_number(merged, "tp_r_multiple", greater_than=0.0)
    _require_number(merged, "tp1_r_multiple", greater_than=0.0)
    _require_number(merged, "tp1_close_pct", greater_than=0.0)
    _require_number(merged, "tp2_r_multiple", greater_than=0.0)
    _require_bool(merged, "use_break_even")
    _require_number(merged, "be_trigger_r", greater_than=0.0)
    _require_number(merged, "be_buffer_r", minimum=0.0)
    _require_bool(merged, "use_trailing")
    _require_int(merged, "trail_atr_len", minimum=1)
    _require_number(merged, "trail_start_r", greater_than=0.0)
    _require_number(merged, "trail_distance_atr_mult", greater_than=0.0)

    if merged["signal_mode"] not in SUPPORTED_SIGNAL_MODES:
        raise ValueError(f"signal_mode must be one of: {sorted(SUPPORTED_SIGNAL_MODES)}")

    if merged["warmup_bars_override"] is not None:
        raise ValueError("warmup_bars_override is reserved for a later layer.")

    _reject_if_not_default(
        merged,
        "fixed_qty",
        1.0,
        "fixed_qty is inactive in the L6 sizing scope.",
    )

    if merged["execution_profile_id"] not in SUPPORTED_EXECUTION_PROFILES:
        raise ValueError(
            "execution_profile_id must be one of: "
            f"{sorted(SUPPORTED_EXECUTION_PROFILES)}"
        )

    if merged["tw_audit_semantics_mode"] not in {"off", "research"}:
        raise ValueError("tw_audit_semantics_mode must be one of: off, research")
    if merged["tw_reversal_reentry_mode"] not in {
        "local",
        "delay_after_protective_exit",
        "carry_to_next_bar_after_protective_exit",
        "next_bar_open_after_protective_exit_signal",
        "next_bar_close_after_protective_exit_signal",
    }:
        raise ValueError(
            "tw_reversal_reentry_mode must be one of: "
            "local, delay_after_protective_exit, carry_to_next_bar_after_protective_exit, "
            "next_bar_open_after_protective_exit_signal, next_bar_close_after_protective_exit_signal"
        )
    if merged["tw_margin_call_mode"] not in {"off", "tradingview"}:
        raise ValueError("tw_margin_call_mode must be one of: off, tradingview")
    if merged["tw_be_semantics_mode"] not in {"local", "tradingview", "next_bar_confirmed"}:
        raise ValueError("tw_be_semantics_mode must be one of: local, tradingview, next_bar_confirmed")
    if merged["tw_trailing_semantics_mode"] not in {"local", "tradingview", "next_bar_confirmed"}:
        raise ValueError(
            "tw_trailing_semantics_mode must be one of: local, tradingview, next_bar_confirmed"
        )

    if "equity_source" in config and str(config["equity_source"]) not in {"Realized", "Equity"}:
        raise ValueError("equity_source must be one of: Realized, Equity")

    if merged["ma_type"] not in SUPPORTED_MA_TYPES:
        raise ValueError(
            f"ma_type must be one of: {', '.join(sorted(SUPPORTED_MA_TYPES))}"
        )

    _VALID_HTF_TFS = {"30", "60", "120", "240", "D", "W"}
    if str(merged["ma_htf_timeframe"]) not in _VALID_HTF_TFS:
        raise ValueError(f"ma_htf_timeframe must be one of: {sorted(_VALID_HTF_TFS)}")
    if str(merged["macd_htf_timeframe"]) not in _VALID_HTF_TFS:
        raise ValueError(f"macd_htf_timeframe must be one of: {sorted(_VALID_HTF_TFS)}")
    if str(merged["htf_trend_timeframe"]) not in _VALID_HTF_TFS:
        raise ValueError(f"htf_trend_timeframe must be one of: {sorted(_VALID_HTF_TFS)}")
    if str(merged["mcginley_htf_timeframe"]) not in _VALID_HTF_TFS:
        raise ValueError(f"mcginley_htf_timeframe must be one of: {sorted(_VALID_HTF_TFS)}")
    if str(merged["adx_htf_timeframe"]) not in _VALID_HTF_TFS:
        raise ValueError(f"adx_htf_timeframe must be one of: {sorted(_VALID_HTF_TFS)}")
    if str(merged["chop_htf_timeframe"]) not in _VALID_HTF_TFS:
        raise ValueError(f"chop_htf_timeframe must be one of: {sorted(_VALID_HTF_TFS)}")
    if str(merged["htf_trend_ma_type"]) not in SUPPORTED_MA_TYPES:
        raise ValueError(f"htf_trend_ma_type must be one of: {', '.join(sorted(SUPPORTED_MA_TYPES))}")

    if merged["sl_swing_basis"] not in {SL_BASIS_WICK, SL_BASIS_CLOSE}:
        raise ValueError("sl_swing_basis must be one of: Wick, Close")

    sl_modes = [
        bool(merged["use_sl_atr"]),
        bool(merged["use_sl_percent"]),
        bool(merged["use_sl_swing_atr"]),
    ]
    if merged["use_sl"]:
        if sum(int(flag) for flag in sl_modes) != 1:
            raise ValueError("Exactly one SL mode must be selected when use_sl=True")
    elif any(sl_modes):
        raise ValueError("All use_sl_* modes must be False when use_sl=False")

    tp_mode = str(merged["tp_mode"])
    if tp_mode not in {TP_MODE_NONE, TP_MODE_ATR, TP_MODE_PERCENT, TP_MODE_R, TP_MODE_MULTI}:
        raise ValueError("tp_mode must be one of: None, ATR, Percent, R, Multi-TP")

    if merged["use_tp"]:
        tp_modes = [
            bool(merged["use_tp_single_atr"]),
            bool(merged["use_tp_single_pct"]),
            bool(merged["use_tp_single_r"]),
            bool(merged["use_tp_multi"]),
        ]
        if sum(int(flag) for flag in tp_modes) != 1:
            raise ValueError("Exactly one TP mode must be selected when use_tp=True")
    else:
        tp_flags = [
            bool(merged["use_tp_single_atr"]),
            bool(merged["use_tp_single_pct"]),
            bool(merged["use_tp_single_r"]),
            bool(merged["use_tp_multi"]),
        ]
        if any(tp_flags):
            raise ValueError("All use_tp_* modes must be False when use_tp=False")

    if merged["use_tp_multi"]:
        tp1_close_pct = float(merged["tp1_close_pct"])
        if not (0.0 < tp1_close_pct < 100.0):
            raise ValueError("tp1_close_pct must be between 0 and 100")
        if float(merged["tp2_r_multiple"]) <= float(merged["tp1_r_multiple"]):
            raise ValueError("tp2_r_multiple must be greater than tp1_r_multiple")

    if merged["allow_flip"] and not bool(merged.get("enable_long", True) or merged.get("enable_short", True)):
        raise ValueError("allow_flip requires at least one enabled side")
    if merged["allow_flip"] and not bool(merged["exit_on_opposite_signal"]):
        raise ValueError("allow_flip requires exit_on_opposite_signal=True")

    _require_bool(merged, "exit_on_opposite_signal")

    # L25 - WunderTrading
    _require_str(merged, "wt_order_type")
    if merged["wt_order_type"] not in {"market", "limit"}:
        raise ValueError("wt_order_type must be 'market' or 'limit'")
    _require_str(merged, "wt_amount_type")
    if merged["wt_amount_type"] not in {"quote", "base"}:
        raise ValueError("wt_amount_type must be 'quote' or 'base'")
    _require_number(merged, "wt_amount", greater_than=0.0)
    _require_int(merged, "wt_leverage", minimum=1)
    _require_bool(merged, "wt_use_tp")
    _require_bool(merged, "wt_use_sl")
    _require_bool(merged, "wt_reduce_only")
    _require_bool(merged, "wt_place_cond_orders")
    if bool(merged["wt_use_tp"]) and not bool(merged["use_tp"]):
        raise ValueError("wt_use_tp requires use_tp=True")
    if bool(merged["wt_use_sl"]) and not bool(merged["use_sl"]):
        raise ValueError("wt_use_sl requires use_sl=True")

    if merged["use_break_even"] and not merged["use_sl"]:
        raise ValueError("BE requires SL")
    if merged["use_trailing"] and not merged["use_sl"]:
        raise ValueError("Trailing requires SL")
    if merged["use_tp_single_r"] and not merged["use_sl"]:
        raise ValueError("R take-profit requires SL")
    if merged["use_tp_multi"] and not merged["use_sl"]:
        raise ValueError("Multi-TP requires SL")



    # L15 validation
    if merged["time_stop_condition"] not in {"Always", "Profit Only", "Loss Only"}:
        raise ValueError("time_stop_condition must be one of: Always, Profit Only, Loss Only")

    # L16 guard recovery validation
    if merged["guard_recovery_mode"] not in {"Bars", "Signals"}:
        raise ValueError("guard_recovery_mode must be 'Bars' or 'Signals'")

    # MACD mode
    if merged["macd_hist_mode"] not in {"POSITIVE", "RISING", "RISING_POSITIVE"}:
        raise ValueError("macd_hist_mode must be one of POSITIVE | RISING | RISING_POSITIVE")


def resolve_config(config: dict[str, object], *, validate: bool = True) -> dict[str, object]:
    merged = dict(DEFAULT_CONFIG)
    merged.update(config)
    explicit_keys = set(config.keys())
    # Deprecated sizing policy surface: runtime is fixed to realized snapshots.
    merged["equity_source"] = "Realized"
    # Deprecated redundant safety surface: leverage-cap sizing already constrains
    # order notional, so runtime keeps this path fixed off.
    merged["use_notional_assert"] = False
    max_leverage_cap = float(merged["max_leverage_cap"])
    derived_margin_pct = 100.0 / max_leverage_cap
    if "margin_long_pct" not in explicit_keys:
        merged["margin_long_pct"] = derived_margin_pct
    if "margin_short_pct" not in explicit_keys:
        merged["margin_short_pct"] = derived_margin_pct

    if not bool(merged["use_sl"]):
        merged["use_sl_atr"] = False
        merged["use_sl_percent"] = False
        merged["use_sl_swing_atr"] = False

    tp_mode = str(merged["tp_mode"])
    merged["use_tp"] = tp_mode != TP_MODE_NONE
    merged["use_tp_single_atr"] = tp_mode == TP_MODE_ATR
    merged["use_tp_single_pct"] = tp_mode == TP_MODE_PERCENT
    merged["use_tp_single_r"] = tp_mode == TP_MODE_R
    merged["use_tp_multi"] = tp_mode == TP_MODE_MULTI

    if validate:
        validate_config(config)

    return merged


def _require_bool(config: dict[str, object], key: str) -> None:
    value = config[key]
    if not isinstance(value, bool):
        raise ValueError(f"{key} must be bool")


def _require_int(config: dict[str, object], key: str, *, minimum: int | None = None) -> None:
    value = config[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{key} must be int")
    if minimum is not None and value < minimum:
        raise ValueError(f"{key} must be >= {minimum}")


def _require_optional_int(config: dict[str, object], key: str) -> None:
    value = config[key]
    if value is None:
        return
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{key} must be int or None")


def _require_number(
    config: dict[str, object],
    key: str,
    *,
    minimum: float | None = None,
    greater_than: float | None = None,
) -> None:
    value = config[key]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{key} must be numeric")
    numeric = float(value)
    if not math.isfinite(numeric):
        raise ValueError(f"{key} must be finite")
    if minimum is not None and numeric < minimum:
        raise ValueError(f"{key} must be >= {minimum}")
    if greater_than is not None and numeric <= greater_than:
        raise ValueError(f"{key} must be > {greater_than}")


def _require_str(config: dict[str, object], key: str) -> None:
    value = config[key]
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be non-empty string")


def _reject_if_not_default(
    config: dict[str, Any],
    key: str,
    expected: Any,
    message: str,
) -> None:
    if config[key] != expected:
        raise ValueError(message)
