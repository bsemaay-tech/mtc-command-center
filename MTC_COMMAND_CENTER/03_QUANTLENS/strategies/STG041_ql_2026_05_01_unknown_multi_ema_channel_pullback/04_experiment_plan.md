# Experiment Plan

## Prototype Scope
Build a research-only Python prototype after deterministic rules are frozen. Use OHLC candles and standard EMA calculations.

## Deterministic Rules To Define
- Market and timeframe.
- EMA calculation source for every line: `EMA(200, high)`, `EMA(200, close)`, `EMA(200, low)`, `EMA(13, high)`, `EMA(13, low)`, `EMA(5, high)`, `EMA(5, low)`.
- Green channel upper/lower boundaries.
- Long trend cross: close above green channel upper boundary or full candle above.
- Short trend cross: close below green channel lower boundary or full candle below.
- Pullback touch: wick touch, close inside, or any overlap with green channel.
- Long invalidation during pullback: wick below green channel or close below green channel.
- Short invalidation during pullback: wick above green channel or close above green channel.
- White/orange channel cross: both upper and lower fast lines must close beyond corresponding medium lines.
- Entry execution: signal close or next candle open.
- Stop anchor: pullback extreme, channel boundary, or max of both.
- Target: fixed `2R` from entry to stop.
- Risk sizing: 1% account risk optional for research reports.

## Validation Gates
- First pass: static rule spec.
- Second pass: one symbol/timeframe OHLC prototype.
- Third pass: multi-symbol/timeframe sanity only if first pass is coherent.

## Explicit Non-Goals
- No MTC_V2 integration.
- No Pine patch.
- No production runner change.
- No optimization before a small prototype validates rule feasibility.
