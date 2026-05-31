# Portable Known Limitations

This portable package is a clean continuation workspace, not the full historical repository.

## Intentional Exclusions

- Generated parity and report fixtures are intentionally excluded.
- TradingView Strategy Tester XLSX audit archives are intentionally excluded.
- Historical generated outputs under `reports/parity/` and `reports/optimization/` are not part of the main package.
- No live trading credentials, API keys, or real `.env` files are included.

## Test Expectations

The full historical pytest suite may fail if a test expects generated `reports/parity` fixture outputs that are not shipped in this package.

Supported portable verification is:

- `py_compile` checks for package scripts
- feature parity smoke after required generated traces are recreated
- reference oracle smoke after traces are generated
- factory regression dry-run

## Audit and Oracle Limits

TradingView final release audit still requires a separate audit workbook archive or fresh TradingView exports.

PineTS is the local `L0`-`L3` feature, indicator, and signal oracle. Python remains the local lifecycle, backtest, and optimization owner when PineTS does not emit lifecycle rows.

## Data Limits

The package currently includes one Binance chart CSV for BTCUSDT.P 1h. Additional symbols and timeframes should be added later under the same data structure after review.
