"""
Supertrend ATR and Factor Optimization Framework.

Performs grid search on Supertrend ATR length and factor parameters
to identify optimal settings that improve trade quality and reduce drawdown.

Usage:
    python supertrend_optimizer.py --atr-range 7 50 --factor-range 1.0 8.0 \
        --suite-root mtc_backtest/parity_suite_350 --baseline-case 001 \
        --output-prefix supertrend_opt
"""

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd
import csv
from datetime import datetime


def run_backtest(
    suite_root: str,
    case_id: str,
    atr_len: int,
    factor: float,
    output_dir: str
) -> Tuple[bool, Dict]:
    """
    Run a single backtest with given Supertrend parameters.

    Returns:
        (success, result_dict) where result_dict contains trade counts and metrics
    """
    case_path = Path(suite_root) / "cases" / f"parity_core_001_baseline_v01.json"

    if not case_path.exists():
        return False, {"error": f"Case file not found: {case_path}"}

    # Load baseline case and modify Supertrend parameters
    with open(case_path, 'r') as f:
        case_config = json.load(f)

    # Set Supertrend parameters
    if 'signals' not in case_config:
        case_config['signals'] = {}
    if 'supertrend' not in case_config['signals']:
        case_config['signals']['supertrend'] = {}

    case_config['signals']['supertrend']['atr_len'] = atr_len
    case_config['signals']['supertrend']['factor'] = factor

    # Create temporary case file for this test
    test_case_name = f"opt_atr{atr_len}_factor{factor:.1f}"
    temp_case_path = Path(output_dir) / f"{test_case_name}.json"

    with open(temp_case_path, 'w') as f:
        json.dump(case_config, f, indent=2)

    # Run backtest via audit script
    audit_cmd = [
        sys.executable,
        str(Path(suite_root) / "scripts" / "audit_case_range_manual.py"),
        "--suite-root", suite_root,
        "--manifest", str(Path(suite_root) / "manifests" / "cases_manifest_all.csv"),
        "--run-order-start", "1",
        "--run-order-end", "1",
        "--output-prefix", test_case_name,
        "--use-tv-trading-range",
    ]

    try:
        result = subprocess.run(audit_cmd, capture_output=True, text=True, timeout=300)

        # Parse output to extract trade counts
        output_csv = Path(output_dir) / f"{test_case_name}_compare.csv"

        if output_csv.exists():
            results = pd.read_csv(output_csv)
            if len(results) > 0:
                row = results.iloc[0]
                return True, {
                    "atr_len": atr_len,
                    "factor": factor,
                    "case_id": case_id,
                    "py_trades": row.get('Python Trades', 0),
                    "tv_trades": row.get('TV Trades', 0),
                    "status": row.get('Status', 'UNKNOWN'),
                    "match_pct": row.get('Match %', 0),
                }

        return False, {"error": "Could not parse backtest output"}

    except subprocess.TimeoutExpired:
        return False, {"error": "Backtest timeout"}
    except Exception as e:
        return False, {"error": str(e)}


def generate_parameter_grid(
    atr_min: int, atr_max: int,
    factor_min: float, factor_max: float
) -> List[Tuple[int, float]]:
    """Generate grid of parameter combinations."""
    grid = []

    # ATR length: step by 1
    for atr_len in range(atr_min, atr_max + 1):
        # Factor: step by 0.5
        factor = factor_min
        while factor <= factor_max + 0.01:
            grid.append((atr_len, round(factor, 1)))
            factor += 0.5

    return grid


def optimize_supertrend(
    suite_root: str,
    atr_range: Tuple[int, int],
    factor_range: Tuple[float, float],
    baseline_case: str = "001",
    output_prefix: str = "supertrend_opt"
) -> None:
    """
    Run Supertrend optimization grid search.

    Args:
        suite_root: Path to parity suite root
        atr_range: (min, max) for ATR length
        factor_range: (min, max) for factor
        baseline_case: Case ID to use as test case
        output_prefix: Prefix for output files
    """

    suite_path = Path(suite_root)
    output_dir = suite_path / "optimize" / output_prefix
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"📊 Supertrend Optimization Starting")
    print(f"   Suite Root: {suite_root}")
    print(f"   ATR Range: {atr_range[0]}-{atr_range[1]}")
    print(f"   Factor Range: {factor_range[0]}-{factor_range[1]}")
    print(f"   Output: {output_dir}")
    print()

    # Generate parameter grid
    grid = generate_parameter_grid(atr_range[0], atr_range[1],
                                    factor_range[0], factor_range[1])

    print(f"   Total combinations to test: {len(grid)}")
    print()

    # Run grid search
    results = []
    successful = 0
    failed = 0

    for i, (atr_len, factor) in enumerate(grid, 1):
        print(f"[{i:3d}/{len(grid)}] Testing ATR={atr_len:2d}, Factor={factor:.1f}...", end=" ")

        success, result = run_backtest(suite_root, baseline_case, atr_len, factor, str(output_dir))

        if success:
            results.append(result)
            status_str = result.get('status', 'UNKNOWN')
            py_trades = result.get('py_trades', 0)
            tv_trades = result.get('tv_trades', 0)
            print(f"✓ {status_str} (PY={py_trades}, TV={tv_trades})")
            successful += 1
        else:
            error = result.get('error', 'Unknown error')
            print(f"✗ {error}")
            failed += 1

    print()
    print(f"Optimization complete: {successful} successful, {failed} failed")
    print()

    # Save results to CSV
    results_csv = output_dir / f"{output_prefix}_results.csv"
    if results:
        df_results = pd.DataFrame(results)
        df_results = df_results.sort_values(['status', 'match_pct'], ascending=[False, False])
        df_results.to_csv(results_csv, index=False)

        print(f"📊 Results saved to: {results_csv}")
        print()
        print("Top 10 Parameter Combinations:")
        print(df_results[['atr_len', 'factor', 'status', 'match_pct', 'py_trades', 'tv_trades']].head(10).to_string(index=False))

    # Generate optimization report
    report_path = output_dir / f"{output_prefix}_report.md"
    with open(report_path, 'w') as f:
        f.write(f"# Supertrend Optimization Report\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Suite Root**: {suite_root}\n")
        f.write(f"**Baseline Case**: {baseline_case}\n\n")

        f.write(f"## Parameter Ranges\n")
        f.write(f"- ATR Length: {atr_range[0]} - {atr_range[1]}\n")
        f.write(f"- Factor: {factor_range[0]} - {factor_range[1]}\n")
        f.write(f"- Total combinations: {len(grid)}\n\n")

        f.write(f"## Results Summary\n")
        f.write(f"- Successful: {successful}\n")
        f.write(f"- Failed: {failed}\n\n")

        if results:
            df = pd.DataFrame(results)
            f.write(f"## Top Performers\n\n")
            top = df.nlargest(5, 'match_pct')
            for idx, row in top.iterrows():
                f.write(f"### ATR={int(row['atr_len'])}, Factor={row['factor']}\n")
                f.write(f"- Status: {row['status']}\n")
                f.write(f"- Match %: {row['match_pct']:.1f}%\n")
                f.write(f"- Python Trades: {int(row['py_trades'])}\n")
                f.write(f"- TV Trades: {int(row['tv_trades'])}\n\n")

    print(f"📄 Report saved to: {report_path}")


def main():
    parser = argparse.ArgumentParser(description="Supertrend Parameter Optimizer")
    parser.add_argument("--suite-root", required=True, help="Path to parity suite root")
    parser.add_argument("--atr-range", nargs=2, type=int, default=[15, 30],
                       help="ATR length range (min max)")
    parser.add_argument("--factor-range", nargs=2, type=float, default=[2.0, 6.0],
                       help="Factor range (min max)")
    parser.add_argument("--baseline-case", default="001", help="Baseline case ID")
    parser.add_argument("--output-prefix", default="supertrend_opt", help="Output prefix")

    args = parser.parse_args()

    optimize_supertrend(
        suite_root=args.suite_root,
        atr_range=tuple(args.atr_range),
        factor_range=tuple(args.factor_range),
        baseline_case=args.baseline_case,
        output_prefix=args.output_prefix
    )


if __name__ == "__main__":
    main()
