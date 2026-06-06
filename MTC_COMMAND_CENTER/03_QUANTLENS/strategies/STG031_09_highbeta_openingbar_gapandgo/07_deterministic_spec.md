# Deterministic Spec — High-Beta Opening Bar Gap and Go (QL_HIGHBETA_OPENINGBAR_GAPANDGO_v0)

> Source: Process strategy intake (Linda Raschke / gap-and-go framework). Research-only batch
> 2026-05-03. **BLOCKED_DATA**: no US high-beta intraday equities or 5m crypto session data.

## Universe
- US high-beta intraday equities, 5m bars.
- Requires: pre-market gap data, 5m OHLCV with session open identification, market cap / beta filters.

## Concept
High-beta stocks that gap up (or down) at the open tend to continue in the gap direction for the
first 15–30 minutes if volume confirms. Entry is on the 5m opening bar close, riding the gap
continuation.

## Expected signal logic (not implemented — blocked)
```
gap_up  = open > close[1] × 1.01              # opens >= 1% above prior close
gap_dn  = open < close[1] × 0.99              # opens >= 1% below prior close
vol_ok  = volume[0] > avg_volume × 1.5        # opening bar volume elevated

# Entry: buy the close of the 5m opening bar on gap-up (or sell on gap-down)
long_entry  = gap_up AND vol_ok AND (is_first_bar_of_session)
short_entry = gap_dn AND vol_ok AND (is_first_bar_of_session)

stop_long  = open - ATR × 0.5                 # tight stop below open
stop_short = open + ATR × 0.5
target_long = open + ATR × 1.5                # 3:1 R (approximate)
```

## Data requirements (not met in current repo)
- US high-beta equity 5m OHLCV with session gap identification
- Pre-market close price for gap calculation
- Beta > 1.5 universe filter
- Liquidity filter (avg volume > 1M shares/day)

## Research classification
**BLOCKED_DATA** — Cannot be tested without the required dataset.

## Known risks
- Gap-and-go fails on news-driven gaps (reversion risk).
- High-beta intraday requires strict risk management (fast moves, wide spreads).
- Locating data with accurate pre-market closes is non-trivial.

## Disposition
Blocked. Acquire US intraday equity 5m data with pre-market gap detection before resuming.
