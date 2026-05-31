import re
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def _run_cmd(cmd, cwd):
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)


def _extract_run_id(stdout: str) -> str:
    m = re.search(r"DB Run Created:\s+([^\s]+)", stdout)
    if not m:
        raise AssertionError(f"Run ID not found in stdout:\n{stdout}")
    return m.group(1).strip()


def test_show_run_and_compare_runs_cli(tmp_path):
    db_path = tmp_path / "runs.db"
    case_path = PROJECT_ROOT / "mtc_backtest" / "configs" / "cases" / "full_jul2025_jan2026_parity.json"
    if not case_path.exists():
        pytest.skip("Config case not found")

    cwd = PROJECT_ROOT / "mtc_backtest"
    create1 = _run_cmd(
        [
            sys.executable, "-m", "src.optimizer_v0", "run",
            "--case", str(case_path),
            "--mode", "random",
            "--iters", "1",
            "--seed", "42",
            "--workers", "1",
            "--db", str(db_path),
        ],
        cwd,
    )
    assert create1.returncode == 0, create1.stderr
    run_a = _extract_run_id(create1.stdout)

    create2 = _run_cmd(
        [
            sys.executable, "-m", "src.optimizer_v0", "run",
            "--case", str(case_path),
            "--mode", "random",
            "--iters", "1",
            "--seed", "43",
            "--workers", "1",
            "--db", str(db_path),
        ],
        cwd,
    )
    assert create2.returncode == 0, create2.stderr
    run_b = _extract_run_id(create2.stdout)

    show = _run_cmd(
        [sys.executable, "-m", "src.optimizer_v0", "show-run", "--db", str(db_path), "--run-id", run_a],
        cwd,
    )
    assert show.returncode == 0, show.stderr
    assert f"Run: {run_a}" in show.stdout
    assert "Trials: total=" in show.stdout

    compare = _run_cmd(
        [
            sys.executable, "-m", "src.optimizer_v0", "compare-runs",
            "--db", str(db_path),
            "--run-a", run_a,
            "--run-b", run_b,
        ],
        cwd,
    )
    assert compare.returncode == 0, compare.stderr
    assert "Overlap params_key:" in compare.stdout


def test_space_file_hash_is_stored(tmp_path):
    db_path = tmp_path / "runs.db"
    case_path = PROJECT_ROOT / "mtc_backtest" / "configs" / "cases" / "full_jul2025_jan2026_parity.json"
    space_path = PROJECT_ROOT / "mtc_backtest" / "configs" / "space_example.json"
    if not case_path.exists() or not space_path.exists():
        pytest.skip("Required files not found")

    cwd = PROJECT_ROOT / "mtc_backtest"
    run = _run_cmd(
        [
            sys.executable, "-m", "src.optimizer_v0", "run",
            "--case", str(case_path),
            "--mode", "random",
            "--iters", "1",
            "--seed", "42",
            "--workers", "1",
            "--db", str(db_path),
            "--space-file", str(space_path),
        ],
        cwd,
    )
    assert run.returncode == 0, run.stderr
    run_id = _extract_run_id(run.stdout)

    with sqlite3.connect(db_path) as conn:
        row = conn.execute("SELECT code_hash FROM runs WHERE run_id=?", (run_id,)).fetchone()
    assert row is not None
    assert row[0] is not None
    assert "space_file_sha256" in row[0]
