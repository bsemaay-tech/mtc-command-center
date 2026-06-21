# Run-Plan UI Wiring + Builder Safety Patch — 2026-06-15

Targeted follow-up after the run-plan builder audit. Read-only. No backtests run, no
profile-separated result artifacts generated, no Pine / MTC_V2 / engine / broker /
write-API touched.

## 1. Files changed
- `03_QUANTLENS/tools/build_run_plan.py` — symbol-default fix + `universe` state + md note.
- `06_SCHEMAS/run_plan.schema.json` — tightened safety contract.
- `08_DASHBOARD_APP/apps/web/app.js` — Strategy Intelligence §4 wired to `night_artifacts.run_plans`; Result Explorer "Required Result Artifacts" panel reads real states; new accessor `runPlanForStrategy()` + helper `artifactStateBadge()`.
- `08_DASHBOARD_APP/apps/web/styles.css` — `.a-state.ok/.warn/.bad` + `.plain-list`.
- `08_DASHBOARD_APP/apps/web/index.html` — cache bump `app.js?v=4 → v=5`.
- `08_DASHBOARD_APP/apps/api/tests/test_build_run_plan.py` — +5 tests (symbol default, explicit symbols, schema safety fields).
- `08_DASHBOARD_APP/apps/api/tests/test_night_artifacts_reader.py` — run_plan fixture updated to new safety contract.
- Regenerated artifacts (see #4).

## 2. Builder changes
- **No silent symbol default.** Removed the `["BTCUSDT"]` fallback. Resolution order: `--symbols` → registry `symbols`/`symbol` metadata → **unresolved** (empty). For `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK` (no validated symbol in registry) the universe is now left explicitly unresolved instead of defaulting to a crypto pair.
- New `universe` block: `{status, source, reason}`. Empty universe → `status:"needs_freeze"`, `reason:"No validated symbol universe found in registry/source metadata. Provide --symbols before approval."`; provided/resolved → `status:"draft"` with source (`cli`/`registry`).
- `missing_assumptions` gains `"symbol universe unresolved (needs_freeze)"` when symbols empty.
- `run_plan.md` shows universe state and, when unresolved, a bold line: *"Symbol universe is unresolved and must be frozen before execution approval."* No default symbol injected.
- Console `[WARN]` emitted when universe unresolved.

## 3. Schema changes (`run_plan.schema.json`)
- `required` now: `run_id, read_only, no_execution, status, strategy_ids, profiles, approval, expected_artifacts`.
- Enforced (via `enum`, validator-compatible): `read_only=true`, `no_execution=true`, `approval.human_review_required=true`, `approval.approved=false`, `approval.execution_allowed=false`.
- `approval` object required `[human_review_required, approved, execution_allowed]`.
- Added `universe` property (`status` enum `draft|needs_freeze|frozen`). Unresolved universe (`symbols: []`) remains valid — explicit, not blocked.

## 4. Regenerated artifact path
`03_QUANTLENS/05_BACKTEST_RESULTS/draft_run_plan_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-15/`
- `run_plan.json` (schema-valid; `symbols: []`, `universe.status: needs_freeze`)
- `artifact_index.json` (schema-valid)
- `run_plan.md` (universe-unresolved note)

Command: `python 03_QUANTLENS/tools/build_run_plan.py --strategy-id QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK` (dry-run validated first).

## 5. UI pages fixed
- **Strategy Intelligence → §4 Backtest Plan & Evidence** — when a usable run plan exists for the selected strategy, shows real metadata: run_id, plan status, approval state + `human_review_required` / `approved` / `execution_allowed`, case count, universe/symbols (or unresolved reason), timeframes, parameter-space state, output_dir, expected artifacts, and rule-freeze/missing assumptions. Profiles row marks "Selected in run_plan". No run plan → previous missing state retained. No fake KPIs.
- **Backtest Result Explorer → Required Result Artifacts** — reads actual `night_artifacts` states: `run_plan.json` and `artifact_index.json` → **Present / usable**; `backtest_profile_result.json` / `top_results.json` → **Missing**; untracked contract files (result/metrics/equity/drawdown/trade_list) → **Missing**. Official profile buckets remain empty; legacy rows stay quarantined under "Legacy Scorecard Reference — profile missing".

## 6. Snapshot evidence (`/api/snapshot?refresh=1`)
- `night_artifacts.summary`: expected_types 14, present_types 4, **usable 2**, invalid 0, **profile_result_rows 0**.
- `run_plans[0]`: state **usable**, `data.symbols: []`, `data.universe.status: needs_freeze`, `data.approval.execution_allowed: false`.
- `artifact_index[0]`: state **usable**.

## 7. Test results
- `node --check app.js` → **JS_OK**.
- API suite → **Ran 55 tests … OK** (+5 builder safety tests; reader fixture updated to new contract).
- Generated `run_plan.json` + `artifact_index.json` → schema-valid (in-tool + reader).
- `/healthz` → `read_only:true`, `overall_ok:true`.
- `POST /api/snapshot` → **405**.

## 8. Safety confirmation
No Pine / MTC_V2 / backtest-engine / broker / live / paper execution code touched. No
backtest executed. No write API added. No KPIs faked. No profile-separated result
artifacts generated (`profile_result_rows = 0`, official buckets empty). Plan remains
`read_only=true`, `no_execution=true`, `approval.execution_allowed=false`. Schema now
*enforces* these so a plan that flips them fails validation and the reader marks it
invalid/incomplete.

## 9. Remaining limitations
- Symbol universe for the US_EQUITIES strategy is unresolved (`needs_freeze`); must be frozen via `--symbols` or validated registry metadata before any approval.
- `parameter_space` still `needs_freeze` (no fabricated numeric sweeps); case_count is an estimate over resolved dims only.
- Official Result Explorer buckets + KPIs stay empty until a real `backtest_profile_result.json` / `top_results.json` exists — must come from outside the read-only app.
- Snapshot cached (30s TTL); use `?refresh=1` to surface freshly written plans.

## 10. Recommended next phase
Produce a real, schema-valid `backtest_profile_result.json` (+ `top_results.json`) for one
profile/timeframe from a writer **outside** the read-only app, so official buckets,
leaderboard validated panel, and SI §5 populate from real profile-separated evidence —
then wire interactive Result Explorer filters to those fields.
