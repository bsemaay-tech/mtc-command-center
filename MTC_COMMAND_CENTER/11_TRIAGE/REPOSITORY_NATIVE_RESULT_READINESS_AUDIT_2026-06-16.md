# Repository Native Result Readiness Audit - 2026-06-16

## 1. Executive summary

Repository-wide native result readiness is mixed, but no artifact-ready native candidate was found.

Read-only inspection found substantial real result evidence:

- 2,207 `*.scorecard.json` files.
- 1,903 `*.eval.json` evaluation artifacts.
- 45 distinct base strategy IDs with scorecard/evaluation evidence.
- 1 existing `backtest_profile_result.json`.
- 0 existing `top_results.json`.
- 1 draft `run_plan.json`.

The usable result evidence is almost entirely crypto/USDT scorecard and eval evidence. It is useful for future artifact planning only after profile separation, provenance tightening, and promotion-gate decisions. The only profile-separated result artifact is a `SOURCE_NAKED` pilot for `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK`, but its rows are XRPUSDT/TRXUSDT/NEARUSDT at 1h/4h/1D, marked `promotion_status=RESEARCH_ONLY`, and therefore not native US equities 10m evidence.

Final verdict: `MIXED EVIDENCE - USER DECISION REQUIRED`

## 2. Search scope and method

Read-only inspection covered:

- `MTC_COMMAND_CENTER/03_QUANTLENS/`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/`
- `MTC_COMMAND_CENTER/03_QUANTLENS/strategies/`
- `MTC_COMMAND_CENTER/03_QUANTLENS/_registry/`
- `MTC_COMMAND_CENTER/05_REGISTRY/`
- `MTC_COMMAND_CENTER/06_SCHEMAS/`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/`
- `MTC_COMMAND_CENTER/11_TRIAGE/`

Methods:

- Parsed strategy inventory from `05_REGISTRY/STRATEGY_RESEARCH_REGISTRY.json`, `TRIAGE_CANDIDATE_REGISTRY.json`, `AI_STRATEGY_NAME_REGISTRY.json`, and `AI_QUANTLENS_VERDICT_REGISTRY.json`.
- Parsed result evidence from `05_BACKTEST_RESULTS/**/*.scorecard.json`, `**/*.eval.json`, `**/backtest_profile_result.json`, and `**/run_plan.json`.
- Searched for `SOURCE_NAKED`, `MTC_LIGHT`, `RISK_NORMALIZED`, `RESEARCH_ONLY`, `universe_mismatch`, `profile_mapping`, `top_results`, `US_EQUITIES`, `10m`, crypto symbols, and walk-forward/evaluation markers.
- Dispatched the broad scan to `_deepseek_driver/ds_agent.py` first per token discipline. That run was read-only, wrote no repo files, and hit max iterations without a final report, so Codex completed the audit directly.

## 3. Strategy inventory source

The inventory is the union of registry and result identities:

| Source | Count / role |
|---|---:|
| `05_REGISTRY/STRATEGY_RESEARCH_REGISTRY.json` | 63 strategy research entries |
| `05_REGISTRY/TRIAGE_CANDIDATE_REGISTRY.json` | 172 triage candidates |
| `05_REGISTRY/AI_STRATEGY_NAME_REGISTRY.json` | 212 display-name entries |
| `05_REGISTRY/AI_QUANTLENS_VERDICT_REGISTRY.json` | 212 AI verdict entries |
| `05_BACKTEST_RESULTS/**/*.scorecard.json` | 45 distinct base strategy IDs with scorecards |
| Combined distinct strategy IDs seen in this pass | 278 |

Important limitation: several scorecard IDs are generated or result-family IDs (`GEN_*`, `QL_*`) that do not have complete intended-universe metadata. Those were not promoted to artifact-ready; they are classified as partial native candidates at best.

## 4. Bucket counts

| Bucket | Count | Meaning |
|---|---:|---|
| A. Artifact-ready native source | 0 | No strategy has profile-separated or otherwise fully native, promotable, same-universe, same-timeframe evidence ready for artifact planning without a user decision. |
| B. Partial native source | 40 | Real scorecard/eval evidence exists, usually crypto/USDT, but profile separation, universe metadata, top-results packaging, and Gate 3/promotion evidence are incomplete. |
| C. Research-only / proxy source | 5 | Result evidence exists but maps to US-equities/SP500/generalizable strategies through crypto proxy symbols or explicit `RESEARCH_ONLY`. |
| D. Blocked / no usable result source | 233 | Registry/name/verdict metadata only, draft plans only, blocked folders, schemas, UI samples, or no parsed result rows. |
| E. Needs manual inspection | 0 | No separate E bucket was needed; ambiguous usable cases were conservatively kept in B or C. |

Direct answers:

1. Artifact-ready native source: 0.
2. Partial native source: 40.
3. Research-only/proxy source: 5.
4. No usable source: 233.
5. Closest to artifact generation: high-score B candidates with scorecards/eval artifacts, listed in section 6 and section 12.
6. Should not be promoted: all C candidates and all B candidates until profile/result artifacts and promotion gates are satisfied.
7. Need new backtest plans: all C candidates needing native universe/timeframe proof, plus D candidates that are still metadata-only.
8. Existing `MTC_LIGHT` evidence: no real result artifact found.
9. Existing `RISK_NORMALIZED` evidence: no real result artifact found.
10. Most existing results crypto/proxy: yes, all parsed scorecard symbols are USDT crypto pairs.
11. True US equities 10m results: none found.
12. Next practical step: choose one high-confidence partial crypto candidate or define/freeze the US-equities universe, then generate approved profile-separated artifacts only from real matching source evidence.

## 5. Artifact-ready native candidates

None.

No inspected strategy simultaneously had:

- real result rows,
- matching intended universe,
- matching intended timeframe or equivalent,
- usable KPI/provenance fields,
- no `RESEARCH_ONLY` / `universe_mismatch` flag,
- and enough profile/result packaging to be safe for artifact planning without a user decision.

## 6. Partial native candidates

These are the strongest candidates for future artifact planning, but they are not artifact-ready. They have real scorecards/eval artifacts and KPI fields, yet no official profile-separated `backtest_profile_result.json`, no `top_results.json`, and no promotable Gate 3 state.

| strategy_id | display name | intended universe | intended timeframe | best available evidence path | evidence type | observed symbols/universe | observed timeframe | profile/source type | rows/trades/cases | KPIs present | promotion_status | classification | reason | next action |
|---|---|---|---|---|---|---|---|---|---:|---|---|---|---|---|
| `GEN_RSI_OVERSOLD_REVERSAL` | RSI Oversold Reversal | unknown/crypto result family | unknown | `03_QUANTLENS/05_BACKTEST_RESULTS/worst_window_2026-06-05_283d198/scorecards/GEN_RSI_OVERSOLD_REVERSAL_ETHUSDT_2h.scorecard.json` | scorecard/eval | TRXUSDT, ETHUSDT, LINKUSDT | 1h/2h/4h | legacy scorecard, no profile | 155 scorecards / 115 evals | net profit, PF, DD, Sharpe, Sortino, trades, CPCV/PBO/DSR | none/promotable false | B | Strong KPI evidence, but no profile artifact or full native provenance package. | Build profile-separated artifact only after same-bucket source/provenance review. |
| `GEN_DONCHIAN_BREAKOUT` | Donchian Breakout | unknown/crypto result family | unknown | `03_QUANTLENS/05_BACKTEST_RESULTS/worst_window_2026-06-05_283d198/scorecards/GEN_DONCHIAN_BREAKOUT_BTCUSDT_4h.scorecard.json` | scorecard/eval | TRXUSDT, SOLUSDT, BTCUSDT | 15m/1h/4h | legacy scorecard, no profile | 123 scorecards / 91 evals | net profit, PF, DD, Sharpe, trades, CPCV/PBO/DSR | none/promotable false | B | Real evidence, but no profile separation or top-results artifact. | Candidate for artifact pilot after profile mapping. |
| `GEN_KELTNER_BREAKOUT` | Keltner Breakout | unknown/crypto result family | unknown | `03_QUANTLENS/05_BACKTEST_RESULTS/worst_window_2026-06-05_283d198/scorecards/GEN_KELTNER_BREAKOUT_ADAUSDT_15m.scorecard.json` | scorecard/eval | TRXUSDT, ADAUSDT, LINKUSDT | 15m/1h/4h | legacy scorecard, no profile | 120 scorecards / 88 evals | net profit, PF, DD, Sharpe, trades, CPCV/PBO/DSR | none/promotable false | B | High score exists but source profile is not explicit. | Profile-result conversion review. |
| `QL_QTREND_V1_ALL_SIGNALS` | QTrend V1 All Signals | crypto result family | unknown | `03_QUANTLENS/05_BACKTEST_RESULTS/night_3M_2026-06-08/iter_09/gate2_scorecards/QL_QTREND_V1_ALL_SIGNALS_ETHUSDT_4h.scorecard.json` | scorecard/eval | TRXUSDT, ETHUSDT, LTCUSDT | 15m/1h/2h/4h | legacy scorecard, no profile | 84 scorecards / 84 evals | net profit, PF, DD, Sharpe, trades, CPCV/PBO/DSR | none/promotable false | B | Real night-run evidence, but still legacy scorecard packaging. | Build SOURCE_NAKED candidate only after same-profile checks. |
| `QL_QTREND_V1_SHORT` | QTrend V1 Short | crypto result family | unknown | `03_QUANTLENS/05_BACKTEST_RESULTS/night_3M_2026-06-08/iter_09/gate2_scorecards/QL_QTREND_V1_SHORT_ADAUSDT_1h.scorecard.json` | scorecard/eval | OPUSDT, ADAUSDT, APTUSDT, ARBUSDT, AVAXUSDT | 1h/2h/4h | legacy scorecard, no profile | 112 scorecards / 112 evals | net profit, PF, DD, Sharpe, trades, CPCV/PBO/DSR | none/promotable false | B | Good scorecard coverage, no profile artifact. | Same-bucket artifact pilot candidate. |
| `QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE` | Support Engulfing Candle | any/general | review_needed | `03_QUANTLENS/05_BACKTEST_RESULTS/worst_window_2026-06-05_283d198/scorecards/QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE_ETHUSDT_2h.scorecard.json` | scorecard/eval | SOLUSDT, ETHUSDT, NEARUSDT | 1h/2h/4h | legacy scorecard, no profile | 122 scorecards / 90 evals | net profit, PF, DD, Sharpe, trades, CPCV/PBO/DSR | none/promotable false | B | Broad "ANY" strategy with crypto result evidence; native universe is not frozen. | Decide target universe before artifact work. |
| `QL_SLINGSHOT_v1` | Slingshot | crypto result family | unknown | `03_QUANTLENS/05_BACKTEST_RESULTS/night_3M_2026-06-08/iter_09/gate2_scorecards/QL_SLINGSHOT_v1_ARBUSDT_2h.scorecard.json` | scorecard/eval | TRXUSDT, ARBUSDT, BTCUSDT, ETHUSDT, LTCUSDT | 1h/2h/4h | legacy scorecard, no profile | 77 scorecards / 77 evals | net profit, PF, DD, Sharpe, trades, CPCV/PBO/DSR | none/promotable false | B | Real evidence but profile/top-results missing. | Candidate after profile conversion review. |
| `QL_FAM_MOMENTUM_CONTINUATION` | Family Momentum Continuation | crypto result family | unknown | `03_QUANTLENS/05_BACKTEST_RESULTS/night_3M_2026-06-08/iter_09/gate2_scorecards/QL_FAM_MOMENTUM_CONTINUATION_BTCUSDT_4h.scorecard.json` | scorecard/eval | TRXUSDT, BTCUSDT, LINKUSDT | 15m/1h/4h | legacy scorecard, no profile | 70 scorecards / 70 evals | net profit, PF, DD, Sharpe, trades, CPCV/PBO/DSR | none/promotable false | B | Existing MCC readiness history but no promotion artifact. | Keep as partial until profile artifact exists. |
| `QL_DEEPAK_153_FILTER_1D` | Deepak 153 Filter | crypto result family | 1D label, tested 2h/4h | `03_QUANTLENS/05_BACKTEST_RESULTS/night_3M_2026-06-08/iter_09/gate2_scorecards/QL_DEEPAK_153_FILTER_1D_BNBUSDT_4h.scorecard.json` | scorecard/eval | BNBUSDT, BTCUSDT, SOLUSDT, TRXUSDT | 2h/4h | legacy scorecard, no profile | 56 scorecards / 56 evals | net profit, PF, DD, Sharpe, trades, CPCV/PBO/DSR | none/promotable false | B | Timeframe label and observed timeframe need reconciliation. | Manual profile/timeframe mapping before artifact. |
| `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY` | Deepak Snapback 50SMA Intraday | crypto result family | intraday | `03_QUANTLENS/05_BACKTEST_RESULTS/night_3M_2026-06-08/iter_09/gate2_scorecards/QL_DEEPAK_SNAPBACK_50SMA_INTRADAY_LTCUSDT_1h.scorecard.json` | scorecard/eval | TRXUSDT, LTCUSDT | 1h/2h/4h | legacy scorecard, no profile | 56 scorecards / 56 evals | net profit, PF, DD, Sharpe, trades, CPCV/PBO/DSR | none/promotable false | B | Real intraday-style evidence, not profile-separated. | Candidate after source/profile decision. |

Additional B candidates with real scorecard/eval evidence include `QL_CRABEL_RANGE_EXP_v1`, `QL_BIGBELUGA_RSI_v1`, `QL_HIGHEST_VOLUME_EDGE_PROSWING_1D`, `QL_FAM_CONSOLIDATION_BREAKOUT`, `QL_RS_PHASE_DAYS_PROSWING_OVERLAY`, `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M`, `QL_LINDA_5SMA_v1`, `GEN_ATR_PULLBACK_TREND`, `GEN_ZSCORE_MEAN_REVERSION`, `QL_VWAP_TREND_CONT_v1`, `GEN_STOCH_OVERSOLD_CROSS`, and `QL_ANTI_CHASE_CRABEL_v1`.

## 7. Research-only / proxy candidates

These have result evidence, but it is not native for the strategy's intended universe/timeframe.

| strategy_id | display name | intended universe | intended timeframe | best available evidence path | evidence type | observed symbols/universe | observed timeframe | profile/source type | rows/trades/cases | KPIs present | promotion_status | classification | reason | next action |
|---|---|---|---|---|---|---|---|---|---:|---|---|---|---|---|
| `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK` | 8 EMA Pullback | US equities/options underlying price | 10m | `03_QUANTLENS/05_BACKTEST_RESULTS/pilot_profile_result_QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-16/backtest_profile_result.json` | profile result + scorecards | XRPUSDT, TRXUSDT, NEARUSDT | 1h/4h/1D | `SOURCE_NAKED` | 4 profile rows; 30 scorecards; 22 evals | net profit, PF, DD, win rate, trades, Sharpe, DSR/FDR | `RESEARCH_ONLY` | C | Exact strategy ID but crypto/timeframe mismatch and explicit research-only status. | Do not promote; freeze US-equities universe and run approved native plan later. |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL` | 8 EMA Pullback + Trailing Exit | US equities/options underlying price | intraday | `03_QUANTLENS/05_BACKTEST_RESULTS/worst_window_2026-06-05_283d198/scorecards/QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL_LINKUSDT_1h.scorecard.json` | scorecard/eval | LINKUSDT, ETHUSDT, NEARUSDT, SOLUSDT | 1h/2h | legacy scorecard, no profile | 34 scorecards / 26 evals | net profit, PF, DD, Sharpe, trades | none/promotable false | C | Intended equity/intraday idea tested only on crypto symbols. | New native US-equities plan required. |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_LE_MODEL_BULL_FLAG` | Bull Flag Breakout | US equities/options underlying price | intraday | `03_QUANTLENS/05_BACKTEST_RESULTS/worst_window_2026-06-05_283d198/scorecards/QL_2026-05-01_US_EQUITIES_INTRADAY_LE_MODEL_BULL_FLAG_TRXUSDT_1D.scorecard.json` | scorecard/eval | TRXUSDT | 1D | legacy scorecard, no profile | 30 scorecards / 22 evals | net profit, PF, DD, Sharpe, trades | none/promotable false | C | Equity/intraday label with crypto 1D evidence. | Do not promote; native plan needed. |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_PURPLE_PROFITS` | 8 EMA Trend (Purple Profits) | US equities/options underlying price | intraday | `03_QUANTLENS/05_BACKTEST_RESULTS/worst_window_2026-06-05_283d198/scorecards/QL_2026-05-01_US_EQUITIES_INTRADAY_PURPLE_PROFITS_TRXUSDT_1D.scorecard.json` | scorecard/eval | TRXUSDT | 1D | legacy scorecard, no profile | 30 scorecards / 22 evals | net profit, PF, DD, Sharpe, trades | none/promotable false | C | Equity/intraday label with crypto 1D evidence. | Do not promote; native plan needed. |
| `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR` | Two-Candle Support/Resistance Breakout | SP500/generalizable index example | 5m/review_needed | `03_QUANTLENS/05_BACKTEST_RESULTS/worst_window_2026-06-05_283d198/scorecards/QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR_ARBUSDT_15m.scorecard.json` | scorecard/eval | TRXUSDT, ARBUSDT, ETHUSDT | 15m/2h | legacy scorecard, no profile | 62 scorecards / 46 evals | net profit, PF, DD, Sharpe, trades | none/promotable false | C | SP500/5m idea tested on crypto/timeframe proxy. | New SP500/native-symbol plan required. |

## 8. Blocked / no usable source candidates

There are 233 strategies/candidates with no usable result evidence in this pass. These are registry-only, name/verdict-only, source-intake-only, draft-only, blocked, schema, UI sample, or otherwise non-result records.

Top blocked/no-source examples:

| strategy_id | display name | current evidence | reason | next action |
|---|---|---|---|---|
| `STG004` | AVWAP Brian Earnings Anchor | strategy registry only | `review_needed`, no parsed scorecard/eval/profile result | Complete deterministic spec/source mapping before any result plan. |
| `STG005` | AVWAP Brian Gap Reclaim | strategy registry only | `review_needed`, no parsed result evidence | Same. |
| `STG007` | Stage2 EMA/MA threshold candidate | registry/spec context | threshold still requires human definition | Baris decision before backtest. |
| `STG021` | VCP contraction candidate | registry/spec context | contraction threshold unresolved | Baris decision before backtest. |
| `STG027` | RSI divergence / CHoCH candidate | registry/spec context | divergence/zone geometry unresolved | Baris decision before backtest. |
| `STG037` | 7-candle pattern | registry/spec context | geometry unresolved | Baris decision before backtest. |
| `STG054` | Fishhook | registry/spec context | depth/speed threshold unresolved | Baris decision before backtest. |
| `STG058` | Parabolic SAR champion filter | registry/spec context | parameters unresolved | Baris decision before backtest. |
| `STG061` | Pierpont extension | registry/spec context | thresholds unresolved | Baris decision before backtest. |
| `STG062` | Weinstein Stage 2 | registry/spec context | MA slope/volume thresholds unresolved | Baris decision before backtest. |
| `STG063` | Tito RS | registry/spec context | RS threshold/crossback unresolved | Baris decision before backtest. |
| `QLR_*` source review entries | many source-intake records | name/verdict/source metadata only | no parsed scorecard/eval/profile result | Triage into codable strategy before result planning. |
| `draft_run_plan_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-15` | draft plan | `run_plan.json`/`run_plan.md` only | universe has `status=needs_freeze`, symbols empty | Provide/freeze symbols before approval; not result evidence. |

## 9. Needs manual inspection

No strategy was left in a separate E bucket.

Manual decisions are still required before promoting any B candidate:

- whether a crypto/USDT result is native for that strategy family,
- whether a legacy scorecard can be mapped to `SOURCE_NAKED`,
- whether profile conversion is acceptable,
- whether Gate 3/paper/live readiness blockers should stay incomplete,
- and whether same-profile/same-timeframe comparisons are valid.

## 10. Existing `SOURCE_NAKED` / `MTC_LIGHT` / `RISK_NORMALIZED` evidence

`SOURCE_NAKED`:

- One real profile-result file exists:
  - `03_QUANTLENS/05_BACKTEST_RESULTS/pilot_profile_result_QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-16/backtest_profile_result.json`
- It has 4 rows.
- All rows are for crypto symbols/timeframes: XRPUSDT 4h, TRXUSDT 1D, TRXUSDT 4h, NEARUSDT 1h.
- All rows have `promotion_status=RESEARCH_ONLY`.
- This is not native US equities 10m evidence.

`MTC_LIGHT`:

- No real `MTC_LIGHT` result row or `backtest_profile_result.json` row was found.
- References exist in schemas, UI labels, tests, and reports only.

`RISK_NORMALIZED`:

- No real `RISK_NORMALIZED` result row or `backtest_profile_result.json` row was found.
- References exist in schemas, UI labels, tests, and reports only.

`top_results.json`:

- No `top_results.json` file exists under `05_BACKTEST_RESULTS`.

## 11. US equities 10m availability

No true US equities 10m result source was found.

Evidence:

- The exact 8 EMA Pullback profile artifact is crypto only and marked `RESEARCH_ONLY`.
- The draft run plan for the same target requests 10m but has `symbols=[]` and `universe.status=needs_freeze`.
- Scorecards for US-equities-labeled strategies are LINKUSDT/TRXUSDT/other USDT crypto pairs, not US equity symbols.
- Parsed scorecard symbol distribution is 100 percent USDT crypto pairs: TRXUSDT, ETHUSDT, SOLUSDT, LINKUSDT, DOGEUSDT, BTCUSDT, BNBUSDT, ARBUSDT, LTCUSDT, DOTUSDT, ADAUSDT, OPUSDT, NEARUSDT, APTUSDT, AVAXUSDT, XRPUSDT.
- Parsed scorecard timeframes are 4h, 1h, 2h, 15m, and 1D. No 10m scorecard result row was found.

## 12. Top 10 next-action candidates

These are the most practical next candidates if the goal is to produce a real profile-separated artifact from existing evidence. They are not promotable now.

| Rank | Candidate | Why next | Required next action |
|---:|---|---|---|
| 1 | `GEN_RSI_OVERSOLD_REVERSAL` | Largest scorecard/eval coverage and high scores | Verify source intent, choose same-profile rows, build SOURCE_NAKED pilot only if provenance checks pass. |
| 2 | `QL_QTREND_V1_ALL_SIGNALS` | Strong night-run scorecards across crypto symbols/timeframes | Same-bucket profile mapping review. |
| 3 | `QL_QTREND_V1_SHORT` | Broad current night-run evidence | Same-bucket profile mapping review. |
| 4 | `GEN_KELTNER_BREAKOUT` | High 15m/1h/4h crypto evidence | Confirm native universe and profile. |
| 5 | `GEN_DONCHIAN_BREAKOUT` | High scorecards/evals and common breakout family | Confirm source profile and benchmark requirements. |
| 6 | `QL_SLINGSHOT_v1` | Clean scorecard/eval package from night runs | Profile conversion review. |
| 7 | `QL_FAM_MOMENTUM_CONTINUATION` | Existing readiness history and repeated scorecards | Keep Gate 3 blocker explicit; profile conversion only. |
| 8 | `QL_DEEPAK_153_FILTER_1D` | Strong crypto scorecard evidence | Reconcile 1D label vs observed 2h/4h evidence. |
| 9 | `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY` | Intraday-style crypto evidence | Confirm profile/timeframe target. |
| 10 | `QL_ANTI_CHASE_CRABEL_v1` | Multiple timeframe TRXUSDT evidence | Profile mapping and robustness review. |

## 13. Strategies not to promote

Do not promote:

- `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK`
- `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL`
- `QL_2026-05-01_US_EQUITIES_INTRADAY_LE_MODEL_BULL_FLAG`
- `QL_2026-05-01_US_EQUITIES_INTRADAY_PURPLE_PROFITS`
- `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR`

Reason: these are equity/SP500-labeled strategies with crypto proxy evidence. The first also has explicit `RESEARCH_ONLY` rows in the only profile artifact.

Also do not promote any B candidate solely from legacy scorecards. Across all parsed scorecards, `promotable=true` was found 0 times and Gate 3 OK was found 0 times in the parsed status fields.

## 14. Evidence gaps

- No native US equities 10m result rows.
- No real `MTC_LIGHT` result artifact.
- No real `RISK_NORMALIZED` result artifact.
- No `top_results.json`.
- Only one `backtest_profile_result.json`, and it is research-only crypto proxy.
- Legacy scorecards lack official profile separation.
- Many generated/registry IDs lack complete intended-universe metadata.
- Gate 3/promotion evidence remains incomplete for scorecard candidates.
- Draft run plans are not result evidence and must not be promoted.

## 15. Recommendation

Do not generate native artifacts for US-equities strategies from the current repository evidence.

Recommended next practical step:

1. Pick one of the high-coverage B candidates if the goal is to prove the artifact pipeline from existing crypto evidence.
2. Otherwise, for US equities, freeze the target symbol universe and timeframe first, then create a new approved backtest plan. The current repo does not contain true US equities 10m results.
3. Keep all C candidates explicitly research-only/proxy.
4. Do not generate `top_results.json` until a real same-profile, same-universe, same-timeframe result set exists.
5. Do not treat schema/UI labels as evidence for `MTC_LIGHT` or `RISK_NORMALIZED`.

## 16. Safety confirmation

- No code was modified.
- No Pine files were touched.
- No MTC_V2 files were touched.
- No parity files were touched.
- No trading, strategy, broker, live, paper, backtest engine, optimizer, or API write behavior was changed.
- No backtest command was run.
- No optimizer command was run.
- No `backtest_profile_result.json` was generated.
- No `top_results.json` was generated.
- No files were staged or committed.
- The DeepSeek dispatch wrote no repository files.
- The only repository file created by this task is this report.

Final verdict: `MIXED EVIDENCE - USER DECISION REQUIRED`
