# Deterministic Spec — CANSLIM Shakeout Plus3 Crypto Proxy (QL_CANSLIM_SHAKEOUT_PLUS_3_v0)

> Source: CANSLIM intake. Research-only Python batch 2026-05-03.
> Signal logic from `run_batch.py::signal_canslim_proxy()`. No Pine, no MTC production integration.
> **Crypto proxy only** — does not prove the equity-specific CANSLIM rule.

## Universe
- Crypto (BTC, ETH, SOL, BNB, XRP), 1D bars.
- Proxy for O'Neil's CANSLIM "shakeout + 3" pattern.

## Concept
After a multi-week base, price shakes below a prior key low, then reclaims it. This "shake" is
a false breakdown that clears weak hands; the reclaim is the buy point. The "+3" refers to buying
3% above the base low that was shaken out.

## Indicators
```
uptrend = close / close[126] - 1 >= 0.30      # 6-month return >= 30% (CANSLIM uptrend proxy)
l1 = lowest(low, 40)[20]                      # 40-bar low, measured 20 bars ago
l2 = lowest(low, 20)                          # current 20-bar low (the shakeout)
shakeout = l2 < l1                            # current low broke below the prior key low
buy_point = l1 × 1.05  (if l1 > 60)          # 5% above prior key low (if level > 60)
          | l1 × 1.10  (if l1 < 30)          # 10% above prior key low (if level < 30)
          | l1 + 3     (else)                 # flat +3 points
```

## Signal definition
```
long_entry = uptrend AND shakeout[1] AND (high >= buy_point)
```

## Stop and target
```
stop   = buy_point × 0.93      # 7% below the buy point
target = buy_point × (1 + target_pct/100)   # default target_pct = 20%
```

## Key limitations
- `l1` is computed on a 40-bar rolling window 20 bars prior — valid (no lookahead).
- The `buy_point` formula using price levels (>60 / <30) is heuristic and symbol-price-dependent;
  not meaningful for crypto at arbitrary price levels.
- CANSLIM shakeout requires fundamental + institutional sponsorship analysis; not capturable from price alone.

## Research classification
**BASELINE_ONLY** — Crypto proxy is exploratory and cannot prove the equity-specific CANSLIM rule.

## Backtesting risks
- Price-level conditions (`if l1 > 60`) are nonsensical for crypto without normalization.
- No fundamental filter (earnings, RS, institutional sponsorship).
- Crypto proxy: CANSLIM shakeout pattern was designed for fundamentally strong US growth stocks.

## Disposition
Research-only. BASELINE_ONLY. The pattern concept (false breakdown → reclaim) is valid and
worth incorporating as a chart pattern filter, but the full CANSLIM system is not testable on crypto.
