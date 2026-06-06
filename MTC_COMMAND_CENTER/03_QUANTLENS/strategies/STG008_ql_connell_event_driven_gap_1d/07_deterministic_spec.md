# Deterministic Spec — Andrew Connell Event-Driven Gap 1D (QL_CONNELL_EVENT_DRIVEN_GAP_1D)

> Source: Andrew Connell event-driven gap intake. Promoted to parity candidate in prior system.
> No active producer_spec.json. Spec reconstructed from strategy name and Connell's method.

## Universe
- US equities (individual stocks), 1D bars.
- Event-driven: earnings surprise, guidance raise, FDA approval, contract win, etc.

## Concept
Andrew Connell's event-driven setup: buy a stock that gaps up strongly on an unexpected positive
catalyst. The gap creates a new baseline; hold as long as it holds above the gap support.
The key filter: the company must have improving fundamentals + institutional interest (not purely
technical).

## Indicators
```
gap_pct   = (open / close[1] - 1) × 100    # gap size as % of prior close
vol_ratio = volume / SMA(volume, 50)       # volume surge ratio
```

## Signal definition (long, reconstructed)
```
gap_up     = gap_pct >= 5.0                            # gaps at least 5% (significant event)
vol_surge  = vol_ratio >= 2.0                          # 2x+ average volume (institutional)
holds_gain = close >= open × 0.97                      # closes near the gap open (no immediate fade)

long_entry = gap_up AND vol_surge AND holds_gain        # on the gap day itself (1D bar)
```
Or alternative: **buy the first pullback to the gap on the day after** (safer entry).

## Stop
`stop = low of gap day` — if price fills back to pre-gap, thesis is broken.

## Target
Trail with 21 EMA or AVWAP anchored at gap open date.

## Data requirements
- 1D OHLCV with volume
- Prior-day close for gap calculation
- Catalyst news feed (optional but improves quality filtering)

## Known risks
- Event-driven gaps without fundamental support often reverse; gap day entry has high false-positive rate.
- First pullback entry (day 2+) misses the initial move but has better R:R.
- Not backtestable without fundamental catalyst filter — pure price/volume proxy overfits.

## Disposition
Parity candidate. Not approved for live trading. Best implemented with a fundamental news feed
for catalyst quality filtering.
