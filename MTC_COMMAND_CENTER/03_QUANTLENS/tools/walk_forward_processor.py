import math
import os
import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timezone

# -------------------------------------------------------------
# DEFINE TIME INTERVALS FOR OOS SPLIT
# -------------------------------------------------------------
TRAIN_END_DATE = datetime(2024, 6, 1, tzinfo=timezone.utc)
COST_BPS = 8.0

# -------------------------------------------------------------
# STRATEGY GRIDS
# -------------------------------------------------------------
GRIDS = {
    "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK": [
        {"rsi_len": 7, "daily_hi": 60.0, "daily_lo": 40.0, "stop_lookback": 10},
        {"rsi_len": 14, "daily_hi": 55.0, "daily_lo": 45.0, "stop_lookback": 5}
    ],
    "QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK": [
        {"pullback_atr": 0.25, "impulse_atr": 0.5},
        {"pullback_atr": 0.35, "impulse_atr": 1.0},
        {"pullback_atr": 0.5, "impulse_atr": 1.5}
    ],
    "QL_2026-05-01_US_EQUITIES_INTRADAY_LE_MODEL_BULL_FLAG": [
        {"pullback_atr": 0.25, "impulse_atr": 0.5},
        {"pullback_atr": 0.35, "impulse_atr": 1.0},
        {"pullback_atr": 0.5, "impulse_atr": 1.5}
    ],
    "QL_2026-05-01_US_EQUITIES_INTRADAY_PURPLE_PROFITS": [
        {"pullback_atr": 0.25, "impulse_atr": 0.5},
        {"pullback_atr": 0.35, "impulse_atr": 1.0},
        {"pullback_atr": 0.5, "impulse_atr": 1.5}
    ],
    "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL": [
        {"pullback_atr": 0.25, "impulse_atr": 0.5},
        {"pullback_atr": 0.35, "impulse_atr": 1.0}
    ],
    "QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNEL_PULLBACK": [
        {"touch_atr": 0.25},
        {"touch_atr": 0.4},
        {"touch_atr": 0.6}
    ],
    "QL_2026-05-01_LIQUID_INTRADAY_VWAP_PULLBACK_REVERSAL": [
        {"session_window": 48, "prox_atr": 0.25},
        {"session_window": 96, "prox_atr": 0.4}
    ],
    "QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PLAYBOOK": [
        {"rsi_len": 7, "sma_len": 50},
        {"rsi_len": 14, "sma_len": 100},
        {"rsi_len": 14, "sma_len": 50}
    ],
    "QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR": [
        {"level_lookback": 32, "upper_third": 0.6},
        {"level_lookback": 48, "upper_third": 0.66}
    ],
    "QL_2026-05-01_ANY_BOLLINGER_BANDS_20_2_TRI_SETUP": [
        {"width_quantile": 0.15, "body_atr": 0.15},
        {"width_quantile": 0.25, "body_atr": 0.25}
    ],
    "QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE": [
        {"level_lookback": 48, "tolerance_atr": 0.25},
        {"level_lookback": 96, "tolerance_atr": 0.4}
    ]
}

# -------------------------------------------------------------
# CORE INDICATORS HELPERS
# -------------------------------------------------------------
def ema(series: pd.Series, length: int) -> pd.Series:
    return series.ewm(span=length, adjust=False, min_periods=length).mean()

def sma(series: pd.Series, length: int) -> pd.Series:
    return series.rolling(length, min_periods=length).mean()

def rsi(series: pd.Series, length: int) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).ewm(alpha=1/length, adjust=False, min_periods=length).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1/length, adjust=False, min_periods=length).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))

def atr(df: pd.DataFrame, length: int) -> pd.Series:
    prev_close = df["close"].shift(1)
    tr = pd.concat([
        df["high"] - df["low"],
        (df["high"] - prev_close).abs(),
        (df["low"] - prev_close).abs()
    ], axis=1).max(axis=1)
    return tr.ewm(alpha=1/length, adjust=False, min_periods=length).mean()

# -------------------------------------------------------------
# STRATEGY SIGNAL DETECTORS
# -------------------------------------------------------------
def get_strategy_signals(strategy: str, df: pd.DataFrame, params: dict, daily_rsi_map: dict = None) -> tuple[pd.Series, pd.Series]:
    close = df["close"]
    high = df["high"]
    low = df["low"]
    
    # Calculate common components if missing
    if "atr_14" not in df:
        df["atr_14"] = atr(df, 14)
    if "ema_8" not in df:
        df["ema_8"] = ema(close, 8)
    if "ema_5" not in df:
        df["ema_5"] = ema(close, 5)
    if "ema_13" not in df:
        df["ema_13"] = ema(close, 13)
    if "ema_200" not in df:
        df["ema_200"] = ema(close, 200)
        
    if strategy == "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK":
        if daily_rsi_map is None:
            return pd.Series(False, index=df.index), pd.Series(np.nan, index=df.index)
        df["daily_rsi"] = df["date"].map(daily_rsi_map)
        df["rsi_1h"] = rsi(close, int(params.get("rsi_len", 7)))
        
        # Dual RSI triggers
        long_signal = (df["daily_rsi"] > params.get("daily_hi", 60.0)) & (df["rsi_1h"].shift(1) < params.get("daily_lo", 40.0)) & (df["rsi_1h"] >= params.get("daily_lo", 40.0))
        stop_long = low.rolling(int(params.get("stop_lookback", 10)), min_periods=1).min()
        return long_signal, stop_long
        
    elif strategy in {"QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK", 
                    "QL_2026-05-01_US_EQUITIES_INTRADAY_LE_MODEL_BULL_FLAG", 
                    "QL_2026-05-01_US_EQUITIES_INTRADAY_PURPLE_PROFITS",
                    "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL"}:
        slope = df["ema_8"] - df["ema_8"].shift(3)
        dist = (close - df["ema_8"]).abs() / df["atr_14"]
        impulse = (close - close.shift(3)).abs() / df["atr_14"]
        
        long_signal = (close > df["ema_8"]) & (slope > 0) & (dist <= params.get("pullback_atr", 0.35)) & (impulse.shift(1) >= params.get("impulse_atr", 1.0))
        stop_long = low.rolling(3, min_periods=1).min()
        return long_signal, stop_long
        
    elif strategy == "QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNEL_PULLBACK":
        dist = (close - df["ema_13"]).abs() / df["atr_14"]
        long_signal = (close > df["ema_200"]) & (df["ema_5"] > df["ema_13"]) & (dist <= params.get("touch_atr", 0.4)) & (close > df["open"])
        stop_long = low.rolling(5, min_periods=1).min()
        return long_signal, stop_long
        
    elif strategy == "QL_2026-05-01_LIQUID_INTRADAY_VWAP_PULLBACK_REVERSAL":
        win = int(params.get("session_window", 96))
        proxy = df["close"].rolling(win, min_periods=win).mean()
        band = df["close"].rolling(win, min_periods=win).std()
        slope = proxy - proxy.shift(4)
        proximity = (close - proxy).abs() / df["atr_14"]
        long_signal = (slope > 0) & (close > proxy) & (proximity <= params.get("prox_atr", 0.4))
        stop_long = proxy - 1.0 * band
        return long_signal, stop_long
        
    elif strategy == "QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PLAYBOOK":
        rsi_len = int(params.get("rsi_len", 14))
        sma_len = int(params.get("sma_len", 50))
        df[f"sma_{sma_len}"] = sma(close, sma_len)
        df[f"rsi_{rsi_len}"] = rsi(close, rsi_len)
        long_signal = (close > df[f"sma_{sma_len}"]) & (df[f"rsi_{rsi_len}"].shift(1) < 50) & (df[f"rsi_{rsi_len}"] >= 50)
        stop_long = low.rolling(5, min_periods=1).min()
        return long_signal, stop_long
        
    elif strategy == "QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR":
        win = int(params.get("level_lookback", 48))
        high_break = high.rolling(win, min_periods=10).max().shift(1)
        candle_range = (high - low).replace(0, np.nan)
        close_pos = (close - low) / candle_range
        strong_bull = (close_pos >= params.get("upper_third", 0.66)) & (close > high.shift(1))
        long_signal = strong_bull & (close > high_break)
        stop_long = low.rolling(2, min_periods=1).min()
        return long_signal, stop_long
        
    elif strategy == "QL_2026-05-01_ANY_BOLLINGER_BANDS_20_2_TRI_SETUP":
        bb_mid = sma(close, 20)
        bb_std = close.rolling(20, min_periods=20).std()
        bb_upper = bb_mid + 2 * bb_std
        bb_width_pct = (2 * 2 * bb_std) / bb_mid
        width_limit = bb_width_pct.rolling(200, min_periods=200).quantile(params.get("width_quantile", 0.25))
        narrow = bb_width_pct <= width_limit
        body_ok = (close - df["open"]).abs() >= params.get("body_atr", 0.25) * df["atr_14"]
        
        long_signal = narrow.shift(1) & (close > bb_upper) & body_ok
        stop_long = low.rolling(5, min_periods=1).min()
        return long_signal, stop_long
        
    elif strategy == "QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE":
        win = int(params.get("level_lookback", 96))
        support = low.rolling(win, min_periods=20).min().shift(1)
        body_low = pd.concat([df["open"], close], axis=1).min(axis=1)
        body_high = pd.concat([df["open"], close], axis=1).max(axis=1)
        prev_body_low = body_low.shift(1)
        prev_body_high = body_high.shift(1)
        bullish_engulf = (close > df["open"]) & (body_low <= prev_body_low) & (body_high >= prev_body_high)
        near_support = ((low - support).abs() / df["atr_14"]) <= params.get("tolerance_atr", 0.4)
        
        long_signal = bullish_engulf & near_support
        stop_long = low - 0.1 * df["atr_14"]
        return long_signal, stop_long
        
    return pd.Series(False, index=df.index), pd.Series(np.nan, index=df.index)

# -------------------------------------------------------------
# CORE SIMULATION
# -------------------------------------------------------------
def simulate_trades(df: pd.DataFrame, long_signal: pd.Series, stop_long: pd.Series, strategy: str, is_train: bool) -> float:
    # Filter by date
    if is_train:
        mask = df["timestamp"] <= TRAIN_END_DATE
    else:
        mask = df["timestamp"] > TRAIN_END_DATE
        
    df_sub = df[mask].reset_index(drop=True)
    sig_sub = long_signal[mask].reset_index(drop=True)
    stop_sub = stop_long[mask].reset_index(drop=True)
    
    if len(df_sub) < 100:
        return 0.0
        
    trades = []
    i = 20
    end = len(df_sub) - 1
    cost = COST_BPS / 10000.0
    
    while i < end:
        if not bool(sig_sub.iloc[i]):
            i += 1
            continue
            
        entry_idx = i + 1
        entry_price = float(df_sub["open"].iloc[entry_idx])
        stop_price = float(stop_sub.iloc[i])
        
        if pd.isna(entry_price) or pd.isna(stop_price) or stop_price >= entry_price or entry_price <= 0:
            i += 1
            continue
            
        risk = entry_price - stop_price
        target_price = entry_price + 2.0 * risk
        
        is_trail_exit = (strategy == "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL")
        
        exit_idx = min(entry_idx + 96, len(df_sub) - 1)
        exit_price = float(df_sub["close"].iloc[exit_idx])
        
        for cursor in range(entry_idx, exit_idx + 1):
            c_high = float(df_sub["high"].iloc[cursor])
            c_low = float(df_sub["low"].iloc[cursor])
            c_close = float(df_sub["close"].iloc[cursor])
            c_ema = float(df_sub["ema_8"].iloc[cursor]) if "ema_8" in df_sub else 0.0
            
            if c_low <= stop_price:
                exit_idx = cursor
                exit_price = stop_price
                break
            
            if not is_trail_exit and c_high >= target_price:
                exit_idx = cursor
                exit_price = target_price
                break
                
            if is_trail_exit and c_close < c_ema:
                exit_idx = cursor
                exit_price = float(df_sub["open"].iloc[min(cursor + 1, len(df_sub)-1)])
                break
                
        raw_ret = (exit_price / entry_price - 1.0)
        trades.append((raw_ret - cost) * 100.0)
        i = max(exit_idx + 1, i + 1)
        
    return sum(trades) if trades else 0.0

# -------------------------------------------------------------
# MAIN PROCESSOR
# -------------------------------------------------------------
def main():
    manifest_path = Path(r"C:\LAB\_MTC_V2_REPO_CLEANUP_ARCHIVE_20260529\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\manifests\dataset_manifest.json")
    bundle_root = manifest_path.parents[1]
    output_dir = Path(r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\05_BACKTEST_RESULTS")
    
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
        
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "AVAXUSDT", "DOGEUSDT"]
    timeframes = ["15m", "1h", "2h", "4h", "1D"]
    
    # Pre-build daily RSI maps for Dual RSI swing
    daily_rsi_maps = {}
    for symbol in symbols:
        ds_1d = next((item for item in manifest["datasets"] 
                      if item["symbol"] == symbol and item["timeframe_normalized"] == "1D" and item.get("ohlcv_validation_status") == "PASS"), None)
        if ds_1d:
            df_1d = pd.read_csv(bundle_root / ds_1d["normalized_path"])
            df_1d["daily_rsi_7"] = rsi(df_1d["close"], 7).shift(1)
            df_1d["daily_rsi_14"] = rsi(df_1d["close"], 14).shift(1)
            df_1d["date"] = pd.to_datetime(df_1d["timestamp_utc"], utc=True).dt.date
            daily_rsi_maps[symbol] = {
                7: df_1d.set_index("date")["daily_rsi_7"].to_dict(),
                14: df_1d.set_index("date")["daily_rsi_14"].to_dict()
            }

    print("=" * 60)
    print("QUANTLENS MASTER WALK-FORWARD & OUT-OF-SAMPLE ENGINE")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)
    
    results = []
    
    # Loop over strategies
    for cid, grid in GRIDS.items():
        print(f"\nEvaluating Walk-Forward for Strategy: {cid}")
        
        for symbol in symbols:
            for tf in timeframes:
                # Dual RSI does not run on 1D (requires MTF)
                if cid == "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK" and tf == "1D":
                    continue
                    
                ds = next((item for item in manifest["datasets"] 
                           if item["symbol"] == symbol and item["timeframe_normalized"] == tf and item.get("ohlcv_validation_status") == "PASS"), None)
                if ds is None:
                    continue
                    
                # Load OHLCV data
                df = pd.read_csv(bundle_root / ds["normalized_path"])
                df["timestamp"] = pd.to_datetime(df["timestamp_utc"], utc=True)
                df["date"] = df["timestamp"].dt.date
                
                # Walk-Forward Optimization
                best_param = None
                best_train_ret = -999999.0
                
                for params in grid:
                    # Resolve daily RSI map if dual RSI strategy
                    daily_map = None
                    if cid == "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK":
                        daily_map = daily_rsi_maps.get(symbol, {}).get(params.get("rsi_len", 7))
                        
                    sig, stop = get_strategy_signals(cid, df, params, daily_map)
                    
                    # Run In-Sample Train optimization
                    train_ret = simulate_trades(df, sig, stop, cid, is_train=True)
                    if train_ret > best_train_ret:
                        best_train_ret = train_ret
                        best_param = params
                        
                # -------------------------------------------------------------
                # Out-of-Sample Evaluation
                # -------------------------------------------------------------
                if best_param is not None:
                    daily_map = None
                    if cid == "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK":
                        daily_map = daily_rsi_maps.get(symbol, {}).get(best_param.get("rsi_len", 7))
                        
                    sig, stop = get_strategy_signals(cid, df, best_param, daily_map)
                    
                    # Run OOS Test
                    oos_ret = simulate_trades(df, sig, stop, cid, is_train=False)
                    
                    results.append({
                        "strategy": cid,
                        "symbol": symbol,
                        "timeframe": tf,
                        "best_param_train": best_param,
                        "train_in_sample_return_pct": best_train_ret,
                        "test_out_of_sample_return_pct": oos_ret,
                        "status": "PASS" if oos_ret > 0 else "FAIL"
                    })
                    print(f" -> {symbol} {tf} | Train (IS): {best_train_ret:.2f}% | Test (OOS): {oos_ret:.2f}% | Status: {results[-1]['status']}")

    # Save to outputs
    output_file_json = output_dir / "walk_forward_oos_results.json"
    output_file_json.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    
    # Save a gorgeous markdown validation report
    md_lines = [
        "# Walk-Forward & Out-of-Sample Validation Report",
        "",
        f"- Generated at: `{datetime.now(timezone.utc).isoformat()}`",
        f"- Train Period: `2020-09-14 to 2024-06-01` (In-Sample)",
        f"- Test Period (OOS): `2024-06-01 to 2026-04-27` (Out-of-Sample)",
        "",
        "## Overall Strategy Performance Summary Table",
        "",
        "| Strategy ID | Symbol | Timeframe | Best Train Params | Train IS Return (%) | Test OOS Return (%) | Status |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in results:
        param_str = json.dumps(r["best_param_train"], separators=(",", ":"))
        md_lines.append(f"| {r['strategy']} | {r['symbol']} | {r['timeframe']} | `{param_str}` | {r['train_in_sample_return_pct']:.2f}% | {r['test_out_of_sample_return_pct']:.2f}% | **{r['status']}** |")
        
    output_file_md = output_dir / "WALK_FORWARD_VALIDATION_REPORT.md"
    output_file_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    
    print("\n" + "=" * 60)
    print("WALK-FORWARD & OOS TESTING COMPLETED SUCCESSFULLY!")
    print(f"Saved JSON results: {output_file_json}")
    print(f"Saved Markdown report: {output_file_md}")
    print("=" * 60)

if __name__ == "__main__":
    main()
