import pandas as pd
import sys

path = r"C:\LAB\tradingview-lab\mtc_backtest\parity_suite_350\tv_manual_inputs\raw_tv_exports\MT_CORE2_BINANCE_BTCUSDT.P_2026-03-08_1e440.xlsx"

try:
    xl = pd.ExcelFile(path)
    with open("tv_export_dump.txt", "w", encoding="utf-8") as f:
        f.write(f"Sheets: {xl.sheet_names}\n\n")
        
        # We need to find the properties sheet. Might be 'Properties', 'Özellikler', etc.
        prop_sheet = next((s for s in xl.sheet_names if s.lower() in ['properties', 'özellikler']), xl.sheet_names[-1])
        f.write(f"Using Prop Sheet: {prop_sheet}\n")
        
        props = pd.read_excel(path, sheet_name=prop_sheet)
        for idx, row in props.dropna(how='all').iterrows():
            r = [str(x) for x in row.values if pd.notna(x)]
            if r:
                f.write(" | ".join(r) + "\n")
                
        # We need to find the trade sheet. Might be 'List of Trades', 'İşlem Listesi', etc.
        trade_sheet = next((s for s in xl.sheet_names if 'list' in s.lower() or 'işlem' in s.lower() or 'oper' in s.lower()), None)
        f.write(f"\nUsing Trade Sheet: {trade_sheet}\n")
        if trade_sheet:
            trades = pd.read_excel(path, sheet_name=trade_sheet)
            f.write(f"Total rows in trade sheet: {len(trades)}\n")
            
except Exception as e:
    import traceback
    with open("tv_export_dump.txt", "w", encoding="utf-8") as f:
        f.write(traceback.format_exc())
