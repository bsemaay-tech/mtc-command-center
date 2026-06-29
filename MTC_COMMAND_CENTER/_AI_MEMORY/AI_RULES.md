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
- `SESSION_LOG.md`      — one-line per session entries
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
- Restate user request in 1–2 lines.
- User value: why does this matter?
- Smallest safe change that delivers value.
- Files allowed (whitelist).
- Files forbidden — cross-check `DO_NOT_TOUCH.md`.
- Success criteria: how do we know it works?

Prompt: `04_SHARED/prompts/05_ai_workflow/01_office_hours_scope_review.md`

### Gate 2 — Engineering Plan (before architecture change)
- Data flow diagram or description.
- Affected modules.
- Edge cases.
- Rollback plan.
- Parity / Pine / MTC impact statement.

Skip Gate 2 for trivial doc / typo / single-line fixes.
Prompt: `04_SHARED/prompts/05_ai_workflow/02_engineering_plan_review.md`

### Gate 3 — Implementation
- Minimal diff.
- No unrelated edits.
- No speculative features, no premature abstractions.
- Stay inside the whitelist from Gate 1.

Prompt: `04_SHARED/prompts/05_ai_workflow/03_implementation_task.md`

### Gate 4 — QA / Tests
- Run tests if a suite exists.
- Run lint / typecheck if configured.
- Note parity regression risk explicitly (parity suite = sacred).
- If UI / chart change: visually verify, do not assume.

Prompt: `04_SHARED/prompts/05_ai_workflow/05_qa_test_review.md`

### Gate 5 — Adversarial Cross-Model Review
- Reviewer model **must differ** from implementer model.
- Reviewer reads adversarially: assume the diff is wrong, prove otherwise.
- Flag: missing edge cases, hidden coupling, parity risk, DO_NOT_TOUCH
  violations, scope creep.

Prompt: `04_SHARED/prompts/05_ai_workflow/04_adversarial_code_review.md`

### Gate 6 — Security Review (only if scope hits security surface)
- Secrets, auth, network calls, file system writes, eval / exec, subprocess.
- Skip for pure doc / Pine plotting / cosmetic changes.

Prompt: `04_SHARED/prompts/05_ai_workflow/06_security_review.md`

### Gate 7 — Memory Write-Back (mandatory before stopping)
Every completed task must update:
- `GLOBAL_HANDOFF.md`   — always
- `NEXT_STEPS.md`       — always
- `SESSION_LOG.md`      — one line
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
