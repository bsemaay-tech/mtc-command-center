"""Read-only reader for the night backtest artifact contract.

Discovers run-planning / run-status / profile-separated result artifacts when
they exist and reports structured missing states when they do not. This module
never writes files, never triggers runs, and tolerates absent/invalid artifacts.

Artifact contract (per run directory under 05_BACKTEST_RESULTS, or top level):
  run_plan.json, run_status.json, artifact_index.json,
  backtest_profile_result.json, top_results.json,
  leaderboard_delta.json, benchmark_update_candidate.json

States per artifact:
  absent     -> file not found anywhere (collected in `missing`)
  invalid    -> file present but JSON could not be parsed
  incomplete -> file parsed but failed schema validation (missing/typed fields)
  usable     -> file parsed and schema-valid
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .paths import canonicalize, default_mcc_root, default_quantlens_root
from .schema import validate_json_schema

# Keep snapshot fast: bound how many run directories we probe and how large a
# single artifact we will parse synchronously.
MAX_RUN_DIRS = 150
MAX_PARSE_BYTES = 4_000_000
PROFILES = ("SOURCE_NAKED", "RISK_NORMALIZED", "MTC_LIGHT", "FULL_MTC_CANDIDATE")

# filename -> (snapshot collection key, schema rel path or None)
STRUCTURED_ARTIFACTS: dict[str, tuple[str, str | None]] = {
    "run_plan.json": ("run_plans", "06_SCHEMAS/run_plan.schema.json"),
    "run_status.json": ("run_status", "06_SCHEMAS/run_status.schema.json"),
    "artifact_index.json": ("artifact_index", "06_SCHEMAS/artifact_index.schema.json"),
    "backtest_profile_result.json": ("profile_result_files", "06_SCHEMAS/backtest_profile_result.schema.json"),
    "top_results.json": ("top_results", "06_SCHEMAS/top_results.schema.json"),
    "leaderboard_delta.json": ("leaderboard_delta", None),
    "benchmark_update_candidate.json": ("benchmark_update_candidates", None),
}

# Companion files we only report presence/path for (not parsed into the model).
COMPANION_ARTIFACTS = (
    "run_plan.md",
    "approval_package.md",
    "expected_artifacts.json",
    "progress.json",
    "heartbeat.json",
    "summary.json",
    "morning_report.md",
)

_EMPTY_COLLECTIONS = (
    "run_plans",
    "run_status",
    "artifact_index",
    "top_results",
    "leaderboard_delta",
    "benchmark_update_candidates",
)


def build_night_artifacts(mcc_root: str | Path | None = None) -> dict[str, Any]:
    root = canonicalize(mcc_root or default_mcc_root())
    quantlens_root = default_quantlens_root(root)
    results_root = quantlens_root / "05_BACKTEST_RESULTS"

    collections: dict[str, list[dict[str, Any]]] = {key: [] for key in _EMPTY_COLLECTIONS}
    collections["profile_result_files"] = []
    profile_results_rows: list[dict[str, Any]] = []
    companions: list[dict[str, Any]] = []
    warnings: list[str] = []
    schema_cache: dict[str, dict[str, Any] | None] = {}
    found_filenames: set[str] = set()

    search_dirs = _search_dirs(results_root)
    if not results_root.exists():
        warnings.append(f"results root not found: {results_root}")

    for run_dir in search_dirs:
        # Structured, parsed artifacts.
        for filename, (key, schema_rel) in STRUCTURED_ARTIFACTS.items():
            path = run_dir / filename
            if not path.is_file():
                continue
            found_filenames.add(filename)
            record = _read_artifact(path, root, run_dir, schema_rel, schema_cache, warnings)
            if filename == "backtest_profile_result.json":
                collections["profile_result_files"].append(record)
                profile_results_rows.extend(_extract_profile_rows(record))
            else:
                collections[key].append(record)
        # Companion files (presence only).
        for filename in COMPANION_ARTIFACTS:
            path = run_dir / filename
            if path.is_file():
                found_filenames.add(filename)
                companions.append(
                    {
                        "type": filename,
                        "run_id": run_dir.name if run_dir != results_root else "(root)",
                        "rel_path": _rel(path, root),
                        "state": "present",
                    }
                )

    all_contract = list(STRUCTURED_ARTIFACTS.keys()) + list(COMPANION_ARTIFACTS)
    missing = [name for name in all_contract if name not in found_filenames]

    all_records = (
        collections["run_plans"]
        + collections["run_status"]
        + collections["artifact_index"]
        + collections["profile_result_files"]
        + collections["top_results"]
        + collections["leaderboard_delta"]
        + collections["benchmark_update_candidates"]
    )

    summary = {
        "expected_types": len(all_contract),
        "present_types": len(found_filenames),
        "missing_types": len(missing),
        "files_found": len(all_records) + len(companions),
        "invalid": sum(1 for r in all_records if r["state"] == "invalid"),
        "incomplete": sum(1 for r in all_records if r["state"] == "incomplete"),
        "usable": sum(1 for r in all_records if r["state"] == "usable"),
        "profile_result_rows": len(profile_results_rows),
        "has_profile_separated_results": bool(profile_results_rows),
    }

    return {
        "schema_version": "1.0",
        "mode": "read_only",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(results_root),
        "run_plans": collections["run_plans"],
        "run_status": collections["run_status"],
        "artifact_index": collections["artifact_index"],
        "profile_results": profile_results_rows,
        "profile_result_files": collections["profile_result_files"],
        "top_results": collections["top_results"],
        "leaderboard_delta": collections["leaderboard_delta"],
        "benchmark_update_candidates": collections["benchmark_update_candidates"],
        "companions": companions,
        "missing": missing,
        "warnings": warnings,
        "summary": summary,
    }


def _search_dirs(results_root: Path) -> list[Path]:
    """Return results_root + its most-recent immediate subdirectories (bounded).

    Single, shallow scan only — no deep recursive globbing, to keep snapshot fast.
    """
    if not results_root.is_dir():
        return []
    dirs: list[tuple[float, Path]] = []
    try:
        with __import__("os").scandir(results_root) as it:
            for entry in it:
                if entry.is_dir():
                    try:
                        dirs.append((entry.stat().st_mtime, Path(entry.path)))
                    except OSError:
                        continue
    except OSError:
        return [results_root]
    dirs.sort(key=lambda pair: pair[0], reverse=True)
    bounded = [path for _, path in dirs[:MAX_RUN_DIRS]]
    return [results_root, *bounded]


def _read_artifact(
    path: Path,
    mcc_root: Path,
    run_dir: Path,
    schema_rel: str | None,
    schema_cache: dict[str, dict[str, Any] | None],
    warnings: list[str],
) -> dict[str, Any]:
    run_id = run_dir.name if run_dir != path.parent.parent else run_dir.name
    base = {
        "run_id": run_dir.name if run_dir.name else "(root)",
        "path": str(path),
        "rel_path": _rel(path, mcc_root),
        "state": "invalid",
        "issues": [],
        "data": None,
    }

    try:
        size = path.stat().st_size
    except OSError as exc:
        base["issues"] = [f"stat error: {exc}"]
        return base

    if size > MAX_PARSE_BYTES:
        base["state"] = "incomplete"
        base["issues"] = [f"file too large to parse synchronously ({size} bytes); see path"]
        base["size_bytes"] = size
        warnings.append(f"{base['rel_path']}: not parsed (>{MAX_PARSE_BYTES} bytes)")
        return base

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError, OSError) as exc:
        base["issues"] = [f"json parse error: {exc}"]
        base["state"] = "invalid"
        return base

    if isinstance(data, dict) and data.get("run_id"):
        base["run_id"] = str(data["run_id"])

    issues: list[str] = []
    if schema_rel:
        schema = _load_schema(mcc_root, schema_rel, schema_cache)
        if schema is not None:
            issues = [f"{i.path}: {i.message}" for i in validate_json_schema(data, schema)]
        else:
            issues = [f"schema missing: {schema_rel}"]

    base["issues"] = issues
    base["state"] = "usable" if not issues else "incomplete"
    base["data"] = data
    return base


def _extract_profile_rows(record: dict[str, Any]) -> list[dict[str, Any]]:
    """Flatten a profile-result file into normalized result rows.

    Only rows that declare an official profile are returned. Never fabricates
    metrics; absent fields stay absent.
    """
    if record["state"] == "invalid" or not isinstance(record.get("data"), (dict, list)):
        return []
    data = record["data"]
    doc_profile_mapping = data.get("profile_mapping") if isinstance(data, dict) else None
    raw_rows: list[Any]
    if isinstance(data, list):
        raw_rows = data
    elif isinstance(data.get("results"), list):
        raw_rows = data["results"]
    elif isinstance(data, dict) and data.get("profile"):
        raw_rows = [data]
    else:
        raw_rows = []

    rows: list[dict[str, Any]] = []
    for raw in raw_rows:
        if not isinstance(raw, dict):
            continue
        profile = raw.get("profile")
        if profile not in PROFILES:
            continue
        rows.append(
            {
                "run_id": raw.get("run_id") or record.get("run_id"),
                "strategy_id": raw.get("strategy_id"),
                "profile": profile,
                "symbol": raw.get("symbol"),
                "timeframe": raw.get("timeframe"),
                "parameter_set_id": raw.get("parameter_set_id"),
                "score_method": raw.get("score_method"),
                "score": raw.get("score"),
                "gate_summary": raw.get("gate_summary"),
                "metrics": raw.get("metrics") if isinstance(raw.get("metrics"), dict) else None,
                "benchmark": raw.get("benchmark"),
                "robustness": raw.get("robustness"),
                "promotion_status": raw.get("promotion_status"),
                # Read-only passthrough so the UI can flag non-native / research-only evidence.
                "provenance": raw.get("provenance"),
                "profile_mapping": raw.get("profile_mapping") or doc_profile_mapping,
                "source_rel_path": record.get("rel_path"),
            }
        )
    return rows


def _load_schema(
    mcc_root: Path, schema_rel: str, cache: dict[str, dict[str, Any] | None]
) -> dict[str, Any] | None:
    if schema_rel in cache:
        return cache[schema_rel]
    schema_path = mcc_root / schema_rel
    schema: dict[str, Any] | None = None
    if schema_path.is_file():
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            schema = None
    cache[schema_rel] = schema
    return schema


def _rel(path: Path, mcc_root: Path) -> str:
    try:
        return path.relative_to(mcc_root).as_posix()
    except ValueError:
        return str(path)
