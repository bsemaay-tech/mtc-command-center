# RP6-P0 — status: PARTIAL and UNAUDITED, do not treat as a deliverable

Written by the Lead 2026-08-10 ~04:20.

`RP6-P0.sh` in this directory is **incomplete work product**, not a finished block. It is
committed rather than discarded because the code that exists is substantive and reviewable,
and because silently deleting partial work would lose the record of what was attempted.

## What happened

The build was dispatched to Codex. Under the repository's standing two-tier rule, Codex
sub-delegated the implementation to the counterpart flagship (Claude Opus 5), which wrote
`RP6-P0.sh` and then hit its account session limit (reset 06:20) before producing the other
two required deliverables. Codex declined to finish the counterpart's work itself and
reported blocked rather than printing a false completion — the correct call.

The routing conflict this exposed, and the fix, are recorded in
`../STANDING_AUTONOMY_AUTHORITY_2026-08-09.md` §A2a.

## What is missing

- `DESIGN_NOTES_RP6.md` — not written.
- `SELF_QA_RP6.md` — not written. **No arm of this block has been driven.** There is no
  evidence that any code path in `RP6-P0.sh` behaves as written.

## What the Lead did verify

Only the cheap mechanical checks, which prove very little on their own:

- `bash -n RP6-P0.sh` returns 0.
- No `mktemp` and no temp-file redirection (the no-mutation constraint).
- Identity is read numerically; the file comments that `id -un` and other name forms are
  deliberately not called.
- `p0_stop` / `p0_fail` exist with the 0/1/3 contract and an ERR trap is installed.
- The single `ssh|scp|curl` grep hit is a comment naming a tool the RO stage will invoke,
  not a contact. No host was contacted by this task.

## What that does NOT establish

The block has not been audited against `../DESIGN_DEFECT_PATTERNS_2026-08-10.md`, which was
a binding input. Syntax and a few greps cannot show that it avoids the ten patterns — the
whole lesson of the B3 cycle is that these defects survive exactly this kind of casual
review. Treat every claim in the script as unverified.

## Required before this block is usable

1. An implementer completes the two missing deliverables, with `SELF_QA_RP6.md` recording
   the exact executable command and real output for every arm.
2. An independent agent audits the result against the defect-pattern catalogue.
3. Only then may it be considered for freezing into a kit — and freezing remains separate
   from any authority to run it.

This block carries no authority. WP-I has neither host-contact authority nor a budget lift,
so nothing here may be executed against any host regardless of its state.
