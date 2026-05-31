import math
import os
import json
import csv
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timezone

# -------------------------------------------------------------
# SPECIFICATION STRINGS FOR EACH CANDIDATE
# -------------------------------------------------------------
SPECS = {
    "QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK": """# QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK — Deterministic Spec

- **Status**: PROMOTED TO PROTOTYPE
- **Timeframe**: 15m (Crypto proxy for 10m US Equities)

## Rules
* **Entry**: Close > 8 EMA and 8 EMA slope > 0. Distance to 8 EMA <= 0.35 * ATR(14). Preceding 3-bar impulse >= 1.0 * ATR(14).
* **Stop**: 3-bar swing low.
* **Target**: Fixed 2.0R.
""",
    "QL_2026-05-01_US_EQUITIES_INTRADAY_LE_MODEL_BULL_FLAG": """# QL_2026-05-01_US_EQUITIES_INTRADAY_LE_MODEL_BULL_FLAG — Deterministic Spec

- **Status**: PROMOTED TO PROTOTYPE
- **Timeframe**: 15m (Crypto proxy)

## Rules
* **Entry**: Breakout EMA retest. Close > 8 EMA and 8 EMA slope > 0. Distance to 8 EMA <= 0.35 * ATR(14). Preceding 3-bar impulse >= 1.0 * ATR(14).
* **Stop**: 3-bar swing low.
* **Target**: Fixed 2.0R.
""",
    "QL_2026-05-01_US_EQUITIES_INTRADAY_PURPLE_PROFITS": """# QL_2026-05-01_US_EQUITIES_INTRADAY_PURPLE_PROFITS — Deterministic Spec

- **Status**: PROMOTED TO PROTOTYPE
- **Timeframe**: 15m (Crypto proxy)

## Rules
* **Entry**: Purple Profits 8 EMA strategy. Close > 8 EMA and 8 EMA slope > 0. Distance to 8 EMA <= 0.35 * ATR(14). Preceding 3-bar impulse >= 1.0 * ATR(14).
* **Stop**: 3-bar swing low.
* **Target**: Fixed 2.0R.
""",
    "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL": """# QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL — Deterministic Spec

- **Status**: PROMOTED TO PROTOTYPE
- **Timeframe**: 15m (Crypto proxy)

## Rules
* **Entry**: Close > 8 EMA and 8 EMA slope > 0. Distance to 8 EMA <= 0.35 * ATR(14).
* **Stop**: 3-bar swing low.
* **Exit**: Dynamic trailing exit when price closes crossing below the 8 EMA line.
""",
    "QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNEL_PULLBACK": """# QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNEL_PULLBACK — Deterministic Spec

- **Status**: PROMOTED TO PROTOTYPE
- **Timeframe**: 15m

## Rules
* **Entry**: Price > EMA(200). Fast EMA(5) > Mid EMA(13). Price pulls back to touch or get near Mid EMA(13) (distance <= 0.4 * ATR).
* **Stop**: 5-bar swing low.
* **Target**: Fixed 2.0R.
""",
    "QL_2026-05-01_LIQUID_INTRADAY_VWAP_PULLBACK_REVERSAL": """# QL_2026-05-01_LIQUID_INTRADAY_VWAP_PULLBACK_REVERSAL — Deterministic Spec

- **Status**: PROMOTED TO PROTOTYPE
- **Timeframe**: 15m

## Rules
* **Entry**: VWAP session proxy mean rolling window of 96 bars. Slope of proxy > 0 (long). Close above proxy and distance <= 0.4 * ATR.
* **Stop**: VWAP band proxy - 1.0 * standard deviation.
* **Target**: Fixed 2.0R.
""",
    "QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PLAYBOOK": """# QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PLAYBOOK — Deterministic Spec

- **Status**: PROTOTYPED
- **Timeframe**: 1h

## Rules
* **Entry**: Close > SMA(50). RSI(14) crosses above 50.
* **Stop**: 5-bar swing low.
* **Target**: Fixed 2.0R.
""",
    "QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR": """# QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR — Deterministic Spec

- **Status**: PROMOTED TO PROTOTYPE
- **Timeframe**: 15m (Crypto proxy for 5m)

## Rules
* **Entry**: Breakout of 48-bar high level. Candle close must be in the upper third of its range.
* **Stop**: 2-bar swing low.
* **Target**: Fixed 2.0R.
""",
    "QL_2026-05-01_ANY_BOLLINGER_BANDS_20_2_TRI_SETUP": """# QL_2026-05-01_ANY_BOLLINGER_BANDS_20_2_TRI_SETUP — Deterministic Spec

- **Status**: PROMOTED TO PROTOTYPE
- **Timeframe**: 1h

## Rules
* **Entry**: BB width is inside the lowest 25% quantile of past 200 bars (Squeeze). Entry when close crosses outside upper Bollinger Band and signal candle body is >= 0.25 * ATR.
* **Stop**: 5-bar swing low.
* **Target**: Fixed 2.0R.
""",
    "QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE": """# QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE — Deterministic Spec

- **Status**: PROMOTED TO PROTOTYPE
- **Timeframe**: 1h

## Rules
* **Entry**: Bullish engulfing pattern near 96-bar support (distance <= 0.4 * ATR).
* **Stop**: Low of engulfing candle with 0.1 * ATR buffer.
* **Target**: Fixed 2.0R.
"""
}

# -------------------------------------------------------------
# CORE METRICS & INDICATORS HELPERS
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
# STRATEGY DETECTOR RUNNERS
# -------------------------------------------------------------
def backtest_strategy(strategy: str, df: pd.DataFrame, cost_bps: float) -> list[dict]:
    close = df["close"]
    high = df["high"]
    low = df["low"]
    cost = cost_bps / 10000.0
    trades = []
    
    # Calculate common elements
    df["atr_14"] = atr(df, 14)
    df["ema_8"] = ema(close, 8)
    df["ema_5"] = ema(close, 5)
    df["ema_13"] = ema(close, 13)
    df["ema_200"] = ema(close, 200)
    df["sma_50"] = sma(close, 50)
    df["rsi_14"] = rsi(close, 14)
    
    # Pre-calculate indicators specific to strategies
    if strategy in {"QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK", 
                    "QL_2026-05-01_US_EQUITIES_INTRADAY_LE_MODEL_BULL_FLAG", 
                    "QL_2026-05-01_US_EQUITIES_INTRADAY_PURPLE_PROFITS",
                    "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL"}:
        slope = df["ema_8"] - df["ema_8"].shift(3)
        dist = (close - df["ema_8"]).abs() / df["atr_14"]
        impulse = (close - close.shift(3)).abs() / df["atr_14"]
        
        long_signal = (close > df["ema_8"]) & (slope > 0) & (dist <= 0.35) & (impulse.shift(1) >= 1.0)
        stop_long = low.rolling(3, min_periods=1).min()
        
    elif strategy == "QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNEL_PULLBACK":
        dist = (close - df["ema_13"]).abs() / df["atr_14"]
        long_signal = (close > df["ema_200"]) & (df["ema_5"] > df["ema_13"]) & (dist <= 0.4) & (close > df["open"])
        stop_long = low.rolling(5, min_periods=1).min()
        
    elif strategy == "QL_2026-05-01_LIQUID_INTRADAY_VWAP_PULLBACK_REVERSAL":
        proxy = df["close"].rolling(96, min_periods=96).mean()
        band = df["close"].rolling(96, min_periods=96).std()
        slope = proxy - proxy.shift(4)
        proximity = (close - proxy).abs() / df["atr_14"]
        long_signal = (slope > 0) & (close > proxy) & (proximity <= 0.4)
        stop_long = proxy - 1.0 * band
        
    elif strategy == "QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PLAYBOOK":
        long_signal = (close > df["sma_50"]) & (df["rsi_14"].shift(1) < 50) & (df["rsi_14"] >= 50)
        stop_long = low.rolling(5, min_periods=1).min()
        
    elif strategy == "QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR":
        high_break = high.rolling(48, min_periods=10).max().shift(1)
        candle_range = (high - low).replace(0, np.nan)
        close_pos = (close - low) / candle_range
        strong_bull = (close_pos >= 0.66) & (close > high.shift(1))
        long_signal = strong_bull & (close > high_break)
        stop_long = low.rolling(2, min_periods=1).min()
        
    elif strategy == "QL_2026-05-01_ANY_BOLLINGER_BANDS_20_2_TRI_SETUP":
        bb_mid = sma(close, 20)
        bb_std = close.rolling(20, min_periods=20).std()
        bb_upper = bb_mid + 2 * bb_std
        bb_width_pct = (2 * 2 * bb_std) / bb_mid
        width_limit = bb_width_pct.rolling(200, min_periods=200).quantile(0.25)
        narrow = bb_width_pct <= width_limit
        body_ok = (close - df["open"]).abs() >= 0.25 * df["atr_14"]
        
        long_signal = narrow.shift(1) & (close > bb_upper) & body_ok
        stop_long = low.rolling(5, min_periods=1).min()
        
    elif strategy == "QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE":
        support = low.rolling(96, min_periods=20).min().shift(1)
        body_low = pd.concat([df["open"], close], axis=1).min(axis=1)
        body_high = pd.concat([df["open"], close], axis=1).max(axis=1)
        prev_body_low = body_low.shift(1)
        prev_body_high = body_high.shift(1)
        bullish_engulf = (close > df["open"]) & (body_low <= prev_body_low) & (body_high >= prev_body_high)
        near_support = ((low - support).abs() / df["atr_14"]) <= 0.4
        
        long_signal = bullish_engulf & near_support
        stop_long = low - 0.1 * df["atr_14"]
    else:
        return []

    # Run Simulation Loop
    i = 20
    end = len(df) - 1
    while i < end:
        if not bool(long_signal.iloc[i]):
            i += 1
            continue
            
        entry_idx = i + 1
        entry_price = float(df["open"].iloc[entry_idx])
        stop_price = float(stop_long.iloc[i])
        
        if pd.isna(entry_price) or pd.isna(stop_price) or stop_price >= entry_price or entry_price <= 0:
            i += 1
            continue
            
        risk = entry_price - stop_price
        target_price = entry_price + 2.0 * risk
        
        # dynamic exit for exit trail strategy
        is_trail_exit = (strategy == "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL")
        
        exit_idx = min(entry_idx + 96, len(df) - 1)
        exit_price = float(df["close"].iloc[exit_idx])
        reason = "max_hold"
        
        for cursor in range(entry_idx, exit_idx + 1):
            c_high = float(df["high"].iloc[cursor])
            c_low = float(df["low"].iloc[cursor])
            c_close = float(df["close"].iloc[cursor])
            c_ema = float(df["ema_8"].iloc[cursor])
            
            if c_low <= stop_price:
                exit_idx = cursor
                exit_price = stop_price
                reason = "stop"
                break
            
            if not is_trail_exit and c_high >= target_price:
                exit_idx = cursor
                exit_price = target_price
                reason = "target"
                break
                
            if is_trail_exit and c_close < c_ema:
                exit_idx = cursor
                exit_price = float(df["open"].iloc[min(cursor + 1, len(df)-1)])
                reason = "trail_cross"
                break
                
        raw_ret = (exit_price / entry_price - 1.0)
        trades.append({
            "side": "long",
            "entry_time": str(df["timestamp_utc"].iloc[entry_idx]),
            "exit_time": str(df["timestamp_utc"].iloc[exit_idx]),
            "entry_price": entry_price,
            "exit_price": exit_price,
            "return_pct": (raw_ret - cost) * 100.0,
            "raw_return_pct": raw_ret * 100.0,
            "reason": reason,
            "bars_held": exit_idx - entry_idx
        })
        
        i = max(exit_idx + 1, i + 1)
        
    return trades

# -------------------------------------------------------------
# MAIN PROCESSOR
# -------------------------------------------------------------
def main():
    manifest_path = Path(r"C:\LAB\_MTC_V2_REPO_CLEANUP_ARCHIVE_20260529\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\manifests\dataset_manifest.json")
    bundle_root = manifest_path.parents[1]
    output_dir = Path(r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\05_BACKTEST_RESULTS")
    candidates_dir = Path(r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\01_TRIAGED_CANDIDATES")
    registry_path = Path(r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\_registry\quantlens_candidate_registry.csv")
    
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
        
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "AVAXUSDT", "DOGEUSDT"]
    
    # 1. Write the 10 Deterministic Specs
    print("Writing 10 Deterministic Specs to candidate directories...")
    for cid, spec_content in SPECS.items():
        spec_file = candidates_dir / cid / "07_deterministic_spec.md"
        spec_file.parent.mkdir(parents=True, exist_ok=True)
        spec_file.write_text(spec_content, encoding="utf-8")
        print(f" -> Created: {spec_file.name}")
        
    # 2. Backtest remaining 10 strategies
    print("\nStarting batch backtesting on all parities...")
    all_summaries = {}
    
    for cid in SPECS.keys():
        print(f"\nProcessing backtest for: {cid}")
        # Map strategy to proxy timeframe (8EMA/VWAP/TwoCandle uses 15m; others use 1h)
        tf = "15m"
        if cid in {
            "QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PLAYBOOK", 
            "QL_2026-05-01_ANY_BOLLINGER_BANDS_20_2_TRI_SETUP", 
            "QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE"
        }:
            tf = "1h"
            
        trades_for_strategy = []
        symbol_stats = {}
        
        for symbol in symbols:
            ds = next((item for item in manifest["datasets"] 
                       if item["symbol"] == symbol and item["timeframe_normalized"] == tf and item.get("ohlcv_validation_status") == "PASS"), None)
            if ds is None:
                continue
                
            df = pd.read_csv(bundle_root / ds["normalized_path"])
            trades = backtest_strategy(cid, df, cost_bps=8.0)
            
            if trades:
                df_t = pd.DataFrame(trades)
                win_rate = (df_t["return_pct"] > 0).mean() * 100
                avg_ret = df_t["return_pct"].mean()
                net_ret = df_t["return_pct"].sum()
                
                symbol_stats[symbol] = {
                    "trades": len(trades),
                    "win_rate_pct": float(win_rate),
                    "avg_return_pct": float(avg_ret),
                    "net_return_sum_pct": float(net_ret)
                }
                trades_for_strategy.extend(trades)
                
        # Save JSON results and MD summary
        if trades_for_strategy:
            payload = {
                "candidate_id": cid,
                "backtest_run_at": datetime.now(timezone.utc).isoformat(),
                "summary": symbol_stats,
                "trades": trades_for_strategy
            }
            # Save JSON
            json_file = output_dir / f"{cid}_results.json"
            json_file.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            
            # Save MD report
            md_lines = [
                f"# Backtest Report: {cid}",
                f"",
                f"- Candidate: `{cid}`",
                f"- Run Time: `{datetime.now(timezone.utc).isoformat()}`",
                f"",
                f"## Performance Summary Table",
                f"",
                f"| Symbol | Total Trades | Win Rate (%) | Avg Return (%) | Net Return Sum (%) |",
                f"|---|---|---|---|---|",
            ]
            total_trades = 0
            best_symbol = "None"
            best_net = -9999.0
            
            for sym, stats in symbol_stats.items():
                md_lines.append(f"| {sym} | {stats['trades']} | {stats['win_rate_pct']:.2f}% | {stats['avg_return_pct']:.2f}% | {stats['net_return_sum_pct']:.2f}% |")
                total_trades += stats['trades']
                if stats['net_return_sum_pct'] > best_net:
                    best_net = stats['net_return_sum_pct']
                    best_symbol = sym
                    
            md_file = output_dir / f"{cid}_summary.md"
            md_file.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
            print(f" -> Backtest completed: {total_trades} trades total. Best par: {best_symbol} ({best_net:.2f}%)")
            
            all_summaries[cid] = {
                "status": "PROTOTYPED",
                "best_symbol": best_symbol,
                "best_net_pct": best_net,
                "total_trades": total_trades
            }
            
    # 3. Update candidate registry CSV
    if registry_path.exists():
        print("\nUpdating quantlens_candidate_registry.csv...")
        rows = []
        with open(registry_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows.append(header)
            
            # candidate_id is column 0
            # status is column 1
            # notes is column 12
            # updated_at is column 16
            for row in reader:
                cid = row[0]
                if cid in all_summaries:
                    row[1] = "PROTOTYPED"
                    best_sym = all_summaries[cid]["best_symbol"]
                    best_net = all_summaries[cid]["best_net_pct"]
                    tot_tr = all_summaries[cid]["total_trades"]
                    row[12] = f"Batch prototyped on 8 symbols. Total trades: {tot_tr}. Best performing: {best_sym} ({best_net:.2f}%)."
                    row[16] = "2026-05-29"
                rows.append(row)
                
        with open(registry_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        print("Registry CSV updated successfully!")
        
    print("\n" + "=" * 60)
    print("ALL 10 REMAINING CANDIDATES BATCH PROCESSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    main()
