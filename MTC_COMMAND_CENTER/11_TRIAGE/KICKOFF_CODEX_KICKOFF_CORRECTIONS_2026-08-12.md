# KICKOFF — apply the second-pass preflight corrections to the four Claude Pro kickoffs

Tier T2 documentation edit. Model `gpt-5.6-sol` (Codex `fourth`), effort xhigh. Dispatched by the
Lead 2026-08-12 ~21:10, ahead of the 23:00 Claude Pro window. Time-critical: your edits must be
complete and your report written well before 23:00.

## Mission

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_CLAUDEPRO_KICKOFF_PREFLIGHT_2026-08-12.md` (working-tree
version, second-pass, "Gate: T2 static. Overall verdict: NO-GO") lists exact corrections for the
four Claude Pro kickoffs. The Lead has independently re-derived the full transport hash table,
the `RP7-WPI-RO.sh` identity (108301 B, `0e93f90d…`), and the existence of every cited path —
all match. Your job: **apply every correction in that report, exactly as specified.**

## Files you own (disjoint — no other lane touches these tonight)

1. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md`
2. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_RP7_2NDFLAGSHIP_AUDIT.md`
3. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md`
4. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_CLAUDEPRO_PATHSCOPE_EXECUTION_AUDIT.md`
5. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_TRANSPORT.md` (one bounded edit, §Extra below)
6. Your report: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_KICKOFF_CORRECTIONS_APPLY_2026-08-12.md` (new file)

**No git mutation of any kind. The Lead commits.** Read anything you need; write only the six
paths above.

## Rules of execution

- **Locate every finding by quoted content, not by line number** — the preflight's `:line`
  anchors shift as you edit. Apply corrections bottom-up within each file where practical.
- **Re-derive every hash and byte count yourself before writing it** (`Get-FileHash -Algorithm
  SHA256` / file length). If your derivation disagrees with the preflight's table, STOP on that
  item, record the disagreement in your report, and do not write either value.
- **Do not touch the delta gates** — the preflight marks all four correct.
- **Do not weaken any correction.** Where the preflight gives exact replacement wording (the RP6
  `:4-7` acceptance-scope paragraph, the RP6 `:163` dual-acceptance sentence, the RP6
  indeterminate-count wording, the RP7 extractor sentence), use that wording verbatim.
- The RP6 kickoff must end **internally consistent**: r16 acceptance = historical, no carry to
  r17 bytes; the Claude verdict fills the current-r17 Claude slot only; dual acceptance still
  needs a fresh `gpt-5.6-sol` xhigh audit of r17 evidence.
- Every shorthand basename → full repo-relative path, per the preflight's canonical mapping.
- Add the two missing RP6 known defects (S1 global every-fence contradiction; U4 author-attested
  negatives) with their citations from
  `MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_RP6_2026-08-12.md`.
- Pathscope: add the historical-pinned-regression disclosure exactly as the preflight specifies.

## Extra item — STATUS_TRANSPORT staleness (GLM sweep finding, Lead-verified source)

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_STATUS_VS_BYTES_SWEEP_GLM_2026-08-12.md` found
`STATUS_TRANSPORT.md` stale: header still `REPAIRED-PENDING-REAUDIT`, body never mentions the
round-6 Codex cycle (`TRANSPORT_CODEX_R6_AUDIT` = REQUEST_CHANGES on the false nine-file claim,
`TRANSPORT_CODEX_R6B_CONFIRM` = PASS closing the Codex slot, commit `7e4b5e9f`). Verify those
two audit files say what the sweep claims, then make the **minimal** edit: update the header
state and add a short round-6/6b entry stating the Codex slot is closed and the remaining
pending item is the Claude flagship slot. Change nothing else in that file.

## Report format

For every preflight finding: `finding → APPLIED` (with the exact new text or a pointer to it) or
`finding → NOT APPLIED + reason`. End with: each edited file's new byte size + SHA-256, a
statement that you ran no harness and mutated no git state, and the actual model/effort from
your session header.

## Authoring rules (binding, from §0 Rule 9b of the handoff)

1. No unfilled slot under a "resolved" claim.
2. Absolutes and numbers need line evidence or an explicit `External evidence:` label.
3. Carried-forward values must be re-derived from current bytes.
