# Deterministic Spec — Brian Shannon AVWAP Stage2 Emerging 1D (QL_AVWAP_BRIAN_STAGE2_EMERGING_1D)

> Source: Brian Shannon AVWAP methodology. Promoted to parity candidate in prior system.
> No active producer_spec.json. Spec reconstructed from strategy name and Shannon's framework.

## Universe
- US equities (individual stocks), 1D bars.
- Stage 2 stocks (Weinstein stage — above rising 30-week MA, breaking out of base).

## Concept
Combine Brian Shannon's AVWAP (anchored at IPO, earnings, or all-time-high) with Stan
Weinstein's Stage 2 criteria. Buy when a Stage 2 emerging stock finds support at its
AVWAP(IPO or all-time-high) for the first time after breaking out — a high-probability
continuation entry.

## Stage 2 criteria (Weinstein proxy)
```
ma30w = SMA(close, 150)               # ~30 week SMA on daily data
stage2 = (close > ma30w)             # price above 30-week MA
       AND (ma30w > ma30w[20])       # 30-week MA rising (trending up)
```

## AVWAP anchor
- Preferred: AVWAP from the most recent base breakout date
- Fallback: AVWAP from 52-week low or prior significant low

```
avwap_base = VWAP anchored at base_breakout_date
```

## Signal definition (long only)
```
trend_ok   = stage2                                          # Stage 2 condition
avwap_supp = (low <= avwap_base × 1.02)                    # price touches AVWAP support
reclaim    = close > avwap_base                             # closes above AVWAP
vol_ok     = volume > SMA(volume, 50) × 0.8               # not on drying volume

long_entry = trend_ok AND avwap_supp[1] AND reclaim AND vol_ok
```
Short: none.

## Stop
`stop = avwap_base × 0.97` — 3% below AVWAP (invalidation).

## Target
Trail: exit when close < MA30w or AVWAP starts declining over 5+ days.

## Data requirements
- 1D OHLCV with 150 bars minimum (30-week MA warmup)
- Earnings/breakout dates for AVWAP anchor (manual or feed)

## Known risks
- Stage 2 identification is partially discretionary in the original Weinstein method.
- AVWAP anchor date selection significantly impacts the level.
- Long-only, bull-market dependent.

## Disposition
Parity candidate. Not approved for live trading. Requires anchor date feed for live use.
