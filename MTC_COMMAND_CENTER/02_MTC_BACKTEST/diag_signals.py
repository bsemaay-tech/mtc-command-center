import pandas as pd

sig_path = r"C:\LAB\tradingview-lab\debug\user_tv_mimic\debug_python_signals_20260308_113805_036e9daf.csv"

try:
    df = pd.read_csv(sig_path)
    
    # We want to find moments after the first trade exited
    after_trade = df[df['timestamp'] > '2025-07-02 06:00:00+00:00']
    
    raw_signals = after_trade[(after_trade['st_raw_long'] == True) | (after_trade['st_raw_short'] == True) | 
                              (after_trade['rf_raw_long'] == True) | (after_trade['rf_raw_short'] == True)]
                              
    print(f"Total raw RF signals after trade 1 exit: {len(raw_signals)}")
    
    if len(raw_signals) > 0:
        first_raw = raw_signals.iloc[0]
        print(f"\nFirst raw signal after exit: {first_raw['timestamp']}")
        block_cols = [c for c in first_raw.index if 'block' in c or 'guard' in c or 'filter' in c]
        for c in block_cols:
            print(f"{c}: {first_raw[c]}")
            
except Exception as e:
    import traceback
    traceback.print_exc()
