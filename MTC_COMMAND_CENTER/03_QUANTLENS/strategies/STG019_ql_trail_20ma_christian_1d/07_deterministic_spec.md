# Deterministic Spec — Christian Flanders Trail 20MA 1D (QL_TRAIL_20MA_CHRISTIAN_1D)

> Source: Christian Flanders trailing exit method. Promoted to parity candidate in prior system.
> No active producer_spec.json. Spec reconstructed from strategy name.

## Universe
- US equities (growth / momentum stocks), 1D bars.
- Exit rule overlay: trail positions with the 20-day MA.

## Concept
Christian Flanders' trailing exit discipline: once in a strong trend, trail the position using
the 20-day (4-week) moving average as the stop. Exit when the stock closes below the 20 MA.
This captures large trend moves while giving the stock room to breathe.

## Indicators
```
ma20 = SMA(close, 20)    # 20-day simple moving average (or EMA in some implementations)
```

## Exit rule (overlay)
```
trail_exit = close < ma20    # exit when daily close drops below 20 MA
```

Applied to any existing long position entered from a producer signal.

## Combined entry + trail (standalone variant)
```
# Entry: buy the first close above 20 MA after a pullback
pulled = (close < ma20) in any of last 5 bars
entry  = pulled.shift(1) AND (close > ma20)

# Exit: trail with 20 MA
exit = close < ma20
```

## Position management
```
# On first new high after entry, move stop to entry price (breakeven)
trail_up = close > entry_price × 1.10    # 10% gain → trail stop to entry
```

## Data requirements
- 1D OHLCV
- Minimum 20 bars warmup

## Known risks
- 20 MA can be breached and recovered in sideways markets (whipsaws).
- Choppy markets with frequent 20 MA crosses destroy this trailing approach.
- For volatile stocks, may need 10 MA or ATR-based trail instead.
- Best suited for stocks in Stage 2 uptrends with few pauses.

## Disposition
Parity candidate / exit overlay. Not an entry signal generator on its own.
Use as trailing exit rule for positions entered via any producer strategy.
Not approved for live trading.
