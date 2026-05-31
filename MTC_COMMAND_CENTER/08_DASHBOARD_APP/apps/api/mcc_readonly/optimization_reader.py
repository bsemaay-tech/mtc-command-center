from __future__ import annotations

import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .paths import canonicalize, default_mcc_root, load_path_config, resolve_configured_path


MAX_RUNS = 80
MAX_CANDIDATES = 30
MAX_RISK_NOTES = 30
MAX_CSV_ROWS_PER_FILE = 8
RISK_NOTE_PATTERN = re.compile(r"(RISK|KNOWN|PROBLEM|LESSON|DECISION|NEXT|REVIEW|VALIDATION)", re.IGNORECASE)


def build_optimization_status(mcc_root: str | Path | None = None) -> dict[str, Any]:
    root = canonicalize(mcc_root or default_mcc_root())
    path_config = load_path_config(root)
    mtc_v2_root = resolve_configured_path(path_config.config, "mtc_v2_root")
    if mtc_v2_root is None:
        return _empty_status("mtc_v2_root_not_configured")

    optimization_root = mtc_v2_root / "reports" / "optimization"
    if not optimization_root.exists():
        return _empty_status(str(optimization_root))

    runs = _collect_runs(optimization_root)
    runs.sort(key=lambda item: item.get("_sort_mtime", 0.0), reverse=True)
    runs = runs[:MAX_RUNS]
    for run in runs:
        run.pop("_sort_mtime", None)

    top_candidates = _collect_top_candidates(optimization_root)
    risk_notes = _collect_risk_notes(optimization_root)
    worker_benchmark = _worker_benchmark(optimization_root)
    artifacts = _artifact_summary(optimization_root)

    return {
        "schema_version": "1.0",
        "generated_at": _latest_timestamp(runs, top_candidates, risk_notes),
        "source": str(optimization_root),
        "summary": _summary(runs, top_candidates, risk_notes, artifacts, worker_benchmark),
        "runs": runs,
        "top_candidates": top_candidates,
        "risk_notes": risk_notes,
        "worker_benchmark": worker_benchmark,
        "artifacts": artifacts,
    }


def _collect_runs(optimization_root: Path) -> list[dict[str, Any]]:
    runs = []
    seen_roots: set[Path] = set()
    for config_path in sorted(optimization_root.rglob("run_config.json")):
        run_root = config_path.parent
        runs.append(_run_from_config(run_root, config_path, optimization_root))
        seen_roots.add(run_root)

    for metrics_path in sorted(optimization_root.rglob("metrics.json")):
        run_root = metrics_path.parent
        if run_root in seen_roots:
            continue
        runs.append(_run_from_metrics(run_root, metrics_path, optimization_root))

    for verification_path in sorted(optimization_root.rglob("resume_smoke_verification.json")):
        run_root = verification_path.parent
        if run_root in seen_roots:
            continue
        runs.append(_run_from_resume_verification(run_root, verification_path, optimization_root))
    return runs


def _run_from_config(run_root: Path, config_path: Path, optimization_root: Path) -> dict[str, Any]:
    config = _read_json_dict(config_path)
    runtime_path = run_root / "logs" / "runtime_summary.json"
    runtime = _read_json_dict(runtime_path) if runtime_path.exists() else {}
    planned = _as_number(_first_present(config.get("planned_evaluations"), runtime.get("planned")))
    completed = _as_number(_first_present(runtime.get("completed"), runtime.get("completed_evaluations")))
    failed = _as_number(_first_present(runtime.get("failed"), runtime.get("failed_evaluations")))
    skipped = _as_number(runtime.get("skipped_already_completed"))
    stat = _newest_stat(config_path, runtime_path if runtime_path.exists() else config_path)
    return {
        "_sort_mtime": stat.st_mtime,
        "run_id": config.get("run_id") or run_root.name,
        "status": _status(planned, completed, failed, skipped),
        "source_type": "run_config",
        "source_path": str(config_path),
        "relative_source_path": _relative_to_root(config_path, optimization_root),
        "report_path": _primary_report(run_root, optimization_root),
        "started_at": config.get("started_at"),
        "deadline": runtime.get("deadline"),
        "planned_evaluations": planned,
        "completed_evaluations": completed,
        "failed_evaluations": failed,
        "skipped_already_completed": skipped,
        "max_workers": config.get("max_workers") or runtime.get("max_workers"),
        "selected_dataset_count": config.get("selected_dataset_count"),
        "unique_parameter_variants": config.get("unique_parameter_variants"),
        "walkforward_split_count": config.get("walkforward_split_count"),
        "mode": config.get("mode"),
        "warning": config.get("warning"),
        "updated_at": _timestamp(stat.st_mtime),
    }


def _run_from_metrics(run_root: Path, metrics_path: Path, optimization_root: Path) -> dict[str, Any]:
    raw = _read_json_dict(metrics_path)
    stat = metrics_path.stat()
    planned = _as_number(_first_present(raw.get("planned_evaluations"), raw.get("planned_smoke_evaluations")))
    completed = _as_number(raw.get("completed_evaluations"))
    failed = _as_number(raw.get("failed_evaluations"))
    skipped = _as_number(raw.get("skipped_already_completed"))
    return {
        "_sort_mtime": stat.st_mtime,
        "run_id": _metrics_run_id(run_root, optimization_root),
        "status": str(raw.get("status") or _status(planned, completed, failed, skipped)).upper(),
        "source_type": "metrics",
        "source_path": str(metrics_path),
        "relative_source_path": _relative_to_root(metrics_path, optimization_root),
        "report_path": _primary_report(run_root, optimization_root),
        "started_at": raw.get("started_at"),
        "ended_at": raw.get("ended_at"),
        "planned_evaluations": planned,
        "completed_evaluations": completed,
        "failed_evaluations": failed,
        "skipped_already_completed": skipped,
        "worker_count": raw.get("worker_count"),
        "max_workers": raw.get("worker_count"),
        "eval_per_second": raw.get("eval_per_second"),
        "eval_per_minute": raw.get("eval_per_minute"),
        "worker_crash_count": raw.get("worker_crash_count"),
        "rows_have_required_metadata": raw.get("rows_have_required_metadata"),
        "updated_at": _timestamp(stat.st_mtime),
    }


def _run_from_resume_verification(run_root: Path, verification_path: Path, optimization_root: Path) -> dict[str, Any]:
    raw = _read_json_dict(verification_path)
    stat = verification_path.stat()
    return {
        "_sort_mtime": stat.st_mtime,
        "run_id": run_root.name,
        "status": "COMPLETED" if raw.get("ok") is not False else "CHECK",
        "source_type": "resume_verification",
        "source_path": str(verification_path),
        "relative_source_path": _relative_to_root(verification_path, optimization_root),
        "report_path": _primary_report(run_root, optimization_root),
        "verified_files": raw.get("verified_files"),
        "updated_at": _timestamp(stat.st_mtime),
    }


def _collect_top_candidates(optimization_root: Path) -> list[dict[str, Any]]:
    candidates = []
    for csv_path in _ranked_csv_paths(optimization_root):
        candidates.extend(_read_candidate_csv(csv_path, optimization_root))
    candidates = _dedupe_candidates(candidates)
    candidates.sort(key=lambda item: item.get("_sort_score", float("-inf")), reverse=True)
    candidates = candidates[:MAX_CANDIDATES]
    for candidate in candidates:
        candidate.pop("_sort_score", None)
    return candidates


def _dedupe_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: dict[tuple[Any, ...], dict[str, Any]] = {}
    for candidate in candidates:
        key = (
            candidate.get("candidate_id"),
            candidate.get("symbol") or candidate.get("symbols_tested"),
            candidate.get("timeframe") or candidate.get("timeframes_tested"),
        )
        current = deduped.get(key)
        if current is None or (candidate.get("_sort_score") or 0) > (current.get("_sort_score") or 0):
            deduped[key] = candidate
    return list(deduped.values())


def _ranked_csv_paths(optimization_root: Path) -> list[Path]:
    names = {
        "ranked_candidates.csv",
        "robust_medium_candidates.csv",
        "robust_strict_candidates.csv",
        "per_asset_timeframe_seed_candidates.csv",
    }
    return sorted(path for path in optimization_root.rglob("*.csv") if path.name in names)


def _read_candidate_csv(path: Path, optimization_root: Path) -> list[dict[str, Any]]:
    candidates = []
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for index, row in enumerate(reader):
                if index >= MAX_CSV_ROWS_PER_FILE:
                    break
                candidates.append(_candidate_from_row(row, path, optimization_root, index + 1))
    except Exception:
        return []
    return candidates


def _candidate_from_row(row: dict[str, Any], path: Path, optimization_root: Path, rank: int) -> dict[str, Any]:
    params = _json_dict(row.get("params_json"))
    score = _as_number(row.get("score"))
    return {
        "_sort_score": score if score is not None else 0.0,
        "candidate_id": row.get("parameter_set_id") or row.get("parameter_hash") or f"{path.stem}:{rank}",
        "rank": _as_number(row.get("rank")) or rank,
        "source_type": path.name.removesuffix(".csv"),
        "parameter_hash": row.get("parameter_hash"),
        "status": row.get("status") or row.get("robust_level") or row.get("confidence") or "RANKED",
        "score": score,
        "symbol": row.get("symbol"),
        "timeframe": row.get("timeframe"),
        "symbols_tested": row.get("symbols_tested"),
        "timeframes_tested": row.get("timeframes_tested"),
        "profit_factor": _as_number(row.get("profit_factor") or row.get("median_test_profit_factor")),
        "test_net_profit_pct": _as_number(row.get("test_net_profit_pct") or row.get("median_test_net_profit_pct")),
        "worst_test_drawdown_pct": _as_number(row.get("worst_test_drawdown_pct") or row.get("max_drawdown_pct")),
        "walkforward_consistency": _as_number(row.get("walkforward_consistency")),
        "positive_window_ratio": _as_number(row.get("positive_window_ratio")),
        "notes": row.get("notes") or row.get("regime_warning"),
        "param_preview": _param_preview(params, row),
        "relative_source_path": _relative_to_root(path, optimization_root),
        "updated_at": _timestamp(path.stat().st_mtime),
    }


def _collect_risk_notes(optimization_root: Path) -> list[dict[str, Any]]:
    notes = []
    for path in sorted(optimization_root.rglob("*.md")):
        if not RISK_NOTE_PATTERN.search(path.name):
            continue
        stat = path.stat()
        notes.append(
            {
                "_sort_mtime": stat.st_mtime,
                "title": _markdown_title(path),
                "relative_path": _relative_to_root(path, optimization_root),
                "updated_at": _timestamp(stat.st_mtime),
            }
        )
    notes.sort(key=lambda item: item.get("_sort_mtime", 0.0), reverse=True)
    notes = notes[:MAX_RISK_NOTES]
    for note in notes:
        note.pop("_sort_mtime", None)
    return notes


def _worker_benchmark(optimization_root: Path) -> dict[str, Any]:
    summary_path = optimization_root / "worker_scaling_benchmark" / "summaries" / "WORKER_SCALING_SUMMARY.csv"
    if not summary_path.exists():
        return {"available": False}

    rows = []
    with summary_path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append(row)
    if not rows:
        return {"available": False, "relative_source_path": _relative_to_root(summary_path, optimization_root)}

    best = max(rows, key=lambda row: _as_number(row.get("eval_per_second")) or 0.0)
    recommended = next((row for row in rows if row.get("classification") == "RECOMMENDED_FOR_OVERNIGHT_RESUME"), best)
    return {
        "available": True,
        "recommended_worker_count": _as_number(recommended.get("worker_count")),
        "recommended_eval_per_second": _as_number(recommended.get("eval_per_second")),
        "best_worker_count": _as_number(best.get("worker_count")),
        "best_eval_per_second": _as_number(best.get("eval_per_second")),
        "benchmark_rows": len(rows),
        "relative_source_path": _relative_to_root(summary_path, optimization_root),
        "updated_at": _timestamp(summary_path.stat().st_mtime),
    }


def _artifact_summary(optimization_root: Path) -> dict[str, Any]:
    files = [path for path in optimization_root.rglob("*") if path.is_file()]
    return {
        "file_count": len(files),
        "metrics_files": sum(1 for path in files if path.name == "metrics.json"),
        "runtime_summary_files": sum(1 for path in files if path.name == "runtime_summary.json"),
        "run_config_files": sum(1 for path in files if path.name == "run_config.json"),
        "ranked_csv_files": len(_ranked_csv_paths(optimization_root)),
        "markdown_reports": sum(1 for path in files if path.suffix.lower() == ".md"),
    }


def _summary(
    runs: list[dict[str, Any]],
    top_candidates: list[dict[str, Any]],
    risk_notes: list[dict[str, Any]],
    artifacts: dict[str, Any],
    worker_benchmark: dict[str, Any],
) -> dict[str, Any]:
    completed = sum(1 for run in runs if run.get("status") == "COMPLETED")
    failed_evaluations = sum(_as_number(run.get("failed_evaluations")) or 0 for run in runs)
    planned_evaluations = sum(_as_number(run.get("planned_evaluations")) or 0 for run in runs)
    completed_evaluations = sum(_as_number(run.get("completed_evaluations")) or 0 for run in runs)
    return {
        "total_runs": len(runs),
        "completed_runs": completed,
        "partial_or_check_runs": len(runs) - completed,
        "planned_evaluations": planned_evaluations,
        "completed_evaluations": completed_evaluations,
        "failed_evaluations": failed_evaluations,
        "top_candidate_count": len(top_candidates),
        "risk_note_count": len(risk_notes),
        "ranked_csv_files": artifacts.get("ranked_csv_files", 0),
        "latest_run_id": runs[0].get("run_id") if runs else None,
        "recommended_worker_count": worker_benchmark.get("recommended_worker_count"),
    }


def _status(planned: float | None, completed: float | None, failed: float | None, skipped: float | None) -> str:
    planned_value = planned or 0
    completed_value = completed or 0
    skipped_value = skipped or 0
    failed_value = failed or 0
    if failed_value > 0:
        return "PARTIAL_WITH_FAILURES"
    if planned_value and completed_value + skipped_value >= planned_value:
        return "COMPLETED"
    if completed_value > 0:
        return "PARTIAL"
    return "UNKNOWN"


def _primary_report(run_root: Path, optimization_root: Path) -> str | None:
    candidates = sorted(run_root.glob("*.md")) + sorted((run_root / "reports").glob("*.md"))
    if not candidates:
        return None
    return _relative_to_root(candidates[0], optimization_root)


def _metrics_run_id(run_root: Path, optimization_root: Path) -> str:
    try:
        relative = run_root.relative_to(optimization_root)
    except ValueError:
        return run_root.name
    return ":".join(relative.parts)


def _param_preview(params: dict[str, Any], row: dict[str, Any]) -> str:
    source = params or row
    keys = ["signal_mode", "st_factor", "global_atr_length", "sl_atr_mult", "tp_mode", "tp_r_multiple", "risk_long", "risk_short"]
    parts = [f"{key}={source.get(key)}" for key in keys if source.get(key) not in (None, "")]
    return ", ".join(parts[:6])


def _markdown_title(path: Path) -> str:
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                return stripped.lstrip("#").strip() or path.stem
            if stripped:
                return stripped[:120]
    except Exception:
        pass
    return path.stem


def _json_dict(value: Any) -> dict[str, Any]:
    if not value:
        return {}
    try:
        raw = json.loads(str(value))
    except json.JSONDecodeError:
        return {}
    return raw if isinstance(raw, dict) else {}


def _read_json_dict(path: Path) -> dict[str, Any]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return raw if isinstance(raw, dict) else {}


def _newest_stat(*paths: Path):
    return max((path.stat() for path in paths), key=lambda stat: stat.st_mtime)


def _latest_timestamp(*collections: list[dict[str, Any]]) -> str | None:
    timestamps: list[str] = []
    for collection in collections:
        timestamps.extend(item.get("updated_at") for item in collection if item.get("updated_at"))
    return max(timestamps) if timestamps else None


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _as_number(value: Any) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return None


def _first_present(*values: Any) -> Any:
    for value in values:
        if value is not None:
            return value
    return None


def _timestamp(epoch_seconds: float) -> str:
    return datetime.fromtimestamp(epoch_seconds, timezone.utc).isoformat()


def _empty_status(source: str) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "generated_at": None,
        "source": source,
        "summary": {
            "total_runs": 0,
            "completed_runs": 0,
            "partial_or_check_runs": 0,
            "planned_evaluations": 0,
            "completed_evaluations": 0,
            "failed_evaluations": 0,
            "top_candidate_count": 0,
            "risk_note_count": 0,
            "ranked_csv_files": 0,
            "latest_run_id": None,
            "recommended_worker_count": None,
        },
        "runs": [],
        "top_candidates": [],
        "risk_notes": [],
        "worker_benchmark": {"available": False},
        "artifacts": {},
    }
