"""
QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK - Isolated Python Prototype
This script performs a rigorous backtest of the Dual RSI multi-timeframe pullback strategy.
It adheres strictly to the mechanical rules specified in the 07_deterministic_spec.md.
"""

import math
import os
import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timezone

# Strategy Constants
RSI_LEN = 7
DAILY_HI = 60.0
DAILY_LO = 40.0
LTF_PULLBACK_HI = 60.0
LTF_PULLBACK_LO = 40.0
PULLBACK_MEMORY = 12  # hours
SWING_LOOKBACK = 10   # bars
ATR_LEN = 14
MAX_ATR_MULT = 2.5    # large-candle filter
RR_RATIO = 2.0        # Risk-to-reward ratio
COST_BPS = 8.0        # Round-trip cost in basis points

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

def run_backtest_for_symbol(symbol: str, manifest_path: Path, bundle_root: Path) -> tuple[list[dict], pd.DataFrame]:
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
        
    # Select 1h and 1D datasets
    ds_1h = next((item for item in manifest["datasets"] 
                  if item["symbol"] == symbol and item["timeframe_normalized"] == "1h" and item.get("ohlcv_validation_status") == "PASS"), None)
    ds_1d = next((item for item in manifest["datasets"] 
                  if item["symbol"] == symbol and item["timeframe_normalized"] == "1D" and item.get("ohlcv_validation_status") == "PASS"), None)
    
    if ds_1h is None or ds_1d is None:
        print(f"Skipping {symbol}: Complete 1h/1D dataset pair not found in manifest.")
        return [], pd.DataFrame()
        
    # Read CSVs
    df_1h = pd.read_csv(bundle_root / ds_1h["normalized_path"])
    df_1d = pd.read_csv(bundle_root / ds_1d["normalized_path"])
    
    # Process daily indicators & shift to prevent lookahead bias
    df_1d["daily_rsi"] = rsi(df_1d["close"], RSI_LEN).shift(1)
    df_1d["date"] = pd.to_datetime(df_1d["timestamp_utc"], utc=True).dt.date
    daily_rsi_map = df_1d.set_index("date")["daily_rsi"].to_dict()
    
    # Process 1h indicators
    df_1h["timestamp"] = pd.to_datetime(df_1h["timestamp_utc"], utc=True)
    df_1h["date"] = df_1h["timestamp"].dt.date
    df_1h["daily_rsi"] = df_1h["date"].map(daily_rsi_map)
    df_1h["rsi_1h"] = rsi(df_1h["close"], RSI_LEN)
    df_1h["atr"] = atr(df_1h, ATR_LEN)
    
    # Swing stop calculation anchors (lookahead-safe shifts)
    df_1h["swing_low"] = df_1h["low"].rolling(SWING_LOOKBACK).min().shift(1)
    df_1h["swing_high"] = df_1h["high"].rolling(SWING_LOOKBACK).max().shift(1)
    
    trades = []
    position = None # 'long', 'short', or None
    pullback_active = False
    pullback_timer = 0
    cost = COST_BPS / 10000.0
    
    for i in range(20, len(df_1h) - 1):
        row = df_1h.iloc[i]
        next_row = df_1h.iloc[i+1]
        
        if pd.isna(row["daily_rsi"]) or pd.isna(row["rsi_1h"]) or pd.isna(row["atr"]):
            continue
            
        if position is None:
            # Bull Regime (Long Only)
            if row["daily_rsi"] > DAILY_HI:
                if row["rsi_1h"] < LTF_PULLBACK_LO:
                    pullback_active = True
                    pullback_timer = 0
                elif pullback_active:
                    pullback_timer += 1
                    if pullback_timer > PULLBACK_MEMORY:
                        pullback_active = False
                    elif row["rsi_1h"] >= LTF_PULLBACK_LO and df_1h.iloc[i-1]["rsi_1h"] < LTF_PULLBACK_LO:
                        # Entry triggered on recovery cross
                        entry_price = float(next_row["open"])
                        stop_price = float(row["swing_low"])
                        risk = entry_price - stop_price
                        
                        if risk > 0 and (risk <= MAX_ATR_MULT * row["atr"]):
                            target_price = entry_price + RR_RATIO * risk
                            position = {
                                "side": "long",
                                "entry_price": entry_price,
                                "stop_price": stop_price,
                                "target_price": target_price,
                                "entry_time": str(next_row["timestamp_utc"]),
                                "idx": i + 1
                            }
                            pullback_active = False
                            
            # Bear Regime (Short Only)
            elif row["daily_rsi"] < DAILY_LO:
                if row["rsi_1h"] > LTF_PULLBACK_HI:
                    pullback_active = True
                    pullback_timer = 0
                elif pullback_active:
                    pullback_timer += 1
                    if pullback_timer > PULLBACK_MEMORY:
                        pullback_active = False
                    elif row["rsi_1h"] <= LTF_PULLBACK_HI and df_1h.iloc[i-1]["rsi_1h"] > LTF_PULLBACK_HI:
                        # Entry triggered on rejection cross
                        entry_price = float(next_row["open"])
                        stop_price = float(row["swing_high"])
                        risk = stop_price - entry_price
                        
                        if risk > 0 and (risk <= MAX_ATR_MULT * row["atr"]):
                            target_price = entry_price - RR_RATIO * risk
                            position = {
                                "side": "short",
                                "entry_price": entry_price,
                                "stop_price": stop_price,
                                "target_price": target_price,
                                "entry_time": str(next_row["timestamp_utc"]),
                                "idx": i + 1
                            }
                            pullback_active = False
        else:
            # Manage Open Position
            high = float(row["high"])
            low = float(row["low"])
            close = float(row["close"])
            
            if position["side"] == "long":
                if low <= position["stop_price"]:
                    raw_ret = (position["stop_price"] / position["entry_price"] - 1.0)
                    trades.append({
                        "symbol": symbol,
                        "side": "long",
                        "entry_time": position["entry_time"],
                        "exit_time": str(row["timestamp_utc"]),
                        "entry_price": position["entry_price"],
                        "exit_price": position["stop_price"],
                        "return_pct": (raw_ret - cost) * 100,
                        "raw_return_pct": raw_ret * 100,
                        "reason": "stop",
                        "bars_held": i - position["idx"]
                    })
                    position = None
                elif high >= position["target_price"]:
                    raw_ret = (position["target_price"] / position["entry_price"] - 1.0)
                    trades.append({
                        "symbol": symbol,
                        "side": "long",
                        "entry_time": position["entry_time"],
                        "exit_time": str(row["timestamp_utc"]),
                        "entry_price": position["entry_price"],
                        "exit_price": position["target_price"],
                        "return_pct": (raw_ret - cost) * 100,
                        "raw_return_pct": raw_ret * 100,
                        "reason": "target",
                        "bars_held": i - position["idx"]
                    })
                    position = None
            elif position["side"] == "short":
                if high >= position["stop_price"]:
                    raw_ret = (position["entry_price"] / position["stop_price"] - 1.0)
                    trades.append({
                        "symbol": symbol,
                        "side": "short",
                        "entry_time": position["entry_time"],
                        "exit_time": str(row["timestamp_utc"]),
                        "entry_price": position["entry_price"],
                        "exit_price": position["stop_price"],
                        "return_pct": (raw_ret - cost) * 100,
                        "raw_return_pct": raw_ret * 100,
                        "reason": "stop",
                        "bars_held": i - position["idx"]
                    })
                    position = None
                elif low <= position["target_price"]:
                    raw_ret = (position["entry_price"] / position["target_price"] - 1.0)
                    trades.append({
                        "symbol": symbol,
                        "side": "short",
                        "entry_time": position["entry_time"],
                        "exit_time": str(row["timestamp_utc"]),
                        "entry_price": position["entry_price"],
                        "exit_price": position["target_price"],
                        "return_pct": (raw_ret - cost) * 100,
                        "raw_return_pct": raw_ret * 100,
                        "reason": "target",
                        "bars_held": i - position["idx"]
                    })
                    position = None
                    
    return trades, df_1h

def main():
    manifest_path = Path(r"C:\LAB\_MTC_V2_REPO_CLEANUP_ARCHIVE_20260529\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\manifests\dataset_manifest.json")
    bundle_root = manifest_path.parents[1]
    output_dir = Path(r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\05_BACKTEST_RESULTS")
    
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "AVAXUSDT", "DOGEUSDT"]
    
    all_trades = []
    symbol_summaries = {}
    
    print("=" * 60)
    print("QUANTLENS ISOLATED PROTOTYPE RUNNER - DUAL RSI PULLBACK")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)
    
    for symbol in symbols:
        print(f"Running backtest for {symbol}...")
        try:
            trades, df = run_backtest_for_symbol(symbol, manifest_path, bundle_root)
            if not trades:
                print(f"No trades triggered for {symbol}.")
                continue
                
            all_trades.extend(trades)
            
            # Compute stats
            df_t = pd.DataFrame(trades)
            win_rate = (df_t["return_pct"] > 0).mean() * 100
            avg_ret = df_t["return_pct"].mean()
            net_ret = df_t["return_pct"].sum() # Simplified arithmetic return sum for sanity check
            long_trades = (df_t["side"] == "long").sum()
            short_trades = (df_t["side"] == "short").sum()
            
            symbol_summaries[symbol] = {
                "trades": len(trades),
                "win_rate_pct": win_rate,
                "avg_return_pct": avg_ret,
                "net_return_sum_pct": net_ret,
                "long_trades": int(long_trades),
                "short_trades": int(short_trades)
            }
            print(f"-> {symbol} complete: {len(trades)} trades | WR: {win_rate:.2f}% | Avg: {avg_ret:.2f}%")
        except Exception as e:
            print(f"ERROR backtesting {symbol}: {str(e)}")
            
    # Save detailed results
    if all_trades:
        results_payload = {
            "strategy": "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK",
            "backtest_run_at": datetime.now(timezone.utc).isoformat(),
            "summary": symbol_summaries,
            "trades": all_trades
        }
        
        output_file = output_dir / "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK_results.json"
        output_file.write_text(json.dumps(results_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print("\n" + "=" * 60)
        print(f"Backtest completed successfully!")
        print(f"Saved results to: {output_file}")
        
        # Save a human-readable markdown report as well
        md_lines = [
            f"# Backtest Report: Dual RSI 60/40 Pullback",
            f"",
            f"- Strategy: `QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK`",
            f"- Run Time: `{datetime.now(timezone.utc).isoformat()}`",
            f"",
            f"## Performance Summary Table",
            f"",
            f"| Symbol | Total Trades | Win Rate (%) | Avg Return (%) | Net Return Sum (%) | Longs | Shorts |",
            f"|---|---|---|---|---|---|---|",
        ]
        for sym, stats in symbol_summaries.items():
            md_lines.append(f"| {sym} | {stats['trades']} | {stats['win_rate_pct']:.2f}% | {stats['avg_return_pct']:.2f}% | {stats['net_return_sum_pct']:.2f}% | {stats['long_trades']} | {stats['short_trades']} |")
            
        md_file = output_dir / "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK_summary.md"
        md_file.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
        print(f"Saved markdown summary to: {md_file}")
        print("=" * 60)
        
if __name__ == "__main__":
    main()
