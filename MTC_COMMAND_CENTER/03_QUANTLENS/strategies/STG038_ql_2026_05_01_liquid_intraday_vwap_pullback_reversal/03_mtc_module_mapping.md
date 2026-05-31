# MTC Module Mapping

## Candidate Role
- Primary role: entry_gate
- Secondary roles: guard, confirmation, exit_rule, sl_tp_method

## Potential MTC_V2 Layers
- Session layer: daily VWAP reset from open.
- Trend layer: price above/below VWAP and VWAP slope.
- Regime layer: trend day versus sideways day.
- Entry layer: VWAP pullback or VWAP band reversal.
- Confirmation layer: support/resistance plus candle signal.
- Exit layer: fixed `2R` or target VWAP.

## Existing Overlap To Inspect Later
- VWAP/session indicator support.
- Standard deviation band support.
- Support/resistance confluence.
- Candlestick pattern confirmation.
- Fixed-R target and VWAP target exits.

## No-Touch Notes
- No change to `01_PINE/MTC_V2.pine`.
- No production Python runner change.
- No backtest, optimization, parity run, or TradingView automation.
