# QL_2026-05-01_LIQUID_INTRADAY_VWAP_PULLBACK_REVERSAL — Deterministic Spec

- **Status**: PROMOTED TO PROTOTYPE
- **Timeframe**: 15m

## Rules
* **Entry**: VWAP session proxy mean rolling window of 96 bars. Slope of proxy > 0 (long). Close above proxy and distance <= 0.4 * ATR.
* **Stop**: VWAP band proxy - 1.0 * standard deviation.
* **Target**: Fixed 2.0R.
