# Risks And Unknowns

## Risks
- The source is a non-verbatim summary, so details may be incomplete.
- Strong overlap with prior EllyDTrades candidates may create duplicate research unless consolidated.
- "EMA catches up", "clear break", "hold", and "rejection" are qualitative.
- Pre-market data availability can vary across datasets.
- Options-focused claims may not translate to underlying OHLC edge.
- Exit on EMA cross may whipsaw in choppy markets.

## Unknowns
- Exact video title as published was not independently verified.
- Channel ID was not provided.
- Exact chart timeframe was not specified in the supplied notes.
- Exact stop-loss placement beyond EMA invalidation is not specified.
- Position sizing and partial profit rules are not specified in detail.

## Required Clarifications Before Backtest
- Use one consolidated candidate or keep separate per-video candidates.
- Select initial timeframe and symbol universe.
- Define pre-market data source and timezone handling.
- Define close-confirmation threshold for level break.
- Define EMA hold/rejection mechanically.
