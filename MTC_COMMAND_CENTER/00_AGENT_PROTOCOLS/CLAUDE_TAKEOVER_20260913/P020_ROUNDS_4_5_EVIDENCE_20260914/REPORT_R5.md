# REPORT_R5 — repairing the P0-20 preselection package after T0 round 3, and re-freezing as V1.4

Lane: P20R5, 2026-09-14. Builder role only; not reviewer, not Lead.

**Status: repaired and re-frozen, NOT executed, NOT reviewed, NOT accepted.** No calibration,
eligibility check, benchmark, or simulation on real datasets was run. No valid tokened `--oneshot`
was run. `check_p020_acceptance.py` was not touched. The V1.3 token
`2e67f3f4ea357b4b974313ddd4a427564860e5618f24d48758f07b599da4b614` is dead.

Identity check allowed by the brief:

```text
git -c safe.directory=* -C C:\P020_IMPL_20260912 rev-parse HEAD
b9b72f858dc830a9389517f79da5ea3c1fa6122c
```

## Diff summary per finding

| Finding | Repair |
| --- | --- |
| T1 | `require_t0_authorization` now reads `PRESELECTION_FROZEN.json` exactly once as bytes, compares the token to `sha256(raw)`, parses `json.loads(raw)`, and returns `(frozen, accepted_digest)`. `_run_oneshot` uses that digest for both output records and never re-opens/re-hashes the frozen artifact. `verify_frozen_identity` hashes `preselect_profile.py` from one byte read. |
| T2 | `verify_frozen_identity` now reads, hashes, parses, and returns the verified `BENCHMARK_PLAN.json` object. `_run_oneshot` receives that object and passes it to `_profile`; there is no post-preflight `load_plan()` call in the execution path. |
| T3 | `ReservedOutputs.commit(calibration_payload, eligibility_payload)` writes and flushes both payloads while both handles remain open, then closes both only after success. On any commit exception, both reserved files are seeked/truncated, written as `ABORTED`, flushed, and closed. Existing-output refusal and partial-reservation ABORTED behavior remain. |
| T4 | `PRESELECT_RUNBOOK.md` and `PRESELECTION_PREREG_V1.md` now split outcomes by phase: before any reservation, partial reservation failure, post-both-reservations transaction failure, and normal recorded outcomes. |

## Tests

Command, cwd `C:\tmp\P020_PRESELECT_20260913`:

```text
C:\tmp\P020_IMPL_20260912\01a0924d-2c4b-7da1-99e1-24e2a7c7685c\.venv\Scripts\python.exe -m pytest tests -q -p no:cacheprovider
........................................................................ [ 80%]
..................                                                       [100%]
90 passed in 3.09s
```

Added coverage:

| Finding | Test evidence |
| --- | --- |
| T1 | Frozen file swap after token read: parsed `frozen` remains the hashed bytes, and both output records carry the accepted digest even after the file on disk is swapped. |
| T2 | Plan file mutation after preflight: `_profile` sees the verified in-memory plan marker, not the mutated file. Static source test forbids `load_plan()` in `_run_oneshot`. |
| T3 | First-write failure, second-write failure, and flush failure all leave both reserved files as `ABORTED`. |
| T4 | Documentation-only phase split; existing transaction tests still cover no-output refusal, partial-reservation ABORTED, post-reservation ABORTED, blocked eligibility, and success. |

## Re-freeze

An initial `--freeze` without command-local `safe.directory` refused before writing new bytes:

```text
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xfd in position 129: invalid start byte
PRESELECT_REFUSED_SOURCE_DRIFT: git rev-parse HEAD exited 128
```

The two required freeze runs were then run with command-local `GIT_CONFIG_COUNT=1`,
`GIT_CONFIG_KEY_0=safe.directory`, `GIT_CONFIG_VALUE_0=C:/P020_IMPL_20260912`, matching the prior
review workaround and writing only in this package directory.

```text
EXIT1=0
EXIT2=0
SHA1=f839c9602b6d210dcdf87a0c4ac20f3d04ad68e26949d0f40a5c66f1fdbaf0ff
SHA2=f839c9602b6d210dcdf87a0c4ac20f3d04ad68e26949d0f40a5c66f1fdbaf0ff
BYTES1=18968
BYTES2=18968
BYTE_IDENTICAL=True
TAIL1=FROZEN_WRITTEN C:\tmp\P020_PRESELECT_20260913\PRESELECTION_FROZEN.json sha256=f839c9602b6d210dcdf87a0c4ac20f3d04ad68e26949d0f40a5c66f1fdbaf0ff
LIMITATION SHORT_CALIBRATION_WINDOW_1D 1D rows 2049-2409 (361 rows, 161 usable after 200-bar warmup) -- accepted by owner decision D1 Option A, 2026-09-13
TAIL2=FROZEN_WRITTEN C:\tmp\P020_PRESELECT_20260913\PRESELECTION_FROZEN.json sha256=f839c9602b6d210dcdf87a0c4ac20f3d04ad68e26949d0f40a5c66f1fdbaf0ff
LIMITATION SHORT_CALIBRATION_WINDOW_1D 1D rows 2049-2409 (361 rows, 161 usable after 200-bar warmup) -- accepted by owner decision D1 Option A, 2026-09-13
```

New frozen digest:

```text
f839c9602b6d210dcdf87a0c4ac20f3d04ad68e26949d0f40a5c66f1fdbaf0ff
```

## Digests

`SHA256SUMS.txt` is written last with LF line endings and covers the review packet. Current file
digests before writing this report's checksum file:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `PRESELECTION_PREREG_V1.md` | 51853 | `beb57c068264db168a07fb69cdf49fd5b0d54f9b24f218c013bc7815854ace5b` |
| `PRESELECTION_FROZEN.json` | 18968 | `f839c9602b6d210dcdf87a0c4ac20f3d04ad68e26949d0f40a5c66f1fdbaf0ff` |
| `PRESELECT_RUNBOOK.md` | 13890 | `757ce32a5bc04dbb8a3422c8ca1c321faec9a993fc5a74948d012467a5f0de4f` |
| `REPORT.md` | 21847 | `47efb87f7e01435a2fcbf9ede484b59f6b41a3673758ea3bdb1f14686766050e` |
| `REPORT_R2.md` | 23752 | `3969621dd0b882b8b88dafe10be02ef71365a73336f46396e9d7c562f15b6541` |
| `REPORT_R3.md` | 33253 | `fe9f765d2a8deeb2861868bc36fc38b731c8bee0cf5b9ab4618614be3ae5ffd5` |
| `REPORT_R4.md` | 33559 | `ee88be55a6a430162a8737112e1739090b9cb77efc25fbab43efbf7b7790ade4` |
| `preselect_profile.py` | 55342 | `c2d435251e58fe372bf422e7f68b81cd9d95e9a1c2c7c720e0c6fbffb664a3af` |
| `tests/test_preselect.py` | 75526 | `a1c9a534f2a3c8c6450544a10bc0cff3a5829e3201aeb9e0305568077f02dbac` |

## Review packet

Reviewable files under `C:/tmp/P020_PRESELECT_20260913/`:

1. `PRESELECTION_PREREG_V1.md`
2. `PRESELECTION_FROZEN.json`
3. `preselect_profile.py`
4. `tests/test_preselect.py`
5. `PRESELECT_RUNBOOK.md`
6. `REPORT.md`
7. `REPORT_R2.md`
8. `REPORT_R3.md`
9. `REPORT_R4.md`
10. `REPORT_R5.md`
11. `SHA256SUMS.txt`

## NOT VERIFIED

- No T0 review, Sol review, Gemini corroboration, Opus review, or Lead acceptance has occurred on
  V1.4.
- No real 45-cell calibration or 15-trial eligibility execution has occurred; no matrix, selection, or
  eligibility result exists.
- The real driver/profile stack was not run end to end; tests use synthetic doubles and refusal paths.
- Worktree cleanliness was not checked because the task forbids git status/diff.
- The command-local `safe.directory` workaround was used only for `--freeze`; no git config was
  written.

This report is a builder report only. It is not a review, not acceptance, and not authorization to
execute.
