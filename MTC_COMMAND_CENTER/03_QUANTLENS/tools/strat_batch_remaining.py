"""Remaining CODEABLE strategies — STG028/033/034/046/053.

Monkey-patch chain: strat_batch_023_034 → strat_extra_runner → overnight_v2_runner
→ mega_walk_forward. No engine file edits.

New strategies (5 families):
  QL_CANSLIM_SHAKEOUT_v1   (STG028)  6 configs  — shakeout proxy + uptrend
  QL_ANTI_CHASE_CRABEL_v1  (STG033) 12 configs  — Crabel range expansion minus chase
  QL_EMA_RETEST_v1         (STG034)  4 configs  — EMA20/50 second retest long
  QL_VWAP_TREND_CONT_v1    (STG046) 18 configs  — VWAP trend continuation (Setup A)
  QL_HARRIS_50DMA_v1       (STG053)  6 configs  — Charles Harris 50DMA/21EMA pullback

STG061 (Ryan Pierpont) + STG063 (Tito) reclassified PRE_REG_NEEDED:
  specs state "Backtest Readiness: Needs review — formalize thresholds first".

Design notes:
  - STG028: dollar-based buy_point from run_batch.py replaced with % logic (crypto)
  - STG033: anti-chase filter wraps Crabel logic; long-only for MEGA worker
  - STG034: groupby-cumsum retest count preserves original run_batch.py logic
  - STG046: session-VWAP → rolling-typical-price (no volume in MEGA bundle)
    Setup B (V-reversal, needs volume for capitulation) NOT implemented
  - STG053: FIRST_PULLBACK_50DMA + 21EMA_PULLBACK mechanical subsets only;
    SWING_AROUND_CORE and REVERSE_PYRAMID are discretionary, not implemented

Launch:
  python strat_batch_remaining.py         # single MEGA sweep
  bash overnight_remaining_2026-06-07.sh  # full overnight pipeline
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import strat_extra_batch_023_034 as _b023  # noqa: E402  stacks all prior patches
import mega_walk_forward as mw              # noqa: E402
import numpy as np                          # noqa: E402
import pandas as pd                         # noqa: E402


# ------------------------------------------------------------------ #
# Helpers                                                               #
# ------------------------------------------------------------------ #

def _atr14(df: pd.DataFrame) -> pd.Series:
    return mw.atr(df, 14)


def _rolling_vwap(df: pd.DataFrame, length: int) -> pd.Series:
    """Rolling VWAP proxy (equal-weight when no volume column)."""
    typical = (df["high"] + df["low"] + df["close"]) / 3
    if "volume" in df.columns:
        vol = df["volume"].replace(0, 1.0)
        return (
            (typical * vol).rolling(length, min_periods=length).sum()
            / vol.rolling(length, min_periods=length).sum()
        )
    return typical.rolling(length, min_periods=length).mean()


# ------------------------------------------------------------------ #
# STG028 — CANSLIM Shakeout Proxy                                      #
# ------------------------------------------------------------------ #

def grid_canslim() -> list[dict]:
    """6 configs: 2 uptrend thresholds × 3 target_pct."""
    return [
        {"uptrend_pct": u, "target_pct": t}
        for u in [0.20, 0.30]
        for t in [10.0, 20.0, 30.0]
    ]


def _sig_canslim_shakeout(df: pd.DataFrame, params: dict):
    uptrend_pct = params.get("uptrend_pct", 0.30)
    close = df["close"]
    high = df["high"]
    low = df["low"]

    # 6-month uptrend (~126 bars on daily; accept shorter warmup via min_periods)
    prior_close = close.shift(126)
    uptrend = (close / prior_close.replace(0, np.nan) - 1) >= uptrend_pct

    # Shakeout: recent 20-bar low undercuts prior 40-bar low (weak hands shaken)
    l40 = low.rolling(40, min_periods=20).min().shift(20)  # prior 40-bar support
    l20 = low.rolling(20, min_periods=10).min()
    shakeout = (l20 < l40).shift(1)  # confirmed prior bar

    # Buy point: 5% above the undercut support (reclaim entry)
    buy_point = l40.shift(1) * 1.05

    long_sig = uptrend & shakeout & (high >= buy_point)
    long_stop = pd.Series(
        np.where(long_sig, buy_point * 0.93, np.nan), index=close.index
    )
    return long_sig.fillna(False), long_stop, "long"


# ------------------------------------------------------------------ #
# STG033 — Anti-Chase Crabel (range expansion minus strong-run chase) #
# ------------------------------------------------------------------ #

def grid_anti_chase() -> list[dict]:
    """12 configs: 3 mult × 2 lookback × 2 atr_block_mult."""
    return [
        {"mult": m, "lookback": lb, "block_mult": bm}
        for m in [0.8, 0.9, 1.0]
        for lb in [2, 3]
        for bm in [0.5, 0.7]
    ]


def _sig_anti_chase_crabel(df: pd.DataFrame, params: dict):
    mult = params.get("mult", 0.9)
    lookback = params.get("lookback", 3)
    block_mult = params.get("block_mult", 0.5)

    close = df["close"]
    high = df["high"]
    low = df["low"]
    a = _atr14(df)

    # Crabel core: narrow-range day followed by range expansion entry
    daily_range = high - low
    narrow = (daily_range < mult * a).shift(1)          # yesterday was narrow
    buy_stop = high.shift(1) + 0.001 * close.shift(1)   # just above yesterday's high
    long_core = narrow & (high >= buy_stop)

    # Anti-chase filter: block if last `lookback` bars all strong green
    body = (close - df["open"]).abs()
    loc = (close - low) / (high - low).replace(0, np.nan)
    strong_green = (close > df["open"]) & (body >= block_mult * a) & (loc >= 0.70)
    block_long = strong_green.shift(1).rolling(lookback, min_periods=lookback).sum() >= lookback

    long_sig = long_core & ~block_long
    long_stop = pd.Series(
        np.where(long_sig, close.shift(1) * 0.97, np.nan), index=close.index
    )
    return long_sig.fillna(False), long_stop, "long"


# ------------------------------------------------------------------ #
# STG034 — EMA20/50 Two-Retests Baseline                               #
# ------------------------------------------------------------------ #

def grid_ema_retest() -> list[dict]:
    """4 configs: 2 tolerance × 2 atr_stop_mult."""
    return [
        {"tolerance": t, "atr_stop_mult": s}
        for t in [0.008, 0.015]
        for s in [1.5, 2.5]
    ]


def _sig_ema_retest(df: pd.DataFrame, params: dict):
    tol = params.get("tolerance", 0.01)
    atr_mult = params.get("atr_stop_mult", 2.0)

    close = df["close"]
    high = df["high"]
    low = df["low"]

    e20 = mw.ema(close, 20)
    e50 = mw.ema(close, 50)

    # Crossup: EMA20 crosses above EMA50
    cross_up = (e20 > e50) & (e20.shift(1) <= e50.shift(1))
    since_up = cross_up.cumsum()   # partition: each block = one bull phase

    # Retest: bar's low dips to/below EMA20 (within tolerance) but closes above
    retest_long = (low <= e20 * (1.0 + tol)) & (close > e20)

    # Count retests within each bull phase
    long_count = retest_long.groupby(since_up).cumsum()

    # Signal: exactly the 2nd retest (not the 1st; avoids noise entry)
    long_sig = (e20 > e50) & (long_count >= 2) & (long_count.shift(1) < 2)

    a = _atr14(df)
    long_stop = pd.Series(
        np.where(long_sig, close - atr_mult * a, np.nan), index=close.index
    )
    return long_sig.fillna(False), long_stop, "long"


# ------------------------------------------------------------------ #
# STG046 — VWAP Trend Continuation (Setup A only)                      #
# ------------------------------------------------------------------ #

def grid_vwap_trend() -> list[dict]:
    """18 configs: 3 vwap_len × 3 above_ratio_thresh × 2 breakout_lb."""
    return [
        {"vwap_len": vl, "above_ratio_thresh": ar, "breakout_lb": bl}
        for vl in [12, 24, 48]        # rolling bars for "session" VWAP proxy
        for ar in [0.55, 0.65, 0.75]  # min fraction of bars above VWAP
        for bl in [8, 16]             # N-bar range breakout lookback
    ]


def _sig_vwap_trend_cont(df: pd.DataFrame, params: dict):
    vwap_len = params.get("vwap_len", 24)
    above_thresh = params.get("above_ratio_thresh", 0.60)
    brk_lb = params.get("breakout_lb", 12)

    close = df["close"]
    high = df["high"]

    # Rolling VWAP proxy (no session boundaries in crypto MEGA data)
    vwap = _rolling_vwap(df, vwap_len)

    # Fraction of last vwap_len bars where close > vwap (trend health)
    above = (close > vwap).rolling(vwap_len, min_periods=vwap_len // 2).mean()

    # VWAP slope: vwap rising
    vwap_slope = vwap > vwap.shift(3)

    # Close slope: close rising
    close_slope = close > close.shift(3)

    # Range breakout: close above N-bar high (excluding current bar)
    range_high = high.shift(1).rolling(brk_lb, min_periods=brk_lb // 2).max()

    # Trend continuation long: VWAP trending, price above VWAP, new high breakout
    long_sig = (
        (above >= above_thresh)
        & vwap_slope
        & close_slope
        & (close > range_high)
        & (close > vwap)
    )

    a = _atr14(df)
    long_stop = pd.Series(
        np.where(long_sig, close - 1.5 * a, np.nan), index=close.index
    )
    return long_sig.fillna(False), long_stop, "long"


# ------------------------------------------------------------------ #
# STG053 — Charles Harris 50DMA/21EMA Pullback                         #
# ------------------------------------------------------------------ #

def grid_harris() -> list[dict]:
    """6 configs: 2 modes × 3 touch tolerance ATR multiples."""
    return [
        {"mode": m, "touch_atr_mult": t}
        for m in ["50DMA", "21EMA"]
        for t in [0.3, 0.6, 1.0]
    ]


def _sig_harris_pullback(df: pd.DataFrame, params: dict):
    mode = params.get("mode", "50DMA")
    touch_mult = params.get("touch_atr_mult", 0.5)

    close = df["close"]
    high = df["high"]
    low = df["low"]
    a = _atr14(df)

    if mode == "50DMA":
        ma = mw.sma(close, 50)
    else:  # 21EMA
        ma = mw.ema(close, 21)

    # Uptrend context: close above MA (rising support)
    uptrend = close > ma

    # Pullback touch: prior bar's low came within touch_mult×ATR of MA
    touch_zone_hi = ma.shift(1) + touch_mult * a.shift(1)
    touch_zone_lo = ma.shift(1) - touch_mult * a.shift(1)
    touched = (low.shift(1) <= touch_zone_hi) & (high.shift(1) >= touch_zone_lo)

    # Recovery: close back above MA after touch
    long_sig = uptrend & touched & (close > ma)

    long_stop = pd.Series(
        np.where(long_sig, low.shift(1) - 0.002 * close, np.nan), index=close.index
    )
    return long_sig.fillna(False), long_stop, "long"


# ------------------------------------------------------------------ #
# Registration                                                          #
# ------------------------------------------------------------------ #

REMAINING_GRIDS: dict[str, list[dict]] = {
    "QL_CANSLIM_SHAKEOUT_v1":  grid_canslim(),      #  6
    "QL_ANTI_CHASE_CRABEL_v1": grid_anti_chase(),   # 12
    "QL_EMA_RETEST_v1":        grid_ema_retest(),   #  4
    "QL_VWAP_TREND_CONT_v1":   grid_vwap_trend(),   # 18
    "QL_HARRIS_50DMA_v1":      grid_harris(),       #  6
}

mw.GRIDS.update(REMAINING_GRIDS)

_DISPATCH_R: dict[str, callable] = {
    "QL_CANSLIM_SHAKEOUT_v1":  _sig_canslim_shakeout,
    "QL_ANTI_CHASE_CRABEL_v1": _sig_anti_chase_crabel,
    "QL_EMA_RETEST_v1":        _sig_ema_retest,
    "QL_VWAP_TREND_CONT_v1":   _sig_vwap_trend_cont,
    "QL_HARRIS_50DMA_v1":      _sig_harris_pullback,
}

_prev_build_r = mw.build_signals


def _remaining_build_signals(strategy, df, params, daily_rsi_map=None):
    fn = _DISPATCH_R.get(strategy)
    if fn is not None:
        return fn(df, params)
    return _prev_build_r(strategy, df, params, daily_rsi_map)


mw.build_signals = _remaining_build_signals

_n_new = len(REMAINING_GRIDS)
_n_cfg = sum(len(v) for v in REMAINING_GRIDS.values())
print(
    f"[strat_remaining] +{_n_new} strategies, +{_n_cfg} configs; "
    f"GRIDS total={len(mw.GRIDS)}",
    flush=True,
)

if __name__ == "__main__":
    mw.main()
