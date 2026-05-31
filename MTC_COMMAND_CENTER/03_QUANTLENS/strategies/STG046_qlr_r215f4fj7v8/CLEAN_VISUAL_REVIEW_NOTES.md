# Clean Visual Review Notes

## Purpose

`standalone_pine_visual_review_CLEAN.pine` is a readable TradingView inspection script for `QLR_R215f4fj7V8`.

It does not replace the original `standalone_pine_visual_review.pine`; it removes chart clutter by using `indicator()` instead of `strategy()`, no order labels, no default text labels, deduplicated signals, and a stricter no-man's-land filter.

## What Changed

- Uses small markers only by default.
- Adds `signal_cooldown_bars` default `20`.
- Suppresses same-direction repeated signals until cooldown or opposite reset.
- Suppresses bars where long and short raw conditions conflict.
- Keeps VWAP/trend guard and right-side-of-V source logic.
- Strengthens no-man's-land filter using:
  - chop around VWAP,
  - Bollinger width compression,
  - narrow recent range,
  - flat VWAP slope.
- Adds a small top-right table with candidate, timeframe, signal counts, active filters, and warning.

## Marker Legend

- Green triangle: filtered long trend continuation.
- Red triangle: filtered short trend continuation.
- Cyan diamond: right-side-of-V long.
- Orange diamond: right-side-of-V short proxy.
- Gray X: no-man's-land if enabled.
- Yellow X: conflict suppressed if debug labels enabled.

## Important Limits

- No profitability claim.
- No backtest/optimization.
- No alerts.
- No production MTC integration.
- Right-side-of-V short is symmetric proxy only.
