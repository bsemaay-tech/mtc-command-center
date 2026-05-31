# BALANCED Visual Review Notes

## Scope

This file documents `standalone_pine_visual_review_BALANCED.pine` for candidate `QLR_R215f4fj7V8`.

The script is visual-only:
- It uses `indicator()`, not `strategy()`.
- It does not place orders.
- It does not create alerts.
- It does not modify or integrate with `MTC_V2.pine`.
- It is not a profitability test.

## Why This Version Exists

`standalone_pine_visual_review_CLEAN.pine` reduced label and marker clutter, but its defaults were too strict for practical manual review. The BALANCED version keeps the chart readable while exposing more filtered candidate markers.

## Review Modes

### STRICT

STRICT is closest to the CLEAN file:
- cooldown preset: 20 bars
- breakout lookback preset: 12 bars
- strongest VWAP and no-man's-land filters
- intended for final visual sanity after candidate behavior is understood

### BALANCED

BALANCED is the default:
- cooldown preset: 10 bars
- breakout lookback preset: 7 bars
- VWAP guard remains active
- no-man's-land filter remains active but is less aggressive than STRICT
- intended first mode for BTCUSDT.P 5m manual review

### EXPLORATORY

EXPLORATORY is for rule inspection only:
- cooldown preset: 4 bars
- weaker no-man's-land blocking
- lower capitulation thresholds
- still blocks same-bar long/short conflicts
- should not be interpreted as better or more profitable

## Manual Overrides

The manual override inputs default to `0`, which means the selected review mode supplies the internal preset. Enter a non-zero value only when inspecting whether a specific threshold is suppressing expected markers.

## Marker Legend

- Green triangle: filtered trend-continuation long.
- Red triangle: filtered trend-continuation short.
- Cyan diamond: right-side-of-V long.
- Orange diamond: right-side-of-V short proxy.
- Faint circles/diamonds: optional raw pulses when `show_raw_pulses = true`.
- Gray X: optional no-man's-land marker when `show_no_trade_zone = true`.

## Source-Faithful Boundaries

The logic remains a visual proxy for Lance Breitstein-style concepts:
- avoid no-man's-land,
- respect VWAP/trend side,
- inspect trend continuation,
- inspect panic/capitulation followed by right-side-of-V confirmation,
- suppress ambiguous same-bar long/short conflicts.

It is not a generic EMA crossover, optimized breakout system, or production MTC signal.
