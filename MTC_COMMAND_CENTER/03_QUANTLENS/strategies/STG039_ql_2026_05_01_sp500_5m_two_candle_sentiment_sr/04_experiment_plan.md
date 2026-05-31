# Experiment Plan

## Prototype Scope
Start with one mechanical variant:

`two_candle_state + support/resistance breakout`

## Deterministic Rules To Define
- Candle range edge case when `high == low`.
- Upper/middle/lower third boundary handling.
- Bull/range/bear comparison rule against previous candle high/low.
- Strong bullish state definition.
- Strong bearish state definition.
- Bias switch rule and required follow-through count.
- Support/resistance construction method.
- Breakout close requirement.
- Entry execution bar.
- Stop anchor and buffer.
- Fixed `1.5R` target.
- Active sentiment-change exit condition.

## Suggested Pilot
- Market: liquid index or futures proxy.
- Timeframe: `5m`.
- Direction: test long and short separately.
- First gate: static event extraction only.
- Second gate: one-symbol pilot after event extraction is stable.

## Explicit Non-Goals
- No discretionary candle narration.
- No named candlestick-pattern library.
- No broad market claim.
- No Pine patch.
- No production runner change.
- No optimization before a clean deterministic pilot.
