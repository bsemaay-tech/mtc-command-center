# Experiment Plan

## Prototype Scope
Evaluate this as a research-only exit module attached to existing EllyDTrades 8 EMA entries. Do not test it as a standalone producer.

## Deterministic Rules To Define
- EMA length: 8.
- Trade timeframe: choose 10m, 30m, or another fixed execution timeframe.
- Long exit: wick below EMA, close below EMA, or confirmed close below EMA.
- Short exit: wick above EMA, close above EMA, or confirmed close above EMA.
- Optional buffer: ticks, percent, or ATR fraction beyond EMA.
- Optional confirmation: one-bar or two-bar break.
- Lower-timeframe noise rule: ignore 1m candles unless the trade timeframe exit triggers.
- Partial-profit interaction: define whether EMA exit applies only to runners or entire position.

## Validation Gates
- First pass: static spec and overlap review.
- Second pass: attach to one existing 8 EMA entry candidate on one symbol/timeframe.
- Third pass: compare early fixed-profit exits versus EMA trailing exits.

## Explicit Non-Goals
- No options contract modeling in first pass.
- No live execution logic.
- No MTC_V2 integration before local prototype evidence.
- No backtest or optimization until rule spec is frozen.
