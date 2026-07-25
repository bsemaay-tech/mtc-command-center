# START_HERE - MTC Backtest Component

Component: `MTC_COMMAND_CENTER/02_MTC_BACKTEST/`
Root router: [COMPONENT_ROUTER.md](../../_AI_MEMORY/COMPONENT_ROUTER.md)

## Cold-start read order

1. Root `AGENTS.md`
2. This file
3. `CURRENT.md`
4. `NEXT_STEPS.md`
5. `DECISIONS.md` (if relevant)
6. `ACTIVE_FILES.md` (if relevant)
7. `README.md` and `AGENT_PROMPT.md` for engine details

Do NOT read root volatile histories for this component unless cross-component coordination is needed.

## Component purpose

Python backtester porting MTC V2 Pine strategy. Parity suite verifies Python output matches
TradingView bar-by-bar. MTC engine validation is a shortlist-only funnel using `MTCRunner`.

## Key files

- `app.py` - Streamlit entry point
- `src/engine/mtc_runner.py` - main backtest engine
- `src/config/profiles/light_risk.py` - engine validation profile
- `README.md` - quick start and project structure
- `AGENT_PROMPT.md` - agent workflow guide
- `_AI_MEMORY/CURRENT.md` - live session state

## Protected surfaces

- Parity suite and TV CSV data files: never edit.
- MTC strategy behaviour: explicit Barış approval required.
- `mtc_bridge.mjs`: protected.

## Approval gate

ANY backtest, optimization, parity execution, or artifact generation requires explicit Barış approval before proceeding — not only exchange or paper/live execution. Consistent with root `DO_NOT_TOUCH.md`.

## Gate 7

Update `CURRENT.md` + `NEXT_STEPS.md` always. `DECISIONS.md` / `ACTIVE_FILES.md` if applicable.
Do not touch root volatile histories.
