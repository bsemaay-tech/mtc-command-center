import pandas as pd
import sys

path = r"C:\LAB\tradingview-lab\mtc_backtest\parity_suite_350\tv_manual_inputs\raw_tv_exports\MT_CORE2_BINANCE_BTCUSDT.P_2026-03-08_1e440.xlsx"

try:
    xl = pd.ExcelFile(path)
    trade_sheet = next((s for s in xl.sheet_names if 'list' in s.lower() or 'işlem' in s.lower() or 'oper' in s.lower()), None)
    
    if trade_sheet:
        trades = pd.read_excel(path, sheet_name=trade_sheet)
        
        print(f"Columns: {trades.columns.tolist()}")
        print(f"Total rows in sheet: {len(trades)}")
        
        # Try to find the trade number column (could be "Trade #", "İşlem No", etc.)
        trade_col = next((c for c in trades.columns if '#' in str(c) or 'no' in str(c).lower() or 'trade' in str(c).lower() or 'işlem' in str(c).lower()), None)
        
        if trade_col:
            trades = trades.dropna(subset=[trade_col])
            print(f"Total valid rows (Entries + Exits): {len(trades)}")
            if len(trades) > 0:
                print("First 5 rows (raw):")
                for idx, row in trades.head(5).iterrows():
                    print(row.to_dict())
        else:
            print("Could not find trade number column.")
            print(trades.head(5).to_dict('records'))
                
except Exception as e:
    import traceback
    traceback.print_exc()
