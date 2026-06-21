# Worktree Closure Plan - 2026-06-21

## Scope

This plan classifies the current dirty/untracked worktree for GitHub-based handoff preparation. It does not stage or commit any pre-existing dirty work. Existing dirty items remain separated from the new protocol-doc commit.

## Preflight Result

- Branch: `master`
- Upstream state at preflight: `master...origin/master [ahead 50]`
- Index state at preflight: empty
- Protected action constraints: no backtests, optimizations, new trading artifacts, `top_results.json`, Pine, MTC_V2, broker/live/paper execution logic, backtest engine execution logic, or strategy logic changes.

## Bucket Summary

- A. Commit now: new handoff protocol/setup files from this session, plus selected pre-existing report docs that look useful but should be committed only in separate reviewed units.
- B. Ignore via `.gitignore`: generated/local noise, logs, temp folders, accidental command-output files.
- C. Leave for user decision: broad modified source/memory files, scripts, tests, local handoff folders, large UI references, screenshots, and ambiguous project folders.
- D. Do not touch: no `.env`, key, credential, or explicit secret file was visible in the current status output.

## A. Commit Now

These files are useful repo state. For this session, only the new handoff protocol/setup files should be staged in the protocol commit. Pre-existing report docs should be committed later only after exact review.

| Path | Status | Size | Reason | Proposed action | Risk |
|---|---:|---:|---|---|---|
| `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CHATGPT_WEB_MENTOR_WORKFLOW.md` | `??` | new | Requested permanent protocol doc. | Stage in protocol commit. | low |
| `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/AGENT_HANDOFF_BUNDLE_PROTOCOL.md` | `??` | new | Requested permanent protocol doc. | Stage in protocol commit. | low |
| `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLEAN_WORKTREE_AND_PUSH_PROTOCOL.md` | `??` | new | Requested permanent protocol doc. | Stage in protocol commit. | low |
| `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/SCREENSHOT_AND_UI_REVIEW_PROTOCOL.md` | `??` | new | Requested permanent protocol doc. | Stage in protocol commit. | low |
| `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/NO_PROMOTION_SAFETY_RULES.md` | `??` | new | Requested permanent safety doc. | Stage in protocol commit. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/HANDOFF_TEMPLATE/CHATGPT_HANDOFF_TEMPLATE.md` | `??` | new | Requested ChatGPT handoff template. | Stage in protocol commit. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/ui_snapshots/latest/.gitkeep` | `??` | new | Requested screenshot folder placeholder. | Stage in protocol commit. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/ui_snapshots/archive/.gitkeep` | `??` | new | Requested screenshot folder placeholder. | Stage in protocol commit. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/WORKTREE_CLOSURE_PLAN_2026-06-21.md` | `??` | new | Requested worktree closure classification. | Stage in protocol commit. | low |
| `MTC_COMMAND_CENTER/README.md` | `M` | 1.9 KB | Small requested pointer to protocol folder. | Stage only README hunk in protocol commit. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/BACKTEST_WORKFLOW_AUDIT_2026-06-13.md` | `??` | 34.1 KB | Looks like a durable audit report. | Commit later in a separate report/docs unit after review. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/BACKTEST_WORKFLOW_UPDATE_WORKLIST_2026-06-13.md` | `??` | 5.4 KB | Looks like a durable worklist report. | Commit later in a separate report/docs unit after review. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/CODEX_RETASK_REPLACE_DASHBOARD_SHELL_2026-06-14.md` | `??` | 3.6 KB | Looks like a durable retask/audit prompt. | Commit later in a separate report/docs unit after review. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/DASHBOARD_DATA_AVAILABILITY_AUDIT_2026-06-15.md` | `??` | 40.0 KB | Looks like a durable dashboard audit report. | Commit later in a separate report/docs unit after review. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/DASHBOARD_LAUNCHER_SINGLE_INSTANCE_FOLLOWUP_REPORT_2026-06-15.md` | `??` | 5.4 KB | Looks like a durable implementation report. | Commit later in a separate report/docs unit after review. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/DASHBOARD_LAUNCHER_SINGLE_INSTANCE_PATCH_AUDIT_2026-06-15.md` | `??` | 8.4 KB | Looks like a durable audit report. | Commit later in a separate report/docs unit after review. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/DASHBOARD_LAUNCHER_SINGLE_INSTANCE_PATCH_REPORT_2026-06-15.md` | `??` | 9.1 KB | Looks like a durable implementation report. | Commit later in a separate report/docs unit after review. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/DASHBOARD_TARGETED_PATCH_REPORT_2026-06-15.md` | `??` | 7.3 KB | Looks like a durable patch report. | Commit later in a separate report/docs unit after review. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/DASHBOARD_UI_INTEGRATION_AUDIT_2026-06-14.md` | `??` | 5.5 KB | Looks like a durable UI audit report. | Commit later in a separate report/docs unit after review. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/FIRST_PROFILE_RESULT_ARTIFACT_PILOT_REPORT_2026-06-15.md` | `??` | 7.7 KB | Looks like a durable pilot report. | Commit later in a separate report/docs unit after review. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/HOME_CANONICAL_UNIVERSE_PATCH_AUDIT_2026-06-15.md` | `??` | 5.8 KB | Looks like a durable audit report. | Commit later in a separate report/docs unit after review. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/HOME_CANONICAL_UNIVERSE_PATCH_REPORT_2026-06-15.md` | `??` | 8.9 KB | Looks like a durable implementation report. | Commit later in a separate report/docs unit after review. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/HOME_METRIC_AGGREGATION_PATCH_REPORT_2026-06-15.md` | `??` | 7.6 KB | Looks like a durable implementation report. | Commit later in a separate report/docs unit after review. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/NATIVE_RESULT_SOURCE_DISCOVERY_2026-06-16.md` | `??` | 14.5 KB | Looks like a durable discovery report. | Commit later in a separate report/docs unit after review. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/NEXT_CODEX_AUDIT_PROMPT_HOME_CANONICAL_UNIVERSE_2026-06-15.md` | `??` | 3.2 KB | Looks like a durable audit prompt. | Commit later in a separate report/docs unit after review. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_REPO_STATUS_2026-06-17.md` | `??` | 2.1 KB | Looks like a durable status report. | Commit later in a separate report/docs unit after review. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/PROFILE_RESULT_RESEARCH_ONLY_UI_HARDENING_REPORT_2026-06-15.md` | `??` | 6.2 KB | Looks like a durable implementation report. | Commit later in a separate report/docs unit after review. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/REMAINING_WORKTREE_CHECKPOINT_PLAN_2026-06-16.md` | `??` | 20.4 KB | Looks like a durable checkpoint plan. | Commit later in a separate report/docs unit after review. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/REPOSITORY_NATIVE_RESULT_READINESS_AUDIT_2026-06-16.md` | `??` | 23.7 KB | Looks like a durable readiness audit. | Commit later in a separate report/docs unit after review. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/RUN_PLAN_BUILDER_AUDIT_2026-06-15.md` | `??` | 16.0 KB | Looks like a durable audit report. | Commit later in a separate report/docs unit after review. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/RUN_PLAN_UI_WIRING_PATCH_AUDIT_2026-06-15.md` | `??` | 8.6 KB | Looks like a durable audit report. | Commit later in a separate report/docs unit after review. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/RUN_PLAN_UI_WIRING_PATCH_REPORT_2026-06-15.md` | `??` | 6.2 KB | Looks like a durable implementation report. | Commit later in a separate report/docs unit after review. | low |
| `MTC_COMMAND_CENTER/11_TRIAGE/WORKTREE_CHECKPOINT_PLAN_2026-06-15.md` | `??` | 15.7 KB | Looks like a durable checkpoint plan. | Commit later in a separate report/docs unit after review. | low |

## B. Ignore via `.gitignore`

These look generated, local-only, or accidental.

| Path | Status | Size | Reason | Proposed action | Risk |
|---|---:|---:|---|---|---|
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/logs/` | `??` | 77.1 KB | Local dashboard logs. | Add/confirm ignore rule; do not commit log contents. | low |
| `Temp/` | `??` | 1.5 MB | Local temp folder. | Add/confirm ignore rule or leave local-only. | low |
| `tatus --short` | `??` | 379 B | Accidental command-output file. | Delete or ignore after user approval; do not commit. | low |

## C. Leave for User Decision

These are useful-looking or large but not safe to stage in this protocol commit without a separate exact review.

| Path | Status | Size | Reason | Proposed action | Risk |
|---|---:|---:|---|---|---|
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_readonly_core.py` | `M` | 11.1 KB | Modified test file from prior dashboard work. | Review as part of dashboard unit before commit. | medium |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/app.js` | `M` | 125.3 KB | Large modified dashboard source. | Review as part of dashboard unit before commit. | high |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/index.html` | `M` | 1.6 KB | Modified dashboard shell. | Review as part of dashboard unit before commit. | medium |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/styles.css` | `M` | 36.9 KB | Large modified dashboard CSS. | Review as part of dashboard unit before commit. | high |
| `MTC_COMMAND_CENTER/_AI_MEMORY/ACTIVE_FILES.md` | `M` | 27.7 KB | Modified memory/handoff state. | Review with related session logs before commit. | medium |
| `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md` | `M` | 158.8 KB | Large modified handoff log. | Review exact appended sections before commit. | medium |
| `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md` | `M` | 104.2 KB | Large modified task log. | Review exact appended sections before commit. | medium |
| `MTC_COMMAND_CENTER/_AI_MEMORY/PROJECT_MEMORY.md` | `M` | 3.7 KB | Modified stable memory file. | Review for durable-fact correctness before commit. | medium |
| `MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOG.md` | `M` | 85.9 KB | Modified session log. | Review exact appended lines before commit. | medium |
| `AUDIT_REPORT_CODEX.md` | `??` | 7.0 KB | Root scratch/report file; location ambiguous. | Move into proper triage/report folder or leave for user decision. | medium |
| `CHATGPT_MEMORY_PROMPT.md` | `??` | 3.1 KB | Root prompt file; location ambiguous. | Move into proper handoff/protocol folder or leave for user decision. | medium |
| `Claude rapor.md` | `??` | 2.1 KB | Root report file with nonstandard name/location. | Rename/move only with user decision. | medium |
| `HERMES/` | `??` | 114.6 KB | Unknown local/project folder. | Review contents before deciding commit or ignore. | medium |
| `HERMES_MTC_MEMORY_IMPORT/` | `??` | 17.6 KB | Local handoff/import folder; unclear durability. | Review contents before deciding commit or ignore. | medium |
| `MCC_COMMAND_CENTER/` | `??` | 8.8 KB | Looks like possible typo/duplicate command-center folder. | Inspect before delete, move, or commit. | high |
| `MTC_COMMAND_CENTER/03_QUANTLENS/_user_guide/13_GATE_SCORECARD_V2_TR.md` | `??` | 17.5 KB | Turkish guide doc; useful but not part of this protocol commit. | User decides whether to commit and whether English companion is needed. | medium |
| `MTC_COMMAND_CENTER/03_QUANTLENS/_user_guide/14_OPTIMIZASYON_SKORLAMA_TR.md` | `??` | 13.6 KB | Turkish guide doc; useful but not part of this protocol commit. | User decides whether to commit and whether English companion is needed. | medium |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_profile_result_artifact.py` | `??` | 12.8 KB | New tool script in QuantLens workflow. | Review tests and scope before commit. | medium |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_run_plan.py` | `??` | 17.5 KB | New tool script in QuantLens workflow. | Review tests and scope before commit. | medium |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/night_1m_2026-06-07.sh` | `??` | 7.6 KB | Backtest/overnight launcher script. | Commit only after backtest workflow review; do not run now. | high |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/overnight_loop_2026-06-08.sh` | `??` | 7.2 KB | Backtest/overnight launcher script. | Commit only after backtest workflow review; do not run now. | high |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/start_night_1m_2026-06-07_keepawake.ps1` | `??` | 1.7 KB | Keep-awake launcher script. | Commit only with related overnight workflow unit. | high |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/start_night_3M_2026-06-08_keepawake.ps1` | `??` | 1.8 KB | Keep-awake launcher script. | Commit only with related overnight workflow unit. | high |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_build_profile_result_artifact.py` | `??` | 8.1 KB | New test for untracked tool. | Review with matching tool before commit. | medium |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_build_run_plan.py` | `??` | 5.8 KB | New test for untracked tool. | Review with matching tool before commit. | medium |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_home_metric_invariants.py` | `??` | 6.1 KB | New dashboard invariant test. | Review with dashboard unit before commit. | medium |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/run_dashboard_server.ps1` | `??` | 7.4 KB | Dashboard launcher script. | Review launcher behavior before commit. | medium |
| `MTC_COMMAND_CENTER/11_TRIAGE/UI_AUDITS/` | `??` | 151.4 KB | Folder of UI audit material; exact contents not reviewed here. | Review contents; commit selected reports only. | medium |
| `MTC_COMMAND_CENTER/11_TRIAGE/ui_references/google_strategy_intelligence_v2_final/` | `??` | 5.0 MB | Large UI reference set. | User decides whether to commit selected references or keep in handoff bundle. | medium |
| `MTC_COMMAND_CENTER/11_TRIAGE/ui_references/strategy_intelligence_lovable/` | `??` | 4.4 MB | Large UI reference set. | User decides whether to commit selected references or keep in handoff bundle. | medium |
| `MTC_COMMAND_CENTER/_AI_MEMORY/UI Reviev/ARCHIVE 1/` | `??` | 1.1 MB | Screenshot/archive folder; large and not clearly curated. | User decides whether to move selected images to `ui_snapshots`. | medium |
| `MTC_COMMAND_CENTER/_AI_MEMORY/UI Reviev/Ekran görüntüsü 2026-06-07 211721.png` | `??` | 235.0 KB | Screenshot; not clearly latest/curated for protocol. | User decides whether to copy curated version to `ui_snapshots`. | medium |
| `MTC_COMMAND_CENTER/_AI_MEMORY/UI Reviev/Ekran görüntüsü 2026-06-07 211746.png` | `??` | 204.1 KB | Screenshot; not clearly latest/curated for protocol. | User decides whether to copy curated version to `ui_snapshots`. | medium |
| `MTC_COMMAND_CENTER/_AI_MEMORY/UI Reviev/Ekran görüntüsü 2026-06-07 211806.png` | `??` | 160.5 KB | Screenshot; not clearly latest/curated for protocol. | User decides whether to copy curated version to `ui_snapshots`. | medium |
| `MTC_COMMAND_CENTER/_AI_MEMORY/UI Reviev/Ekran görüntüsü 2026-06-07 211857.png` | `??` | 217.2 KB | Screenshot; not clearly latest/curated for protocol. | User decides whether to copy curated version to `ui_snapshots`. | medium |
| `MTC_COMMAND_CENTER/_AI_MEMORY/UI Reviev/Ekran görüntüsü 2026-06-07 211911.png` | `??` | 192.0 KB | Screenshot; not clearly latest/curated for protocol. | User decides whether to copy curated version to `ui_snapshots`. | medium |
| `Quantlens.md` | `??` | 9.6 KB | Root scratch/report file; location ambiguous. | Move into proper docs/report location or leave for user decision. | medium |
| `YT_TRANSCRIPT_COLLECTOR/` | `??` | 18.3 MB | Large utility/project folder. | Review as its own commit unit or keep local; do not stage in protocol commit. | high |
| `_HERMES_MEMORY_IMPORT/` | `??` | 7.8 KB | Local handoff/import folder; unclear durability. | Review contents before deciding commit or ignore. | medium |

## D. Do Not Touch

No dirty `.env`, key, token, credential, broker config, or explicit secret file was visible in the current status output. If such files appear in later status checks, classify them here and do not stage them.

## Recommended Next Actions

1. Commit only the protocol/setup files from this session.
2. Push the branch so the existing 50 ahead commits plus the new protocol commit reach GitHub.
3. Create and commit the final setup report separately.
4. In a later cleanup session, review Bucket A report docs as one or more exact staged sets.
5. Treat Bucket C as user-decision work; do not stage it casually.
6. Add ignore rules for Bucket B only after confirming no useful local evidence is being hidden.
