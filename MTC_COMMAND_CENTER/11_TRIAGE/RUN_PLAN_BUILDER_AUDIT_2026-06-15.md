# Run Plan Builder Audit - 2026-06-15

## 1. Executive verdict

Verdict: **ACCEPT THE BUILDER / REQUIRES TARGETED UI PATCHES BEFORE CLAIMING FULL DASHBOARD INTEGRATION**.

The run-plan artifact builder exists, the generated `run_plan.json` and `artifact_index.json` are schema-valid, `night_artifacts_reader.py` discovers them from the expected `05_BACKTEST_RESULTS/<run_id>/` directory, and `/api/snapshot?refresh=1` exposes the run plan as `usable`.

The implementation remains read-only at API level. `POST /api/snapshot` is blocked with HTTP 405, dashboard API tests pass, and no `backtest_profile_result.json` or fake profile-separated result rows were created.

Main problems:

- `Strategy Intelligence -> Backtest Plan & Evidence` does **not** display the generated `run_plan.json`; it still renders `Pending run_plan.json` copy.
- `Backtest Result Explorer` keeps official profile buckets empty as expected, but its Required Result Artifacts panel still marks `run_plan.json` and `artifact_index.json` as `Missing` even though both exist and are exposed by `night_artifacts`.
- The generated run plan uses `symbols=["BTCUSDT"]` for a `2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK` strategy. This is not a fake KPI, but it is a questionable/default market universe for a US-equities strategy and should be treated as a run-plan quality issue.
- The worktree has many unrelated dirty/untracked files, so isolated scope cannot be confirmed from `git status`.

## 2. Files inspected

Core implementation:

- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_run_plan.py`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/night_artifacts_reader.py`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/app.js`

Tests:

- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_build_run_plan.py`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_night_artifacts_reader.py`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_readonly_core.py`

Schemas:

- `MTC_COMMAND_CENTER/06_SCHEMAS/run_plan.schema.json`
- `MTC_COMMAND_CENTER/06_SCHEMAS/artifact_index.schema.json`
- `MTC_COMMAND_CENTER/06_SCHEMAS/backtest_profile_result.schema.json`
- `MTC_COMMAND_CENTER/06_SCHEMAS/top_results.schema.json`
- `MTC_COMMAND_CENTER/06_SCHEMAS/run_status.schema.json`

Worktree scope:

- `git diff --stat`
- `git status --short`

## 3. Generated artifacts inspected

Directory:

`MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/draft_run_plan_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-15/`

Files present:

- `run_plan.json` - 3,523 bytes
- `artifact_index.json` - 4,081 bytes
- `run_plan.md` - 1,603 bytes

Key `run_plan.json` values verified:

- `run_id`: `draft_run_plan_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-15`
- `status`: `draft_pending_approval`
- `read_only`: `true`
- `strategy_id`: `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK`
- `strategy_display_name`: `UNKNOWN_TITLE - 8 EMA purple line Amazon trade`
- `profiles`: `SOURCE_NAKED`, `RISK_NORMALIZED`, `MTC_LIGHT`, `FULL_MTC_CANDIDATE`
- `symbols`: `BTCUSDT`
- `timeframes`: `10m`
- `case_count`: `4`
- `no_execution`: `true`
- `approval.human_review_required`: `true`
- `approval.approved`: `false`
- `approval.execution_allowed`: `false`

Key `artifact_index.json` values verified:

- `run_id`: `draft_run_plan_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-15`
- `read_only`: `true`
- `root_dir`: `03_QUANTLENS/05_BACKTEST_RESULTS/draft_run_plan_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-15`
- `artifact_count`: `11`
- Artifact types: `run_plan`, `artifact_index`, `run_plan_md`, `run_status`, `progress`, `heartbeat`, `backtest_profile_result`, `top_results`, `leaderboard_delta`, `benchmark_update_candidate`, `morning_report`

Missing in the generated directory:

- `backtest_profile_result.json`
- `top_results.json`
- `run_status.json`

This supports the claim that no profile-separated result artifact was generated.

## 4. Schema validation result

Validation command used the repo's own `mcc_readonly.schema.validate_json_schema`.

Results:

- `run_plan.json` vs `06_SCHEMAS/run_plan.schema.json`: `issues=0`
- `artifact_index.json` vs `06_SCHEMAS/artifact_index.schema.json`: `issues=0`

Additional observation:

- The schemas are permissive. `run_plan.schema.json` requires only `run_id`, `read_only`, `strategy_ids`, and `profiles`.
- It does not require or enforce `approval.execution_allowed=false`, `no_execution=true`, or `status=draft_pending_approval`.
- The generated file itself has the correct safety flags, but the schema would not fully protect that contract.

## 5. Reader discovery result

`night_artifacts_reader.py` scan logic:

- Scans `03_QUANTLENS/05_BACKTEST_RESULTS`.
- Uses `results_root` plus the most recent immediate subdirectories.
- Bounds scanning with `MAX_RUN_DIRS = 150`.
- Parses structured artifacts:
  - `run_plan.json`
  - `run_status.json`
  - `artifact_index.json`
  - `backtest_profile_result.json`
  - `top_results.json`
  - `leaderboard_delta.json`
  - `benchmark_update_candidate.json`
- Reports companion artifacts:
  - `run_plan.md`
  - `approval_package.md`
  - `expected_artifacts.json`
  - `progress.json`
  - `heartbeat.json`
  - `summary.json`
  - `morning_report.md`

Direct reader result:

```text
summary = {
  "expected_types": 14,
  "present_types": 4,
  "missing_types": 10,
  "files_found": 6,
  "invalid": 0,
  "incomplete": 0,
  "usable": 2,
  "profile_result_rows": 0,
  "has_profile_separated_results": false
}
```

Discovered records:

- `run_plans`: 1
  - state: `usable`
  - path: `03_QUANTLENS/05_BACKTEST_RESULTS/draft_run_plan_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-15/run_plan.json`
  - issues: `[]`
- `artifact_index`: 1
  - state: `usable`
  - path: `03_QUANTLENS/05_BACKTEST_RESULTS/draft_run_plan_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-15/artifact_index.json`
  - issues: `[]`
- `profile_results`: 0
- `profile_result_files`: 0
- `companions`: includes the generated `run_plan.md` plus existing `morning_report.md` companions elsewhere.

Conclusion: reader discovery passes.

## 6. Snapshot/API evidence

Commands and results:

- `Invoke-WebRequest http://127.0.0.1:8765/healthz -UseBasicParsing`
  - HTTP 200
  - `mode=read_only`
  - `overall_ok=true`

- `Invoke-WebRequest http://127.0.0.1:8765/api/snapshot?refresh=1 -UseBasicParsing`
  - HTTP 200
  - Returned after about 110 seconds in this audit environment.
  - `mode=read_only`
  - `night_artifacts.summary.expected_types=14`
  - `present_types=4`
  - `usable=2`
  - `invalid=0`
  - `profile_result_rows=0`
  - first run plan state: `usable`
  - first run plan id: `draft_run_plan_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-15`

- `POST /api/snapshot`
  - HTTP 405 Method Not Allowed

Snapshot run-plan data verified:

- `status=draft_pending_approval`
- `approval.execution_allowed=false`
- `profiles` contains the four official buckets.
- `profile_results_len=0`
- `profile_result_files_len=0`

Concern:

- `/api/snapshot?refresh=1` works but is slow. This is not a builder correctness failure, but it is relevant for dashboard usability.

## 7. Dashboard/UI evidence

Backtest Planner:

- Uses `usableRunPlans()[0]`.
- Displays `run_plan.json present`.
- Displays `Run ID`, `Approval State`, `Case Count`, `Output Dir`, `Timeframes`, `Universe`, parameter-space count, and expected artifacts from `run_plan.json`.
- This page is wired to the generated run-plan data.

Strategy Intelligence -> Backtest Plan & Evidence:

- `renderIntelligence()` calls `evidenceSection(m)`.
- `evidenceSection(m)` does **not** read `usableRunPlans()`, `night_artifacts.run_plans`, or `run_plan.data`.
- It still renders:
  - `Plan Readiness` as `Pending run_plan.json`
  - `Estimated Cells / Cases` from strategy model only
  - `Case Count Calculator` as `Parameter space and case-count calculation require run_plan.json - pending / artifact missing`
  - `Parameter Space Preview` as `Parameter space not present in read model`
- This does **not** satisfy the expected UI display for Strategy Intelligence -> Backtest Plan & Evidence.

Advanced Artifacts:

- Uses `nightArtifacts()`.
- Maps `run_plan.json` to `naList("run_plans")`.
- Maps `artifact_index.json` to `naList("artifact_index")`.
- Shows contract summary using `night_artifacts.summary`.
- Shows artifact state and path for discovered run-plan artifacts.
- This page is wired to the generated run-plan data.

Result Explorer:

- Uses `profileRows()` from `night_artifacts.profile_results`.
- Official profile buckets are generated from profile-separated rows only.
- Because there is no `backtest_profile_result.json`, buckets remain empty.
- Legacy scorecard rows are quarantined in `Legacy Scorecard Reference - profile missing`.
- This satisfies the official bucket safety requirement.

Result Explorer gap:

- The Required Result Artifacts panel is static and marks all listed artifacts as `Missing`, including `run_plan.json` and `artifact_index.json`.
- Since both artifacts exist and are exposed by `night_artifacts`, this panel is now stale/misleading.

Forbidden UI wording grep:

- Search across active `apps/web/app.js`, `index.html`, and `styles.css` for:
  - `Launch`
  - `Deploy`
  - `Execute`
  - `Run Now`
  - `Start Backtest`
  - `Connect broker`
  - `Safe to trade`
  - `Live trading`
- Result: no matches.

`node --check`:

- `node --check 08_DASHBOARD_APP/apps/web/app.js`
- Result: PASS.

## 8. Safety/read-only evidence

Builder safety:

- `build_run_plan.py` docstring states it does not run backtests, trigger execution, touch Pine/MTC_V2/backtest engine/brokers, or add a write API.
- The builder writes only planning artifacts when executed without `--dry-run`.
- It was not run during this audit.
- The unit test suite did run `build_run_plan.py --dry-run`; output confirmed `[DRY-RUN] no files written`.

Generated artifact safety:

- `run_plan.json` has `read_only=true`.
- `run_plan.json` has `no_execution=true`.
- `approval.approved=false`.
- `approval.execution_allowed=false`.
- `run_plan.md` states it is not executed and `execution_allowed=false`.

API safety:

- `/healthz` reports `mode=read_only`.
- `POST /api/snapshot` is blocked with HTTP 405.
- API tests passed.

No fake KPI/profile-result evidence:

- No `backtest_profile_result.json` exists in the generated directory.
- No `top_results.json` exists in the generated directory.
- No `run_status.json` exists in the generated directory.
- `night_artifacts.profile_results` length is `0`.
- `night_artifacts.profile_result_files` length is `0`.
- `run_plan.md` explicitly says selection is operator-driven, not a performance claim.
- Search hits for performance terms in generated artifacts are only contract references such as `backtest_profile_result.json`, `same_bucket_rule`, and `not a performance claim`.

Protected files:

- I did not run a backtest.
- I did not modify Pine, MTC_V2, broker/live/paper trading, execution code, or production code.

## 9. Issues found

### RPB-AUDIT-001 - Strategy Intelligence does not consume run_plan.json

Severity: P1 High

Evidence:

- `evidenceSection(m)` still renders `Pending run_plan.json`.
- It does not read `night_artifacts.run_plans` or `usableRunPlans()`.

Why it matters:

- One audit objective requires Strategy Intelligence -> Backtest Plan & Evidence to display run-plan data.
- The generated run plan is exposed by the API but not surfaced on this key page.

Recommended next action:

- Patch Strategy Intelligence's evidence section to select the relevant run plan by strategy ID and display run ID, approval state, case count, profiles, symbols, timeframes, parameter-space state, expected artifacts, and output dir.

### RPB-AUDIT-002 - Result Explorer marks present planning artifacts as missing

Severity: P1 High

Evidence:

- Result Explorer's Required Result Artifacts panel statically labels `run_plan.json` and `artifact_index.json` as `Missing`.
- `night_artifacts` exposes both as `usable`.

Why it matters:

- This contradicts the new reader/API state and makes the run-plan integration look broken from the Result Explorer.

Recommended next action:

- Use `night_artifacts.run_plans` and `night_artifacts.artifact_index` in Result Explorer's artifact panel while keeping profile-result buckets empty until `backtest_profile_result.json` exists.

### RPB-AUDIT-003 - Generated run plan uses BTCUSDT for a US-equities strategy

Severity: P2 Medium

Evidence:

- `run_plan.json` has `strategy_id=QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK`.
- `symbols=["BTCUSDT"]`.
- `build_run_plan.py` defaults to `["BTCUSDT"]` when no symbol is found.

Why it matters:

- This is not a fake KPI, but it is a questionable/fabricated market universe for a strategy identified as US equities / 10m / 8 EMA pullback.
- A review-only plan should mark the symbol universe as unresolved rather than defaulting to a crypto symbol.

Recommended next action:

- Change future builder behavior to emit an explicit missing/unresolved universe state when the registry lacks symbol data, or require `--symbols` for non-crypto/intake-derived strategies.

### RPB-AUDIT-004 - Schemas are too weak for the safety contract

Severity: P2 Medium

Evidence:

- `run_plan.schema.json` does not require `status`, `no_execution`, `approval`, `approval.approved=false`, or `approval.execution_allowed=false`.
- The generated artifact has the correct values, but schema validation would not enforce them.

Why it matters:

- The audit objective checks schema validity, but the schema does not fully encode the claimed safety contract.

Recommended next action:

- Tighten `run_plan.schema.json` after approval so draft planning artifacts must include explicit non-execution approval fields.

### RPB-AUDIT-005 - Worktree scope is not clean

Severity: P2 Medium

Evidence:

- `git status --short` shows modified dashboard API/web files, modified `_AI_MEMORY` files, renamed legacy prototype files, untracked schemas, untracked builder/reader/tests, untracked reports, and other unrelated untracked folders/files.
- `git diff --stat` shows tracked changes in dashboard web/API and memory files.

Why it matters:

- The audit objective asks to verify no unrelated files were modified. In the current dirty worktree, that cannot be confirmed.

Recommended next action:

- Before accepting/committing the run-plan builder work, stage/review only the intended files and explicitly exclude unrelated memory/prototype/report/temp changes.

### RPB-AUDIT-006 - Snapshot refresh is slow

Severity: P3 Low

Evidence:

- `/api/snapshot?refresh=1` returned HTTP 200 but took about 110 seconds during this audit.

Why it matters:

- The reader is shallow and bounded, but the full snapshot path remains expensive enough to affect dashboard UX and validation cadence.

Recommended next action:

- Profile snapshot build time separately. Do not block run-plan builder acceptance on this unless the slowness is introduced by `night_artifacts_reader.py`.

## 10. Recommended next step

Do not run backtests. Do not generate profile-result artifacts yet.

Recommended next step:

1. Apply a targeted UI-only patch so Strategy Intelligence and Result Explorer consume `night_artifacts.run_plans` / `artifact_index` consistently.
2. Patch builder behavior so unresolved/non-crypto symbol universes do not default to `BTCUSDT`.
3. Tighten the run-plan schema safety fields in a separate schema-focused change.
4. Review/stage the intended builder-related files only, because the current worktree has unrelated dirty state.

Validation already passed for the core builder/reader contract:

- `node --check`: PASS
- dashboard API tests: `51 tests OK`
- `run_plan.json`: schema-valid
- `artifact_index.json`: schema-valid
- `/healthz`: read-only OK
- `/api/snapshot?refresh=1`: exposes run plan as usable
- `POST /api/snapshot`: blocked with HTTP 405
- official profile buckets remain empty because no `backtest_profile_result.json` exists
