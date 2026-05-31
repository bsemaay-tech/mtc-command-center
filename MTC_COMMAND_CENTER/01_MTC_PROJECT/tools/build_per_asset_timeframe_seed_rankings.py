from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import median
from typing import Any


RESEARCH_WARNING = "Research seed only; not Pine default; not production parameter."


def finite_number(value: Any) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def as_float(row: dict[str, Any], key: str, default: float = 0.0) -> float:
    try:
        return float(row.get(key, default))
    except (TypeError, ValueError):
        return default


def as_int(row: dict[str, Any], key: str, default: int = 0) -> int:
    try:
        return int(float(row.get(key, default)))
    except (TypeError, ValueError):
        return default


def median_or_none(values: list[float]) -> float | None:
    return median(values) if values else None


def split_rows(rows: list[dict[str, Any]], split_type: str) -> list[dict[str, Any]]:
    return [row for row in rows if str(row.get("split_type", "")).lower() == split_type]


def positive_row(row: dict[str, Any]) -> bool:
    return (
        str(row.get("failed_runner", "False")).lower() != "true"
        and str(row.get("dataset_hash_valid", "True")).lower() == "true"
        and finite_number(row.get("net_profit_pct"))
        and finite_number(row.get("profit_factor"))
        and finite_number(row.get("max_drawdown_pct"))
        and as_float(row, "net_profit_pct") > 0.0
        and as_float(row, "profit_factor") > 1.0
        and as_float(row, "max_drawdown_pct") <= 35.0
    )


def normalize(value: float, low: float, high: float) -> float:
    if high <= low:
        return 0.0
    return max(0.0, min(1.0, (value - low) / (high - low)))


def load_rows(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row.keys()}) if rows else ["status"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def params_from_row(row: dict[str, Any]) -> dict[str, Any]:
    raw = row.get("params_json") or "{}"
    try:
        parsed = json.loads(str(raw))
    except json.JSONDecodeError:
        parsed = {}
    return parsed if isinstance(parsed, dict) else {}


def summarize_regimes(rows: list[dict[str, Any]]) -> tuple[str, str]:
    warnings: list[str] = []
    summary: dict[str, Any] = {}
    for regime in ["choppy", "consolidating", "ranging", "trending"]:
        key = f"regime_{regime}_net_profit"
        values = [as_float(row, key) for row in rows if finite_number(row.get(key))]
        if values:
            total = sum(values)
            summary[regime] = round(total, 6)
            if regime in {"choppy", "consolidating"} and total < 0:
                warnings.append(f"{regime.upper()} weakness")
    return json.dumps(summary, sort_keys=True), " | ".join(warnings)


def build_seed_rankings(evaluations: list[dict[str, Any]], *, source_run_id: str, source_output_path: str, top_n: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in evaluations:
        if str(row.get("failed_runner", "False")).lower() == "true":
            continue
        symbol = str(row.get("symbol") or row.get("asset") or "")
        timeframe = str(row.get("timeframe_normalized") or row.get("timeframe") or "")
        parameter_hash = str(row.get("parameter_hash") or "")
        if not symbol or not timeframe or not parameter_hash:
            continue
        groups[(symbol, timeframe, parameter_hash)].append(row)

    candidates: list[dict[str, Any]] = []
    for (symbol, timeframe, parameter_hash), rows in groups.items():
        train_rows = split_rows(rows, "train")
        validation_rows = split_rows(rows, "validation")
        test_rows = split_rows(rows, "test")
        params = params_from_row(rows[0])
        missing_metrics = not (train_rows and validation_rows and test_rows)
        train_np = median_or_none([as_float(row, "net_profit_pct") for row in train_rows if finite_number(row.get("net_profit_pct"))])
        validation_np = median_or_none([as_float(row, "net_profit_pct") for row in validation_rows if finite_number(row.get("net_profit_pct"))])
        test_np = median_or_none([as_float(row, "net_profit_pct") for row in test_rows if finite_number(row.get("net_profit_pct"))])
        test_pf = median_or_none([as_float(row, "profit_factor") for row in test_rows if finite_number(row.get("profit_factor"))])
        max_dd = max([as_float(row, "max_drawdown_pct", 999.0) for row in rows if finite_number(row.get("max_drawdown_pct"))], default=999.0)
        win_rate = median_or_none([as_float(row, "win_rate") for row in test_rows if finite_number(row.get("win_rate"))])
        trade_count = sum(as_int(row, "total_trades") for row in rows)
        positive_windows = len([row for row in test_rows if positive_row(row)])
        positive_window_ratio = positive_windows / max(1, len(test_rows))
        walkforward_consistency = positive_window_ratio
        validation_positive_ratio = len([row for row in validation_rows if positive_row(row)]) / max(1, len(validation_rows))

        score = (
            0.30 * normalize(test_np or 0.0, 0.0, 20.0)
            + 0.20 * normalize(test_pf or 0.0, 1.0, 2.5)
            + 0.20 * (1.0 - normalize(max_dd, 0.0, 35.0))
            + 0.20 * positive_window_ratio
            + 0.10 * validation_positive_ratio
        )
        status = "INSUFFICIENT_DATA" if missing_metrics else "RESEARCH_SEED"
        if not missing_metrics and validation_positive_ratio >= 0.5 and positive_window_ratio >= 0.5 and (test_pf or 0.0) > 1.0:
            status = "MEDIUM_SEED"
        if missing_metrics or validation_positive_ratio <= 0.0 or positive_window_ratio <= 0.0:
            status = "REJECTED" if not missing_metrics else "INSUFFICIENT_DATA"
        confidence = "LOW"
        if len(rows) >= 9 and validation_positive_ratio >= 0.5 and positive_window_ratio >= 0.5:
            confidence = "MEDIUM"
        if len(rows) >= 15 and validation_positive_ratio >= 0.7 and positive_window_ratio >= 0.7:
            confidence = "HIGH"

        regime_summary, regime_warning = summarize_regimes(rows)
        warnings = [RESEARCH_WARNING]
        if regime_warning:
            warnings.append(regime_warning)
        if timeframe == "1D":
            warnings.append("1D requires separate-profile caution")

        candidates.append(
            {
                "strategy_id": "MTC_V2",
                "producer_id": str(params.get("signal_mode") or "Supertrend"),
                "asset": symbol,
                "symbol": symbol,
                "timeframe": timeframe,
                "rank": 0,
                "parameter_set_id": f"{symbol}_{timeframe}_{parameter_hash}",
                "parameter_hash": parameter_hash,
                "source_run_id": source_run_id,
                "source_output_path": source_output_path,
                "dataset_ids": "|".join(sorted({str(row.get("dataset_id", "")) for row in rows if row.get("dataset_id")})),
                "source_type_summary": "|".join(sorted({str(row.get("source_type", "")) for row in rows if row.get("source_type")})),
                "st_factor": params.get("st_factor"),
                "global_atr_length": params.get("global_atr_length"),
                "sl_atr_mult": params.get("sl_atr_mult"),
                "tp_mode": params.get("tp_mode"),
                "tp_r_multiple": params.get("tp_r_multiple"),
                "risk_long": params.get("risk_long"),
                "risk_short": params.get("risk_short"),
                "train_net_profit_pct": train_np,
                "validation_net_profit_pct": validation_np,
                "test_net_profit_pct": test_np,
                "profit_factor": test_pf,
                "max_drawdown_pct": max_dd,
                "win_rate": win_rate,
                "trade_count": trade_count,
                "walkforward_consistency": walkforward_consistency,
                "positive_window_ratio": positive_window_ratio,
                "regime_summary": regime_summary,
                "regime_warning": regime_warning,
                "status": status,
                "confidence": confidence,
                "score": score,
                "evaluations": len(rows),
                "evaluation_key_examples": "|".join(str(row.get("evaluation_key", "")) for row in rows[:3] if row.get("evaluation_key")),
                "notes": "Research seed only; not Pine default; not production parameter.",
            }
        )

    ranked: list[dict[str, Any]] = []
    for (_symbol, _timeframe), rows in defaultdict(list, {}).items():
        pass
    by_asset_tf: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in candidates:
        by_asset_tf[(str(row["symbol"]), str(row["timeframe"]))].append(row)
    for (_symbol, _timeframe), rows in sorted(by_asset_tf.items()):
        rows.sort(key=lambda item: float(item["score"]), reverse=True)
        for rank, row in enumerate(rows[:top_n], start=1):
            item = dict(row)
            item["rank"] = rank
            ranked.append(item)

    summary_rows: list[dict[str, Any]] = []
    for (symbol, timeframe), rows in sorted(by_asset_tf.items()):
        all_rows = [row for group_row in rows for row in groups[(symbol, timeframe, str(group_row["parameter_hash"]))]]
        summary_rows.append(
            {
                "asset": symbol,
                "symbol": symbol,
                "timeframe": timeframe,
                "candidate_count": len(rows),
                "seed_rows_emitted": min(top_n, len(rows)),
                "evaluation_rows": len(all_rows),
                "dataset_ids": "|".join(sorted({str(row.get("dataset_id", "")) for row in all_rows if row.get("dataset_id")})),
                "source_type_summary": "|".join(sorted({str(row.get("source_type", "")) for row in all_rows if row.get("source_type")})),
                "status": "OK" if rows else "INSUFFICIENT_DATA",
                "notes": RESEARCH_WARNING,
            }
        )
    return ranked, summary_rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evaluations", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--source-run-id", default="unknown_run")
    parser.add_argument("--source-output-path", default="")
    parser.add_argument("--top-n", type=int, default=5)
    args = parser.parse_args()

    evaluations = load_rows(Path(args.evaluations))
    ranked, summary = build_seed_rankings(
        evaluations,
        source_run_id=args.source_run_id,
        source_output_path=args.source_output_path or args.evaluations,
        top_n=args.top_n,
    )
    out = Path(args.out)
    write_csv(out / "ranked/per_asset_timeframe_seed_candidates.csv", ranked)
    write_csv(out / "ranked/per_asset_timeframe_summary.csv", summary)
    (out / "ranked/per_asset_timeframe_seed_candidates.json").write_text(
        json.dumps(ranked, indent=2, sort_keys=True, default=str),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
