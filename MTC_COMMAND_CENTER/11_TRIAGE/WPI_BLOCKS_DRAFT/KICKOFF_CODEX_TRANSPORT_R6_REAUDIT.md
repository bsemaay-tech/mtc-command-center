# KICKOFF — Codex T0 re-audit: transport round 6 (R5-F2 + R5-F3 closure)

Date: 2026-08-11. Codex `gpt-5.6-sol` xhigh, AUDITOR of record, fresh session. Read-only:
edit nothing except your verdict file, no git mutation, no host, no network. T0 surface.

## OUTPUT-HYGIENE (a prior transport audit was filter-killed)
Redirect any fixture output to files; in your own output quote only summary lines
(`SCRIPT_RC=`, `RESIDUE_PRESENT=`, `REFUSAL_BYTE_IDENTICAL=`, `BA1_ARMS_RECORDED=`,
`DISTINCT_SUBJECT_ARGV_LINES=`). Refer to any sensitive fixture by symbolic name. Verdict
first, evidence after.

## Scope — commit `979552d9`

Round 6 changed ONLY the BA-1 harness + evidence docs; **no transport script byte changed**
(7/7 executable/plan targets byte-identical to round 5). So this is a focused re-audit of the
two round-5 findings that were still open, not a full re-review.

Your round-5 findings now dispositioned:
- **R5-F1 (F1 draft overclaim)** — the Lead applied it directly to both prereg drafts
  (commit `008d2dde`): main draft derivation-class 5 + remote-launch-domain section and
  successor draft now state "inner child closed; outer SSH account-shell boundary OPEN." F1
  itself stays honestly OPEN. Confirm no residual text in either prereg draft claims F1 closed
  on the composition or the startup residual unreachable.
- **R5-F2 (HIGH) — BA-1 arms did not use same argv.** Round 6 rewrote `_r5_wsl_fixtures.sh`:
  10 arms, ONE common subject pathname + ONE common EV/RUNID/`WORK_ROOT` argv, only the
  subject bytes vary. Recorded: RED (pre-repair blob `29b6412a…`) `RESIDUE_PRESENT=yes`, GREEN
  (repaired) `RESIDUE_PRESENT=no`, `REFUSAL_BYTE_IDENTICAL=yes`, `BA1_ARMS_RECORDED=10`,
  `DISTINCT_SUBJECT_ARGV_LINES=1`. The round-5 transcript is WITHDRAWN (one reproducibility
  target). The Lead reran it verbatim and reproduced the RED/GREEN discrimination. Re-run
  §R6-2 yourself (write blob `61696132…` to `<scratch>/r6/pre/remote_close_tree_wpi.sh`, pass
  the block dir + scratch); confirm RED residue present, GREEN absent, byte-identical refusal,
  and that the carried fence (close script line ~402→483) is unchanged and still discriminates.
- **R5-F3 (MEDIUM) — stale "pending" status.** STATUS/report/self-QA now say the draft edits
  are APPLIED and cite commits; `TRANSPORT_R5_DRAFT_EDITS_PENDING.md` is marked SUPERSEDED (not
  deleted). Confirm no "pending"/"not yet landed" claim remains.

Also confirm: census 37/38 unchanged, `bash -n` clean ×5, PS 5.1 parse clean, 0 CR bytes.
Hunt any NEW defect the harness rewrite introduced. Verdict: PASS / PASS-WITH-NITS /
REQUEST_CHANGES / BLOCK. F1 being honestly OPEN is NOT an acceptance blocker for this round —
it is the correct disposition; the block is simply not freezable until F1 is later closed by a
mechanism acting before account-shell startup (out of scope).

Write ONE new file: `TRANSPORT_CODEX_R6_AUDIT_2026-08-11.md`.
