from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "00_PYTHON"))

from mtc_v2.core.config import DEFAULT_CONFIG, validate_config
from tools.optimization_parameter_mapper import apply_parameter_mapping
from tools.run_big_overnight_multiasset_optimization import canonical_params


def test_tp_mode_none_canonicalizes_tp_r_multiple_to_null() -> None:
    params = canonical_params(
        {
            "signal_mode": "Supertrend",
            "tp_mode": "None",
            "tp_r_multiple": 3.0,
        }
    )

    assert params["tp_mode"] == "None"
    assert params["tp_r_multiple"] is None


def test_tp_mode_none_null_is_numeric_before_runner_validation() -> None:
    canonical = canonical_params(
        {
            "signal_mode": "Supertrend",
            "st_factor": 3.5,
            "global_atr_length": 10,
            "sl_atr_mult": 3.0,
            "tp_mode": "None",
            "tp_r_multiple": 2.5,
            "risk_long": 0.25,
            "risk_short": 0.75,
            "guards_disabled_for_phase1": True,
            "integrations_disabled": True,
            "visualization_disabled": True,
            "exit_on_filter_bundle": True,
        }
    )
    runner_params = dict(canonical)
    if runner_params.get("tp_mode") == "None" and runner_params.get("tp_r_multiple") is None:
        runner_params["tp_r_multiple"] = 1.0

    overrides = apply_parameter_mapping(runner_params)
    merged = dict(DEFAULT_CONFIG)
    merged.update(overrides)

    assert canonical["tp_r_multiple"] is None
    assert overrides["tp_r_multiple"] == 1.0
    validate_config(merged)
