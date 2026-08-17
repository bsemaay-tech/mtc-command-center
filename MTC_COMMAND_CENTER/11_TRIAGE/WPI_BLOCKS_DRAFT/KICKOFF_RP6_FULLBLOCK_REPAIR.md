# KICKOFF — RP6-P0 full-block repair: close the seven Claude-flagship T0 findings

Dispatched by the Claude Lead, 2026-08-10. The Claude flagship T0 audit
(`RP6_CLAUDE_T0_AUDIT_2026-08-10.md`) returned BLOCK: 7 on bytes `bff3c86e…` (57441 B).
This is round 1→repair of the full-block T0 acceptance cycle (cap 3). Apply the
auditor's minimal fixes; one Lead adjudication below is binding.

**Owner amendment A2/A2a in force: implement yourself, no sub-delegation.**

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`)

1. `WPI_BLOCKS_DRAFT/RP6_CLAUDE_T0_AUDIT_2026-08-10.md` — findings 1–7 with executed
   falsifications and minimal fixes; the repair contract.
2. `WPI_BLOCKS_DRAFT/RP6-P0.sh`, `SELF_QA_RP6.md`, `STATUS_RP6_P0.md` — targets.
3. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — round 1.6 §8.1; edit only
   where a fix names it (row-9 wording stays — see adjudication; grammar alignments of
   finding 7).
4. `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` — reference ONLY for the argv[0]-prefix classifier
   repair shape (its F1 fix) and the attested-gate shape (`:444` area). Do not modify.
5. `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — binding pre-read.

## Lead adjudication (binding)

**Finding 2 / row 8: IMPLEMENT, do not reduce.** Add the execution-domain gate to P0,
mirroring RP7's shape: new preregistered constants (attested user/mount/PID/net
namespace identities + canonical root-mount identity) as `<PIN-AT-FREEZE>` placeholders
consumed via the same prelude mechanism, with the rc-3 missing-input pre-check + `:?`
backstop pattern; comparison emits `execution_domain_unattested` (constants unfilled /
unreadable identities) and `execution_domain_mismatch` (identities differ) — both STOP
rc 3 per the F2 polarity. Row 9's "only after row 8" precondition becomes real: gate
the manager query behind the domain gate. The block cannot GREEN end-to-end until
freeze fills the pins — record that as a freeze-gate item in STATUS exactly like RP7's.

## The other six

Apply the audit's minimal fixes as written: F1 parameterised argv[0]-prefix classifier
(port RP7's repaired shape, including the R3-narrowing lesson from RP7 round-2 finding
4 — match only the invocation the block controls) + real-lstat QA arms; F3 route the
non-canonical preregistered input to the input-error class (rc 3), not host FAIL; F4
duplicate/conflicting tool pins → STOP (`prereg_input_malformed` family), never
first-wins; F5 give the three readlink STOP arms real diagnostics (capture stderr into
detail= with grammar constraint); F6 extend the R4 sentinel to survive NUL bytes (byte
count comparison or equivalent — prove with a NUL-only rc-2 fixture RED/GREEN); F7
implement or table-record the two missing divergence tokens and unify the
`identity_unexpected` field grammar (block + draft together).

## Deliverables

Repaired `RP6-P0.sh` + extended `SELF_QA_RP6.md` (REAL local RED/GREEN for every fix;
the auditor's falsification fixtures must flip) + updated `STATUS_RP6_P0.md` + the
narrow draft grammar edits + `RP6_FULLBLOCK_REPAIR_REPORT.md` (finding → disposition →
evidence). `bash -n` PASS; new SHA-256 + bytes. Touch ONLY those five files. Do not
commit.
