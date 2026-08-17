# KICKOFF — Codex T0 re-audit: transport round 5

Date: 2026-08-11. Codex `gpt-5.6-sol` xhigh, AUDITOR of record, fresh session. Read-only:
edit nothing except your verdict file, no git mutation, no host, no network. T0 surface.

## OUTPUT-HYGIENE (a prior transport audit was killed by the content filter)

When you run any fixture, redirect its stdout to a file; in your own output quote only
SUMMARY lines (`SCRIPT_RC=`, `RESIDUE_PRESENT=`, `TR_RUN ...`, `CLOSE_STOP ...`) and counts.
Refer to any sensitive path/startup fixture by symbolic name (`SENSITIVE_SYS_FILE`,
`STARTUP_PLANT`), never the raw literal. Write the verdict + findings FIRST, evidence after.

## Bytes under audit — commit `37a87046`

Nine transport files + `SELF_QA_TRANSPORT.md`, `STATUS_TRANSPORT.md`,
`TRANSPORT_R5_REPORT_2026-08-11.md`, `_r5_wsl_fixtures.sh`, and the two prereg drafts
(`WPI_PREREGISTRATION_DRAFT.md`, `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md`).

## Your round-4 findings (both bands REQUEST_CHANGES)

Band B: F1 "closed on the composition" overclaim. Band A: BA-1 (cleanup armed after
post-creation STOP → residue), BA-2 (false `declare -F` second-defect claim), BA-3 (T8
prose overstates the two prerequisite reason tokens).

## Round-5 dispositions to verify

- **F1 → OPEN.** Verdict corrected to "inner child closed; outer SSH account-shell boundary
  open" in the report, self-QA §R4-1/§R4-4, runner + five script comments, and both prereg
  drafts. Verify NO residual text anywhere claims F1 closed on the composition or the
  startup residual unreachable. This is a wording/consistency check — no exploit reproduction.
- **BA-1 → repaired, D026 in §R5-1.** mkdir rc + diagnostics captured without stopping;
  cleanup armed before diagnostic adjudication on rc 0. RED (pre-repair blob `29b6412a…`)
  `RESIDUE_PRESENT=yes`, GREEN `RESIDUE_PRESENT=no`, same instrument/launch/argv; the fence
  discriminating-power block quotes both old and new assertion. A NONZERO mkdir is
  deliberately uncovered and STOPs recording `object_after_failed_create=`. Reproduce the
  RED and GREEN yourself (redirect output; report only `SCRIPT_RC`/`RESIDUE_PRESENT`), and
  confirm the fence is not weakened.
- **BA-2 → claim withdrawn.** Bare `declare -F` returns 0; the guard is kept as no-op
  hardening, and the report + five scripts are corrected. Confirm no false RED remains.
- **BA-3 → prose narrowed** (not the classifier) in report + both prereg drafts; the two
  successor occurrences must stay byte-identical (`grep -c 'first applicable reason recorded'`
  = 2). Confirm the narrowed prose matches the classifier's actual reason-token order.

Also: verify census 37/38 unchanged, `bash -n` clean ×5, PS 5.1 parse clean, 0 CR bytes.
Hunt new defects with the 13 patterns. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES /
BLOCK. Note: F1 being honestly OPEN is NOT a blocker to accepting the round — it is the
correct disposition; the block simply is not freezable until F1 is later closed by a
mechanism acting before account-shell startup (out of this round's scope).

Write ONE new file: `TRANSPORT_CODEX_R5_AUDIT_2026-08-11.md`.
