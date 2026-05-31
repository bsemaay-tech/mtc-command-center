# QL_2026-05-01_ANY_BOLLINGER_BANDS_20_2_TRI_SETUP — Deterministic Spec

- **Status**: PROMOTED TO PROTOTYPE
- **Timeframe**: 1h

## Rules
* **Entry**: BB width is inside the lowest 25% quantile of past 200 bars (Squeeze). Entry when close crosses outside upper Bollinger Band and signal candle body is >= 0.25 * ATR.
* **Stop**: 5-bar swing low.
* **Target**: Fixed 2.0R.
