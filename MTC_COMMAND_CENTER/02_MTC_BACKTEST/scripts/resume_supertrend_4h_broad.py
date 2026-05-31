from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.run_supertrend_4h_broad_overnight import (
    DEFAULT_BE_SPACE,
    DEFAULT_CASE_FULL,
    DEFAULT_MULTI_TP_SPACE,
    DEFAULT_SL_SPACE,
    DEFAULT_TP_SPACE,
    DEFAULT_TRAIL_SPACE,
    _backtest_case,
    _best_stage,
    _candidate_path,
    _materialize_family,
    _run_checked,
    _stage_record,
    _walkforward,
    _write_json,
)
from scripts.walk_forward_validate import build_walkforward_reports


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _replay_candidates(case_path: Path, candidates_dir: Path, out_csv: Path, min_trades: int, max_dd: float) -> None:
    cmd = [
        sys.executable,
        "-m",
        "src.optimizer_v0",
        "replay-candidates",
        "--case",
        str(case_path),
        "--candidates-dir",
        str(candidates_dir),
        "--out",
        str(out_csv),
        "--min-trades",
        str(min_trades),
        "--max-dd",
        str(max_dd),
    ]
    _run_checked(cmd, cwd=PROJECT_ROOT, step=f"replay_{out_csv.stem}")


def _ensure_sl_summary(
    *,
    run_dir: Path,
    target2_case: Path,
    min_trades: int,
    max_dd: float,
) -> dict[str, Any]:
    sl_dir = run_dir / "runs" / "sl_joint"
    summary_path = sl_dir / "summary.json"
    if summary_path.exists():
        return _read_json(summary_path)

    replay_target2 = sl_dir / "replay_target2.csv"
    replay_target2_manual = sl_dir / "replay_target2_manual.csv"
    candidates_dir = sl_dir / "candidates"
    if replay_target2_manual.exists() and not replay_target2.exists():
        shutil.copyfile(replay_target2_manual, replay_target2)
    elif not replay_target2.exists():
        _replay_candidates(target2_case, candidates_dir, replay_target2, min_trades, max_dd)

    build_walkforward_reports(sl_dir)
    return _read_json(summary_path)


def _finalize(run_dir: Path, state: dict[str, Any]) -> None:
    best = _best_stage(state["stages"])
    final_payload = {
        "status": "PASS",
        "baseline": state.get("baseline"),
        "stages": state["stages"],
        "recommended_stage": best["stage"],
        "recommended_case_path": best["case_path"],
        "recommended_metrics": best["full_run"],
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    state["status"] = "PASS"
    state["recommended_stage"] = best["stage"]
    state["recommended_case_path"] = best["case_path"]
    _write_json(run_dir / "state.json", state)
    _write_json(run_dir / "final_summary.json", final_payload)


def main() -> int:
    ap = argparse.ArgumentParser(description="Resume a failed broad Supertrend 4h overnight run.")
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--workers", type=int, default=18)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--sl-iters", type=int, default=2200)
    ap.add_argument("--tp-iters", type=int, default=1600)
    ap.add_argument("--mtp-iters", type=int, default=1200)
    ap.add_argument("--min-trades", type=int, default=5)
    ap.add_argument("--max-dd", type=float, default=85.0)
    ap.add_argument("--top-k", type=int, default=100)
    args = ap.parse_args()

    run_dir = Path(args.run_dir).resolve()
    state_path = run_dir / "state.json"
    if not state_path.exists():
        raise FileNotFoundError(f"State file not found: {state_path}")

    state = _read_json(state_path)
    work_cases = run_dir / "cases"
    work_runs = run_dir / "runs"
    work_eval = run_dir / "evaluations"

    try:
        confirm_cases = {
            "full": work_cases / "confirm_guards_full.json",
            "train": work_cases / "confirm_guards_train.json",
            "target1": work_cases / "confirm_guards_target1.json",
            "target2": work_cases / "confirm_guards_target2.json",
        }
        for path in confirm_cases.values():
            if not path.exists():
                raise FileNotFoundError(f"Missing prerequisite confirm_guards case: {path}")

        sl_summary = _ensure_sl_summary(
            run_dir=run_dir,
            target2_case=confirm_cases["target2"],
            min_trades=args.min_trades,
            max_dd=args.max_dd,
        )
        sl_candidate = _candidate_path(work_runs / "sl_joint", sl_summary, "sl_joint")
        sl_cases = _materialize_family(
            base_full=confirm_cases["full"],
            base_train=confirm_cases["train"],
            base_target1=confirm_cases["target1"],
            base_target2=confirm_cases["target2"],
            candidate=sl_candidate,
            work_cases=work_cases,
            prefix="sl",
        )
        sl_full_results = _backtest_case(sl_cases["full"], work_eval / "sl_full", "sl_full_backtest")
        state["stages"].append(_stage_record("sl_joint", sl_summary, sl_full_results, sl_cases["full"]))
        _write_json(state_path, state)

        tp_dir = work_runs / "tp_joint"
        tp_summary = _walkforward(
            train_case=sl_cases["train"],
            target1_case=sl_cases["target1"],
            target2_case=sl_cases["target2"],
            mode="random",
            iters=args.tp_iters,
            seed=args.seed + 300,
            workers=args.workers,
            min_trades=args.min_trades,
            max_dd=args.max_dd,
            top_k=args.top_k,
            space_file=DEFAULT_TP_SPACE,
            outdir=tp_dir,
        )
        tp_candidate = _candidate_path(tp_dir, tp_summary, "tp_joint")
        tp_cases = _materialize_family(
            base_full=sl_cases["full"],
            base_train=sl_cases["train"],
            base_target1=sl_cases["target1"],
            base_target2=sl_cases["target2"],
            candidate=tp_candidate,
            work_cases=work_cases,
            prefix="tp",
        )
        tp_full_results = _backtest_case(tp_cases["full"], work_eval / "tp_full", "tp_full_backtest")
        state["stages"].append(_stage_record("tp_joint", tp_summary, tp_full_results, tp_cases["full"]))
        _write_json(state_path, state)

        mtp_dir = work_runs / "multi_tp_joint"
        mtp_summary = _walkforward(
            train_case=tp_cases["train"],
            target1_case=tp_cases["target1"],
            target2_case=tp_cases["target2"],
            mode="random",
            iters=args.mtp_iters,
            seed=args.seed + 350,
            workers=args.workers,
            min_trades=args.min_trades,
            max_dd=args.max_dd,
            top_k=args.top_k,
            space_file=DEFAULT_MULTI_TP_SPACE,
            outdir=mtp_dir,
        )
        mtp_candidate = _candidate_path(mtp_dir, mtp_summary, "multi_tp_joint")
        mtp_cases = _materialize_family(
            base_full=tp_cases["full"],
            base_train=tp_cases["train"],
            base_target1=tp_cases["target1"],
            base_target2=tp_cases["target2"],
            candidate=mtp_candidate,
            work_cases=work_cases,
            prefix="multi_tp",
        )
        mtp_full_results = _backtest_case(mtp_cases["full"], work_eval / "multi_tp_full", "multi_tp_full_backtest")
        state["stages"].append(_stage_record("multi_tp_joint", mtp_summary, mtp_full_results, mtp_cases["full"]))
        _write_json(state_path, state)

        be_dir = work_runs / "be_grid"
        be_summary = _walkforward(
            train_case=mtp_cases["train"],
            target1_case=mtp_cases["target1"],
            target2_case=mtp_cases["target2"],
            mode="grid",
            iters=0,
            seed=args.seed + 400,
            workers=args.workers,
            min_trades=args.min_trades,
            max_dd=args.max_dd,
            top_k=args.top_k,
            space_file=DEFAULT_BE_SPACE,
            outdir=be_dir,
        )
        be_candidate = _candidate_path(be_dir, be_summary, "be_grid")
        be_cases = _materialize_family(
            base_full=mtp_cases["full"],
            base_train=mtp_cases["train"],
            base_target1=mtp_cases["target1"],
            base_target2=mtp_cases["target2"],
            candidate=be_candidate,
            work_cases=work_cases,
            prefix="be",
        )
        be_full_results = _backtest_case(be_cases["full"], work_eval / "be_full", "be_full_backtest")
        state["stages"].append(_stage_record("be_grid", be_summary, be_full_results, be_cases["full"]))
        _write_json(state_path, state)

        trail_dir = work_runs / "trailing_grid"
        trail_summary = _walkforward(
            train_case=be_cases["train"],
            target1_case=be_cases["target1"],
            target2_case=be_cases["target2"],
            mode="grid",
            iters=0,
            seed=args.seed + 500,
            workers=args.workers,
            min_trades=args.min_trades,
            max_dd=args.max_dd,
            top_k=args.top_k,
            space_file=DEFAULT_TRAIL_SPACE,
            outdir=trail_dir,
        )
        trail_candidate = _candidate_path(trail_dir, trail_summary, "trailing_grid")
        trail_cases = _materialize_family(
            base_full=be_cases["full"],
            base_train=be_cases["train"],
            base_target1=be_cases["target1"],
            base_target2=be_cases["target2"],
            candidate=trail_candidate,
            work_cases=work_cases,
            prefix="trailing",
        )
        trail_full_results = _backtest_case(trail_cases["full"], work_eval / "trailing_full", "trailing_full_backtest")
        state["stages"].append(_stage_record("trailing_grid", trail_summary, trail_full_results, trail_cases["full"]))
        _finalize(run_dir, state)
        print("resume_status=PASS")
        print(f"run_dir={run_dir}")
        return 0
    except Exception as exc:
        state["status"] = "FAIL"
        state["error"] = str(exc)
        _write_json(state_path, state)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
