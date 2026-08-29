# Owner decision — WP-P0-11 parked by its own stopping rule (one label left)

**Date:** 2026-08-29 afternoon. **Package state:** branch
`feature/wp-p0-11-kernel-legacy-compatible-20260825` at `37a4c191` (repair 6), worktree clean,
gate outcome STOP by design, NOT pushed, NOT merged.

## What happened, in plain words

Before repair 6 ran, I wrote a stopping rule: *if the round-6 audit finds ANY status or label
that still claims an act the code did not perform, the repair chain stops and the package goes
to you.* The audits are in:

- **Flagship (Claude Pro): PASS.** No new defect instances, the finalizer's status now says
  exactly what it verified.
- **Detection (Codex): one finding, demonstrated with a working probe.** The receipt still
  publishes a field named **`double_build` with `byte_identical: true`** — but the code never
  builds anything; it hashes **two files the caller hands it** and checks they are identical. A
  probe that fabricated everything and called only the finalizer got a receipt saying
  `double_build / byte_identical: true`. The name claims two build acts that did not occur.

That meets the rule I wrote. Rules written before the verdict do not get re-litigated after it,
so the package is parked — even though the flagship passed it, and even though the fix is small.

## The score after six repair rounds

Every earlier hole detection found is now closed and re-verified: zero-row matrices, self-
declared universes, empty artifacts, moved digest flags — all REFUSED at repair-6. The finalizer
status itself is honest ("SHAPE_AND_IDENTITY_ACCEPTED; producer execution NOT verified by this
gate"). What is left is **one field name and its echo in the lane report** (`p011_gate.py:
1305-1333,1407-1421`; `LANE_REPORT.md:136-140`).

## Your options

1. **(Recommended) Authorize repair 7, scope frozen to the label.** Rename the receipt field to
   what it measures (e.g. `caller_supplied_byte_comparison`), correct the LANE_REPORT echo,
   nothing else; one delta audit pair. Estimated one round, ~1–1.5 h of lanes (estimate, not
   measured). Say: **"repair 7 approved — label only"**.
2. **Accept as-is and carry it to v3.** The v3 repin (which you already unblocked with your 3
   YES answers) rewrites the receipt anyway; the honest renaming happens there. The package
   waits parked until v3 work starts. Say: **"carry to v3"**.
3. **Park indefinitely** pending anything else you want. Say: **"hold"**.

Either of 1 or 2 keeps your P0-12 kernel approval on track — P0-12 starts when P0-11 is
accepted, and P0-11's acceptance path resumes the moment you pick.

## For the record

Six repair rounds, three auditors, the same defect family every time, each round one layer
deeper — and each round's fix held under re-probing. The package is materially stronger than at
round 1; this park is the stopping rule doing its job, not a failure.
