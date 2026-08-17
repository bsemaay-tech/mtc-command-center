# KICKOFF — GLM re-audit of repaired RP6-P0.sh (read-only)

You are GLM-5.2, the independent auditor for this round. Codex (implementer) repaired
RP6-P0.sh per the bounded scope F1/F3/F4 and claims all three closed with RED/GREEN
evidence. You audited this block originally (`RP6_P0_GLM_AUDIT_2026-08-10.md`); now verify
the repair. Report only — modify nothing.

Read (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`):

1. `WPI_BLOCKS_DRAFT/RP6-P0.sh` — repaired block (claimed SHA-256
   `6c5b89456b4b4072969f7c928328d2d0ecb51e8476a15c5a7401f2988c9766f7`).
2. `WPI_BLOCKS_DRAFT/SELF_QA_RP6.md` — repair QA with RED/GREEN transcripts.
3. `WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md` — updated status.
4. `WPI_BLOCKS_DRAFT/RP6_P0_GLM_AUDIT_2026-08-10.md` — your original findings F1–F4.
5. `WPI_BLOCKS_DRAFT/LEAD_ADJUDICATION_RP6_2026-08-10.md` — binding adjudication:
   F2 closed (rc-3 polarity correct), draft-side Pattern 8 repaired separately.
6. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — round 1.4, current binding
   spec (P0 rows section 8.1).

Verify:

- **V1** F1 closed: no false child-execution claim remains; the disclosed child-launch
  surface matches what the code actually does (count the actual child invocations).
- **V2** F3 closed: the intermediate-symlink residual is either eliminated by
  canonicalization or honestly disclosed in the `does_not_establish` line; consistent
  with round-1.4 row 18.
- **V3** F4 closed: the `:?` backstops exist behind the rc-3 input pre-checks and are
  behaviorally falsified in the QA (not just present).
- **V4** No regression: STOP-vs-FAIL truthfulness, rc 0/1/3 contract, numeric-identity
  rule, read-only scope all intact. Check the diff mentality: nothing outside F1/F3/F4
  changed semantically.
- **V5** QA transcripts are literally re-runnable: pick at least one RED and one GREEN
  command and re-run them yourself (local, no host contact); confirm output matches.
- **V6** The block conforms to the round-1.4 spec's P0 rows (numeric identity, capability
  ledger, STOP grammar) and the ten-pattern catalogue (spot-check patterns 1, 4, 8).

Output: verdict line first — `PASS` or `BLOCK: <n> findings` — then one row per V-item
with PASS/FAIL + one-line evidence, then any findings (location, defect, minimal fix).
