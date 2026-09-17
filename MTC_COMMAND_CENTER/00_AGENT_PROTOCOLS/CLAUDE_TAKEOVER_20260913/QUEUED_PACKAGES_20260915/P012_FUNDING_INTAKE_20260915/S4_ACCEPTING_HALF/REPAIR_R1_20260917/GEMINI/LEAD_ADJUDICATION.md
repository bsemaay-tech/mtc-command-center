# LEAD_ADJUDICATION — P012_INTAKE_R1_GEMINI (delta/detection review of the P0-12 intake slice-4 T0 repair round 1) — 2026-09-17 14:5x UTC+3

Reviewer: gemini-3.8-flash-high, read-only, `SUPPLEMENTAL_UNEXECUTED`. Subject: `a871e429` = `9ef072a8` + the D-6 `position_source` fix + two tests (+94/−14, two files). Attempt 1 COUNTED: `SUCCESS`, 88 s, 11:36:47-11:38:28Z; 19 native reads over all 15 packet files, 0 outside, 0 content mismatches (`NATIVE_READ_AUDIT_attempt1.json`); no Opus lane was running during the call; 0 "Filesystem changes were observed".

## Verdict as returned
`PASS`; `required_1: CLOSED`; `no_fills_branch_reached: true`; `mutants_killed: M1 true, M2 true, M3 true`; `findings: []`; `required_scope_unread: []`.

## Comparison with the Lead's evidence
- No-fills trace: `_real_fills(b"[]", "BTC")` → `(None, [])` and the ETH-only fixture is filtered by symbol → `payments_position = 0.00058`; grid [17:00, 18:00]; expected == observed == both hours; per-row szi check trivially consistent; `completion_check.position_source = REAL_POSITION_SOURCE_PAYMENTS`, `opening_position None` — as the Lead's reproduction and GREEN run show. M1 (→ `Decimal(0)`) empties `expected` → refusal → the accepted-is-True assertion fails; M2 fails the label assertions; the reviewer's kill map matches the Lead's RED files (2/232, 3/232).
- Normal-path trace: `opening_position == "0.0"` from the first fill's `startPosition`, fills label; M3 killed (1/232) — matches.
- Behaviour preservation: no refusal code or message changed; synthetic path untouched; scope exactly two files. Honesty: every `LEAD_*.txt` read and found consistent with the record.
- NITs 1-8 of the first read: documentation/label polish outside this commit; none elevated.

## Standing
Repair round 1 stands as reviewed; lane 8 re-pinned to `a871e429`; the second exact-Opus read runs after the Pro window reopens (18:01 alarm); Sol (Sat) generates from the pin that stands. The Lead never accepts its own code.

Recorded by Claude Opus 5 Lead (session 6, `4a8233`).
