from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SAFE_ATR_LENGTH_FIELDS = [
    "st_atr_len",
    "sl_atr_len",
    "tp_atr_len",
    "trail_atr_len",
]

ATR_MAPPING_REVIEW_NEEDED = [
    "atr_vol_floor_fast_len",
    "atr_vol_floor_baseline_len",
    "momentum_atr_len",
    "sl_swing_atr_len",
]

BUNDLE_OVERRIDES: dict[str, dict[str, Any]] = {
    "exit_on_filter_bundle": {
        "exit_on_ma_block": False,
        "exit_on_ma_slope_block": False,
        "exit_on_mcginley_block": False,
        "exit_on_htf_trend_block": False,
        "exit_on_vol_block": False,
        "exit_on_atr_vol_block": False,
        "exit_on_range_block": False,
        "exit_on_candle_pattern_block": False,
        "exit_on_level_prox_block": False,
    },
    "guards_disabled_for_phase1": {
        "use_daily_loss_limit": False,
        "use_max_trades_per_day": False,
        "use_max_drawdown_guard": False,
        "use_consecutive_loss_halt": False,
        "use_equity_curve_filter": False,
        "use_mae_guard": False,
        "use_guard_recovery": False,
        "use_trade_cooldown": False,
    },
    "visualization_disabled": {
        "debug_mode": False,
    },
    "integrations_disabled": {
        "wt_enter_long_code": "",
        "wt_exit_long_code": "",
        "wt_enter_short_code": "",
        "wt_exit_short_code": "",
        "wt_exit_all_code": "",
        "wt_use_tp": False,
        "wt_use_sl": False,
        "wt_place_cond_orders": False,
    },
}


def apply_parameter_mapping(params: dict[str, Any]) -> dict[str, Any]:
    params = dict(params)
    overrides: dict[str, Any] = {}
    for bundle_name, bundle_values in BUNDLE_OVERRIDES.items():
        if bool(params.pop(bundle_name, False)):
            overrides.update(bundle_values)
    if "global_atr_length" in params:
        value = int(params.pop("global_atr_length"))
        for field in SAFE_ATR_LENGTH_FIELDS:
            overrides[field] = value
    if "risk_long" in params:
        overrides["risk_per_long_pct"] = params.pop("risk_long")
    if "risk_short" in params:
        overrides["risk_per_short_pct"] = params.pop("risk_short")
    overrides.update(params)
    return overrides


def mapper_payload() -> dict[str, Any]:
    return {
        "exposed_parameters": ["global_atr_length", "exit_on_filter_bundle", "guards_disabled_for_phase1", "visualization_disabled", "integrations_disabled"],
        "safe_atr_length_fields": SAFE_ATR_LENGTH_FIELDS,
        "atr_mapping_review_needed": ATR_MAPPING_REVIEW_NEEDED,
        "bundles": BUNDLE_OVERRIDES,
        "notes": [
            "Mapper is optimization-only and does not change Pine or DEFAULT_CONFIG.",
            "Guard, visualization, and integration bundles are fixed off in early profiles.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", required=True)
    args = parser.parse_args()
    target = Path(args.write)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(mapper_payload(), indent=2, sort_keys=True), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
