"""
Run the Supertrend walk-forward workflow on the corrected BTCUSDT.P parity contract.

Default profile:
- train  : 2025-01-01 .. 2025-06-30
- target1: 2025-07-01 .. 2025-09-30
- target2: 2025-10-01 .. 2026-01-01
- space  : high-ATR cluster that held up least-bad on holdout
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TRAIN_CASE = "configs/cases/supertrend_wf_train_20260308.json"
DEFAULT_TARGET1_CASE = "configs/cases/supertrend_wf_target1_20260308.json"
DEFAULT_TARGET2_CASE = "configs/cases/supertrend_wf_target2_20260308.json"
PROFILE_SPACE_FILES = {
    "high_atr": "configs/spaces/supertrend_walkforward_high_atr_20260308.json",
    "short_atr": "configs/spaces/supertrend_walkforward_short_atr_20260308.json",
}
DEFAULT_PROFILE = "high_atr"
DEFAULT_OBJECTIVES = "net_profit,max_dd_pct,profit_factor,win_rate,total_trades"


def resolve_space_file(profile: str, override: str) -> str:
    if override:
        return override
    try:
        return PROFILE_SPACE_FILES[profile]
    except KeyError as exc:
        raise ValueError(f"Unknown profile: {profile}") from exc


def build_command(args: argparse.Namespace, outdir: Path) -> list[str]:
    return [
        sys.executable,
        "-m",
        "scripts.walk_forward_validate",
        "--train-case",
        args.train_case,
        "--target-case-1",
        args.target_case_1,
        "--target-case-2",
        args.target_case_2,
        "--mode",
        args.mode,
        "--iters",
        str(args.iters),
        "--seed",
        str(args.seed),
        "--workers",
        str(args.workers),
        "--min-trades",
        str(args.min_trades),
        "--max-dd",
        str(args.max_dd),
        "--space-file",
        args.space_file,
        "--objectives",
        args.objectives,
        "--top-k",
        str(args.top_k),
        "--outdir",
        str(outdir),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Supertrend walk-forward workflow.")
    parser.add_argument("--train-case", default=DEFAULT_TRAIN_CASE)
    parser.add_argument("--target-case-1", default=DEFAULT_TARGET1_CASE)
    parser.add_argument("--target-case-2", default=DEFAULT_TARGET2_CASE)
    parser.add_argument("--profile", choices=sorted(PROFILE_SPACE_FILES.keys()), default=DEFAULT_PROFILE)
    parser.add_argument("--space-file", default="")
    parser.add_argument("--mode", choices=["grid", "random", "bayes"], default="grid")
    parser.add_argument("--iters", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 1) - 1))
    parser.add_argument("--min-trades", type=int, default=10)
    parser.add_argument("--max-dd", type=float, default=80.0)
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--objectives", default=DEFAULT_OBJECTIVES)
    parser.add_argument("--outdir", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    args.space_file = resolve_space_file(args.profile, args.space_file)

    if args.outdir:
        outdir = (PROJECT_ROOT / args.outdir).resolve()
    else:
        stamp = time.strftime("%Y%m%d_%H%M%S")
        outdir = (PROJECT_ROOT / "results" / "walkforward" / f"supertrend_{args.profile}_{stamp}").resolve()

    cmd = build_command(args, outdir)

    print("Supertrend walk-forward setup")
    print(f"  profile    : {args.profile}")
    print(f"  train_case : {args.train_case}")
    print(f"  target_1   : {args.target_case_1}")
    print(f"  target_2   : {args.target_case_2}")
    print(f"  space_file : {args.space_file}")
    print(f"  mode       : {args.mode}")
    print(f"  outdir     : {outdir}")

    if args.dry_run:
        print("\nCommand:")
        print(" ".join(cmd))
        return 0

    outdir.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
    return int(result.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
