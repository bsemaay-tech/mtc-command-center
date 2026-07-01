#!/usr/bin/env python3
"""
variant_missing_knobs.py  (Faz 3 — NEW strategy logic, monkey-patch, UNVALIDATED)

Adds NEW strategy variants that fill documented "missing knobs" from the param-spec
registry, WITHOUT editing the canonical engine. Follows the sanctioned monkey-patch
pattern (see overnight_v2_runner.py): extend `mega_walk_forward.GRIDS` + wrap
`build_signals`; never modify the upstream module.

WHAT THIS IS / IS NOT
- This is NEW trading logic = a NEW strategy (not a tuning of an existing one). It must
  be validated from scratch (two-stage: broad discovery -> narrow pre-registered
  confirmation) before it means anything. NOTHING here is promotable. No backtest is
  run by importing this module.
- Contract limit (honest): the engine's `simulate_slice` fixes the stop at entry and
  uses a fixed 2R target + holding limit. A TRUE trailing opposite-channel EXIT
  (re-evaluated every bar, the full Turtle signature) needs an engine-core change to
  `simulate_slice` and would alter EVERY strategy's behavior -> that is Faz 3b
  (approval-gated, not done here). What fits the (signal, stop) contract is the Turtle
  STRUCTURAL STOP: place the stop at the opposite N-low channel instead of a short
  rolling-low window. That is the variant implemented below.

VARIANTS
- GEN_DONCHIAN_TURTLE: DONCHIAN channel-breakout entry, but the stop is the opposite
  `exit_channel_len`-low channel (structural Turtle stop) rather than the base
  strategy's short `stop_lookback` rolling low. New knob: exit_channel_len.

Usage:
  import variant_missing_knobs as v; v.apply()   # patch mega_walk_forward in-process
  python variant_missing_knobs.py --smoke        # self-check: builds signals on synthetic data
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import mega_walk_forward as mw  # noqa: E402


def grid_donchian_turtle():
    out = []
    for entry_ch in (20, 40, 80):
        for exit_ch in (10, 20, 40):
            if exit_ch <= entry_ch:  # exit channel is the tighter/opposite channel
                for atr_buf in (0.0, 0.10, 0.25):
                    out.append({"entry_channel_len": entry_ch,
                                "exit_channel_len": exit_ch,
                                "atr_buf": atr_buf})
    return out  # 6 valid (entry,exit) pairs * 3 buf = 18


NEW_GRIDS = {
    "GEN_DONCHIAN_TURTLE": grid_donchian_turtle(),
}


def signals_new(strategy, df, params, daily_rsi_map=None):
    close = df["close"]; high = df["high"]; low = df["low"]
    if "atr_14" not in df:
        df["atr_14"] = mw.atr(df, 14)

    if strategy == "GEN_DONCHIAN_TURTLE":
        ech = int(params["entry_channel_len"])
        xch = int(params["exit_channel_len"])
        hh = high.rolling(ech, min_periods=ech).max().shift(1)
        buf = params.get("atr_buf", 0.0) * df["atr_14"]
        sig = close > (hh + buf)
        # Turtle STRUCTURAL stop = opposite (lower) channel, not a short rolling-low.
        stop = low.rolling(xch, min_periods=1).min()
        return sig.fillna(False), stop

    return None


_original_build_signals = mw.build_signals
_applied = False


def patched_build_signals(strategy, df, params, daily_rsi_map=None):
    if strategy in NEW_GRIDS:
        close = df["close"]
        if "atr_14" not in df: df["atr_14"] = mw.atr(df, 14)
        result = signals_new(strategy, df, params, daily_rsi_map)
        if result is None:
            return pd.Series(False, index=df.index), pd.Series(np.nan, index=df.index)
        return result
    return _original_build_signals(strategy, df, params, daily_rsi_map)


def apply():
    """Patch mega_walk_forward in-process (idempotent)."""
    global _applied
    if _applied:
        return NEW_GRIDS
    mw.GRIDS.update(NEW_GRIDS)
    mw.build_signals = patched_build_signals
    _applied = True
    return NEW_GRIDS


def _smoke():
    apply()
    n = 800
    rng = np.random.default_rng(7)
    price = 100 + np.cumsum(rng.normal(0, 1, n))
    df = pd.DataFrame({
        "open": price, "high": price + np.abs(rng.normal(0, 0.5, n)),
        "low": price - np.abs(rng.normal(0, 0.5, n)), "close": price,
        "volume": rng.integers(1, 100, n).astype(float),
    })
    total_grids = sum(len(g) for g in mw.GRIDS.values())
    print(f"[variant] GRIDS now {len(mw.GRIDS)} strategies (+{len(NEW_GRIDS)}); total param sets {total_grids}")
    for sid, grid in NEW_GRIDS.items():
        p = grid[0]
        sig, stop = mw.build_signals(sid, df.copy(), p)
        assert len(sig) == n and len(stop) == n, "signal/stop length mismatch"
        print(f"[variant] {sid}: grid={len(grid)} sample_params={p} signals={int(sig.sum())} stop_nonnull={int(stop.notna().sum())}")
    print("[variant] SMOKE OK (builds signals; NOT validated, NOT promotable)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    if args.smoke:
        _smoke()
    else:
        apply()
        print(f"[variant] applied. new strategies: {list(NEW_GRIDS)}")
