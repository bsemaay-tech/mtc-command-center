# Codex Triage

## Executive Triage
Status: READY_FOR_PYTHON_PROTOTYPE

The transcript contains a codable 8 EMA pullback trend-continuation strategy. The core is simple and testable on OHLC data, but several execution details are discretionary and must be converted into deterministic rules before any backtest.

## STOP Condition Check
- Closed source dependency: no hard dependency; the mentioned optional script is not required for the 8 EMA logic.
- Repaint/lookahead: low repaint risk for EMA itself, but high-of-day/low-of-day target logic can become lookahead if implemented incorrectly.
- Marketing risk: high promotional language and unsupported performance claims.
- Rule completeness: partial, because entry proximity, exhaustion exit, runner management, and option contract handling are not fully specified.
- MTC_V2 compatibility: possible as an entry gate or trend-following guard, pending module mapping.

## Strategy Completeness Check
- Entry: usable but needs a numeric distance-to-EMA rule.
- Exit: partials at HOD/LOD and runner until EMA break are described but need exact definitions.
- Stop: clear candle high/low stop rule.
- Risk: two failed attempts stop rule is useful but needs session-level implementation.
- Timeframe: 10m shown for Amazon; examples include SPY and Tesla without full parameter detail.
- Market: equities/options; prototype should test underlying OHLC first.

## MTC_V2 Compatibility
The strategy maps most naturally to:
- Trend filter: price above/below 8 EMA.
- Entry gate: pullback to EMA after impulse.
- Guard: avoid chasing when price is extended away from EMA.
- Exit rule: candle stop, HOD/LOD partial, EMA break runner exit.

## Existing vs New Module Decision
Do not add a new MTC_V2 feature yet. First check whether existing EMA/trend and pullback modules can express the rule. If not, any future feature must be default OFF and parity-gated.

## Salvageable Ideas
- Two-loss stop to prevent repeated re-entry chop.
- Distance-to-EMA anti-FOMO guard.
- Runner fraction by position size.
- EMA break as trend-runner exit.

## Final Status
READY_FOR_PYTHON_PROTOTYPE

## Next Action
Create a prototype spec only: deterministic OHLC rules for pullback proximity, impulse qualification, target, stop, re-entry, and runner exit. Do not run backtests yet.
