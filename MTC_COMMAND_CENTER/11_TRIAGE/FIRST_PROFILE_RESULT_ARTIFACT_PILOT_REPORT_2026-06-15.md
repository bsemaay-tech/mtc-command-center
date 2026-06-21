# First Profile-Separated Result Artifact Pilot — Report — 2026-06-15

## 1. Executive verdict
**Option A — artifact created from real existing source data.** A real deterministic-soak
result file (`MEGA_results_iter_1_20260601_054633_results.json`) contains genuine
lockbox-OOS metrics for the pilot strategy `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK`.
A read-only converter re-shaped its PASS-classified rows into one schema-valid
`backtest_profile_result.json`. **No backtest run, no optimization, no fabricated KPIs.**
Provenance, universe mismatch, and non-robust status are all surfaced explicitly. Reader
discovered it; official SOURCE_NAKED bucket now populates with `profile_result_rows = 4`.

## 2. Preflight worktree scope
`git status --short` / `git diff --stat`: tree dirty from prior accepted phases (dashboard
`app.js`/`index.html`/`styles.css`, `read_model.py`, `_AI_MEMORY/*`, prototype renames) plus
unrelated untracked noise (`../HERMES/`, `Temp/`, transcript collectors, screenshots).
Nothing cleaned/deleted/reset/staged/committed. This task added only NEW files
(converter, test, pilot artifact dir, this report) — cleanly isolable. Intended touch scope
declared up front: converter tool + test + report + one pilot artifact directory.

## 3. Source result files inspected
- `03_QUANTLENS/05_BACKTEST_RESULTS/` — many `MEGA_results_iter_*_results.json` (deterministic soak output), the draft run-plan dir, `FOCUSED_VALIDATION_2026-05-31/`, `FORWARD_PAPER_QUEUE.md`, `CLAUDE_AUDIT_FINDINGS.md`.
- `04_REPORTS/` — subdirs (backtests, optimization, quantlens, parity, …).
- Inspected MEGA structure: `{generated_utc, runtime_seconds, workers, config, results[]}`; each result row has `strategy, symbol, timeframe, classification, summary{best_params, fold_*; lockbox_oos{num_trades, win_rate, net_return_pct, max_drawdown_pct, profit_factor, sharpe, ...}}, dsr_p_value, dsr_robust, bh_fdr_survivor, robust_final`.

## 4. Candidate source classification
| Source | Class | Notes |
|---|---|---|
| `MEGA_results_iter_*_results.json` | **A — real structured result source** | Real lockbox-OOS KPIs, params, date range, cost model; pilot strategy present (85 rows in one file, 4 PASS). Used. |
| draft `run_plan.json` (pilot) | run plan only | Universe `needs_freeze`, symbols `[]`; no results. Not a result source. |
| scorecard cards (snapshot) | C — legacy scorecard rows | Gate heuristic scores, no profile-separated KPIs. Quarantined, not used. |
| `04_REPORTS/*` morning/summary | B — reports, limited structured KPI | Narrative; not used for the artifact. |
| (none found) | D — demo/mock | None used. |

## 5. Selected pilot strategy / run / profile
- **strategy_id:** `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK` (exact match in source).
- **source:** `03_QUANTLENS/05_BACKTEST_RESULTS/MEGA_results_iter_1_20260601_054633_results.json`.
- **profile:** `SOURCE_NAKED` (mapping decision — soak ran raw source rules + param sweep, no MTC risk normalization; recorded as `profile_mapping.is_interpretation = true`).
- **rows:** 4 PASS-classified (XRPUSDT/4h, TRXUSDT/1D, TRXUSDT/4h, NEARUSDT/1h).

## 6. Was real source data sufficient?
Yes for metrics; **with an important honesty caveat.** Real KPIs exist
(net_profit, profit_factor, max_drawdown, win_rate, trade_count, sharpe). BUT the soak
universe is **crypto** (XRP/TRX/NEAR USDT) at 4h/1D/1h — the strategy id implies US
equities at ~10m. This **universe mismatch** is recorded per-row in
`provenance.universe_mismatch`, and every row is `robust_final = false` →
`promotion_status = RESEARCH_ONLY`. The artifact is honest research evidence of the
strategy logic on a non-native universe, not a native-universe validation claim.

## 7. Files changed
- **New:** `03_QUANTLENS/tools/build_profile_result_artifact.py` (read-only converter).
- **New:** `08_DASHBOARD_APP/apps/api/tests/test_build_profile_result_artifact.py` (8 tests).
- **New artifact:** `03_QUANTLENS/05_BACKTEST_RESULTS/pilot_profile_result_QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-16/backtest_profile_result.json`.
- **New:** this report; `_AI_MEMORY/{SESSION_LOG,NEXT_STEPS,ACTIVE_FILES}.md` updated.
- No changes to API server, schemas, Pine, MTC_V2, engine, or UI code (reader already consumes the contract).

## 8. Artifacts created
- `backtest_profile_result.json` — 1 file, 4 result rows, profile SOURCE_NAKED, run_id `profileresult_MEGA_results_iter_1_20260601_054633_results`. Each row carries metrics (copied 1:1), robustness block (dsr/fdr/robust_final/folds), artifacts/source pointer, promotion_status RESEARCH_ONLY, and per-row provenance.
- `top_results.json` — **NOT created** (deliberate). The 4 rows are each a distinct symbol+timeframe bucket; no valid same-bucket multi-row comparison exists, so emitting top_results would violate same-bucket rules. Documented skip.

## 9. Schema validation result
Validated against `06_SCHEMAS/backtest_profile_result.schema.json` in-tool (`schema valid: YES`) and again by the reader (`profile_result_files[0].state = usable`). Unit test `test_output_is_schema_valid` passes.

## 10. Reader / snapshot result (`/api/snapshot?refresh=1`)
- `night_artifacts.summary.profile_result_rows = 4`, `has_profile_separated_results = true`, `usable = 3`, `invalid = 0`.
- `profile_results[*]`: profile SOURCE_NAKED, strategy_id = pilot, real metrics (e.g. XRPUSDT/4h net 40.407%, PF 1.358), promotion RESEARCH_ONLY.
- `profile_result_files[0].state = usable`.

## 11. Dashboard pages affected (read-only, already wired)
- **Result Explorer** — official SOURCE_NAKED bucket now populates from `profile_results`; legacy scorecard rows remain quarantined under "Legacy Scorecard Reference".
- **Strategy Intelligence §5** — profile result preview reads the same `profile_results` (best row for the strategy).
- **Leaderboard / Diagnostics / Advanced Artifacts** — contract counts reflect 1 profile-result file usable.
- No UI redesign; no code change needed.

## 12. Tests run
- `node --check app.js` → JS_OK.
- API suite → **Ran 68 tests … OK** (+8 new converter tests: dry-run no-write, refuses insufficient source, refuses unknown strategy, schema-valid output, provenance preserved, no fake KPIs when absent, non-robot→RESEARCH_ONLY, reader discovers+populates official bucket).
- `/api/snapshot?refresh=1` → 200; `POST /api/snapshot` → 405; `/healthz` → 200.

## 13. Safety confirmation
No backtest, no optimization, no fake KPIs, no fabricated profit/dd/winrate/trade values
(absent metrics = explicit null). No Pine / MTC_V2 / backtest engine / broker / live / paper
execution touched. No POST/PUT/PATCH/DELETE behavior added. No strategy logic modified. No
guessed values. Converter refuses (rc 4) when rows lack real lockbox metrics or strategy id
absent. Universe mismatch and non-robust status surfaced, not hidden.

## 14. If stopped
Not stopped — Option A completed. (Had the only sources been legacy scorecard rows or
demo data, or had KPIs needed guessing, the converter would have refused and this would be
Option B.)

## 15. Recommended next phase
- Product decision: should the pilot's official-bucket row be visually flagged in the UI as `universe_mismatch` / RESEARCH_ONLY (badge) so it is never misread as native-universe validation? (Currently honest in data + promotion_status; a UI badge would harden it.)
- If/when a native US-equities 10m soak exists, regenerate the artifact from that source for a clean-universe pilot.
- Consider a `top_results.json` only once multiple rows share an identical profile+symbol+timeframe+score_method bucket.
- Keep the converter as the single sanctioned path; never hand-author profile results.
