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

## 2026-04-28 Optimizer Detached Runner Ready

- This portable handoff is optimizer-detached-runner ready.
- The big optimization data bundle is external and intentionally not included.
- For large optimization, use the detached PowerShell script; do not run the big optimizer in the Codex foreground terminal.
- Next big resume policy: use `--max-workers 16`, pin `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, and `NUMEXPR_NUM_THREADS=1`.
- Preserve `resume_registry.sqlite` in the external run output when resuming, but do not include registry files in the portable zip.
- Detached mechanics smoke passed with 12 evaluations, metadata present, `duplicate_conflicts=0`, and `failed_evaluations=0`.
- Manual Codex UI close/reopen proof was not performed; treat it as optional manual proof before the real overnight resume.
- Heavy optimization outputs, worker folders, and all-evaluations CSVs are intentionally excluded.

## 2026-04-28 Optimizer Detached Runner Policy Addendum

- Big optimization data bundle remains external and is not included.
- Large optimization must use detached PowerShell, not Codex foreground terminal.
- Resume policy: explicit `--max-workers 16`, thread pinning with `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1`, preserved external `resume_registry.sqlite`, external `dataset_manifest.json`, and external `regime_registry.json`.
- Manual Codex UI close/reopen proof was not performed; detached mechanics smoke passed and this is not a handoff blocker.
- Heavy optimization outputs are intentionally excluded.
- Medium robust candidates are research seeds only and must not change Pine defaults.
- Optimization output does not claim TradingView release parity.
