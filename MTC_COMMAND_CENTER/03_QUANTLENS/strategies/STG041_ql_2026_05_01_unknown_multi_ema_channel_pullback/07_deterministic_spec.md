# QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNEL_PULLBACK — Deterministic Spec

- **Status**: PROMOTED TO PROTOTYPE
- **Timeframe**: 15m

## Rules
* **Entry**: Price > EMA(200). Fast EMA(5) > Mid EMA(13). Price pulls back to touch or get near Mid EMA(13) (distance <= 0.4 * ATR).
* **Stop**: 5-bar swing low.
* **Target**: Fixed 2.0R.
