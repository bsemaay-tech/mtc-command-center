# Deterministic Spec — Daily Extension Anti-Chase Filter (QL_DAILY_EXTENSION_ANTI_CHASE_FILTER_v0)

> Source: Daily extension anti-chase intake. Research-only Python batch 2026-05-03.
> Signal logic from `run_batch.py::signal_anti_chase_crabel()`. No Pine, no MTC production integration.
> **FILTER-ONLY**: use as entry gate, not standalone system.

## Universe
- Crypto (BTC, ETH, SOL, BNB, XRP), 1D bars.

## Concept
Built on Crabel range-expansion entries (prior close ± mult × prior range), but with a
"chase block": if the last N bars were all strong directional closes (large body + strong close
location), the Crabel signal is suppressed — because we'd be chasing an overextended move.

## Indicators
```
atr  = ATR(14)
body = abs(close - open)
loc  = (close - low) / (high - low)             # close location in bar (0 = at low, 1 = at high)

strong_green = (close > open) AND (body >= 0.5 × atr) AND (loc >= 0.70)
strong_red   = (close < open) AND (body >= 0.5 × atr) AND (loc <= 0.30)
```

## Base signal (Crabel)
```
prev_range = high[1] - low[1]
buy_stop   = close[1] + prev_range × 0.9
sell_stop  = close[1] - prev_range × 0.9
long_entry_base  = high >= buy_stop
short_entry_base = low <= sell_stop
```

## Anti-chase filter
```
block_long  = all N prior bars were strong_green   # N = lookback (default 3)
block_short = all N prior bars were strong_red

long_entry  = long_entry_base  AND NOT block_long
short_entry = short_entry_base AND NOT block_short
```

## Research classification
**FILTER_ONLY** — Filter reduced or reshaped entries; use only as gate research.
Standalone Crabel has weak edge on crypto daily. The anti-chase filter improves
quality of entries by removing the most overextended situations.

## Use cases
- As a pre-filter gate: suppress entry signals from any producer when the last 3+ daily closes
  are all large-body strong closes in the same direction.
- Combined with a trend filter to create a "only enter pullbacks, never chase" discipline.

## Disposition
Research-only. FILTER_ONLY. Do not use standalone. Valuable as a meta-rule component:
"if the last N bars were all strongly directional, do not enter in that direction today."
