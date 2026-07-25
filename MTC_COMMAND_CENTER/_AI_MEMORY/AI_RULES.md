# AI_RULES

GStack-inspired workflow rules for any AI agent (Codex / Claude)
working in this repository. Read **after** `AGENTS.md` and `START_HERE.md`.

This file does **not** replace the existing memory files. It is the rule
layer on top of them. Canonical state is route-scoped:

**Component-scoped task** — canonical state is the selected component's local chain only:
- `<component>/_AI_MEMORY/CURRENT.md`   - live session state
- `<component>/_AI_MEMORY/NEXT_STEPS.md` - what to do next
- `<component>/_AI_MEMORY/DECISIONS.md`  - sticky decisions (if applicable)
- `<component>/_AI_MEMORY/ACTIVE_FILES.md` - current working set (if applicable)
Do NOT read or write root volatile histories for component-scoped tasks.

**Cross-component task** — canonical state is every affected component's local chain first:
- Load and update each affected component's `CURRENT.md` / `NEXT_STEPS.md` / `DECISIONS.md` / `ACTIVE_FILES.md` as applicable.
- Then add one concise coordination entry to root `GLOBAL_HANDOFF.md`.
- Root `NEXT_STEPS.md` updated only when cross-component next steps need coordination; root volatile reads remain conditional.

**Global/policy task** — canonical state is root memory:
- `GLOBAL_HANDOFF.md`   - last session status / cross-component coordination
- `NEXT_STEPS.md`       - what to do next
- `DECISIONS.md`        - sticky decisions
- `DO_NOT_TOUCH.md`     - protected files / behaviour
- `ACTIVE_FILES.md`     - current working set
- `SESSION_LOCK.md`     - write-session lock state
- `PROJECT_MEMORY.md`   - stable repo facts (layout, modules, contracts)

**SESSION_LOG.md** — RETIRED: historical-only. Never current state. Never written by any agent.

Strategy-research layer (read before combining strategies/indicators):
- `STRATEGY_COMPONENT_LIBRARY.md`     - human-readable inventory + combine guidance
- `STRATEGY_RESEARCH_WORKFLOW.md`     - 16-step research process (points to backtest rules)
- `STRATEGY_CODE_REVIEW_CHECKLIST.md` - repaint/lookahead/conversion safety
- `05_REGISTRY/STRATEGY_RESEARCH_REGISTRY.json` + `INDICATOR_/COMPONENT_REGISTRY.json` + `TAG_DICTIONARY.json` - machine-readable taxonomy (generated; do not hand-edit)
- `05_REGISTRY/RESEARCH_RUN_/VARIANT_LOG_/RESEARCH_BACKTEST_REGISTRY.json` - research records shown in the **Strategy Research Lab** dashboard tab

## 7 Gates (must pass before claiming "done")

### Gate 1 - Scope Review (before coding)

**Actor: Lead Orchestrator.** Scope definition and acceptance authority rest with the lead. If the counterpart implementer CLI is unavailable, surface the blocker here and do not self-implement.

Gate 1 must be complete before Gate 2: produce objective, exact whitelist, acceptance criteria, safety/authorization, validation plan, and contract path.

- Restate user request in 1-2 sentences.
- User value: why does this matter?
- Smallest safe change that delivers value.
- Files allowed (whitelist).
- Files forbidden - cross-check `DO_NOT_TOUCH.md`.
- Success criteria: how do we know it works?

Prompt: `04_SHARED/prompts/05_ai_workflow/01_office_hours_scope_review.md`

### Gate 2 - Engineering Plan (before architecture change)

**Actor: Implementer.** Produces the plan; passes it to the Lead for acceptance before Gate 3 may begin.

- Data flow diagram or description.
- Affected modules.
- Edge cases.
- Rollback plan.
- Parity / Pine / MTC impact statement.

Skip Gate 2 for trivial doc / typo / single-line fixes.
Prompt: `04_SHARED/prompts/05_ai_workflow/02_engineering_plan_review.md`

### Gate 3 - Implementation

**Actor: Implementer.**

- Minimal diff.
- No unrelated edits.
- No speculative features, no premature abstractions.
- Stay inside the whitelist from Gate 1.

Prompt: `04_SHARED/prompts/05_ai_workflow/03_implementation_task.md`

### Gate 4 - QA / Tests

**Actor: Implementer (self-QA).** Produces concrete evidence for Lead review at Gate 5. Do not claim PASS without verifiable output.

- Run tests if a suite exists.
- Run lint / typecheck if configured.
- Note parity regression risk explicitly (parity suite = sacred).
- If UI / chart change: visually verify, do not assume.

Prompt: `04_SHARED/prompts/05_ai_workflow/05_qa_test_review.md`

### Gate 5 - Adversarial Cross-Model Review (Lead's independent inspection)
- The **LEAD ORCHESTRATOR** runs this gate - not the implementer. See two-tier model in `AGENTS.md`.
- **Exact model/effort required** - see `AGENTS.md` CANONICAL AUDIT ROSTER. Claude auditor: `claude-opus-4-8` + `xhigh`. Codex auditor: `gpt-5.6-sol` + `high` (ordinary G5) or `xhigh` (protected/re-audit). No Sonnet, no implicit alias, no silent fallback - BLOCK if unavailable unless Barış waives. `--fallback-model` forbidden for Claude; `--resume`/`--continue` forbidden for all auditors.
- **Fresh independent session every round** - never resume or continue the implementer session.
- The lead independently inspects the actual diff/files; accepting the implementer's self-report alone is not Gate 5.
- Audits are diff-first: unified diff by default; full files only for necessary context with stated reason.
- Reviewer reads adversarially: assume the diff is wrong, prove otherwise.
- Flag: missing edge cases, hidden coupling, parity risk, DO_NOT_TOUCH violations, scope creep.
- Verdicts: **PASS** / **PASS-WITH-NITS** (accepting, optional nits only) / **REQUEST_CHANGES** (required repair) / **BLOCK** (cannot continue). PASS-WITH-NITS cannot contain a required repair.
- On REQUEST_CHANGES or BLOCK: lead sends focused repair prompt to the same counterpart implementer. **Maximum 3 repair/re-audit rounds.** After the third non-accepting verdict, stop and report to Barış.

Prompt: `04_SHARED/prompts/05_ai_workflow/04_adversarial_code_review.md`

### Gate 6 - Security Review (only if scope hits security surface)

**Actor: Lead Orchestrator** — the lead runs the exact canonical audit (see `AGENTS.md` CANONICAL AUDIT ROSTER) or invokes an exact-roster fresh audit instance. Human/Fable/Gemini review is advisory and cannot satisfy G6.
**Exact model/effort:** Gate 6 always uses `xhigh`. Claude auditor: exact `claude-opus-4-8` xhigh. Codex auditor: exact `gpt-5.6-sol` xhigh.
**Verdicts:** PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK.

- Secrets, auth, network calls, file system writes, eval / exec, subprocess.
- Skip for pure doc / Pine plotting / cosmetic changes.

Prompt: `04_SHARED/prompts/05_ai_workflow/06_security_review.md`

### Gate 7 - Memory Write-Back (mandatory before stopping)

**Actor: Lead Orchestrator**, after accepting Gate 5 verdict (PASS or PASS-WITH-NITS) is verified. Implementer may supply factual inputs (commit hashes if authorized, test results, file lists); final write-back and authorized sequencing are Lead-owned. Do not execute without an accepting Gate 5 verdict. G7 must not require a future commit hash.

Sequence: accepting G5 verdict -> G6 if applicable -> G7 handoff -> then and only then authorized hygiene/commit/push.

**Write-back scope is determined by the route selected at startup (see `COMPONENT_ROUTER.md` Section 5):**

- **Component-scoped task:** update `<component>/_AI_MEMORY/CURRENT.md` (always) + `<component>/_AI_MEMORY/NEXT_STEPS.md` (always) + `DECISIONS.md` / `ACTIVE_FILES.md` if applicable. Do NOT touch root `GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, `ACTIVE_FILES.md`, or `SESSION_LOG.md`.
- **Cross-component task:** update every affected component per the above, then add one concise coordination entry to root `GLOBAL_HANDOFF.md`. Root `NEXT_STEPS.md` updated only for cross-component next steps.
- **Global/policy task:** use root memory files: `GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, `DECISIONS.md`, `ACTIVE_FILES.md`, `PROJECT_MEMORY.md`.

Prompt: `04_SHARED/prompts/05_ai_workflow/07_handoff_update.md`

## Hard Safety Rules

- No changes to Pine logic, MTC strategy behavior, or parity files
  without explicit Barış approval.
- Never recommend live trading.
- Never add secrets, tokens, or credentials to the repo.
- Never run destructive git operations: `reset --hard`, `restore`, `clean -fdx`, `stash drop`, branch deletion, `push --force`. These are prohibited for all agents; explicit Barış approval required.
- Implementer is additionally forbidden from commit, push, merge, rebase - git sequencing is Lead-only and requires the sequence: accepting G5, G6 if applicable, G7 handoff.
- Never bypass commit hooks (`--no-verify`).
- Cross-check `DO_NOT_TOUCH.md` before every write.
- Fable and Gemini are advisory/non-gate reviewers only - they may supplement but never replace a canonical Claude/Codex gate audit. Only the CANONICAL AUDIT ROSTER (Claude `claude-opus-4-8` xhigh; Codex `gpt-5.6-sol`) can accept G5/G6.

## Entry Point for a Fresh Agent

1. Read root `AGENTS.md`.
2. Read `_AI_MEMORY/START_HERE.md`.
3. Read `_AI_MEMORY/COMPONENT_ROUTER.md` and identify the route.
4. **Component-scoped route:** load component `AGENTS.md` -> component `_AI_MEMORY/START_HERE.md` -> `CURRENT.md` -> `NEXT_STEPS.md`. Skip root volatile history unless cross-component context is needed.
5. **Global/policy route:** read this file, `PROJECT_MEMORY.md`, `DO_NOT_TOUCH.md`, `GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`.
6. Pick the right prompt template under `04_SHARED/prompts/05_ai_workflow/` for the current gate.
   - Backtest data + canonical run -> root `AGENTS.md` "DATA & LAUNCH".
   - Results -> dashboard -> `11_TRIAGE/RESULTS_TO_DASHBOARD_MAP_2026-06-29.md`.
   - Authoring an AI/QuantLens verdict -> `03_QUANTLENS/_user_guide/13_AI_VERDICT_AUTHORING_PROCEDURE.md`.
7. After finishing the task: execute Gate 7 (scoped memory write-back per COMPONENT_ROUTER.md Section 5).
