# Backtest Workflow Update Worklist - 2026-06-13

## P0 - Must Update First

| Order | File | Change |
|---:|---|---|
| 1 | `06_SCHEMAS/run_plan.schema.json` | Add the durable launch-plan contract. |
| 2 | `06_SCHEMAS/run_status.schema.json` | Add approval/smoke/running/completed/failed state contract. |
| 3 | `06_SCHEMAS/backtest_profile_result.schema.json` | Add SOURCE_NAKED/RISK_NORMALIZED/MTC_LIGHT/FULL_MTC_CANDIDATE result envelope. |
| 4 | `03_QUANTLENS/tools/build_run_plan.py` | New deterministic planner that writes `run_plan.json` and `run_plan.md` without launching. |
| 5 | `08_DASHBOARD_APP/apps/api/mcc_readonly/run_plan_reader.py` | New read-only plan reader for the dashboard snapshot. |
| 6 | `08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py` | Add a `backtest_launch` / `run_plans` snapshot key. |
| 7 | `03_QUANTLENS/tools/night_runner.sh` | Require an approved plan before full execution. |
| 8 | `04_SHARED/prompts/05_ai_workflow/08_backtest_launch.md` | Change prompt from launch-capable to plan-first/approval-gated. |
| 9 | `11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md` | Update operational flow: plan -> approval -> smoke -> execution -> artifacts. |
| 10 | `03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md` | Add profiles, fair comparison, sizing/leverage rules. |
| 11 | `08_DASHBOARD_APP/apps/web/app.js` | Add Backtest Plan & Evidence preview to Strategy Intelligence Page and Launch Center read model rendering. |

## P1 - Should Update Next

| File | Change |
|---|---|
| `06_SCHEMAS/progress.schema.json` | Add progress monitor contract. |
| `06_SCHEMAS/artifact_index.schema.json` | Add canonical artifact inventory contract. |
| `06_SCHEMAS/backtest_status.schema.json` | Tighten or reference new status/progress/artifact schemas. |
| `03_QUANTLENS/tools/mcc_night_tail.sh` | Write/update `artifact_index.json` during validation tail. |
| `03_QUANTLENS/tools/single_strategy_backtest.py` | Use the same plan/status/profile flow for single-strategy runs. |
| `03_QUANTLENS/tools/build_needs_backtest_selector.py` | Feed planner and include default profile recommendations. |
| `03_QUANTLENS/tools/build_evaluation_artifact.py` | Preserve profile, sizing, leverage, and cost metadata. |
| `03_QUANTLENS/tools/score_all_gates.py` | Carry profile metadata into `scorecard_v2`. |
| `08_DASHBOARD_APP/apps/api/mcc_readonly/backtest_reader.py` | Merge plan/status/progress/artifact-index data into run rows. |
| `08_DASHBOARD_APP/apps/api/mcc_readonly/heartbeat_reader.py` | Prefer per-run heartbeat/progress over newest global heartbeat only. |
| `08_DASHBOARD_APP/apps/api/mcc_readonly/scorecard_reader.py` | Normalize profile and artifact links on scorecards. |
| `08_DASHBOARD_APP/apps/web/index.html` | Add containers/nav if Launch Center/Monitor/Explorer become separate screens. |
| `08_DASHBOARD_APP/apps/web/styles.css` | Add compact styles for plan tables, approval states, progress, and artifact index. |
| `02_MTC_BACKTEST/src/cli/mtc_engine_validate.py` | Emit MTC_LIGHT-compatible profile result/artifact index. |
| `08_DASHBOARD_APP/apps/api/tests/` | Add schema/reader tests for plans/status/progress/artifacts. |

## P2 - Nice To Have / Later

| File | Change |
|---|---|
| `03_QUANTLENS/tools/overnight_v2_runner.py` | Expose grid metadata/reasons without executing the runner. |
| `03_QUANTLENS/tools/strat_extra_runner.py` | Same grid metadata export for extra strategies. |
| `02_MTC_BACKTEST/src/config/profiles/light_risk.py` | Document as the implementation of MTC_LIGHT; avoid behavior changes unless approved. |
| `04_SHARED/prompts/05_ai_workflow/00_index.md` | Link plan-first backtest flow. |
| `_AI_MEMORY/AI_RULES.md` | Add a short rule that backtests require plan artifacts and approval. |
| `_AI_MEMORY/GLOBAL_HANDOFF.md` | Update after approved implementation only. |
| `_AI_MEMORY/NEXT_STEPS.md` | Add AI-tagged implementation tasks after approval only. |
| `_AI_MEMORY/SESSION_LOG.md` | Log implementation after approval only. |
| `11_TRIAGE/lessons_archive/OVERNIGHT_LESSONS_INDEX.md` | Add lesson link after implementation or owner approval. |

## Suggested Implementation Order

1. Add schemas and fixtures first.
2. Add `build_run_plan.py` and make it produce both JSON and Markdown from current selector/registry/grid data.
3. Add read-only `run_plan_reader.py` and wire it into `read_model.py`.
4. Add UI plan preview in Strategy Intelligence Page Section 3.
5. Add Backtest Launch Center as read-only plan display.
6. Update `night_runner.sh` to require approved plan before full execution.
7. Add `progress.json` and `artifact_index.json` writers/readers.
8. Update docs/prompts to make the artifact path mandatory.
9. Add tests and run `python -m unittest discover`, `node --check app.js`, and schema validation.

## Files Requiring User Approval Before Modification

- Any change that alters trading logic, signal behavior, stop/target behavior, sizing behavior, Pine logic, MTC strategy behavior, parity files, or `MTC_V2.pine`.
- `03_QUANTLENS/tools/mega_walk_forward.py` if the change goes beyond output-only metadata/progress writing.
- `02_MTC_BACKTEST/src/modules/risk/position_sizer.py` and MTC risk defaults if behavior changes are proposed.
- `02_MTC_BACKTEST/src/engine/mtc_runner.py`.
- Any Pine file or parity oracle.
- Any dashboard write-back/approval mechanism, because current hard constraint says MCC dashboard is read-only.

