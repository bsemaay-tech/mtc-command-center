# Codex Triage

## Executive Triage
Status: READY_FOR_PYTHON_PROTOTYPE

The transcript contains two codable VWAP day-trading setups: trend pullbacks to VWAP and sideways reversals from VWAP bands. The candidate is suitable for a deterministic prototype after ambiguous confirmations are formalized.

## STOP Condition Check
- Closed source dependency: low; VWAP and standard deviation bands are standard calculations.
- Repaint/lookahead: low for VWAP if computed intraday bar-by-bar; medium for support/resistance if future pivots are used incorrectly.
- Marketing risk: moderate due broad claims across all assets.
- Rule completeness: good, but support/resistance, candlestick patterns, and sideways filters need exact definitions.
- MTC_V2 compatibility: plausible as session VWAP guard/entry/exit module.

## Strategy Completeness Check
- Entry: defined by VWAP pullback or VWAP band reversal plus confirmation.
- Exit: fixed `2R` for pullbacks, VWAP target for reversals.
- Stop: local swing/candle/resistance/support stop.
- Risk: minimum `1:1` for reversal setups; no account-level sizing.
- Timeframe: `5m`.
- Market: liquid assets.

## MTC_V2 Compatibility
Potential mapping:
- Trend filter: price vs session VWAP and VWAP slope.
- Entry gate: pullback to VWAP or band touch in sideways regime.
- Guard: avoid first hour for reversals; avoid band-hugging trend days.
- Confirmation: support/resistance confluence and candle pattern.
- SL/TP: fixed `2R` or mean reversion to VWAP.

## Existing vs New Module Decision
Do not add a new MTC_V2 feature yet. First inspect whether existing VWAP, session, S/R, candle, and fixed-R components exist. Any new feature must be research-only and default OFF.

## Salvageable Ideas
- Separate trend-continuation and sideways mean-reversion use cases.
- Compare current day VWAP to prior day VWAP for fair-value drift.
- Use VWAP bands as overbought/oversold only after sideways regime is confirmed.
- Treat VWAP pullbacks as fair-value entries, not chase entries.

## Final Status
READY_FOR_PYTHON_PROTOTYPE

## Next Action
Write deterministic prototype spec for VWAP calculation, band multipliers, trend/sideways regime detection, support/resistance confluence, candle confirmation, stops, and targets.
