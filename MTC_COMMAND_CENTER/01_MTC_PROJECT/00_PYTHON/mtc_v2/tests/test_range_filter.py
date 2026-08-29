from __future__ import annotations

from datetime import datetime, UTC

import pytest

from mtc_v2.core.types import Bar
from mtc_v2.signals.range_filter import RangeFilterSignal


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


def test_range_filter_emits_one_bar_flip_pulses_and_trace_snapshot() -> None:
    signal = RangeFilterSignal({"rf_range": 1.0})
    closes = [100.0, 100.5, 101.2, 101.4, 99.8, 99.6, 101.1]
    outputs = [signal.calculate(_bar(index, close)) for index, close in enumerate(closes)]
    snapshots = [signal.indicator_snapshot() for _ in outputs]

    assert [int(item.long) for item in outputs] == [0, 0, 1, 0, 0, 0, 1]
    assert [int(item.short) for item in outputs] == [0, 0, 0, 0, 1, 0, 0]
    assert outputs[2].reason == "rf_flip_long"
    assert outputs[4].reason == "rf_flip_short"
    assert outputs[-1].direction == 1
    assert outputs[-1].line == pytest.approx(100.1)
    assert snapshots[-1]["filter_line"] == pytest.approx(100.1)
    assert snapshots[-1]["upper_band"] == pytest.approx(101.1)
    assert snapshots[-1]["lower_band"] == pytest.approx(99.1)


def test_range_filter_flat_state_down_flip_needs_no_band_and_this_is_intended() -> None:
    """Document the intended flat-state gating asymmetry.

    This matches Pine (`MTC_V2.pine:630-649` at `77a10e65`) and the independent
    reference oracle (`parity_oracles/tests/test_independent_reference_oracle.py:36-56`).
    A future change is a three-place change to Python, Pine, and the oracle, not a
    one-place fix.
    """
    down_signal = RangeFilterSignal({"rf_range": 1.0})
    down_outputs = [
        down_signal.calculate(_bar(index, close))
        for index, close in enumerate([100.0, 99.0])
    ]

    assert down_outputs[0].reason == "rf_init"
    assert down_outputs[0].direction == 0
    assert down_outputs[0].line == 100.0
    assert down_outputs[1].reason == "rf_flip_short"
    assert down_outputs[1].short is True
    assert down_outputs[1].direction == -1
    assert down_outputs[1].line == 99.0 + 1.0

    up_signal = RangeFilterSignal({"rf_range": 1.0})
    up_outputs = [
        up_signal.calculate(_bar(index, close))
        for index, close in enumerate([100.0, 100.5])
    ]

    assert up_outputs[1].reason == "rf_hold"
    assert up_outputs[1].long is False
    assert up_outputs[1].short is False
    assert up_outputs[1].direction == 0
