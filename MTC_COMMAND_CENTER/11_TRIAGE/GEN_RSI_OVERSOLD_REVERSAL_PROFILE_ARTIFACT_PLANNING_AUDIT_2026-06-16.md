# GEN_RSI_OVERSOLD_REVERSAL Profile Artifact Planning Audit - 2026-06-16

## 1. Executive summary

`GEN_RSI_OVERSOLD_REVERSAL` has enough real evidence to justify planning discussion for a future `SOURCE_NAKED` profile artifact, but it is not ready for artifact generation without a user decision.

Focused read-only inspection found:

- 155 matching scorecard files.
- 115 matching eval artifacts.
- 60 `scorecard_v2` / all-gate scorecard files.
- 0 existing profile-result rows for `GEN_RSI_OVERSOLD_REVERSAL`.
- 0 `top_results.json` files for this strategy.
- Observed scorecard/eval symbols: `TRXUSDT`, `ETHUSDT`, `LINKUSDT`.
- Observed scorecard/eval timeframes: `1h`, `2h`, `4h`.

The evidence rows are real, KPI-rich, and traceable to MEGA/evaluation artifacts. The best repeated scorecard bucket is `GEN_RSI_OVERSOLD_REVERSAL|LINKUSDT|2h` with Gate 2 score 99.18 across multiple runs. The strongest metric bucket by Sharpe/net return is `TRXUSDT|1h`, and the strategy folder also contains an older `QL_ALPHA_LTC_RSI_OVERSOLD_1H` promotion packet tied to `LTCUSDT|1h`. That conflict means the first artifact pilot bucket must be selected explicitly before generation.

Final verdict: `PARTIAL - NEEDS USER DECISION`

## 2. Candidate identity

| Field | Finding |
|---|---|
| Engine strategy ID | `GEN_RSI_OVERSOLD_REVERSAL` |
| Display name | `RSI Oversold Reversal` from `05_REGISTRY/AI_STRATEGY_NAME_REGISTRY.json` |
| AI verdict registry presence | Present in `05_REGISTRY/AI_QUANTLENS_VERDICT_REGISTRY.json` |
| Related strategy folder | `03_QUANTLENS/strategies/STG003_ql_alpha_ltc_rsi_oversold_1h/` |
| Related legacy/promotion candidate | `QL_ALPHA_LTC_RSI_OVERSOLD_1H` |
| Related source folder symbol/timeframe | `LTCUSDT|1h` |
| Current highest repeated scorecard bucket | `LINKUSDT|2h` |
| Current strongest eval-metric bucket | `TRXUSDT|1h` |

The candidate is an engine strategy family, not a single frozen source-profile result. That is the main planning issue.

## 3. Search scope and method

Read-only search covered:

- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/`
- `MTC_COMMAND_CENTER/03_QUANTLENS/strategies/`
- `MTC_COMMAND_CENTER/03_QUANTLENS/_registry/`
- `MTC_COMMAND_CENTER/05_REGISTRY/`
- `MTC_COMMAND_CENTER/11_TRIAGE/`

Methods:

- Dispatched the focused scan/report to `_deepseek_driver/ds_agent.py` first. The harness wrote no repo files and hit max iterations without a final report.
- Parsed matching `GEN_RSI_OVERSOLD_REVERSAL*.scorecard.json`.
- Parsed matching `GEN_RSI_OVERSOLD_REVERSAL*.eval.json`.
- Searched profile artifacts for existing `GEN_RSI_OVERSOLD_REVERSAL` rows.
- Searched registry/name/verdict files for candidate identity.
- Read related STG003 source-folder docs and `producer_spec.json`.

No backtest, optimizer, builder, converter, dashboard server, or artifact generator was run.

## 4. Evidence inventory

| Evidence type | Count | Notes |
|---|---:|---|
| Matching scorecard files | 155 | Includes raw `scorecards`, `gate2_scorecards`, `gate3_scorecards`, `scorecard_v2`, all-gate, and iter-specific scorecards. |
| Matching eval files | 115 | KPI-rich `evaluation_artifacts` / `all_gate` / `all_gate_g3enriched` files. |
| Canonical `scorecard_v2` / all-gate scorecards | 60 | Best source for gate/promotion status. |
| Existing profile-result rows | 0 | No `backtest_profile_result.json` row for `GEN_RSI_OVERSOLD_REVERSAL`. |
| Existing `top_results.json` | 0 | No bucketed top-results artifact exists. |
| Related strategy source folder | 1 | `STG003_ql_alpha_ltc_rsi_oversold_1h`. |

Matching scorecard/eval runs:

| Run/folder | Scorecards | Evals | Notes |
|---|---:|---:|---|
| `final_gate2_2026-06-05_39b51db` | 30 | 15 | Contains `scorecard_v2`, all-gate, and gate folders. |
| `night_1m_2026-06-07` | 15 | 15 | Iter 05 evidence. |
| `heavy_tier_2026-06-05` | 15 | 15 | Repeated high-score evidence. |
| `full_sweep_2026-06-07` | 15 | 15 | Repeated high-score evidence. |
| `batch023_034_2026-06-07` | 15 | 15 | Repeated high-score evidence. |
| `night_3M_2026-06-08` | 10 | 10 | Iter 09 evidence. |
| `worst_window_2026-06-05_283d198` | 10 | 5 | Stress/enrichment variant. |
| `slippage_2026-06-05_5c68419` | 10 | 5 | Stress/enrichment variant. |
| `enriched_metrics_2026-06-05` | 10 | 5 | Enriched metrics. |
| `bh_benchmark_2026-06-05_7175ff6` | 10 | 5 | Benchmark comparison. |
| `annualized_risk_2026-06-05_15e8d47` | 10 | 5 | Risk enrichment. |
| `confirm_2026-06-04` | 5 | 5 | Earlier confirmation evidence. |

## 5. Scorecard/eval coverage

The strongest repeated `scorecard_v2` bucket is:

| Bucket | `scorecard_v2` count | Max Gate 2 score | Gate statuses seen | Promotable |
|---|---:|---:|---|---|
| `LINKUSDT|2h` | 12 | 99.18 | Gate 1 OK, Gate 1B OK, Gate 2 OK, Gate 3 INCOMPLETE in mature rows | false |
| `TRXUSDT|1h` | 12 | 92.00 | Gate 1 OK, Gate 1B OK, Gate 2 OK, Gate 3 INCOMPLETE in mature rows | false |
| `TRXUSDT|2h` | 12 | 92.00 | Gate 1 OK, Gate 1B OK, Gate 2 OK, Gate 3 INCOMPLETE in mature rows | false |
| `ETHUSDT|4h` | 12 | 89.19 | Gate 1 OK, Gate 1B OK, Gate 2 OK, Gate 3 INCOMPLETE in mature rows | false |
| `ETHUSDT|2h` | 12 | 74.20 | Gate 2 FAIL in mature rows | false |

Best scorecard example:

`03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/scorecard_v2/GEN_RSI_OVERSOLD_REVERSAL_LINKUSDT_2h.scorecard.json`

- Gate 1: OK
- Gate 1B: OK
- Gate 2: OK
- Gate 3: INCOMPLETE
- Gate 2 score: 99.18
- `promotable`: false

Strongest eval-metric bucket by Sharpe/net return:

`03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/evaluation_artifacts/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`

- net profit: 70.498%
- profit factor: 1.381
- max drawdown: 13.07%
- trades: 280
- Sharpe: 1.753
- Sortino: 2.4775
- CPCV pass ratio: 0.9778 in the all-gate/night evidence
- PBO: 0.00021 in the night/full-sweep evidence
- DSR p-value: 0.0
- bootstrap p-value: 0.004

## 6. Symbols and timeframes

Scorecard/eval evidence is concentrated in crypto/USDT markets.

| Evidence set | Symbols | Timeframes |
|---|---|---|
| All matching scorecards | TRXUSDT 62, ETHUSDT 61, LINKUSDT 32 | 2h 93, 1h 32, 4h 30 |
| All matching evals | TRXUSDT 46, ETHUSDT 45, LINKUSDT 24 | 2h 69, 1h 24, 4h 22 |
| `scorecard_v2` buckets | LINKUSDT, TRXUSDT, ETHUSDT | 1h, 2h, 4h |
| Broader MEGA rows | 17 USDT symbols across 15m/1h/2h/4h/1D | Broad historical research evidence, not a selected artifact bucket |

Important mismatch:

- The related strategy folder `STG003_ql_alpha_ltc_rsi_oversold_1h` is tied to `LTCUSDT|1h`.
- The focused result scorecard/eval evidence for `GEN_RSI_OVERSOLD_REVERSAL` under current `05_BACKTEST_RESULTS` is strongest for `LINKUSDT|2h` and `TRXUSDT|1h`.
- The current parsed scorecard/eval set did not surface a matching `LTCUSDT|1h` scorecard/eval artifact, although older docs and reports reference it.

## 7. KPI availability

Eval artifacts contain the required KPI fields for profile-result planning:

| KPI | Availability |
|---|---|
| net profit | Present as `metrics.net_profit_pct` |
| profit factor | Present as `metrics.profit_factor` |
| max drawdown | Present as `metrics.max_drawdown_pct` |
| win rate | Not consistently present in eval metric key list; available in older promotion docs for LTC bucket |
| trade count | Present as `metrics.trades` |
| Sharpe | Present as `metrics.sharpe` |
| Sortino | Present as `metrics.sortino` |
| DSR | Present as `metrics.dsr_p_value` |
| PBO | Present as `metrics.pbo` in most enriched/night evidence |
| CPCV | Present as `metrics.cpcv_pass_ratio` in all-gate/night evidence |
| benchmark alpha | Present in eval `benchmark.excess_alpha_pct` |
| source path | Present on metric fields, e.g. `mega:summary.lockbox_oos.net_return_pct` |

The KPI set is adequate for a future research/profile artifact, provided the selected row set is narrowed to one compatible bucket.

## 8. Gate and promotion status

Mature `scorecard_v2` rows show:

- Gate 1: OK
- Gate 1B: OK
- Gate 2: OK for the strongest buckets, FAIL for `ETHUSDT|2h`
- Gate 3: INCOMPLETE
- `promotable`: false

Across canonical `scorecard_v2` / all-gate rows:

- 60 rows parsed.
- 0 rows had `promotable=true`.
- 0 rows had Gate 3 OK.
- 0 profile-result rows existed for this strategy.

Related STG003 docs state `PROMOTE_TO_FORWARD_PAPER_TRADE` for `QL_ALPHA_LTC_RSI_OVERSOLD_1H`, but also explicitly say it is not approved for live trading, has parity deferred, weak fold consistency, and source fidelity still needs confirmation. That historical promotion packet should not override current artifact-readiness gates.

## 9. Provenance assessment

Provenance is usable but not complete enough for immediate artifact generation.

Positive evidence:

- Eval metrics include source paths such as `mega:summary.lockbox_oos.net_return_pct`, `cpcv:pass_rate`, and `pbo:pbo`.
- Scorecard files point to consistent strategy/symbol/timeframe IDs.
- Multiple runs repeat the same leading buckets.
- Related STG003 docs include deterministic producer/spec context for an RSI oversold recovery strategy.

Gaps:

- Existing evidence does not declare `SOURCE_NAKED` profile.
- No `backtest_profile_result.json` row exists for this strategy.
- No `top_results.json` exists.
- The highest current bucket (`LINKUSDT|2h`) does not match the older source-folder/promotion identity (`LTCUSDT|1h`).
- `SOURCE_NAKED` mapping would be an interpretation that needs explicit user approval before conversion.

## 10. Same-bucket/profile assessment

A same-bucket pilot can be identified, but not automatically chosen.

Candidate buckets:

| Bucket | Strength | Weakness |
|---|---|---|
| `LINKUSDT|2h` | Highest repeated Gate 2 score, 99.18; Gate 1/Gate 1B/Gate 2 OK; repeated across several runs | Only 50 trades in best eval; lower Sharpe than TRXUSDT; does not match STG003 LTC source identity |
| `TRXUSDT|1h` | Strongest eval metrics: 70.498% net, PF 1.381, 280 trades, Sharpe 1.753, Sortino 2.4775 | Gate 2 score lower than LINK bucket; crypto/proxy nature must be accepted |
| `TRXUSDT|2h` | Solid score/eval evidence and repeated rows | Less compelling than TRXUSDT 1h |
| `LTCUSDT|1h` | Matches STG003 source/promotion docs and producer spec | Current focused scorecard/eval parse did not find matching current artifacts; older docs warn weak fold consistency/source confirmation |

Planning conclusion:

- Do not mix symbols/timeframes into one profile artifact bucket.
- Do not convert all 155 scorecards or 115 evals as one artifact.
- If user approves artifact planning, choose exactly one same-bucket source: likely `LINKUSDT|2h` for scorecard strength or `TRXUSDT|1h` for metric strength.

## 11. Artifact planning readiness

Classification: `PARTIAL - NEEDS USER DECISION`

Why it is not `READY FOR SOURCE_NAKED ARTIFACT PLANNING`:

- No existing profile declaration.
- No existing profile-result rows.
- Bucket choice is ambiguous.
- Gate 3 remains incomplete and `promotable=false`.
- Related STG003 docs point to a different symbol/timeframe than the leading current scorecard bucket.

Why it is not `RESEARCH-ONLY ONLY - DO NOT PLAN ARTIFACT`:

- Rows are real.
- Strategy identity is consistent at the engine-strategy level.
- KPI fields are present and traceable.
- No fatal `RESEARCH_ONLY` or `universe_mismatch` flag was found for the GEN_RSI scorecard/eval rows.
- A research-grade `SOURCE_NAKED` planning step can be considered if explicitly scoped to one same-bucket row set and labeled non-promotional.

## 12. Risks and blockers

- Profile mapping risk: `SOURCE_NAKED` is not explicitly present in the source rows.
- Bucket-mixing risk: evidence spans multiple symbols, timeframes, run folders, and enrichment variants.
- Promotion confusion risk: historical STG003 docs use promotion language for forward paper-trade prep, but current Gate 3 is incomplete and `promotable=false`.
- Source fidelity risk: STG003 docs say fidelity to original YouTube source needs confirmation.
- Comparability risk: high scorecard bucket (`LINKUSDT|2h`) is not the same as strongest eval bucket (`TRXUSDT|1h`) or older source bucket (`LTCUSDT|1h`).
- Artifact risk: generating `top_results.json` now would be premature without an approved same-profile result set.

## 13. Recommendation

Do not generate an artifact yet.

Recommended next step, if Baris wants to proceed:

1. User chooses one pilot bucket:
   - `LINKUSDT|2h` for highest repeated Gate 2 score, or
   - `TRXUSDT|1h` for strongest KPI/eval profile, or
   - `LTCUSDT|1h` only if the older STG003 source/promotion identity is intentionally prioritized and matching current artifacts are located/validated.
2. Treat the future artifact as research/profile evidence only, not promotion.
3. Require the future artifact builder/converter to use only one strategy/symbol/timeframe/run-source bucket.
4. Preserve `promotable=false` / Gate 3 incomplete status.
5. Do not create `top_results.json` until same-profile rows are available and the comparison set is approved.

Final verdict: `PARTIAL - NEEDS USER DECISION`

## 14. Safety confirmation

- No code was modified.
- No files were staged or committed.
- No files were deleted, reset, or moved.
- No backtests were run.
- No optimizations were run.
- No artifacts were generated.
- No `backtest_profile_result.json` was generated.
- No `top_results.json` was generated.
- No Pine files were touched.
- No MTC_V2 files were touched.
- No parity files were touched.
- No backtest engine execution logic was touched.
- No broker/live/paper execution logic was touched.
- No API write behavior was changed.
- No strategy logic was changed.
- The DeepSeek dispatch wrote no repository files.
- The only repository file created by this task is this report.
