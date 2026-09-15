from __future__ import annotations

from mtc_v2.core.instrument import InstrumentMetadata
from mtc_v2.core.position_sizer import PositionSizer


def _sizer(**overrides: object) -> PositionSizer:
    config: dict[str, object] = {
        "risk_per_long_pct": 10.0,
        "risk_per_short_pct": 10.0,
        "fallback_size_pct": 10.0,
        "max_leverage_cap": 10.0,
    }
    config.update(overrides)
    return PositionSizer(config)


def _instrument(**overrides: float) -> InstrumentMetadata:
    values = {
        "symbol": "SYNTH",
        "point_value": 1.0,
        "price_tick": 1.0,
        "qty_step": 1.0,
        "min_qty": 0.0,
        "min_notional": 0.0,
        "contract_multiplier": 2.0,
    }
    values.update(overrides)
    return InstrumentMetadata(**values)


def test_corrected_risk_and_fallback_sizing_include_contract_multiplier() -> None:
    sizer = _sizer()
    instrument = _instrument()

    assert sizer.calc_qty(100.0, 90.0, 1000.0, True, instrument) == 10.0
    assert (
        sizer.calc_qty(
            100.0,
            90.0,
            1000.0,
            True,
            instrument,
            semantics_id="2.0.0",
        )
        == 5.0
    )
    assert (
        sizer.calc_qty(
            100.0,
            float("nan"),
            1000.0,
            True,
            _instrument(contract_multiplier=1.0),
            semantics_id="2.0.0",
        )
        == 1.0
    )


def test_corrected_zero_distance_stop_remains_zero() -> None:
    assert (
        _sizer().calc_qty(
            100.0,
            100.0,
            1000.0,
            True,
            _instrument(),
            semantics_id="2.0.0",
        )
        == 0.0
    )


def test_corrected_minimum_notional_uses_final_fill_and_equality_passes() -> None:
    sizer = _sizer(risk_per_long_pct=1.0)

    assert (
        sizer.calc_qty(
            100.0,
            90.0,
            1000.0,
            True,
            _instrument(contract_multiplier=1.0, min_notional=101.0),
            semantics_id="2.0.0",
        )
        == 0.0
    )
    assert (
        sizer.calc_qty(
            100.0,
            90.0,
            1000.0,
            True,
            _instrument(contract_multiplier=1.0, min_notional=100.0),
            semantics_id="2.0.0",
        )
        == 1.0
    )
    assert (
        sizer.calc_qty(
            101.0,
            91.0,
            1000.0,
            True,
            _instrument(contract_multiplier=1.0, min_notional=100.5),
            semantics_id="2.0.0",
        )
        == 1.0
    )
