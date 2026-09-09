# Memory index — read only for the relevant question

Current instructions start at root `AGENTS.md`. This index routes memory questions; it is not an
extra mandatory onboarding document. Search the table or file inventory, then open the matching
source. Do not load all memory files, old worker briefs or journals into a new agent's context.

## Current questions

| Question / trigger | Source to consult |
|---|---|
| Which stage owns this task? | Root `CONTEXT_MAP.md`, then that stage's `AGENTS.md` |
| What is authorized or superseded? | Matching root `DECISIONS.md` rows; governance `AUTONOMY_AUTHORIZATION.md` when applicable |
| How much review does this change require? | `../00_AGENT_PROTOCOLS/REVIEW_POLICY.md`, including its activation boundary |
| What is the current verified task state? | Selected stage `HANDOFF.md`, exact refs and the task's evidence/official tracker |
| Who owns these writable paths? | `SESSION_LOCK.md` mirror plus actual lane/dependency verification; the mirror alone grants no takeover |
| What is protected? | `DO_NOT_TOUCH.md`, selected stage rules and the approved task scope |
| Is a strategy approved for live use? | `LIVE_TRADING_GATE.md`; this reconciliation changes no signature, numeric threshold or readiness row |
| Which account/provider route should be used? | `AI_ACCOUNT_AND_MODEL_ROUTING.md`; refresh only the chosen route's relevant availability |
| Which recurring failure should this task avoid? | Search `LESSONS.md` by failure class; load relevant entries only |
| Where is strategy research/registry guidance? | `../03_QUANTLENS/INPUTS.md`; task-triggered research references |
| What did an older session actually record? | Search `history/`, `archive/`, or the matching dated result; re-verify any claim needed now |

## Historical material and compatibility files

- `history/` and `archive/` preserve past facts, instructions and evidence. They are not a queue
  or fresh authority. A current decision may explicitly reference a particular preserved contract;
  that narrow reference does not activate the rest of a journal.
- `PARALLEL_AGENT_PROMPTS/S*.md` and `PARALLEL_AGENT_REPORTS/S*.md` are dated worker dispatches and
  reports. Do not execute their commands or reuse their model roster, branches, scope, permissions
  or state as current. The Claude routing entry is a compatibility pointer to current policy.
- `RESULT_*.md`, dated pickups, recovery notes, codability/readiness reports and old working sets
  record their stated period. An old PASS, open task or quota is not a current result.
- The nested `01_MTC_PROJECT/_AI_MEMORY/`, `02_MTC_BACKTEST/_AI_MEMORY/` and
  `03_QUANTLENS/_AI_MEMORY/` Phase-1 ACTIVE_FILES/DECISIONS/HANDOFF/NEXT_STEPS files are legacy
  templates. Their blank fields and "review Phase 1" next steps are not current instructions.
  Use their parent stage's routed files and root decisions. Keep templates intact as history.
- The nested QuantLens `STRATEGY_REGISTRY.md` is an import-provenance table. Frozen legacy source
  paths identify provenance; they are not permission to inspect or operate the old checkout.
- `START_HERE.md`, `AI_RULES.md`, review/workflow aliases and retired reference stubs point to
  current authority. Edit the authoritative source instead of copying policy into every alias.

Materially shortened references have linked originals under `history/workflow-20260909/`.
All product packages, code and accepted evidence retain their original scope/status. Source
presence, a local test result and independent package acceptance are separate facts.

Inventory and verification: [reconciliation record](../11_TRIAGE/WORKFLOW_MEMORY_RECONCILIATION_2026-09-09.md).
Foreign untracked memory files in the canonical checkout are inspected as dated material and left
untouched; they are not silently imported into this branch or promoted into policy.
