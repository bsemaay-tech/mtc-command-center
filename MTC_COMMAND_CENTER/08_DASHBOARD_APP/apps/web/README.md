# MCC Web App

This folder contains the MVP-1 read-only browser dashboard shell.

## Tabs

- Home
- AI Task Board
- Parity Matrix
- Backtest Summary
- Strategy Registry
- Pine Builder
- Optimization Lab
- LiveOps Dry-run
- Reports
- Diagnostics

## Read-only Interactions

- Task search and status filtering
- Pine draft status inspection
- Optimization run, candidate, and risk note inspection
- LiveOps dry-run safety gate and paper-plan inspection
- Report search and category filtering
- Report manifest item viewer for local Markdown/text reports

## Run

Serve through the read-only API:

```powershell
cd MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api
python -m mcc_readonly serve --host 127.0.0.1 --port 8765
```

Open `http://127.0.0.1:8765/dashboard`.

The web shell consumes `/healthz` and `/api/snapshot`. It does not expose write controls.
