# MTC Engine Adapter

This adapter will read MTC_v2 Python engine outputs and summarize them for MCC status files.

## MVP-0 State

Not implemented. No Python engine files are modified.

## Future Contract

The adapter may read run manifests, metrics summaries, logs, and error reports. It should output normalized backtest status records for `03_STATUS/BACKTEST_STATUS.json`.

## Safety

Read and report only unless a future task explicitly approves deeper integration.
