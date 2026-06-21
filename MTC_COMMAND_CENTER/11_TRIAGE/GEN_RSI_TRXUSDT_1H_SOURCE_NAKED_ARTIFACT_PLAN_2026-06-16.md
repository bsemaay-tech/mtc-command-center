# GEN_RSI_OVERSOLD_REVERSAL TRXUSDT 1h SOURCE_NAKED Artifact Plan - 2026-06-16

## 1. Executive summary

This is a planning-only report for a future `SOURCE_NAKED` `backtest_profile_result.json` artifact for:

`GEN_RSI_OVERSOLD_REVERSAL | TRXUSDT | 1h`

Focused read-only inspection found a coherent same-bucket evidence set:

- 23 exact eval files for `GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`.
- 31 exact scorecard files for `GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`.
- A same-run primary candidate in `night_1m_2026-06-07/iter_05`.
- Direct KPI fields for net profit, profit factor, max drawdown, trades, Sharpe, Sortino, CPCV pass ratio, PBO, DSR p-value, bootstrap p-value, and max consecutive losses.
- Gate 1, Gate 1B, and Gate 2 are OK in the primary same-run `scorecard_v2`; Gate 3 remains INCOMPLETE and `gate_summary.promotable=false`.
- Registry verdict remains `RESEARCH_ONLY`.

Final verdict: `READY FOR CONTROLLED ARTIFACT GENERATION`

This verdict means only that a future research/profile artifact can be generated from the selected same-bucket evidence. It does not promote the strategy, does not make it paper-ready, does not make it live-ready, and does not create native US equities evidence.

## 2. Selected bucket

| Field | Selected value |
|---|---|
| Strategy family | `GEN_RSI_OVERSOLD_REVERSAL` |
| Display name | `RSI Oversold Reversal` |
| Symbol | `TRXUSDT` |
| Timeframe | `1h` |
| Planned profile | `SOURCE_NAKED` |
| Evidence class | Crypto/USDT research evidence |
| Excluded buckets | `LINKUSDT|2h`, `TRXUSDT|2h`, `ETHUSDT|4h`, `LTCUSDT|1h`, and every other symbol/timeframe |

The selected bucket is the strongest eval/KPI bucket from the prior focused audit and is now explicitly chosen by user decision.

## 3. Source file inventory

Exact eval files found for the selected bucket:

- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/annualized_risk_2026-06-05_15e8d47/evaluation_artifacts/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/batch023_034_2026-06-07/all_gate/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/batch023_034_2026-06-07/all_gate_g3enriched/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/batch023_034_2026-06-07/evaluation_artifacts/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/bh_benchmark_2026-06-05_7175ff6/evaluation_artifacts/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/confirm_2026-06-04/evaluation_artifacts/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/enriched_metrics_2026-06-05/evaluation_artifacts/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/final_gate2_2026-06-05_39b51db/all_gate_artifacts/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/final_gate2_2026-06-05_39b51db/all_gate_g3enriched/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/final_gate2_2026-06-05_39b51db/evaluation_artifacts/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/full_sweep_2026-06-07/all_gate/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/full_sweep_2026-06-07/all_gate_g3enriched/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/full_sweep_2026-06-07/evaluation_artifacts/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/heavy_tier_2026-06-05/all_gate/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/heavy_tier_2026-06-05/all_gate_g3enriched/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/heavy_tier_2026-06-05/evaluation_artifacts/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/all_gate/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/all_gate_g3enriched/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/evaluation_artifacts/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_3M_2026-06-08/iter_09/all_gate/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_3M_2026-06-08/iter_09/evaluation_artifacts/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/slippage_2026-06-05_5c68419/evaluation_artifacts/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/worst_window_2026-06-05_283d198/evaluation_artifacts/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`

Exact scorecard files found for the selected bucket:

- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/annualized_risk_2026-06-05_15e8d47/scorecard_v2/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/annualized_risk_2026-06-05_15e8d47/scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/batch023_034_2026-06-07/gate2_scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/batch023_034_2026-06-07/gate3_scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/batch023_034_2026-06-07/scorecard_v2/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/bh_benchmark_2026-06-05_7175ff6/scorecard_v2/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/bh_benchmark_2026-06-05_7175ff6/scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/confirm_2026-06-04/scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/enriched_metrics_2026-06-05/scorecard_v2/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/enriched_metrics_2026-06-05/scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/final_gate2_2026-06-05_39b51db/gate1_scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/final_gate2_2026-06-05_39b51db/gate1b_scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/final_gate2_2026-06-05_39b51db/gate2_scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/final_gate2_2026-06-05_39b51db/gate3_scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/final_gate2_2026-06-05_39b51db/scorecard_v2/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/final_gate2_2026-06-05_39b51db/scorecard_v2_all_gate/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/full_sweep_2026-06-07/gate2_scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/full_sweep_2026-06-07/gate3_scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/full_sweep_2026-06-07/scorecard_v2/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/heavy_tier_2026-06-05/gate2_scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/heavy_tier_2026-06-05/gate3_scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/heavy_tier_2026-06-05/scorecard_v2/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/gate2_scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/gate3_scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/scorecard_v2/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_3M_2026-06-08/iter_09/gate2_scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_3M_2026-06-08/iter_09/scorecard_v2/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/slippage_2026-06-05_5c68419/scorecard_v2/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/slippage_2026-06-05_5c68419/scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/worst_window_2026-06-05_283d198/scorecard_v2/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/worst_window_2026-06-05_283d198/scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`

## 4. Primary source recommendation

Primary eval source:

`MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/evaluation_artifacts/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`

Primary companion scorecard:

`MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/scorecard_v2/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`

Same-run enrichment/supporting files:

- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/all_gate/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/all_gate_g3enriched/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/gate2_scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/gate3_scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`

Reason for primary selection:

- It is in the user-selected bucket: `GEN_RSI_OVERSOLD_REVERSAL | TRXUSDT | 1h`.
- It has the KPI values cited by the user decision.
- It has same-run `all_gate`, `all_gate_g3enriched`, Gate 2, Gate 3, and `scorecard_v2` companions.
- Its primary `scorecard_v2` has Gate 1 OK, Gate 1B OK, Gate 2 OK, Gate 3 INCOMPLETE, and `promotable=false`.

## 5. Duplicate/enrichment variant analysis

The same selected bucket appears across multiple result folders. Most mature rows repeat the same main KPI values:

| Run group | Main role | Main KPI pattern |
|---|---|---|
| `night_1m_2026-06-07/iter_05` | Recommended primary | Net 70.498, PF 1.381, DD 13.07, trades 280, Sharpe 1.753, Sortino 2.4775, CPCV 0.9778, PBO 0.00021, DSR p 0.0, bootstrap p 0.004 |
| `full_sweep_2026-06-07` | Supporting duplicate | Same main values as primary; contains `all_gate` and `all_gate_g3enriched` variants |
| `batch023_034_2026-06-07` | Supporting duplicate | Same main values; PBO observed as 0.00026 |
| `heavy_tier_2026-06-05` | Supporting duplicate | Same main values; CPCV 1.0 and PBO 0.0 |
| `final_gate2_2026-06-05_39b51db` | Supporting duplicate | Same main values; mature Gate 2 evidence |
| `night_3M_2026-06-08/iter_09` | Supporting duplicate | Same main values; Gate 2 score lower/incomplete in scorecard_v2 |
| `confirm_2026-06-04` | Older/non-primary | Weaker metrics: net 7.823, PF 1.093, DD 18.423 |

Do not aggregate or blend these rows in the future artifact. The future artifact should use one primary row and preserve duplicate/enrichment files only as provenance/supporting artifacts.

## 6. Schema mapping plan

Target schema:

`MTC_COMMAND_CENTER/06_SCHEMAS/backtest_profile_result.schema.json`

Required document-level field:

| Schema field | Planned source/value |
|---|---|
| `run_id` | Use a generated artifact run id that includes the primary source folder and source `backtest_run_id`, for example `night_1m_2026-06-07_iter_05_MEGA_walk_forward_results_SOURCE_NAKED_TRXUSDT_1h`. |
| `schema_version` | Use the current profile artifact writer version if one exists; otherwise set a clear local version such as `backtest_profile_result.v1`. |
| `results` | One-row array for the selected bucket only. |

Required row fields:

| Schema field | Planned source/value |
|---|---|
| `strategy_id` | `GEN_RSI_OVERSOLD_REVERSAL` or preserve full source id in provenance while normalizing row id to strategy family. Source eval/scorecard id is `GEN_RSI_OVERSOLD_REVERSAL|TRXUSDT|1h`. |
| `profile` | `SOURCE_NAKED` |
| `symbol` | `TRXUSDT` |
| `timeframe` | `1h` |

Optional row fields:

| Schema field | Planned source/value |
|---|---|
| `parameter_set_id` | `null` unless an exact parameter-set identifier is found in the future generator pass. |
| `score_method` | `gate_scorecard_v2` or equivalent explicit method label. |
| `score` | `92.0` from primary `scorecard_v2.gate2.score`; do not imply full promotion score. |
| `gate_summary` | Copy from primary `scorecard_v2.gate_summary`: Gate 1 OK, Gate 1B OK, Gate 2 OK, Gate 3 INCOMPLETE, `all_pass=false`, `promotable=false`, blocking `gate3`. |
| `metrics.net_profit` | `metrics.net_profit_pct.value = 70.498` |
| `metrics.profit_factor` | `metrics.profit_factor.value = 1.381` |
| `metrics.max_drawdown` | `metrics.max_drawdown_pct.value = 13.07` |
| `metrics.win_rate` | `null`; no direct win-rate field observed in the primary eval metrics. |
| `metrics.trade_count` | `metrics.trades.value = 280` |
| `metrics.buy_hold_return` | `null`; benchmark object contains alpha/beat flags but no direct buy-hold return value in primary eval. |
| `metrics.buy_hold_alpha` | `benchmark.excess_alpha_pct.value = -37.743` |
| `metrics.sharpe` | `metrics.sharpe.value = 1.753` |
| `metrics.sortino` | `metrics.sortino.value = 2.4775` |
| `metrics.exposure` | `null`; no direct exposure metric observed. |
| `metrics.avg_trade` | `null`; only `avg_trade_vs_cost=3.147` is available and should not be silently remapped as average trade return. |
| `metrics.max_loss_streak` | `metrics.max_consecutive_losses.value = 10` |
| `benchmark` | Preserve primary eval `benchmark`, including `excess_alpha_pct=-37.743`, `beats_bh_risk_adjusted=false`, and `beats_ema_benchmark=true`. |
| `robustness` | Preserve CPCV/PBO/DSR/bootstrap/WFO/multi-window fields from primary eval. |
| `artifacts` | Include exact source eval, same-run all-gate evals, primary scorecard, Gate 2 scorecard, and Gate 3 scorecard paths. |
| `promotion_status` | `RESEARCH_ONLY` |

Additional useful robustness fields from the primary eval:

- `metrics.cpcv_pass_ratio.value = 0.9778`
- `metrics.pbo.value = 0.00021`
- `metrics.dsr_p_value.value = 0.0`
- `metrics.boot_p_value.value = 0.004`
- `metrics.wfo_pass.value = true`
- `metrics.multi_window_pass.value = true`
- `metrics.net_after_slippage_pct.value = 52.459`
- `metrics.worst_window_drawdown_pct.value = 16.473`
- `hard_flags.overfit_suspect = false`
- `flags.parity_status = N_A`

## 7. Missing fields / null/default handling

Use explicit `null` rather than invented values for:

- `win_rate`
- `parameter_set_id`
- `buy_hold_return`
- `exposure`
- `avg_trade`

Do not coerce:

- `avg_trade_vs_cost` into `metrics.avg_trade`
- `benchmark.excess_alpha_pct` into `buy_hold_return`
- Gate 2 score into a promotion approval score
- `SOURCE_NAKED` profile into `MTC_LIGHT` or `RISK_NORMALIZED`

Defaults that must be explicit in the future artifact:

- `profile=SOURCE_NAKED`
- `promotion_status=RESEARCH_ONLY`
- `promotable=false`
- `paper_ready=false` if such a field is included outside the schema core
- `live_ready=false` if such a field is included outside the schema core
- `native_us_equities=false` or equivalent provenance note if included

## 8. Required safety flags

Future artifact generation must preserve:

- `profile_type=SOURCE_NAKED` or schema field `profile=SOURCE_NAKED`.
- `promotion_status=RESEARCH_ONLY`.
- `promotable=false`.
- Gate 3 incomplete.
- Not paper-ready.
- Not live-ready.
- Crypto/USDT evidence only.
- Not US equities evidence.
- Not `MTC_LIGHT`.
- Not `RISK_NORMALIZED`.
- Not native US equities.
- Not a strategy promotion packet.

## 9. Gate/promotion status handling

Primary scorecard:

`MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/scorecard_v2/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`

Observed primary gate summary:

| Gate | Status | Score |
|---|---|---:|
| Gate 1 | OK | 96.0 |
| Gate 1B | OK | 80.0 |
| Gate 2 | OK | 92.0 |
| Gate 3 | INCOMPLETE | 46.0 |

Primary `gate_summary`:

- `all_pass=false`
- `promotable=false`
- `blocking=["gate3"]`

Registry status:

`MTC_COMMAND_CENTER/05_REGISTRY/AI_QUANTLENS_VERDICT_REGISTRY.json` records `GEN_RSI_OVERSOLD_REVERSAL` as `RESEARCH_ONLY`, with `risk_flags=["blocking:gate3"]`.

Future generation must not change any of these semantics.

## 10. `top_results.json` decision

Do not generate `top_results.json` in the next controlled artifact generation phase.

Reason:

- This planning pass is for a single selected bucket and a single future profile artifact row.
- `top_results.json` represents a top-N same-bucket ranking contract, not a single-row conversion proof.
- Generating it now would create ranking semantics before the first GEN_RSI profile row has been produced and reviewed.

Later generation can be reconsidered only after a validated `backtest_profile_result.json` exists and the ranking scope is explicitly defined as same profile, same timeframe, same universe, and same score method.

## 11. Artifact generation readiness

Classification: `READY FOR CONTROLLED ARTIFACT GENERATION`

Controlled generation is safe in the next phase if all of the following are enforced:

- Generate only `backtest_profile_result.json` for the selected `GEN_RSI_OVERSOLD_REVERSAL | TRXUSDT | 1h` row.
- Use the primary `night_1m_2026-06-07/iter_05` eval and scorecard sources.
- Preserve supporting same-run all-gate/enrichment files as provenance, not blended metric sources.
- Do not use any other symbol/timeframe bucket.
- Preserve `promotion_status=RESEARCH_ONLY` and `promotable=false`.
- Preserve Gate 3 incomplete.
- Do not generate `top_results.json` in the same step.
- Do not run backtests or optimization.

## 12. Risks and blockers

- The evidence is crypto/USDT only and must not be described as native US equities evidence.
- The profile label `SOURCE_NAKED` is a planned mapping decision; it is not present as an original source field in the eval/scorecard files.
- Related strategy-folder history points to older `LTCUSDT|1h` material, so provenance must be explicit that this artifact is for the engine bucket `GEN_RSI_OVERSOLD_REVERSAL|TRXUSDT|1h`.
- Gate 3 remains incomplete, so the artifact cannot be used for promotion, paper trading, or live trading.
- `win_rate`, direct `buy_hold_return`, exposure, average trade return, and parameter-set id are missing from the primary eval and must stay `null` unless found in a future read-only source review.
- Multiple duplicate/enrichment variants exist; a future generator must not average or cherry-pick across incompatible run folders.

## 13. Recommended next action

Proceed next with a controlled artifact-generation task that:

1. Creates one `backtest_profile_result.json` row for `GEN_RSI_OVERSOLD_REVERSAL | TRXUSDT | 1h`.
2. Uses `night_1m_2026-06-07/iter_05/evaluation_artifacts` as the primary metric source.
3. Uses `night_1m_2026-06-07/iter_05/scorecard_v2` as the primary gate source.
4. Records same-run `all_gate`, `all_gate_g3enriched`, Gate 2 scorecard, and Gate 3 scorecard paths as provenance.
5. Sets `profile=SOURCE_NAKED`, `promotion_status=RESEARCH_ONLY`, `promotable=false`, and Gate 3 incomplete.
6. Leaves `top_results.json` ungenerated.

## 14. Safety confirmation

Confirmed for this planning pass:

- No code modified.
- No files staged or committed.
- No backtests run.
- No optimizations run.
- No artifacts generated.
- No `backtest_profile_result.json` generated.
- No `top_results.json` generated.
- Only this planning report was created.
