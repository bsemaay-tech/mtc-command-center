# PineTS Adapter

This adapter will read PineTS parity results and expose dashboard-friendly parity summaries.

## MVP-0 State

Not implemented. PineTS and parity pipeline files are untouched.

## Future Contract

The adapter may read case manifests, parity result JSON, per-case logs, and aggregate summaries. It should output normalized records for `03_STATUS/PARITY_STATUS.json`.

## Safety

Do not edit parity engine code or TradingView exports from this adapter.
