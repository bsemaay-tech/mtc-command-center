# Deterministic Spec — Christian Flanders Open Range 5% Stop 5m (QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M)

> Source: Christian Flanders open range method. Promoted to parity candidate in prior system.
> No active producer_spec.json. Spec reconstructed from strategy name.

## Universe
- US equities (liquid, large-cap), 5m intraday bars.
- Session: 09:30–16:00 ET.

## Concept
Trade the opening range breakout (first 30 minutes) with a predefined 5% stop from the opening
range low. Simple, mechanical: buy the OR breakout, stop is 5% below entry.

## Indicators
```
or_high = highest(high from 09:30 to 10:00 ET)    # opening range high (first 30 min)
or_low  = lowest(low from 09:30 to 10:00 ET)       # opening range low
atr     = ATR(14, on 5m bars)
```

## Signal definition
```
# After 10:00 ET (OR formation complete)
long_entry  = (close > or_high) AND (bar_index_since_open >= 6)
short_entry = (close < or_low)  AND (bar_index_since_open >= 6)
```

## Stop
- Long: `stop = entry × 0.95` (5% from entry)
- Short: `stop = entry × 1.05` (5% from entry)
- Alternative: `stop = or_low` (structural stop below the opening range low)

## Target
- R-multiple based: `target = entry + 2 × (entry - stop)` (2R)
- Or: prior day high / resistance level

## Data requirements
- 5m OHLCV with 09:30 ET session anchor
- Session filter for OR calculation period

## Known risks
- 5% stop is too wide for intraday trades on most equities (especially large-cap).
- Simple OR breakout has low win rate without additional filters (trend, volume, sector).
- Not testable in repo (no 5m intraday data with session anchor).

## Disposition
Parity candidate (blocked by missing 5m data). Not approved for live trading.
The 5% fixed stop is a conservative setting that allows riding volatile stocks; tune for the asset.
