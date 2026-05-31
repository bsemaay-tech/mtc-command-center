# MVP-1 Read Model

MVP-1 is read-only. The API or static reader may read only these files:

| File | Schema / Contract | Required |
|---|---|---|
| `03_STATUS/CURRENT_STATUS.json` | `06_SCHEMAS/current_status.schema.json` | Yes |
| `02_TASKS/TASK_QUEUE.json` | `06_SCHEMAS/task_queue.schema.json` | Yes |
| `02_TASKS/TASK_HISTORY.json` | `06_SCHEMAS/task_history.schema.json` | Yes |
| `03_STATUS/PARITY_STATUS.json` | `06_SCHEMAS/parity_status.schema.json` | Yes |
| `03_STATUS/BACKTEST_STATUS.json` | `06_SCHEMAS/backtest_status.schema.json` | Yes |
| `03_STATUS/REPORT_MANIFEST.json` | `06_SCHEMAS/report_manifest.schema.json` | Yes |
| `05_REGISTRY/STRATEGY_REGISTRY.json` | `06_SCHEMAS/strategy_registry.schema.json` | Yes |
| `00_CONFIG/paths.example.json` | `06_SCHEMAS/paths.schema.json` | Yes |
| `00_CONFIG/paths.local.json` | `06_SCHEMAS/paths.schema.json` | Optional, gitignored |
| `00_CONFIG/dashboard_config.example.json` | `06_SCHEMAS/dashboard_config.schema.json` | Yes |

Reader behavior:

- Missing required files render warnings, not crashes.
- Invalid JSON renders a diagnostics warning and leaves the related panel in an error state.
- MVP-1 must not write status, task, registry, or report files.
- MVP-1 must not run backtests, parity commands, webhooks, package installs, or shell commands.

Current implementation:

```powershell
cd MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api
python -m mcc_readonly read-model
python -m mcc_readonly snapshot
python -m mcc_readonly serve --host 127.0.0.1 --port 8765
```

HTTP endpoints:

- `GET /healthz`
- `GET /api/read-model`
- `GET /api/snapshot`
- `GET /api/report?path=<manifest_report_path>`

All mutation verbs return `405` with a read-only error payload.
