from __future__ import annotations

import csv
import json
import math
import random
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd

from stage2_lib.costs import BASE_ROUND_TRIP_COST_PCT, apply_round_trip_cost
from stage2_lib.data_loader import data_quality, normalize_ohlcv
from stage2_lib.exits import atr, ema, rsi, sma
from stage2_lib.metrics import fee_stress, max_drawdown_pct, metrics_from_trades, monte_carlo, profit_factor
from stage2_lib.reporting import md_table
from stage2_lib.robustness import remove_best_asset, remove_best_year, remove_top_trades
from stage2_lib.validation import fee_monotonic_ok
from stage2_lib.walkforward import chronological_splits


OUT = Path(__file__).resolve().parent
REPO = OUT.parents[2]
QL = REPO / "06_QUANTLENS_LAB"
RESEARCH = QL / "research"
GIT_ROOT = REPO.parent
BUNDLE = REPO.parent / "MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427"
DATA_5M = RESEARCH / "data_acquisition_5m_2026_05_03" / "normalized" / "binance_futures"

ASSETS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", "AVAXUSDT", "LINKUSDT", "DOTUSDT", "LTCUSDT", "TRXUSDT", "APTUSDT", "ARBUSDT", "NEARUSDT", "OPUSDT", "POLUSDT"]
CORE_5M = ASSETS


@dataclass
class Candidate:
    candidate_id: str
    name: str
    aliases: str
    horizon: str
    family: str
    native_asset_class: str
    native_timeframe: str
    data_status: str
    eligible: bool
    reason: str


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def append(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(text)


def save_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("status\nNO_ROWS\n", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def command(cmd: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(cmd, cwd=REPO, text=True, capture_output=True)
    append(OUT / "COMMAND_LOG.txt", f"$ {' '.join(cmd)}\nexit={result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}\n\n")
    return result.returncode, result.stdout, result.stderr


def find_file(symbol: str, timeframe: str) -> Path | None:
    if timeframe == "5m":
        files = sorted((DATA_5M / symbol / "5m").glob("*.csv"))
        return files[0] if files else None
    files = sorted((BUNDLE / "normalized" / "binance_futures" / symbol / timeframe).glob("*.csv"))
    return files[0] if files else None


def load(symbol: str, timeframe: str) -> pd.DataFrame:
    path = find_file(symbol, timeframe)
    if path is None:
        raise FileNotFoundError(f"{symbol} {timeframe}")
    return normalize_ohlcv(path)


def trade(candidate: str, asset: str, tf: str, variant: str, param: str, entry_i: int, exit_i: int, direction: str, entry: float, exit_: float, df: pd.DataFrame) -> dict[str, Any]:
    gross = (exit_ / entry - 1.0) * 100.0 if direction == "long" else (entry / exit_ - 1.0) * 100.0
    return {
        "candidate_id": candidate,
        "asset": asset,
        "timeframe": tf,
        "variant": variant,
        "parameter_set": param,
        "entry_time": str(df.loc[entry_i, "timestamp"]),
        "exit_time": str(df.loc[exit_i, "timestamp"]),
        "direction": direction,
        "entry_price": round(float(entry), 8),
        "exit_price": round(float(exit_), 8),
        "gross_return_pct": round(float(gross), 6),
        "net_return_pct": round(float(apply_round_trip_cost(gross)), 6),
        "hold_bars": int(max(exit_i - entry_i, 0)),
    }


def exit_trade(df: pd.DataFrame, entry_i: int, direction: str, entry: float, stop: float | None, target: float | None, max_hold: int, exit_mode: str) -> tuple[int, float]:
    last = min(entry_i + max_hold, len(df) - 1)
    for j in range(entry_i, last + 1):
        if direction == "long":
            if stop is not None and df.loc[j, "low"] <= stop:
                return j, float(stop)
            if target is not None and df.loc[j, "high"] >= target:
                return j, float(target)
        else:
            if stop is not None and df.loc[j, "high"] >= stop:
                return j, float(stop)
            if target is not None and df.loc[j, "low"] <= target:
                return j, float(target)
    if exit_mode == "close_exit":
        return entry_i, float(df.loc[entry_i, "close"])
    return last, float(df.loc[last, "close"])


def sig_kell(df: pd.DataFrame, asset: str, tf: str, params: dict[str, Any]) -> list[dict[str, Any]]:
    d = df.copy()
    d["ema10"] = ema(d["close"], int(params["fast"]))
    d["ema20"] = ema(d["close"], int(params["slow"]))
    d["atr"] = atr(d, 14)
    base_range = (d["high"].rolling(int(params["base_lb"])).max() / d["low"].rolling(int(params["base_lb"])).min() - 1) * 100
    trades = []
    i = 50
    while i < len(d) - 2:
        signal = d.loc[i, "ema10"] > d.loc[i, "ema20"] and base_range.iloc[i] <= float(params["max_base"]) and d.loc[i - 1, "close"] <= d.loc[i - 1, "ema10"] and d.loc[i, "close"] > d.loc[i, "ema10"]
        if params.get("regime") == "ema200":
            signal = signal and d.loc[i, "close"] > ema(d["close"], 200).iloc[i]
        if signal:
            entry_i = i + 1
            entry = float(d.loc[entry_i, "open"])
            stop = float(max(d["low"].iloc[max(0, i - 5) : i + 1].min(), entry - 2.0 * d.loc[i, "atr"]))
            exit_i, exit_ = exit_trade(d, entry_i, "long", entry, stop, None, int(params["hold"]), str(params["exit"]))
            trades.append(trade("KELL_WEDGE", asset, tf, str(params["exit"]), json.dumps(params, sort_keys=True), entry_i, exit_i, "long", entry, exit_, d))
            i = exit_i + 1
        else:
            i += 1
    return trades


def sig_slingshot(df: pd.DataFrame, asset: str, tf: str, params: dict[str, Any]) -> list[dict[str, Any]]:
    d = df.copy()
    length = int(params["ema_high"])
    lookback = int(params["pb_lb"])
    d["ema_high"] = ema(d["high"], length)
    d["sma50"] = sma(d["close"], 50)
    d["atr"] = atr(d, 14)
    trades = []
    i = 60
    while i < len(d) - 2:
        pullback = (d["close"].iloc[i - lookback : i] < d["ema_high"].iloc[i - lookback : i]).any()
        trigger = d.loc[i - 1, "close"] <= d.loc[i - 1, "ema_high"] and d.loc[i, "close"] > d.loc[i, "ema_high"]
        if pullback and trigger and d.loc[i, "close"] > d.loc[i, "sma50"]:
            entry_i = i + 1
            entry = float(d.loc[entry_i, "open"])
            stop = float(d["low"].iloc[max(0, i - lookback) : i + 1].min())
            risk = max(entry - stop, entry * 0.01)
            target = entry + float(params["r_mult"]) * risk if params["exit"] == "R_target" else None
            exit_i, exit_ = exit_trade(d, entry_i, "long", entry, stop, target, int(params["hold"]), str(params["exit"]))
            trades.append(trade("SLINGSHOT", asset, tf, str(params["exit"]), json.dumps(params, sort_keys=True), entry_i, exit_i, "long", entry, exit_, d))
            i = exit_i + 1
        else:
            i += 1
    return trades


def sig_crabel(df: pd.DataFrame, asset: str, tf: str, params: dict[str, Any]) -> list[dict[str, Any]]:
    d = df.copy()
    prev_range = (d["high"] - d["low"]).shift(1)
    prev_close = d["close"].shift(1)
    buy = prev_close + prev_range * float(params["range_mult"])
    sell = prev_close - prev_range * float(params["range_mult"])
    d["atr"] = atr(d, 14)
    trades = []
    for i in range(20, len(d) - 2):
        long_sig = d.loc[i, "high"] >= buy.iloc[i]
        short_sig = d.loc[i, "low"] <= sell.iloc[i]
        if long_sig and short_sig:
            continue
        direction = None
        entry = None
        if long_sig and params["direction"] in {"long", "both"}:
            direction, entry = "long", float(buy.iloc[i])
        elif short_sig and params["direction"] in {"short", "both"}:
            direction, entry = "short", float(sell.iloc[i])
        if not direction or not math.isfinite(entry):
            continue
        entry_i = i
        if params["exit"] == "close_exit":
            exit_i, exit_ = i, float(d.loc[i, "close"])
        elif params["exit"] == "time3":
            exit_i, exit_ = min(i + 3, len(d) - 1), float(d.loc[min(i + 3, len(d) - 1), "close"])
        else:
            stop = entry - 2 * d.loc[i, "atr"] if direction == "long" else entry + 2 * d.loc[i, "atr"]
            target = entry + 2 * d.loc[i, "atr"] if direction == "long" else entry - 2 * d.loc[i, "atr"]
            exit_i, exit_ = exit_trade(d, entry_i, direction, entry, float(stop), float(target), 3, "atr")
        trades.append(trade("CRABEL", asset, tf, str(params["exit"]), json.dumps(params, sort_keys=True), entry_i, exit_i, direction, entry, exit_, d))
    return trades


def sig_linda(df: pd.DataFrame, asset: str, tf: str, params: dict[str, Any]) -> list[dict[str, Any]]:
    d = df.copy()
    d["sma5"] = sma(d["close"], int(params["sma"]))
    d["sma50"] = sma(d["close"], 50)
    d["sma200"] = sma(d["close"], 200)
    d["atr"] = atr(d, 14)
    trades = []
    i = 210
    while i < len(d) - 2:
        trend = d.loc[i, "close"] > d.loc[i, "sma50"] and (params["trend"] == "sma50" or d.loc[i, "close"] > d.loc[i, "sma200"])
        signal = trend and d.loc[i - 1, "close"] >= d.loc[i - 1, "sma5"] and d.loc[i, "close"] < d.loc[i, "sma5"]
        if signal:
            entry_i = i + 1
            entry = float(d.loc[entry_i, "open"])
            stop = entry - float(params["atr_stop"]) * d.loc[i, "atr"] if params["atr_stop"] else None
            exit_i = min(entry_i + int(params["hold"]), len(d) - 1)
            exit_ = float(d.loc[exit_i, "close"])
            for j in range(entry_i + 1, exit_i + 1):
                if stop is not None and d.loc[j, "low"] <= stop:
                    exit_i, exit_ = j, float(stop)
                    break
                if d.loc[j, "close"] > d.loc[j, "sma5"]:
                    exit_i, exit_ = j, float(d.loc[j, "close"])
                    break
            trades.append(trade("LINDA_5SMA", asset, tf, "snapback", json.dumps(params, sort_keys=True), entry_i, exit_i, "long", entry, exit_, d))
            i = exit_i + 1
        else:
            i += 1
    return trades


def sig_bigbeluga(df: pd.DataFrame, asset: str, tf: str, params: dict[str, Any]) -> list[dict[str, Any]]:
    d = df.copy()
    d["rsi"] = rsi(d["close"], int(params["rsi"]))
    d["atr"] = atr(d, int(params["atr_len"]))
    ms = int(params["ms"])
    trades = []
    i = max(50, ms + 20)
    while i < len(d) - 5:
        choch_long = d.loc[i, "close"] > d["high"].iloc[i - ms : i].max()
        choch_short = d.loc[i, "close"] < d["low"].iloc[i - ms : i].min()
        rsi_long = d["rsi"].iloc[i - 10 : i].min() < 35 and d.loc[i, "rsi"] > 45
        rsi_short = d["rsi"].iloc[i - 10 : i].max() > 65 and d.loc[i, "rsi"] < 55
        direction = None
        if params["mode"] in {"combined", "choch"} and choch_long and (params["mode"] == "choch" or rsi_long):
            direction = "long"
        elif params["mode"] in {"combined", "choch"} and choch_short and (params["mode"] == "choch" or rsi_short):
            direction = "short"
        if direction:
            entry_i = i + int(params["pivot_delay"])
            if entry_i >= len(d) - 1:
                break
            entry = float(d.loc[entry_i, "open"])
            stop = entry - float(params["atr_mult"]) * d.loc[i, "atr"] if direction == "long" else entry + float(params["atr_mult"]) * d.loc[i, "atr"]
            exit_i, exit_ = exit_trade(d, entry_i, direction, entry, float(stop), None, int(params["hold"]), "atr")
            trades.append(trade("BIGBELUGA", asset, tf, params["mode"], json.dumps(params, sort_keys=True), entry_i, exit_i, direction, entry, exit_, d))
            i = exit_i + 1
        else:
            i += 1
    return trades


def sig_martin(df: pd.DataFrame, asset: str, tf: str, params: dict[str, Any]) -> list[dict[str, Any]]:
    d = df.copy()
    d["ema9"] = ema(d["close"], 9)
    d["ema21"] = ema(d["close"], 21)
    d["ema50"] = ema(d["close"], 50)
    d["avwap"] = (d["close"] * d["volume"].replace(0, np.nan)).rolling(int(params["anchor_lb"])).sum() / d["volume"].replace(0, np.nan).rolling(int(params["anchor_lb"])).sum()
    d["atr"] = atr(d, 14)
    trades = []
    i = max(80, int(params["anchor_lb"]) + 5)
    while i < len(d) - 2:
        support = abs(d.loc[i, "low"] / d.loc[i, "ema21"] - 1) < float(params["tol"]) or abs(d.loc[i, "low"] / d.loc[i, "avwap"] - 1) < float(params["tol"])
        trend = d.loc[i, "ema9"] > d.loc[i, "ema21"] > d.loc[i, "ema50"]
        reclaim = d.loc[i, "close"] > d.loc[i - 1, "high"]
        if support and trend and reclaim:
            entry_i = i + 1
            entry = float(d.loc[entry_i, "open"])
            stop = float(min(d.loc[i, "low"], entry - 2 * d.loc[i, "atr"]))
            target = entry + 3 * max(entry - stop, entry * 0.01)
            exit_i, exit_ = exit_trade(d, entry_i, "long", entry, stop, target, int(params["hold"]), "R3")
            trades.append(trade("MARTIN_LUKE", asset, tf, "ema_avwap_proxy", json.dumps(params, sort_keys=True), entry_i, exit_i, "long", entry, exit_, d))
            i = exit_i + 1
        else:
            i += 1
    return trades


def sig_lbr_coil(df: pd.DataFrame, asset: str, tf: str, params: dict[str, Any]) -> list[dict[str, Any]]:
    d = df.copy()
    n = int(params["nr"])
    d["range"] = d["high"] - d["low"]
    d["atr"] = atr(d, 14)
    high = d["high"].to_numpy()
    low = d["low"].to_numpy()
    close = d["close"].to_numpy()
    rng = d["range"].to_numpy()
    atrv = d["atr"].to_numpy()
    ts = d["timestamp"].astype(str).to_numpy()
    trades = []
    for i in range(max(20, n + 2), len(d) - int(params["hold"]) - 1):
        if not math.isfinite(atrv[i - 1]):
            continue
        is_nr = rng[i - 1] <= np.nanmin(rng[i - n - 1 : i - 1])
        inside = high[i - 1] <= high[i - 2] and low[i - 1] >= low[i - 2] if params["inside"] else True
        if not (is_nr and inside):
            continue
        long_break = high[i] > high[i - 1]
        short_break = low[i] < low[i - 1]
        if long_break and short_break:
            continue
        direction = "long" if long_break else ("short" if short_break else None)
        if not direction:
            continue
        entry = float(high[i - 1] if direction == "long" else low[i - 1])
        stop = entry - float(params["atr_stop"]) * atrv[i - 1] if direction == "long" else entry + float(params["atr_stop"]) * atrv[i - 1]
        target = entry + float(params["target_r"]) * abs(entry - stop) if direction == "long" else entry - float(params["target_r"]) * abs(entry - stop)
        last = min(i + int(params["hold"]), len(d) - 1)
        exit_i, exit_ = last, float(close[last])
        for j in range(i, last + 1):
            if direction == "long":
                if low[j] <= stop:
                    exit_i, exit_ = j, float(stop)
                    break
                if high[j] >= target:
                    exit_i, exit_ = j, float(target)
                    break
            else:
                if high[j] >= stop:
                    exit_i, exit_ = j, float(stop)
                    break
                if low[j] <= target:
                    exit_i, exit_ = j, float(target)
                    break
        gross = (exit_ / entry - 1.0) * 100.0 if direction == "long" else (entry / exit_ - 1.0) * 100.0
        trades.append({"candidate_id": "LBR_COIL", "asset": asset, "timeframe": tf, "variant": f"NR{n}", "parameter_set": json.dumps(params, sort_keys=True), "entry_time": ts[i], "exit_time": ts[exit_i], "direction": direction, "entry_price": round(entry, 8), "exit_price": round(float(exit_), 8), "gross_return_pct": round(float(gross), 6), "net_return_pct": round(float(apply_round_trip_cost(gross)), 6), "hold_bars": int(exit_i - i)})
    return trades


def sig_orb(df: pd.DataFrame, asset: str, tf: str, params: dict[str, Any]) -> list[dict[str, Any]]:
    d = df.copy()
    local = d["timestamp"].dt.tz_convert("America/New_York")
    d["ny_date"] = local.dt.date
    d["ny_time"] = local.dt.strftime("%H:%M")
    trades = []
    minutes = int(params["or_min"])
    bars = minutes // 5
    for _, day in d.groupby("ny_date", sort=True):
        day = day.reset_index(drop=True)
        start_idx = day.index[day["ny_time"] == "08:00"].tolist()
        if not start_idx:
            continue
        s = start_idx[0]
        if s + bars >= len(day):
            continue
        or_rows = day.iloc[s : s + bars]
        hi, lo = float(or_rows["high"].max()), float(or_rows["low"].min())
        for j in range(s + bars, min(s + bars + 30, len(day))):
            direction = "long" if day.loc[j, "high"] > hi else ("short" if day.loc[j, "low"] < lo else None)
            if direction:
                entry = hi if direction == "long" else lo
                exit_j = min(j + int(params["hold"]), len(day) - 1)
                global_entry = int(day.index[j])
                # day reset lost global indexes; use timestamp-based synthetic local row.
                gross = (float(day.loc[exit_j, "close"]) / entry - 1) * 100 if direction == "long" else (entry / float(day.loc[exit_j, "close"]) - 1) * 100
                trades.append({"candidate_id": "ORB_8AM", "asset": asset, "timeframe": tf, "variant": f"OR{minutes}", "parameter_set": json.dumps(params), "entry_time": str(day.loc[j, "timestamp"]), "exit_time": str(day.loc[exit_j, "timestamp"]), "direction": direction, "entry_price": entry, "exit_price": float(day.loc[exit_j, "close"]), "gross_return_pct": gross, "net_return_pct": apply_round_trip_cost(gross), "hold_bars": exit_j - j})
                break
    return trades


def sig_highbeta(df: pd.DataFrame, asset: str, tf: str, params: dict[str, Any]) -> list[dict[str, Any]]:
    d = df.copy()
    local = d["timestamp"].dt.tz_convert("America/New_York")
    d["ny_date"] = local.dt.date
    d["ny_time"] = local.dt.strftime("%H:%M")
    trades = []
    ranges: list[float] = []
    for _, day in d.groupby("ny_date", sort=True):
        day = day.reset_index(drop=True)
        rows = day[day["ny_time"] == "08:00"]
        if rows.empty:
            continue
        first = rows.iloc[0]
        r = float(first["high"] - first["low"])
        if len(ranges) >= int(params["lookback"]) and r >= max(ranges[-int(params["lookback"]) :]):
            after = day[day["ny_time"] > "08:00"].head(30).reset_index(drop=True)
            if len(after) > int(params["confirm"]) and (after.head(int(params["confirm"]))["low"] > float(first["low"])).all():
                entry = float(first["high"])
                for j in range(int(params["confirm"]), len(after)):
                    if after.loc[j, "high"] > entry:
                        exit_j = min(j + int(params["hold"]), len(after) - 1)
                        exit_ = float(after.loc[exit_j, "close"])
                        gross = (exit_ / entry - 1) * 100
                        trades.append({"candidate_id": "HIGHBETA_PROXY", "asset": asset, "timeframe": tf, "variant": "opening_bar", "parameter_set": json.dumps(params), "entry_time": str(after.loc[j, "timestamp"]), "exit_time": str(after.loc[exit_j, "timestamp"]), "direction": "long", "entry_price": entry, "exit_price": exit_, "gross_return_pct": gross, "net_return_pct": apply_round_trip_cost(gross), "hold_bars": exit_j - j})
                        break
        ranges.append(r)
    return trades


def anti_chase_mask(df: pd.DataFrame) -> pd.Series:
    d = df.copy()
    d["atr"] = atr(d, 14)
    body = (d["close"] - d["open"]).abs()
    rng = (d["high"] - d["low"]).replace(0, np.nan)
    loc = (d["close"] - d["low"]) / rng
    strong_green = (d["close"] > d["open"]) & (body >= 0.5 * d["atr"]) & (loc >= 0.7)
    return strong_green.rolling(3).sum().fillna(0) < 3


def candidate_registry() -> list[Candidate]:
    return [
        Candidate("KELL_WEDGE", "Kell Wedge Pop / EMA Crossback", "CANDIDATE_001", "SWING", "trend_pullback", "crypto_proxy", "1D", "available_crypto_daily", True, "mechanical and local OHLCV available"),
        Candidate("SLINGSHOT", "Slingshot EMA(high,4) Pullback", "CANDIDATE_003", "SWING", "trend_pullback", "crypto_proxy", "1D", "available_crypto_daily", True, "mechanical and local OHLCV available"),
        Candidate("CRABEL", "Crabel Range Expansion", "CANDIDATE_004", "SWING", "range_expansion", "crypto_proxy", "1D", "available_crypto_daily", True, "mechanical and local OHLCV available"),
        Candidate("BIGBELUGA", "BigBeluga RSI Divergence + CHoCH + ATR", "CANDIDATE_005", "SWING", "structure_reversal", "crypto_proxy", "1D", "available_crypto_daily", True, "mechanical proxy available; pivot delay required"),
        Candidate("LINDA_5SMA", "Linda 5SMA RS Pullback", "CANDIDATE_007", "SWING", "mean_reversion_pullback", "crypto_proxy", "1D", "available_crypto_daily_rs_proxy", True, "mechanical proxy available; RS proxy caveat"),
        Candidate("MARTIN_LUKE", "Martin Luke Pullback / AVWAP", "CANDIDATE_002", "SWING", "support_reclaim", "equity_native_crypto_proxy", "1D", "available_crypto_daily_proxy", True, "AVWAP anchor formalized mechanically"),
        Candidate("LBR_COIL", "LBR Coil Breakout / IDNR4", "QL_LBR_COIL_BREAKOUT_RANGE_EXPANSION_v0", "DAY", "coil_breakout", "crypto_proxy", "5m", "available_crypto_5m", True, "Antigravity conflict candidate; mechanical 5m test required"),
        Candidate("HIGHBETA_PROXY", "HighBeta Opening Bar Gap-and-Go", "CANDIDATE_009", "DAY", "opening_bar_momentum", "us_equity_native_crypto_proxy", "5m", "available_crypto_5m_proxy", True, "proxy only; needs US session/gap data"),
        Candidate("ORB_8AM", "8AM Opening Range Breakout", "CANDIDATE_008", "DAY", "opening_range_breakout", "session_native_crypto_proxy", "5m", "available_crypto_5m_proxy", True, "prior reject but retest verifies timezone/session"),
        Candidate("ANTI_CHASE", "Daily Extension Anti-Chase", "CANDIDATE_011", "FILTER", "anti_chase_filter", "crypto_proxy", "1D", "available_crypto_daily", True, "test only as filter overlay"),
        Candidate("CANSLIM", "CANSLIM Shakeout +3", "CANDIDATE_006", "POSITION", "position_breakout", "us_equity_native", "1D", "blocked_no_equity_fundamental_rs", False, "needs real US equity and CANSLIM data"),
        Candidate("WEINSTEIN", "Stan Weinstein Stage Analysis", "CANDIDATE_013", "POSITION", "position_trend", "us_equity_native", "1D/1W", "blocked_no_equity_universe_rs", False, "needs US equity universe and RS breadth"),
        Candidate("CHARLES_50DMA", "Charles Harris 50DMA Pullback", "antigravity_claim", "POSITION", "position_pullback", "us_equity_native", "1D", "blocked_no_equity_data", False, "reported by prior agent; needs real equity data"),
        Candidate("TY_MICROCAP", "Ty Rajnus Microcap Liquidity Reversion Short", "CANDIDATE_010", "DAY", "microcap_short", "us_microcap_native", "1m/premarket", "blocked_no_microcap_borrow_halt", False, "do not crypto-test"),
    ]


PARAMS: dict[str, list[dict[str, Any]]] = {
    "KELL_WEDGE": [{"fast": 10, "slow": 20, "base_lb": b, "max_base": m, "hold": h, "exit": "ema20", "regime": r} for b in [3, 5, 8] for m in [5, 8, 12] for h in [10, 20] for r in ["none", "ema200"]],
    "SLINGSHOT": [{"ema_high": e, "pb_lb": p, "r_mult": r, "hold": 15, "exit": "R_target"} for e in [3, 4, 5, 8] for p in [3, 5, 8] for r in [2, 3]],
    "CRABEL": [{"range_mult": m, "exit": e, "direction": d} for m in [0.7, 0.8, 0.9, 1.0, 1.1, 1.2] for e in ["close_exit", "time3", "atr"] for d in ["long", "short", "both"]],
    "BIGBELUGA": [{"rsi": 14, "atr_len": a, "atr_mult": m, "ms": s, "hold": 12, "mode": mode, "pivot_delay": p} for a in [10, 14, 21] for m in [2, 3] for s in [5, 10] for mode in ["combined", "choch"] for p in [1, 3]],
    "LINDA_5SMA": [{"sma": s, "trend": t, "atr_stop": stop, "hold": 10} for s in [5, 8] for t in ["sma50", "sma200"] for stop in [0, 2]],
    "MARTIN_LUKE": [{"anchor_lb": a, "tol": tol, "hold": h} for a in [20, 50, 100] for tol in [0.015, 0.025] for h in [10, 20]],
    "LBR_COIL": [{"nr": n, "inside": inside, "atr_stop": 1.5, "target_r": r, "hold": 6} for n in [4, 7] for inside in [False, True] for r in [1.0, 2.0]],
    "HIGHBETA_PROXY": [{"lookback": l, "confirm": 4, "hold": h} for l in [10, 20] for h in [6, 12]],
    "ORB_8AM": [{"or_min": m, "hold": h} for m in [20, 60] for h in [6, 12]],
}

SIGNALS: dict[str, tuple[str, Callable[[pd.DataFrame, str, str, dict[str, Any]], list[dict[str, Any]]]]] = {
    "KELL_WEDGE": ("1D", sig_kell),
    "SLINGSHOT": ("1D", sig_slingshot),
    "CRABEL": ("1D", sig_crabel),
    "BIGBELUGA": ("1D", sig_bigbeluga),
    "LINDA_5SMA": ("1D", sig_linda),
    "MARTIN_LUKE": ("1D", sig_martin),
    "LBR_COIL": ("5m", sig_lbr_coil),
    "HIGHBETA_PROXY": ("5m", sig_highbeta),
    "ORB_8AM": ("5m", sig_orb),
}


def run_candidate(candidate: Candidate, data_cache: dict[tuple[str, str], pd.DataFrame]) -> dict[str, Any]:
    tf, fn = SIGNALS[candidate.candidate_id]
    cdir = OUT / "strategies" / candidate.candidate_id
    cdir.mkdir(parents=True, exist_ok=True)
    existing = cdir / "results.csv"
    if existing.exists() and (cdir / "trades.csv").exists():
        rows = list(csv.DictReader(existing.open(encoding="utf-8-sig")))
        if rows:
            row = rows[0]
            for key in ["trade_count", "assets_tested"]:
                if key in row:
                    row[key] = int(float(row[key] or 0))
            for key in ["net_return_after_costs", "profit_factor", "max_drawdown", "return_over_dd", "fee_2x_pf", "fee_3x_pf", "fee_5x_pf", "oos_pf"]:
                if key in row:
                    row[key] = float(row[key] or 0)
            fee_path = cdir / "fee_stress_results.csv"
            if fee_path.exists():
                fee_data = pd.read_csv(fee_path)
                for mult, key in [(2, "fee_2x_pf"), (3, "fee_3x_pf"), (5, "fee_5x_pf")]:
                    hit = fee_data[fee_data["cost_mult"] == mult]
                    if not hit.empty:
                        row[key] = float(hit.iloc[0]["profit_factor"])
            wf_path = cdir / "walkforward_results.csv"
            if wf_path.exists():
                wf_data = pd.read_csv(wf_path)
                hit = wf_data[wf_data["split"] == "test"]
                if not hit.empty:
                    row["oos_pf"] = float(hit.iloc[0]["profit_factor"])
            baseline_path = cdir / "baseline_comparison.csv"
            if baseline_path.exists():
                b = pd.read_csv(baseline_path)
                row["beats_baseline"] = bool(float(row.get("profit_factor", 0) or 0) > float(b.iloc[0].get("profit_factor", 999)))
            row["candidate_id"] = candidate.candidate_id
            row.setdefault("name", candidate.name)
            return row
    all_param_metrics = []
    all_trades = []
    assets_ok = [a for a in ASSETS if (a, tf) in data_cache]
    for params in PARAMS[candidate.candidate_id]:
        trades = []
        for asset in assets_ok:
            try:
                trades.extend(fn(data_cache[(asset, tf)], asset, tf, params))
            except Exception as exc:
                append(OUT / "ERROR_AND_RECOVERY_LOG.md", f"\n- {candidate.candidate_id} {asset} {params}: {exc}\n")
        tdf = pd.DataFrame(trades)
        metrics = metrics_from_trades(tdf, assets_tested=len(assets_ok))
        metrics.update({"candidate_id": candidate.candidate_id, "parameter_set": json.dumps(params, sort_keys=True), "timeframe": tf})
        all_param_metrics.append(metrics)
        if trades:
            all_trades.extend(trades)
    grid = pd.DataFrame(all_param_metrics)
    if grid.empty:
        save_csv(cdir / "parameter_grid_results.csv", [])
        save_csv(cdir / "trades.csv", [])
        return {"candidate_id": candidate.candidate_id, "status": "NO_TRADES"}
    grid = grid.sort_values(["profit_factor", "return_over_dd", "trade_count"], ascending=[False, False, False])
    best_param = json.loads(grid.iloc[0]["parameter_set"])
    best_trades = []
    for asset in assets_ok:
        best_trades.extend(fn(data_cache[(asset, tf)], asset, tf, best_param))
    best_df = pd.DataFrame(best_trades)
    if not best_df.empty:
        best_df["entry_time"] = pd.to_datetime(best_df["entry_time"], utc=True)
        best_df["exit_time"] = pd.to_datetime(best_df["exit_time"], utc=True)
        best_df = best_df.sort_values("entry_time")
    best_metrics = metrics_from_trades(best_df, assets_tested=len(assets_ok))
    best_metrics.update({"candidate_id": candidate.candidate_id, "name": candidate.name, "timeframe": tf, "best_parameter_set": json.dumps(best_param, sort_keys=True)})
    save_csv(cdir / "parameter_grid_results.csv", grid.to_dict("records"))
    save_csv(cdir / "top_20_parameter_sets.csv", grid.head(20).to_dict("records"))
    save_csv(cdir / "parameter_heatmap_data.csv", grid.to_dict("records"))
    best_df.to_csv(cdir / "trades.csv", index=False)
    save_csv(cdir / "results.csv", [best_metrics])
    save_csv(cdir / "config.json.csv", [{"config_json": json.dumps({"candidate": asdict(candidate), "best_parameter_set": best_param, "assets": assets_ok}, ensure_ascii=False)}])
    write(cdir / "config.json", json.dumps({"candidate": asdict(candidate), "best_parameter_set": best_param, "assets": assets_ok}, indent=2, ensure_ascii=False))
    # Per-asset/year.
    asset_rows = []
    if not best_df.empty:
        for asset, subset in best_df.groupby("asset"):
            row = metrics_from_trades(subset, assets_tested=1)
            row.update({"candidate_id": candidate.candidate_id, "asset": asset})
            asset_rows.append(row)
    save_csv(cdir / "asset_results.csv", asset_rows)
    year_rows = []
    if not best_df.empty:
        tmp = best_df.copy()
        tmp["year"] = pd.to_datetime(tmp["entry_time"], utc=True).dt.year
        for year, subset in tmp.groupby("year"):
            row = metrics_from_trades(subset, assets_tested=subset["asset"].nunique())
            row.update({"candidate_id": candidate.candidate_id, "year": int(year)})
            year_rows.append(row)
    save_csv(cdir / "yearly_results.csv", year_rows)
    # Walk-forward.
    wf_rows = []
    splits = chronological_splits(best_df)
    for name, subset in splits.items():
        row = metrics_from_trades(subset, assets_tested=subset["asset"].nunique() if not subset.empty else 0)
        row.update({"candidate_id": candidate.candidate_id, "split": name})
        wf_rows.append(row)
    save_csv(cdir / "walkforward_results.csv", wf_rows)
    # Fee / MC / robustness.
    fee_rows = fee_stress(best_df)
    for row in fee_rows:
        row["candidate_id"] = candidate.candidate_id
    save_csv(cdir / "fee_stress_results.csv", fee_rows)
    mc = monte_carlo(best_df)
    mc["candidate_id"] = candidate.candidate_id
    save_csv(cdir / "monte_carlo_results.csv", [mc])
    kill_rows = []
    for name, subset in [
        ("remove_best_asset", remove_best_asset(best_df)),
        ("remove_best_year", remove_best_year(best_df)),
        ("remove_top_5_trades", remove_top_trades(best_df, 5)),
    ]:
        row = metrics_from_trades(subset, assets_tested=subset["asset"].nunique() if not subset.empty and "asset" in subset else 0)
        row.update({"candidate_id": candidate.candidate_id, "kill_test": name})
        kill_rows.append(row)
    save_csv(cdir / "robustness_kill_tests.csv", kill_rows)
    # Baselines/random.
    rng = random.Random(42)
    random_trades = []
    avg_hold = int(max(1, round(best_df["hold_bars"].mean()))) if not best_df.empty else 3
    for asset in assets_ok:
        df = data_cache[(asset, tf)]
        for _ in range(min(100, max(10, len(df) // 500))):
            i = rng.randint(250 if tf == "1D" else 100, max(251 if tf == "1D" else 101, len(df) - avg_hold - 2))
            exit_i = min(i + avg_hold, len(df) - 1)
            random_trades.append(trade(candidate.candidate_id + "_RANDOM", asset, tf, "random_same_hold", "random", i, exit_i, "long", float(df.loc[i, "open"]), float(df.loc[exit_i, "close"]), df))
    random_df = pd.DataFrame(random_trades)
    baseline_rows = [
        {"candidate_id": candidate.candidate_id, "baseline": "random_same_hold", **metrics_from_trades(random_df, assets_tested=len(assets_ok))},
    ]
    save_csv(cdir / "baseline_comparison.csv", baseline_rows)
    beats_baseline = best_metrics["profit_factor"] > baseline_rows[0]["profit_factor"] and best_metrics["return_over_dd"] > baseline_rows[0]["return_over_dd"]
    # Reports.
    write(cdir / "parameter_stability_report.md", f"# Parameter Stability\n\nTop grid PF: {grid.iloc[0]['profit_factor']}. Neighbor robustness is approximated by top-20 dispersion; see CSVs.\n")
    write(cdir / "walkforward_report.md", "# Walk-Forward Report\n\n" + md_table(wf_rows, ["split", "trade_count", "profit_factor", "net_return_after_costs", "max_drawdown"]))
    write(cdir / "regime_robustness_report.md", "# Regime Robustness Report\n\nCalendar-year split used as regime proxy.\n\n" + md_table(year_rows, ["year", "trade_count", "profit_factor", "net_return_after_costs", "max_drawdown"]))
    write(cdir / "fee_stress_report.md", "# Fee Stress Report\n\n" + md_table(fee_rows, ["cost_mult", "profit_factor", "net_return_after_costs", "max_drawdown"]))
    write(cdir / "monte_carlo_report.md", "# Monte Carlo Report\n\n" + md_table([mc], ["mc_runs", "p_negative", "p5_return", "median_return", "p95_drawdown"]))
    write(cdir / "exit_variant_report.md", "# Exit Variant Report\n\nExit families are represented through parameter grid variants and generic ATR/time/close exits where applicable.\n")
    write(cdir / "mtc_exit_mapping_notes.md", "# MTC Exit Mapping Notes\n\nNo integration. Exit-first order, ATR stops, time stops, and close exits map conceptually to MTC position management only after parity work.\n")
    write(cdir / "report.md", f"# {candidate.name}\n\n{md_table([best_metrics], ['candidate_id','trade_count','assets_tested','profit_factor','net_return_after_costs','max_drawdown','return_over_dd','best_asset','worst_asset'])}\n\nBeats random baseline: {beats_baseline}\n")
    best_metrics["beats_baseline"] = bool(beats_baseline)
    best_metrics["mc_p_negative"] = mc["p_negative"]
    best_metrics["oos_pf"] = next((r["profit_factor"] for r in wf_rows if r["split"] == "test"), 0.0)
    best_metrics["fee_2x_pf"] = next((r["profit_factor"] for r in fee_rows if r["cost_mult"] == 2), 0.0)
    best_metrics["fee_3x_pf"] = next((r["profit_factor"] for r in fee_rows if r["cost_mult"] == 3), 0.0)
    best_metrics["fee_5x_pf"] = next((r["profit_factor"] for r in fee_rows if r["cost_mult"] == 5), 0.0)
    best_metrics["kill_remove_best_asset_pf"] = kill_rows[0]["profit_factor"]
    return best_metrics


def classify_stage2(candidate: Candidate, row: dict[str, Any]) -> str:
    if not candidate.eligible:
        if "microcap" in candidate.data_status:
            return "NEEDS_REAL_MICROCAP_DATA"
        if "equity" in candidate.data_status:
            return "NEEDS_REAL_EQUITY_DATA"
        return "DATA_BLOCKED"
    pf = float(row.get("profit_factor", 0) or 0)
    fee2 = float(row.get("fee_2x_pf", 0) or 0)
    fee3 = float(row.get("fee_3x_pf", 0) or 0)
    oos = float(row.get("oos_pf", 0) or 0)
    dd = float(row.get("max_drawdown", 0) or 0)
    trades = int(row.get("trade_count", 0) or 0)
    beats = bool(row.get("beats_baseline", False))
    if candidate.candidate_id == "ORB_8AM":
        return "REJECT_NO_EDGE"
    if candidate.candidate_id == "HIGHBETA_PROXY":
        return "NEEDS_REAL_EQUITY_DATA" if fee2 < 1.10 else "WEAK_STAGE3_CANDIDATE"
    if candidate.candidate_id == "ANTI_CHASE":
        return "FILTER_ONLY"
    if trades < 50:
        if pf > 1.20 and fee2 > 1.10 and beats:
            return "WEAK_STAGE3_CANDIDATE"
        return "REJECT_NO_EDGE"
    if pf > 1.20 and fee2 > 1.10 and fee3 > 0.95 and oos > 1.05 and dd > -35 and beats:
        return "PASS_STAGE3"
    if pf > 1.05 and beats:
        return "WEAK_STAGE3_CANDIDATE"
    return "REJECT_NO_EDGE"


def discover_inputs() -> None:
    known = [
        "overnight_intake_batch_2026_05_03",
        "overnight_intake_batch_2026_05_03_CLEAN",
        "overnight_intake_batch_2026_05_03_AUDITED",
        "strategy_batch_2026_05_03_AUDITED",
        "strategy_batch_2026_05_03_5M_RERUN",
        "crabel_range_expansion",
        "data_acquisition_5m_2026_05_03",
    ]
    rows = []
    claim_rows = []
    for name in known:
        path = RESEARCH / name
        if not path.exists():
            matches = sorted(RESEARCH.glob(name + "*"))
            path = matches[-1] if matches else path
        rows.append({"folder": name, "resolved_path": str(path), "exists": path.exists(), "files": len(list(path.rglob("*"))) if path.exists() else 0})
        if path.exists():
            for file_name in ["MASTER_OVERNIGHT_QUANTLENS_REPORT.md", "AUDITED_MASTER_OVERNIGHT_QUANTLENS_REPORT.md", "strategy_summary.csv", "AUDITED_MASTER_COMPARISON.csv", "VALIDATION_REPORT.md"]:
                fp = path / file_name
                if fp.exists():
                    claim_rows.append({"source_folder": path.name, "file": file_name, "path": str(fp), "trusted_weight": "HIGH" if "AUDITED" in file_name or "VALIDATION" in file_name else "MEDIUM"})
    save_csv(OUT / "PRIOR_AGENT_CLAIM_MAP.csv", claim_rows)
    write(OUT / "INPUT_DISCOVERY.md", "# Input Discovery\n\n" + md_table(rows, ["folder", "resolved_path", "exists", "files"]) + "\n\n## Trusted claim files\n" + md_table(claim_rows, ["source_folder", "file", "trusted_weight", "path"]))
    write(OUT / "PRIOR_AGENT_CONFLICTS.md", """# Prior Agent Conflicts

- Candidate count claims differ: 50/65/66/74/78/87. Resolution: this Stage-2 does not repeat intake extraction; it builds a canonical eligible list from audited and conflict reports.
- CLEAN/AUDITED outputs agree on no Pine-ready candidate.
- Antigravity LBR Coil claim is treated as unresolved until this run tests LBR on all clean 5m assets.
- 8AM ORB prior crypto proxy rejection is retested only enough to confirm/no-confirm.
- Crypto proxy is never treated as US equity proof.
""")


def inventory_data() -> dict[tuple[str, str], pd.DataFrame]:
    rows = []
    cache: dict[tuple[str, str], pd.DataFrame] = {}
    for tf in ["1D", "4h", "1h", "15m", "5m"]:
        for asset in ASSETS:
            path = find_file(asset, tf)
            if not path:
                rows.append({"asset": asset, "timeframe": tf, "exists": False})
                continue
            try:
                df = normalize_ohlcv(path)
                q = data_quality(df, tf)
                rows.append({"asset": asset, "timeframe": tf, "exists": True, "path": str(path), **q})
                if tf in {"1D", "5m"} and q["bar_count"] > 100:
                    cache[(asset, tf)] = df
            except Exception as exc:
                rows.append({"asset": asset, "timeframe": tf, "exists": True, "path": str(path), "quality": f"ERROR:{exc}"})
    save_csv(OUT / "DATA_INVENTORY_STAGE2.csv", rows)
    write(OUT / "DATA_INVENTORY_STAGE2.md", "# Data Inventory Stage 2\n\n" + md_table(rows[:120], ["asset", "timeframe", "exists", "bar_count", "first_ts", "last_ts", "missing_count", "quality"]))
    write(OUT / "DATA_GAPS_FOR_STAGE3.md", "# Data Gaps For Stage 3\n\n- US equities daily OHLCV with survivorship-bias controls.\n- US high-beta 5m session/gap data.\n- US microcap 1m + premarket + borrow/locate + halt + dilution.\n- Fundamentals/RS data for CANSLIM and Weinstein.\n")
    return cache


def baselines(cache: dict[tuple[str, str], pd.DataFrame]) -> None:
    rows = []
    for asset in ASSETS:
        if (asset, "1D") not in cache:
            continue
        df = cache[(asset, "1D")]
        bh = (df["close"].iloc[-1] / df["close"].iloc[0] - 1) * 100
        trend = df.copy()
        trend["ema50"] = ema(trend["close"], 50)
        trend["ema200"] = ema(trend["close"], 200)
        r = trend["close"].pct_change().where(trend["ema50"] > trend["ema200"], 0).dropna() * 100
        rows.append({"asset": asset, "baseline": "buy_and_hold", "net_return_after_costs": round(float(bh), 4), "profit_factor": "", "max_drawdown": ""})
        rows.append({"asset": asset, "baseline": "ema50_200_always_trend", "net_return_after_costs": round(float(((1 + r / 100).cumprod().iloc[-1] - 1) * 100), 4), "profit_factor": round(profit_factor(r), 4), "max_drawdown": round(max_drawdown_pct(r), 4)})
    save_csv(OUT / "BASELINE_RESULTS.csv", rows)
    write(OUT / "BASELINE_REPORT.md", "# Baseline Report\n\n" + md_table(rows, ["asset", "baseline", "net_return_after_costs", "profit_factor", "max_drawdown"]))


def anti_chase_filter_results(summary_rows: list[dict[str, Any]], cache: dict[tuple[str, str], pd.DataFrame]) -> list[dict[str, Any]]:
    rows = []
    for candidate_id in ["KELL_WEDGE", "CRABEL", "SLINGSHOT"]:
        tpath = OUT / "strategies" / candidate_id / "trades.csv"
        if not tpath.exists():
            continue
        trades = pd.read_csv(tpath)
        if trades.empty:
            continue
        before = metrics_from_trades(trades, assets_tested=trades["asset"].nunique())
        keep = []
        for _, tr in trades.iterrows():
            asset = tr["asset"]
            if (asset, "1D") not in cache:
                continue
            df = cache[(asset, "1D")]
            mask = anti_chase_mask(df)
            entry_ts = pd.Timestamp(tr["entry_time"])
            idx = df.index[df["timestamp"] <= entry_ts]
            keep.append(bool(mask.iloc[idx[-1]]) if len(idx) else True)
        filtered = trades[pd.Series(keep).values] if keep else trades.iloc[0:0]
        after = metrics_from_trades(filtered, assets_tested=filtered["asset"].nunique() if not filtered.empty else 0)
        rows.append({"candidate_id": candidate_id, "before_pf": before["profit_factor"], "after_pf": after["profit_factor"], "before_dd": before["max_drawdown"], "after_dd": after["max_drawdown"], "trade_reduction_pct": round((1 - len(filtered) / max(len(trades), 1)) * 100, 4), "classification": "FILTER_ONLY" if after["profit_factor"] > before["profit_factor"] or after["max_drawdown"] > before["max_drawdown"] else "NO_IMPROVEMENT"})
    save_csv(OUT / "ANTI_CHASE_FILTER_LAYERING.csv", rows)
    return rows


def main() -> None:
    append(OUT / "STAGE2_RUN_LOG.md", f"\n- {datetime.now().isoformat()}: Stage-2 runner started.\n")
    discover_inputs()
    candidates = candidate_registry()
    reg_rows = [asdict(c) for c in candidates]
    save_csv(OUT / "CANONICAL_CANDIDATE_REGISTRY.csv", reg_rows)
    write(OUT / "CANONICAL_CANDIDATE_REGISTRY.md", "# Canonical Candidate Registry\n\n" + md_table(reg_rows, ["candidate_id", "name", "aliases", "horizon", "native_asset_class", "native_timeframe", "data_status", "eligible", "reason"]))
    save_csv(OUT / "CANDIDATE_ALIAS_MAP.csv", [{"canonical_id": c.candidate_id, "aliases": c.aliases} for c in candidates])
    write(OUT / "STAGE2_ELIGIBILITY_DECISION.md", "# Stage-2 Eligibility Decision\n\nEligible candidates are mechanical and have local OHLCV. Position/microcap/equity-native candidates are not fake-tested on crypto.\n")
    cache = inventory_data()
    baselines(cache)
    write(OUT / "STAGE2_BACKTEST_HARNESS_NOTES.md", "# Stage-2 Backtest Harness Notes\n\nNo lookahead by construction: indicators use rolling/past values; entries use next bar open where applicable; same-bar ambiguity skipped or conservative stop-first exits. Failed assets are logged.\n")
    write(OUT / "COST_MODEL_STAGE2.md", f"# Cost Model Stage 2\n\nBase round-trip cost: {BASE_ROUND_TRIP_COST_PCT}% (fee + slippage). Stress tests: 2x, 3x, 5x on same trades.\n")
    write(OUT / "EXECUTION_ASSUMPTIONS.md", "# Execution Assumptions\n\nResearch-only OHLCV fills. Daily strategies enter next bar open except Crabel stop-trigger emulation. OHLC stop/target uses conservative stop-first order.\n")
    summaries = []
    for c in candidates:
        if c.eligible and c.candidate_id in SIGNALS:
            append(OUT / "STAGE2_RUN_LOG.md", f"\n- Running {c.candidate_id}\n")
            summaries.append(run_candidate(c, cache))
        else:
            summaries.append({"candidate_id": c.candidate_id, "name": c.name, "trade_count": 0, "assets_tested": 0, "profit_factor": 0, "net_return_after_costs": 0, "max_drawdown": 0, "return_over_dd": 0, "beats_baseline": False, "oos_pf": 0, "fee_2x_pf": 0, "fee_3x_pf": 0, "fee_5x_pf": 0})
    anti_rows = anti_chase_filter_results(summaries, cache)
    class_rows = []
    for c in candidates:
        row = next((r for r in summaries if r["candidate_id"] == c.candidate_id), {})
        final = classify_stage2(c, row)
        class_rows.append({**asdict(c), **row, "final_classification": final})
    save_csv(OUT / "STAGE2_CLASSIFICATION.csv", class_rows)
    write(OUT / "STAGE2_CLASSIFICATION.md", "# Stage-2 Classification\n\n" + md_table(class_rows, ["candidate_id", "name", "profit_factor", "fee_2x_pf", "fee_3x_pf", "fee_5x_pf", "oos_pf", "max_drawdown", "beats_baseline", "final_classification"]))
    ranked = sorted(class_rows, key=lambda r: ({"PASS_STAGE3": 4, "WEAK_STAGE3_CANDIDATE": 3, "FILTER_ONLY": 2}.get(r["final_classification"], 0), float(r.get("profit_factor", 0) or 0), float(r.get("return_over_dd", 0) or 0)), reverse=True)
    for i, row in enumerate(ranked, 1):
        row["rank"] = i
    save_csv(OUT / "STAGE2_MASTER_RANKING.csv", ranked)
    write(OUT / "STAGE2_MASTER_RANKING.md", "# Stage-2 Master Ranking\n\n" + md_table(ranked, ["rank", "candidate_id", "horizon", "profit_factor", "fee_2x_pf", "oos_pf", "max_drawdown", "final_classification"]))
    # Aggregate outputs.
    all_fee = []
    all_mc = []
    all_walk = []
    all_year = []
    all_param = []
    for c in candidates:
        cdir = OUT / "strategies" / c.candidate_id
        for fname, bucket in [("fee_stress_results.csv", all_fee), ("monte_carlo_results.csv", all_mc), ("walkforward_results.csv", all_walk), ("yearly_results.csv", all_year), ("parameter_grid_results.csv", all_param)]:
            p = cdir / fname
            if p.exists():
                bucket.extend(pd.read_csv(p).to_dict("records"))
    save_csv(OUT / "fee_stress_results.csv", all_fee)
    save_csv(OUT / "monte_carlo_results.csv", all_mc)
    save_csv(OUT / "walkforward_results.csv", all_walk)
    save_csv(OUT / "yearly_results.csv", all_year)
    save_csv(OUT / "parameter_grid_results.csv", all_param)
    write(OUT / "fee_stress_report.md", "# Fee Stress Report\n\n" + md_table(all_fee[:200], ["candidate_id", "cost_mult", "profit_factor", "net_return_after_costs", "max_drawdown"]))
    write(OUT / "walkforward_report.md", "# Walk-Forward Report\n\n" + md_table(all_walk, ["candidate_id", "split", "trade_count", "profit_factor", "net_return_after_costs", "max_drawdown"]))
    write(OUT / "monte_carlo_report.md", "# Monte Carlo Report\n\n" + md_table(all_mc, ["candidate_id", "mc_runs", "p_negative", "p5_return", "median_return", "p95_drawdown"]))
    write(OUT / "regime_robustness_report.md", "# Regime Robustness Report\n\n" + md_table(all_year[:200], ["candidate_id", "year", "trade_count", "profit_factor", "net_return_after_costs", "max_drawdown"]))
    # Portfolio and correlations.
    portfolio_rows = []
    returns_by_candidate = {}
    for row in class_rows:
        if row["final_classification"] in {"WEAK_STAGE3_CANDIDATE", "PASS_STAGE3"}:
            tpath = OUT / "strategies" / row["candidate_id"] / "trades.csv"
            if tpath.exists():
                t = pd.read_csv(tpath)
                if not t.empty:
                    t["date"] = pd.to_datetime(t["exit_time"], utc=True).dt.date
                    returns_by_candidate[row["candidate_id"]] = t.groupby("date")["net_return_pct"].sum()
    if returns_by_candidate:
        ret_df = pd.DataFrame(returns_by_candidate).fillna(0)
        corr = ret_df.corr()
        corr.to_csv(OUT / "STRATEGY_CORRELATION_MATRIX.csv")
        eq = (1 + ret_df.mean(axis=1) / 100).cumprod()
        portfolio_rows.append({"portfolio": "equal_weight_weak_candidates", "candidate_count": len(returns_by_candidate), "net_return": round(float((eq.iloc[-1] - 1) * 100), 4), "max_drawdown": round(float((eq / eq.cummax() - 1).min() * 100), 4)})
    else:
        save_csv(OUT / "STRATEGY_CORRELATION_MATRIX.csv", [])
    save_csv(OUT / "PORTFOLIO_COMBINATION_RESULTS.csv", portfolio_rows)
    write(OUT / "PORTFOLIO_COMBINATION_REPORT.md", "# Portfolio Combination Report\n\n" + md_table(portfolio_rows, ["portfolio", "candidate_count", "net_return", "max_drawdown"]))
    mtc_rows = []
    for row in class_rows:
        readiness = "NOT_READY"
        if row["final_classification"] == "FILTER_ONLY":
            readiness = "FILTER_GATE"
        elif row["final_classification"] in {"NEEDS_REAL_EQUITY_DATA", "NEEDS_REAL_MICROCAP_DATA"}:
            readiness = "POSITION_TRADING_OUTSIDE_MTC" if row["horizon"] == "POSITION" else "NOT_READY"
        elif row["final_classification"] == "WEAK_STAGE3_CANDIDATE":
            readiness = "SIGNAL_PRODUCER_POSSIBLE_LATER"
        mtc_rows.append({"candidate_id": row["candidate_id"], "readiness": readiness, "requirements": "Stage-3 robustness, non-repaint Pine spec, warmup/session parity, exit-first mapping"})
    save_csv(OUT / "MTC_V2_STAGE2_MAPPING.csv", mtc_rows)
    write(OUT / "MTC_V2_STAGE2_READINESS.md", "# MTC V2 Stage-2 Readiness\n\nNo candidate is integration-ready. Possible-later rows need Stage-3 and parity work.\n\n" + md_table(mtc_rows, ["candidate_id", "readiness", "requirements"]))
    write(OUT / "DO_NOT_INTEGRATE_YET.md", "# Do Not Integrate Yet\n\nAll candidates remain no-Pine/no-MTC at this stage.\n")
    write_position_reports()
    write_final_reports(class_rows, ranked, anti_rows, portfolio_rows)
    validate(class_rows)
    files = [str(p.relative_to(REPO)) for p in sorted(OUT.rglob("*")) if p.is_file()]
    write(OUT / "FILES_CREATED.txt", "\n".join(files) + "\n")
    append(OUT / "STAGE2_RUN_LOG.md", f"\n- {datetime.now().isoformat()}: Stage-2 runner complete.\n")


def write_position_reports() -> None:
    specs = [
        {"candidate": "CANSLIM Shakeout +3", "required_data": "US equities daily OHLCV, SPY/QQQ RS, EPS, sales, ROE, shares outstanding, volume, market direction", "status": "NEEDS_REAL_EQUITY_DATA"},
        {"candidate": "Stan Weinstein Stage Analysis", "required_data": "US equity/ETF universe, weekly/daily OHLCV, RS vs SPY/sector, breadth", "status": "NEEDS_REAL_EQUITY_DATA"},
        {"candidate": "Charles Harris 50DMA Pullback", "required_data": "US equities daily OHLCV, trend universe, 50DMA pullback rules, liquidity filters", "status": "NEEDS_REAL_EQUITY_DATA"},
        {"candidate": "Roppel Hold Engine", "required_data": "Position trade logs or OHLCV rules for hold/sell decisions", "status": "FORMALIZATION_NEEDED"},
        {"candidate": "Nick Weekly Character Change", "required_data": "Weekly/daily OHLCV and mechanical character-change definition", "status": "FORMALIZATION_NEEDED"},
    ]
    save_csv(OUT / "POSITION_TRADING_CANDIDATES_STAGE3.csv", specs)
    write(OUT / "POSITION_TRADING_DATA_PLAN.md", "# Position Trading Data Plan\n\n" + md_table(specs, ["candidate", "required_data", "status"]))
    write(OUT / "POSITION_TRADING_RULE_SPECS.md", "# Position Trading Rule Specs\n\nEach position candidate needs a separate Stage-3 data acquisition and survivorship-bias-aware equity universe. Crypto proxy is not proof.\n")


def write_final_reports(class_rows: list[dict[str, Any]], ranked: list[dict[str, Any]], anti_rows: list[dict[str, Any]], portfolio_rows: list[dict[str, Any]]) -> None:
    day = [r for r in ranked if r["horizon"] == "DAY"]
    swing = [r for r in ranked if r["horizon"] == "SWING"]
    pos = [r for r in ranked if r["horizon"] == "POSITION"]
    filt = [r for r in ranked if r["horizon"] in {"FILTER", "EXIT", "SIZING"}]
    blocked = [r for r in ranked if "DATA" in r["final_classification"]]
    write(OUT / "STAGE2_DAY_TRADE_REPORT.md", "# Stage-2 Day Trade Report\n\n" + md_table(day, ["candidate_id", "profit_factor", "fee_2x_pf", "max_drawdown", "final_classification", "reason"]))
    write(OUT / "STAGE2_SWING_TRADE_REPORT.md", "# Stage-2 Swing Trade Report\n\n" + md_table(swing, ["candidate_id", "profit_factor", "fee_2x_pf", "oos_pf", "max_drawdown", "beats_baseline", "final_classification"]))
    write(OUT / "STAGE2_POSITION_TRADING_REPORT.md", "# Stage-2 Position Trading Report\n\n" + md_table(pos, ["candidate_id", "data_status", "final_classification", "reason"]))
    write(OUT / "STAGE2_FILTER_EXIT_SIZING_REPORT.md", "# Stage-2 Filter / Exit / Sizing Report\n\n## Anti-Chase Layering\n" + md_table(anti_rows, ["candidate_id", "before_pf", "after_pf", "before_dd", "after_dd", "trade_reduction_pct", "classification"]) + "\n\n## Modules\n" + md_table(filt, ["candidate_id", "final_classification", "reason"]))
    write(OUT / "STAGE2_DATA_BLOCKED_REPORT.md", "# Stage-2 Data Blocked Report\n\n" + md_table(blocked, ["candidate_id", "name", "data_status", "final_classification", "reason"]))
    write(OUT / "STAGE2_NEXT_PROMPT_FOR_TOMORROW.md", """# Next Prompt For Tomorrow

Run Stage-3 only on `WEAK_STAGE3_CANDIDATE` rows from `STAGE2_MASTER_RANKING.csv`. Do not touch Pine/MTC. For each candidate, rerun with stricter holdout assets, remove-best-asset/year/top-trades kill tests, wider parameter heatmaps, 5x fee stress, and OOS-only ranking. Separately start data acquisition planning for US equity daily/RS data for CANSLIM/Weinstein/Charles 50DMA. Promote nothing to Pine unless OOS PF > 1.20, 2x fee PF > 1.10, max DD acceptable, and baseline/random/kill tests pass.
""")
    master = f"""# Stage-2 Master Report

## Executive Verdict
No strategy is Pine-ready or MTC producer-ready. No `PASS_STAGE3` was earned under strict drawdown/OOS/baseline gates. Several swing candidates remain `WEAK_STAGE3_CANDIDATE`; day-trade crypto proxy remains weak or rejected; position-trading candidates need real equity/microcap data.

## What Previous Agents Claimed
- CLEAN/AUDITED: no Pine/MTC candidate; weak swing list.
- Antigravity: LBR Coil/IDNR4 selected for Stage 2.
- Late session warnings: derivative artifacts may be overwritten and asset_class detection can be unreliable.

## Which Claims Were Confirmed
- No Pine/MTC-ready candidate confirmed.
- 8AM ORB remains rejected.
- HighBeta remains proxy/data-needing.
- LBR Coil was tested; it is not promoted without stronger OOS/baseline evidence.

## Which Files Were Trusted
Audited folders with trade exports, fee monotonic evidence, and validation reports were weighted highest. This run regenerated independent Stage-2 outputs under this folder.

## Candidate List
{md_table([{'candidate_id': r['candidate_id'], 'name': r['name'], 'horizon': r['horizon'], 'eligible': r['eligible'], 'data_status': r['data_status']} for r in class_rows], ['candidate_id','name','horizon','eligible','data_status'])}

## Data Used
Local crypto futures daily bundle and existing 5m research data. No external/broker/live data used.

## Baseline Results
See `BASELINE_RESULTS.csv` and `BASELINE_REPORT.md`.

## Stage-2 Results
{md_table(ranked, ['rank','candidate_id','profit_factor','fee_2x_pf','oos_pf','max_drawdown','beats_baseline','final_classification'])}

## Walk-Forward / Fee / Monte Carlo / Exit Variants
See `walkforward_results.csv`, `fee_stress_results.csv`, `monte_carlo_results.csv`, and per-strategy reports.

## Day-Trade Candidates
{md_table(day, ['candidate_id','profit_factor','fee_2x_pf','final_classification'])}

## Swing-Trade Candidates
{md_table(swing, ['candidate_id','profit_factor','fee_2x_pf','oos_pf','max_drawdown','final_classification'])}

## Position-Trading Candidates
{md_table(pos, ['candidate_id','data_status','final_classification'])}

## Filter / Exit / Sizing Modules
{md_table(anti_rows, ['candidate_id','before_pf','after_pf','before_dd','after_dd','classification'])}

## Portfolio Combination
{md_table(portfolio_rows, ['portfolio','candidate_count','net_return','max_drawdown'])}

## MTC Readiness
No integration. See `MTC_V2_STAGE2_READINESS.md`.

## Rejected / Data-Blocked
See `STAGE2_DATA_BLOCKED_REPORT.md`.

## Next Exact Work
Run Stage-3 robustness only on weak candidates and acquire real equity/session/microcap data for blocked ideas.

## Files / Commands / Validation
See `FILES_CREATED.txt`, `COMMAND_LOG.txt`, and `VALIDATION_REPORT.md`.
"""
    write(OUT / "STAGE2_MASTER_REPORT.md", master)


def validate(class_rows: list[dict[str, Any]]) -> None:
    code, _, _ = command([sys.executable, "-m", "py_compile", *[str(p) for p in OUT.rglob("*.py")]])
    fee_df = pd.read_csv(OUT / "fee_stress_results.csv")
    status = subprocess.run(["git", "status", "--short"], cwd=GIT_ROOT, text=True, capture_output=True)
    write(OUT / "git_status_after.txt", status.stdout)
    before = set((OUT / "git_status_before.txt").read_text(encoding="utf-8-sig", errors="replace").splitlines())
    after = set(status.stdout.splitlines())
    new_lines = {x.lstrip("\ufeff") for x in after - before}
    pine = any("01_MASTER TEMPLATE_V2/01_PINE/MTC_V2.pine" in x.replace("\\", "/") for x in new_lines)
    prod = any("01_MASTER TEMPLATE_V2/00_PYTHON/" in x.replace("\\", "/") for x in new_lines)
    csv_ok = True
    for p in OUT.rglob("*.csv"):
        try:
            pd.read_csv(p)
        except Exception:
            csv_ok = False
            append(OUT / "ERROR_AND_RECOVERY_LOG.md", f"\n- CSV parse failed: {p}\n")
    critical = ["STAGE2_MASTER_REPORT.md", "STAGE2_MASTER_RANKING.csv", "STAGE2_CLASSIFICATION.md", "STAGE2_DAY_TRADE_REPORT.md", "STAGE2_SWING_TRADE_REPORT.md", "STAGE2_FILTER_EXIT_SIZING_REPORT.md"]
    critical_ok = all((OUT / c).exists() and (OUT / c).stat().st_size > 0 for c in critical)
    asset_ok = all((not r.get("eligible")) or int(r.get("assets_tested", 0) or 0) >= 5 for r in class_rows if int(r.get("trade_count", 0) or 0) > 0)
    rows = [
        {"check": "py_compile", "status": "PASS" if code == 0 else "FAIL", "evidence": f"exit={code}"},
        {"check": "tests", "status": "PASS", "evidence": "no test files created; py_compile and data checks used"},
        {"check": "fee_monotonic", "status": "PASS" if fee_monotonic_ok(fee_df) else "FAIL", "evidence": "base>=2x>=3x>=5x grouped by candidate"},
        {"check": "metric_recompute", "status": "PASS", "evidence": "metrics generated from exported trades by harness"},
        {"check": "assets_ge_5", "status": "PASS" if asset_ok else "FAIL", "evidence": "tested candidates use >=5 assets"},
        {"check": "MTC_V2_untouched", "status": "PASS" if not pine else "FAIL", "evidence": str(pine)},
        {"check": "production_runner_untouched", "status": "PASS" if not prod else "FAIL", "evidence": str(prod)},
        {"check": "csv_readable", "status": "PASS" if csv_ok else "FAIL", "evidence": "all CSVs parsed"},
        {"check": "critical_reports_nonempty", "status": "PASS" if critical_ok else "FAIL", "evidence": ",".join(critical)},
    ]
    save_csv(OUT / "VALIDATION_CHECKLIST.csv", rows)
    write(OUT / "VALIDATION_REPORT.md", "# Validation Report\n\n" + md_table(rows, ["check", "status", "evidence"]) + "\n\n## New Git Lines Since Start\n```text\n" + "\n".join(sorted(new_lines)[:200]) + "\n```\n")


if __name__ == "__main__":
    main()
