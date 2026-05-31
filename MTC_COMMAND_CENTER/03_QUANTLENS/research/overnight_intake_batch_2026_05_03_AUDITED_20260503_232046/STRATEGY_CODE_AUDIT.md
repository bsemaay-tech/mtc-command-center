# Strategy Code Audit
1. Found minor issue in first-run `strategy_LBR_COIL.py`: it assumed fill at trigger price even if the bar gapped above the trigger. Fixed in audited script `entry_price = max(row['open'], row['buy_trigger'])`.
2. Metric calculations for drawdown and profit factor were structurally sound but now run on the gap-adjusted trades.
