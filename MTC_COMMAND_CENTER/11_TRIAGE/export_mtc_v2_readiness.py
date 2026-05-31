from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
API_SRC = ROOT / "08_DASHBOARD_APP" / "apps" / "api"
if str(API_SRC) not in sys.path:
    sys.path.insert(0, str(API_SRC))

from mcc_readonly.read_model import build_dashboard_snapshot  # noqa: E402


def main() -> int:
    snapshot = build_dashboard_snapshot(ROOT)
    readiness = snapshot.get("mtc_v2_readiness", {})
    rows = readiness.get("rows", []) or []
    out_dir = ROOT / "11_TRIAGE"
    csv_path = out_dir / "mtc_v2_readiness_export_2026-05-31.csv"
    md_path = out_dir / "mtc_v2_readiness_export_2026-05-31.md"

    _write_csv(csv_path, rows)
    _write_markdown(md_path, readiness, rows)
    print(f"wrote {csv_path}")
    print(f"wrote {md_path}")
    return 0


def _write_csv(path: Path, rows: list[dict]) -> None:
    fields = [
        "stg_code",
        "id",
        "score",
        "status",
        "stage",
        "blocker",
        "next_action",
        "forward_label",
        "decision_sentence",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            forward = row.get("forward_progress") or {}
            writer.writerow(
                {
                    "stg_code": row.get("stg_code") or "",
                    "id": row.get("id") or "",
                    "score": row.get("score") or 0,
                    "status": row.get("status") or "",
                    "stage": row.get("stage") or "",
                    "blocker": row.get("blocker") or "",
                    "next_action": row.get("next_action") or "",
                    "forward_label": forward.get("label") or "",
                    "decision_sentence": row.get("decision_sentence") or "",
                }
            )


def _write_markdown(path: Path, readiness: dict, rows: list[dict]) -> None:
    summary = readiness.get("summary") or {}
    counts = Counter(row.get("status") or "UNKNOWN" for row in rows)
    leading = rows[:20]
    lines = [
        "# MTC_V2 Readiness Export",
        "",
        "Date: 2026-05-31",
        "",
        "Read-only export. This report does not edit `MTC_V2.pine`.",
        "",
        "## Calibration",
        "",
        f"- {summary.get('calibration_note') or 'No calibration note.'}",
        f"- Total rows: {summary.get('total_rows', len(rows))}",
        f"- Ready for MTC_V2 review: {summary.get('ready_for_review', 0)}",
        f"- Needs forward evidence: {summary.get('needs_forward_evidence', 0)}",
        f"- Needs PineTS parity: {summary.get('needs_pinets_parity', 0)}",
        f"- Blocked or parked: {summary.get('blocked_or_parked', 0)}",
        "",
        "## Buckets",
        "",
    ]
    for status, count in sorted(counts.items()):
        lines.append(f"- `{status}`: {count}")
    lines.extend(
        [
            "",
            "## Leading Queue",
            "",
            "| Stg | Strategy | Score | Bucket | Forward | Decision |",
            "|---|---|---:|---|---|---|",
        ]
    )
    for row in leading:
        forward = row.get("forward_progress") or {}
        lines.append(
            "| {stg} | `{sid}` | {score} | {status} | {forward} | {decision} |".format(
                stg=_cell(row.get("stg_code") or ""),
                sid=_cell(row.get("id") or ""),
                score=int(row.get("score") or 0),
                status=_cell(row.get("status") or ""),
                forward=_cell(forward.get("label") or ""),
                decision=_cell(row.get("decision_sentence") or ""),
            )
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def _cell(value: str) -> str:
    return str(value).replace("|", "/").replace("\n", " ").strip()


if __name__ == "__main__":
    raise SystemExit(main())
