# Deterministic Spec — Brian Shannon AVWAP Intraday Opening Range 5m (QL_AVWAP_BRIAN_INTRADAY_OR_5M)

> Source: Brian Shannon AVWAP methodology. Promoted to parity candidate in prior system.
> No active producer_spec.json. Spec reconstructed from strategy name and Shannon's framework.

## Universe
- US equities (liquid, moderate-to-large cap), 5m intraday bars.
- Requires 5m OHLCV with session timestamps.

## Concept
Combine the session AVWAP with the Opening Range (OR = high/low of the first 30 minutes).
Trade when price breaks out of the OR in the direction of the AVWAP trend.

## Indicators
```
session_avwap = VWAP anchored at 09:30 ET session open (resets daily)
or_high       = highest(high, first 6 bars × 5m = 30 minutes from 09:30)
or_low        = lowest(low, first 6 bars × 5m = 30 minutes from 09:30)
avwap_slope   = session_avwap > session_avwap[5]     # AVWAP trending up
```

## Signal definition
```
# Long: OR breakout with AVWAP support
long_entry  = (close > or_high)                     # breaks OR high
            AND (close > session_avwap)             # above AVWAP (AVWAP is support)
            AND avwap_slope                          # AVWAP trending up
            AND (bar_index > 6)                      # after OR formation period

# Short: OR breakdown with AVWAP resistance
short_entry = (close < or_low)
            AND (close < session_avwap)
            AND NOT avwap_slope
            AND (bar_index > 6)
```

## Stop
- Long: `stop = or_low` or `session_avwap × 0.99`
- Short: `stop = or_high` or `session_avwap × 1.01`

## Target
Next key level; or session close. Trail via AVWAP.

## Data requirements
- 5m OHLCV with 09:30 ET session anchor
- Session reset logic for AVWAP
- Opening range calculation (first 30 minutes)

## Known risks
- OR breakouts fail frequently in choppy markets; volume confirmation is critical.
- AVWAP direction can conflict with OR direction in mixed sessions.
- Session-bound: not applicable to 24h crypto.

## Disposition
Parity candidate (blocked by missing 5m intraday data). Not approved for live trading.
