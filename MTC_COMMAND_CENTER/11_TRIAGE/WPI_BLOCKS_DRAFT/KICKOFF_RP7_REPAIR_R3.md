# KICKOFF — RP7-WPI-RO round 3 (FINAL T0 round): close the six re-audit findings

Dispatched by the Claude Lead, 2026-08-10. Round-2 re-audit
(`RP7_CLAUDEPRO_REAUDIT_R2_2026-08-10.md`): all 13 round-1 findings CLOSED by
execution, verdict still BLOCK on 6 new/residual findings. This is round 3 of the T0
cap — the last round. Apply the auditor's minimal fixes exactly; no scope creep.

**Owner amendment A2/A2a in force: implement yourself, no sub-delegation.**

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`)

1. `WPI_BLOCKS_DRAFT/RP7_CLAUDEPRO_REAUDIT_R2_2026-08-10.md` — findings 1–6 + the
   observations; the repair contract. Baseline bytes `ed9aa6b3…`, 54001 B.
2. `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh`, `SELF_QA_RP7.md`, `STATUS_RP7.md` — targets.
3. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — round 1.6; edit ONLY where
   a finding's fix names a draft change (attestation paragraph → projection **v2**
   definition; `binding=` token set declared; row 17 byte-count form; row 22
   `observed=non_preregistered_address`; row 19 component-walk FAIL grammar;
   execution-environment paragraph per your F6 choice).

## The six, with binding dispositions

- **F1 (BLOCK)** — `normalised_path_projection_v2`: per preregistered root emit
  covering-mount record ∪ every mountinfo record at-or-below the root (mountinfo
  order) ∪ per-root count; add `requirements.lock` + `verify_lock.py` literal paths to
  the point list; tie-break `-ge` (last match = effective mount) + emit count of
  records sharing the winning mount point. Update draft attestation paragraph to v2.
- **F2 (MEDIUM)** — QA: (a) GNU-prefix GREEN arm via a `WPI_STAT` wrapper fixture
  emitting each accepted literal (assert absent ×6, RED on a seventh); (b) replace the
  placebo `:117` mutant with the real pre-fix `wpi_fail` body and assert
  `MOUNT_WINDOW_CLOSED` absent; (d) drop the two guard stubs, use computed
  attestations. (c) — the accepting `wpi_validate_inputs` arm — is a FREEZE-GATE item:
  record it in STATUS as such, do not fake it now.
- **F3 (MEDIUM)** — emit `attestation=self` for stat/env/sha256sum/timeout,
  `attestation=bound_instrument` for the rest; disclose in the draft binding paragraph.
- **F4 (LOW)** — narrow the ENOENT match back to the exact invocation the block
  controls (per the finding's text).
- **F5 (LOW)** — reconciliation: declare the `binding=` token set in the draft; row 17
  byte-count FAIL form; row 22 address rendering; row 19 component-walk FAIL; route
  `:287`/`:646` through `wpi_kind_token`.
- **F6 (LOW)** — invert to `exec "$WPI_ENV" -i … "$WPI_TIMEOUT" … "$@"` (preferred) or
  disclose in the draft; if inverting, prove bounding still works in QA (2 s budget vs
  8 s child, wall clock).

Also apply observation 4's cosmetic if trivial (elapsed_s ceiling display), and keep
observation 1 in mind — no new conditional assignments of late-bound globals.

## Deliverables

Repaired block + extended QA (REAL runs; auditor's N1/N2 projection falsifications
must now flip: decoy bind under release → digest differs; stacked mount → digest
differs) + STATUS + draft edits + `RP7_REPAIR_R3_REPORT.md` (finding → disposition →
evidence). `bash -n` PASS; new SHA-256 + bytes. Touch ONLY those five files. Do not
commit.
