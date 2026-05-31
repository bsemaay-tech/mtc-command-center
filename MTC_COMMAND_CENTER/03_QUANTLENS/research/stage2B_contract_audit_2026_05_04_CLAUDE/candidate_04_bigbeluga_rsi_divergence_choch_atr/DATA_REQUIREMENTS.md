# DATA_REQUIREMENTS — BigBeluga

## Status
- **CURRENT_CRYPTO_DATA_ENOUGH_FOR_PROXY** (asset-agnostic indicator).
- No special data needs (OHLC + RSI(close) only).

## Caveats
- Strategy promises symmetry; backtest must include full bull and bear regimes (BTC 2020–2024 multi-cycle minimum).
- Lower-liquidity assets will produce more whipsaws.

## Decision rule
- Strategy is fairly testable on existing crypto bundle once look-ahead-clean implementation is built.
- This is the **only** of the six candidates whose data requirement is fully met by the current bundle.
