# Experiment Plan

## Prototype Scope
Build a research-only Python prototype after the rule spec is frozen. Use underlying OHLC candles first; options and 0DTE contract modeling are out of scope for the first pass.

## Deterministic Rules To Define
- Session calendar and pre-market window.
- Previous day high/low and pre-market high/low calculation.
- Bullish setup: break above required level set.
- Bearish setup: break below required level set.
- Retest routing: choose level retest or 8 EMA retest based on which valid support/resistance is reached first.
- EMA length: 8.
- Entry proximity threshold to level/EMA.
- Flag quality: maximum pullback size, minimum impulse size, acceptable candle shape, and volume optionality.
- Long stop: entry candle low.
- Short stop: entry candle high.
- Partial exit: high of day for longs, low of day for shorts, computed bar-by-bar.
- Runner exit: close through 8 EMA, wick through 8 EMA, or confirmed EMA break.
- Time guard: restrict new entries to first two to three hours and block lunch entries.

## Validation Gates
- First pass: static rule spec review.
- Second pass: one-symbol intraday OHLC prototype.
- Third pass: multi-day SPY replay focused on the cited pattern dates.
- Fourth pass: broader symbols/timeframes only if the SPY replay is coherent.

## Explicit Non-Goals
- No MTC_V2 Pine integration.
- No production Python runner changes.
- No live trading logic.
- No options-chain or Greek modeling in the first prototype.
