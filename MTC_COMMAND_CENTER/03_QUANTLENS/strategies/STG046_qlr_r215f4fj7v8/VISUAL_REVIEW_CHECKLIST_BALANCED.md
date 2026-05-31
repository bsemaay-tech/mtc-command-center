# BALANCED Visual Review Checklist

## First Chart

Open TradingView and load:
- Symbol: `BTCUSDT.P`
- Timeframe: `5m`
- Script: `standalone_pine_visual_review_BALANCED.pine`
- Mode: `BALANCED`

## Display Defaults

Use these defaults first:
- `show_filtered_signals = true`
- `show_raw_pulses = false`
- `show_vwap = true`
- `show_no_trade_zone = false`
- `show_stops = false`
- `show_targets = false`
- `show_debug_labels = false`

## What To Check

1. Confirm filtered markers are readable and not printed every few bars.
2. Confirm green trend-long triangles appear above VWAP during positive slope/range-break behavior.
3. Confirm red trend-short triangles appear below VWAP during negative slope/range-break behavior.
4. Confirm cyan right-side-of-V long diamonds appear only after a downside capitulation proxy and turn confirmation.
5. Confirm orange right-side-of-V short diamonds are treated as proxy-only and not overtrusted.
6. Confirm the table shows raw, filtered, blocked no-man's-land, blocked cooldown, and blocked conflict counts.
7. If too few markers appear, switch to `EXPLORATORY` before touching manual overrides.
8. If too many markers appear, switch to `STRICT`.

## PASS_VISUAL

Use PASS_VISUAL only if markers broadly match the intended visual behavior and the chart remains readable.

## FAIL_VISUAL

Use FAIL_VISUAL if markers consistently appear in sideways/no-man's-land price action, violate VWAP/trend side, or fire both long and short on the same bar.

## NEEDS_RULE_CLARIFICATION

Use NEEDS_RULE_CLARIFICATION if the visual proxy is plausible but the source material does not define enough detail for exact capitulation, right-side-of-V, stop, or target behavior.

## Notes For US Equities

For US equities, start with `BALANCED` on the native timeframe if known. If the market has gaps or thin premarket liquidity, disable extended-hours data or review regular session behavior separately before judging the marker quality.
