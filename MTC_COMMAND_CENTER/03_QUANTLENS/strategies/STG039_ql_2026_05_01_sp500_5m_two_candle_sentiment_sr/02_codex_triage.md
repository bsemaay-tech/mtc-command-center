# Codex Triage

## Executive Triage
Status: READY_FOR_PYTHON_PROTOTYPE

The transcript contains a codable candle sentiment classification framework. It is suitable as a research-only entry confirmation or guard module, especially around support/resistance breaks.

## STOP Condition Check
- Closed source dependency: low; all rules use OHLC only.
- Repaint/lookahead: low for candle state itself; medium if support/resistance levels are built with future pivots.
- Marketing risk: medium; method is presented as broadly useful but still discretionary.
- Rule completeness: partial; candle states are clear, support/resistance and active exit rules need deterministic definitions.
- MTC_V2 compatibility: plausible as a confirmation or guard layer.

## Strategy Completeness Check
- Entry: examples define long on resistance breakout and short on support breakdown with candle-state confirmation.
- Exit: examples use `1:1.5` fixed R and active sentiment-change exits.
- Stop: long below signal candle low, short above signal candle high.
- Risk: no position sizing model.
- Timeframe: S&P 500 `5m` example.
- Market: S&P 500 example; general OHLC applicability claimed but not validated.

## MTC_V2 Compatibility
Potential mapping:
- Candle sentiment state as entry confirmation.
- Candle sentiment state as trend/bias guard.
- Level breakout filter for support/resistance modules.
- Signal candle high/low stop anchor.
- Fixed `1.5R` target.
- Optional early exit on opposite candle-state sequence.

## Existing vs New Module Decision
Do not add a broad discretionary price-action reader. First inspect whether MTC_V2 already has candle body/range or breakout confirmation logic. If added later, it should be a research-only deterministic state machine and default OFF.

## Salvageable Ideas
- 3x3 candle-state matrix from close position and previous-range comparison.
- Require follow-through after strong state before bias switch.
- Use strong state at level break as entry confirmation.
- Use opposite strong state or failed follow-through as caution/exit condition.

## Final Status
READY_FOR_PYTHON_PROTOTYPE

## Next Action
Define a deterministic prototype for `two_candle_state + support/resistance breakout` on `5m`, including level construction, follow-through count, entry bar, stop anchor, target, and sentiment-change exit rule.
