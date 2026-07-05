"""Three-ledger reconciliation for local SYSTEM_TEST_ONLY vertical-slice runs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .constants import BANNER, CANDIDATE_ID


def reconcile_ledgers(
    *,
    expected_signals: list[dict[str, Any]],
    received_rows: list[dict[str, Any]],
    fills: list[dict[str, Any]],
) -> dict[str, Any]:
    expected_ids = {row["signal_id"] for row in expected_signals if row.get("signal_id")}
    received_ids = {row["signal_id"] for row in received_rows if row.get("signal_id")}
    filled_ids = {row["signal_id"] for row in fills if row.get("signal_id")}

    accepted_received_ids = {
        row["signal_id"]
        for row in received_rows
        if row.get("signal_id") and row.get("disposition") == "accepted"
    }
    explained_rejections = sum(
        1 for row in received_rows if str(row.get("disposition", "")).startswith("rejected(")
    )

    expected_not_received = sorted(expected_ids - received_ids)
    received_not_expected = sorted(accepted_received_ids - expected_ids)
    received_not_filled = sorted(accepted_received_ids - filled_ids)
    unexplained = (
        len(expected_not_received)
        + len(received_not_expected)
        + len(received_not_filled)
    )

    return {
        "banner": BANNER,
        "candidate_id": CANDIDATE_ID,
        "status": "HALT" if unexplained else "OK",
        "expected_count": len(expected_signals),
        "received_count": len(received_rows),
        "filled_count": len(fills),
        "duplicates_dropped": sum(
            1 for row in received_rows if row.get("disposition") == "duplicate_dropped"
        ),
        "rejected_count": sum(
            1 for row in received_rows if str(row.get("disposition", "")).startswith("rejected(")
        ),
        "explained_rejections": explained_rejections,
        "expected_not_received": expected_not_received,
        "received_not_expected": received_not_expected,
        "received_not_filled": received_not_filled,
        "unexplained_count": unexplained,
    }


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def reconcile_run_directory(run_dir: str | Path) -> dict[str, Any]:
    root = Path(run_dir)
    return reconcile_ledgers(
        expected_signals=_read_jsonl(root / "expected_signals.jsonl"),
        received_rows=_read_jsonl(root / "received_signals.jsonl"),
        fills=_read_jsonl(root / "simulated_fills.jsonl"),
    )


def write_reconciliation_summary(run_dir: str | Path, summary: dict[str, Any]) -> Path:
    path = Path(run_dir) / "reconciliation_summary.json"
    path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_reconciliation_report(run_dir: str | Path, summary: dict[str, Any]) -> Path:
    path = Path(run_dir) / "reconciliation_report.md"
    lines = [
        "# SYSTEM_TEST_ONLY Reconciliation Report",
        "",
        BANNER,
        "",
        f"- Status: {summary.get('status')}",
        f"- Unexplained count: {summary.get('unexplained_count')}",
        f"- Explained rejections: {summary.get('explained_rejections', 0)}",
        f"- EXPECTED-not-RECEIVED: {summary.get('expected_not_received', [])}",
        f"- RECEIVED-not-EXPECTED: {summary.get('received_not_expected', [])}",
        f"- RECEIVED-not-FILLED: {summary.get('received_not_filled', [])}",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    write_reconciliation_summary(run_dir, summary)
    return path
