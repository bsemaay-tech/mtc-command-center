# AI Memory File Classification — Batch 1

**Date:** 2026-08-17 01:29 +03:00  
**Mode:** read-only classification; this report is the only write  
**Repository:** `C:\LAB\Tradingview_LAB_CLEAN`  
**Result:** authority files identified for preservation, three live drift risks isolated, and historical June artifacts grouped for no-loss archival review.

## 1. Scope and exclusions

This package audits the largest and highest-impact files under `MTC_COMMAND_CENTER/_AI_MEMORY` while excluding all files involved in the concurrent lossless rotation and all other protected concurrent surfaces.

Explicitly not read for classification or changed by this task:

- live `GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, and `START_HERE.md` rotation payloads
- the three new rotation archive files
- `SESSION_LOCK.md`
- `ACTIVE_FILES.md`
- `IBKR_PAPER_BRIDGE/docs/30_V2_BACKEND_AND_DASHBOARD_DESIGN_DECISIONS.md`
- Help/System Map files
- hosts, credentials, secrets, or deployment state

No memory file was moved, edited, deleted, staged, or committed.

## 2. Verdict meanings

- **KEEP:** current canonical, operational, safety, or durable historical authority. Preserve at its current logical role.
- **ROTATE-CANDIDATE:** still needed, but generated/snapshot content should be refreshed or losslessly split while keeping a stable entry point.
- **ARCHIVE-CANDIDATE:** historical task/sprint artifact that should leave the active memory surface only through a verbatim archive plus index/reference repair.
- **HOLD:** must stay in place until a discovered contradiction or dependency is repaired; neither archive nor unconditional keep is safe yet.

“Archive candidate” never means delete or summarize away.

## 3. Method

For each classified file, the audit recorded:

- exact byte size from the current filesystem
- first and last Git commit dates for that path (`git log --follow`)
- direct name references from repo-root `AGENTS.md` and the current onboarding entry point
- total tracked textual references under `AGENTS.md`, `MTC_COMMAND_CENTER`, and `IBKR_PAPER_BRIDGE`
- role, authority, overlap, and drift risk

Git history dates describe when the tracked path changed, not every date mentioned inside the prose.

## 4. Existing archives — KEEP

| File | Bytes | Git first–last | Direct onboarding refs | Tracked refs | Verdict |
|---|---:|---|---:|---:|---|
| `archive/GLOBAL_HANDOFF_pre-2026-08-01.md` | 238,645 | 2026-08-15 | 0 | 1 | KEEP |
| `archive/NEXT_STEPS_pre-2026-08-01.md` | 129,822 | 2026-08-15 | 0 | 3 | KEEP |
| `archive/SESSION_LOG_pre-2026-07-06.md` | 113,446 | 2026-05-31–2026-08-15 | 0 | 1 | KEEP |

These already perform the correct no-loss role: history is retained outside routine onboarding. Do not compact, merge, or rewrite their payloads. Maintain only navigational indexes around them.

## 5. Canonical and operational authorities

| File | Bytes | Git first–last | Direct onboarding refs | Tracked refs | Verdict |
|---|---:|---|---:|---:|---|
| `DECISIONS.md` | 29,062 | 2026-05-31–2026-08-10 | 0 | 83 | KEEP |
| `AI_ACCOUNT_AND_MODEL_ROUTING.md` | 25,824 | 2026-08-02–2026-08-16 | 1 | 12 | KEEP |
| `AI_RULES.md` | 11,527 | 2026-06-06–2026-08-11 | 4 | 57 | HOLD |
| `PROJECT_MEMORY.md` | 7,690 | 2026-06-06–2026-08-08 | 1 | 46 | HOLD |
| `LESSONS.md` | 7,587 | 2026-08-15 | 1 | 2 | KEEP |
| `SPRINT_WORKFLOW.md` | 4,186 | 2026-06-06–2026-07-31 | 1 | 9 | HOLD |
| `LIVE_TRADING_GATE.md` | 3,670 | 2026-07-02 | 0 | 20 | KEEP |
| `STRATEGY_RESEARCH_WORKFLOW.md` | 2,888 | 2026-06-06 | 2 | 11 | KEEP |
| `STRATEGY_COMPONENT_LIBRARY.md` | 2,836 | 2026-06-06 | 1 | 6 | ROTATE-CANDIDATE |
| `TOOL_OUTPUT_OFFLOAD_PROTOCOL.md` | 2,252 | 2026-08-09 | 0 | 2 | KEEP |
| `STRATEGY_CODE_REVIEW_CHECKLIST.md` | 2,208 | 2026-06-06 | 1 | 12 | KEEP |
| `REVIEW_CHECKLIST.md` | 2,070 | 2026-06-06 | 1 | 31 | HOLD |
| `DO_NOT_TOUCH.md` | 1,309 | 2026-05-31–2026-06-29 | 0 | 32 | KEEP |
| `SESSION_LOG.md` | 279 | 2026-05-31–2026-08-15 | 1 | 91 | KEEP |

### `DECISIONS.md` — KEEP

This is the sticky provenance ledger. Its 29,062 bytes are dense because decisions are long single records. The audit-tier policy is also present in `AGENTS.md`, but this is intentional provenance, not disposable duplication.

Future token optimization may split decisions by ID range behind a stable index, but exact IDs and wording must remain intact. Do not summarize or deduplicate decision records against policy files.

### `AI_ACCOUNT_AND_MODEL_ROUTING.md` — KEEP

This is directly referenced by onboarding and was updated through 2026-08-16. It correctly says:

- it is an operational index, not policy;
- `AGENTS.md` wins on disagreement;
- usage/quota figures are time-stamped snapshots;
- no secrets may appear.

That boundary prevents its dated quota numbers from masquerading as live capacity. Preserve it. Later rotation may move obsolete provider snapshots into a dated history section, but the account-home/wrapper index must remain stable.

### `AI_RULES.md` — HOLD pending synchronization

This is a direct onboarding authority and its audit-tier text is aligned with current `AGENTS.md`. It must not be archived.

However, it still identifies `ACTIVE_FILES.md` as the current working set and requires updates to it at Gate 7. It also retains old memory-layer references that become inconsistent if `ACTIVE_FILES.md` is retired. Synchronize it with the approved memory rotation before declaring it clean `KEEP`.

Duplication risk: it repeats parts of `AGENTS.md`. Keep only the gate-level workflow here and point to `AGENTS.md` for roster/tier tables so future policy changes do not drift.

### `PROJECT_MEMORY.md` — HOLD pending synchronization

This file is correctly positioned as stable repo facts and is directly referenced by onboarding. It must remain.

It still says volatile state belongs in `SESSION_LOG.md` or `ACTIVE_FILES.md`, calls `ACTIVE_FILES.md` the active working set, and routes “what I did today” to the retired `SESSION_LOG.md`. Those references conflict with the current single-handoff/rotation design. Repair those pointers before classifying it as clean `KEEP`.

### `LESSONS.md` — KEEP

This is explicitly capped, durable, and directly in the read order. Its 16 lessons are short paid-for rules rather than session history. Preserve the cap and archive older lessons through the existing lesson process if the cap is reached.

### `SPRINT_WORKFLOW.md` — HOLD for governance repair

This is directly referenced by onboarding and should remain the visual sprint loop. It correctly describes the two-tier Lead/Implementer split, but its Gate-5 table still says `≤3 repair rounds`, which contradicts the permanent tier-specific caps (`T0=3`, `T1=2`, `T2=1`, `T3=0`).

Do not archive it; repair the contradiction and point the cap solely to `AGENTS.md`/`AI_RULES.md`.

### `LIVE_TRADING_GATE.md` — KEEP

The document is deliberately unsigned/DRAFT and explicitly states live trading remains blocked. That conservative boundary is safety-positive. It does not duplicate an approval; it proves none exists. Preserve it until replaced by an owner-signed version.

### Strategy research workflow/checklist — KEEP

`STRATEGY_RESEARCH_WORKFLOW.md` and `STRATEGY_CODE_REVIEW_CHECKLIST.md` are permanent, directly referenced process authorities. They point to the canonical backtest rules rather than copying the complete methodology.

### `STRATEGY_COMPONENT_LIBRARY.md` — ROTATE-CANDIDATE

This file correctly declares the registries as the machine-readable authority and says its counts are a snapshot. The snapshot is now materially stale:

- library claim: **46** strategy directories;
- live `STG*` directory count: **63**;
- live `STRATEGY_RESEARCH_REGISTRY.json` entries: **63**.

Because onboarding tells strategy-research agents to read this file first and not re-derive the inventory, stale counts can misdirect new research. Regenerate it from the current registries before strategy work resumes; preserve its guidance sections unless the generator intentionally replaces them.

### `REVIEW_CHECKLIST.md` — HOLD for memory-rule repair

This is directly referenced by onboarding, but Gate 7 still requires a `SESSION_LOG.md` entry and an `ACTIVE_FILES.md` update. `SESSION_LOG.md` is retired, and `ACTIVE_FILES.md` is under retirement review. Repair these checklist rows to match the accepted memory design; do not archive the whole checklist.

### `TOOL_OUTPUT_OFFLOAD_PROTOCOL.md`, `DO_NOT_TOUCH.md`, `SESSION_LOG.md` — KEEP

- Tool offload is a current compact-context convention and clearly separates scratch from durable evidence.
- `DO_NOT_TOUCH.md` is a compact safety boundary with 32 tracked references.
- `SESSION_LOG.md` is a 279-byte tombstone/pointer. Keeping it prevents old references from becoming broken links and costs effectively nothing.

## 6. Generated repository map

| File | Bytes | Git first–last | Direct onboarding refs | Tracked refs | Verdict |
|---|---:|---|---:|---:|---|
| `REPO_MAP.md` | 22,294 | 2026-08-09 | 0 | 3 | ROTATE-CANDIDATE |

`REPO_MAP.md` is explicitly generated and says to regenerate after structural merges. It is now stale:

- its `_AI_MEMORY` count says 52 files, while the inventory measured 59 before the current rotation;
- its triage/repository counts predate the large August worktree/evidence expansion;
- its prose says Codex is always Lead and Claude is always implementer, while current `AGENTS.md` says whichever flagship receives the task is Lead and delegates to the counterpart.

Regenerate mechanically from the current repository and update the two-tier description from the canonical authority. Do not hand-maintain counts.

## 7. Historical programme/snapshot files

| File | Bytes | Git first–last | Direct onboarding refs | Tracked refs | Verdict |
|---|---:|---|---:|---:|---|
| `MCC_COMPLETION_MASTER_PLAN.md` | 23,565 | 2026-06-06 | 0 | 5 | ARCHIVE-CANDIDATE |
| `CODEX_PICKUP_2026-06-08.md` | 9,468 | 2026-06-08 | 1 | 16 | ARCHIVE-CANDIDATE |
| `MCC_READINESS_REPORT.md` | 8,355 | 2026-06-06–2026-06-07 | 0 | 4 | ARCHIVE-CANDIDATE |
| `N5_CODABILITY_AUDIT.md` | 8,097 | 2026-06-07 | 0 | 5 | ARCHIVE-CANDIDATE |
| `HANDOFF_PROMPT_SP004_PHASE3.md` | 7,849 | 2026-06-06 | 0 | 3 | ARCHIVE-CANDIDATE |
| `DEEPSEEK_DISPATCH.md` | 7,556 | 2026-06-06–2026-07-31 | 0 | 13 | ARCHIVE-CANDIDATE |
| `A3_GAP_MATRIX.md` | 7,123 | 2026-06-06 | 0 | 10 | ARCHIVE-CANDIDATE |
| `PIPELINE_STATE.md` | 4,121 | 2026-06-06 | 0 | 9 | ARCHIVE-CANDIDATE |
| `NIGHT_BATCHES.md` | 4,069 | 2026-06-06–2026-06-07 | 0 | 8 | ARCHIVE-CANDIDATE |
| `IMPECCABLE_STRATEGY_DETAIL_PICKUP_2026-06-21.md` | 2,885 | 2026-06-21 | 0 | 3 | ARCHIVE-CANDIDATE |
| `FORWARD_PAPER_QUEUE.md` | 2,095 | 2026-06-06 | 0 | 19 | ARCHIVE-CANDIDATE |

These are dated execution plans, handoffs, and point-in-time strategy/pipeline snapshots. Their open items and counts have been superseded by current handoffs, current registries, and later Bridge work.

No-loss archive conditions:

1. Archive the cohort verbatim with old path, new path, SHA-256, Git identity, and reference count.
2. Keep a small redirect at `CODEX_PICKUP_2026-06-08.md` because onboarding explicitly names it as historical.
3. Preserve cross-links among `MCC_COMPLETION_MASTER_PLAN`, `A3_GAP_MATRIX`, `PIPELINE_STATE`, `N5_CODABILITY_AUDIT`, `NIGHT_BATCHES`, and `FORWARD_PAPER_QUEUE`.
4. Do not execute old `NIGHT_BATCHES.md` launch recipes; current backtest rules/runbook control execution.
5. Do not treat historical `FORWARD_PAPER_QUEUE` membership as current promotion evidence.

### `DEEPSEEK_DISPATCH.md` overlap risk

Its six prompts are June-specific and point at old pipeline/gap files. Current generic sub-delegation policy now lives in `AGENTS.md`, Cline instructions, and `_deepseek_driver/README.md`. Keeping both as active instructions risks sending an agent into obsolete June work. Archive the task prompts as a cohort; retain only a small pointer to current routing policy if callers still reference the filename.

## 8. June parallel-agent prompt/report cohort

All 14 files were created for the 2026-06-06 sprint and should be preserved together, not separated.

| File | Bytes | Verdict |
|---|---:|---|
| `PARALLEL_AGENT_PROMPTS/S1_DEEPSEEK_PROMPT.md` | 4,783 | ARCHIVE-CANDIDATE |
| `PARALLEL_AGENT_PROMPTS/S2_CODEX_PROMPT.md` | 8,132 | ARCHIVE-CANDIDATE |
| `PARALLEL_AGENT_PROMPTS/S3_ANTIGRAVITY_PROMPT.md` | 10,314 | ARCHIVE-CANDIDATE |
| `PARALLEL_AGENT_PROMPTS/S4_COPILOT_PROMPT.md` | 12,113 | ARCHIVE-CANDIDATE |
| `PARALLEL_AGENT_PROMPTS/S5_CODEX_A8_PROMPT.md` | 6,317 | ARCHIVE-CANDIDATE |
| `PARALLEL_AGENT_PROMPTS/S6_D3B_WORKER_MONITOR_PROMPT.md` | 7,237 | ARCHIVE-CANDIDATE |
| `PARALLEL_AGENT_PROMPTS/S7_A4_MISSING_METADATA_PROMPT.md` | 5,471 | ARCHIVE-CANDIDATE |
| `PARALLEL_AGENT_REPORTS/S1_DEEPSEEK_A1_REPORT.md` | 4,490 | ARCHIVE-CANDIDATE |
| `PARALLEL_AGENT_REPORTS/S2_CODEX_UI_REPORT.md` | 3,862 | ARCHIVE-CANDIDATE |
| `PARALLEL_AGENT_REPORTS/S3_ANTIGRAVITY_BACKEND_REPORT.md` | 3,070 | ARCHIVE-CANDIDATE |
| `PARALLEL_AGENT_REPORTS/S4_COPILOT_REPORT.md` | 5,745 | ARCHIVE-CANDIDATE |
| `PARALLEL_AGENT_REPORTS/S5_CODEX_A8_REPORT.md` | 2,640 | ARCHIVE-CANDIDATE |
| `PARALLEL_AGENT_REPORTS/S6_D3B_WORKER_MONITOR_REPORT.md` | 3,239 | ARCHIVE-CANDIDATE |
| `PARALLEL_AGENT_REPORTS/S7_A4_MISSING_METADATA_REPORT.md` | 3,049 | ARCHIVE-CANDIDATE |

Combined size: about 78.5 KiB.

Duplication/overlap: prompt requirements, completion summaries, and session-history excerpts are repeated in the pre-August handoff/session archives. Preserve the original prompt→report pairs and add an archive index rather than deduplicating prose within the records.

## 9. Highest-impact duplication and drift risks

Priority order:

1. **`STRATEGY_COMPONENT_LIBRARY.md`: factual drift.** Direct onboarding says 46 strategies; live registry/directory count is 63.
2. **`SPRINT_WORKFLOW.md`: governance drift.** Blanket `≤3` repair wording conflicts with tier-specific caps.
3. **`REPO_MAP.md`: generated drift.** Counts and Lead-role description are stale.
4. **`AI_RULES.md`, `PROJECT_MEMORY.md`, `REVIEW_CHECKLIST.md`: memory-design drift.** They still prescribe retired `SESSION_LOG`/`ACTIVE_FILES` behavior.
5. **`DEEPSEEK_DISPATCH.md`: routing/task overlap.** Old June prompts sit beside current canonical routing policy.
6. **June plan/gap/pipeline/readiness files: status overlap.** Several documents describe the same 2026-06-06 snapshot with slightly different counts and next actions.

The first four are repair/regeneration work, not archive work. The last two are no-loss archival work.

## 10. Recommended next packages

### Package A — current-authority synchronization

Documentation-only, review as one coherent boundary:

- align `AI_RULES.md`, `PROJECT_MEMORY.md`, and `REVIEW_CHECKLIST.md` with the accepted memory rotation;
- correct `SPRINT_WORKFLOW.md` tier-cap wording;
- retain stable filenames and authority links.

### Package B — generated-index refresh

- regenerate `REPO_MAP.md` mechanically;
- regenerate `STRATEGY_COMPONENT_LIBRARY.md` from the current 63-entry registry;
- verify exact counts against source directories and registry JSON.

### Package C — June historical cohort

- archive the dated master-plan/readiness/gap/pipeline/night-run/forward-paper files and all parallel prompt/report pairs verbatim;
- create one manifest with old path, new path, SHA-256, Git history dates, and redirect requirements;
- keep current execution rules pointing only to current runbooks and `AGENTS.md`.

Do not combine Packages A, B, and C into one unreviewable change. No package is executed by this classification report.
