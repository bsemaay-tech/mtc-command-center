# parity_suite_350 quick start

## Execution contract note (2026-03-08)
- `OPP_SIGNAL` + `allow_flip=true` + `exit_on_opposite_signal=true` is now treated as a same-bar reversal path.
- Other close-style exits remain next-bar only.
- Canonical contract lives in `mtc_backtest/docs/PARITY_FREEZE.md`.

## Research note (2026-03-08)
- `optimizer_v0` walk-forward replay path had an alias-preservation bug:
  - `src/optimizer_v0/replay_candidates.py` rebuilt configs from alias-less dumps and could silently change candidate behavior.
- After alias-fix, corrected Supertrend walk-forward winner is:
  - `ATR 48`
  - `Factor 4.8`
  - `Entry Mode = Edge`
  - `Regime Lock = Off`
  - `Use HA = Off`
  - `Use Wicks = Off`
- `HA` and `Wicks` worsened OOS behavior in the 16-combo toggle sweep.
- `Regime Lock` and `Edge/Signal` produced identical outcomes for this naked Supertrend candidate.

## Research note (2026-03-09)
- `walk_forward_validate.py` train leg was not forwarding `--min-trades` / `--max-dd` into `optimizer_v0 run`.
- Fixed workflow contract:
  - train and replay legs now use the same thresholds
  - missing replay CSVs now degrade to `EMPTY` summary instead of crashing the workflow
- Supertrend `% SL + risk` research on top of the corrected base candidate:
  - naked base (`ATR 48 / F 4.8`): OOS `+752.30`, DD `19.79%`
  - net-focused SL+risk candidate: `% 0.3`, `risk_long=0.05`, `risk_short=0.2`, `max_leverage=3.0`
    - OOS `+484.21`, DD `6.67%`
  - risk-aware current-best candidate: `% 0.3`, `risk_long=0.01`, `risk_short=0.15`, `max_leverage=2.0`
    - OOS `+363.95`, DD `4.47%`
- Materialized candidates:
  - `mtc_backtest/configs/cases/supertrend_sl_risk_current_best_candidate_20260309.json`
  - `mtc_backtest/configs/cases/supertrend_sl_risk_net_candidate_20260309.json`
- Comparison report:
  - `mtc_backtest/results/walkforward/supertrend_sl_risk_comparison_20260309.xlsx`
- Important interpretation:
  - SL-only search without risk tuning was misleading because base config used `risk_long/short = 100`
  - after joint tuning, `%` mode remains the only viable SL family
  - full-period `2025-01-01 .. 2026-01-01` is still negative for all tested variants, but the risk-aware candidates materially reduce DD

## Research note (2026-03-09 continued)
- `train_top_score` replay was added because Pareto-only export was hiding OOS-better configs that were dominated on train.
- Wrapper hardening:
  - `run_supertrend_walkforward.py`, `run_supertrend_sl_walkforward.py`, and `run_supertrend_tp_walkforward.py` now call `python -m scripts.walk_forward_validate`
  - this removes the accidental dependency on ambient `PYTHONPATH`
- Revised no-TP winner after `train_top_score` replay:
  - `% SL 0.3`
  - `risk_long=0.01`
  - `risk_short=0.4`
  - `max_leverage=2.0`
  - OOS `+963.77`, DD `11.29%`
- Exit-layer continuation on top of that no-TP winner:
  - best TP: `% 2.5`
    - OOS `+1371.52`, DD `9.83%`
  - best BE on top of TP: `rr=2.0`, `buffer_r=0.2`
    - OOS `+1603.74`, DD `7.91%`
  - best trailing on top of TP+BE:
    - OOS `+436.50`, DD `7.13%`
    - rejected because net collapses versus TP and TP+BE
- Current OOS-best tested Supertrend branch:
  - `mtc_backtest/configs/cases/supertrend_sl_risk_tp_be_current_best_candidate_20260309.json`
- Stage comparison report:
  - `mtc_backtest/results/walkforward/supertrend_exit_stack_comparison_20260309.xlsx`
- Important qualifier:
  - least-bad full-period defensive branch is still `supertrend_sl_risk_balanced_candidate_20260309.json` with net `-139.19`, DD `12.6%`
  - OOS-best and full-period-least-bad are not the same candidate right now

## Comparison mode policy (current)
- Parity reporting now keeps two views together:
  - `raw strict` (full horizon)
  - `clip-overlap strict` (shared timeline only)
- Batch scripts auto-write both statuses into notes/output CSV.
- If `clip=PASS` but `raw=FAIL` with only trailing extra Python trades, case is tagged:
  - `TV_EARLY_TRADE_END_CANDIDATE`
  - with `gap_days` in notes
- Tracker columns written by workflow:
  - `compare_status` (canonical, raw strict)
  - `clip_strict_status`
  - `raw_strict_status`
  - `early_trade_end_candidate`
  - `gap_days`
  - `clip_tv_trades`, `clip_py_trades`, `raw_tv_trades`, `raw_py_trades`

## Current live status (2026-03-03)
- Active operational baseline is the downloaded TV XLSX in `tv_manual_inputs/001_parity_core_005_enable_long_trades_v01/`.
- Current verified live baseline parity is `241` trades, not `240`.
- Historical `baseline_freeze_record.json` values from earlier restart attempts are obsolete for the ongoing parity run and must not be treated as source-of-truth.
- Stable closed parity cases currently include:
  - `001` baseline
  - `236`
  - `281`
  - `395`
  - `404`
  - `412`
- Current confirmation-cluster rerun summary:
  - `PASS`: `18`
  - `MISMATCH`: `6`
  - `NOT_RUN`: `37`
- Remaining real confirmation mismatches with downloaded XLSX:
  - `398`
  - `401`
  - `402`
  - `409`
  - `416`
  - `422`
- Current technical classification of the open set:
  - `398`: likely confirmation/raw-signal divergence; TV stops at `2025-12-22 19:00 UTC`, Python opens an extra long on `2025-12-23 18:15 UTC`
  - `401`: mixed confirmation + broker-emulator liquidation cluster drift
  - `402`: not a clean pivot-only case; TV ends at `2025-09-25 02:30 UTC`, Python continues later, so capital/liquidation drift is also involved

Detailed handoff:
- `mtc_backtest/parity_suite_350/CURRENT_STATUS_HANDOFF_20260303.md`
- `mtc_backtest/parity_suite_350/compare_runs/CONFIRMATION_PROGRESS_20260303.md`

## 1) Initialize scaffold
```powershell
powershell -ExecutionPolicy Bypass -File mtc_backtest/parity_suite_350/run_parity_suite_350.ps1 -Stage init
```

## 2) Freeze baseline (Phase-0)
```powershell
powershell -ExecutionPolicy Bypass -File mtc_backtest/parity_suite_350/run_parity_suite_350.ps1 -Stage baseline-freeze -BaselineCaseId parity_core_001_baseline_touch -BaselineXlsx "mtc_backtest/parity_suite_350/manifests/baseline_sources/baseline_tv_export_FILLED_v6.xlsx"
```

Outputs:
- `manifests/baseline_freeze_record.json`
- `manifests/baseline_freeze_record.md`
- `manifests/frozen_baseline_case_parity_core_001_baseline_touch.json`

Historical note:
- the old freeze record still contains `240`, but that is not the live baseline used by the current parity operation
- the live operational baseline is the TV XLSX under `tv_manual_inputs/001_parity_core_005_enable_long_trades_v01/`
- current verified live count: `241`

## 3) Generate fresh case set from FILLED_v6 (457-source)
```powershell
powershell -ExecutionPolicy Bypass -File mtc_backtest/parity_suite_350/run_parity_suite_350.ps1 -Stage build-from-v6
```

Outputs:
- `manifests/cases_manifest_all.csv`
- `manifests/cases_manifest_core.csv`
- `manifests/cases_manifest_boundary.csv`
- `manifests/cases_manifest_pairwise.csv`
- `manifests/input_map_generation_report.json`
- rewritten `cases/*.json`

## 4) Sync TV folders to current manifest
```powershell
python mtc_backtest/parity_suite_350/scripts/sync_tv_case_folders.py --suite-root mtc_backtest/parity_suite_350
```

## 5) Build user tracker workbook
```powershell
python mtc_backtest/parity_suite_350/scripts/build_case_setup_guide.py --suite-root mtc_backtest/parity_suite_350 --no-preserve
```

Output:
- `mtc_backtest/parity_suite_350/CASE_SETUP_GUIDE.xlsx`

## 6) Put all TV XLSX exports into raw folder
- `mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/`

## 7) Auto-route XLSX to case folders
```powershell
powershell -ExecutionPolicy Bypass -File mtc_backtest/parity_suite_350/run_parity_suite_350.ps1 -Stage route
```

Notes:
- Route stage uses `--sequential-fallback` by default for ambiguous default-value cases.
- Best practice: export cases in `CASE_SETUP_GUIDE.xlsx` run_order order.

Optional:
```powershell
# dry run
powershell -ExecutionPolicy Bypass -File mtc_backtest/parity_suite_350/run_parity_suite_350.ps1 -Stage route -DryRun

# copy instead of move
powershell -ExecutionPolicy Bypass -File mtc_backtest/parity_suite_350/run_parity_suite_350.ps1 -Stage route -Copy
```

## Routing outputs
- `manifests/tv_collection_status.csv`
- `manifests/tv_unmatched.csv`
- updated `CASE_SETUP_GUIDE.xlsx` status columns

## Post-compare diagnostics (single command)
```powershell
python mtc_backtest/parity_suite_350/scripts/run_post_compare_diagnostics.py
```

Generates:
- `compare_runs/tv_trade_list_truncation_scan.csv`
- `compare_runs/mismatch_split_latest.csv`
- `compare_runs/mismatch_split_latest.md`
- `compare_runs/parity_policy_view_latest.csv`
- `compare_runs/parity_policy_view_latest.md`
