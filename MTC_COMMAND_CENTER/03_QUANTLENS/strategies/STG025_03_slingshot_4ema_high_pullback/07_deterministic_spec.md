# Deterministic Spec — Slingshot 4EMA High Pullback (QL_SLINGSHOT_4EMA_HIGH_PULLBACK_v0)

> Source: Slingshot pullback intake. Research-only Python batch 2026-05-03.
> Signal logic from `run_batch.py::signal_slingshot()`. No Pine, no MTC production integration.

## Universe
- Crypto (BTC, ETH, SOL, BNB, XRP), 1D bars.

## Concept
Price makes an impulse move (slingshot), then pulls back to EMA of highs, then re-crosses above it.
Entry triggers on the crossback = continuation of the impulse.

## Indicators
```
eh = EMA(high, ema_len)           # EMA of highs (default ema_len=4)
sma50 = SMA(close, 50)
atr = ATR(14)
```

## Signal definition
```
strength = close > sma50                             # trend filter: price above 50 SMA

pulled = any(close < eh) in last [lookback] bars     # was below EMA-high recently (pulled back)

high_ref = highest(high, lookback)
depth_ok = (high_ref - lowest(low, lookback)) / high_ref × 100 <= depth   # pullback depth not too deep

cross = (close > eh) AND (close[1] <= eh[1])         # crossback above EMA-high

long_entry = strength AND pulled[1] AND depth_ok AND cross
```

## Stop
- Default: `lowest(low, lookback)[1]`
- ATR_trail variant: `close - 2 × ATR`

## Target
- R2 variant: `close + 2 × (close − stop)`
- R3 (default): `close + 3 × (close − stop)`

## Trailing exit
`close < eh` → exit next bar open (close_below variant)

## Best tested parameters (best scored)
`{"ema_len": [3-8], "lookback": [3-13], "depth": [5-25], "exit_mode": "close_below|R3"}`

## Research classification
**WEAK_CANDIDATE** — LOW_SAMPLE: too few trades for promotion (daily timeframe).

## Backtesting risks
- Very few 1D trades — statistical significance low.
- "Depth" filter is a lookahead over the pullback window; ensure lookback uses historical bars only.
- EMA of highs is non-standard; verify broker/backtesting engine calculates it correctly.

## Disposition
Research-only. WEAK_CANDIDATE. Best tested on 1D. May have value as entry timing component
within a broader trend system.
