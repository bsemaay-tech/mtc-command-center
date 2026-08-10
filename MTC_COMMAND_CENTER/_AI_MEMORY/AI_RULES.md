# AI_RULES

GStack-inspired workflow rules for any AI agent (Codex / Claude / Gemini)
working in this repository. Read **after** `AGENTS.md` and `START_HERE.md`.

This file does **not** replace the existing memory files. It is the rule
layer on top of them. Canonical state lives in:

- `GLOBAL_HANDOFF.md`   — last session status
- `NEXT_STEPS.md`       — what to do next
- `DECISIONS.md`        — sticky decisions
- `DO_NOT_TOUCH.md`     — protected files / behaviour
- `ACTIVE_FILES.md`     — current working set
- `SESSION_LOG.md`      — RETIRED 2026-07-05 (Barış): do not write; GLOBAL_HANDOFF.md covers it
- `SESSION_LOCK.md`     — write-session lock state
- `PROJECT_MEMORY.md`   — stable repo facts (layout, modules, contracts)

Strategy-research layer (read before combining strategies/indicators):
- `STRATEGY_COMPONENT_LIBRARY.md`     — human-readable inventory + combine guidance
- `STRATEGY_RESEARCH_WORKFLOW.md`     — 16-step research process (points to backtest rules)
- `STRATEGY_CODE_REVIEW_CHECKLIST.md` — repaint/lookahead/conversion safety
- `05_REGISTRY/STRATEGY_RESEARCH_REGISTRY.json` + `INDICATOR_/COMPONENT_REGISTRY.json` + `TAG_DICTIONARY.json` — machine-readable taxonomy (generated; do not hand-edit)
- `05_REGISTRY/RESEARCH_RUN_/VARIANT_LOG_/RESEARCH_BACKTEST_REGISTRY.json` — research records shown in the **Strategy Research Lab** dashboard tab

## 7 Gates (must pass before claiming "done")

### Gate 1 — Scope Review (before coding)

**Actor: Lead Orchestrator.** Scope definition and acceptance authority rest with the lead. If the counterpart implementer CLI is unavailable, surface the blocker here and do not self-implement.

- Restate user request in 1–2 lines.
- User value: why does this matter?
- Smallest safe change that delivers value.
- Files allowed (whitelist).
- Files forbidden — cross-check `DO_NOT_TOUCH.md`.
- **Audit tier classification (T0/T1/T2/T3) — mandatory, recorded before audit dispatch** (see `AGENTS.md` § AUDIT TIER POLICY — PERMANENT DEFAULT).
- Success criteria: how do we know it works?

Prompt: `04_SHARED/prompts/05_ai_workflow/01_office_hours_scope_review.md`

### Gate 2 — Engineering Plan (before architecture change)

**Actor: Implementer.** Produces the plan; passes it to the Lead for acceptance before Gate 3 may begin.

- Data flow diagram or description.
- Affected modules.
- Edge cases.
- Rollback plan.
- Parity / Pine / MTC impact statement.

Skip Gate 2 for trivial doc / typo / single-line fixes.
Prompt: `04_SHARED/prompts/05_ai_workflow/02_engineering_plan_review.md`

### Gate 3 — Implementation

**Actor: Implementer.**

- Minimal diff.
- No unrelated edits.
- No speculative features, no premature abstractions.
- Stay inside the whitelist from Gate 1.

Prompt: `04_SHARED/prompts/05_ai_workflow/03_implementation_task.md`

### Gate 4 — QA / Tests

**Actor: Implementer (self-QA).** Produces concrete evidence for Lead review at Gate 5. Do not claim PASS without verifiable output.

- Run tests if a suite exists.
- Run lint / typecheck if configured.
- Note parity regression risk explicitly (parity suite = sacred).
- If UI / chart change: visually verify, do not assume.

Prompt: `04_SHARED/prompts/05_ai_workflow/05_qa_test_review.md`

### Gate 5 — Tiered Independent Cross-Model Review (Lead's independent inspection)
- The **LEAD ORCHESTRATOR** runs this gate — not the implementer. See two-tier model in `AGENTS.md`.
- **Auditor count, effort, and round cap are decided by the audit tier** — see `AGENTS.md` § AUDIT TIER POLICY — PERMANENT DEFAULT. T0: 2 independent flagships (`claude-opus-5` + `gpt-5.6-sol`) at `xhigh`, max 3 rounds. T1: 1 flagship (alternate Claude/Codex per round) at `high`, plus GLM-5.2 second opinion only if the flagship raises findings or the diff exceeds ~300 lines, max 2 rounds. T2: single reviewer, single round, GLM-5.2 preferred / DeepSeek acceptable / flagship at `medium` only if neither is available, max 1 round. T3: implementer self-verification only, no model audit, max 0 rounds. Exact model identity for invoked slots per `AGENTS.md` §CANONICAL AUDIT ROSTER; no implicit alias, no silent fallback — BLOCK if unavailable unless Barış waives.
- **Fresh independent session every round** — never resume or continue the implementer session.
- The lead independently inspects the actual diff/files; accepting the implementer's self-report alone is not Gate 5.
- Reviewer reads adversarially: assume the diff is wrong, prove otherwise.
- Flag: missing edge cases, hidden coupling, parity risk, DO_NOT_TOUCH violations, scope creep.
- Verdicts: **PASS** / **PASS-WITH-NITS** (accepting, optional nits only) / **REQUEST_CHANGES** (required repair) / **BLOCK** (cannot continue). PASS-WITH-NITS cannot contain a required repair.
- On REQUEST_CHANGES or BLOCK: lead sends focused repair prompt to the same counterpart implementer. **Repair/re-audit rounds capped per tier: T0=3, T1=2, T2=1, T3=0.** After the cap is exhausted with no accepting verdict, stop and report to Barış.

Prompt: `04_SHARED/prompts/05_ai_workflow/04_adversarial_code_review.md`

### Gate 6 — Security Review (only if scope hits security surface)

**Actor: Lead or designated independent reviewer** — must not be the implementer of the change under review. Lead retains final acceptance authority.
**Tier default:** security/auth/secret/network/host/deploy surfaces default to **T0** — two independent flagships (`claude-opus-5` + `gpt-5.6-sol`) at `xhigh` — unless an explicit owner contract says otherwise. Exact model identity per `AGENTS.md` §CANONICAL AUDIT ROSTER; no implicit alias, no silent fallback — BLOCK if unavailable unless Barış waives.
**Verdicts:** PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK.

- Secrets, auth, network calls, file system writes, eval / exec, subprocess.
- Skip for pure doc / Pine plotting / cosmetic changes.

Prompt: `04_SHARED/prompts/05_ai_workflow/06_security_review.md`

### Gate 7 — Memory Write-Back (mandatory before stopping)

**Actor: Lead Orchestrator**, after the tier-required acceptance is verified. For T0/T1/T2 this is a Gate 5 PASS or PASS-WITH-NITS under the recorded auditor contract; for **T3**, recorded implementer self-verification stands in place of a model Gate 5. Implementer may supply factual inputs (commit hashes, test results, file lists); final write-back and authorized sequencing are Lead-owned. See `AGENTS.md` § AUDIT TIER POLICY — PERMANENT DEFAULT.

Every completed task must update:
- `GLOBAL_HANDOFF.md`   — always
- `NEXT_STEPS.md`       — always
- `DECISIONS.md`        — if a sticky decision was made
- `ACTIVE_FILES.md`     — if working set changed
- `PROJECT_MEMORY.md`   — if a stable repo fact changed

Prompt: `04_SHARED/prompts/05_ai_workflow/07_handoff_update.md`

## Hard Safety Rules

- No changes to Pine logic, MTC strategy behavior, or parity files
  without explicit Barış approval.
- Never recommend live trading.
- Never add secrets, tokens, or credentials to the repo.
- Never run destructive git operations (`reset --hard`, `push --force`,
  `clean -fdx`, branch deletion) without explicit approval.
- Never bypass commit hooks (`--no-verify`).
- Cross-check `DO_NOT_TOUCH.md` before every write.

## Entry Point for a Fresh Agent

1. Read `AGENTS.md`.
2. Read `_AI_MEMORY/START_HERE.md`.
3. Read this file (`AI_RULES.md`).
4. Read `GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, `DO_NOT_TOUCH.md`.
5. Pick the right prompt template under
   `04_SHARED/prompts/05_ai_workflow/` for the current gate.
   - Backtest data + canonical run → `AGENTS.md` "DATA & LAUNCH".
   - Results → dashboard → `11_TRIAGE/RESULTS_TO_DASHBOARD_MAP_2026-06-29.md`.
   - Authoring an AI/QuantLens verdict → `03_QUANTLENS/_user_guide/13_AI_VERDICT_AUTHORING_PROCEDURE.md`.
6. After finishing the task: execute Gate 7 (memory write-back).

## GLM Supplemental Routing

For Z.AI Coding Plan model selection when sub-delegating, see `AGENTS.md` §GLM SUPPLEMENTAL ROUTING (canonical source; routing table not copied here). GLM never replaces a flagship slot required by the audit tier or the counterpart flagship implementer. GLM fills **only** auditor slots selected by the tier policy (see `AGENTS.md` § AUDIT TIER POLICY — PERMANENT DEFAULT) and never silently adds a round. Every delegated GLM task requires a routing record (classification, protected flag, model+provider, cheaper-model rationale, exact paths, budget, fallback, external API credits).
