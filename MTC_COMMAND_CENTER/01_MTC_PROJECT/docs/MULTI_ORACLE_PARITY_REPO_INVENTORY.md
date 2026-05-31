# Multi Oracle Parity Repo Inventory

- Command: `python --version; pip --version; node --version; npm.cmd --version; git status --short`
- Data hash: not applicable for repo inventory
- Config hash: not applicable for repo inventory
- Code hash: `fbc1392b1f1065a418eabcd5149259f98087b55c`
- Repo root: `C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2`
- Sandbox path observed: `C:\Users\CodexSandboxOffline\.codex\.sandbox\cwd\ad3f83d068fc54d4`

## Tool Versions

- Python: `3.14.2`
- pip: `26.0.1`
- Node: `v24.13.0`
- npm: `11.6.2` via `npm.cmd`; direct `npm` hit PowerShell execution policy.
- `rg`: access denied in this sandbox, PowerShell recursive scans used instead.

## Git Status Notes

- Worktree already had deleted files under `06_PINE_TESTING`.
- Worktree already had modified/generated files under `../data`, `../reports`, and many untracked parity export artifacts.
- This implementation is additive under `docs`, `tools`, `parity_oracles`, `experiments`, `cases`, and `reports/parity/SYNTH_001`.

## Pine Source Files

- `01_PINE/MTC_V2.pine`
- Pine scanner output: `reports/mtc_runtime_compat_scan.md`
- Scanner detected Pine v6, one `strategy(...)`, 10 `request.security`, 2 `strategy.entry`, 8 `strategy.exit`, 10 `strategy.close`, 152 `input.*`, and 88 plot calls.

## Existing Python Engine Files

- `00_PYTHON/mtc_v2/core/runner.py`
- `00_PYTHON/mtc_v2/core/config.py`
- `00_PYTHON/mtc_v2/core/confirmation.py`
- `00_PYTHON/mtc_v2/core/exits.py`
- `00_PYTHON/mtc_v2/core/gates.py`
- `00_PYTHON/mtc_v2/core/htf.py`
- `00_PYTHON/mtc_v2/core/indicators.py`
- `00_PYTHON/mtc_v2/core/position_manager.py`
- `00_PYTHON/mtc_v2/core/position_sizer.py`
- `00_PYTHON/mtc_v2/signals/supertrend.py`

## Existing Parity Files

- `05_PARITY/parity_summary.md`
- `05_PARITY/parity_results.json`
- `05_PARITY/validate_export_parity.py`
- `05_PARITY/manual_tw_futures_audit.py`
- `05_PARITY/manual_tw_lifecycle_audit.py`
- `05_PARITY/run_close_only_canonical.py`
- `05_PARITY/_nightly/parity_summary.md`
- `05_PARITY/_nightly/parity_results.json`

## Existing TradingView Export Files

- `05_PARITY/TW_EXPORT_CASES_V2/case_001..case_162`
- Many `MTC_V2...xlsx` and `MTCV2...xlsx` exports exist under case folders.
- Existing chart data includes `05_PARITY/01_TW_CHART_DATA/BINANCE_BTCUSDT.P, 60_consolidated_stable.csv`.

## Existing Data Files

- `05_PARITY/MTC_V2_PARITY_CASES.csv`
- `05_PARITY/MTC_V2_TW_EXPORT_CASE_SUITE_V2.csv`
- `05_PARITY/MTC_V2_TW_EXPORT_CASE_SUITE_V2.json`
- `05_PARITY/_nightly/case_queue.json`
- `../data/pinets_mock_binance/*.json` exists outside this workspace root.

## Requirements / Project Files

- `00_PYTHON/pyproject.toml`
- No root `requirements.txt` was detected in the workspace root scan.

## Existing Tests

- `00_PYTHON/test_parity.py`
- `00_PYTHON/test_band_calculation.py`
- `00_PYTHON/mtc_v2/tests/test_advanced_confirm.py`
- `00_PYTHON/mtc_v2/tests/test_capital_block_fix.py`
- `00_PYTHON/mtc_v2/tests/test_htf_infrastructure.py`
- `00_PYTHON/mtc_v2/tests/test_l12_ma_filters.py`
- `00_PYTHON/mtc_v2/tests/test_l12_new_filters.py`
- `00_PYTHON/mtc_v2/tests/test_l18b_scaffold.py`
- `00_PYTHON/mtc_v2/tests/test_level_retest.py`
- `00_PYTHON/mtc_v2/tests/test_manual_tw_futures_audit.py`
- `00_PYTHON/mtc_v2/tests/test_plan_b_gates.py`
- `00_PYTHON/mtc_v2/tests/test_supertrend_smoke.py`
