# Deterministic Spec — Linda 5SMA RS Pullback (QL_LINDA_5SMA_RS_PULLBACK_v0)

> Source: Linda Bradford Raschke process strategy intake. Research-only Python batch 2026-05-03.
> Signal logic from `run_batch.py::signal_linda()`. No Pine, no MTC production integration.

## Universe
- Crypto (BTC, ETH, SOL, BNB, XRP), 1D bars.
- Based on Linda Raschke's 5-period SMA pullback / mean-reversion entry in trending markets.

## Indicators
```
ma5   = SMA(close, 5)
ma50  = SMA(close, 50)
ma200 = SMA(close, 200)
```

## Signal definition (long only)
```
trend = (close > ma50) AND (close > ma200)     # dual MA trend filter (both medium + long term)

# Setup: prior bar closed above or on ma5, then current bar dips below → mean-reversion setup
long_entry = trend
           AND (close[1] >= ma5[1])             # prior bar was at or above ma5
           AND (close < ma5)                    # current bar dipped below ma5 (pullback into ma5)
```
Short: none.

## Exit
```
exit_long = close > ma5    # price reclaims above ma5 → exit
```

## Stop options
- `"none"`: no hard stop (rely on exit signal only)
- `"ATR_2"`: `stop = close - 2 × ATR`
- `"fixed_8pct"`: `stop = close × 0.92`

## Key notes
- This is a short-duration trade: enter on ma5 dip, exit on ma5 reclaim (typically 1-3 bars).
- High frequency, low R:R; profitability depends on trend quality.
- No target (exit is always via ma5 reclaim or stop).

## Research classification
**WEAK_CANDIDATE** — Edge exists but robustness and symbol-level drawdown not strong enough.

## Backtesting risks
- Very short hold duration on 1D — execution timing matters significantly.
- No ATR or volatility filter → trades in choppy sideways periods reduce edge.
- Crypto 24h markets vs Linda's equity focus (session timing, gap behaviour differ).

## Disposition
Research-only. WEAK_CANDIDATE. The 5SMA pullback in a trend is a well-known tactical
concept (Linda's "Holy Grail" setup family). Best suited as a precision entry component
within a larger trend system rather than standalone.
