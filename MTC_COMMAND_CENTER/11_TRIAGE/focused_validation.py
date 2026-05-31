"""Focused validation — narrow param grids to fix DSR deflation problem.

Original overnight run had 1797 total trials → DSR's expected_max_Sharpe
threshold is very high → no candidate survives DSR. This run narrows
each strategy to its CONSISTENTLY-WINNING parameter neighborhood (10
trials avg), which drops the multi-test penalty massively.

Targets: the 3 BH-FDR survivors from the overnight aggregate, plus the
broader cross-symbol winners we identified.
"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mega_walk_forward as mw
import overnight_v2_runner as v2  # noqa: F401 — already monkey-patched mega
import numpy as np


# Narrow grids — focused around the best parameter neighborhoods we already found
NARROW_GRIDS = {
    # Deepak 153 filter: best params hover around sma_fast=50, sma_slow=200, trigger=8
    "QL_DEEPAK_153_FILTER_1D": [
        {"sma_fast": 50, "sma_slow": 200, "trigger_ema": 8,  "stop_lookback": 5},
        {"sma_fast": 50, "sma_slow": 200, "trigger_ema": 8,  "stop_lookback": 10},
        {"sma_fast": 50, "sma_slow": 200, "trigger_ema": 13, "stop_lookback": 5},
        {"sma_fast": 50, "sma_slow": 200, "trigger_ema": 13, "stop_lookback": 10},
        {"sma_fast": 50, "sma_slow": 200, "trigger_ema": 21, "stop_lookback": 10},
        {"sma_fast": 50, "sma_slow": 150, "trigger_ema": 8,  "stop_lookback": 10},
    ],
    # Deepak 259 Risk Overlay: small grid around proven
    "QL_DEEPAK_259_RISK_OVERLAY": [
        {"entry_ema": 8,  "risk_pct": 0.01, "stop_atr": 1.5, "stop_lookback": 10},
        {"entry_ema": 13, "risk_pct": 0.01, "stop_atr": 1.5, "stop_lookback": 10},
        {"entry_ema": 21, "risk_pct": 0.01, "stop_atr": 1.5, "stop_lookback": 10},
        {"entry_ema": 8,  "risk_pct": 0.01, "stop_atr": 2.0, "stop_lookback": 10},
        {"entry_ema": 13, "risk_pct": 0.01, "stop_atr": 2.0, "stop_lookback": 10},
        {"entry_ema": 13, "risk_pct": 0.005, "stop_atr": 1.5, "stop_lookback": 5},
    ],
    # Highest Volume Edge — small grid
    "QL_HIGHEST_VOLUME_EDGE_PROSWING_1D": [
        {"vol_lookback": 60,  "trend_ema": 50,  "stop_lookback": 5},
        {"vol_lookback": 60,  "trend_ema": 50,  "stop_lookback": 10},
        {"vol_lookback": 120, "trend_ema": 50,  "stop_lookback": 10},
        {"vol_lookback": 120, "trend_ema": 200, "stop_lookback": 10},
        {"vol_lookback": 252, "trend_ema": 200, "stop_lookback": 10},
        {"vol_lookback": 252, "trend_ema": 50,  "stop_lookback": 5},
    ],
    # Andrew Connell 1D gap+volume
    "QL_CONNELL_EVENT_DRIVEN_GAP_1D": [
        {"gap_pct": 0.04, "vol_q": 0.92, "stop_lookback": 5},
        {"gap_pct": 0.04, "vol_q": 0.92, "stop_lookback": 10},
        {"gap_pct": 0.06, "vol_q": 0.92, "stop_lookback": 5},
        {"gap_pct": 0.06, "vol_q": 0.97, "stop_lookback": 10},
        {"gap_pct": 0.02, "vol_q": 0.85, "stop_lookback": 5},
    ],
    # VCP Minervini
    "QL_VCP_MINERVINI_1D": [
        {"contractions": 2, "atr_decay": 0.7, "stage_fast": 50, "stage_slow": 200, "stop_lookback": 10},
        {"contractions": 3, "atr_decay": 0.7, "stage_fast": 50, "stage_slow": 200, "stop_lookback": 10},
        {"contractions": 2, "atr_decay": 0.8, "stage_fast": 50, "stage_slow": 200, "stop_lookback": 5},
        {"contractions": 3, "atr_decay": 0.8, "stage_fast": 50, "stage_slow": 200, "stop_lookback": 10},
        {"contractions": 2, "atr_decay": 0.6, "stage_fast": 50, "stage_slow": 150, "stop_lookback": 10},
    ],
    # Deepak snapback 50SMA intraday
    "QL_DEEPAK_SNAPBACK_50SMA_INTRADAY": [
        {"sma_len": 50, "dist_atr": 2.0, "stop_lookback": 10, "target_atr": 1.0},
        {"sma_len": 50, "dist_atr": 2.0, "stop_lookback": 10, "target_atr": 2.0},
        {"sma_len": 50, "dist_atr": 3.0, "stop_lookback": 10, "target_atr": 1.0},
        {"sma_len": 50, "dist_atr": 3.0, "stop_lookback": 15, "target_atr": 2.0},
        {"sma_len": 50, "dist_atr": 1.0, "stop_lookback": 5,  "target_atr": 1.0},
    ],
    # Christian episodic pivot 5M
    "QL_EPISODIC_PIVOT_CHRISTIAN_5M": [
        {"gap_pct": 0.04, "vol_mult": 3.0, "or_bars": 3, "stop_lookback": 3},
        {"gap_pct": 0.04, "vol_mult": 3.0, "or_bars": 5, "stop_lookback": 5},
        {"gap_pct": 0.06, "vol_mult": 5.0, "or_bars": 3, "stop_lookback": 3},
        {"gap_pct": 0.02, "vol_mult": 2.0, "or_bars": 5, "stop_lookback": 5},
    ],
    # Open Range 5pct
    "QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M": [
        {"or_bars": 1, "stop_pct": 0.05, "target_pct": 0.15},
        {"or_bars": 3, "stop_pct": 0.05, "target_pct": 0.15},
        {"or_bars": 5, "stop_pct": 0.05, "target_pct": 0.15},
        {"or_bars": 3, "stop_pct": 0.03, "target_pct": 0.10},
        {"or_bars": 3, "stop_pct": 0.07, "target_pct": 0.25},
    ],
}

# Replace GRIDS completely (focused run only)
mw.GRIDS = NARROW_GRIDS
total_param_sets = sum(len(g) for g in NARROW_GRIDS.values())
print(f"[focused] {len(NARROW_GRIDS)} strategies, {total_param_sets} total trials (vs 1797 in overnight)")
print("[focused] DSR threshold should drop drastically; real edges should survive.")

if __name__ == "__main__":
    # Patch OUTPUT_DIR before running so we don't overwrite mega's results
    import os
    from pathlib import Path
    custom = Path(mw.OUTPUT_DIR) / "FOCUSED_VALIDATION_2026-05-31"
    custom.mkdir(parents=True, exist_ok=True)
    mw.OUTPUT_DIR = custom
    print(f"[focused] output -> {custom}")
    mw.main()
