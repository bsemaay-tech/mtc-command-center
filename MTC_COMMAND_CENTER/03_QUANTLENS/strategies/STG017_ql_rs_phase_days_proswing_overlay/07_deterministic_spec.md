# Deterministic Spec — RS Phase Days ProSwing Overlay (QL_RS_PHASE_DAYS_PROSWING_OVERLAY)

> Source: ProSwing RS phase days intake. Promoted to parity candidate in prior system.
> No active producer_spec.json. Spec reconstructed from strategy name.

## Universe
- US equities (growth stocks), 1D bars.
- Overlay / filter: applied on top of entry signals from a producer strategy.

## Concept
"RS Phase Days" tracks how many consecutive days a stock has been outperforming its benchmark
(e.g., SPY). Stocks in a sustained RS phase have persistent institutional buying momentum.
This overlay gates entries to only fire when RS has been positive for N+ consecutive days.

## Indicators
```
# Relative strength vs benchmark
rs_daily   = (close / close[1]) / (spy / spy[1]) - 1    # daily return relative to SPY
             (positive = outperformed SPY today)

# Count consecutive RS-positive days
rs_phase_days = consecutive bars where rs_daily > 0
```

## Overlay logic
```
min_rs_phase = 5    # require at least 5 consecutive RS-positive days before entry

overlay_pass = rs_phase_days >= min_rs_phase   # stock has been outperforming for N days

# Use as gate on any producer entry:
final_entry = producer_signal AND overlay_pass
```

## Additional RS filters
```
rs_vs_52w_high = close / highest(close, 252) - 1   # distance from 52-week high (relative strength proxy)
rs_52w_strong  = rs_vs_52w_high >= -0.20           # within 20% of 52-week high
```

## Data requirements
- 1D OHLCV for the stock
- Benchmark 1D OHLCV (SPY or relevant index) for RS calculation
- Minimum 5 bars warmup (for RS phase count)

## Known risks
- RS phase streaks can break suddenly on sector rotation or market event.
- Benchmark selection significantly impacts RS calculation.
- Using longer RS phase requirements (>10 days) reduces trade frequency sharply.

## Disposition
Overlay / filter. Not an entry signal generator. Use to ensure entries occur in stocks
with sustained institutional momentum (RS phase). Not approved for live trading.
