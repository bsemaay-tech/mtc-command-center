"""Generate provisional golden signals from the fixture with a reference rule.

This deliberately does not import the production strategy class. It is the task
3b fallback path for a night where a read-only QuantLens source run is infeasible.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean
from typing import Any


def _rows(path: Path) -> list[dict[str, float | str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return [
            {
                "ts": row["ts"],
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"]),
                "volume": float(row["volume"]),
            }
            for row in csv.DictReader(handle)
        ]


def _runtime_ts(value: str) -> str:
    return value.replace("+00:00", "Z")


def generate_golden_from_csv(
    csv_path: str | Path,
    kc_length: int = 20,
    kc_mult: float = 2.0,
    atr_length: int = 20,
) -> dict[str, Any]:
    bars = _rows(Path(csv_path))
    signals: list[dict[str, Any]] = []
    last_direction: str | None = None

    true_ranges: list[float] = []
    prev_close: float | None = None
    for bar in bars:
        high = float(bar["high"])
        low = float(bar["low"])
        close = float(bar["close"])
        if prev_close is None:
            tr = high - low
        else:
            tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
        true_ranges.append(tr)
        prev_close = close

    for idx in range(max(kc_length, atr_length), len(bars)):
        closes = [float(row["close"]) for row in bars[idx - kc_length : idx]]
        atr = mean(true_ranges[idx - atr_length : idx])
        mid = mean(closes)
        upper = mid + kc_mult * atr
        lower = mid - kc_mult * atr
        close = float(bars[idx]["close"])

        direction: str | None = None
        if close > upper:
            direction = "LONG"
        elif close < lower:
            direction = "SHORT"

        if direction and direction != last_direction:
            signals.append(
                {
                    "ts": _runtime_ts(str(bars[idx]["ts"])),
                    "direction": direction,
                    "ref_price": close,
                    "reason": f"close {'above' if direction == 'LONG' else 'below'} keltner",
                }
            )
            last_direction = direction

    return {
        "provisional": True,
        "source": "synthetic_fixture_reference_keltner",
        "bar_alignment": "UTC_1h_24x7_close_confirmed_mkt_next",
        "params": {
            "kc_length": kc_length,
            "kc_mult": kc_mult,
            "atr_length": atr_length,
            "trail_ema": 8,
        },
        "signals": signals,
    }


def main() -> None:
    fixture = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "BTC_1h.csv"
    out_path = fixture.with_name("golden_signals.json")
    out_path.write_text(
        json.dumps(generate_golden_from_csv(fixture), indent=2) + "\n",
        encoding="utf-8",
    )
    print(out_path)


if __name__ == "__main__":
    main()
