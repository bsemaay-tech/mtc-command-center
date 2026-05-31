import json
from pathlib import Path

from scripts.health_alerts import evaluate_operational_alerts, evaluate_walkforward_summary


def test_health_alerts_ok(tmp_path: Path):
    p = tmp_path / "summary.json"
    p.write_text(json.dumps({"status": "OK", "ok_candidates": 2}), encoding="utf-8")
    result = evaluate_walkforward_summary(p)
    assert result["status"] == "OK"


def test_health_alerts_missing_summary(tmp_path: Path):
    result = evaluate_walkforward_summary(tmp_path / "missing.json")
    assert result["status"] == "ALERT"


def test_operational_alerts_parity_fail(tmp_path: Path):
    metrics = tmp_path / "ops_metrics.json"
    metrics.write_text(json.dumps({"overall_pass": False}), encoding="utf-8")
    result = evaluate_operational_alerts(metrics)
    assert result["status"] == "ALERT"
    assert result["reason"] == "parity_nightly_fail"


def test_operational_alerts_checksum_mismatch(tmp_path: Path):
    metrics = tmp_path / "ops_metrics.json"
    metrics.write_text(json.dumps({"overall_pass": True}), encoding="utf-8")
    checksum = tmp_path / "checksum.json"
    checksum.write_text(json.dumps({"checksum_mismatch_count": 2}), encoding="utf-8")
    result = evaluate_operational_alerts(metrics, checksum)
    assert result["status"] == "ALERT"
    assert result["reason"] == "checksum_mismatch"
