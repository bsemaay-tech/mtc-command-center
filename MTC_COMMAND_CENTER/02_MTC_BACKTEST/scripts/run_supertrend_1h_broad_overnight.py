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
DEFAULT_CASE_FULL = PROJECT_ROOT / "configs" / "cases" / "supertrend_1h_full_20260312.json"
DEFAULT_SIGNAL_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_4h_signal_broad_20260310.json"
DEFAULT_FILTERS_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_1h_filters_broad_20260312.json"
DEFAULT_TRADE_TIME_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_1h_trade_time_session_20260312.json"
DEFAULT_CONFIRM_GUARDS_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_1h_confirmation_guards_20260312.json"
DEFAULT_SL_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_4h_sl_joint_20260310.json"
DEFAULT_TP_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_4h_tp_joint_20260310.json"
DEFAULT_MULTI_TP_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_4h_multi_tp_20260311.json"
DEFAULT_BE_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_4h_be_20260310.json"
DEFAULT_TRAIL_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_4h_trailing_20260310.json"
DEFAULT_DATASET = "C:/LAB/tradingview-lab/110_/data/processed_hist/binance_usdm/BTCUSDT.P/1h.parquet"
DEFAULT_EVAL_START = "2020-01-01T00:00:00"
DEFAULT_EVAL_END = "2026-01-01T00:00:00"
DEFAULT_HOLDOUT_START = "2026-01-01T00:00:00"
DEFAULT_HOLDOUT_END = "2026-03-12T23:59:59"


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


def _window_optimize(
    *,
    base_case: Path,
    space_file: Path,
    mode: str,
    iters: int,
    seed: int,
    workers: int,
    min_trades_per_window: int,
    min_total_trades: int,
    min_profitable_windows: int,
    max_dd: float,
    top_k: int,
    outdir: Path,
    dataset: str,
    eval_start: str,
    eval_end: str,
    holdout_start: str,
    holdout_end: str,
) -> dict[str, Any]:
    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "scripts" / "run_supertrend_windowed_optimization.py"),
        "--base-case",
        str(base_case),
        "--space-file",
        str(space_file),
        "--dataset",
        dataset,
        "--eval-start",
        eval_start,
        "--eval-end",
        eval_end,
        "--window-months",
        "6",
        "--require-full-windows",
        "--holdout-start",
        holdout_start,
        "--holdout-end",
        holdout_end,
        "--mode",
        mode,
        "--iters",
        str(iters),
        "--seed",
        str(seed),
        "--workers",
        str(workers),
        "--min-trades-per-window",
        str(min_trades_per_window),
        "--min-total-trades",
        str(min_total_trades),
        "--min-profitable-windows",
        str(min_profitable_windows),
        "--max-dd",
        str(max_dd),
        "--top-k",
        str(top_k),
        "--outdir",
        str(outdir),
    ]
    _run_checked(cmd, cwd=PROJECT_ROOT, step=f"window_optimize_{outdir.name}")
    return _read_json(outdir / "summary.json")


def _candidate_path(summary: dict[str, Any], step: str) -> Path:
    if summary.get("status") != "PASS" or not summary.get("best_candidate_path"):
        raise RuntimeError(f"{step} did not produce a valid candidate: {summary}")
    candidate = Path(str(summary["best_candidate_path"])).resolve()
    if not candidate.exists():
        raise RuntimeError(f"{step} candidate file missing: {candidate}")
    return candidate


def _stage_record(stage: str, opt_summary: dict[str, Any] | None, full_results: dict[str, Any], case_path: Path) -> dict[str, Any]:
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
    if opt_summary is not None:
        payload["window_optimization"] = {
            "ok_trials": opt_summary.get("ok_trials"),
            "scheduled_trials": opt_summary.get("scheduled_trials"),
            "best_candidate_path": opt_summary.get("best_candidate_path"),
            "best_score": opt_summary.get("best_score"),
            "best_metrics": opt_summary.get("best_metrics"),
            "windows": opt_summary.get("windows"),
        }
        payload["holdout_run"] = (opt_summary.get("holdout_result") or {}).get("metrics")
    return payload


def _best_stage(stages: list[dict[str, Any]]) -> dict[str, Any]:
    def sort_key(item: dict[str, Any]) -> tuple[float, float, float, float]:
        holdout = item.get("holdout_run") or {}
        full_run = item.get("full_run") or {}
        return (
            float(holdout.get("net_profit") or float("-inf")),
            float(full_run.get("net_profit") or float("-inf")),
            -float((holdout.get("max_drawdown_pct") or holdout.get("max_drawdown") or float("inf"))),
            float(holdout.get("profit_factor") or 0.0),
        )

    return sorted(stages, key=sort_key, reverse=True)[0]


def main() -> int:
    ap = argparse.ArgumentParser(description="Run broad Supertrend 1h multi-window optimization workflow on BTCUSDT.P.")
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 4) - 2))
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--signal-iters", type=int, default=900)
    ap.add_argument("--filters-iters", type=int, default=1000)
    ap.add_argument("--trade-time-iters", type=int, default=900)
    ap.add_argument("--confirm-iters", type=int, default=900)
    ap.add_argument("--sl-iters", type=int, default=1000)
    ap.add_argument("--tp-iters", type=int, default=700)
    ap.add_argument("--mtp-iters", type=int, default=500)
    ap.add_argument("--min-trades-per-window", type=int, default=2)
    ap.add_argument("--min-total-trades", type=int, default=80)
    ap.add_argument("--min-profitable-windows", type=int, default=6)
    ap.add_argument("--max-dd", type=float, default=40.0)
    ap.add_argument("--top-k", type=int, default=40)
    ap.add_argument("--dataset", default=DEFAULT_DATASET)
    ap.add_argument("--eval-start", default=DEFAULT_EVAL_START)
    ap.add_argument("--eval-end", default=DEFAULT_EVAL_END)
    ap.add_argument("--holdout-start", default=DEFAULT_HOLDOUT_START)
    ap.add_argument("--holdout-end", default=DEFAULT_HOLDOUT_END)
    ap.add_argument("--outdir", default="")
    args = ap.parse_args()

    stamp = time.strftime("%Y%m%d_%H%M%S")
    outdir = (PROJECT_ROOT / args.outdir).resolve() if args.outdir else (PROJECT_ROOT / "results" / "overnight" / f"supertrend_1h_broad_{stamp}").resolve()
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
        "dataset": args.dataset,
        "eval_start": args.eval_start,
        "eval_end": args.eval_end,
        "holdout_start": args.holdout_start,
        "holdout_end": args.holdout_end,
        "stages": [],
        "status": "RUNNING",
    }
    _write_json(state_path, state)

    try:
        baseline_results = _backtest_case(DEFAULT_CASE_FULL, work_eval / "baseline", "baseline_backtest")
        state["baseline"] = _stage_record("baseline", None, baseline_results, DEFAULT_CASE_FULL)
        _write_json(state_path, state)

        current_case = DEFAULT_CASE_FULL
        stage_specs = [
            ("signal_broad", DEFAULT_SIGNAL_SPACE, "random", args.signal_iters, args.seed),
            ("signal_refine", None, "grid", 0, args.seed + 50),
            ("filters_broad", DEFAULT_FILTERS_SPACE, "random", args.filters_iters, args.seed + 100),
            ("trade_time_session", DEFAULT_TRADE_TIME_SPACE, "random", args.trade_time_iters, args.seed + 130),
            ("confirm_guards", DEFAULT_CONFIRM_GUARDS_SPACE, "random", args.confirm_iters, args.seed + 150),
            ("sl_joint", DEFAULT_SL_SPACE, "random", args.sl_iters, args.seed + 200),
            ("tp_joint", DEFAULT_TP_SPACE, "random", args.tp_iters, args.seed + 300),
            ("multi_tp_joint", DEFAULT_MULTI_TP_SPACE, "random", args.mtp_iters, args.seed + 350),
            ("be_grid", DEFAULT_BE_SPACE, "grid", 0, args.seed + 400),
            ("trailing_grid", DEFAULT_TRAIL_SPACE, "grid", 0, args.seed + 500),
        ]

        signal_candidate: Path | None = None
        for stage_name, default_space, mode, iters, seed in stage_specs:
            run_dir = work_runs / stage_name
            if stage_name == "signal_refine":
                if signal_candidate is None:
                    raise RuntimeError("signal_refine requires signal candidate")
                space_file = _build_signal_refine_space(signal_candidate, work_spaces / "signal_refine.json")
            else:
                space_file = default_space
            if space_file is None:
                raise RuntimeError(f"No space file configured for {stage_name}")

            summary = _window_optimize(
                base_case=current_case,
                space_file=space_file,
                mode=mode,
                iters=iters,
                seed=seed,
                workers=args.workers,
                min_trades_per_window=args.min_trades_per_window,
                min_total_trades=args.min_total_trades,
                min_profitable_windows=args.min_profitable_windows,
                max_dd=args.max_dd,
                top_k=args.top_k,
                outdir=run_dir,
                dataset=args.dataset,
                eval_start=args.eval_start,
                eval_end=args.eval_end,
                holdout_start=args.holdout_start,
                holdout_end=args.holdout_end,
            )
            candidate = _candidate_path(summary, stage_name)
            if stage_name == "signal_broad":
                signal_candidate = candidate
            out_case = work_cases / f"{stage_name}_full.json"
            current_case = _materialize(current_case, candidate, out_case, f"{stage_name}_full")
            full_results = _backtest_case(current_case, work_eval / f"{stage_name}_full", f"{stage_name}_full_backtest")
            state["stages"].append(_stage_record(stage_name, summary, full_results, current_case))
            _write_json(state_path, state)

        best = _best_stage(state["stages"])
        final_payload = {
            "status": "PASS",
            "baseline": state.get("baseline"),
            "stages": state["stages"],
            "recommended_stage": best["stage"],
            "recommended_case_path": best["case_path"],
            "recommended_metrics": best["full_run"],
            "recommended_holdout_metrics": best.get("holdout_run"),
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
