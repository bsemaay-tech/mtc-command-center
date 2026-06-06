# Deterministic Spec — Market Wizards Sell Rules Overlay (QL_SELL_RULES_MARKET_WIZARDS_OVERLAY)

> Source: Market Wizards sell rules intake (Linda Raschke, Mark Minervini, David Ryan, et al.).
> Promoted to parity candidate in prior system. No active producer_spec.json.
> Spec reconstructed from strategy name and the Market Wizards sell-rule framework.

## Universe
- US equities (growth stocks), 1D bars.
- Overlay: systematic sell/exit rules applied to any existing long position.

## Concept
Systematize the most cited sell rules from Market Wizards interviews (Minervini, O'Neil,
Raschke, Ryan) into an overlay that governs when to reduce or exit a long position.
Not an entry signal — purely an exit/risk discipline layer.

## Sell rules (from interviews, systematized)

### Rule 1: Stop-Loss (O'Neil / Minervini)
```
exit_stop = close <= entry_price × 0.92     # 8% from entry (O'Neil's max loss rule)
```

### Rule 2: Moving Average Break (Ryan / Minervini)
```
exit_ma = close < SMA(close, 50)            # 50-day MA break = exit
```
For shorter hold: `close < EMA(close, 21)`

### Rule 3: Climax / Extension (Linda / Minervini)
```
extended = close > SMA(close, 50) × 1.25   # 25%+ above 50 SMA (climax run)
exit_extension = extended AND (volume > SMA(volume, 50) × 2.0)  # on high volume
```

### Rule 4: Trend Break (Weinstein stage)
```
exit_stage = SMA(close, 150) < SMA(close, 150)[5]    # 30-week MA turning down
```

### Rule 5: Loss of RS
```
rs_losing = (close / close[5]) < (SPY / SPY[5]) × 0.97    # underperforming SPY by 3% in 1 week
```

## Composite exit signal
```
exit_long = exit_stop OR exit_ma OR exit_extension OR exit_stage
```
(RS loss is a soft signal — reduce size; not necessarily full exit.)

## Data requirements
- 1D OHLCV with volume
- Benchmark OHLCV (SPY) for RS calculation
- Minimum 200 bars warmup (for 150-day MA)

## Disposition
Overlay / exit-rule framework. Apply as the exit layer on top of any long producer entry.
Not an entry signal. Not approved for live trading as a standalone system.
