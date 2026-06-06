# Deterministic Spec — Minervini VCP Pivot Breakout 1D (QL_VCP_MINERVINI_1D)

> Source: Mark Minervini VCP (Volatility Contraction Pattern) intake. Promoted to parity candidate
> in prior system. No active producer_spec.json. Spec reconstructed from Minervini's published method.

## Universe
- US equities (growth stocks with strong fundamentals), 1D bars.
- Minervini's SEPA (Specific Entry Point Analysis) method.

## Concept
The VCP is a base pattern where price makes decreasing-depth pullbacks (contractions) with drying
volume, ending in a tight handle. Buy the breakout above the pivot point (high of the tightest
contraction) on strong volume.

## Trend template criteria (Minervini SEPA pre-filter)
```
# All must be true for a qualifying setup
T1 = close > SMA(close, 200)             # above 200 SMA
T2 = SMA(close, 200) > SMA(close, 200)[20]  # 200 SMA trending up for 1 month
T3 = SMA(close, 50) > SMA(close, 150)   # medium > long-term MA
T4 = SMA(close, 50) > SMA(close, 200)   # medium > very long-term
T5 = SMA(close, 150) > SMA(close, 200)  # long > very long-term
T6 = close > SMA(close, 50)             # price above 50 SMA
T7 = close >= close[252] × 1.25         # at least 25% above 52-week low
T8 = close >= close[63] × 0.75          # within 25% of 52-week high

trend_template = T1 AND T2 AND T3 AND T4 AND T5 AND T6 AND T7 AND T8
```

## VCP pattern detection (simplified systematic proxy)
```
atr = ATR(14)
volume_ma20 = SMA(volume, 20)

# Handle: recent 3–5 bars are tight (VCP final contraction)
recent_range_pct = (highest(high, 5) - lowest(low, 5)) / close × 100
tight_handle     = recent_range_pct <= 5.0
vol_drying       = SMA(volume, 5) < volume_ma20 × 0.5

# Pivot: high of the tight handle period
pivot = highest(high, 5)[1]
```

## Signal definition
```
long_entry = trend_template
           AND tight_handle
           AND vol_drying[1]
           AND (close > pivot)                   # closes above pivot (breakout)
           AND (volume > volume_ma20 × 1.5)     # volume surge on breakout
```
Short: none.

## Stop
`stop = lowest(low, 5)[1]` (handle low) or `entry × 0.92` (8% rule).

## Target
Typically 20–30%+ gain target; trail with 50 SMA.

## Data requirements
- 1D OHLCV with volume
- Minimum 252 bars warmup (52-week comparison)

## Known risks
- Trend template requires all 8 conditions — very restrictive; low trade frequency.
- VCP detection is partially discretionary in the original method.
- Systematic proxy (tight handle + volume dry) is a simplification; many failed breakouts pass.
- Fundamental criteria (EPS growth, RS) not capturable from price data.

## Disposition
Parity candidate. Not approved for live trading. Systematic price-only proxy for Minervini's VCP;
real implementation requires fundamental + RS screening.
