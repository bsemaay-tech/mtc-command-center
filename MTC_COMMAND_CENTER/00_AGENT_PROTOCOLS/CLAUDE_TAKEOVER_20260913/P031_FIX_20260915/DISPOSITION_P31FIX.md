# P31FIX Disposition

Worktree: `C:/tmp/P031_M1_20260913`
Branch: `feature/p031-m1-20260913-refresh`
Starting HEAD: `96af3eb61bfdf23f3315ca1d984f19407c02b9d5`
Runtime used: Python 3.14.2. Python 3.12 is not installed in this sandbox.

## Findings

| Item | Disposition | Evidence | Tests |
| --- | --- | --- | --- |
| J-01 | FIXED | `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:399`, `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:402` raise `ACCEPTED_EVALUATION_CATALOG_INVALID` for invalid accepted catalog shapes. | `test_accepted_evaluation_catalog_rejects_invalid_shapes` at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py:2827`; `test_accepted_evaluation_catalog_accepts_valid_hash_tuple` at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py:2847`. |
| J-02 | FIXED | `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:557` raises `CATALOG_BACKED_INVALID` for non-bool `catalog_backed`. | `test_catalog_backed_argument_must_be_bool` at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py:2858`. |
| J-03 | FIXED | `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:747` raises `CATALOG_BACKED_WITHOUT_EVALUATION_HASH`; the refusal code is documented at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:315`. | RED arm in `test_configured_catalog_refuses_absent_hash_and_accepts_present_hash` at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py:2927`; existing GREEN present-hash arm remains at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py:2872`. |
| J-04 | FIXED | This disposition corrects the OD-2 citation: unchanged DEMOTED deployment identity is enforced by `DEPLOYMENT_IDENTITY_MISMATCH` at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:832` and `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:833`, not by deployment refresh refusal. | Documentation-only disposition correction. |
| J-05 | FIXED | `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:811` raises `DEPLOYMENT_REFRESH_IDENTITY_INVALID` for invalid registrar refresh identity branches. | `test_deployment_refresh_returns_to_frozen_under_new_composite` covers same identity at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py:2523`, missing identity at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py:2539`, package drift at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py:2555`, and green refresh at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py:2570`. |

## Test Output

Command:

```powershell
python -m pytest MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py -q -p no:cacheprovider
```

Output:

```text
................s.................... [ 33%]
....................... [ 55%]
............................ [ 80%]
.....................             [100%]
108 passed, 1 skipped, 167 subtests passed in 9.25s
```

Command:

```powershell
python -m py_compile MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py
```

Output:

```text
```

Command:

```powershell
py -3.12 --version
```

Output:

```text
No suitable Python runtime found
Pass --list (-0) to see all detected environments on your machine
or set environment variable PYLAUNCHER_ALLOW_INSTALL to use winget
or open the Microsoft Store to the requested version.
```

Command:

```powershell
python -m ruff check --select E9,F821,F811 MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py
```

Output:

```text
C:\Python314\python.exe: No module named ruff
```

## SHA256SUMS.txt

```text
81eedf03b79289dce92019a16a56e21ed9612be8cca16660d1b79095cb7ab816  MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py
80271ea3ef50701cfabc41f7679bfaabe52fd48ee5157e5feca518224ada8983  MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py
```

## Commit Attempt

Command:

```powershell
git -c safe.directory=* add -- MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py
```

Output:

```text
fatal: Unable to create 'C:/LAB/Tradingview_LAB_CLEAN/.git/worktrees/P031_M1_20260913/index.lock': Permission denied
```

HEAD:

```text
96af3eb61bfdf23f3315ca1d984f19407c02b9d5
```

> **Addendum 2026-09-16 (lane-1 review N-1):** row J-04 names `:832-833` (`DEPLOYMENT_IDENTITY_MISMATCH`) as the guard enforcing an unchanged DEMOTED deployment identity; for `DEMOTED` (previous_state in the deep-rung set) the guard that actually fires is `:675-686` (`DEPLOYMENT_REFRESH_ENVELOPE_UNRESOLVED`), which precedes it. `:832-833` is the FROZEN-path guard (post-refresh re-admission), now fenced by `e9e37aec`. Citation corrected here, not in the row text.
