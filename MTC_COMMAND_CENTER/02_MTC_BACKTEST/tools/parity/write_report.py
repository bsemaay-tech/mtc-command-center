from __future__ import annotations

import json
from pathlib import Path


def write_report(output_dir: Path, results: list[dict], summary: dict) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "parity_results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    recurring = {}
    for row in results:
        note = ""
        compare = row.get("compare") or {}
        if isinstance(compare, dict):
            note = str(compare.get("note", "")).strip()
        if not note:
            note = str(row.get("error", "")).strip()
        if note:
            recurring[note] = recurring.get(note, 0) + 1
    lines = [
        "# Parity Summary",
        "",
        f"- total planned cases: {summary.get('total_planned', 0)}",
        f"- total processed: {summary.get('processed', 0)}",
        f"- pass count: {summary.get('pass', 0)}",
        f"- fail count: {summary.get('fail', 0)}",
        f"- partial count: {summary.get('partial', 0)}",
        f"- error count: {summary.get('error', 0)}",
        f"- skipped count: {summary.get('skipped', 0)}",
        "",
        "## Manual Review",
    ]
    for item in summary.get("manual_review", []):
        lines.append(f"- {item}")
    lines.extend(["", "## Recurring Failure Patterns"])
    if recurring:
        for note, count in sorted(recurring.items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"- {count}x {note}")
    else:
        lines.append("- none")
    (output_dir / "parity_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
