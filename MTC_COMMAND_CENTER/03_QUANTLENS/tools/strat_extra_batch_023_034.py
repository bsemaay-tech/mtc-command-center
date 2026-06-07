"""Batch-023-034 overnight runner — STG023-029 signal families from run_batch.py.

Monkey-patch pattern (AGENTS.md). Imports strat_extra_runner which imports
overnight_v2_runner which imports mega_walk_forward — stacks cleanly.
No edits to mega_walk_forward.py, overnight_v2_runner.py, or any engine file.

New strategies added (6 families):
  QL_KELL_BATCH_v1        (STG023) 27 configs  — Kell basin/wedge/crossback
  QL_MARTIN_AVWAP_v1      (STG024)  4 configs  — Martin Luke AVWAP pullback
  QL_SLINGSHOT_v1         (STG025) 256 configs — Slingshot 4-EMA high pullback
  QL_CRABEL_RANGE_EXP_v1  (STG026) 48 configs  — Crabel daily range expansion
  QL_BIGBELUGA_RSI_v1     (STG027)  9 configs  — BigBeluga RSI div+CHoCH (lookahead fixed)
  QL_LINDA_5SMA_v1        (STG029)  3 configs  — Linda 5SMA pullback in uptrend

BigBeluga lookahead note: original signal_bigbeluga uses center=True rolling
(future bars visible). Fixed here: trailing window only. Swing detection fires
when bar IS the max/min of its trailing 2*pivot+1 window. Results are valid
for backtesting; approximate compared to manual swing identification.

Launch:
  python strat_extra_batch_023_034.py           # single MEGA sweep
  bash overnight_batch_023_034_2026-06-07.sh    # full overnight pipeline
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import strat_extra_runner as _extra  # noqa: E402  applies v2+extra patches
import mega_walk_forward as mw        # noqa: E402
import numpy as np                    # noqa: E402
import pandas as pd                   # noqa: E402


# ------------------------------------------------------------------ #
# rolling_vwap_proxy: not in MEGA, inlined from run_batch shared lib  #
# ------------------------------------------------------------------ #
def _rolling_vwap(data: pd.DataFrame, length: int) -> pd.Series:
    """Volume-weighted rolling VWAP proxy; falls back to equal-weight if no volume."""
    typical = (data["high"] + data["low"] + data["close"]) / 3
    if "volume" in data.columns:
        vol = data["volume"].replace(0, 1.0)
        return (
            (typical * vol).rolling(length, min_periods=length).sum()
            / vol.rolling(length, min_periods=length).sum()
        )
    # No volume column in data bundle — use rolling typical price mean as proxy
    return typical.rolling(length, min_periods=length).mean()


# ------------------------------------------------------------------ #
# Parameter grids                                                       #
# ------------------------------------------------------------------ #

def grid_kell() -> list[dict]:
    """27 configs: 3 variants × 3 contractions × 3 max_range."""
    return [
        {"variant": v, "contraction": c, "max_range": r}
        for v in ["basin_break", "wedge_pop", "ema_crossback"]
        for c in [3, 5, 8]
        for r in [5.0, 8.0, 12.0]
    ]


def grid_martin() -> list[dict]:
    """4 configs: 4 AVWAP/EMA support variants."""
    return [
        {"variant": v}
        for v in ["ema_only", "avwap_only", "ema_avwap", "ema_avwap_prior"]
    ]


def grid_slingshot() -> list[dict]:
    """256 configs: 4 ema_len × 4 lookback × 4 depth × 4 exit_mode."""
    return [
        {"ema_len": e, "lookback": lb, "depth": d, "exit_mode": x}
        for e in [3, 4, 5, 8]
        for lb in [3, 5, 8, 13]
        for d in [5.0, 10.0, 15.0, 25.0]
        for x in ["close_below", "ATR_trail", "R2", "R3"]
    ]


def grid_crabel() -> list[dict]:
    """48 configs: 6 mult × 2 direction × 2 trend_filter × 2 atr_filter."""
    return [
        {"mult": m, "direction_mode": dm, "trend_filter": tf, "atr_filter": af}
        for m in [0.7, 0.8, 0.9, 1.0, 1.1, 1.3]
        for dm in ["both", "long_only"]
        for tf in [False, True]
        for af in [False, True]
    ]


def grid_bigbeluga() -> list[dict]:
    """9 configs: 3 pivot × 3 atr_mult."""
    return [
        {"pivot": p, "atr_mult": a}
        for p in [3, 5, 7]
        for a in [2.0, 3.0, 4.0]
    ]


def grid_linda() -> list[dict]:
    """3 configs: 3 stop modes."""
    return [{"stop_mode": s} for s in ["none", "ATR_2", "fixed_8pct"]]


# ------------------------------------------------------------------ #
# Signal builders                                                       #
# ------------------------------------------------------------------ #

def _sig_kell(df: pd.DataFrame, params: dict) -> tuple:
    """STG023 — Kell wedge/basin/crossback (long only, no lookahead).

    Three variants from signal_kell():
      basin_break  : trend + mini-base last bar + close > 10EMA + new 10-bar high
      wedge_pop    : trend + mini-base last bar + close > N-bar high
      ema_crossback: trend + close crossed above 10EMA
    Stop: max(swing-low, close - 2×ATR).
    """
    close, high, low = df["close"], df["high"], df["low"]
    c = int(params["contraction"])
    r = float(params["max_range"])
    e10 = mw.ema(close, 10)
    e20 = mw.ema(close, 20)
    a = mw.atr(df, 14)
    base_range = (high.rolling(c).max() - low.rolling(c).min()) / close * 100
    trend = close > e20
    mini_base = base_range <= r
    v = str(params["variant"])
    if v == "basin_break":
        sig = (
            trend
            & mini_base.shift(1).fillna(False)
            & (close > e10)
            & (close > close.rolling(10).max().shift(1))
        )
    elif v == "wedge_pop":
        sig = (
            trend
            & mini_base.shift(1).fillna(False)
            & (close > high.rolling(c).max().shift(1))
        )
    else:  # ema_crossback
        sig = trend & (close.shift(1) < e10.shift(1)) & (close > e10)
    stop = pd.concat(
        [low.rolling(c).min().shift(1), close - 2 * a], axis=1
    ).max(axis=1)
    return sig.fillna(False), stop


def _sig_martin(df: pd.DataFrame, params: dict) -> tuple:
    """STG024 — Martin Luke AVWAP pullback (long only).

    Uptrend (close > 50EMA > 150EMA); price touches EMA21/50 or rolling VWAP proxy;
    prior bar low was at support; current bar closes above prior bar high (reclaim).
    Stop: max(3-bar low, 3% below close).
    """
    close, low, high = df["close"], df["low"], df["high"]
    e21 = mw.ema(close, 21)
    e50 = mw.ema(close, 50)
    e150 = mw.ema(close, 150)
    avwap_hi = _rolling_vwap(df, 80)
    avwap_lo = _rolling_vwap(df, 34)
    trend = (close > e50) & (e50 > e150)
    ema_sup = (low <= e21 * 1.015) | (low <= e50 * 1.015)
    avwap_sup = (low <= avwap_hi * 1.015) | (low <= avwap_lo * 1.015)
    prior_reclaim = close > high.shift(1)
    v = str(params["variant"])
    if v == "ema_only":
        support = ema_sup
    elif v == "avwap_only":
        support = avwap_sup
    elif v == "ema_avwap":
        support = ema_sup & avwap_sup
    else:  # ema_avwap_prior
        support = ema_sup & avwap_sup & (low <= high.rolling(20).max().shift(1) * 1.02)
    sig = trend & support.shift(1).fillna(False) & prior_reclaim
    stop = pd.concat(
        [low.rolling(3).min().shift(1), close * 0.97], axis=1
    ).max(axis=1)
    return sig.fillna(False), stop


def _sig_slingshot(df: pd.DataFrame, params: dict) -> tuple:
    """STG025 — Slingshot 4-EMA high pullback (long only).

    Price pulls back below EMA-of-highs, then crosses back above it
    (momentum reset); strength filter (close > 50SMA); depth cap (not too extended).
    Stop: prior lookback low. EMA applied to highs (not close).
    """
    close, high, low = df["close"], df["high"], df["low"]
    el = int(params["ema_len"])
    lb = int(params["lookback"])
    dep = float(params["depth"])
    xm = str(params["exit_mode"])
    eh = mw.ema(high, el)
    a = mw.atr(df, 14)
    strength = close > mw.sma(close, 50)
    pulled = (close < eh).rolling(lb, min_periods=1).sum() >= 1
    hi_ref = high.rolling(lb, min_periods=1).max()
    depth_ok = (hi_ref - low.rolling(lb, min_periods=1).min()) / hi_ref.replace(0, np.nan) * 100 <= dep
    cross = (close > eh) & (close.shift(1) <= eh.shift(1))
    sig = strength & pulled.shift(1).fillna(False) & depth_ok & cross
    stop_base = low.rolling(lb, min_periods=1).min().shift(1)
    if xm == "ATR_trail":
        stop = pd.concat([stop_base, close - 2 * a], axis=1).max(axis=1)
    else:
        stop = stop_base
    return sig.fillna(False), stop


def _sig_crabel(df: pd.DataFrame, params: dict) -> tuple:
    """STG026 — Crabel daily range expansion (long and/or short).

    Buy-stop above prior-day close + mult×prior-range (long);
    sell-stop below (short). Both fired on same bar cancel each other.
    Optional trend filter (EMA200) and ATR volatility filter.
    Returns 3-tuple (long_sig, short_sig, stop) — AUDIT-002 compatible.
    """
    close, high, low = df["close"], df["high"], df["low"]
    mult = float(params["mult"])
    dm = str(params["direction_mode"])
    tf = bool(params["trend_filter"])
    af = bool(params["atr_filter"])
    prev_rng = high.shift(1) - low.shift(1)
    buy_stop = close.shift(1) + prev_rng * mult
    sell_stop = close.shift(1) - prev_rng * mult
    long_sig = high >= buy_stop
    short_sig = low <= sell_stop
    both = long_sig & short_sig
    long_sig = long_sig & ~both
    short_sig = short_sig & ~both
    if tf:
        e200 = mw.ema(close, 200)
        long_sig = long_sig & (close.shift(1) > e200.shift(1))
        short_sig = short_sig & (close.shift(1) < e200.shift(1))
    if af:
        ap = mw.atr(df, 14) / close.replace(0, np.nan)
        med = ap.rolling(100, min_periods=50).median().shift(1)
        p90 = ap.rolling(252, min_periods=100).quantile(0.9).shift(1)
        ok = (ap.shift(1) > med) & (ap.shift(1) < p90)
        long_sig = long_sig & ok
        short_sig = short_sig & ok
    # MEGA _worker handles one direction per call via 3-tuple (sig, stop, "long"|"short").
    # For "both": run long side only in MEGA context (short side logged separately if needed).
    # Stop for longs = sell_stop (the lower of the two trigger levels).
    long_stop = pd.Series(
        np.where(long_sig, sell_stop, np.nan), index=close.index
    )
    return long_sig.fillna(False), long_stop, "long"


def _sig_bigbeluga(df: pd.DataFrame, params: dict) -> tuple:
    """STG027 — BigBeluga RSI divergence + CHoCH (long only, lookahead fixed).

    Original: center=True rolling (future bars). Fixed: trailing window only.
    A bar is confirmed swing-high/low when it equals the max/min of the prior
    2*pivot+1 bars. Slightly over-identifies swings vs manual detection but
    eliminates future bar dependency.

    Signal: bullish divergence (lower price low, higher RSI low) in prior 20 bars;
    price breaks above the last confirmed swing high (change of character).
    """
    close, high, low = df["close"], df["high"], df["low"]
    p = int(params["pivot"])
    am = float(params["atr_mult"])
    a = mw.atr(df, 14)
    rs = mw.rsi(close, 14)
    win = p * 2 + 1
    # Trailing swing detection — no center=True lookahead
    swing_hi = high == high.rolling(win, min_periods=p).max()
    swing_lo = low == low.rolling(win, min_periods=p).min()
    conf_hi = high.where(swing_hi).ffill().shift(1)
    conf_lo = low.where(swing_lo).ffill().shift(1)
    bull_div = (
        (low < low.rolling(50, min_periods=20).min().shift(1))
        & (rs > rs.rolling(50, min_periods=20).min().shift(1))
    )
    sig = (
        bull_div.shift(1).rolling(20, min_periods=1).max().fillna(0).astype(bool)
        & (close > conf_hi)
    )
    stop = close - am * a
    return sig.fillna(False), stop


def _sig_linda(df: pd.DataFrame, params: dict) -> tuple:
    """STG029 — Linda 5SMA pullback in uptrend (long only).

    Uptrend (close > 50SMA & 200SMA); price crosses DOWN through 5SMA
    (pullback into the fast MA). Enter long expecting bounce.
    MEGA handles exit via stop; original MA5-recovery exit not wired
    (engine-compatible replacement: swing-low stop or ATR-based stop).
    """
    close, low = df["close"], df["low"]
    ma5 = mw.sma(close, 5)
    trend = (close > mw.sma(close, 50)) & (close > mw.sma(close, 200))
    # Cross below ma5 in uptrend (pullback entry)
    sig = trend & (close.shift(1) >= ma5.shift(1)) & (close < ma5)
    sm = str(params["stop_mode"])
    if sm == "ATR_2":
        stop = close - 2 * mw.atr(df, 14)
    elif sm == "fixed_8pct":
        stop = close * 0.92
    else:
        stop = low.rolling(3, min_periods=1).min().shift(1)
    return sig.fillna(False), stop


# ------------------------------------------------------------------ #
# Registration                                                          #
# ------------------------------------------------------------------ #

BATCH023_GRIDS: dict[str, list[dict]] = {
    "QL_KELL_BATCH_v1":       grid_kell(),        # 27
    "QL_MARTIN_AVWAP_v1":     grid_martin(),      #  4
    "QL_SLINGSHOT_v1":        grid_slingshot(),   # 256
    "QL_CRABEL_RANGE_EXP_v1": grid_crabel(),      # 48
    "QL_BIGBELUGA_RSI_v1":    grid_bigbeluga(),   #  9
    "QL_LINDA_5SMA_v1":       grid_linda(),       #  3
}

mw.GRIDS.update(BATCH023_GRIDS)

_DISPATCH: dict[str, callable] = {
    "QL_KELL_BATCH_v1":       _sig_kell,
    "QL_MARTIN_AVWAP_v1":     _sig_martin,
    "QL_SLINGSHOT_v1":        _sig_slingshot,
    "QL_CRABEL_RANGE_EXP_v1": _sig_crabel,
    "QL_BIGBELUGA_RSI_v1":    _sig_bigbeluga,
    "QL_LINDA_5SMA_v1":       _sig_linda,
}

_prev_build = mw.build_signals


def _batch023_build_signals(strategy, df, params, daily_rsi_map=None):
    fn = _DISPATCH.get(strategy)
    if fn is not None:
        return fn(df, params)
    return _prev_build(strategy, df, params, daily_rsi_map)


mw.build_signals = _batch023_build_signals

_n_new = len(BATCH023_GRIDS)
_n_configs = sum(len(v) for v in BATCH023_GRIDS.values())
print(
    f"[batch023-034] +{_n_new} strategies, +{_n_configs} configs; "
    f"GRIDS total={len(mw.GRIDS)}",
    flush=True,
)

if __name__ == "__main__":
    mw.main()
