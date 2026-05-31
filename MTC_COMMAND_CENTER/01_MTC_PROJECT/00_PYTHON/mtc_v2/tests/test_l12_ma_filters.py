from __future__ import annotations

from datetime import datetime

import pytest

from mtc_v2.core.config import validate_config
from mtc_v2.core.runner import Runner
from mtc_v2.core.types import Bar, RawSignal


def _build_config(**overrides: object) -> dict[str, object]:
    config: dict[str, object] = {
        "enable_long": True,
        "enable_short": True,
        "allow_flip": True,
        "regime_lock": False,
        "max_entries": 1,
        "cooldown_bars": 0,
        "signal_mode": "Supertrend",
        "st_atr_len": 3,
        "st_factor": 1.0,
        "st_use_wicks": False,
        "st_use_ha": False,
        "instrument_symbol": "TEST",
        "instrument_point_value": 1.0,
        "instrument_price_tick": 0.1,
        "instrument_qty_step": 0.1,
        "instrument_min_qty": 0.0,
        "instrument_min_notional": 0.0,
        "instrument_contract_multiplier": 1.0,
        "initial_capital": 10_000.0,
        "margin_long_pct": 100.0,
        "margin_short_pct": 100.0,
        "risk_per_long_pct": 0.5,
        "risk_per_short_pct": 0.5,
        "fallback_size_pct": 10.0,
        "max_leverage_cap": 10.0,
        "equity_source": "Realized",
        "use_notional_assert": False,
        "use_sl": False,
        "tp_mode": "None",
    }
    config.update(overrides)
    return config


def _bars(closes: list[float]) -> list[Bar]:
    bars: list[Bar] = []
    for idx, close in enumerate(closes):
        bars.append(
            Bar(
                timestamp=datetime(2025, 1, idx + 1),
                open=close,
                high=close + 0.5,
                low=close - 0.5,
                close=close,
                volume=100.0,
                bar_index=idx,
            )
        )
    return bars


class _StaticSignalProducer:
    def __init__(self, outputs: list[RawSignal]) -> None:
        self._outputs = outputs
        self._index = 0
        self.warmup_bars_required = 0

    def calculate(self, bar: Bar) -> RawSignal:
        raw = self._outputs[self._index]
        self._index += 1
        return raw


def test_l12_ma_filter_blocks_long_below_ma() -> None:
    runner = Runner(
        _build_config(
            use_ma_filter=True,
            ma_type="SMA",
            ma_length=2,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(False, False, "seed_0", direction=1, line=10.0),
            RawSignal(False, False, "seed_1", direction=1, line=10.1),
            RawSignal(True, False, "manual_long", direction=1, line=10.2),
        ]
    )

    out = runner.run(_bars([100.0, 100.0, 99.0]))

    assert out[-1].long is False
    assert out[-1].short is False
    assert runner.state.gated_long is False
    assert runner.state.position is None
    assert runner.state.gate_results["ma_filter"].long_ok is False
    assert runner.state.gate_results["ma_filter"].short_ok is True


def test_l12_ma_filter_allows_short_below_ma() -> None:
    runner = Runner(
        _build_config(
            use_ma_filter=True,
            ma_type="SMA",
            ma_length=2,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(False, False, "seed_0", direction=-1, line=10.0),
            RawSignal(False, False, "seed_1", direction=-1, line=10.1),
            RawSignal(False, True, "manual_short", direction=-1, line=10.2),
        ]
    )

    out = runner.run(_bars([100.0, 100.0, 99.0]))

    assert out[-1].short is True
    assert runner.state.gated_short is True
    assert runner.state.position is not None
    assert runner.state.position.side == "short"


def test_l12_ma_slope_filter_allows_only_positive_slope_longs() -> None:
    runner = Runner(
        _build_config(
            use_ma_slope_filter=True,
            ma_type="SMA",
            ma_slope_len=2,
            ma_slope_min_pct=0.005,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(False, False, "seed_0", direction=1, line=10.0),
            RawSignal(False, False, "seed_1", direction=1, line=10.1),
            RawSignal(True, False, "manual_long", direction=1, line=10.2),
        ]
    )

    out = runner.run(_bars([100.0, 101.0, 102.0]))

    assert out[-1].long is True
    assert runner.state.position is not None
    assert runner.state.position.side == "long"
    assert runner.state.gate_results["ma_slope_filter"].long_ok is True
    assert runner.state.gate_results["ma_slope_filter"].short_ok is False


def test_l12_config_accepts_use_ma_mtf() -> None:
    """use_ma_mtf is now fully implemented — config must accept it without error."""
    from mtc_v2.core.config import resolve_config
    cfg = resolve_config(_build_config(use_ma_filter=True, use_ma_mtf=True))
    assert cfg["use_ma_mtf"] is True


def test_l12_ma_mtf_override_series_bypasses_local_htf_warmup() -> None:
    runner = Runner(
        _build_config(
            use_ma_filter=True,
            use_ma_mtf=True,
            ma_type="EMA",
            ma_length=200,
            st_atr_len=2,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(False, False, "seed_0", direction=1, line=10.0),
            RawSignal(False, False, "seed_1", direction=1, line=10.1),
            RawSignal(True, False, "manual_long", direction=1, line=10.2),
        ]
    )
    runner.set_gate_overrides(ma_filter_line_map={2: 95.0})

    out = runner.run(_bars([100.0, 100.0, 100.0]), htf_data={})

    assert out[-1].long is True
    assert runner.state.gate_results["ma_filter"].value == pytest.approx(95.0)


def test_l12_htf_trend_override_series_bypasses_local_htf_warmup() -> None:
    runner = Runner(
        _build_config(
            use_htf_trend_filter=True,
            htf_trend_ma_type="EMA",
            htf_trend_ma_len=200,
            htf_trend_timeframe="240",
            htf_trend_buffer_pct=0.1,
            st_atr_len=2,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(False, False, "seed_0", direction=1, line=10.0),
            RawSignal(False, False, "seed_1", direction=1, line=10.1),
            RawSignal(True, False, "manual_long", direction=1, line=10.2),
        ]
    )
    runner.set_gate_overrides(htf_trend_line_map={2: 95.0})

    out = runner.run(_bars([100.0, 100.0, 100.0]), htf_data={})

    assert out[-1].long is True
    assert runner.state.gate_results["htf_trend_filter"].value == pytest.approx(95.0)
    assert runner.state.position is not None
    assert runner.state.position.side == "long"


def test_l12_mcginley_htf_override_series_bypasses_local_htf_warmup() -> None:
    runner = Runner(
        _build_config(
            use_mcginley_filter=True,
            mcginley_length=2,
            mcginley_use_higher_timeframe=True,
            mcginley_htf_timeframe="D",
            st_atr_len=2,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(False, False, "seed_0", direction=1, line=10.0),
            RawSignal(False, False, "seed_1", direction=1, line=10.1),
            RawSignal(True, False, "manual_long", direction=1, line=10.2),
        ]
    )
    runner.set_gate_overrides(mcginley_line_map={2: 95.0})

    out = runner.run(_bars([100.0, 100.0, 100.0]), htf_data={})

    assert out[-1].long is True
    assert runner.state.gate_results["mcginley_filter"].value == pytest.approx(95.0)
    assert runner.state.position is not None
    assert runner.state.position.side == "long"
