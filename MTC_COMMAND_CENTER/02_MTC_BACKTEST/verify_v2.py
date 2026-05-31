import os
import sys
import shutil
import subprocess
import pandas as pd
from pathlib import Path

# Paths
ROOT = Path(__file__).parent.parent 
RESULTS = ROOT / "results"
DB_PATH = RESULTS / "test_verify.db"
CSV_NO_DB = RESULTS / "smoke_verify_no_db.csv"
CSV_WITH_DB = RESULTS / "smoke_verify_with_db.csv"

def cleanup():
    print("Cleaning up...")
    if DB_PATH.exists():
        try:
            DB_PATH.unlink()
            print(f"Deleted {DB_PATH}")
        except PermissionError:
            print("Warning: could not delete DB (locked?)")
    if CSV_NO_DB.exists(): 
        CSV_NO_DB.unlink()
        print(f"Deleted {CSV_NO_DB}")
    if CSV_WITH_DB.exists(): 
        CSV_WITH_DB.unlink()
        print(f"Deleted {CSV_WITH_DB}")

def run_optimizer(args, check=True):
    cmd = [sys.executable, "-m", "src.optimizer_v0", "run"] + args
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, cwd=str(ROOT / "mtc_backtest"), check=check)

def main():
    cleanup()
    
    # 1. Run without DB
    print("\n[1/3] Running NO-DB...")
    run_optimizer([
        "--case", "configs/cases/full_jul2025_jan2026_parity.json",
        "--mode", "random", "--iters", "5", "--seed", "42", "--workers", "1",
        "--out", str(CSV_NO_DB)
    ])
    
    # 2. Run with DB
    print("\n[2/3] Running WITH-DB...")
    run_optimizer([
        "--case", "configs/cases/full_jul2025_jan2026_parity.json",
        "--mode", "random", "--iters", "5", "--seed", "42", "--workers", "1",
        "--db", str(DB_PATH),
        "--out", str(CSV_WITH_DB)
    ])
    
    # 3. Compare
    print("\n[3/3] Comparing...")
    if not CSV_NO_DB.exists() or not CSV_WITH_DB.exists():
        print("FAIL: One or both output CSVs missing")
        sys.exit(1)
        
    df1 = pd.read_csv(CSV_NO_DB).drop(columns=["runtime_s"], errors="ignore")
    df2 = pd.read_csv(CSV_WITH_DB).drop(columns=["runtime_s"], errors="ignore")
    
    try:
        pd.testing.assert_frame_equal(df1, df2)
        print("PASS: Determinism verified (CSV headers and data identical)")
    except AssertionError as e:
        print(f"FAIL: Dataframes distinct\n{e}")
        print(f"Left ({len(df1)}): {CSV_NO_DB}")
        print(f"Right ({len(df2)}): {CSV_WITH_DB}")
        sys.exit(1)

    # 4. List runs
    print("\n[List Runs check]")
    run_optimizer(["--db", str(DB_PATH), "--list-runs"])

    print("\nALL PASSED.")

if __name__ == "__main__":
    main()
