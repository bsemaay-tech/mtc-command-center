# RUN_PLAN_UI_WIRING_PATCH Audit - 2026-06-15

## 1. Executive verdict

Verdict: ACCEPT WITH SMALL FOLLOW-UP

The functional and safety objectives pass: the builder no longer injects a silent BTCUSDT fallback, explicit `--symbols` works, the regenerated draft run plan is review-only with unresolved symbols marked `needs_freeze`, the schema rejects flipped safety fields, the reader surfaces usable run-plan/artifact-index records only, official profile buckets remain empty, no fake KPI rows were generated, and API write methods remain blocked.

Small follow-up: the current worktree is not clean and contains unrelated modified/untracked files outside the reported targeted patch scope. Commit/stage/isolate the intended patch set before treating scope-control objective 14 as fully satisfied.

## 2. Files inspected

- `03_QUANTLENS/tools/build_run_plan.py`
- `06_SCHEMAS/run_plan.schema.json`
- `08_DASHBOARD_APP/apps/api/mcc_readonly/night_artifacts_reader.py`
- `08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py`
- `08_DASHBOARD_APP/apps/api/mcc_readonly/server.py`
- `08_DASHBOARD_APP/apps/api/tests/test_build_run_plan.py`
- `08_DASHBOARD_APP/apps/api/tests/test_night_artifacts_reader.py`
- `08_DASHBOARD_APP/apps/api/tests/test_readonly_core.py`
- `08_DASHBOARD_APP/apps/web/app.js`
- `03_QUANTLENS/05_BACKTEST_RESULTS/draft_run_plan_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-15/run_plan.json`
- `03_QUANTLENS/05_BACKTEST_RESULTS/draft_run_plan_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-15/artifact_index.json`
- `03_QUANTLENS/05_BACKTEST_RESULTS/draft_run_plan_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-15/run_plan.md`

## 3. Builder behavior verification

PASS.

Evidence:
- `build_run_plan.py` resolves symbols only from explicit CLI symbols or validated metadata.
- Unknown/unresolved strategy dry-run printed:
  - `symbols           : []`
  - warning: `symbol universe unresolved; run_plan.universe.status=needs_freeze`
  - warning explicitly says no default symbol was injected.
- Explicit-symbol dry-run passed:
  - command used `--symbols AAPL,MSFT`
  - output showed `symbols           : ['AAPL', 'MSFT']`
  - `run_plan valid    : YES`
  - `[DRY-RUN] no files written.`
- Unit tests include:
  - unresolved universe does not default BTCUSDT
  - explicit symbols are used
  - unknown strategy dry-run never injects a default symbol

## 4. Schema safety verification

PASS.

`run_plan.schema.json` requires and enforces:
- `read_only: true`
- `no_execution: true`
- `approval.human_review_required: true`
- `approval.approved: false`
- `approval.execution_allowed: false`

In-memory validation against the real regenerated `run_plan.json`:
- base plan: valid
- `read_only=false`: rejected
- `no_execution=false`: rejected
- `approval.human_review_required=false`: rejected
- `approval.approved=true`: rejected
- `approval.execution_allowed=true`: rejected

## 5. Generated artifact verification

PASS.

`run_plan.json` contains:
- `symbols: []`
- `universe.status: needs_freeze`
- `read_only: true`
- `no_execution: true`
- `approval.execution_allowed: false`
- `approval.approved: false`
- `approval.human_review_required: true`
- `status: draft_pending_approval`
- `expected_artifacts` lists `backtest_profile_result.json` and `top_results.json`, but does not create them.

`artifact_index.json` marks:
- `run_plan` exists: true
- `artifact_index` exists: true
- `run_plan_md` exists: true
- `backtest_profile_result` exists: false
- `top_results` exists: false

`run_plan.md` states:
- symbols are unresolved
- universe state is `needs_freeze`
- no default symbol was injected
- no backtest, worker, broker, or trade is triggered

## 6. Reader/snapshot verification

PASS.

Direct reader summary:
- `mode: read_only`
- `run_plan_count: 1`
- `artifact_index_count: 1`
- `profile_result_file_count: 0`
- `profile_result_count: 0`
- `top_results_count: 0`
- `has_profile_separated_results: false`
- `usable: 2`
- `invalid: 0`
- `incomplete: 0`

Dashboard snapshot includes `night_artifacts` with the same state:
- one usable `run_plan.json`
- one usable `artifact_index.json`
- zero profile result rows
- zero top result files

Invalid/incomplete behavior is covered by `test_night_artifacts_reader.py`:
- invalid JSON is reported as `invalid`
- schema-failing run plans are reported as `incomplete`
- reader does not write files

## 7. Strategy Intelligence UI verification

PASS, by static renderer and real snapshot-data inspection.

`app.js` now has `runPlanForStrategy(id)` selecting from `night_artifacts.run_plans` by `data.strategy_id` / `data.strategy_ids`, not hardcoded pilot text.

Strategy Intelligence section 4 (`Backtest Plan & Evidence`) reads real `run_plan.json` data:
- run id
- plan status
- approval state
- human review required
- approved
- execution allowed
- estimated cases
- universe/symbol status
- timeframes
- parameter-space state
- output dir
- expected artifacts
- missing assumptions / rule-freeze requirements

Browser visual QA was not performed because the browser automation tool was not exposed in this session and prior repo notes say localhost browser access has been policy-blocked. The renderer and read-model wiring were verified directly.

## 8. Result Explorer UI verification

PASS.

`Required Result Artifacts` in `app.js` reads states from `night_artifacts` through `artifactStateBadge()`:
- `run_plan.json` -> `run_plans`
- `artifact_index.json` -> `artifact_index`
- `backtest_profile_result.json` -> `profile_result_files`
- `top_results.json` -> `top_results`

Given the current reader state, the panel resolves to:
- `run_plan.json` - Present / usable
- `artifact_index.json` - Present / usable
- `backtest_profile_result.json` - Missing
- `top_results.json` - Missing

Official profile buckets are built only from `night_artifacts.profile_results`. Since `profile_results` is empty, all official profile buckets remain empty.

Legacy scorecards remain quarantined under:
- `Legacy Scorecard Reference - profile missing`

## 9. Safety/read-only verification

PASS.

Commands/checks run:
- `git status --short`
- `git diff --stat`
- `node --check 08_DASHBOARD_APP\apps\web\app.js` - PASS
- `python -m unittest discover tests` from `08_DASHBOARD_APP/apps/api` - PASS, 55 tests
- `GET /healthz` - PASS, `mode=read_only`, `overall_ok=true`
- `GET /api/snapshot?refresh=1` - PASS
- `POST /api/snapshot` - blocked with HTTP 405

Server code still blocks:
- POST
- PUT
- PATCH
- DELETE

Forbidden active UI wording grep over active web files returned no matches for:
- `Launch`
- `Deploy`
- `Execute`
- `Run Now`
- `Start Backtest`
- `Connect broker`
- `Safe to trade`
- `Live trading`
- `Manual trigger`
- `Manual local worker`
- `Execution Source`
- `Backtest Execution`

No `backtest_profile_result.json` or `top_results.json` exists anywhere under `03_QUANTLENS/05_BACKTEST_RESULTS`.

No Pine / MTC_V2 / backtest engine / broker / live / paper execution code diff was found in the inspected patch paths. Current `git status` showed no modified tracked Pine/MTC/backtest-engine execution files. One unrelated untracked HERMES parity-skill folder exists outside the MCC patch scope.

## 10. Issues found

1. Scope hygiene issue - current worktree is dirty beyond the reported targeted patch scope.
   - Modified tracked files include API/web shell files and `_AI_MEMORY` handoff files from earlier work.
   - Staged/deleted prototype moves are present under `08_DASHBOARD_APP/apps/web/prototypes`.
   - Many untracked files/directories exist, including schemas/readers/tests/reports from this artifact-reader/run-plan work and other unrelated workspace material.
   - Because the baseline is dirty, objective 14 cannot be fully proven from `git status` alone.

2. Visual UI verification limitation.
   - The exact visible browser rendering was not screenshot-verified in this audit.
   - Static renderer inspection plus live snapshot/reader state confirms the expected data path and labels.

No safety-contract, fake-KPI, profile-artifact, API-write, or execution-code issue was found.

## 11. Recommended next step

Freeze the intended patch scope into a clean review unit: stage/commit or otherwise isolate only the run-plan builder, schemas, night-artifact reader/tests, app.js UI wiring, regenerated draft plan artifacts, and patch reports. Then freeze the US equities symbol universe with explicit `--symbols` before any future approval path. Do not generate `backtest_profile_result.json` or `top_results.json` until a real validated profile run exists.
