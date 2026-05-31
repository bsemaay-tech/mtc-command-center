# QL_Crabel_Range_Expansion_v0

Python-only QuantLens research prototype for the Crabel-style range expansion idea.

## Run

```powershell
python 06_QUANTLENS_LAB/research/crabel_range_expansion/run_crabel_backtest.py
```

## Scope

- Uses repo-local Binance futures 1D CSV data from `MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427`.
- Tests BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, and XRPUSDT.
- Runs expansion multipliers `0.50, 0.75, 0.90, 1.00, 1.25`.
- Runs four exit variants and three same-bar ambiguity modes.
- Does not write Pine Script and does not change production MTC code.

## Outputs

- `reports/QL_CRABEL_RANGE_EXPANSION_REPORT.md`
- `reports/QL_CRABEL_RANGE_EXPANSION_RESULTS.csv`
- `reports/QL_CRABEL_RANGE_EXPANSION_TRADES.csv`
