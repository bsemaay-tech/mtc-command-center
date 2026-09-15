"""Regression fence for finding D8 (2026-09-07): ``debug_mode`` metadata must not raise.

``Runner.run()`` builds ``_debug_metadata`` with ``EXECUTION_PROFILE_RAW_CLOSE_ONLY`` when
``config["debug_mode"]`` is true, but ``runner.py`` never imported that constant from
``mtc_v2.core.config``; the first bar processed with ``debug_mode=True`` raised ``NameError``.
No trading calculation, threshold, default, or parity behaviour is changed or asserted here: the
config below is the same smoke configuration ``test_supertrend_smoke.py`` uses, on four synthetic
bars, and ``debug_mode`` keeps its ``False`` default.
"""

from __future__ import annotations

from datetime import datetime

import mtc_v2.core.runner as runner_module
from mtc_v2.core.config import EXECUTION_PROFILE_RAW_CLOSE_ONLY, resolve_config
from mtc_v2.core.runner import Runner
from mtc_v2.core.types import Bar


def _smoke_config(**overrides: object) -> dict[str, object]:
    config: dict[str, object] = {
        "enable_long": True,
        "enable_short": True,
        "allow_flip": True,
        "regime_lock": False,
        "max_entries": 1,
        "cooldown_bars": 0,
        "warmup_bars_override": None,
        "signal_mode": "Supertrend",
        "st_atr_len": 3,
        "st_factor": 1.0,
        "st_use_wicks": False,
        "st_use_ha": False,
        "instrument_symbol": "TEST",
        "instrument_point_value": 1.0,
        "instrument_price_tick": 0.25,
        "instrument_qty_step": 1.0,
        "instrument_min_qty": 0.0,
        "instrument_min_notional": 0.0,
        "instrument_contract_multiplier": 1.0,
        "initial_capital": 1000.0,
        "margin_long_pct": 100.0,
        "margin_short_pct": 100.0,
        "execution_profile_id": EXECUTION_PROFILE_RAW_CLOSE_ONLY,
        "risk_per_long_pct": 0.4,
        "risk_per_short_pct": 0.4,
        "fallback_size_pct": 10.1,
        "max_leverage_cap": 1.0,
        "equity_source": "Realized",
        "use_notional_assert": False,
        "use_sl": True,
        "use_sl_atr": True,
        "sl_atr_len": 1,
        "sl_atr_mult": 4.0,
        "tp_mode": "None",
        "tp_atr_len": 1,
        "tp_atr_mult": 4.0,
    }
    config.update(overrides)
    return config


def _synthetic_bars() -> list[Bar]:
    return [
        Bar(datetime(2025, 1, 1), 10.0, 10.0, 10.0, 10.0, 100, 0),
        Bar(datetime(2025, 1, 2), 10.0, 11.0, 9.8, 10.8, 120, 1),
        Bar(datetime(2025, 1, 3), 10.8, 11.2, 10.5, 11.0, 110, 2),
        Bar(datetime(2025, 1, 4), 11.0, 11.3, 10.7, 11.1, 130, 3),
    ]


def test_runner_module_binds_execution_profile_constant() -> None:
    assert runner_module.EXECUTION_PROFILE_RAW_CLOSE_ONLY == EXECUTION_PROFILE_RAW_CLOSE_ONLY


def test_debug_mode_metadata_reports_execution_profile() -> None:
    runner = Runner(_smoke_config(debug_mode=True))
    runner.run(_synthetic_bars())
    metadata = runner.get_debug_metadata()
    assert metadata["execution_profile_id"] == EXECUTION_PROFILE_RAW_CLOSE_ONLY


def test_debug_mode_default_is_off_and_metadata_stays_empty() -> None:
    assert resolve_config(_smoke_config())["debug_mode"] is False
    runner = Runner(_smoke_config())
    runner.run(_synthetic_bars())
    assert runner.get_debug_metadata() == {}
