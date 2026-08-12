# KICKOFF — GLM-5.2: sweep the closed WP-L/B3 evidence records against their own bytes

You are GLM-5.2 via the Z.AI route. **You are running UNATTENDED — do not ask for approval, do
not write a plan and stop. Execute directly and write your verdict file.** Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. Read-only: create nothing except your verdict file, no git
mutation, no host, no network.

## Why this exists
The `.gitattributes` durability analysis (`WPI_GITATTRIBUTES_DURABILITY_ANALYSIS_2026-08-12.md`)
found **198 identity-quoted paths in the closed WP-L evidence index**, of which **170 are LF-only
tracked files that would materialize with different bytes on a fresh Windows checkout**. It also
surfaced one live discrepancy in passing: a WP-L record no longer matches its evidence-index row
because a later integrity record documents an append.

WP-L is **declared closed and accepted** (`WPL_P2_STAGING_.../UNIT_CLOSURE_RECORD.md`), and its
index claims every listed hash was mechanically recomputed. That combination — closed, trusted,
quoted downstream, and never re-verified since — is exactly where a silent identity drift would
sit unnoticed. Audit 2 will inherit these records.

## What to sweep
Base: `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/`.

1. **Re-derive identities.** For every artifact the `EVIDENCE_INDEX.md` names with a byte count
   and/or SHA-256, recompute both from the current working tree and compare. Report every
   mismatch with the indexed value, the current value, and the file.
2. **Classify each mismatch honestly.** Distinguish:
   - **Documented change** — a later record explains it (e.g. the known append). Not a defect;
     say which record explains it and whether the index was updated.
   - **Undocumented drift** — nothing explains it. This is the finding.
   - **Missing artifact** — indexed but not present in the checkout (three WP-L evidence logs are
     untracked, so they cannot appear in a clone at all — confirm which).
3. **Check the closure record's own claims.** `UNIT_CLOSURE_RECORD.md` declares the unit closed
   and accepted. Does every artifact it relies on still exist and still match? A closure record
   resting on a drifted artifact is worth surfacing even though the unit is closed.
4. **Check the "mechanically recomputed" claim** in `EVIDENCE_INDEX.md`. Is there a recorded
   command or transcript for that recomputation, or is it an assertion? Say which — an assertion
   is not evidence, and this project's standing rule is that a claim without a located command is
   supplemental.

## Rules
- Every finding carries the file, the indexed value, and the recomputed value.
- **Do not edit any WP-L file.** Report; the Lead decides what to do.
- A clean sweep is a genuinely useful result — WP-L being intact is worth knowing before Audit 2
  inherits it. Say so plainly if that is what you find.
- Mark anything you could not compute `PENDING-LEAD-EXECUTION`; **never fabricate a green run.**
- Do not re-litigate WP-L's technical conclusions. This is an identity-and-provenance sweep only.

## Deliverable
Write ONE new file:
`MTC_COMMAND_CENTER/11_TRIAGE/WPL_B3_RECORD_SWEEP_GLM_2026-08-12.md`.
Print: artifacts checked, identities matching, documented changes, undocumented drift, missing
artifacts, and the single most consequential finding.
