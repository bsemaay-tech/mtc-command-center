# Experiment Plan

## Prototype Scope
Do not prototype all 15 combinations at once. Start with one deterministic variant and add variants only after the first one is clean.

## Candidate First Variant
- RSI `50` pullback continuation.
- Confluence: `SMA(50)` trend/dynamic support-resistance.
- Timeframe: `1h`.
- Target: fixed `2R`.

## Deterministic Rules To Define
- RSI length and smoothing.
- RSI `10` moving average type if using crossover variant.
- Uptrend/downtrend definition.
- "RSI stays below/above 50 for 8-10 candles" invalidation.
- Support/resistance construction if using S/R.
- Fibonacci swing selection if using Fib.
- Divergence pivot window if using divergence.
- RSI trendline pivot construction if using trendline breakout.
- Entry execution bar.
- Stop anchor and buffer.
- Fixed `2R` target.

## Validation Gates
- First pass: static spec for one variant.
- Second pass: one symbol/timeframe pilot.
- Third pass: compare variants only after the first variant is stable.

## Explicit Non-Goals
- No 15-strategy batch initially.
- No Pine patch.
- No production runner change.
- No optimization before a clean pilot.
