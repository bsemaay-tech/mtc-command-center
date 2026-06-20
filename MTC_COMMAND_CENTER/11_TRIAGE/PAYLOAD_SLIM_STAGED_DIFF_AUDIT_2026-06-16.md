# Payload Slim Staged Diff Audit - 2026-06-16

## 1. Executive verdict

Verdict: **REQUIRES STAGING FIX**

The live payload-slim behavior remains correct, but the currently staged review unit is still not clean enough to accept as the `SNAPSHOT_PAYLOAD_SLIM_LOW_RISK_PATCH` review unit.

The previous prototype renames are no longer staged. However, the staged diff still has two staging defects:

- `read_model.py` stages the earlier `night_artifacts` reader introduction (`build_night_artifacts` import, call, and top-level `night_artifacts` snapshot key).
- `test_readonly_core.py` is not staged at all, so the payload-slim test assertions are missing from the staged review unit.

The staged diff also includes this staged-diff audit report itself. That report is required by this audit task, but it is not listed in the supplied payload-slim staged report whitelist, so the user should decide whether to include it with the payload-slim checkpoint or keep it as a separate audit artifact.

No code was modified, no files were staged/unstaged, no commit/reset/delete/move/backtest was performed. This report file was updated as the requested audit output.

## 2. Staged file list

`git diff --cached --name-status`:

- `M  MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py`
- `A  MTC_COMMAND_CENTER/11_TRIAGE/PAYLOAD_SLIM_REVIEW_UNIT_PLAN_2026-06-16.md`
- `A  MTC_COMMAND_CENTER/11_TRIAGE/PAYLOAD_SLIM_STAGED_DIFF_AUDIT_2026-06-16.md`
- `A  MTC_COMMAND_CENTER/11_TRIAGE/SNAPSHOT_PAYLOAD_PERFORMANCE_AUDIT_2026-06-16.md`
- `A  MTC_COMMAND_CENTER/11_TRIAGE/SNAPSHOT_PAYLOAD_SLIM_LOW_RISK_PATCH_AUDIT_2026-06-16.md`
- `A  MTC_COMMAND_CENTER/11_TRIAGE/SNAPSHOT_PAYLOAD_SLIM_LOW_RISK_PATCH_REPORT_2026-06-16.md`

`git diff --cached --stat` at final sanity check:

- `6 files changed, 989 insertions(+), 2 deletions(-)`

Prototype renames are no longer staged in the cached diff.

## 3. Staged hunk review

### `read_model.py`

Allowed payload-slim hunks are staged:

- `_count_or_passthrough()`
- `_slim_rows_cases()`
- `_slim_http_snapshot()`
- `candidate_audit` omitted from the outgoing HTTP snapshot dictionary
- `scorecards.by_strategy` removed inside `_slim_http_snapshot()`
- `scorecards.cards` preserved by shallow-copying `scorecards` and only popping `by_strategy`
- `candidate_pipeline.rows[].scorecard_v2_cases` converted from list to count
- `candidate_pipeline.candidates[].scorecard_v2_cases` also converted if present
- `build_dashboard_snapshot()` now assembles `snapshot` and returns `_slim_http_snapshot(snapshot)`
- internal `candidate_audit` is still built before slimming and still passed to `build_mtc_v2_readiness`

Disallowed/non-payload hunks are also staged:

- `from .night_artifacts_reader import build_night_artifacts`
- `night_artifacts = build_night_artifacts(model["mcc_root"])`
- top-level `"night_artifacts": night_artifacts`

Those are earlier night-artifact/data-contract hunks. They are not part of the payload-slim unit unless the night-artifact phase has already been committed as a prerequisite. In the current staged diff, they are mixed into the payload-slim checkpoint.

### `test_readonly_core.py`

No staged diff exists for `08_DASHBOARD_APP/apps/api/tests/test_readonly_core.py`.

This means the staged review unit is missing the allowed payload-slim test hunks:

- `candidate_audit` absent from HTTP snapshot
- `scorecards.cards` present
- `scorecards.by_strategy` absent
- `scorecard_v2_cases` int or null, never list

The working tree does contain those payload-slim test hunks, plus a non-payload dashboard title assertion change, but none of that file is currently staged.

## 4. Files that should not be staged

Currently staged items that need user decision or staging cleanup:

- non-payload hunks in `08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py`:
  - `night_artifacts_reader` import/call/snapshot key
- missing staged test file:
  - `08_DASHBOARD_APP/apps/api/tests/test_readonly_core.py` payload-slim assertions are not in the staged unit
- `11_TRIAGE/PAYLOAD_SLIM_STAGED_DIFF_AUDIT_2026-06-16.md`:
  - required audit output, but not listed in the supplied allowed staged report whitelist

No staged `app.js`, `index.html`, `styles.css`, prototype renames, launcher files, logs, profile-result converter/artifacts, run-plan builder/artifacts, schemas, Home metric invariant files, memory files, generated result files, Pine/MTC_V2/backtest-engine/broker/live/paper execution files were found in the cached diff.

## 5. Payload-slim behavior verification

Working-tree live behavior:

- `/api/snapshot?refresh=1`: HTTP `200`
- elapsed: `35.27s`
- raw content length: `46,808,919`
- size: `44.64 MB`
- top-level `candidate_audit` present: `False`
- `scorecards.cards` count: `837`
- `scorecards.by_strategy` present: `False`
- first `candidate_pipeline.rows[].scorecard_v2_cases` type: `System.Int32`

The behavior remains correct in the working tree. The staged diff still needs cleanup before the staged review unit can be accepted.

## 6. API/read-only verification

Health:

- `/healthz`: HTTP `200`
- `mode`: `read_only`
- `overall_ok`: `true`

Write API:

- `POST /api/snapshot`: `405`

No write API regression was observed.

## 7. Test results

JavaScript syntax:

- `node --check 08_DASHBOARD_APP\apps\web\app.js`: passed

API tests:

- command: `python -m unittest discover tests`
- result: `Ran 69 tests in 34.741s`
- status: `OK`

The test run printed expected dry-run messages from profile-result/run-plan tests. No backtest was run.

## 8. Protected scope check

Staged protected-scope check:

- `git diff --cached --name-only -- 02_MTC_BACKTEST 07_ADAPTERS 01_PINE MTC_V2 03_QUANTLENS`: no output

Working-tree protected-scope tracked diff check:

- `git diff --name-only -- 02_MTC_BACKTEST 07_ADAPTERS 01_PINE MTC_V2`: no output

No staged or tracked working-tree changes were found in Pine, MTC_V2, backtest engine, broker/live/paper execution paths, or strategy logic via these checks.

## 9. Issues found

1. **`read_model.py` includes non-payload night-artifact hunks.** The staged import/call/top-level snapshot key for `night_artifacts` is not part of the payload-slim patch unless already committed as a prerequisite.

2. **`test_readonly_core.py` is missing from the staged unit.** The allowed payload-slim test assertions are present only in the working tree, not in the cached diff.

3. **The staged-diff audit report itself is staged.** This report is required for the audit task, but it was not listed in the allowed staged payload-slim report files. User decision needed: include with audit/report checkpoint or leave unstaged.

No behavior or read-only safety failure was found.

## 10. Recommended manual action

Manual-only; not run by this audit:

1. Decide whether the night-artifact reader phase and dashboard shell title assertion are already accepted/committed prerequisites.
2. If not, restage only the payload-slim hunks:
   - keep `_count_or_passthrough()`, `_slim_rows_cases()`, `_slim_http_snapshot()`, candidate-audit omission, by-strategy removal, and scorecard-case count conversion;
   - exclude `night_artifacts_reader` import/call/top-level key from this checkpoint;
   - stage only the payload-slim assertions from `test_readonly_core.py`, excluding the dashboard title assertion hunk.
3. Decide whether to include `PAYLOAD_SLIM_STAGED_DIFF_AUDIT_2026-06-16.md` in this payload-slim checkpoint or keep it as a separate audit artifact.
4. Re-run the staged diff audit after restaging.

Suggested manual checks after restaging:

```powershell
cd C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER
git diff --cached --stat
git diff --cached --name-status
git diff --cached -- 08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py
git diff --cached -- 08_DASHBOARD_APP/apps/api/tests/test_readonly_core.py
git diff --cached --name-only -- 02_MTC_BACKTEST 07_ADAPTERS 01_PINE MTC_V2 03_QUANTLENS
```
