"""
Print first divergence row from a parity comparison report.

Example:
  python scripts/first_divergence_finder.py --report debug/BTCUSDT/15m/parity_compare.csv
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

import pandas as pd


def find_first_mismatch(report: pd.DataFrame) -> Optional[pd.Series]:
    if "all_core_match" not in report.columns:
        raise ValueError("Missing required column: all_core_match")
    bad = report[~report["all_core_match"]]
    if bad.empty:
        return None
    sort_cols = [c for c in ("tv_seq", "py_seq", "tv_entry_time", "py_entry_time") if c in bad.columns]
    if sort_cols:
        bad = bad.sort_values(sort_cols, kind="mergesort")
    return bad.iloc[0]


def main() -> None:
    p = argparse.ArgumentParser(description="Find first mismatch in parity compare report.")
    p.add_argument("--report", required=True, help="Path to parity_compare_report.csv")
    args = p.parse_args()

    report_path = Path(args.report)
    df = pd.read_csv(report_path)
    first = find_first_mismatch(df)
    if first is None:
        print("No mismatches found.")
        return

    print("First mismatch:")
    fields = [
        "tv_seq", "py_seq",
        "tv_side", "py_side",
        "tv_reason", "py_reason",
        "tv_entry_time", "py_entry_time",
        "tv_exit_time", "py_exit_time",
        "entry_time_diff_min", "exit_time_diff_min",
    ]
    for f in fields:
        if f in first:
            print(f"{f}: {first[f]}")


if __name__ == "__main__":
    main()
