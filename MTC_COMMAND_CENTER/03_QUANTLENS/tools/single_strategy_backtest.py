#!/usr/bin/env python
"""Run the mandatory single-strategy QuantLens validation workflow."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from data_check import verify_actual_range

TOOLS_DIR = Path(__file__).resolve().parent
DEFAULT_OUT_ROOT = TOOLS_DIR / "single_strategy_runs"


def run_step(cmd: list[str], env: dict, cwd: Path) -> dict:
    started = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(cmd, cwd=cwd, env=env, text=True, capture_output=True, check=False)
    return {
        "cmd": cmd,
        "started_utc": started,
        "returncode": result.returncode,
        "stdout_tail": result.stdout.splitlines()[-20:],
        "stderr_tail": result.stderr.splitlines()[-20:],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("strategy_id")
    parser.add_argument("symbol")
    parser.add_argument("timeframe")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--v2", action="store_true", help="use overnight_v2_runner monkey-patched strategies")
    args = parser.parse_args()

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_dir = (args.out_dir or DEFAULT_OUT_ROOT / f"{args.strategy_id}_{args.symbol}_{args.timeframe}_{stamp}").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    validation = verify_actual_range(args.symbol, args.timeframe)
    (out_dir / "data_validation.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
    if validation["status"] != "PASS":
        print(f"DATA_VALIDATION_FAIL {validation}")
        return 2

    env = os.environ.copy()
    env["MEGA_OUTPUT_DIR"] = str(out_dir)
    env["MEGA_WORKERS"] = str(args.workers)
    runner = "overnight_v2_runner.py" if args.v2 else "mega_walk_forward.py"
    steps = [
        [sys.executable, runner, "--strategy", args.strategy_id, "--symbol", args.symbol, "--tf", args.timeframe, "--checkpoint-every", "1"],
        [sys.executable, "alpha_vs_buyhold.py"],
        [sys.executable, "cpcv_validator.py", "--input", str(out_dir / "MEGA_walk_forward_results.json"), "--out-dir", str(out_dir / "cpcv"), "--max-candidates", "20"] + (["--v2"] if args.v2 else []),
        [sys.executable, "probabilistic_pbo.py", "--cpcv", str(out_dir / "cpcv" / "cpcv_results.json"), "--out-dir", str(out_dir / "pbo")],
    ]

    log = {"data_validation": validation, "steps": []}
    for cmd in steps:
        step = run_step(cmd, env, TOOLS_DIR)
        log["steps"].append(step)
        (out_dir / "single_strategy_workflow_log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
        if step["returncode"] != 0:
            print(f"STEP_FAIL rc={step['returncode']} cmd={' '.join(cmd)}")
            return step["returncode"]

    summary = [
        "# Single Strategy Backtest Workflow",
        "",
        f"- Strategy: `{args.strategy_id}`",
        f"- Symbol/timeframe: `{args.symbol}` `{args.timeframe}`",
        f"- Output: `{out_dir}`",
        f"- Data: `{validation['first']}` -> `{validation['last']}` bars=`{validation['bar_count']}`",
        "",
        "Artifacts:",
        "- `MEGA_walk_forward_results.json`",
        "- `alpha_summary.json`",
        "- `cpcv/CPCV_VALIDATION_REPORT.md`",
        "- `pbo/PBO_REPORT.md`",
    ]
    (out_dir / "SINGLE_STRATEGY_SUMMARY.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    # Refresh the dashboard: aggregate sprint_runs and export to 05_BACKTEST_RESULTS.
    # Non-fatal — a refresh failure does not invalidate the completed workflow.
    agg = run_step(
        [sys.executable, "aggregate_overnight_iters.py", "--runs-dir", str(TOOLS_DIR / "sprint_runs")],
        env,
        TOOLS_DIR,
    )
    log["dashboard_refresh"] = agg
    (out_dir / "single_strategy_workflow_log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
    if agg["returncode"] == 0:
        print("Dashboard updated")
    else:
        print(f"WARN dashboard refresh failed rc={agg['returncode']}")

    print(f"SINGLE_STRATEGY_DONE out={out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
