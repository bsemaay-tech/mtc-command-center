from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

METRICS = ("net_profit", "max_dd_pct", "profit_factor", "win_rate", "total_trades")


def _to_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def load_metric_rows(path: Path) -> list[dict[str, float]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            rows.append({m: _to_float(row.get(m, "0")) for m in METRICS})
    return rows


def summarize(rows: list[dict[str, float]]) -> dict[str, float]:
    if not rows:
        return {f"{m}_mean": 0.0 for m in METRICS}
    out: dict[str, float] = {}
    count = float(len(rows))
    for metric in METRICS:
        out[f"{metric}_mean"] = sum(r[metric] for r in rows) / count
    return out


def compare(a: dict[str, float], b: dict[str, float]) -> dict[str, float]:
    return {k: b.get(k, 0.0) - a.get(k, 0.0) for k in sorted(set(a) | set(b))}


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare optimizer objective summaries across two trial CSV files.")
    parser.add_argument("--run-a", required=True, help="First trials CSV")
    parser.add_argument("--run-b", required=True, help="Second trials CSV")
    parser.add_argument("--out", required=False, help="Optional output JSON")
    args = parser.parse_args()

    a_rows = load_metric_rows(Path(args.run_a))
    b_rows = load_metric_rows(Path(args.run_b))
    summary_a = summarize(a_rows)
    summary_b = summarize(b_rows)
    delta = compare(summary_a, summary_b)
    payload = {"run_a": summary_a, "run_b": summary_b, "delta_b_minus_a": delta}

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"Wrote: {out}")
    else:
        print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
