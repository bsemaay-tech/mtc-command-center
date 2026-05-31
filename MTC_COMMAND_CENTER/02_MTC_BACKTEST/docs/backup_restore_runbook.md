# Backup and Restore Runbook

## Backup
```powershell
cd C:\LAB\tradingview-lab\mtc_backtest
python scripts/backup_restore.py backup --outdir backups --include results --include debug --include reports
```

## Restore
```powershell
cd C:\LAB\tradingview-lab\mtc_backtest
python scripts/backup_restore.py restore --archive backups/<archive>.tar.gz --dest restore_out
```

## Notes
- This is file-level backup for artifacts and reports.
- Database files can be included by adding `--include <path_to_db>`.
