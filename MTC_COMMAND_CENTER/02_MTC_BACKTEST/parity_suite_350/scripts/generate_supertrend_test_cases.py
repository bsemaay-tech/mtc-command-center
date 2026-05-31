"""
Generate Supertrend optimization test cases from baseline.

Creates case JSON files with different ATR length and factor combinations
for Phase 1 sensitivity analysis.

Usage:
    python generate_supertrend_test_cases.py \
        --suite-root mtc_backtest/parity_suite_350 \
        --baseline-case parity_core_005_enable_long_trades_v01 \
        --atr-lengths 14 21 28 \
        --factors 3.0 4.0 5.0
"""

import argparse
import json
from pathlib import Path
from typing import List, Tuple


def generate_test_cases(
    suite_root: str,
    baseline_case_name: str,
    atr_lengths: List[int],
    factors: List[float]
) -> Tuple[int, List[str]]:
    """
    Generate test cases with different Supertrend parameters.

    Returns:
        (total_generated, case_names)
    """

    suite_path = Path(suite_root)
    cases_dir = suite_path / "cases"

    # Load baseline case
    baseline_path = cases_dir / f"{baseline_case_name}.json"

    if not baseline_path.exists():
        raise FileNotFoundError(f"Baseline case not found: {baseline_path}")

    with open(baseline_path, 'r') as f:
        baseline = json.load(f)

    generated_cases = []

    for atr_len in atr_lengths:
        for factor in factors:
            # Create case ID
            case_name = f"parity_opt_001_atr{atr_len:02d}_factor{factor:.1f}".replace(".", "_")
            case_path = cases_dir / f"{case_name}.json"

            # Copy baseline and modify Supertrend parameters
            case_config = baseline.copy()

            # Update case ID and description
            case_config["_case_id"] = case_name
            case_config["_generated"] = {
                "description": f"Supertrend optimization: ATR={atr_len}, Factor={factor}",
                "baseline_case": baseline_case_name,
                "supertrend_atr_len": atr_len,
                "supertrend_factor": factor,
            }

            # Update Supertrend parameters
            if "config" not in case_config:
                case_config["config"] = {}
            if "supertrend" not in case_config["config"]:
                case_config["config"]["supertrend"] = {}

            case_config["config"]["supertrend"]["atr_len"] = atr_len
            case_config["config"]["supertrend"]["factor"] = factor

            # Write case file
            with open(case_path, 'w') as f:
                json.dump(case_config, f, indent=2)

            generated_cases.append(case_name)
            print(f"  ✓ {case_name}")

    return len(generated_cases), generated_cases


def main():
    parser = argparse.ArgumentParser(description="Generate Supertrend Test Cases")
    parser.add_argument("--suite-root", required=True, help="Path to parity suite root")
    parser.add_argument("--baseline-case", default="parity_core_005_enable_long_trades_v01",
                       help="Baseline case name (without .json)")
    parser.add_argument("--atr-lengths", nargs="+", type=int, default=[14, 21, 28],
                       help="ATR lengths to test")
    parser.add_argument("--factors", nargs="+", type=float, default=[3.0, 4.0, 5.0],
                       help="Factors to test")

    args = parser.parse_args()

    print(f"📝 Generating Supertrend Test Cases")
    print(f"   Suite Root: {args.suite_root}")
    print(f"   Baseline: {args.baseline_case}")
    print(f"   ATR Lengths: {args.atr_lengths}")
    print(f"   Factors: {args.factors}")
    print()

    total = len(args.atr_lengths) * len(args.factors)
    print(f"   Total combinations: {total}")
    print()

    try:
        generated, case_names = generate_test_cases(
            suite_root=args.suite_root,
            baseline_case_name=args.baseline_case,
            atr_lengths=args.atr_lengths,
            factors=args.factors
        )

        print()
        print(f"✓ Generated {generated} test cases")
        print()
        print("Case names for manifest:")
        for name in case_names:
            print(f"  {name}")

    except Exception as e:
        print(f"✗ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
