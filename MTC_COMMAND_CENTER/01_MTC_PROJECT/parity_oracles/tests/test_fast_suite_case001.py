from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_python_engine_runner_emits_real_case001_normalized_files(tmp_path: Path) -> None:
    out_dir = tmp_path / "python_engine"
    completed = subprocess.run(
        [
            sys.executable,
            "parity_oracles/engines/python_engine_runner.py",
            "--case-plan",
            "05_PARITY/TW_EXPORT_CASES_V2/case_001/case_plan.json",
            "--out-dir",
            str(out_dir),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr + completed.stdout
    result = json.loads((out_dir / "result.json").read_text(encoding="utf-8"))
    assert result["status"] == "success"
    assert result["output_files"]["data"].endswith("normalized_data.csv")
    assert sum(1 for _ in (out_dir / "normalized_data.csv").open(encoding="utf-8")) > 10
    assert sum(1 for _ in (out_dir / "normalized_indicators.csv").open(encoding="utf-8")) > 10
    assert sum(1 for _ in (out_dir / "normalized_signals.csv").open(encoding="utf-8")) > 10


def test_pinets_runner_records_real_case001_attempt_and_same_data(tmp_path: Path) -> None:
    out_dir = tmp_path / "pinets"
    completed = subprocess.run(
        [
            sys.executable,
            "parity_oracles/engines/pinets_runner.py",
            "--case-plan",
            "05_PARITY/TW_EXPORT_CASES_V2/case_001/case_plan.json",
            "--out-dir",
            str(out_dir),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode in {0, 2}, completed.stderr + completed.stdout
    result = json.loads((out_dir / "result.json").read_text(encoding="utf-8"))
    assert result["status"] in {"success", "failed", "engine_unavailable"}
    assert sum(1 for _ in (out_dir / "normalized_data.csv").open(encoding="utf-8")) > 10
    assert (out_dir / "pinets_raw.json").exists() or (out_dir / "pinets_error.txt").exists()


def test_supertrend_isolation_reports_first_divergence(tmp_path: Path) -> None:
    out_dir = tmp_path / "supertrend_isolation"
    completed = subprocess.run(
        [
            sys.executable,
            "parity_oracles/engines/supertrend_isolation_runner.py",
            "--case-plan",
            "05_PARITY/TW_EXPORT_CASES_V2/case_001/case_plan.json",
            "--out-dir",
            str(out_dir),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode in {0, 1}, completed.stderr + completed.stdout
    result = json.loads((out_dir / "supertrend_isolation.json").read_text(encoding="utf-8"))
    assert result["case_id"] == "case_001"
    assert result["compared_fields"] == ["supertrend_line", "direction", "long_raw", "short_raw"]
    assert "first_divergence" in result
    assert (out_dir / "supertrend_isolation.md").exists()


def test_python_engine_runner_supports_case_plan_override_config_source(tmp_path: Path) -> None:
    out_dir = tmp_path / "python_engine_case_plan"
    completed = subprocess.run(
        [
            sys.executable,
            "parity_oracles/engines/python_engine_runner.py",
            "--case-plan",
            "05_PARITY/TW_EXPORT_CASES_V2/case_001/case_plan.json",
            "--out-dir",
            str(out_dir),
            "--config-source",
            "case_plan_overrides",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr + completed.stdout
    result = json.loads((out_dir / "result.json").read_text(encoding="utf-8"))
    assert result["status"] == "success"
    assert result["config_source"] == "case_plan_overrides"
    assert result["case"]["mtc_config"]["st_atr_len"] == 21
    indicator_text = (out_dir / "normalized_indicators.csv").read_text(encoding="utf-8")
    assert "2024-12-31T16:00:00+00:00,supertrend_line" not in indicator_text
    assert "2024-12-31T23:00:00+00:00,supertrend_line,90570.140476190" in indicator_text


def test_python_engine_case_plan_mode_normalizes_supertrend_raw_pulses(tmp_path: Path) -> None:
    out_dir = tmp_path / "python_engine_case_plan"
    completed = subprocess.run(
        [
            sys.executable,
            "parity_oracles/engines/python_engine_runner.py",
            "--case-plan",
            "05_PARITY/TW_EXPORT_CASES_V2/case_001/case_plan.json",
            "--out-dir",
            str(out_dir),
            "--config-source",
            "case_plan_overrides",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr + completed.stdout
    signals = (out_dir / "normalized_signals.csv").read_text(encoding="utf-8")
    assert "2025-01-10T18:00:00+00:00,255,0,0,0,0,st_hold_long" in signals


def test_orchestrator_reports_export_and_case_plan_surfaces() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "parity_oracles/run_multi_oracle_case.py",
            "--case",
            "cases/fast_suite_case_001.json",
            "--engines",
            "python_engine",
            "pinets",
            "--baseline",
            "python_engine",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr + completed.stdout
    summary = (ROOT / "reports/parity/case_001/MULTI_ORACLE_PARITY_SUMMARY.md").read_text(encoding="utf-8")
    assert "export_workbook" in summary
    assert "case_plan_overrides" in summary
    assert "python_engine_case_plan_vs_pinets_supertrend_only_L1" in summary
    assert "python_engine_case_plan_vs_pinets_supertrend_only_L2" in summary
