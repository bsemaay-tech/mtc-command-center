from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

import pytest

from bridge.engine.strategies.keltner_trail_ema8 import KeltnerTrailEma8
from bridge.engine.types import Bar

FIXTURES = Path(__file__).parent / "fixtures"


def _load_bars(path: Path) -> list[Bar]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return [
            Bar(
                ts=datetime.fromisoformat(row["ts"]),
                open=float(row["open"]),
                high=float(row["high"]),
                low=float(row["low"]),
                close=float(row["close"]),
                volume=float(row["volume"]),
            )
            for row in csv.DictReader(handle)
        ]


def test_keltner_strategy_matches_golden_signal_timestamps():
    fixture = FIXTURES / "BTC_1h.csv"
    golden = json.loads((FIXTURES / "golden_signals.json").read_text())
    strategy = KeltnerTrailEma8()
    bars = _load_bars(fixture)

    signals = [
        signal.model_dump(mode="json")
        for idx in range(len(bars))
        if (signal := strategy.on_bar(bars[: idx + 1], position=None)) is not None
    ]
    assert all(signal["stop_loss"] is not None for signal in signals)

    expected = [
        {
            "ts": item["ts"],
            "symbol": "BTC",
            "direction": item["direction"],
            "reason": item["reason"],
            "ref_price": item["ref_price"],
        }
        for item in golden["signals"]
    ]
    comparable = [
        {key: signal[key] for key in ("ts", "symbol", "direction", "reason", "ref_price")}
        for signal in signals
    ]
    assert comparable == expected


def _synthetic_bars(closes: list[float]) -> list[Bar]:
    return [
        Bar(
            ts=datetime(2026, 1, 1),
            open=close,
            high=close,
            low=close,
            close=close,
            volume=0,
        )
        for close in closes
    ]


def test_trail_level_ema8_exact_recursive_match():
    """Synthetic prices where last-8 SMA != full-history EMA; verify exact recursive EMA."""
    closes = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]
    bars = _synthetic_bars(closes)
    strategy = KeltnerTrailEma8()

    class Position:
        size = 1.0

    trail = strategy.trail_level(bars, Position())
    assert trail is not None
    assert sum(closes[-8:]) / 8 == 65.0
    assert trail == pytest.approx(68.64558996000855, rel=1e-12)


def test_trail_level_ema8_long_short_same_level():
    """Both long and short position produce identical trail level."""
    closes = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]
    bars = _synthetic_bars(closes)
    strategy = KeltnerTrailEma8()

    class PositionLong:
        size = 1.0

    class PositionShort:
        size = -1.0

    long_trail = strategy.trail_level(bars, PositionLong())
    short_trail = strategy.trail_level(bars, PositionShort())

    assert long_trail is not None
    assert short_trail is not None
    assert long_trail == short_trail


def test_trail_level_ema8_insufficient_history():
    """Return None when fewer bars than trail_ema."""
    closes = [10.0, 20.0, 30.0, 40.0]  # only 4 bars, trail_ema=8
    bars = _synthetic_bars(closes)
    strategy = KeltnerTrailEma8()

    class Position:
        size = 1.0

    assert strategy.trail_level(bars, Position()) is None
