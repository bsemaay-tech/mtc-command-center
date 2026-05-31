from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from scripts.ops_metrics import build_metrics, compute_run_duration_seconds, parity_drift_count


def test_compute_run_duration_seconds_from_file_mtimes(tmp_path: Path):
    run_dir = tmp_path / "run"
    run_dir.mkdir(parents=True, exist_ok=True)
    f1 = run_dir / "a.txt"
    f2 = run_dir / "b.txt"
    f1.write_text("a", encoding="utf-8")
    f2.write_text("b", encoding="utf-8")
    assert compute_run_duration_seconds(run_dir) >= 0.0


def test_parity_drift_count_uses_all_core_match_column(tmp_path: Path):
    p = tmp_path / "parity.csv"
    pd.DataFrame({"all_core_match": [True, False, True, False]}).to_csv(p, index=False)
    assert parity_drift_count(p) == 2


def test_build_metrics_pass_fail_logic(tmp_path: Path):
    summary = tmp_path / "summary.json"
    summary.write_text(json.dumps({"status": "OK", "ok_candidates": 1}), encoding="utf-8")
    parity = tmp_path / "parity.csv"
    pd.DataFrame({"all_core_match": [True, True]}).to_csv(parity, index=False)

    metrics = build_metrics(run_dir=tmp_path, walkforward_summary=summary, parity_report=parity)
    assert metrics["walkforward_pass"] is True
    assert metrics["parity_drift_count"] == 0
    assert metrics["overall_pass"] is True
