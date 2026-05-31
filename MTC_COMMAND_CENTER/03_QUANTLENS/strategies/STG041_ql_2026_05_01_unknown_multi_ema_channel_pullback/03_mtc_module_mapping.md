# MTC Module Mapping

## Candidate Role
- Primary role: entry_gate
- Secondary roles: guard, confirmation, exit_rule, sl_tp_method, money_management

## Potential MTC_V2 Layers
- Trend layer: price above/below `EMA(200)` high/close/low channel.
- Pullback layer: price touch or entry into slow green channel.
- Momentum layer: white `EMA(5)` high/low channel crosses orange `EMA(13)` high/low channel.
- Stop layer: pullback extreme or slow channel boundary.
- Target layer: fixed `2R`.

## Existing Overlap To Inspect Later
- EMA producer/filter support.
- Source-specific EMA calculation on high/close/low.
- Pullback-to-band or channel logic.
- MA channel crossover logic.
- Fixed risk/reward exits.

## No-Touch Notes
- No change to `01_PINE/MTC_V2.pine`.
- No production Python runner change.
- No backtest, optimization, parity run, or TradingView automation.
