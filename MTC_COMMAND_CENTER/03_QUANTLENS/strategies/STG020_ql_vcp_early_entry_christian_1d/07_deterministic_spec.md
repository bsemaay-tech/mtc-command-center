# Deterministic Spec — Christian Flanders VCP Early Entry 1D (QL_VCP_EARLY_ENTRY_CHRISTIAN_1D)

> Source: Christian Flanders VCP early entry intake. Promoted to parity candidate in prior system.
> No active producer_spec.json. Spec reconstructed from strategy name.

## Universe
- US equities (growth stocks), 1D bars.
- Early entry into VCP (Volatility Contraction Pattern) before the formal pivot breakout.

## Concept
The classic VCP (Minervini) entry is at the pivot breakout. Christian Flanders' early entry
variant enters during the last contraction of the VCP — before price breaks the pivot — for
better R:R. Requires recognition that the VCP structure is forming.

## VCP Structure (simplified)
```
# 3-4 contractions of decreasing depth and range
contraction_1: 25–30% depth from prior high
contraction_2: 15–20% depth
contraction_3: 8–12% depth
contraction_4 (final): 3–5% depth (tight handle)
```

## Indicators
```
atr = ATR(14)
volume_ma20 = SMA(volume, 20)

# Depth of current contraction
contraction_depth = (highest(high, 20) - lowest(low, 20)) / highest(high, 20) × 100
volume_dry        = SMA(volume, 5) < volume_ma20 × 0.6    # volume drying in handle
```

## Signal definition (early entry, reconstructed)
```
# VCP is forming: at least 3 prior contractions, currently in final tight contraction
final_contraction = contraction_depth <= 5.0    # final handle: ≤ 5% range
vol_dry_confirmed = volume_dry                   # volume is drying in the handle
trend_ok          = close > SMA(close, 200)     # still in uptrend

long_entry = trend_ok AND final_contraction AND vol_dry_confirmed
           AND (close > SMA(close, 50))          # above 50 SMA (not breaking down)
```
Short: none.

## Stop
`stop = lowest(low, 3)[1]` — low of the contraction handle.

## Target
The formal VCP pivot breakout level + 10–20%.

## Data requirements
- 1D OHLCV with volume
- Minimum 200 bars warmup

## Known risks
- Early entry increases risk of entering before the pattern completes (failed VCP).
- Contraction depth detection with rolling high/low does not perfectly identify VCP contractions.
- Manual pattern recognition is still required to confirm the 3–4 contraction sequence.

## Disposition
Parity candidate. Not approved for live trading. Best combined with manual chart review or
pattern-scanning software. The systematizable component (tight range + drying volume) is valid
as an entry filter.
