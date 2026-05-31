from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

from parity_oracles.feature_traces.time_utils import looks_iso_utc
from parity_oracles.run_feature_parity import _policy_mismatch


ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "reports" / "parity" / "case_001" / "features" / "producer_supertrend_current" / "FEATURE_PARITY_REPORT.json"
PYTHON_TRACE = ROOT / "reports" / "parity" / "case_001" / "features" / "producer_supertrend_current" / "python_feature_trace.csv"
PINETS_TRACE = ROOT / "reports" / "parity" / "case_001" / "features" / "producer_supertrend_current" / "pinets_feature_trace.csv"


def _run_feature_parity() -> dict[str, object]:
    completed = subprocess.run(
        [
            sys.executable,
            "parity_oracles/run_feature_parity.py",
            "--contract",
            "feature_contracts/active/producer_supertrend_current.yml",
            "--case",
            "cases/fast_suite_case_001.json",
            "--oracles",
            "python",
            "pinets",
            "--levels",
            "L0",
            "L1",
            "L2",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr or completed.stdout
    return json.loads(REPORT.read_text(encoding="utf-8"))


def _first_rows(path: Path, count: int = 8) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [row for _, row in zip(range(count), reader)]


def test_supertrend_traces_use_iso_utc_timestamps() -> None:
    _run_feature_parity()
    python_rows = _first_rows(PYTHON_TRACE)
    pinets_rows = _first_rows(PINETS_TRACE)
    assert all(looks_iso_utc(row["timestamp"]) for row in python_rows)
    assert all(looks_iso_utc(row["timestamp"]) for row in pinets_rows)


def test_bar_index_zero_refers_to_same_first_candle() -> None:
    _run_feature_parity()
    python_first = _first_rows(PYTHON_TRACE, 1)[0]
    pinets_first = _first_rows(PINETS_TRACE, 1)[0]
    assert python_first["bar_index"] == "0"
    assert pinets_first["bar_index"] == "0"
    assert python_first["timestamp"] == pinets_first["timestamp"]


def test_policy_mismatch_rejects_timestamp_policy_drift() -> None:
    contract = {"trace": {"timestamp_policy": "ISO_UTC", "bar_index_policy": "zero_based_case_candle_index"}}
    python_status = {"timestamp_policy": "UNIX_SECONDS", "bar_index_policy": "zero_based_case_candle_index"}
    pinets_status = {"timestamp_policy": "ISO_UTC", "bar_index_policy": "zero_based_case_candle_index"}
    mismatches = _policy_mismatch(contract, python_status, pinets_status)
    assert any("timestamp_policy" in item for item in mismatches)


def test_supertrend_dry_run_no_longer_compares_unix_seconds_to_iso() -> None:
    payload = _run_feature_parity()
    assert payload["timestamp_policy"] == "ISO_UTC"
    assert payload["python_trace_status"]["first_timestamps"][0] == "2024-12-31T03:00:00+00:00"
    assert payload["python_trace_status"]["first_timestamps"] == payload["pinets_trace_status"]["first_timestamps"]
    assert payload["verdict"] != "TRACE_POLICY_MISMATCH"


def test_known_good_supertrend_feature_trace_passes_l1_l2_surface() -> None:
    payload = _run_feature_parity()
    assert payload["verdict"] in {"FEATURE_TRACE_PASS", "FEATURE_TRACE_PASS_WITH_TOLERANCE"}
    assert payload["comparison"]["first_divergence"] is None
    assert payload["comparison"]["baseline_rows"] == payload["comparison"]["candidate_rows"]
