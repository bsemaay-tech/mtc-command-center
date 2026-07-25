# AGENTS.md - MTC Backtest Component

Inherits root two-tier model, canonical audit roster, safety gates, and parallel-agent safety
from [root AGENTS.md](../../AGENTS.md). Read root AGENTS.md first.

## Routing

This component's onboarding chain:
`02_MTC_BACKTEST/AGENTS.md` -> `_AI_MEMORY/START_HERE.md` -> `_AI_MEMORY/CURRENT.md` -> `_AI_MEMORY/NEXT_STEPS.md`

Do NOT load root volatile histories for component-scoped tasks.

## Scope

Python backtester, parity suite, and MTC engine validation for MTC V2.
- Backtest engine: `src/engine/mtc_runner.py`
- Parity suite: `src/` parity scripts, `data/` TV CSVs
- MTC engine validate: `python -m src.cli.mtc_engine_validate` (uses `src/config/profiles/light_risk.py` and adapters under `src/modules/signals/producers/`)
- Run interface: `app.py` (Streamlit) or `RUN_MTC_BACKTEST.ps1`

## Protected surfaces

- Parity suite and TV CSV files: never edit.
- Pine logic and MTC strategy behaviour: never change without explicit Barış approval.
- `mtc_bridge.mjs`: protected.

## Non-negotiables

1. Only edit `src/` and `configs/cases/` unless explicitly authorized.
2. Never edit data files or TV CSVs.
3. After every code change: show `git diff` before running tests.
4. Explicit Barış approval required before ANY backtest, optimization, parity execution, or artifact generation — not only for exchange or paper/live. Consistent with root `DO_NOT_TOUCH.md`.
5. Explicit Barış approval required before running against live or paper exchange (separate gate from #4).

## Gate 7 write-back (component-scoped)

Update `_AI_MEMORY/CURRENT.md` and `_AI_MEMORY/NEXT_STEPS.md` (always).
Update `_AI_MEMORY/DECISIONS.md` / `_AI_MEMORY/ACTIVE_FILES.md` if applicable.
Do NOT touch root volatile histories.
