from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .backtest_reader import build_backtest_status
from .heartbeat_reader import build_overnight_heartbeat
from .json_io import read_json_file
from .liveops_reader import build_liveops_status
from .mtc_v2_reader import build_mtc_v2_readiness
from .night_artifacts_reader import build_night_artifacts
from .optimization_reader import build_optimization_status
from .paths import canonicalize, default_mcc_root
from .parity_reader import build_parity_status
from .pine_builder_reader import build_pine_builder_status
from .audit_reader import build_candidate_audit
from .ai_names_reader import (
    attach_ai_strategy_names_to_rows,
    attach_ai_strategy_names_to_scorecards,
    build_ai_strategy_names,
)
from .expert_quantlens_reader import (
    attach_expert_quantlens_to_rows,
    attach_expert_quantlens_to_scorecards,
    build_expert_quantlens,
)
from .pipeline_reader import build_candidate_pipeline
from .registry_reader import build_strategy_registry
from .research_reader import build_strategy_research
from .quantlens_reader import build_quantlens
from .scorecard_reader import attach_scorecards_to_rows, build_scorecards
from .schema import validate_json_schema
from .task_lifecycle import build_task_lifecycle


def _load_transcript_reclassification(mcc_root: Path) -> dict[str, Any] | None:
    path = mcc_root / "11_TRIAGE" / "transcript_reclassification.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


@dataclass(frozen=True)
class ReadModelFile:
    key: str
    rel_path: str
    schema_rel_path: str
    required: bool = True


READ_MODEL_FILES: tuple[ReadModelFile, ...] = (
    ReadModelFile("current_status", "03_STATUS/CURRENT_STATUS.json", "06_SCHEMAS/current_status.schema.json"),
    ReadModelFile("task_queue", "02_TASKS/TASK_QUEUE.json", "06_SCHEMAS/task_queue.schema.json"),
    ReadModelFile("task_history", "02_TASKS/TASK_HISTORY.json", "06_SCHEMAS/task_history.schema.json"),
    ReadModelFile("liveops_status", "03_STATUS/LIVEOPS_STATUS.json", "06_SCHEMAS/liveops_status.schema.json"),
    ReadModelFile("parity_status", "03_STATUS/PARITY_STATUS.json", "06_SCHEMAS/parity_status.schema.json"),
    ReadModelFile("backtest_status", "03_STATUS/BACKTEST_STATUS.json", "06_SCHEMAS/backtest_status.schema.json"),
    ReadModelFile("optimization_status", "03_STATUS/OPTIMIZATION_STATUS.json", "06_SCHEMAS/optimization_status.schema.json"),
    ReadModelFile("pine_builder_status", "03_STATUS/PINE_BUILDER_STATUS.json", "06_SCHEMAS/pine_builder_status.schema.json"),
    ReadModelFile("report_manifest", "03_STATUS/REPORT_MANIFEST.json", "06_SCHEMAS/report_manifest.schema.json"),
    ReadModelFile("strategy_registry", "05_REGISTRY/STRATEGY_REGISTRY.json", "06_SCHEMAS/strategy_registry.schema.json"),
    ReadModelFile("paths_config", "00_CONFIG/paths.example.json", "06_SCHEMAS/paths.schema.json"),
    ReadModelFile("paths_local", "00_CONFIG/paths.local.json", "06_SCHEMAS/paths.schema.json", required=False),
    ReadModelFile(
        "dashboard_config",
        "00_CONFIG/dashboard_config.example.json",
        "06_SCHEMAS/dashboard_config.schema.json",
    ),
)

_SNAPSHOT_CACHE: dict[str, tuple[float, dict[str, Any]]] = {}
_SNAPSHOT_CACHE_TTL_SECONDS = 30.0

# Full (un-slimmed) scorecards retained for the lazy-load detail endpoint. The default
# HTTP snapshot drops per-card gate ``sub_scores`` / verbose notes; the detail endpoint
# serves the full cards for one requested strategy from this cache.
_FULL_SCORECARDS_CACHE: dict[str, tuple[float, dict[str, Any]]] = {}
_FULL_SCORECARDS_TTL_SECONDS = 120.0

_GATE_KEYS = ("gate1", "gate1B", "gate2", "gate3")
_NOTES_PREVIEW_CHARS = 160


def build_read_model(mcc_root: str | Path | None = None) -> dict[str, Any]:
    root = canonicalize(mcc_root or default_mcc_root())
    files: dict[str, Any] = {}

    for item in READ_MODEL_FILES:
        result = read_json_file(root, item.rel_path, required=item.required)
        schema_issues: list[str] = []
        schema_ok: bool | None = None

        if result.exists and result.ok:
            schema_path = root / item.schema_rel_path
            if schema_path.exists():
                try:
                    schema = json.loads(schema_path.read_text(encoding="utf-8"))
                    schema_issues = [
                        f"{issue.path}: {issue.message}"
                        for issue in validate_json_schema(result.data, schema)
                    ]
                    schema_ok = not schema_issues
                except Exception as exc:
                    schema_issues = [f"schema read/validation error: {exc}"]
                    schema_ok = False
            else:
                schema_issues = [f"schema missing: {item.schema_rel_path}"]
                schema_ok = False
        elif not result.exists and not item.required:
            schema_ok = None

        record_ok = result.ok and (schema_ok is not False)
        files[item.key] = {
            "path": item.rel_path,
            "schema_path": item.schema_rel_path,
            "required": item.required,
            "exists": result.exists,
            "ok": record_ok,
            "json_ok": result.ok,
            "schema_ok": schema_ok,
            "error": result.error,
            "schema_issues": schema_issues,
            "data": result.data if result.ok else None,
        }

    required_files_ok = all(record["ok"] for record in files.values() if record["required"])
    present_optional_ok = all(record["ok"] for record in files.values() if not record["required"] and record["exists"])
    schema_validation_ok = required_files_ok and present_optional_ok

    return {
        "schema_version": "1.0",
        "mode": "read_only",
        "mcc_root": str(root),
        "summary": {
            "file_count": len(files),
            "required_file_count": sum(1 for record in files.values() if record["required"]),
            "required_files_ok": required_files_ok,
            "schema_validation_ok": schema_validation_ok,
        },
        "files": files,
    }


def _count_or_passthrough(value: Any) -> Any:
    """Collapse a heavy list to its length; preserve existing int/None as-is.

    The frontend already reads ``scorecard_v2_cases`` as either an array length or a
    plain number (see app.js), so emitting the count keeps UI behavior identical while
    dropping the large embedded case arrays from the HTTP payload.
    """
    if isinstance(value, list):
        return len(value)
    return value


def _slim_rows_cases(rows: Any) -> Any:
    if not isinstance(rows, list):
        return rows
    slimmed = []
    for row in rows:
        if isinstance(row, dict) and "scorecard_v2_cases" in row:
            new_row = dict(row)
            new_row["scorecard_v2_cases"] = _count_or_passthrough(row["scorecard_v2_cases"])
            slimmed.append(new_row)
        else:
            slimmed.append(row)
    return slimmed


def _slim_gate(gate: Any) -> Any:
    """Drop the verbose ``sub_scores`` detail from a gate object; keep score/max/status.

    The per-gate ``sub_scores`` arrays (full criterion / deduction text) are the bulk of the
    snapshot. Scores, max, and statuses stay inline so list/summary pages keep working; the
    full sub_scores are served on demand by the scorecard-detail endpoint.
    """
    if not isinstance(gate, dict) or "sub_scores" not in gate:
        return gate
    trimmed = dict(gate)
    trimmed.pop("sub_scores", None)
    return trimmed


def _slim_card(card: Any) -> Any:
    """Return a summary copy of a scorecard card with verbose gate detail removed.

    Preserves: ids, names, symbol/timeframe/profile, gate scores+statuses, gate_summary,
    promotion_status, provenance, profile_mapping, robustness, universe_mismatch, and all
    other small fields. Removes per-gate ``sub_scores`` and collapses the verbose ``notes``
    array to ``notes_count`` (+ a short ``notes_preview``).
    """
    if not isinstance(card, dict):
        return card
    out = dict(card)
    for key in _GATE_KEYS:
        if isinstance(out.get(key), dict):
            out[key] = _slim_gate(out[key])
    notes = out.get("notes")
    if isinstance(notes, list):
        out["notes_count"] = len(notes)
        first = next((str(n) for n in notes if n), "")
        out["notes_preview"] = first[:_NOTES_PREVIEW_CHARS]
        out.pop("notes", None)
    return out


def _slim_scorecard_cases(rows: Any) -> Any:
    """Drop ``scorecard_v2`` gate ``sub_scores`` from pipeline rows (kept score/status)."""
    if not isinstance(rows, list):
        return rows
    out = []
    for row in rows:
        if isinstance(row, dict) and isinstance(row.get("scorecard_v2"), dict):
            new_row = dict(row)
            v2 = dict(row["scorecard_v2"])
            for key in _GATE_KEYS:
                if isinstance(v2.get(key), dict):
                    v2[key] = _slim_gate(v2[key])
            new_row["scorecard_v2"] = v2
            out.append(new_row)
        else:
            out.append(row)
    return out


def _slim_http_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Strip heavy, UI-unused fields from the HTTP snapshot (read-only serialization only).

    Payload slimming per SNAPSHOT_PAYLOAD_PERFORMANCE_AUDIT_2026-06-16:
      - drop ``scorecards.by_strategy`` (duplicate of ``cards``; never read by the frontend);
      - omit top-level ``candidate_audit`` (CLI/tests only; not read by the frontend);
      - collapse ``candidate_pipeline.rows[].scorecard_v2_cases`` arrays to integer counts.
    M1 lazy-load slimming (full detail served via /api/scorecard-detail):
      - drop per-card gate ``sub_scores`` and verbose ``notes`` from ``scorecards.cards``;
      - drop ``scorecard_v2`` gate ``sub_scores`` from pipeline rows (scores/statuses kept).
    Underlying readers, CLI, source artifacts, and the full scorecards cache are untouched.
    """
    slimmed = dict(snapshot)
    slimmed.pop("candidate_audit", None)

    scorecards = slimmed.get("scorecards")
    if isinstance(scorecards, dict):
        scorecards = dict(scorecards)
        scorecards.pop("by_strategy", None)
        if isinstance(scorecards.get("cards"), list):
            scorecards["cards"] = [_slim_card(c) for c in scorecards["cards"]]
        slimmed["scorecards"] = scorecards

    pipeline = slimmed.get("candidate_pipeline")
    if isinstance(pipeline, dict):
        pipeline = dict(pipeline)
        if isinstance(pipeline.get("rows"), list):
            pipeline["rows"] = _slim_scorecard_cases(_slim_rows_cases(pipeline["rows"]))
        if isinstance(pipeline.get("candidates"), list):
            pipeline["candidates"] = _slim_scorecard_cases(_slim_rows_cases(pipeline["candidates"]))
        slimmed["candidate_pipeline"] = pipeline

    return slimmed


def build_scorecard_detail(
    mcc_root: str | Path | None = None, strategy_id: str | None = None
) -> dict[str, Any]:
    """Read-only full-detail lookup for one strategy's scorecard cards (lazy-load endpoint).

    Returns full cards (including gate ``sub_scores`` and notes) for the requested base/
    strategy id. Never reads arbitrary files or accepts paths — only an id is matched against
    the in-memory full scorecards. ``count`` is 0 with an empty ``cards`` list when not found.
    """
    root = str(canonicalize(mcc_root or default_mcc_root()))
    sid = (strategy_id or "").strip()
    result: dict[str, Any] = {
        "schema_version": "1.0",
        "mode": "read_only",
        "strategy_id": sid,
        "source": "scorecards",
        "generated_at": _utc_now_iso(),
        "count": 0,
        "cards": [],
    }
    if not sid:
        return result

    scorecards = _full_scorecards_cached(root)
    cards = scorecards.get("cards") if isinstance(scorecards, dict) else None
    if not isinstance(cards, list):
        return result

    matched = [
        card
        for card in cards
        if isinstance(card, dict)
        and sid in {card.get("base_strategy_id"), card.get("strategy_id")}
    ]
    result["count"] = len(matched)
    result["cards"] = matched
    return result


def _full_scorecards_cached(root: str) -> dict[str, Any]:
    now = time.monotonic()
    cached = _FULL_SCORECARDS_CACHE.get(root)
    if cached and now - cached[0] <= _FULL_SCORECARDS_TTL_SECONDS:
        return cached[1]
    # Rebuild + repopulate the cache via a normal snapshot build (it stores full scorecards).
    build_dashboard_snapshot(root)
    cached = _FULL_SCORECARDS_CACHE.get(root)
    return cached[1] if cached else {}


def _utc_now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()


def build_dashboard_snapshot(mcc_root: str | Path | None = None) -> dict[str, Any]:
    model = build_read_model(mcc_root)
    files = model["files"]
    task_lifecycle = build_task_lifecycle(files["task_queue"]["data"])
    liveops_status = build_liveops_status(model["mcc_root"])
    parity_status = build_parity_status(model["mcc_root"])
    backtest_status = build_backtest_status(model["mcc_root"])
    optimization_status = build_optimization_status(model["mcc_root"])
    strategy_registry = build_strategy_registry(model["mcc_root"])
    pine_builder_status = build_pine_builder_status(model["mcc_root"])
    candidate_pipeline = build_candidate_pipeline(
        model["mcc_root"], strategy_registry, pine_builder_status,
        liveops_status, parity_status, backtest_status,
    )
    candidate_audit = build_candidate_audit(
        model["mcc_root"],
        candidate_pipeline=candidate_pipeline,
        strategy_registry=strategy_registry,
    )
    scorecards = build_scorecards(model["mcc_root"])
    ai_strategy_names = build_ai_strategy_names(model["mcc_root"])
    scorecards = attach_ai_strategy_names_to_scorecards(scorecards, ai_strategy_names)
    expert_quantlens = build_expert_quantlens(model["mcc_root"])
    scorecards = attach_expert_quantlens_to_scorecards(scorecards, expert_quantlens)
    # Retain full (un-slimmed) scorecards for the lazy-load detail endpoint before the HTTP
    # response is slimmed. Keyed by canonical root to match the snapshot cache.
    _FULL_SCORECARDS_CACHE[str(canonicalize(model["mcc_root"]))] = (time.monotonic(), scorecards)
    if isinstance(candidate_audit.get("rows"), list):
        candidate_audit = dict(candidate_audit)
        candidate_audit["rows"] = attach_ai_strategy_names_to_rows(candidate_audit["rows"], ai_strategy_names)
        candidate_audit["rows"] = attach_expert_quantlens_to_rows(candidate_audit["rows"], expert_quantlens)
        candidate_audit["rows"] = attach_scorecards_to_rows(candidate_audit["rows"], scorecards)
    if isinstance(candidate_pipeline.get("candidates"), list):
        candidate_pipeline = dict(candidate_pipeline)
        candidate_pipeline["candidates"] = attach_ai_strategy_names_to_rows(
            candidate_pipeline["candidates"], ai_strategy_names
        )
        candidate_pipeline["candidates"] = attach_expert_quantlens_to_rows(
            candidate_pipeline["candidates"], expert_quantlens
        )
        candidate_pipeline["candidates"] = attach_scorecards_to_rows(candidate_pipeline["candidates"], scorecards)
    if isinstance(candidate_pipeline.get("rows"), list):
        candidate_pipeline = dict(candidate_pipeline)
        candidate_pipeline["rows"] = attach_ai_strategy_names_to_rows(candidate_pipeline["rows"], ai_strategy_names)
        candidate_pipeline["rows"] = attach_expert_quantlens_to_rows(candidate_pipeline["rows"], expert_quantlens)
        candidate_pipeline["rows"] = attach_scorecards_to_rows(candidate_pipeline["rows"], scorecards)
    mtc_v2_readiness = build_mtc_v2_readiness(
        model["mcc_root"],
        candidate_pipeline=candidate_pipeline,
        candidate_audit=candidate_audit,
    )
    strategy_research = build_strategy_research(model["mcc_root"])
    quantlens = build_quantlens(model["mcc_root"])
    overnight_heartbeat = build_overnight_heartbeat()
    night_artifacts = build_night_artifacts(model["mcc_root"])
    snapshot = {
        "schema_version": "1.0",
        "mode": "read_only",
        "mcc_root": model["mcc_root"],
        "diagnostics": model["summary"],
        "current_status": files["current_status"]["data"],
        "task_queue": files["task_queue"]["data"],
        "task_history": files["task_history"]["data"],
        "liveops_status": liveops_status,
        "parity_status": parity_status,
        "backtest_status": backtest_status,
        "optimization_status": optimization_status,
        "pine_builder_status": pine_builder_status,
        "candidate_pipeline": candidate_pipeline,
        "mtc_v2_readiness": mtc_v2_readiness,
        "report_manifest": files["report_manifest"]["data"],
        "strategy_registry": strategy_registry,
        "strategy_research": strategy_research,
        "quantlens": quantlens,
        "ai_strategy_names": ai_strategy_names,
        "expert_quantlens": expert_quantlens,
        "overnight_heartbeat": overnight_heartbeat,
        "night_artifacts": night_artifacts,
        "scorecards": scorecards,
        "dashboard_config": files["dashboard_config"]["data"],
        "task_lifecycle": task_lifecycle,
        "transcript_reclassification": _load_transcript_reclassification(canonicalize(model["mcc_root"])),
        "file_diagnostics": {
            key: {
                "path": value["path"],
                "required": value["required"],
                "exists": value["exists"],
                "ok": value["ok"],
                "json_ok": value["json_ok"],
                "schema_ok": value["schema_ok"],
                "error": value["error"],
                "schema_issues": value["schema_issues"],
            }
            for key, value in files.items()
        },
    }
    return _slim_http_snapshot(snapshot)


def build_dashboard_snapshot_cached(
    mcc_root: str | Path | None = None,
    *,
    force_refresh: bool = False,
    ttl_seconds: float = _SNAPSHOT_CACHE_TTL_SECONDS,
) -> dict[str, Any]:
    root = str(canonicalize(mcc_root or default_mcc_root()))
    now = time.monotonic()
    cached = _SNAPSHOT_CACHE.get(root)
    if not force_refresh and cached and now - cached[0] <= ttl_seconds:
        payload = dict(cached[1])
        payload["snapshot_cache"] = {
            "status": "HIT",
            "ttl_seconds": ttl_seconds,
            "age_seconds": round(now - cached[0], 3),
        }
        return payload

    snapshot = build_dashboard_snapshot(root)
    _SNAPSHOT_CACHE[root] = (now, snapshot)
    payload = dict(snapshot)
    payload["snapshot_cache"] = {
        "status": "MISS" if not force_refresh else "REFRESH",
        "ttl_seconds": ttl_seconds,
        "age_seconds": 0,
    }
    return payload
