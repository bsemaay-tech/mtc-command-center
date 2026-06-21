# GEN_RSI TRXUSDT 1H SOURCE_NAKED Artifact Generation Report - 2026-06-16

## 1. Executive summary

Controlled artifact generation completed for the approved bucket:

`GEN_RSI_OVERSOLD_REVERSAL | TRXUSDT | 1h | SOURCE_NAKED`

One research-only `backtest_profile_result.json` artifact was created from the approved same-bucket source files. The artifact contains exactly one result row, preserves `promotion_status=RESEARCH_ONLY`, preserves `promotable=false`, preserves Gate 3 as `INCOMPLETE`, and does not create or imply paper/live readiness.

Final verdict: `ARTIFACT GENERATED - READY FOR AUDIT`

## 2. Generated files

Generated exactly one artifact JSON:

`MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/profile_result_GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h_SOURCE_NAKED_2026-06-16/backtest_profile_result.json`

Generated this report:

`MTC_COMMAND_CENTER/11_TRIAGE/GEN_RSI_TRXUSDT_1H_SOURCE_NAKED_ARTIFACT_GENERATION_REPORT_2026-06-16.md`

No `top_results.json` was generated.

## 3. Source files used

Primary eval source:

`MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/evaluation_artifacts/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`

Primary scorecard source:

`MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/scorecard_v2/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`

Supporting same-run provenance files:

- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/all_gate/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/all_gate_g3enriched/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/gate2_scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/gate3_scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`

No other symbol/timeframe bucket was used.

## 4. Schema/structure validation

Schema reference:

`MTC_COMMAND_CENTER/06_SCHEMAS/backtest_profile_result.schema.json`

Validation results:

- JSON parse: PASS.
- `jsonschema` validation against `backtest_profile_result.schema.json`: PASS.
- `schema_version` present: PASS.
- `run_id` present: PASS.
- `results` present: PASS.
- `results` count is exactly 1: PASS.
- Row identity is `GEN_RSI_OVERSOLD_REVERSAL | TRXUSDT | 1h | SOURCE_NAKED`: PASS.
- `promotion_status == RESEARCH_ONLY`: PASS.
- `promotable == false`: PASS.
- Gate 3 remains `INCOMPLETE`: PASS.
- `blocking` preserves `gate3`: PASS.
- All artifact provenance paths exist: PASS.
- Required missing fields are explicit `null`: PASS.

## 5. Metrics mapping

| Artifact field | Source field | Value |
|---|---|---:|
| `metrics.net_profit` | `metrics.net_profit_pct.value` | 70.498 |
| `metrics.profit_factor` | `metrics.profit_factor.value` | 1.381 |
| `metrics.max_drawdown` | `metrics.max_drawdown_pct.value` | 13.07 |
| `metrics.trade_count` | `metrics.trades.value` | 280 |
| `metrics.sharpe` | `metrics.sharpe.value` | 1.753 |
| `metrics.sortino` | `metrics.sortino.value` | 2.4775 |
| `metrics.max_loss_streak` | `metrics.max_consecutive_losses.value` | 10 |
| `metrics.buy_hold_alpha` | `benchmark.excess_alpha_pct.value` | -37.743 |

Robustness fields preserved:

- `cpcv_pass_ratio=0.9778`
- `pbo=0.00021`
- `dsr_p_value=0.0`
- `boot_p_value=0.004`
- `wfo_pass=true`
- `multi_window_pass=true`
- `net_after_slippage_pct=52.459`
- `worst_window_drawdown_pct=16.473`
- `overfit_suspect=false`
- `parity_status=N_A`

## 6. Null/default handling

Explicit null fields:

- `parameter_set_id=null`
- `metrics.win_rate=null`
- `metrics.buy_hold_return=null`
- `metrics.exposure=null`
- `metrics.avg_trade=null`

No missing values were fabricated. `avg_trade_vs_cost` was not remapped as `avg_trade`, and `benchmark.excess_alpha_pct` was not remapped as `buy_hold_return`.

## 7. Gate/promotion status

Gate summary preserved:

| Gate | Status | Score |
|---|---|---:|
| Gate 1 | OK | 96.0 |
| Gate 1B | OK | 80.0 |
| Gate 2 | OK | 92.0 |
| Gate 3 | INCOMPLETE | 46.0 |

Promotion and readiness fields:

- `promotion_status=RESEARCH_ONLY`
- `promotable=false`
- `all_pass=false`
- `blocking=["gate3"]`
- `paper_ready=false`
- `live_ready=false`
- `native_us_equities=false`
- `mtc_light=false`
- `risk_normalized=false`
- `top_results_ranking=false`
- `strategy_promotion=false`

## 8. Provenance

The artifact includes exact provenance paths for:

- primary eval
- primary scorecard
- all-gate eval
- all-gate Gate-3-enriched eval
- Gate 2 scorecard
- Gate 3 scorecard
- planning report

Manual provenance check confirmed that all row-level `artifacts` paths resolve to existing files in this workspace.

## 9. `top_results.json` confirmation

Before generation, recursive `top_results.json` count under `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/` was 0.

After generation, recursive `top_results.json` count remains 0.

No `top_results.json` was generated.

## 10. Git/index status

Required preflight was run:

- `git status --short`
- `git diff --cached --stat`
- `git log --oneline -8`

Preflight index status:

- `git diff --cached --stat` returned no output.
- Index was empty, so generation proceeded.

Post-generation index status:

- `git diff --cached --stat` returned no output.
- No files were staged.

Profile artifact count:

- Before generation: 1 `backtest_profile_result.json`.
- After generation: 2 `backtest_profile_result.json` files.
- The added file is the GEN_RSI/TRXUSDT/1h SOURCE_NAKED artifact listed in section 2.

Worktree note:

The repository had unrelated modified and untracked files before generation. They were left untouched. The intended new outputs are the artifact JSON and this report.

Git visibility note:

- The generation report appears as an untracked file.
- The artifact JSON exists on disk but does not appear in `git status --short` because `.gitignore` ignores `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/`.
- Direct file existence and recursive artifact count checks confirm the artifact was created.

## 11. Protected scope check

Protected scope commands were run:

```powershell
git diff --name-only -- MTC_COMMAND_CENTER/02_MTC_BACKTEST MTC_COMMAND_CENTER/07_ADAPTERS MTC_COMMAND_CENTER/01_PINE MTC_COMMAND_CENTER/MTC_V2
git diff --cached --name-only -- MTC_COMMAND_CENTER/02_MTC_BACKTEST MTC_COMMAND_CENTER/07_ADAPTERS MTC_COMMAND_CENTER/01_PINE MTC_COMMAND_CENTER/MTC_V2
```

Result: no output.

Protected scopes were not modified or staged.

## 12. Safety confirmation

Confirmed:

- No code modified.
- No files staged or committed.
- No files deleted, reset, or moved.
- No backtests run.
- No optimizations run.
- No `top_results.json` generated.
- No Pine files touched.
- No MTC_V2 files touched.
- No backtest engine execution logic touched.
- No broker/live/paper execution logic touched.
- No API write behavior changed.
- No strategy logic changed.
- Exactly one new `backtest_profile_result.json` artifact was generated.
- Exactly one generation report was generated.

## 13. Recommended next action

Audit the generated artifact as a read-only research/profile result. If accepted, run a dashboard/read-model discovery check in a separate task to confirm whether the existing reader detects the new `SOURCE_NAKED` row as non-promotional research evidence.
