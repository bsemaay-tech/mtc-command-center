# KICKOFF — Audit 2 readiness package (assembly only, no audit dispatched)

Authorized private-repo documentation assembly. You are building the package an Audit 2
auditor will be HANDED. You are NOT auditing anything and NOT dispatching anything. No
host contact, no git mutation, nothing executed against any machine. Write ONLY into this
directory. ASCII only. English only.

## Why this exists

Audit 2 is the two-flagship T0 round that freezes the pre-WP-A SHA. It cannot start yet:
by the D2 sequencing rule it runs only after WP-L Phase 2 **and** WP-I both close, and WP-I
is not dispatchable (it still needs explicit host-contact authority and a budget lift).
This package makes the eventual dispatch immediate rather than a fresh research effort —
everything an auditor needs, assembled, with each item either present or explicitly marked
as produced-at-freeze.

## Inputs (read these, nothing else)

- This file.
- `../AUDIT2_EVIDENCE_CHECKLIST_DRAFT_2026-08-09.md` — the v2 checklist, including the
  §2b transport-evidence package. This is your table of contents.
- `../WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/UNIT_CLOSURE_RECORD.md` — what WP-L P2
  achieved and what it left open.
- `../WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/EVIDENCE_INDEX.md` — the per-stage file
  and hash inventory plus the RUNID ledger.
- `../OWNER_DECISION_AUDIT_TIERS_2026-08-09.md` — tier policy, cadence, acceptance floor.
- `../WPL_P2_PROPOSALS_LEAD_ACCEPTANCE_2026-08-09.md` — what was accepted and by whom.

Do not read the audit reports themselves; you are indexing, not re-adjudicating.

## Deliverables

1. `AUDIT2_HANDOFF_PACKAGE.md` — the auditor-facing document. For every checklist item,
   one row: item, **state** (PRESENT / PRODUCED-AT-FREEZE / BLOCKED-UPSTREAM), the exact
   file path if present, and **how the auditor verifies it** (what to recompute or
   compare). An item with no verification method is a defect in this package — flag it
   rather than papering over it.
2. `AUDIT2_FREEZE_PREREQUISITES.md` — the ordered list of what must be true before Audit 2
   may be dispatched at all: WP-L P2 closed (done, cite it), WP-I closed (not done, cite
   the two missing authorities), the freeze SHA cut, the ledger figure ratified. State
   plainly which are satisfied today and which are not.
3. `AUDIT2_AUDITOR_SESSION_INPUTS.md` — what each auditor session receives: scope contract
   (what Audit 2 accepts and rejects), isolated-worktree instructions at the frozen SHA
   with the required cleanliness proof, the mandated test-suite command and its expected
   baseline including the currently accepted anomaly set, and the D026 rule that an
   auditor unable to execute the suite must return BLOCK.
4. `AUDIT2_D026_RED_LOCATIONS.md` — for every test offered as closure evidence, where its
   RED demonstration lives. Use the evidence index and the closure record. Where a RED
   location is not recorded anywhere, say so explicitly — an unlocated RED is supplemental,
   not closure, and the auditor must be told which ones those are.
5. `OPEN_QUESTIONS_FOR_DISPATCHER.md` — decisions the dispatching Lead must make, each with
   the options and a recommendation. At minimum: the unresolved GLM supplemental-vs-omitted
   flag from the checklist's §0, and how the two flagship sessions are kept independent.

## Hard constraints

- Assemble and index; do not re-audit, do not re-adjudicate, do not soften any recorded
  BLOCKED or open item.
- Where the checklist says an item is produced by the round itself, mark it
  PRODUCED-AT-FREEZE rather than inventing content for it.
- Cite exact paths. A claim without a path is not usable by an auditor.
