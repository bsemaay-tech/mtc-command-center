from __future__ import annotations

from datetime import UTC, datetime

import pytest

from mtc_v2.core.config import resolve_config, validate_config
from mtc_v2.core.runner import Runner
from mtc_v2.core.types import Bar
from mtc_v2.signals.range_filter import RangeFilterSignal
from mtc_v2.signals.supertrend import SupertrendSignal


def _bar(index: int, close: float) -> Bar:
    return Bar(
        timestamp=datetime(2025, 1, 1, index, tzinfo=UTC),
        open=close,
        high=close + 0.5,
        low=close - 0.5,
        close=close,
        volume=100.0,
        bar_index=index,
    )


def test_default_signal_mode_remains_supertrend() -> None:
    config = resolve_config({}, validate=True)
    runner = Runner({})

    assert config["signal_mode"] == "Supertrend"
    assert isinstance(runner.signal_producer, SupertrendSignal)


def test_range_filter_signal_mode_is_valid_and_selectable() -> None:
    config = resolve_config({"signal_mode": "Range Filter", "rf_range": 1.0}, validate=True)
    runner = Runner({"signal_mode": "Range Filter", "rf_range": 1.0})

    assert config["signal_mode"] == "Range Filter"
    assert isinstance(runner.signal_producer, RangeFilterSignal)


def test_range_filter_selected_produces_deterministic_raw_pulses() -> None:
    runner = Runner({"signal_mode": "Range Filter", "rf_range": 1.0})
    closes = [100.0, 100.5, 101.2, 101.4, 99.8, 99.6, 101.1]
    outputs = [runner.signal_producer.calculate(_bar(index, close)) for index, close in enumerate(closes)]

    assert [int(item.long) for item in outputs] == [0, 0, 1, 0, 0, 0, 1]
    assert [int(item.short) for item in outputs] == [0, 0, 0, 0, 1, 0, 0]


def test_unknown_signal_mode_still_rejected() -> None:
    with pytest.raises(ValueError, match="signal_mode"):
        validate_config({"signal_mode": "Unknown Producer"})
