# WP-P0-05 AFTER measurement — routed AI-onboarding burden

Measured: 2026-08-25 (Europe/Chisinau)

Repository worktree: `C:\WPP005_20260825`

Branch: `feature/wp-p0-05-context-routing-20260825`

Base: `0253d014daa61d51f9b4f6d93c1f10d3f3e509de`

## Method and classification

This uses the BEFORE evidence's exact method:

- **Bytes:** filesystem length.
- **Lines:** `.NET File.ReadAllLines(path).Count`.
- **Approx. tokens:** `ceil(bytes / 4)`. Aggregate tokens are `ceil(aggregate bytes / 4)`.
- **ALWAYS-LOAD:** the same Claude entrypoint assumption as BEFORE, now followed through root
  `AGENTS.md`, `CONTEXT_MAP.md`, and root `DECISIONS.md`.
- **TASK-CLASS-SPECIFIC:** exactly one stage's five files plus only the sources that stage makes
  mandatory for the same scenario boundary used by BEFORE.
- **HISTORY:** `_AI_MEMORY/history/` and `11_TRIAGE/INDEX.md` are excluded because the router says
  not to load them by default; they are grep-on-demand.
- Lazy `CONTEXT.md` glossaries are excluded because they are read only when terminology is unclear.

## Summary

| Burden / task class | Incremental bytes beyond ALWAYS-LOAD | Incremental approx. tokens | Total bytes including ALWAYS-LOAD | Total approx. tokens including ALWAYS-LOAD | Total lines | Scenario boundary |
|---|---:|---:|---:|---:|---:|---|
| **ALWAYS-LOAD baseline** | — | — | **12,769** | **3,193** | 115 | Claude entrypoint, root router, route map, capped decisions index |
| Research run | 278,702 | 69,676 | 291,471 | 72,868 | 7,389 | Full strategy-research session proceeding to canonical backtest, same inputs/gates/registries as BEFORE plus the one QuantLens stage |
| Bridge work | 60,692 | 15,173 | 73,461 | 18,366 | 1,166 | Bridge work designing/auditing an executable check, same defect catalogue plus the one Bridge stage |
| Planning | 74,092 | 18,523 | 86,861 | 21,716 | 1,385 | Gate-1/Gate-2 planning for an executable check, current gate prompts plus the one governance stage |
| Git/handoff | 40,500 | 10,125 | 53,269 | 13,318 | 654 | Full write-session close-out, governance stage, Gate-7 prompt, and checked `SESSION_LOCK` mirror |

## Before versus after

| Task class | BEFORE bytes | AFTER bytes | Byte reduction | BEFORE approx. tokens | AFTER approx. tokens | Token reduction |
|---|---:|---:|---:|---:|---:|---:|
| ALWAYS-LOAD | 672,863 | 12,769 | 660,094 (98.10%) | 168,216 | 3,193 | 165,023 (98.10%) |
| Research run | 952,196 | 291,471 | 660,725 (69.39%) | 238,049 | 72,868 | 165,181 (69.39%) |
| Bridge work | 729,009 | 73,461 | 655,548 (89.92%) | 182,253 | 18,366 | 163,887 (89.92%) |
| Planning | 766,876 | 86,861 | 680,015 (88.67%) | 191,719 | 21,716 | 170,003 (88.67%) |
| Git/handoff | 797,836 | 53,269 | 744,567 (93.32%) | 199,459 | 13,318 | 186,141 (93.32%) |

These measurements support the later conditional-split trigger only. They do not decide repository
topology; the stage-routed monorepo doctrine is already ratified.

## Per-file inventory

### ALWAYS-LOAD

| Path | Bytes | Lines | Approx. tokens | Why loaded |
|---|---:|---:|---:|---|
| `CLAUDE.md` | 280 | 1 | 70 | Same entrypoint assumption as BEFORE; routes to root contract |
| `AGENTS.md` | 3,979 | 57 | 995 | Identity, invariants, and next route |
| `CONTEXT_MAP.md` | 1,239 | 19 | 310 | Selects exactly one stage |
| `DECISIONS.md` | 7,271 | 38 | 1,818 | Only historical/current decision index loaded by default |
| **TOTAL** | **12,769** | **115** | **3,193** | |

### Research-run increment

| Path/group | Bytes | Lines | Approx. tokens |
|---|---:|---:|---:|
| `03_QUANTLENS/{AGENTS,INPUTS,OUTPUTS,TESTS,HANDOFF}.md` | 5,920 | 92 | 1,480 |
| `04_SHARED/prompts/05_ai_workflow/08_backtest_launch.md` | 7,038 | 146 | 1,760 |
| `03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md` | 19,269 | 337 | 4,818 |
| `11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md` | 32,402 | 460 | 8,101 |
| `03_QUANTLENS/data/README.md` | 4,651 | 57 | 1,163 |
| `_AI_MEMORY/STRATEGY_COMPONENT_LIBRARY.md` | 2,894 | 58 | 724 |
| `05_REGISTRY/STRATEGY_RESEARCH_REGISTRY.json` | 132,996 | 3,493 | 33,249 |
| `05_REGISTRY/INDICATOR_REGISTRY.json` | 25,494 | 803 | 6,374 |
| `05_REGISTRY/COMPONENT_REGISTRY.json` | 38,185 | 1,484 | 9,547 |
| `05_REGISTRY/TAG_DICTIONARY.json` | 4,666 | 253 | 1,167 |
| `_AI_MEMORY/STRATEGY_RESEARCH_WORKFLOW.md` | 2,938 | 50 | 735 |
| `_AI_MEMORY/STRATEGY_CODE_REVIEW_CHECKLIST.md` | 2,249 | 41 | 563 |
| **TOTAL** | **278,702** | **7,274** | **69,676** |

### Bridge-work increment

| Path/group | Bytes | Lines | Approx. tokens |
|---|---:|---:|---:|
| `IBKR_PAPER_BRIDGE/{AGENTS,INPUTS,OUTPUTS,TESTS,HANDOFF}.md` | 4,546 | 69 | 1,137 |
| `11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md` | 56,146 | 982 | 14,037 |
| **TOTAL** | **60,692** | **1,051** | **15,173** |

### Planning increment

| Path/group | Bytes | Lines | Approx. tokens |
|---|---:|---:|---:|
| `00_AGENT_PROTOCOLS/{AGENTS,INPUTS,OUTPUTS,TESTS,HANDOFF}.md` | 10,676 | 146 | 2,669 |
| `04_SHARED/prompts/05_ai_workflow/00_index.md` | 3,003 | 35 | 751 |
| `04_SHARED/prompts/05_ai_workflow/01_office_hours_scope_review.md` | 2,457 | 57 | 615 |
| `04_SHARED/prompts/05_ai_workflow/02_engineering_plan_review.md` | 1,810 | 50 | 453 |
| `11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md` | 56,146 | 982 | 14,037 |
| **TOTAL** | **74,092** | **1,270** | **18,523** |

### Git/handoff increment

| Path/group | Bytes | Lines | Approx. tokens |
|---|---:|---:|---:|
| `00_AGENT_PROTOCOLS/{AGENTS,INPUTS,OUTPUTS,TESTS,HANDOFF}.md` | 10,676 | 146 | 2,669 |
| `04_SHARED/prompts/05_ai_workflow/07_handoff_update.md` | 2,613 | 71 | 654 |
| `_AI_MEMORY/SESSION_LOCK.md` | 27,211 | 322 | 6,803 |
| **TOTAL** | **40,500** | **539** | **10,125** |

## Boundary notes

1. The full research scenario intentionally remains registry-heavy. The router removes unrelated
   onboarding, not the canonical inputs a full strategy-research/backtest task truly consumes.
2. Planning no longer loads `SPRINT_WORKFLOW.md` or the account-routing inventory by default because
   the governance stage carries the binding gate/roster rules and names the Claude→Codex launcher.
   The account file remains conditional for account, quota, credential-source, or route diagnosis.
3. Git/handoff no longer loads the 66,766-byte global `ACTIVE_FILES.md`, the full decisions archive,
   or either append-only journal. Current state is stage-local; `SESSION_LOCK` remains conditional
   because every write task checks it as the GitHub claim's mirror/history.
4. Index and history sizes are deliberately excluded: the contract says grep them, then read at most
   the relevant record. Counting all history would contradict the routed load contract.
