# Native Result Source Discovery - 2026-06-16

## 1. Executive summary

No native usable result source was found for `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK`.

The repository contains real result data for the same strategy id, but every inspected result source is crypto/proxy evidence, not native US equities 10m validation. The one existing `backtest_profile_result.json` is explicitly profile-separated `SOURCE_NAKED` evidence, but its rows are XRPUSDT/TRXUSDT/NEARUSDT at 1h/4h/1D and each row is marked `promotion_status = RESEARCH_ONLY`.

Artifact generation for a native US equities 10m validation artifact is not allowed next.

## 2. Search scope and methods

Read-only discovery was performed across:

- `MTC_COMMAND_CENTER/03_QUANTLENS/`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/`
- `MTC_COMMAND_CENTER/03_QUANTLENS/strategies/`
- `MTC_COMMAND_CENTER/05_REGISTRY/`
- `MTC_COMMAND_CENTER/06_SCHEMAS/`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/`
- `MTC_COMMAND_CENTER/11_TRIAGE/`

Methods used:

- Exact text search for the target strategy id and related terms: `8EMA`, `8 EMA`, `EMA Pullback`, `US_EQUITIES`, `10M`, `10m`, `SOURCE_NAKED`, `MTC_LIGHT`, `RISK_NORMALIZED`, `MEGA_results`, `deterministic soak`, `profile result`, and `backtest_profile_result`.
- Read-only JSON/CSV/Markdown inspection of candidate files.
- Read-only Python parsing of existing JSON/CSV result files to aggregate target rows, symbols, timeframes, profile buckets, scorecards, evaluation artifacts, and profile result files.
- No backtest, optimizer, builder, dashboard server, API write, or artifact-generation command was executed.

## 3. Exact target definition

- `strategy_id`: `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK`
- Market/universe: US equities
- Timeframe: 10m
- Method: 8 EMA Pullback
- Desired source profile: `SOURCE_NAKED`, `MTC_LIGHT`, or `RISK_NORMALIZED`

Native match criteria:

- Same or clearly equivalent strategy id/name.
- US equities universe, or clearly US equity symbols.
- 10-minute timeframe, or clearly equivalent 10m bars.
- Real result output, not synthetic/fake/demo placeholder.
- Usable performance/evidence fields.
- Enough metadata to trace provenance.

## 4. Candidate source table

| Candidate source | Type | Strategy id/name | Symbols/universe | Timeframe | Profile | Rows/trades/cases | KPIs present | Provenance/source fields | Classification | Safe for later artifact generation? | Reason |
|---|---|---|---|---|---|---:|---|---|---|---|---|
| `03_QUANTLENS/05_BACKTEST_RESULTS/pilot_profile_result_QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-16/backtest_profile_result.json` | Profile result JSON | Exact target | XRPUSDT, TRXUSDT, NEARUSDT crypto | 4h, 1D, 1h | `SOURCE_NAKED` | 4 rows | net_profit, profit_factor, max_drawdown, win_rate, trade_count, sharpe, DSR/FDR flags | `provenance.source_path`, `source_type=deterministic_soak_mega_results` | C - Non-native / research-only | No, not for native artifact | Real sourced evidence, but crypto/timeframe mismatch and marked `RESEARCH_ONLY`. |
| `03_QUANTLENS/05_BACKTEST_RESULTS/QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_results.json` plus summary | Backtest JSON/Markdown | Exact target | BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, AVAXUSDT, DOGEUSDT | Not native 10m; crypto proxy run | None | 35,411 trades in raw result; summary by crypto symbol | avg_return_pct, net_return_sum_pct, trades, win_rate_pct | `backtest_run_at=2026-05-29T19:48:47.739225+00:00` | C - Non-native / research-only | No | Real result data but explicitly crypto proxy, not US equities 10m. |
| `03_QUANTLENS/05_BACKTEST_RESULTS/QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK/` | Dedicated blocked-result folder | Exact target | `ALL` / `N/A`; config notes requested BTCUSDT etc. | `N/A` | None | `symbol_results.csv`: 1 row; `walk_forward_results.csv`: 3 rows | Status fields only; trades all 0 | Folder notes and CSV status rows | D - Not usable | No | Files explicitly say backtest/walk-forward not run because deterministic rules or compatible data were missing. |
| `03_QUANTLENS/05_BACKTEST_RESULTS/*/scorecard_v2/QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_TRXUSDT_1D.scorecard.json` and related scorecard folders | Scorecard JSON | Exact target plus `TRXUSDT|1D` | TRXUSDT crypto | 1D | None | 30 scorecard files found across scorecard/gate folders | Gate scores, pass/fail, notes, flags | Scorecard fields, gate summaries | C - Non-native / research-only | No | Real scorecards exist, but only for crypto TRXUSDT 1D, not US equities 10m. |
| `03_QUANTLENS/05_BACKTEST_RESULTS/*/evaluation_artifacts/QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK__TRXUSDT__1D.eval.json` and related all-gate folders | Evaluation artifact JSON | Exact target plus `TRXUSDT|1D` | TRXUSDT crypto | 1D | None | 22 eval files found | net_profit_pct, profit_factor, expectancy_r, max_drawdown_pct, trades, OOS, WFO, benchmark, DSR/PBO/CPCV fields | `backtest_run_id`, metric `source_path` fields | C - Non-native / research-only | No | Real enriched evidence exists but for crypto TRXUSDT 1D only. |
| `03_QUANTLENS/05_BACKTEST_RESULTS/MEGA_results_iter_*_results.json`, `MEGA_walk_forward_results.json`, partials, and run folders | MEGA deterministic soak results | Exact target rows present | Crypto symbols only: ADAUSDT, APTUSDT, ARBUSDT, AVAXUSDT, BNBUSDT, BTCUSDT, DOGEUSDT, DOTUSDT, ETHUSDT, LINKUSDT, LTCUSDT, NEARUSDT, OPUSDT, POLUSDT, SOLUSDT, TRXUSDT, XRPUSDT | 15m, 1h, 2h, 4h, 1D | None | 115 MEGA files with target rows; aggregate parser found target rows across 202 result-related files | Lockbox/OOS and fold metrics depending on file | MEGA filenames and embedded metric source paths | C - Non-native / research-only | No | Same strategy id appears, but all inspected symbols/timeframes are crypto proxy buckets; no 10m US equity row found. |
| `03_QUANTLENS/05_BACKTEST_RESULTS/draft_run_plan_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-15/run_plan.json` | Draft run plan | Exact target | Empty symbols; universe status `needs_freeze`, source `unresolved` | `10m` requested | Planned profiles only | `case_count=5000`; no result rows | Plan metadata only | D - Not usable | No | Review/draft-only plan; no executed results and no validated symbol universe. |
| `03_QUANTLENS/_registry/quantlens_candidate_registry.jsonl` and `.csv` | Candidate registry | Exact target | `US_EQUITIES_OPTIONS_UNDERLYING_PRICE` metadata | `10m` metadata | None | No result rows | Candidate metadata, source URL, status | D - Not usable | No | Useful target metadata, not result evidence. CSV also notes batch prototype used crypto and best was BTCUSDT. |
| `05_REGISTRY/TRIAGE_CANDIDATE_REGISTRY.json` | Generated triage registry | Exact target | Strategy metadata only | 10m/source metadata if present | None | No result rows | Registry generated metadata | D - Not usable | No | Registry source, not a backtest/result source. |
| `05_REGISTRY/AI_STRATEGY_NAME_REGISTRY.json` | Display-name registry | Exact target display name `8 EMA Pullback` | None | None | None | No result rows | Generated name metadata | D - Not usable | No | Name metadata only. |
| `05_REGISTRY/AI_QUANTLENS_VERDICT_REGISTRY.json` | AI verdict registry | Exact target | None | None | None | No result rows | Generated AI verdict metadata | D - Not usable | No | Expert/verdict metadata only, not native result evidence. |
| `06_SCHEMAS/backtest_profile_result.schema.json`, `top_results.schema.json`, `run_plan.schema.json` | Schemas | N/A | N/A | N/A | Defines profiles | No result rows | Schema fields only | D - Not usable | No | Contract definitions only; no source result data. |
| `08_DASHBOARD_APP` references and tests | Reader/UI/test code | Target appears in tests; profile terms in UI | Test/mock context | Test/mock context | Test profiles | No real result rows | Test assertions only | D - Not usable | No | Code/tests/UI references are not source validation evidence. |
| `11_TRIAGE/FIRST_PROFILE_RESULT_ARTIFACT_PILOT_REPORT_2026-06-15.md` | Prior audit report | Exact target | XRPUSDT/TRXUSDT/NEARUSDT | 4h, 1D, 1h | `SOURCE_NAKED` | Describes 4 pilot rows | Describes copied metrics and robustness blocks | Prior report text | C - Non-native / research-only | No | Confirms pilot artifact is crypto sourced and `RESEARCH_ONLY`. |
| `11_TRIAGE/RUN_PLAN_BUILDER_AUDIT_2026-06-15.md` and `RUN_PLAN_UI_WIRING_PATCH_REPORT_2026-06-15.md` | Prior audit/report | Exact target | Unresolved; no silent BTCUSDT default after patch | 10m requested | Planned profiles | No result rows | Report/audit text | D - Not usable | No | Confirms the run plan is draft/review-only and unresolved without user-provided symbols. |

Aggregate read-only parser results for `05_BACKTEST_RESULTS`:

- Target rows discovered across result-related files: 16,616.
- Files containing target rows: 202.
- Symbols observed: `ADAUSDT`, `APTUSDT`, `ARBUSDT`, `AVAXUSDT`, `BNBUSDT`, `BTCUSDT`, `DOGEUSDT`, `DOTUSDT`, `ETHUSDT`, `LINKUSDT`, `LTCUSDT`, `NEARUSDT`, `OPUSDT`, `POLUSDT`, `SOLUSDT`, `TRXUSDT`, `XRPUSDT`, plus blocked `ALL`/`N/A` rows.
- Timeframes observed: `15m`, `1h`, `2h`, `4h`, `1D`, `N/A`.
- Profiles observed in actual profile result rows: `SOURCE_NAKED`.
- Native-like rows with `10m` and non-USDT symbols: none.

## 5. Native usable candidates

None found.

No inspected source simultaneously matched:

- exact target or equivalent 8 EMA Pullback strategy,
- US equities universe or equity symbols,
- 10m timeframe,
- real result data,
- usable KPI/provenance fields.

## 6. Partial native candidates

No partial native result source was found.

The closest partial metadata sources are the candidate registry and draft run plan, because they preserve the intended target (`US_EQUITIES...`, `10m`, `8 EMA Pullback`). They are not result sources and contain no native performance rows.

## 7. Non-native / research-only candidates

The real result sources are non-native:

- `backtest_profile_result.json` under `pilot_profile_result_..._2026-06-16` has four `SOURCE_NAKED` rows:
  - XRPUSDT 4h, score 1.1282, net profit 40.407, PF 1.358, trade_count 108, `promotion_status=RESEARCH_ONLY`.
  - TRXUSDT 1D, score 0.2015, net profit 1.976, PF 1.083, trade_count 41, `promotion_status=RESEARCH_ONLY`.
  - TRXUSDT 4h, score 0.6751, net profit 16.078, PF 1.160, trade_count 153, `promotion_status=RESEARCH_ONLY`.
  - NEARUSDT 1h, score 1.6037, net profit 46.012, PF 1.732, trade_count 71, `promotion_status=RESEARCH_ONLY`.
- The May 29 direct result file has 35,411 crypto trades summarized by BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT, ADAUSDT, AVAXUSDT, and DOGEUSDT. Its companion folder states the market/data mismatch.
- Scorecard/evaluation artifacts repeatedly cite `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK|TRXUSDT|1D`, with real KPIs and provenance-style metric source paths, but still crypto 1D evidence.
- MEGA result files contain many exact-target rows across crypto symbols and 15m/1h/2h/4h/1D timeframes only.

These sources are safe as research-only historical evidence, but not safe as native validation evidence and not safe for promotion.

## 8. Not usable candidates

The following are not usable as result sources:

- Dedicated blocked-result folder `03_QUANTLENS/05_BACKTEST_RESULTS/QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK/`:
  - `symbol_results.csv` says `status=NEEDS_MORE_INFO`, `trades=0`, and "Backtest not run; missing deterministic rules or compatible data."
  - `walk_forward_results.csv` says train/validation/oos were not run and `trades=0`.
  - `robustness_summary.md` says the available local bundle is Binance futures data and lacks US equities/options/10m data.
  - `pass_fail_decision.md` repeats the market/data mismatch.
- `draft_run_plan_.../run_plan.json`:
  - Has `strategy_id` exact match and desired profiles/timeframe planning context.
  - Has `symbols=[]` and `universe.status=needs_freeze`.
  - Says no validated symbol universe was found and user-provided symbols are required before approval.
  - It is a draft/review plan, not result evidence.
- Registry files in `03_QUANTLENS/_registry/` and `05_REGISTRY/`:
  - Useful for metadata and naming/verdict context.
  - Not result data.
- Schemas in `06_SCHEMAS/`:
  - Define contracts only.
  - Not source data.
- Dashboard code/tests/UI references:
  - Some tests use the target id to validate builder behavior.
  - Not real validation evidence.
- Prior triage reports:
  - Useful provenance/audit notes.
  - Not primary result sources.

## 9. Evidence gaps

- No native US equity symbol set was found for this strategy.
- No existing 10m US equity result rows were found.
- No `MTC_LIGHT` or `RISK_NORMALIZED` native result rows were found.
- The only `SOURCE_NAKED` profile result rows are crypto/timeframe mismatches and are marked `RESEARCH_ONLY`.
- No result source proves native US equities 10m validation with traceable performance fields.
- Existing draft run-plan metadata says the universe is unresolved and needs user-provided symbols before approval.

## 10. Recommendation

Do not generate a native profile artifact from the existing repo data.

The only real result evidence for the target strategy is crypto/proxy research evidence. It can be referenced as historical research-only context, but it must not be promoted, presented as native validation, or used as a native artifact generation source.

To proceed later, first obtain or define a validated US equities symbol universe, confirm 10m data availability, freeze deterministic rules, and run an approved backtest/validation workflow under the repository gates. That is outside this discovery task and was not performed here.

## 11. Whether artifact generation is allowed next

No.

Artifact generation for this target is not allowed next because no native source was found. Generating a native `backtest_profile_result.json` or `top_results.json` now would either reuse research-only crypto evidence or fabricate a native validation layer that does not exist.

## 12. Safety confirmation

- No code was modified.
- No Pine, parity, MTC_V2, strategy logic, backtest engine logic, broker/live/paper execution logic, or API write behavior was touched.
- No files were staged or committed.
- No files were deleted, reset, moved, or overwritten outside the requested report creation.
- No backtests or optimizations were run.
- No `backtest_profile_result.json` or `top_results.json` was generated.
- Inside the repository, only this report file was created.

ONLY RESEARCH-ONLY SOURCE FOUND - DO NOT PROMOTE
