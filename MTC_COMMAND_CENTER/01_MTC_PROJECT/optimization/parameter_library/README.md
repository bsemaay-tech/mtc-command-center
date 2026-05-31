# Optimization Parameter Library

Research seeds only; not Pine defaults; not production parameters.

## What This Is

The parameter library stores reusable research seed settings and parameter regions found during staged optimization.

## Why It Exists

It reduces search-space waste by preventing future optimization stages from testing exits, filters, gates, and regime mitigations across clearly weak producer settings.

## How To Use It

1. Run producer-only baseline research.
2. Save accepted producer seeds under the producer namespace.
3. Use those seeds as inputs for exit/risk refinement.
4. Use refined seeds for filter/gate evaluation.
5. Use stable candidates for regime mitigation and cross-market validation.

## Why Seeds Are Not Production Defaults

Seeds are research evidence. They are not strict robust candidates, not TradingView-audited, and not authorized Pine defaults.

## Adding New Producers

Each producer gets its own namespace, for example `supertrend/`, `range_filter/`, or a future producer id. Shared exit/risk/filter/regime templates belong under `shared/`.

## Per-Asset/Timeframe Seed Ranking

- Per-asset/per-timeframe seed ranking is now required for staged optimization outputs; aggregate candidate rows are not enough for exit/filter refinement.
- Future producer-only runs must emit `ranked/per_asset_timeframe_seed_candidates.csv` and `ranked/per_asset_timeframe_summary.csv`.
- Refinement jobs must consume seeds from `optimization/parameter_library/`, not promote aggregate medium candidates directly.
- Smoke-derived asset/timeframe seeds are schema/pipeline proof only; they are not Pine defaults, not production parameters, and not final optimization conclusions.
- Reference: `docs/optimization/SEARCH_SPACE_REDUCTION_AND_SMART_SAMPLING.md`, `optimization/parameter_library/README.md`, and `reports/optimization/seed_granularity/PER_ASSET_TIMEFRAME_SEED_RANKING_REPORT.md`.

- Each producer namespace should keep aggregate research rows separate from granular asset/timeframe seed rows.
