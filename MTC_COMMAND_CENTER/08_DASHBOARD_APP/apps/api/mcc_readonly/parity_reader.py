from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .paths import canonicalize, default_mcc_root, load_path_config, resolve_configured_path


def build_parity_status(mcc_root: str | Path | None = None) -> dict[str, Any]:
    root = canonicalize(mcc_root or default_mcc_root())
    path_config = load_path_config(root)
    pinets_root = resolve_configured_path(path_config.config, "pinets_root")
    if pinets_root is None:
        return _empty_status("pinets_root_not_configured")

    candidates = [
        pinets_root / "_nightly" / "parity_results.json",
        pinets_root / "parity_results.json",
    ]
    existing = [path for path in candidates if path.exists() and path.is_file()]
    if not existing:
        return _empty_status("parity_results_missing")

    source_path = max(existing, key=lambda item: item.stat().st_mtime)
    try:
        raw = json.loads(source_path.read_text(encoding="utf-8"))
    except Exception as exc:
        status = _empty_status("parity_results_error")
        status["warnings"] = [str(exc)]
        return status

    if isinstance(raw, dict) and isinstance(raw.get("rows"), list):
        return _from_manual_summary(raw, source_path)
    if isinstance(raw, list):
        return _from_nightly_results(raw, source_path)

    status = _empty_status("parity_results_unknown_shape")
    status["source"] = str(source_path)
    return status


def _from_manual_summary(raw: dict[str, Any], source_path: Path) -> dict[str, Any]:
    rows = raw.get("rows", [])
    failed = [row for row in rows if row.get("parity_classification") == "FAIL"]
    needs_export = raw.get("summary", {}).get("cases_missing", 0)
    cases = [_manual_case(row) for row in rows]
    summary = {
        "total_cases": len(rows),
        "runnable_cases": len(rows),
        "python_pass": _count_true(rows, "pine_vs_python_strict"),
        "pinets_pass": _count_true(rows, "tw_vs_pine_strict"),
        "tradingview_pass": _count_true(rows, "tw_vs_python_strict"),
        "overall_pass": len(rows) - len(failed),
        "failed": len(failed),
        "needs_user_export": needs_export,
        "strict_pass": sum(1 for row in rows if row.get("parity_classification") == "STRICT_PASS"),
        "soft_pass": sum(1 for row in rows if row.get("parity_classification") == "SOFT_PASS"),
    }
    return {
        "schema_version": "1.0",
        "generated_at": raw.get("timestamp"),
        "source": str(source_path),
        "summary": summary,
        "cases": cases,
    }


def _from_nightly_results(raw: list[dict[str, Any]], source_path: Path) -> dict[str, Any]:
    cases = [_nightly_case(row) for row in raw]
    failed = [case for case in cases if case.get("overall_status") in {"FAIL", "MISMATCH"}]
    partial = [case for case in cases if case.get("overall_status") == "PARTIAL"]
    summary = {
        "total_cases": len(cases),
        "runnable_cases": len(cases),
        "python_pass": sum(1 for case in cases if case.get("python_status") == "OK"),
        "pinets_pass": 0,
        "tradingview_pass": sum(1 for case in cases if case.get("tradingview_status") == "OK"),
        "overall_pass": sum(1 for case in cases if case.get("overall_status") == "PASS"),
        "failed": len(failed),
        "partial": len(partial),
        "needs_user_export": 0,
    }
    return {
        "schema_version": "1.0",
        "generated_at": None,
        "source": str(source_path),
        "summary": summary,
        "cases": cases,
    }


def _manual_case(row: dict[str, Any]) -> dict[str, Any]:
    classification = row.get("parity_classification")
    return {
        "case_id": row.get("case"),
        "title": row.get("title"),
        "description": row.get("description"),
        "overall_status": classification,
        "overall_pass": classification in {"STRICT_PASS", "SOFT_PASS"},
        "tw_vs_pine_strict": row.get("tw_vs_pine_strict"),
        "tw_vs_python_strict": row.get("tw_vs_python_strict"),
        "pine_vs_python_strict": row.get("pine_vs_python_strict"),
        "tw_trades": row.get("tw_trades"),
        "pine_trades": row.get("pine_trades"),
        "python_trades": row.get("python_trades"),
        "report_json": row.get("report_json"),
        "first_mismatch": row.get("tw_first_mismatch"),
    }


def _nightly_case(row: dict[str, Any]) -> dict[str, Any]:
    compare = row.get("compare") or {}
    python = row.get("python") or {}
    tv_collect = row.get("tv_collect") or {}
    status = compare.get("status") or row.get("status")
    return {
        "case_id": row.get("case_no"),
        "title": str(row.get("case_no")),
        "description": compare.get("note"),
        "overall_status": status,
        "overall_pass": status == "PASS",
        "python_status": python.get("status"),
        "tradingview_status": tv_collect.get("status"),
        "started_at": row.get("started_at"),
    }


def _count_true(rows: list[dict[str, Any]], key: str) -> int:
    return sum(1 for row in rows if row.get(key) is True)


def _empty_status(source: str) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "generated_at": None,
        "source": source,
        "summary": {
            "total_cases": 0,
            "runnable_cases": 0,
            "python_pass": 0,
            "pinets_pass": 0,
            "tradingview_pass": 0,
            "overall_pass": 0,
            "failed": 0,
            "needs_user_export": 0,
        },
        "cases": [],
    }
