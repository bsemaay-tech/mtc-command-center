# Go-Live Checklist

## Pre-Go-Live
- [ ] Full test suite green: `python -m pytest mtc_backtest/tests -v`
- [ ] Staging mirror validation complete
- [ ] UAT scenarios completed
- [ ] Known limitations documented

## Rollback Plan
- [ ] Previous release tag recorded
- [ ] Backup generated for `results.db` and artifacts
- [ ] Restore procedure tested (`scripts/backup_restore.py`)

## On-Call Readiness
- [ ] Alert channels configured for parity and checksum failures
- [ ] Incident owner rotation assigned
- [ ] Runbook links shared with on-call members

## Release Decision
- [ ] Final sign-off by maintainer
- [ ] Release notes/changelog updated
