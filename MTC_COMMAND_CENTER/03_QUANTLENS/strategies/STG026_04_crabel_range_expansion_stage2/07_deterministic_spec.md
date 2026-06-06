# Deterministic Spec — Crabel Range Expansion Stage2 (QL_CRABEL_RANGE_EXPANSION_STAGE2_v0)

> Source: Crabel range expansion intake. Research-only Python batch 2026-05-03.
> Signal logic from `run_batch.py::signal_crabel()`. No Pine, no MTC production integration.

## Universe
- Crypto (BTC, ETH, SOL, BNB, XRP), 1D bars.
- Crabel's "Opening Range Breakout" adapted: prior-day close + fraction of prior range.

## Concept
Buy/sell stop orders placed above/below prior close by a fraction of the prior day's range.
If price exceeds the buy stop, long; if price drops to sell stop, short. If both trigger on the
same bar (whipsaw), no trade is taken.

## Indicators
```
prev_range = high[1] - low[1]                    # prior bar true range
buy_stop   = close[1] + prev_range × mult        # long trigger
sell_stop  = close[1] - prev_range × mult        # short trigger
```

## Signal definition
```
long_entry  = (high >= buy_stop)  AND NOT (long AND short on same bar)
short_entry = (low <= sell_stop)  AND NOT (long AND short on same bar)
```

### Optional filters
- **trend_filter**: `long_entry &= close[1] > EMA(close, 200)[1]`; `short_entry &= close[1] < EMA(200)[1]`
- **atr_filter**: only trade when ATR/price is above median but below 90th percentile (non-extreme volatility)

## Variants
- `direction_mode = "both"` (default), `"long_only"`, `"short_only"`
- `mult` tested: 0.5 to 1.5 (step 0.1)

## Stop
`stop = sell_stop` (for long); `stop = buy_stop` (for short)

## Target
No fixed target (mean-reversion logic; research only — exit not fully specified).

## Research classification
**WEAK_CANDIDATE** — Edge exists but robustness and symbol-level DD not strong enough.

## Backtesting risks
- Crabel ORB is intraday (5m/15m); daily adaptation loses the intraday timing edge.
- No explicit exit rule in research code — real implementation needs a target or trailing stop.
- Crypto futures are 24h; session open concept is not applicable.

## Disposition
Research-only. WEAK_CANDIDATE. The core range-expansion concept is valid but needs proper
intraday data and session-based implementation for its natural habitat.
