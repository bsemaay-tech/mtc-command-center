# KICKOFF — does the Audit-2 readiness package still describe reality?

Fresh `gpt-5.6-sol` session, effort high. **Analysis only**, one output file, no commit, no
host contact, no network, no edits to the package. Working dir `C:\LAB\Tradingview_LAB_CLEAN`.

## Why

`11_TRIAGE/AUDIT2_READINESS_PACKAGE/` was assembled to hand Audit 2 a coherent picture of
WP-I. Since it was written, RP6-P0 has gone through six repair rounds, RP7 four, transport
three, and today produced several findings that change what the artifacts claim: a tool
that was declared but never bound, a §10.2 prover that under-reports, an allowlist that
does not cover what the blocks reach, and the discovery that **no executable implements
§8.2 rows 1–9**. A readiness package that describes a superseded state will send Audit 2
looking at the wrong things.

## Inputs (relative to `MTC_COMMAND_CENTER\11_TRIAGE\`)

1. `AUDIT2_READINESS_PACKAGE/` — every file in it.
2. Current state of record: `WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md`, `STATUS_RP7.md`,
   `STATUS_TRANSPORT.md` (if present), and the newest audit report per artifact:
   `RP7_CODEX_T0_AUDIT_R4_2026-08-10.md`, `RP6_CODEX_AUDIT_R6_2026-08-10.md`,
   `TRANSPORT_CODEX_FINAL_AUDIT_2026-08-10.md`, `TRANSPORT_CLAUDE_FINAL_AUDIT_2026-08-10.md`.
3. Today's cross-cutting analyses: `WPI_PREREG_DRAFT_ROUND1/SKELETON_REVIEW_CODEX_2026-08-10.md`,
   `SEC101_RECONCILIATION_CODEX_2026-08-10.md`,
   `PATHSCOPE_CODEX_T1_AUDIT_2026-08-10.md`, `PATHSCOPE_LEAD_RERUN_2026-08-10.md`,
   `DEFECT_PATTERNS_REVIEW_CODEX_2026-08-10.md`.
4. `OVERNIGHT_PLAN_2026-08-10_NIGHT.md` for the current per-artifact state table.

## What to determine

1. **Stale claims.** Every statement in the package that is now false or superseded, quoted
   verbatim, with the current truth beside it.
2. **Missing material.** Anything Audit 2 will need that the package does not contain —
   including the rows 1–9 gap, the §10.1 delta, the prover's unsound status, and the fact
   that no artifact has yet been accepted by both flagships.
3. **Premise inheritance.** Which of Audit 2's stated premises depend on a WP-I result that
   is not yet established? Name each one and the artifact it waits on. If Audit 2 cannot
   honestly start until specific artifacts are accepted, say so and list them.
4. **Ordering.** Is the package's assumed sequence (WP-I closure → Audit 2 → WP-A → Gate B)
   still coherent given the freeze blockers? If a blocker changes the order, say how.

## Output

Write **only** `AUDIT2_COHERENCE_CODEX_2026-08-10.md` in `11_TRIAGE/`: a verdict
(`COHERENT` / `NEEDS-UPDATE: <n> items`), the stale-claim table, the missing-material list,
the premise-inheritance list, and a short closing statement of what would have to be true
before Audit 2 can honestly begin. Do not edit the package — the Lead applies changes.
