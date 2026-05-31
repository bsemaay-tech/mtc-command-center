import pandas as pd
import sys

path = r"C:\LAB\tradingview-lab\mtc_backtest\parity_suite_350\tv_manual_inputs\raw_tv_exports\Supertrend ATR 21 F 5.5.xlsx"

try:
    xl = pd.ExcelFile(path)
    print("Sheets:", xl.sheet_names)
    
    # 1. Check Properties
    prop_sheet = next((s for s in xl.sheet_names if s.lower() in ['properties', 'özellikler']), 'Properties')
    props = pd.read_excel(path, sheet_name=prop_sheet)
    print("\n--- PROPERTIES ---")
    for idx, row in props.dropna(how='all').head(100).iterrows():
        r = [str(x) for x in row.values if pd.notna(x)]
        if r:
            print(" | ".join(r))
            
    # 2. Check Trades
    trade_sheet = next((s for s in xl.sheet_names if 'list' in s.lower() or 'işlem' in s.lower() or 'oper' in s.lower()), None)
    if trade_sheet:
        trades = pd.read_excel(path, sheet_name=trade_sheet)
        print(f"\n--- TRADES ({trade_sheet}) ---")
        print("Total rows:", len(trades))
        if len(trades) > 0:
            # Check Types to confirm if any Longs exist
            type_counts = trades['Type'].value_counts() if 'Type' in trades.columns else "Type col not found"
            print("Trade Types found:\n", type_counts)
            
except Exception as e:
    import traceback
    traceback.print_exc()
