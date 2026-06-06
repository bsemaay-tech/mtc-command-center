#!/usr/bin/env python
"""Estimate Probabilistic Backtest Overfitting from CPCV split returns."""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
from statistics import mean, median

TOOLS_DIR = Path(__file__).resolve().parent


def candidate_id(row: dict) -> str:
    return f"{row.get('strategy')}|{row.get('symbol')}|{row.get('timeframe')}"


def load_cpcv_matrix(path: Path) -> tuple[list[str], list[list[float]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = [r for r in data.get("results", []) if r.get("status") == "OK" and r.get("split_results")]
    if not rows:
        raise ValueError("no CPCV rows with split_results found")

    split_count = min(len(r["split_results"]) for r in rows)
    ids = [candidate_id(r) for r in rows]
    matrix = [[float(s["return_pct"]) for s in r["split_results"][:split_count]] for r in rows]
    return ids, matrix


def percentile_rank(values: list[float], selected: float) -> float:
    if len(values) <= 1:
        return 0.5
    below = sum(1 for value in values if value < selected)
    equal = sum(1 for value in values if value == selected)
    return (below + 0.5 * equal) / len(values)


def logit(p: float) -> float:
    eps = 1e-6
    p = min(1.0 - eps, max(eps, p))
    return math.log(p / (1.0 - p))


def estimate_pbo(ids: list[str], matrix: list[list[float]], max_combinations: int = 0) -> dict:
    n_candidates = len(ids)
    n_splits_available = len(matrix[0]) if matrix else 0
    if n_candidates < 2:
        raise ValueError("PBO needs at least 2 candidates/configurations")
    if n_splits_available < 2:
        raise ValueError("PBO needs at least 2 CPCV splits")

    usable = n_splits_available - (n_splits_available % 2)
    half = usable // 2
    n_splits = usable
    dropped_note = (
        f"dropped {n_splits_available - usable} column(s) for symmetric CSCV partition"
        if usable < n_splits_available else None
    )

    combos = []
    for combo in itertools.combinations(range(n_splits), half):
        if 0 not in combo:
            continue  # skip complement duplicates
        combos.append(combo)
    if max_combinations > 0:
        combos = combos[:max_combinations]

    records = []
    lambdas = []
    for train_idx in combos:
        train_set = set(train_idx)
        test_idx = [i for i in range(n_splits) if i not in train_set]
        train_means = [mean(row[i] for i in train_idx) for row in matrix]
        test_means = [mean(row[i] for i in test_idx) for row in matrix]
        winner_idx = max(range(n_candidates), key=lambda i: train_means[i])
        pct = percentile_rank(test_means, test_means[winner_idx])
        lam = logit(pct)
        lambdas.append(lam)
        records.append({
            "train_splits": list(train_idx),
            "test_splits": test_idx,
            "winner": ids[winner_idx],
            "winner_train_mean": round(train_means[winner_idx], 6),
            "winner_test_mean": round(test_means[winner_idx], 6),
            "winner_oos_percentile": round(pct, 6),
            "logit_lambda": round(lam, 6),
            "overfit": lam < 0,
        })

    pbo_val = round(sum(1 for x in lambdas if x < 0) / len(lambdas), 6) if lambdas else None
    result = {
        "candidate_count": n_candidates,
        "split_count": n_splits,
        "splits_available": n_splits_available,
        "splits_used": usable,
        "cscv_combinations": len(records),
        "pbo": pbo_val,
        "lambda_median": round(median(lambdas), 6) if lambdas else None,
        "records": records,
        "status": "OK",
    }
    if pbo_val is None:
        result["status"] = "INSUFFICIENT_DATA"
        result["reason"] = "No CSCV combinations generated (check split/split_count)"
    if dropped_note:
        result["partition_note"] = dropped_note
    return result


def write_markdown(path: Path, result: dict, source: Path) -> None:
    lines = [
        "# Probabilistic Backtest Overfitting Report",
        "",
        f"- Source CPCV: `{source}`",
        f"- Candidates/configurations: `{result['candidate_count']}`",
        f"- CPCV splits: `{result['split_count']}`",
        f"- CSCV combinations: `{result['cscv_combinations']}`",
        f"- PBO: `{result['pbo']}`",
        f"- Median logit(lambda): `{result['lambda_median']}`",
        "",
        "| Train Splits | Winner | Train Mean | Test Mean | OOS Percentile | Lambda | Overfit |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in result["records"][:100]:
        lines.append(
            f"| {row['train_splits']} | `{row['winner'][:54]}` | {row['winner_train_mean']:.3f} | "
            f"{row['winner_test_mean']:.3f} | {row['winner_oos_percentile']:.3f} | "
            f"{row['logit_lambda']:.3f} | {row['overfit']} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cpcv", type=Path, default=TOOLS_DIR / "cpcv_runs" / "smoke" / "cpcv_results.json")
    parser.add_argument("--out-dir", type=Path, default=TOOLS_DIR / "pbo_runs")
    parser.add_argument("--max-combinations", type=int, default=0)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    out_json = args.out_dir / "pbo_results.json"
    out_md = args.out_dir / "PBO_REPORT.md"
    try:
        ids, matrix = load_cpcv_matrix(args.cpcv)
        result = estimate_pbo(ids, matrix, args.max_combinations)
    except ValueError as exc:
        result = {
            "candidate_count": 0,
            "split_count": 0,
            "cscv_combinations": 0,
            "pbo": None,
            "lambda_median": None,
            "records": [],
            "status": "INSUFFICIENT_DATA",
            "reason": str(exc),
        }
    out_json.write_text(json.dumps({"source": str(args.cpcv), **result}, indent=2), encoding="utf-8")
    write_markdown(out_md, result, args.cpcv)
    print(f"Wrote {out_json}")
    print(f"Wrote {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
