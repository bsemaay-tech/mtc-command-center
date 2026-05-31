# Observability Runbook

## Build Dataset Catalog
```powershell
cd C:\LAB\tradingview-lab\mtc_backtest
python scripts/build_dataset_catalog.py --data-dir data --out-json reports/catalog/datasets.json --out-csv reports/catalog/datasets.csv
```

## Walk-Forward Health Check
```powershell
cd C:\LAB\tradingview-lab\mtc_backtest
python scripts/health_alerts.py --walkforward-summary results/walkforward_smoke/summary.json --out reports/health/walkforward_health.json
```

Exit code `2` means alert condition (missing summary or unhealthy run).
