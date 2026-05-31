# MTC_MAPPING_NOT_INTEGRATION — BigBeluga

## MTC role
**SIGNAL_PRODUCER_POSSIBLE** with FSM and partial-exit ladder.

## Producer raw signal
- Bull entry: `direction == false AND crossover(close, last_confirmed_pivot_high) [AND optionally divergence_flag_active]`.
- Bear entry: mirror.

## Non-repaint
- `pivothigh(10, 10)` is non-repainting only when read at `confirmed_bar_index + 10`. Any earlier read is repainting.
- Use `nz(ph[10])` style in Pine; in Python explicitly shift.

## Timeframe
- Native indicator-agnostic; recommended 1D and 4h.

## Stateful transform
- FSM with `direction` (bool), `last_confirmed_phigh`, `last_confirmed_plow`, divergence flag, anti-whipsaw cooldown. Non-trivial but standard.

## Filters
- Optional EMA200 trend filter, anti-whipsaw cooldown, liquidity gate.

## SL/TP compatibility
- Initial SL at price level: direct fit.
- Ladder TPs at price levels: needs MTC partial-exit support (3 partials).
- Trailing stop chandelier-style: needs MTC trailing-stop primitive.
- Opposite CHoCH exit: works as a separate exit transform.

## UI complexity
- High: pivot markers, trend coloured background, three TP lines, trail line, divergence highlight. Existing BigBeluga Pine indicator already does this — easiest path is to fork the indicator into a strategy.

## Parity risks
- The pivot confirmation lag is the most common parity bug.
- Trail-stop reset on each new high must match Pine `ta.highest()`-based logic.
