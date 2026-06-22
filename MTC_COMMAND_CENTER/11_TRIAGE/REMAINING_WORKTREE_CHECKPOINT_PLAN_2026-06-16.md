# Remaining Worktree Checkpoint Plan - 2026-06-16

## Executive summary

Verdict: the payload-performance work is cleanly committed, the index is clean, and the remaining dirty worktree should be split before any native-result/backtest-artifact work continues.

Recent completed commits:

- `3900ec6 Lazy-load scorecard gate details`
- `7ce20ff Slim dashboard snapshot payload`
- `aedded9 Move legacy dashboard prototypes to triage references`

The remaining work is broad and not safe as one review unit. The safest checkpoint order is:

1. Night artifacts reader + schemas.
2. Run-plan builder.
3. Profile-result artifact pilot.
4. Home metrics / canonical universe.
5. Dashboard UI shell / Strategy Intelligence UI.
6. Launcher / single-instance guard.
7. Memory and handoff docs.

Do not stage the dashboard web files as part of the earlier backend/artifact checkpoints unless a reviewer intentionally hunk-stages specific UI wiring. `app.js` is a large interleaved shell rewrite and is best reviewed as one UI checkpoint after the backend contracts are reviewed.

## Current git status summary

Preflight commands were run from `C:\LAB\Tradingview_LAB_CLEAN`.

- `git diff --cached --stat`: empty. Index is clean.
- `git diff --stat`: 10 tracked files changed, 3156 insertions, 5212 deletions.
- Protected-scope diff check for `02_MTC_BACKTEST`, `07_ADAPTERS`, `01_PINE`, and `MTC_V2`: no output.
- Current tracked modified files:
  - `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py`
  - `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_readonly_core.py`
  - `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/app.js`
  - `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/index.html`
  - `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/styles.css`
  - `MTC_COMMAND_CENTER/_AI_MEMORY/ACTIVE_FILES.md`
  - `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md`
  - `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md`
  - `MTC_COMMAND_CENTER/_AI_MEMORY/PROJECT_MEMORY.md`
  - `MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOG.md`

Line-ending warnings appeared for tracked text files: Git reports LF will be replaced by CRLF next time it touches them. Do not mix formatting-only churn into review checkpoints.

## Already completed commits

Group 1 - already committed / should no longer be staged:

- The slim snapshot payload and M1 gate-detail lazy-load payload are already represented by `7ce20ff` and `3900ec6`.
- Legacy prototype relocation is already represented by `aedded9`.
- Do not restage already accepted M1 reports or payload-slim reports unless a future task explicitly reopens them.
- The remaining dirty `test_readonly_core.py` dynamic scorecard-id hunk is post-M1 residue. It should not be silently bundled into unrelated checkpoints; treat it as a user-decision item or a tiny explicit test-hardening follow-up.

## Tracked modified file classification

| File | Remaining hunk summary | Group | Checkpoint | Staging guidance |
| --- | --- | --- | --- | --- |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py` | Imports `build_night_artifacts`, calls it during snapshot build, adds `night_artifacts` to snapshot. | 3 - Night artifacts reader + schemas | A | Whole file is acceptable; current diff is only the night-artifact integration. |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_readonly_core.py` | Changes `/dashboard` title assertion to `Strategy Intelligence Command Center`; changes scorecard-detail test from fixed `GEN_ATR_PULLBACK_TREND` to first live scorecard id. | 2 and 12 | E plus user decision | Requires hunk-based staging. Title belongs with UI shell. Dynamic-id hunk is a separate M1 test-hardening decision. |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/app.js` | Large shell replacement with Strategy Intelligence navigation, canonical home metrics, night-artifact feeds, run-plan UI, backtest result explorer, leaderboard, detail lazy-load usage, and artifact diagnostics. | 2, 3, 5, 6, 7 | Prefer E | Do not whole-file stage with A-D. Hunk staging is high-risk because features are interleaved; prefer one UI checkpoint after A-D contracts are settled. |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/index.html` | Replaces old tabbed dashboard markup with compact app shell/container and footer; title becomes `MTC Strategy Intelligence Command Center`. | 2 - Dashboard UI shell | E | Whole file with UI shell checkpoint. |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/styles.css` | Large dark Strategy Intelligence visual system, nav, panels, metrics, banners, detail sections, artifact/result UI styling. | 2 - Dashboard UI shell | E | Whole file with UI shell checkpoint. |
| `MTC_COMMAND_CENTER/_AI_MEMORY/ACTIVE_FILES.md` | Append-only active sets for M1, payload slim, launcher, profile-result, home metrics, run-plan, night-artifact, and UI work. | 10 - Memory / handoff only | G | Whole file only after code checkpoints are accepted. |
| `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md` | Appended handoff sections for UI work and overnight notes. | 10 - Memory / handoff only | G | Whole file after review for stale/duplicated status. |
| `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md` | Appended night-artifact/live status and completed UI tasks. | 10 - Memory / handoff only | G | Whole file after code checkpoints; verify task tags. |
| `MTC_COMMAND_CENTER/_AI_MEMORY/PROJECT_MEMORY.md` | Small appended project memory note. | 10 - Memory / handoff only | G | Whole file after review. |
| `MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOG.md` | Appended session log entries. | 10 - Memory / handoff only | G | Whole file after review. |

## Untracked file classification

### Group 3 - Night artifacts reader + schemas

Commit A candidates:

- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/night_artifacts_reader.py`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_night_artifacts_reader.py`
- `MTC_COMMAND_CENTER/06_SCHEMAS/artifact_index.schema.json`
- `MTC_COMMAND_CENTER/06_SCHEMAS/backtest_profile_result.schema.json`
- `MTC_COMMAND_CENTER/06_SCHEMAS/run_plan.schema.json`
- `MTC_COMMAND_CENTER/06_SCHEMAS/run_status.schema.json`
- `MTC_COMMAND_CENTER/06_SCHEMAS/top_results.schema.json`
- Relevant `read_model.py` hunk.
- Reports:
  - `MTC_COMMAND_CENTER/11_TRIAGE/BACKTEST_ARTIFACT_READER_INTEGRATION_REPORT_2026-06-15.md`
  - `MTC_COMMAND_CENTER/11_TRIAGE/DASHBOARD_DATA_AVAILABILITY_AUDIT_2026-06-15.md` if accepted as supporting evidence.

Observed contract: the reader is read-only, bounds directory scans and parse size, discovers artifact presence/state, and does not trigger execution.

### Group 4 - Run-plan builder

Commit B candidates:

- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_run_plan.py`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_build_run_plan.py`
- `MTC_COMMAND_CENTER/11_TRIAGE/RUN_PLAN_BUILDER_AUDIT_2026-06-15.md`

Observed contract: the script creates draft/review-only planning artifacts and explicitly does not run backtests or execution. It should still be reviewed separately because it can write files when invoked.

### Group 5 - Run-plan UI wiring

Commit E candidates, or a separate E1 if UI is split:

- Relevant `app.js` render/navigation sections for Backtest Planner and run-plan display.
- `MTC_COMMAND_CENTER/11_TRIAGE/RUN_PLAN_UI_WIRING_PATCH_REPORT_2026-06-15.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/RUN_PLAN_UI_WIRING_PATCH_AUDIT_2026-06-15.md`

Guidance: because `app.js` is interleaved, splitting run-plan UI from the broader shell may not be worth the review risk.

### Group 6 - Profile-result artifact pilot

Commit C candidates:

- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_profile_result_artifact.py`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_build_profile_result_artifact.py`
- `MTC_COMMAND_CENTER/11_TRIAGE/FIRST_PROFILE_RESULT_ARTIFACT_PILOT_REPORT_2026-06-15.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/PROFILE_RESULT_RESEARCH_ONLY_UI_HARDENING_REPORT_2026-06-15.md`
- UI display pieces in `app.js` should wait for Commit E unless intentionally hunk-staged.

Observed contract: the converter reshapes existing deterministic-soak result rows and states that it does not run backtests, optimize, or fabricate metrics.

### Group 7 - Home metrics / canonical universe

Commit D candidates:

- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_home_metric_invariants.py`
- Relevant home/canonical universe aggregation hunks in `app.js`, if reviewers decide to split them from the UI shell.
- `MTC_COMMAND_CENTER/11_TRIAGE/HOME_CANONICAL_UNIVERSE_PATCH_REPORT_2026-06-15.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/HOME_CANONICAL_UNIVERSE_PATCH_AUDIT_2026-06-15.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/HOME_METRIC_AGGREGATION_PATCH_REPORT_2026-06-15.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/NEXT_CODEX_AUDIT_PROMPT_HOME_CANONICAL_UNIVERSE_2026-06-15.md`

Guidance: the invariant test can be its own small checkpoint. The matching UI aggregation in `app.js` is probably safer inside the UI checkpoint unless hunk boundaries are clean.

### Group 8 - Launcher / single-instance guard

Commit F candidates:

- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/run_dashboard_server.ps1`
- `MTC_COMMAND_CENTER/11_TRIAGE/DASHBOARD_LAUNCHER_SINGLE_INSTANCE_PATCH_REPORT_2026-06-15.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/DASHBOARD_LAUNCHER_SINGLE_INSTANCE_PATCH_AUDIT_2026-06-15.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/DASHBOARD_LAUNCHER_SINGLE_INSTANCE_FOLLOWUP_REPORT_2026-06-15.md`

Do not include `MTC_COMMAND_CENTER/08_DASHBOARD_APP/logs/` unless a specific log is requested as evidence.

### Group 9 - Reports only

Reports should travel with their owning checkpoint when they explain that checkpoint. Remaining report-only files:

- `MTC_COMMAND_CENTER/11_TRIAGE/DASHBOARD_TARGETED_PATCH_REPORT_2026-06-15.md` - UI/supporting report.
- `MTC_COMMAND_CENTER/11_TRIAGE/DASHBOARD_UI_INTEGRATION_AUDIT_2026-06-14.md` - UI/supporting report.
- `MTC_COMMAND_CENTER/11_TRIAGE/CODEX_RETASK_REPLACE_DASHBOARD_SHELL_2026-06-14.md` - UI/supporting prompt/report.
- `MTC_COMMAND_CENTER/11_TRIAGE/UI_AUDITS/` - UI audit reports; tiny markdown files, review before inclusion.
- `MTC_COMMAND_CENTER/11_TRIAGE/WORKTREE_CHECKPOINT_PLAN_2026-06-15.md` - older checkpoint plan, likely superseded by this plan unless user wants historical trace.
- `MTC_COMMAND_CENTER/11_TRIAGE/REMAINING_WORKTREE_CHECKPOINT_PLAN_2026-06-16.md` - this plan, report-only.

### Group 10 - Memory / handoff only

Commit G candidates:

- `MTC_COMMAND_CENTER/_AI_MEMORY/ACTIVE_FILES.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/PROJECT_MEMORY.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOG.md`

Guidance: commit after code/reports so the handoff does not claim unaccepted work as landed.

### Group 11 - Local scratch / should not commit

Do not commit without explicit user override:

- `AUDIT_REPORT_CODEX.md`
- `CHATGPT_MEMORY_PROMPT.md`
- `Claude rapor.md`
- `Quantlens.md`
- `HERMES/`
- `HERMES_MTC_MEMORY_IMPORT/`
- `_HERMES_MEMORY_IMPORT/`
- `MCC_COMMAND_CENTER/`
- `Temp/`
- `YT_TRANSCRIPT_COLLECTOR/`
- `tatus --short`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/logs/`
- `MTC_COMMAND_CENTER/_AI_MEMORY/UI Reviev/ARCHIVE 1/`
- `MTC_COMMAND_CENTER/_AI_MEMORY/UI Reviev/*.png`

Rationale: these are local scratch, duplicated workspace/import folders, accidental command-output files, logs, or image evidence. Keep them out of checkpoint commits unless the user explicitly promotes a specific file.

### Group 12 - Needs user decision

Do not commit until the user assigns ownership:

- `MTC_COMMAND_CENTER/03_QUANTLENS/_user_guide/13_GATE_SCORECARD_V2_TR.md`
- `MTC_COMMAND_CENTER/03_QUANTLENS/_user_guide/14_OPTIMIZASYON_SKORLAMA_TR.md`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/night_1m_2026-06-07.sh`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/overnight_loop_2026-06-08.sh`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/start_night_1m_2026-06-07_keepawake.ps1`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/start_night_3M_2026-06-08_keepawake.ps1`
- `MTC_COMMAND_CENTER/11_TRIAGE/BACKTEST_WORKFLOW_AUDIT_2026-06-13.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/BACKTEST_WORKFLOW_UPDATE_WORKLIST_2026-06-13.md`
- The dynamic-id hunk in `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_readonly_core.py`.

Rationale: the Turkish guide docs and run/overnight launcher scripts may be useful, but they are not part of the clean A-G checkpoint chain. The backtest workflow reports are related to future native-result/backtest artifact work and should not ride along with dashboard cleanup unless explicitly selected.

### Group 13 - Unknown / inspect manually

- `MTC_COMMAND_CENTER/11_TRIAGE/ui_references/google_strategy_intelligence_v2_final/`
- `MTC_COMMAND_CENTER/11_TRIAGE/ui_references/strategy_intelligence_lovable/`

Likely UI reference/evidence material for Commit E, but these directories contain many assets/screenshots and should be manually reviewed for size, relevance, and duplication before committing.

## Recommended checkpoint order

### Commit A - Night artifacts reader + schemas

Purpose: add the read-only `night_artifacts` snapshot contract and schema validation surface.

Include:

- `night_artifacts_reader.py`
- five schema files under `06_SCHEMAS`
- `test_night_artifacts_reader.py`
- `read_model.py`
- optional supporting reports.

Do not include:

- `app.js`, `index.html`, `styles.css`
- run-plan/profile-result builder scripts
- logs or launcher scripts

### Commit B - Run-plan builder

Purpose: add the review-only run-plan artifact builder and tests.

Include:

- `build_run_plan.py`
- `test_build_run_plan.py`
- run-plan builder report.

Do not run the builder unless a later task explicitly allows generating artifacts.

### Commit C - Profile-result artifact pilot

Purpose: add the read-only converter for existing result rows into profile-separated result artifacts.

Include:

- `build_profile_result_artifact.py`
- `test_build_profile_result_artifact.py`
- profile-result pilot reports.

Do not run the converter unless a later task explicitly allows generating artifacts.

### Commit D - Home metrics / canonical universe

Purpose: protect canonical strategy-universe counts and prevent raw scorecard-row inflation.

Include:

- `test_home_metric_invariants.py`
- related home/canonical reports.
- Optionally hunk-stage matching `app.js` home aggregation only if the hunk is isolated and reviewed.

### Commit E - Dashboard UI shell / Strategy Intelligence UI

Purpose: replace the old dashboard shell with the Strategy Intelligence UI and wire the read-only artifact display.

Include:

- `app.js`
- `index.html`
- `styles.css`
- UI reports and selected UI references after manual review.

Validation should be heavier here because this is the largest and riskiest diff.

### Commit F - Launcher / single-instance guard

Purpose: add the dashboard server launcher with single-instance and bounded log behavior.

Include:

- `run_dashboard_server.ps1`
- launcher patch/audit/follow-up reports.

Exclude:

- `logs/`

### Commit G - Memory / handoff docs

Purpose: reconcile project memory with what actually landed.

Include:

- `_AI_MEMORY/*.md`

Review first for stale claims, model-name/date header format, and task tags.

## Files not to commit

Keep these out of normal checkpoint commits:

- Root scratch docs: `AUDIT_REPORT_CODEX.md`, `CHATGPT_MEMORY_PROMPT.md`, `Claude rapor.md`, `Quantlens.md`.
- Scratch/import/duplicate folders: `HERMES/`, `HERMES_MTC_MEMORY_IMPORT/`, `_HERMES_MEMORY_IMPORT/`, `MCC_COMMAND_CENTER/`, `Temp/`, `YT_TRANSCRIPT_COLLECTOR/`.
- Accidental file: `tatus --short`.
- Logs: `MTC_COMMAND_CENTER/08_DASHBOARD_APP/logs/`.
- UI screenshots and archived UI review evidence under `MTC_COMMAND_CENTER/_AI_MEMORY/UI Reviev/`, unless a specific evidence pack is explicitly approved.

## Files needing user decision

- Turkish guide docs under `03_QUANTLENS/_user_guide/`: decide whether these are canonical docs, draft docs, or local notes.
- Overnight shell/keepawake scripts under `03_QUANTLENS/tools/`: decide whether they are reusable operational scripts or run-local scratch.
- `BACKTEST_WORKFLOW_AUDIT_2026-06-13.md` and `BACKTEST_WORKFLOW_UPDATE_WORKLIST_2026-06-13.md`: decide whether they belong to the future native-result/backtest artifact workstream.
- `WORKTREE_CHECKPOINT_PLAN_2026-06-15.md`: decide whether to keep as historical checkpoint evidence or supersede with this report.
- `ui_references/google_strategy_intelligence_v2_final/` and `ui_references/strategy_intelligence_lovable/`: decide whether full asset directories are needed or only selected screenshots/docs.
- `test_readonly_core.py` dynamic-id hunk: decide whether to keep as a tiny M1 robustness follow-up or leave it out of the remaining checkpoint chain.

## Validation plan per checkpoint

General rules:

- No backtests.
- No optimization.
- No Pine edits.
- No MTC_V2 edits.
- No broker/live/paper execution.
- No API write behavior changes.
- Before every checkpoint review, run `git diff --cached --stat` and ensure only intended files are staged.
- After every checkpoint review, run protected-scope check:
  - `git diff --name-only -- MTC_COMMAND_CENTER/02_MTC_BACKTEST MTC_COMMAND_CENTER/07_ADAPTERS MTC_COMMAND_CENTER/01_PINE MTC_COMMAND_CENTER/MTC_V2`

Commit A validation:

- `python -m unittest discover MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests`
- `Invoke-WebRequest http://127.0.0.1:8765/api/snapshot?refresh=1 -UseBasicParsing -TimeoutSec 90`
- Verify `night_artifacts` exists and remains read-only/missing-safe.

Commit B validation:

- `python -m unittest MTC_COMMAND_CENTER.08_DASHBOARD_APP.apps.api.tests.test_build_run_plan` if import path supports it, otherwise use discovery from API app root.
- Static review that script does not run backtests and only writes planning artifacts when invoked.
- Do not execute the builder unless artifact generation is explicitly allowed.

Commit C validation:

- `python -m unittest MTC_COMMAND_CENTER.08_DASHBOARD_APP.apps.api.tests.test_build_profile_result_artifact` if import path supports it, otherwise use discovery from API app root.
- Static review that converter only reshapes existing source data and does not calculate/fabricate KPIs.
- Do not execute the converter unless artifact generation is explicitly allowed.

Commit D validation:

- Run the home metric invariant test.
- If UI aggregation hunks are included, run `node --check MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js`.

Commit E validation:

- `node --check MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js`
- API unittest discovery from `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api`.
- Browser/manual smoke for `/dashboard`, core nav routes, strategy detail lazy-load, empty/error states, artifact pages, and responsive layout.
- Confirm no API write endpoint or strategy logic changed.

Commit F validation:

- Static PowerShell syntax/parser check.
- `-StatusOnly` dry read check only if allowed; do not kill or start processes during an audit-only pass.
- Confirm logs remain untracked.

Commit G validation:

- Read changed memory sections for accuracy after A-F are accepted.
- Confirm `NEXT_STEPS.md` tasks use `[AI: ...]` tags.
- Confirm `GLOBAL_HANDOFF.md` new headers use `## [MODEL_NAME] YYYY-MM-DD - Topic` style.

## Risks if committed as one large batch

- Reviewers cannot distinguish read-only schema/reader work from UI shell work.
- `app.js` mixes artifact display, run-plan display, home metrics, leaderboards, and Strategy Intelligence routing, making regression attribution hard.
- Memory docs could claim unaccepted or partially reviewed work as landed.
- Local scratch and logs could be accidentally preserved.
- User-decision files could become canonical without explicit approval.
- Future native-result/backtest artifact work would inherit an unclear base and make later audits more expensive.

## Recommended next action

Proceed with Commit A as the next review unit only: night artifacts reader + schemas + its direct snapshot integration + its tests + directly relevant report(s).

Before staging Commit A, explicitly exclude `app.js`, `index.html`, `styles.css`, memory docs, logs, scratch folders, overnight launcher scripts, Turkish guide docs, and the dynamic-id hunk in `test_readonly_core.py`.
