# MTC Module Mapping

## Candidate Role
- Primary role: entry_gate
- Secondary roles: guard, exit_rule, sl_tp_method, money_management

## Potential MTC_V2 Layers
- Trend layer: price relative to 8 EMA defines long/short bias.
- Entry layer: pullback to 8 EMA after impulse.
- Guard layer: reject entries too far from EMA.
- Exit layer: entry candle stop, high/low-of-day partial target, 8 EMA break runner exit.
- Risk layer: maximum two failed attempts per symbol/session.

## Existing Overlap To Inspect Later
- EMA trend filters.
- Pullback or mean-reversion-to-trend entry gates.
- Candle high/low stop logic.
- Session high/low target logic.
- Re-entry and cooldown controls.

## No-Touch Notes
- No change to 01_PINE/MTC_V2.pine.
- No production Python runner change.
- No backtest, optimization, or parity run.
