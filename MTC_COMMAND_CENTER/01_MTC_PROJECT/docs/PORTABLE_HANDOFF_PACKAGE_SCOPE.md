# Portable Handoff Package Scope

## Purpose

The portable handoff package is a clean continuation workspace for MTC V2 development. It should let another developer or agent continue Pine, Python, parity factory, reference oracle, and planning work without the original repository.

## Main Package Includes

- canonical Pine source: `01_PINE/MTC_V2.pine`
- Python MTC V2 source and test source under `00_PYTHON/`
- Feature Factory and parity oracle source under `parity_oracles/`
- feature contracts, schemas, templates, and acceptance profiles under `feature_contracts/`
- current architecture, handoff, runbook, workflow, and oracle policy docs
- local smoke case fixtures under `cases/`
- helper scripts under `tools/`
- the approved Binance chart CSV under `data/chart/binance/<symbol>/<timeframe>/`

## Main Package Excludes

- `.git/`
- virtual environments
- `node_modules/`
- Python caches and test caches
- generated parity reports
- generated optimization reports
- logs, temporary files, and backup files
- local secrets or real `.env` files
- TradingView audit XLSX archives unless separately approved

## Separate Audit Bundle Candidates

TradingView Strategy Tester XLSX exports and tracker workbooks are review-needed. They can be useful as audit evidence, but they are not required for the main portable code package and can make the handoff large and stale.

Put these into a separate audit bundle only if the user explicitly approves:

- `05_PARITY/TW_EXPORT_CASES_V2/`
- `05_PARITY/MTC_V2_TW_EXPORT_CASE_TRACKER.xlsx`
- selected historical audit reports
- selected manual TradingView audit outputs

## Future Optimization Data Bundle Candidates

Future optimization data should stay separate until the schema and source labels are approved.

Candidates:

- additional Binance chart CSV symbols and timeframes
- non-Binance exchange data
- downloaded CCXT or exchange-native OHLCV data
- scoring profiles and optimization job examples

## Data Source Rules

TradingView chart CSV data and TradingView Strategy Tester XLSX exports are different artifacts.

- Chart CSV files are market data inputs.
- Strategy Tester XLSX files are audit outputs with settings, trades, and performance views.
- Downloaded exchange data must be labeled separately from TradingView chart exports.

## Reports and Tests

Generated reports are excluded because they are reproducible outputs, can be heavy, and may reflect stale intermediate states.

Test source files are included because they define expected behavior and smoke checks. Test outputs, `.pytest_cache/`, and `__pycache__/` are excluded because they are local generated artifacts.
# Optimization Data Bundle Scope

Large optimization datasets are intentionally outside `MTC_V2_PORTABLE_HANDOFF`.

The portable package may include rules, schemas, examples, and lightweight validators, but it must not include the full chart-data archive or `MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427`.

Future optimizer runs should reference the external bundle by manifest and `dataset_id`, not by copying data into the handoff zip.
