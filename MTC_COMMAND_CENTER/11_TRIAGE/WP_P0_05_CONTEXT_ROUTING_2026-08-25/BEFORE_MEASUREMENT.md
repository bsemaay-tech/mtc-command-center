# WP-P0-05 BEFORE Baseline — Mandatory AI-Onboarding Reading Burden

Measured: 2026-08-25 (Europe/Chisinau)  
Repository worktree: `C:\WPP009_20260825`  
Local `master`: `46f5bafbf82f3366c8bc7ee08f6f0eee08d46138`  
Worktree HEAD: `861dfc620d0634b5e151128e8b5c53cd7c2d8394` (`feature/wp-p0-09-capability-table-20260825`)

The onboarding files measured below have no diff against local `master`; therefore the byte/line figures are the current-master baseline even though the worktree itself is on a feature branch. Existing unrelated worktree modifications were not read as inputs, changed, staged, or otherwise touched.

## Method and classification

- **Bytes:** filesystem length.
- **Lines:** `.NET File.ReadAllLines(path).Count`.
- **Approx. tokens:** `ceil(bytes / 4)`, exactly the requested estimator. Aggregate token figures use `ceil(aggregate bytes / 4)`, so they can differ slightly from sums of individually rounded rows.
- **ALWAYS-LOAD:** explicitly in the fresh-agent/read-order chain without a task condition. `GLOBAL_HANDOFF.md` is counted at full file size even though `START_HERE.md` narrows the initial read to its newest top sections; this is a conservative whole-file burden, not a claim that every historical line must be loaded.
- **TASK-CLASS-SPECIFIC:** the chain names the file only for a job, gate, trigger, working-set condition, or project handoff.
- **HISTORY:** explicitly described as historical/back-context only.
- References that merely say a file exists, preserves an old record, or is an output to write were not turned into reading burden. Generated run/variant registries that the chain instructs an agent to update rather than pre-read are likewise excluded unless separately included by an explicit read-order sentence.

## Summary

| Burden / task class | Incremental bytes beyond ALWAYS-LOAD | Incremental approx. tokens | Total bytes including ALWAYS-LOAD | Total approx. tokens including ALWAYS-LOAD | Scenario boundary |
|---|---:|---:|---:|---:|---|
| **ALWAYS-LOAD baseline** | — | — | **672,863** | **168,216** | Root entry chain plus fresh-agent safety reads |
| Research run | 279,333 | 69,834 | 952,196 | 238,049 | Full strategy-research session that proceeds to a backtest: both mandatory backtest pre-reads, launch prompt, data inventory, strategy inventories/workflow/checklist, and QuantLens handoffs |
| Bridge work | 56,146 | 14,037 | 729,009 | 182,253 | Bridge work that designs or audits an executable check/block/preregistration; the chain provides no general Bridge-local onboarding file, so the explicit design-defect prerequisite is the only Bridge-specific increment |
| Planning | 94,013 | 23,504 | 766,876 | 191,719 | Gate-1/Gate-2 planning/dispatch: sprint workflow, prompt index, scope and engineering-plan prompts, executable-check defect catalogue, and model-routing index |
| Git/handoff | 124,973 | 31,244 | 797,836 | 199,459 | Write-session close-out: handoff prompt, active-set/decision records, and write-lock table; conditional “if changed” files are included for a full close-out |

The task-class totals are deliberately scenario totals, not claims that every task in the class always needs every conditional file. For example, pure Bridge documentation that does not design/audit an executable check does not trigger the 56,146-byte defect catalogue; a backtest that does not combine strategies does not trigger the strategy-research inventory block.

## Per-file inventory

| # | Path | Bytes | Lines | Approx. tokens | Classification / task class | Chain sentence that makes the read mandatory or conditional |
|---:|---|---:|---:|---:|---|---|
| 1 | `CLAUDE.md` | 524 | 6 | 131 | ALWAYS-LOAD | Repository entrypoint itself; it begins: “Read `AGENTS.md` first. Then read `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`.” |
| 2 | `AGENTS.md` | 30,905 | 295 | 7,727 | ALWAYS-LOAD | `CLAUDE.md`: “Read `AGENTS.md` first.” |
| 3 | `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md` | 6,881 | 66 | 1,721 | ALWAYS-LOAD | `AGENTS.md`: “Read this file first, then read `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`.” |
| 4 | `MTC_COMMAND_CENTER/_AI_MEMORY/LESSONS.md` | 7,697 | 110 | 1,925 | ALWAYS-LOAD | `START_HERE.md`: “Read order: `AGENTS.md`, this file, `LESSONS.md` (capped, 2-min read — durable paid-for rules), `AI_RULES.md`, `PROJECT_MEMORY.md`, `GLOBAL_HANDOFF.md` if needed, `NEXT_STEPS.md`, then project handoff files.” |
| 5 | `MTC_COMMAND_CENTER/_AI_MEMORY/AI_RULES.md` | 11,527 | 176 | 2,882 | ALWAYS-LOAD | Same `START_HERE.md` read-order sentence; `AI_RULES.md` also says it is read “after `AGENTS.md` and `START_HERE.md`.” |
| 6 | `MTC_COMMAND_CENTER/_AI_MEMORY/PROJECT_MEMORY.md` | 7,690 | 130 | 1,923 | ALWAYS-LOAD | Same `START_HERE.md` read-order sentence. |
| 7 | `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md` | 258,810 | 3,463 | 64,703 | ALWAYS-LOAD | `START_HERE.md`: “**CURRENT STATE: read `_AI_MEMORY/GLOBAL_HANDOFF.md` (newest section first) + `NEXT_STEPS.md` for live work.**” |
| 8 | `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md` | 347,520 | 4,060 | 86,880 | ALWAYS-LOAD | `START_HERE.md`: “**CURRENT STATE: read `_AI_MEMORY/GLOBAL_HANDOFF.md` (newest section first) + `NEXT_STEPS.md` for live work.**” |
| 9 | `MTC_COMMAND_CENTER/_AI_MEMORY/DO_NOT_TOUCH.md` | 1,309 | 28 | 328 | ALWAYS-LOAD | `AI_RULES.md`, “Entry Point for a Fresh Agent”: “Read `GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, `DO_NOT_TOUCH.md`.” It also says: “Cross-check `DO_NOT_TOUCH.md` before every write.” |
| 10 | `MTC_COMMAND_CENTER/_AI_MEMORY/ACTIVE_FILES.md` | 66,766 | 1,007 | 16,692 | TASK-CLASS-SPECIFIC — Git/handoff/current working set | `AI_RULES.md`: “Every completed task must update: … `ACTIVE_FILES.md` — if working set changed.” This is conditional handling rather than an unconditional fresh-agent read, despite the earlier statement that canonical state “lives in” this file. |
| 11 | `MTC_COMMAND_CENTER/_AI_MEMORY/AI_ACCOUNT_AND_MODEL_ROUTING.md` | 26,317 | 332 | 6,580 | TASK-CLASS-SPECIFIC — planning/model routing | `START_HERE.md`: “Account homes, wrappers, and credential *source* names …: `AI_ACCOUNT_AND_MODEL_ROUTING.md` — operational index only, no secrets; usage figures there are a dated snapshot and must be re-checked.” `CLAUDE.md` additionally makes its launcher route mandatory. |
| 12 | `MTC_COMMAND_CENTER/_AI_MEMORY/SPRINT_WORKFLOW.md` | 4,280 | 94 | 1,070 | TASK-CLASS-SPECIFIC — planning/dispatch | `START_HERE.md`: “See `AI_RULES.md` and `SPRINT_WORKFLOW.md` for gate-level actor assignments.” |
| 13 | `MTC_COMMAND_CENTER/04_SHARED/prompts/05_ai_workflow/00_index.md` | 3,003 | 35 | 751 | TASK-CLASS-SPECIFIC — planning/workflow | `START_HERE.md`: “Workflow gates and prompt templates: see `AI_RULES.md` and `..\04_SHARED\prompts\05_ai_workflow\00_index.md`.” |
| 14 | `MTC_COMMAND_CENTER/04_SHARED/prompts/05_ai_workflow/01_office_hours_scope_review.md` | 2,457 | 57 | 615 | TASK-CLASS-SPECIFIC — planning, Gate 1 | `AI_RULES.md`: “Pick the right prompt template under `04_SHARED/prompts/05_ai_workflow/` for the current gate”; Gate 1 names this prompt. |
| 15 | `MTC_COMMAND_CENTER/04_SHARED/prompts/05_ai_workflow/02_engineering_plan_review.md` | 1,810 | 50 | 453 | TASK-CLASS-SPECIFIC — planning, Gate 2 | Same current-gate instruction; Gate 2 names this prompt and says Gate 2 is skipped for trivial doc/typo/single-line fixes. |
| 16 | `MTC_COMMAND_CENTER/04_SHARED/prompts/05_ai_workflow/03_implementation_task.md` | 2,504 | 48 | 626 | TASK-CLASS-SPECIFIC — implementation, Gate 3 | Same current-gate instruction; Gate 3 names this prompt. |
| 17 | `MTC_COMMAND_CENTER/04_SHARED/prompts/05_ai_workflow/04_adversarial_code_review.md` | 5,550 | 89 | 1,388 | TASK-CLASS-SPECIFIC — review, Gate 5 | Same current-gate instruction; Gate 5 names this prompt. |
| 18 | `MTC_COMMAND_CENTER/04_SHARED/prompts/05_ai_workflow/05_qa_test_review.md` | 1,763 | 53 | 441 | TASK-CLASS-SPECIFIC — QA, Gate 4 | Same current-gate instruction; Gate 4 names this prompt. |
| 19 | `MTC_COMMAND_CENTER/04_SHARED/prompts/05_ai_workflow/06_security_review.md` | 3,539 | 75 | 885 | TASK-CLASS-SPECIFIC — security, Gate 6 | Same current-gate instruction; Gate 6 names this prompt and says it is only used when scope hits a security surface. |
| 20 | `MTC_COMMAND_CENTER/04_SHARED/prompts/05_ai_workflow/07_handoff_update.md` | 2,613 | 71 | 654 | TASK-CLASS-SPECIFIC — Git/handoff, Gate 7 | `AI_RULES.md`: “After finishing the task: execute Gate 7 (memory write-back).” Gate 7 names this prompt. |
| 21 | `MTC_COMMAND_CENTER/04_SHARED/prompts/05_ai_workflow/08_backtest_launch.md` | 7,038 | 146 | 1,760 | TASK-CLASS-SPECIFIC — research run | `AGENTS.md`: “Follow `04_SHARED\prompts\05_ai_workflow\08_backtest_launch.md`.” |
| 22 | `MTC_COMMAND_CENTER/03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md` | 19,269 | 337 | 4,818 | TASK-CLASS-SPECIFIC — research run | `AGENTS.md`: “For ANY backtest / optimization … TWO files are mandatory pre-read (Gate 0): 1. Canonical rules: `…07_BACKTEST_AND_OPTIMIZATION_RULES.md` … 2. Operational runbook: `…BACKTEST_OPTIMIZATION_RUNBOOK.md`.” |
| 23 | `MTC_COMMAND_CENTER/11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md` | 32,402 | 460 | 8,101 | TASK-CLASS-SPECIFIC — research run | Same “ANY backtest / optimization” mandatory-pre-read sentence. |
| 24 | `MTC_COMMAND_CENTER/03_QUANTLENS/data/README.md` | 4,651 | 57 | 1,163 | TASK-CLASS-SPECIFIC — research run | `AGENTS.md`: “Before running ANY backtest you must know which data the engine uses. … **Authoritative data inventory:** `MTC_COMMAND_CENTER\03_QUANTLENS\data\README.md`.” |
| 25 | `MTC_COMMAND_CENTER/11_TRIAGE/RESULTS_TO_DASHBOARD_MAP_2026-06-29.md` | 4,315 | 53 | 1,079 | TASK-CLASS-SPECIFIC — research result publication | `START_HERE.md`: “Per-job procedures … results → dashboard → `..\11_TRIAGE\RESULTS_TO_DASHBOARD_MAP_2026-06-29.md`.” |
| 26 | `MTC_COMMAND_CENTER/03_QUANTLENS/_user_guide/13_AI_VERDICT_AUTHORING_PROCEDURE.md` | 5,152 | 82 | 1,288 | TASK-CLASS-SPECIFIC — AI/QuantLens verdict | `START_HERE.md`: “Per-job procedures … AI/QuantLens verdict authoring → `..\03_QUANTLENS\_user_guide\13_AI_VERDICT_AUTHORING_PROCEDURE.md`.” |
| 27 | `MTC_COMMAND_CENTER/_AI_MEMORY/STRATEGY_COMPONENT_LIBRARY.md` | 2,894 | 58 | 724 | TASK-CLASS-SPECIFIC — strategy research | `START_HERE.md`: “Before any strategy-research session, read in this order: 1. `STRATEGY_COMPONENT_LIBRARY.md` — what exists, what combines.” |
| 28 | `MTC_COMMAND_CENTER/05_REGISTRY/STRATEGY_RESEARCH_REGISTRY.json` | 132,996 | 3,493 | 33,249 | TASK-CLASS-SPECIFIC — strategy research | `START_HERE.md`: “Before any strategy-research session, read in this order: … 2. `05_REGISTRY/STRATEGY_RESEARCH_REGISTRY.json` + `INDICATOR_REGISTRY.json` + `COMPONENT_REGISTRY.json` + `TAG_DICTIONARY.json`.” |
| 29 | `MTC_COMMAND_CENTER/05_REGISTRY/INDICATOR_REGISTRY.json` | 25,494 | 803 | 6,374 | TASK-CLASS-SPECIFIC — strategy research | Same strategy-research read-order sentence. |
| 30 | `MTC_COMMAND_CENTER/05_REGISTRY/COMPONENT_REGISTRY.json` | 38,185 | 1,484 | 9,547 | TASK-CLASS-SPECIFIC — strategy research | Same strategy-research read-order sentence. |
| 31 | `MTC_COMMAND_CENTER/05_REGISTRY/TAG_DICTIONARY.json` | 4,666 | 253 | 1,167 | TASK-CLASS-SPECIFIC — strategy research | Same strategy-research read-order sentence. |
| 32 | `MTC_COMMAND_CENTER/_AI_MEMORY/STRATEGY_RESEARCH_WORKFLOW.md` | 2,938 | 50 | 735 | TASK-CLASS-SPECIFIC — strategy research | `START_HERE.md`: “Before any strategy-research session, read in this order: … 3. `STRATEGY_RESEARCH_WORKFLOW.md` (16-step process) and `STRATEGY_CODE_REVIEW_CHECKLIST.md`.” |
| 33 | `MTC_COMMAND_CENTER/_AI_MEMORY/STRATEGY_CODE_REVIEW_CHECKLIST.md` | 2,249 | 41 | 563 | TASK-CLASS-SPECIFIC — strategy research | Same strategy-research read-order sentence. |
| 34 | `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md` | 56,146 | 982 | 14,037 | TASK-CLASS-SPECIFIC — Bridge/planning executable checks | `START_HERE.md`: “Before designing or auditing any executable check/block/preregistration, read `..\11_TRIAGE\DESIGN_DEFECT_PATTERNS_2026-08-10.md`.” |
| 35 | `MTC_COMMAND_CENTER/09_DOCS/AI_TOOLING/AI_TOOL_INTEGRATION_PLAN.md` | 17,080 | 225 | 4,270 | TASK-CLASS-SPECIFIC — triggered local tooling | `START_HERE.md`: “AI tool auto-use … see the `AI TOOL AUTO-USE` section in `AGENTS.md` and `..\09_DOCS\AI_TOOLING\AI_TOOL_INTEGRATION_PLAN.md`. Use them automatically at their triggers.” |
| 36 | `_deepseek_driver/README.md` | 3,891 | 70 | 973 | TASK-CLASS-SPECIFIC — DeepSeek fallback dispatch | `AGENTS.md`: “Harness: `_deepseek_driver\ds_agent.py`; how-to: `_deepseek_driver\README.md` (READ before dispatching).” |
| 37 | `MTC_COMMAND_CENTER/01_MTC_PROJECT/_AI_MEMORY/HANDOFF.md` | 264 | 25 | 66 | TASK-CLASS-SPECIFIC — MTC project handoff | `START_HERE.md` read order ends with: “then project handoff files.” |
| 38 | `MTC_COMMAND_CENTER/01_MTC_PROJECT/03_DOCS/HANDOFF.md` | 7,528 | 118 | 1,882 | TASK-CLASS-SPECIFIC — MTC project handoff | Same “then project handoff files” instruction. |
| 39 | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/_AI_MEMORY/HANDOFF.md` | 264 | 25 | 66 | TASK-CLASS-SPECIFIC — MTC backtest handoff | Same “then project handoff files” instruction. |
| 40 | `MTC_COMMAND_CENTER/03_QUANTLENS/_AI_MEMORY/HANDOFF.md` | 264 | 25 | 66 | TASK-CLASS-SPECIFIC — research run/QuantLens handoff | Same “then project handoff files” instruction. |
| 41 | `MTC_COMMAND_CENTER/03_QUANTLENS/HANDOFF.md` | 6,287 | 79 | 1,572 | TASK-CLASS-SPECIFIC — research run/QuantLens handoff | Same “then project handoff files” instruction. |
| 42 | `MTC_COMMAND_CENTER/_AI_MEMORY/DECISIONS.md` | 29,062 | 63 | 7,266 | TASK-CLASS-SPECIFIC — Git/handoff | `AI_RULES.md`: “Every completed task must update: … `DECISIONS.md` — if a sticky decision was made.” |
| 43 | `MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOCK.md` | 26,532 | 317 | 6,633 | TASK-CLASS-SPECIFIC — Git/write-session coordination | `AI_RULES.md`: “One writable owner per workstream. Claim before the first write, release at handoff — mechanism and current table in `SESSION_LOCK.md`.” |
| 44 | `MTC_COMMAND_CENTER/_AI_MEMORY/CODEX_PICKUP_2026-06-08.md` | 9,547 | 79 | 2,387 | HISTORY | `START_HERE.md`: “The older `_AI_MEMORY/CODEX_PICKUP_2026-06-08.md` is historical (most items DONE) — read only for back-context.” Excluded from all default burdens. |

## Boundary notes

1. `ACTIVE_FILES.md` and `AI_ACCOUNT_AND_MODEL_ROUTING.md` were explicitly requested for measurement, but the chain does not place either in the unconditional fresh-agent numbered list. They are therefore task-class-specific rather than silently added to ALWAYS-LOAD.
2. `DECISIONS.md` and `SESSION_LOCK.md` are included because `AI_RULES.md` declares their conditional close-out/write-session use. `SESSION_LOG.md` is excluded because `AI_RULES.md` explicitly marks it retired and says not to write it.
3. The historical `archive/START_HERE_STALE_BANNER_2026-08-12.md` is excluded: `START_HERE.md` says it preserves rotated text but does not instruct a default read. The generic archive is grep-on-demand, not always-load.
4. The five concrete project `HANDOFF.md` files are enumerated because `START_HERE.md` says “then project handoff files.” Only the handoff(s) for the active project belong in a task-class subtotal.
5. No generic Bridge-local `AGENTS.md`, `CLAUDE.md`, or `HANDOFF.md` exists under `IBKR_PAPER_BRIDGE`. Consequently no such file is invented for the Bridge subtotal.
6. The ALWAYS-LOAD total is the sum of rows 1–9 only: **672,863 bytes / approximately 168,216 tokens**.

P0-05 BASELINE DONE — ALWAYS-LOAD: **672,863 bytes, 8,334 lines, approximately 168,216 tokens**.
