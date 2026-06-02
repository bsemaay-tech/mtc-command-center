from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .paths import (
    canonicalize,
    default_mcc_root,
    default_quantlens_root,
    load_path_config,
    resolve_configured_path,
)


MAX_PARSE_BYTES = 6_000_000
MAX_RUNS = 80
SUCCESS_STATUSES = {"COMPLETED", "OK", "PASS", "SUCCESS"}
FAILED_STATUSES = {"ERROR", "FAIL", "FAILED"}


def build_backtest_status(mcc_root: str | Path | None = None) -> dict[str, Any]:
    root = canonicalize(mcc_root or default_mcc_root())
    path_config = load_path_config(root)
    mtc_v2_root = resolve_configured_path(path_config.config, "mtc_v2_root")
    if mtc_v2_root is None:
        return _empty_status("mtc_v2_root_not_configured")

    # Resolve the QuantLens root the same way registry_reader does: prefer the
    # in-repo 03_QUANTLENS, falling back to the legacy mtc_v2_root/06_QUANTLENS_LAB.
    quantlens_root = default_quantlens_root(root)
    if not quantlens_root.exists():
        quantlens_root = mtc_v2_root / "06_QUANTLENS_LAB"

    runs: list[dict[str, Any]] = []
    runs.extend(_collect_quantlens_results(quantlens_root))
    runs.extend(_collect_detached_statuses(quantlens_root))
    runs.extend(_collect_optimization_metrics(mtc_v2_root))
    runs.sort(key=lambda item: item.get("_sort_mtime", 0.0), reverse=True)
    runs = runs[:MAX_RUNS]

    for run in runs:
        run.pop("_sort_mtime", None)

    return {
        "schema_version": "1.0",
        "generated_at": _latest_timestamp(runs),
        "source": str(mtc_v2_root),
        "summary": _summary(runs),
        "runs": runs,
    }


def _collect_quantlens_results(quantlens_root: Path) -> list[dict[str, Any]]:
    root = quantlens_root / "05_BACKTEST_RESULTS"
    if not root.exists():
        return []

    runs = []
    for path in sorted(root.glob("*_results.json")):
        runs.append(_quantlens_result_run(path, root))
    return runs


def _collect_detached_statuses(quantlens_root: Path) -> list[dict[str, Any]]:
    root = quantlens_root / "05_BACKTEST_RESULTS"
    if not root.exists():
        return []
    return [_detached_status_run(path, root) for path in sorted(root.glob("**/detached/run_status.json"))]


def _collect_optimization_metrics(mtc_v2_root: Path) -> list[dict[str, Any]]:
    root = mtc_v2_root / "reports" / "optimization"
    if not root.exists():
        return []
    metrics = [_optimization_metrics_run(path, root) for path in sorted(root.glob("**/metrics.json"))]
    return metrics


def _quantlens_result_run(path: Path, root: Path) -> dict[str, Any]:
    stat = path.stat()
    base = _base_run(path, root, "quantlens_result")
    if stat.st_size > MAX_PARSE_BYTES:
        base.update(
            {
                "run_id": _run_id_from_results_path(path),
                "status": "COMPLETED",
                "warning": "large_result_json_not_loaded",
                "size_bytes": stat.st_size,
            }
        )
        return base

    try:
        raw = _read_json(path)
    except Exception as exc:
        base.update({"run_id": path.stem, "status": "ERROR", "error": str(exc)})
        return base

    if isinstance(raw, list):
        base.update(_walk_forward_summary(path, raw))
        return base
    if isinstance(raw, dict) and isinstance(raw.get("results"), list):
        if _is_matrix_walk_forward(raw):
            base.update(_matrix_walk_forward_summary(path, raw))
        else:
            base.update(_walk_forward_summary(path, raw["results"]))
        base["ended_at"] = raw.get("generated_utc")
        base["runtime_seconds"] = raw.get("runtime_seconds")
        base["workers"] = raw.get("workers")
        return base
    if isinstance(raw, dict) and ("candidate_id" in raw or "strategy" in raw) and isinstance(raw.get("summary"), dict):
        base.update(_candidate_summary(path, raw))
        return base

    base.update({"run_id": path.stem, "status": "UNKNOWN_SHAPE"})
    return base


def _detached_status_run(path: Path, root: Path) -> dict[str, Any]:
    base = _base_run(path, root, "detached_run_status")
    try:
        raw = _read_json(path)
    except Exception as exc:
        base.update({"run_id": path.parent.parent.name, "status": "ERROR", "error": str(exc)})
        return base

    status = str(raw.get("status") or "UNKNOWN").upper()
    base.update(
        {
            "run_id": raw.get("run_id") or path.parent.parent.name,
            "status": status,
            "started_at": raw.get("started_at"),
            "ended_at": raw.get("stopped_at") or raw.get("ended_at") or raw.get("updated_at"),
            "completed_evaluations": raw.get("completed_evaluations"),
            "failed_evaluations": raw.get("failed_evaluations"),
            "selected_dataset_count": raw.get("selected_dataset_count"),
            "symbol": _join_values(raw.get("symbols")),
            "timeframe": _join_values(raw.get("timeframes")),
            "external_report_path": raw.get("summary_path"),
        }
    )
    return base


def _optimization_metrics_run(path: Path, root: Path) -> dict[str, Any]:
    base = _base_run(path, root, "optimization_metrics")
    try:
        raw = _read_json(path)
    except Exception as exc:
        base.update({"run_id": path.parent.name, "status": "ERROR", "error": str(exc)})
        return base

    failed = _as_number(raw.get("failed_evaluations")) or 0
    status = "COMPLETED" if failed == 0 else "PARTIAL"
    base.update(
        {
            "run_id": path.parent.name,
            "status": status,
            "started_at": raw.get("started_at"),
            "ended_at": raw.get("ended_at"),
            "completed_evaluations": raw.get("completed_evaluations"),
            "failed_evaluations": raw.get("failed_evaluations"),
            "planned_evaluations": raw.get("planned_evaluations"),
            "eval_per_minute": raw.get("eval_per_minute"),
            "worker_count": raw.get("worker_count"),
            "worker_crash_count": raw.get("worker_crash_count"),
        }
    )
    return base


def _candidate_summary(path: Path, raw: dict[str, Any]) -> dict[str, Any]:
    summary = raw.get("summary") if isinstance(raw.get("summary"), dict) else {}
    symbol_rows = [value for value in summary.values() if isinstance(value, dict)]
    trades = [_as_number(row.get("trades")) for row in symbol_rows]
    win_rates = [_as_number(row.get("win_rate_pct")) for row in symbol_rows]
    net_returns = [_as_number(row.get("net_return_sum_pct")) for row in symbol_rows]
    avg_returns = [_as_number(row.get("avg_return_pct")) for row in symbol_rows]
    return {
        "run_id": raw.get("candidate_id") or raw.get("strategy") or _run_id_from_results_path(path),
        "status": "COMPLETED",
        "started_at": raw.get("backtest_run_at"),
        "ended_at": raw.get("backtest_run_at"),
        "symbol": _join_values(summary.keys()),
        "timeframe": "multi",
        "symbols": len(symbol_rows),
        "trades": _sum_numbers(trades),
        "avg_win_rate_pct": _avg_numbers(win_rates),
        "net_return_sum_pct": _sum_numbers(net_returns),
        "avg_return_pct": _avg_numbers(avg_returns),
    }


def _walk_forward_summary(path: Path, rows: list[Any]) -> dict[str, Any]:
    dict_rows = [row for row in rows if isinstance(row, dict)]
    statuses = [_row_status(row) for row in dict_rows]
    pass_count = sum(1 for status in statuses if status in {"PASS", "STRONG_PASS"})
    fail_count = sum(1 for status in statuses if status == "FAIL")
    test_returns = [_as_number(row.get("test_out_of_sample_return_pct")) for row in dict_rows]
    status = "PASS" if dict_rows and fail_count == 0 else "FAIL" if fail_count else "UNKNOWN"
    return {
        "run_id": path.stem,
        "status": status,
        "symbol": _join_values({row.get("symbol") for row in dict_rows if row.get("symbol")}),
        "timeframe": _join_values({row.get("timeframe") for row in dict_rows if row.get("timeframe")}),
        "evaluations": len(dict_rows),
        "pass_count": pass_count,
        "fail_count": fail_count,
        "other_count": len(dict_rows) - pass_count - fail_count,
        "best_test_return_pct": _max_numbers(test_returns),
        "worst_test_return_pct": _min_numbers(test_returns),
    }


def _is_matrix_walk_forward(raw: dict[str, Any]) -> bool:
    rows = raw.get("results")
    if not isinstance(raw.get("config"), dict) or not isinstance(rows, list):
        return False
    dict_rows = [row for row in rows[:10] if isinstance(row, dict)]
    return any("classification" in row and isinstance(row.get("summary"), dict) for row in dict_rows)


def _matrix_walk_forward_summary(path: Path, raw: dict[str, Any]) -> dict[str, Any]:
    rows = [row for row in raw.get("results", []) if isinstance(row, dict)]
    classifications = _value_counts(_row_status(row) or "UNCLASSIFIED" for row in rows)
    symbols = {row.get("symbol") for row in rows if row.get("symbol")}
    timeframes = {row.get("timeframe") for row in rows if row.get("timeframe")}
    strategies = {row.get("strategy") for row in rows if row.get("strategy")}
    trade_count = _matrix_trade_count(rows)
    return {
        "run_id": _run_id_from_results_path(path),
        "status": "COMPLETED",
        "symbol": _join_values(symbols),
        "timeframe": _join_values(timeframes),
        "symbols_tested": sorted(symbols),
        "timeframes_tested": sorted(timeframes),
        "evaluations": len(rows),
        "strategy_count": len(strategies),
        "symbol_count": len(symbols),
        "timeframe_count": len(timeframes),
        "trade_count": trade_count,
        "trades": trade_count,
        "classification_counts": classifications,
        "pass_count": classifications.get("PASS", 0) + classifications.get("STRONG_PASS", 0),
        "fail_count": classifications.get("FAIL", 0),
        "robust_final_count": sum(1 for row in rows if row.get("robust_final") is True),
        "bh_fdr_survivor_count": sum(1 for row in rows if row.get("bh_fdr_survivor") is True),
    }


def _matrix_trade_count(rows: list[dict[str, Any]]) -> int:
    total = 0.0
    for row in rows:
        summary = row.get("summary")
        if not isinstance(summary, dict):
            continue
        lockbox = summary.get("lockbox_oos")
        if not isinstance(lockbox, dict):
            continue
        trades = _as_number(lockbox.get("num_trades") or lockbox.get("trades"))
        if trades is not None:
            total += trades
    return int(total)


def _value_counts(values: Any) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        key = str(value or "UNKNOWN").upper()
        counts[key] = counts.get(key, 0) + 1
    return counts


def _summary(runs: list[dict[str, Any]]) -> dict[str, Any]:
    failed_runs = [run for run in runs if str(run.get("status", "")).upper() in FAILED_STATUSES]
    successful = [run for run in runs if str(run.get("status", "")).upper() in SUCCESS_STATUSES]
    return {
        "total_runs": len(runs),
        "last_run_id": runs[0].get("run_id") if runs else None,
        "last_successful_run": successful[0].get("run_id") if successful else None,
        "failed_runs": len(failed_runs),
        "quantlens_result_runs": sum(1 for run in runs if run.get("source_type") == "quantlens_result"),
        "detached_status_runs": sum(1 for run in runs if run.get("source_type") == "detached_run_status"),
        "optimization_metric_runs": sum(1 for run in runs if run.get("source_type") == "optimization_metrics"),
        "large_result_json_not_loaded": sum(1 for run in runs if run.get("warning") == "large_result_json_not_loaded"),
    }


def _base_run(path: Path, root: Path, source_type: str) -> dict[str, Any]:
    stat = path.stat()
    return {
        "_sort_mtime": stat.st_mtime,
        "source_type": source_type,
        "source_path": str(path),
        "relative_source_path": str(path.relative_to(root)),
        "updated_at": _timestamp(stat.st_mtime),
    }


def _row_status(row: dict[str, Any]) -> str:
    return str(row.get("status") or row.get("classification") or "").upper()


def _latest_timestamp(runs: list[dict[str, Any]]) -> str | None:
    timestamps = [run.get("updated_at") for run in runs if run.get("updated_at")]
    return max(timestamps) if timestamps else None


def _timestamp(epoch_seconds: float) -> str:
    return datetime.fromtimestamp(epoch_seconds, timezone.utc).isoformat()


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _run_id_from_results_path(path: Path) -> str:
    stem = path.stem
    if stem.endswith("_results"):
        return stem.removesuffix("_results")
    return stem


def _join_values(values: Any) -> str | None:
    if values is None:
        return None
    if isinstance(values, str):
        return values
    try:
        cleaned = sorted(str(value) for value in values if value not in (None, ""))
    except TypeError:
        return str(values)
    if not cleaned:
        return None
    if len(cleaned) > 4:
        return f"{len(cleaned)} values"
    return ", ".join(cleaned)


def _as_number(value: Any) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return None


def _sum_numbers(values: list[float | None]) -> float | None:
    numbers = [value for value in values if value is not None]
    return sum(numbers) if numbers else None


def _avg_numbers(values: list[float | None]) -> float | None:
    numbers = [value for value in values if value is not None]
    return sum(numbers) / len(numbers) if numbers else None


def _max_numbers(values: list[float | None]) -> float | None:
    numbers = [value for value in values if value is not None]
    return max(numbers) if numbers else None


def _min_numbers(values: list[float | None]) -> float | None:
    numbers = [value for value in values if value is not None]
    return min(numbers) if numbers else None


def _empty_status(source: str) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "generated_at": None,
        "source": source,
        "summary": {
            "total_runs": 0,
            "last_run_id": None,
            "last_successful_run": None,
            "failed_runs": 0,
        },
        "runs": [],
    }
