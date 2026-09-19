# LEAD_ADJUDICATION — P031_R2_GEMINI (delta/detection review of the P0-31 M1 T0 repair round 2: the two OD-7 refresh-path fence tests) — 2026-09-17 08:4x UTC+3

Reviewer: gemini-3.8-flash-high, read-only, `SUPPLEMENTAL_UNEXECUTED`. Subject: `61c56148` = `e9e37aec` + two tests + one docstring fix (+158/−2, test file only, no ledger change). Attempt 1 COUNTED: `SUCCESS`, 199 s, 05:41:21-05:44:40Z; 23 native reads over all 15 packet files, 0 outside, 0 content mismatches (`NATIVE_READ_AUDIT_attempt1.json`); 0 "Filesystem changes were observed" although the exact-Opus lane 2 (P1CAP) was running read-only git in another worktree during the call — the overlap is recorded, the call is counted.

## Verdict as returned
`PASS`; `finding_F2: CLOSED`; `first_guard_to_fire_test1: DEPLOYMENT_IDENTITY_RETIRED (:812-813)`; `first_guard_to_fire_test2: DEPLOYMENT_IDENTITY_BOUND_TO_ANOTHER_CANDIDATE (:814-816)`; `mutant_812_would_accept: true`; `mutant_814_would_accept: true`; `findings: []`; `required_scope_unread: []`.

## Comparison with the Lead's evidence
- Test 1 preparatory walk (SHADOW → RETIRED → RE_ENTRY → FROZEN `PACKAGE_B` → SHADOW `DEPLOYMENT_B`): every step accepted, with the bookkeeping named (`deployment_owners[DEPLOYMENT_A]` = the candidate; `retired_deployments` ∋ `DEPLOYMENT_A`; `retired_packages[cid]` ∋ `PACKAGE_A`; the re-freeze passes `:819-820` because `PACKAGE_B` is not retired). Refresh naming `DEPLOYMENT_A`: `:805-811` does not fire (package equal, identity differs) → `:812-813` fires. On the `:812-813` mutant: `:814-816` does not rescue (same owner), `:819-820` does not rescue (`PACKAGE_B`), ladder checks skipped (registrar) → ACCEPTED → the test's `ValueError not raised`. Matches the Lead's RED arm M4 (1 failed / 111 passed, exactly that test).
- Test 2: two candidates in one ledger do not collide (timestamps partitioned per candidate at bookkeeping `:114`; writer sequences per `(writer_class, writer_id)`); refresh of A naming `DEPLOYMENT_B`: `:805-811` no, `:812-813` no (not retired), `:814-816` fires (`deployment_owners[DEPLOYMENT_B]` = `CANDIDATE_B`). On the `:814-816` mutant: nothing else refuses → ACCEPTED, two candidates sharing `DEPLOYMENT_B`. Matches the Lead's RED arm M7.
- Whole invariant: exact codes; state/package/identity unchanged (both candidates in test 2); replay carries exactly the genuine FROZEN records — all asserted.
- Scope: one file, +158/−2; the −2 are exactly the two round-1 docstring lines (N-12). Honesty: REPRO 110/110, RED 1/111 ×2, GREEN 112 + contracts 50, guard PASS — each read from the `LEAD_*.txt` bytes.
- NITs N-1..N-13: none REQUIRED for M1 acceptance in the reviewer's reading; N-12 resolved by this commit; N-11 record fix; N-13 owner question.

## Standing
Repair round 2 stands as reviewed; lane 1 re-pinned to `61c56148` for the third exact-Opus read (round 2 of the T0 cap 3) later today; Sol (Sep 19) generates from the pin that stands then. The Lead never accepts its own code.

Recorded by Claude Opus 5 Lead (session 6, `4a8233`).
