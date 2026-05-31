# Codex Triage

## Executive Triage
Status: READY_FOR_PYTHON_PROTOTYPE

The source contains a codable exit and trade-management rule: hold longs until price breaks below the 8 EMA and hold shorts until price breaks above the 8 EMA. It is a useful module candidate but not a full strategy by itself.

## STOP Condition Check
- Closed source dependency: none; 8 EMA is computable from OHLC data.
- Repaint/lookahead: low if the EMA break is evaluated bar-by-bar.
- Marketing risk: moderate; claims are psychological and anecdotal.
- Rule completeness: partial because "break" is not mechanically defined.
- MTC_V2 compatibility: likely compatible as an exit or trailing-stop layer.

## Strategy Completeness Check
- Entry: not defined; this candidate depends on an existing entry model.
- Exit: clear conceptually, but needs close/wick/confirmation definition.
- Risk: reduces early exit behavior but does not define position sizing or max loss.
- Timeframe: warns against using 1m noise during 10m/30m trends; exact execution timeframe must be selected.
- Market: equities/options framing; first prototype should use underlying OHLC.

## MTC_V2 Compatibility
Potential mapping:
- Exit rule: adverse break of 8 EMA.
- Trailing stop method: dynamic EMA trail.
- Guard/psychology note: ignore lower-timeframe pullback candles when the trade timeframe trend remains intact.

## Existing vs New Module Decision
Do not add a new MTC_V2 feature yet. First inspect whether existing trailing stop or EMA exit logic can express this behavior. This should be consolidated with the existing EllyDTrades 8 EMA candidates.

## Salvageable Ideas
- EMA break as objective exit rule.
- Avoid lower-timeframe panic exits while higher-timeframe trend remains valid.
- Use post-trade review to quantify early exit cost.

## Final Status
READY_FOR_PYTHON_PROTOTYPE

## Next Action
Define a deterministic EMA-break exit spec and attach it to the consolidated EllyDTrades 8 EMA prototype plan.
