# KICKOFF — distil the night's audit findings into a reusable defect-pattern catalogue

Authorized private-repo documentation work. Documentation only: no host contact, no git
mutation, nothing executed against any machine. Write ONLY the single deliverable named
below, into `MTC_COMMAND_CENTER/11_TRIAGE/`. ASCII only. English only.

## Why

In one night, an adversarial cycle over two artefacts (a staging admission block and a
staging-verification preregistration draft) produced roughly twenty distinct required
findings. Most are instances of a much smaller number of *recurring defect patterns*. Left
as prose scattered across nine audit reports, those patterns will be rediscovered the
expensive way in WP-I, WP-A and every future design cycle. Your job is to compress them
into a catalogue a designer can check work against, and an auditor can attack work with.

This is a distillation task. Do not re-adjudicate any finding, do not soften any verdict,
and do not invent patterns that the evidence does not support.

## Inputs (read these, nothing else)

Under `WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/06_B3_REPAIR/`:
`audit1/AUDIT1_REPORT.md`, `audit2/AUDIT2_REPORT.md`, `audit3/AUDIT3_REPORT.md`,
`audit4/AUDIT4_REPORT.md`, `audit5/AUDIT5_REPORT.md`, `audit6/AUDIT6_REPORT.md`.

Also: `WPI_DRAFT_CODEX_AUDIT_2026-08-09.md`, and
`WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/03_TRANSPORT/B3_STOP_ADJUDICATION.md`.

## Deliverable — `DESIGN_DEFECT_PATTERNS_2026-08-10.md`

For each pattern you identify:

1. **Name** — short and memorable, so it can be cited in a review comment.
2. **The mistake, in one sentence.**
3. **Why it survives casual review** — what makes it look correct.
4. **Concrete instances**, each citing the audit report and finding id it came from. A
   pattern with fewer than two instances is not a pattern; report it as a one-off in a
   separate short section at the end.
5. **The falsification** — the specific fixture or host state that exposes it. Quote the
   actual observed output where an audit recorded one.
6. **The rule that prevents it** — phrased as something a designer can apply before
   writing code, not as a post-hoc fix.

Order patterns by how much damage they cause, most severe first.

Candidate patterns visible in the evidence (verify each against the reports; add, merge or
drop as the evidence dictates — this list is a starting point, not an answer key):

- Inability-to-evaluate reported as a finding (STOP collapsed into FAIL).
- Trusting a rendered name where the identity is numeric.
- Verifying a path without verifying what the path resolves through.
- Reading a tool's stdout before adjudicating that tool's exit status and diagnostics.
- Substring matching where the data has structure.
- An interpreter or child process inheriting an attacker-influenced environment.
- A claim whose scope is narrower than the sentence that states it.
- A check that cannot fail (self-attesting evidence).
- A guard whose own failure path is unguarded.

Close with a short section: **"What the cycle cost, and what it bought."** State plainly how
many rounds were needed, which findings only appeared after an earlier fix, and which were
caught only because an auditor executed a fixture rather than reading the code. That
section is the argument for keeping adversarial audits; make it factual, not
promotional.

## Constraints

- Every claim carries a citation to the report and finding it came from.
- Where an audit recorded real command output, quote it rather than paraphrasing.
- Do not name or rate the models involved; patterns are about designs, not agents.
