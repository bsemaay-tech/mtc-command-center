from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .paths import canonicalize, default_mcc_root, load_path_config, resolve_configured_path


MAX_DRAFTS = 80


def build_pine_builder_status(mcc_root: str | Path | None = None) -> dict[str, Any]:
    root = canonicalize(mcc_root or default_mcc_root())
    path_config = load_path_config(root)
    mtc_v2_root = resolve_configured_path(path_config.config, "mtc_v2_root")
    if mtc_v2_root is None:
        return _empty_status("mtc_v2_root_not_configured")
    if not mtc_v2_root.exists():
        return _empty_status(str(mtc_v2_root))

    observations = _compile_observations(mtc_v2_root)
    pine_files = sorted(mtc_v2_root.rglob("*.pine"))
    protected_core_files = [path for path in pine_files if _is_protected_core(path, mtc_v2_root)]
    draft_paths = [path for path in pine_files if _is_review_draft(path, mtc_v2_root)]
    supporting_files = [
        path for path in pine_files if path not in protected_core_files and path not in draft_paths
    ]

    drafts = [_draft_record(path, mtc_v2_root, observations) for path in draft_paths]
    drafts.sort(key=lambda item: item.get("_sort_mtime", 0.0), reverse=True)
    drafts = drafts[:MAX_DRAFTS]
    for draft in drafts:
        draft.pop("_sort_mtime", None)

    return {
        "schema_version": "1.0",
        "generated_at": _latest_timestamp(drafts, observations),
        "source": str(mtc_v2_root),
        "summary": _summary(drafts, pine_files, protected_core_files, supporting_files),
        "drafts": drafts,
    }


def _compile_observations(mtc_v2_root: Path) -> dict[str, dict[str, Any]]:
    promoted_root = mtc_v2_root / "06_QUANTLENS_LAB" / "06_PROMOTED_TO_PARITY"
    if not promoted_root.exists():
        return {}

    observations: dict[str, dict[str, Any]] = {}
    for plan_path in sorted(promoted_root.glob("*/PINE_PARITY_PLAN.md")):
        candidate_id = plan_path.parent.name
        text = _read_text(plan_path)
        compile_status = _compile_status(text)
        chart_status = _chart_status(text)
        observations[candidate_id] = {
            "candidate_id": candidate_id,
            "compile_status": compile_status,
            "chart_status": chart_status,
            "compile_observation_path": _relative_to_mtc(plan_path, mtc_v2_root),
            "updated_at": _timestamp(plan_path.stat().st_mtime),
        }
    return observations


def _draft_record(path: Path, mtc_v2_root: Path, observations: dict[str, dict[str, Any]]) -> dict[str, Any]:
    stat = path.stat()
    rel_path = _relative_to_mtc(path, mtc_v2_root)
    candidate_id = _candidate_id(path, mtc_v2_root)
    observation = observations.get(candidate_id or "", {})
    compile_status = observation.get("compile_status") or "UNKNOWN"
    chart_status = observation.get("chart_status") or "NOT_OBSERVED"
    source_type = _source_type(path, mtc_v2_root)

    return {
        "_sort_mtime": stat.st_mtime,
        "draft_id": _draft_id(path, mtc_v2_root, candidate_id),
        "candidate_id": candidate_id,
        "name": path.stem,
        "status": _draft_status(compile_status, chart_status),
        "compile_status": compile_status,
        "chart_status": chart_status,
        "promotion_gate": _promotion_gate(compile_status, chart_status, source_type),
        "source_type": source_type,
        "protected_core": False,
        "source_path": str(path),
        "relative_path": rel_path,
        "compile_observation_path": observation.get("compile_observation_path"),
        "updated_at": _timestamp(stat.st_mtime),
        "size_bytes": stat.st_size,
    }


def _compile_status(text: str) -> str:
    if _matches(text, r"server compile[^\n]{0,120}\bpass\b"):
        return "PASS"
    if _matches(text, r"compile_parity[`*:\s]*[^\n]{0,80}\bpass\b"):
        return "PASS"
    if _matches(text, r"compile[^\n]{0,120}\b(fail|failed)\b"):
        return "FAIL"
    return "UNKNOWN"


def _chart_status(text: str) -> str:
    if _matches(text, r"live chart run[^\n]{0,120}\bpass\b"):
        return "PASS"
    if _matches(text, r"compiled \+ added to chart"):
        return "PASS"
    if _matches(text, r"chart[^\n]{0,120}\bpending\b"):
        return "PENDING"
    if _matches(text, r"not yet loaded|not yet performed"):
        return "PENDING"
    return "NOT_OBSERVED"


def _draft_status(compile_status: str, chart_status: str) -> str:
    if compile_status == "FAIL":
        return "COMPILE_FAIL"
    if compile_status == "PASS" and chart_status == "PASS":
        return "CHART_RUN_PASS"
    if compile_status == "PASS":
        return "COMPILE_PASS_CHART_PENDING"
    return "WAITING_FOR_TRADINGVIEW_COMPILE"


def _promotion_gate(compile_status: str, chart_status: str, source_type: str) -> str:
    if source_type == "sandbox_review":
        return "SANDBOX_REVIEW_ONLY"
    if compile_status == "FAIL":
        return "NEEDS_PINE_DEBUG"
    if compile_status == "PASS" and chart_status == "PASS":
        return "PARITY_REVIEW_LIMITED_NOT_PRODUCTION_READY"
    if compile_status == "PASS":
        return "NEEDS_CHART_PARITY"
    return "NEEDS_COMPILE_OBSERVATION"


def _summary(
    drafts: list[dict[str, Any]],
    pine_files: list[Path],
    protected_core_files: list[Path],
    supporting_files: list[Path],
) -> dict[str, Any]:
    return {
        "total_pine_files": len(pine_files),
        "total_drafts": len(drafts),
        "compile_pass": sum(1 for draft in drafts if draft.get("compile_status") == "PASS"),
        "compile_fail": sum(1 for draft in drafts if draft.get("compile_status") == "FAIL"),
        "waiting_for_tradingview_compile": sum(
            1 for draft in drafts if draft.get("compile_status") == "UNKNOWN"
        ),
        "chart_run_pass": sum(1 for draft in drafts if draft.get("chart_status") == "PASS"),
        "chart_run_pending": sum(1 for draft in drafts if draft.get("chart_status") == "PENDING"),
        "protected_core_files": len(protected_core_files),
        "supporting_pine_artifacts": len(supporting_files),
        "production_pine_protected": True,
    }


def _is_review_draft(path: Path, mtc_v2_root: Path) -> bool:
    if _is_protected_core(path, mtc_v2_root):
        return False
    rel_parts = _relative_parts(path, mtc_v2_root)
    if any(part in {"parity_oracles", "reports", "templates", "examples"} for part in rel_parts):
        return False
    return "review" in path.stem.lower() or "06_PROMOTED_TO_PARITY" in rel_parts


def _is_protected_core(path: Path, mtc_v2_root: Path) -> bool:
    parts = _relative_parts(path, mtc_v2_root)
    return path.name == "MTC_V2.pine" and "01_PINE" in parts


def _source_type(path: Path, mtc_v2_root: Path) -> str:
    parts = _relative_parts(path, mtc_v2_root)
    if "06_PROMOTED_TO_PARITY" in parts:
        return "promoted_to_parity_review"
    if "strategy_sandboxes" in parts:
        return "sandbox_review"
    return "review_draft"


def _candidate_id(path: Path, mtc_v2_root: Path) -> str | None:
    parts = _relative_parts(path, mtc_v2_root)
    for marker in ("06_PROMOTED_TO_PARITY", "strategy_sandboxes"):
        if marker in parts:
            index = parts.index(marker)
            if len(parts) > index + 1:
                return parts[index + 1]
    return path.parent.name


def _draft_id(path: Path, mtc_v2_root: Path, candidate_id: str | None) -> str:
    if candidate_id:
        return f"{candidate_id}:{path.stem}"
    return _relative_to_mtc(path, mtc_v2_root)


def _relative_parts(path: Path, mtc_v2_root: Path) -> list[str]:
    try:
        return list(path.relative_to(mtc_v2_root).parts)
    except ValueError:
        return list(path.parts)


def _relative_to_mtc(path: Path, mtc_v2_root: Path) -> str:
    try:
        return str(path.relative_to(mtc_v2_root))
    except ValueError:
        return str(path)


def _matches(text: str, pattern: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _latest_timestamp(drafts: list[dict[str, Any]], observations: dict[str, dict[str, Any]]) -> str | None:
    timestamps = [draft.get("updated_at") for draft in drafts if draft.get("updated_at")]
    timestamps.extend(
        observation.get("updated_at")
        for observation in observations.values()
        if observation.get("updated_at")
    )
    return max(timestamps) if timestamps else None


def _timestamp(epoch_seconds: float) -> str:
    return datetime.fromtimestamp(epoch_seconds, timezone.utc).isoformat()


def _empty_status(source: str) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "generated_at": None,
        "source": source,
        "summary": {
            "total_pine_files": 0,
            "total_drafts": 0,
            "compile_pass": 0,
            "compile_fail": 0,
            "waiting_for_tradingview_compile": 0,
            "chart_run_pass": 0,
            "chart_run_pending": 0,
            "protected_core_files": 0,
            "supporting_pine_artifacts": 0,
            "production_pine_protected": True,
        },
        "drafts": [],
    }
