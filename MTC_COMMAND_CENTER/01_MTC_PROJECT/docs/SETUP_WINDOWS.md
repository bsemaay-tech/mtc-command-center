# Windows Setup Draft

## Python

Recommended Python version: 3.11 or newer.

Create and activate a virtual environment from the portable package root:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Install the local Python package from the available project config:

```powershell
python -m pip install -e .\00_PYTHON
```

If a future package adds requirements files, install them explicitly after review:

```powershell
python -m pip install -r requirements.txt
```

## Node and PineTS

Node.js and npm are required for PineTS-backed local oracle checks when PineTS is available.

The current project expects PineTS support through local runner code under `parity_oracles/engines/`. If PineTS is not installed or available, PineTS checks should report unavailable instead of becoming release claims.

Do not install packages during package review. Install only after the user approves setup.

## Safe Compile Checks

```powershell
python -m py_compile tools/scaffold_new_feature.py
python -m py_compile parity_oracles/run_feature_parity.py
python -m py_compile parity_oracles/run_factory_regression_suite.py
python -m py_compile parity_oracles/reference_oracles/compare_reference_oracle.py
```

## Basic Pytest Smoke

```powershell
python -m pytest parity_oracles/tests -q
```

## Feature Parity Smoke

```powershell
python parity_oracles/run_feature_parity.py --contract feature_contracts/active/producer_range_filter_v1.yml --case cases/fast_suite_case_001_range_filter.json --oracles python pinets --levels L0 L1 L2 L3
```

## Reference Oracle Smoke

Generate the Range Filter reference trace:

```powershell
python parity_oracles/reference_oracles/producer_range_filter_v1_reference.py --case cases/fast_suite_case_001_range_filter.json --contract feature_contracts/active/producer_range_filter_v1.yml --out reports/INDEPENDENT_REFERENCE_ORACLE/range_filter_reference_trace.csv
```

Compare the independent reference against Python and PineTS traces:

```powershell
python parity_oracles/reference_oracles/compare_reference_oracle.py --reference reports/INDEPENDENT_REFERENCE_ORACLE/range_filter_reference_trace.csv --python-trace reports/parity/case_001_range_filter/features/producer_range_filter_v1/python_feature_trace.csv --pinets-trace reports/parity/case_001_range_filter/features/producer_range_filter_v1/pinets_feature_trace.csv --out-md reports/INDEPENDENT_REFERENCE_ORACLE/range_filter_reference_oracle_report.md --out-json reports/INDEPENDENT_REFERENCE_ORACLE/range_filter_reference_oracle_report.json
```

## Factory Regression Dry Run

```powershell
python parity_oracles/run_factory_regression_suite.py --suite fast --dry-run --out reports/FACTORY_REGRESSION_SUITE_V1/fast
```

## Data Note

The current portable package plan contains one Binance chart CSV:

```text
05_PARITY/01_TW_CHART_DATA/BINANCE_BTCUSDT.P, 60_consolidated_stable.csv
```

It should be placed under:

```text
data/chart/binance/BTCUSDTP/1h/
```

Future ETH, SOL, BNB, ADA, and other crypto chart CSVs can be added under the same structure after review.
