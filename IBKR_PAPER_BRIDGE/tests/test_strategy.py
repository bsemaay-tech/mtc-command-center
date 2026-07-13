from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

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
    # REAL golden parity: replay the bridge port over the exact BTCUSD 1h bars
    # QuantLens processed (48,077 bars) and require signal-for-signal equality
    # with the QuantLens-derived golden. See docs/18_GOLDEN_REPORT.md.
    fixture = FIXTURES / "BTC_1h_real.csv"
    golden = json.loads((FIXTURES / "golden_signals.json").read_text())
    assert golden["provisional"] is False
    assert golden["signal_count"] == len(golden["signals"]) > 0
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


def test_keltner_strategy_trail_level_uses_ema8_for_long_position():
    strategy = KeltnerTrailEma8()
    bars = _load_bars(FIXTURES / "BTC_1h_real.csv")[:30]

    class Position:
        size = 1.0

    trail = strategy.trail_level(bars, Position())
    assert trail is not None
    assert trail > 0
