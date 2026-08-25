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
- **Root router:** the same Claude entrypoint assumption as BEFORE, followed through root
  `AGENTS.md`, `CONTEXT_MAP.md`, and root `DECISIONS.md`. This is not the ALWAYS-LOAD floor because
  root `AGENTS.md` unconditionally requires one stage's five files too.
- **TASK-CLASS-SPECIFIC:** exactly one stage's five files plus only the sources that stage makes
  mandatory for the same scenario boundary used by BEFORE.
- **HISTORY:** `_AI_MEMORY/history/` and `11_TRIAGE/INDEX.md` are excluded because the router says
  not to load them by default; they are grep-on-demand.
- Lazy `CONTEXT.md` glossaries are excluded because they are read only when terminology is unclear.
- **Line endings:** BEFORE rows are CRLF working-tree bytes. AFTER filesystem columns are this
  checkout's mixed form: new routed files are LF on disk and in Git blobs, while unchanged legacy
  inputs can remain CRLF. The projected-CRLF columns add one byte for every LF not already preceded
  by CR, matching a fresh `autocrlf=true` checkout without changing the measured files.

## Summary

| Burden / task class | Incremental bytes beyond root router | Incremental approx. tokens | Total bytes including root router | Total approx. tokens including root router | Total lines | Scenario boundary |
|---|---:|---:|---:|---:|---:|---|
| **Root router only** | — | — | **12,959** | **3,240** | 118 | Claude entrypoint, root router, route map, capped decisions index; excludes the mandatory stage |
| Research run | 279,384 | 69,846 | 292,343 | 73,086 | 7,394 | Full strategy-research session proceeding to canonical backtest, same inputs/gates/registries as BEFORE plus the one QuantLens stage |
| Bridge work | 60,724 | 15,181 | 73,683 | 18,421 | 1,170 | Bridge work designing/auditing an executable check, same defect catalogue plus the one Bridge stage |
| Planning | 87,769 | 21,943 | 100,728 | 25,182 | 1,588 | Gate-1/Gate-2 planning for an executable check, current gate prompts and their required reads plus the one governance stage |
| Git/handoff | 41,845 | 10,462 | 54,804 | 13,701 | 663 | Full write-session close-out, governance stage, Gate-7 prompt, and checked `SESSION_LOCK` mirror |

The unconditional floor is root router plus one selected stage. The smallest stage is shown for the
lower bound, QuantLens for a common product route, and `00_AGENT_PROTOCOLS/` because it is the
catch-all for every repository path not assigned elsewhere:

| Unconditional routed floor | Actual mixed bytes / tokens | Projected CRLF bytes / tokens | CRLF byte reduction from BEFORE ALWAYS-LOAD |
|---|---:|---:|---:|
| Root + `mtc_cli/` (smallest) | 15,806 / 3,952 | 15,973 / 3,994 | 97.63% |
| Root + `03_QUANTLENS/` | 18,879 / 4,720 | 19,089 / 4,773 | 97.16% |
| Root + `00_AGENT_PROTOCOLS/` (catch-all) | **25,469 / 6,368** | **25,756 / 6,439** | **96.17%** |

## Before versus after

| Task class | BEFORE CRLF bytes / tokens | AFTER actual mixed bytes / tokens | Mixed-form byte reduction | AFTER projected CRLF bytes / tokens | Same-form byte reduction |
|---|---:|---:|---:|---:|---:|
| Root router only (not a floor) | 672,863 / 168,216 | 12,959 / 3,240 | 659,904 (98.07%) | 13,077 / 3,270 | 659,786 (98.06%) |
| Research run | 952,196 / 238,049 | 292,343 / 73,086 | 659,853 (69.30%) | 292,572 / 73,143 | 659,624 (69.27%) |
| Bridge work | 729,009 / 182,253 | 73,683 / 18,421 | 655,326 (89.89%) | 73,871 / 18,468 | 655,138 (89.87%) |
| Planning | 766,876 / 191,719 | 100,728 / 25,182 | 666,148 (86.87%) | 101,037 / 25,260 | 665,839 (86.82%) |
| Git/handoff | 797,836 / 199,459 | 54,804 / 13,701 | 743,032 (93.13%) | 55,137 / 13,785 | 742,699 (93.09%) |

These measurements support the later conditional-split trigger only. They do not decide repository
topology; the stage-routed monorepo doctrine is already ratified.

## Per-file inventory

### Root router only

| Path | Bytes | Lines | Approx. tokens | Why loaded |
|---|---:|---:|---:|---|
| `CLAUDE.md` | 280 | 1 | 70 | Same entrypoint assumption as BEFORE; routes to root contract |
| `AGENTS.md` | 4,169 | 60 | 1,043 | Identity, invariants, and next route |
| `CONTEXT_MAP.md` | 1,239 | 19 | 310 | Selects exactly one stage |
| `DECISIONS.md` | 7,271 | 38 | 1,818 | Only historical/current decision index loaded by default |
| **TOTAL** | **12,959** | **118** | **3,240** | |

### Research-run increment

| Path/group | Bytes | Lines | Approx. tokens |
|---|---:|---:|---:|
| `03_QUANTLENS/{AGENTS,INPUTS,OUTPUTS,TESTS,HANDOFF}.md` | 5,920 | 92 | 1,480 |
| `04_SHARED/prompts/05_ai_workflow/08_backtest_launch.md` | 7,417 | 147 | 1,855 |
| `03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md` | 19,269 | 337 | 4,818 |
| `11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md` | 32,587 | 460 | 8,147 |
| `03_QUANTLENS/data/README.md` | 4,651 | 57 | 1,163 |
| `_AI_MEMORY/STRATEGY_COMPONENT_LIBRARY.md` | 2,894 | 58 | 724 |
| `05_REGISTRY/STRATEGY_RESEARCH_REGISTRY.json` | 132,996 | 3,493 | 33,249 |
| `05_REGISTRY/INDICATOR_REGISTRY.json` | 25,494 | 803 | 6,374 |
| `05_REGISTRY/COMPONENT_REGISTRY.json` | 38,185 | 1,484 | 9,547 |
| `05_REGISTRY/TAG_DICTIONARY.json` | 4,666 | 253 | 1,167 |
| `_AI_MEMORY/STRATEGY_RESEARCH_WORKFLOW.md` | 3,056 | 51 | 764 |
| `_AI_MEMORY/STRATEGY_CODE_REVIEW_CHECKLIST.md` | 2,249 | 41 | 563 |
| **TOTAL** | **279,384** | **7,276** | **69,846** |

### Bridge-work increment

| Path/group | Bytes | Lines | Approx. tokens |
|---|---:|---:|---:|
| `IBKR_PAPER_BRIDGE/{AGENTS,INPUTS,OUTPUTS,TESTS,HANDOFF}.md` | 4,578 | 70 | 1,145 |
| `11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md` | 56,146 | 982 | 14,037 |
| **TOTAL** | **60,724** | **1,052** | **15,181** |

### Planning increment

| Path/group | Bytes | Lines | Approx. tokens |
|---|---:|---:|---:|
| `00_AGENT_PROTOCOLS/{AGENTS,INPUTS,OUTPUTS,TESTS,HANDOFF}.md` | 12,510 | 169 | 3,128 |
| `04_SHARED/prompts/05_ai_workflow/00_index.md` | 3,080 | 35 | 770 |
| `04_SHARED/prompts/05_ai_workflow/01_office_hours_scope_review.md` | 2,688 | 59 | 672 |
| `04_SHARED/prompts/05_ai_workflow/02_engineering_plan_review.md` | 1,818 | 49 | 455 |
| `_AI_MEMORY/AI_RULES.md` (required by the G2 prompt; stale but still load-bearing) | 11,527 | 176 | 2,882 |
| `11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md` | 56,146 | 982 | 14,037 |
| **TOTAL** | **87,769** | **1,470** | **21,943** |

### Git/handoff increment

| Path/group | Bytes | Lines | Approx. tokens |
|---|---:|---:|---:|
| `00_AGENT_PROTOCOLS/{AGENTS,INPUTS,OUTPUTS,TESTS,HANDOFF}.md` | 12,510 | 169 | 3,128 |
| `04_SHARED/prompts/05_ai_workflow/07_handoff_update.md` | 2,124 | 54 | 531 |
| `_AI_MEMORY/SESSION_LOCK.md` | 27,211 | 322 | 6,803 |
| **TOTAL** | **41,845** | **545** | **10,462** |

## Boundary notes

1. The full research scenario intentionally remains registry-heavy. The router removes unrelated
   onboarding, not the canonical inputs a full strategy-research/backtest task truly consumes.
2. The workflow index and backtest launch prompt no longer load the old pre-router chain. The honest
   59-file sweep still finds two current-gate prompt reads of `_AI_MEMORY/AI_RULES.md` (G2 and G5),
   so the final stale required-read count is 2, not 0. Those files were outside this focused repair;
   the G2 `AI_RULES.md` read is therefore included in the Planning measurement rather than hidden.
   Account routing remains conditional for account, quota, credential-source, or route diagnosis.
3. Git/handoff no longer loads the 66,766-byte global `ACTIVE_FILES.md`, the full decisions archive,
   or either append-only journal. Current state is stage-local; `SESSION_LOCK` remains conditional
   because every write task checks it as the GitHub claim's mirror/history.
4. Index and history sizes are deliberately excluded: the contract says grep them, then read at most
   the relevant record. Counting all history would contradict the routed load contract.
