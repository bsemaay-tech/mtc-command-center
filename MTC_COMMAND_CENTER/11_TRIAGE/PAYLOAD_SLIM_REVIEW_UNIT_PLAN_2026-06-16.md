# Payload Slim Review Unit Plan - 2026-06-16

## 1. Executive summary

Purpose: prepare `SNAPSHOT_PAYLOAD_SLIM_LOW_RISK_PATCH` as a clean review/checkpoint unit without staging, committing, deleting, resetting, moving, or modifying code.

Behavior is re-verified and still acceptable:

- `/healthz`: HTTP `200`, `mode=read_only`, `overall_ok=true`
- `/api/snapshot?refresh=1`: HTTP `200`
- Snapshot size: `46,808,919` bytes / `44.64 MB`
- Top-level `candidate_audit`: absent
- `scorecards.cards`: present, `837` cards
- `scorecards.by_strategy`: absent
- `candidate_pipeline.rows[].scorecard_v2_cases`: `System.Int32`, list count `0`
- `POST /api/snapshot`: `405`
- `node --check`: passed
- API tests: `Ran 69 tests ... OK`

Checkpoint recommendation: **do not blindly `git add` whole tracked files until prior phase changes are isolated or committed.** `read_model.py` and `test_readonly_core.py` contain payload-slim hunks plus earlier accepted-phase hunks. Use either prerequisite commits first, or hunk-based staging for this checkpoint.

## 2. Current worktree status

Tracked modified files from `git status --short`:

- `08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py`
- `08_DASHBOARD_APP/apps/api/tests/test_readonly_core.py`
- `08_DASHBOARD_APP/apps/web/app.js`
- `08_DASHBOARD_APP/apps/web/index.html`
- `08_DASHBOARD_APP/apps/web/styles.css`
- `_AI_MEMORY/ACTIVE_FILES.md`
- `_AI_MEMORY/GLOBAL_HANDOFF.md`
- `_AI_MEMORY/NEXT_STEPS.md`
- `_AI_MEMORY/PROJECT_MEMORY.md`
- `_AI_MEMORY/SESSION_LOG.md`

Tracked renames:

- `08_DASHBOARD_APP/apps/web/prototypes/*` -> `11_TRIAGE/ui_references/legacy_web_prototypes/*`

Important staging note:

- `git diff --cached --stat` is already non-empty before this payload-slim plan. The staged index contains the 12 legacy prototype renames above (`0 insertions`, `0 deletions`). These appear to be prior UI cleanup work, not payload-slim work. They must be committed or explicitly unstaged by the user before creating a clean payload-slim checkpoint.

Untracked files include:

- Payload-slim reports:
  - `11_TRIAGE/SNAPSHOT_PAYLOAD_PERFORMANCE_AUDIT_2026-06-16.md`
  - `11_TRIAGE/SNAPSHOT_PAYLOAD_SLIM_LOW_RISK_PATCH_REPORT_2026-06-16.md`
  - `11_TRIAGE/SNAPSHOT_PAYLOAD_SLIM_LOW_RISK_PATCH_AUDIT_2026-06-16.md`
  - `11_TRIAGE/PAYLOAD_SLIM_REVIEW_UNIT_PLAN_2026-06-16.md`
- Other accepted-phase reports under `11_TRIAGE/`
- Night artifact schemas under `06_SCHEMAS/`
- Run-plan/profile-result tooling under `03_QUANTLENS/tools/`
- Reader/tests such as `night_artifacts_reader.py`, `test_build_run_plan.py`, `test_night_artifacts_reader.py`
- Launcher file/logs under `08_DASHBOARD_APP/`
- UI references/screenshots
- unrelated root-level folders/files such as `../HERMES/`, `../Temp/`, `../YT_TRANSCRIPT_COLLECTOR/`

`git diff --stat` currently reports 10 tracked files changed with `3172 insertions` and `5200 deletions`; this excludes many untracked reports/tools/schemas.

## 3. Files that belong to payload-slim checkpoint

Core payload-slim implementation and test:

- `08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py`
  - Payload-slim hunks only:
    - `_count_or_passthrough()`
    - `_slim_rows_cases()`
    - `_slim_http_snapshot()`
    - omit top-level `candidate_audit` from HTTP snapshot output
    - return `_slim_http_snapshot(snapshot)`
    - convert `scorecard_v2_cases` arrays to counts in outgoing HTTP rows/candidates
  - Caution: this file also contains earlier `night_artifacts` wiring hunks. Do not include those in this checkpoint unless the night-artifact phase is intentionally part of an earlier/prerequisite commit.

- `08_DASHBOARD_APP/apps/api/tests/test_readonly_core.py`
  - Payload-slim hunks only:
    - assert `candidate_audit` absent from HTTP snapshot
    - assert `scorecards.cards` present
    - assert `scorecards.by_strategy` absent
    - assert `scorecard_v2_cases` is int or null, never list
  - Caution: this file also contains an earlier dashboard-title assertion change (`MTC Command Center` -> `Strategy Intelligence Command Center`). Do not include that hunk in this payload-only checkpoint unless the UI shell phase has already been committed.

Payload-slim evidence reports:

- `11_TRIAGE/SNAPSHOT_PAYLOAD_PERFORMANCE_AUDIT_2026-06-16.md`
- `11_TRIAGE/SNAPSHOT_PAYLOAD_SLIM_LOW_RISK_PATCH_REPORT_2026-06-16.md`
- `11_TRIAGE/SNAPSHOT_PAYLOAD_SLIM_LOW_RISK_PATCH_AUDIT_2026-06-16.md`

Optional planning report:

- `11_TRIAGE/PAYLOAD_SLIM_REVIEW_UNIT_PLAN_2026-06-16.md`
  - Include with payload-slim reports if the checkpoint is intended to carry the hygiene plan.
  - Otherwise keep it for a separate triage/report checkpoint.

## 4. Files that should not be included

Do not include these in the payload-slim checkpoint:

- Dashboard UI shell / redesign files:
  - `08_DASHBOARD_APP/apps/web/app.js`
  - `08_DASHBOARD_APP/apps/web/index.html`
  - `08_DASHBOARD_APP/apps/web/styles.css`
  - moved prototype references under `11_TRIAGE/ui_references/legacy_web_prototypes/`
- Launcher patch files/logs:
  - `08_DASHBOARD_APP/run_dashboard_server.ps1`
  - `08_DASHBOARD_APP/logs/`
  - launcher reports
- Night-artifact reader/schema/run-plan work unless already committed as a prerequisite:
  - `08_DASHBOARD_APP/apps/api/mcc_readonly/night_artifacts_reader.py`
  - `06_SCHEMAS/*.schema.json`
  - `03_QUANTLENS/tools/build_run_plan.py`
  - `08_DASHBOARD_APP/apps/api/tests/test_build_run_plan.py`
  - `08_DASHBOARD_APP/apps/api/tests/test_night_artifacts_reader.py`
  - generated draft run-plan directories
- Profile-result pilot work:
  - `03_QUANTLENS/tools/build_profile_result_artifact.py`
  - profile-result pilot reports/artifacts
  - `08_DASHBOARD_APP/apps/api/tests/test_build_profile_result_artifact.py`
- Home metric/canonical universe reports and tests:
  - `08_DASHBOARD_APP/apps/api/tests/test_home_metric_invariants.py`
  - `HOME_*` reports
- UI screenshots/reference folders/zips unless committed in a dedicated UI-reference checkpoint
- unrelated root-level/local files:
  - `../HERMES/`
  - `../Temp/`
  - `../YT_TRANSCRIPT_COLLECTOR/`
  - `../AUDIT_REPORT_CODEX.md`
  - `../CHATGPT_MEMORY_PROMPT.md`
  - `../Quantlens.md`
  - similar local scratch/import folders
- Pine, MTC_V2, backtest engine, broker/live/paper execution, strategy logic, and API write behavior files.

## 5. Files needing user decision

Memory files:

- `_AI_MEMORY/SESSION_LOG.md`
- `_AI_MEMORY/NEXT_STEPS.md`
- `_AI_MEMORY/ACTIVE_FILES.md`
- `_AI_MEMORY/GLOBAL_HANDOFF.md`
- `_AI_MEMORY/PROJECT_MEMORY.md`

Reason: these diffs are mixed. They include payload-slim notes, but also launcher, profile-result pilot, Home canonical universe, UI shell, overnight, and earlier dashboard phase updates. Best handling is a separate documentation/handoff checkpoint after code review units are isolated.

Other user-decision groups:

- Earlier accepted-phase reports in `11_TRIAGE/`
- UI reference folders and screenshots
- generated sample artifacts under `03_QUANTLENS/05_BACKTEST_RESULTS/`
- startup/launcher files
- root-level HERMES/Temp/transcript/import folders

## 6. Behavior verification results

Snapshot measurement:

- Endpoint: `http://127.0.0.1:8765/api/snapshot?refresh=1`
- HTTP status: `200`
- Elapsed: `30.01s`
- Raw content length: `46,808,919`
- Size: `44.64 MB`

Snapshot structure:

- `candidate_audit present`: `False`
- `scorecards.cards count`: `837`
- `scorecards.by_strategy present`: `False`
- `candidate_pipeline.rows count`: `176`
- first `scorecard_v2_cases` type: `System.Int32`
- observed `scorecard_v2_cases` types: `System.Int32`
- `scorecard_v2_cases` list count: `0`

This confirms the accepted L1+L2+L3 behavior remains active.

## 7. API/read-only verification

Health:

- `/healthz`: HTTP `200`
- `mode`: `read_only`
- `overall_ok`: `true`

Write method:

- `POST /api/snapshot`: `405`

No API write behavior change was detected.

## 8. Test results

JavaScript:

- `node --check 08_DASHBOARD_APP\apps\web\app.js`: passed

API:

- Command: `python -m unittest discover tests`
- Result: `Ran 69 tests in 29.041s`
- Status: `OK`

The API test run printed expected dry-run messages from profile-result/run-plan tests and did not run a backtest.

## 9. Protected scope check

Tracked protected-scope diff:

- `git diff --name-only -- 02_MTC_BACKTEST 07_ADAPTERS 01_PINE MTC_V2 03_QUANTLENS`: no output

Requested protected status check:

- `git status --short -- 03_QUANTLENS 02_MTC_BACKTEST 07_ADAPTERS` shows untracked `03_QUANTLENS` docs/tools only:
  - `03_QUANTLENS/_user_guide/13_GATE_SCORECARD_V2_TR.md`
  - `03_QUANTLENS/_user_guide/14_OPTIMIZASYON_SKORLAMA_TR.md`
  - `03_QUANTLENS/tools/build_profile_result_artifact.py`
  - `03_QUANTLENS/tools/build_run_plan.py`
  - overnight helper scripts

No tracked Pine, MTC_V2, backtest engine execution, broker/live/paper execution, API write behavior, or strategy logic changes were identified for this payload-slim checkpoint.

## 10. Manual checkpoint commands

Do not run these automatically. Manual-only.

Preferred sequence if earlier accepted phases are committed first:

```powershell
cd C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER

git diff --cached --stat
# If this shows the legacy prototype renames, checkpoint or unstage those first.

git add 08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py
git add 08_DASHBOARD_APP/apps/api/tests/test_readonly_core.py
git add 11_TRIAGE/SNAPSHOT_PAYLOAD_PERFORMANCE_AUDIT_2026-06-16.md
git add 11_TRIAGE/SNAPSHOT_PAYLOAD_SLIM_LOW_RISK_PATCH_REPORT_2026-06-16.md
git add 11_TRIAGE/SNAPSHOT_PAYLOAD_SLIM_LOW_RISK_PATCH_AUDIT_2026-06-16.md
git add 11_TRIAGE/PAYLOAD_SLIM_REVIEW_UNIT_PLAN_2026-06-16.md

git diff --cached --stat
git diff --cached -- 08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py
git diff --cached -- 08_DASHBOARD_APP/apps/api/tests/test_readonly_core.py

git commit -m "Slim dashboard snapshot payload"
```

Safer sequence if committing from the current broad dirty tree:

```powershell
cd C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER

git diff --cached --stat
# Current audit observed pre-existing staged legacy prototype renames.
# Do not create the payload-slim commit until the staged index contains only payload-slim files.

# Stage only payload-slim hunks. Do not stage earlier night_artifacts wiring
# or the dashboard-title assertion hunk unless those prerequisite phases are already committed.
git add -p 08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py
git add -p 08_DASHBOARD_APP/apps/api/tests/test_readonly_core.py

git add 11_TRIAGE/SNAPSHOT_PAYLOAD_PERFORMANCE_AUDIT_2026-06-16.md
git add 11_TRIAGE/SNAPSHOT_PAYLOAD_SLIM_LOW_RISK_PATCH_REPORT_2026-06-16.md
git add 11_TRIAGE/SNAPSHOT_PAYLOAD_SLIM_LOW_RISK_PATCH_AUDIT_2026-06-16.md
git add 11_TRIAGE/PAYLOAD_SLIM_REVIEW_UNIT_PLAN_2026-06-16.md

git diff --cached --stat
git diff --cached -- 08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py
git diff --cached -- 08_DASHBOARD_APP/apps/api/tests/test_readonly_core.py

node --check 08_DASHBOARD_APP\apps\web\app.js
cd C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api
$env:PYTHONPATH="."
python -m unittest discover tests

cd C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER
git commit -m "Slim dashboard snapshot payload"
```

Optional separate documentation/handoff checkpoint:

```powershell
cd C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER

git add _AI_MEMORY/SESSION_LOG.md
git add _AI_MEMORY/NEXT_STEPS.md
git add _AI_MEMORY/ACTIVE_FILES.md
git add _AI_MEMORY/GLOBAL_HANDOFF.md
git add _AI_MEMORY/PROJECT_MEMORY.md

git diff --cached --stat
git commit -m "Update dashboard payload-slim handoff notes"
```

Manual handling options for the pre-existing staged prototype renames:

```powershell
cd C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER

# Option A: keep them staged and commit them as their own UI-reference checkpoint.
git diff --cached --stat
git commit -m "Move legacy dashboard prototypes to triage references"

# Option B: if the user wants the index clean before any checkpoint, unstage them manually.
# This does not delete or move files; it only removes them from the staged index.
git restore --staged 08_DASHBOARD_APP/apps/web/prototypes
git restore --staged 11_TRIAGE/ui_references/legacy_web_prototypes
```

## 11. Risks if not isolated

- A whole-file commit of `read_model.py` from the current tree may include prior `night_artifacts` reader wiring, not only payload slimming.
- A whole-file commit of `test_readonly_core.py` may include a prior dashboard shell title assertion change, not only payload-slim contract assertions.
- The staged index is already non-empty with prior prototype renames; committing payload-slim without clearing or separating the index would mix review units.
- Including `app.js`, `index.html`, or `styles.css` would mix the payload-slim patch with broad UI shell/Home/Result Explorer changes.
- Including memory files directly would mix multiple accepted phases and make rollback/review noisy.
- Including generated sample artifacts or profile-result pilot outputs could blur the distinction between payload serialization and research-only artifact work.
- Including launcher/log files would mix operational process management with read-model serialization.

## 12. Recommended next phase

1. Checkpoint earlier accepted dashboard/data-contract phases in their own review units, or use hunk-based staging for payload-slim only.
2. Commit the payload-slim review unit after confirming the staged diff contains only L1+L2+L3 serialization changes and the three evidence reports.
3. Commit mixed memory/handoff updates separately if desired.
4. Defer M1 lazy-load work. Do not start per-strategy gate-detail lazy loading in this checkpoint.
