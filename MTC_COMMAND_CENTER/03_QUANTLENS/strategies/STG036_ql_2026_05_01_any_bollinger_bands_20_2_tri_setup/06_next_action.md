# Next Action

## Recommended Next Step
Select one deterministic variant before prototype work.

## Suggested First Variant
Use Bollinger squeeze breakout:
- `BB(20, 2)`.
- Band width below a defined threshold.
- Price contained inside bands for a fixed lookback.
- Entry on strong close outside upper/lower band.

## Required Decisions
- Band-width threshold.
- Containment lookback.
- Strong candle definition.
- Stop and target model.
- Whether to require follow-through.

## Stop Condition
Do not build a combined Bollinger breakout/reversal/pullback strategy until each variant is separately deterministic and lookahead-safe.
