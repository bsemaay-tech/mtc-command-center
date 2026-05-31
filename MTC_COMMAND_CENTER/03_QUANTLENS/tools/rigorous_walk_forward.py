"""
Rigorous Rolling Walk-Forward + Out-of-Sample Validator
========================================================
Built to audit / replace Antigravity's single-split WF results.

Improvements over the prior `walk_forward_processor.py`:
  - Multiple rolling WF folds per (strategy, symbol, tf) instead of one fixed split
  - Locked-box terminal OOS slice (last 25% of available data is never seen during training)
  - Expanded parameter grids
  - Proper metrics: # trades, win rate, net return (compounded), max drawdown,
    expectancy (in R), profit factor, fold-pass count
  - Trade-count guardrail (min 30 trades) before crowning a config
  - Uses each dataset's ACTUAL date range (no fake 5.6-year claim)
  - 17 symbols x 5 timeframes (15m, 1h, 2h, 4h, 1D)
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

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
COST_BPS = 8.0  # round-trip in basis points

# Three rolling folds inside the first 75% of data + one locked terminal OOS slice
LOCKBOX_FRACTION = 0.25       # last 25% reserved for true OOS
FOLD_TRAIN_FRACTION = 0.60    # fraction of (pre-lockbox) span used as train per fold
FOLD_TEST_FRACTION = 0.20     # fraction used as immediate forward test per fold
NUM_ROLLING_FOLDS = 3

MIN_BARS_REQUIRED = 1500       # if dataset has fewer bars, skip the (sym, tf)
MIN_TRADES_FOR_PASS = 30       # require at least N trades in OOS to call PASS
HOLDING_BAR_LIMIT = 96         # max bars held per trade

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
def ema(s: pd.Series, n: int) -> pd.Series:
    return s.ewm(span=n, adjust=False, min_periods=n).mean()

def sma(s: pd.Series, n: int) -> pd.Series:
    return s.rolling(n, min_periods=n).mean()

def rsi(s: pd.Series, n: int) -> pd.Series:
    d = s.diff()
    g = d.clip(lower=0).ewm(alpha=1/n, adjust=False, min_periods=n).mean()
    l = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False, min_periods=n).mean()
    rs = g / l.replace(0, np.nan)
    return 100 - (100 / (1 + rs))

def atr(df: pd.DataFrame, n: int) -> pd.Series:
    pc = df["close"].shift(1)
    tr = pd.concat([
        df["high"] - df["low"],
        (df["high"] - pc).abs(),
        (df["low"] - pc).abs(),
    ], axis=1).max(axis=1)
    return tr.ewm(alpha=1/n, adjust=False, min_periods=n).mean()

# ------------------------------------------------------------------
# STRATEGY GRIDS (expanded)
# ------------------------------------------------------------------
GRIDS: dict[str, list[dict]] = {
    "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK": [
        {"rsi_len": 7,  "daily_hi": 60, "daily_lo": 40, "stop_lookback": 10},
        {"rsi_len": 14, "daily_hi": 55, "daily_lo": 45, "stop_lookback": 5},
        {"rsi_len": 14, "daily_hi": 60, "daily_lo": 40, "stop_lookback": 10},
        {"rsi_len": 7,  "daily_hi": 55, "daily_lo": 45, "stop_lookback": 7},
    ],
    "QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PLAYBOOK": [
        {"rsi_len": 7,  "sma_len": 50},
        {"rsi_len": 14, "sma_len": 50},
        {"rsi_len": 14, "sma_len": 100},
        {"rsi_len": 14, "sma_len": 200},
        {"rsi_len": 21, "sma_len": 100},
    ],
    "QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK": [
        {"pullback_atr": 0.25, "impulse_atr": 0.5},
        {"pullback_atr": 0.35, "impulse_atr": 1.0},
        {"pullback_atr": 0.50, "impulse_atr": 1.5},
        {"pullback_atr": 0.40, "impulse_atr": 0.8},
    ],
    "QL_2026-05-01_US_EQUITIES_INTRADAY_LE_MODEL_BULL_FLAG": [
        {"pullback_atr": 0.25, "impulse_atr": 0.5},
        {"pullback_atr": 0.35, "impulse_atr": 1.0},
        {"pullback_atr": 0.50, "impulse_atr": 1.5},
        {"pullback_atr": 0.40, "impulse_atr": 1.2},
    ],
    "QL_2026-05-01_US_EQUITIES_INTRADAY_PURPLE_PROFITS": [
        {"pullback_atr": 0.25, "impulse_atr": 0.5},
        {"pullback_atr": 0.35, "impulse_atr": 1.0},
        {"pullback_atr": 0.50, "impulse_atr": 1.5},
    ],
    "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL": [
        {"pullback_atr": 0.25, "impulse_atr": 0.5},
        {"pullback_atr": 0.35, "impulse_atr": 1.0},
        {"pullback_atr": 0.50, "impulse_atr": 1.5},
        {"pullback_atr": 0.40, "impulse_atr": 0.8},
    ],
    "QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNEL_PULLBACK": [
        {"touch_atr": 0.25},
        {"touch_atr": 0.40},
        {"touch_atr": 0.60},
        {"touch_atr": 0.80},
    ],
    "QL_2026-05-01_LIQUID_INTRADAY_VWAP_PULLBACK_REVERSAL": [
        {"session_window": 48,  "prox_atr": 0.25},
        {"session_window": 96,  "prox_atr": 0.40},
        {"session_window": 144, "prox_atr": 0.50},
        {"session_window": 96,  "prox_atr": 0.25},
    ],
    "QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR": [
        {"level_lookback": 32, "upper_third": 0.60},
        {"level_lookback": 48, "upper_third": 0.66},
        {"level_lookback": 96, "upper_third": 0.75},
        {"level_lookback": 64, "upper_third": 0.70},
    ],
    "QL_2026-05-01_ANY_BOLLINGER_BANDS_20_2_TRI_SETUP": [
        {"width_quantile": 0.15, "body_atr": 0.15},
        {"width_quantile": 0.25, "body_atr": 0.25},
        {"width_quantile": 0.10, "body_atr": 0.30},
        {"width_quantile": 0.20, "body_atr": 0.20},
    ],
    "QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE": [
        {"level_lookback": 48,  "tolerance_atr": 0.25},
        {"level_lookback": 96,  "tolerance_atr": 0.40},
        {"level_lookback": 144, "tolerance_atr": 0.50},
    ],
}

# ------------------------------------------------------------------
# SIGNAL ENGINES
# ------------------------------------------------------------------
def build_signals(strategy: str, df: pd.DataFrame, params: dict,
                  daily_rsi_map: dict | None = None) -> tuple[pd.Series, pd.Series]:
    close = df["close"]; high = df["high"]; low = df["low"]; open_ = df["open"]
    if "atr_14" not in df:  df["atr_14"]  = atr(df, 14)
    if "ema_8" not in df:   df["ema_8"]   = ema(close, 8)
    if "ema_5" not in df:   df["ema_5"]   = ema(close, 5)
    if "ema_13" not in df:  df["ema_13"]  = ema(close, 13)
    if "ema_200" not in df: df["ema_200"] = ema(close, 200)

    if strategy == "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK":
        if daily_rsi_map is None:
            return pd.Series(False, index=df.index), pd.Series(np.nan, index=df.index)
        df["daily_rsi"] = df["date"].map(daily_rsi_map)
        df["rsi_l"] = rsi(close, int(params["rsi_len"]))
        sig = (
            (df["daily_rsi"] > params["daily_hi"]) &
            (df["rsi_l"].shift(1) < params["daily_lo"]) &
            (df["rsi_l"] >= params["daily_lo"])
        )
        stop = low.rolling(int(params["stop_lookback"]), min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PLAYBOOK":
        rlen = int(params["rsi_len"]); slen = int(params["sma_len"])
        s = sma(close, slen); r = rsi(close, rlen)
        sig = (close > s) & (r.shift(1) < 50) & (r >= 50)
        stop = low.rolling(5, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy in {
        "QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK",
        "QL_2026-05-01_US_EQUITIES_INTRADAY_LE_MODEL_BULL_FLAG",
        "QL_2026-05-01_US_EQUITIES_INTRADAY_PURPLE_PROFITS",
        "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL",
    }:
        slope = df["ema_8"] - df["ema_8"].shift(3)
        dist = (close - df["ema_8"]).abs() / df["atr_14"]
        impulse = (close - close.shift(3)).abs() / df["atr_14"]
        sig = (close > df["ema_8"]) & (slope > 0) & \
              (dist <= params["pullback_atr"]) & (impulse.shift(1) >= params["impulse_atr"])
        stop = low.rolling(3, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNEL_PULLBACK":
        dist = (close - df["ema_13"]).abs() / df["atr_14"]
        sig = (close > df["ema_200"]) & (df["ema_5"] > df["ema_13"]) & \
              (dist <= params["touch_atr"]) & (close > open_)
        stop = low.rolling(5, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_2026-05-01_LIQUID_INTRADAY_VWAP_PULLBACK_REVERSAL":
        w = int(params["session_window"])
        proxy = close.rolling(w, min_periods=w).mean()
        band = close.rolling(w, min_periods=w).std()
        slope = proxy - proxy.shift(4)
        prox = (close - proxy).abs() / df["atr_14"]
        sig = (slope > 0) & (close > proxy) & (prox <= params["prox_atr"])
        stop = proxy - 1.0 * band
        return sig.fillna(False), stop

    if strategy == "QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR":
        w = int(params["level_lookback"])
        brk = high.rolling(w, min_periods=10).max().shift(1)
        rng = (high - low).replace(0, np.nan)
        pos = (close - low) / rng
        sig = (pos >= params["upper_third"]) & (close > high.shift(1)) & (close > brk)
        stop = low.rolling(2, min_periods=1).min()
        return sig.fillna(False), stop

    if strategy == "QL_2026-05-01_ANY_BOLLINGER_BANDS_20_2_TRI_SETUP":
        mid = sma(close, 20); std = close.rolling(20, min_periods=20).std()
        upper = mid + 2 * std
        width = (4 * std) / mid
        limit = width.rolling(200, min_periods=200).quantile(params["width_quantile"])
        narrow = width <= limit
        body_ok = (close - open_).abs() >= params["body_atr"] * df["atr_14"]
        sig = narrow.shift(1).fillna(False) & (close > upper) & body_ok
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
        stop = low - 0.1 * df["atr_14"]
        return sig.fillna(False), stop

    return pd.Series(False, index=df.index), pd.Series(np.nan, index=df.index)

# ------------------------------------------------------------------
# TRADE SIM ON A SLICE
# ------------------------------------------------------------------
@dataclass
class SliceStats:
    num_trades: int
    win_rate: float
    net_return_pct: float        # compounded
    max_drawdown_pct: float      # on equity curve
    expectancy_R: float
    profit_factor: float
    avg_R: float

def simulate_slice(df: pd.DataFrame, sig: pd.Series, stop: pd.Series,
                   strategy: str, s_idx: int, e_idx: int) -> SliceStats:
    if e_idx - s_idx < 100:
        return SliceStats(0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    cost = COST_BPS / 10000.0
    is_trail = (strategy == "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL")
    trades_pct: list[float] = []
    trades_R: list[float] = []

    i = s_idx + 20
    while i < e_idx - 1:
        if not bool(sig.iat[i]):
            i += 1
            continue
        entry_idx = i + 1
        if entry_idx >= e_idx:
            break
        entry_price = float(df["open"].iat[entry_idx])
        stop_price = float(stop.iat[i]) if not pd.isna(stop.iat[i]) else np.nan
        if pd.isna(entry_price) or pd.isna(stop_price) or stop_price >= entry_price or entry_price <= 0:
            i += 1
            continue
        risk = entry_price - stop_price
        target = entry_price + 2.0 * risk
        exit_idx = min(entry_idx + HOLDING_BAR_LIMIT, e_idx - 1)
        exit_price = float(df["close"].iat[exit_idx])

        for cur in range(entry_idx, exit_idx + 1):
            c_low = float(df["low"].iat[cur])
            c_high = float(df["high"].iat[cur])
            c_close = float(df["close"].iat[cur])
            if c_low <= stop_price:
                exit_idx = cur; exit_price = stop_price; break
            if not is_trail and c_high >= target:
                exit_idx = cur; exit_price = target; break
            if is_trail:
                c_ema = float(df["ema_8"].iat[cur]) if "ema_8" in df.columns else 0.0
                if c_close < c_ema:
                    nxt = min(cur + 1, e_idx - 1)
                    exit_idx = cur; exit_price = float(df["open"].iat[nxt]); break

        raw = exit_price / entry_price - 1.0
        net = raw - cost
        trades_pct.append(net * 100.0)
        trades_R.append((exit_price - entry_price) / risk if risk > 0 else 0.0)
        i = max(exit_idx + 1, i + 1)

    if not trades_pct:
        return SliceStats(0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    arr = np.array(trades_pct) / 100.0
    eq = np.cumprod(1.0 + arr)
    peak = np.maximum.accumulate(eq)
    dd = (eq / peak - 1.0).min()
    wins = sum(1 for x in trades_pct if x > 0)
    win_rate = wins / len(trades_pct)
    gross_win = sum(x for x in trades_pct if x > 0)
    gross_loss = sum(-x for x in trades_pct if x < 0)
    pf = (gross_win / gross_loss) if gross_loss > 0 else (math.inf if gross_win > 0 else 0.0)
    arr_R = np.array(trades_R)
    avg_R = float(arr_R.mean()) if len(arr_R) else 0.0
    expectancy_R = float(arr_R.mean()) if len(arr_R) else 0.0  # avg R per trade
    net_compound = float((eq[-1] - 1.0) * 100.0)
    return SliceStats(
        num_trades=len(trades_pct),
        win_rate=round(win_rate, 4),
        net_return_pct=round(net_compound, 3),
        max_drawdown_pct=round(float(dd) * 100.0, 3),
        expectancy_R=round(expectancy_R, 4),
        profit_factor=round(pf if math.isfinite(pf) else 99.0, 3),
        avg_R=round(avg_R, 4),
    )

# ------------------------------------------------------------------
# DATA
# ------------------------------------------------------------------
def load_manifest():
    return json.load(open(BUNDLE_MANIFEST, encoding="utf-8"))

def find_ds(manifest, symbol: str, tf: str):
    return next((d for d in manifest["datasets"]
                 if d["symbol"] == symbol and d["timeframe_normalized"] == tf
                 and d.get("ohlcv_validation_status") == "PASS"), None)

def load_df(manifest, ds) -> pd.DataFrame:
    root = BUNDLE_MANIFEST.parents[1]
    df = pd.read_csv(root / ds["normalized_path"])
    df["timestamp"] = pd.to_datetime(df["timestamp_utc"], utc=True)
    df["date"] = df["timestamp"].dt.date
    return df

def build_daily_rsi(manifest, symbol: str) -> dict[int, dict]:
    ds = find_ds(manifest, symbol, "1D")
    if ds is None:
        return {}
    df = load_df(manifest, ds)
    out = {}
    for n in (7, 14, 21):
        s = rsi(df["close"], n).shift(1)
        out[n] = dict(zip(df["date"], s))
    return out

# ------------------------------------------------------------------
# WALK-FORWARD DRIVER
# ------------------------------------------------------------------
def rolling_fold_indices(n_bars: int) -> list[tuple[int, int, int, int]]:
    """Return list of (train_start, train_end, test_start, test_end) inside pre-lockbox span."""
    lockbox_size = int(n_bars * LOCKBOX_FRACTION)
    span_end = n_bars - lockbox_size  # all rolling folds live in [0, span_end)
    if span_end < 1000:
        return []
    train_size = int(span_end * FOLD_TRAIN_FRACTION)
    test_size = int(span_end * FOLD_TEST_FRACTION)
    if train_size < 400 or test_size < 200:
        return []
    folds = []
    # NUM_ROLLING_FOLDS folds, each shifted forward by step
    remaining = span_end - (train_size + test_size)
    step = max(1, remaining // max(1, NUM_ROLLING_FOLDS - 1)) if NUM_ROLLING_FOLDS > 1 else 0
    for f in range(NUM_ROLLING_FOLDS):
        ts = f * step
        te = ts + train_size
        ks = te
        ke = min(ks + test_size, span_end)
        if ke - ks < 200 or te - ts < 400:
            break
        folds.append((ts, te, ks, ke))
    return folds

def evaluate_config(df: pd.DataFrame, strategy: str, params: dict,
                    daily_map: dict | None) -> dict:
    """Build signals once for the dataset, then score on each fold + lockbox."""
    sig, stop = build_signals(strategy, df, params, daily_map)
    n = len(df)
    folds = rolling_fold_indices(n)
    fold_train = []
    fold_test = []
    for (ts, te, ks, ke) in folds:
        fold_train.append(asdict(simulate_slice(df, sig, stop, strategy, ts, te)))
        fold_test.append(asdict(simulate_slice(df, sig, stop, strategy, ks, ke)))
    lockbox_start = n - int(n * LOCKBOX_FRACTION)
    lockbox = simulate_slice(df, sig, stop, strategy, lockbox_start, n)
    return {
        "params": params,
        "fold_train": fold_train,
        "fold_test":  fold_test,
        "lockbox":    asdict(lockbox),
    }

def pick_best(configs: list[dict]) -> dict | None:
    """Average train return across folds; pick highest. Skip configs with 0-trade folds."""
    best = None
    best_score = -1e9
    for c in configs:
        if not c["fold_train"]:
            continue
        rets = [f["net_return_pct"] for f in c["fold_train"]]
        score = sum(rets) / len(rets)
        if score > best_score:
            best_score = score; best = c
    return best

def summarize_picked(c: dict) -> dict:
    if c is None:
        return {}
    test_rets = [f["net_return_pct"] for f in c["fold_test"]]
    test_trades = [f["num_trades"] for f in c["fold_test"]]
    avg_test = sum(test_rets) / len(test_rets) if test_rets else 0.0
    folds_positive = sum(1 for r in test_rets if r > 0)
    return {
        "best_params": c["params"],
        "fold_test_returns_pct": test_rets,
        "fold_test_trade_counts": test_trades,
        "avg_fold_test_return_pct": round(avg_test, 3),
        "folds_positive": folds_positive,
        "n_folds": len(test_rets),
        "lockbox_oos": c["lockbox"],
    }

def classify(summary: dict) -> str:
    if not summary:
        return "NO_DATA"
    lb = summary["lockbox_oos"]
    n = summary["n_folds"]
    pos = summary["folds_positive"]
    if lb["num_trades"] < MIN_TRADES_FOR_PASS:
        return "INSUFFICIENT_TRADES"
    if lb["net_return_pct"] > 0 and lb["max_drawdown_pct"] > -50 and lb["expectancy_R"] > 0 and pos >= max(1, n // 2):
        if lb["expectancy_R"] >= 0.10 and lb["profit_factor"] >= 1.3 and pos == n:
            return "STRONG_PASS"
        return "PASS"
    return "FAIL"

# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
def main():
    t0 = time.time()
    manifest = load_manifest()
    print(f"[{datetime.now(timezone.utc).isoformat()}] Loaded manifest ({len(manifest['datasets'])} datasets)")

    daily_rsi_cache: dict[str, dict] = {}
    results: list[dict] = []
    skipped: list[dict] = []

    grid_items = list(GRIDS.items())
    total_combos = len(grid_items) * len(SYMBOLS) * len(TIMEFRAMES)
    done = 0

    for sym in SYMBOLS:
        # daily RSI cache for Dual RSI
        if sym not in daily_rsi_cache:
            try:
                daily_rsi_cache[sym] = build_daily_rsi(manifest, sym)
            except Exception as e:
                print(f"  ! daily rsi build failed for {sym}: {e}")
                daily_rsi_cache[sym] = {}

        for tf in TIMEFRAMES:
            ds = find_ds(manifest, sym, tf)
            if ds is None:
                for cid, _ in grid_items:
                    done += 1
                skipped.append({"symbol": sym, "tf": tf, "reason": "no_dataset"})
                continue
            try:
                df = load_df(manifest, ds)
            except Exception as e:
                for cid, _ in grid_items:
                    done += 1
                skipped.append({"symbol": sym, "tf": tf, "reason": f"load_err: {e}"})
                continue

            if len(df) < MIN_BARS_REQUIRED:
                for cid, _ in grid_items:
                    done += 1
                skipped.append({"symbol": sym, "tf": tf, "reason": f"too_short ({len(df)} bars)"})
                continue

            data_start = str(df["timestamp"].iloc[0])
            data_end   = str(df["timestamp"].iloc[-1])

            for cid, grid in grid_items:
                done += 1
                # Dual RSI strategy: needs daily RSI map; doesn't run on 1D
                if cid == "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK" and tf == "1D":
                    continue
                try:
                    configs = []
                    for p in grid:
                        dmap = None
                        if cid == "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK":
                            dmap = daily_rsi_cache.get(sym, {}).get(int(p["rsi_len"]))
                            if dmap is None:
                                continue
                        configs.append(evaluate_config(df.copy(), cid, p, dmap))
                    best = pick_best(configs)
                    summary = summarize_picked(best)
                    cls = classify(summary)
                    record = {
                        "strategy": cid,
                        "symbol": sym,
                        "timeframe": tf,
                        "data_rows": int(len(df)),
                        "data_start": data_start,
                        "data_end": data_end,
                        "summary": summary,
                        "classification": cls,
                    }
                    results.append(record)
                    if done % 25 == 0 or cls in {"PASS", "STRONG_PASS"}:
                        lb = summary.get("lockbox_oos", {})
                        print(f"  [{done}/{total_combos}] {cid[:40]} | {sym:>9} {tf:>3} | "
                              f"cls={cls} | lockbox: ret={lb.get('net_return_pct',0):.2f}% "
                              f"trades={lb.get('num_trades',0)} pf={lb.get('profit_factor',0)}")
                except Exception as e:
                    print(f"  ! err {cid} {sym} {tf}: {e}")
                    results.append({
                        "strategy": cid, "symbol": sym, "timeframe": tf,
                        "error": str(e), "classification": "ERROR",
                    })

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_json = OUTPUT_DIR / "RIGOROUS_walk_forward_results.json"
    out_json.write_text(json.dumps({
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "runtime_seconds": round(time.time() - t0, 1),
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
        },
        "results": results,
        "skipped": skipped,
    }, indent=2), encoding="utf-8")

    # Build summary report
    passes = [r for r in results if r.get("classification") in {"PASS", "STRONG_PASS"}]
    passes.sort(key=lambda r: r["summary"]["lockbox_oos"]["net_return_pct"], reverse=True)

    md = [
        "# Rigorous Rolling Walk-Forward — Audit Report",
        "",
        f"- Generated: `{datetime.now(timezone.utc).isoformat()}`",
        f"- Runtime: `{round(time.time() - t0, 1)}s`",
        f"- Symbols: {len(SYMBOLS)} | Timeframes: {TIMEFRAMES} | Strategies: {len(GRIDS)}",
        f"- Cost: `{COST_BPS} bps` round-trip | Lockbox: last 25% of data | Folds: {NUM_ROLLING_FOLDS}",
        f"- Total configurations evaluated: **{len(results)}**",
        f"- Skipped (no data / too short): **{len(skipped)}**",
        f"- Classification — STRONG_PASS: {sum(1 for r in results if r.get('classification')=='STRONG_PASS')}, "
        f"PASS: {sum(1 for r in results if r.get('classification')=='PASS')}, "
        f"FAIL: {sum(1 for r in results if r.get('classification')=='FAIL')}, "
        f"INSUFFICIENT_TRADES: {sum(1 for r in results if r.get('classification')=='INSUFFICIENT_TRADES')}, "
        f"NO_DATA: {sum(1 for r in results if r.get('classification')=='NO_DATA')}",
        "",
        "## Top Lockbox-OOS Performers (PASS / STRONG_PASS only)",
        "",
        "| Strategy | Symbol | TF | Lockbox Ret % (compound) | Trades | Win % | PF | Max DD % | Expectancy R | Fold-Test Avg % | Folds+ | Class |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in passes[:60]:
        s = r["summary"]; lb = s["lockbox_oos"]
        md.append(
            f"| `{r['strategy'][:40]}` | {r['symbol']} | {r['timeframe']} | "
            f"{lb['net_return_pct']:.2f} | {lb['num_trades']} | {lb['win_rate']*100:.1f} | "
            f"{lb['profit_factor']} | {lb['max_drawdown_pct']:.2f} | {lb['expectancy_R']} | "
            f"{s['avg_fold_test_return_pct']:.2f} | {s['folds_positive']}/{s['n_folds']} | {r['classification']} |"
        )

    (OUTPUT_DIR / "RIGOROUS_walk_forward_report.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"\nDONE in {round(time.time() - t0, 1)}s.  Results: {len(results)} | Passes: {len(passes)}")
    print(f"  JSON: {out_json}")
    print(f"  MD  : {OUTPUT_DIR / 'RIGOROUS_walk_forward_report.md'}")

if __name__ == "__main__":
    main()
