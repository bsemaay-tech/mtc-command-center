# Common Failure Playbook

## `FileNotFoundError` for case paths in runbook
- Use `powershell -File .\runbook.ps1 ...` from any directory.
- Runbook resolves cases via `$PSScriptRoot`; avoid manual `mtc_backtest\...` prefixes.

## `NameError: timezone is not defined` in replay-candidates
- Use current `src/optimizer_v0/replay_candidates.py` (contains explicit timezone import).
- Re-run tests: `python -m pytest tests/test_replay_crash.py -v`.

## `--db + --out existing CSV requires --run-id`
- Use a fresh output CSV filename, or pass `--run-id`, or delete stale CSV artifact.

## Missing/corrupt artifact files
- Validate outputs before downstream steps:
```powershell
python scripts/artifact_guard.py --required-csv results/replay_target1.csv --required-csv results/replay_target2.csv
```

## Parity drift suspicion
- Use checklist: `docs/strategy_properties_checklist.md`
- Use compare tooling:
```powershell
python scripts/compare_tv_web_trades.py --tv <tv.csv> --py <py.csv> --out <diff.csv>
python scripts/first_divergence_finder.py --report <diff.csv>
```
