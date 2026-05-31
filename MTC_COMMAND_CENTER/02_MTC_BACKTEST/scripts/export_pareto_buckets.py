from __future__ import annotations

import argparse
import json
from pathlib import Path


def assign_bucket(max_dd_pct: float) -> str:
    if max_dd_pct <= 15.0:
        return "low_risk"
    if max_dd_pct <= 30.0:
        return "mid_risk"
    return "high_risk"


def _sort_key(item: dict) -> tuple[float, float, int]:
    return (
        -float(item.get("net_profit", 0.0)),
        float(item.get("max_dd_pct", item.get("dd_pct", 0.0))),
        int(item.get("trial_id", item.get("idx", 0))),
    )


def bucket_top_k(rows: list[dict], top_k: int) -> dict[str, list[dict]]:
    buckets: dict[str, list[dict]] = {"low_risk": [], "mid_risk": [], "high_risk": []}
    for row in rows:
        bucket = assign_bucket(float(row.get("max_dd_pct", row.get("dd_pct", 0.0))))
        buckets[bucket].append(row)
    for name in buckets:
        buckets[name] = sorted(buckets[name], key=_sort_key)[:top_k]
    return buckets


def main() -> None:
    parser = argparse.ArgumentParser(description="Bucket Pareto candidates by risk profile and export top-K per bucket.")
    parser.add_argument("--pareto", required=True, help="Input Pareto JSON")
    parser.add_argument("--outdir", required=True, help="Output folder")
    parser.add_argument("--top-k", type=int, default=5, help="Top rows per bucket")
    args = parser.parse_args()

    raw = json.loads(Path(args.pareto).read_text(encoding="utf-8"))
    rows = raw["items"] if isinstance(raw, dict) and "items" in raw else raw
    if not isinstance(rows, list):
        raise ValueError("Unsupported pareto JSON format: expected list or object with 'items' list")
    buckets = bucket_top_k(rows, args.top_k)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    for name, items in buckets.items():
        path = outdir / f"{name}_top{args.top_k}.json"
        path.write_text(json.dumps(items, indent=2), encoding="utf-8")
        print(f"Wrote: {path}")


if __name__ == "__main__":
    main()
