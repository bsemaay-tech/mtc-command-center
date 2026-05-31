# MTC Module Mapping

## Candidate Role
- Primary role: entry_gate
- Secondary roles: guard, confirmation, exit_rule, sl_tp_method

## Potential MTC_V2 Layers
- RSI threshold filter: `50`, `70`, `30`.
- RSI moving-average crossover: RSI versus `SMA/EMA(10)` on RSI.
- Divergence confirmation: regular and hidden divergence.
- Trendline confirmation: RSI trendline break.
- Confluence layers: support/resistance, Fibonacci golden zone, `SMA(50)`.
- Exit layer: fixed `2R`.

## Existing Overlap To Inspect Later
- RSI indicator support.
- Divergence or pivot detection support.
- Fibonacci swing selection.
- Support/resistance levels.
- Moving-average trend filter.
- Fixed-R target support.

## No-Touch Notes
- No change to `01_PINE/MTC_V2.pine`.
- No production Python runner change.
- No backtest, optimization, parity run, or TradingView automation.
