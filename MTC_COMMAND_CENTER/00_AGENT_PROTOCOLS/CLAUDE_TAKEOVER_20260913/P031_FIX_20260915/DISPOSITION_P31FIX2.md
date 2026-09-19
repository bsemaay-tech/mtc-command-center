# P31FIX2 Disposition — Lead-authored (Codex routes capped 2026-09-15; disclosed)

Worktree: `C:/tmp/P031_M1_20260913`, branch `feature/p031-m1-20260913-refresh`.
Starting HEAD: `bd0d56d07eebf22ebbc1cdc96a27ddabeacd7acc` → new HEAD **`48bd70dec54aba83dd4270fa0bef97b542163bda`** (backup-pushed).
Author: Claude Opus 5 Lead (session 743291) — every Codex home answered "usage limit" (secondary/fourth until 2026-09-19 18:47 local, free until 2026-09-19 11:10, third until 2026-10-06); OpenCode Go hung on a trivial probe; the Gemini coder wrapper needs PowerShell 7 (absent). The Lead wrote the one test from its own probe (`LEAD_registrar_fail_open_probe.py`) and discloses it so the reviewers weigh the authorship; acceptance still requires the independent roster (Gemini delta, exact Sol, exact Opus).

| Item | Disposition | Evidence | Test |
|---|---|---|---|
| K-D-01 (Gemini delta, REQUIRED) = Lead P31FIX-L-1 | FIXED | test-only change (+56 lines); `p031_lifecycle_ledger.py` untouched | `test_registrar_refresh_with_catalog_backed_claim_requires_evaluation_hash` at `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py:2946-3001`: registrar refresh SHADOW→FROZEN with `catalog_backed=True` on a catalog-configured ledger → `ValueError` `CATALOG_BACKED_WITHOUT_EVALUATION_HASH`, state stays SHADOW; the same refresh without the claim → FROZEN with the new deployment identity |

## RED / GREEN (pinned Python 3.12.12, `-p no:cacheprovider`)
RED — scratch tree with the PRE-FIX ledger (`git show 96af3eb6:…/p031_lifecycle_ledger.py`, sha256 `2e54ee7b…`) + this test file (`LEAD_RED_prefix_ledger.txt`):
```text
E       AssertionError: ValueError not raised
FAILED MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py::LifecycleLedgerTests::test_registrar_refresh_with_catalog_backed_claim_requires_evaluation_hash
1 failed, 109 deselected in 0.54s
```
GREEN — worktree (`LEAD_GREEN_worktree.txt`): `1 passed, 109 deselected in 0.43s`.
Full module (`LEAD_PYTEST_312.txt`): `109 passed, 1 skipped, 167 subtests passed in 23.43s`. `py_compile` OK; Ruff 0.16.4 `--select E9,F821,F811` `All checks passed!`; repo guard `RESULT: PASS` (`LEAD_GUARD.txt`); staged set = the one test file.

## SHA256SUMS.txt
See `SHA256SUMS.txt` (LF) beside this file.
