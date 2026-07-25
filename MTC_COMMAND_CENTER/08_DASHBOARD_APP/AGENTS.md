# AGENTS.md - Dashboard App Component

Inherits root two-tier model, canonical audit roster, safety gates, and parallel-agent safety
from [root AGENTS.md](../../AGENTS.md). Read root AGENTS.md first.

## Routing

This component's onboarding chain:
`08_DASHBOARD_APP/AGENTS.md` -> `_AI_MEMORY/START_HERE.md` -> `_AI_MEMORY/CURRENT.md` -> `_AI_MEMORY/NEXT_STEPS.md`

Do NOT load root volatile histories for component-scoped tasks.

## Scope

MCC Dashboard App: read-only API server and web UI (Strategy Intelligence Command Center).
- API: `apps/api/` (Python, dependency-free, `/healthz`, `/api/read-model`, `/api/snapshot`)
- Web UI: `apps/web/` (vanilla HTML/JS/CSS, dark command-center theme)
- Launch: `START_DASHBOARD.bat` or `run_dashboard_server.ps1`

## Protected surfaces

- Dashboard is read-only: no write controls, no backtest triggering, no broker/paper/live execution.
- Do not imply or introduce backtest, broker, paper, or live execution capability.
- Web UI must follow the dark command-center reference (teal/blue/amber/red accents); do not revert to a light admin skeleton.
- No new dependencies without explicit Barış approval.

## Non-negotiables

1. API remains read-only; no write endpoints without explicit approval.
2. No React runtime; vanilla HTML/JS/CSS only.
3. Dashboard must not imply execution capability.

## Gate 7 write-back (component-scoped)

Update `_AI_MEMORY/CURRENT.md` and `_AI_MEMORY/NEXT_STEPS.md` (always).
Update `_AI_MEMORY/DECISIONS.md` / `_AI_MEMORY/ACTIVE_FILES.md` if applicable.
Do NOT touch root volatile histories.
