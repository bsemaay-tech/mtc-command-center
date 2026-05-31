# Experiment Plan

## Prototype Scope
Build a research-only Python prototype after consolidating this candidate with the other EllyDTrades 8 EMA candidates. Use underlying OHLC/session data first.

## Deterministic Rules To Define
- Previous day high/low calculation.
- Pre-market high/low calculation using 04:00-09:30 Eastern Time.
- Valid break: close beyond level by ticks, percent, or ATR fraction.
- Invalid break: wick-only touch without close confirmation.
- EMA length: 8.
- EMA readiness: maximum allowed distance between price and EMA.
- Bullish hold: definition of hold above EMA after pullback.
- Bearish rejection: definition of reject from EMA after pullback.
- Exit: wick cross, close cross, or confirmed cross through EMA.
- Entry execution: touch, close, next open, or limit near EMA.

## Validation Gates
- First pass: static spec and overlap review against existing candidates.
- Second pass: one-symbol intraday OHLC prototype.
- Third pass: multi-session replay only if no lookahead risks remain.

## Explicit Non-Goals
- No options PnL modeling in first pass.
- No live execution logic.
- No MTC_V2 integration.
- No backtest or optimization until rule spec is frozen.
