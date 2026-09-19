# P31B continuation inventory

Date: 2026-09-14
Worktree: `C:/tmp/P031_M1_20260913`
Branch: `feature/p031-m1-20260913-refresh`

## Guard and git inventory

- `tasklist | findstr /i agy.exe`: no `agy.exe` line observed. Unsuppressed `tasklist` emitted an unrelated Windows `ERROR: Access denied` line while enumerating processes, so later checks used `tasklist 2>NUL | findstr /i agy.exe`.
- `git -c safe.directory=* status --porcelain`: modified `MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py`; modified `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py`; untracked `TASK_P31B.md`; untracked `TASK_P31B_CONT.md`.
- `git -c safe.directory=* diff --stat`: two tracked files changed, 384 insertions and 48 deletions.
- Untracked task files are instruction inputs only and must not be committed.

## Diff inventory by owner item

- OD-2 `DEMOTED`: PARTIAL. Code assigns `DEMOTED` to `MULTI_WORKER_SUPERVISOR` and adds descent validation at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:122`, `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:134`, and `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:688`; however the old refusal test still expects `DEMOTION_TARGET_RUNG_MAPPING_UNRESOLVED` at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py:4598`, so RED/GREEN coverage is incomplete/conflicting.
- OD-5 `REJECTED`: PARTIAL/DONE for main mechanism. Code restores REJECTED transitions and validates supplied purpose/hash/failing checks at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:70`, `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:613`, `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:722`, and `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:765`; tests were updated at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py:671` and `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py:731`. Old deep-history tests still contain stale unresolved expectations at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py:4117`, so re-verification is needed.
- OD-6 capacity withholding target: DONE/PARTIAL pending test run. Code resolves capacity purpose from configured `check_set_version` at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:617` and validates rung/purpose at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:718`. Tests cover accepted SHADOW capacity and wrong-purpose refusal at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py:1978` and `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py:1997`.
- OD-7 deployment refresh: PARTIAL. Code adds registrar refresh detection and identity checks at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:663` and `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:796`, but the old tests still expect `DEPLOYMENT_REFRESH_ENVELOPE_UNRESOLVED` at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py:2477` and `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py:2711`.
- OD-9 `RETIRED -> RE_ENTRY`: PARTIAL. Code adds `OWNER_EXTERNAL_CHANGE` and one-sentence validation at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:95`, `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:261`, and `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:751`; no matching focused tests were found.
- OD-10 same-epoch reuse assertions: DONE/PARTIAL pending test run. The previous no-assertion section now asserts purposes, versions, hashes, and current states at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py:2366`.
- OD-11 catalog: PARTIAL. Code adds optional `accepted_evaluation_catalog`, `catalog_backed`, fail-closed catalog-backed claims, and absent-hash refusal at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:320`, `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:387`, `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:738`, and `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:741`; no catalog-specific RED/GREEN tests were found.
- OD-1 doc-only worthiness wording: NOT STARTED. `DECISIONS.md` is not modified.
- OD-4/OD-8 ratification recording/report text: PARTIAL. Report strings were moved from unresolved to ratified at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:1445`, but the tests still expect the old unresolved strings at `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py:2510` and `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py:4647`. Runbook/report text is not started.

## Required pre-edit ledger test

Command attempted:

```powershell
py -3.12 -m pytest MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py -q -p no:cacheprovider
```

Output:

```text
No suitable Python runtime found
Pass --list (-0) to see all detected environments on your machine
or set environment variable PYLAUNCHER_ALLOW_INSTALL to use winget
or open the Microsoft Store to the requested version.
```

Result: BLOCKED before collection because this machine exposes Python 3.14 and 3.13 only (`py -0p`); Python 3.12.12 from `P031_M1_SCOPE_AND_STATUS.md` is not registered, and no repo `pyvenv.cfg` was found.
