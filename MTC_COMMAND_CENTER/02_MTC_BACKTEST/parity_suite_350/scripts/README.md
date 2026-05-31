# scripts

- `case_rules.json`: dependency and routing contract.
- `bootstrap_from_340.py`: builds initial 350 manifests/case-json set from suite_340 with dedupe.
- `freeze_baseline_record.py`: freezes baseline metadata from TV XLSX + baseline case JSON.
- `generate_case_set_from_input_map.py`: rebuilds full case/manifest set from `input_map_FILLED_v6.xlsx` (457-source).
- `optimize_ui_coverage_case_set.py`: reduces case set to minimum from-scratch UI coverage set.
- `build_case_setup_guide.py`: builds `CASE_SETUP_GUIDE.xlsx` from manifest.
- `sync_tv_case_folders.py`: archives obsolete case folders and creates only current manifest folders.
- `route_tv_xlsx.py`: routes raw TradingView XLSX exports to case folders.

## usage

```powershell
python mtc_backtest/parity_suite_350/scripts/bootstrap_from_340.py --workspace-root . --source-suite mtc_backtest/parity_suite_340 --target-suite mtc_backtest/parity_suite_350
python mtc_backtest/parity_suite_350/scripts/freeze_baseline_record.py --workspace-root . --suite-root mtc_backtest/parity_suite_350 --baseline-case-id parity_core_001_baseline_touch --baseline-xlsx "mtc_backtest/parity_suite_340/tv_manual_inputs/TW Ekran goruntusu/MT_CORE2_BINANCE_BTCUSDT.P_2026-02-25_afc89_FILLED_v6.xlsx"
python mtc_backtest/parity_suite_350/scripts/generate_case_set_from_input_map.py --suite-root mtc_backtest/parity_suite_350 --input-map mtc_backtest/parity_suite_350/manifests/input_map_FILLED_v6.xlsx --purge-cases
python mtc_backtest/parity_suite_350/scripts/optimize_ui_coverage_case_set.py --suite-root mtc_backtest/parity_suite_350 --baseline-case-id parity_core_001_baseline_touch
python mtc_backtest/parity_suite_350/scripts/sync_tv_case_folders.py --suite-root mtc_backtest/parity_suite_350
python mtc_backtest/parity_suite_350/scripts/build_case_setup_guide.py --suite-root mtc_backtest/parity_suite_350
python mtc_backtest/parity_suite_350/scripts/route_tv_xlsx.py --suite-root mtc_backtest/parity_suite_350
```
