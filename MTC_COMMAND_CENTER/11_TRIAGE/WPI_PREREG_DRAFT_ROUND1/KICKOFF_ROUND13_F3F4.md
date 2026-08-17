# KICKOFF — WP-I draft round 1.3 (close the two open audit findings F3 and F4)

Authorized private-repo documentation repair. Round 1.2 applied F1, F2, F5 and F6 and
left F3 and F4 explicitly OPEN. This round closes them. Documentation only: no host
contact, no git mutation, nothing executed against any machine. Overwrite the three
draft files in place; touch nothing else. ASCII only. English only.

## Inputs (read these, nothing else)

- This file.
- `../WPI_DRAFT_CODEX_AUDIT_2026-08-09.md` — findings **F3** and **F4** are the entire
  scope. Their concrete failure scenarios are binding; do not restate them as milder.
- `WPI_PREREGISTRATION_DRAFT.md`, `WPI_CHECK_FEASIBILITY.tsv`, `SELF_QA.md` — the round
  1.2 state you are revising. Read the round 1.2 sections first so you extend that work
  rather than duplicating or contradicting it.

## The one principle both findings share

An inability to evaluate must STOP (rc 3); only a probe that actually ran and observed
deviant state may FAIL (rc 1). Both F3 and F4 are cases where the draft lets an access
or traversal failure reach a FAIL verdict, which accuses a correct host. This is the
same defect class as `B3-GAP-ENV` and as F1/F2 last round.

## Required repairs

1. **F3 — system-manager access (B2 and B4).** If `gatea` is denied the system bus by a
   D-Bus or polkit policy, `systemctl` is absent, or the login sits in a PID/mount
   namespace without the system manager, then `systemctl is-active` / `show` / `cat`
   fails before returning unit state — and the draft's rows offer only
   `B2_FAIL`/`B4_FAIL`, so an error is rendered as "unit not active", a missing
   candidate binding, or a property mismatch. Repair: preregister an explicit
   system-manager reachability precondition, add `systemctl` (and the bus) to the
   general STOP list at the cited lines, and give every affected row a dedicated
   could-not-evaluate divergence — e.g. `B2_STOP reason=system_manager_unreachable`,
   `B4_STOP reason=unit_property_unreadable` — so an access failure can never surface as
   host drift. State the adjudication order explicitly.
2. **F4 — partial `find` output (B3 sweep).** A world-writable file encountered early,
   followed later in traversal order by a directory with an ACL denying `gatea`, makes
   `find … -perm /222` emit the offending pathname AND then EACCES with a nonzero rc.
   Because row 12 precedes row 14 and nothing requires the rc and all diagnostics to be
   adjudicated *before* stdout is interpreted, a wrapper can emit `B3_FAIL` for the
   writable path when the sweep was incomplete and the correct first outcome is
   `B3_STOP`. Repair: make the ordering binding and explicit — the sweep's exit status
   and its complete diagnostic stream must be adjudicated first; only a sweep proven
   complete may have its stdout read as a finding. Generalise the rule to any partial
   walk terminated by an LSM, ACL, mount or traversal error, and mirror it wherever the
   draft interprets command stdout.
3. Update `WPI_CHECK_FEASIBILITY.tsv` wherever a repair changes a check's feasibility
   class or adds a precondition (a check needing a privileged precondition moves to
   DEFER-ROOT-SIDE with the reason).
4. Add a **round 1.3** section to `SELF_QA.md` recording, per finding, exactly what
   changed and why — and state plainly that F3 and F4 are now closed, so the open-items
   list from round 1.2 is superseded.

## Constraints

- Still a DRAFT: no concrete one-use RUNID, no date-stamped unit id, no collision-prone
  record root; keep the `<ALLOCATE-AT-DISPATCH>` / `<PIN-BEFORE-DISPATCH>` discipline.
- Do not weaken anything earlier rounds established, and keep every truthful caveat —
  including the round 1.2 statement that a successor needs explicit host-contact
  authority and a budget lift before it is dispatchable.
- Preregister no mutating check.

Report what you changed, per finding.
