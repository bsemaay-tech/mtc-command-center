from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any

from .paths import canonicalize, default_mcc_root
from .presentation_reader import action_hint


def build_mtc_v2_readiness(
    mcc_root: str | Path | None = None,
    candidate_pipeline: dict[str, Any] | None = None,
    candidate_audit: dict[str, Any] | None = None,
) -> dict[str, Any]:
    root = canonicalize(mcc_root or default_mcc_root())
    mtc_root = root.parent / "01_MASTER TEMPLATE_V2"
    pipeline_rows = (candidate_pipeline or {}).get("rows", []) or []
    audit_rows = (candidate_audit or {}).get("rows", []) or []
    audit_by_id = {str(row.get("id") or ""): row for row in audit_rows}

    rows = [
        _readiness_row(row, audit_by_id.get(str(row.get("id") or "")))
        for row in pipeline_rows
        if not (audit_by_id.get(str(row.get("id") or "")) or {}).get("is_source_parent")
    ]
    rows.sort(key=lambda row: (int(row.get("readiness_rank") or 99), -int(row.get("score") or 0), str(row.get("id") or "")))

    status_counts: dict[str, int] = {}
    for row in rows:
        status = str(row.get("status") or "UNKNOWN")
        status_counts[status] = status_counts.get(status, 0) + 1

    parity_meta = _read_mtc_v2_parity(mtc_root)
    return {
        "schema_version": "1.0",
        "mode": "read_only",
        "source": "Pipeline + Audit + MTC_V2 parity tracker",
        "mtc_v2_root": str(mtc_root),
        "pine_path": str(mtc_root / "01_PINE" / "MTC_V2.pine"),
        "pine_exists": (mtc_root / "01_PINE" / "MTC_V2.pine").exists(),
        "architecture_path": str(mtc_root / "03_DOCS" / "MTC_V2_ARCHITECTURE.md"),
        "architecture_exists": (mtc_root / "03_DOCS" / "MTC_V2_ARCHITECTURE.md").exists(),
        "parity_tracker": parity_meta,
        "summary": {
            "total_rows": len(rows),
            "ready_for_review": status_counts.get("READY_FOR_MTC_V2_REVIEW", 0),
            "needs_forward_evidence": status_counts.get("NEEDS_FORWARD_EVIDENCE", 0),
            "needs_pinets_parity": status_counts.get("NEEDS_PINETS_PARITY", 0),
            "needs_promotion_pack": status_counts.get("NEEDS_PROMOTION_PACK", 0),
            "needs_backtest": status_counts.get("NEEDS_BACKTEST", 0),
            "blocked_or_parked": sum(
                count
                for status, count in status_counts.items()
                if status in {"BLOCKED_SOURCE_AUDIT", "PARKED_OR_SPLIT", "LOW_SCORE_REVIEW"}
            ),
            "status_counts": status_counts,
            "calibration_note": _calibration_note(status_counts),
        },
        "rows": rows,
    }


def _readiness_row(row: dict[str, Any], audit_row: dict[str, Any] | None) -> dict[str, Any]:
    audit_row = audit_row or {}
    stage = str(row.get("current_stage_key") or audit_row.get("current_stage_key") or "")
    next_action = str(row.get("next_action") or audit_row.get("recommended_next_pipeline_step") or "Review")
    score = _number(row.get("score") or audit_row.get("score"))
    score = int(score or 0)
    blocked_reason = str(audit_row.get("blocked_reason") or "").strip()
    eligible = bool(audit_row.get("eligible_for_backtest", True))
    audit_status = str(audit_row.get("audit_status") or "").upper()
    forward_progress = _forward_progress(row.get("paper_trade_detail"))
    status, reason, blocker = _readiness_status(
        stage=stage,
        next_action=next_action,
        score=score,
        blocked_reason=blocked_reason,
        eligible=eligible,
        audit_status=audit_status,
        forward_progress=forward_progress,
    )
    decision_sentence = _decision_sentence(
        strategy_id=str(row.get("id") or audit_row.get("id") or ""),
        status=status,
        score=score,
        reason=reason,
        blocker=blocker,
        forward_progress=forward_progress,
    )
    return {
        "id": row.get("id") or audit_row.get("id") or "",
        "stg_code": row.get("stg_code") or audit_row.get("stg_code") or "",
        "score": score,
        "score_label": f"{score}/100",
        "score_band": _score_band(score),
        "status": status,
        "status_label": status.replace("_", " ").title(),
        "readiness_rank": _readiness_rank(status),
        "reason": reason,
        "blocker": blocker,
        "decision_sentence": decision_sentence,
        "stage": stage,
        "stage_label": str(row.get("current_stage_label") or audit_row.get("pipeline_stage_label") or stage).replace("_", " "),
        "next_action": next_action,
        "next_action_hint": action_hint(next_action),
        "source_quality": audit_row.get("source_quality") or "",
        "eligible_for_backtest": eligible,
        "has_deterministic_rules": bool(audit_row.get("has_deterministic_rules", False)),
        "has_source_material": bool(audit_row.get("has_source_url_transcript", False) or row.get("source_url")),
        "direction_status": (row.get("directional_research") or {}).get("status", ""),
        "forward_progress": forward_progress,
    }


def _readiness_status(
    *,
    stage: str,
    next_action: str,
    score: int,
    blocked_reason: str,
    eligible: bool,
    audit_status: str,
    forward_progress: dict[str, Any],
) -> tuple[str, str, str]:
    action_upper = next_action.upper()
    if audit_status == "SPLIT_REQUIRED" or "SPLIT" in action_upper:
        return "PARKED_OR_SPLIT", "Split the source into separate formulas before MTC_V2 work.", "split required"
    if blocked_reason or not eligible or "SOURCE" in action_upper and "AUDIT" in action_upper:
        return "BLOCKED_SOURCE_AUDIT", "Resolve source/formula evidence before any MTC_V2 integration.", blocked_reason or "source audit"
    if score < 65:
        return "LOW_SCORE_REVIEW", "The evidence score is still too low for MTC_V2 planning.", "score below 65"
    if "PAPER" in action_upper or stage == "pre_parity":
        target = forward_progress.get("target_trades")
        actual = forward_progress.get("actual_trades")
        if target:
            return (
                "NEEDS_FORWARD_EVIDENCE",
                f"Parity is close/done; collect forward paper-trade evidence ({actual}/{target} trades).",
                "forward evidence",
            )
        return "NEEDS_FORWARD_EVIDENCE", "Parity is close or done; collect forward paper-trade evidence next.", "forward evidence"
    if "PINETS" in action_upper or stage == "promoted":
        return "NEEDS_PINETS_PARITY", "Run PineTS/Python parity before this can become an MTC_V2 candidate.", "PineTS parity"
    if "PROMOTION" in action_upper or stage == "backtested":
        return "NEEDS_PROMOTION_PACK", "Build the promotion proof packet before parity review.", "promotion packet"
    if stage in {"classified", "discovered"}:
        return "NEEDS_BACKTEST", "Backtest/OOS evidence is required before MTC_V2 planning.", "backtest evidence"
    if score >= 85:
        return "READY_FOR_MTC_V2_REVIEW", "Evidence is strong enough for a read-only MTC_V2 review queue.", ""
    return "LOW_SCORE_REVIEW", "Manual review is needed before MTC_V2 planning.", "manual review"


def _forward_progress(detail: Any) -> dict[str, Any]:
    if not isinstance(detail, dict):
        return {
            "status": "NO_FORWARD_PLAN",
            "actual_trades": 0,
            "target_trades": None,
            "progress_pct": 0,
            "label": "No forward plan",
        }
    results = detail.get("forward_results") if isinstance(detail.get("forward_results"), dict) else {}
    metrics = results.get("metrics") if isinstance(results.get("metrics"), dict) else {}
    actual = _number(
        metrics.get("trades")
        or metrics.get("trade_count")
        or metrics.get("forward_trade_count")
        or detail.get("forward_trades")
    )
    actual_int = int(actual or 0)
    target = _target_forward_trades(detail)
    progress_pct = int(round((actual_int / target) * 100)) if target else 0
    progress_pct = max(0, min(100, progress_pct))
    if target and actual_int >= target:
        status = "TARGET_MET"
    elif target:
        status = "COLLECTING_FORWARD_TRADES"
    else:
        status = str(detail.get("forward_status") or detail.get("status") or "WAITING_FOR_FORWARD_RESULTS")
    label = f"{actual_int}/{target} trades" if target else f"{actual_int} forward trades"
    return {
        "status": status,
        "actual_trades": actual_int,
        "target_trades": target,
        "progress_pct": progress_pct,
        "label": label,
        "plan_path": detail.get("plan_path"),
        "results_file": results.get("file"),
    }


def _target_forward_trades(detail: dict[str, Any]) -> int | None:
    for line in detail.get("plan_summary") or []:
        match = re.search(r"Minimum\s+NEW\s+forward\s+trades[^0-9]*(\d+)", str(line), re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None


def _decision_sentence(
    *,
    strategy_id: str,
    status: str,
    score: int,
    reason: str,
    blocker: str,
    forward_progress: dict[str, Any],
) -> str:
    if status == "NEEDS_FORWARD_EVIDENCE" and forward_progress.get("target_trades"):
        return (
            f"{strategy_id} scores {score}/100 but is not MTC_V2-ready because forward paper-trade "
            f"evidence is incomplete ({forward_progress.get('actual_trades')}/{forward_progress.get('target_trades')} trades)."
        )
    if blocker:
        return f"{strategy_id} scores {score}/100 and is held in {status} because of {blocker}."
    return f"{strategy_id} scores {score}/100. {reason}"


def _readiness_rank(status: str) -> int:
    order = {
        "READY_FOR_MTC_V2_REVIEW": 0,
        "NEEDS_FORWARD_EVIDENCE": 1,
        "NEEDS_PINETS_PARITY": 2,
        "NEEDS_PROMOTION_PACK": 3,
        "NEEDS_BACKTEST": 4,
        "LOW_SCORE_REVIEW": 5,
        "BLOCKED_SOURCE_AUDIT": 6,
        "PARKED_OR_SPLIT": 7,
    }
    return order.get(status, 99)


def _calibration_note(status_counts: dict[str, int]) -> str:
    ready = status_counts.get("READY_FOR_MTC_V2_REVIEW", 0)
    forward = status_counts.get("NEEDS_FORWARD_EVIDENCE", 0)
    if ready == 0 and forward:
        return "No strategy is fully MTC_V2-ready yet; the leading candidate still needs forward paper-trade evidence."
    if ready == 0:
        return "No strategy is fully MTC_V2-ready yet under the current source, score, parity, and forward-evidence gates."
    return f"{ready} strategy candidate(s) are ready for read-only MTC_V2 review."


def _read_mtc_v2_parity(mtc_root: Path) -> dict[str, Any]:
    tracker = mtc_root / "05_PARITY" / "MTC_V2_PARITY_CASES.csv"
    if not tracker.exists():
        return {"path": str(tracker), "exists": False, "total_cases": 0, "pass_cases": 0}
    total = 0
    passed = 0
    done = 0
    try:
        with tracker.open("r", encoding="utf-8-sig", newline="") as handle:
            for record in csv.DictReader(handle):
                total += 1
                verdict = str(record.get("parity_verdict") or "").upper()
                status = str(record.get("status") or record.get("case_status") or "").upper()
                if verdict == "PASS":
                    passed += 1
                if status == "DONE":
                    done += 1
    except Exception as exc:
        return {"path": str(tracker), "exists": True, "ok": False, "error": str(exc)}
    return {
        "path": str(tracker),
        "exists": True,
        "ok": True,
        "total_cases": total,
        "done_cases": done,
        "pass_cases": passed,
    }


def _score_band(score: int) -> str:
    if score >= 85:
        return "high"
    if score >= 65:
        return "medium"
    return "low"


def _number(value: Any) -> float | None:
    try:
        if value is None or value == "":
            return None
        return float(value)
    except Exception:
        return None
