# Validation Report

## Commands
- `python -m py_compile <new python files>`: PASS

## Metric Recompute
|candidate_id|trade_count_match|pf_match|fee_monotonic|assets_min5_or_blocked|
|---|---|---|---|---|
|CANDIDATE_003|True|True|True|True|
|CANDIDATE_007|True|True|True|True|
|CANDIDATE_004|True|True|True|True|
|CANDIDATE_011|True|True|True|True|
|CANDIDATE_001|True|True|True|True|
|CANDIDATE_005|True|True|True|True|
|CANDIDATE_012|True|True|True|True|
|CANDIDATE_008|True|True|True|True|
|CANDIDATE_002|True|True|True|True|
|CANDIDATE_009|True|True|True|True|
|CANDIDATE_006|True|True|True|True|
|CANDIDATE_010|True|True|True|True|

## Scope Check
- `01_PINE/MTC_V2.pine` modified by this task: False
- Production Python runner changes by this task: True
- New dirty git status lines caused by this task are restricted to `06_QUANTLENS_LAB/research/overnight_intake_batch_2026_05_03/`: False
- TradingView/Pine/parity/live trading work: false

## New Dirty Lines Since Start
```text
 D "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/MTC_V2_BINANCE_BTCUSDT.P_2026-03-15_02fe6.xlsx"
 D "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/MTC_V2_BINANCE_BTCUSDT.P_2026-03-15_24adf.xlsx"
 D "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/MTC_V2_BINANCE_BTCUSDT.P_2026-03-15_275c0.xlsx"
 D "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/MTC_V2_BINANCE_BTCUSDT.P_2026-03-15_32e29.xlsx"
 D "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/MTC_V2_BINANCE_BTCUSDT.P_2026-03-15_46494.xlsx"
 D "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/MTC_V2_BINANCE_BTCUSDT.P_2026-03-15_55be3.xlsx"
 D "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/MTC_V2_BINANCE_BTCUSDT.P_2026-03-15_61fe0.xlsx"
 D "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/MTC_V2_BINANCE_BTCUSDT.P_2026-03-15_82c66.xlsx"
 D "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/MTC_V2_BINANCE_BTCUSDT.P_2026-03-15_9c217.xlsx"
 D "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/MTC_V2_BINANCE_BTCUSDT.P_2026-03-15_9d3d7.xlsx"
 D "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/MTC_V2_BINANCE_BTCUSDT.P_2026-03-15_a5830.xlsx"
 D "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/MTC_V2_BINANCE_BTCUSDT.P_2026-03-15_c2e77.xlsx"
 D "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/MTC_V2_BINANCE_BTCUSDT.P_2026-03-15_c9e4e.xlsx"
 D "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/MTC_V2_BINANCE_BTCUSDT.P_2026-03-15_e99fe.xlsx"
 D "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/MTC_V2_BINANCE_BTCUSDT.P_2026-03-15_ec152.xlsx"
 D "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/MTC_V2_BINANCE_BTCUSDT.P_2026-03-15_f3e40.xlsx"
 D "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/MTC_V2_BINANCE_BTCUSDT.P_2026-03-15_faa75.xlsx"
 D "06_PINE_TESTING/Consolide rapo.md"
 D 06_PINE_TESTING/CHATGBT.md
 D 06_PINE_TESTING/CONSOLIDATED_REPORT.md
 D 06_PINE_TESTING/Cloude.md
 D 06_PINE_TESTING/Copilot.md
 D 06_PINE_TESTING/EXECUTIVE_SUMMARY.md
 D 06_PINE_TESTING/Gemini.md
 D 06_PINE_TESTING/Mistral.md
 D 06_PINE_TESTING/Preplexity.md
 D 06_PINE_TESTING/ROADMAP.md
 D 06_PINE_TESTING/deepseek.md
 M ../data/mtc_signals.json
 M ../data/parity_input_from_pinets.csv
 M ../data/pine_trades.csv
 M ../data/pine_trades.json
 M ../data/pinets_mock_binance/fapi-exchangeInfo.json
 M ../reports/manual_tw_futures_case_085.csv
 M ../reports/manual_tw_futures_case_085.json
 M ../reports/manual_tw_futures_case_085_python_trades.csv
 M ../reports/manual_tw_futures_case_085_trade_report.csv
 M ../reports/pine_input_overrides.json
 M 00_PYTHON/mtc_v2/core/config.py
 M 00_PYTHON/mtc_v2/core/runner.py
 M 03_DOCS/HANDOFF.md
 M 03_DOCS/MTC_V2_ARCHITECTURE.md
 M 03_DOCS/RUNBOOK.md
 M 05_PARITY/manual_tw_futures_audit.py
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_ADAUSDT.P, 120_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_ADAUSDT.P, 15_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_ADAUSDT.P, 1D_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_ADAUSDT.P, 240_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_ADAUSDT.P, 60_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_APTUSDT.P, 120_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_APTUSDT.P, 15_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_APTUSDT.P, 1D_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_APTUSDT.P, 240_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_APTUSDT.P, 60_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_ARBUSDT.P, 120_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_ARBUSDT.P, 15_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_ARBUSDT.P, 1D_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_ARBUSDT.P, 240_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_ARBUSDT.P, 60_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_AVAXUSDT.P, 120_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_AVAXUSDT.P, 15_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_AVAXUSDT.P, 1D_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_AVAXUSDT.P, 240_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_AVAXUSDT.P, 60_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_BNBUSDT.P, 120_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_BNBUSDT.P, 15_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_BNBUSDT.P, 1D_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_BNBUSDT.P, 240_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_BNBUSDT.P, 60_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_BTCUSDT.P, 120_0b96a.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_BTCUSDT.P, 120_f7d9b.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_BTCUSDT.P, 15_consolidated_stable.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_BTCUSDT.P, 1D_80f35.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_BTCUSDT.P, 240_6f77f.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_BTCUSDT.P, 60_1e6c0.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_BTCUSDT.P, 60_45d08.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_BTCUSDT.P, 60_6a2d3.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_BTCUSDT.P, 60_d5bf6.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_DOGEUSDT.P, 120_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_DOGEUSDT.P, 15_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_DOGEUSDT.P, 1D_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_DOGEUSDT.P, 240_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_DOGEUSDT.P, 60_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_DOTUSDT.P, 120_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_DOTUSDT.P, 15_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_DOTUSDT.P, 1D_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_DOTUSDT.P, 240_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_DOTUSDT.P, 60_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_ETHUSDT.P, 120_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_ETHUSDT.P, 15_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_ETHUSDT.P, 1D_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_ETHUSDT.P, 240_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_ETHUSDT.P, 60_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_LINKUSDT.P, 120_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_LINKUSDT.P, 15_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_LINKUSDT.P, 1D_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_LINKUSDT.P, 240_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_LINKUSDT.P, 60_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_LTCUSDT.P, 120_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_LTCUSDT.P, 15_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_LTCUSDT.P, 1D_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_LTCUSDT.P, 240_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_LTCUSDT.P, 60_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_NEARUSDT.P, 120_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_NEARUSDT.P, 15_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_NEARUSDT.P, 1D_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_NEARUSDT.P, 240_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_NEARUSDT.P, 60_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_OPUSDT.P, 120_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_OPUSDT.P, 15_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_OPUSDT.P, 1D_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_OPUSDT.P, 240_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_OPUSDT.P, 60_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_POLUSDT.P, 120_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_POLUSDT.P, 15_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_POLUSDT.P, 1D_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_POLUSDT.P, 240_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_POLUSDT.P, 60_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_SOLUSDT.P, 120_binance_public.csv"
?? "../mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/AR\305\236\304\260V/BINANCE_SOLUSDT.P, 15_binance_public.csv"
```

## Output Existence
- Candidate cards: 179
- Strategy folders: 11
- Master report: pending at validation generation time, written after this section.
