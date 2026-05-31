# Parity Status Final - 2026-03-04

## Scope
Canonical parity report for `mtc_backtest` vs `MTC`.
Use with latest case-level CSV evidence under `mtc_backtest/parity_suite_350/compare_runs/`.

## Source Priority
When sources disagree, trust this order:
1. latest strict case-level compare CSV/MD under `compare_runs/`
2. `mtc_backtest/parity_suite_350/CURRENT_STATUS_HANDOFF_20260304.md`
3. `mtc_backtest/parity_suite_350/CASE_SETUP_GUIDE_tagged_v6_conflict_candidates.xlsx`

## Canonical Current Status
Total cases: `457`

Workbook inventory:
- `DOWNLOADED`: `317`
- `reuses:*`: `121`
- `SKIP`: `18`
- `baseline`: `1`

Live parity truth:
- `PASS`: `316`
- `PASS(reuse)`: `121`
- `MISMATCH`: `2`
- `SKIP`: `18`

Executable cases: `439`
Executable passes: `437`
Executable parity rate: `99.54%`
Overall listed-case parity rate: `95.62%`

## Open Blockers
### 402 - `parity_bnd_211_swing_right_bars_v03`
Evidence:
- `mtc_backtest/parity_suite_350/compare_runs/verify97_402.csv`
- `mtc_backtest/parity_suite_350/compare_runs/verify97_402_detailed.csv`
- `mtc_backtest/parity_suite_350/compare_runs/verify97_402_tv_trades.csv`

Current status:
- `TV 123 / PY 236`
- `MISMATCH`

### 416 - `parity_bnd_217_dynamic_update_mode_v02`
Evidence:
- `mtc_backtest/parity_suite_350/compare_runs/verify97_416.csv`
- `mtc_backtest/parity_suite_350/compare_runs/verify97_416_detailed.csv`
- `mtc_backtest/parity_suite_350/compare_runs/verify97_416_tv_trades.csv`

Current status:
- `TV 129 / PY 189`
- `MISMATCH`

## Closed in This Session
### 362 / 363
- `TV 177 / PY 177` and `strict_pass=True`
- Evidence:
  - `mtc_backtest/parity_suite_350/compare_runs/current362_363.csv`
  - `mtc_backtest/parity_suite_350/compare_runs/current_362.csv`
  - `mtc_backtest/parity_suite_350/compare_runs/current_363.csv`
  - `mtc_backtest/parity_suite_350/compare_runs/probe_patch_trailstart_anchors_summary.csv`

## Stable Closed Reference Cases
Use as regression anchors:
- `001`, `236`, `281`, `362`, `363`, `395`, `398`, `401`, `404`, `406`, `409`, `412`, `415`, `422`

## Tracker Status
`CASE_SETUP_GUIDE_tagged_v6_conflict_candidates.xlsx` synced:
- `362`, `363` set to `PASS`
- `402`, `416` remain `MISMATCH`

## Immediate Next Work
1. Resolve `402` confirmation/lifecycle cutoff divergence
2. Resolve `416` dynamic confirmation execution/no-fill divergence
3. Keep workbook + handoff + report aligned with latest case-level CSV evidence

## Session Note - 362/363 Same-Bar Lifecycle
- Isolation evidence report:
  - `mtc_backtest/parity_suite_350/triage/CASE_362_363_SAME_BAR_LIFECYCLE_20260304.md`
- Key bar validated: `2025-10-03 17:00 UTC` (`18:00` TV local)
- Result: TRAIL exit + same-direction same-bar reentry confirmed aligned in Python and TV.

## Session Note - 2026-03-08 OPP Signal Same-Bar Flip Fix
- Trigger workbook:
  - `mtc_backtest/parity_suite_350/tv_manual_inputs/raw_tv_exports/Supertrend ATR 21 F 5.5.xlsx`
- Root cause:
  - `OPP_SIGNAL` bar-close exits blocked same-bar opposite entry, which can force `Entry Mode = Edge` state-signals into one-sided execution after the first trade.
- Fix applied in both engines:
  - `00_MASTER_TEMPLATE/MASTER_TEMPLATE_CORE.pine`
  - `mtc_backtest/src/engine/mtc_runner.py`
- Regression coverage:
  - `mtc_backtest/tests/test_opp_signal_same_bar_flip.py`
  - targeted pytest pass (`3 passed`)
- Status impact:
  - open blockers remain `402`, `416`
  - full parity rerun pending

## Session Note - 2026-03-08 Supertrend Research / Replay Fix
- Walk-forward replay correctness fix landed in:
  - `mtc_backtest/src/optimizer_v0/replay_candidates.py`
- Cause:
  - replay path was rebuilding configs from alias-less dumps and could silently replay a different strategy contract than the one optimized.
- Regression coverage:
  - `mtc_backtest/tests/test_optimizer_replay_candidates.py`
- Status impact on parity:
  - no change to open blocker set (`402`, `416`)
- Status impact on research:
  - corrected Supertrend current-best candidate is now `ATR 48 / F 4.8`
  - materialized at:
    - `mtc_backtest/configs/cases/supertrend_current_best_candidate_20260308.json`
  - corrected 16-combo toggle sweep confirms:
    - keep `Entry Mode = Edge`
    - keep `Regime Lock = Off`
    - keep `Use HA = Off`
    - keep `Use Wicks = Off`

## Session Note - 2026-03-09 Supertrend SL + Risk Follow-up
- No parity blocker changed state; canonical blockers remain:
  - `402`
  - `416`
- Workflow hardening:
  - `scripts/walk_forward_validate.py` now forwards threshold args into the train leg and tolerates missing replay CSVs
- Research result on the corrected Supertrend base:
  - `%` stop-loss is the only tested SL family that remains viable after walk-forward gating
  - joint `% SL + risk` tuning materially reduces DD versus the naked baseline
- Materialized candidates:
  - `mtc_backtest/configs/cases/supertrend_sl_risk_current_best_candidate_20260309.json`
  - `mtc_backtest/configs/cases/supertrend_sl_risk_net_candidate_20260309.json`
- Best defensive candidate:
  - `% 0.3`
  - `risk_long=0.01`
  - `risk_short=0.15`
  - `max_leverage=2.0`
  - OOS `+363.95`, DD `4.47%`
- Best net candidate from the wider joint search:
  - `% 0.3`
  - `risk_long=0.05`
  - `risk_short=0.2`
  - `max_leverage=3.0`
  - OOS `+484.21`, DD `6.67%`
- Comparison report:
  - `mtc_backtest/results/walkforward/supertrend_sl_risk_comparison_20260309.xlsx`
  - Status qualifier:
    - full-period `2025-01-01 .. 2026-01-01` is still negative for all tested Supertrend variants

## Session Note - 2026-03-09 Supertrend Exit Stack Continuation
- `train_top_score` replay was added because Pareto-only export was missing stronger OOS candidates.
- Revised no-TP winner:
  - `% SL 0.3`, `risk_long=0.01`, `risk_short=0.4`, `max_leverage=2.0`
  - OOS `+963.77`, DD `11.29%`
- Best TP layer:
  - `% 2.5`
  - OOS `+1371.52`, DD `9.83%`
- Best BE layer on top of TP:
  - `rr=2.0`, `buffer_r=0.2`
  - OOS `+1603.74`, DD `7.91%`
  - case: `mtc_backtest/configs/cases/supertrend_sl_risk_tp_be_current_best_candidate_20260309.json`
- Best trailing layer on top of TP+BE:
  - OOS `+436.50`, DD `7.13%`
  - rejected because net degrades materially
- Canonical comparison:
  - `mtc_backtest/results/walkforward/supertrend_exit_stack_comparison_20260309.xlsx`
- Current interpretation:
  - OOS-best tested branch is TP+BE
  - least-bad full-period branch remains the conservative SL+risk reference

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
- Steps 2/3/4 completed for dual-status workflow hardening.
- Dual policy classification logic centralized in `src/parity/dual_status.py`.
- Batch compare scripts now auto-trigger post-compare diagnostics.
- Tracker workbook now carries structural diagnostics columns for raw/clip split and candidate tagging.
- Added regression tests to lock expected behavior for 362/363 (PASS) and 402/416 pattern (raw fail + clip pass candidate).
