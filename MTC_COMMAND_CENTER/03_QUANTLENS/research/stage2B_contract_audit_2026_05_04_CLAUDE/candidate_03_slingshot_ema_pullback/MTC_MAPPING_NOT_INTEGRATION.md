# MTC_MAPPING_NOT_INTEGRATION — Slingshot

## MTC role
**SIGNAL_PRODUCER_POSSIBLE** — the cleanest fit of the six candidates.

## Producer raw signal
`raw_slingshot_long = prior_strength_any AND pullback_flag AND fresh_cross_up_EMA_high_4`

## Non-repaint
- All inputs (close, EMA, rolling pullback flag) on bar close → safe.
- Trigger evaluated on close; entry next bar open.

## Timeframe
- 1D native; supports 4h or 1h with rescaled context.
- Single TF — no HTF dependency required (optional benchmark gate is HTF-friendly but not required).

## Stateful transform
- Stateless apart from the rolling pullback flag. Easy.

## Filters
- Prior-strength OR-gate (multi-leg; needs UI for which legs to enable).
- Optional macro gate.

## SL/TP compatibility
- Stop = price level. Direct fit.
- TP = price level (R-multiple) or trail-MA. Direct fit (existing MTC primitives).
- Time stop = bar count. Compatible.

## UI complexity
- Low–Medium: one EMA pane line, pullback-state visualization, fresh-cross marker.

## Parity risks
- EMA series choice (`EMA(high)` vs `EMA(close)`) is the most common bug to expect.
- Otherwise low-risk strategy to port.
