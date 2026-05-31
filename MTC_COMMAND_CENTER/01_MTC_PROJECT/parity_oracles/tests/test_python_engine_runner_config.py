from __future__ import annotations

from parity_oracles.engines.python_engine_runner import _config_from_case_plan_overrides


def test_case_plan_swing_atr_sl_mode_selects_swing_atr_flag() -> None:
    config = _config_from_case_plan_overrides(
        {
            "use_sl": False,
            "use_sl_atr": False,
            "use_sl_percent": False,
            "use_sl_swing_atr": False,
        },
        {"planned_overrides": {"sl_mode": "Swing+ATR"}},
    )

    assert config["use_sl"] is True
    assert config["use_sl_atr"] is False
    assert config["use_sl_percent"] is False
    assert config["use_sl_swing_atr"] is True
