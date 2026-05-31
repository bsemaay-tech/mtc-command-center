from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)


def sma(values: list[float], length: int) -> list[float | None]:
    out: list[float | None] = []
    for index in range(len(values)):
        if index + 1 < length:
            out.append(None)
        else:
            out.append(sum(values[index + 1 - length : index + 1]) / length)
    return out


def main() -> None:
    closes = [100, 101, 102, 99, 98, 103, 105, 104, 106, 108]
    timestamps = [f"2026-01-01T0{index}:00:00Z" for index in range(len(closes))]
    fast = sma(closes, 2)
    slow = sma(closes, 4)
    trades = []
    position = None
    for index in range(1, len(closes)):
        if fast[index - 1] is None or slow[index - 1] is None or fast[index] is None or slow[index] is None:
            continue
        long_cross = fast[index - 1] <= slow[index - 1] and fast[index] > slow[index]
        close_cross = fast[index - 1] >= slow[index - 1] and fast[index] < slow[index]
        if long_cross and position != "long":
            position = "long"
            trades.append({"trade_id": len(trades) + 1, "timestamp": timestamps[index], "bar_index": index, "event_type": "ENTRY", "side": "long", "qty": 1, "price": closes[index], "reason": "MA_CROSS"})
        elif close_cross and position == "long":
            position = None
            trades.append({"trade_id": len(trades) + 1, "timestamp": timestamps[index], "bar_index": index, "event_type": "EXIT", "side": "long", "qty": 1, "price": closes[index], "reason": "MA_CROSS_CLOSE"})
    with (OUT / "pynecore_poc_trades.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["trade_id", "timestamp", "bar_index", "event_type", "side", "qty", "price", "reason"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(trades)
    (OUT / "pynecore_poc_stats.json").write_text(json.dumps({"trade_count": len(trades), "initial_capital": 10000}, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
