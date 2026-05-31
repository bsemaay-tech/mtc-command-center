# MTC Module Mapping

## Candidate Role
- Primary role: entry_gate
- Secondary roles: confirmation, guard, exit_rule

## Potential MTC_V2 Layers
- Level layer: previous day high, previous day low, pre-market high, pre-market low.
- Confirmation layer: close-based break beyond the selected level.
- Entry layer: 8 EMA hold for long or 8 EMA rejection for short.
- Guard layer: reject trades when EMA is not close enough to price.
- Exit layer: adverse cross through 8 EMA.

## Existing Overlap To Inspect Later
- Prior-day level logic.
- Pre-market/session level logic.
- EMA trend and EMA pullback logic.
- Close-based breakout confirmation.
- EMA cross invalidation rules.

## No-Touch Notes
- No change to `01_PINE/MTC_V2.pine`.
- No production Python runner change.
- No backtest, optimization, parity run, or TradingView automation.
