import pytest
import sys
import subprocess
import pandas as pd
from pathlib import Path

# Ensure src can be imported
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

def test_single_invocation_run_count(tmp_path):
    """Verify that a single CLI invocation runs exactly the specified number of iterations."""
    
    # Paths
    case_path = PROJECT_ROOT / "mtc_backtest" / "configs" / "cases" / "full_jul2025_jan2026_parity.json"
    out_csv = tmp_path / "dup_test.csv"
    
    if not case_path.exists():
        pytest.skip("Config case not found")

    # Command: run 3 iters
    iters = 3
    cmd = [
        sys.executable, "-m", "src.optimizer_v0", "run",
        "--case", str(case_path),
        "--mode", "random",
        "--iters", str(iters),
        "--seed", "42",
        "--workers", "1",
        "--out", str(out_csv)
    ]
    
    cwd = PROJECT_ROOT / "mtc_backtest"
    result = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Run failed: {result.stderr}"
    
    # Assert CSV exists and has exactly 'iters' rows
    assert out_csv.exists()
    df = pd.read_csv(out_csv)
    
    # If the bug exists, this might be 2 * iters
    assert len(df) == iters, f"Expected {iters} rows, got {len(df)}. Double execution likely."

def test_db_single_run_creation(tmp_path):
    """Verify only one run_id is created in DB per invocation."""
    db_path = tmp_path / "dup_test.db"
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
        "--db", str(db_path)
    ]
    
    cwd = PROJECT_ROOT / "mtc_backtest"
    subprocess.run(cmd, cwd=str(cwd), check=True, capture_output=True)
    
    # Check DB runs count
    import sqlite3
    with sqlite3.connect(db_path) as conn:
        count = conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
        
    assert count == 1, f"Expected 1 run in DB, found {count}"
