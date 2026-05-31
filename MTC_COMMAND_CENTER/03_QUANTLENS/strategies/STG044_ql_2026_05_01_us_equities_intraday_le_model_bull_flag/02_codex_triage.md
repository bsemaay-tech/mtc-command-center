# Codex Triage

## Executive Triage
Status: READY_FOR_PYTHON_PROTOTYPE

The transcript contains a codable intraday bull flag / breakout-retest strategy. The strategy is more complete than a simple 8 EMA pullback because it defines a state sequence: key level break, level-or-EMA retest, tight candle stop, partial at high of day, and runner trailed by the 8 EMA.

## STOP Condition Check
- Closed source dependency: no hard dependency; the rules can be expressed from OHLC and session-derived levels.
- Repaint/lookahead: low for EMA and prior/premarket levels, medium for HOD/LOD targets if implemented incorrectly.
- Marketing risk: high promotional language and anecdotal return claims.
- Rule completeness: partial; flag quality and distance thresholds are discretionary.
- MTC_V2 compatibility: likely compatible as entry gate plus guard, pending exact module mapping.

## Strategy Completeness Check
- Entry: usable after deterministic level-break and retest rules are specified.
- Exit: partial at HOD/LOD plus 8 EMA runner exit is usable but needs bar-by-bar definitions.
- Stop: clear for long side; bearish mirror is implied.
- Risk: tight candle-risk idea is useful; fixed position sizing and loss limits are not fully specified.
- Timeframe: intraday, with SPY examples; exact candle timeframe is not explicitly formalized in the transcript.
- Market: equities/options; prototype should start with underlying OHLC.

## MTC_V2 Compatibility
Potential mapping:
- Entry gate: level break then retest of level or 8 EMA.
- Confirmation: outside-day state from prior day high/low break.
- Guard: reject chasing, reject lunch/chop entries, reject violent pullbacks.
- Exit: HOD/LOD partial and 8 EMA runner trail.

## Existing vs New Module Decision
Do not add a new MTC_V2 feature yet. First inspect whether existing level, EMA, session, and trailing modules can express the model. Any missing feature must remain research-only, default OFF, and parity-gated.

## Salvageable Ideas
- Route entries between level retest and EMA retest depending on which support comes first.
- Use previous day and pre-market levels as breakout state filters.
- Use a flag-quality guard to reject large reversal pullbacks.
- Avoid new entries after the first two to three trading hours.

## Final Status
READY_FOR_PYTHON_PROTOTYPE

## Next Action
Write a deterministic prototype specification. Do not backtest until the thresholds for breakout, retest distance, flag quality, session window, partial target, and EMA runner exit are fixed.
