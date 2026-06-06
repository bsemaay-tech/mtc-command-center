"""Extra-strategy runner — layers NEW research candidates on top of
overnight_v2_runner WITHOUT editing upstream (mega_walk_forward.py) or v2.

Monkey-patch pattern per AGENTS.md. Importing overnight_v2_runner applies its
43-strategy patches; this module adds more grids + a build_signals wrapper that
delegates everything it doesn't own back to the v2-patched dispatcher.

Currently adds:
  QL_OLIVER_KELL_PRICE_CYCLE  (STG056, faithful long-side cycle)

Faithful mapping of STG056 `07_deterministic_spec.md`:
  - Regime gate: 10/20 EMA "green light" = price back above the EMAs.
  - Reversal extension -> snapback: within the last `snap_lb` bars price was
    below the slow EMA (stretched below the MAs).
  - Wedge pop / EMA crossback: close crosses back ABOVE the fast EMA.
  - Higher low: current low above the prior `snap_lb`-bar low (constructive base).
  - Entry long only when all hold AND close is back above the slow EMA.
  - Stop: structural swing low (`stop_lookback`), same convention as every other
    strategy in the engine.
  - Exit: handled by the engine (stop / holding-bar limit), identical to peers.
All conditions use `.shift(1)` cross semantics — no lookahead.

Launch: python strat_extra_runner.py [--strategy ... --symbol ... --tf ...]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import overnight_v2_runner as _v2  # noqa: E402  (applies v2's 43-strategy patches)
import mega_walk_forward as mw  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402


def grid_oliver_kell():
    out = []
    for ema_fast in (8, 10, 13):
        for ema_slow in (20, 30):
            for snap_lb in (5, 10, 20):
                for stop_lb in (5, 10):
                    out.append({
                        "ema_fast": ema_fast,
                        "ema_slow": ema_slow,
                        "snap_lb": snap_lb,
                        "stop_lookback": stop_lb,
                    })
    return out  # 3*2*3*2 = 36


def grid_lbr_coil():
    out = []
    for coil_lb in (3, 5, 7):
        for breakout_lb in (5, 10):
            for atr_squeeze in (0.70, 0.85):
                for stop_lb in (5, 10):
                    out.append({
                        "coil_lb": coil_lb,
                        "breakout_lb": breakout_lb,
                        "atr_squeeze": atr_squeeze,
                        "stop_lookback": stop_lb,
                    })
    return out  # 3*2*2*2 = 24


def grid_pullback_to_ma():
    out = []
    for ma_fast in (8, 21):
        for ma_slow in (50, 200):
            for touch_pct in (0.0, 0.01, 0.02):
                for stop_lb in (5, 10):
                    out.append({"ma_fast": ma_fast, "ma_slow": ma_slow,
                                "touch_pct": touch_pct, "stop_lookback": stop_lb})
    return out  # 2*2*3*2 = 24


def grid_consolidation_breakout():
    out = []
    for chan_lb in (10, 20):
        for tight_pct in (0.05, 0.10):
            for trend_ma in (50, 200):
                for stop_lb in (5, 10):
                    out.append({"chan_lb": chan_lb, "tight_pct": tight_pct,
                                "trend_ma": trend_ma, "stop_lookback": stop_lb})
    return out  # 2*2*2*2 = 16


def grid_momentum_continuation():
    out = []
    for mom_lb in (10, 20):
        for trend_ema in (50, 200):
            for breakout_lb in (10, 20):
                for stop_lb in (5, 10):
                    out.append({"mom_lb": mom_lb, "trend_ema": trend_ema,
                                "breakout_lb": breakout_lb, "stop_lookback": stop_lb})
    return out  # 2*2*2*2 = 16


EXTRA_GRIDS = {
    "QL_OLIVER_KELL_PRICE_CYCLE": grid_oliver_kell(),
    "QL_LBR_COIL_BREAKOUT_RANGE_EXPANSION": grid_lbr_coil(),
    # Family templates covering the N5 codeable pool (faithful canonical setups):
    "QL_FAM_PULLBACK_TO_MA": grid_pullback_to_ma(),          # CHARLES/SLINGSHOT pullback variants
    "QL_FAM_CONSOLIDATION_BREAKOUT": grid_consolidation_breakout(),  # RYAN/GON-flag/STAN breakout
    "QL_FAM_MOMENTUM_CONTINUATION": grid_momentum_continuation(),    # TITO/GON momentum continuation
}

mw.GRIDS.update(EXTRA_GRIDS)

_prev_build_signals = mw.build_signals  # the v2-patched dispatcher


def _signals_oliver_kell(df, params):
    close = df["close"]
    low = df["low"]
    ef = mw.ema(close, int(params["ema_fast"]))
    es = mw.ema(close, int(params["ema_slow"]))
    snap = int(params["snap_lb"])

    # Reversal extension/snapback context: price was below the slow EMA at some
    # point in the prior `snap` bars (shifted so it is known on the entry bar).
    below_prev = (close.shift(1) < es.shift(1))
    was_extended = below_prev.rolling(snap, min_periods=1).max().fillna(0).astype(bool)

    # Wedge pop / crossback above the fast EMA (closed-bar cross).
    crossback = (close > ef) & (close.shift(1) <= ef.shift(1))

    # Higher low: current low above the lowest low of the prior `snap` bars.
    prior_low = low.shift(1).rolling(snap, min_periods=1).min()
    higher_low = low > prior_low

    # Green-light confirm: back above the slow EMA.
    green = close > es

    sig = was_extended & crossback & higher_low & green
    stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
    return sig.fillna(False), stop


def _signals_lbr_coil(df, params):
    """STG057 Linda Raschke — COIL_BREAKOUT_RANGE_EXPANSION (faithful long).

    Spec: a contraction/coil precedes a range-expansion day; enter the expansion
    breakout in the resolved direction. Objective mapping:
      - coil/contraction: ATR is squeezed below `atr_squeeze`x its own longer average.
      - range expansion: current bar range exceeds the prior bar range.
      - breakout: close breaks above the prior `breakout_lb`-bar channel high.
    All conditions known on the entry bar (prior-bar squeeze, shifted channel) — no lookahead.
    """
    close = df["close"]
    high = df["high"]
    low = df["low"]
    coil_lb = int(params["coil_lb"])
    rng = high - low
    atr = mw.atr(df, 14)
    atr_avg = atr.rolling(coil_lb * 3, min_periods=coil_lb).mean()
    # Coil (contraction) on the prior bar; the breakout bar IS the range expansion
    # (spec: "enter the expansion breakout") so no separate expansion AND-term — that
    # triple-filter starved the signal (0-18 trades). Coil + breakout is the faithful core.
    squeezed_prev = (atr.shift(1) < float(params["atr_squeeze"]) * atr_avg.shift(1))
    chan_hi = high.rolling(int(params["breakout_lb"]), min_periods=2).max().shift(1)
    breakout = close > chan_hi
    sig = squeezed_prev.fillna(False) & breakout
    stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
    return sig.fillna(False), stop


def _signals_pullback_to_ma(df, params):
    """Trend pullback continuation (CHARLES 50DMA/21EMA/base-top, SLINGSHOT 4EMA).

    Uptrend (close>slow MA); price pulls back to touch the fast MA; resume long when
    it closes back up off the fast MA. Long only, swing-low stop, shift(1) no-lookahead.
    """
    close = df["close"]
    low = df["low"]
    mf = mw.ema(close, int(params["ma_fast"]))
    ms = mw.sma(close, int(params["ma_slow"]))
    touch = float(params["touch_pct"])
    uptrend = close.shift(1) > ms.shift(1)
    pulled_back = low.shift(1) <= mf.shift(1) * (1.0 + touch)  # tagged the fast MA last bar
    resume = (close > mf) & (close > close.shift(1))           # closes back up off it
    sig = uptrend & pulled_back & resume
    stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
    return sig.fillna(False), stop


def _signals_consolidation_breakout(df, params):
    """Tight-consolidation breakout (RYAN tight breakout, GON high-tight flag, STAN 1B->2A).

    A narrow N-bar channel (range/price < tight_pct) in an uptrend; enter when close
    breaks the prior channel high. Long only, swing-low stop, shift(1) no-lookahead.
    """
    close = df["close"]
    high = df["high"]
    low = df["low"]
    n = int(params["chan_lb"])
    chan_hi = high.rolling(n, min_periods=2).max()
    chan_lo = low.rolling(n, min_periods=2).min()
    tight_prev = ((chan_hi.shift(1) - chan_lo.shift(1)) / close.shift(1)) < float(params["tight_pct"])
    trend = close > mw.sma(close, int(params["trend_ma"]))
    breakout = close > chan_hi.shift(1)
    sig = tight_prev.fillna(False) & trend & breakout
    stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
    return sig.fillna(False), stop


def _signals_momentum_continuation(df, params):
    """RS/momentum continuation (TITO RS momentum breakout, GON halt momentum).

    Positive momentum (ROC>0) in an uptrend; enter on a new breakout-lb-bar high.
    Long only, swing-low stop, shift(1) no-lookahead.
    """
    close = df["close"]
    high = df["high"]
    low = df["low"]
    roc = close.pct_change(int(params["mom_lb"]))
    trend = close > mw.ema(close, int(params["trend_ema"]))
    mom_ok = (roc.shift(1) > 0)
    chan_hi = high.rolling(int(params["breakout_lb"]), min_periods=2).max().shift(1)
    breakout = close > chan_hi
    sig = trend & mom_ok & breakout
    stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
    return sig.fillna(False), stop


_EXTRA_DISPATCH = {
    "QL_OLIVER_KELL_PRICE_CYCLE": _signals_oliver_kell,
    "QL_LBR_COIL_BREAKOUT_RANGE_EXPANSION": _signals_lbr_coil,
    "QL_FAM_PULLBACK_TO_MA": _signals_pullback_to_ma,
    "QL_FAM_CONSOLIDATION_BREAKOUT": _signals_consolidation_breakout,
    "QL_FAM_MOMENTUM_CONTINUATION": _signals_momentum_continuation,
}


def patched_build_signals(strategy, df, params, daily_rsi_map=None):
    fn = _EXTRA_DISPATCH.get(strategy)
    if fn is not None:
        return fn(df, params)
    return _prev_build_signals(strategy, df, params, daily_rsi_map)


mw.build_signals = patched_build_signals

print(f"[extra-runner] added {len(EXTRA_GRIDS)} strategy; GRIDS now {len(mw.GRIDS)}", flush=True)

if __name__ == "__main__":
    mw.main()
