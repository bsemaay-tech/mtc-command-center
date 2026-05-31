import os
import glob
import pandas as pd
import numpy as np

DATA_ROOT = r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\data_acquisition_5m_2026_05_03\normalized\binance_futures"
OUTPUT_DIR = r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\stage2_robustness_2026_05_03_CODEX"
ASSETS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", "AVAXUSDT", "LINKUSDT", "DOTUSDT"]

def load_data(asset, timeframe="5m"):
    path = os.path.join(DATA_ROOT, asset, "5m", "*.csv")
    files = glob.glob(path)
    if not files: return pd.DataFrame()
    df = pd.read_csv(files[0], parse_dates=['timestamp'] if 'timestamp' in pd.read_csv(files[0], nrows=0).columns else None)
    df.columns = [c.lower() for c in df.columns]
    
    if timeframe == "1D":
        if 'timestamp' in df.columns:
            df.set_index('timestamp', inplace=True)
            df = df.resample('D').agg({'open':'first', 'high':'max', 'low':'min', 'close':'last', 'volume':'sum'}).dropna()
            df.reset_index(inplace=True)
        else:
            # Fake a daily resample if no timestamp
            df = df.groupby(df.index // 288).agg({'open':'first', 'high':'max', 'low':'min', 'close':'last', 'volume':'sum'})
            
    return df

def test_lbr_coil(asset, df):
    # LBR Coil IDNR4 Limit Entry
    df['range'] = df['high'] - df['low']
    df['prev_range_1'] = df['range'].shift(1)
    df['prev_range_2'] = df['range'].shift(2)
    df['prev_range_3'] = df['range'].shift(3)
    df['is_nr4'] = (df['range'] < df['prev_range_1']) & (df['range'] < df['prev_range_2']) & (df['range'] < df['prev_range_3'])
    df['is_inside'] = (df['high'] < df['high'].shift(1)) & (df['low'] > df['low'].shift(1))
    df['is_idnr4'] = df['is_nr4'] & df['is_inside']
    df['signal'] = df['is_idnr4'].shift(1)
    df['buy_trigger'] = df['high'].shift(1)
    
    trades = []
    in_trade = False
    entry_price = 0
    bars_held = 0
    
    for idx, row in df.iterrows():
        if pd.isna(row['signal']): continue
        if in_trade:
            bars_held += 1
            if bars_held >= 5: # Time exit
                ret = (row['close'] - entry_price) / entry_price
                trades.append(ret)
                in_trade = False
        else:
            if row['signal']:
                # Limit order at buy_trigger.
                if row['low'] <= row['buy_trigger'] <= row['high']:
                    entry_price = row['buy_trigger']
                    in_trade = True
                    bars_held = 0
                elif row['open'] < row['buy_trigger'] and row['high'] > row['buy_trigger']:
                    entry_price = row['buy_trigger']
                    in_trade = True
                    bars_held = 0
                    
    return trades

def test_stan_weinstein(asset, df):
    # Stan Weinstein Stage 2 Breakout (Daily)
    df['sma50'] = df['close'].rolling(50).mean()
    df['sma150'] = df['close'].rolling(150).mean()
    df['sma200'] = df['close'].rolling(200).mean()
    df['sma200_slope'] = df['sma200'] - df['sma200'].shift(20)
    
    # Mathematical Stage 2 definition
    df['is_stage2'] = (df['close'] > df['sma150']) & (df['sma150'] > df['sma200']) & (df['sma200_slope'] > 0)
    df['signal'] = df['is_stage2'] & (~df['is_stage2'].shift(1).fillna(False)) # Breakout into Stage 2
    
    trades = []
    in_trade = False
    entry_price = 0
    
    for idx, row in df.iterrows():
        if in_trade:
            if row['close'] < row['sma200']: # Exit rule
                ret = (row['close'] - entry_price) / entry_price
                trades.append(ret)
                in_trade = False
        else:
            if row['signal']:
                entry_price = row['open'] # Next bar open
                in_trade = True
                
    return trades

def run_tests():
    print("Running Stage 2 Tests...")
    results = []
    
    for asset in ASSETS:
        df_5m = load_data(asset, "5m")
        df_1d = load_data(asset, "1D")
        
        if df_5m.empty: continue
        
        # Test LBR
        trades_lbr = test_lbr_coil(asset, df_5m)
        df_lbr = pd.DataFrame({"ret": trades_lbr})
        pf_lbr = df_lbr[df_lbr['ret']>0]['ret'].sum() / abs(df_lbr[df_lbr['ret']<=0]['ret'].sum()) if not df_lbr.empty and df_lbr[df_lbr['ret']<=0]['ret'].sum() != 0 else 0
        
        # Test Stan Weinstein
        trades_stan = test_stan_weinstein(asset, df_1d)
        df_stan = pd.DataFrame({"ret": trades_stan})
        pf_stan = df_stan[df_stan['ret']>0]['ret'].sum() / abs(df_stan[df_stan['ret']<=0]['ret'].sum()) if not df_stan.empty and df_stan[df_stan['ret']<=0]['ret'].sum() != 0 else 0
        
        results.append({
            "asset": asset,
            "lbr_trades": len(trades_lbr),
            "lbr_pf_gross": pf_lbr,
            "stan_trades": len(trades_stan),
            "stan_pf_gross": pf_stan
        })
        
    df_res = pd.DataFrame(results)
    df_res.to_csv(os.path.join(OUTPUT_DIR, "stage2_prelim_results.csv"), index=False)
    print("Stage 2 Tests complete.")

if __name__ == "__main__":
    run_tests()
