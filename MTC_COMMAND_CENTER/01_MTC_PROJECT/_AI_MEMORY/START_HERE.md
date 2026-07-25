# START_HERE - MTC V2 Component

Component: `MTC_COMMAND_CENTER/01_MTC_PROJECT/`
Root router: [COMPONENT_ROUTER.md](../../_AI_MEMORY/COMPONENT_ROUTER.md)

## Cold-start read order

1. Root `AGENTS.md` (two-tier model, audit roster, safety)
2. This file
3. `CURRENT.md` (live state and active objective)
4. `NEXT_STEPS.md` (what to do next)
5. `DECISIONS.md` (sticky decisions, if relevant)
6. `ACTIVE_FILES.md` (current working set, if relevant)

Do NOT read root `GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, `ACTIVE_FILES.md`, or `SESSION_LOG.md`
for this component unless cross-component coordination is needed.

## Component purpose

MTC V2 Pine strategy development and parity verification.
Python and Pine advance together, layer by layer, with parity passing before moving on.

## Key files

- `03_DOCS/MTC_V2_ARCHITECTURE.md` - architecture source of truth
- `03_DOCS/MTC_V2_INPUT_UI_SPEC.md` - Pine UI spec
- `03_DOCS/RUNBOOK.md` - run and validation commands
- `05_PARITY/` - parity test cases and oracles
- `_AI_MEMORY/CURRENT.md` - live session state

## Protected surfaces

Pine logic, MTC strategy behaviour, and parity files require explicit Barış approval to modify.
See [root DO_NOT_TOUCH.md](../../_AI_MEMORY/DO_NOT_TOUCH.md).

## Gate 7

Update `CURRENT.md` + `NEXT_STEPS.md` always. `DECISIONS.md` / `ACTIVE_FILES.md` if applicable.
Do not touch root volatile histories.
