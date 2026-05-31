# QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL — Deterministic Spec

- **Status**: PROMOTED TO PROTOTYPE
- **Timeframe**: 15m (Crypto proxy)

## Rules
* **Entry**: Close > 8 EMA and 8 EMA slope > 0. Distance to 8 EMA <= 0.35 * ATR(14).
* **Stop**: 3-bar swing low.
* **Exit**: Dynamic trailing exit when price closes crossing below the 8 EMA line.
