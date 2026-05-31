# Supertrend Extraction Report

Research seed only; not Pine default; not production parameter.

## Source

- Input granular seed file: `reports\optimization\seed_granularity_smoke\ranked\per_asset_timeframe_seed_candidates.csv`
- Producer: `Supertrend`

## Backup Files

- `optimization\parameter_library\supertrend\supertrend_best_by_asset_timeframe.backup_20260428T165353Z.csv`
- `optimization\parameter_library\supertrend\supertrend_seed_regions.backup_20260428T165353Z.yml`
- `optimization\parameter_library\supertrend\supertrend_rejected_regions.backup_20260428T165353Z.yml`
- `optimization\parameter_library\supertrend\supertrend_extraction_report.backup_20260428T165353Z.md`

## Seed Source Types

- `AGGREGATE_MEDIUM_SEED`: `5`
- `SMOKE_ASSET_TIMEFRAME_SEED`: `30`

## Asset/Timeframe Rows

- `BTCUSDT:15m`
- `BTCUSDT:1h`
- `BTCUSDT:4h`
- `ETHUSDT:15m`
- `ETHUSDT:1h`
- `ETHUSDT:4h`

## Warnings

- Smoke-derived rows are `SMOKE_ASSET_TIMEFRAME_SEED` and confidence LOW.
- Aggregate big-run rows are preserved as `AGGREGATE_MEDIUM_SEED`.
- No row is a Pine default or production parameter.
