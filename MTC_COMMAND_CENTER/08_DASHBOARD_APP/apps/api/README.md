# MCC Read-only API

MVP-1 starts with a dependency-free Python read-only API core. It reads MCC JSON files, validates them against local schemas, and exposes health/read-model payloads.

## Commands

Run from this directory:

```powershell
python -m mcc_readonly health
python -m mcc_readonly read-model
python -m mcc_readonly snapshot
python -m mcc_readonly serve --host 127.0.0.1 --port 8765
```

Endpoints when served:

- `GET /dashboard`
- `GET /healthz`
- `GET /api/read-model`
- `GET /api/snapshot`
- `GET /api/report?path=<manifest_report_path>`

All mutation verbs return `405`. MVP-1 does not run backtests, shell commands, or MTC_v2 subprocesses.

## Controlled Writer CLI

MVP-2 introduces a local CLI write gate for task proposals. The HTTP API remains read-only.

```powershell
python -m mcc_readonly process-inbox
python -m mcc_readonly task-diagnostics
python -m mcc_readonly liveops-status
python -m mcc_readonly parity-status
python -m mcc_readonly backtest-status
python -m mcc_readonly optimization-status
python -m mcc_readonly registry-status
python -m mcc_readonly pine-builder-status
```

The writer reads `02_TASKS/inbox/*.json`, applies accepted `create_task` proposals through the task lock and schema validation path, writes receipts under `02_TASKS/outbox`, and appends status events.
