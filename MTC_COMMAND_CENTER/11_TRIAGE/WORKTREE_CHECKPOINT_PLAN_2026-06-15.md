# Worktree Checkpoint Plan - 2026-06-15

## 1. Executive summary

Current worktree contains accepted dashboard/data-contract work plus unrelated local noise. Validation is green, but the tree is not checkpoint-ready as one clean unit.

Recommended approach: create separate checkpoints for UI shell/cleanup, read-only artifact reader + schemas, run-plan builder + optional sample plan, run-plan UI/safety wiring, Home aggregation/canonical universe, then reports/memory. Do not include unrelated external folders, logs, screenshots, Turkish guide drafts, or old overnight launcher scripts without an explicit owner decision.

Important staging note: 12 legacy prototype relocations are already staged. They will be included in the next commit unless the user intentionally unstages or commits them as the UI shell checkpoint.

## 2. Current git status summary

Commands run:
- `git status --short`
- `git diff --stat`
- `git diff --name-only`
- `git diff --cached --name-status`
- `git ls-files --others --exclude-standard`

Tracked unstaged diff:
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

Tracked diff stat:
- 10 files changed
- 2,974 insertions
- 5,198 deletions

Staged changes:
- 12 exact renames from `08_DASHBOARD_APP/apps/web/prototypes/*` to `11_TRIAGE/ui_references/legacy_web_prototypes/*`.

Untracked but likely intended for recent phases:
- new schemas under `06_SCHEMAS/`
- `night_artifacts_reader.py`
- API tests for run-plan, night artifacts, and Home metrics
- `build_run_plan.py`
- multiple `11_TRIAGE/*REPORT*.md` / audit prompt files
- UI reference folders under `11_TRIAGE/ui_references/`

Ignored but present:
- `03_QUANTLENS/05_BACKTEST_RESULTS/draft_run_plan_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-15/`
- ignored by `.gitignore:95` via `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/`

Validation:
- `node --check 08_DASHBOARD_APP\apps\web\app.js`: PASS
- API unittest discovery: PASS, 60 tests OK
- `/healthz`: PASS, `mode=read_only`, `overall_ok=true`
- `/api/snapshot?refresh=1`: PASS, HTTP 200
- `POST /api/snapshot`: blocked, HTTP 405

## 3. Group A intended UI files

Intended dashboard UI shell / cleanup files:
- `08_DASHBOARD_APP/apps/web/app.js`
- `08_DASHBOARD_APP/apps/web/index.html`
- `08_DASHBOARD_APP/apps/web/styles.css`

Staged intended UI/reference relocation, if the prototype cleanup is accepted:
- `08_DASHBOARD_APP/apps/web/prototypes/README.md` -> `11_TRIAGE/ui_references/legacy_web_prototypes/README.md`
- `proto_A_tabbed.html`
- `proto_B2_clinical.html`
- `proto_B2_editorial.html`
- `proto_B2_terminal.html`
- `proto_B_scroll.html`
- `proto_C_compact.html`
- `proto_stage_backtested.html`
- `proto_stage_promotion.html`
- `proto_stage_rules_extracted.html`
- `proto_stage_testability.html`
- `proto_terminal.css`

Untracked UI reference inputs likely associated with accepted UI phases:
- `11_TRIAGE/ui_references/google_strategy_intelligence_v2_final/`
- `11_TRIAGE/ui_references/strategy_intelligence_lovable/`

Checkpoint recommendation:
- Keep active app files and intentional legacy prototype relocation together in the UI shell/checkpoint.
- Treat bulky reference screenshots/zips as optional; include only if the repo should preserve design source evidence.

## 4. Group B intended API/reader files

Intended read-only API / reader files:
- `08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py`
- `08_DASHBOARD_APP/apps/api/mcc_readonly/night_artifacts_reader.py`
- `08_DASHBOARD_APP/apps/api/tests/test_readonly_core.py`
- `08_DASHBOARD_APP/apps/api/tests/test_build_run_plan.py`
- `08_DASHBOARD_APP/apps/api/tests/test_home_metric_invariants.py`
- `08_DASHBOARD_APP/apps/api/tests/test_night_artifacts_reader.py`

Checkpoint recommendation:
- Commit `night_artifacts_reader.py`, `read_model.py`, and related API tests with the schema reader/data-contract checkpoint.
- The Home invariant test belongs with the Home metric/canonical universe checkpoint.

## 5. Group C intended schema files

Intended schema files:
- `06_SCHEMAS/artifact_index.schema.json`
- `06_SCHEMAS/backtest_profile_result.schema.json`
- `06_SCHEMAS/run_plan.schema.json`
- `06_SCHEMAS/run_status.schema.json`
- `06_SCHEMAS/top_results.schema.json`

Checkpoint recommendation:
- Commit these with the night artifact reader/data-contract checkpoint.
- Do not mix schema introduction with unrelated Home UI metric changes if avoidable.

## 6. Group D intended tooling files

Intended tooling:
- `03_QUANTLENS/tools/build_run_plan.py`
- `08_DASHBOARD_APP/apps/api/tests/test_build_run_plan.py`

Needs user decision / probably not part of current dashboard/data-contract checkpoint:
- `03_QUANTLENS/tools/night_1m_2026-06-07.sh`
- `03_QUANTLENS/tools/overnight_loop_2026-06-08.sh`
- `03_QUANTLENS/tools/start_night_1m_2026-06-07_keepawake.ps1`
- `03_QUANTLENS/tools/start_night_3M_2026-06-08_keepawake.ps1`

Checkpoint recommendation:
- Commit `build_run_plan.py` and its test in the run-plan builder checkpoint.
- Do not include old overnight launch/keep-awake scripts in this checkpoint sequence unless the user explicitly wants to preserve those run launchers.

## 7. Group E intended generated artifacts

Review-only sample artifacts found on disk:
- `03_QUANTLENS/05_BACKTEST_RESULTS/draft_run_plan_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-15/run_plan.json`
- `03_QUANTLENS/05_BACKTEST_RESULTS/draft_run_plan_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-15/artifact_index.json`
- `03_QUANTLENS/05_BACKTEST_RESULTS/draft_run_plan_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-15/run_plan.md`

File sizes:
- `artifact_index.json`: 4,080 bytes
- `run_plan.json`: 3,753 bytes
- `run_plan.md`: 1,909 bytes

Git note:
- These files are ignored by `.gitignore:95` through `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/`.
- If the sample plan should be tracked, the user must intentionally force-add it.

Checkpoint recommendation:
- Prefer not committing generated backtest-result-tree artifacts by default.
- If a durable sample fixture is required, either force-add this exact draft directory or move a minimized fixture to a non-ignored test fixture path in a later approved task.

## 8. Group F intended reports/memory files

Intended reports / audit artifacts:
- `11_TRIAGE/BACKTEST_ARTIFACT_READER_INTEGRATION_REPORT_2026-06-15.md`
- `11_TRIAGE/DASHBOARD_DATA_AVAILABILITY_AUDIT_2026-06-15.md`
- `11_TRIAGE/DASHBOARD_TARGETED_PATCH_REPORT_2026-06-15.md`
- `11_TRIAGE/DASHBOARD_UI_INTEGRATION_AUDIT_2026-06-14.md`
- `11_TRIAGE/HOME_CANONICAL_UNIVERSE_PATCH_AUDIT_2026-06-15.md`
- `11_TRIAGE/HOME_CANONICAL_UNIVERSE_PATCH_REPORT_2026-06-15.md`
- `11_TRIAGE/HOME_METRIC_AGGREGATION_PATCH_REPORT_2026-06-15.md`
- `11_TRIAGE/NEXT_CODEX_AUDIT_PROMPT_HOME_CANONICAL_UNIVERSE_2026-06-15.md`
- `11_TRIAGE/RUN_PLAN_BUILDER_AUDIT_2026-06-15.md`
- `11_TRIAGE/RUN_PLAN_UI_WIRING_PATCH_AUDIT_2026-06-15.md`
- `11_TRIAGE/RUN_PLAN_UI_WIRING_PATCH_REPORT_2026-06-15.md`
- `11_TRIAGE/WORKTREE_CHECKPOINT_PLAN_2026-06-15.md`
- `11_TRIAGE/UI_AUDITS/`

Related earlier reports/worklists that may be separate history, not necessarily part of these accepted phases:
- `11_TRIAGE/BACKTEST_WORKFLOW_AUDIT_2026-06-13.md`
- `11_TRIAGE/BACKTEST_WORKFLOW_UPDATE_WORKLIST_2026-06-13.md`
- `11_TRIAGE/CODEX_RETASK_REPLACE_DASHBOARD_SHELL_2026-06-14.md`

Memory/handoff files:
- `_AI_MEMORY/ACTIVE_FILES.md`
- `_AI_MEMORY/GLOBAL_HANDOFF.md`
- `_AI_MEMORY/NEXT_STEPS.md`
- `_AI_MEMORY/PROJECT_MEMORY.md`
- `_AI_MEMORY/SESSION_LOG.md`

UI review memory/screenshots:
- `_AI_MEMORY/UI Reviev/ARCHIVE 1/` (shown in status with encoded Turkish characters)
- `_AI_MEMORY/UI Reviev/Ekran goruntusu ... .png`

Checkpoint recommendation:
- Reports and memory updates can be committed last as a documentation/checkpoint bundle.
- Screenshots and archived UI review folders need a size/value decision before inclusion.

## 9. Group G unrelated / needs user decision

Unrelated or needs user decision before commit:
- `../AUDIT_REPORT_CODEX.md`
- `../CHATGPT_MEMORY_PROMPT.md`
- `../Claude rapor.md`
- `../HERMES/`
- `../HERMES_MTC_MEMORY_IMPORT/`
- `../MCC_COMMAND_CENTER/`
- `../Quantlens.md`
- `../Temp/`
- `../YT_TRANSCRIPT_COLLECTOR/`
- `../_HERMES_MEMORY_IMPORT/`
- `03_QUANTLENS/_user_guide/13_GATE_SCORECARD_V2_TR.md`
- `03_QUANTLENS/_user_guide/14_OPTIMIZASYON_SKORLAMA_TR.md`
- `08_DASHBOARD_APP/logs/dashboard_server.log`
- `08_DASHBOARD_APP/run_dashboard_server.ps1`
- old overnight launcher/keep-awake scripts listed in Group D unless separately approved
- bulky UI reference screenshots/zips unless the user wants design evidence tracked
- `_AI_MEMORY/UI Reviev/` screenshot/archive files unless explicitly intended as repo history

## 10. Files that should NOT be committed yet

Do not include in the accepted dashboard/data-contract checkpoint without explicit user decision:
- external/root-level memory migration folders: `../HERMES/`, `../HERMES_MTC_MEMORY_IMPORT/`, `../_HERMES_MEMORY_IMPORT/`
- root-level local notes/prompts: `../AUDIT_REPORT_CODEX.md`, `../CHATGPT_MEMORY_PROMPT.md`, `../Claude rapor.md`, `../Quantlens.md`
- unrelated local folders: `../Temp/`, `../YT_TRANSCRIPT_COLLECTOR/`, `../MCC_COMMAND_CENTER/`
- server runtime log: `08_DASHBOARD_APP/logs/dashboard_server.log`
- dashboard server helper: `08_DASHBOARD_APP/run_dashboard_server.ps1` until reviewed
- Turkish guide drafts: `03_QUANTLENS/_user_guide/13_GATE_SCORECARD_V2_TR.md`, `14_OPTIMIZASYON_SKORLAMA_TR.md`
- old overnight launchers/keep-awake scripts unless checkpointing overnight-run ops
- ignored `03_QUANTLENS/05_BACKTEST_RESULTS/...` sample artifacts unless deliberately force-added
- all Pine, MTC_V2, backtest engine execution, broker/live/paper execution files

## 11. Suggested checkpoint/commit sequence

1. Dashboard UI shell + targeted cleanup
   - Active files: `app.js`, `index.html`, `styles.css`
   - Include staged legacy prototype relocation only if intentional.
   - Include UI reference folders only if design source evidence should live in git.

2. Night artifact reader + schemas
   - `night_artifacts_reader.py`
   - `read_model.py`
   - schema files under `06_SCHEMAS/`
   - `test_night_artifacts_reader.py`
   - `test_readonly_core.py` if its change is the read-model contract update.

3. Run-plan builder
   - `03_QUANTLENS/tools/build_run_plan.py`
   - `tests/test_build_run_plan.py`
   - optionally force-add the exact generated draft plan directory if the sample must be tracked.

4. Run-plan UI wiring + safety patch
   - UI portions in `app.js`
   - run-plan schema safety changes if not already included in checkpoint 2
   - run-plan wiring/safety reports.

5. Home metric aggregation + canonical universe
   - `app.js`
   - `index.html` cache bump
   - `test_home_metric_invariants.py`
   - Home metric/canonical universe reports.

6. Reports and memory updates
   - `11_TRIAGE/*REPORT*.md`
   - accepted audit reports
   - `_AI_MEMORY/ACTIVE_FILES.md`
   - `_AI_MEMORY/GLOBAL_HANDOFF.md`
   - `_AI_MEMORY/NEXT_STEPS.md`
   - `_AI_MEMORY/PROJECT_MEMORY.md`
   - `_AI_MEMORY/SESSION_LOG.md`

## 12. Risk notes

- The staging area is already non-empty. Any commit made without checking staged content will include the prototype relocation.
- `git diff --name-only` does not show untracked or ignored files; use `git status --short` and explicit ignored-file checks for the draft sample plan.
- The active app diff is large because several accepted UI phases accumulated in one worktree.
- Generated sample artifacts are under an ignored backtest-results tree. Force-adding them is a deliberate policy decision.
- UI reference folders include many screenshots/zips/source files. They may be useful for audit provenance but will add bulk.
- Validation is currently green, but any manual staging split should re-run `node --check`, API tests, `/healthz`, `/api/snapshot?refresh=1`, and POST 405 before each final commit/PR.
- No protected Pine/MTC/backtest execution files showed tracked modifications in the protected-path status check.

## 13. Exact commands the user may run manually, but do not run them yourself

Inspect before doing anything:

```powershell
cd C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER
git status --short
git diff --cached --name-status
git diff --name-status
git ls-files --others --exclude-standard
```

If the staged prototype relocation should not be in the next commit:

```powershell
git restore --staged 08_DASHBOARD_APP/apps/web/prototypes 11_TRIAGE/ui_references/legacy_web_prototypes
```

Checkpoint 1, dashboard UI shell + cleanup:

```powershell
git add 08_DASHBOARD_APP/apps/web/app.js 08_DASHBOARD_APP/apps/web/index.html 08_DASHBOARD_APP/apps/web/styles.css
git add -A 08_DASHBOARD_APP/apps/web/prototypes 11_TRIAGE/ui_references/legacy_web_prototypes
git commit -m "Update dashboard strategy intelligence shell"
```

Checkpoint 2, night artifact reader + schemas:

```powershell
git add 08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py
git add 08_DASHBOARD_APP/apps/api/mcc_readonly/night_artifacts_reader.py
git add 08_DASHBOARD_APP/apps/api/tests/test_readonly_core.py
git add 08_DASHBOARD_APP/apps/api/tests/test_night_artifacts_reader.py
git add 06_SCHEMAS/artifact_index.schema.json 06_SCHEMAS/backtest_profile_result.schema.json 06_SCHEMAS/run_plan.schema.json 06_SCHEMAS/run_status.schema.json 06_SCHEMAS/top_results.schema.json
git commit -m "Add read-only night artifact contracts"
```

Checkpoint 3, run-plan builder:

```powershell
git add 03_QUANTLENS/tools/build_run_plan.py
git add 08_DASHBOARD_APP/apps/api/tests/test_build_run_plan.py
git commit -m "Add review-only run plan builder"
```

Optional, only if the ignored sample draft plan should be tracked:

```powershell
git add -f 03_QUANTLENS/05_BACKTEST_RESULTS/draft_run_plan_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-15/run_plan.json
git add -f 03_QUANTLENS/05_BACKTEST_RESULTS/draft_run_plan_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-15/artifact_index.json
git add -f 03_QUANTLENS/05_BACKTEST_RESULTS/draft_run_plan_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-15/run_plan.md
git commit -m "Add review-only draft run plan sample"
```

Checkpoint 4, Home metrics/canonical universe:

```powershell
git add 08_DASHBOARD_APP/apps/web/app.js 08_DASHBOARD_APP/apps/web/index.html
git add 08_DASHBOARD_APP/apps/api/tests/test_home_metric_invariants.py
git commit -m "Use canonical strategy universe on dashboard home"
```

Checkpoint 5, reports and memory:

```powershell
git add 11_TRIAGE/*REPORT*.md
git add 11_TRIAGE/*AUDIT*.md
git add 11_TRIAGE/WORKTREE_CHECKPOINT_PLAN_2026-06-15.md
git add _AI_MEMORY/ACTIVE_FILES.md _AI_MEMORY/GLOBAL_HANDOFF.md _AI_MEMORY/NEXT_STEPS.md _AI_MEMORY/PROJECT_MEMORY.md _AI_MEMORY/SESSION_LOG.md
git commit -m "Record dashboard data-contract checkpoint reports"
```

Validation before final release review:

```powershell
node --check 08_DASHBOARD_APP\apps\web\app.js
cd C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api
$env:PYTHONPATH="."
python -m unittest discover tests
cd C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER
Invoke-WebRequest http://127.0.0.1:8765/healthz -UseBasicParsing
Invoke-WebRequest "http://127.0.0.1:8765/api/snapshot?refresh=1" -UseBasicParsing
try {
  Invoke-WebRequest "http://127.0.0.1:8765/api/snapshot" -Method POST -UseBasicParsing
} catch {
  $_.Exception.Response.StatusCode.value__
}
```
