from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any


REJECT_RULES = {
    "min_total_trades": 20,
    "min_net_profit_pct": 0.0,
    "min_profit_factor": 1.0,
    "max_drawdown_pct": 35.0,
}


def _finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def rejection_reasons(record: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    numeric_fields = ["net_profit_pct", "profit_factor", "max_drawdown_pct", "win_rate", "total_trades"]
    for field in numeric_fields:
        if not _finite(record.get(field)):
            reasons.append(f"{field}_unavailable")
    if reasons:
        return reasons
    if int(record["total_trades"]) < REJECT_RULES["min_total_trades"]:
        reasons.append("total_trades_below_20")
    if float(record["net_profit_pct"]) <= REJECT_RULES["min_net_profit_pct"]:
        reasons.append("net_profit_not_positive")
    if float(record["profit_factor"]) <= REJECT_RULES["min_profit_factor"]:
        reasons.append("profit_factor_not_above_1")
    if float(record["max_drawdown_pct"]) > REJECT_RULES["max_drawdown_pct"]:
        reasons.append("drawdown_above_35")
    if bool(record.get("failed_runner")):
        reasons.append("failed_runner")
    if bool(record.get("dataset_hash_mismatch")):
        reasons.append("dataset_hash_mismatch")
    if bool(record.get("unrealistic_qty_or_leverage")):
        reasons.append("unrealistic_qty_or_leverage")
    return reasons


def normalize(value: float, low: float, high: float) -> float:
    if high <= low:
        return 0.0
    return max(0.0, min(1.0, (value - low) / (high - low)))


def score_record(record: dict[str, Any]) -> dict[str, Any]:
    reasons = rejection_reasons(record)
    scored = dict(record)
    scored["rejected"] = bool(reasons)
    scored["reject_reasons"] = reasons
    if reasons:
        scored["score"] = 0.0
        return scored
    net_profit = float(record["net_profit_pct"])
    profit_factor = float(record["profit_factor"])
    max_dd = float(record["max_drawdown_pct"])
    win_rate = float(record["win_rate"])
    trades = float(record["total_trades"])
    oos_quality = float(record.get("out_of_sample_quality", 0.0) or 0.0)
    scored["score"] = (
        0.30 * normalize(net_profit, 0.0, 60.0)
        + 0.20 * normalize(profit_factor, 1.0, 3.0)
        + 0.20 * (1.0 - normalize(max_dd, 0.0, 35.0))
        + 0.10 * normalize(win_rate, 35.0, 70.0)
        + 0.10 * normalize(trades, 20.0, 200.0)
        + 0.10 * max(0.0, min(1.0, oos_quality))
    )
    return scored


def write_scored_outputs(records: list[dict[str, Any]], out_dir: Path) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    scored = [score_record(record) for record in records]
    ranked = sorted((row for row in scored if not row["rejected"]), key=lambda row: row["score"], reverse=True)
    rejected = [row for row in scored if row["rejected"]]
    failed = [row for row in scored if row.get("failed_runner")]
    all_path = out_dir / "all_results.csv"
    ranked_path = out_dir / "ranked_results.csv"
    fieldnames = sorted({key for row in scored for key in row.keys()})
    for path, rows in [(all_path, scored), (ranked_path, ranked)]:
        with path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    rejected_path = out_dir / "rejected_variants.json"
    failed_path = out_dir / "failed_variants.json"
    top_path = out_dir / "top_20_candidates.json"
    rejected_path.write_text(json.dumps(rejected, indent=2, sort_keys=True), encoding="utf-8")
    failed_path.write_text(json.dumps(failed, indent=2, sort_keys=True), encoding="utf-8")
    top_path.write_text(json.dumps(ranked[:20], indent=2, sort_keys=True), encoding="utf-8")
    return {
        "all_results": all_path,
        "ranked_results": ranked_path,
        "rejected_variants": rejected_path,
        "failed_variants": failed_path,
        "top_20_candidates": top_path,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    input_path = Path(args.input)
    records = json.loads(input_path.read_text(encoding="utf-8"))
    write_scored_outputs(records, Path(args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
