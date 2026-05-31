from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import median
from typing import Any


ROBUST_FILTERS = {
    "min_walkforward_consistency": 0.70,
    "min_validation_positive_ratio": 0.50,
    "min_test_positive_ratio": 0.50,
    "min_positive_timeframe_count_when_multiple": 2,
    "min_positive_symbol_count_when_multiple": 2,
    "max_drawdown_pct": 35.0,
    "min_total_trades": 20,
}


def finite_number(value: Any) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def normalize(value: float, low: float, high: float) -> float:
    if high <= low:
        return 0.0
    return max(0.0, min(1.0, (value - low) / (high - low)))


def variant_hash_from_row(row: dict[str, Any]) -> str:
    return str(row.get("parameter_hash") or row.get("variant_id") or "")


def _float(row: dict[str, Any], key: str, default: float = 0.0) -> float:
    value = row.get(key, default)
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _int(row: dict[str, Any], key: str, default: int = 0) -> int:
    value = row.get(key, default)
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def robust_split_ok(row: dict[str, Any]) -> bool:
    return (
        finite_number(row.get("net_profit_pct"))
        and finite_number(row.get("profit_factor"))
        and finite_number(row.get("max_drawdown_pct"))
        and _float(row, "net_profit_pct") > 0.0
        and _float(row, "profit_factor") > 1.0
        and _float(row, "max_drawdown_pct") <= 35.0
        and _int(row, "total_trades") >= 20
        and str(row.get("dataset_hash_valid", "False")).lower() == "true"
        and str(row.get("failed_runner", "False")).lower() != "true"
    )


def score_candidates(evaluations: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in evaluations:
        grouped[variant_hash_from_row(row)].append(row)

    candidates: list[dict[str, Any]] = []
    robust: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for parameter_hash, rows in grouped.items():
        split_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            split_groups[str(row.get("split_type", ""))].append(row)
        test_rows = split_groups.get("test", [])
        validation_rows = split_groups.get("validation", [])
        train_rows = split_groups.get("train", [])
        positive_test = [row for row in test_rows if robust_split_ok(row)]
        positive_validation = [row for row in validation_rows if robust_split_ok(row)]
        positive_train = [row for row in train_rows if robust_split_ok(row)]
        timeframes = sorted({str(row.get("timeframe_normalized", "")) for row in rows})
        symbols = sorted({str(row.get("symbol", "")) for row in rows})
        positive_timeframes = sorted({str(row.get("timeframe_normalized", "")) for row in positive_test})
        positive_symbols = sorted({str(row.get("symbol", "")) for row in positive_test})
        validation_positive_ratio = len(positive_validation) / max(1, len(validation_rows))
        test_positive_ratio = len(positive_test) / max(1, len(test_rows))

        test_np = [_float(row, "net_profit_pct") for row in test_rows if finite_number(row.get("net_profit_pct"))]
        test_pf = [_float(row, "profit_factor") for row in test_rows if finite_number(row.get("profit_factor"))]
        test_dd = [_float(row, "max_drawdown_pct") for row in test_rows if finite_number(row.get("max_drawdown_pct"))]
        trade_counts = [_int(row, "total_trades") for row in rows]
        median_test_np = median(test_np) if test_np else 0.0
        median_test_pf = median(test_pf) if test_pf else 0.0
        worst_dd = max(test_dd) if test_dd else 999.0
        consistency = len(positive_test) / max(1, len(test_rows))
        timeframe_robustness = len(positive_timeframes) / max(1, len(timeframes))
        symbol_robustness = len(positive_symbols) / max(1, len(symbols))
        cross_timeframe_status = "MULTI_TIMEFRAME_VALIDATED" if len(timeframes) >= 2 else "INSUFFICIENT_TIMEFRAME_COVERAGE"
        cross_symbol_status = "MULTI_SYMBOL_VALIDATED" if len(symbols) >= 2 else "INSUFFICIENT_SYMBOL_COVERAGE"
        trade_quality = normalize(median(trade_counts) if trade_counts else 0.0, 20.0, 200.0)
        score = (
            0.25 * normalize(median_test_np, 0.0, 30.0)
            + 0.20 * normalize(median_test_pf, 1.0, 2.5)
            + 0.20 * (1.0 - normalize(worst_dd, 0.0, 35.0))
            + 0.15 * consistency
            + 0.10 * timeframe_robustness
            + 0.10 * trade_quality
        )
        candidate = {
            "parameter_hash": parameter_hash,
            "profile": rows[0].get("profile", ""),
            "variant_id": rows[0].get("variant_id", ""),
            "params_json": rows[0].get("params_json", ""),
            "evaluations": len(rows),
            "symbols_tested": "|".join(symbols),
            "timeframes_tested": "|".join(timeframes),
            "positive_test_timeframes": "|".join(positive_timeframes),
            "positive_test_symbols": "|".join(positive_symbols),
            "positive_timeframe_count": len(positive_timeframes),
            "positive_symbol_count": len(positive_symbols),
            "median_test_net_profit_pct": median_test_np,
            "median_test_profit_factor": median_test_pf,
            "worst_test_drawdown_pct": worst_dd,
            "walkforward_consistency": consistency,
            "validation_positive_ratio": validation_positive_ratio,
            "test_positive_ratio": test_positive_ratio,
            "cross_timeframe_robustness": timeframe_robustness,
            "cross_symbol_robustness": symbol_robustness,
            "cross_timeframe_status": cross_timeframe_status,
            "cross_symbol_status": cross_symbol_status,
            "trade_count_quality": trade_quality,
            "score": score,
            "train_positive_count": len(positive_train),
            "validation_positive_count": len(positive_validation),
            "test_positive_count": len(positive_test),
            "train_total_count": len(train_rows),
            "validation_total_count": len(validation_rows),
            "test_total_count": len(test_rows),
        }
        is_robust = (
            len(train_rows) > 0
            and len(validation_rows) > 0
            and len(test_rows) > 0
            and len(positive_train) == len(train_rows)
            and len(positive_validation) == len(validation_rows)
            and len(positive_test) == len(test_rows)
            and consistency >= ROBUST_FILTERS["min_walkforward_consistency"]
            and validation_positive_ratio >= ROBUST_FILTERS["min_validation_positive_ratio"]
            and test_positive_ratio >= ROBUST_FILTERS["min_test_positive_ratio"]
            and (
                len(timeframes) < 2
                or len(positive_timeframes) >= ROBUST_FILTERS["min_positive_timeframe_count_when_multiple"]
            )
            and (
                len(symbols) < 2
                or len(positive_symbols) >= ROBUST_FILTERS["min_positive_symbol_count_when_multiple"]
            )
            and len(symbols) >= 2
        )
        candidate["robust_candidate"] = is_robust
        if is_robust:
            robust.append(candidate)
        else:
            reasons = []
            if len(positive_train) < len(train_rows):
                reasons.append("train_not_all_positive")
            if len(positive_validation) < len(validation_rows):
                reasons.append("validation_not_all_positive")
            if len(positive_test) < len(test_rows):
                reasons.append("test_not_all_positive")
            if consistency < ROBUST_FILTERS["min_walkforward_consistency"]:
                reasons.append("walkforward_consistency_below_0_70")
            if validation_positive_ratio < ROBUST_FILTERS["min_validation_positive_ratio"]:
                reasons.append("validation_positive_ratio_below_0_50")
            if test_positive_ratio < ROBUST_FILTERS["min_test_positive_ratio"]:
                reasons.append("test_positive_ratio_below_0_50")
            if len(timeframes) >= 2 and len(positive_timeframes) < ROBUST_FILTERS["min_positive_timeframe_count_when_multiple"]:
                reasons.append("positive_timeframe_count_below_2")
            if len(symbols) >= 2 and len(positive_symbols) < ROBUST_FILTERS["min_positive_symbol_count_when_multiple"]:
                reasons.append("positive_symbol_count_below_2")
            if len(symbols) < 2:
                reasons.append("insufficient_symbol_coverage_not_production_robust")
            rejected.append({**candidate, "reject_reasons": reasons})
        candidates.append(candidate)

    candidates.sort(key=lambda row: float(row["score"]), reverse=True)
    robust.sort(key=lambda row: float(row["score"]), reverse=True)
    return {"ranked": candidates, "robust": robust, "rejected": rejected}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row.keys()})
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def summarize_by(evaluations: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in evaluations:
        groups[str(row.get(key, ""))].append(row)
    result = []
    for value, rows in groups.items():
        test_rows = [row for row in rows if row.get("split_type") == "test"]
        result.append(
            {
                key: value,
                "evaluations": len(rows),
                "test_evaluations": len(test_rows),
                "positive_test_evaluations": len([row for row in test_rows if robust_split_ok(row)]),
                "median_test_net_profit_pct": median([_float(row, "net_profit_pct") for row in test_rows]) if test_rows else 0.0,
                "median_test_profit_factor": median([_float(row, "profit_factor") for row in test_rows]) if test_rows else 0.0,
                "worst_test_drawdown_pct": max([_float(row, "max_drawdown_pct", 999.0) for row in test_rows]) if test_rows else 0.0,
            }
        )
    return sorted(result, key=lambda row: str(row[key]))


def write_outputs(evaluations: list[dict[str, Any]], out_root: Path) -> None:
    scored = score_candidates(evaluations)
    write_csv(out_root / "results/all_evaluations.csv", evaluations)
    write_csv(out_root / "ranked/all_unique_variants.csv", scored["ranked"])
    write_csv(out_root / "ranked/ranked_candidates.csv", scored["ranked"])
    write_csv(out_root / "ranked/robust_candidates.csv", scored["robust"])
    (out_root / "ranked/rejected_candidates.json").write_text(json.dumps(scored["rejected"], indent=2, sort_keys=True), encoding="utf-8")
    failed = [row for row in evaluations if str(row.get("failed_runner", "False")).lower() == "true"]
    (out_root / "failures/failed_evaluations.json").parent.mkdir(parents=True, exist_ok=True)
    (out_root / "failures/failed_evaluations.json").write_text(json.dumps(failed, indent=2, sort_keys=True), encoding="utf-8")
    write_csv(out_root / "cross_timeframe/per_timeframe_summary.csv", summarize_by(evaluations, "timeframe_normalized"))
    write_csv(out_root / "cross_symbol/per_symbol_summary.csv", summarize_by(evaluations, "symbol"))
    write_csv(out_root / "walkforward/per_window_summary.csv", summarize_by(evaluations, "window_id"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evaluations", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    with Path(args.evaluations).open("r", encoding="utf-8", newline="") as fh:
        evaluations = list(csv.DictReader(fh))
    write_outputs(evaluations, Path(args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
