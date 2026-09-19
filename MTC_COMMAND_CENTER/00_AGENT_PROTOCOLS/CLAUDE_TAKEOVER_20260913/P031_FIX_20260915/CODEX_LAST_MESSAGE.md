Implemented the P31FIX code/test repair in the two scoped repo files:

- [p031_lifecycle_ledger.py](C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:747): added `CATALOG_BACKED_WITHOUT_EVALUATION_HASH` and documented it in the catalog refusal docstring.
- [test_p031_lifecycle_ledger.py](C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py:2827): added J-01/J-02/J-03/J-05 coverage, including the refresh identity `None` and package-drift arms.

Wrote lane artifacts:

- `C:\tmp\CLAUDE_P0_RUN_20260913\laneP31FIX_build\DISPOSITION_P31FIX.md`
- `C:\tmp\CLAUDE_P0_RUN_20260913\laneP31FIX_build\SHA256SUMS.txt` verified LF-only

Verification:

```text
python -m pytest MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py -q -p no:cacheprovider
108 passed, 1 skipped, 167 subtests passed in 9.25s
```

`py_compile` passed for both files. Used Python 3.14.2; Python 3.12 is not installed here. Ruff is unavailable: `C:\Python314\python.exe: No module named ruff`.

Commit was blocked by the worktree Git index permission:

```text
fatal: Unable to create 'C:/LAB/Tradingview_LAB_CLEAN/.git/worktrees/P031_M1_20260913/index.lock': Permission denied
```

No commit was created. HEAD remains:

```text
96af3eb61bfdf23f3315ca1d984f19407c02b9d5
```