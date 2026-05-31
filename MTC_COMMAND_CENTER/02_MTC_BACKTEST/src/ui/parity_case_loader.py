from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def _parse_case_date(raw: str) -> datetime.date:
    text = str(raw).strip()
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        dt = datetime.strptime(text, "%Y-%m-%d")
    return dt.date()


def build_backtest_state_from_case(case_path: Path) -> dict[str, Any]:
    """
    Convert case JSON fields into Streamlit backtest widget state keys.
    This is UI wiring only; engine behavior remains unchanged.
    """
    data = json.loads(case_path.read_text(encoding="utf-8"))
    cfg = data.get("config", {})
    strategy = cfg.get("strategy", {})
    trade = cfg.get("trade", {})
    supertrend = cfg.get("supertrend", {})
    range_filter = cfg.get("range_filter", {})
    time_stop = cfg.get("time_stop", {})
    risk = cfg.get("risk", {})
    stop_loss = cfg.get("stop_loss", {})
    take_profit = cfg.get("take_profit", {})
    multi_tp = cfg.get("multi_tp", {})
    break_even = cfg.get("break_even", {})
    trailing = cfg.get("trailing", {})
    filters = cfg.get("filters", {})
    guards = cfg.get("guards", {})
    exit_filter_block = cfg.get("exit_filter_block", {})
    parity = cfg.get("parity", {})

    preroll_days = data.get("preroll_days")
    if preroll_days is None:
        preroll_days = parity.get("preroll_days")
    if preroll_days is None:
        preroll_days = 90

    state = {
        "bt_dataset": data.get("dataset"),
        "bt_range_start": _parse_case_date(data["start_date"]),
        "bt_range_end": _parse_case_date(data["end_date"]),
        "bt_warmup": int(data.get("warmup_bars", 200)),
        "bt_preroll_days": int(preroll_days),
        "bt_signal_mode": cfg.get("signal_mode", "Supertrend"),
        "bt_st_atr_len": int(supertrend.get("atr_len", 21)),
        "bt_st_factor": float(supertrend.get("factor", 4.0)),
        "bt_st_ha": bool(supertrend.get("use_ha", True)),
        "bt_st_wicks": bool(supertrend.get("use_wicks", True)),
        "bt_rf_adx_tr": int(range_filter.get("adx_trend_threshold", 25)),
        "bt_rf_adx_rg": int(range_filter.get("adx_range_threshold", 20)),
        "bt_rf_chop_tr": int(range_filter.get("chop_trend_threshold", 50)),
        "bt_rf_chop_rg": int(range_filter.get("chop_range_threshold", 62)),
        "bt_rf_rsi_len": int(range_filter.get("rsi_len", 14)),
        "bt_rf_rsi_os": int(range_filter.get("rsi_oversold", 30)),
        "bt_rf_rsi_ob": int(range_filter.get("rsi_overbought", 70)),
        "bt_rf_bb_len": int(range_filter.get("bb_len", 20)),
        "bt_rf_bb_mult": float(range_filter.get("bb_mult", 2.0)),
        "bt_rf_use_bb": bool(range_filter.get("use_bb_filter", True)),
        "bt_enable_long": bool(trade.get("enable_long", True)),
        "bt_enable_short": bool(trade.get("enable_short", True)),
        "bt_allow_flip": bool(trade.get("allow_flip", True)),
        "bt_exit_opp": bool(trade.get("exit_on_opposite_signal", False)),
        "bt_exit_fb": bool(trade.get("exit_on_filter_block", False)),
        "bt_regime_lock": bool(trade.get("use_regime_lock", False)),
        "bt_entry_mode": str(trade.get("entry_mode", "Signal")),
        "bt_init_cap": float(strategy.get("initial_capital", 10000.0)),
        "bt_comm": float(strategy.get("commission_percent", 0.04)),
        "bt_slip": int(strategy.get("slippage_ticks", 5)),
        "bt_mintick": float(strategy.get("mintick", 0.1)),
        "bt_pyramiding": int(strategy.get("pyramiding", 1)),
        "bt_pyr_max": int(trade.get("max_pyramid_positions", 1)),
        "bt_sig_max_ent": int(trade.get("signal_mode_max_entries", 1)),
        "bt_sig_cd": int(trade.get("signal_mode_cooldown_bars", 10)),
        "bt_ts_en": bool(time_stop.get("enabled", False)),
        "bt_ts_bars": int(time_stop.get("bars", 50)),
        "bt_ts_eod": bool(time_stop.get("eod", False)),
        "bt_ts_eow": bool(time_stop.get("eow", False)),
        "bt_ts_cond": str(time_stop.get("condition", "Always")),
        "bt_efb_ma": bool(exit_filter_block.get("exit_on_ma_block", False)),
        "bt_efb_maslope": bool(exit_filter_block.get("exit_on_ma_slope_block", False)),
        "bt_efb_mcg": bool(exit_filter_block.get("exit_on_mcginley_block", False)),
        "bt_efb_htf": bool(exit_filter_block.get("exit_on_htf_trend_block", False)),
        "bt_efb_vol": bool(
            exit_filter_block.get("exit_on_vol_part_block", exit_filter_block.get("exit_on_vol_block", False))
        ),
        "bt_efb_atrvol": bool(exit_filter_block.get("exit_on_atr_vol_block", False)),
        "bt_efb_range": bool(exit_filter_block.get("exit_on_range_block", False)),
        "bt_risk_long": float(risk.get("risk_long_percent", 4.0)),
        "bt_risk_short": float(risk.get("risk_short_percent", 3.0)),
        "bt_lev_cap": float(risk.get("max_leverage_cap", 5.0)),
        "bt_fallback_qty": float(risk.get("fallback_qty_pct", 5.0)),
        "bt_risk_equity_mode": str(risk.get("risk_equity_mode", "Initial")),
        "bt_notional_hard_assert": bool(risk.get("use_notional_hard_assert", False)),
        "bt_daily_loss_en": bool(risk.get("use_daily_loss_limit", False)),
        "bt_daily_loss": float(risk.get("max_daily_loss_percent", 5.0)),
        "bt_max_trades_en": bool(risk.get("use_max_trades_per_day", False)),
        "bt_max_trades": int(risk.get("max_trades_per_day", 5)),
        "bt_sl_en": bool(stop_loss.get("enabled", stop_loss.get("use_sl", True))),
        "bt_sl_mode": str(stop_loss.get("mode", "ATR")),
        "bt_sl_atr_len": int(stop_loss.get("atr_len", 14)),
        "bt_sl_atr_mult": float(stop_loss.get("atr_mult", 4.0)),
        "bt_sl_pct": float(stop_loss.get("percent", 1.0)),
        "bt_sl_swing_basis": str(stop_loss.get("swing_basis", "Wick")),
        "bt_sl_swing_lb": int(stop_loss.get("swing_lookback", 20)),
        "bt_sl_swing_atr_len": int(stop_loss.get("swing_atr_len", 14)),
        "bt_sl_swing_atr_mult": float(stop_loss.get("swing_atr_mult", 0.5)),
        "bt_tp_en": bool(take_profit.get("enabled", take_profit.get("use_tp", True))),
        "bt_tp_mode": str(take_profit.get("mode", "ATR")),
        "bt_tp_atr_len": int(take_profit.get("atr_len", 14)),
        "bt_tp_atr_mult": float(take_profit.get("atr_mult", 3.0)),
        "bt_tp_pct": float(take_profit.get("percent", 2.0)),
        "bt_tp_rr": float(take_profit.get("rr", 2.0)),
        "bt_mtp_en": bool(multi_tp.get("enabled", multi_tp.get("use_multi_tp", True))),
        "bt_tp1_rr": float(multi_tp.get("tp1_rr", 3.0)),
        "bt_tp1_pct": float(multi_tp.get("tp1_pct", 50.0)),
        "bt_tp2_rr": float(multi_tp.get("tp2_rr", 5.5)),
        "bt_be_en": bool(break_even.get("enabled", break_even.get("use_break_even", True))),
        "bt_be_rr": float(break_even.get("rr", 1.0)),
        "bt_be_buf": float(break_even.get("buffer_r", 0.1)),
        "bt_trail_en": bool(trailing.get("enabled", trailing.get("use_trailing", True))),
        "bt_trail_atr_len": int(trailing.get("atr_len", 14)),
        "bt_trail_start": float(trailing.get("start_r", 2.5)),
        "bt_trail_dist": float(trailing.get("dist_r", 2.0)),
        "bt_use_ma": bool(filters.get("use_ma_filter", False)),
        "bt_use_ma_slope": bool(filters.get("use_ma_slope_filter", False)),
        "bt_ma_type": str(filters.get("ma_type", "EMA")),
        "bt_ma_len": int(filters.get("ma_length", 200)),
        "bt_ma_slope_len": int(filters.get("ma_slope_len", 200)),
        "bt_ma_slope_pct": float(filters.get("ma_slope_min_pct", 0.005)),
        "bt_use_vol": bool(filters.get("use_volume_filter", False)),
        "bt_vol_len": int(filters.get("vol_filter_len", 50)),
        "bt_vol_mult": float(filters.get("vol_filter_mult", 0.5)),
        "bt_use_atr_vol": bool(filters.get("use_atr_vol_filter", False)),
        "bt_atr_vol_len": int(filters.get("atr_vol_len", 14)),
        "bt_atr_vol_smooth": int(filters.get("atr_vol_smooth_len", 100)),
        "bt_atr_vol_mult": float(filters.get("atr_vol_floor_mult", 1.2)),
        "bt_use_htf": bool(filters.get("use_htf_trend_filter", False)),
        "bt_htf_tf": str(filters.get("htf_trend_timeframe", "240")),
        "bt_htf_ma_type": str(filters.get("htf_trend_ma_type", "EMA")),
        "bt_htf_len": int(filters.get("htf_trend_ma_len", 100)),
        "bt_htf_buf": float(filters.get("htf_trend_buffer_pct", 0.1)),
        "bt_g_dd_en": bool(guards.get("use_dd_guard", False)),
        "bt_g_dd_pct": float(guards.get("dd_guard_pct", 10.0)),
        "bt_g_cl_en": bool(guards.get("use_consec_loss_guard", False)),
        "bt_g_cl_max": int(guards.get("consec_loss_max", 3)),
        "bt_g_cd_en": bool(guards.get("use_cooldown_guard", False)),
        "bt_g_cd_bars": int(guards.get("cooldown_bars", 5)),
        "bt_g_eq_en": bool(guards.get("use_eq_curve_guard", False)),
        "bt_g_eq_len": int(guards.get("eq_curve_ma_len", 5)),
        "bt_g_mae_en": bool(guards.get("use_mae_guard", False)),
        "bt_g_mae_pct": float(guards.get("mae_max_pct", 2.0)),
        "bt_parity_en": bool(parity.get("enabled", True)),
        "bt_fill_mode": parity.get("fill_contract", "touch"),
        "bt_debug_export": bool(parity.get("export_debug_csv", False)),
        "bt_debug_dir": parity.get("debug_dir", "debug"),
    }
    return state


def diff_backtest_state_with_case(case_path: Path, current_state: dict[str, Any]) -> list[str]:
    """
    Compare current Streamlit widget state with expected state loaded from case.
    Returns deterministic sorted mismatch list (keys only).
    """
    expected = build_backtest_state_from_case(case_path)
    mismatches: list[str] = []
    for key in sorted(expected.keys()):
        if key not in current_state:
            mismatches.append(key)
            continue
        if current_state[key] != expected[key]:
            mismatches.append(key)
    return mismatches
