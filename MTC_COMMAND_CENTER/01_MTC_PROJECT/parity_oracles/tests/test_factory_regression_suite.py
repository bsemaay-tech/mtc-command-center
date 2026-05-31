from __future__ import annotations

import json
from pathlib import Path

from parity_oracles.run_factory_regression_suite import (
    ALLOWED_STATUSES,
    build_case_result,
    build_inventory,
    select_suite_cases,
    write_suite_outputs,
)


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _repo_fixture(root: Path) -> None:
    _write_json(
        root / "05_PARITY/MTC_V2_TW_EXPORT_CASE_SUITE_V2.json",
        {
            "cases": [
                {
                    "case_name": "case_001",
                    "status": "READY",
                    "title": "Baseline",
                    "export_file": "baseline.xlsx",
                    "planned_overrides": {"signal_mode": "Supertrend", "sl_mode": "None", "tp_mode": "None"},
                },
                {
                    "case_name": "case_010",
                    "status": "READY",
                    "title": "use_ma_filter",
                    "export_file": "ma.xlsx",
                    "planned_overrides": {"signal_mode": "Supertrend", "use_ma_filter": True},
                },
                {
                    "case_name": "case_020",
                    "status": "PLANNED",
                    "title": "tp_mode",
                    "export_file": "",
                    "planned_overrides": {"signal_mode": "Supertrend", "tp_mode": "ATR"},
                },
            ]
        },
    )
    _write_json(
        root / "05_PARITY/parity_results.json",
        {"rows": [{"case": "case_010", "parity_classification": "SOFT_PASS"}]},
    )
    _write_json(root / "05_PARITY/TW_EXPORT_CASES_V2/case_001/case_plan.json", {"planned_overrides": {"signal_mode": "Supertrend"}})
    _write_json(root / "05_PARITY/TW_EXPORT_CASES_V2/case_010/case_plan.json", {"planned_overrides": {"signal_mode": "Supertrend", "use_ma_filter": True}})
    _write_json(root / "05_PARITY/TW_EXPORT_CASES_V2/case_020/case_plan.json", {"planned_overrides": {"signal_mode": "Supertrend", "tp_mode": "ATR"}})
    (root / "05_PARITY/TW_EXPORT_CASES_V2/case_001/baseline.xlsx").write_text("fake", encoding="utf-8")
    (root / "05_PARITY/TW_EXPORT_CASES_V2/case_010/ma.xlsx").write_text("fake", encoding="utf-8")
    _write_json(root / "cases/fast_suite_case_001.json", {"case_id": "case_001", "mtc_config": {"source": "05_PARITY/TW_EXPORT_CASES_V2/case_001/case_plan.json"}})
    _write_json(root / "cases/fast_suite_case_001_range_filter.json", {"case_id": "case_001_range_filter", "planned_overrides": {"signal_mode": "Range Filter"}})


def test_inventory_classifies_factory_and_missing_export_surfaces(tmp_path: Path) -> None:
    _repo_fixture(tmp_path)

    inventory = build_inventory(tmp_path)
    by_case = {item["case_id"]: item for item in inventory["cases"]}

    assert by_case["case_001"]["case_plan_exists"] == "yes"
    assert by_case["case_001"]["xlsx_export_exists"] == "yes"
    assert by_case["case_001"]["expected_feature_family"] == "producer_supertrend_current"
    assert by_case["case_001"]["can_run_factory_l0_l3"] == "yes"
    assert by_case["case_001_range_filter"]["has_reference_oracle"] == "yes"
    assert by_case["case_020"]["xlsx_export_exists"] == "no"
    assert by_case["case_020"]["can_run_factory_l0_l3"] == "no"


def test_fast_suite_keeps_missing_export_as_classification_only(tmp_path: Path) -> None:
    _repo_fixture(tmp_path)
    inventory = build_inventory(tmp_path)

    selected = select_suite_cases(inventory, "fast")
    selected_ids = [item["case_id"] for item in selected]

    assert "case_001" in selected_ids
    assert "case_001_range_filter" in selected_ids
    assert "case_020" in selected_ids
    assert selected[-1]["can_run_factory_l0_l3"] == "no"


def test_dry_run_writes_schema_shaped_case_and_suite_outputs(tmp_path: Path) -> None:
    _repo_fixture(tmp_path)
    inventory = build_inventory(tmp_path)
    case = next(item for item in inventory["cases"] if item["case_id"] == "case_020")

    result = build_case_result(tmp_path, case, tmp_path / "reports", dry_run=True)
    assert result["status"] in ALLOWED_STATUSES
    assert result["status"] == "MISSING_EXPORT"
    assert set(result["levels"]) == {"L0", "L1", "L2", "L3", "L4", "L5", "L6"}
    assert result["tradingview_export_status"] == "MISSING_EXPORT"

    summary = write_suite_outputs(tmp_path / "reports", "fast", [result], dry_run=True)
    assert summary["case_count"] == 1
    assert (tmp_path / "reports/FAST_FACTORY_SUITE_REPORT.json").exists()
    assert (tmp_path / "reports/FAST_FACTORY_SUITE_REPORT.md").exists()


def test_internal_fail_count_surfaces_hidden_lifecycle_failures(tmp_path: Path) -> None:
    """internal_fail_count must be non-zero when python_lifecycle_status==FAIL even if
    top-level status is NOT_COMPARABLE, and full_suite_safe_to_run_next must be False."""
    # Build three synthetic results: one clean, one NOT_COMPARABLE with a hidden lifecycle FAIL.
    results_clean = [
        {
            "case_id": "case_001",
            "status": "PASS",
            "python_lifecycle_status": "PASS",
            "reference_oracle_status": "ORACLE_UNAVAILABLE",
            "first_divergence": None,
        },
    ]
    results_hidden_fail = [
        {
            "case_id": "case_074",
            "status": "NOT_COMPARABLE",
            "python_lifecycle_status": "FAIL",
            "reference_oracle_status": "ORACLE_UNAVAILABLE",
            "first_divergence": None,
        },
    ]

    summary_clean = write_suite_outputs(tmp_path / "clean", "fast", results_clean)
    assert summary_clean["internal_fail_count"] == 0
    assert summary_clean["no_internal_failures"] is True
    assert summary_clean["full_suite_safe_to_run_next"] is True

    summary_fail = write_suite_outputs(tmp_path / "fail", "fast", results_hidden_fail)
    assert summary_fail["internal_fail_count"] == 1
    assert summary_fail["no_internal_failures"] is False
    # Hidden internal failure must block full suite safety even though fail_count==0
    assert summary_fail["fail_count"] == 0
    assert summary_fail["full_suite_safe_to_run_next"] is False

    # Verify the JSON report also carries the new fields
    report_json = json.loads((tmp_path / "fail/FAST_FACTORY_SUITE_REPORT.json").read_text(encoding="utf-8"))
    assert report_json["internal_fail_count"] == 1
    assert report_json["no_internal_failures"] is False
