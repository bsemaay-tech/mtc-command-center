from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .paths import canonicalize, default_mcc_root


REGISTRY_REL_PATH = Path("05_REGISTRY") / "AI_QUANTLENS_VERDICT_REGISTRY.json"


def build_expert_quantlens(mcc_root: str | Path | None = None) -> dict[str, Any]:
    root = canonicalize(mcc_root or default_mcc_root())
    path = root / REGISTRY_REL_PATH
    if not path.exists():
        return _empty("registry_not_found")
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return _empty(f"json_error: {exc}")

    entries = raw.get("entries") if isinstance(raw, dict) else []
    by_strategy_id: dict[str, dict[str, Any]] = {}
    if isinstance(entries, list):
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            strategy_id = _string(entry.get("strategy_id"))
            decision = _string(entry.get("decision"))
            if not strategy_id or not decision:
                continue
            by_strategy_id[strategy_id] = {
                "strategy_id": strategy_id,
                "strategy_display_name": _string(entry.get("strategy_display_name")),
                "decision": decision,
                "decision_label": _string(entry.get("decision_label")) or _decision_label(decision),
                "reason": _string(entry.get("reason")),
                "can_test": _string(entry.get("can_test")),
                "blocking": _string(entry.get("blocking")),
                "next_action": _string(entry.get("next_action")),
                "commercial_value": _string(entry.get("commercial_value")),
                "literature_relevance": _string(entry.get("literature_relevance")),
                "testability": _string(entry.get("testability")),
                "complexity": _string(entry.get("complexity")),
                "risk_flags": entry.get("risk_flags") if isinstance(entry.get("risk_flags"), list) else [],
                "score_reference": _string(entry.get("score_reference")),
                "source": _string(entry.get("source")) or "ai_quantlens_verdict_registry",
            }

    return {
        "schema_version": raw.get("schema_version") or "1.0" if isinstance(raw, dict) else "1.0",
        "source": REGISTRY_REL_PATH.as_posix(),
        "generated_at": raw.get("generated_at") if isinstance(raw, dict) else None,
        "model": raw.get("model") if isinstance(raw, dict) else None,
        "count": len(by_strategy_id),
        "by_strategy_id": by_strategy_id,
        "diagnostics": {"available": True},
    }


def attach_expert_quantlens_to_rows(
    rows: list[dict[str, Any]],
    expert_quantlens: dict[str, Any],
) -> list[dict[str, Any]]:
    by_strategy_id = expert_quantlens.get("by_strategy_id") if isinstance(expert_quantlens, dict) else {}
    if not isinstance(by_strategy_id, dict) or not by_strategy_id:
        return rows
    out: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            out.append(row)
            continue
        match = _match(row, by_strategy_id)
        if not match:
            out.append(row)
            continue
        new_row = dict(row)
        new_row["expert_quantlens_verdict"] = match
        out.append(new_row)
    return out


def attach_expert_quantlens_to_scorecards(
    scorecards: dict[str, Any],
    expert_quantlens: dict[str, Any],
) -> dict[str, Any]:
    by_strategy_id = expert_quantlens.get("by_strategy_id") if isinstance(expert_quantlens, dict) else {}
    if not isinstance(scorecards, dict) or not isinstance(by_strategy_id, dict) or not by_strategy_id:
        return scorecards
    out = dict(scorecards)
    cards = scorecards.get("cards")
    if isinstance(cards, list):
        out["cards"] = [_scorecard_with_verdict(card, by_strategy_id) for card in cards]
    by_strategy = scorecards.get("by_strategy")
    if isinstance(by_strategy, dict):
        named_by_strategy = {}
        for strategy_id, payload in by_strategy.items():
            if not isinstance(payload, dict):
                named_by_strategy[strategy_id] = payload
                continue
            named_payload = dict(payload)
            if isinstance(payload.get("display_card"), dict):
                named_payload["display_card"] = _scorecard_with_verdict(payload["display_card"], by_strategy_id)
            if isinstance(payload.get("cards"), list):
                named_payload["cards"] = [
                    _scorecard_with_verdict(card, by_strategy_id) for card in payload["cards"]
                ]
            named_by_strategy[strategy_id] = named_payload
        out["by_strategy"] = named_by_strategy
    return out


def _scorecard_with_verdict(card: Any, by_strategy_id: dict[str, Any]) -> Any:
    if not isinstance(card, dict):
        return card
    match = _match(card, by_strategy_id)
    if not match:
        return card
    out = dict(card)
    out["expert_quantlens_verdict"] = match
    return out


def _match(row: dict[str, Any], by_strategy_id: dict[str, Any]) -> dict[str, Any] | None:
    keys = (
        row.get("id"),
        row.get("strategy_id"),
        row.get("candidate_id"),
        row.get("base_strategy_id"),
    )
    for key in keys:
        text = _string(key)
        if text and text in by_strategy_id:
            return by_strategy_id[text]
    return None


def _decision_label(decision: str) -> str:
    return {
        "PASS": "Pass to technical scoring",
        "NEEDS_CLARIFICATION": "Needs source clarification",
        "RESEARCH_ONLY": "Research only",
        "SALVAGE": "Salvage ideas only",
        "REJECT": "Reject",
        "GARBAGE": "Garbage",
        "CLOSED_SOURCE_STOP": "Closed-source / paid indicator detected - analysis stopped",
        "COMPLEXITY_OVERLOAD": "Too complex - simplification required",
    }.get(decision, decision.replace("_", " ").title())


def _empty(reason: str) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "source": REGISTRY_REL_PATH.as_posix(),
        "count": 0,
        "by_strategy_id": {},
        "diagnostics": {"available": False, "reason": reason},
    }


def _string(value: Any) -> str:
    return str(value or "").strip()
