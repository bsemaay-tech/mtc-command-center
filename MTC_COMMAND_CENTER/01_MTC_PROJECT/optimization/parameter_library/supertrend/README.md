# Supertrend Parameter Library

Research seeds only; not Pine defaults; not production parameters.

This namespace stores Supertrend producer research seeds extracted from optimization outputs. Current seeds are aggregate medium robust research rows from the partial big overnight run. Asset/timeframe granular seed ranking is not yet available in the current output.

## 2026-04-28 Granular Smoke Seeds

- Supertrend now has smoke-derived per-asset/per-timeframe research seed rows from `reports/optimization/seed_granularity_smoke/`.
- Existing aggregate medium seeds from the partial big overnight run are preserved separately as `AGGREGATE_MEDIUM_SEED`.
- New rows are marked `SMOKE_ASSET_TIMEFRAME_SEED` / `SMOKE_RESEARCH_SEED` and `granularity_status=ASSET_TIMEFRAME_AVAILABLE`.
- These rows prove the ranking/extraction pipeline only; they are not Pine defaults, production parameters, or final optimization conclusions.
