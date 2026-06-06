from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any

from .backtest_reader import build_backtest_status
from .liveops_reader import build_liveops_status
from .parity_reader import build_parity_status
from .paths import canonicalize, default_mcc_root, default_quantlens_root
from .pine_builder_reader import build_pine_builder_status
from .presentation_reader import action_hint, build_scorecard, load_stg_code_map, resolve_stg_code
from .pipeline_reader import build_candidate_pipeline
from .registry_reader import build_strategy_registry


_SOURCE_PATTERNS = (
    "_registry/quantlens_candidate_registry.jsonl",
    "research/**/AUDITED_CANDIDATE_EXTRACTION.jsonl",
    "research/**/FINAL_LLM_KNOWLEDGE_BASE.jsonl",
    "12_LLM_WIKI/**/quantlens_strategy_candidates.jsonl",
    "12_LLM_WIKI/**/quantlens_knowledge_base.jsonl",
)
_SOURCE_MAP_PATTERNS = (
    "12_LLM_WIKI/**/quantlens_source_map.csv",
)

_QUALITY_ORDER = {"REJECTED": 0, "LOW": 1, "MEDIUM": 2, "PARENT": 2, "HIGH": 3}
_STAGE_ORDER = {"discovered": 0, "backtested": 1, "promoted": 2, "pre_parity": 3, "paper_trade": 4, "integrated": 5}


def build_candidate_audit(
    mcc_root: str | Path | None = None,
    candidate_pipeline: dict[str, Any] | None = None,
    strategy_registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    root = canonicalize(mcc_root or default_mcc_root())

    if strategy_registry is None:
        strategy_registry = build_strategy_registry(root)
    if candidate_pipeline is None:
        pine_builder_status = build_pine_builder_status(root)
        liveops_status = build_liveops_status(root)
        parity_status = build_parity_status(root)
        backtest_status = build_backtest_status(root)
        candidate_pipeline = build_candidate_pipeline(
            root,
            strategy_registry,
            pine_builder_status,
            liveops_status,
            parity_status,
            backtest_status,
        )

    source_index = _load_source_index(root)
    stg_map = load_stg_code_map(root)
    pipeline_by_id = {
        str(row.get("id") or ""): row
        for row in (candidate_pipeline.get("rows", []) or [])
        if str(row.get("id") or "").strip()
    }
    base_rows = [_audit_row_base(row, source_index, stg_map) for row in (candidate_pipeline.get("rows", []) or [])]
    rows = _finalize_audit_rows(base_rows)
    for row in rows:
        row["scorecard"] = build_scorecard(pipeline_by_id.get(row["id"], {}), row)
        row["score"] = row["scorecard"]["total"]
        row["score_band"] = row["scorecard"]["band"]
        row["next_action_hint"] = action_hint(row.get("recommended_next_pipeline_step") or row.get("pipeline_next_action"))
    summary = _audit_summary(rows)

    return {
        "schema_version": "1.0",
        "mode": "read_only",
        "mcc_root": str(root),
        "summary": summary,
        "rows": rows,
        "source_record_count": source_index["source_record_count"],
    }


def _load_source_index(root: Path) -> dict[str, Any]:
    by_candidate_id: dict[str, dict[str, Any]] = {}
    by_group_key: dict[str, dict[str, Any]] = {}
    source_record_count = 0
    quantlens_root = default_quantlens_root(root)
    scan_roots: list[Path] = []
    for candidate in (quantlens_root, root):
        if candidate.exists() and candidate not in scan_roots:
            scan_roots.append(candidate)

    for pattern in _SOURCE_PATTERNS:
        for scan_root in scan_roots:
            for path in sorted(scan_root.glob(pattern)):
                for raw in _iter_jsonl(path):
                    source_record_count += 1
                    record = _source_record(raw, path, scan_root)
                    if record is None:
                        continue
                    cid = record.get("candidate_id") or record.get("original_candidate_id") or record.get("audited_candidate_id")
                    if cid:
                        previous = by_candidate_id.get(cid)
                        by_candidate_id[cid] = _merged_source_record(previous, record)
                    group_key = record.get("group_key")
                    if group_key:
                        previous = by_group_key.get(group_key)
                        by_group_key[group_key] = _merged_source_record(previous, record)

    for pattern in _SOURCE_MAP_PATTERNS:
        for scan_root in scan_roots:
            for path in sorted(scan_root.glob(pattern)):
                for raw in _iter_csv(path):
                    source_record_count += 1
                    record = _source_map_record(raw, path, scan_root)
                    if record is None:
                        continue
                    cid = record.get("candidate_id")
                    if cid:
                        previous = by_candidate_id.get(cid)
                        by_candidate_id[cid] = _merged_source_record(previous, record)
                    group_key = record.get("group_key")
                    if group_key:
                        previous = by_group_key.get(group_key)
                        by_group_key[group_key] = _merged_source_record(previous, record)

    return {
        "by_candidate_id": by_candidate_id,
        "by_group_key": by_group_key,
        "source_record_count": source_record_count,
        "source_root": quantlens_root if quantlens_root.exists() else root,
        "quantlens_root": quantlens_root,
    }


def _merged_source_record(previous: dict[str, Any] | None, record: dict[str, Any]) -> dict[str, Any]:
    if previous is None:
        return record
    if record.get("_rank", 0) > previous.get("_rank", 0):
        primary = dict(record)
        secondary = previous
    else:
        primary = dict(previous)
        secondary = record
    for key in ("transcript_path", "source_url", "source_url_source", "source_file"):
        if not primary.get(key) and secondary.get(key):
            primary[key] = secondary[key]
    if not primary.get("rules_text") and secondary.get("rules_text"):
        primary["rules_text"] = secondary["rules_text"]
    if primary.get("source_quality") == "MANUAL_BACKFILL" and secondary.get("source_quality"):
        secondary_quality = str(secondary.get("source_quality") or "").upper()
        if secondary_quality != "REJECTED":
            primary["source_quality"] = secondary["source_quality"]
    for key in ("summary", "recommended_next_action", "verdict", "source_role"):
        if not primary.get(key) and secondary.get(key):
            primary[key] = secondary[key]
    return primary


def _audit_row_base(row: dict[str, Any], source_index: dict[str, Any], stg_map: dict[str, str]) -> dict[str, Any]:
    candidate_id = str(row.get("id") or row.get("candidate_id") or row.get("strategy_id") or "").strip()
    origin_candidate = str(row.get("origin_candidate") or "").strip()
    source_record = _lookup_source_record(row, source_index)
    description = row.get("description") if isinstance(row.get("description"), dict) else {}
    directional = row.get("directional_research") if isinstance(row.get("directional_research"), dict) else {}
    current_stage_key = str(row.get("current_stage_key") or "").strip()
    current_stage_rank = _STAGE_ORDER.get(current_stage_key, -1)

    source_url = _string_value(row.get("source_url") or (source_record.get("source_url") if source_record else ""))
    transcript_path = _string_value(source_record.get("transcript_path") if source_record else "")
    transcript_source_url = _transcript_source_url(transcript_path, source_index)
    source_url_source = _source_url_source(row, source_record, transcript_source_url)
    resolved_source_url = source_url or transcript_source_url
    if resolved_source_url and not source_url:
        source_url = resolved_source_url
    if transcript_source_url and source_url_source == "missing":
        source_url_source = "transcript"
    has_source_url = bool(source_url.strip())
    has_transcript = bool(transcript_path)
    has_source_material = has_source_url or has_transcript

    rule_text = _best_rule_text(row, source_record, directional)
    has_deterministic_rules = _has_deterministic_rules(rule_text, current_stage_key, current_stage_rank)
    split_analysis = _split_candidate_analysis(row, source_record, source_index)
    blocked_reason = _blocked_reason(
        row,
        source_record,
        has_source_material,
        has_deterministic_rules,
        current_stage_key,
        current_stage_rank,
        split_analysis,
    )
    source_role = _source_role(source_record, has_deterministic_rules, blocked_reason)
    source_quality = _source_quality(
        row=row,
        source_record=source_record,
        has_source_material=has_source_material,
        has_deterministic_rules=has_deterministic_rules,
        blocked_reason=blocked_reason,
        current_stage_key=current_stage_key,
        current_stage_rank=current_stage_rank,
    )
    group_key = _group_key(
        row.get("source_url"),
        row.get("name") or row.get("title") or row.get("id"),
        row.get("timeframe"),
        row.get("description"),
    )
    if not group_key:
        group_key = candidate_id
    if not group_key:
        group_key = f"row::{row.get('id') or ''}"

    return {
        "id": candidate_id,
        "name": row.get("name") or row.get("title") or candidate_id,
        "origin_candidate": origin_candidate,
        "symbol": row.get("symbol") or "",
        "timeframe": row.get("timeframe") or "",
        "current_stage_key": current_stage_key,
        "next_stage_key": row.get("next_stage_key"),
        "pipeline_next_action": row.get("next_action") or "",
        "source_url": source_url,
        "source_url_source": source_url_source,
        "transcript_source_url": transcript_source_url,
        "transcript_path": transcript_path,
        "has_source_url": has_source_url,
        "has_transcript": has_transcript,
        "has_source_url_transcript": has_source_material,
        "has_deterministic_rules": has_deterministic_rules,
        "split_candidate_count": split_analysis["count"],
        "split_candidate_evidence": split_analysis["evidence"],
        "split_candidate_explanation": split_analysis["explanation"],
        "eligible_for_backtest": False,
        "blocked_reason": blocked_reason,
        "source_role": source_role,
        "source_quality": source_quality,
        "source_quality_reason": _source_quality_reason(source_record, has_source_material, has_deterministic_rules, blocked_reason),
        "source_quality_explanation": _source_quality_explanation(source_record, source_quality, has_source_material, has_deterministic_rules, blocked_reason, source_url_source),
        "deterministic_rules_explanation": _deterministic_rules_explanation(source_record, has_deterministic_rules, current_stage_key, rule_text),
        "eligibility_explanation": "",
        "audit_status": "CANONICAL",
        "canonical_id": candidate_id,
        "duplicate_of": None,
        "duplicate_group_size": 1,
        "duplicate_group_key": group_key,
        "recommended_next_pipeline_step": "",
        "recommended_next_pipeline_step_explanation": "",
        "pipeline_stage_label": _stage_label(current_stage_key),
        "description_family": description.get("family") or "",
        "description_hint": description.get("what") or "",
        "direction_status": directional.get("status") or "",
        "source_record": _compact_source_record(source_record),
        "quality_rank": _QUALITY_ORDER.get(source_quality, 0),
        "stage_rank": current_stage_rank,
        "stg_code": _stg_code(candidate_id, origin_candidate, row.get("canonical_id"), stg_map=stg_map),
        "stg_number": _stg_number(_stg_code(candidate_id, origin_candidate, row.get("canonical_id"), stg_map=stg_map)),
    }


def _finalize_audit_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_parent_ids = _source_parent_ids(rows)
    groups: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        group_key = row.get("duplicate_group_key") or row.get("id") or ""
        groups.setdefault(group_key, []).append(row)

    finalized: list[dict[str, Any]] = []
    for group_key, group in groups.items():
        canonical = sorted(
            group,
            key=lambda item: (
                int(bool(item.get("blocked_reason"))),
                -int(bool(item.get("has_deterministic_rules"))),
                -int(bool(item.get("eligible_for_backtest"))),
                -int(item.get("stage_rank", -1)),
                -int(item.get("quality_rank", 0)),
                item.get("id", ""),
            ),
        )[0]
        canonical_id = canonical.get("id") or ""
        for row in group:
            duplicate_of = None if row.get("id") == canonical_id else canonical_id
            blocked_reason = row.get("blocked_reason") or ""
            is_source_parent = row.get("id") in source_parent_ids
            if is_source_parent:
                blocked_reason = ""
                duplicate_of = None
                row["blocked_reason"] = ""
                row["source_role"] = "SOURCE_PARENT"
                row["source_quality"] = "PARENT"
                row["source_quality_reason"] = "source parent with extracted child candidates"
                row["source_quality_explanation"] = (
                    "This is a source-parent row. Child candidates from the same video carry the "
                    "testable strategy workflow; the parent is hidden from normal strategy queues."
                )
                row["source_parent_explanation"] = row["source_quality_explanation"]
            eligible_for_backtest = _eligible_for_backtest(
                row=row,
                blocked_reason=blocked_reason,
                duplicate_of=duplicate_of,
                has_source_material=bool(row.get("has_source_url_transcript")),
                has_deterministic_rules=bool(row.get("has_deterministic_rules")),
                current_stage_key=str(row.get("current_stage_key") or ""),
            )
            row["duplicate_of"] = duplicate_of
            row["canonical_id"] = canonical_id
            row["duplicate_group_size"] = len(group)
            row["audit_status"] = (
                "SOURCE_PARENT"
                if is_source_parent
                else "SPLIT_REQUIRED"
                if blocked_reason == "needs indicator split"
                else (
                    "SOURCE_AUDIT"
                    if blocked_reason in {"needs source/formula audit", "salvage only"}
                    else ("BLOCKED" if blocked_reason else ("DUPLICATE" if duplicate_of else "CANONICAL"))
                )
            )
            row["is_source_parent"] = is_source_parent
            row["visible_in_strategy_tables"] = not is_source_parent
            row["eligible_for_backtest"] = False if is_source_parent else eligible_for_backtest
            row["eligibility_explanation"] = _eligibility_explanation(
                blocked_reason,
                duplicate_of,
                bool(row.get("has_source_url_transcript")),
                bool(row.get("has_deterministic_rules")),
                str(row.get("current_stage_key") or ""),
                False if is_source_parent else eligible_for_backtest,
            )
            if is_source_parent:
                row["eligibility_explanation"] = (
                    "Not eligible because this is the source-parent record. Use the extracted child "
                    "candidate rows from the same video for review and backtesting."
                )
            row["duplicate_mapping_explanation"] = _duplicate_mapping_explanation(
                row,
                canonical_id,
                duplicate_of,
                len(group),
            )
            row["recommended_next_pipeline_step"] = _recommended_next_step(
                row=row,
                blocked_reason=blocked_reason,
                duplicate_of=duplicate_of,
                eligible_for_backtest=False if is_source_parent else eligible_for_backtest,
                current_stage_key=str(row.get("current_stage_key") or ""),
            )
            row["recommended_next_pipeline_step_explanation"] = _recommended_next_pipeline_step_explanation(
                row=row,
                blocked_reason=blocked_reason,
                duplicate_of=duplicate_of,
                eligible_for_backtest=False if is_source_parent else eligible_for_backtest,
                current_stage_key=str(row.get("current_stage_key") or ""),
            )
            if is_source_parent:
                row["recommended_next_pipeline_step"] = "Hidden source parent"
                row["recommended_next_pipeline_step_explanation"] = (
                    "Keep this row only as source lineage. Work from the extracted child candidates."
                )
            finalized.append(row)
    return finalized


def _audit_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    source_quality_counts = _count_by(rows, "source_quality")
    step_counts = _count_by(rows, "recommended_next_pipeline_step")
    blocked_reason_counts = _count_by([row for row in rows if row.get("blocked_reason")], "blocked_reason")
    stage_counts = _count_by(rows, "current_stage_key")

    return {
        "total_rows": len(rows),
        "canonical_rows": sum(1 for row in rows if row.get("audit_status") == "CANONICAL"),
        "duplicate_rows": sum(1 for row in rows if row.get("audit_status") == "DUPLICATE"),
        "blocked_rows": sum(1 for row in rows if row.get("audit_status") == "BLOCKED"),
        "split_required_rows": sum(1 for row in rows if row.get("audit_status") == "SPLIT_REQUIRED"),
        "source_audit_rows": sum(1 for row in rows if row.get("audit_status") == "SOURCE_AUDIT"),
        "source_parent_rows": sum(1 for row in rows if row.get("audit_status") == "SOURCE_PARENT"),
        "visible_strategy_rows": sum(1 for row in rows if row.get("visible_in_strategy_tables", True)),
        "eligible_for_backtest_rows": sum(1 for row in rows if row.get("eligible_for_backtest")),
        "deterministic_rule_rows": sum(1 for row in rows if row.get("has_deterministic_rules")),
        "source_material_rows": sum(1 for row in rows if row.get("has_source_url_transcript")),
        "source_quality_counts": source_quality_counts,
        "stage_counts": stage_counts,
        "next_step_counts": step_counts,
        "blocked_reason_counts": blocked_reason_counts,
    }


def _source_parent_ids(rows: list[dict[str, Any]]) -> set[str]:
    by_video: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        video_key = _source_video_key(row.get("source_url"))
        if video_key:
            by_video.setdefault(video_key, []).append(row)

    parent_ids: set[str] = set()
    for item in rows:
        item_id = str(item.get("id") or "")
        if item_id.startswith("QLR_") and int(item.get("split_candidate_count") or 0) >= 2:
            parent_ids.add(item_id)

    for group in by_video.values():
        has_child_candidate = any(not str(item.get("id") or "").startswith("QLR_") for item in group)
        if not has_child_candidate:
            continue
        for item in group:
            item_id = str(item.get("id") or "")
            if item_id.startswith("QLR_"):
                parent_ids.add(item_id)
    return parent_ids


def _load_source_record_map(root: Path) -> dict[str, dict[str, Any]]:
    return _load_source_index(root)


def _lookup_source_record(row: dict[str, Any], source_index: dict[str, Any]) -> dict[str, Any]:
    by_candidate_id = source_index.get("by_candidate_id", {})
    by_group_key = source_index.get("by_group_key", {})
    ids = [
        str(row.get("id") or "").strip(),
        str(row.get("origin_candidate") or "").strip(),
    ]
    for cid in ids:
        if cid and cid in by_candidate_id:
            return by_candidate_id[cid]

    group_key = _group_key(
        row.get("source_url"),
        row.get("name") or row.get("title") or row.get("id"),
        row.get("timeframe"),
        row.get("description"),
    )
    if group_key and group_key in by_group_key:
        return by_group_key[group_key]
    return {}


def _source_url_source(row: dict[str, Any], source_record: dict[str, Any], transcript_source_url: str) -> str:
    if _string_value(row.get("source_url")).strip():
        return "pipeline_row"
    if source_record.get("source_url"):
        if source_record.get("source_url_source"):
            return str(source_record.get("source_url_source"))
        return "source_map" if source_record.get("relative_source_path", "").endswith(".csv") else "source_record"
    if transcript_source_url:
        return "transcript"
    return "missing"


def _eligible_for_backtest(
    row: dict[str, Any],
    blocked_reason: str,
    duplicate_of: str | None,
    has_source_material: bool,
    has_deterministic_rules: bool,
    current_stage_key: str,
) -> bool:
    if duplicate_of:
        return False
    if blocked_reason:
        return False
    if current_stage_key in {"backtested", "promoted", "pre_parity", "paper_trade", "integrated"}:
        return True
    return bool(has_source_material and has_deterministic_rules)


def _blocked_reason(
    row: dict[str, Any],
    source_record: dict[str, Any],
    has_source_material: bool,
    has_deterministic_rules: bool,
    current_stage_key: str,
    current_stage_rank: int,
    split_analysis: dict[str, Any] | None = None,
) -> str:
    hard_block_tokens = (
        "REJECT",
        "REJECTED",
        "DO_NOT_TEST",
        "DATA_BLOCKED",
    )
    split_required_tokens = ("OPEN_FORMULA", "FORMULA IS SELECTED", "INDICATOR PACK", "BUYSELL_INDICATOR_PACK")
    source_audit_tokens = ("SALVAGE_ONLY", "REPAINT AUDIT", "EXACT SOURCE", "SOURCE AND FORMULA AUDIT")
    soft_module_tokens = (
        "WIKI_ONLY",
        "TRADER_WISDOM_ONLY",
        "PROCESS_OR_WORKFLOW_ONLY",
        "MANUAL_VISUAL_REVIEW_ONLY",
        "FILTER_MODULE",
        "ADD_TO_WIKI_ONLY",
        "WISDOM_ONLY",
        "NO_BACKTEST",
    )
    blob = " ".join(
        _string_value(value) for value in (
            row.get("next_action"),
            row.get("notes"),
            row.get("pipeline_next_action"),
            row.get("direction_status"),
            source_record.get("recommended_next_action") if source_record else "",
            source_record.get("summary") if source_record else "",
            source_record.get("verdict") if source_record else "",
            source_record.get("final_classification") if source_record else "",
            source_record.get("audit_verdict") if source_record else "",
            source_record.get("source_quality") if source_record else "",
        )
    ).upper()

    if any(token in blob for token in hard_block_tokens):
        return _first_matching_reason(blob, hard_block_tokens) or "blocked source classification"
    if split_analysis and int(split_analysis.get("count") or 0) >= 2 and current_stage_rank < _STAGE_ORDER["backtested"]:
        return "needs indicator split"
    if any(token in blob for token in split_required_tokens):
        return _first_matching_reason(blob, split_required_tokens) or "needs indicator split"
    if any(token in blob for token in source_audit_tokens):
        return _first_matching_reason(blob, source_audit_tokens) or "needs source/formula audit"
    if any(token in blob for token in soft_module_tokens) and not has_deterministic_rules:
        return _first_matching_reason(blob, soft_module_tokens) or "module-only source"
    if current_stage_rank >= _STAGE_ORDER["backtested"]:
        return ""
    if not has_source_material:
        return "missing source URL or transcript"
    if not has_deterministic_rules:
        return "no deterministic rules extracted"
    return ""


def _source_quality(
    row: dict[str, Any],
    source_record: dict[str, Any],
    has_source_material: bool,
    has_deterministic_rules: bool,
    blocked_reason: str,
    current_stage_key: str,
    current_stage_rank: int,
) -> str:
    quality = str(source_record.get("source_quality") if source_record else "").strip().upper()
    if quality in _QUALITY_ORDER:
        floor = "LOW"
        if current_stage_rank >= _STAGE_ORDER["promoted"]:
            floor = "HIGH"
        elif current_stage_rank >= _STAGE_ORDER["backtested"]:
            floor = "MEDIUM"
        return quality if _QUALITY_ORDER[quality] >= _QUALITY_ORDER[floor] else floor

    blob = " ".join(
        _string_value(value) for value in (
            row.get("next_action"),
            row.get("notes"),
            source_record.get("recommended_next_action") if source_record else "",
            source_record.get("summary") if source_record else "",
            source_record.get("verdict") if source_record else "",
            source_record.get("final_classification") if source_record else "",
            source_record.get("audit_verdict") if source_record else "",
        )
    ).upper()
    if any(token in blob for token in ("REJECT", "WIKI_ONLY", "DO_NOT_TEST", "DATA_BLOCKED", "PROCESS_OR_WORKFLOW_ONLY", "TRADER_WISDOM_ONLY")):
        return "REJECTED"
    if blocked_reason:
        return "LOW"
    if current_stage_rank >= _STAGE_ORDER["promoted"]:
        return "HIGH"
    if current_stage_rank >= _STAGE_ORDER["backtested"]:
        return "MEDIUM"
    if has_source_material and has_deterministic_rules:
        return "HIGH" if str(row.get("current_stage_key") or "") in {"backtested", "promoted", "pre_parity", "paper_trade", "integrated"} else "MEDIUM"
    if has_source_material:
        return "LOW"
    return "LOW"


def _source_quality_reason(
    source_record: dict[str, Any],
    has_source_material: bool,
    has_deterministic_rules: bool,
    blocked_reason: str,
) -> str:
    if blocked_reason:
        return blocked_reason
    parts = []
    if has_source_material:
        parts.append("source material present")
    if has_deterministic_rules:
        parts.append("deterministic rules extracted")
    if source_record and source_record.get("transcript_path"):
        parts.append("transcript linked")
    if source_record and source_record.get("source_url"):
        parts.append("source URL linked")
    return ", ".join(parts) or "insufficient evidence"


def _source_quality_explanation(
    source_record: dict[str, Any],
    source_quality: str,
    has_source_material: bool,
    has_deterministic_rules: bool,
    blocked_reason: str,
    source_url_source: str,
) -> str:
    if blocked_reason:
        return f"Quality is treated as {source_quality} because the record is blocked: {blocked_reason}."
    quality = source_quality
    evidence = []
    if source_url_source == "source_map":
        evidence.append("source URL recovered from quantlens_source_map.csv")
    elif source_url_source == "transcript":
        evidence.append("source URL recovered from transcript markdown")
    elif source_url_source == "record":
        evidence.append("source URL present in the classification record")
    if source_record and source_record.get("transcript_path"):
        evidence.append("transcript path available")
    if has_deterministic_rules:
        evidence.append("mechanically testable rules were extracted")
    if not evidence:
        evidence.append("evidence is thin or incomplete")
    return f"Quality is {quality}: " + "; ".join(evidence) + "."


def _deterministic_rules_explanation(
    source_record: dict[str, Any],
    has_deterministic_rules: bool,
    current_stage_key: str,
    rule_text: str,
) -> str:
    if has_deterministic_rules:
        return f"Deterministic rules were detected from the rule text because it contains machine-testable signals such as comparisons or indicator terms; current stage is {current_stage_key or 'unknown'}."
    if source_record and source_record.get("recommended_next_action"):
        return f"No deterministic rule was isolated from the source material. The source mostly contains guidance or classification text (`{source_record.get('recommended_next_action')}`) instead of an executable entry/exit rule."
    if rule_text.strip():
        return "A rule-like phrase exists, but it does not describe a fully mechanical entry/exit condition that we can test without interpretation."
    return "No deterministic rules were extracted from the available source material."


def _eligibility_explanation(
    blocked_reason: str,
    duplicate_of: str | None,
    has_source_material: bool,
    has_deterministic_rules: bool,
    current_stage_key: str,
    eligible_for_backtest: bool,
) -> str:
    if duplicate_of:
        return f"Not eligible because this row is a duplicate of canonical record {duplicate_of}."
    if blocked_reason == "needs indicator split":
        return "Not eligible for a single backtest yet because this is an indicator pack; split each open formula into its own candidate first."
    if blocked_reason in {"needs source/formula audit", "salvage only"}:
        return "Not eligible until the exact source, formula, repaint/lookahead behavior, and entry/exit rules are audited."
    if blocked_reason:
        return f"Not eligible because the source is blocked: {blocked_reason}."
    if eligible_for_backtest:
        return f"Eligible because source material exists, deterministic rules were extracted, and current stage is {current_stage_key or 'discovered'}."
    missing = []
    if not has_source_material:
        missing.append("source material")
    if not has_deterministic_rules:
        missing.append("deterministic rules")
    if missing:
        return "Not eligible because " + " and ".join(missing) + " are still missing."
    return "Not eligible pending pipeline review."


def _duplicate_mapping_explanation(
    row: dict[str, Any],
    canonical_id: str,
    duplicate_of: str | None,
    duplicate_group_size: int,
) -> str:
    if duplicate_group_size <= 1:
        return "This record currently has no duplicate siblings in the audit group, so it is the canonical row for itself."
    if duplicate_of:
        return f"This row shares the same source group with {duplicate_group_size - 1} other row(s) and is mapped as a duplicate of canonical record {canonical_id}."
    return f"This row is the canonical representative for a duplicate group of {duplicate_group_size} row(s)."


def _recommended_next_pipeline_step_explanation(
    row: dict[str, Any],
    blocked_reason: str,
    duplicate_of: str | None,
    eligible_for_backtest: bool,
    current_stage_key: str,
) -> str:
    if duplicate_of:
        return "Merge or compare this row against the canonical record first; do not run a separate backtest until the duplication is resolved."
    if blocked_reason == "needs indicator split":
        return "Split the pack into separate indicator/formula candidates, then audit and backtest each case independently."
    if blocked_reason in {"needs source/formula audit", "salvage only"}:
        return "Keep this as a salvage/source-audit item until the exact formula and source evidence are resolved."
    if blocked_reason:
        return f"Parked because the source is blocked. Resolve the source issue before any next-stage work: {blocked_reason}."
    if current_stage_key == "discovered":
        if eligible_for_backtest:
            return "The row has enough source quality and rule clarity to move into backtest next."
        return "The row is discovered but not yet ready for backtest; extract or rewrite the rule set first."
    if current_stage_key == "backtested":
        return "Backtest evidence exists; the next step is to build the promotion packet."
    if current_stage_key == "promoted":
        return "Promotion is complete; the next verification step is PineTS parity."
    if current_stage_key == "pre_parity":
        return "Parity is the gate; next step is forward paper-trade collection."
    if current_stage_key == "paper_trade":
        return "Forward paper-trade has started; next step is collecting enough forward result data."
    if current_stage_key == "integrated":
        return "The strategy is integrated; next step is monitoring and ongoing operations."
    return row.get("next_action") or "Review"


def _recommended_next_step(
    row: dict[str, Any],
    blocked_reason: str,
    duplicate_of: str | None,
    eligible_for_backtest: bool,
    current_stage_key: str,
) -> str:
    if duplicate_of:
        return "Merge into canonical record"
    if blocked_reason == "needs indicator split":
        return "Split into indicator cases"
    if blocked_reason in {"needs source/formula audit", "salvage only"}:
        return "Resolve source/formula audit"
    if blocked_reason:
        return "Source audit / park"
    if current_stage_key == "discovered":
        return "Run backtest" if eligible_for_backtest else "Extract deterministic rules"
    if current_stage_key == "backtested":
        return "Build promotion packet"
    if current_stage_key == "promoted":
        return "Run PineTS parity"
    if current_stage_key == "pre_parity":
        return "Start forward paper-trade"
    if current_stage_key == "paper_trade":
        return "Collect forward paper-trade results"
    if current_stage_key == "integrated":
        return "Monitor integrated strategy"
    return row.get("next_action") or "Review"


def _best_rule_text(row: dict[str, Any], source_record: dict[str, Any], directional: dict[str, Any]) -> str:
    pieces: list[str] = []
    if directional.get("long_signal_definition"):
        pieces.append(_string_value(directional.get("long_signal_definition")))
    if directional.get("short_signal_definition"):
        pieces.append(_string_value(directional.get("short_signal_definition")))
    for key in ("exact_rules_if_available", "exact_rules", "rules_text", "rules"):
        if source_record and source_record.get(key):
            pieces.append(_string_value(source_record.get(key)))
    for key in ("notes", "description_hint", "pipeline_next_action"):
        if row.get(key):
            pieces.append(_string_value(row.get(key)))
    return " | ".join(piece for piece in pieces if piece)


def _has_deterministic_rules(rule_text: str, current_stage_key: str, current_stage_rank: int) -> bool:
    if current_stage_rank >= _STAGE_ORDER["backtested"]:
        return True
    text = rule_text.strip()
    if not text:
        return False
    upper = text.upper()
    if any(token in upper for token in ("WIKI_ONLY", "TRADER_WISDOM_ONLY", "PROCESS_OR_WORKFLOW_ONLY", "REJECT", "UNKNOWN")):
        return False
    if any(symbol in text for symbol in ("<", ">", "=", "AND", "OR", "EMA", "RSI", "VWAP", "SMA", "ATR", "BREAK", "CROSS")):
        return True
    return len(text.split()) >= 6


def _split_candidate_analysis(
    row: dict[str, Any],
    source_record: dict[str, Any],
    source_index: dict[str, Any],
) -> dict[str, Any]:
    text = _source_material_text(source_record, source_index)
    snippets = [
        _string_value(row.get("name")),
        _string_value(row.get("notes")),
        _string_value(row.get("pipeline_next_action")),
        _string_value(row.get("description_hint")),
        _string_value(source_record.get("title") if source_record else ""),
        _string_value(source_record.get("summary") if source_record else ""),
        _string_value(source_record.get("recommended_next_action") if source_record else ""),
        text,
    ]
    blob = "\n".join(piece for piece in snippets if piece).lower()
    if not blob.strip():
        return {"count": 1, "evidence": [], "explanation": ""}

    evidence: list[str] = []
    count = 1
    numeric_patterns = [
        (r"\b(?:five|5)\s+(?:tradingview\s+)?(?:buy/sell\s+)?(?:signal\s+)?indicators?\b", 5),
        (r"\b(?:five|5)\s+(?:setups?|strategies|cases|models)\b", 5),
        (r"\b(?:seven|7)\s+(?:patterns?|setups?|strategies|cases|models)\b", 7),
        (r"\b(?:three|3|uc|üç)\s+(?:different\s+)?(?:setups?|strategies|cases|models|rejim|regimes)\b", 3),
        (r"\b(?:two|2|iki)\s+(?:different\s+)?(?:setups?|strategies|cases|models|entry\s+zones?)\b", 2),
        (r"\b(?:multiple|several|birden fazla)\s+(?:setups?|strategies|indicators?|cases|models)\b", 2),
    ]
    for pattern, value in numeric_patterns:
        match = re.search(pattern, blob, flags=re.IGNORECASE)
        if match:
            count = max(count, value)
            evidence.append(match.group(0)[:140])

    line_hits: list[str] = []
    for line in blob.splitlines():
        stripped = line.strip(" -*\t")
        if not stripped:
            continue
        if re.search(r"\b(long|short|bullish|bearish|breakout|reversal|pullback|squeeze|trend)\s+(setup|entry|case|variant|zone)\b", stripped):
            line_hits.append(stripped[:140])
        elif re.search(r"\b(setup|indicator|strategy|model|case|variant)\s*(?:#?\d+|[a-e]\b|:)", stripped):
            line_hits.append(stripped[:140])
        if len(line_hits) >= 6:
            break
    if len(line_hits) >= 2:
        count = max(count, len(line_hits))
        evidence.extend(line_hits[:4])

    if count < 2:
        return {"count": 1, "evidence": [], "explanation": ""}
    unique_evidence = []
    seen = set()
    for item in evidence:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            unique_evidence.append(item)
    explanation = (
        f"Source material appears to contain {count} candidate setup/indicator case(s). "
        "Treat the video/intake as a parent source and split each formula or setup into a separate candidate before backtest."
    )
    return {"count": count, "evidence": unique_evidence[:6], "explanation": explanation}


def _source_material_text(source_record: dict[str, Any], source_index: dict[str, Any]) -> str:
    if not source_record:
        return ""
    roots: list[Path] = []
    for key in ("source_root", "quantlens_root"):
        value = source_index.get(key)
        if value:
            roots.append(Path(str(value)))
    rels = [
        _string_value(source_record.get("source_file")),
        _string_value(source_record.get("transcript_path")),
    ]
    texts: list[str] = []
    seen: set[str] = set()
    for rel in rels:
        if not rel:
            continue
        rel_path = Path(rel)
        for root in roots:
            candidates = [
                root / rel_path,
                root / "00_INBOX_REPORTS" / rel_path,
                root / "research" / rel_path,
            ]
            for path in candidates:
                key = str(path)
                if key in seen or not path.exists() or not path.is_file():
                    continue
                seen.add(key)
                try:
                    texts.append(path.read_text(encoding="utf-8", errors="replace")[:80000])
                except Exception:
                    continue
    return "\n".join(texts)


def _compact_source_record(source_record: dict[str, Any]) -> dict[str, Any] | None:
    if not source_record:
        return None
    return {
        "candidate_id": source_record.get("candidate_id"),
        "title": source_record.get("title"),
        "source_url": source_record.get("source_url"),
        "source_url_source": source_record.get("source_url_source"),
        "transcript_path": source_record.get("transcript_path"),
        "source_file": source_record.get("source_file"),
        "source_role": source_record.get("source_role"),
        "split_candidate_count": source_record.get("split_candidate_count"),
        "split_candidate_evidence": source_record.get("split_candidate_evidence"),
        "recommended_next_action": source_record.get("recommended_next_action"),
        "source_quality": source_record.get("source_quality"),
        "summary": source_record.get("summary"),
        "rules_text": source_record.get("rules_text"),
        "verdict": source_record.get("verdict"),
        "relative_source_path": source_record.get("relative_source_path"),
    }


def _source_record(raw: dict[str, Any], path: Path, root: Path) -> dict[str, Any] | None:
    candidate_id = _first_non_empty(
        raw.get("candidate_id"),
        raw.get("strategy_id"),
        raw.get("audited_candidate_id"),
        raw.get("original_candidate_id"),
    )
    if not candidate_id:
        return None
    title = _string_value(raw.get("title") or raw.get("strategy_name") or candidate_id)
    raw_source_url = _normalize_url(raw.get("source_url"))
    source_url = raw_source_url
    transcript_path = _string_value(raw.get("transcript_path") or raw.get("transcript"))
    source_file = _string_value(raw.get("source_file") or raw.get("intake_path") or raw.get("corrected_intake_path"))
    if not source_url and source_file:
        source_url = _source_url_from_source_file(source_file, root)
    summary = _string_value(raw.get("summary"))
    recommended = _string_value(raw.get("recommended_next_action") or raw.get("next_action"))
    exact_rules = _string_value(
        raw.get("exact_rules_if_available")
        or raw.get("exact_rules")
        or raw.get("rules")
        or raw.get("rule_text")
    )
    verdict = _string_value(
        raw.get("verdict")
        or raw.get("audit_verdict")
        or raw.get("final_classification")
        or raw.get("status")
    )
    quality = _string_value(raw.get("source_quality"))
    if not quality:
        quality = _infer_quality_label(summary, recommended, verdict, exact_rules, source_url, transcript_path)
    source_role = _source_role(
        {
            "recommended_next_action": recommended,
            "summary": summary,
            "verdict": verdict,
            "final_classification": raw.get("final_classification"),
            "audit_verdict": raw.get("audit_verdict"),
            "source_quality": quality,
            "rules_text": exact_rules,
        },
        bool(exact_rules or source_url or transcript_path),
        "",
    )
    group_key = _group_key(source_url, title, raw.get("timeframe"), raw.get("source_file"))
    return {
        "_rank": _record_rank_from_path(path),
        "candidate_id": str(candidate_id),
        "title": title,
        "source_url": source_url,
        "source_url_source": "source_file" if source_url and not raw_source_url else "source_record",
        "transcript_path": transcript_path,
        "source_file": source_file,
        "summary": summary,
        "recommended_next_action": recommended,
        "rules_text": exact_rules,
        "verdict": verdict,
        "source_quality": quality.upper(),
        "source_role": source_role,
        "relative_source_path": _relative_to_root(path, root),
        "group_key": group_key,
        "raw": raw,
    }


def _source_map_record(raw: dict[str, Any], path: Path, root: Path) -> dict[str, Any] | None:
    candidate_id = _string_value(raw.get("candidate_id")).strip()
    if not candidate_id:
        return None
    title = _string_value(raw.get("source_title") or raw.get("title") or candidate_id)
    transcript_path = _string_value(raw.get("transcript_path"))
    source_url = _normalize_url(raw.get("source_url"))
    source_url_source = "source_map" if source_url else "missing"
    if not source_url and transcript_path:
        source_url = _transcript_source_url(transcript_path, {"quantlens_root": root, "source_root": root})
        if source_url:
            source_url_source = "transcript"
    group_key = _group_key(source_url, title, None, transcript_path or raw.get("intake_path"))
    source_quality = _string_value(raw.get("source_quality")).strip().upper() or _infer_quality_label(
        title,
        _string_value(raw.get("next_action")),
        _string_value(raw.get("classification")),
        "",
        source_url,
        transcript_path,
    )
    source_role = _source_role(
        {
            "recommended_next_action": _string_value(raw.get("next_action")),
            "summary": _string_value(raw.get("classification")),
            "verdict": _string_value(raw.get("classification")),
            "audit_verdict": _string_value(raw.get("classification")),
            "source_quality": source_quality,
        },
        bool(source_url or transcript_path),
        "",
    )
    return {
        "_rank": 60,
        "candidate_id": candidate_id,
        "title": title,
        "source_url": source_url,
        "source_url_source": source_url_source,
        "transcript_path": transcript_path,
        "summary": _string_value(raw.get("classification") or raw.get("do_not_test_yet_reason")),
        "recommended_next_action": _string_value(raw.get("next_action")),
        "rules_text": "",
        "verdict": _string_value(raw.get("classification")),
        "source_quality": source_quality,
        "source_role": source_role,
        "source_file": _string_value(raw.get("intake_path") or raw.get("corrected_intake_path")),
        "relative_source_path": _relative_to_root(path, root),
        "group_key": group_key,
        "raw": raw,
    }


def _infer_quality_label(
    summary: str,
    recommended: str,
    verdict: str,
    exact_rules: str,
    source_url: str,
    transcript_path: str,
) -> str:
    blob = " ".join([summary, recommended, verdict, exact_rules]).upper()
    if any(token in blob for token in ("REJECT", "WIKI_ONLY", "DO_NOT_TEST", "DATA_BLOCKED", "PROCESS_OR_WORKFLOW_ONLY", "TRADER_WISDOM_ONLY")):
        return "REJECTED"
    if exact_rules and (source_url or transcript_path):
        return "HIGH"
    if source_url and (summary or recommended or verdict):
        return "MEDIUM"
    if source_url or transcript_path:
        return "LOW"
    return "LOW"


def _transcript_source_url(transcript_path: str, source_index: dict[str, Any]) -> str:
    if not transcript_path:
        return ""
    roots: list[Path] = []
    for key in ("quantlens_root", "source_root"):
        value = source_index.get(key)
        if value:
            roots.append(Path(str(value)))
    seen: set[str] = set()
    for root in roots:
        path = root / transcript_path
        key = str(path)
        if key in seen:
            continue
        seen.add(key)
        if not path.exists():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for pattern in (
            r"https?://(?:www\.)?youtube\.com/watch\?v=[A-Za-z0-9_-]+(?:[^\s<>\"]*)?",
            r"https?://(?:www\.)?youtu\.be/[A-Za-z0-9_-]+(?:[^\s<>\"]*)?",
        ):
            match = re.search(pattern, text)
            if match:
                return _normalize_url(match.group(0))
    return ""


def _source_url_from_source_file(source_file: str, root: Path) -> str:
    if not source_file:
        return ""
    rel = Path(source_file)
    quantlens_root = default_quantlens_root(root)
    search_roots = [
        root,
        quantlens_root,
        quantlens_root / "00_INBOX_REPORTS",
        quantlens_root / "research",
    ]
    candidates: list[Path] = []
    for base in search_roots:
        direct = base / rel
        if direct.exists():
            candidates.append(direct)
    if not candidates:
        for base in search_roots:
            if base.exists():
                candidates.extend(sorted(base.rglob(rel.name)))
            if candidates:
                break
    for candidate in candidates:
        url = _first_youtube_url(candidate)
        if url:
            return _normalize_url(url)
    return ""


def _first_youtube_url(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""
    for pattern in (
        r"https?://(?:www\.)?youtube\.com/watch\?v=[A-Za-z0-9_-]+(?:[^\s<>\"]*)?",
        r"https?://(?:www\.)?youtu\.be/[A-Za-z0-9_-]+(?:[^\s<>\"]*)?",
    ):
        match = re.search(pattern, text)
        if match:
            return match.group(0).rstrip(").,")
    return ""


def _iter_csv(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                if isinstance(row, dict):
                    rows.append(row)
    except Exception:
        return rows
    return rows


def _record_rank_from_path(path: Path) -> int:
    text = str(path).upper()
    if "AUDITED_CANDIDATE_EXTRACTION" in text:
        return 50
    if "FINAL_LLM_KNOWLEDGE_BASE" in text:
        return 40
    if "QUANTLENS_STRATEGY_CANDIDATES" in text:
        return 30
    if "QUANTLENS_KNOWLEDGE_BASE" in text:
        return 25
    if "QUANTLENS_CANDIDATE_REGISTRY" in text:
        return 20
    return 10


def _iter_jsonl(path: Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return items
    for line in lines:
        if not line.strip():
            continue
        try:
            raw = json.loads(line)
        except Exception:
            continue
        if isinstance(raw, dict):
            items.append(raw)
    return items


def _count_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = row.get(key)
        label = _string_value(value).strip() or "UNKNOWN"
        counts[label] = counts.get(label, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))


def _group_key(
    source_url: Any,
    title: Any,
    timeframe: Any = None,
    fallback: Any = None,
) -> str:
    parts = []
    raw_url = _string_value(source_url).strip()
    url = _normalize_url(source_url) or raw_url
    if url:
        parts.append(url.lower())
    norm_title = _normalize_text(title)
    if norm_title:
        parts.append(norm_title)
    norm_timeframe = _normalize_text(timeframe)
    if norm_timeframe:
        parts.append(norm_timeframe)
    norm_fallback = _normalize_text(fallback)
    if not parts and norm_fallback:
        parts.append(norm_fallback)
    return "::".join(parts)


def _normalize_text(value: Any) -> str:
    text = _string_value(value).lower().strip()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _normalize_url(value: Any) -> str:
    text = _string_value(value).strip().lstrip("*").strip()
    match = re.search(r"https?://(?:www\.)?(?:youtube\.com/watch\?v=[^\s]+|youtu\.be/[^\s]+)", text)
    if match:
        text = match.group(0).rstrip(").,")
    if "youtube.com/watch" in text or "youtu.be/" in text:
        return text
    return ""


def _source_video_key(value: Any) -> str:
    url = _normalize_url(value) or _string_value(value)
    match = re.search(r"(?:[?&]v=|youtu\.be/)([A-Za-z0-9_-]+)", url)
    if match:
        return match.group(1)
    return url.strip().lower()


def _string_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (str, int, float)):
        return str(value)
    if isinstance(value, list):
        return ", ".join(str(item) for item in value if item not in (None, ""))
    if isinstance(value, dict):
        try:
            return json.dumps(value, ensure_ascii=False, sort_keys=True)
        except Exception:
            return str(value)
    return str(value)


def _first_non_empty(*values: Any) -> Any:
    for value in values:
        if value not in (None, "", [], {}):
            return value
    return ""


def _first_matching_reason(blob: str, tokens: tuple[str, ...]) -> str:
    mapping = {
        "REJECT": "rejected source classification",
        "REJECTED": "rejected source classification",
        "WIKI_ONLY": "wiki-only source",
        "DO_NOT_TEST": "do not test",
        "NO_BACKTEST": "do not test",
        "PROCESS_OR_WORKFLOW_ONLY": "workflow-only source",
        "TRADER_WISDOM_ONLY": "wisdom-only source",
        "DATA_BLOCKED": "data blocked",
        "MANUAL_VISUAL_REVIEW_ONLY": "manual visual review only",
        "SALVAGE_ONLY": "salvage only",
        "OPEN_FORMULA": "needs indicator split",
        "FORMULA IS SELECTED": "needs indicator split",
        "INDICATOR PACK": "needs indicator split",
        "BUYSELL_INDICATOR_PACK": "needs indicator split",
        "REPAINT AUDIT": "needs source/formula audit",
        "EXACT SOURCE": "needs source/formula audit",
        "SOURCE AND FORMULA AUDIT": "needs source/formula audit",
    }
    for token in tokens:
        if token in blob:
            return mapping.get(token, token.lower().replace("_", " "))
    return ""


def _source_role(source_record: dict[str, Any], has_deterministic_rules: bool, blocked_reason: str) -> str:
    blob = " ".join(
        _string_value(value) for value in (
            source_record.get("recommended_next_action") if source_record else "",
            source_record.get("summary") if source_record else "",
            source_record.get("verdict") if source_record else "",
            source_record.get("final_classification") if source_record else "",
            source_record.get("audit_verdict") if source_record else "",
            source_record.get("source_quality") if source_record else "",
            source_record.get("rules_text") if source_record else "",
        )
    ).upper()
    if blocked_reason == "needs indicator split":
        return "SPLIT_REQUIRED"
    if blocked_reason in {"needs source/formula audit", "salvage only"}:
        return "SOURCE_AUDIT"
    if blocked_reason and blocked_reason in {"rejected source classification", "data blocked", "do not test"}:
        return "REJECTED"
    if has_deterministic_rules and any(token in blob for token in ("WIKI_ONLY", "TRADER_WISDOM_ONLY", "PROCESS_OR_WORKFLOW_ONLY", "MANUAL_VISUAL_REVIEW_ONLY", "FILTER_MODULE", "ADD_TO_WIKI_ONLY", "WISDOM_ONLY")):
        return "HYBRID_CANDIDATE"
    if any(token in blob for token in ("WIKI_ONLY", "TRADER_WISDOM_ONLY", "PROCESS_OR_WORKFLOW_ONLY", "MANUAL_VISUAL_REVIEW_ONLY", "FILTER_MODULE", "ADD_TO_WIKI_ONLY", "WISDOM_ONLY")):
        return "WIKI_MODULE"
    if has_deterministic_rules:
        return "CANDIDATE"
    return "UNCLASSIFIED"


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _stage_label(key: str) -> str:
    mapping = {
        "classified": "Classified",
        "discovered": "Discovered",
        "backtested": "Backtested",
        "promoted": "Promoted",
        "pre_parity": "Pre-Parity",
        "paper_trade": "Paper-Trade",
        "integrated": "Integrated",
    }
    return mapping.get(key, key or "Unknown")


def _stg_code(*args: Any, stg_map: dict[str, str] | None = None) -> str:
    mapping = stg_map or {}
    for candidate in args:
        key = str(candidate or "").strip()
        if key and key in mapping:
            return mapping[key]
    return ""


def _stg_number(stg_code: str) -> int | None:
    if not stg_code:
        return None
    digits = "".join(ch for ch in str(stg_code) if ch.isdigit())
    if not digits:
        return None
    try:
        return int(digits)
    except Exception:
        return None
