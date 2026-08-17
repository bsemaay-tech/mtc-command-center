# KICKOFF — Transport documentary repairs from the Claude second-flagship audit

Tier T2 documentation/evidence edit. Model `gpt-5.6-sol` (Codex `fourth`), effort xhigh.
Dispatched by the Lead 2026-08-12 ~23:20. **No git mutation. No executable or plan target may
change: the seven frozen targets (`run_p0.sh`, `run_ro.sh`, `transport_runner.ps1`,
`TRANSPORT_PLAN.tsv`, `remote_setup_wpi.sh`, `remote_extract_verify_wpi.sh`,
`remote_close_tree_wpi.sh`) must remain byte-identical.**

## Input — read first

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md`
(34422 B), verdict REQUEST_CHANGES. Its §8 lists six documentary prose repairs. Summary of the
confirmed defects (all re-derived by the auditor; adopt its exact numbers):

- F-2: eleven J banners / eleven `COMMAND:` lines, J5 GREEN-only — prose says "ten", wrong twice
  in one sentence.
- U-1: real OpenSSH executions = 17 (M7 as 8 rows) or 10 (M7 as one arm); L1–L3 start zero;
  never twelve.
- U-2: true by construction but unsupported as evidence — repair the argument (marker gate at
  `:456-461` fires before record-root creation at `:499`; `Flush-Log` writes nothing while
  `RecordReady` false), do not weaken the claim.
- F-1 second half: `f2_config_qa.ps1` fixture not idempotent (`icacls … | Out-Null` never checks
  `$LASTEXITCODE`) — record as a bounded reproducibility disclosure per the auditor's wording.
- The false integrity sentence the verdict names as its acceptance blocker (the self-QA's own
  rule at `:2688-2690` makes a false evidence claim a defect regardless of code) — correct the
  sentence to what the transcript proves.
- N-1 (LOW, optional per the verdict): `Invoke-LocalBind` Ordinal-comparer nit — if you touch
  it at all, adjust classification prose only.

Apply §8 exactly as the verdict specifies; where this summary and the verdict differ, **the
verdict file governs**.

## Binding rules

- Locate by quoted content, not line numbers.
- **Grep every changed count repo-wide** (the round reports echo them) — the verdict explicitly
  requires this for repairs 3/4. Fix echoes only in transport-lane files you own; list any
  echo outside your ownership in the report for the Lead instead of editing it.
- Rule 9b: no unfilled slot under a resolved claim; absolutes/numbers need pasted-line evidence
  or an `External evidence:` label; re-derive carried identities after your final edit.

## Files you own (disjoint — no other lane touches these tonight)

1. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md`
2. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_TRANSPORT.md`
3. Transport round reports under `WPI_BLOCKS_DRAFT/` ONLY where a corrected count is echoed
   (marker-style corrections; do not rewrite history)
4. Your report: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PROSE_REPAIR_REPORT_2026-08-12.md`
   (new) — per-repair before/after, repo-wide grep evidence for every changed count, final
   identity table (all seven targets unchanged + new SELF_QA/STATUS identities), delta-gate
   proof, session-header model/effort.

## Output hygiene

Narrow bands; harness output (if any is quoted) from existing transcripts only — you run
nothing; no large fixture bodies.
