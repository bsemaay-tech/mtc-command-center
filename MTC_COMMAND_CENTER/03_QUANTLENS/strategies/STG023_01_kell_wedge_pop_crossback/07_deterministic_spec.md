# Deterministic Spec — Kell Wedge Pop / Crossback 10/20 EMA (QL_KELL_WEDGE_POP_CROSSBACK_10_20EMA_v0)

> Source: Oliver Kell price-cycle intake report. Research-only Python batch
> 2026-05-03. Signal logic from `run_batch.py::signal_kell()`. No Pine, no MTC
> production integration.

## Universe
- Crypto (BTC, ETH, SOL, BNB, XRP), 1D and 4h bars.
- Research proxy for Oliver Kell's 10/20 EMA price-cycle system.

## Indicators
```
e10       = EMA(close, 10)
e20       = EMA(close, 20)
atr       = ATR(14)
base_range = (highest(high, N) - lowest(low, N)) / close × 100    # N-bar range as % of price
```

## Variants tested (best: basin_break at 1D)

### A. wedge_pop
```
long_entry = (close > e20)                                              # trend filter
           AND (base_range[1] <= max_range)                            # prior bar had tight base (<=8%)
           AND (close > highest(high, N)[1])                           # close breaks above N-bar high
```

### B. ema_crossback
```
long_entry = (close > e20)
           AND (close[1] < e10[1])                                     # prior bar below EMA10
           AND (close > e10)                                           # crossback above EMA10
```

### C. basin_break (best variant)
```
long_entry = (close > e20)
           AND (base_range[1] <= max_range)                            # tight base condition
           AND (close > e10)                                           # above EMA10
           AND (close > highest(close, 10)[1])                         # 10-bar closing high breakout
```

### D. ma_ride_exit (default)
```
long_entry = (close > e20)
           AND (low <= e10 × 1.01)                                     # touch/near EMA10
           AND (close > e10)
```

## Stop
- Default: `close − 2 × ATR`
- Alternative: `lowest(low, N)[1]` (N-bar low)

## Target
`close + 3 × (close − stop)`

## Trailing exit
`close < e20` → exit next bar open

## Best tested parameters
`{"contraction": 8, "max_range": 5, "stop_mode": "ATR_2", "variant": "basin_break"}`

## Research classification
**WEAK_CANDIDATE** — LOW_SAMPLE: too few 1D trades for promotion.
4h shows edge (1840 trades, PF 1.24 aggregate) but drawdown risk high (-44% to -56% per asset).

## Backtesting risks
- Crypto proxy for equity method (Oliver Kell trades US equities).
- 1D sample too small for statistical significance.
- High per-asset drawdowns on 4h.

## Disposition
Research-only. WEAK_CANDIDATE. Not for Pine or MTC production. Revisit as filter component
or combined with stage/regime gate.
