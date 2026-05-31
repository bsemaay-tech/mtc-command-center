import argparse
import csv
import hashlib
import itertools
import json
import math
import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd


DEFAULT_SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "AVAXUSDT", "DOGEUSDT"]
DEFAULT_TIMEFRAMES = ["15m", "1h", "4h"]
BASE_CANDIDATES = {
    "QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK": "ema_pullback",
    "QL_2026-05-01_US_EQUITIES_INTRADAY_LE_MODEL_BULL_FLAG": "ema_pullback",
    "QL_2026-05-01_US_EQUITIES_INTRADAY_PURPLE_PROFITS": "ema_pullback",
    "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL": "ema_exit_module",
    "QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNEL_PULLBACK": "multi_ema_channel",
    "QL_2026-05-01_LIQUID_INTRADAY_VWAP_PULLBACK_REVERSAL": "vwap_proxy",
    "QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PLAYBOOK": "rsi_sma_pullback",
    "QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR": "two_candle_sr",
    "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK": "dual_rsi_mtf",
    "QL_2026-05-01_ANY_BOLLINGER_BANDS_20_2_TRI_SETUP": "bb_squeeze_breakout",
    "QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE": "engulfing_sr",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_line(path: Path, line: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line.rstrip() + "\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload["datasets"])


def select_datasets(manifest: list[dict[str, Any]], symbols: list[str], timeframes: list[str]) -> list[dict[str, Any]]:
    selected_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    wanted_symbols = set(symbols)
    wanted_timeframes = set(timeframes)
    for item in manifest:
        if item.get("symbol") not in wanted_symbols:
            continue
        if item.get("timeframe_normalized") not in wanted_timeframes:
            continue
        if item.get("ohlcv_validation_status") != "PASS":
            continue
        key = (str(item["symbol"]), str(item["timeframe_normalized"]))
        previous = selected_by_key.get(key)
        if previous is None or int(item.get("row_count", 0)) > int(previous.get("row_count", 0)):
            selected_by_key[key] = item
    selected = list(selected_by_key.values())
    selected.sort(key=lambda item: (symbols.index(item["symbol"]), timeframes.index(item["timeframe_normalized"])))
    return selected


def read_ohlc(bundle_root: Path, item: dict[str, Any], verify_sha: bool) -> pd.DataFrame:
    path = bundle_root / item["normalized_path"]
    if verify_sha:
        actual = sha256_file(path)
        expected = item.get("sha256_normalized")
        if expected and actual != expected:
            raise ValueError(f"sha256 mismatch dataset_id={item['dataset_id']} expected={expected} actual={actual}")
    df = pd.read_csv(path)
    df = df.rename(columns={"timestamp_utc": "timestamp"})
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    for col in ["open", "high", "low", "close"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["timestamp", "open", "high", "low", "close"]).sort_values("timestamp").reset_index(drop=True)
    return df


def ema(series: pd.Series, length: int) -> pd.Series:
    return series.ewm(span=length, adjust=False, min_periods=length).mean()


def sma(series: pd.Series, length: int) -> pd.Series:
    return series.rolling(length, min_periods=length).mean()


def rsi(series: pd.Series, length: int) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / length, adjust=False, min_periods=length).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / length, adjust=False, min_periods=length).mean()
    rs = gain / loss.replace(0, math.nan)
    return 100 - (100 / (1 + rs))


def atr(df: pd.DataFrame, length: int) -> pd.Series:
    prev_close = df["close"].shift(1)
    tr = pd.concat(
        [
            df["high"] - df["low"],
            (df["high"] - prev_close).abs(),
            (df["low"] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return tr.ewm(alpha=1 / length, adjust=False, min_periods=length).mean()


def add_common_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for length in [5, 8, 13, 20, 50, 100, 200]:
        out[f"ema_{length}"] = ema(out["close"], length)
        out[f"sma_{length}"] = sma(out["close"], length)
    for length in [7, 14]:
        out[f"rsi_{length}"] = rsi(out["close"], length)
    out["atr_14"] = atr(out, 14)
    out["bb_mid_20"] = sma(out["close"], 20)
    out["bb_std_20"] = out["close"].rolling(20, min_periods=20).std()
    out["bb_upper_20_2"] = out["bb_mid_20"] + 2 * out["bb_std_20"]
    out["bb_lower_20_2"] = out["bb_mid_20"] - 2 * out["bb_std_20"]
    out["bb_width_pct"] = (out["bb_upper_20_2"] - out["bb_lower_20_2"]) / out["bb_mid_20"]
    out["typical"] = (out["high"] + out["low"] + out["close"]) / 3
    return out


def build_daily_rsi_map(bundle_root: Path, manifest: list[dict[str, Any]], symbols: list[str], verify_sha: bool) -> dict[str, pd.DataFrame]:
    daily = {}
    by_symbol = {item["symbol"]: item for item in manifest if item.get("timeframe_normalized") == "1D" and item.get("symbol") in symbols}
    for symbol, item in by_symbol.items():
        df = read_ohlc(bundle_root, item, verify_sha)
        df["date"] = df["timestamp"].dt.floor("D")
        for length in [7, 14]:
            df[f"daily_rsi_{length}"] = rsi(df["close"], length).shift(1)
        daily[symbol] = df[["date", "daily_rsi_7", "daily_rsi_14"]].copy()
    return daily


def trade_stats(trades: list[dict[str, Any]], initial_equity: float = 1.0) -> dict[str, Any]:
    if not trades:
        return {
            "trades": 0,
            "net_return_pct": 0.0,
            "profit_factor": 0.0,
            "max_drawdown_pct": 0.0,
            "win_rate": 0.0,
            "avg_trade_pct": 0.0,
            "long_trades": 0,
            "short_trades": 0,
        }
    equity = initial_equity
    curve = [equity]
    gross_profit = 0.0
    gross_loss = 0.0
    wins = 0
    long_trades = 0
    short_trades = 0
    returns = []
    for trade in trades:
        ret = float(trade["return_pct"])
        returns.append(ret)
        equity *= 1 + ret
        curve.append(equity)
        if ret > 0:
            wins += 1
            gross_profit += ret
        else:
            gross_loss += abs(ret)
        if trade["side"] == "long":
            long_trades += 1
        else:
            short_trades += 1
    peak = curve[0]
    max_dd = 0.0
    for value in curve:
        peak = max(peak, value)
        if peak > 0:
            max_dd = min(max_dd, value / peak - 1)
    return {
        "trades": len(trades),
        "net_return_pct": (equity / initial_equity - 1) * 100,
        "profit_factor": gross_profit / gross_loss if gross_loss > 0 else (999.0 if gross_profit > 0 else 0.0),
        "max_drawdown_pct": max_dd * 100,
        "win_rate": wins / len(trades) * 100,
        "avg_trade_pct": sum(returns) / len(returns) * 100,
        "long_trades": long_trades,
        "short_trades": short_trades,
    }


def backtest_fixed_r(
    df: pd.DataFrame,
    long_signal: pd.Series,
    short_signal: pd.Series,
    stop_long: pd.Series,
    stop_short: pd.Series,
    rr: float,
    max_hold: int,
    cost_bps_round_trip: float,
    exit_long_signal: pd.Series | None = None,
    exit_short_signal: pd.Series | None = None,
) -> list[dict[str, Any]]:
    trades: list[dict[str, Any]] = []
    index = 0
    cost = cost_bps_round_trip / 10000
    last_entry = len(df) - 2
    while index < last_entry:
        side = None
        if bool(long_signal.iloc[index]):
            side = "long"
        elif bool(short_signal.iloc[index]):
            side = "short"
        if side is None:
            index += 1
            continue
        entry_index = index + 1
        entry = float(df["open"].iloc[entry_index])
        if not math.isfinite(entry) or entry <= 0:
            index += 1
            continue
        if side == "long":
            stop = float(stop_long.iloc[index])
            if not math.isfinite(stop) or stop >= entry:
                index += 1
                continue
            risk = entry - stop
            target = entry + rr * risk
        else:
            stop = float(stop_short.iloc[index])
            if not math.isfinite(stop) or stop <= entry:
                index += 1
                continue
            risk = stop - entry
            target = entry - rr * risk
        exit_index = min(entry_index + max_hold, len(df) - 1)
        exit_price = float(df["close"].iloc[exit_index])
        reason = "max_hold"
        for cursor in range(entry_index, exit_index + 1):
            high = float(df["high"].iloc[cursor])
            low = float(df["low"].iloc[cursor])
            if side == "long":
                if low <= stop:
                    exit_index = cursor
                    exit_price = stop
                    reason = "stop"
                    break
                if high >= target:
                    exit_index = cursor
                    exit_price = target
                    reason = "target"
                    break
                if exit_long_signal is not None and cursor > entry_index and bool(exit_long_signal.iloc[cursor]):
                    exit_index = min(cursor + 1, len(df) - 1)
                    exit_price = float(df["open"].iloc[exit_index])
                    reason = "signal_exit"
                    break
            else:
                if high >= stop:
                    exit_index = cursor
                    exit_price = stop
                    reason = "stop"
                    break
                if low <= target:
                    exit_index = cursor
                    exit_price = target
                    reason = "target"
                    break
                if exit_short_signal is not None and cursor > entry_index and bool(exit_short_signal.iloc[cursor]):
                    exit_index = min(cursor + 1, len(df) - 1)
                    exit_price = float(df["open"].iloc[exit_index])
                    reason = "signal_exit"
                    break
        raw_return = (exit_price / entry - 1) if side == "long" else (entry / exit_price - 1)
        trades.append(
            {
                "side": side,
                "entry_time": str(df["timestamp"].iloc[entry_index]),
                "exit_time": str(df["timestamp"].iloc[exit_index]),
                "entry": entry,
                "exit": exit_price,
                "return_pct": raw_return - cost,
                "raw_return_pct": raw_return,
                "reason": reason,
                "bars_held": exit_index - entry_index,
            }
        )
        index = max(exit_index + 1, index + 1)
    return trades


def signals_for(strategy: str, df: pd.DataFrame, params: dict[str, Any], daily: pd.DataFrame | None = None) -> tuple[pd.Series, pd.Series, pd.Series, pd.Series, pd.Series | None, pd.Series | None]:
    close = df["close"]
    false = pd.Series(False, index=df.index)
    if strategy in {"ema_pullback", "ema_exit_module"}:
        ema_len = int(params.get("ema_len", 8))
        slope_len = int(params.get("slope_len", 3))
        pullback_atr = float(params.get("pullback_atr", 0.35))
        impulse_atr = float(params.get("impulse_atr", 1.0))
        ema_col = f"ema_{ema_len}" if f"ema_{ema_len}" in df else "ema_8"
        ema_line = df[ema_col]
        slope = ema_line - ema_line.shift(slope_len)
        dist = (close - ema_line).abs() / df["atr_14"]
        impulse = (close - close.shift(slope_len)).abs() / df["atr_14"]
        long_signal = (close > ema_line) & (slope > 0) & (dist <= pullback_atr) & (impulse.shift(1) >= impulse_atr)
        short_signal = (close < ema_line) & (slope < 0) & (dist <= pullback_atr) & (impulse.shift(1) >= impulse_atr)
        stop_long = df["low"].rolling(int(params.get("stop_lookback", 3)), min_periods=1).min()
        stop_short = df["high"].rolling(int(params.get("stop_lookback", 3)), min_periods=1).max()
        exit_long = close < ema_line
        exit_short = close > ema_line
        return long_signal, short_signal, stop_long, stop_short, exit_long, exit_short
    if strategy == "multi_ema_channel":
        fast = ema(close, int(params.get("fast", 5)))
        mid = ema(close, int(params.get("mid", 13)))
        slow = ema(close, int(params.get("slow", 200)))
        touch_atr = float(params.get("touch_atr", 0.4))
        long_signal = (close > slow) & (fast > mid) & ((close - mid).abs() / df["atr_14"] <= touch_atr) & (close > close.shift(1))
        short_signal = (close < slow) & (fast < mid) & ((close - mid).abs() / df["atr_14"] <= touch_atr) & (close < close.shift(1))
        stop_long = df["low"].rolling(int(params.get("stop_lookback", 5)), min_periods=1).min()
        stop_short = df["high"].rolling(int(params.get("stop_lookback", 5)), min_periods=1).max()
        return long_signal, short_signal, stop_long, stop_short, close < mid, close > mid
    if strategy == "rsi_sma_pullback":
        rsi_len = int(params.get("rsi_len", 14))
        sma_len = int(params.get("sma_len", 50))
        r = df[f"rsi_{rsi_len}"]
        ma = df[f"sma_{sma_len}"]
        long_signal = (close > ma) & (r.shift(1) < 50) & (r >= 50)
        short_signal = (close < ma) & (r.shift(1) > 50) & (r <= 50)
        stop_long = df["low"].rolling(int(params.get("stop_lookback", 5)), min_periods=1).min()
        stop_short = df["high"].rolling(int(params.get("stop_lookback", 5)), min_periods=1).max()
        return long_signal, short_signal, stop_long, stop_short, close < ma, close > ma
    if strategy == "dual_rsi_mtf":
        if daily is None:
            return false, false, close * math.nan, close * math.nan, None, None
        frame = df.copy()
        frame["date"] = frame["timestamp"].dt.floor("D")
        frame = frame.merge(daily, on="date", how="left")
        rsi_len = int(params.get("rsi_len", 7))
        daily_col = f"daily_rsi_{rsi_len}"
        r = frame[f"rsi_{rsi_len}"]
        hi = float(params.get("daily_hi", 60))
        lo = float(params.get("daily_lo", 40))
        long_signal = (frame[daily_col] > hi) & (r.shift(1) < lo) & (r >= lo)
        short_signal = (frame[daily_col] < lo) & (r.shift(1) > hi) & (r <= hi)
        stop_long = df["low"].rolling(int(params.get("stop_lookback", 10)), min_periods=1).min()
        stop_short = df["high"].rolling(int(params.get("stop_lookback", 10)), min_periods=1).max()
        return long_signal, short_signal, stop_long, stop_short, None, None
    if strategy == "bb_squeeze_breakout":
        width_q = int(params.get("width_quantile_window", 200))
        threshold = float(params.get("width_quantile", 0.25))
        width_limit = df["bb_width_pct"].rolling(width_q, min_periods=width_q).quantile(threshold)
        narrow = df["bb_width_pct"] <= width_limit
        body = (df["close"] - df["open"]).abs()
        body_ok = body >= float(params.get("body_atr", 0.25)) * df["atr_14"]
        long_signal = narrow.shift(1) & (close > df["bb_upper_20_2"]) & body_ok
        short_signal = narrow.shift(1) & (close < df["bb_lower_20_2"]) & body_ok
        stop_long = df["low"].rolling(int(params.get("stop_lookback", 5)), min_periods=1).min()
        stop_short = df["high"].rolling(int(params.get("stop_lookback", 5)), min_periods=1).max()
        return long_signal, short_signal, stop_long, stop_short, close < df["bb_mid_20"], close > df["bb_mid_20"]
    if strategy == "two_candle_sr":
        high_break = df["high"].rolling(int(params.get("level_lookback", 48)), min_periods=10).max().shift(1)
        low_break = df["low"].rolling(int(params.get("level_lookback", 48)), min_periods=10).min().shift(1)
        candle_range = (df["high"] - df["low"]).replace(0, math.nan)
        close_pos = (df["close"] - df["low"]) / candle_range
        strong_bull = (close_pos >= float(params.get("upper_third", 0.66))) & (df["close"] > df["high"].shift(1))
        strong_bear = (close_pos <= float(params.get("lower_third", 0.34))) & (df["close"] < df["low"].shift(1))
        long_signal = strong_bull & (df["close"] > high_break)
        short_signal = strong_bear & (df["close"] < low_break)
        stop_long = df["low"].rolling(int(params.get("stop_lookback", 2)), min_periods=1).min()
        stop_short = df["high"].rolling(int(params.get("stop_lookback", 2)), min_periods=1).max()
        return long_signal, short_signal, stop_long, stop_short, strong_bear, strong_bull
    if strategy == "engulfing_sr":
        level_lookback = int(params.get("level_lookback", 96))
        tolerance_atr = float(params.get("tolerance_atr", 0.4))
        support = df["low"].rolling(level_lookback, min_periods=20).min().shift(1)
        resistance = df["high"].rolling(level_lookback, min_periods=20).max().shift(1)
        body_low = pd.concat([df["open"], df["close"]], axis=1).min(axis=1)
        body_high = pd.concat([df["open"], df["close"]], axis=1).max(axis=1)
        prev_body_low = body_low.shift(1)
        prev_body_high = body_high.shift(1)
        bullish_engulf = (df["close"] > df["open"]) & (body_low <= prev_body_low) & (body_high >= prev_body_high)
        bearish_engulf = (df["close"] < df["open"]) & (body_low <= prev_body_low) & (body_high >= prev_body_high)
        near_support = ((df["low"] - support).abs() / df["atr_14"]) <= tolerance_atr
        near_resistance = ((df["high"] - resistance).abs() / df["atr_14"]) <= tolerance_atr
        long_signal = bullish_engulf & near_support
        short_signal = bearish_engulf & near_resistance
        stop_long = df["low"] - float(params.get("buffer_atr", 0.1)) * df["atr_14"]
        stop_short = df["high"] + float(params.get("buffer_atr", 0.1)) * df["atr_14"]
        return long_signal, short_signal, stop_long, stop_short, None, None
    if strategy == "vwap_proxy":
        session_window = int(params.get("session_window", 96))
        proxy = df["typical"].rolling(session_window, min_periods=session_window).mean()
        band = df["typical"].rolling(session_window, min_periods=session_window).std()
        slope = proxy - proxy.shift(int(params.get("slope_len", 4)))
        proximity = (close - proxy).abs() / df["atr_14"]
        long_signal = (slope > 0) & (close > proxy) & (proximity <= float(params.get("prox_atr", 0.4)))
        short_signal = (slope < 0) & (close < proxy) & (proximity <= float(params.get("prox_atr", 0.4)))
        stop_long = proxy - float(params.get("band_mult", 1.0)) * band
        stop_short = proxy + float(params.get("band_mult", 1.0)) * band
        return long_signal, short_signal, stop_long, stop_short, close < proxy, close > proxy
    return false, false, close * math.nan, close * math.nan, None, None


def parameter_grid(strategy: str) -> list[dict[str, Any]]:
    if strategy in {"ema_pullback", "ema_exit_module"}:
        keys = ["pullback_atr", "impulse_atr", "stop_lookback", "rr", "max_hold"]
        vals = [[0.25, 0.5, 0.75], [0.5, 1.0, 1.5], [2, 3, 5], [1.25, 1.5, 2.0, 2.5], [24, 48, 96]]
    elif strategy == "multi_ema_channel":
        keys = ["touch_atr", "stop_lookback", "rr", "max_hold"]
        vals = [[0.25, 0.5, 0.75], [3, 5, 8], [1.5, 2.0, 2.5], [48, 96, 160]]
    elif strategy == "rsi_sma_pullback":
        keys = ["rsi_len", "sma_len", "stop_lookback", "rr", "max_hold"]
        vals = [[7, 14], [50, 100, 200], [3, 5, 10], [1.5, 2.0, 2.5], [48, 96, 160]]
    elif strategy == "dual_rsi_mtf":
        keys = ["rsi_len", "daily_hi", "daily_lo", "stop_lookback", "rr", "max_hold"]
        vals = [[7, 14], [55, 60], [40, 45], [5, 10, 20], [1.5, 2.0, 2.5], [48, 96, 160]]
    elif strategy == "bb_squeeze_breakout":
        keys = ["width_quantile", "body_atr", "stop_lookback", "rr", "max_hold"]
        vals = [[0.15, 0.25, 0.35], [0.15, 0.25, 0.4], [3, 5, 10], [1.5, 2.0, 2.5], [48, 96, 160]]
    elif strategy == "two_candle_sr":
        keys = ["level_lookback", "upper_third", "lower_third", "stop_lookback", "rr", "max_hold"]
        vals = [[32, 48, 96], [0.6, 0.66, 0.75], [0.25, 0.34, 0.4], [2, 3, 5], [1.25, 1.5, 2.0], [24, 48, 96]]
    elif strategy == "engulfing_sr":
        keys = ["level_lookback", "tolerance_atr", "buffer_atr", "rr", "max_hold"]
        vals = [[48, 96, 160], [0.25, 0.5, 0.75], [0.05, 0.1, 0.2], [1.5, 2.0, 2.5], [48, 96, 160]]
    elif strategy == "vwap_proxy":
        keys = ["session_window", "prox_atr", "band_mult", "rr", "max_hold"]
        vals = [[48, 96, 192], [0.25, 0.5, 0.75], [0.75, 1.0, 1.5], [1.25, 1.5, 2.0], [24, 48, 96]]
    else:
        keys, vals = ["rr"], [[2.0]]
    return [dict(zip(keys, combo)) for combo in itertools.product(*vals)]


def score_result(row: dict[str, Any]) -> float:
    trades = int(row["trades"])
    if trades < 30:
        return -9999 + trades
    pf = min(float(row["profit_factor"]), 5.0)
    net = float(row["net_return_pct"])
    dd = abs(float(row["max_drawdown_pct"]))
    win = float(row["win_rate"])
    return net * 0.35 + pf * 20 + win * 0.15 - dd * 1.5 + min(trades, 500) * 0.02


def evaluate_one(
    candidate_id: str,
    strategy: str,
    dataset: dict[str, Any],
    df: pd.DataFrame,
    params: dict[str, Any],
    daily: pd.DataFrame | None,
    cost_bps_round_trip: float,
) -> dict[str, Any]:
    long_signal, short_signal, stop_long, stop_short, exit_long, exit_short = signals_for(strategy, df, params, daily)
    trades = backtest_fixed_r(
        df,
        long_signal.fillna(False),
        short_signal.fillna(False),
        stop_long,
        stop_short,
        rr=float(params.get("rr", 2.0)),
        max_hold=int(params.get("max_hold", 96)),
        cost_bps_round_trip=cost_bps_round_trip,
        exit_long_signal=exit_long,
        exit_short_signal=exit_short,
    )
    stats = trade_stats(trades)
    row = {
        "candidate_id": candidate_id,
        "strategy": strategy,
        "symbol": dataset["symbol"],
        "timeframe": dataset["timeframe_normalized"],
        "dataset_id": dataset["dataset_id"],
        "source_type": dataset["source_type"],
        "params_json": json.dumps(params, sort_keys=True, separators=(",", ":")),
        **stats,
    }
    row["score"] = score_result(row)
    return row


def write_csv_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        if not exists:
            writer.writeheader()
        writer.writerows(rows)


def build_rollup(all_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    for row in all_rows:
        key = (row["candidate_id"], row["strategy"], row["params_json"])
        grouped.setdefault(key, []).append(row)
    out = []
    for (candidate_id, strategy, params_json), rows in grouped.items():
        symbols = sorted({r["symbol"] for r in rows})
        timeframes = sorted({r["timeframe"] for r in rows})
        total_trades = sum(int(r["trades"]) for r in rows)
        avg_net = sum(float(r["net_return_pct"]) for r in rows) / len(rows)
        avg_pf = sum(float(r["profit_factor"]) for r in rows) / len(rows)
        worst_dd = min(float(r["max_drawdown_pct"]) for r in rows)
        avg_score = sum(float(r["score"]) for r in rows) / len(rows)
        positive = sum(1 for r in rows if float(r["net_return_pct"]) > 0)
        coverage = len(symbols) * len(timeframes)
        robust = coverage >= 8 and total_trades >= 200 and positive / len(rows) >= 0.55 and avg_pf >= 1.05 and worst_dd > -45
        out.append(
            {
                "candidate_id": candidate_id,
                "strategy": strategy,
                "params_json": params_json,
                "evaluations": len(rows),
                "symbols": "|".join(symbols),
                "timeframes": "|".join(timeframes),
                "total_trades": total_trades,
                "avg_net_return_pct": avg_net,
                "avg_profit_factor": avg_pf,
                "worst_max_drawdown_pct": worst_dd,
                "positive_evaluations": positive,
                "coverage_cells": coverage,
                "robust_promising": robust,
                "score": avg_score + (10 if robust else 0),
            }
        )
    out.sort(key=lambda row: float(row["score"]), reverse=True)
    return out


def write_markdown_summary(out_root: Path, rollup: list[dict[str, Any]], status: dict[str, Any]) -> None:
    path = out_root / "reports/OVERNIGHT_RESEARCH_SUMMARY.md"
    lines = [
        "# QuantLens Overnight Research Summary",
        "",
        f"- Generated at: `{utc_now()}`",
        f"- Status: `{status.get('status')}`",
        f"- Completed evaluations: `{status.get('completed_evaluations')}`",
        f"- Failed evaluations: `{status.get('failed_evaluations')}`",
        f"- Output root: `{out_root}`",
        "",
        "## Top Research Candidates",
    ]
    if not rollup:
        lines.append("- No completed evaluations yet.")
    for row in rollup[:20]:
        lines.append(
            f"- `{row['candidate_id']}` / `{row['strategy']}` score `{float(row['score']):.2f}` "
            f"avg_net `{float(row['avg_net_return_pct']):.2f}%` avg_pf `{float(row['avg_profit_factor']):.2f}` "
            f"worst_dd `{float(row['worst_max_drawdown_pct']):.2f}%` trades `{row['total_trades']}` "
            f"coverage `{row['coverage_cells']}` promising `{row['robust_promising']}` params `{row['params_json']}`"
        )
    lines.extend(
        [
            "",
            "## Guardrails",
            "- Research-only outputs; no Pine or production Python runner behavior was changed.",
            "- Data source is manifest-first Binance futures OHLC from the local optimization bundle.",
            "- US equities, options, SP500, 5m, and true volume VWAP claims are not validated by these crypto-adapted tests.",
            "- A profitable row is not production approval; require parity and forward/OOS checks before promotion.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=r"C:\LAB\tradingview-lab\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\manifests\dataset_manifest.json")
    parser.add_argument("--out", default="06_QUANTLENS_LAB/05_BACKTEST_RESULTS/overnight_research_20260501")
    parser.add_argument("--time-budget-minutes", type=int, default=480)
    parser.add_argument("--symbols", default=",".join(DEFAULT_SYMBOLS))
    parser.add_argument("--timeframes", default=",".join(DEFAULT_TIMEFRAMES))
    parser.add_argument("--cost-bps-round-trip", type=float, default=8.0)
    parser.add_argument("--max-params-per-strategy", type=int, default=1000000)
    parser.add_argument("--verify-sha", action="store_true")
    parser.add_argument("--no-verify-sha", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest_path = Path(args.manifest)
    bundle_root = manifest_path.parents[1]
    out_root = Path(args.out)
    if args.smoke:
        out_root = out_root / "smoke"
        args.time_budget_minutes = min(args.time_budget_minutes, 5)
        args.max_params_per_strategy = min(args.max_params_per_strategy, 2)
        args.symbols = "BTCUSDT,ETHUSDT"
        args.timeframes = "1h"
    symbols = [item.strip() for item in args.symbols.split(",") if item.strip()]
    timeframes = [item.strip() for item in args.timeframes.split(",") if item.strip()]
    verify_sha = args.verify_sha and not args.no_verify_sha
    deadline = datetime.now(timezone.utc) + timedelta(minutes=args.time_budget_minutes)
    out_root.mkdir(parents=True, exist_ok=True)
    status_path = out_root / "detached/run_status.json"
    heartbeat_path = out_root / "heartbeat/heartbeat.log"
    evaluations_path = out_root / "results/all_evaluations.csv"
    rollup_path = out_root / "ranked/candidate_rollup.csv"
    failures_path = out_root / "failures/failed_evaluations.jsonl"
    manifest = load_manifest(manifest_path)
    selected = select_datasets(manifest, symbols, timeframes)
    daily_maps = build_daily_rsi_map(bundle_root, manifest, symbols, verify_sha)
    write_json(out_root / "datasets/selected_datasets.json", {"manifest": str(manifest_path), "datasets": selected})
    status = {
        "status": "running",
        "started_at": utc_now(),
        "pid": os.getpid(),
        "manifest": str(manifest_path),
        "out": str(out_root),
        "symbols": symbols,
        "timeframes": timeframes,
        "selected_dataset_count": len(selected),
        "cost_bps_round_trip": args.cost_bps_round_trip,
        "completed_evaluations": 0,
        "failed_evaluations": 0,
        "time_budget_minutes": args.time_budget_minutes,
    }
    write_json(status_path, status)
    append_line(heartbeat_path, f"{utc_now()} started pid={os.getpid()} selected_datasets={len(selected)}")
    data_cache: dict[str, pd.DataFrame] = {}
    all_rows: list[dict[str, Any]] = []
    completed = 0
    failed = 0
    last_flush = time.time()
    done_planning = True
    try:
        for dataset in selected:
            if datetime.now(timezone.utc) >= deadline:
                done_planning = False
                break
            df = data_cache.get(dataset["dataset_id"])
            if df is None:
                df = add_common_indicators(read_ohlc(bundle_root, dataset, verify_sha))
                data_cache[dataset["dataset_id"]] = df
            for candidate_id, strategy in BASE_CANDIDATES.items():
                if datetime.now(timezone.utc) >= deadline:
                    done_planning = False
                    break
                if strategy == "dual_rsi_mtf" and dataset["timeframe_normalized"] != "1h":
                    continue
                grid = parameter_grid(strategy)[: args.max_params_per_strategy]
                for params in grid:
                    if datetime.now(timezone.utc) >= deadline:
                        done_planning = False
                        break
                    try:
                        row = evaluate_one(
                            candidate_id,
                            strategy,
                            dataset,
                            df,
                            params,
                            daily_maps.get(dataset["symbol"]),
                            args.cost_bps_round_trip,
                        )
                        all_rows.append(row)
                        completed += 1
                    except Exception as exc:
                        failed += 1
                        append_line(
                            failures_path,
                            json.dumps(
                                {
                                    "at": utc_now(),
                                    "candidate_id": candidate_id,
                                    "strategy": strategy,
                                    "dataset_id": dataset["dataset_id"],
                                    "params": params,
                                    "error": str(exc),
                                },
                                sort_keys=True,
                            ),
                        )
                    if len(all_rows) >= 500:
                        write_csv_rows(evaluations_path, all_rows)
                        all_rows.clear()
                    if time.time() - last_flush > 60:
                        status.update(
                            {
                                "status": "running",
                                "updated_at": utc_now(),
                                "completed_evaluations": completed,
                                "failed_evaluations": failed,
                            }
                        )
                        write_json(status_path, status)
                        append_line(heartbeat_path, f"{utc_now()} running completed={completed} failed={failed}")
                        last_flush = time.time()
                if not done_planning:
                    break
            if not done_planning:
                break
        if all_rows:
            write_csv_rows(evaluations_path, all_rows)
            all_rows.clear()
        if evaluations_path.exists():
            evals = pd.read_csv(evaluations_path)
            rollup = build_rollup(evals.to_dict("records"))
            write_csv_rows(rollup_path, rollup)
        else:
            rollup = []
        final_status = {
            **status,
            "status": "completed" if done_planning else "time_budget_reached",
            "ended_at": utc_now(),
            "completed_evaluations": completed,
            "failed_evaluations": failed,
            "time_budget_reached": not done_planning,
            "evaluations_path": str(evaluations_path),
            "rollup_path": str(rollup_path),
            "summary_path": str(out_root / "reports/OVERNIGHT_RESEARCH_SUMMARY.md"),
        }
        write_json(status_path, final_status)
        append_line(heartbeat_path, f"{utc_now()} {final_status['status']} completed={completed} failed={failed}")
        write_markdown_summary(out_root, rollup, final_status)
        return 0
    except Exception as exc:
        status.update({"status": "failed", "ended_at": utc_now(), "error": str(exc), "completed_evaluations": completed, "failed_evaluations": failed})
        write_json(status_path, status)
        append_line(heartbeat_path, f"{utc_now()} failed error={exc}")
        raise


if __name__ == "__main__":
    raise SystemExit(main())
