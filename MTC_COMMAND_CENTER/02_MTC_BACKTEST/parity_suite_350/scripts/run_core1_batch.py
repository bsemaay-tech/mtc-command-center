#!/usr/bin/env python3
"""
Run Python backtest for all PASS cases from Core-1 setup check.

Executes: python scripts/run_case.py for each PASS case in core1_setup_check.csv
Outputs: runs/{case_id}_metrics.json and runs/{case_id}_trades.csv per case
"""

import subprocess
import csv
from pathlib import Path
from typing import List, Tuple

def read_pass_cases(csv_path: Path) -> List[Tuple[int, str]]:
    """Read PASS cases from setup check CSV."""
    pass_cases = []
    try:
        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("status") == "PASS":
                    run_order = int(row.get("run_order", 0))
                    case_id = row.get("case_id", "")
                    if case_id:
                        pass_cases.append((run_order, case_id))
    except Exception as e:
        print(f"ERROR reading {csv_path}: {e}")
        return []
    return pass_cases

def run_case(case_id: str, mtc_backtest_base: Path) -> bool:
    """Run a single case. Returns True if successful."""
    case_json = mtc_backtest_base / "parity_suite_350" / "cases" / f"{case_id}.json"
    if not case_json.exists():
        print(f"  ERROR: case JSON not found: {case_json}")
        return False

    cmd = [
        "python",
        str(mtc_backtest_base / "scripts" / "run_case.py"),
        str(case_json),
    ]

    try:
        result = subprocess.run(cmd, cwd=str(mtc_backtest_base), capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            return True
        else:
            print(f"  ERROR: case run failed")
            if result.stderr:
                print(f"  stderr: {result.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  ERROR: case run timeout (>300s)")
        return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def main():
    base_path = Path(__file__).parent.parent
    compare_runs_base = base_path / "compare_runs"
    csv_path = compare_runs_base / "core1_setup_check.csv"

    if not csv_path.exists():
        print(f"ERROR: setup check CSV not found: {csv_path}")
        print("Run check_setup_core1.py first")
        return

    mtc_backtest_base = base_path.parent

    pass_cases = read_pass_cases(csv_path)
    print(f"Found {len(pass_cases)} PASS cases to run")
    print()

    pass_count = 0
    fail_count = 0

    for run_order, case_id in pass_cases:
        print(f"[{run_order:03d}] {case_id}...", end=" ")
        if run_case(case_id, mtc_backtest_base):
            print("[OK]")
            pass_count += 1
        else:
            print("[FAILED]")
            fail_count += 1

    print()
    print(f"Summary: {pass_count} OK, {fail_count} FAILED")

if __name__ == "__main__":
    main()
