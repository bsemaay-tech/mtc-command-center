import os
import glob
import pandas as pd
import numpy as np
import json

DATA_ROOT = r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\data_acquisition_5m_2026_05_03\normalized\binance_futures"
OUTPUT_DIR = r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\overnight_intake_batch_2026_05_03\strategies\QL_LBR_COIL_BREAKOUT_RANGE_EXPANSION_v0"

ASSETS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]
FEES = [0.0004, 0.0008, 0.0012] # base, 2x, 3x

def load_data(asset):
    path = os.path.join(DATA_ROOT, asset, "5m", "*.csv")
    files = glob.glob(path)
    if not files: return pd.DataFrame()
    df = pd.read_csv(files[0])
    # Ensure columns exist, standard is open, high, low, close, volume
    df.columns = [c.lower() for c in df.columns]
    return df

def run_backtest():
    all_results = []
    all_trades = []
    
    for asset in ASSETS:
        df = load_data(asset)
        if df.empty: continue
        
        # Calculate IDNR4
        df['range'] = df['high'] - df['low']
        df['prev_range_1'] = df['range'].shift(1)
        df['prev_range_2'] = df['range'].shift(2)
        df['prev_range_3'] = df['range'].shift(3)
        
        df['is_nr4'] = (df['range'] < df['prev_range_1']) & (df['range'] < df['prev_range_2']) & (df['range'] < df['prev_range_3'])
        df['is_inside'] = (df['high'] < df['high'].shift(1)) & (df['low'] > df['low'].shift(1))
        df['is_idnr4'] = df['is_nr4'] & df['is_inside']
        
        # Shift signals
        df['signal'] = df['is_idnr4'].shift(1)
        df['buy_trigger'] = df['high'].shift(1)
        df['sell_trigger'] = df['low'].shift(1)
        
        trades = []
        in_trade = False
        entry_price = 0
        bars_held = 0
        
        for idx, row in df.iterrows():
            if pd.isna(row['signal']): continue
            
            if in_trade:
                bars_held += 1
                if bars_held >= 5: # Time exit
                    exit_price = row['close']
                    ret = (exit_price - entry_price) / entry_price
                    trades.append(ret)
                    in_trade = False
            else:
                if row['signal']:
                    if row['high'] > row['buy_trigger']: # Long breakout
                        entry_price = row['buy_trigger']
                        in_trade = True
                        bars_held = 0
                        
        df_trades = pd.DataFrame({"return": trades})
        if df_trades.empty: continue
        
        # Fee stress
        def calc_metrics(trades_series, fee):
            net = trades_series - fee
            wins = net[net > 0]
            losses = net[net <= 0]
            pf = abs(wins.sum() / losses.sum()) if losses.sum() != 0 else float('inf')
            wr = len(wins) / len(net) if len(net) > 0 else 0
            cum = (1 + net).cumprod()
            dd = (cum.cummax() - cum) / cum.cummax()
            max_dd = dd.max()
            total_ret = cum.iloc[-1] - 1 if len(cum) > 0 else 0
            return pf, wr, max_dd, total_ret
            
        pf_base, wr, mdd, ret = calc_metrics(df_trades['return'], FEES[0])
        pf_2x, _, _, _ = calc_metrics(df_trades['return'], FEES[1])
        pf_3x, _, _, _ = calc_metrics(df_trades['return'], FEES[2])
        
        monotonic = (pf_base >= pf_2x) and (pf_2x >= pf_3x)
        
        all_results.append({
            "asset": asset,
            "trades": len(trades),
            "win_rate": wr,
            "max_dd": mdd,
            "total_ret": ret,
            "pf_base": pf_base,
            "pf_2x": pf_2x,
            "pf_3x": pf_3x,
            "fee_monotonic": monotonic
        })
        
    res_df = pd.DataFrame(all_results)
    res_df.to_csv(os.path.join(OUTPUT_DIR, "results.csv"), index=False)
    
    # Save Report
    with open(os.path.join(OUTPUT_DIR, "report.md"), "w") as f:
        f.write("# QL_LBR_COIL_BREAKOUT_RANGE_EXPANSION_v0 Report\n\n")
        f.write("## Overview\nTested IDNR4 breakout on 5m crypto proxy.\n")
        f.write("## Results\n")
        f.write(res_df.to_markdown())
        
        avg_pf = res_df['pf_base'].mean()
        if avg_pf > 1.05 and res_df['fee_monotonic'].all():
            verdict = "PASS_STAGE2"
        else:
            verdict = "WEAK_CANDIDATE"
        f.write(f"\n\n**Verdict:** {verdict}")

if __name__ == "__main__":
    run_backtest()
