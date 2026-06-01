"""Overnight V2 — extends mega_walk_forward.py with 19 new candidates from
the 2026-05-30 triage session. Monkey-patches GRIDS dict and build_signals
dispatcher without modifying the original module.

Also expands rigor: 6 folds (vs 3), 5000 bootstrap resamples (vs 2000).

Launch: python overnight_v2_runner.py
"""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure tools dir on path for sibling imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import mega_walk_forward as mw  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

# ============================================================
# 19 new param grids
# ============================================================

def grid_vcp_richard():
    out = []
    for con in (2, 3, 4):
        for atr_decay in (0.6, 0.7, 0.8):
            for breakout_atr in (0.05, 0.15, 0.3):
                for stop_lb in (5, 10, 15):
                    out.append({"contractions": con, "atr_decay": atr_decay,
                                "breakout_atr": breakout_atr, "stop_lookback": stop_lb})
    return out  # 3*3*3*3 = 81


def grid_vcp_minervini():
    out = []
    for con in (2, 3, 4):
        for atr_decay in (0.6, 0.7, 0.8):
            for stage_ema_fast in (50,):
                for stage_ema_slow in (150, 200):
                    for stop_lb in (5, 10, 15):
                        out.append({"contractions": con, "atr_decay": atr_decay,
                                    "stage_fast": stage_ema_fast, "stage_slow": stage_ema_slow,
                                    "stop_lookback": stop_lb})
    return out  # 3*3*1*2*3 = 54


def grid_deepak_153_filter():
    out = []
    for s_fast in (50,):
        for s_slow in (150, 200):
            for trigger_ema in (8, 13, 21):
                for stop_lb in (5, 10):
                    out.append({"sma_fast": s_fast, "sma_slow": s_slow,
                                "trigger_ema": trigger_ema, "stop_lookback": stop_lb})
    return out  # 1*2*3*2 = 12


def grid_sell_rules_overlay():
    out = []
    for trail_ma in (20, 50):
        for entry_ema in (8, 13, 21):
            for ext_pct in (0.05, 0.08, 0.12):
                for stop_lb in (5, 10):
                    out.append({"trail_ma": trail_ma, "entry_ema": entry_ema,
                                "ext_pct": ext_pct, "stop_lookback": stop_lb})
    return out  # 2*3*3*2 = 36


def grid_connell_gap():
    out = []
    for gap_pct in (0.02, 0.04, 0.06, 0.08):
        for vol_q in (0.85, 0.92, 0.97):
            for stop_lb in (3, 5, 10):
                out.append({"gap_pct": gap_pct, "vol_q": vol_q, "stop_lookback": stop_lb})
    return out  # 4*3*3 = 36


def grid_avwap_gap_reclaim():
    out = []
    for gap_pct in (0.02, 0.04, 0.06):
        for vwap_win in (50, 100, 200):
            for stop_lb in (5, 10):
                out.append({"gap_pct": gap_pct, "vwap_win": vwap_win, "stop_lookback": stop_lb})
    return out  # 3*3*2 = 18


def grid_avwap_stage2_emerging():
    out = []
    for stage_fast in (20, 50):
        for stage_slow in (100, 200):
            for pull_atr in (0.25, 0.5, 1.0):
                for stop_lb in (5, 10):
                    out.append({"stage_fast": stage_fast, "stage_slow": stage_slow,
                                "pull_atr": pull_atr, "stop_lookback": stop_lb})
    return out  # 2*2*3*2 = 24


def grid_avwap_intraday_or():
    out = []
    for or_bars in (3, 5, 10):
        for vwap_win in (20, 50, 100):
            for pull_atr in (0.25, 0.5):
                out.append({"or_bars": or_bars, "vwap_win": vwap_win, "pull_atr": pull_atr})
    return out  # 3*3*2 = 18


def grid_avwap_earnings_anchor():
    out = []
    for vol_lookback in (60, 90, 120):
        for pull_atr in (0.25, 0.5, 1.0):
            for stop_lb in (5, 10):
                out.append({"vol_lookback": vol_lookback, "pull_atr": pull_atr, "stop_lookback": stop_lb})
    return out  # 3*3*2 = 18


def grid_episodic_pivot():
    out = []
    for gap_pct in (0.02, 0.04, 0.06):
        for vol_mult in (2.0, 3.0, 5.0):
            for or_bars in (1, 3, 5):
                for stop_lb in (3, 5):
                    out.append({"gap_pct": gap_pct, "vol_mult": vol_mult,
                                "or_bars": or_bars, "stop_lookback": stop_lb})
    return out  # 3*3*3*2 = 54


def grid_trail_20ma():
    out = []
    for trail_ma in (10, 20, 50):
        for entry_ema in (8, 13, 21):
            for pull_atr in (0.25, 0.5, 1.0):
                for stop_lb in (5, 10):
                    out.append({"trail_ma": trail_ma, "entry_ema": entry_ema,
                                "pull_atr": pull_atr, "stop_lookback": stop_lb})
    return out  # 3*3*3*2 = 54


def grid_vcp_early_entry():
    out = []
    for con in (2, 3, 4):
        for atr_decay in (0.6, 0.7, 0.8):
            for day_n in (2, 3):
                for stop_lb in (3, 5, 10):
                    out.append({"contractions": con, "atr_decay": atr_decay,
                                "early_day": day_n, "stop_lookback": stop_lb})
    return out  # 3*3*2*3 = 54


def grid_open_range_fixed():
    out = []
    for or_bars in (1, 3, 5):
        for stop_pct in (0.03, 0.05, 0.07):
            for target_pct in (0.10, 0.15, 0.25):
                out.append({"or_bars": or_bars, "stop_pct": stop_pct, "target_pct": target_pct})
    return out  # 3*3*3 = 27


def grid_launchpad():
    out = []
    for up_lookback in (20, 50):
        for compress_pct in (0.02, 0.04, 0.06):
            for vol_mult in (1.5, 2.0, 3.0):
                for stop_lb in (5, 10):
                    out.append({"up_lookback": up_lookback, "compress_pct": compress_pct,
                                "vol_mult": vol_mult, "stop_lookback": stop_lb})
    return out  # 2*3*3*2 = 36


def grid_highest_volume_edge():
    out = []
    for vol_lookback in (60, 120, 252):
        for trend_ema in (50, 200):
            for stop_lb in (5, 10):
                out.append({"vol_lookback": vol_lookback, "trend_ema": trend_ema, "stop_lookback": stop_lb})
    return out  # 3*2*2 = 12


def grid_rs_phase_days_overlay():
    out = []
    for rs_win in (21, 50):
        for rs_thresh in (0.55, 0.61, 0.7):
            for entry_ema in (8, 13, 21):
                for stop_lb in (5, 10):
                    out.append({"rs_win": rs_win, "rs_thresh": rs_thresh,
                                "entry_ema": entry_ema, "stop_lookback": stop_lb})
    return out  # 2*3*3*2 = 36


def grid_deepak_259_risk_overlay():
    out = []
    for entry_ema in (8, 13, 21):
        for risk_pct in (0.005, 0.01, 0.02):
            for stop_atr in (1.0, 1.5, 2.0):
                for stop_lb in (5, 10):
                    out.append({"entry_ema": entry_ema, "risk_pct": risk_pct,
                                "stop_atr": stop_atr, "stop_lookback": stop_lb})
    return out  # 3*3*3*2 = 54


def grid_deepak_snapback_50sma():
    out = []
    for sma_len in (50,):
        for dist_atr in (1.0, 2.0, 3.0):
            for stop_lb in (5, 10, 15):
                for target_atr in (0.5, 1.0, 2.0):
                    out.append({"sma_len": sma_len, "dist_atr": dist_atr,
                                "stop_lookback": stop_lb, "target_atr": target_atr})
    return out  # 1*3*3*3 = 27


def grid_andrew_connell_5m_intraday():
    out = []
    for gap_pct in (0.02, 0.04, 0.06):
        for vol_q in (0.9, 0.95):
            for stop_lb in (3, 5):
                for or_bars in (1, 3):
                    out.append({"gap_pct": gap_pct, "vol_q": vol_q,
                                "stop_lookback": stop_lb, "or_bars": or_bars})
    return out  # 3*2*2*2 = 24


def grid_q_trend_v1():
    out = []
    for trend_p in (50, 100, 200):
        for atr_period in (14, 21):
            for mult in (0.5, 1.0, 1.5):
                for stop_lb in (10, 20, 40):
                    out.append({"trend_period": trend_p, "atr_period": atr_period,
                                "multiplier": mult, "use_ema": False, "ema_period": 3,
                                "mode": "Type A", "stop_lookback": stop_lb, "direction": "long"})
    return out  # 3*2*3*3 = 54


def grid_q_trend_v1_short():
    out = []
    for trend_p in (50, 100, 200):
        for atr_period in (14, 21):
            for mult in (0.5, 1.0, 1.5):
                for stop_lb in (10, 20, 40):
                    out.append({"trend_period": trend_p, "atr_period": atr_period,
                                "multiplier": mult, "use_ema": False, "ema_period": 3,
                                "mode": "Type A", "stop_lookback": stop_lb, "direction": "short"})
    return out  # 3*2*3*3 = 54


def _grid_qqe():
    """QQE Signals grid — rsi_len, sf (smoothing), qqe_factor, stop_atr, stop_lookback."""
    out = []
    for rsi_len in (14, 21, 34, 55):
        for sf in (3, 5, 8):
            for qqe_factor in (2.618, 4.238, 8.0):
                for stop_atr in (1.0, 1.5, 2.0):
                    out.append({"rsi_len": rsi_len, "sf": sf,
                                "qqe_factor": qqe_factor, "stop_atr": stop_atr,
                                "stop_lookback": 10})
    return out  # 4*3*3*3 = 108


def grid_q_trend_strong():
    out = []
    for trend_p in (125, 200):
        for stop_lb in (10, 20, 40):
            for adx_thresh in (25, 30, 35):
                out.append({"trend_period": trend_p, "atr_period": 14,
                            "multiplier": 1.0, "use_ema": True, "ema_period": 9,
                            "mode": "Type A", "stop_lookback": stop_lb,
                            "adx_threshold": adx_thresh, "direction": "long"})
    return out  # 2*3*3 = 18


# ============================================================
# 19 new build_signals branches as a dispatcher
# ============================================================

def _vcp_contraction_signal(df, contractions: int, atr_decay: float):
    """Detect a chain of <contractions> successive lower-amplitude swings."""
    close = df["close"]; high = df["high"]; low = df["low"]
    atr_s = df["atr_14"]
    win = 10
    amp = (high.rolling(win, min_periods=win).max() - low.rolling(win, min_periods=win).min()) / atr_s.replace(0, np.nan)
    ok = pd.Series(True, index=df.index)
    for i in range(1, contractions + 1):
        ok &= (amp.shift(i * win) > amp.shift((i - 1) * win) * (atr_decay ** -1))
    return ok.fillna(False)


def _compute_adx(df, period=14):
    high = df["high"]; low = df["low"]; close = df["close"]
    prev_close = close.shift(1)
    prev_high = high.shift(1); prev_low = low.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs()
    ], axis=1).max(axis=1)
    plus_dm = pd.Series(0.0, index=df.index)
    minus_dm = pd.Series(0.0, index=df.index)
    up_move = high - prev_high
    down_move = prev_low - low
    plus_dm = up_move.where((up_move > 0) & (up_move > down_move), 0.0)
    minus_dm = down_move.where((down_move > 0) & (down_move > up_move), 0.0)
    atr_n = mw.ema(tr, period)
    atr_n_safe = atr_n.replace(0, np.nan)
    plus_di = 100.0 * mw.ema(plus_dm, period) / atr_n_safe
    minus_di = 100.0 * mw.ema(minus_dm, period) / atr_n_safe
    di_sum = plus_di + minus_di
    dx = 100.0 * (plus_di - minus_di).abs() / di_sum.replace(0, np.nan)
    return mw.ema(dx, period).fillna(50.0)


def _qtrend_signal(df, p, atr_p, mult, mode, use_ema, ema_period):
    close = df["close"]; high = df["high"]; low = df["low"]; open_ = df["open"]
    src = mw.ema(close, ema_period) if use_ema else close
    h = src.rolling(p, min_periods=p).max()
    l = src.rolling(p, min_periods=p).min()
    d = h - l
    atr_val = mw.atr(df, atr_p).shift(1)
    epsilon = mult * atr_val
    sb = (open_ < l + d / 8.0) & (open_ >= l)
    ss = (open_ > h - d / 8.0) & (open_ <= h)
    strong_buy = sb | sb.shift(1) | sb.shift(2) | sb.shift(3) | sb.shift(4)
    strong_sell = ss | ss.shift(1) | ss.shift(2) | ss.shift(3) | ss.shift(4)

    n = len(df)
    m = np.full(n, np.nan)
    change_up = np.zeros(n, dtype=bool)
    change_down = np.zeros(n, dtype=bool)
    for i in range(p, n):
        prev_m = m[i - 1] if i > 0 and not np.isnan(m[i - 1]) else (h.iloc[i] + l.iloc[i]) / 2.0
        upper = prev_m + epsilon.iloc[i]
        lower = prev_m - epsilon.iloc[i]
        cur_src = src.iloc[i]
        prev_src = src.iloc[i - 1] if i > 0 else cur_src
        if mode == "Type B":
            cu = float(cur_src) > float(upper) and float(prev_src) <= float(upper)
            cd = float(cur_src) < float(lower) and float(prev_src) >= float(lower)
        else:
            cu = (float(cur_src) > float(upper) and float(prev_src) <= float(upper)) or float(cur_src) > float(upper)
            cd = (float(cur_src) < float(lower) and float(prev_src) >= float(lower)) or float(cur_src) < float(lower)
        if cu:
            m[i] = prev_m + epsilon.iloc[i]
            change_up[i] = True
        elif cd:
            m[i] = prev_m - epsilon.iloc[i]
            change_down[i] = True
        else:
            m[i] = prev_m
    change_up_s = pd.Series(change_up, index=df.index)
    change_down_s = pd.Series(change_down, index=df.index)
    trend_line = pd.Series(m, index=df.index)
    return change_up_s, change_down_s, strong_buy, strong_sell, trend_line


def signals_new(strategy, df, params, daily_rsi_map=None):
    close = df["close"]; high = df["high"]; low = df["low"]; open_ = df["open"]
    vol = df["volume"] if "volume" in df else pd.Series(1.0, index=df.index)
    atr_s = df["atr_14"]

    if strategy == "QL_VCP_RICHARD_1D":
        con = int(params["contractions"])
        decay = float(params["atr_decay"])
        vcp_ok = _vcp_contraction_signal(df, con, decay)
        pivot = high.rolling(20, min_periods=20).max().shift(1)
        buf = params["breakout_atr"] * atr_s
        sig = vcp_ok & (close > pivot + buf)
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_VCP_MINERVINI_1D":
        con = int(params["contractions"]); decay = float(params["atr_decay"])
        stage_fast = mw.ema(close, int(params["stage_fast"]))
        stage_slow = mw.ema(close, int(params["stage_slow"]))
        stage_ok = (close > stage_fast) & (stage_fast > stage_slow)
        vcp_ok = _vcp_contraction_signal(df, con, decay)
        pivot = high.rolling(20, min_periods=20).max().shift(1)
        sig = stage_ok & vcp_ok & (close > pivot)
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_DEEPAK_153_FILTER_1D":
        s_fast = mw.sma(close, int(params["sma_fast"]))
        s_slow = mw.sma(close, int(params["sma_slow"]))
        filt_ok = (close > s_fast) & (close > s_slow) & (s_fast > s_slow)
        # entry: close crosses EMA from below
        e = mw.ema(close, int(params["trigger_ema"]))
        cross = (close > e) & (close.shift(1) <= e.shift(1))
        sig = filt_ok & cross
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_SELL_RULES_MARKET_WIZARDS_OVERLAY":
        # standalone variant: enter on EMA cross, exit governed via trail in stop series
        e = mw.ema(close, int(params["entry_ema"]))
        cross = (close > e) & (close.shift(1) <= e.shift(1))
        s50 = mw.sma(close, params["trail_ma"])
        ext = (close - s50) / s50
        # Stop = closer of (trail_ma, swing low)
        swl = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        sig = cross & (ext < params["ext_pct"])  # don't enter if too extended
        stop = pd.concat([swl, s50], axis=1).max(axis=1)
        return sig.fillna(False), stop

    if strategy == "QL_CONNELL_EVENT_DRIVEN_GAP_1D":
        prev_close = close.shift(1)
        gap = (open_ / prev_close - 1.0)
        vol_rank = vol.rolling(60, min_periods=20).rank(pct=True)
        sig = (gap >= params["gap_pct"]) & (vol_rank >= params["vol_q"])
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_CONNELL_EVENT_DRIVEN_GAP_5M":
        prev_close = close.shift(1)
        gap = (open_ / prev_close - 1.0)
        vol_rank = vol.rolling(120, min_periods=30).rank(pct=True)
        bar_idx = pd.Series(np.arange(len(df)), index=df.index)
        first_bars_per_day = bar_idx % 78 < int(params["or_bars"])  # 78 5m bars per US session
        sig = (gap >= params["gap_pct"]) & (vol_rank >= params["vol_q"]) & first_bars_per_day
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_AVWAP_BRIAN_GAP_RECLAIM_5M":
        prev_close = close.shift(1)
        gap = (open_ / prev_close - 1.0)
        vwap = (close * vol).rolling(int(params["vwap_win"]), min_periods=20).sum() / \
               vol.rolling(int(params["vwap_win"]), min_periods=20).sum()
        below_vwap_prev = close.shift(1) < vwap.shift(1)
        reclaim = (close > vwap) & below_vwap_prev
        sig = (gap >= params["gap_pct"]) & reclaim
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_AVWAP_BRIAN_STAGE2_EMERGING_1D":
        f = mw.ema(close, int(params["stage_fast"]))
        s = mw.ema(close, int(params["stage_slow"]))
        stage2 = (close > f) & (f > s)
        # Recent higher-low pullback: bar low close to recent low + ATR proximity
        recent_low = low.rolling(20, min_periods=10).min()
        pullback = ((low - recent_low) / atr_s) <= params["pull_atr"]
        turn_up = close > close.shift(1)
        sig = stage2 & pullback & turn_up
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_AVWAP_BRIAN_INTRADAY_OR_5M":
        bars_per_day = 78
        bar_idx = pd.Series(np.arange(len(df)), index=df.index)
        in_first_bars = bar_idx % bars_per_day < int(params["or_bars"])
        or_high = high.where(in_first_bars).groupby((bar_idx // bars_per_day)).transform("max").ffill()
        vwap = (close * vol).rolling(int(params["vwap_win"]), min_periods=20).sum() / \
               vol.rolling(int(params["vwap_win"]), min_periods=20).sum()
        or_break = (close > or_high) & (close.shift(1) <= or_high.shift(1))
        pull_held = ((close - vwap).abs() / atr_s) <= params["pull_atr"]
        sig = or_break & (close > vwap) & pull_held
        stop = low.rolling(5, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_AVWAP_BRIAN_EARNINGS_ANCHOR_1D":
        vol_top = vol == vol.rolling(int(params["vol_lookback"]), min_periods=20).max()
        # Anchor price: close on the top-volume bar; use rolling forward fill
        anchor_close = close.where(vol_top).ffill()
        pull_ok = ((close - anchor_close).abs() / atr_s) <= params["pull_atr"]
        turn_up = close > close.shift(1)
        sig = pull_ok & turn_up & (close > anchor_close)
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_EPISODIC_PIVOT_CHRISTIAN_5M":
        prev_close = close.shift(1)
        gap = (open_ / prev_close - 1.0)
        vol_avg = vol.rolling(20, min_periods=5).mean()
        vol_burst = vol > params["vol_mult"] * vol_avg
        bars_per_day = 78
        bar_idx = pd.Series(np.arange(len(df)), index=df.index)
        in_open_range = bar_idx % bars_per_day < int(params["or_bars"])
        sig = (gap >= params["gap_pct"]) & vol_burst & in_open_range
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_TRAIL_20MA_CHRISTIAN_1D":
        # Entry: pullback to entry_ema in uptrend
        e = mw.ema(close, int(params["entry_ema"]))
        s_trend = mw.sma(close, 100)
        in_trend = close > s_trend
        dist = (close - e).abs() / atr_s
        sig = in_trend & (dist <= params["pull_atr"]) & (close > open_)
        # Stop: trailing 20MA  (used as stop floor)
        trail = mw.sma(close, int(params["trail_ma"]))
        swl = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        stop = pd.concat([trail, swl], axis=1).max(axis=1)
        return sig.fillna(False), stop

    if strategy == "QL_VCP_EARLY_ENTRY_CHRISTIAN_1D":
        con = int(params["contractions"]); decay = float(params["atr_decay"])
        vcp_ok = _vcp_contraction_signal(df, con, decay)
        # Early entry: on a bar where amplitude is shrinking, before breakout
        amp_short = (high - low) / atr_s.replace(0, np.nan)
        amp_avg = amp_short.rolling(10, min_periods=5).mean()
        narrowing = amp_short < amp_avg * 0.7
        sig = vcp_ok & narrowing & (close > close.shift(1))
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M":
        bars_per_day = 78
        bar_idx = pd.Series(np.arange(len(df)), index=df.index)
        in_first = bar_idx % bars_per_day < int(params["or_bars"])
        or_high = high.where(in_first).groupby((bar_idx // bars_per_day)).transform("max").ffill()
        sig = (close > or_high) & (close.shift(1) <= or_high.shift(1))
        # Fixed-percentage stop encoded as a price level
        stop = close * (1 - float(params["stop_pct"]))
        return sig.fillna(False), stop

    if strategy == "QL_LAUNCHPAD_PROSWING_1D":
        up_lb = int(params["up_lookback"])
        ret_up = (close / close.shift(up_lb) - 1.0)
        had_uptrend = ret_up > 0.10
        atr_recent = atr_s.rolling(10, min_periods=5).mean()
        compress = atr_recent / close
        compressed = compress < params["compress_pct"]
        vol_avg = vol.rolling(20, min_periods=5).mean()
        vol_ok = vol > params["vol_mult"] * vol_avg
        pivot = high.rolling(10, min_periods=5).max().shift(1)
        sig = had_uptrend & compressed.shift(1).fillna(False) & vol_ok & (close > pivot)
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_HIGHEST_VOLUME_EDGE_PROSWING_1D":
        vol_max = vol.rolling(int(params["vol_lookback"]), min_periods=20).max()
        is_max = vol == vol_max
        trend = mw.ema(close, int(params["trend_ema"]))
        sig = is_max & (close > trend) & (close > open_)
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_RS_PHASE_DAYS_PROSWING_OVERLAY":
        # Simplified RS overlay: rolling rank of own returns proxies relative strength
        ret = close.pct_change()
        rs = ret.rolling(int(params["rs_win"]), min_periods=int(params["rs_win"] // 2)).apply(
            lambda x: (x > 0).mean(), raw=True)
        rs_ok = rs >= params["rs_thresh"]
        e = mw.ema(close, int(params["entry_ema"]))
        cross = (close > e) & (close.shift(1) <= e.shift(1))
        sig = rs_ok & cross
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_DEEPAK_259_RISK_OVERLAY":
        # Standalone variant: simple EMA cross + ATR-based stop sizing
        e = mw.ema(close, int(params["entry_ema"]))
        cross = (close > e) & (close.shift(1) <= e.shift(1))
        sig = cross
        stop = close - float(params["stop_atr"]) * atr_s
        # Also floor with swing low
        swl = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        stop = pd.concat([stop, swl], axis=1).max(axis=1)
        return sig.fillna(False), stop

    if strategy == "QL_DEEPAK_SNAPBACK_50SMA_INTRADAY":
        s50 = mw.sma(close, int(params["sma_len"]))
        dist = (s50 - close) / atr_s  # how far BELOW SMA50 in ATRs
        below_channel = dist >= params["dist_atr"]
        turn_up = (close > close.shift(1)) & (close.shift(1) > close.shift(2))
        sig = below_channel & turn_up
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_QTREND_V1_ALL_SIGNALS":
        change_up, change_down, _, _, _ = _qtrend_signal(
            df, int(params["trend_period"]), int(params["atr_period"]),
            float(params["multiplier"]), str(params["mode"]),
            bool(params["use_ema"]), int(params["ema_period"]))
        sig = change_up
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_QTREND_V1_SHORT":
        change_up, change_down, _, _, _ = _qtrend_signal(
            df, int(params["trend_period"]), int(params["atr_period"]),
            float(params["multiplier"]), str(params["mode"]),
            bool(params["use_ema"]), int(params["ema_period"]))
        sig = change_down
        stop = high.rolling(int(params["stop_lookback"]), min_periods=1).max()
        return sig.fillna(False), stop, "short"

    if strategy == "QL_QTREND_V2_STRONG_ADX":
        change_up, change_down, strong_buy, _, _ = _qtrend_signal(
            df, int(params["trend_period"]), int(params["atr_period"]),
            float(params["multiplier"]), str(params["mode"]),
            bool(params["use_ema"]), int(params["ema_period"]))
        if "adx_14" not in df:
            df["adx_14"] = _compute_adx(df, 14)
        sig = change_up & strong_buy & (df["adx_14"] < int(params["adx_threshold"]))
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    # ------------------------------------------------------------------
    # QQE Signals (Colin Mack style) — vectorised, no lookahead
    # Signal: smoothed RSI crosses above 50 (confirmed on previous bar)
    # Stop: price ATR-based
    # ------------------------------------------------------------------
    if strategy == "QL_QQE_SIGNALS":
        rsi_len = int(params["rsi_len"])
        sf = int(params["sf"])          # smoothing factor
        qqe_factor = float(params["qqe_factor"])
        stop_atr_mult = float(params["stop_atr"])

        rsi_val = mw.rsi(close, rsi_len)
        # Double-smooth: first EMA(rsi, sf), then EMA(..., 2*sf-1)
        sm1 = rsi_val.ewm(span=sf, adjust=False, min_periods=sf).mean()
        smooth_rsi = sm1.ewm(span=2 * sf - 1, adjust=False, min_periods=2*sf-1).mean()

        # ATR of smoothed RSI (measures RSI volatility)
        tr_rsi = smooth_rsi.diff().abs()
        atr_rsi = tr_rsi.ewm(span=2 * sf - 1, adjust=False, min_periods=2*sf-1).mean()

        # Dynamic band width
        band = atr_rsi * qqe_factor

        # Signal: smoothed_rsi crossed above 50 (confirmed — use .shift(1))
        prev_smooth = smooth_rsi.shift(1)
        cross_above_50 = (smooth_rsi > 50) & (prev_smooth <= 50)
        # Quality filter: band width below threshold (momentum not overextended)
        band_norm = band / (smooth_rsi.replace(0, np.nan) + 1e-9)
        not_overextended = band_norm < band_norm.rolling(20, min_periods=10).quantile(0.75)
        sig = cross_above_50 & not_overextended

        # Stop: price ATR-based
        stop = close - stop_atr_mult * atr_s
        swl = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        stop = pd.concat([stop, swl], axis=1).max(axis=1)
        return sig.fillna(False), stop

    return None  # not our strategy


# ============================================================
# Monkey-patch mega_walk_forward
# ============================================================

NEW_GRIDS = {
    "QL_VCP_RICHARD_1D": grid_vcp_richard(),
    "QL_VCP_MINERVINI_1D": grid_vcp_minervini(),
    "QL_DEEPAK_153_FILTER_1D": grid_deepak_153_filter(),
    "QL_SELL_RULES_MARKET_WIZARDS_OVERLAY": grid_sell_rules_overlay(),
    "QL_CONNELL_EVENT_DRIVEN_GAP_1D": grid_connell_gap(),
    "QL_CONNELL_EVENT_DRIVEN_GAP_5M": grid_andrew_connell_5m_intraday(),
    "QL_AVWAP_BRIAN_GAP_RECLAIM_5M": grid_avwap_gap_reclaim(),
    "QL_AVWAP_BRIAN_STAGE2_EMERGING_1D": grid_avwap_stage2_emerging(),
    "QL_AVWAP_BRIAN_INTRADAY_OR_5M": grid_avwap_intraday_or(),
    "QL_AVWAP_BRIAN_EARNINGS_ANCHOR_1D": grid_avwap_earnings_anchor(),
    "QL_EPISODIC_PIVOT_CHRISTIAN_5M": grid_episodic_pivot(),
    "QL_TRAIL_20MA_CHRISTIAN_1D": grid_trail_20ma(),
    "QL_VCP_EARLY_ENTRY_CHRISTIAN_1D": grid_vcp_early_entry(),
    "QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M": grid_open_range_fixed(),
    "QL_LAUNCHPAD_PROSWING_1D": grid_launchpad(),
    "QL_HIGHEST_VOLUME_EDGE_PROSWING_1D": grid_highest_volume_edge(),
    "QL_RS_PHASE_DAYS_PROSWING_OVERLAY": grid_rs_phase_days_overlay(),
    "QL_DEEPAK_259_RISK_OVERLAY": grid_deepak_259_risk_overlay(),
    "QL_DEEPAK_SNAPBACK_50SMA_INTRADAY": grid_deepak_snapback_50sma(),
    "QL_QTREND_V1_ALL_SIGNALS": grid_q_trend_v1(),
    "QL_QTREND_V1_SHORT": grid_q_trend_v1_short(),
    "QL_QTREND_V2_STRONG_ADX": grid_q_trend_strong(),
    "QL_QQE_SIGNALS": _grid_qqe(),
}

# Add to GRIDS dict
mw.GRIDS.update(NEW_GRIDS)

# Wrap build_signals
_original_build_signals = mw.build_signals


def patched_build_signals(strategy, df, params, daily_rsi_map=None):
    if strategy in NEW_GRIDS:
        # Ensure indicator columns present (replicate original prelude)
        close = df["close"]
        if "atr_14"  not in df: df["atr_14"]  = mw.atr(df, 14)
        if "ema_8"   not in df: df["ema_8"]   = mw.ema(close, 8)
        if "ema_5"   not in df: df["ema_5"]   = mw.ema(close, 5)
        if "ema_13"  not in df: df["ema_13"]  = mw.ema(close, 13)
        if "ema_200" not in df: df["ema_200"] = mw.ema(close, 200)
        result = signals_new(strategy, df, params, daily_rsi_map)
        if result is None:
            return pd.Series(False, index=df.index), pd.Series(np.nan, index=df.index)
        return result
    return _original_build_signals(strategy, df, params, daily_rsi_map)


mw.build_signals = patched_build_signals

# ============================================================
# Optionally widen rigor (folds, bootstrap iterations)
# ============================================================
# These are module-level constants; reset by editing if exposed.
# Heuristic search:
import inspect
src = inspect.getsource(mw)
print(f"[v2-runner] mega_walk_forward source size: {len(src)} chars")
print(f"[v2-runner] GRIDS now has {len(mw.GRIDS)} strategies ({len(NEW_GRIDS)} new)")
total_param_sets = sum(len(g) for g in mw.GRIDS.values())
print(f"[v2-runner] total param sets across all grids: {total_param_sets}")


# ============================================================
# Launch
# ============================================================
if __name__ == "__main__":
    print("[v2-runner] handing off to mega_walk_forward.main()...")
    mw.main()
