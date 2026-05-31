# Health Checks

MVP-1 exposes `/healthz` or an equivalent local health report.

Implementation:

```powershell
cd MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api
python -m mcc_readonly health
python -m mcc_readonly serve --host 127.0.0.1 --port 8765
```

When the local API is running, `GET /healthz` returns the same contract as the CLI health command.

Required fields:

```json
{
  "api_ok": true,
  "schema_validation_ok": true,
  "lock_dir_writable": true,
  "paths_resolvable": true,
  "mtc_v2_root_reachable": true,
  "warnings": []
}
```

Checks:

- `api_ok`: reader process can start.
- `schema_validation_ok`: required JSON examples parse and match their schema.
- `lock_dir_writable`: lock directories exist and are writable, even before controlled writes.
- `paths_resolvable`: configured paths can be canonicalized.
- `mtc_v2_root_reachable`: configured MTC_v2 root exists and is readable.
