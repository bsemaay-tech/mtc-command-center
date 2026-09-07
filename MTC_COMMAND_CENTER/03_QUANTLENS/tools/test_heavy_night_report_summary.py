"""Regression test for heavy_night_report.py's computed-but-unwritten `passcells`.

Lane K's static hunt (MTC_COMMAND_CENTER/11_TRIAGE/
OVERNIGHT_LANE_K_NONPROTECTED_STATIC_HUNT_2026-09-07.md, finding #5) found that
`heavy_night_report.py` computes `passcells` (rows classified PASS or
STRONG_PASS) in both branches of the MEGA-results if/else but never writes the
count into the produced report. This test builds a tiny synthetic run
directory in tmp_path, runs the report's `main()` against it (no subprocess,
no real run data), and asserts the pass-cells count appears in the output
markdown.

RED (before the fix): the assertion below fails because no "pass cells" line
is emitted anywhere in the report.
GREEN (after the fix): `main()` appends
`- pass cells (PASS+STRONG_PASS): **N**` right after the existing
`robust_final` / `DSR p>=0.50` summary line in section 1, mirroring every
other computed-collection line in that section.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parent / "heavy_night_report.py"
SPEC = importlib.util.spec_from_file_location("heavy_night_report", MODULE_PATH)
assert SPEC and SPEC.loader
heavy_night_report = importlib.util.module_from_spec(SPEC)
sys.modules["heavy_night_report"] = heavy_night_report
SPEC.loader.exec_module(heavy_night_report)


def _write_mega_results(run_dir: Path) -> None:
    payload = {
        "runtime_seconds": 1234,
        "workers": 4,
        "config": {
            "strategy_count": 3,
            "selected_symbols": ["BTCUSDT", "ETHUSDT"],
            "selected_timeframes": ["1h"],
        },
        "results": [
            {"classification": "STRONG_PASS", "robust_final": True, "dsr_p_value": 0.97},
            {"classification": "PASS", "robust_final": False, "dsr_p_value": 0.6},
            {"classification": "FAIL", "robust_final": False, "dsr_p_value": 0.1},
        ],
    }
    (run_dir / "MEGA_walk_forward_results.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )


def test_pass_cells_count_is_written_to_report(tmp_path: Path) -> None:
    run_dir = tmp_path / "night_run"
    run_dir.mkdir()
    _write_mega_results(run_dir)
    out_path = tmp_path / "HEAVY_NIGHT_REPORT.md"

    rc = heavy_night_report.main(
        ["--run-dir", str(run_dir), "--night-id", "2026-09-07", "--out", str(out_path)]
    )

    assert rc == 0
    report = out_path.read_text(encoding="utf-8")
    # 2 of the 3 synthetic rows are PASS or STRONG_PASS.
    assert "pass cells" in report.lower()
    assert "**2**" in report


def test_pass_cells_zero_when_mega_results_missing(tmp_path: Path) -> None:
    """MISSING-mega branch still sets passcells = [] and must not crash on it."""
    run_dir = tmp_path / "empty_night_run"
    run_dir.mkdir()
    out_path = tmp_path / "HEAVY_NIGHT_REPORT.md"

    rc = heavy_night_report.main(
        ["--run-dir", str(run_dir), "--night-id", "2026-09-07", "--out", str(out_path)]
    )

    assert rc == 0
    report = out_path.read_text(encoding="utf-8")
    assert "MEGA results: **MISSING**" in report
