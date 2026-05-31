"""
CLI entry point for optimizer_v0.

Usage:
    python -m src.optimizer_v0 run --case configs/cases/full_jul2025_jan2026_parity.json --mode random --iters 200 --seed 42
    python -m src.optimizer_v0 run --case configs/cases/full_jul2025_jan2026_parity.json --mode grid
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, time as dt_time, timezone, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import os
import pandas as pd

from src.config.defaults import MTCConfig
from src.optimizer_v0.search import (
    DEFAULT_PARAMS,
    ParamDef,
    bayes_search,
    grid_search,
    random_search,
    results_to_csv,
    print_top_n,
    load_search_space,
)
from src.optimizer_v0.store_sqlite import SQLiteStore
import src.optimizer_v0.pareto as pareto
import src.optimizer_v0.candidates as candidates
import src.optimizer_v0.replay_candidates as replay_candidates

SUPPORTED_OBJECTIVES = {"net_profit", "profit_factor", "win_rate", "total_trades", "max_dd_pct", "dd_pct"}


def _parse_dt(raw: str, *, as_end: bool = False) -> datetime:
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        dt = datetime.strptime(raw, "%Y-%m-%d")
    if dt.hour == 0 and dt.minute == 0 and dt.second == 0 and "T" not in raw:
        dt = datetime.combine(dt.date(), dt_time.max if as_end else dt_time.min)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def load_data(case: dict) -> tuple:
    """Load dataset and compute eval window. Returns (df_filtered, warmup_bars, eval_start, eval_end)."""
    dataset_path = PROJECT_ROOT / "data" / case["dataset"]
    if dataset_path.suffix == ".parquet":
        df = pd.read_parquet(dataset_path)
    else:
        df = pd.read_csv(dataset_path)

    if "timestamp" in df.columns:
        if pd.api.types.is_numeric_dtype(df["timestamp"]):
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        else:
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    if df["timestamp"].dt.tz is None:
        df["timestamp"] = df["timestamp"].dt.tz_localize("UTC")
    else:
        df["timestamp"] = df["timestamp"].dt.tz_convert("UTC")

    start_dt = _parse_dt(case["start_date"], as_end=False)
    end_dt = _parse_dt(case["end_date"], as_end=True)
    preroll_days = case.get("preroll_days", 90)

    filter_start = start_dt - timedelta(days=preroll_days) if preroll_days > 0 else start_dt
    mask = (df["timestamp"] >= filter_start) & (df["timestamp"] <= end_dt)
    df_filtered = df.loc[mask].copy().reset_index(drop=True)

    warmup_bars = case.get("warmup_bars", 200)
    eval_start = start_dt if preroll_days > 0 else None

    return df_filtered, warmup_bars, eval_start, end_dt


def _parse_objectives(raw: str) -> tuple[list[str], list[str]]:
    metrics = [m.strip() for m in raw.split(",") if m.strip()]
    if not metrics:
        raise ValueError("At least one objective is required.")

    unknown = [m for m in metrics if m not in SUPPORTED_OBJECTIVES]
    if unknown:
        raise ValueError(f"Unsupported objectives: {', '.join(unknown)}")

    minimize = [m for m in metrics if m in {"max_dd_pct", "dd_pct"}]
    maximize = [m for m in metrics if m not in {"max_dd_pct", "dd_pct"}]
    if not maximize:
        raise ValueError("At least one maximize objective is required.")
    if not minimize:
        raise ValueError("At least one minimize objective is required (e.g. max_dd_pct).")
    return maximize, minimize


def _space_file_hash(space_file: Path | None) -> str | None:
    if space_file is None:
        return None
    if not space_file.exists():
        return None
    payload = space_file.read_bytes()
    return hashlib.sha256(payload).hexdigest()


def _require_resume_compat(existing: dict, args: argparse.Namespace) -> None:
    mismatches: list[str] = []
    checks = {
        "mode": (existing.get("mode"), args.mode),
        "seed": (existing.get("seed"), args.seed),
        "case_path": (existing.get("case_path"), args.case),
        "workers": (existing.get("workers"), args.workers),
        "min_trades": (existing.get("min_trades"), args.min_trades),
        "max_dd_pct": (existing.get("max_dd_pct"), args.max_dd),
    }
    for name, (lhs, rhs) in checks.items():
        if str(lhs) != str(rhs):
            mismatches.append(f"{name}: run={lhs} cli={rhs}")
    if mismatches:
        raise ValueError("Resume mismatch detected: " + "; ".join(mismatches))


def cmd_run(args: argparse.Namespace) -> None:
    """Execute optimizer run."""
    case_file = PROJECT_ROOT / args.case
    with open(case_file, encoding="utf-8") as f:
        case = json.load(f)

    config = MTCConfig.model_validate(case.get("config", {}))
    config.parity.export_debug_csv = False  # never export during optimization

    df, warmup_bars, eval_start, eval_end = load_data(case)
    print(f"Data: {len(df)} bars | eval: {eval_start} .. {eval_end}")

    # Parse param overrides from --params JSON if provided
    param_defs = list(DEFAULT_PARAMS)
    
    # 1. Load from space file (if provided)
    if args.space_file:
        gp, rp = load_search_space(PROJECT_ROOT / args.space_file)
        param_defs = gp if args.mode == "grid" else rp

    # 2. Overrides from --params (highest priority)
    if args.params:
        param_defs = []
        for p in json.loads(args.params):
            param_defs.append(ParamDef(**p))
            
    # Reporting
    src = "DEFAULT"
    if args.params: src = "PARAMS_JSON"
    elif args.space_file: src = "SPACE_FILE"
    print(f"Search Space: source={src} | params={len(param_defs)}")
    try:
        maximize_objectives, minimize_objectives = _parse_objectives(args.objectives)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(2)

    # Dry-run inspector
    if args.print_space:
        print(f"\nSEARCH SPACE (DRY RUN)")
        print(f"mode={args.mode}")
        print(f"source={src}")
        print(f"count={len(param_defs)}")
        print(f"\nPARAMS")
        
        # Sort by key
        param_defs.sort(key=lambda p: p.key)
        
        for p in param_defs:
            if p.choices is not None:
                kind = f"choice(values={json.dumps(p.choices)})"
            else:
                # Reconstruct dist/range info loosely
                # If step > 0 it's a range.
                dist_str = ""
                if args.mode == "random":
                     if p.dtype == "int": dist_str = ", dist=uniform_int"
                     else: dist_str = ", dist=uniform_float"
                
                kind = f"range(low={p.low}, high={p.high}, step={p.step}, dtype={p.dtype}{dist_str})"
                
            print(f"- {p.key} | {kind}")
        
        sys.exit(0)

    if args.out and args.export_csv:
        print("Error: --out and --export-csv cannot be used together.")
        sys.exit(2)

    # Output path
    if args.export_csv:
        out_path: Path | None = PROJECT_ROOT / args.export_csv
    elif args.out:
        out_path = PROJECT_ROOT / args.out
    elif args.db:
        # DB-primary mode: CSV export is optional.
        out_path = None
    else:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = PROJECT_ROOT / "results" / f"optimizer_v0_{args.mode}_{ts}.csv"

    if out_path is None:
        print("Output CSV: disabled (DB-primary mode)")
    else:
        print(f"Output CSV: {out_path}")

    # Initialize DB (if requested)
    store = None
    run_id = args.run_id
    
    # Guardrail: Prevent mixing DB runs into one CSV without explicit resume
    # If --db used, --out used, and no --run-id, ensures we start fresh CSV or fail
    if args.db and out_path is not None and not run_id:
        if out_path.exists():
            print(f"Error: --db + --out with existing CSV requires --run-id to resume, or delete/change --out.")
            sys.exit(2)

    if args.list_runs:
        if not args.db:
            print("Error: --list-runs requires --db <path>")
            sys.exit(2)
        store = SQLiteStore(Path(args.db))
        runs = store.list_runs()
        print(f"\nRecent Runs (DB: {args.db})")
        print(f"{'Run ID':<38}  {'Created':<20}  {'Mode':<8}  {'Seed':<5}  {'Iters':<6}  {'Case'}")
        print("-" * 100)
        for r in runs:
            # truncate case path
            case_short = Path(r['case_path']).name
            print(f"{r['run_id']:<38}  {r['created_at'][:19]:<20}  {r['mode']:<8}  {r['seed']:<5}  {r['iters']:<6}  {case_short}")
        sys.exit(0)

    if args.db:
        store = SQLiteStore(Path(args.db))
        if not run_id:
            meta: dict[str, object] = {}
            if args.space_file:
                resolved_space = PROJECT_ROOT / args.space_file
                space_hash = _space_file_hash(resolved_space)
                if space_hash:
                    meta["space_file_sha256"] = space_hash
            if args.mode == "bayes":
                meta.update(
                    {
                        "optimizer_mode": "bayes",
                        "sampler": "deterministic_local",
                        "seed": args.seed,
                        "bayes_init": args.bayes_init,
                        "bayes_iter": args.bayes_iter,
                        "bayes_workers": args.bayes_workers,
                    }
                )
            code_hash = json.dumps(meta, sort_keys=True) if meta else None
            # Create new run
            run_id = store.create_run(
                case_path=args.case,
                mode=args.mode,
                seed=args.seed,
                iters=args.iters,
                workers=args.workers,
                min_trades=args.min_trades,
                max_dd_pct=args.max_dd,
                space_file=args.space_file,
                out_csv=str(out_path) if out_path is not None else None,
                code_hash=code_hash,
                run_name=args.run_name,
            )
            print(f"DB Run Created: {run_id}")
            if args.run_name:
                print(f"Run Name: {args.run_name}")
        else:
            # Resume/Attach to existing run
            existing = store.get_run(run_id)
            print(f"Attached to DB Run: {run_id} (Created: {existing['created_at']})")
            try:
                _require_resume_compat(existing, args)
            except ValueError as e:
                print(f"Error: {e}")
                sys.exit(1)

    if args.mode == "grid":
        results = grid_search(
            df, config, param_defs, out_path=out_path,
            warmup_bars=warmup_bars, eval_start=eval_start, eval_end=eval_end,
            min_trades=args.min_trades, max_dd_pct=args.max_dd,
            workers=args.workers,
            store=store, run_id=run_id
        )
    elif args.mode == "random":
        results = random_search(
            df, config, param_defs, out_path=out_path,
            n_iters=args.iters, seed=args.seed,
            warmup_bars=warmup_bars, eval_start=eval_start, eval_end=eval_end,
            min_trades=args.min_trades, max_dd_pct=args.max_dd,
            workers=args.workers,
            store=store, run_id=run_id
        )
    else:
        if args.bayes_workers != 1:
            print("Error: --bayes-workers must be 1 for deterministic bayes mode.")
            sys.exit(2)
        results = bayes_search(
            df, config, param_defs, out_path=out_path,
            n_init=args.bayes_init, n_iter=args.bayes_iter, seed=args.seed,
            warmup_bars=warmup_bars, eval_start=eval_start, eval_end=eval_end,
            min_trades=args.min_trades, max_dd_pct=args.max_dd,
            workers=args.bayes_workers,
            store=store, run_id=run_id
        )
    
    # Pareto Export (v2.1)
    if args.pareto_out:
        print(f"Computing Pareto Frontier...")
        trials = []
        source = "unknown"
        
        # Priority 1: DB
        if args.db:
            if not run_id:
                # Should have been set creation or CLI
                print("Error: Pareto export with --db requires active run_id (should be set internally).")
            else:
                source = "db"
                trials = pareto.load_trials_from_db(Path(args.db), run_id, args.pareto_include_pruned)
        
        # Priority 2: CSV
        elif out_path is not None:
            source = "csv"
            trials = pareto.load_trials_from_csv(out_path, args.pareto_include_pruned)
        
        else:
            print("Error: --pareto-out requires either --db or --out to load trials.")
            sys.exit(1)

        frontier = pareto.compute_pareto(
            trials,
            maximize=maximize_objectives,
            minimize=minimize_objectives,
        )
        
        # Filter top N by profit (if requested)
        if args.pareto_top > 0 and len(frontier) > args.pareto_top:
            # Sort by profit DESC and take top N
            # Frontier is already sorted by DD ASC / Profit DESC?
            # Wait, sort key was (dd, -profit).
            # To get top profits, we just sort by net_profit DESC.
            frontier.sort(key=lambda x: -float(x["net_profit"]))
            frontier = frontier[:args.pareto_top]
            # Re-sort by Pareto definition for output consistency (DD ASC)
            frontier.sort(key=lambda x: (float(x["dd_pct"]), -float(x["net_profit"])))

        payload = {
            "source": source,
            "run_id": run_id,
            "case": args.case,
            "mode": args.mode,
            "seed": args.seed,
            "iters": args.iters,
            "count_total": len(trials),
            "count_considered": len(trials), # Same as total loaded
            "count_pareto": len(frontier),
            "objectives": {"maximize": maximize_objectives, "minimize": minimize_objectives},
            "items": frontier
        }
        
        out_json = Path(args.pareto_out)
        pareto.write_pareto_json(out_json, payload)
        print(f"Pareto export written: {out_json} (Count: {len(frontier)})")
    print_top_n(results, n=10)
    if args.report == "pareto":
        report_items = []
        for r in results:
            if not args.pareto_include_pruned and r.status == "PRUNED":
                continue
            report_items.append(
                {
                    "idx": r.idx,
                    "status": r.status,
                    "param_key": json.dumps(r.params, sort_keys=True),
                    "params": r.params,
                    "net_profit": r.net_profit,
                    "max_dd_pct": r.max_dd_pct,
                    "total_trades": r.total_trades,
                    "win_rate": r.win_rate,
                    "profit_factor": r.profit_factor,
                }
            )

        frontier = pareto.compute_pareto(
            report_items,
            maximize=maximize_objectives,
            minimize=minimize_objectives,
        )
        if args.pareto_top > 0:
            frontier = frontier[: args.pareto_top]

        print(f"\nPareto Frontier Report (count={len(frontier)})")
        print(f"Objectives: maximize={','.join(maximize_objectives)} | minimize={','.join(minimize_objectives)}")
        for i, item in enumerate(frontier, start=1):
            print(
                f"{i:>3}. net={float(item.get('net_profit', 0.0)):.2f} "
                f"dd={float(item.get('dd_pct', item.get('max_dd_pct', 0.0))):.2f}% "
                f"pf={float(item.get('profit_factor', 0.0)):.2f} "
                f"wr={float(item.get('win_rate', 0.0)):.2f} "
                f"trades={int(item.get('total_trades', item.get('trades', 0)))} "
                f"status={item.get('status', 'N/A')}"
            )


def cmd_export_candidates(args: argparse.Namespace) -> None:
    """Execute candidate export from Pareto JSON."""
    pareto_path = Path(args.pareto)
    outdir = Path(args.outdir)
    
    print(f"Loading Pareto: {pareto_path}")
    try:
        payload = candidates.load_pareto(pareto_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
        
    # Inject source path for meta
    payload["source_pareto_path"] = str(pareto_path)
    
    selected = candidates.select_candidates(
        payload, 
        top_k=args.top_k, 
        include_pruned=args.include_pruned
    )
    
    print(f"Selected {len(selected)} candidates (Top-K={args.top_k}). Writing to {outdir}...")
    
    try:
        written = candidates.write_candidates(
            selected, 
            payload, 
            outdir, 
            name_prefix=args.name_prefix, 
            overwrite=args.overwrite
        )
    except FileExistsError as e:
        print(f"Error: {e}")
        sys.exit(2)
        
    for p in written:
        print(f"  - {p.name}")
    print(f"Done. Exported {len(written)} files.")


def cmd_replay_candidates(args: argparse.Namespace) -> None:
    """Execute candidate replay."""
    cand_dir = Path(args.candidates_dir)
    case_path = Path(args.case)
    out_csv = Path(args.out)
    
    files = replay_candidates.load_candidate_files(cand_dir)
    if not files:
        print(f"No candidate files found in {cand_dir}")
        sys.exit(0)
        
    replay_candidates.run_replay_batch(
        case_path=case_path,
        candidate_files=files,
        out_csv=out_csv,
        min_trades=args.min_trades,
        max_dd_pct=args.max_dd
    )


def cmd_show_run(args: argparse.Namespace) -> None:
    store = SQLiteStore(Path(args.db))
    run = store.get_run(args.run_id)
    trials = [dict(r) for r in store.fetch_trials(args.run_id)]

    ok = sum(1 for t in trials if t.get("status") == "OK")
    pruned = sum(1 for t in trials if t.get("status") == "PRUNED")
    errors = sum(1 for t in trials if str(t.get("status", "")).startswith("ERROR"))
    print(f"Run: {run['run_id']}")
    print(f"Created: {run['created_at']}")
    print(f"Mode: {run.get('mode')} | Seed: {run.get('seed')} | Iters: {run.get('iters')}")
    print(f"Case: {run.get('case_path')}")
    print(f"Trials: total={len(trials)} ok={ok} pruned={pruned} errors={errors}")
    if run.get("code_hash"):
        print(f"Meta: {run['code_hash']}")


def cmd_compare_runs(args: argparse.Namespace) -> None:
    store = SQLiteStore(Path(args.db))
    run_a = store.get_run(args.run_a)
    run_b = store.get_run(args.run_b)
    trials_a = [dict(r) for r in store.fetch_trials(args.run_a)]
    trials_b = [dict(r) for r in store.fetch_trials(args.run_b)]

    keys_a = {t["params_key"] for t in trials_a if t.get("params_key")}
    keys_b = {t["params_key"] for t in trials_b if t.get("params_key")}
    overlap = keys_a.intersection(keys_b)

    ok_a = [t for t in trials_a if t.get("status") == "OK" and t.get("score") is not None]
    ok_b = [t for t in trials_b if t.get("status") == "OK" and t.get("score") is not None]
    best_a = max(ok_a, key=lambda x: float(x["score"])) if ok_a else None
    best_b = max(ok_b, key=lambda x: float(x["score"])) if ok_b else None

    print(f"Run A: {run_a['run_id']} ({run_a.get('mode')})")
    print(f"Run B: {run_b['run_id']} ({run_b.get('mode')})")
    print(f"Overlap params_key: {len(overlap)}")
    if best_a:
        print(f"Best A: idx={best_a['idx']} score={float(best_a['score']):.6f}")
    if best_b:
        print(f"Best B: idx={best_b['idx']} score={float(best_b['score']):.6f}")


def main() -> None:
    # Default workers
    default_workers = max(1, (os.cpu_count() or 1) - 1)

    parser = argparse.ArgumentParser(prog="optimizer_v0", description="MTC Optimizer v0")
    sub = parser.add_subparsers(dest="command", required=True)

    # Subcommand: run
    run_p = sub.add_parser("run", help="Run optimization")
    run_p.add_argument("--case", required=True, help="Path to case JSON")
    run_p.add_argument("--mode", choices=["grid", "random", "bayes"], default="random")
    run_p.add_argument("--iters", type=int, default=200, help="Iterations (random mode)")
    run_p.add_argument("--seed", type=int, default=42, help="Random seed")
    run_p.add_argument("--bayes-init", type=int, default=20, help="Bayes warmup random trials")
    run_p.add_argument("--bayes-iter", type=int, default=50, help="Bayes guided trials")
    run_p.add_argument("--bayes-workers", type=int, default=1, help="Bayes worker count (locked to 1)")
    run_p.add_argument("--min-trades", type=int, default=50, help="Min trades guardrail")
    run_p.add_argument("--max-dd", type=float, default=40.0, help="Max DD%% guardrail")
    run_p.add_argument("--params", type=str, default=None, help="JSON array of ParamDef overrides")
    run_p.add_argument("--out", type=str, default=None, help="Output CSV path (for resume/append)")
    run_p.add_argument("--export-csv", type=str, default=None, help="Optional CSV export path (DB-primary mode)")
    run_p.add_argument("--workers", type=int, default=default_workers, help=f"Number of worker processes (default: {default_workers})")
    run_p.add_argument("--space-file", type=str, default=None, help="Path to JSON defining search space")
    run_p.add_argument("--print-space", action="store_true", help="Print resolved search space and exit")
    
    # DB arguments
    run_p.add_argument("--db", type=str, default=None, help="Path to SQLite DB for persistence")
    run_p.add_argument("--run-name", type=str, default=None, help="Optional run tag included in run_id")
    run_p.add_argument("--run-id", type=str, default=None, help="Resume specific Run ID from DB")
    run_p.add_argument("--list-runs", action="store_true", help="List recent runs in DB and exit")

    # Pareto arguments
    run_p.add_argument("--pareto-out", type=str, default=None, help="Path to write Pareto frontier JSON")
    run_p.add_argument("--pareto-include-pruned", action="store_true", help="Include PRUNED trials in Pareto set")
    run_p.add_argument("--pareto-top", type=int, default=0, help="Keep top N Pareto items by net_profit (0=all)")
    run_p.add_argument("--report", choices=["pareto"], default=None, help="Print extra deterministic report(s)")
    run_p.add_argument(
        "--objectives",
        type=str,
        default="net_profit,max_dd_pct,profit_factor,win_rate,total_trades",
        help="Comma-separated objectives. max_dd_pct/dd_pct are minimized; others maximized.",
    )

    # Subcommand: export-candidates
    cand_p = sub.add_parser("export-candidates", help="Export top candidates from Pareto JSON to files")
    cand_p.add_argument("--pareto", required=True, help="Path to input Pareto JSON")
    cand_p.add_argument("--outdir", required=True, help="Directory to write candidate files")
    cand_p.add_argument("--top-k", type=int, default=10, help="Number of candidates to export")
    cand_p.add_argument("--include-pruned", action="store_true", help="Include PRUNED trials")
    cand_p.add_argument("--name-prefix", type=str, default="candidate", help="Prefix for filenames")
    cand_p.add_argument("--overwrite", action="store_true", help="Overwrite existing files")

    # Subcommand: replay-candidates
    replay_p = sub.add_parser("replay-candidates", help="Replay candidate JSONs and output summary CSV")
    replay_p.add_argument("--case", required=True, help="Path to case JSON")
    replay_p.add_argument("--candidates-dir", required=True, help="Directory containing candidate JSONs")
    replay_p.add_argument("--out", required=True, help="Output CSV path")
    replay_p.add_argument("--min-trades", type=int, default=1, help="Min trades threshold")
    replay_p.add_argument("--min-trades-reward", type=int, default=10, help="Min trades to start rewarding consistency (unused in replay?)")
    replay_p.add_argument("--max-dd", type=float, default=100.0, help="Max drawdown %% threshold")

    # Subcommand: show-run
    show_p = sub.add_parser("show-run", help="Show a run summary from DB")
    show_p.add_argument("--db", required=True, help="Path to SQLite DB")
    show_p.add_argument("--run-id", required=True, help="Run ID to inspect")

    # Subcommand: compare-runs
    cmp_p = sub.add_parser("compare-runs", help="Compare two runs from DB")
    cmp_p.add_argument("--db", required=True, help="Path to SQLite DB")
    cmp_p.add_argument("--run-a", required=True, help="First run ID")
    cmp_p.add_argument("--run-b", required=True, help="Second run ID")

    args = parser.parse_args()
    if args.command == "run":
        cmd_run(args)
    elif args.command == "export-candidates":
        cmd_export_candidates(args)
    elif args.command == "replay-candidates":
        cmd_replay_candidates(args)
    elif args.command == "show-run":
        cmd_show_run(args)
    elif args.command == "compare-runs":
        cmd_compare_runs(args)
    else:
        parser.print_help()




if __name__ == "__main__":
    main()
