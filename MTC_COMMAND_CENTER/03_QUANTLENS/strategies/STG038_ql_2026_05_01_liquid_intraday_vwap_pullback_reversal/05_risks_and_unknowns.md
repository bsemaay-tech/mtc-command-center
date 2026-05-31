# Risks And Unknowns

## Risks
- Support/resistance confirmation may become discretionary or lookahead-biased.
- Sideways versus trend regime classification can dominate results.
- VWAP band reversals can fail badly on trend days.
- VWAP pullbacks can whipsaw around fair value.
- Transaction costs matter on `5m` intraday trades.
- Claims across stocks, forex, crypto, and bonds are too broad without separate validation.

## Unknowns
- Source URL and channel metadata.
- Exact VWAP band standard deviation implementation.
- Exact session timezone and market hours.
- Exact support/resistance construction.
- Exact candlestick pattern definitions.
- Whether examples include extended hours.

## Required Clarifications Before Backtest
- Target market and data source.
- Regular session versus extended-hours VWAP.
- Deterministic support/resistance rule.
- Candlestick confirmation library/rules.
- Separate evaluation for pullback and reversal setups.
