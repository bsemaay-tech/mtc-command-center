# Codex Triage

## Executive Triage
Status: READY_FOR_PYTHON_PROTOTYPE

The transcript contains a codable candlestick playbook. It should be treated as a pattern-confirmation library plus confluence examples, not as one combined strategy.

## STOP Condition Check
- Closed source dependency: low; uses OHLC pattern definitions.
- Repaint/lookahead: low for candle patterns; high for support/resistance, trendline, and target selection if built with future pivots.
- Marketing risk: medium due "masterclass" and high-probability claims.
- Rule completeness: partial; entries/stops are described but target, context, trendline, and S/R construction need mechanical rules.
- MTC_V2 compatibility: plausible as candle confirmation around existing level modules.

## Strategy Completeness Check
- Entry: above bullish pattern high or below bearish pattern low.
- Exit: target next resistance/support or previous swing levels.
- Stop: beyond the pattern low/high or doji/pin bar.
- Risk: no fixed position sizing or R model.
- Timeframe: not specified.
- Market: broad claim, not validated.

## MTC_V2 Compatibility
Potential mapping:
- Pin bar confirmation.
- Engulfing confirmation.
- Morning/Evening Star confirmation.
- Doji as compression/pause marker, not standalone direction.
- Support/resistance or trendline confluence guard.
- Pattern high/low stop anchor.

## Existing vs New Module Decision
Before implementing, inspect existing MTC_V2 candle pattern and level proximity modules. If already present, this candidate may be a documentation/spec refinement rather than a new module. Any new pattern logic should be research-only and default OFF.

## Salvageable Ideas
- Pattern confirmation only when near past-only S/R or trendline.
- Momentum-loss filter using shrinking candles into support/resistance.
- Pattern high/low as deterministic entry and stop anchor.
- Doji cluster as breakout-watch condition rather than directional entry.

## Final Status
READY_FOR_PYTHON_PROTOTYPE

## Next Action
Pick one narrow variant, preferably `engulfing + support/resistance confluence`, and define exact OHLC ratios, level construction, entry, stop, and target before Python prototype.
