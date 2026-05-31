"""
Mega Rolling Walk-Forward + Deflated Sharpe — Overnight Edition
================================================================
- 11 prototyped strategies (existing) + 7 generic well-known patterns
- Expanded parameter grids (per-strategy 30-150 sets)
- 17 symbols x 5 timeframes (15m, 1h, 2h, 4h, 1D)
- 3 rolling walk-forward folds + locked terminal OOS
- Per-config metrics: trades, win_rate, compound return, max_dd, sharpe,
  expectancy_R, profit_factor
- Post-process: Bailey & Lopez de Prado Deflated Sharpe Ratio (DSR) p-value
  per strategy family (controls for multiple-testing)
- Output JSON + comprehensive Markdown report
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from multiprocessing import Pool, cpu_count
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as sps

# ------------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------------
BUNDLE_MANIFEST = Path(
    r"C:\LAB\_MTC_V2_REPO_CLEANUP_ARCHIVE_20260529"
    r"\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\manifests\dataset_manifest.json"
)
OUTPUT_DIR = Path(
    r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2"
    r"\06_QUANTLENS_LAB\05_BACKTEST_RESULTS"
)
COST_BPS = 8.0

LOCKBOX_FRACTION = 0.25
FOLD_TRAIN_FRACTION = 0.60
FOLD_TEST_FRACTION = 0.20
NUM_ROLLING_FOLDS = 3

MIN_BARS_REQUIRED = 1500
MIN_TRADES_FOR_PASS = 30
HOLDING_BAR_LIMIT = 96

SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT",
    "ADAUSDT", "AVAXUSDT", "DOGEUSDT", "LINKUSDT", "DOTUSDT",
    "LTCUSDT", "TRXUSDT", "NEARUSDT", "APTUSDT", "ARBUSDT",
    "OPUSDT", "POLUSDT",
]
TIMEFRAMES = ["15m", "1h", "2h", "4h", "1D"]

# ------------------------------------------------------------------
# INDICATORS
# ------------------------------------------------------------------
def ema(s, n): return s.ewm(span=n, adjust=False, min_periods=n).mean()
def sma(s, n): return s.rolling(n, min_periods=n).mean()

def rsi(s, n):
    d = s.diff()
    g = d.clip(lower=0).ewm(alpha=1/n, adjust=False, min_periods=n).mean()
    l = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False, min_periods=n).mean()
    rs = g / l.replace(0, np.nan)
    return 100 - (100 / (1 + rs))

def atr(df, n):
    pc = df["close"].shift(1)
    tr = pd.concat([df["high"]-df["low"], (df["high"]-pc).abs(), (df["low"]-pc).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1/n, adjust=False, min_periods=n).mean()

# ------------------------------------------------------------------
# GRID BUILDERS — expanded
# ------------------------------------------------------------------
def grid_dual_rsi():
    out = []
    for rsi_len in (7, 10, 14, 21):
        for daily_hi, daily_lo in [(60,40),(55,45),(65,35),(50,50)]:
            for stop_lb in (5, 7, 10, 14):
                out.append({"rsi_len": rsi_len, "daily_hi": daily_hi,
                            "daily_lo": daily_lo, "stop_lookback": stop_lb})
    return out  # 4*4*4 = 64

def grid_rsi_confluence():
    out = []
    for rsi_len in (5, 7, 9, 14, 21):
        for sma_len in (20, 50, 100, 150, 200):
            for cross_lvl in (45, 50, 55):
                out.append({"rsi_len": rsi_len, "sma_len": sma_len, "cross_lvl": cross_lvl})
    return out  # 5*5*3 = 75

def grid_ema8_family():
    out = []
    for pa in (0.20, 0.30, 0.40, 0.50, 0.65):
        for ia in (0.5, 0.8, 1.0, 1.3, 1.6):
            for sw in (3, 5, 7):
                out.append({"pullback_atr": pa, "impulse_atr": ia, "slope_window": sw})
    return out  # 5*5*3 = 75

def grid_multi_ema_channel():
    out = []
    for touch in (0.15, 0.25, 0.40, 0.55, 0.75, 1.0):
        for short_ema in (3, 5, 8):
            for long_ema in (13, 21, 34):
                if short_ema < long_ema:
                    out.append({"touch_atr": touch, "short_ema": short_ema, "long_ema": long_ema})
    return out  # ~54

def grid_vwap_pullback():
    out = []
    for w in (24, 48, 96, 144, 200):
        for prox in (0.15, 0.25, 0.40, 0.55, 0.75):
            for slope_w in (3, 5, 8):
                out.append({"session_window": w, "prox_atr": prox, "slope_window": slope_w})
    return out  # 5*5*3 = 75

def grid_two_candle_sr():
    out = []
    for lb in (24, 48, 96, 144, 200):
        for upper_third in (0.55, 0.6, 0.66, 0.75, 0.85):
            for break_buf_atr in (0.0, 0.10, 0.25):
                out.append({"level_lookback": lb, "upper_third": upper_third, "break_buf_atr": break_buf_atr})
    return out  # 5*5*3 = 75

def grid_bb_squeeze():
    out = []
    for wq in (0.05, 0.10, 0.15, 0.25, 0.35):
        for ba in (0.10, 0.20, 0.30, 0.45):
            for bb_len in (20, 30, 50):
                out.append({"width_quantile": wq, "body_atr": ba, "bb_len": bb_len})
    return out  # 5*4*3 = 60

def grid_candlestick_engulf():
    out = []
    for lb in (24, 48, 96, 144, 200):
        for tol in (0.15, 0.30, 0.50, 0.75):
            for atr_stop_mult in (0.05, 0.1, 0.25):
                out.append({"level_lookback": lb, "tolerance_atr": tol, "atr_stop_mult": atr_stop_mult})
    return out  # 5*4*3 = 60

# New generic patterns
def grid_donchian_breakout():
    out = []
    for lb in (10, 20, 40, 80, 150):
        for atr_buf in (0.0, 0.10, 0.25, 0.50):
            for stop_lb in (5, 10, 20):
                out.append({"channel_len": lb, "atr_buf": atr_buf, "stop_lookback": stop_lb})
    return out  # 5*4*3 = 60

def grid_golden_cross_pullback():
    out = []
    for fast in (20, 50):
        for slow in (100, 150, 200):
            if fast < slow:
                for pull_atr in (0.10, 0.25, 0.40, 0.6):
                    for stop_lb in (5, 10, 20):
                        out.append({"fast_ema": fast, "slow_ema": slow,
                                    "pull_atr": pull_atr, "stop_lookback": stop_lb})
    return out  # ~72

def grid_rsi_oversold_reverse():
    out = []
    for rl in (5, 7, 14, 21):
        for ob in (25, 30, 35):
            for rec in (35, 40, 45, 50):
                if rec > ob:
                    out.append({"rsi_len": rl, "oversold": ob, "recovery": rec})
    return out  # ~36-48

def grid_macd_cross():
    out = []
    for fast in (8, 12, 17):
        for slow in (21, 26, 34):
            if fast < slow:
                for signal in (5, 9, 13):
                    out.append({"fast": fast, "slow": slow, "signal": signal})
    return out  # ~27

def grid_zscore_meanrev():
    out = []
    for win in (20, 50, 100, 200):
        for z_lo in (-3.0, -2.5, -2.0, -1.5):
            for trend_ema in (50, 100, 200):
                out.append({"win": win, "z_lo": z_lo, "trend_ema": trend_ema})
    return out  # 4*4*3 = 48

def grid_atr_pullback_trend():
    out = []
    for ema_len in (20, 50, 100):
        for dist_atr in (0.25, 0.50, 0.75, 1.0):
            for slope_atr in (0.10, 0.25, 0.50):
                for stop_lb in (5, 10):
                    out.append({"ema_len": ema_len, "dist_atr": dist_atr,
                                "slope_atr": slope_atr, "stop_lookback": stop_lb})
    return out  # 3*4*3*2 = 72

def grid_keltner_breakout():
    out = []
    for ema_len in (20, 50):
        for atr_len in (10, 20):
            for mult in (1.5, 2.0, 2.5, 3.0):
                out.append({"ema_len": ema_len, "atr_len": atr_len, "mult": mult})
    return out  # 2*2*4 = 16

def grid_triple_ema_stack():
    out = []
    for touch_atr in (0.15, 0.30, 0.50, 0.75):
        for stop_lb in (5, 10):
            out.append({"touch_atr": touch_atr, "stop_lookback": stop_lb})
    return out  # 8

def grid_stoch_oversold():
    out = []
    for n in (14, 21):
        for oversold in (20, 25, 30):
            for recover in (3, 5):  # bars structure via smooth
                out.append({"stoch_n": n, "oversold": oversold, "smooth_d": recover})
    return out  # 2*3*2 = 12

# Master GRID dict
GRIDS: dict[str, list[dict]] = {
    "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK": grid_dual_rsi(),
    "QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PLAYBOOK": grid_rsi_confluence(),
    "QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK": grid_ema8_family(),
    "QL_2026-05-01_US_EQUITIES_INTRADAY_LE_MODEL_BULL_FLAG": grid_ema8_family(),
    "QL_2026-05-01_US_EQUITIES_INTRADAY_PURPLE_PROFITS": grid_ema8_family(),
    "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL": grid_ema8_family(),
    "QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNEL_PULLBACK": grid_multi_ema_channel(),
    "QL_2026-05-01_LIQUID_INTRADAY_VWAP_PULLBACK_REVERSAL": grid_vwap_pullback(),
    "QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR": grid_two_candle_sr(),
    "QL_2026-05-01_ANY_BOLLINGER_BANDS_20_2_TRI_SETUP": grid_bb_squeeze(),
    "QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE": grid_candlestick_engulf(),
    # New generic patterns
    "GEN_DONCHIAN_BREAKOUT": grid_donchian_breakout(),
    "GEN_GOLDEN_CROSS_PULLBACK": grid_golden_cross_pullback(),
    "GEN_RSI_OVERSOLD_REVERSAL": grid_rsi_oversold_reverse(),
    "GEN_MACD_BULL_CROSS": grid_macd_cross(),
    "GEN_ZSCORE_MEAN_REVERSION": grid_zscore_meanrev(),
    "GEN_ATR_PULLBACK_TREND": grid_atr_pullback_trend(),
    "GEN_KELTNER_BREAKOUT": grid_keltner_breakout(),
    "GEN_TRIPLE_EMA_STACK": grid_triple_ema_stack(),
    "GEN_STOCH_OVERSOLD_CROSS": grid_stoch_oversold(),
}

# ------------------------------------------------------------------
# SIGNALS
# ------------------------------------------------------------------
def build_signals(strategy, df, params, daily_rsi_map=None):
    close = df["close"]; high = df["high"]; low = df["low"]; open_ = df["open"]
    if "atr_14"  not in df: df["atr_14"]  = atr(df, 14)
    if "ema_8"   not in df: df["ema_8"]   = ema(close, 8)
    if "ema_5"   not in df: df["ema_5"]   = ema(close, 5)
    if "ema_13"  not in df: df["ema_13"]  = ema(close, 13)
    if "ema_200" not in df: df["ema_200"] = ema(close, 200)

    if strategy == "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK":
        if daily_rsi_map is None:
            return pd.Series(False, index=df.index), pd.Series(np.nan, index=df.index)
        df["daily_rsi"] = df["date"].map(daily_rsi_map)
        df["rsi_l"] = rsi(close, int(params["rsi_len"]))
        sig = (df["daily_rsi"] > params["daily_hi"]) & \
              (df["rsi_l"].shift(1) < params["daily_lo"]) & \
              (df["rsi_l"] >= params["daily_lo"])
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PLAYBOOK":
        rlen = int(params["rsi_len"]); slen = int(params["sma_len"]); cl = params.get("cross_lvl", 50)
        s = sma(close, slen); r = rsi(close, rlen)
        sig = (close > s) & (r.shift(1) < cl) & (r >= cl)
        stop = low.rolling(5, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy in {
        "QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK",
        "QL_2026-05-01_US_EQUITIES_INTRADAY_LE_MODEL_BULL_FLAG",
        "QL_2026-05-01_US_EQUITIES_INTRADAY_PURPLE_PROFITS",
        "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL",
    }:
        sw = int(params.get("slope_window", 3))
        slope = df["ema_8"] - df["ema_8"].shift(sw)
        dist = (close - df["ema_8"]).abs() / df["atr_14"]
        impulse = (close - close.shift(sw)).abs() / df["atr_14"]
        sig = (close > df["ema_8"]) & (slope > 0) & \
              (dist <= params["pullback_atr"]) & (impulse.shift(1) >= params["impulse_atr"])
        stop = low.rolling(3, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNEL_PULLBACK":
        se = int(params.get("short_ema", 5)); le = int(params.get("long_ema", 13))
        emaS = ema(close, se); emaL = ema(close, le)
        dist = (close - emaL).abs() / df["atr_14"]
        sig = (close > df["ema_200"]) & (emaS > emaL) & \
              (dist <= params["touch_atr"]) & (close > open_)
        stop = low.rolling(5, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_2026-05-01_LIQUID_INTRADAY_VWAP_PULLBACK_REVERSAL":
        w = int(params["session_window"])
        proxy = close.rolling(w, min_periods=w).mean()
        band = close.rolling(w, min_periods=w).std()
        sw = int(params.get("slope_window", 4))
        slope = proxy - proxy.shift(sw)
        prox = (close - proxy).abs() / df["atr_14"]
        sig = (slope > 0) & (close > proxy) & (prox <= params["prox_atr"])
        stop = proxy - 1.0 * band
        return sig.fillna(False), stop

    if strategy == "QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR":
        w = int(params["level_lookback"])
        brk = high.rolling(w, min_periods=10).max().shift(1)
        rng = (high - low).replace(0, np.nan)
        pos = (close - low) / rng
        buf = params.get("break_buf_atr", 0.0) * df["atr_14"]
        sig = (pos >= params["upper_third"]) & (close > high.shift(1)) & (close > brk + buf)
        stop = low.rolling(2, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_2026-05-01_ANY_BOLLINGER_BANDS_20_2_TRI_SETUP":
        bb_len = int(params.get("bb_len", 20))
        mid = sma(close, bb_len); std = close.rolling(bb_len, min_periods=bb_len).std()
        upper = mid + 2 * std
        width = (4 * std) / mid
        limit = width.rolling(200, min_periods=200).quantile(params["width_quantile"])
        narrow = width <= limit
        body_ok = (close - open_).abs() >= params["body_atr"] * df["atr_14"]
        sig = narrow.shift(1).fillna(False).astype(bool) & (close > upper) & body_ok
        stop = low.rolling(5, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE":
        w = int(params["level_lookback"])
        sup = low.rolling(w, min_periods=20).min().shift(1)
        bl = pd.concat([open_, close], axis=1).min(axis=1)
        bh = pd.concat([open_, close], axis=1).max(axis=1)
        engulf = (close > open_) & (bl <= bl.shift(1)) & (bh >= bh.shift(1))
        near = ((low - sup).abs() / df["atr_14"]) <= params["tolerance_atr"]
        sig = engulf & near
        stop = low - params.get("atr_stop_mult", 0.1) * df["atr_14"]
        return sig.fillna(False), stop

    if strategy == "GEN_DONCHIAN_BREAKOUT":
        ch = int(params["channel_len"])
        hh = high.rolling(ch, min_periods=ch).max().shift(1)
        buf = params.get("atr_buf", 0.0) * df["atr_14"]
        sig = close > (hh + buf)
        stop = low.rolling(int(params.get("stop_lookback", 10)), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "GEN_GOLDEN_CROSS_PULLBACK":
        fast = ema(close, int(params["fast_ema"]))
        slow = ema(close, int(params["slow_ema"]))
        dist = (close - fast).abs() / df["atr_14"]
        sig = (fast > slow) & (close > fast) & (dist <= params["pull_atr"])
        stop = low.rolling(int(params.get("stop_lookback", 10)), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "GEN_RSI_OVERSOLD_REVERSAL":
        r = rsi(close, int(params["rsi_len"]))
        sig = (r.shift(1) < params["oversold"]) & (r >= params["recovery"])
        stop = low.rolling(5, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "GEN_MACD_BULL_CROSS":
        fast = ema(close, int(params["fast"]))
        slow = ema(close, int(params["slow"]))
        macd_line = fast - slow
        sig_line = ema(macd_line, int(params["signal"]))
        sig = (macd_line.shift(1) <= sig_line.shift(1)) & (macd_line > sig_line) & (close > df["ema_200"])
        stop = low.rolling(5, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "GEN_ZSCORE_MEAN_REVERSION":
        w = int(params["win"])
        m = close.rolling(w, min_periods=w).mean()
        s = close.rolling(w, min_periods=w).std().replace(0, np.nan)
        z = (close - m) / s
        trend = ema(close, int(params["trend_ema"]))
        sig = (z < params["z_lo"]) & (close > trend)  # buy dip in uptrend
        stop = low.rolling(10, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "GEN_ATR_PULLBACK_TREND":
        emaT = ema(close, int(params["ema_len"]))
        slope = (emaT - emaT.shift(5)) / df["atr_14"]
        dist = (close - emaT) / df["atr_14"]
        sig = (close > emaT) & (slope > params["slope_atr"]) & (dist.abs() <= params["dist_atr"])
        stop = low.rolling(int(params.get("stop_lookback", 10)), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "GEN_KELTNER_BREAKOUT":
        el = int(params["ema_len"]); al = int(params["atr_len"]); mult = params["mult"]
        mid = ema(close, el); a = atr(df, al)
        upper = mid + mult * a
        sig = (close > upper) & (close.shift(1) <= upper.shift(1)) & (close > df["ema_200"])
        stop = low.rolling(5, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "GEN_TRIPLE_EMA_STACK":
        e5 = ema(close, 5); e13 = ema(close, 13); e50 = ema(close, 50)
        dist = (close - e13).abs() / df["atr_14"]
        sig = (e5 > e13) & (e13 > e50) & (dist <= params["touch_atr"]) & (close > open_)
        stop = low.rolling(int(params.get("stop_lookback", 10)), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "GEN_STOCH_OVERSOLD_CROSS":
        n = int(params["stoch_n"]); d = int(params["smooth_d"]); ob = params["oversold"]
        ll = low.rolling(n, min_periods=n).min()
        hh = high.rolling(n, min_periods=n).max()
        k = 100 * (close - ll) / (hh - ll).replace(0, np.nan)
        dd = k.rolling(d, min_periods=d).mean()
        sig = (k.shift(1) <= dd.shift(1)) & (k > dd) & (k.shift(1) < ob) & (close > df["ema_200"])
        stop = low.rolling(5, min_periods=1).min()
        return sig.fillna(False), stop

    return pd.Series(False, index=df.index), pd.Series(np.nan, index=df.index)

# ------------------------------------------------------------------
# TRADE SIM (numpy fast path)
# ------------------------------------------------------------------
@dataclass
class SliceStats:
    num_trades: int
    win_rate: float
    net_return_pct: float        # compound
    max_drawdown_pct: float
    expectancy_R: float
    profit_factor: float
    avg_R: float
    sharpe: float                # per-trade sharpe * sqrt(n_trades)  (scaled / t-stat-like)
    sharpe_pt: float             # per-trade sharpe (mean/std, UNSCALED) — correct DSR input

def bootstrap_p_positive(R, n_boot=2000, seed=0):
    """One-sided bootstrap p-value that mean(R) <= 0. Lower = stronger positive edge."""
    R = np.asarray(R, dtype=float)
    n = len(R)
    if n < 5:
        return float("nan")
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(n_boot, n))
    means = R[idx].mean(axis=1)
    return float((means <= 0).mean())

def simulate_slice(df, sig, stop, strategy, s_idx, e_idx, return_trades=False):
    if e_idx - s_idx < 100:
        empty = SliceStats(0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        return (empty, np.array([])) if return_trades else empty

    cost = COST_BPS / 10000.0
    is_trail = (strategy == "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL")

    op = df["open"].to_numpy()
    hi = df["high"].to_numpy()
    lo = df["low"].to_numpy()
    cl = df["close"].to_numpy()
    em = df["ema_8"].to_numpy() if "ema_8" in df.columns else np.zeros(len(df))
    sg = sig.to_numpy()
    st = stop.to_numpy()

    trades_pct = []
    trades_R = []

    i = s_idx + 20
    end = e_idx - 1
    while i < end:
        if not sg[i]:
            i += 1
            continue
        entry_idx = i + 1
        if entry_idx >= e_idx:
            break
        entry_price = op[entry_idx]
        stop_price = st[i]
        if np.isnan(entry_price) or np.isnan(stop_price) or stop_price >= entry_price or entry_price <= 0:
            i += 1
            continue
        risk = entry_price - stop_price
        target = entry_price + 2.0 * risk
        exit_idx = min(entry_idx + HOLDING_BAR_LIMIT, e_idx - 1)
        exit_price = cl[exit_idx]

        for cur in range(entry_idx, exit_idx + 1):
            if lo[cur] <= stop_price:
                exit_idx = cur; exit_price = stop_price; break
            if not is_trail and hi[cur] >= target:
                exit_idx = cur; exit_price = target; break
            if is_trail and cl[cur] < em[cur]:
                nxt = min(cur + 1, e_idx - 1)
                exit_idx = cur; exit_price = op[nxt]; break

        raw = exit_price / entry_price - 1.0
        net = raw - cost
        trades_pct.append(net * 100.0)
        trades_R.append((exit_price - entry_price) / risk if risk > 0 else 0.0)
        i = max(exit_idx + 1, i + 1)

    if not trades_pct:
        empty = SliceStats(0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        return (empty, np.array([])) if return_trades else empty

    arr = np.array(trades_pct) / 100.0
    eq = np.cumprod(1.0 + arr)
    peak = np.maximum.accumulate(eq)
    dd = float((eq / peak - 1.0).min())
    wins = int((arr > 0).sum())
    win_rate = wins / len(arr)
    gw = float(arr[arr > 0].sum())
    gl = float(-arr[arr < 0].sum())
    pf = (gw / gl) if gl > 0 else (99.0 if gw > 0 else 0.0)
    arr_R = np.array(trades_R)
    avg_R = float(arr_R.mean()) if len(arr_R) else 0.0
    net_compound = float((eq[-1] - 1.0) * 100.0)
    std = float(arr.std(ddof=1)) if len(arr) > 1 else 0.0
    sharpe_pt = float(arr.mean() / std) if std > 0 else 0.0          # per-trade (unscaled)
    sharpe = float(sharpe_pt * math.sqrt(len(arr)))                  # scaled / t-stat-like
    stats = SliceStats(
        num_trades=len(trades_pct),
        win_rate=round(win_rate, 4),
        net_return_pct=round(net_compound, 3),
        max_drawdown_pct=round(dd * 100.0, 3),
        expectancy_R=round(avg_R, 4),
        profit_factor=round(min(pf, 99.0), 3),
        avg_R=round(avg_R, 4),
        sharpe=round(sharpe, 4),
        sharpe_pt=round(sharpe_pt, 6),
    )
    return (stats, arr_R) if return_trades else stats

# ------------------------------------------------------------------
# DATA HELPERS
# ------------------------------------------------------------------
def find_ds(manifest, symbol, tf):
    return next((d for d in manifest["datasets"]
                 if d["symbol"] == symbol and d["timeframe_normalized"] == tf
                 and d.get("ohlcv_validation_status") == "PASS"), None)

def load_df(ds_path):
    root = BUNDLE_MANIFEST.parents[1]
    df = pd.read_csv(root / ds_path)
    df["timestamp"] = pd.to_datetime(df["timestamp_utc"], utc=True)
    df["date"] = df["timestamp"].dt.date
    return df

def build_daily_rsi(manifest, symbol):
    ds = find_ds(manifest, symbol, "1D")
    if ds is None:
        return {}
    df = load_df(ds["normalized_path"])
    out = {}
    for n in (7, 10, 14, 21):
        s = rsi(df["close"], n).shift(1)
        out[n] = dict(zip(df["date"], s))
    return out

# ------------------------------------------------------------------
# FOLDS
# ------------------------------------------------------------------
def rolling_fold_indices(n_bars):
    lockbox_size = int(n_bars * LOCKBOX_FRACTION)
    span_end = n_bars - lockbox_size
    if span_end < 1000:
        return []
    train_size = int(span_end * FOLD_TRAIN_FRACTION)
    test_size = int(span_end * FOLD_TEST_FRACTION)
    if train_size < 400 or test_size < 200:
        return []
    remaining = span_end - (train_size + test_size)
    step = max(1, remaining // max(1, NUM_ROLLING_FOLDS - 1)) if NUM_ROLLING_FOLDS > 1 else 0
    folds = []
    for f in range(NUM_ROLLING_FOLDS):
        ts = f * step
        te = ts + train_size
        ks = te
        ke = min(ks + test_size, span_end)
        if ke - ks < 200 or te - ts < 400:
            break
        folds.append((ts, te, ks, ke))
    return folds

# ------------------------------------------------------------------
# WORKER
# ------------------------------------------------------------------
_MANIFEST = None
_DAILY_CACHE = {}

def _init_worker():
    global _MANIFEST
    _MANIFEST = json.load(open(BUNDLE_MANIFEST, encoding="utf-8"))

def _worker(job):
    """job = (strategy_id, symbol, timeframe)."""
    strategy, symbol, tf = job
    try:
        if strategy == "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK" and tf == "1D":
            return {"strategy": strategy, "symbol": symbol, "timeframe": tf,
                    "classification": "SKIPPED_RULE", "summary": {}}
        ds = find_ds(_MANIFEST, symbol, tf)
        if ds is None:
            return {"strategy": strategy, "symbol": symbol, "timeframe": tf,
                    "classification": "NO_DATA", "summary": {}}
        df = load_df(ds["normalized_path"])
        if len(df) < MIN_BARS_REQUIRED:
            return {"strategy": strategy, "symbol": symbol, "timeframe": tf,
                    "classification": "NO_DATA", "summary": {}, "data_rows": int(len(df))}

        needs_daily = (strategy == "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK")
        daily_maps = _DAILY_CACHE.get(symbol)
        if needs_daily and daily_maps is None:
            daily_maps = build_daily_rsi(_MANIFEST, symbol)
            _DAILY_CACHE[symbol] = daily_maps

        grid = GRIDS[strategy]
        # We evaluate each config and store its train-fold mean + lockbox stats
        configs = []
        sharpe_train_pool = []  # for DSR
        for p in grid:
            dmap = None
            if needs_daily:
                dmap = daily_maps.get(int(p["rsi_len"])) if daily_maps else None
                if dmap is None:
                    continue
            df_w = df.copy()
            sig, stop = build_signals(strategy, df_w, p, dmap)
            n = len(df_w)
            folds = rolling_fold_indices(n)
            if not folds:
                continue
            ft, fk = [], []
            for (ts, te, ks, ke) in folds:
                ft.append(asdict(simulate_slice(df_w, sig, stop, strategy, ts, te)))
                fk.append(asdict(simulate_slice(df_w, sig, stop, strategy, ks, ke)))
            lockbox_start = n - int(n * LOCKBOX_FRACTION)
            lb = asdict(simulate_slice(df_w, sig, stop, strategy, lockbox_start, n))
            mean_train_ret = sum(f["net_return_pct"] for f in ft) / len(ft) if ft else 0.0
            mean_train_sharpe_pt = sum(f["sharpe_pt"] for f in ft) / len(ft) if ft else 0.0
            configs.append({"params": p, "fold_train": ft, "fold_test": fk,
                            "lockbox": lb, "mean_train_ret": mean_train_ret,
                            "mean_train_sharpe_pt": mean_train_sharpe_pt})
            sharpe_train_pool.append(mean_train_sharpe_pt)

        if not configs:
            return {"strategy": strategy, "symbol": symbol, "timeframe": tf,
                    "classification": "NO_DATA", "summary": {}, "data_rows": int(len(df))}

        # Pick best by train return
        best = max(configs, key=lambda c: c["mean_train_ret"])

        # Re-run best config's lockbox capturing the per-trade R series for bootstrap
        bp = best["params"]
        dmap_b = None
        if needs_daily:
            dmap_b = daily_maps.get(int(bp["rsi_len"])) if daily_maps else None
        df_b = df.copy()
        sig_b, stop_b = build_signals(strategy, df_b, bp, dmap_b)
        nb = len(df_b)
        lockbox_start_b = nb - int(nb * LOCKBOX_FRACTION)
        _lb_stats, lb_R = simulate_slice(df_b, sig_b, stop_b, strategy, lockbox_start_b, nb, return_trades=True)
        # deterministic seed from job identity
        seed = (abs(hash((strategy, symbol, tf))) % (2**31))
        boot_p = bootstrap_p_positive(lb_R, n_boot=2000, seed=seed) if len(lb_R) >= MIN_TRADES_FOR_PASS else float("nan")

        test_rets = [f["net_return_pct"] for f in best["fold_test"]]
        test_trades = [f["num_trades"] for f in best["fold_test"]]
        pos = sum(1 for r in test_rets if r > 0)
        n_folds = len(test_rets)
        lb = best["lockbox"]
        if lb["num_trades"] < MIN_TRADES_FOR_PASS:
            cls = "INSUFFICIENT_TRADES"
        elif lb["net_return_pct"] > 0 and lb["max_drawdown_pct"] > -50 and lb["expectancy_R"] > 0 and pos >= max(1, n_folds // 2):
            if lb["expectancy_R"] >= 0.10 and lb["profit_factor"] >= 1.3 and pos == n_folds:
                cls = "STRONG_PASS"
            else:
                cls = "PASS"
        else:
            cls = "FAIL"

        # Deflated Sharpe local stats (within this strategy+symbol+tf trial pool)
        n_trials = len(sharpe_train_pool)
        std_sr = float(np.std(sharpe_train_pool, ddof=1)) if n_trials > 1 else 0.0
        max_sr = max(sharpe_train_pool) if sharpe_train_pool else 0.0

        return {
            "strategy": strategy, "symbol": symbol, "timeframe": tf,
            "data_rows": int(len(df)),
            "data_start": str(df["timestamp"].iloc[0]),
            "data_end":   str(df["timestamp"].iloc[-1]),
            "trial_count": n_trials,
            "trial_sr_std": round(std_sr, 4),
            "trial_sr_max": round(max_sr, 4),
            "boot_p_value": round(boot_p, 5) if boot_p == boot_p else None,
            "summary": {
                "best_params": best["params"],
                "fold_test_returns_pct": test_rets,
                "fold_test_trade_counts": test_trades,
                "fold_test_sharpes": [f["sharpe"] for f in best["fold_test"]],
                "avg_fold_test_return_pct": round(sum(test_rets)/n_folds, 3) if n_folds else 0.0,
                "folds_positive": pos,
                "n_folds": n_folds,
                "lockbox_oos": lb,
                "best_train_sharpe_pt": round(best["mean_train_sharpe_pt"], 6),
            },
            "classification": cls,
        }
    except Exception as e:
        return {"strategy": strategy, "symbol": symbol, "timeframe": tf,
                "classification": "ERROR", "error": str(e), "summary": {}}

# ------------------------------------------------------------------
# DEFLATED SHARPE RATIO (Bailey & López de Prado)
# ------------------------------------------------------------------
def deflated_sharpe_pvalue(observed_sr: float, n_trials: int, sr_std: float,
                           n_trades: int, skew: float = 0.0, kurt: float = 3.0) -> float:
    """
    Returns P(observed_sr <= chance | N trials, sigma_sr).
    Higher is better. p > 0.95 → robust beyond multiple-testing noise.

    Simplified DSR per Bailey-LdP (2014). Uses Euler-Mascheroni approximation
    for E[max{SR_i}] under null = 0.
    """
    if n_trials <= 1 or sr_std <= 0 or n_trades <= 1:
        return float("nan")
    EM = 0.5772156649  # Euler-Mascheroni
    # Expected max of N standard normals
    Z_emax = (1 - EM) * sps.norm.ppf(1 - 1/n_trials) + EM * sps.norm.ppf(1 - 1/(n_trials * math.e))
    expected_max_sr = sr_std * Z_emax  # null SR ~ N(0, sr_std)
    # Variance of estimator on n_trades
    denom = math.sqrt(max(1e-9, (1 - skew * observed_sr + (kurt - 1)/4 * observed_sr**2) / (n_trades - 1)))
    z = (observed_sr - expected_max_sr) / denom if denom > 0 else 0.0
    return float(sps.norm.cdf(z))

# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
def main():
    t0 = time.time()
    workers = max(2, min(8, cpu_count() - 1))
    total_param_sets = sum(len(g) for g in GRIDS.values())
    print(f"[start] workers={workers} symbols={len(SYMBOLS)} tfs={TIMEFRAMES} strategies={len(GRIDS)} param_sets_total={total_param_sets}", flush=True)

    jobs = [(s, sym, tf) for s in GRIDS for sym in SYMBOLS for tf in TIMEFRAMES]
    print(f"[start] total jobs (sym*tf*strat): {len(jobs)}; configs evaluated ~{len(jobs) * (total_param_sets // len(GRIDS))}", flush=True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    done = 0
    last_print = time.time()

    with Pool(processes=workers, initializer=_init_worker) as pool:
        for r in pool.imap_unordered(_worker, jobs, chunksize=1):
            results.append(r)
            done += 1
            now = time.time()
            if now - last_print > 60:
                cls_counts = {}
                for rr in results:
                    c = rr.get("classification", "?")
                    cls_counts[c] = cls_counts.get(c, 0) + 1
                print(f"  [{done}/{len(jobs)}] elapsed={int(now - t0)}s | counts={cls_counts}", flush=True)
                last_print = now

    runtime = round(time.time() - t0, 1)
    print(f"[end] all jobs done in {runtime}s", flush=True)

    # Post-process: per-strategy DSR
    by_strat: dict[str, list] = {}
    for r in results:
        by_strat.setdefault(r["strategy"], []).append(r)

    # ---- Deflated Sharpe Ratio (corrected: per-trade SR units) ----
    # Trial pool = the per-trade train Sharpe of the SELECTED config across all
    # (symbol, tf) of a strategy. sr_std measures dispersion of trial outcomes; the
    # number of parameter sets in the grid is the true N of trials per cell.
    for strat, rows in by_strat.items():
        grid_n = len(GRIDS[strat])  # number of parameter trials per (symbol, tf) cell
        pool_sr = [r["summary"]["best_train_sharpe_pt"] for r in rows
                   if r.get("classification") not in {"NO_DATA","ERROR","SKIPPED_RULE"}
                   and r.get("summary", {}).get("best_train_sharpe_pt") is not None]
        sr_std_global = float(np.std(pool_sr, ddof=1)) if len(pool_sr) > 1 else 0.0
        for r in rows:
            s = r.get("summary", {})
            lb = s.get("lockbox_oos") or {}
            sr_pt = lb.get("sharpe_pt") or 0.0          # PER-TRADE sharpe (correct units)
            n_t = lb.get("num_trades") or 0
            dsr_p = deflated_sharpe_pvalue(sr_pt, grid_n, max(sr_std_global, 1e-6), n_t)
            r["dsr_p_value"] = round(dsr_p, 4) if dsr_p == dsr_p else None
            r["dsr_robust"] = bool(dsr_p == dsr_p and dsr_p >= 0.95)

    # ---- Benjamini-Hochberg FDR over bootstrap p-values (primary multiplicity control) ----
    # Family = every selected best-config with a valid lockbox bootstrap p-value.
    bh_family = [r for r in results if r.get("boot_p_value") is not None]
    m = len(bh_family)
    Q = 0.10  # target false-discovery rate
    if m > 0:
        ordered = sorted(bh_family, key=lambda r: r["boot_p_value"])
        # largest k with p_(k) <= (k/m)*Q
        k_max = 0
        for k, r in enumerate(ordered, start=1):
            if r["boot_p_value"] <= (k / m) * Q:
                k_max = k
        survivors = set(id(r) for r in ordered[:k_max]) if k_max > 0 else set()
        bh_threshold = (k_max / m) * Q if k_max > 0 else 0.0
        for r in results:
            r["bh_fdr_survivor"] = bool(id(r) in survivors)
    else:
        bh_threshold = 0.0
        for r in results:
            r["bh_fdr_survivor"] = False

    # ---- Final robustness flag: PASS AND survives BH-FDR AND DSR-robust ----
    for r in results:
        cls = r.get("classification")
        r["robust_final"] = bool(
            cls in {"PASS", "STRONG_PASS"}
            and r.get("bh_fdr_survivor")
            and r.get("dsr_robust")
        )

    # Save full JSON
    out_json = OUTPUT_DIR / "MEGA_walk_forward_results.json"
    out_json.write_text(json.dumps({
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "runtime_seconds": runtime,
        "workers": workers,
        "config": {
            "cost_bps": COST_BPS,
            "lockbox_fraction": LOCKBOX_FRACTION,
            "fold_train_fraction": FOLD_TRAIN_FRACTION,
            "fold_test_fraction": FOLD_TEST_FRACTION,
            "num_rolling_folds": NUM_ROLLING_FOLDS,
            "min_bars": MIN_BARS_REQUIRED,
            "min_trades_for_pass": MIN_TRADES_FOR_PASS,
            "holding_bar_limit": HOLDING_BAR_LIMIT,
            "symbols": SYMBOLS,
            "timeframes": TIMEFRAMES,
            "strategy_count": len(GRIDS),
            "param_set_total": total_param_sets,
        },
        "results": results,
    }, indent=2), encoding="utf-8")

    # Build markdown report
    counts = {}
    for r in results:
        counts[r.get("classification","?")] = counts.get(r.get("classification","?"), 0) + 1

    passes = [r for r in results if r.get("classification") in {"PASS", "STRONG_PASS"}]
    passes.sort(key=lambda r: r["summary"]["lockbox_oos"]["net_return_pct"], reverse=True)

    robust = [r for r in passes if r.get("robust_final")]
    bh_survivors = [r for r in passes if r.get("bh_fdr_survivor")]
    dsr_only = [r for r in passes if r.get("dsr_robust")]

    md = [
        "# MEGA Rolling Walk-Forward + Deflated Sharpe + Bootstrap-FDR — Overnight Audit",
        "",
        f"- Generated: `{datetime.now(timezone.utc).isoformat()}`",
        f"- Runtime: `{runtime}s` ({round(runtime/60, 1)} min) with `{workers}` worker processes",
        f"- Symbols: {len(SYMBOLS)} | Timeframes: {TIMEFRAMES}",
        f"- Strategies: {len(GRIDS)} (11 prototyped + 6 generic patterns)",
        f"- Param sets total across grids: **{total_param_sets}**",
        f"- Total (strategy, symbol, tf) jobs: **{len(jobs)}**",
        f"- Cost: `{COST_BPS} bps` round-trip | Lockbox: last 25% | Rolling folds: {NUM_ROLLING_FOLDS}",
        f"- Classification counts: `{counts}`",
        f"- PASS configurations: **{len(passes)}**",
        f"- Bootstrap-FDR family size (testable lockboxes): **{m}** | BH q=0.10 | threshold p≤{bh_threshold:.5f}",
        f"- BH-FDR survivors: **{len(bh_survivors)}** | DSR-robust (p≥0.95): **{len(dsr_only)}**",
        f"- **FINAL ROBUST (PASS ∧ BH-FDR ∧ DSR): {len(robust)}**",
        "",
        "## Methodology note",
        "",
        "Three independent gates must ALL pass for `robust_final`:",
        "1. **Rolling walk-forward** — best param chosen on train folds; profitable on a 25% locked-box OOS slice never seen in selection; positive in ≥ half of forward folds.",
        "2. **Bootstrap significance** — 2000-resample one-sided bootstrap that lockbox mean-R > 0, then **Benjamini-Hochberg FDR (q=0.10)** across ALL testable cells to control multiple-testing.",
        "3. **Deflated Sharpe Ratio** — Bailey & López de Prado, per-trade Sharpe deflated by the expected max across the grid's parameter trials; p ≥ 0.95.",
        "",
        "## FINAL ROBUST Survivors (all three gates)",
        "",
        "| Strategy | Symbol | TF | Best Params | Lockbox Ret % | Sharpe | Boot p | DSR p | Trades | PF | Max DD % | Folds+ | Class |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    robust.sort(key=lambda r: r["summary"]["lockbox_oos"]["net_return_pct"], reverse=True)
    if not robust:
        md.append("| _(none survived all three gates)_ | | | | | | | | | | | | |")
    for r in robust[:80]:
        s = r["summary"]; lb = s["lockbox_oos"]
        md.append(
            f"| `{r['strategy'][:38]}` | {r['symbol']} | {r['timeframe']} | "
            f"`{json.dumps(s['best_params'], separators=(',',':'))[:60]}` | "
            f"{lb['net_return_pct']:.2f} | {lb['sharpe']:.2f} | {r.get('boot_p_value')} | {r['dsr_p_value']} | "
            f"{lb['num_trades']} | {lb['profit_factor']} | {lb['max_drawdown_pct']:.2f} | "
            f"{s['folds_positive']}/{s['n_folds']} | {r['classification']} |"
        )

    md += ["", "## Bootstrap-FDR Survivors (gate 1+2, DSR aside)", "",
           "| Strategy | Sym | TF | Lockbox Ret % | Sharpe | Boot p | DSR p | Trades | PF | Folds+ | Class |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    bh_survivors.sort(key=lambda r: r["summary"]["lockbox_oos"]["net_return_pct"], reverse=True)
    for r in bh_survivors[:120]:
        s = r["summary"]; lb = s["lockbox_oos"]
        md.append(
            f"| `{r['strategy'][:38]}` | {r['symbol']} | {r['timeframe']} | "
            f"{lb['net_return_pct']:.2f} | {lb['sharpe']:.2f} | {r.get('boot_p_value')} | {r.get('dsr_p_value','-')} | "
            f"{lb['num_trades']} | {lb['profit_factor']} | {s['folds_positive']}/{s['n_folds']} | {r['classification']} |"
        )

    md += ["", "## All PASS / STRONG_PASS (no multiplicity filter)", "",
           "| Strategy | Sym | TF | Lockbox Ret % | Sharpe | Boot p | DSR p | Trades | PF | MaxDD % | Folds+ | Class |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in passes[:200]:
        s = r["summary"]; lb = s["lockbox_oos"]
        md.append(
            f"| `{r['strategy'][:38]}` | {r['symbol']} | {r['timeframe']} | "
            f"{lb['net_return_pct']:.2f} | {lb['sharpe']:.2f} | {r.get('boot_p_value','-')} | {r.get('dsr_p_value','-')} | "
            f"{lb['num_trades']} | {lb['profit_factor']} | {lb['max_drawdown_pct']:.2f} | "
            f"{s['folds_positive']}/{s['n_folds']} | {r['classification']} |"
        )

    md += ["", "## Per-Strategy Top 3 PASS configurations", ""]
    for strat in sorted(GRIDS.keys()):
        rows = sorted([r for r in by_strat[strat]
                       if r.get("classification") in {"PASS","STRONG_PASS"}],
                      key=lambda r: r["summary"]["lockbox_oos"]["net_return_pct"], reverse=True)[:3]
        if not rows:
            continue
        md.append(f"### `{strat}`")
        md.append("")
        md.append("| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |")
        md.append("|---|---|---|---|---|---|---|---|---|")
        for r in rows:
            s = r["summary"]; lb = s["lockbox_oos"]
            md.append(
                f"| {r['symbol']} | {r['timeframe']} | "
                f"`{json.dumps(s['best_params'], separators=(',',':'))[:70]}` | "
                f"{lb['net_return_pct']:.2f} | {lb['sharpe']:.2f} | {r.get('dsr_p_value','-')} | "
                f"{lb['num_trades']} | {lb['profit_factor']} | {s['folds_positive']}/{s['n_folds']} |"
            )
        md.append("")

    (OUTPUT_DIR / "MEGA_walk_forward_report.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"DONE_MARKER  results={len(results)} passes={len(passes)} bh_survivors={len(bh_survivors)} dsr_robust={len(dsr_only)} robust_final={len(robust)} runtime={runtime}s", flush=True)
    print(f"  JSON: {out_json}", flush=True)
    print(f"  MD  : {OUTPUT_DIR / 'MEGA_walk_forward_report.md'}", flush=True)

if __name__ == "__main__":
    main()
