# Clean Visual Review Checklist

## First Setup

1. Open TradingView on a liquid intraday US equity chart.
2. Use `5m` first.
3. Add `standalone_pine_visual_review_CLEAN.pine`.
4. Keep defaults initially:
   - `show_raw_pulses=false`
   - `show_filtered_signals=true`
   - `show_vwap=true`
   - `show_no_trade_zone=false`
   - `show_stops=false`
   - `show_targets=false`
   - `show_debug_labels=false`

## PASS_VISUAL

- Signals are sparse enough to inspect.
- Long signals appear above VWAP after trend/range break or after right-side-of-V confirmation.
- Cyan right-side-of-V long marker appears after panic and after price stops falling.
- Short proxy markers do not conflict with long markers.
- No-man's-land areas do not spam signals.

## FAIL_VISUAL

- Repeated same-direction markers still spam the trend.
- Long and short markers appear on the same bar.
- Long markers appear below VWAP without capitulation/turn confirmation.
- Signals cluster inside flat VWAP chop.

## NEEDS_RULE_CLARIFICATION

- Chart needs news/catalyst context not visible in OHLCV.
- A discretionary setup looks correct but the proxy does not mark it.
- The source rule needs a clearer threshold before coding.

## Optional Toggles

- Turn on `show_raw_pulses` only to debug why filtered signals disappeared.
- Turn on `show_no_trade_zone` to see suppressed chop zones.
- Turn on `show_stops` / `show_targets` only for a few examples; leave off for normal review.
