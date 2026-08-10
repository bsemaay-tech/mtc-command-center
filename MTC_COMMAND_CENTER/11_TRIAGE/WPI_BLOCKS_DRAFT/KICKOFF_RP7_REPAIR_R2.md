# KICKOFF — RP7-WPI-RO round 2: repair all 13 audit findings

Dispatched by the Claude Lead, 2026-08-10. You (Codex) authored the block; Claude Opus 5
audited it BLOCK with 13 findings, every one falsified by an executed fixture. Repair
them all. The auditor for the re-audit will again be cross-model.

**The repository's two-tier counterpart-implementer rule is suspended by owner amendment
A2/A2a. Implement this yourself. Do not sub-delegate.**

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`)

1. `WPI_BLOCKS_DRAFT/RP7_CLAUDEPRO_AUDIT_2026-08-10.md` — the audit. Findings 1–13 with
   locations, executed falsifications and minimal fixes. It is the repair contract.
2. `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh`, `SELF_QA_RP7.md`, `STATUS_RP7.md` — repair targets.
3. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — round 1.5 spec. You may edit
   ONLY section 8.2 row text where a Lead adjudication below says so; every draft edit
   must be listed in your report.
4. `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — binding pre-read.
5. `WPI_PREREG_DRAFT_ROUND1/LEAD_PIN_RESOLUTION_2026-08-10.md` — pinned `WPI_LOG_DIR`.

## Lead adjudications (binding) on the design-level findings

- **F7 / WPI_LOG_DIR:** pin literally to `/var/log/mtc-bridge` (resolved in
  LEAD_PIN_RESOLUTION). Update the draft §2 row from `<PIN-BEFORE-DISPATCH>` to the
  literal value with origin "LEAD_PIN_RESOLUTION_2026-08-10.md, unit-template
  ReadWritePaths at the candidate SHA" — this is the Lead filling its own pin, not you
  inventing one.
- **F7 / WPI_INTERPRETER_TARGET:** take the auditor's second branch — drop the accepted-
  symlink arm; require `<venv>/bin/python` to be a non-symlink regular file, and make an
  observed symlink `B1_STOP reason=interpreter_object_unbound` routing to Lead
  adjudication. Rationale: no committed record establishes the venv's symlink layout, so
  preregistering a target would be guessing (Pattern 8-adjacent). Update draft row 18
  accordingly (remove "any accepted symlink … preregistered and bound" in favour of the
  non-symlink requirement + STOP).
- **F8 / row grammar:** reconcile TOWARD the audit's list: add the row-19
  verifier-identity tokens to the draft as a new row (19a — the digest-verified
  verifier is kept, it needs a row); delete `walk_permission_error` from row 13 with
  the recorded reason (Pattern 5 forbids classifying find's prose); align all field
  spellings block↔draft (`elapsed_s` emitted alongside `elapsed_ms`); record the three
  content-suppression renderings (`observed=unpreregistered_version`,
  `observed_sha256=`, `observed_count=`) in the table as accepted renderings.
- **F10 / row 21:** split per the audit — absent key → `schema_unexpected` STOP;
  present key wrong type → `flag_mismatch` FAIL with `observed_type=<t>`. Update the
  draft row and the block together.
- **F11 / mount binding:** implement the normalised-projection comparison (per-path
  covering mount: device id, root, mount point, fstype, source), captured once into a
  create-once evidence leaf that is both parsed and hashed. The deploy-channel
  attestation format changes accordingly — record the new format in the draft's
  attestation paragraph.

## Everything else

Apply the audit's minimal fixes as written (F1 parameterised prefix + real-lstat QA arm;
F2 STOP class for tool binding + merged-/usr QA arm; F3 count-classify-suppress
rendering; F4 hoisted guard + FAIL-through-guard helper with `mount_topology_changed`
downgrade; F5 the full fixture list the auditor names, including the four JSON arms;
F6 pinned `timeout` as ninth tool bounding every child, keep post-hoc gate, emit
`elapsed_s`; F9 unfiltered `ss -H -ltn` captured whole as evidence then scoped in-block;
F12 sanitize the symlink target and audit every host-derived printf; F13 `set -f`).
Also fix the observation-4 disclosure (binding=tokens must not claim a window that was
closed before exec) and remove the line-358 no-op.

## Deliverables

Repaired `RP7-WPI-RO.sh` + extended `SELF_QA_RP7.md` (every new arm with REAL RED/GREEN
run locally; the auditor's falsification fixtures must now pass in the repaired
direction) + updated `STATUS_RP7.md` + the adjudicated draft edits + your report
`WPI_BLOCKS_DRAFT/RP7_REPAIR_R2_REPORT.md` (finding → disposition → evidence pointer,
plus the list of draft rows touched). `bash -n` PASS; record new SHA-256 + bytes.
Touch ONLY those five files. Do not commit.
