# Codex Triage

## Executive Triage
Status: READY_FOR_PYTHON_PROTOTYPE

The transcript contains three codable Bollinger Band setup families. It is useful, but too broad as a single strategy. The first implementation should isolate one deterministic variant.

## STOP Condition Check
- Closed source dependency: low; uses standard Bollinger Bands.
- Repaint/lookahead: low for bands; medium if support/resistance, trendlines, or range boundaries use future pivots.
- Marketing risk: medium due broad "expert" and high-quality claims.
- Rule completeness: partial; setup logic is clear but stops, targets, exact band-width thresholds, and confirmations are missing.
- MTC_V2 compatibility: plausible as volatility regime, breakout confirmation, mean-reversion guard, or trend pullback module.

## Strategy Completeness Check
- Entry: described for breakout, reversal, and pullback variants.
- Exit: not fully specified; reversal implies opposite band/range movement, pullback/breakout exits unspecified.
- Stop: not specified.
- Risk: not specified.
- Timeframe: not specified.
- Market: broad claim, not validated.

## MTC_V2 Compatibility
Potential mapping:
- Bollinger Band width volatility regime filter.
- Squeeze/range breakout entry gate.
- Mean-reversion reversal entry gate.
- Middle-band trend pullback entry gate.
- Support/resistance or candle confirmation guard.

## Existing vs New Module Decision
Inspect existing volatility, band, and range-breakout modules before any implementation. If missing, prototype as research-only and default OFF. Do not merge all three setups into one feature.

## Salvageable Ideas
- Band width as low/high volatility regime detector.
- Avoid trend strategies when bands are narrow.
- Avoid reversal strategies when bands are wide.
- Breakout after narrow-band compression.
- Middle-band pullback in established band trend.

## Final Status
READY_FOR_PYTHON_PROTOTYPE

## Next Action
Choose one prototype variant. Recommended first variant: Bollinger squeeze/range breakout with exact band-width threshold, range containment rule, breakout close rule, stop, and target.
