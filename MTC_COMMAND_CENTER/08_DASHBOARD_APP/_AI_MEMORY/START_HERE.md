# START_HERE - Dashboard App Component

Component: `MTC_COMMAND_CENTER/08_DASHBOARD_APP/`
Root router: [COMPONENT_ROUTER.md](../../_AI_MEMORY/COMPONENT_ROUTER.md)

## Cold-start read order

1. Root `AGENTS.md`
2. This file
3. `CURRENT.md`
4. `NEXT_STEPS.md`
5. `README.md` for app structure

Do NOT read root volatile histories for this component unless cross-component coordination is needed.

## Component purpose

Read-only dashboard serving MCC status and strategy intelligence data.
- `apps/api/`: dependency-free Python read-only API core
- `apps/web/`: vanilla HTML/JS/CSS dark command-center UI

## Key files

- `README.md` - app structure and MVP-1 state
- `apps/api/` - API server
- `apps/web/index.html` - dashboard shell
- `START_DASHBOARD.bat` / `run_dashboard_server.ps1` - launch scripts
- `_AI_MEMORY/CURRENT.md` - live session state

## Visual contract

Dark canvas, compact left navigation, dense dark cards/tables, teal/blue/amber/red status accents,
workflow cards, read-only missing-artifact states. Reference:
[`../../11_TRIAGE/STRATEGY_INTELLIGENCE_DESIGN_CONTEXT.md`](../../11_TRIAGE/STRATEGY_INTELLIGENCE_DESIGN_CONTEXT.md).

## Protected surfaces

- Read-only: no write endpoints, no backtest/broker/paper/live execution.
- No React runtime; vanilla HTML/JS/CSS only.

## Gate 7

Update `CURRENT.md` + `NEXT_STEPS.md` always. `DECISIONS.md` / `ACTIVE_FILES.md` if applicable.
Do not touch root volatile histories.
