# KICKOFF — Retroactive defect-catalogue pass over the accepted WP-I preregistration draft

Dispatched by the Claude Lead, 2026-08-10. Owner-authorized (grant #4 in
`../NEW_SESSION_KICKOFF_PROMPT_2026-08-09_NIGHT.md`).

**The repository's two-tier counterpart-implementer rule is suspended by owner amendment
A2/A2a. Implement this yourself. Do not sub-delegate to Claude Max or any other agent.**

## Task

Apply the full defect catalogue to the whole accepted WP-I draft — every row, every block,
every preflight — not only the rows earlier audits reached.

Read exactly these two files (both relative to `MTC_COMMAND_CENTER/11_TRIAGE/`):

1. `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — the catalogue (10 patterns).
2. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — the accepted draft (round 1.3,
   audit-clean at `fe8f1b11`, GLM-verified `2f5523c9`).

Do not read handoff files, GATE_A_A* files, or anything else.

## Known instance (seed — verify and repair, do not assume it is the only one)

The identity row specifies a **name-based check** — Pattern 8 (identity by name where the
contract is the allocated account). Prior resolution context: `install.sh` allocates the
service account dynamically, so the NAME is the contract; a recorded `getent` preflight on
the host gave uid 999, gid 988 (they differ). **Repair the draft row, not the host block.**

## Rules

- Sweep ALL 10 patterns across the ENTIRE draft. For each pattern, either list findings or
  state "no instance found" with one line saying what you looked for.
- Repair `WPI_PREREGISTRATION_DRAFT.md` in place. Repairs must not weaken any check: an
  inability to evaluate is a STOP, never a FAIL; a check that cannot fail proves nothing.
- Do NOT change the draft's scope (read-only host contact), authority claims, or any
  `<PIN-BEFORE-DISPATCH>` placeholder — those are filled by the Lead at prereg finalization.
- Write your report to `WPI_PREREG_DRAFT_ROUND1/WPI_CATALOGUE_PASS_CODEX_2026-08-10.md`:
  one row per finding — pattern #, draft location (section/row), defect, repair applied —
  plus the per-pattern no-instance notes, plus a final verdict line
  (`CATALOGUE-PASS-COMPLETE: N findings repaired, M patterns clean`).
- Touch ONLY those two files (the draft + your new report). Do not commit — the Lead
  verifies, has GLM independently check, and commits.
