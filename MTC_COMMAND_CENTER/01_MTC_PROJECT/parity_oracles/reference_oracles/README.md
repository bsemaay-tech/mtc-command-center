# Independent Reference Oracles

This folder contains small, pure-Python expected-value calculators for feature-level parity checks.

## Role

- Cross-checks Python feature traces and PineTS feature traces against a third local reference.
- Works only at feature trace level.
- Does not replace the Python MTC engine, PineTS, or TradingView export.
- Must not import the production implementation it checks.

## Trace Format

Reference trace columns:

- `timestamp`
- `bar_index`
- `feature_id`
- `column_name`
- `expected_value`
- `value_type`
- `source`

Comparison verdicts:

- `REFERENCE_PASS`
- `PINETS_MISMATCH`
- `PYTHON_MISMATCH`
- `BOTH_MISMATCH`
- `NOT_COMPARABLE`

## Range Filter Example

Generate reference trace:

```powershell
python parity_oracles/reference_oracles/producer_range_filter_v1_reference.py --case cases/fast_suite_case_001_range_filter.json --contract feature_contracts/active/producer_range_filter_v1.yml --out reports/INDEPENDENT_REFERENCE_ORACLE/range_filter_reference_trace.csv
```

Compare reference against Python and PineTS traces:

```powershell
python parity_oracles/reference_oracles/compare_reference_oracle.py --reference reports/INDEPENDENT_REFERENCE_ORACLE/range_filter_reference_trace.csv --python-trace reports/parity/case_001/features/producer_range_filter_v1/python_feature_trace.csv --pinets-trace reports/parity/case_001/features/producer_range_filter_v1/pinets_feature_trace.csv --out-md reports/INDEPENDENT_REFERENCE_ORACLE/range_filter_reference_oracle_report.md --out-json reports/INDEPENDENT_REFERENCE_ORACLE/range_filter_reference_oracle_report.json
```
