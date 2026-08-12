# KICKOFF — pathscope r3 repair (GLM source-level implementer; Lead executes)

You are GLM, running unattended with `-PermissionMode acceptEdits`. **Do not ask for approval;
no human is watching. Never fabricate an execution result** — you cannot run the PowerShell
harness on this host; the Lead runs it after you finish and your report must mark every
execution step `PENDING-LEAD-EXECUTION`. Tier T1 repair, source-level. No git mutation.

## Input — read in this order

1. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_CLAUDE_T1_EXEC_AUDIT_2026-08-12.md`
   — the flagship execution verdict (REQUEST_CHANGES). Finding **C-1 (CRITICAL)** is the work
   order; its §"Recommended next steps" constrains the fix shape.
2. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py` (122446 B,
   `890016f0…`) — the artifact under repair.
3. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SELF_QA_PATHSCOPE.md` — the evidence
   document with the embedded harness and D026 table.

## The repair — binding shape, from the verdict

**C-1:** variable assignment prefixes (`VAR=value cmd`, and assignment-only commands feeding
`LD_PRELOAD`/`LD_LIBRARY_PATH`/`BASH_ENV`-class loader behaviour) are discarded with no PATH
record and no coverage record, so an out-of-allowlist loader path returns `PASS rc=0`.

Fix **fail-closed on the construct, not on a name list**: extract assignment values; emit a
PATH row when the value is path-shaped; emit a `kind=coverage` record when it is not. **Do NOT
implement a name-based `LD_*`/`BASH_ENV` allowlist as the whole fix** — the verdict explicitly
warns that repeats the round-1 `NO_PATH_COMMANDS` mistake and fails open on the next variable
nobody listed.

Also fold in the cheap items: the `:325-327` wording fix (exact replacement text is in the
verdict), the U-3 evidence citation, and NIT-1 (`ENDPOINT` rows read `ALLOW-LEXICAL` like
`PATH` rows do).

## D026 discipline

Extend the D026 fixture table with RED fixtures against the delivered r2 bytes proving the
C-1 acceptance (assignment-prefix fragment → r2 PASS) and GREEN expectations for r3 (same
fragment → PATH row or coverage record, non-zero rc where the row is out-of-allowlist). Write
the fixtures and expected outputs; mark actual transcripts `PENDING-LEAD-EXECUTION`. Keep the
harness's pinned-blob RED-before-GREEN structure; update the harness section for r3 the same
way r2 did, with the r3 identity slots left as explicit `<FILLED-AFTER-LEAD-RUN>` markers.

## Authoring rules (binding)

1. No unfilled slot under a "resolved" claim — every pending slot sits under a heading that
   says PENDING.
2. Absolutes and numbers need pasted evidence or an `External evidence:` label.
3. Re-derive every identity you state from current bytes; the r2 identity is history once you
   edit, and your report must carry the new `pathscope_prover.py` bytes + SHA-256.

## Files you own (disjoint — nothing else)

1. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py`
2. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SELF_QA_PATHSCOPE.md`
3. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/STATUS_PATHSCOPE.md`
4. Your report: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_R3_REPAIR_REPORT_2026-08-13.md`
   (new) — per-item repair evidence, new identities, the exact Lead-execution checklist
   (commands + expected summary lines), and an honest statement that no harness was executed
   by this lane.
