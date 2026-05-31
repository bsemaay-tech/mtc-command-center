from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DEFAULT_CASE_FULL = PROJECT_ROOT / "configs" / "cases" / "supertrend_4h_full_20260310.json"
DEFAULT_CASE_TRAIN = PROJECT_ROOT / "configs" / "cases" / "supertrend_4h_wf_train_20260310.json"
DEFAULT_CASE_TARGET1 = PROJECT_ROOT / "configs" / "cases" / "supertrend_4h_wf_target1_20260310.json"
DEFAULT_CASE_TARGET2 = PROJECT_ROOT / "configs" / "cases" / "supertrend_4h_wf_target2_20260310.json"
DEFAULT_SIGNAL_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_4h_signal_broad_20260310.json"
DEFAULT_FILTERS_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_4h_filters_broad_20260311.json"
DEFAULT_CONFIRM_GUARDS_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_4h_confirmation_guards_20260311.json"
DEFAULT_SL_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_4h_sl_joint_20260310.json"
DEFAULT_TP_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_4h_tp_joint_20260310.json"
DEFAULT_MULTI_TP_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_4h_multi_tp_20260311.json"
DEFAULT_BE_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_4h_be_20260310.json"
DEFAULT_TRAIL_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_4h_trailing_20260310.json"
DEFAULT_OBJECTIVES = "net_profit,max_dd_pct,profit_factor,win_rate,total_trades"
DEFAULT_CANDIDATE_SOURCE = "train_top_score"


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return str(path.resolve())


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _run(cmd: list[str], *, cwd: Path) -> int:
    print(f"$ {' '.join(cmd)}", flush=True)
    proc = subprocess.Popen(cmd, cwd=str(cwd))
    return proc.wait()


def _run_checked(cmd: list[str], *, cwd: Path, step: str) -> None:
    rc = _run(cmd, cwd=cwd)
    if rc != 0:
        raise RuntimeError(f"{step} failed with exit code {rc}")


def _materialize(base_case: Path, candidate: Path, out_case: Path, tag: str) -> Path:
    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "scripts" / "materialize_candidate_case.py"),
        "--base-case",
        str(base_case),
        "--candidate",
        str(candidate),
        "--out-case",
        str(out_case),
        "--tag",
        tag,
    ]
    _run_checked(cmd, cwd=PROJECT_ROOT, step=f"materialize_{tag}")
    return out_case


def _materialize_family(
    *,
    base_full: Path,
    base_train: Path,
    base_target1: Path,
    base_target2: Path,
    candidate: Path,
    work_cases: Path,
    prefix: str,
) -> dict[str, Path]:
    return {
        "full": _materialize(base_full, candidate, work_cases / f"{prefix}_full.json", f"{prefix}_full"),
        "train": _materialize(base_train, candidate, work_cases / f"{prefix}_train.json", f"{prefix}_train"),
        "target1": _materialize(base_target1, candidate, work_cases / f"{prefix}_target1.json", f"{prefix}_target1"),
        "target2": _materialize(base_target2, candidate, work_cases / f"{prefix}_target2.json", f"{prefix}_target2"),
    }


def _build_signal_refine_space(candidate_file: Path, out_path: Path) -> Path:
    candidate = _read_json(candidate_file)
    params = candidate.get("params", {})
    atr = int(params.get("supertrend.atr_len", 21))
    factor = float(params.get("supertrend.factor", 4.0))
    atr_low = max(5, atr - 5)
    atr_high = atr + 5
    factor_low = max(1.0, round(factor - 0.6, 2))
    factor_high = round(factor + 0.6, 2)
    steps = int(round((factor_high - factor_low) / 0.1))

    payload = {
        "grid": {
            "supertrend.atr_len": {
                "dtype": "int",
                "values": list(range(atr_low, atr_high + 1)),
            },
            "supertrend.factor": {
                "dtype": "float",
                "values": [round(factor_low + i * 0.1, 2) for i in range(steps + 1)],
            },
            "supertrend.use_wicks": {
                "values": [False, True],
            },
            "supertrend.use_ha": {
                "values": [False, True],
            },
        }
    }
    _write_json(out_path, payload)
    return out_path


def _backtest_case(case_path: Path, artifacts_dir: Path, step: str) -> dict[str, Any]:
    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "scripts" / "run_case.py"),
        str(case_path),
        "--artifacts-dir",
        str(artifacts_dir),
    ]
    _run_checked(cmd, cwd=PROJECT_ROOT, step=step)
    return _read_json(artifacts_dir / "results.json")


def _walkforward(
    *,
    train_case: Path,
    target1_case: Path,
    target2_case: Path,
    mode: str,
    iters: int,
    seed: int,
    workers: int,
    min_trades: int,
    max_dd: float,
    top_k: int,
    space_file: Path,
    outdir: Path,
) -> dict[str, Any]:
    cmd = [
        sys.executable,
        "-m",
        "scripts.walk_forward_validate",
        "--train-case",
        _rel(train_case),
        "--target-case-1",
        _rel(target1_case),
        "--target-case-2",
        _rel(target2_case),
        "--mode",
        mode,
        "--iters",
        str(iters),
        "--seed",
        str(seed),
        "--workers",
        str(workers),
        "--min-trades",
        str(min_trades),
        "--max-dd",
        str(max_dd),
        "--space-file",
        _rel(space_file),
        "--objectives",
        DEFAULT_OBJECTIVES,
        "--top-k",
        str(top_k),
        "--candidate-source",
        DEFAULT_CANDIDATE_SOURCE,
        "--outdir",
        str(outdir),
    ]
    _run_checked(cmd, cwd=PROJECT_ROOT, step=f"walkforward_{outdir.name}")
    return _read_json(outdir / "summary.json")


def _candidate_path(run_dir: Path, summary: dict[str, Any], step: str) -> Path:
    if summary.get("status") != "OK" or not summary.get("best_candidate_file"):
        raise RuntimeError(f"{step} did not produce a valid candidate: {summary}")
    candidate = run_dir / "candidates" / str(summary["best_candidate_file"])
    if not candidate.exists():
        raise RuntimeError(f"{step} candidate file missing: {candidate}")
    return candidate


def _stage_record(stage: str, wf_summary: dict[str, Any] | None, full_results: dict[str, Any], case_path: Path) -> dict[str, Any]:
    metrics = full_results.get("metrics", {})
    payload = {
        "stage": stage,
        "case_path": str(case_path),
        "full_run": {
            "net_profit": metrics.get("net_profit"),
            "net_profit_pct": metrics.get("net_profit_pct"),
            "max_drawdown": metrics.get("max_drawdown"),
            "profit_factor": metrics.get("profit_factor"),
            "win_rate": metrics.get("win_rate"),
            "total_trades": metrics.get("total_trades"),
        },
    }
    if wf_summary is not None:
        payload["walkforward"] = {
            "ok_candidates": wf_summary.get("ok_candidates"),
            "best_candidate_file": wf_summary.get("best_candidate_file"),
            "best_net_sum": wf_summary.get("best_net_sum"),
            "best_dd_max": wf_summary.get("best_dd_max"),
        }
    return payload


def _best_stage(stages: list[dict[str, Any]]) -> dict[str, Any]:
    return sorted(
        stages,
        key=lambda item: (
            float(item["full_run"].get("net_profit") or float("-inf")),
            -float(item["full_run"].get("max_drawdown") or float("inf")),
            float(item["full_run"].get("profit_factor") or 0.0),
        ),
        reverse=True,
    )[0]


def main() -> int:
    ap = argparse.ArgumentParser(description="Run broad Supertrend 4h optimization workflow on BTCUSDT.P.")
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--signal-iters", type=int, default=4000)
    ap.add_argument("--filters-iters", type=int, default=4000)
    ap.add_argument("--confirm-iters", type=int, default=3000)
    ap.add_argument("--sl-iters", type=int, default=2200)
    ap.add_argument("--tp-iters", type=int, default=1600)
    ap.add_argument("--mtp-iters", type=int, default=1200)
    ap.add_argument("--min-trades", type=int, default=5)
    ap.add_argument("--max-dd", type=float, default=85.0)
    ap.add_argument("--top-k", type=int, default=100)
    ap.add_argument("--outdir", default="")
    args = ap.parse_args()

    stamp = time.strftime("%Y%m%d_%H%M%S")
    outdir = (PROJECT_ROOT / args.outdir).resolve() if args.outdir else (PROJECT_ROOT / "results" / "overnight" / f"supertrend_4h_broad_{stamp}").resolve()
    work_cases = outdir / "cases"
    work_spaces = outdir / "spaces"
    work_runs = outdir / "runs"
    work_eval = outdir / "evaluations"
    for path in (outdir, work_cases, work_spaces, work_runs, work_eval):
        path.mkdir(parents=True, exist_ok=True)

    state_path = outdir / "state.json"
    final_path = outdir / "final_summary.json"
    state: dict[str, Any] = {
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "outdir": str(outdir),
        "workers": args.workers,
        "seed": args.seed,
        "stages": [],
        "status": "RUNNING",
    }
    _write_json(state_path, state)

    try:
        baseline_results = _backtest_case(DEFAULT_CASE_FULL, work_eval / "baseline", "baseline_backtest")
        state["baseline"] = _stage_record("baseline", None, baseline_results, DEFAULT_CASE_FULL)
        _write_json(state_path, state)

        signal_dir = work_runs / "signal_broad"
        signal_summary = _walkforward(
            train_case=DEFAULT_CASE_TRAIN,
            target1_case=DEFAULT_CASE_TARGET1,
            target2_case=DEFAULT_CASE_TARGET2,
            mode="random",
            iters=args.signal_iters,
            seed=args.seed,
            workers=args.workers,
            min_trades=args.min_trades,
            max_dd=args.max_dd,
            top_k=args.top_k,
            space_file=DEFAULT_SIGNAL_SPACE,
            outdir=signal_dir,
        )
        signal_candidate = _candidate_path(signal_dir, signal_summary, "signal_broad")
        signal_cases = _materialize_family(
            base_full=DEFAULT_CASE_FULL,
            base_train=DEFAULT_CASE_TRAIN,
            base_target1=DEFAULT_CASE_TARGET1,
            base_target2=DEFAULT_CASE_TARGET2,
            candidate=signal_candidate,
            work_cases=work_cases,
            prefix="signal_broad",
        )
        signal_full_results = _backtest_case(signal_cases["full"], work_eval / "signal_broad_full", "signal_broad_full_backtest")
        state["stages"].append(_stage_record("signal_broad", signal_summary, signal_full_results, signal_cases["full"]))
        _write_json(state_path, state)

        refine_space = _build_signal_refine_space(signal_candidate, work_spaces / "signal_refine.json")
        refine_dir = work_runs / "signal_refine"
        refine_summary = _walkforward(
            train_case=signal_cases["train"],
            target1_case=signal_cases["target1"],
            target2_case=signal_cases["target2"],
            mode="grid",
            iters=0,
            seed=args.seed,
            workers=args.workers,
            min_trades=args.min_trades,
            max_dd=args.max_dd,
            top_k=args.top_k,
            space_file=refine_space,
            outdir=refine_dir,
        )
        refine_candidate = _candidate_path(refine_dir, refine_summary, "signal_refine")
        refine_cases = _materialize_family(
            base_full=signal_cases["full"],
            base_train=signal_cases["train"],
            base_target1=signal_cases["target1"],
            base_target2=signal_cases["target2"],
            candidate=refine_candidate,
            work_cases=work_cases,
            prefix="signal_refine",
        )
        refine_full_results = _backtest_case(refine_cases["full"], work_eval / "signal_refine_full", "signal_refine_full_backtest")
        state["stages"].append(_stage_record("signal_refine", refine_summary, refine_full_results, refine_cases["full"]))
        _write_json(state_path, state)

        filters_dir = work_runs / "filters_broad"
        filters_summary = _walkforward(
            train_case=refine_cases["train"],
            target1_case=refine_cases["target1"],
            target2_case=refine_cases["target2"],
            mode="random",
            iters=args.filters_iters,
            seed=args.seed + 100,
            workers=args.workers,
            min_trades=args.min_trades,
            max_dd=args.max_dd,
            top_k=args.top_k,
            space_file=DEFAULT_FILTERS_SPACE,
            outdir=filters_dir,
        )
        filters_candidate = _candidate_path(filters_dir, filters_summary, "filters_broad")
        filters_cases = _materialize_family(
            base_full=refine_cases["full"],
            base_train=refine_cases["train"],
            base_target1=refine_cases["target1"],
            base_target2=refine_cases["target2"],
            candidate=filters_candidate,
            work_cases=work_cases,
            prefix="filters_broad",
        )
        filters_full_results = _backtest_case(filters_cases["full"], work_eval / "filters_broad_full", "filters_broad_full_backtest")
        state["stages"].append(_stage_record("filters_broad", filters_summary, filters_full_results, filters_cases["full"]))
        _write_json(state_path, state)

        confirm_dir = work_runs / "confirm_guards"
        confirm_summary = _walkforward(
            train_case=filters_cases["train"],
            target1_case=filters_cases["target1"],
            target2_case=filters_cases["target2"],
            mode="random",
            iters=args.confirm_iters,
            seed=args.seed + 150,
            workers=args.workers,
            min_trades=args.min_trades,
            max_dd=args.max_dd,
            top_k=args.top_k,
            space_file=DEFAULT_CONFIRM_GUARDS_SPACE,
            outdir=confirm_dir,
        )
        confirm_candidate = _candidate_path(confirm_dir, confirm_summary, "confirm_guards")
        confirm_cases = _materialize_family(
            base_full=filters_cases["full"],
            base_train=filters_cases["train"],
            base_target1=filters_cases["target1"],
            base_target2=filters_cases["target2"],
            candidate=confirm_candidate,
            work_cases=work_cases,
            prefix="confirm_guards",
        )
        confirm_full_results = _backtest_case(confirm_cases["full"], work_eval / "confirm_guards_full", "confirm_guards_full_backtest")
        state["stages"].append(_stage_record("confirm_guards", confirm_summary, confirm_full_results, confirm_cases["full"]))
        _write_json(state_path, state)

        sl_dir = work_runs / "sl_joint"
        sl_summary = _walkforward(
            train_case=confirm_cases["train"],
            target1_case=confirm_cases["target1"],
            target2_case=confirm_cases["target2"],
            mode="random",
            iters=args.sl_iters,
            seed=args.seed + 200,
            workers=args.workers,
            min_trades=args.min_trades,
            max_dd=args.max_dd,
            top_k=args.top_k,
            space_file=DEFAULT_SL_SPACE,
            outdir=sl_dir,
        )
        sl_candidate = _candidate_path(sl_dir, sl_summary, "sl_joint")
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
        _write_json(state_path, state)
        _write_json(final_path, final_payload)

        print("overnight_status=PASS")
        print(f"outdir={outdir}")
        print(f"recommended_stage={best['stage']}")
        print(f"recommended_case={best['case_path']}")
        return 0
    except Exception as exc:
        state["status"] = "FAIL"
        state["error"] = str(exc)
        _write_json(state_path, state)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
