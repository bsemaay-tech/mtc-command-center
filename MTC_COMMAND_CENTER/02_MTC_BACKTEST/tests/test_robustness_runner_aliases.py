from __future__ import annotations

from scripts.robustness_runner import _apply_dot_params
from src.config.defaults import MTCConfig


def test_apply_dot_params_respects_alias_fields() -> None:
    base = MTCConfig()
    updated = _apply_dot_params(
        base,
        {
            "stop_loss.use_sl": False,
            "take_profit.use_tp": False,
            "break_even.use_break_even": False,
            "multi_tp.use_multi_tp": False,
            "trailing.use_trailing": False,
        },
    )

    assert updated.stop_loss.enabled is False
    assert updated.take_profit.enabled is False
    assert updated.break_even.enabled is False
    assert updated.multi_tp.enabled is False
    assert updated.trailing.enabled is False
