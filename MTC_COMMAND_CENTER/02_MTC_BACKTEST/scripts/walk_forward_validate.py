from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
from src.optimizer_v0.candidates import write_candidates


def run_checked(cmd: list[str], cwd: Path) -> None:
    result = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(cmd)}\n{result.stderr}\n{result.stdout}")


_RESERVED_TRAIN_COLS = {
    "idx",
    "score",
    "net_profit",
    "max_dd_pct",
    "total_trades",
    "win_rate",
    "profit_factor",
    "runtime_s",
    "status",
    "prune_reason",
    "min_trades_threshold",
    "max_dd_threshold_pct",
    "pruned_metric_value",
}


def _stable_param_key(params: dict) -> str:
    normalized = {}
    for key, value in params.items():
        if hasattr(value, "item"):
            value = value.item()
        if isinstance(value, float):
            normalized[key] = round(value, 6)
        else:
            normalized[key] = value
    return json.dumps(normalized, sort_keys=True)


def export_candidates_from_train_csv(trials_csv: Path, outdir: Path, top_k: int, overwrite: bool = True) -> list[Path]:
    df = pd.read_csv(trials_csv)
    if df.empty:
        return []

    items: list[dict] = []
    for _, row in df.iterrows():
        if row.get("status") != "OK":
            continue
        params = {}
        for key, value in row.to_dict().items():
            if key in _RESERVED_TRAIN_COLS:
                continue
            if hasattr(value, "item"):
                value = value.item()
            if pd.isna(value):
                continue
            params[key] = value

        item = {
            "idx": int(row["idx"]),
            "status": str(row["status"]),
            "score": float(row["score"]),
            "net_profit": float(row["net_profit"]),
            "dd_pct": float(row["max_dd_pct"]),
            "win_rate": float(row["win_rate"]),
            "pf": float(row["profit_factor"]),
            "trades": int(row["total_trades"]),
            "params": params,
            "param_key": _stable_param_key(params),
        }
        items.append(item)

    items.sort(
        key=lambda x: (
            -float(x["score"]),
            -float(x["net_profit"]),
            float(x["dd_pct"]),
            str(x["param_key"]),
        )
    )
    selected = items[:top_k] if top_k > 0 else items
    return write_candidates(
        selected,
        {"source_pareto_path": str(trials_csv), "run_id": None},
        outdir,
        name_prefix="candidate",
        overwrite=overwrite,
    )


def build_commands(args: argparse.Namespace, outdir: Path) -> tuple[list[list[str]], Path]:
    db = outdir / "walkforward.db"
    trials = outdir / "train_trials.csv"
    pareto = outdir / "train_pareto.json"
    candidates = outdir / "candidates"
    replay1 = outdir / "replay_target1.csv"
    replay2 = outdir / "replay_target2.csv"

    mode = getattr(args, "mode", "random")
    space_file = getattr(args, "space_file", None)
    objectives = getattr(args, "objectives", None)
    top_k = int(getattr(args, "top_k", 10))

    train_cmd = [
        sys.executable, "-m", "src.optimizer_v0", "run",
        "--case", args.train_case,
        "--mode", mode,
        "--iters", str(args.iters),
        "--seed", str(args.seed),
        "--workers", str(args.workers),
        "--min-trades", str(args.min_trades),
        "--max-dd", str(args.max_dd),
        "--db", str(db),
        "--out", str(trials),
        "--pareto-out", str(pareto),
    ]
    if space_file:
        train_cmd.extend(["--space-file", str(space_file)])
    if objectives:
        train_cmd.extend(["--objectives", str(objectives)])

    commands = [
        train_cmd,
        [
            sys.executable, "-m", "src.optimizer_v0", "export-candidates",
            "--pareto", str(pareto),
            "--outdir", str(candidates),
            "--top-k", str(top_k),
            "--overwrite",
        ],
        [
            sys.executable, "-m", "src.optimizer_v0", "replay-candidates",
            "--case", args.target_case_1,
            "--candidates-dir", str(candidates),
            "--out", str(replay1),
            "--min-trades", str(args.min_trades),
            "--max-dd", str(args.max_dd),
        ],
        [
            sys.executable, "-m", "src.optimizer_v0", "replay-candidates",
            "--case", args.target_case_2,
            "--candidates-dir", str(candidates),
            "--out", str(replay2),
            "--min-trades", str(args.min_trades),
            "--max-dd", str(args.max_dd),
        ],
    ]
    return commands, candidates


def build_walkforward_reports(outdir: Path) -> tuple[Path, Path]:
    replay1 = outdir / "replay_target1.csv"
    replay2 = outdir / "replay_target2.csv"
    ranking = outdir / "ranking.csv"
    summary = outdir / "summary.json"

    if not replay1.exists() or not replay2.exists():
        payload = {
            "status": "EMPTY",
            "ok_candidates": 0,
            "reason": "missing_replay_csv",
        }
        summary.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        pd.DataFrame().to_csv(ranking, index=False)
        return ranking, summary

    df1 = pd.read_csv(replay1)
    df2 = pd.read_csv(replay2)
    df1 = df1[df1["status"] == "OK"].copy()
    df2 = df2[df2["status"] == "OK"].copy()
    merged = pd.merge(df1, df2, on="candidate_file", suffixes=("_1", "_2"))
    if merged.empty:
        payload = {"status": "EMPTY", "ok_candidates": 0}
        summary.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        merged.to_csv(ranking, index=False)
        return ranking, summary

    merged["net_sum"] = merged["net_profit_1"] + merged["net_profit_2"]
    merged["dd_max"] = merged[["max_dd_pct_1", "max_dd_pct_2"]].max(axis=1)
    merged = merged.sort_values(["net_sum", "dd_max", "candidate_file"], ascending=[False, True, True]).reset_index(drop=True)
    merged.to_csv(ranking, index=False)

    payload = {
        "status": "OK",
        "ok_candidates": int(len(merged)),
        "best_candidate_file": str(merged.iloc[0]["candidate_file"]),
        "best_net_sum": float(merged.iloc[0]["net_sum"]),
        "best_dd_max": float(merged.iloc[0]["dd_max"]),
        "ranking_csv": str(ranking),
    }
    summary.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return ranking, summary


def main() -> None:
    p = argparse.ArgumentParser(description="Walk-forward validation workflow for optimizer_v0.")
    p.add_argument("--train-case", required=True)
    p.add_argument("--target-case-1", required=True)
    p.add_argument("--target-case-2", required=True)
    p.add_argument("--mode", choices=["grid", "random", "bayes"], default="random")
    p.add_argument("--iters", type=int, default=200)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--workers", type=int, default=1)
    p.add_argument("--min-trades", type=int, default=10)
    p.add_argument("--max-dd", type=float, default=40.0)
    p.add_argument("--space-file", default="")
    p.add_argument("--objectives", default="")
    p.add_argument("--top-k", type=int, default=10)
    p.add_argument("--candidate-source", choices=["pareto", "train_top_score"], default="pareto")
    p.add_argument("--outdir", required=True)
    args = p.parse_args()

    root = Path(__file__).resolve().parents[1]
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    commands, _ = build_commands(args, outdir)
    run_checked(commands[0], root)
    if args.candidate_source == "pareto":
        run_checked(commands[1], root)
    else:
        export_candidates_from_train_csv(outdir / "train_trials.csv", outdir / "candidates", args.top_k, overwrite=True)
    for cmd in commands[2:]:
        run_checked(cmd, root)
    build_walkforward_reports(outdir)
    print("Walk-forward workflow: PASS")


if __name__ == "__main__":
    main()
