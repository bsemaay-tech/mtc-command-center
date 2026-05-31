# MTC Module Mapping

## Candidate Role
This candidate can map to volatility regime filtering and setup-specific entry gates.

## Proposed Signals
- `bb_mid`: `SMA(close, 20)`.
- `bb_upper`: `bb_mid + 2 * stdev(close, 20)`.
- `bb_lower`: `bb_mid - 2 * stdev(close, 20)`.
- `bb_width`: `(bb_upper - bb_lower) / bb_mid`.
- `low_vol_regime`: band width below threshold.
- `high_vol_regime`: band width above threshold.

## Breakout Variant
- Context: narrow bands and sideways containment.
- Long trigger: strong close above upper band/range.
- Short trigger: strong close below lower band/range.
- Missing: stop and target definitions.

## Reversal Variant
- Context: narrow/range regime.
- Short trigger: upper band touch/rejection.
- Long trigger: lower band touch/rejection.
- Missing: candle confirmation, stop, and target definitions.

## Pullback Variant
- Uptrend context: price between middle and upper band.
- Long trigger: pullback to middle band.
- Downtrend context: price between middle and lower band.
- Short trigger: pullback to middle band.
- Missing: confirmation and stop/target definitions.

## Integration Boundary
No Pine or production Python change should be made until one variant is selected and all missing trade-management rules are specified.
