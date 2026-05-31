import pytest
import sys
import subprocess
from pathlib import Path
import os

# Ensure src can be imported
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

def test_db_out_existing_csv_requires_run_id(tmp_path):
    """Verify that --db + --out on existing CSV requires --run-id."""
    
    # Setup
    csv_path = tmp_path / "existing.csv"
    db_path = tmp_path / "test.db"
    
    # Create dummy existing CSV
    csv_path.write_text("idx,score,status\n0,1.0,OK\n")
    
    case_path = PROJECT_ROOT / "mtc_backtest" / "configs" / "cases" / "full_jul2025_jan2026_parity.json"
    if not case_path.exists():
        pytest.skip("Config case not found")

    cmd = [
        sys.executable, "-m", "src.optimizer_v0", "run",
        "--case", str(case_path),
        "--mode", "random",
        "--iters", "1",
        "--seed", "42",
        "--workers", "1",
        "--db", str(db_path),
        "--out", str(csv_path)
        # --run-id MISSING
    ]
    
    cwd = PROJECT_ROOT / "mtc_backtest"
    result = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True
    )
    
    # Assert failure
    assert result.returncode == 2
    assert "Error: --db + --out with existing CSV requires --run-id" in result.stdout or \
           "Error: --db + --out with existing CSV requires --run-id" in result.stderr

def test_db_out_fresh_ok(tmp_path):
    """Verify that --db + --out on NEW CSV works fine without run-id."""
    
    csv_path = tmp_path / "fresh.csv"
    db_path = tmp_path / "test.db"
    
    case_path = PROJECT_ROOT / "mtc_backtest" / "configs" / "cases" / "full_jul2025_jan2026_parity.json"
    if not case_path.exists():
        pytest.skip("Config case not found")

    cmd = [
        sys.executable, "-m", "src.optimizer_v0", "run",
        "--case", str(case_path),
        "--mode", "random",
        "--iters", "1",
        "--seed", "42",
        "--workers", "1",
        "--db", str(db_path),
        "--out", str(csv_path)
    ]
    
    cwd = PROJECT_ROOT / "mtc_backtest"
    result = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True
    )
    
    # Assert success
    assert result.returncode == 0, f"Run failed: {result.stderr}"
    assert csv_path.exists()


def test_db_export_csv_fresh_ok(tmp_path):
    """Verify --db + --export-csv on new path works."""
    csv_path = tmp_path / "fresh_export.csv"
    db_path = tmp_path / "test.db"

    case_path = PROJECT_ROOT / "mtc_backtest" / "configs" / "cases" / "full_jul2025_jan2026_parity.json"
    if not case_path.exists():
        pytest.skip("Config case not found")

    cmd = [
        sys.executable, "-m", "src.optimizer_v0", "run",
        "--case", str(case_path),
        "--mode", "random",
        "--iters", "1",
        "--seed", "42",
        "--workers", "1",
        "--db", str(db_path),
        "--export-csv", str(csv_path)
    ]

    cwd = PROJECT_ROOT / "mtc_backtest"
    result = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Run failed: {result.stderr}"
    assert csv_path.exists()


def test_out_and_export_csv_mutually_exclusive(tmp_path):
    """Verify --out and --export-csv cannot be passed together."""
    csv1 = tmp_path / "a.csv"
    csv2 = tmp_path / "b.csv"
    case_path = PROJECT_ROOT / "mtc_backtest" / "configs" / "cases" / "full_jul2025_jan2026_parity.json"
    if not case_path.exists():
        pytest.skip("Config case not found")

    cmd = [
        sys.executable, "-m", "src.optimizer_v0", "run",
        "--case", str(case_path),
        "--mode", "random",
        "--iters", "1",
        "--seed", "42",
        "--workers", "1",
        "--out", str(csv1),
        "--export-csv", str(csv2),
    ]

    cwd = PROJECT_ROOT / "mtc_backtest"
    result = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True
    )

    assert result.returncode == 2
    assert "--out and --export-csv cannot be used together" in (result.stdout + result.stderr)
