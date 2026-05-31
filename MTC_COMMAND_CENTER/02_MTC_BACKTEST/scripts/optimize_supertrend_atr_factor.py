"""
Supertrend ATR Length x Factor Grid Optimization
=================================================
Naked Supertrend signals only (all filters/guards/SL/TP OFF).
Baseline: ATR=21, Factor=4.0 from MT_CORE2 TV export.

Grid:
  ATR Length : 7 -> 50, step 1  (44 values)
  Factor     : 1.0 -> 8.0, step 0.5  (15 values)
  Total      : 660 combinations

Usage:
  cd mtc_backtest
  python scripts/optimize_supertrend_atr_factor.py
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

# Ensure project root on path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config.defaults import MTCConfig
from src.optimizer_v0.search import ParamDef, grid_search, print_top_n


def main():
    # -- 1. Load data -----------------------------------------------
    data_path = PROJECT_ROOT / "data" / "BTCUSDT_PERP_15m_20240101_20260101_long.parquet"
    print(f"Loading data: {data_path}")
    df = pd.read_parquet(data_path)
    if "timestamp" in df.columns:
        ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        print(f"  Rows: {len(df):,}  |  Range: {ts.min()} -- {ts.max()}")
    else:
        print(f"  Rows: {len(df):,}  |  Range: {df.index.min()} -- {df.index.max()}")

    # -- 2. Load baseline config ------------------------------------
    config_path = PROJECT_ROOT / "configs" / "cases" / "supertrend_atr_factor_optimize.json"
    with open(config_path, encoding="utf-8") as f:
        cfg_dict = json.load(f)
    # Remove meta keys
    cfg_dict.pop("_meta", None)
    base_config = MTCConfig.model_validate(cfg_dict)
    # TV workbook exports are for BINANCE:BTCUSDT.P and include a terminal
    # MANUAL close at eval-window end. Keep optimizer runs on the same contract.
    base_config.parity.enabled = True
    base_config.parity.force_terminal_manual_close = True

    # Verify key settings
    print("\n-- Baseline Config --")
    print(f"  Signal Mode    : {base_config.signal_mode}")
    print(f"  Entry Mode     : {base_config.trade.entry_mode}")
    print(f"  ST ATR Len     : {base_config.supertrend.atr_len}")
    print(f"  ST Factor      : {base_config.supertrend.factor}")
    print(f"  ST Use Wicks   : {base_config.supertrend.use_wicks}")
    print(f"  ST Use HA      : {base_config.supertrend.use_ha}")
    print(f"  SL Enabled     : {base_config.stop_loss.enabled}")
    print(f"  TP Enabled     : {base_config.take_profit.enabled}")
    print(f"  BE Enabled     : {base_config.break_even.enabled}")
    print(f"  Trailing       : {base_config.trailing.enabled}")
    print(f"  MA Filter      : {base_config.filters.use_ma_filter}")
    print(f"  MACD Filter    : {base_config.filters.use_macd_filter}")
    print(f"  Confirmation   : {base_config.confirmation.enabled}")
    print(f"  Commission     : {base_config.strategy.commission_percent}%")
    print(f"  Capital        : {base_config.strategy.initial_capital}")
    print(f"  Exit Opposite  : {base_config.trade.exit_on_opposite_signal}")
    print(f"  Parity Mode    : {base_config.parity.enabled}")
    print(f"  Terminal Close : {base_config.parity.force_terminal_manual_close}")

    # -- 3. Define eval window (matching TV export) -----------------
    eval_start = datetime(2025, 6, 30, 7, 45, tzinfo=timezone.utc)
    eval_end   = datetime(2026, 1, 1, 0, 0, tzinfo=timezone.utc)
    print(f"\n  Eval Window    : {eval_start} -- {eval_end}")

    # -- 4. Define search space -------------------------------------
    # Phase 1: Coarse grid (step=2 for ATR, step=0.5 for Factor)
    # 22 x 15 = 330 combos (~2h with parallel workers)
    param_defs = [
        ParamDef(key="supertrend.atr_len", low=7, high=50, step=2, dtype="int"),
        ParamDef(key="supertrend.factor",  low=1.0, high=8.0, step=0.5, dtype="float"),
    ]

    total_combos = 1
    for p in param_defs:
        total_combos *= len(p.grid_values())
    print(f"\n  Search Space   : {total_combos} combinations")
    for p in param_defs:
        vals = p.grid_values()
        print(f"    {p.key}: {vals[0]} -- {vals[-1]} (step={p.step}, count={len(vals)})")

    # -- 5. Output path ---------------------------------------------
    out_dir = PROJECT_ROOT / "optimize_results"
    out_dir.mkdir(exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"supertrend_atr_factor_{timestamp}.csv"
    print(f"\n  Output CSV     : {out_path}")

    # -- 6. Run grid search -----------------------------------------
    cpu_count = os.cpu_count() or 1
    workers = max(1, cpu_count - 1)  # Leave 1 core free
    print(f"\n{'='*80}")
    print(f"Starting grid search with {workers} workers...")
    print(f"{'='*80}\n")

    t0 = time.time()
    results = grid_search(
        df=df,
        base_config=base_config,
        param_defs=param_defs,
        out_path=out_path,
        warmup_bars=200,
        eval_start=eval_start,
        eval_end=eval_end,
        min_trades=10,      # Low threshold since naked signals may have few trades with high ATR
        max_dd_pct=80.0,    # Relaxed since no SL
        workers=workers,
    )
    elapsed = time.time() - t0

    # -- 7. Print results -------------------------------------------
    print(f"\nCompleted in {elapsed:.1f}s ({elapsed/60:.1f} min)")
    print_top_n(results, n=20)

    # -- 8. Find baseline result ------------------------------------
    baseline = [r for r in results
                if r.params.get("supertrend.atr_len") == 21
                and r.params.get("supertrend.factor") == 4.0]
    if baseline:
        b = baseline[0]
        print(f"\n-- Baseline (ATR=21, Factor=4.0) --")
        print(f"  Score         : {b.score:.4f}")
        print(f"  Net Profit    : {b.net_profit:.2f}")
        print(f"  Max DD%       : {b.max_dd_pct:.1f}%")
        print(f"  Total Trades  : {b.total_trades}")
        print(f"  Win Rate      : {b.win_rate:.1f}%")
        print(f"  Profit Factor : {b.profit_factor:.2f}")

    print(f"\nResults saved to: {out_path}")


if __name__ == "__main__":
    main()
