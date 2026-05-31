# Current Status Handoff - 2026-03-04

## Canonical Current Truth
Use this handoff with `PARITY_STATUS_FINAL_20260304.md`.

Current parity state:
- `PASS`: `316`
- `PASS(reuse)`: `121`
- `MISMATCH`: `2`
- `SKIP`: `18`
- executable pass rate: `437 / 439 = 99.54%`

Open blockers:
- `402`
- `416`

## Source Priority
When sources disagree, use this order:
1. latest case-level compare CSV in `compare_runs/`
2. this handoff
3. tracker workbook

## Live Evidence Files
- `mtc_backtest/parity_suite_350/compare_runs/current362_363.csv`
- `mtc_backtest/parity_suite_350/compare_runs/probe_patch_trailstart_anchors_summary.csv`
- `mtc_backtest/parity_suite_350/compare_runs/verify97_402.csv`
- `mtc_backtest/parity_suite_350/compare_runs/verify97_416.csv`
- `mtc_backtest/parity_suite_350/PARITY_STATUS_FINAL_20260304.md`

## Resolved in This Session
### 362 / 363
- Status moved to `PASS`.
- Root cause was `TRAIL` lifecycle conflation.
- Safe discriminator added:
  - if bar-start trailing stop is hit intrabar -> stop-style trail fill path
  - else -> close-style trail path
- Regression anchors stayed green (`001`, `236`, `281`, `395`, `415`).

## Remaining Blockers
### 402
- Python continues after TV cutoff.
- First 123 trades align; remaining gap is lifecycle/confirmation after the final TV BE exit.

### 416
- TV emits entry-attempt style debug markers but no closed trade is created.
- Treat as execution/no-fill divergence until disproven.

## Stable Closed Anchors
Keep these as regression anchors:
- `001`, `236`, `281`, `362`, `363`, `395`, `398`, `401`, `404`, `406`, `409`, `412`, `415`, `422`

## Workbook Status
`CASE_SETUP_GUIDE_tagged_v6_conflict_candidates.xlsx` is synced:
- `362`, `363` -> `PASS`
- `402`, `416` -> `MISMATCH`

## Mandatory Session-End Update Rule
Every meaningful session must update:
- `100_PROJECT_MEMORY_FİLE/00_LLM_HANDOFF.md`
- `100_PROJECT_MEMORY_FİLE/01_Project_contex.md`
- `100_PROJECT_MEMORY_FİLE/09_NEXT_STEPS.md`
- `mtc_backtest/parity_suite_350/CURRENT_STATUS_HANDOFF_20260304.md`
- `mtc_backtest/parity_suite_350/PARITY_STATUS_FINAL_20260304.md`

If a session changes the open-blocker set, these files must be updated before the session ends.

## Session Note - 362/363 Same-Bar Lifecycle
- Isolation evidence report:
  - `mtc_backtest/parity_suite_350/triage/CASE_362_363_SAME_BAR_LIFECYCLE_20260304.md`
- Key bar validated: `2025-10-03 17:00 UTC` (`18:00` TV local)
- Result: TRAIL exit + same-direction same-bar reentry confirmed aligned in Python and TV.

## Session Note - 2026-03-08 OPP Signal Same-Bar Flip Fix
- Trigger workbook:
  - `mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/Supertrend ATR 21 F 5.5.xlsx`
- Root cause:
  - `OPP_SIGNAL` closed the active side at bar close but also blocked same-bar opposite entry, which can collapse `Entry Mode = Edge` state-signals into one-sided trade streams.
- Fix applied:
  - `00_MASTER_TEMPLATE/MASTER_TEMPLATE_CORE.pine`
  - `mtc_backtest/src/engine/mtc_runner.py`
  - `mtc_backtest/tests/test_opp_signal_same_bar_flip.py`
- Validation:
  - `python -m pytest tests/test_same_bar_reentry_and_capital_guard.py tests/test_opp_signal_same_bar_flip.py -q`
  - `3 passed`
- Status:
  - open blocker set unchanged (`402`, `416`)
  - full parity regression still pending

## Session Note - 2026-03-08 Supertrend Research / Replay Fix
- `optimizer_v0` walk-forward replay path was corrected to preserve alias-backed config fields:
  - `mtc_backtest/src/optimizer_v0/replay_candidates.py`
- Regression lock:
  - `mtc_backtest/tests/test_optimizer_replay_candidates.py`
- Parity blocker state is unchanged:
  - still `402`, `416`
- But research outputs tied to walk-forward replay changed after the fix.
- Corrected current-best Supertrend candidate is now:
  - `ATR 48`
  - `Factor 4.8`
  - `Entry Mode = Edge`
  - `Regime Lock = Off`
  - `Use HA = Off`
  - `Use Wicks = Off`
- Materialized candidate case:
  - `mtc_backtest/configs/cases/supertrend_current_best_candidate_20260308.json`
- 16-combo toggle sweep completed after the replay fix:
  - `mtc_backtest/optimize_results/supertrend_candidate_toggle_sweep_20260308_195806.xlsx`
  - no improvement over the corrected base candidate
  - `HA` and `Wicks` degrade OOS
  - `Regime Lock` and `Edge/Signal` are neutral for this candidate

## Session Note - 2026-03-09 Supertrend SL + Risk Follow-up
- Parity blocker state is still unchanged:
  - `402`
  - `416`
- Research follow-up on top of the corrected base candidate:
  - fixed `scripts/walk_forward_validate.py` threshold forwarding bug
  - added regression coverage for the walk-forward wrapper contract
- SL-mode conclusion:
  - `%` stop-loss is the only viable family on the corrected Supertrend base under tested windows
- Joint `% SL + risk` outputs:
  - net-focused candidate:
    - `% 0.3`
    - `risk_long=0.05`
    - `risk_short=0.2`
    - `max_leverage=3.0`
    - OOS `+484.21`, DD `6.67%`
  - risk-aware promoted candidate:
    - `% 0.3`
    - `risk_long=0.01`
    - `risk_short=0.15`
    - `max_leverage=2.0`
    - OOS `+363.95`, DD `4.47%`
- Materialized case files:
  - `mtc_backtest/configs/cases/supertrend_sl_risk_current_best_candidate_20260309.json`
  - `mtc_backtest/configs/cases/supertrend_sl_risk_net_candidate_20260309.json`
- Comparison report:
  - `mtc_backtest/results/walkforward/supertrend_sl_risk_comparison_20260309.xlsx`
  - Important qualifier:
    - full-period `2025-01-01 .. 2026-01-01` remains negative even for the risk-aware candidate
    - this is research progress, not a production promotion

## Session Note - 2026-03-09 Supertrend Exit Stack Continuation
- `train_top_score` replay was added because Pareto-only export was missing stronger OOS candidates.
- Revised no-TP winner:
  - `% SL 0.3`, `risk_long=0.01`, `risk_short=0.4`, `max_leverage=2.0`
  - OOS `+963.77`, DD `11.29%`
- TP continuation:
  - best TP `% 2.5`
  - OOS `+1371.52`, DD `9.83%`
  - case: `mtc_backtest/configs/cases/supertrend_sl_risk_tp_current_best_candidate_20260309.json`
- Break-even continuation:
  - best BE `rr=2.0`, `buffer_r=0.2`
  - OOS `+1603.74`, DD `7.91%`
  - case: `mtc_backtest/configs/cases/supertrend_sl_risk_tp_be_current_best_candidate_20260309.json`
- Trailing continuation:
  - best trailing OOS `+436.50`, DD `7.13%`
  - rejected because net collapses versus TP and TP+BE
- Full-period nuance:
  - TP+BE OOS-best case is still negative over `2025-01-01 .. 2026-01-01` (`-178.23`, DD `20.2%`)
  - least-bad full-period branch remains `supertrend_sl_risk_balanced_candidate_20260309.json` (`-139.19`, DD `12.6%`)
- Canonical comparison:
  - `mtc_backtest/results/walkforward/supertrend_exit_stack_comparison_20260309.xlsx`

## Session Note - 402/416 Truncation Candidate
- Evidence report:
  - `mtc_backtest/parity_suite_350/triage/CASE_402_416_TV_TRADELIST_TRUNCATION_20260304.md`
- Observed:
  - clip-overlap compare passes for both 402 and 416
  - no-clip compare fails due TV list ending ~125+ days before case end
- Interpretation: TV early trade-end candidate; overlap lifecycle currently aligned. Needs policy decision (raw-count vs overlap).


## Session Note - Dual Reporting Pipeline
- Implemented dual parity outputs (`raw strict` + `clip-overlap strict`) in:
  - `scripts/compare_tv_web_trades.py`
  - `parity_suite_350/scripts/check_and_run_new_cases.py`
  - `parity_suite_350/scripts/run_and_compare_batch.py`
- Auto tag added in compare notes/workbook flow:
  - `TV_EARLY_TRADE_END_CANDIDATE gap_days=...`
- Truncation candidate scan utility:
  - `parity_suite_350/scripts/detect_tv_trade_list_truncation.py`
  - output: `parity_suite_350/compare_runs/tv_trade_list_truncation_scan.csv`

## Session Note - Mismatch Split Report
- Generated from workbook compare_status + dual-status notes:
  - `mtc_backtest/parity_suite_350/compare_runs/mismatch_split_latest.csv`
  - `mtc_backtest/parity_suite_350/compare_runs/mismatch_split_latest.md`
- Current split:
  - total mismatch: 2
  - EARLY_TRADE_END_CANDIDATE: 2 (`402`, `416`)
  - TRUE_LOGIC_MISMATCH: 0

## Session Note - Policy View Snapshot
- `mtc_backtest/parity_suite_350/compare_runs/parity_policy_view_latest.md`
- Current numbers:
  - raw strict: 437/439 (`99.54%`)
  - clip-overlap effective: 439/439 (`100.00%`)

## Session Note - One-shot Diagnostics Command
- Added orchestrator:
  - `mtc_backtest/parity_suite_350/scripts/run_post_compare_diagnostics.py`
- Runs in order:
  1) `detect_tv_trade_list_truncation.py`
  2) `split_mismatch_by_dual_status.py`
  3) `build_policy_parity_view.py`

## Session Update - 2026-03-05
- Applied pending steps 2/3/4 from previous plan.
- Added shared dual-status policy module: `src/parity/dual_status.py`.
- Wired compare workflows to auto-run diagnostics:
  - `parity_suite_350/scripts/check_and_run_new_cases.py`
  - `parity_suite_350/scripts/run_and_compare_batch.py`
- Added structural diagnostics columns to workbook generation + updaters and ensured both active tracker files contain them.
- Added regression tests for expected policy semantics:
  - `tests/test_dual_status_regression.py` (PASS)
- Current high-level parity picture unchanged:
  - Executable raw strict: `437/439`
  - Clip-overlap effective: `439/439`
  - Open blockers: `402`, `416`
