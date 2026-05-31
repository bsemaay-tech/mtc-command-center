from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd
from pandas.errors import EmptyDataError


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TRAIN_CASE = "configs/cases/supertrend_tp_wf_train_20260309.json"
DEFAULT_TARGET1_CASE = "configs/cases/supertrend_tp_wf_target1_20260309.json"
DEFAULT_TARGET2_CASE = "configs/cases/supertrend_tp_wf_target2_20260309.json"
PROFILE_SPACE_FILES = {
    "atr": "configs/spaces/supertrend_tp_walkforward_atr_20260309.json",
    "pct": "configs/spaces/supertrend_tp_walkforward_pct_20260309.json",
    "r": "configs/spaces/supertrend_tp_walkforward_r_20260309.json",
}
DEFAULT_OBJECTIVES = "net_profit,max_dd_pct,profit_factor,win_rate,total_trades"


def resolve_space_file(profile: str, override: str) -> str:
    if override:
        return override
    try:
        return PROFILE_SPACE_FILES[profile]
    except KeyError as exc:
        raise ValueError(f"Unknown profile: {profile}") from exc


def build_command(args: argparse.Namespace, outdir: Path, space_file: str) -> list[str]:
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
        space_file,
        "--objectives",
        args.objectives,
        "--top-k",
        str(args.top_k),
        "--candidate-source",
        args.candidate_source,
        "--outdir",
        str(outdir),
    ]


def run_profile(profile: str, args: argparse.Namespace, outdir: Path) -> int:
    space_file = resolve_space_file(profile, args.space_file if args.profile != "all" else "")
    cmd = build_command(args, outdir, space_file)
    print(f"TP walk-forward profile: {profile}")
    print(f"  space_file : {space_file}")
    print(f"  outdir     : {outdir}")
    if args.dry_run:
        print("  command    :")
        print(" ".join(cmd))
        return 0
    outdir.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
    return int(result.returncode)


def write_aggregate(base_outdir: Path, rows: list[dict]) -> tuple[Path, Path, Path]:
    csv_path = base_outdir / "tp_profile_summary.csv"
    json_path = base_outdir / "tp_profile_summary.json"
    xlsx_path = base_outdir / "tp_profile_summary.xlsx"
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values(
            ["wf_net_sum", "wf_dd_max", "profile"],
            ascending=[False, True, True],
        ).reset_index(drop=True)
    df.to_csv(csv_path, index=False)
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="summary")
    json_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    return csv_path, json_path, xlsx_path


def load_profile_summary(profile: str, outdir: Path) -> dict:
    summary_path = outdir / "summary.json"
    ranking_path = outdir / "ranking.csv"
    payload = {"profile": profile, "outdir": str(outdir)}
    if not summary_path.exists():
        payload["status"] = "MISSING_SUMMARY"
        return payload

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    payload.update(
        {
            "status": summary.get("status"),
            "ok_candidates": summary.get("ok_candidates", 0),
            "wf_net_sum": summary.get("best_net_sum"),
            "wf_dd_max": summary.get("best_dd_max"),
            "best_candidate_file": summary.get("best_candidate_file"),
        }
    )
    if ranking_path.exists():
        try:
            df = pd.read_csv(ranking_path)
        except EmptyDataError:
            df = pd.DataFrame()
        if not df.empty:
            top = df.iloc[0].to_dict()
            payload["target1_net_profit"] = top.get("net_profit_1")
            payload["target1_dd_pct"] = top.get("max_dd_pct_1")
            payload["target2_net_profit"] = top.get("net_profit_2")
            payload["target2_dd_pct"] = top.get("max_dd_pct_2")
            payload["candidate_file"] = top.get("candidate_file")
            candidate_name = top.get("candidate_file")
            if candidate_name:
                candidate_path = outdir / "candidates" / str(candidate_name)
                if candidate_path.exists():
                    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
                    take_profit = candidate.get("config", {}).get("take_profit", {})
                    params = candidate.get("params", {})
                    payload["take_profit.mode"] = take_profit.get("mode", params.get("take_profit.mode"))
                    payload["take_profit.percent"] = take_profit.get("percent", params.get("take_profit.percent"))
                    payload["take_profit.rr"] = take_profit.get("rr", params.get("take_profit.rr"))
                    payload["take_profit.atr_len"] = take_profit.get("atr_len", params.get("take_profit.atr_len"))
                    payload["take_profit.atr_mult"] = take_profit.get("atr_mult", params.get("take_profit.atr_mult"))
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Supertrend take-profit walk-forward optimization.")
    parser.add_argument("--train-case", default=DEFAULT_TRAIN_CASE)
    parser.add_argument("--target-case-1", default=DEFAULT_TARGET1_CASE)
    parser.add_argument("--target-case-2", default=DEFAULT_TARGET2_CASE)
    parser.add_argument("--profile", choices=[*sorted(PROFILE_SPACE_FILES.keys()), "all"], default="all")
    parser.add_argument("--space-file", default="")
    parser.add_argument("--mode", choices=["grid", "random", "bayes"], default="grid")
    parser.add_argument("--iters", type=int, default=250)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 1) - 1))
    parser.add_argument("--min-trades", type=int, default=10)
    parser.add_argument("--max-dd", type=float, default=80.0)
    parser.add_argument("--top-k", type=int, default=30)
    parser.add_argument("--objectives", default=DEFAULT_OBJECTIVES)
    parser.add_argument("--candidate-source", choices=["pareto", "train_top_score"], default="train_top_score")
    parser.add_argument("--outdir", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    profiles = sorted(PROFILE_SPACE_FILES.keys()) if args.profile == "all" else [args.profile]
    if args.outdir:
        base_outdir = (PROJECT_ROOT / args.outdir).resolve()
    else:
        stamp = time.strftime("%Y%m%d_%H%M%S")
        base_outdir = (PROJECT_ROOT / "results" / "walkforward" / f"supertrend_tp_{stamp}").resolve()

    if args.profile != "all":
        profile = profiles[0]
        target_outdir = base_outdir
        return run_profile(profile, args, target_outdir)

    rows: list[dict] = []
    if not args.dry_run:
        base_outdir.mkdir(parents=True, exist_ok=True)
    exit_code = 0
    for profile in profiles:
        profile_outdir = base_outdir / profile
        rc = run_profile(profile, args, profile_outdir)
        if rc != 0:
            exit_code = rc
            break
        if not args.dry_run:
            rows.append(load_profile_summary(profile, profile_outdir))

    if rows:
        csv_path, json_path, xlsx_path = write_aggregate(base_outdir, rows)
        print(f"Aggregate summary CSV : {csv_path}")
        print(f"Aggregate summary JSON: {json_path}")
        print(f"Aggregate summary XLSX: {xlsx_path}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
