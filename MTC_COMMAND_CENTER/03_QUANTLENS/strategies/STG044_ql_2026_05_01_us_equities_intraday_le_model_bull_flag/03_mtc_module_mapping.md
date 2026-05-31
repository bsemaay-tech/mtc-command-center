# MTC Module Mapping

## Candidate Role
- Primary role: entry_gate
- Secondary roles: confirmation, guard, exit_rule, sl_tp_method, money_management

## Potential MTC_V2 Layers
- Level layer: previous day high/low and pre-market high/low.
- Trend layer: 8 EMA as dynamic support/resistance and runner trail.
- Entry layer: level retest or EMA retest after key level break.
- Guard layer: no breakout chasing, no lunch/chop entries, no violent pullback candles.
- Exit layer: partial at session high/low and runner until EMA break.
- Risk layer: entry candle low/high stop.

## Existing Overlap To Inspect Later
- Previous-day and session-level logic.
- EMA trend or EMA pullback filters.
- Candle high/low stop methods.
- Time/session guards.
- Partial exit and trailing stop support.

## No-Touch Notes
- No change to `01_PINE/MTC_V2.pine`.
- No production Python runner change.
- No backtest, optimization, parity run, or TradingView automation.
