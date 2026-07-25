# AGENTS.md - MTC V2 Component

Inherits root two-tier model, canonical audit roster, safety gates, and parallel-agent safety
from [root AGENTS.md](../../AGENTS.md). Read root AGENTS.md first.

## Routing

This component's onboarding chain:
`01_MTC_PROJECT/AGENTS.md` -> `_AI_MEMORY/START_HERE.md` -> `_AI_MEMORY/CURRENT.md` -> `_AI_MEMORY/NEXT_STEPS.md`

Do NOT load root `GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, or `ACTIVE_FILES.md` for component-scoped tasks.
`SESSION_LOG.md` is retired historical-only — never load it as a cold-start file.

## Scope

Active development target: **MTC V2**.
V1 and legacy backtest engine are reference-only.

## Source of truth

- Architecture: `03_DOCS/MTC_V2_ARCHITECTURE.md`
- Pine UI spec: `03_DOCS/MTC_V2_INPUT_UI_SPEC.md`
- Session state: `_AI_MEMORY/CURRENT.md` (live); `_AI_MEMORY/HANDOFF.md` (compatibility pointer)
- Run/validation commands: `03_DOCS/RUNBOOK.md`

## Non-negotiables

1. Parity-first development.
2. Pine and Python advance together, same layer.
3. Do not advance to the next layer before the current layer passes parity.
4. Do not add new features; work only within the requested scope.
5. Do not redesign the architecture during implementation.
6. On ambiguity: leave a short note and surface the blocker. Do not invent behaviour.
7. Update `_AI_MEMORY/CURRENT.md` before stopping.

## Build vs Validate

- **Build:** write/modify code.
- **Validate:** run, test, parity comparison, audit.
- Do not suggest or assume run commands unless Validate is explicitly in scope.

## Pine policy

- Pine side is handled as a single physical file.
- `LIB_*` names are logical module families; do not assume separate Pine library files.
- Input surface, strategy declaration, orchestration, and final wiring remain in the main Pine file.

## Coding policy

- Minimal change.
- Do not break owner boundaries.
- Do not duplicate state ownership.
- Do not copy the same logic to two places.
- No broad refactor without tests/verification.

## Gate 7 write-back (component-scoped)

Update `_AI_MEMORY/CURRENT.md` and `_AI_MEMORY/NEXT_STEPS.md` (always).
Update `_AI_MEMORY/DECISIONS.md` / `_AI_MEMORY/ACTIVE_FILES.md` if applicable.
Do NOT touch root volatile histories.
