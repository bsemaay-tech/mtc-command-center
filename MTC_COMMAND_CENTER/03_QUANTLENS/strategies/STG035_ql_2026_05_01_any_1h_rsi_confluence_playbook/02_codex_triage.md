# Codex Triage

## Executive Triage
Status: READY_FOR_PYTHON_PROTOTYPE

The transcript contains a codable RSI playbook, but the full 15-strategy combination set is too broad for a first prototype. The candidate should be decomposed into smaller deterministic variants.

## STOP Condition Check
- Closed source dependency: low; RSI, SMA, Fibonacci, and S/R are standard.
- Repaint/lookahead: high risk for divergence, trendlines, support/resistance, and Fibonacci swing selection if implemented with future pivots.
- Marketing risk: high due broad profitability claims across markets.
- Rule completeness: partial; many discretionary pattern definitions remain.
- MTC_V2 compatibility: plausible after decomposition.

## Strategy Completeness Check
- Entry: setup plus confluence rules are described.
- Exit: examples use fixed `2R`.
- Stop: beyond support/resistance, golden zone, or moving average.
- Risk: no position sizing beyond fixed R examples.
- Timeframe: examples use `1h`.
- Market: any market claimed, not validated.

## MTC_V2 Compatibility
Potential mapping:
- RSI momentum/threshold filter.
- RSI divergence or hidden divergence confirmation.
- RSI trendline break confirmation.
- RSI moving-average crossover confirmation.
- Support/resistance, Fibonacci, or SMA confluence guard.
- Fixed `2R` target.

## Existing vs New Module Decision
Do not add a broad "RSI playbook" feature. First select one deterministic variant and inspect existing MTC_V2 modules. Any new feature must be research-only and default OFF.

## Salvageable Ideas
- RSI `50` line as trend-pullback threshold.
- Avoid RSI `50` pullback trades if RSI remains across the line for `8-10` candles.
- Hidden divergence as continuation filter.
- RSI trendline break as early momentum shift.
- RSI `10` MA crossover near `30/70`.

## Final Status
READY_FOR_PYTHON_PROTOTYPE

## Next Action
Choose one prototype variant, preferably RSI `50` pullback plus `50` SMA or support/resistance confluence, and define all pivot/level/entry rules mechanically.
