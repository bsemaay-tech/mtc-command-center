# LiveOps Adapter

This adapter layer is dry-run only. It may simulate signal routing, alert
payloads, state transitions, safety gates, and audit logs, but it must not send
webhooks, create broker clients, or place orders.

## Dry-Run Adapter

`dry_run_adapter.py` accepts one all-gate artifact, generates a representative
signal event, runs the no-execution lifecycle, and writes:

- `<strategy>__<symbol>__<tf>.dry_run_evidence.json`
- `<strategy>__<symbol>__<tf>.readiness.json`

Example:

```powershell
python MTC_COMMAND_CENTER\07_ADAPTERS\liveops\dry_run_adapter.py `
  --artifact-in MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\fam_templates_2026-06-06\all_gate_g3enriched\QL_FAM_MOMENTUM_CONTINUATION__TRXUSDT__4h.eval.json `
  --out-dir MTC_COMMAND_CENTER\03_STATUS\dry_run_evidence_2026-06-06 `
  --status-out MTC_COMMAND_CENTER\03_STATUS\LIVEOPS_STATUS.json
```

## Safety

The adapter forces `dry_run=true`, `live_trading_enabled=false`,
`webhook_sending_enabled=false`, and `broker_integration_enabled=false` in the
status output. Unsafe live/webhook/broker flags are recorded as a fail-safe
case and skipped.
