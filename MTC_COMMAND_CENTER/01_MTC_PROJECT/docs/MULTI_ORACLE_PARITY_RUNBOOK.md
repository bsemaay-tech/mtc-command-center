# Multi Oracle Parity Runbook

- Command: `python parity_oracles/run_multi_oracle_case.py --case cases/BTCUSDT_15m_CORE_001.json --engines python_engine pinets pynecore vectorbt --baseline python_engine`
- Data hash: recorded in each engine `result.json` and comparator JSON.
- Config hash: recorded in each engine `result.json` and comparator JSON.
- Code hash: recorded in each engine `result.json` and comparator JSON.

## FAST_SUITE

- Scope: 3 small cases.
- Trigger: every code change.
- Engines: Python engine and PineTS.
- Levels: PineTS L0/L1/L2 only; Python engine L0-L6 if fast enough.
- Rule: no parity claim unless comparator JSON returns PASS or PASS_WITH_TOLERANCE.

## CORE_SUITE

- Scope: 20 representative cases.
- Trigger: before major patch.
- Engines: Python engine, PineTS, PyneCore where available.
- Levels: Python vs PineTS L1/L2/L3; Python vs PyneCore L1-L6 when PyneCore output exists.
- Rule: continue on failure; one atomic log folder per case.

## NIGHTLY_SUITE

- Scope: 100+ cases.
- Trigger: overnight.
- Engines: Python engine, PineTS, PyneCore where available, vectorbt sweeps if needed.
- Levels: L0-L6 where comparable.
- Rule: restart from existing `reports/parity/<case_id>` outputs and skip completed PASS comparisons unless forced.

## RELEASE_SUITE

- Scope: release candidate cases with TradingView export reference included.
- Trigger: before declaring parity-safe release.
- Engines: TradingView export, Python engine, PineTS, PyneCore where available.
- Levels: TradingView/Python L0-L6, Python/PineTS L1-L3, Python/PyneCore L1-L6.
- Rule: TradingView export remains final external reference when available.

## Standard Commands

- Scanner: `python tools/mtc_runtime_compat_scan.py --pine 01_PINE/MTC_V2.pine`
- Synthetic comparator L1: `python parity_oracles/compare/parity_compare.py --case cases/synthetic_multi_oracle_case.json --baseline python_engine --candidate pinets --level L1`
- Synthetic comparator L2: `python parity_oracles/compare/parity_compare.py --case cases/synthetic_multi_oracle_case.json --baseline python_engine --candidate pinets --level L2`
- PineTS runner stub: `python parity_oracles/engines/pinets_runner.py --case cases/synthetic_multi_oracle_case.json --out-dir reports/parity/SYNTH_001/pinets`
- Python runner stub: `python parity_oracles/engines/python_engine_runner.py --case cases/synthetic_multi_oracle_case.json --out-dir reports/parity/SYNTH_001/python_engine`
