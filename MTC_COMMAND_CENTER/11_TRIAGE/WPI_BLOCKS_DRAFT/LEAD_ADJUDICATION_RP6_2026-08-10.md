# Lead adjudication — RP6-P0 audit findings

Written 2026-08-10 ~05:30, on the GLM audit in `RP6_P0_GLM_AUDIT_2026-08-10.md`.
Verdict accepted: NEEDS-REPAIR-FIRST, repair scope bounded and mechanical.

## F2 — RESOLVED, no block change required

The auditor could not confirm the rc polarity of the two identity arms because the
authoritative expectation table was not among its inputs, and correctly flagged that
rather than guessing. Resolved here against
`../WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` section 8.1:

- Row 1: `P0_STOP reason=identity_unexpected` — rc 3.
- Row 2: `P0_STOP reason=capability_wider_than_ledger` — rc 3.

The block emits rc 3 for both. **Polarity is correct as written.** F2 is closed with no
change; the auditor's caution was right and cost nothing.

## NEW finding, raised by the Lead — the specification instantiates Pattern 8

Resolving F2 surfaced a defect in the draft, not the block. Section 8.1 row 1 reads:

> `id -un` is `gatea`; uid/gid/groups captured verbatim

That is a **name-based identity check** — Pattern 8, "the name is not the identity", the
same defect a prior audit found when a rendered `root:root` proved spoofable through an NSS
mapping. A login whose *name* renders as `gatea` need not be the preregistered numeric
identity.

The block did not implement it. `RP6-P0.sh` asks `id` only for `-u`, `-g` and `-G`, never
`-un`, and its header states the numeric-only rule explicitly. So the implementer silently
built something stronger than its specification.

**Adjudication: the draft is wrong and the block is right.** Repair the draft — row 1 must
compare the numeric uid against the preregistered value, with the name kept as diagnostic
output only. Do not "fix" the block to match the table.

This is worth recording as a process point: a specification that has been through an
adversarial audit can still carry a defect the audit did not reach, because that audit
examined the *draft's* internal consistency rather than every line against the pattern
catalogue — which did not exist when the draft was first written. The catalogue is now a
binding input for new work; applying it retroactively to the accepted WP-I draft is a
separate, worthwhile pass that has not been done.

## Remaining repair scope (unchanged from the audit)

1. **F1 [MEDIUM]** — correct the false child-execution claim at lines 59-62 and the
   `children=2_readonly_cleared_env` token at line 861. The block runs ~20+ children; only
   the two `env -i` launches are cleared-env. State the surface honestly or drop the token.
2. **F3 [LOW]** — either canonicalize the components of `$P0_VENV_ROOT/bin/python` or
   disclose the intermediate-symlink residual in the `does_not_establish` line.
3. **F4 [LOW/nit]** — add the `:?` fail-closed backstops behind the rc-3 input pre-checks,
   matching the accepted block's defence in depth.

Plus the draft repair above. After F1 and the draft fix, the block is sound enough to drive
and `SELF_QA_RP6.md` can be written against it.

## Standing

`RP6-P0.sh` remains PARTIAL, UNAUDITED-BY-EXECUTION and carries no authority. No arm has
been driven. WP-I still has neither host-contact authority nor a budget lift, so nothing
here may run against any host.
