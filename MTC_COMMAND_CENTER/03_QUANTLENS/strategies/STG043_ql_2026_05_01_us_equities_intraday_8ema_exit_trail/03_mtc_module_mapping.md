# MTC Module Mapping

## Candidate Role
- Primary role: exit_rule
- Secondary roles: sl_tp_method, trailing_be_method

## Potential MTC_V2 Layers
- Exit layer: close or confirmed break through the 8 EMA.
- Trailing layer: dynamic EMA-based trailing stop.
- Risk layer: objective invalidation to prevent emotional early exits.

## Existing Overlap To Inspect Later
- EMA-based trailing stop support.
- Close-through moving-average exit rules.
- Intrabar versus close-based stop semantics.
- Multi-timeframe entry/exit separation, if present.

## No-Touch Notes
- No change to `01_PINE/MTC_V2.pine`.
- No production Python runner change.
- No backtest, optimization, parity run, or TradingView automation.
