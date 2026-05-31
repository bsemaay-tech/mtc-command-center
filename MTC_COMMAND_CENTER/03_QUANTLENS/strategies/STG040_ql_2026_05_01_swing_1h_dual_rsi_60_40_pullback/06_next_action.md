# Next Action

## Recommended Next Step
Write a deterministic prototype spec for the core dual-RSI variant.

## Suggested First Variant
Use completed daily `RSI(7)` as the regime filter and `1h RSI(7)` as the pullback-entry trigger. Exclude support/resistance and candlestick confirmation from the first core variant unless they are separately specified.

## Required Decisions
- Daily bar alignment rule.
- Pullback memory expiry.
- Past-only swing stop window.
- Maximum stop distance or large-candle filter.
- Whether `2R` is fixed or configurable.

## Stop Condition
Do not run a prototype if daily RSI uses incomplete future daily information or if swing stops require future pivots.
