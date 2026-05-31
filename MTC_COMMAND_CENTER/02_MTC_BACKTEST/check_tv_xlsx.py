import pandas as pd
import sys

path = r"C:\LAB\tradingview-lab\mtc_backtest\parity_suite_350\tv_manual_inputs\raw_tv_exports\MT_CORE2_BINANCE_BTCUSDT.P_2026-03-08_1e440.xlsx"

try:
    xl = pd.ExcelFile(path)
    print("Sheets available:", xl.sheet_names)
    
    props = pd.read_excel(path, sheet_name="Properties")
    
    # Store properties in a dict for easy reading
    param_dict = {}
    for idx, row in props.dropna(how='all').iterrows():
        r = [x for x in row.values if pd.notna(x)]
        if len(r) >= 2:
            param_dict[str(r[0]).strip()] = r[1]
            
    print("\n--- KEY PROPERTIES EXTRACTED ---")
    keys_of_interest = [
        "Time Range", 
        "Date Range",
        "Enable Long Trades", "Enable Short Trades",
        "Exit On Opposite Signal",
        "[RF] ADX Trend Threshold", "[RF] ADX Range Threshold",
        "[RF] BB Length", "[RF] BB Multiplier",
        "[RF] Chop Range Threshold", "[RF] Chop Trend Threshold",
        "SL Mode", "Stop Loss ATR Multiplier", "Take Profit ATR Multiplier", "Take Profit R:R Ratio",
        "Break Even R:R", "Start Trailing R:R", 
        "Enable Filters", "[F] MA Period", "[F] McGinley Period", "[F] Volume Filter Period",
        "Equity Curve Guard Threshold %", "Equity Guard MA Length",
        "Risk per Long (% of equity)", "Risk per Short (% of equity)"
    ]
    
    for k in keys_of_interest:
        print(f"{k}: {param_dict.get(k, 'NOT_FOUND')}")

    # Display arbitrary properties if they don't match our exact strings:
    print("\n--- ALL RAW PARAMS RELATED TO SL/TP/FILTERS ---")
    for k, v in param_dict.items():
        if any(substring in k for substring in ["SL", "TP", "Filter", "Guard", "MultiTP"]):
            print(f"{k}: {v}")

    # Find the trade sheet
    trade_sheet = next((s for s in xl.sheet_names if "Trade" in s or "trade" in s.lower() or "list" in s.lower()), None)
    if trade_sheet:
        trades = pd.read_excel(path, sheet_name=trade_sheet)
        print(f"\n--- TRADES COUNT ({trade_sheet}) ---")
        print(f"Count: {len(trades)}")
        if len(trades) > 0:
            print("First row:", trades.iloc[-1].to_dict())
            print("Last row:", trades.iloc[0].to_dict())
    else:
        print(f"Could not find a valid trade sheet among {xl.sheet_names}")
    
except Exception as e:
    import traceback
    traceback.print_exc()
