import pandas as pd
import sys

path = r"C:\LAB\tradingview-lab\mtc_backtest\parity_suite_350\tv_manual_inputs\raw_tv_exports\Supertrend ATR 21 F 5.5.xlsx"

try:
    xl = pd.ExcelFile(path)
    prop_sheet = next((s for s in xl.sheet_names if s.lower() in ['properties', 'özellikler']), 'Properties')
    props = pd.read_excel(path, sheet_name=prop_sheet)
    with open("supertrend_props.txt", "w", encoding="utf-8") as f:
        for idx, row in props.dropna(how='all').iterrows():
            r = [str(x) for x in row.values if pd.notna(x)]
            if r:
                f.write(" | ".join(r) + "\n")
    print("Full properties dumped to mtc_backtest/supertrend_props.txt")
except Exception as e:
    print(f"Error: {e}")
