# Dashboard App

This folder contains the implemented MTC Command Center dashboard, its local
HTTP API, and the browser assets it serves.

## Launch locally

From the repository root, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\MTC_COMMAND_CENTER\08_DASHBOARD_APP\run_dashboard_server.ps1
```

The launcher changes to `apps/api`, runs `python -m mcc_readonly`, starts the
server on `127.0.0.1:8765`, and asks the default browser to open:

`http://127.0.0.1:8765/dashboard`

Stop the server with `Ctrl+C` in its terminal. `START_DASHBOARD.bat` is an
optional convenience launcher that also attempts to start a Cloudflare tunnel;
`cloudflared` is not required for the local dashboard.

## Implemented routes

The local server currently exposes these GET routes:

- `/` - service metadata and the endpoint list
- `/dashboard` - the browser dashboard (`apps/web/index.html`)
- `/web/<asset>` - static dashboard assets
- `/healthz` - dashboard health report
- `/api/read-model` - read-model diagnostics
- `/api/snapshot` - dashboard snapshot; `?refresh=1` requests a cache refresh
- `/api/report?path=<report-path>` - a report listed by the dashboard manifest
- `/api/scorecard-detail?strategy_id=<id>` - scorecard details for a strategy

## Read-only boundary

The served dashboard and HTTP API are read-only. POST, PUT, PATCH, and DELETE
requests return HTTP 405. The normal launcher does not invoke a writer.

The same Python package also exposes a separate `process-inbox` CLI subcommand
for the MVP-2 controlled task-proposal writer. That command is outside the
read-only dashboard/API boundary and must be treated as an explicit write
operation.

## Prerequisites

- Windows PowerShell for `run_dashboard_server.ps1`
- A `python` command available on `PATH`
- Local port `8765` available for the default launch

The launcher does not install dependencies or configure Python.

## Troubleshooting

- If the browser does not open automatically, navigate to
  `http://127.0.0.1:8765/dashboard` manually.
- If port `8765` is already in use, start the server on another local port from
  `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api`:

  ```powershell
  python -m mcc_readonly serve --host 127.0.0.1 --port 8766
  ```

  Then open `http://127.0.0.1:8766/dashboard` manually.
- If PowerShell reports that `python` is not recognized, make the required
  `python` command available on `PATH` before retrying.
