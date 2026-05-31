"""
optimize.py — MTC_V2 Overnight Optimization Entry Point

Runs Optuna parameter sweep against the MTC backtest engine.
Uses the real Python engine (99.54% TV parity) — not vectorbt.

Usage:
  python optimize.py [--trials 50] [--objective profit_factor] [--case <json>]

Outputs:
  reports/optimization_results.json
  reports/optimization_results.md   (human-readable top-N summary)

Defaults: Supertrend 1h BTCUSDT.P, 50 trials, profit_factor objective.
"""

from __future__ import annotations

import argparse
import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

# ─── Sys path: resolve clean backtest package root ───────────────────────────
REPO_ROOT = Path(__file__).resolve().parents[2]
MTC_ROOT  = REPO_ROOT / "MTC_COMMAND_CENTER/02_MTC_BACKTEST"
sys.path.insert(0, str(MTC_ROOT))

import optuna
import pandas as pd

from src.config.defaults import MTCConfig
from src.config.schema   import ParamRange
from src.optimize.runner import OptimizationRunner

# Silence Optuna logging (progress shown via callback instead)
optuna.logging.set_verbosity(optuna.logging.WARNING)

# ─── Default dataset / case ──────────────────────────────────────────────────
# Actual parquet location (catalog paths point to 110_ which is under the
# İ-prefixed directory on this machine).
_DATASET_CANDIDATES = [
    MTC_ROOT / "data/processed_hist/binance_usdm/BTCUSDT.P/1h.parquet",
    MTC_ROOT / "data/optimization/processed_hist/binance_usdm/BTCUSDT.P/1h.parquet",
    MTC_ROOT   / "data/BTCUSDT_15m_20180701_20260308.parquet",   # fallback (15m)
]

DEFAULT_CASE = MTC_ROOT / "configs/cases/supertrend_1h_full_20260312.json"

REPORTS_DIR = MTC_ROOT / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


def _find_dataset() -> Path:
    for p in _DATASET_CANDIDATES:
        if p.exists():
            return p
    raise FileNotFoundError(
        "No BTCUSDT dataset found. Checked:\n" +
        "\n".join(f"  {p}" for p in _DATASET_CANDIDATES)
    )


def _load_dataset(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path)
    # Normalize to timestamp column
    if "timestamp" not in df.columns:
        if isinstance(df.index, pd.DatetimeIndex):
            df = df.reset_index()
            if "timestamp" not in df.columns:
                df = df.rename(columns={df.columns[0]: "timestamp"})
    if pd.api.types.is_numeric_dtype(df["timestamp"]):
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    else:
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df["timestamp"].dt.tz is None:
        df["timestamp"] = df["timestamp"].dt.tz_localize("UTC")
    return df.sort_values("timestamp").reset_index(drop=True)


def _load_case_config(case_path: Path) -> tuple[dict, MTCConfig]:
    with case_path.open(encoding="utf-8") as f:
        case = json.load(f)
    cfg = MTCConfig.model_validate(case["config"])
    return case, cfg


def _filter_df(df: pd.DataFrame, start: str, end: str, preroll_days: int = 365) -> tuple[pd.DataFrame, datetime, datetime]:
    from datetime import timedelta
    start_dt = datetime.fromisoformat(start).replace(tzinfo=timezone.utc)
    end_dt   = datetime.fromisoformat(end  ).replace(tzinfo=timezone.utc)
    filter_start = start_dt - timedelta(days=preroll_days)
    mask = (df["timestamp"] >= filter_start) & (df["timestamp"] <= end_dt)
    return df.loc[mask].copy().reset_index(drop=True), start_dt, end_dt


# ─── Parameter search space (Supertrend + SL/TP) ─────────────────────────────
SUPERTREND_SPACE: dict[str, ParamRange] = {
    "supertrend.atr_len": ParamRange(param_type="int",   low=10,  high=40,  step=2),
    "supertrend.factor":  ParamRange(param_type="float", low=2.0, high=8.0, step=0.5),
}

SL_TP_SPACE: dict[str, ParamRange] = {
    "stop_loss.atr_mult":  ParamRange(param_type="float", low=1.5, high=5.0, step=0.5),
    "take_profit.atr_mult":ParamRange(param_type="float", low=1.5, high=6.0, step=0.5),
}

SPACE_PRESETS = {
    "signal":    SUPERTREND_SPACE,
    "signal_sl": {**SUPERTREND_SPACE, **SL_TP_SPACE},
    "sl_tp":     SL_TP_SPACE,
}


def main() -> int:
    ap = argparse.ArgumentParser(description="MTC_V2 Optuna optimization")
    ap.add_argument("--trials",    type=int,   default=50,              help="Number of Optuna trials")
    ap.add_argument("--objective", type=str,   default="profit_factor", help="Objective metric")
    ap.add_argument("--space",     type=str,   default="signal",        choices=list(SPACE_PRESETS), help="Parameter space preset")
    ap.add_argument("--case",      type=str,   default=str(DEFAULT_CASE), help="Base case JSON path")
    ap.add_argument("--min-trades",type=int,   default=10,              help="Min trades to not prune a trial")
    ap.add_argument("--out",       type=str,   default=str(REPORTS_DIR / "optimization_results.json"))
    ap.add_argument("--sampler",   type=str,   default="tpe",           choices=["tpe", "random"])
    args = ap.parse_args()

    # Force UTF-8 output on Windows
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print("=" * 60)
    print("MTC_V2 Optuna Optimization")
    print("=" * 60)
    print(f"  Trials    : {args.trials}")
    print(f"  Objective : {args.objective}")
    print(f"  Space     : {args.space}")
    print(f"  Sampler   : {args.sampler}")
    print(f"  Min trades: {args.min_trades}")
    print()

    # ─── Load dataset ─────────────────────────────────────────────────────────
    dataset_path = _find_dataset()
    print(f"Dataset: {dataset_path}")
    df_full = _load_dataset(dataset_path)
    print(f"  Total bars: {len(df_full)}  ({df_full['timestamp'].iloc[0].date()} -> {df_full['timestamp'].iloc[-1].date()})")

    # ─── Load base case ───────────────────────────────────────────────────────
    case_path = Path(args.case)
    case, base_config = _load_case_config(case_path)
    print(f"\nBase case: {case_path.name}")
    print(f"  Range  : {case['start_date']} .. {case['end_date']}")
    preroll = int(case.get("preroll_days", 365))
    warmup  = int(case.get("warmup_bars",  200))
    df_filtered, eval_start, eval_end = _filter_df(
        df_full, case["start_date"], case["end_date"], preroll
    )
    print(f"  Filtered: {len(df_filtered)} bars (incl. {preroll}d preroll)")

    # ─── Build param space ────────────────────────────────────────────────────
    param_space = SPACE_PRESETS[args.space]
    print(f"\nSearch space ({args.space}): {list(param_space.keys())}")

    # ─── Run optimization ─────────────────────────────────────────────────────
    completed = [0]
    def _progress(study: optuna.Study, trial: optuna.trial.FrozenTrial) -> None:
        completed[0] += 1
        best = study.best_value if study.best_trial else float("nan")
        status = "PRUNED" if trial.state == optuna.trial.TrialState.PRUNED else f"{trial.value:.4f}"
        print(f"  Trial {completed[0]:>3}/{args.trials}  val={status:>10}  best={best:.4f}", flush=True)

    print()
    opt = OptimizationRunner(
        df              = df_filtered,
        base_config     = base_config,
        param_space     = param_space,
        objective       = args.objective,
        min_trades      = args.min_trades,
        warmup_bars     = warmup,
        eval_start      = eval_start,
        eval_end        = eval_end,
    )

    t0 = datetime.now()
    try:
        results = opt.run(
            n_trials         = args.trials,
            n_jobs           = 1,
            sampler          = args.sampler,
            progress_callback= None,   # we use Optuna callback above
        )
        # Attach our per-trial callback via study object after run
        # (OptimizationRunner.run creates the study internally; progress shown by our print above)
    except Exception as e:
        print(f"\nOptimization FAILED: {e}")
        traceback.print_exc()
        return 1

    elapsed = (datetime.now() - t0).total_seconds()

    # ─── Extract best trial ───────────────────────────────────────────────────
    best = results.get("best_params", {})
    best_val = results.get("best_value", None)
    all_trials = results.get("all_trials", [])

    print(f"\n{'=' * 60}")
    print(f"OPTIMIZATION COMPLETE  ({elapsed:.1f}s, {len(all_trials)} trials)")
    print(f"  Best {args.objective}: {best_val}")
    print(f"  Best params:")
    for k, v in best.items():
        print(f"    {k}: {v}")

    # Top 5
    valid = [t for t in all_trials if t.get("value") is not None and not (isinstance(t.get("value"), float) and t["value"] != t["value"]) and t.get("state") != "PRUNED"]
    top5 = sorted(valid, key=lambda t: t.get("value", 0), reverse=True)[:5]
    if top5:
        print(f"\n  Top 5 trials:")
        for i, t in enumerate(top5, 1):
            p = t.get("params", {})
            v = t.get("value", None)
            # all_trials stores metrics at top level (not in user_attrs)
            trades = t.get("total_trades", "?")
            wr     = t.get("win_rate", None)
            print(f"    #{i}  val={v:.4f}  trades={trades}  wr={f'{wr:.1f}%' if wr else '?'}")
            for k, pv in p.items():
                print(f"         {k}={pv}")

    # ─── Save output ──────────────────────────────────────────────────────────
    out_path = Path(args.out)

    output = {
        "timestamp":   datetime.now(timezone.utc).isoformat(),
        "case":        case_path.name,
        "dataset":     str(dataset_path),
        "objective":   args.objective,
        "space":       args.space,
        "n_trials":    args.trials,
        "elapsed_sec": round(elapsed, 1),
        "best_value":  best_val,
        "best_params": best,
        "top5": [
            {
                "rank":           i + 1,
                "value":          t.get("value"),
                "params":         t.get("params", {}),
                "total_trades":   t.get("total_trades"),
                "win_rate":       t.get("win_rate"),
                "net_profit_pct": t.get("net_profit_pct"),
                "max_dd_pct":     t.get("max_drawdown_pct"),
            }
            for i, t in enumerate(top5)
        ],
        "all_trials_count": len(all_trials),
    }

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, default=str)

    # Markdown summary
    md_path = out_path.with_suffix(".md")
    with md_path.open("w", encoding="utf-8") as f:
        f.write(f"# Optimization Results\n")
        f.write(f"Generated: {output['timestamp']}\n\n")
        f.write(f"- Case: `{output['case']}`\n")
        f.write(f"- Objective: `{output['objective']}`\n")
        f.write(f"- Space: `{output['space']}`\n")
        f.write(f"- Trials: {output['n_trials']}  Elapsed: {output['elapsed_sec']}s\n\n")
        f.write(f"## Best Result\n\n")
        f.write(f"**{args.objective}: {best_val}**\n\n")
        f.write("| Parameter | Value |\n|-----------|-------|\n")
        for k, v in best.items():
            f.write(f"| `{k}` | `{v}` |\n")
        f.write(f"\n## Top 5 Trials\n\n")
        f.write("| Rank | Value | Trades | Win Rate | Net PnL% | Max DD% | Params |\n")
        f.write("|------|-------|--------|----------|----------|---------|--------|\n")
        for row in output["top5"]:
            params_str = ", ".join(f"{k}={v}" for k, v in row["params"].items())
            wr = f"{row['win_rate']:.1f}%" if row.get("win_rate") else "-"
            pnl = f"{row['net_profit_pct']:.2f}%" if row.get("net_profit_pct") else "-"
            dd  = f"{row['max_dd_pct']:.1f}%" if row.get("max_dd_pct") else "-"
            f.write(f"| {row['rank']} | {row['value']:.4f} | {row['total_trades']} | {wr} | {pnl} | {dd} | {params_str} |\n")

    print(f"\nResults saved:")
    print(f"  {out_path}")
    print(f"  {md_path}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
