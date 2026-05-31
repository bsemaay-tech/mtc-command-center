# Codex Triage

## Executive Triage
Status: READY_FOR_PYTHON_PROTOTYPE

The source contains a codable four-level plus 8 EMA intraday strategy. It is mostly a clearer framing of the same EllyDTrades pattern family already seen in the 8 EMA pullback and LE model bull flag candidates.

## STOP Condition Check
- Closed source dependency: no hard dependency; four levels and 8 EMA are computable from OHLC/session data.
- Repaint/lookahead: low for prior-day levels and EMA, medium for pre-market/session handling and exit definitions.
- Marketing risk: moderate to high; source makes broad profitability claims without evidence.
- Rule completeness: partial; several key thresholds remain qualitative.
- MTC_V2 compatibility: likely compatible after mapping to existing level and EMA modules.

## Strategy Completeness Check
- Entry: partially defined through level break plus EMA hold/reject.
- Exit: partially defined through adverse 8 EMA cross.
- Risk: no explicit stop distance, sizing model, or max daily loss in the provided summary.
- Time/session: pre-market window is specified as 04:00-09:30 Eastern Time.
- Market: equities/options framing; prototype should start with underlying OHLC.

## MTC_V2 Compatibility
Potential mapping:
- Confirmation: valid break of PDH/PDL/PMH/PML.
- Entry gate: 8 EMA hold/rejection after valid break.
- Guard: reject entries when EMA is too far from price.
- Exit rule: adverse cross through 8 EMA.

## Existing vs New Module Decision
Do not create a new MTC_V2 feature from this candidate yet. First consolidate it against the previous `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK` and `QL_2026-05-01_US_EQUITIES_INTRADAY_LE_MODEL_BULL_FLAG` candidates.

## Salvageable Ideas
- Explicit four-level universe: PDH, PDL, PMH, PML.
- Require candle close break instead of wick-only touch.
- Require EMA to be close enough to price before entry.
- Use EMA hold/rejection as directional confirmation.

## Final Status
READY_FOR_PYTHON_PROTOTYPE

## Next Action
Create a consolidated deterministic spec for the EllyDTrades level-plus-8-EMA family before writing prototype code.
