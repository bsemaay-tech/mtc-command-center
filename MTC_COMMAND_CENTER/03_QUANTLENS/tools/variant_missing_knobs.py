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


def grid_triple_ema_tuned():
    out = []
    for f in (3, 5, 8):
        for m in (13, 21):
            for s in (34, 50, 100):
                if f < m < s:
                    for touch in (0.25, 0.5, 0.75):
                        out.append({"e_fast": f, "e_mid": m, "e_slow": s, "touch_atr": touch})
    return out  # promote the fixed 5/13/50 stack to swept knobs


def grid_ema_pullback_tuned():
    out = []
    for el in (5, 8, 13, 21):
        for pa in (0.3, 0.5, 0.65):
            for ia in (0.5, 1.0):
                for sw in (3, 5):
                    out.append({"ema_len": el, "pullback_atr": pa, "impulse_atr": ia, "slope_window": sw})
    return out  # promote the fixed ema_8 anchor to a swept period


def grid_bb_mult_tuned():
    out = []
    for bb_len in (20, 30, 50):
        for mult in (1.5, 2.0, 2.5, 3.0):
            for body in (0.2, 0.45):
                out.append({"bb_len": bb_len, "mult": mult, "body_atr": body})
    return out  # promote the fixed 2.0 std multiplier to a swept knob


def grid_macd_nofilter():
    out = []
    for f in (8, 12, 17):
        for s in (21, 26, 34):
            if f < s:
                for sig in (5, 9, 13):
                    out.append({"fast": f, "slow": s, "signal": sig})
    return out  # MACD cross WITHOUT the hardcoded ema_200 trend gate


def grid_rsi_trend_gated():
    out = []
    for rl in (7, 14, 21):
        for ob in (25, 30, 35):
            for rec in (40, 45, 50):
                if rec > ob:
                    out.append({"rsi_len": rl, "oversold": ob, "recovery": rec})
    return out  # RSI oversold WITH an added ema_200 regime gate


def grid_golden_atr_stop():
    out = []
    for fast in (20, 50):
        for slow in (100, 200):
            if fast < slow:
                for pull in (0.25, 0.5):
                    for stop_mult in (1.5, 2.5, 3.5):
                        out.append({"fast_ema": fast, "slow_ema": slow, "pull_atr": pull, "atr_stop_mult": stop_mult})
    return out  # golden-cross pullback with an ATR stop instead of the swing-low stop


NEW_GRIDS = {
    "GEN_DONCHIAN_TURTLE": grid_donchian_turtle(),
    "GEN_TRIPLE_EMA_TUNED": grid_triple_ema_tuned(),
    "GEN_EMA_PULLBACK_TUNED": grid_ema_pullback_tuned(),
    "GEN_BB_MULT_TUNED": grid_bb_mult_tuned(),
    "GEN_MACD_NOFILTER": grid_macd_nofilter(),
    "GEN_RSI_TREND_GATED": grid_rsi_trend_gated(),
    "GEN_GOLDEN_ATR_STOP": grid_golden_atr_stop(),
}


def signals_new(strategy, df, params, daily_rsi_map=None):
    close = df["close"]; high = df["high"]; low = df["low"]; open_ = df["open"]
    if "atr_14" not in df:
        df["atr_14"] = mw.atr(df, 14)
    atr = df["atr_14"]

    if strategy == "GEN_DONCHIAN_TURTLE":
        ech = int(params["entry_channel_len"]); xch = int(params["exit_channel_len"])
        hh = high.rolling(ech, min_periods=ech).max().shift(1)
        buf = params.get("atr_buf", 0.0) * atr
        sig = close > (hh + buf)
        stop = low.rolling(xch, min_periods=1).min()  # Turtle STRUCTURAL stop (opposite channel)
        return sig.fillna(False), stop

    if strategy == "GEN_TRIPLE_EMA_TUNED":
        ef = mw.ema(close, int(params["e_fast"])); em = mw.ema(close, int(params["e_mid"])); es = mw.ema(close, int(params["e_slow"]))
        dist = (close - em).abs() / atr
        sig = (ef > em) & (em > es) & (dist <= params["touch_atr"]) & (close > open_)
        stop = low.rolling(10, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "GEN_EMA_PULLBACK_TUNED":
        el = int(params["ema_len"]); sw = int(params.get("slope_window", 3))
        e = mw.ema(close, el)
        slope = e - e.shift(sw)
        dist = (close - e).abs() / atr
        impulse = (close - close.shift(sw)).abs() / atr
        sig = (close > e) & (slope > 0) & (dist <= params["pullback_atr"]) & (impulse.shift(1) >= params["impulse_atr"])
        stop = low.rolling(3, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "GEN_BB_MULT_TUNED":
        bb_len = int(params["bb_len"]); mult = params["mult"]
        mid = mw.sma(close, bb_len); std = close.rolling(bb_len, min_periods=bb_len).std()
        upper = mid + mult * std
        body_ok = (close - open_).abs() >= params["body_atr"] * atr
        sig = (close > upper) & (close.shift(1) <= upper.shift(1)) & body_ok
        stop = low.rolling(5, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "GEN_MACD_NOFILTER":
        fast = mw.ema(close, int(params["fast"])); slow = mw.ema(close, int(params["slow"]))
        macd = fast - slow; sigl = mw.ema(macd, int(params["signal"]))
        sig = (macd.shift(1) <= sigl.shift(1)) & (macd > sigl)  # NO ema_200 filter (base forces it)
        stop = low.rolling(5, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "GEN_RSI_TREND_GATED":
        r = mw.rsi(close, int(params["rsi_len"])); e200 = mw.ema(close, 200)
        sig = (r.shift(1) < params["oversold"]) & (r >= params["recovery"]) & (close > e200)  # ADDED trend gate
        stop = low.rolling(5, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "GEN_GOLDEN_ATR_STOP":
        f = mw.ema(close, int(params["fast_ema"])); s = mw.ema(close, int(params["slow_ema"]))
        dist = (close - f).abs() / atr
        sig = (f > s) & (close > f) & (dist <= params["pull_atr"])
        stop = close - params.get("atr_stop_mult", 2.0) * atr  # ATR stop instead of swing-low
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
