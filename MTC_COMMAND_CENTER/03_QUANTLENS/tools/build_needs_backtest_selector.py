from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MCC_ROOT = Path(__file__).resolve().parents[2]
API_ROOT = MCC_ROOT / "08_DASHBOARD_APP" / "apps" / "api"
OUTPUT_ROOT = MCC_ROOT / "03_QUANTLENS" / "05_BACKTEST_RESULTS"
JSON_OUTPUT = OUTPUT_ROOT / "NEEDS_BACKTEST_SELECTOR.json"
MD_OUTPUT = OUTPUT_ROOT / "NEEDS_BACKTEST_SELECTOR.md"

if str(API_ROOT) not in sys.path:
    sys.path.insert(0, str(API_ROOT))

from mcc_readonly.read_model import build_dashboard_snapshot  # noqa: E402


def select_needs_backtest(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        if not row.get("eligible_for_backtest"):
            continue
        if row.get("scorecard_v2"):
            continue
        verdict = row.get("expert_quantlens_verdict") if isinstance(row.get("expert_quantlens_verdict"), dict) else {}
        decision = str(verdict.get("decision") or "").upper()
        if decision in {"SALVAGE", "GARBAGE", "CLOSED_SOURCE_STOP"}:
            continue
        selected.append(_selector_row(row, verdict))

    selected.sort(
        key=lambda item: (
            item["priority_rank"],
            item["strategy_id"],
        )
    )
    return selected


def build_selector(mcc_root: str | Path | None = None) -> dict[str, Any]:
    root = Path(mcc_root).resolve() if mcc_root else MCC_ROOT
    snapshot = build_dashboard_snapshot(root)
    rows = snapshot.get("candidate_audit", {}).get("rows") or []
    selected = select_needs_backtest(rows)
    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "candidate_audit.rows",
        "criteria": [
            "eligible_for_backtest == true",
            "scorecard_v2 is absent",
            "expert_quantlens.decision not in SALVAGE/GARBAGE/CLOSED_SOURCE_STOP",
        ],
        "count": len(selected),
        "candidates": selected,
    }


def write_outputs(payload: dict[str, Any], json_path: Path = JSON_OUTPUT, md_path: Path = MD_OUTPUT) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    md_path.write_text(_markdown(payload), encoding="utf-8")


def _selector_row(row: dict[str, Any], verdict: dict[str, Any]) -> dict[str, Any]:
    strategy_id = str(row.get("id") or row.get("strategy_id") or row.get("candidate_id") or "")
    display_name = str(row.get("strategy_display_name") or row.get("name") or row.get("title") or strategy_id)
    deterministic = bool(row.get("has_deterministic_rules"))
    source_ready = bool(row.get("has_source_url_transcript"))
    priority_rank = _priority_rank(row, verdict)
    return {
        "strategy_id": strategy_id,
        "strategy_display_name": display_name,
        "priority_rank": priority_rank,
        "priority_band": _priority_band(priority_rank),
        "expert_decision": verdict.get("decision") or "UNKNOWN",
        "expert_blocking": verdict.get("blocking") or "",
        "next_action": verdict.get("next_action") or row.get("recommended_next_pipeline_step") or "Run source audit.",
        "has_deterministic_rules": deterministic,
        "has_source_url_transcript": source_ready,
        "stg_code": row.get("stg_code") or "",
        "source_url": row.get("source_url") or "",
        "transcript_path": row.get("transcript_path") or "",
    }


def _priority_rank(row: dict[str, Any], verdict: dict[str, Any]) -> int:
    rank = 100
    if row.get("has_deterministic_rules"):
        rank -= 30
    if row.get("has_source_url_transcript"):
        rank -= 20
    if str(verdict.get("decision") or "").upper() == "NEEDS_CLARIFICATION":
        rank += 10
    if str(row.get("source_quality") or "").upper() == "REJECTED":
        rank += 10
    return rank


def _priority_band(rank: int) -> str:
    if rank <= 50:
        return "HIGH"
    if rank <= 75:
        return "MEDIUM"
    return "LOW"


def _markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# NEEDS_BACKTEST_SELECTOR",
        "",
        f"Generated: `{payload.get('generated_at')}`",
        f"Candidate count: **{payload.get('count', 0)}**",
        "",
        "## Criteria",
        "",
    ]
    lines.extend(f"- {item}" for item in payload.get("criteria", []))
    lines.extend([
        "",
        "## Candidates",
        "",
        "| # | Priority | Strategy | Expert decision | Deterministic | Source ready | Next action |",
        "|---:|---|---|---|---|---|---|",
    ])
    for idx, row in enumerate(payload.get("candidates", []), 1):
        lines.append(
            "| {idx} | {priority} | `{sid}`<br>{name} | {decision} | {det} | {src} | {action} |".format(
                idx=idx,
                priority=row.get("priority_band", ""),
                sid=row.get("strategy_id", ""),
                name=_pipe_safe(row.get("strategy_display_name", "")),
                decision=row.get("expert_decision", ""),
                det="yes" if row.get("has_deterministic_rules") else "no",
                src="yes" if row.get("has_source_url_transcript") else "no",
                action=_pipe_safe(row.get("next_action", "")),
            )
        )
    return "\n".join(lines) + "\n"


def _pipe_safe(value: Any) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", " ")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-out", default=str(JSON_OUTPUT))
    parser.add_argument("--md-out", default=str(MD_OUTPUT))
    args = parser.parse_args()

    payload = build_selector()
    write_outputs(payload, Path(args.json_out), Path(args.md_out))
    print(f"written {args.json_out}")
    print(f"written {args.md_out}")
    print(f"candidates {payload['count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
