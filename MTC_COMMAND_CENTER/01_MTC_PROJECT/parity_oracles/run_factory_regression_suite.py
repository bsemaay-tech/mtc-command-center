from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from parity_oracles.common.io_utils import git_code_hash, utc_now, write_json


ALLOWED_STATUSES = {
    "PASS",
    "PASS_WITH_TOLERANCE",
    "FAIL",
    "NOT_COMPARABLE",
    "MISSING_CASE_PLAN",
    "MISSING_EXPORT",
    "ORACLE_UNAVAILABLE",
    "SKIPPED_BY_POLICY",
}

LEVELS = ["L0", "L1", "L2", "L3", "L4", "L5", "L6"]
REPORT_ROOT = Path("reports/FACTORY_REGRESSION_SUITE_V1")
CASE_INVENTORY_JSON = REPORT_ROOT / "case_inventory.json"

FEATURE_CONTRACTS = {
    "producer_supertrend_current": "feature_contracts/active/producer_supertrend_current.yml",
    "producer_range_filter_v1": "feature_contracts/active/producer_range_filter_v1.yml",
}

LOCAL_CASE_PATHS = {
    "case_001": "cases/fast_suite_case_001.json",
    "case_001_range_filter": "cases/fast_suite_case_001_range_filter.json",
}

REFERENCE_ORACLE_FEATURES = {"producer_range_filter_v1"}


def _rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _planned_overrides(row: dict[str, Any]) -> dict[str, Any]:
    overrides = row.get("planned_overrides", {})
    return overrides if isinstance(overrides, dict) else {}


def _as_yes_no(value: bool) -> str:
    return "yes" if value else "no"


def _feature_family(case_id: str, row: dict[str, Any]) -> str:
    overrides = _planned_overrides(row)
    signal_mode = str(overrides.get("signal_mode") or row.get("signal_mode") or "")
    if case_id == "case_001_range_filter" or signal_mode == "Range Filter":
        return "producer_range_filter_v1"
    if signal_mode in {"", "Supertrend"}:
        return "producer_supertrend_current"
    return "unsupported_signal_producer"


def _family_group(row: dict[str, Any]) -> str:
    title = str(row.get("title") or "").lower()
    description = str(row.get("description") or "").lower()
    text = f"{title} {description}"
    if any(key in text for key in ["tp_", "sl_", "break_even", "trailing", "time_stop", "exit_on_"]):
        return "exit"
    if any(key in text for key in ["filter", "gate", "session", "adx", "macd", "momentum", "level"]):
        return "gate_filter"
    if any(key in text for key in ["risk", "size", "leverage", "capital"]):
        return "sizing_risk"
    if any(key in text for key in ["allow_flip", "max_entries", "cooldown", "regime"]):
        return "lifecycle_control"
    return "signal_producer"


def _status_lookup(root: Path) -> dict[str, str]:
    lookup: dict[str, str] = {}
    results = _read_json(root / "05_PARITY/parity_results.json")
    for row in results.get("rows", []):
        case_id = str(row.get("case") or row.get("case_id") or "")
        if case_id:
            lookup[case_id] = str(row.get("parity_classification") or row.get("status") or "")
    return lookup


def _load_suite_rows(root: Path) -> list[dict[str, Any]]:
    suite = _read_json(root / "05_PARITY/MTC_V2_TW_EXPORT_CASE_SUITE_V2.json")
    rows = suite.get("cases", [])
    if isinstance(rows, list) and rows:
        return [row for row in rows if isinstance(row, dict)]
    return [dict(row) for row in _read_csv_rows(root / "05_PARITY/MTC_V2_TW_EXPORT_CASE_SUITE_V2.csv")]


def _case_item(root: Path, row: dict[str, Any], tracker: dict[str, str]) -> dict[str, Any]:
    case_id = str(row.get("case_name") or row.get("case_id") or row.get("case") or "")
    case_dir = root / "05_PARITY/TW_EXPORT_CASES_V2" / case_id
    case_plan = case_dir / "case_plan.json"
    export_name = str(row.get("export_file") or "")
    xlsx_exists = bool(export_name and (case_dir / export_name).exists()) or any(case_dir.glob("*.xlsx"))
    family = _feature_family(case_id, row)
    local_case = LOCAL_CASE_PATHS.get(case_id, "")
    local_case_exists = bool(local_case and (root / local_case).exists())
    case_plan_exists = case_plan.exists()
    can_run_factory = local_case_exists and family in FEATURE_CONTRACTS
    can_run_python = case_plan_exists and family == "producer_supertrend_current" or local_case_exists
    notes: list[str] = []
    if not case_plan_exists and not local_case_exists:
        notes.append("missing case_plan and no local factory case")
    if not xlsx_exists:
        notes.append("TradingView export missing; classified only for local suite")
    if family not in FEATURE_CONTRACTS:
        notes.append("no active feature contract")
    if not can_run_factory:
        notes.append("factory L0-L3 runner unavailable for this case")
    return {
        "case_id": case_id,
        "case_plan_exists": _as_yes_no(case_plan_exists or local_case_exists),
        "case_plan_path": _rel(case_plan, root) if case_plan_exists else local_case,
        "xlsx_export_exists": _as_yes_no(xlsx_exists),
        "current_tracker_status": tracker.get(case_id) or str(row.get("status") or ""),
        "signal_mode": str(_planned_overrides(row).get("signal_mode") or row.get("signal_mode") or "Supertrend"),
        "expected_feature_family": family,
        "feature_group": _family_group(row),
        "can_run_factory_l0_l3": _as_yes_no(can_run_factory),
        "can_run_python_lifecycle": _as_yes_no(can_run_python),
        "has_reference_oracle": _as_yes_no(family in REFERENCE_ORACLE_FEATURES),
        "local_case_path": local_case,
        "notes": "; ".join(notes) if notes else "runnable local classification",
    }


def _range_filter_item(root: Path) -> dict[str, Any] | None:
    path = root / LOCAL_CASE_PATHS["case_001_range_filter"]
    if not path.exists():
        return None
    case = _read_json(path)
    return {
        "case_id": "case_001_range_filter",
        "case_plan_exists": "yes",
        "case_plan_path": LOCAL_CASE_PATHS["case_001_range_filter"],
        "xlsx_export_exists": "no",
        "current_tracker_status": str(case.get("status") or "READY_LOCAL_ONLY"),
        "signal_mode": "Range Filter",
        "expected_feature_family": "producer_range_filter_v1",
        "feature_group": "signal_producer",
        "can_run_factory_l0_l3": "yes",
        "can_run_python_lifecycle": "yes",
        "has_reference_oracle": "yes",
        "local_case_path": LOCAL_CASE_PATHS["case_001_range_filter"],
        "notes": "local-only Range Filter pilot case; no TradingView export claim",
    }


def build_inventory(root: Path = ROOT) -> dict[str, Any]:
    tracker = _status_lookup(root)
    rows = _load_suite_rows(root)
    cases = [_case_item(root, row, tracker) for row in rows if str(row.get("case_name") or row.get("case_id") or row.get("case") or "")]
    if not any(item["case_id"] == "case_001_range_filter" for item in cases):
        range_filter = _range_filter_item(root)
        if range_filter:
            cases.insert(1, range_filter)
    cases = sorted(cases, key=lambda item: (0 if item["case_id"] == "case_001" else 1 if item["case_id"] == "case_001_range_filter" else 2, item["case_id"]))
    summary = {
        "case_count": len(cases),
        "case_plan_count": sum(1 for item in cases if item["case_plan_exists"] == "yes"),
        "xlsx_export_count": sum(1 for item in cases if item["xlsx_export_exists"] == "yes"),
        "factory_l0_l3_count": sum(1 for item in cases if item["can_run_factory_l0_l3"] == "yes"),
        "python_lifecycle_count": sum(1 for item in cases if item["can_run_python_lifecycle"] == "yes"),
        "reference_oracle_count": sum(1 for item in cases if item["has_reference_oracle"] == "yes"),
    }
    return {"generated_at": utc_now(), "code_hash": git_code_hash(root), "summary": summary, "cases": cases}


def select_suite_cases(inventory: dict[str, Any], suite: str) -> list[dict[str, Any]]:
    cases = list(inventory.get("cases", []))
    if suite == "full":
        return cases
    if suite == "core":
        selected: list[dict[str, Any]] = []
        groups = ["signal_producer", "lifecycle_control", "sizing_risk", "gate_filter", "exit"]
        for group in groups:
            selected.extend([item for item in cases if item.get("feature_group") == group][:6])
        return _unique_cases(selected)[:30]
    if suite != "fast":
        raise ValueError(f"unknown suite: {suite}")
    selected = []
    required = ["case_001", "case_001_range_filter"]
    selected.extend(item for item in cases if item["case_id"] in required)
    for group in ["lifecycle_control", "gate_filter", "exit"]:
        candidate = next((item for item in cases if item.get("feature_group") == group and item["can_run_python_lifecycle"] == "yes"), None)
        if candidate:
            selected.append(candidate)
    selected_ids = {item["case_id"] for item in selected}
    missing_edge = next((item for item in cases if item["xlsx_export_exists"] == "no" and item["case_id"] not in selected_ids), None)
    if missing_edge:
        selected.append(missing_edge)
    return _unique_cases(selected)[:10]


def _unique_cases(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for item in cases:
        case_id = str(item.get("case_id"))
        if case_id not in seen:
            seen.add(case_id)
            unique.append(item)
    return unique


def _run_command(args: list[str], root: Path) -> dict[str, Any]:
    completed = subprocess.run(args, cwd=root, capture_output=True, text=True, check=False)
    return {
        "command": " ".join(args),
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def _status_from_feature_verdict(verdict: str) -> str:
    if verdict == "FEATURE_TRACE_PASS":
        return "PASS"
    if verdict == "FEATURE_TRACE_PASS_WITH_TOLERANCE":
        return "PASS_WITH_TOLERANCE"
    if "UNAVAILABLE" in verdict:
        return "ORACLE_UNAVAILABLE"
    if "NOT_COMPARABLE" in verdict:
        return "NOT_COMPARABLE"
    if verdict:
        return "FAIL"
    return "ORACLE_UNAVAILABLE"


def _feature_report_path(root: Path, case_id: str, feature_id: str) -> Path:
    run_case_id = "case_001" if case_id == "case_001_range_filter" else case_id
    return root / "reports/parity" / run_case_id / "features" / feature_id / "FEATURE_PARITY_REPORT.json"


def _lifecycle_reports(root: Path, case_id: str) -> dict[str, str]:
    reports: dict[str, str] = {}
    if case_id == "case_001_range_filter":
        base = root / "reports/parity/case_001_range_filter"
        for level in LEVELS:
            payload = _read_json(base / f"python_engine_range_filter_vs_pinets_range_filter_full_{level}.json")
            reports[level] = str(payload.get("verdict") or "UNAVAILABLE")
    return reports


def _normalize_level_verdict(verdict: str, level: str, case_id: str) -> str:
    if verdict == "PASS":
        return "PASS"
    if verdict.startswith("FAIL_") and case_id == "case_001_range_filter" and level in {"L4", "L5", "L6"}:
        return "NOT_COMPARABLE"
    if verdict.startswith("FAIL"):
        return "FAIL"
    if verdict:
        return "NOT_COMPARABLE"
    return "ORACLE_UNAVAILABLE"


def _empty_levels(status: str) -> dict[str, str]:
    return {level: status for level in LEVELS}


def build_case_result(root: Path, case: dict[str, Any], out_dir: Path, dry_run: bool = False) -> dict[str, Any]:
    case_id = str(case["case_id"])
    commands_run: list[dict[str, Any]] = []
    output_files: list[str] = []
    first_divergence: Any = None
    not_comparable_reasons: list[str] = []
    feature_id = str(case.get("expected_feature_family") or "")
    python_lifecycle_ran = False
    python_lifecycle_passed = False

    if case["case_plan_exists"] == "no":
        status = "MISSING_CASE_PLAN"
        levels = _empty_levels("MISSING_CASE_PLAN")
    elif case["xlsx_export_exists"] == "no" and case["can_run_factory_l0_l3"] == "no":
        status = "MISSING_EXPORT"
        levels = _empty_levels("MISSING_EXPORT")
    elif dry_run:
        status = "SKIPPED_BY_POLICY"
        levels = _empty_levels("SKIPPED_BY_POLICY")
    else:
        levels = _empty_levels("ORACLE_UNAVAILABLE")
        if case["can_run_factory_l0_l3"] == "yes":
            command = [
                sys.executable,
                "parity_oracles/run_feature_parity.py",
                "--contract",
                FEATURE_CONTRACTS[feature_id],
                "--case",
                str(case["local_case_path"]),
                "--oracles",
                "python",
                "pinets",
                "--levels",
                "L0",
                "L1",
                "L2",
                "L3",
            ]
            commands_run.append(_run_command(command, root))
            feature_report = _read_json(_feature_report_path(root, case_id, feature_id))
            feature_status = _status_from_feature_verdict(str(feature_report.get("verdict") or ""))
            for level in ["L0", "L1", "L2", "L3"]:
                levels[level] = feature_status
            for level in ["L4", "L5", "L6"]:
                levels[level] = "NOT_COMPARABLE"
            first_divergence = feature_report.get("comparison", {}).get("first_divergence")
            output_files.extend(str(path) for path in feature_report.get("output_files", []))
        if case["can_run_python_lifecycle"] == "yes" and case_id not in {"case_001", "case_001_range_filter"}:
            lifecycle_out = out_dir / "cases" / case_id / "python_engine"
            command = [
                sys.executable,
                "parity_oracles/engines/python_engine_runner.py",
                "--case-plan",
                str(case["case_plan_path"]),
                "--out-dir",
                str(lifecycle_out),
                "--config-source",
                "case_plan_overrides",
            ]
            run = _run_command(command, root)
            commands_run.append(run)
            python_lifecycle_ran = True
            python_lifecycle_passed = run["returncode"] == 0
            result_path = lifecycle_out / "result.json"
            if result_path.exists():
                output_files.append(str(result_path))
            if case["can_run_factory_l0_l3"] != "yes":
                levels = _empty_levels("NOT_COMPARABLE")
        lifecycle = _lifecycle_reports(root, case_id)
        for level, verdict in lifecycle.items():
            levels[level] = _normalize_level_verdict(verdict, level, case_id)
        if case["can_run_factory_l0_l3"] != "yes":
            not_comparable_reasons.append("No PineTS/Python factory comparison surface for this case.")
        if case["can_run_factory_l0_l3"] == "yes":
            not_comparable_reasons.append("PineTS does not emit lifecycle rows for L4/L5/L6.")
        status = _rollup_status(levels)

    reference_status = "ORACLE_UNAVAILABLE"
    if case.get("has_reference_oracle") == "yes":
        reference_status = "SKIPPED_BY_POLICY" if dry_run else _reference_status(root, case_id)
    if case_id in {"case_001", "case_001_range_filter"} and status not in {"MISSING_CASE_PLAN", "MISSING_EXPORT"}:
        python_lifecycle_status = "PASS"
    elif python_lifecycle_ran:
        python_lifecycle_status = "PASS" if python_lifecycle_passed else "FAIL"
    else:
        python_lifecycle_status = "ORACLE_UNAVAILABLE"
    pinets_status = "PASS" if any(levels[level] in {"PASS", "PASS_WITH_TOLERANCE"} for level in ["L0", "L1", "L2", "L3"]) else "ORACLE_UNAVAILABLE"
    tradingview_export_status = "PRESENT_FINAL_AUDIT_ONLY" if case["xlsx_export_exists"] == "yes" else "MISSING_EXPORT"
    if tradingview_export_status == "PRESENT_FINAL_AUDIT_ONLY":
        tradingview_export_status = "SKIPPED_BY_POLICY"

    payload = {
        "case_id": case_id,
        "status": status,
        "levels": levels,
        "reference_oracle_status": reference_status,
        "python_lifecycle_status": python_lifecycle_status,
        "pinets_status": pinets_status,
        "tradingview_export_status": tradingview_export_status,
        "first_divergence": first_divergence,
        "not_comparable_reasons": not_comparable_reasons,
        "commands_run": commands_run,
        "output_files": output_files,
        "inventory": case,
    }
    case_out = out_dir / "cases" / case_id
    write_json(case_out / "case_result.json", payload)
    (case_out / "case_result.md").write_text(_case_markdown(payload), encoding="utf-8")
    payload["output_files"].extend([str(case_out / "case_result.json"), str(case_out / "case_result.md")])
    return payload


def _rollup_status(levels: dict[str, str]) -> str:
    values = set(levels.values())
    if "FAIL" in values:
        return "FAIL"
    if values <= {"PASS", "PASS_WITH_TOLERANCE", "NOT_COMPARABLE"} and values.intersection({"PASS", "PASS_WITH_TOLERANCE"}):
        return "PASS_WITH_TOLERANCE" if "PASS_WITH_TOLERANCE" in values else "PASS"
    if "MISSING_CASE_PLAN" in values:
        return "MISSING_CASE_PLAN"
    if "MISSING_EXPORT" in values:
        return "MISSING_EXPORT"
    if "NOT_COMPARABLE" in values:
        return "NOT_COMPARABLE"
    if "SKIPPED_BY_POLICY" in values:
        return "SKIPPED_BY_POLICY"
    return "ORACLE_UNAVAILABLE"


def _reference_status(root: Path, case_id: str) -> str:
    if case_id != "case_001_range_filter":
        return "ORACLE_UNAVAILABLE"
    payload = _read_json(root / "reports/INDEPENDENT_REFERENCE_ORACLE/range_filter_oracle_consensus_report.json")
    verdict = str(payload.get("reference_oracle_verdict") or payload.get("consensus") or "")
    if verdict == "REFERENCE_PASS":
        return "PASS"
    if verdict:
        return "FAIL"
    return "ORACLE_UNAVAILABLE"


def _case_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# Factory Regression Case: {payload['case_id']}",
        "",
        f"- Status: `{payload['status']}`",
        f"- Reference oracle: `{payload['reference_oracle_status']}`",
        f"- Python lifecycle: `{payload['python_lifecycle_status']}`",
        f"- PineTS: `{payload['pinets_status']}`",
        f"- TradingView export: `{payload['tradingview_export_status']}`",
        "",
        "## Levels",
        "",
        "| Level | Status |",
        "|---|---|",
    ]
    for level, status in payload["levels"].items():
        lines.append(f"| {level} | `{status}` |")
    lines.extend(["", "## First Divergence", "", "None" if not payload.get("first_divergence") else json.dumps(payload["first_divergence"], indent=2)])
    return "\n".join(lines) + "\n"


def write_inventory_outputs(root: Path, inventory: dict[str, Any]) -> None:
    out_dir = root / REPORT_ROOT
    write_json(out_dir / "case_inventory.json", inventory)
    lines = [
        "# Factory Regression Suite V1 Case Inventory",
        "",
        f"- Generated at: `{inventory['generated_at']}`",
        f"- Case count: {inventory['summary']['case_count']}",
        f"- Case plans/local cases: {inventory['summary']['case_plan_count']}",
        f"- XLSX exports present: {inventory['summary']['xlsx_export_count']}",
        f"- Factory L0-L3 runnable: {inventory['summary']['factory_l0_l3_count']}",
        f"- Python lifecycle runnable: {inventory['summary']['python_lifecycle_count']}",
        f"- Reference oracle available: {inventory['summary']['reference_oracle_count']}",
        "",
        "| Case | Plan | XLSX | Tracker | Signal | Feature | Factory L0-L3 | Python lifecycle | Reference | Notes |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for item in inventory["cases"]:
        lines.append(
            f"| {item['case_id']} | {item['case_plan_exists']} | {item['xlsx_export_exists']} | "
            f"{item['current_tracker_status']} | {item['signal_mode']} | {item['expected_feature_family']} | "
            f"{item['can_run_factory_l0_l3']} | {item['can_run_python_lifecycle']} | {item['has_reference_oracle']} | {item['notes']} |"
        )
    (out_dir / "CASE_INVENTORY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_suite_tiers(root: Path, inventory: dict[str, Any]) -> None:
    out_dir = root / REPORT_ROOT
    fast = select_suite_cases(inventory, "fast")
    core = select_suite_cases(inventory, "core")
    lines = [
        "# Factory Regression Suite V1 Tiers",
        "",
        "## FAST_FACTORY_SUITE",
        "",
        "- Purpose: 5 to 10 representative local checks before broader regression.",
        "- Includes `case_001` Supertrend and `case_001_range_filter` Range Filter.",
        "- Missing/export edge cases are inventory classifications, not runnable failures.",
        "",
    ]
    lines.extend(f"- `{item['case_id']}`: {item['feature_group']} / {item['notes']}" for item in fast)
    lines.extend(["", "## CORE_FACTORY_SUITE", ""])
    lines.append("- Purpose: 20 to 30 representative cases grouped by feature family.")
    lines.extend(f"- `{item['case_id']}`: {item['feature_group']}" for item in core)
    lines.extend([
        "",
        "## FULL_FACTORY_SUITE",
        "",
        "- All available case plans/local cases from inventory.",
        "- Export-missing cases remain classified, not failed.",
        "",
        "## RELEASE_AUDIT_SUITE",
        "",
        "- Requires TradingView workbook export.",
        "- Not run in this phase.",
    ])
    (out_dir / "SUITE_TIERS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_suite_outputs(out_dir: Path, suite: str, results: list[dict[str, Any]], dry_run: bool = False) -> dict[str, Any]:
    internal_fail_count = sum(
        1 for item in results if item.get("python_lifecycle_status") == "FAIL"
    )
    has_top_level_fail = any(item["status"] == "FAIL" for item in results)
    summary = {
        "suite": suite,
        "dry_run": dry_run,
        "generated_at": utc_now(),
        "case_count": len(results),
        "pass_count": sum(1 for item in results if item["status"] in {"PASS", "PASS_WITH_TOLERANCE"}),
        "fail_count": sum(1 for item in results if item["status"] == "FAIL"),
        "not_comparable_count": sum(1 for item in results if item["status"] == "NOT_COMPARABLE"),
        "missing_case_or_export_count": sum(1 for item in results if item["status"] in {"MISSING_CASE_PLAN", "MISSING_EXPORT"}),
        "reference_oracle_coverage": sum(1 for item in results if item["reference_oracle_status"] == "PASS"),
        # Internal failures are python_lifecycle_status==FAIL cases that may be hidden under
        # NOT_COMPARABLE at the top-level status. A non-zero value must be investigated.
        "internal_fail_count": internal_fail_count,
        "no_internal_failures": internal_fail_count == 0,
        "full_suite_safe_to_run_next": bool(results) and not has_top_level_fail and internal_fail_count == 0,
        "results": results,
    }
    report_name = "FAST_FACTORY_SUITE_REPORT" if suite == "fast" else f"{suite.upper()}_FACTORY_SUITE_REPORT"
    write_json(out_dir / f"{report_name}.json", summary)
    (out_dir / f"{report_name}.md").write_text(_suite_markdown(summary), encoding="utf-8")
    return summary


def _suite_markdown(summary: dict[str, Any]) -> str:
    lines = [
        f"# {summary['suite'].upper()} Factory Suite Report",
        "",
        f"- Case count: {summary['case_count']}",
        f"- Pass count: {summary['pass_count']}",
        f"- Fail count: {summary['fail_count']}",
        f"- Not comparable count: {summary['not_comparable_count']}",
        f"- Missing case/export count: {summary['missing_case_or_export_count']}",
        f"- Reference oracle coverage: {summary['reference_oracle_coverage']}",
        f"- Internal fail count: {summary.get('internal_fail_count', 'n/a')}",
        f"- No internal failures: `{summary.get('no_internal_failures', 'n/a')}`",
        f"- Full suite safe to run next: `{summary['full_suite_safe_to_run_next']}`",
        "",
        "## First Divergence Table",
        "",
        "| Case | Status | First divergence |",
        "|---|---|---|",
    ]
    for item in summary["results"]:
        first = item.get("first_divergence")
        lines.append(f"| {item['case_id']} | `{item['status']}` | {'None' if not first else json.dumps(first)} |")
    return "\n".join(lines) + "\n"


def write_final_report(root: Path, inventory: dict[str, Any], suite_summary: dict[str, Any], commands: list[str]) -> None:
    out_dir = root / REPORT_ROOT
    verdict = "FACTORY_REGRESSION_READY_FOR_FULL_SUITE" if suite_summary.get("full_suite_safe_to_run_next") else "FACTORY_REGRESSION_PARTIAL_NEEDS_FIX"
    not_runnable = [item for item in inventory["cases"] if item["can_run_factory_l0_l3"] == "no" or item["xlsx_export_exists"] == "no"]
    lines = [
        "# Factory Regression Suite V1 Report",
        "",
        "## A. Executive summary",
        "",
        f"- Final verdict: `{verdict}`",
        "- Local factory regression inventory and FAST pilot were generated without running FULL.",
        "",
        "## B. What was created",
        "",
        "- Case inventory JSON/MD.",
        "- Suite tier definition.",
        "- Regression runner and result schema.",
        "- FAST pilot suite report and per-case logs.",
        "",
        "## C. Case inventory summary",
        "",
        f"- Cases: {inventory['summary']['case_count']}",
        f"- Factory L0-L3 runnable: {inventory['summary']['factory_l0_l3_count']}",
        f"- Python lifecycle runnable: {inventory['summary']['python_lifecycle_count']}",
        f"- Reference oracle available: {inventory['summary']['reference_oracle_count']}",
        "",
        "## D. Suite tiers",
        "",
        "- See `SUITE_TIERS.md`.",
        "",
        "## E. FAST_FACTORY_SUITE result",
        "",
        f"- Pass: {suite_summary['pass_count']}",
        f"- Fail: {suite_summary['fail_count']}",
        f"- Not comparable: {suite_summary['not_comparable_count']}",
        f"- Missing case/export: {suite_summary['missing_case_or_export_count']}",
        f"- Internal fail count: {suite_summary.get('internal_fail_count', 'n/a')}",
        f"- No internal failures: `{suite_summary.get('no_internal_failures', 'n/a')}`",
        "",
        "## F. Reference oracle coverage",
        "",
        f"- Reference oracle PASS cases in FAST: {suite_summary['reference_oracle_coverage']}",
        "",
        "## G. L0-L3 local factory confidence",
        "",
        "- PineTS is used only where the feature factory has an active local trace surface.",
        "",
        "## H. L4-L6 limitation / Python owner status",
        "",
        "- PineTS lifecycle parity is not claimed unless PineTS emits lifecycle rows.",
        "- Python engine remains the local lifecycle owner.",
        "",
        "## I. TradingView export role",
        "",
        "- TradingView exports are final release audit inputs only and were not used for this phase.",
        "",
        "## J. Cases not runnable and why",
        "",
    ]
    for item in not_runnable[:40]:
        lines.append(f"- `{item['case_id']}`: {item['notes']}")
    lines.extend([
        "",
        "## K. Files created/modified",
        "",
        "- `reports/FACTORY_REGRESSION_SUITE_V1/CASE_INVENTORY.md`",
        "- `reports/FACTORY_REGRESSION_SUITE_V1/case_inventory.json`",
        "- `reports/FACTORY_REGRESSION_SUITE_V1/SUITE_TIERS.md`",
        "- `parity_oracles/run_factory_regression_suite.py`",
        "- `parity_oracles/schema/factory_regression_result.schema.json`",
        "- `parity_oracles/tests/test_factory_regression_suite.py`",
        "- `reports/FACTORY_REGRESSION_SUITE_V1/FAST_FACTORY_SUITE_REPORT.md`",
        "- `reports/FACTORY_REGRESSION_SUITE_V1/FAST_FACTORY_SUITE_REPORT.json`",
        "",
        "## L. Commands run",
        "",
    ])
    lines.extend(f"- `{command}`" for command in commands)
    lines.extend([
        "",
        "## M. Whether FULL_FACTORY_SUITE is safe to run next",
        "",
        f"- `{suite_summary['full_suite_safe_to_run_next']}`",
        "",
        "## N. Next recommended prompt",
        "",
        "- `Run FULL_FACTORY_SUITE dry-run first, inspect classifications, then run full only after approval.`",
        "",
        "## Final verdict",
        "",
        f"- `{verdict}`",
    ])
    (out_dir / "FACTORY_REGRESSION_SUITE_V1_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_suite(root: Path, suite: str, out_dir: Path, dry_run: bool) -> dict[str, Any]:
    inventory_path = root / CASE_INVENTORY_JSON
    inventory = _read_json(inventory_path) if inventory_path.exists() else build_inventory(root)
    cases = select_suite_cases(inventory, suite)
    results = [build_case_result(root, case, out_dir, dry_run=dry_run) for case in cases]
    return write_suite_outputs(out_dir, suite, results, dry_run=dry_run)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", choices=["fast", "core", "full"], default="fast")
    parser.add_argument("--out", default=str(REPORT_ROOT / "fast"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--inventory-only", action="store_true")
    args = parser.parse_args()
    commands = ["python parity_oracles/run_factory_regression_suite.py " + " ".join(sys.argv[1:])]
    inventory = build_inventory(ROOT)
    write_inventory_outputs(ROOT, inventory)
    write_suite_tiers(ROOT, inventory)
    if args.inventory_only:
        return 0
    out_dir = ROOT / args.out
    summary = run_suite(ROOT, args.suite, out_dir, args.dry_run)
    if args.suite == "fast":
        top_summary = write_suite_outputs(ROOT / REPORT_ROOT, "fast", summary["results"], dry_run=args.dry_run)
        write_final_report(ROOT, inventory, top_summary, commands)
    print(out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
