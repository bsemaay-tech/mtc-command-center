Round 1.2 repair complete. All four in-scope findings applied across the three deliverables; the audit is **not** fully resolved — F3/F4 are explicitly deferred.

## What I applied (the governing principle: inability-to-evaluate → STOP, never FAIL)

**F1 (HIGH) — B1 metadata readability** — `WPI_PREREGISTRATION_DRAFT.md`
- Row 19 now carries an explicit preflight readability precondition over *every* metadata object the verifier consumes (`*.dist-info` + `METADATA`/`RECORD`).
- Divergence restructured: `B1_FAIL reason=lock_installed_parity` is admissible **only** on a positively-distinguished set mismatch; `metadata_unreadable` and `verifier_not_evaluable` STOPs cover every open/parse/permission/LSM/traversal/generic-nonzero case.
- New **Metadata-readability adjudication rule** paragraph states the fixed precedence. The row-14 traversal guard is now explicitly non-sufficient.
- B1 stays INCLUDE-READ-ONLY (no class change — readability of 0555-tree files is unprivileged).

**F2 (HIGH) — B6 network-namespace binding** — draft + TSV
- Rows 22-23 now require the namespace binding proven (`readlink /proc/self/ns/net` == `/proc/<MainPID>/ns/net`) before `ss` output is interpreted; mismatch/unreadable → `B6_STOP`. External probe kept as independent corroboration.
- **Class change:** listener-set half → INCLUDE *conditional on netns binding* / DEFER-ROOT-SIDE *(the binding itself if `gatea` can't read the service netns identity)*. TSV B6 updated, including **correcting the false claim** that `ss` lists sockets system-wide — it lists the caller's netns.
- New M4-11 in SELF_QA records the unverified netns-readability premise (fail-closed).

**F5 (MED) — hash could-not-read** — draft + TSV: rows 7 & 17 gained explicit hash-error STOPs (`fragment_unreadable`, `installed_lock_unreadable`); digest-mismatch FAIL now requires rc 0 + valid 64-hex digest + byte count.

**F6 (MED) — dispatch authority** — draft: the three pre-dispatch items now stated **necessary but not sufficient**, with written host-contact authority + budget lift added as gates; `-Execute`/`-Confirm` marked technical interlocks, not authority.

## Two judgment calls (both documented transparently in the round-1.2 addendum)
1. **Scope:** the audit marks F1–F4 HIGH, but the task contract scopes this round to "F1, F2, and any lower-severity items" → F1/F2/F5/F6. **F3 and F4 are out of scope** and recorded as OPEN; I made no claim the audit is fully resolved.
2. **Consistency fix in service of F1:** row 14's stale cross-reference ("disqualifies row 18") contradicted its own ordering rule (row 14 gates row 19/parity) — a round-1.1 leftover. Corrected to "row 19" so the table matches the ordering rule F1 makes central. No predicate changed.

## Constraints honored
Still a DRAFT — no RUNID/unit-id/record-root minted; `<ALLOCATE-AT-DISPATCH>`/`<PIN-BEFORE-DISPATCH>` intact. No check weakened (every edit adds a precondition or STOP; one factual correction replaced a claim the audit proved false). No mutating check preregistered. Touched only the three named deliverables.

**Not done (correctly):** no Git action, no handoff-file updates — the task constrained me to the three deliverables ("read-only elsewhere"), and Git sequencing is Lead-owned per the two-tier model. Ready for the Lead's independent Gate-5 audit (Codex `gpt-5.6-sol` xhigh per the roster).
