# Deterministic Spec — Linda 8am ET Opening Range Breakout (QL_8AM_ET_OPENING_RANGE_BREAKOUT_v0)

> Source: Linda Raschke process strategy intake. Research-only Python batch 2026-05-03.
> **BLOCKED_DATA**: requires 5m OHLCV with 08:00 ET session anchor — not available in repo.
> No signal code was run.

## Universe
- US equities or liquid US-session futures, 5m bars.
- Requires intraday 5m data with session timestamps anchored to 08:00–09:30 ET pre-market open.

## Concept
Linda Raschke's 8am Opening Range: the range formed in the first 30 minutes from 8am ET
(or the first bar after 8am) defines resistance and support. Trade the breakout of that range
on 5m bars, typically targeting the 09:30 regular-session open as a catalyst.

## Expected signal logic (not implemented — blocked)
```
or_high = highest(high from 08:00 ET bar, first 30 min)    # opening range high
or_low  = lowest(low from 08:00 ET bar, first 30 min)      # opening range low

long_entry  = close > or_high    # breakout above OR high
short_entry = close < or_low     # breakdown below OR low
stop_long   = or_low             # stop at OR low for longs
stop_short  = or_high            # stop at OR high for shorts
```

## Data requirements (not met in current repo)
- 5m OHLCV data for at least 5 liquid assets with 08:00 ET session timestamps
- Session filter: 08:00–16:00 ET
- Premarket volume confirmation (optional but important)

## Research classification
**BLOCKED_DATA** — Cannot be tested without the required dataset.

## Known risks
- Strong opening ranges often have false breakouts; requires volume confirmation.
- Gap opens can put price outside the OR before the session begins.
- Specific to US equity/futures session timing; not applicable to 24h crypto.

## Disposition
Blocked. Acquire 5m intraday data with ET session anchor before resuming.
Concept is well-validated in Linda Raschke's published work.
