"""
Fine-grid Supertrend ATR x Factor optimization on the BTCUSDT.P parity contract.

Runs two focused grids around the only in-sample basins that stayed positive after
switching the optimizer to the correct perpetual dataset / terminal MANUAL close:

1. short_atr_cluster:
   ATR 5 -> 11 step 1
   Factor 3.6 -> 4.4 step 0.1

2. high_atr_cluster:
   ATR 35 -> 49 step 1
   Factor 4.8 -> 5.2 step 0.1

Outputs per-cluster CSVs plus combined CSV/XLSX summary.
"""
from __future__ import annotations

import json
import os
import sys
import time
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config.defaults import MTCConfig
from src.optimizer_v0.search import ParamDef, grid_search


FINE_GRIDS = [
    {
        "name": "short_atr_cluster",
        "atr_low": 5,
        "atr_high": 11,
        "atr_step": 1,
        "factor_low": 3.6,
        "factor_high": 4.4,
        "factor_step": 0.1,
    },
    {
        "name": "high_atr_cluster",
        "atr_low": 35,
        "atr_high": 49,
        "atr_step": 1,
        "factor_low": 4.8,
        "factor_high": 5.2,
        "factor_step": 0.1,
    },
]


def _load_data() -> pd.DataFrame:
    data_path = PROJECT_ROOT / "data" / "BTCUSDT_PERP_15m_20240101_20260101_long.parquet"
    print(f"Loading data: {data_path}")
    df = pd.read_parquet(data_path)
    if "timestamp" not in df.columns:
        df = df.reset_index()
        if "timestamp" not in df.columns:
            df = df.rename(columns={df.columns[0]: "timestamp"})
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    print(f"  Rows: {len(df):,}  |  Range: {df['timestamp'].min()} -- {df['timestamp'].max()}")
    return df


def _load_base_config() -> MTCConfig:
    config_path = PROJECT_ROOT / "configs" / "cases" / "supertrend_atr_factor_optimize.json"
    with open(config_path, encoding="utf-8") as f:
        cfg_dict = json.load(f)
    cfg_dict.pop("_meta", None)
    base_config = MTCConfig.model_validate(cfg_dict)
    base_config.parity.enabled = True
    base_config.parity.force_terminal_manual_close = True
    return base_config


def _run_grid(
    *,
    df: pd.DataFrame,
    base_config: MTCConfig,
    out_path: Path,
    atr_low: int,
    atr_high: int,
    atr_step: int,
    factor_low: float,
    factor_high: float,
    factor_step: float,
    eval_start: datetime,
    eval_end: datetime,
    workers: int,
) -> list[dict]:
    param_defs = [
        ParamDef(
            key="supertrend.atr_len",
            low=atr_low,
            high=atr_high,
            step=atr_step,
            dtype="int",
        ),
        ParamDef(
            key="supertrend.factor",
            low=factor_low,
            high=factor_high,
            step=factor_step,
            dtype="float",
        ),
    ]
    results = grid_search(
        df=df,
        base_config=deepcopy(base_config),
        param_defs=param_defs,
        out_path=out_path,
        warmup_bars=200,
        eval_start=eval_start,
        eval_end=eval_end,
        min_trades=10,
        max_dd_pct=80.0,
        workers=workers,
    )
    rows = []
    for r in results:
        row = {
            "idx": r.idx,
            "score": r.score if r.score > float("-inf") else None,
            "net_profit": r.net_profit,
            "max_dd_pct": r.max_dd_pct,
            "total_trades": r.total_trades,
            "win_rate": r.win_rate,
            "profit_factor": r.profit_factor,
            "runtime_s": r.runtime_s,
            "status": r.status,
            "prune_reason": r.prune_reason,
            "min_trades_threshold": r.min_trades_threshold,
            "max_dd_threshold_pct": r.max_dd_threshold_pct,
            "pruned_metric_value": r.pruned_metric_value,
        }
        row.update(r.params)
        rows.append(row)
    return rows


def main() -> None:
    df = _load_data()
    base_config = _load_base_config()
    eval_start = datetime(2025, 6, 30, 7, 45, tzinfo=timezone.utc)
    eval_end = datetime(2026, 1, 1, 0, 0, tzinfo=timezone.utc)
    workers = max(1, (os.cpu_count() or 1) - 1)

    print("\n-- Fine Grid Setup --")
    print(f"  Eval Window    : {eval_start} -- {eval_end}")
    print(f"  Workers        : {workers}")
    print(f"  Parity Mode    : {base_config.parity.enabled}")
    print(f"  Terminal Close : {base_config.parity.force_terminal_manual_close}")

    out_dir = PROJECT_ROOT / "optimize_results"
    out_dir.mkdir(exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")

    combined_rows: list[dict] = []
    cluster_summaries: list[dict] = []

    for grid in FINE_GRIDS:
        cluster_name = str(grid["name"])
        cluster_csv = out_dir / f"supertrend_atr_factor_fine_{cluster_name}_{timestamp}.csv"
        print("\n" + "=" * 80)
        print(f"Running cluster: {cluster_name}")
        print(
            "  "
            f"ATR {grid['atr_low']}..{grid['atr_high']} step {grid['atr_step']} | "
            f"Factor {grid['factor_low']}..{grid['factor_high']} step {grid['factor_step']}"
        )
        print(f"  Output CSV: {cluster_csv}")
        print("=" * 80)

        rows = _run_grid(
            df=df,
            base_config=base_config,
            out_path=cluster_csv,
            atr_low=int(grid["atr_low"]),
            atr_high=int(grid["atr_high"]),
            atr_step=int(grid["atr_step"]),
            factor_low=float(grid["factor_low"]),
            factor_high=float(grid["factor_high"]),
            factor_step=float(grid["factor_step"]),
            eval_start=eval_start,
            eval_end=eval_end,
            workers=workers,
        )
        for row in rows:
            row["cluster"] = cluster_name
        combined_rows.extend(rows)

        ok_rows = [r for r in rows if r["status"] == "OK"]
        if ok_rows:
            best = sorted(ok_rows, key=lambda x: x["score"], reverse=True)[0]
            cluster_summaries.append(
                {
                    "cluster": cluster_name,
                    "best_atr_len": best["supertrend.atr_len"],
                    "best_factor": best["supertrend.factor"],
                    "best_score": best["score"],
                    "best_net_profit": best["net_profit"],
                    "best_max_dd_pct": best["max_dd_pct"],
                    "best_total_trades": best["total_trades"],
                    "best_win_rate": best["win_rate"],
                    "best_profit_factor": best["profit_factor"],
                }
            )

    combined_df = pd.DataFrame(combined_rows)
    combined_csv = out_dir / f"supertrend_atr_factor_fine_combined_{timestamp}.csv"
    combined_xlsx = combined_csv.with_suffix(".xlsx")
    summary_df = pd.DataFrame(cluster_summaries)

    combined_df.to_csv(combined_csv, index=False)
    with pd.ExcelWriter(combined_xlsx, engine="openpyxl") as writer:
        combined_df.to_excel(writer, index=False, sheet_name="results")
        summary_df.to_excel(writer, index=False, sheet_name="summary")

    print("\n" + "=" * 80)
    print("Fine-grid complete")
    print(f"Combined CSV : {combined_csv}")
    print(f"Combined XLSX: {combined_xlsx}")
    if not summary_df.empty:
        print("\nBest per cluster:")
        print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
