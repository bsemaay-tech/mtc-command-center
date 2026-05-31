# QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK — Deterministic Spec

- **Status**: PROMOTED TO PROTOTYPE
- **Timeframe**: 15m (Crypto proxy for 10m US Equities)

## Rules
* **Entry**: Close > 8 EMA and 8 EMA slope > 0. Distance to 8 EMA <= 0.35 * ATR(14). Preceding 3-bar impulse >= 1.0 * ATR(14).
* **Stop**: 3-bar swing low.
* **Target**: Fixed 2.0R.
