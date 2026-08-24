# Run/Result Inventory — WP-P0-07

## Result

No strict survivor was found. All result rows in the **67 directly parseable tracked final result JSONs** explicitly record `robust_final=false`. This does **not** prove the all-time claim: primary bytes for part of the recorded, git-ignored result estate are absent, older May research packages predate the comparable strict field, the canonical backtest registry is empty, and one registered run has an identity conflict. See `F22_VERDICT.md`.

## Method and field rules

- A directly parseable run below is one completed JSON artefact with a top-level `results` array. Deterministic loop iterations remain separate rows because the contract asks for one row per recorded run; known duplicates are labeled later rather than silently collapsed.
- Strict survivor means `results[*].robust_final=true`, the current MEGA conjunction of PASS/STRONG_PASS, BH-FDR survival, and DSR at least 0.95 (`03_QUANTLENS/tools/mega_walk_forward.py:1695-1725`).
- Trial count is the exact sum of recorded `results[*].trial_count`. Parentheses show `rows with trial_count / all result rows`; rows without the field are not guessed.
- `UNKNOWN — <what was searched>` is used whenever the record cannot supply a field.
- Dates are `generated_utc` dates where present.

Evidence codes used in the direct table:

- **E1:** the cited JSON path, top-level `generated_utc`, and every `results[*].trial_count` / `results[*].robust_final` field were parsed read-only.
- **E2:** older MEGA JSON schema; engine is recorded by the `MEGA_*` artefact identity, but no top-level or row-level `engine_version` value exists.
- **E3:** rows record `engine_version=faz3b-exit-mode-v1`.

## A. Directly parseable completed result files — 67/67

| # | Run/result path | Engine + version (as recorded) | Date | Configuration/trial count | Strict survivors | Evidence |
|---:|---|---|---|---:|---:|---|
| 1 | `03_QUANTLENS/tools/overnight_runs/MEGA_results_iter_1_20260531_005604.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-05-30 | 144,725 (3,146/3,315 rows) | 0 | E1, E2 |
| 2 | `03_QUANTLENS/tools/overnight_runs/MEGA_results_iter_2_20260531_011502.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-05-30 | 144,725 (3,146/3,315 rows) | 0 | E1, E2 |
| 3 | `03_QUANTLENS/tools/overnight_runs/MEGA_results_iter_3_20260531_013318.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-05-30 | 144,725 (3,146/3,315 rows) | 0 | E1, E2 |
| 4 | `03_QUANTLENS/tools/overnight_runs/MEGA_results_iter_4_20260531_015136.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-05-30 | 144,725 (3,146/3,315 rows) | 0 | E1, E2 |
| 5 | `03_QUANTLENS/tools/overnight_runs/MEGA_results_iter_5_20260531_020944.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-05-30 | 144,725 (3,146/3,315 rows) | 0 | E1, E2 |
| 6 | `03_QUANTLENS/tools/overnight_runs/MEGA_results_iter_6_20260531_022816.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-05-30 | 144,725 (3,146/3,315 rows) | 0 | E1, E2 |
| 7 | `03_QUANTLENS/tools/overnight_runs/MEGA_results_iter_7_20260531_024617.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-05-31 | 144,725 (3,146/3,315 rows) | 0 | E1, E2 |
| 8 | `03_QUANTLENS/tools/overnight_runs/MEGA_results_iter_8_20260531_030428.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-05-31 | 144,725 (3,146/3,315 rows) | 0 | E1, E2 |
| 9 | `03_QUANTLENS/tools/overnight_runs/MEGA_results_iter_9_20260531_032301.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-05-31 | 144,725 (3,146/3,315 rows) | 0 | E1, E2 |
| 10 | `03_QUANTLENS/tools/overnight_runs/MEGA_results_iter_10_20260531_034109.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-05-31 | 144,725 (3,146/3,315 rows) | 0 | E1, E2 |
| 11 | `03_QUANTLENS/tools/overnight_runs/MEGA_results_iter_11_20260531_035917.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-05-31 | 144,725 (3,146/3,315 rows) | 0 | E1, E2 |
| 12 | `03_QUANTLENS/tools/overnight_runs/MEGA_results_iter_12_20260531_041738.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-05-31 | 144,725 (3,146/3,315 rows) | 0 | E1, E2 |
| 13 | `03_QUANTLENS/tools/overnight_runs/MEGA_results_iter_13_20260531_043556.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-05-31 | 144,725 (3,146/3,315 rows) | 0 | E1, E2 |
| 14 | `03_QUANTLENS/tools/overnight_runs/MEGA_results_iter_14_20260531_045426.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-05-31 | 144,725 (3,146/3,315 rows) | 0 | E1, E2 |
| 15 | `03_QUANTLENS/tools/overnight_runs/MEGA_results_iter_15_20260531_051238.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-05-31 | 144,725 (3,146/3,315 rows) | 0 | E1, E2 |
| 16 | `03_QUANTLENS/tools/overnight_runs/MEGA_results_iter_16_20260531_053109.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-05-31 | 144,725 (3,146/3,315 rows) | 0 | E1, E2 |
| 17 | `03_QUANTLENS/tools/overnight_runs/MEGA_results_iter_17_20260531_054930.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-05-31 | 144,725 (3,146/3,315 rows) | 0 | E1, E2 |
| 18 | `03_QUANTLENS/tools/overnight_runs/MEGA_results_iter_18_20260531_060748.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-05-31 | 144,725 (3,146/3,315 rows) | 0 | E1, E2 |
| 19 | `03_QUANTLENS/tools/overnight_runs/MEGA_results_iter_19_20260531_062631.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-05-31 | 144,725 (3,146/3,315 rows) | 0 | E1, E2 |
| 20 | `03_QUANTLENS/tools/overnight_runs/MEGA_results_iter_22_20260531_070703.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-05-31 | 144,725 (3,146/3,315 rows) | 0 | E1, E2 |
| 21 | `03_QUANTLENS/tools/overnight_runs/MEGA_results_iter_23_20260531_072639.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-05-31 | 144,725 (3,146/3,315 rows) | 0 | E1, E2 |
| 22 | `03_QUANTLENS/tools/night_runs/MEGA_results_iter_1_20260602_201203.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-02 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 23 | `03_QUANTLENS/tools/night_runs/MEGA_results_iter_2_20260602_204840.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-02 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 24 | `03_QUANTLENS/tools/night_runs/MEGA_results_iter_3_20260602_212338.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-02 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 25 | `03_QUANTLENS/tools/night_runs/MEGA_results_iter_4_20260602_215842.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-02 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 26 | `03_QUANTLENS/tools/night_runs/MEGA_results_iter_5_20260602_223357.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-02 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 27 | `03_QUANTLENS/tools/night_runs/MEGA_results_iter_6_20260602_230711.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-02 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 28 | `03_QUANTLENS/tools/night_runs/MEGA_results_iter_7_20260602_233811.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-02 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 29 | `03_QUANTLENS/tools/night_runs/MEGA_results_iter_8_20260603_000856.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-02 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 30 | `03_QUANTLENS/tools/night_runs/MEGA_results_iter_9_20260603_003943.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-02 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 31 | `03_QUANTLENS/tools/night_runs/MEGA_results_iter_10_20260603_011018.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-02 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 32 | `03_QUANTLENS/tools/night_runs/MEGA_results_iter_11_20260603_014102.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-02 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 33 | `03_QUANTLENS/tools/night_runs/MEGA_results_iter_12_20260603_021135.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-02 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 34 | `03_QUANTLENS/tools/night_runs/MEGA_results_iter_13_20260603_024226.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-03 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 35 | `03_QUANTLENS/tools/night_runs/MEGA_results_iter_14_20260603_031317.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-03 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 36 | `03_QUANTLENS/tools/night_runs/MEGA_results_iter_15_20260603_034354.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-03 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 37 | `03_QUANTLENS/tools/night_runs/MEGA_results_iter_16_20260603_041437.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-03 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 38 | `03_QUANTLENS/tools/night_runs/MEGA_results_iter_17_20260603_044533.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-03 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 39 | `03_QUANTLENS/tools/night_runs/MEGA_results_iter_18_20260603_051619.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-03 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 40 | `03_QUANTLENS/tools/night_runs/MEGA_results_iter_19_20260603_054701.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-03 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 41 | `03_QUANTLENS/tools/night_runs/MEGA_results_iter_20_20260603_061749.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-03 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 42 | `03_QUANTLENS/tools/night_runs/MEGA_results_iter_21_20260603_064825.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-03 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 43 | `03_QUANTLENS/tools/night_runs/night_2026-06-03/MEGA_results_iter_1_20260603_193753.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-03 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 44 | `03_QUANTLENS/tools/night_runs/night_2026-06-03/MEGA_results_iter_2_20260603_201410.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-03 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 45 | `03_QUANTLENS/tools/night_runs/night_2026-06-03/MEGA_results_iter_3_20260603_204906.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-03 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 46 | `03_QUANTLENS/tools/night_runs/night_2026-06-03/MEGA_results_iter_4_20260603_212343.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-03 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 47 | `03_QUANTLENS/tools/night_runs/night_2026-06-03/MEGA_results_iter_5_20260603_215810.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-03 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 48 | `03_QUANTLENS/tools/night_runs/night_2026-06-03/MEGA_results_iter_6_20260603_223244.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-03 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 49 | `03_QUANTLENS/tools/night_runs/night_2026-06-03/MEGA_results_iter_7_20260603_230730.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-03 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 50 | `03_QUANTLENS/tools/night_runs/night_2026-06-03/MEGA_results_iter_8_20260603_234157.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-03 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 51 | `03_QUANTLENS/tools/night_runs/night_2026-06-03/MEGA_results_iter_9_20260604_001619.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-03 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 52 | `03_QUANTLENS/tools/night_runs/night_2026-06-03/MEGA_results_iter_10_20260604_005032.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-03 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 53 | `03_QUANTLENS/tools/night_runs/night_2026-06-03/MEGA_results_iter_11_20260604_012445.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-03 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 54 | `03_QUANTLENS/tools/night_runs/night_2026-06-03/MEGA_results_iter_12_20260604_015904.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-03 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 55 | `03_QUANTLENS/tools/night_runs/night_2026-06-03/MEGA_results_iter_13_20260604_023327.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-04 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 56 | `03_QUANTLENS/tools/night_runs/night_2026-06-03/MEGA_results_iter_14_20260604_030736.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-04 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 57 | `03_QUANTLENS/tools/night_runs/night_2026-06-03/MEGA_results_iter_15_20260604_034151.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-04 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 58 | `03_QUANTLENS/tools/night_runs/night_2026-06-03/MEGA_results_iter_16_20260604_041612.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-04 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 59 | `03_QUANTLENS/tools/night_runs/night_2026-06-03/MEGA_results_iter_17_20260604_045034.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-04 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 60 | `03_QUANTLENS/tools/night_runs/night_2026-06-03/MEGA_results_iter_18_20260604_052448.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-04 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 61 | `03_QUANTLENS/tools/night_runs/night_2026-06-03/MEGA_results_iter_19_20260604_055904.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-04 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 62 | `03_QUANTLENS/tools/night_runs/night_2026-06-03/MEGA_results_iter_20_20260604_063318.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-04 | 163,679 (3,470/3,655 rows) | 0 | E1, E2 |
| 63 | `03_QUANTLENS/tools/night_runs/confirm_2026-06-04/MEGA_results_iter_1_20260604_233125.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-04 | 3,672 (306/306 rows) | 0 | E1, E2 |
| 64 | `03_QUANTLENS/tools/smoke_runs/smoke_20260603_overnight/MEGA_walk_forward_results.json` | MEGA walk-forward; `UNKNOWN — engine_version absent` | 2026-06-03 | 64 (1/1 row) | 0 | E1, E2 |
| 65 | `03_QUANTLENS/research/faz3b_stage1_20260705/pass1_10m/MEGA_walk_forward_results.json` | MEGA walk-forward; `faz3b-exit-mode-v1` | 2026-07-05 | 7,371 (399/420 rows) | 0 | E1, E3 |
| 66 | `03_QUANTLENS/research/faz3b_stage1_20260705/pass2_1h/MEGA_walk_forward_results.json` | MEGA walk-forward; `faz3b-exit-mode-v1` | 2026-07-05 | 9,828 (532/560 rows) | 0 | E1, E3 |
| 67 | `03_QUANTLENS/research/donchian_crypto_ladder_2026-07-13/MEGA_walk_forward_results.json` | MEGA walk-forward; `faz3b-exit-mode-v1` | 2026-07-12 | 240 (4/4 rows) | 0 | E1, E3 |

The `overnight_runs` sequence contains no tracked iteration 20 or 21; the inventory lists the 21 files actually present and does not manufacture missing runs. The smoke partial JSON is an in-progress copy of the same one-row final smoke record and is excluded as a completed run.

## B. Present derived result records — not independent runs

| Record/path | Engine + version (as recorded) | Date | Configuration/trial count | Strict survivors | Evidence / treatment |
|---|---|---|---:|---:|---|
| `03_QUANTLENS/tools/sprint_runs/cpcv_input_top_alpha.json` | Derived MEGA row selection; `UNKNOWN — engine_version absent` | `UNKNOWN — no generated_utc; adjacent report date not assumed` | 572 recorded trials across 13/13 rows | 0 | Top-level note says `Filtered: top alpha cells for CPCV`; all 13 rows explicitly have `robust_final=false`. Do not count as a new sweep. |
| `03_QUANTLENS/05_BACKTEST_RESULTS/profile_result_GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h_SOURCE_NAKED_2026-06-16/backtest_profile_result.json` | `UNKNOWN — searched profile and absent provenance paths` | 2026-06-20 (artefact generation date) | `UNKNOWN — one represented result, original run count absent` | `UNKNOWN — robust_final absent` | Derived profile points to absent `night_1m_2026-06-07/iter_05` artefacts. Its `gate_summary.all_pass=false` is not substituted for the strict field. |

## C. Recorded canonical/legacy run families whose primary result bytes are absent here

These rows come from run registries, tracked handoffs, and the prior primary-byte inspection recorded in `11_TRIAGE/RESEARCH_TRUTH_LEDGER_INVENTORY_2026-08-17.md:1-95`. Where the current worktree cannot re-open the primary JSON/report, that limitation is explicit.

| Run/family/path as recorded | Engine + version (as recorded) | Date | Configuration/trial count | Strict survivors | Evidence citation / status |
|---|---|---|---|---:|---|
| 2026-05-30 Appendix-B sweep; primary run path not recorded | MEGA walk-forward; `UNKNOWN — snapshot has no version` | 2026-05-30 | ~93,000 configurations | 0 | `03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md:287-294`. This is F-22's original bounded evidence. |
| root `05_BACKTEST_RESULTS/MEGA_walk_forward_results.json` | MEGA walk-forward; `UNKNOWN — older schema does not record engine version` | `UNKNOWN — searched truth-ledger cluster and tracked handoffs` | 3,655 result rows; `UNKNOWN — exact trial count not recoverable from searched truth-ledger and handoffs` | `UNKNOWN — primary JSON absent` | `11_TRIAGE/RESEARCH_TRUTH_LEDGER_INVENTORY_2026-08-17.md:77`. |
| `heavy_tier_2026-06-05` | MEGA walk-forward; `UNKNOWN — older schema does not record engine version` | 2026-06-05 | 3,655 cells; `UNKNOWN — exact trial count not recoverable from searched truth-ledger and handoffs` | 0 | `_AI_MEMORY/NEXT_STEPS.md:2074`; truth-ledger `:77`. Reported no cell passed even the weaker DSR 0.50 conjunction. |
| `enriched_metrics_2026-06-05` | MEGA walk-forward; `UNKNOWN — older schema does not record engine version` | 2026-06-05 | 1,700 result rows; `UNKNOWN — exact trial count not recoverable from searched truth-ledger and handoffs` | `UNKNOWN — primary JSON absent` | Truth-ledger `:78`; `_AI_MEMORY/NEXT_STEPS.md:2108`. |
| `bh_benchmark_2026-06-05_7175ff6` | MEGA walk-forward; `UNKNOWN — older schema does not record engine version` | 2026-06-05 | 1,700 result rows; `UNKNOWN — exact trial count not recoverable from searched truth-ledger and handoffs` | `UNKNOWN — report states 0 promotable, not robust_final` | Truth-ledger `:78`; `_AI_MEMORY/NEXT_STEPS.md:2118`. |
| `worst_window_2026-06-05_283d198` | MEGA walk-forward; `UNKNOWN — older schema does not record engine version` | 2026-06-05 | 1,700 result rows; `UNKNOWN — exact trial count not recoverable from searched truth-ledger and handoffs` | `UNKNOWN — report states 0 promotable, not robust_final` | Truth-ledger `:78`; `_AI_MEMORY/NEXT_STEPS.md:2124`. |
| `annualized_risk_2026-06-05_15e8d47` | MEGA walk-forward; `UNKNOWN — older schema does not record engine version` | 2026-06-05 | 1,700 result rows; `UNKNOWN — exact trial count not recoverable from searched truth-ledger and handoffs` | `UNKNOWN — report states 0 promotable, not robust_final` | Truth-ledger `:78`; `_AI_MEMORY/NEXT_STEPS.md:2131`. |
| `slippage_2026-06-05_5c68419` | MEGA walk-forward; `UNKNOWN — older schema does not record engine version` | 2026-06-05 | 1,700 result rows; `UNKNOWN — exact trial count not recoverable from searched truth-ledger and handoffs` | 0 | Truth-ledger `:78`; archived session record reports `0 robust final`. |
| `final_gate2_2026-06-05_39b51db` | MEGA walk-forward; `UNKNOWN — older schema does not record engine version` | 2026-06-05 | 1,700 result rows; `UNKNOWN — exact trial count not recoverable from searched truth-ledger and handoffs` | `UNKNOWN — report states 0 promotable, not robust_final` | Truth-ledger `:78`; `_AI_MEMORY/NEXT_STEPS.md:2146`. |
| `FOCUSED_VALIDATION_2026-05-31` | MEGA walk-forward; `UNKNOWN — older schema does not record engine version` | 2026-05-31 | 680 result rows; `UNKNOWN — exact trial count not recoverable from searched truth-ledger and handoffs` | `UNKNOWN — primary JSON absent` | Truth-ledger `:79`. |
| `new_strategies_2026-06-06` | MEGA walk-forward; `UNKNOWN — older schema does not record engine version` | 2026-06-06 | 68 result rows; `UNKNOWN — exact trial count not recoverable from searched truth-ledger and handoffs` | `UNKNOWN — primary JSON absent` | Truth-ledger `:80`. |
| `lbr_coil_2026-06-06` | MEGA walk-forward; `UNKNOWN — older schema does not record engine version` | 2026-06-06 | 68 result rows; `UNKNOWN — exact trial count not recoverable from searched truth-ledger and handoffs` | `UNKNOWN — primary JSON absent` | Truth-ledger `:80`. |
| `fam_templates_2026-06-06` | MEGA walk-forward; `UNKNOWN — older schema does not record engine version` | 2026-06-06 | 204 result rows; `UNKNOWN — exact trial count not recoverable from searched truth-ledger and handoffs` | 0 | Truth-ledger `:80`; `_AI_MEMORY/archive/SESSION_LOG_pre-2026-07-06.md:111` records best DSR 0.492, below strict 0.95. |
| `batch023_034_2026-06-07` | MEGA walk-forward; `UNKNOWN — older schema does not record engine version` | 2026-06-07 | 4,590 result rows; `UNKNOWN — exact trial count not recoverable from searched truth-ledger and handoffs` | 0 | Truth-ledger `:59-62`: partition of the zero-survivor full sweep. |
| `remaining_2026-06-07-recovery` | MEGA walk-forward; `UNKNOWN — older schema does not record engine version` | 2026-06-07 | 425 result rows; `UNKNOWN — exact trial count not recoverable from searched truth-ledger and handoffs` | 0 | Truth-ledger `:59-62`: complementary partition of the zero-survivor full sweep. |
| `full_sweep_2026-06-07` | MEGA walk-forward; `UNKNOWN — older schema does not record engine version` | 2026-06-07 | 5,015 result rows; `UNKNOWN — exact trial count not recoverable from searched truth-ledger and handoffs` | 0 | Truth-ledger `:43-62` records 5,015 rows and zero robust-final rows. |
| `night_1m_2026-06-07` (iter 01-05) | MEGA walk-forward; `UNKNOWN — older schema` | 2026-06-07 | ~1.08M evaluations recorded for parent; five 5,015-row deterministic iterations | 0 | `_AI_MEMORY/CODEX_PICKUP_2026-06-08.md:27`; truth-ledger `:43-54` proves semantic duplicate and zero. |
| `night_3M_2026-06-08` (iter 01-09) | MEGA walk-forward; `UNKNOWN — older schema` | 2026-06-08 | `UNKNOWN — name/launch target is not an exact completed trial count`; nine 5,015-row deterministic iterations | 0 | Truth-ledger `:43-54` proves semantic duplicate and zero. |
| `smoke_night_1m_2026-06-07` | MEGA walk-forward; `UNKNOWN — older schema does not record engine version` | 2026-06-07 | 1 result row; `UNKNOWN — exact trial count not recoverable from searched truth-ledger and handoffs` | `UNKNOWN — primary JSON absent` | Truth-ledger `:82`; operational smoke, not independent research evidence. |
| `overnight_multiasset_2026-06-29` | MEGA walk-forward; `UNKNOWN — older schema` | 2026-06-29 | ~399,840 configurations / 7,140 result rows | 0 | `05_REGISTRY/RESEARCH_RUN_REGISTRY.json:6-18`; truth-ledger `:22-23`; tracked session record supplies config total. Registry path absent here. |
| `turtle_heavy_2026-07-01` | MEGA walk-forward; `UNKNOWN — older schema` | 2026-07-01 | 357 cells × grid 24 = 8,568 configurations | 0 | Registry `:32-40`; truth-ledger `:28-29`. Registry path absent here. |
| `overnight_full_2026-07-02/stageA_v2_multiasset` | MEGA walk-forward; `UNKNOWN — older schema does not record engine version` | 2026-07-02 | 8,211 result rows; `UNKNOWN — exact trial count not recoverable from searched truth-ledger and registry` | 0 for pointed artefact | Registry `:42-50`; truth-ledger `:30-34`. **Identity conflict:** path holds 23 strategies, not the registered six variants. |
| `overnight_resilient_2026-07-02/variants` | MEGA walk-forward; `UNKNOWN — older schema does not record engine version` | 2026-07-02 | 2,856 result rows; `UNKNOWN — exact trial count not recoverable from searched truth-ledger and handoffs` | 0 | Truth-ledger `:35`; unregistered and absent here. |
| `overnight_archetypes_2026-07-03` | MEGA walk-forward; `UNKNOWN — older schema does not record engine version` | 2026-07-03 | 4,284 result rows; `UNKNOWN — exact trial count not recoverable from searched truth-ledger and registry` | 0 | Registry `:52-60`; truth-ledger `:36`. Registry path absent here. |

FAZ3B and Donchian are not duplicated in this table because their primary result files are present in section A. The `confirm_2026-06-04` tracked result is likewise section A row 63.

## D. Tracked pre-strict research result packages

These are recorded backtest/result packages under `03_QUANTLENS/research/`, but their custom reports predate or do not expose the comparable MEGA `robust_final` gate. Strategy, trade, asset, or parameter-grid row counts are not silently relabeled as the total configuration count.

| Run/result package | Engine + version (as recorded) | Date | Configuration/trial count | Strict survivors | Evidence citation |
|---|---|---|---|---|---|
| `crabel_range_expansion` | `run_crabel_backtest.py` / `run_stage2_robustness.py`; `UNKNOWN — version not recorded in searched scripts and reports` | `UNKNOWN — searched README and robustness report` | `UNKNOWN — parameter sweep exists but no run-total field` | `UNKNOWN — no robust_final field` | `research/crabel_range_expansion/QL_CRABEL_RANGE_EXPANSION_STAGE2_ROBUSTNESS_REPORT.md`; `QL_CRABEL_STAGE2_PARAMETER_SWEEP.csv`. |
| `overnight_intake_batch_2026_05_03` | `run_overnight_batch.py`; `UNKNOWN — version not recorded in searched script and reports` | 2026-05-03 | `UNKNOWN — searched master report, strategy_summary.csv, and per-strategy results` | `UNKNOWN — pre-strict classifications` | `research/overnight_intake_batch_2026_05_03/MASTER_OVERNIGHT_QUANTLENS_REPORT.md`; `RUN_LOG.md`. |
| `overnight_intake_batch_2026_05_03_CLEAN` | `run_overnight_batch.py`; `UNKNOWN — version not recorded in searched script and reports` | 2026-05-03 | `UNKNOWN — master report records 14 candidates, not total configurations` | `UNKNOWN — pre-strict classifications` | `research/overnight_intake_batch_2026_05_03_CLEAN/MASTER_OVERNIGHT_QUANTLENS_REPORT.md:1-29`. |
| `stage2_robustness_2026_05_03` | `run_stage2_robustness.py`; `UNKNOWN — version not recorded in searched script and reports` | 2026-05-03 | `UNKNOWN — report records 3 strategies and component tables, not a run-total configuration count` | `UNKNOWN — no robust_final field` | `research/stage2_robustness_2026_05_03/STAGE2_MASTER_REPORT.md:1-14,121-129`. |
| `stage2_robustness_2026_05_03_CODEX` | custom Stage-2 scripts; `UNKNOWN — version not recorded in searched scripts and reports` | 2026-05-03 | `UNKNOWN — searched prelim results and master report` | `UNKNOWN — no robust_final field` | `research/stage2_robustness_2026_05_03_CODEX/STAGE2_MASTER_REPORT.md`; `stage2_prelim_results.csv`. |
| `stage2_robustness_2026_05_03_CODEX_20260503_232808` | `run_stage2_codex.py`; `UNKNOWN — version not recorded in searched script and reports` | 2026-05-03 | `UNKNOWN — parameter-grid and result CSVs lack one authoritative run-total field` | `UNKNOWN — report says no PASS_STAGE3, not current strict gate` | `research/.../STAGE2_MASTER_REPORT.md:1-18,41-63`; `parameter_grid_results.csv`. |
| `strategy_batch_2026_05_03` | `run_batch.py`; `UNKNOWN — version not recorded in searched script and reports` | 2026-05-03 | `UNKNOWN — searched master report and candidate index` | `UNKNOWN — no robust_final field` | `research/strategy_batch_2026_05_03/MASTER_BATCH_REPORT.md`; `STRATEGY_CANDIDATE_INDEX.csv`. |
| `strategy_batch_2026_05_03_5M_RERUN` | `run_5m_rerun.py`; `UNKNOWN — version not recorded in searched script and reports` | 2026-05-03 | `UNKNOWN — report records 2 strategies / 5 tested assets each, not configuration total` | `UNKNOWN — no robust_final field` | `research/strategy_batch_2026_05_03_5M_RERUN/5M_RERUN_MASTER_REPORT.md:1-47`; `summary.csv`. |
| `stage2B_code_verification_2026_05_04_CODEX` | `run_stage2b_codex_verification.py`; `UNKNOWN — version not recorded in searched script and reports` | 2026-05-04 | `UNKNOWN — six candidate verification folders, no authoritative run-total configuration count` | `UNKNOWN — reused OOS and synthetic verification, no robust_final` | `research/stage2B_code_verification_2026_05_04_CODEX/CODEX_STAGE2B_MASTER_REPORT.md`; `RUN_LOG.md`. |

`strategy_batch_2026_05_03_AUDITED` and the dated `overnight_intake...AUDITED*` / transcript-audit directories are derived audits or report rewrites, not independent backtest runs; their source run is already represented above. Data acquisition, transcript intake, contract audits, rankings, and code-only audits were excluded because they contain no independent recorded backtest/result run.

## Completeness boundary

The search enumerated every directly available final JSON rather than sampling it and also surfaced unprompted tool-run trees. Nevertheless, this checkout cannot provide an all-time proof because historical result directories were git-ignored, four of six registered run directories are absent, the backtest registry is empty, and older/custom result packages do not encode the current strict field. Therefore the strict count is **zero for the directly parseable 67-file corpus**, while the repository-wide all-time count remains **UNKNOWN — all-time strict count not recoverable from the searched tracked checkout, registries, handoffs, and archived evidence**.
