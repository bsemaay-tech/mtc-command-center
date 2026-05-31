# Staging Environment Mirror

## Objective
- Keep a production-like staging setup for final release validation.

## Minimum Mirror Requirements
- Same Python version and dependency lock as production (`requirements-lock.txt`).
- Same dataset mount structure (`data/`, `results/`, `reports/`).
- Same runbook entrypoint (`runbook.ps1`) and CLI commands.
- Same parity profiles (`configs/cases/parity_profile_*.json`).

## Validation Steps
1. Run `python -m pytest mtc_backtest/tests -v`.
2. Run a staging optimize/validate cycle with deterministic seed/workers.
3. Produce staging ops metrics:
   - `python scripts/ops_metrics.py ... --out reports/staging_ops_metrics.json`
4. Run health alerts:
   - `python scripts/health_alerts.py --ops-metrics reports/staging_ops_metrics.json --out reports/staging_ops_alerts.json`

## Exit Criteria
- Test suite green.
- Ops metrics `overall_pass=true`.
- No parity drift and no checksum mismatch alerts.
