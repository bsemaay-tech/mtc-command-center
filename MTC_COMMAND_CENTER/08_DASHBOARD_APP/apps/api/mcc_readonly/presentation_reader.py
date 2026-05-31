from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


_ACTION_HINTS: dict[str, str] = {
    "Extract deterministic rules": "Turn the source into explicit entry/exit rules that can be tested mechanically.",
    "Run backtest": "Run a sandbox backtest on the candidate's deterministic rules.",
    "Run walk-forward / OOS / alpha test": "Run the strategy through out-of-sample or walk-forward validation before promotion.",
    "Build promotion packet": "Collect the proof package needed to move the strategy into PineTS parity review.",
    "Build promotion pack": "Collect the proof package needed to move the strategy into PineTS parity review.",
    "Run PineTS parity": "Compare Python and Pine on the same data to confirm the signals match bar-for-bar.",
    "Run PineTS Pine=Python parity": "Compare PineTS and Python on the same bars and require matching signals before MTC_V2 work.",
    "Start forward paper-trade": "Begin a paper-trade run with live data but without risking capital.",
    "Finish: Start forward paper-trade (collect new trades)": "The parity gate is done; start or continue forward paper trading until enough new live-paper trades exist.",
    "Collect forward paper-trade results": "Keep recording forward trades until there is enough real-time evidence to judge the strategy.",
    "Monitor integrated strategy": "Watch the integrated strategy in production and keep the evidence current.",
    "Source audit / park": "Hold the item until the source or formula is verified well enough to test safely.",
    "Resolve source/formula audit": "Verify the exact source, formula, repaint/lookahead behavior, and entry/exit rules.",
    "Split into indicator cases": "Break a multi-signal pack into separate testable formulas before any backtest.",
    "Split into indicator cases ? then audit each formula": "Break this mixed source into separate formulas, then audit each formula as its own candidate.",
    "Wiki/module branch ? park": "Keep the item in the wiki/module lane instead of the strategy lane.",
    "Rejected source ? source audit / park": "Do not backtest rejected material; keep it parked unless the source classification changes.",
    "Merge into canonical record": "This row duplicates another strategy; keep the canonical row and merge evidence there.",
    "Review": "No stronger next step was detected; review the row manually.",
}


def action_hint(action: Any) -> str:
    key = str(action or "").strip()
    return _ACTION_HINTS.get(key, "Read the row details for the next explicit step.")


@lru_cache(maxsize=8)
def _load_stg_code_map_file(path_str: str) -> dict[str, str]:
    path = Path(path_str)
    if not path.exists():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(raw, dict):
        return {}
    return {str(key): str(value) for key, value in raw.items() if str(value).strip()}


def load_stg_code_map(mcc_root: str | Path) -> dict[str, str]:
    root = Path(mcc_root)
    map_path = root / "11_TRIAGE" / "strategies" / "_stg_code_map.json"
    return _load_stg_code_map_file(str(map_path))


def resolve_stg_code(stg_map: dict[str, str], *candidates: Any) -> str:
    for candidate in candidates:
        key = str(candidate or "").strip()
        if key and key in stg_map:
            return stg_map[key]
    return ""


def build_scorecard(row: dict[str, Any], audit_row: dict[str, Any] | None = None) -> dict[str, Any]:
    audit_row = audit_row or {}
    source_record = audit_row.get("source_record") if isinstance(audit_row.get("source_record"), dict) else {}
    source_url = _first_text(
        row.get("source_url"),
        audit_row.get("source_url"),
        source_record.get("source_url"),
    )
    transcript_path = _first_text(
        row.get("transcript_path"),
        audit_row.get("transcript_path"),
        source_record.get("transcript_path"),
    )
    source_material = bool(
        row.get("has_source_url_transcript")
        or audit_row.get("has_source_url_transcript")
        or source_url
        or transcript_path
    )
    deterministic_rules = bool(
        row.get("has_deterministic_rules")
        or audit_row.get("has_deterministic_rules")
        or _has_rule_text(row, audit_row, source_record)
    )
    blocked_reason = str(
        audit_row.get("blocked_reason")
        or row.get("blocked_reason")
        or ""
    ).strip()
    current_stage_key = str(
        row.get("current_stage_key")
        or audit_row.get("current_stage_key")
        or ""
    ).strip()
    source_quality = str(
        audit_row.get("source_quality")
        or row.get("source_quality")
        or source_record.get("source_quality")
        or ""
    ).strip().upper()

    source_score, source_note = _source_coverage_score(source_url, transcript_path)
    rule_score, rule_note = _rule_quality_score(row, audit_row, source_record, deterministic_rules)
    backtest_score, backtest_note = _backtest_evidence_score(row, audit_row, current_stage_key)
    readiness_score, readiness_note = _execution_readiness_score(row, audit_row, current_stage_key)
    risk_score, risk_note = _risk_score(
        blocked_reason=blocked_reason,
        source_quality=source_quality,
        source_material=source_material,
        deterministic_rules=deterministic_rules,
        current_stage_key=current_stage_key,
    )

    components = [
        {
            "key": "source_coverage",
            "label": "Source coverage",
            "score": source_score,
            "max": 20,
            "note": source_note,
        },
        {
            "key": "rule_quality",
            "label": "Rule quality",
            "score": rule_score,
            "max": 25,
            "note": rule_note,
        },
        {
            "key": "backtest_evidence",
            "label": "Backtest evidence",
            "score": backtest_score,
            "max": 35,
            "note": backtest_note,
        },
        {
            "key": "execution_readiness",
            "label": "Execution readiness",
            "score": readiness_score,
            "max": 10,
            "note": readiness_note,
        },
        {
            "key": "risk_adjustment",
            "label": "Risk / cleanliness",
            "score": risk_score,
            "max": 10,
            "note": risk_note,
        },
    ]
    total = sum(int(component["score"]) for component in components)
    total = max(0, min(100, total))
    return {
        "total": total,
        "max": 100,
        "label": f"{total}/100",
        "band": _score_band(total),
        "note": "Heuristic composite score for triage; not a profit forecast.",
        "components": components,
    }


def _first_text(*values: Any) -> str:
    for value in values:
        text = str(value or "").strip()
        if text:
            return text
    return ""


def _has_rule_text(row: dict[str, Any], audit_row: dict[str, Any], source_record: dict[str, Any]) -> bool:
    checks = [
        row.get("producer_spec"),
        row.get("description"),
        row.get("metrics"),
        audit_row.get("source_record"),
        source_record.get("rules_text"),
        source_record.get("exact_rules_if_available"),
        source_record.get("exact_rules"),
    ]
    for value in checks:
        if isinstance(value, dict):
            if any(_first_text(v) for v in value.values()):
                return True
        elif _first_text(value):
            return True
    return False


def _source_coverage_score(source_url: str, transcript_path: str) -> tuple[int, str]:
    score = 0
    parts = []
    if source_url:
        score += 10
        parts.append("URL linked")
    if transcript_path:
        score += 10
        parts.append("transcript linked")
    return score, ", ".join(parts) or "missing source coverage"


def _rule_quality_score(
    row: dict[str, Any],
    audit_row: dict[str, Any],
    source_record: dict[str, Any],
    deterministic_rules: bool,
) -> tuple[int, str]:
    score = 0
    parts = []
    if deterministic_rules:
        score += 15
        parts.append("deterministic rules detected")
    entry_rule = _first_text(
        row.get("description", {}).get("entry") if isinstance(row.get("description"), dict) else "",
        row.get("producer_spec", {}).get("entry_pseudo") if isinstance(row.get("producer_spec"), dict) else "",
        source_record.get("exact_rules_if_available"),
        source_record.get("exact_rules"),
        source_record.get("rules_text"),
    )
    exit_rule = _first_text(
        row.get("description", {}).get("exit") if isinstance(row.get("description"), dict) else "",
        row.get("producer_spec", {}).get("exit_pseudo") if isinstance(row.get("producer_spec"), dict) else "",
        source_record.get("exact_rules_if_available"),
        source_record.get("exact_rules"),
    )
    if entry_rule:
        score += 5
        parts.append("entry rule explicit")
    if exit_rule:
        score += 5
        parts.append("exit rule explicit")
    high_confidence = row.get("producer_spec", {}).get("rules_high_confidence") if isinstance(row.get("producer_spec"), dict) else None
    if isinstance(high_confidence, list) and high_confidence:
        score += 5
        parts.append("high-confidence rule list")
    elif source_record.get("recommended_next_action") or audit_row.get("source_quality"):
        score += 2
        parts.append("source classification present")
    return min(score, 25), ", ".join(parts) or "thin rule evidence"


def _stage_rank(stage_key: str) -> int:
    order = {
        "discovered": 0,
        "classified": 1,
        "backtested": 2,
        "promoted": 3,
        "pre_parity": 4,
        "paper_trade": 5,
        "integrated": 6,
    }
    return order.get(stage_key, 0)


def _backtest_evidence_score(row: dict[str, Any], audit_row: dict[str, Any], current_stage_key: str) -> tuple[int, str]:
    score = 0
    parts = []
    stage_rank = _stage_rank(current_stage_key)
    stage_points = {
        0: 0,
        1: 2,
        2: 12,
        3: 16,
        4: 20,
        5: 23,
        6: 25,
    }.get(stage_rank, 0)
    score += stage_points
    if stage_points:
        parts.append(f"stage maturity {current_stage_key or 'unknown'}")

    metrics = row.get("metrics") if isinstance(row.get("metrics"), dict) else {}
    return_pct = _number(metrics.get("return_pct_compound") or metrics.get("return_pct") or metrics.get("strategy_return_pct"))
    profit_factor = _number(metrics.get("profit_factor"))
    trades = _number(metrics.get("trades"))
    pf_points = 0
    if profit_factor is not None:
        pf_points = max(0, min(5, int(round((profit_factor - 1.0) * 5))))
        if pf_points:
            parts.append(f"PF {profit_factor:.2f}")
    return_points = 0
    if return_pct is not None and return_pct > 0:
        return_points = max(0, min(5, int(round(return_pct / 20.0))))
        if return_points:
            parts.append(f"positive return {return_pct:.2f}%")
    trade_points = 0
    if trades is not None and trades > 0:
        trade_points = max(0, min(5, int(round(min(trades, 50) / 10.0))))
        if trade_points:
            parts.append(f"{int(trades)} trades")

    parity = row.get("pinets_parity_proof") if isinstance(row.get("pinets_parity_proof"), dict) else {}
    if parity:
        summary = parity.get("summary") if isinstance(parity.get("summary"), dict) else {}
        if summary.get("verdict") == "PASS":
            score += 3
            parts.append("PineTS parity pass")
    score += min(10, pf_points + return_points + trade_points)
    return min(score, 35), ", ".join(parts) or "backtest evidence missing"


def _execution_readiness_score(row: dict[str, Any], audit_row: dict[str, Any], current_stage_key: str) -> tuple[int, str]:
    score = 0
    parts = []
    stage_rank = _stage_rank(current_stage_key)
    if stage_rank >= 3:
        score += 3
        parts.append("promotion-ready stage")
    if stage_rank >= 4:
        score += 3
        parts.append("pre-parity or later")
    if stage_rank >= 5:
        score += 2
        parts.append("paper-trade ready")
    if stage_rank >= 6:
        score += 2
        parts.append("integrated")

    if row.get("pinets_parity_proof"):
        score += 2
        parts.append("parity proof attached")
    if row.get("paper_trade_detail"):
        score += 2
        parts.append("paper-trade detail attached")

    return min(score, 10), ", ".join(parts) or "not yet ready for execution"


def _risk_score(
    *,
    blocked_reason: str,
    source_quality: str,
    source_material: bool,
    deterministic_rules: bool,
    current_stage_key: str,
) -> tuple[int, str]:
    score = 10
    parts = ["clean source path"]
    if blocked_reason:
        score -= 6
        parts.append(f"blocked: {blocked_reason}")
    if source_quality == "REJECTED":
        score -= 3
        parts.append("rejected source quality")
    elif source_quality == "LOW":
        score -= 1
        parts.append("low source quality")
    if not source_material:
        score -= 2
        parts.append("missing source material")
    if not deterministic_rules and _stage_rank(current_stage_key) < 2:
        score -= 1
        parts.append("rules still thin")
    return max(0, min(10, score)), ", ".join(parts)


def _score_band(total: int) -> str:
    if total >= 85:
        return "high"
    if total >= 65:
        return "medium"
    return "low"


def _number(value: Any) -> float | None:
    try:
        if value is None or value == "":
            return None
        return float(value)
    except Exception:
        return None
