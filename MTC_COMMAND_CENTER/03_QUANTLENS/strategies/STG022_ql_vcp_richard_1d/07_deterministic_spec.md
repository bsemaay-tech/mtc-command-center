# Deterministic Spec — Richard Moglen VCP 1D (QL_VCP_RICHARD_1D)

> Source: Richard Moglen VCP intake. Promoted to parity candidate in prior system.
> No active producer_spec.json. Spec reconstructed from strategy name and Richard's method.

## Universe
- US equities (growth stocks), 1D bars.
- Richard Moglen's variant of the VCP — slightly less restrictive than Minervini's SEPA,
  focused on practical entries with fewer pre-conditions.

## Concept
Richard Moglen's VCP approach emphasizes the pattern itself (decreasing volatility contractions)
without requiring the full 8-point trend template. Key focus: price must be in a clear uptrend,
base must be showing 3+ contractions, and the final handle must be unusually tight before breakout.

## Indicators
```
atr = ATR(14)
volume_ma20 = SMA(volume, 20)
sma50  = SMA(close, 50)
sma200 = SMA(close, 200)
```

## Trend filter (simplified vs Minervini)
```
uptrend = (close > sma50) AND (sma50 > sma200)
```

## VCP detection proxy
```
# Measure contraction depth over rolling windows
c1_depth = (highest(high, 30) - lowest(low, 30)) / highest(high, 30) × 100   # outer base
c2_depth = (highest(high, 15) - lowest(low, 15)) / highest(high, 15) × 100   # mid contraction
c3_depth = (highest(high,  5) - lowest(low,  5)) / highest(high,  5) × 100   # final handle

# Contracting structure: each depth smaller than the prior
contracting = (c3_depth < c2_depth) AND (c2_depth < c1_depth)

# Handle tight
tight_handle = c3_depth <= 8.0         # Richard's threshold: < 8% in final handle
vol_dry      = SMA(volume, 5) < volume_ma20 × 0.6

# Pivot level
pivot = highest(high, 5)[1]
```

## Signal definition
```
long_entry = uptrend
           AND contracting
           AND tight_handle
           AND vol_dry[1]
           AND (close > pivot)                  # breakout above handle pivot
           AND (volume > volume_ma20 × 1.3)    # volume confirms (less strict than Minervini)
```
Short: none.

## Stop
`stop = lowest(low, 3)[1]` or `sma50 × 0.97`.

## Target
20%+ gain. Trail with sma50.

## Data requirements
- 1D OHLCV with volume
- Minimum 200 bars warmup

## Key difference from STG021 (Minervini VCP)
- No 8-point trend template requirement → more trades, lower quality threshold
- Wider handle definition (8% vs 5%)
- Lower volume breakout requirement (1.3× vs 1.5×)

## Disposition
Parity candidate. Not approved for live trading. Looser criteria than STG021 — higher frequency,
lower precision. Best combined with fundamental RS screening.
