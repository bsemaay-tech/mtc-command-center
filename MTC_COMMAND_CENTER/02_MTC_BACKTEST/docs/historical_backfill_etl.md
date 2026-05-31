# Historical Backfill and ETL Procedure

## Scope
- Keep dataset lifecycle deterministic for parity and optimizer reliability.
- Do not change engine behavior; only data ingestion and validation flow.

## Inputs
- Source export or provider dump (`csv` or `parquet`)
- Target dataset key:
  - `symbol` (normalized, e.g. `BTCUSDT`)
  - `exchange` (upper-case, e.g. `BINANCE`)
  - `timeframe` (e.g. `15m`)
  - target date range

## Procedure
1. Place raw file under a staging folder (outside `data/`).
2. Convert to canonical schema (`timestamp, open, high, low, close, volume`).
3. Force UTC timestamps and sort by `timestamp`.
4. Drop exact duplicate timestamp rows.
5. Validate quality and checksum:
   - `python scripts/data_parity_guard.py --dataset <staging_file> --symbol BINANCE:BTCUSDT.P --exchange binance --time-col timestamp --timeframe 15m --strict-quality --out reports/backfill_quality.json`
6. Register checksum:
   - `python scripts/checksum_registry.py --registry reports/benchmarks/checksum_registry.json --dataset <staging_file> --symbol BTCUSDT --exchange BINANCE --timeframe 15m --update`
7. Move the validated file to `data/` with deterministic naming:
   - `<SYMBOL>_<TF>_<YYYYMMDD>_<YYYYMMDD>.parquet`
8. Rebuild dataset catalog:
   - `python scripts/build_dataset_catalog.py --data-dir data --out-json reports/benchmarks/dataset_catalog.json --out-csv reports/benchmarks/dataset_catalog.csv`
9. Re-verify registry after final path move:
   - `python scripts/checksum_registry.py --registry reports/benchmarks/checksum_registry.json --dataset data/<final_file>.parquet --verify`

## Failure Handling
- If quality guard fails (`duplicate_timestamps > 0` or `gap_count > 0`), do not publish dataset.
- If checksum verify fails after move, regenerate checksum entry and investigate file mutation cause.
- If symbol/exchange normalization differs from expected case profile, fix metadata before publishing.

## Publish Criteria
- Quality check is clean under `--strict-quality`.
- Dataset checksum is registered and verifies.
- Catalog includes the new file with correct coverage window.
- Full test suite remains green:
  - `python -m pytest mtc_backtest/tests -v`
