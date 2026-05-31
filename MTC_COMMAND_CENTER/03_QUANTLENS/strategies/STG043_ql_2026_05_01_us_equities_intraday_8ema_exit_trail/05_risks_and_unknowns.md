# Risks And Unknowns

## Risks
- EMA exits can give back open profit before triggering.
- EMA exits can whipsaw in choppy markets.
- The source is a non-verbatim summary, so exact phrasing and exceptions may be missing.
- Options PnL decay can make a delayed EMA exit behave differently than underlying OHLC.
- A single EMA rule may be too simple across regimes.

## Unknowns
- Exact chart timeframe for the EMA exit.
- Whether exit is wick-based or close-based.
- Whether partial profits should occur before EMA trailing exit.
- Whether the EMA exit applies to all contracts or runner only.
- Channel ID was not provided.

## Required Clarifications Before Backtest
- Pick execution timeframe.
- Define EMA break trigger mechanically.
- Define interaction with existing partial exits.
- Define whether lower-timeframe candles are ignored completely or used for stop execution.
