# LEAD_ADJUDICATION — P031_R1_GEMINI (delta/detection review of the P0-31 M1 T0 repair round 1: the OD-7 revocation fence test) — 2026-09-16 15:5x UTC+3

Reviewer: gemini-3.8-flash-high, read-only, `SUPPLEMENTAL_UNEXECUTED`. Subject: `e9e37aec` = `48bd70de` + one test (+79/−0), no ledger change. Attempt 1 COUNTED: `SUCCESS`, 87 s, 12:43:55-12:45:33Z; 18 native reads, 0 outside (the patch complete, the helpers 1-420 complete, the new test in context, the ledger guard region 640-880 complete, the first exact-Opus report's F-1 and NITs, every `LEAD_*.txt`).

## Verdict as returned
`PASS`; `finding_F1: CLOSED`; `first_guard_to_fire: p031_lifecycle_ledger.py:832-833 (DEPLOYMENT_IDENTITY_MISMATCH)`; `mutant_would_accept: true`; `findings: []`; `required_scope_unread: []`.

## Comparison with the Lead's evidence
- Guard order for the OLD-identity admission on the candidate: the reviewer's walk agrees with the ledger bytes — `LADDER_IDENTITY_INCOMPLETE` (both hashes present → no), `PACKAGE_IDENTITY_MISMATCH` (PACKAGE_A = frozen package → no), then `:832-833` fires. On the mutant the remaining guards (`DEPLOYMENT_IDENTITY_RETIRED` — the refresh does not retire the old identity; `DEPLOYMENT_IDENTITY_BOUND_TO_ANOTHER_CANDIDATE` — same candidate) let the admission through → `mutant_would_accept: true`, i.e. the test fences `:832-833` specifically. This matches the Lead's RED arm (`LEAD_RED_ARM_mutant_M2_guard_removed.txt`: 1 failed / 109 passed, exactly the new test) and the GREEN (110 passed).
- Whole-invariant check: refused with the exact code; state still FROZEN with `deployment_identity_hash = DEPLOYMENT_B`; the replay carries exactly one `SHADOW_ELIGIBLE` for the candidate (the original); the new-identity admission accepted and recorded — all four asserted.
- Scope: one file, +79/−0 (diff stat read).

## Standing
Repair round 1 stands as reviewed; lane 1 re-pinned to `e9e37aec` for tonight's exact-Opus read; Sol Friday generates from it. The first read's NITs N-1..N-10 are carried as design/record follow-ups (not part of this commit). The Lead never accepts its own code.

Recorded by Claude Opus 5 Lead (session 6, `4a8233`).
