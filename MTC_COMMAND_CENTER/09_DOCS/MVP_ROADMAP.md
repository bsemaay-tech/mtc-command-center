# MVP Roadmap

## MVP-0 Foundation

Create folder structure, architecture location, prompt templates, status files, registries, schemas, adapter notes, dashboard notes, and safety rules.

## MVP-1 Read-only Dashboard

Design and implement a dashboard that reads MCC files without modifying MTC_v2, PineTS, TradingView exports, or live systems.

## MVP-2 AI Task Queue

Define task lifecycle, assignment rules, status transitions, history records, and handoff reports.

## MVP-3 Parity Status Reader

Read existing parity outputs and generate dashboard-ready summaries without altering parity engine files.

Current reader command:

```powershell
cd MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api
python -m mcc_readonly parity-status
```

## MVP-4 Backtest Status Reader

Read backtest outputs and expose latest run summaries, failures, and report links.

Current reader command:

```powershell
cd MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api
python -m mcc_readonly backtest-status
```

## MVP-5 QuantLens Registry

Track research candidates, intake status, and strategy promotion readiness.

Current reader command:

```powershell
cd MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api
python -m mcc_readonly registry-status
```

## MVP-6 Pine Builder Workflow

Track Pine drafts, reviews, compile observations, and promotion gates while protecting production Pine files.

Current reader command:

```powershell
cd MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api
python -m mcc_readonly pine-builder-status
```

## MVP-7 Optimization Lab

Track optimization runs, parameter sweeps, results, and risk notes.

Current reader command:

```powershell
cd MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api
python -m mcc_readonly optimization-status
```

## MVP-8 LiveOps Dry-run Sandbox

Simulate signal operations in dry-run mode only. No live trading or webhook sending.

Current reader command:

```powershell
cd MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api
python -m mcc_readonly liveops-status
```
