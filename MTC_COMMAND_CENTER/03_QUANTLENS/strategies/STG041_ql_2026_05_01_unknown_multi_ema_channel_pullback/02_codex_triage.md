# Codex Triage

## Executive Triage
Status: READY_FOR_PYTHON_PROTOTYPE

The transcript contains a complete enough multi-EMA channel pullback strategy. It defines a slow trend channel, fast/medium pullback channels, directional setup, entry trigger, stop placement, and fixed 2R target.

## STOP Condition Check
- Closed source dependency: low; all calculations are standard EMAs on OHLC sources.
- Repaint/lookahead: low if evaluated bar-by-bar on closed candles.
- Marketing risk: moderate due "best EMA settings ever" framing.
- Rule completeness: good, but edge cases need deterministic definitions.
- MTC_V2 compatibility: plausible as trend filter plus entry gate and fixed R exit.

## Strategy Completeness Check
- Entry: defined by price crossing green channel, pullback into green channel, then white/orange channel recross.
- Exit: fixed 2R target.
- Stop: beyond pullback or green channel.
- Risk: generic 1% rule mention.
- Timeframe: not specified.
- Market: not specified.

## MTC_V2 Compatibility
Potential mapping:
- Trend filter: price relation to `EMA(200)` high/close/low channel.
- Entry gate: pullback to slow EMA channel.
- Confirmation: fast `EMA(5)` channel crossing medium `EMA(13)` channel after pullback.
- SL/TP: pullback/green-channel stop with 2R target.

## Existing vs New Module Decision
Do not add a new MTC_V2 feature yet. First inspect whether existing EMA trend, pullback, MA cross, and fixed-R modules can express the model. Any new implementation should remain research-only and default OFF.

## Salvageable Ideas
- Use EMA channels from high/close/low instead of single EMA lines.
- Require pullback to slow channel before fast/medium recross trigger.
- Use symmetric long/short logic.
- Fixed 2R target keeps the first prototype simple.

## Final Status
READY_FOR_PYTHON_PROTOTYPE

## Next Action
Write deterministic prototype spec for channel boundaries, cross timing, stop anchor, 2R target, and execution bar assumptions.
