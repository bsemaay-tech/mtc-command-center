# LEAD_VERIFICATION_P31FIX — WP-P0-31 correction candidate `bd0d56d07eebf22ebbc1cdc96a27ddabeacd7acc` — 2026-09-15 05:58Z

**Result: candidate VERIFIED by the Lead and committed as `bd0d56d0` on `feature/p031-m1-20260913-refresh` (parent `96af3eb6`), backup-pushed to origin (no PR). NONACCEPTING: delta review (Gemini 3.8 + exact Sol) not started; exact Opus after the 2026-09-16 20:00Z reset.** Lane P31FIX: Codex Plus gpt-5.5 high, 05:40:09-05:48:25Z, exit 0 (commit blocked in the sandbox by the shared index lock, as before; verified on Python 3.14 there).

## Diff inspected (2 files, +113/−1; lane `SHA256SUMS.txt` verified OK)
| Path | Change |
|---|---|
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py` (sha256 `81eedf03…`) | docstring lists the three catalog refusal codes (`:313-319`); **J-03** new refusal `CATALOG_BACKED_WITHOUT_EVALUATION_HASH` when `catalog_backed and evaluation_run_hash is None` (`:746-747`), placed before the writer-class chain |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py` (sha256 `80271ea3…`) | J-05 arms (missing identity, package drift) in `test_deployment_refresh_returns_to_frozen_under_new_composite` (`:2538-2569`); J-01 `test_accepted_evaluation_catalog_rejects_invalid_shapes` (`:2827`) + `..._accepts_valid_hash_tuple` (`:2847`); J-02 `test_catalog_backed_argument_must_be_bool` (`:2858`); J-03 RED arm appended to `test_configured_catalog_refuses_absent_hash_and_accepts_present_hash` (`:2919-2944`) |
J-04 = documentation-only correction in the lane `DISPOSITION_P31FIX.md` (no report rewritten) — matches the brief.

## Lead re-run (pinned Python 3.12.12 `C:/tmp/P020_IMPL_20260912/…/.venv/Scripts/python.exe`, `-p no:cacheprovider`, cwd = worktree)
| Check | Observed |
|---|---|
| `pytest MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py -q` | `108 passed, 1 skipped, 167 subtests passed in 18.50s` (`LEAD_PYTEST_312.txt`; builder on 3.14: same counts, 9.25 s) |
| shared contracts `MTC_COMMAND_CENTER/contracts/tests` | `50 passed` (`LEAD_CONTRACTS_312.txt`) |
| `py_compile` both files | OK |
| Ruff 0.16.4 `--select E9,F821,F811` | `All checks passed!` (`LEAD_RUFF.txt`) |
| `git diff --check` | clean |
| repo guard (dry-run, worktree) | `PINE_ALERT_GUARD PASS files=21 matches=0` → `RESULT: PASS` (`LEAD_GUARD.txt`) |
| staged set | exactly the two paths (`git diff --cached --name-only`) |

## RED-arm evidence (TESTS.md: real RED on exact pre-fix behaviour)
- Scratch tree `C:/tmp/P31FIX_RED_SCRATCH_20260915` = OLD ledger (`git show 96af3eb6:…/p031_lifecycle_ledger.py`, sha256 `2e54ee7b…`) + NEW tests + contracts copy. Selected new tests against the OLD ledger: `1 failed, 3 passed` (`LEAD_RED_ARM_PREFIX_LEDGER.txt`) — the J-03 test fails pre-fix, but with `AssertionError: "CATALOG_BACKED_WITHOUT_EVALUATION_HASH" does not match "EVALUATION_RUN_HASH_REQUIRED"`: for its ENVIRONMENT_ADMISSION_AUTHORITY writer the pre-fix ledger ALREADY refused (older code, `:778-779`). So the builder's RED arm proves the refusal-code precedence, not the fail-open closure. J-01/J-02/J-05 tests are GREEN on both ledgers (they fence pre-existing refusals, as the review asked).
- **The real J-03 fail-open edge is the REGISTRAR path**: deployment refresh (`SHADOW → FROZEN`, registrar writer, catalog configured, `catalog_backed=True`, no hash — registrar events must not carry one). Lead probe `LEAD_registrar_fail_open_probe.py` (reuses the suite's fixtures): pre-fix ledger **APPENDED (fail-open), state FROZEN**; candidate **REFUSED `CATALOG_BACKED_WITHOUT_EVALUATION_HASH`** (`LEAD_REGISTRAR_FAIL_OPEN_PROBE.txt`). The fix closes the edge.
- **Lead finding P31FIX-L-1 (NIT, carried to the delta review):** no permanent test exercises the registrar-path edge; add a registrar refresh with `catalog_backed=True` and no hash as a RED test in the next P031 correction (or the reviewers may require it).

## Next (in order)
1. Gemini 3.8 DELTA review of `bd0d56d0` vs `96af3eb6` (J-01..J-05 RESOLVED/NOT/REGRESSED + P31FIX-L-1) — after the P1CAP detection review (Gemini calls are serial; no Codex builder lane in a worktree meanwhile).
2. Exact Sol review (Codex Plus bucket permitting), exact Opus after Wednesday 20:00Z.
3. PR only after the roster accepts (owner Q4 YES covers the backup push only).

Recorded by Claude Opus 5 Lead (743291).
