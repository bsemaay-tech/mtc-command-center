# Codex Triage

## Executive Triage
Status: READY_FOR_PYTHON_PROTOTYPE

The transcript contains a focused dual-RSI trend-pullback system. It is more implementation-ready than the broad RSI confluence playbook because the core signal is deterministic: daily `RSI(7)` regime plus `1h RSI(7)` pullback recovery/rejection.

## STOP Condition Check
- Closed source dependency: low; uses standard RSI and OHLC.
- Repaint/lookahead: low for RSI crosses; medium if swing lows/highs and support/resistance are defined with future pivots.
- Marketing risk: medium due "secret" and simplicity claims.
- Rule completeness: mostly complete for RSI logic; partial for price action confluence.
- MTC_V2 compatibility: plausible as regime filter plus entry gate.

## Strategy Completeness Check
- Entry: daily RSI regime plus `1h` RSI crossing back through `40` or `60`.
- Exit: fixed `2R` target.
- Stop: below recent swing low for long, above recent swing high for short.
- Risk: no position sizing beyond R-based target.
- Timeframe: `1h` entries/exits, daily trend RSI.
- Market: broad claim, not validated.

## MTC_V2 Compatibility
Potential mapping:
- Higher timeframe RSI regime filter.
- Local RSI pullback entry gate.
- Sideways no-trade guard when HTF RSI is between `40` and `60`.
- Swing high/low stop anchor.
- Fixed `2R` target.
- Optional price-action confirmation layer.

## Existing vs New Module Decision
Before adding anything, inspect existing MTC_V2 RSI, MTF, and regime modules. If missing, prototype as research-only and default OFF. Price-action confirmation should remain optional until mechanically defined.

## Salvageable Ideas
- `RSI(7)` daily `60/40` trend regime.
- `RSI(7)` `1h` oversold/overbought pullback recovery as entry timing.
- No-trade zone when daily RSI is `40-60`.
- Reject large signal candles if stop distance is too wide.
- Fixed `2R` target with swing stop.

## Final Status
READY_FOR_PYTHON_PROTOTYPE

## Next Action
Define deterministic RSI calculation source, MTF bar alignment, signal-candle size filter, swing stop rule, and optional support/resistance confirmation before Python prototype.
