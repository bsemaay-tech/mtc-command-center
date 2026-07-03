#!/usr/bin/env python3
"""
research_archetypes_20260703.py  (Faz-3 R&D — genuinely-NEW strategy LOGIC)

Five NEW strategy archetypes that use signal sources the existing (non-robust) families
IGNORE — volume, session gaps, and volatility-regime switching. This is new logic, not a
variant/grid tweak of the breakout/EMA/RSI/MACD families (which the 2026-06-29..07-02
sweeps confirmed are non-robust on this universe).

Monkey-patch pattern (engine untouched): extend mega_walk_forward.GRIDS + wrap
build_signals. Contract-compatible (returns (signal_bool, stop_price)); the engine's
long-only sim applies its 2R target + holding limit. UNVALIDATED — nothing promotable
until a two-stage run yields robust_final.

Archetypes:
  NEW_VOL_BREAKOUT_CONFIRMED  - N-high breakout CONFIRMED by a relative-volume spike
  NEW_VOLUME_CLIMAX_REVERSAL  - reversal off a capitulation volume climax after a drop
  NEW_GAP_GO                  - session-open gap-up continuation (uses date boundary)
  NEW_VOL_REGIME_SWITCH       - regime switch: hi-vol -> breakout, lo-vol -> mean-revert
  NEW_RELVOL_MOMENTUM         - momentum entry gated by high relative volume (participation)
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


def grid_vol_breakout_confirmed():
    out = []
    for ch in (20, 40, 80):
        for vlen in (20, 50):
            for vmult in (1.5, 2.0, 3.0):
                for stop_lb in (10, 20):
                    out.append({"channel_len": ch, "vol_len": vlen, "vol_mult": vmult, "stop_lookback": stop_lb})
    return out  # 36


def grid_volume_climax_reversal():
    out = []
    for drop_atr in (1.0, 2.0, 3.0):
        for vlen in (20, 50):
            for vmult in (2.0, 3.0, 4.0):
                for look in (3, 5):
                    out.append({"drop_atr": drop_atr, "vol_len": vlen, "vol_mult": vmult, "drop_look": look})
    return out  # 36


def grid_gap_go():
    out = []
    for gap_atr in (0.5, 1.0, 2.0):
        for stop_lb in (5, 10, 20):
            for vmult in (1.0, 1.5, 2.0):
                out.append({"gap_atr": gap_atr, "stop_lookback": stop_lb, "vol_mult": vmult})
    return out  # 27


def grid_vol_regime_switch():
    out = []
    for rwin in (50, 100):
        for ch in (20, 40):
            for hi in (1.2, 1.5):
                for lo in (0.7, 0.8):
                    out.append({"regime_win": rwin, "channel_len": ch, "hi_mult": hi, "lo_mult": lo})
    return out  # 16


def grid_relvol_momentum():
    out = []
    for mom in (5, 10, 20):
        for vlen in (20, 50):
            for vmult in (1.3, 1.8, 2.5):
                for trend in (50, 100, 200):
                    out.append({"mom_win": mom, "vol_len": vlen, "vol_mult": vmult, "trend_ema": trend})
    return out  # 54


def grid_gap_fade():
    out = []
    for gap_atr in (0.5, 1.0, 2.0):
        for stop_lb in (5, 10, 20):
            for rev in (0.0, 0.3):
                out.append({"gap_atr": gap_atr, "stop_lookback": stop_lb, "rev_body_atr": rev})
    return out  # 18


def grid_vol_contraction_breakout():
    out = []
    for ch in (20, 40):
        for cfrac in (0.7, 0.9):
            for vmult in (1.5, 2.0):
                for stop_lb in (10, 20):
                    out.append({"channel_len": ch, "contract_frac": cfrac, "vol_mult": vmult, "stop_lookback": stop_lb})
    return out  # 16


def grid_inside_bar_breakout():
    out = []
    for trend in (0, 50, 200):
        for stop_lb in (5, 10, 20):
            for vmult in (1.0, 1.5):
                out.append({"trend_ema": trend, "stop_lookback": stop_lb, "vol_mult": vmult})
    return out  # 18


def grid_vwap_reversion():
    out = []
    for k in (1.0, 1.5, 2.0, 2.5):
        for trend in (0, 100, 200):
            out.append({"dev_atr": k, "trend_ema": trend})
    return out  # 12


def grid_volume_dryup_pullback():
    out = []
    for trend in (50, 100, 200):
        for fast in (10, 20):
            for dry in (0.7, 1.0):
                out.append({"trend_ema": trend, "fast_ema": fast, "dry_mult": dry})
    return out  # 12


def grid_range_expansion_thrust():
    out = []
    for k in (1.5, 2.0, 2.5):
        for top in (0.6, 0.7, 0.8):
            for trend in (50, 200):
                out.append({"range_atr": k, "close_top": top, "trend_ema": trend})
    return out  # 18


def grid_high_proximity_pullback():
    out = []
    for hi_len in (50, 100, 200):
        for prox in (0.5, 1.0, 2.0):
            for fast in (10, 20):
                out.append({"high_len": hi_len, "prox_atr": prox, "fast_ema": fast})
    return out  # 18


NEW_GRIDS = {
    "NEW_VOL_BREAKOUT_CONFIRMED": grid_vol_breakout_confirmed(),
    "NEW_VOLUME_CLIMAX_REVERSAL": grid_volume_climax_reversal(),
    "NEW_GAP_GO": grid_gap_go(),
    "NEW_VOL_REGIME_SWITCH": grid_vol_regime_switch(),
    "NEW_RELVOL_MOMENTUM": grid_relvol_momentum(),
    "NEW_GAP_FADE": grid_gap_fade(),
    "NEW_VOL_CONTRACTION_BREAKOUT": grid_vol_contraction_breakout(),
    "NEW_INSIDE_BAR_BREAKOUT": grid_inside_bar_breakout(),
    "NEW_VWAP_REVERSION": grid_vwap_reversion(),
    "NEW_VOLUME_DRYUP_PULLBACK": grid_volume_dryup_pullback(),
    "NEW_RANGE_EXPANSION_THRUST": grid_range_expansion_thrust(),
    "NEW_HIGH_PROXIMITY_PULLBACK": grid_high_proximity_pullback(),
}


def _relvol(df, vlen):
    v = df["volume"] if "volume" in df.columns else pd.Series(1.0, index=df.index)
    base = v.rolling(int(vlen), min_periods=max(2, int(vlen) // 2)).mean().replace(0, np.nan)
    return v / base


def signals_new(strategy, df, params, daily_rsi_map=None):
    close = df["close"]; high = df["high"]; low = df["low"]; open_ = df["open"]
    if "atr_14" not in df:
        df["atr_14"] = mw.atr(df, 14)
    atr = df["atr_14"]

    if strategy == "NEW_VOL_BREAKOUT_CONFIRMED":
        ch = int(params["channel_len"])
        hh = high.rolling(ch, min_periods=ch).max().shift(1)
        rv = _relvol(df, params["vol_len"])
        sig = (close > hh) & (rv >= params["vol_mult"])
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "NEW_VOLUME_CLIMAX_REVERSAL":
        look = int(params["drop_look"])
        dropped = close < (close.shift(look) - params["drop_atr"] * atr)   # recent decline
        rv = _relvol(df, params["vol_len"])
        climax = rv >= params["vol_mult"]                                   # capitulation volume
        reclaim = close > open_                                             # bullish reversal bar
        sig = dropped & climax & reclaim
        stop = low.rolling(3, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "NEW_GAP_GO":
        new_day = pd.Series(df["date"].values != pd.Series(df["date"]).shift(1).values, index=df.index) if "date" in df.columns else pd.Series(False, index=df.index)
        gap = (open_ - close.shift(1)) / atr
        rv = _relvol(df, 20)
        sig = new_day & (gap >= params["gap_atr"]) & (close > open_) & (rv >= params["vol_mult"])
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "NEW_VOL_REGIME_SWITCH":
        rwin = int(params["regime_win"]); ch = int(params["channel_len"])
        atr_med = atr.rolling(rwin, min_periods=max(5, rwin // 2)).median()
        hi_regime = atr > (params["hi_mult"] * atr_med)
        lo_regime = atr < (params["lo_mult"] * atr_med)
        breakout = close > high.rolling(ch, min_periods=ch).max().shift(1)
        ma = close.rolling(ch, min_periods=ch).mean()
        meanrev = (close < (ma - atr)) & (close > open_)                   # stretched dip that turns up
        sig = (hi_regime & breakout) | (lo_regime & meanrev)
        stop = low.rolling(10, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "NEW_RELVOL_MOMENTUM":
        mom = int(params["mom_win"])
        up = close > close.shift(mom)
        rv = _relvol(df, params["vol_len"])
        trend = mw.ema(close, int(params["trend_ema"]))
        sig = up & (rv >= params["vol_mult"]) & (close > trend)
        stop = low.rolling(10, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "NEW_GAP_FADE":
        new_day = pd.Series(df["date"].values != pd.Series(df["date"]).shift(1).values, index=df.index) if "date" in df.columns else pd.Series(False, index=df.index)
        gap = (open_ - close.shift(1)) / atr
        rev = (close - open_) >= params.get("rev_body_atr", 0.0) * atr   # intraday reversal up
        sig = new_day & (gap <= -params["gap_atr"]) & rev
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "NEW_VOL_CONTRACTION_BREAKOUT":
        ch = int(params["channel_len"])
        contracted = atr < (params["contract_frac"] * atr.rolling(ch, min_periods=ch).mean())
        brk = close > high.rolling(ch, min_periods=ch).max().shift(1)
        rv = _relvol(df, 20)
        sig = contracted.shift(1).fillna(False) & brk & (rv >= params["vol_mult"])
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "NEW_INSIDE_BAR_BREAKOUT":
        prev_inside = (high.shift(1) < high.shift(2)) & (low.shift(1) > low.shift(2))
        brk = close > high.shift(2)                                        # break the mother bar high
        te = int(params.get("trend_ema", 0) or 0)
        trend_ok = (close > mw.ema(close, te)) if te > 0 else pd.Series(True, index=df.index)
        rv = _relvol(df, 20)
        sig = prev_inside & brk & trend_ok & (rv >= params["vol_mult"])
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "NEW_VWAP_REVERSION":
        if "date" in df.columns and "volume" in df.columns:
            tp = (high + low + close) / 3.0
            pv = (tp * df["volume"]).groupby(df["date"]).cumsum()          # causal per-day cumulative
            vv = df["volume"].groupby(df["date"]).cumsum().replace(0, np.nan)
            vwap = pv / vv
        else:
            vwap = close.rolling(48, min_periods=10).mean()
        dev = (close - vwap) / atr
        te = int(params.get("trend_ema", 0) or 0)
        trend_ok = (close > mw.ema(close, te)) if te > 0 else pd.Series(True, index=df.index)
        sig = (dev <= -params["dev_atr"]) & (close > open_) & trend_ok     # stretched below VWAP, turning up
        stop = low.rolling(5, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "NEW_VOLUME_DRYUP_PULLBACK":
        trend = mw.ema(close, int(params["trend_ema"]))
        fast = mw.ema(close, int(params["fast_ema"]))
        rv = _relvol(df, 20)
        pulled = close.shift(1) < fast.shift(1)                            # prior bar pulled below fast EMA
        dry = rv.shift(1) <= params["dry_mult"]                            # on low ("dried up") volume
        sig = (close > trend) & pulled & dry & (close > open_)            # resume up in uptrend
        stop = low.rolling(10, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "NEW_RANGE_EXPANSION_THRUST":
        rng = (high - low).replace(0, np.nan)
        wide = rng > (params["range_atr"] * atr)
        strong = (close - low) / rng >= params["close_top"]
        up = close > mw.ema(close, int(params["trend_ema"]))
        sig = wide & strong & up
        stop = low.rolling(5, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "NEW_HIGH_PROXIMITY_PULLBACK":
        hl = int(params["high_len"])
        rmax = high.rolling(hl, min_periods=hl).max()
        near_high = (rmax - close) / atr <= params["prox_atr"]            # close near the trailing high
        fast = mw.ema(close, int(params["fast_ema"]))
        sig = near_high & (close > fast) & (close > open_)
        stop = low.rolling(10, min_periods=1).min()
        return sig.fillna(False), stop

    return None


_original_build_signals = mw.build_signals
_applied = False


def patched_build_signals(strategy, df, params, daily_rsi_map=None):
    if strategy in NEW_GRIDS:
        if "atr_14" not in df:
            df["atr_14"] = mw.atr(df, 14)
        result = signals_new(strategy, df, params, daily_rsi_map)
        if result is None:
            return pd.Series(False, index=df.index), pd.Series(np.nan, index=df.index)
        return result
    return _original_build_signals(strategy, df, params, daily_rsi_map)


def apply():
    global _applied
    if _applied:
        return NEW_GRIDS
    mw.GRIDS.update(NEW_GRIDS)
    mw.build_signals = patched_build_signals
    _applied = True
    return NEW_GRIDS


def _smoke():
    apply()
    n = 900
    rng = np.random.default_rng(11)
    price = 100 + np.cumsum(rng.normal(0, 1, n))
    df = pd.DataFrame({
        "open": price + rng.normal(0, 0.2, n), "high": price + np.abs(rng.normal(0, 0.6, n)),
        "low": price - np.abs(rng.normal(0, 0.6, n)), "close": price,
        "volume": np.abs(rng.normal(1000, 400, n)),
    })
    df["date"] = np.repeat(np.arange(n // 30 + 1), 30)[:n]  # ~30 bars/day
    print(f"[archetypes] +{len(NEW_GRIDS)} strategies; total param sets {sum(len(g) for g in NEW_GRIDS.values())}")
    for sid, grid in NEW_GRIDS.items():
        sig, stop = mw.build_signals(sid, df.copy(), grid[len(grid) // 2])
        assert len(sig) == n and len(stop) == n
        print(f"[archetypes] {sid}: grid={len(grid)} signals={int(sig.sum())} stop_nonnull={int(stop.notna().sum())}")
    print("[archetypes] SMOKE OK (builds signals; NOT validated, NOT promotable)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    if args.smoke:
        _smoke()
    else:
        apply()
        print(f"[archetypes] applied: {list(NEW_GRIDS)}")
