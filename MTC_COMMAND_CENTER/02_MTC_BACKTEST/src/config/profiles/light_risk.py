"""Light-risk profile for MTC-Engine Validation.

This is a preset only. It does not change MTCRunner behavior.
"""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from typing import Any

from src.config.defaults import MTCConfig


def _set_dotted(payload: dict[str, Any], dotted_key: str, value: Any) -> None:
    target = payload
    parts = dotted_key.split(".")
    if not parts or any(not part for part in parts):
        raise ValueError(f"Invalid override key: {dotted_key!r}")
    for part in parts[:-1]:
        current = target.get(part)
        if not isinstance(current, dict):
            current = {}
            target[part] = current
        target = current
    target[parts[-1]] = value


def _apply_overrides(payload: dict[str, Any], overrides: Mapping[str, Any]) -> dict[str, Any]:
    merged = deepcopy(payload)
    for key, value in overrides.items():
        if "." in key:
            _set_dotted(merged, key, value)
        else:
            existing = merged.get(key)
            if isinstance(existing, dict) and isinstance(value, Mapping):
                existing.update(value)
            else:
                merged[key] = value
    return merged


def build_light_risk_config(overrides: Mapping[str, Any] | None = None) -> MTCConfig:
    """Build an MTCConfig with filters/guards off and risk management on.

    Per-producer overrides may use either nested dictionaries or dotted keys,
    for example: ``{"stop_loss.mode": "%", "take_profit.percent": 2.0}``.
    The returned config is a fresh instance and never mutates global defaults.
    """

    cfg = MTCConfig()

    cfg.signal_mode = "None"
    cfg.confirmation.enabled = False

    # Filters OFF.
    cfg.filters.use_ma_filter = False
    cfg.filters.ma_use_higher_timeframe = False
    cfg.filters.use_ma_slope_filter = False
    cfg.filters.use_volume_filter = False
    cfg.filters.use_atr_vol_filter = False
    cfg.filters.use_mcginley_filter = False
    cfg.filters.use_mcginley_htf = False
    cfg.filters.use_htf_trend_filter = False
    cfg.filters.use_macd_filter = False
    cfg.filters.macd_use_htf_bias = False
    cfg.filters.use_range_filters = False
    cfg.filters.use_range_regime_filter = False
    cfg.filters.adx_use_higher_timeframe = False
    cfg.filters.chop_use_higher_timeframe = False

    # Guards OFF.
    cfg.guards.use_dd_guard = False
    cfg.guards.use_consec_loss_guard = False
    cfg.guards.use_cooldown_guard = False
    cfg.guards.use_eq_curve_guard = False
    cfg.guards.use_mae_guard = False
    cfg.guards.use_guard_recovery = False
    cfg.risk.use_daily_loss_limit = False
    cfg.risk.use_max_trades_per_day = False
    cfg.time_stop.enabled = False
    cfg.time_stop.use_bars = False
    cfg.time_stop.eod = False
    cfg.time_stop.eow = False
    cfg.trade.use_regime_lock = False
    cfg.trade.exit_on_filter_block = False
    cfg.exit_filter_block.exit_on_ma_block = False
    cfg.exit_filter_block.exit_on_ma_slope_block = False
    cfg.exit_filter_block.exit_on_mcginley_block = False
    cfg.exit_filter_block.exit_on_htf_trend_block = False
    cfg.exit_filter_block.exit_on_vol_part_block = False
    cfg.exit_filter_block.exit_on_atr_vol_block = False
    cfg.exit_filter_block.exit_on_range_block = False

    # Risk ON.
    cfg.stop_loss.enabled = True
    cfg.take_profit.enabled = True
    cfg.break_even.enabled = True
    cfg.multi_tp.enabled = True
    cfg.trailing.enabled = True
    cfg.risk.risk_long_percent = 4.0
    cfg.risk.risk_short_percent = 3.0
    cfg.risk.max_leverage_cap = 5.0
    cfg.risk.fallback_qty_pct = 5.0

    if not overrides:
        return cfg

    payload = _apply_overrides(cfg.model_dump(by_alias=True), overrides)
    return MTCConfig.model_validate(payload)
