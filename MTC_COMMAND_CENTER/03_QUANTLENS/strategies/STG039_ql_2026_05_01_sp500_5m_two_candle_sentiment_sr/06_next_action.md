# Next Action

## Recommended Next Step
Write a deterministic spec for the two-candle state machine before any code or backtest.

## Suggested First Variant
Use `HIGH_CLOSE_BULL` breakout above past-only resistance for long entries and `LOW_CLOSE_BEAR` breakdown below past-only support for short entries on `5m`.

## Required Decisions
- Support/resistance algorithm.
- Follow-through count for bias confirmation.
- Sentiment-change exit rule.
- Whether fixed `1.5R` is mandatory or test parameter.

## Stop Condition
Do not prototype discretionary narration. If a rule cannot be expressed from OHLC without future bars, mark it as unresolved.
