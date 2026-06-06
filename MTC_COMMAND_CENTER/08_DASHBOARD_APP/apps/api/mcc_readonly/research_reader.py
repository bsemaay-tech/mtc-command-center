from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .paths import canonicalize, default_mcc_root

REVIEW = "review_needed"

# Strategy fields that must be confidently classified for research use.
_KEY_STRATEGY_FIELDS = (
    "strategy_category", "method", "expected_market_regime",
    "long_only_or_long_short", "indicators_used",
)


def _load(mcc_root: Path, filename: str) -> dict[str, Any]:
    path = mcc_root / "05_REGISTRY" / filename
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _needs_review(value: Any) -> bool:
    return value in (None, "", [], REVIEW, [REVIEW])


def build_strategy_research(mcc_root: str | Path | None = None) -> dict[str, Any]:
    """Aggregate the Strategy Research Lab registries into one read-only payload.

    Backs the dashboard ``strategy_research`` snapshot key. Read-only: never
    writes, never runs backtests. Source registries live in ``05_REGISTRY/``
    and are produced by ``03_QUANTLENS/tools/build_strategy_research_registry.py``.
    """
    root = canonicalize(mcc_root or default_mcc_root())

    strategy_reg = _load(root, "STRATEGY_RESEARCH_REGISTRY.json")
    indicator_reg = _load(root, "INDICATOR_REGISTRY.json")
    component_reg = _load(root, "COMPONENT_REGISTRY.json")
    tag_reg = _load(root, "TAG_DICTIONARY.json")
    run_reg = _load(root, "RESEARCH_RUN_REGISTRY.json")
    variant_reg = _load(root, "VARIANT_LOG_REGISTRY.json")
    backtest_reg = _load(root, "RESEARCH_BACKTEST_REGISTRY.json")
    triage_reg = _load(root, "TRIAGE_CANDIDATE_REGISTRY.json")

    strategies = strategy_reg.get("strategies", []) or []
    indicators = indicator_reg.get("indicators", []) or []
    components = component_reg.get("components", []) or []
    tags = tag_reg.get("tags", {}) or {}
    runs = run_reg.get("research_runs", []) or []
    variants = variant_reg.get("variants", []) or []
    backtests = backtest_reg.get("results", []) or []
    triage_candidates = triage_reg.get("candidates", []) or []
    triage_summary = triage_reg.get("summary", {}) or {}

    # --- Missing-metadata / review-needed detection ---
    missing: list[dict[str, Any]] = []
    for s in strategies:
        gaps = [f for f in _KEY_STRATEGY_FIELDS if _needs_review(s.get(f))]
        if not (root / s.get("source_folder", "")).exists():
            gaps.append("source_folder(broken)")
        if gaps:
            missing.append({
                "type": "strategy",
                "id": s.get("strategy_id"),
                "name": s.get("strategy_name"),
                "missing_fields": gaps,
            })
    for ind in indicators:
        gaps = [k for k in ("indicator_category", "primary_use") if _needs_review(ind.get(k))]
        if gaps:
            missing.append({
                "type": "indicator",
                "id": ind.get("indicator_id"),
                "name": ind.get("indicator_name"),
                "missing_fields": gaps,
            })

    rejected = sum(1 for v in variants if str(v.get("decision", "")).lower().startswith("reject"))
    candidates = sum(
        1 for v in variants
        if str(v.get("decision", "")).lower() in {"recommended", "promote", "promoted",
                                                   "recommended_for_further_paper_testing"}
    )

    tag_count = 0
    if isinstance(tags, dict):
        for key, values in tags.items():
            if isinstance(values, list):
                tag_count += len(values)

    overview = {
        "total_strategies": len(strategies),
        "total_indicators": len(indicators),
        "total_components": len(components),
        "total_tags": tag_count,
        "total_research_runs": len(runs),
        "total_variants": len(variants),
        "final_candidate_strategies": candidates,
        "rejected_variants": rejected,
        "strategies_needing_review": sum(1 for m in missing if m["type"] == "strategy"),
        "triage_total": triage_summary.get("total", len(triage_candidates)),
        "triage_with_transcript": triage_summary.get("with_transcript", 0),
        "triage_eligible_for_retriage": triage_summary.get("eligible_for_retriage", 0),
    }

    workflow_docs = {
        "backtest_rules": "03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md",
        "backtest_runbook": "11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md",
        "research_workflow": "_AI_MEMORY/STRATEGY_RESEARCH_WORKFLOW.md",
        "code_review_checklist": "_AI_MEMORY/STRATEGY_CODE_REVIEW_CHECKLIST.md",
        "component_library": "_AI_MEMORY/STRATEGY_COMPONENT_LIBRARY.md",
        "variant_log_template": "03_QUANTLENS/_templates/VARIANT_LOG_TEMPLATE.md",
        "research_report_template": "03_QUANTLENS/_templates/STRATEGY_RESEARCH_REPORT_TEMPLATE.md",
        "transcript_intake_workflow": "03_QUANTLENS/_user_guide/09_TRANSCRIPT_INTAKE_WORKFLOW.md",
        "user_intake_inbox": "00_INBOX/USER_INTAKE/",
    }

    return {
        "schema_version": "1.0",
        "mode": "read_only",
        "overview": overview,
        "strategies": strategies,
        "indicators": indicators,
        "components": components,
        "tags": tags,
        "research_runs": runs,
        "variants": variants,
        "backtest_results": backtests,
        "triage_candidates": triage_candidates,
        "triage_summary": triage_summary,
        "missing_metadata": missing,
        "workflow_docs": workflow_docs,
        "generated_at": strategy_reg.get("generated_at"),
    }
