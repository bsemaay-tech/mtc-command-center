# TradingView Export Adapter

This adapter will read TradingView exports that the user manually provides.

## MVP-0 State

Not implemented. Export files are never modified.

## Future Contract

The adapter may validate file presence, timestamps, symbols, timeframes, and expected columns. It should produce data health warnings for `03_STATUS/DATA_HEALTH_STATUS.json`.

## Safety

Treat TradingView exports as immutable source evidence.
