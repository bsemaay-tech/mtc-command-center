"""
Rigorous Rolling Walk-Forward + OOS — Multiprocess Edition
==========================================================
Same methodology as rigorous_walk_forward.py but parallelised across
(strategy, symbol, timeframe) jobs via multiprocessing.Pool.

Worker granularity: one (strategy, symbol, tf) per task. Each worker:
  * loads the OHLCV CSV for that (symbol, tf)
  * lazily builds daily-RSI map for that symbol if the strategy needs it
  * iterates the strategy's parameter grid, computes 3 rolling folds + lockbox
  * returns one result dict

Results streamed back through the pool, aggregated, and dumped to
RIGOROUS_walk_forward_results.json + RIGOROUS_walk_forward_report.md.
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
# GRIDS
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
        {"touch_atr": 0.25}, {"touch_atr": 0.40},
        {"touch_atr": 0.60}, {"touch_atr": 0.80},
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
        stop = low - 0.1 * df["atr_14"]
        return sig.fillna(False), stop

    return pd.Series(False, index=df.index), pd.Series(np.nan, index=df.index)

# ------------------------------------------------------------------
# TRADE SIM
# ------------------------------------------------------------------
@dataclass
class SliceStats:
    num_trades: int
    win_rate: float
    net_return_pct: float
    max_drawdown_pct: float
    expectancy_R: float
    profit_factor: float
    avg_R: float

def simulate_slice(df, sig, stop, strategy, s_idx, e_idx):
    if e_idx - s_idx < 100:
        return SliceStats(0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    cost = COST_BPS / 10000.0
    is_trail = (strategy == "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL")

    # Pull numpy views once (fast iat-like access)
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
        return SliceStats(0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

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
    return SliceStats(
        num_trades=len(trades_pct),
        win_rate=round(win_rate, 4),
        net_return_pct=round(net_compound, 3),
        max_drawdown_pct=round(dd * 100.0, 3),
        expectancy_R=round(avg_R, 4),
        profit_factor=round(min(pf, 99.0), 3),
        avg_R=round(avg_R, 4),
    )

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
    for n in (7, 14, 21):
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
    """Each pool worker loads the manifest once."""
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
                    "classification": "NO_DATA", "summary": {},
                    "data_rows": int(len(df))}

        needs_daily = (strategy == "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK")
        daily_maps = _DAILY_CACHE.get(symbol)
        if needs_daily and daily_maps is None:
            daily_maps = build_daily_rsi(_MANIFEST, symbol)
            _DAILY_CACHE[symbol] = daily_maps

        grid = GRIDS[strategy]
        configs = []
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
            ft, fk = [], []
            for (ts, te, ks, ke) in folds:
                ft.append(asdict(simulate_slice(df_w, sig, stop, strategy, ts, te)))
                fk.append(asdict(simulate_slice(df_w, sig, stop, strategy, ks, ke)))
            lockbox_start = n - int(n * LOCKBOX_FRACTION)
            lb = asdict(simulate_slice(df_w, sig, stop, strategy, lockbox_start, n))
            configs.append({"params": p, "fold_train": ft, "fold_test": fk, "lockbox": lb})

        # Pick best by mean train return
        best = None; best_score = -1e18
        for c in configs:
            if not c["fold_train"]:
                continue
            s = sum(f["net_return_pct"] for f in c["fold_train"]) / len(c["fold_train"])
            if s > best_score:
                best_score = s; best = c

        if best is None:
            return {"strategy": strategy, "symbol": symbol, "timeframe": tf,
                    "classification": "NO_DATA", "summary": {}, "data_rows": int(len(df))}

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

        return {
            "strategy": strategy, "symbol": symbol, "timeframe": tf,
            "data_rows": int(len(df)),
            "data_start": str(df["timestamp"].iloc[0]),
            "data_end":   str(df["timestamp"].iloc[-1]),
            "summary": {
                "best_params": best["params"],
                "fold_test_returns_pct": test_rets,
                "fold_test_trade_counts": test_trades,
                "avg_fold_test_return_pct": round(sum(test_rets)/n_folds, 3) if n_folds else 0.0,
                "folds_positive": pos,
                "n_folds": n_folds,
                "lockbox_oos": lb,
            },
            "classification": cls,
        }
    except Exception as e:
        return {"strategy": strategy, "symbol": symbol, "timeframe": tf,
                "classification": "ERROR", "error": str(e), "summary": {}}

# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
def main():
    t0 = time.time()
    workers = max(2, min(8, cpu_count() - 1))
    print(f"[start] workers={workers} symbols={len(SYMBOLS)} tfs={TIMEFRAMES} strategies={len(GRIDS)}")
    jobs = [(s, sym, tf) for s in GRIDS for sym in SYMBOLS for tf in TIMEFRAMES]
    print(f"[start] total jobs: {len(jobs)}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    done = 0
    last_print = time.time()

    with Pool(processes=workers, initializer=_init_worker) as pool:
        for r in pool.imap_unordered(_worker, jobs, chunksize=2):
            results.append(r)
            done += 1
            cls = r.get("classification")
            now = time.time()
            if cls in {"PASS", "STRONG_PASS"} or now - last_print > 10:
                lb = r.get("summary", {}).get("lockbox_oos", {})
                strat = r["strategy"][:40]
                print(f"  [{done}/{len(jobs)}] {strat} | {r['symbol']:>9} {r['timeframe']:>3} | "
                      f"cls={cls} | lb_ret={lb.get('net_return_pct',0)} trades={lb.get('num_trades',0)} pf={lb.get('profit_factor',0)}",
                      flush=True)
                last_print = now

    runtime = round(time.time() - t0, 1)
    # Save JSON
    out_json = OUTPUT_DIR / "RIGOROUS_walk_forward_results.json"
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
        },
        "results": results,
    }, indent=2), encoding="utf-8")

    counts = {}
    for r in results:
        counts[r.get("classification","?")] = counts.get(r.get("classification","?"), 0) + 1

    passes = [r for r in results if r.get("classification") in {"PASS", "STRONG_PASS"}]
    passes.sort(key=lambda r: r["summary"]["lockbox_oos"]["net_return_pct"], reverse=True)

    md = [
        "# Rigorous Rolling Walk-Forward — Audit Report (Parallel)",
        "",
        f"- Generated: `{datetime.now(timezone.utc).isoformat()}`",
        f"- Runtime: `{runtime}s` with `{workers}` worker processes",
        f"- Symbols: {len(SYMBOLS)} | Timeframes: {TIMEFRAMES} | Strategies: {len(GRIDS)}",
        f"- Cost: `{COST_BPS} bps` round-trip | Lockbox: last 25% | Rolling folds: {NUM_ROLLING_FOLDS}",
        f"- Total configurations: **{len(results)}**",
        f"- Classification counts: {counts}",
        "",
        "## Top Lockbox-OOS Performers (PASS / STRONG_PASS only)",
        "",
        "| Strategy | Symbol | TF | Lockbox Ret % (compound) | Trades | Win % | PF | Max DD % | Expectancy R | Fold-Test Avg % | Folds+ | Class |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in passes[:100]:
        s = r["summary"]; lb = s["lockbox_oos"]
        md.append(
            f"| `{r['strategy'][:40]}` | {r['symbol']} | {r['timeframe']} | "
            f"{lb['net_return_pct']:.2f} | {lb['num_trades']} | {lb['win_rate']*100:.1f} | "
            f"{lb['profit_factor']} | {lb['max_drawdown_pct']:.2f} | {lb['expectancy_R']} | "
            f"{s['avg_fold_test_return_pct']:.2f} | {s['folds_positive']}/{s['n_folds']} | {r['classification']} |"
        )

    md += ["", "## All Results Per Strategy (lockbox)", ""]
    by_strat = {}
    for r in results:
        by_strat.setdefault(r["strategy"], []).append(r)
    for strat, rows in by_strat.items():
        md.append(f"### `{strat}`")
        md.append("")
        md.append("| Symbol | TF | Class | Lockbox Ret % | Trades | PF | Max DD % | Expectancy R |")
        md.append("|---|---|---|---|---|---|---|---|")
        rows.sort(key=lambda r: (r.get("summary", {}).get("lockbox_oos", {}).get("net_return_pct", -999)), reverse=True)
        for r in rows:
            lb = r.get("summary", {}).get("lockbox_oos", {})
            md.append(
                f"| {r['symbol']} | {r['timeframe']} | {r.get('classification','?')} | "
                f"{lb.get('net_return_pct',0):.2f} | {lb.get('num_trades',0)} | {lb.get('profit_factor',0)} | "
                f"{lb.get('max_drawdown_pct',0):.2f} | {lb.get('expectancy_R',0)} |"
            )
        md.append("")

    (OUTPUT_DIR / "RIGOROUS_walk_forward_report.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"\nDONE in {runtime}s with {workers} workers. Results: {len(results)} | Passes: {len(passes)}")
    print(f"  JSON: {out_json}")
    print(f"  MD  : {OUTPUT_DIR / 'RIGOROUS_walk_forward_report.md'}")
    print(f"  Counts: {counts}")

if __name__ == "__main__":
    main()
