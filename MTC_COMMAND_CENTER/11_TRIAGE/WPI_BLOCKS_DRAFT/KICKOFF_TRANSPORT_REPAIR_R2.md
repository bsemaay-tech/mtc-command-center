# KICKOFF — Transport-set round 2: combined repair of both flagship T0 audits

Dispatched by the Claude Lead, 2026-08-10. Round 1 verdicts: Codex xhigh
REQUEST_CHANGES 10 (`TRANSPORT_CODEX_AUDIT_2026-08-10.md`), Claude xhigh
REQUEST_CHANGES 6+5 nits (`TRANSPORT_CLAUDE_T0_AUDIT_2026-08-10.md`). This round must
close BOTH lists (they overlap — the Claude report isolates root causes for several
Codex findings, e.g. the `$Matches` clobber behind the evidence-binder failure). Round
2 of the T0 cap 3.

**Owner amendment A2/A2a in force: implement yourself, no sub-delegation.**

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/`)

1. Both audit reports above — the repair contract. Where they overlap, satisfy the
   stricter reading; where a Claude nit overlaps a Codex required finding, it is
   required.
2. The eight transport files (targets): `run_p0.sh`, `run_ro.sh`,
   `transport_runner.ps1`, `TRANSPORT_PLAN.tsv`, `remote_setup_wpi.sh`,
   `remote_extract_verify_wpi.sh`, `SELF_QA_TRANSPORT.md`, `STATUS_TRANSPORT.md`.
3. `../WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — edit only where a fix
   names a §4/§5/§7 change; list every draft edit in your report.
4. `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — binding pre-read.

## Non-negotiable closures (union highlights — the full lists bind)

- Evidence binder ops 11/12: fix the `$Matches` clobber; a byte-equal remote/local
  pair MUST bind PASS and a differing pair MUST FAIL — both proven RED/GREEN in QA
  with a real `remote_close_tree.sh`-format transcript.
- Runner outcome grammar: child STOP rc 3 propagates as runner not-evaluable (its
  documented exit 3), never rolled into FAIL rc 1; first-FAIL ordering unchanged.
- Program-identity binding: `ssh`, `scp`/transfer tool, `sha256sum`, and every
  executable the runner or wrappers invoke resolved by pinned absolute path (or
  digest-bound), never inherited PATH.
- `remote_setup_wpi.sh`: refuse allocation through an unbound/ambiguous parent; any
  ambiguous path diagnostic is STOP.
- Extractor derivation: bring every changed executable predicate back inside the §4
  permitted constants block, or (if genuinely impossible) record a Lead-visible
  deviation request in the report — do NOT silently widen §4.
- Op 02 cwd per §5; ops 07/08 stdin file existence; `<ALLOCATE-AT-DISPATCH>`
  fail-closed guard; row-24 QA command recorded exactly re-runnable; QA arms for §7
  binding and the process-launch path (8 of 12 ops) — real executed RED/GREEN, no
  stubs (a stub cannot fail).

## Deliverables

Repaired files + extended `SELF_QA_TRANSPORT.md` (every closure with REAL local
RED/GREEN; both auditors' falsification fixtures must flip) + updated
`STATUS_TRANSPORT.md` + narrow draft edits + `TRANSPORT_REPAIR_R2_REPORT.md`
(finding → disposition → evidence, both lists, plus draft-edit list). `bash -n` each
shell file; PS 5.1 parse check; per-file SHA-256 + bytes. Touch ONLY those ten files.
Do not commit.
