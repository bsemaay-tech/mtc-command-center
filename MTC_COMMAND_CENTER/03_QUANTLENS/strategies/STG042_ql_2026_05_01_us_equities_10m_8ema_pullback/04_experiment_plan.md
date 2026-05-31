# Experiment Plan

## Prototype Scope
Build a research-only Python prototype after the rules below are frozen. Use underlying OHLC candles first; options PnL is out of scope for the first pass.

## Deterministic Rules To Define
- EMA length: 8.
- Timeframe: start with 10m because the Amazon example uses 10m.
- Long bias: close above 8 EMA and EMA slope positive.
- Short bias: close below 8 EMA and EMA slope negative.
- Impulse qualifier: require a recent move away from EMA before the pullback.
- Entry proximity: define maximum distance from 8 EMA in ATR, percent, or ticks.
- Long stop: entry candle low.
- Short stop: entry candle high.
- Partial target: high of day for longs, low of day for shorts, computed only from past/current bars.
- Runner exit: close back through 8 EMA or confirmed EMA break.
- Re-entry limit: maximum two failed attempts per symbol per session.

## Validation Gates
- First pass: static rule spec review.
- Second pass: small OHLC prototype on one symbol/timeframe.
- Third pass: multi-symbol/timeframe sanity check only if first pass is coherent.

## Explicit Non-Goals
- No options chain modeling in the first prototype.
- No live execution logic.
- No TradingView automation.
- No MTC_V2 integration until local prototype evidence exists.
