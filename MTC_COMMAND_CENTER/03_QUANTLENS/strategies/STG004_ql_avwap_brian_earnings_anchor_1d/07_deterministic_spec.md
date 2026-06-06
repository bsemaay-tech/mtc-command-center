# Deterministic Spec — Brian Shannon AVWAP Earnings Anchor 1D (QL_AVWAP_BRIAN_EARNINGS_ANCHOR_1D)

> Source: Brian Shannon AVWAP methodology. Promoted to parity candidate in prior system.
> No active producer_spec.json — this spec reconstructs the method from the strategy name
> and Brian Shannon's published AVWAP framework.

## Universe
- US equities (individual stocks), 1D bars.
- Requires earnings date annotation or quarterly date anchor.

## Concept
Anchor a VWAP at the most recent earnings release date. The AVWAP(earnings) becomes a key
dynamic support/resistance level. Price finding support at AVWAP(earnings) in an uptrend is
a high-probability buy zone.

## Indicators
```
avwap_earnings = VWAP anchored at the most recent quarterly earnings date
                 = cumulative sum(OHLC/4 × volume, from earnings date) / cumulative sum(volume, from earnings date)
```

## Signal definition (long only, reconstructed)
```
trend_ok     = close > SMA(close, 200)           # long-term trend filter
approaching  = low <= avwap_earnings × 1.02      # price within 2% of AVWAP
reclaim      = close > avwap_earnings            # bar closes above AVWAP (reclaim)
volume_ok    = volume > SMA(volume, 20)          # above-average volume

long_entry = trend_ok AND approaching[1] AND reclaim AND volume_ok
```
Short: none (long-only).

## Stop
`stop = avwap_earnings × 0.98` — 2% below AVWAP (invalidation of support).

## Target
No fixed target. Trail via AVWAP or next quarterly earnings anchor.

## Data requirements
- Earnings date calendar for each symbol
- OHLCV daily with volume (for AVWAP computation)
- Minimum: stock must have at least 1 earnings event in data history

## Known risks
- AVWAP requires an anchor date — backtesting must replay the earnings date in sequence.
- Gap opens on earnings day can distort the initial AVWAP value significantly.
- Long-only and earnings-driven; performs poorly in bear markets.

## Disposition
Parity candidate. Not approved for live trading. Requires earnings date feed for live implementation.
