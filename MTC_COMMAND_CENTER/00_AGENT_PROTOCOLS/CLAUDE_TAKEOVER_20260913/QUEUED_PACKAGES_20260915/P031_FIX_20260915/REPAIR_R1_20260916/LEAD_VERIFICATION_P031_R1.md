# LEAD_VERIFICATION — WP-P0-31 M1, T0 repair round 1 (`e9e37aec`) after the lane-1 exact-Opus REQUEST_CHANGES on `48bd70de` — 2026-09-16 15:4x UTC+3

**Trigger:** Wednesday lane 1 run early (owner: use the Pro allowance) 15:09-15:36 UTC+3: exact `claude-opus-5` xhigh T0 review of `48bd70de` → **REQUEST_CHANGES**, one REQUIRED finding F-1 + ten NITs (`OPUS_QUEUE_20260916/P031/ATTEMPT1_REQUEST_CHANGES_48bd70de/OPUS_T0_REPORT.md`, 611 lines, 43 own arms all as specified).
**F-1:** the OD-7 (6A) revocation guard `p031_lifecycle_ledger.py:832-833` (`DEPLOYMENT_IDENTITY_MISMATCH`) is the only line pair that forces the post-refresh climb to be made under the NEW deployment identity; in the reviewed base it was dead code (no deep-rung→FROZEN arc; FROZEN forbade a deployment identity); OD-7 made it load-bearing and the batch added no test — the reviewer's mutant M-2 (guard removed) left 109 tests green while the ledger accepted a `SHADOW_ELIGIBLE` carrying the revoked identity. D026 class (K-D-01 precedent).
**Role:** Lead = builder of the fence test (disclosed; the candidate's batch was Codex-built, P31FIX and this test Lead-built); T0 cap 3 rounds — round 1.

## Repair (`e9e37aec`, +79/−0, one test, no ledger change)
`test_post_refresh_admission_cannot_reuse_the_revoked_deployment_identity` in `LifecycleLedgerTests`: build to SHADOW under `DEPLOYMENT_A` (`build_to_rung`), registrar refresh SHADOW→FROZEN under `DEPLOYMENT_B` (the existing refresh idiom), assert `SHADOW_ELIGIBLE` carrying `DEPLOYMENT_A` raises `DEPLOYMENT_IDENTITY_MISMATCH`, the candidate stays FROZEN with `DEPLOYMENT_B`, the replay carries only the original `SHADOW_ELIGIBLE`; then the same admission under `DEPLOYMENT_B` is accepted and recorded. Same shape as the reviewer's arm A36.

## Evidence
| Arm | Result | File |
|---|---|---|
| RED (mutant M-2: the two guard lines removed by file swap; ledger restored byte-identical afterwards) | **1 failed / 109 passed / 1 skipped** — exactly the new test (`ValueError not raised`) | `LEAD_RED_ARM_mutant_M2_guard_removed.txt` |
| GREEN (candidate bytes) | **110 passed, 1 skipped, 167 subtests** | `LEAD_PYTEST_GREEN_R1.txt` |
| Ruff | the file's 36 pre-existing findings, 0 new (the 5 000-line test module is not ruff-formatted; left as is) | console |
| Guard | `RESULT: PASS`; staged exactly the test file | `LEAD_GUARD_R1.txt` |
| Gemini delta (`P031_R1_GEMINI`) | COUNTED **PASS**, F1 CLOSED, first guard to fire `:832-833`, mutant would accept, 0 findings; 18 reads / 0 outside | `…/GEMINI/` |

## Roster
Lane 1 re-pinned to `e9e37aec` (launcher, brief + addendum naming the mutant to reproduce, agent brief, queue row); attempt 1 archived. Tonight's launcher re-runs it; Sol Friday generates from the re-pinned brief.

## Carried NITs of the first read (documentary / design; not part of this commit)
N-1 J-04 wording (a guard that never fires for DEMOTED), N-2 a half-named test, N-3 OD-6 replay-seam invariant note, N-4 ambiguous `check_set_version`, N-5 the one-sentence rule too weak/strong, N-6 report omits OD-9/OD-11 and the catalog, N-7 the G1 public seam changed without the amendment its `:18` requires, N-8 dead OD-5 row, N-9 contracts invocation cwd, N-10 OD-7 × OD-10 epoch interaction. To be folded into the M1 record set / the M2 packet as design notes; N-7 needs a G1 amendment line.

Recorded by Claude Opus 5 Lead (session 6, `4a8233`).
