# Deterministic Spec — Martin/Luke Pullback to EMA/AVWAP (QL_MARTIN_LUKE_PULLBACK_AVWAP_v0)

> Source: Martin/Luke pullback intake report. Research-only Python batch 2026-05-03.
> Signal logic from `run_batch.py::signal_martin()`. No Pine, no MTC production integration.

## Universe
- Crypto (BTC, ETH, SOL, BNB, XRP), 1D and 4h bars.

## Indicators
```
e9, e21, e50, e150 = EMA(close, 9/21/50/150)
avwap_high = rolling_vwap_proxy(data, 80)    # 80-bar volume-weighted avg
avwap_low  = rolling_vwap_proxy(data, 34)    # 34-bar volume-weighted avg
```

## Signal definition

### Trend filter (all variants)
```
trend = (close > e50) AND (e50 > e150)    # price above rising 50 EMA in long-term uptrend
```

### Support conditions
```
ema_support   = (low <= e21 × 1.015) OR (low <= e50 × 1.015)       # touch within 1.5% of EMA
avwap_support = (low <= avwap_high × 1.015) OR (low <= avwap_low × 1.015)
```

### Variants tested
- **ema_only**: `support = ema_support`
- **avwap_only**: `support = avwap_support`
- **ema_avwap**: `support = ema_support AND avwap_support`
- **ema_avwap_prior** (best): `support = ema_support AND avwap_support AND (low <= highest(high, 20)[1] × 1.02)`

### Entry trigger (all variants)
```
prior_reclaim = close > high[1]       # close above prior bar high (strength confirmation)
long_entry = trend AND support[1] AND prior_reclaim
```
Short: none.

## Stop
```
stop = max(lowest(low, 3)[1], close × 0.97)    # low of 3 bars OR 3% hard floor
```

## Target
`close + 3 × (close − stop)`

## Trailing exit
`close < e21` → exit next bar open

## Research classification
**WEAK_CANDIDATE** — Edge exists but robustness and symbol-level drawdown not strong enough.
PF 1.24 aggregate across assets, but per-asset drawdowns reach -40 to -50%.

## Backtesting risks
- AVWAP proxy (rolling VWAP) is a simplification; real AVWAP uses a chosen anchor date.
- High drawdown per asset; regime-sensitive.
- Not tested on US equities (the primary target market for this method).

## Disposition
Research-only. WEAK_CANDIDATE. Suitable for filter/gate experiments or as an entry confirmation
component in a system with a stronger trend filter.
