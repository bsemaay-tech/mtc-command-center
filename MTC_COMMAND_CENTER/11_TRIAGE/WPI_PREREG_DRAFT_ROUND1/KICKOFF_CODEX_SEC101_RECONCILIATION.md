# KICKOFF — §10.1 allowlist reconciliation for the two preflight blocks

You are a fresh `gpt-5.6-sol` session, effort high. **Analysis only.** Produce one
decision table. Edit nothing except your own output file. Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network, no commit.

## The problem in one paragraph

`WPI_PREREGISTRATION_DRAFT.md` §10.1 declares the allowlist of host paths the two
read-only preflight blocks are permitted to touch. §10.1 was written before the blocks
grew through six and four repair rounds, so it is now out of date: the static path-scope
prover reports paths the blocks reach that §10.1 does not cover — `/dev/null`,
`/proc/self/mountinfo` and `/proc/uptime` among them. Every gap must be closed one of two
ways, per path, before freeze: **(a) extend §10.1 with a written justification**, or
**(b) change the block so it no longer needs that path.** Nothing may be closed by
loosening the prover.

## Inputs (relative to `MTC_COMMAND_CENTER\11_TRIAGE\`)

1. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — §10.1 (allowlist) and §10.2
   (what Stage 1 must prove). Quote §10.1's current entries verbatim in your report.
2. `WPI_BLOCKS_DRAFT/RP6-P0.sh` — 93421 B, SHA-256
   `75db028e76438bc88caba19b9c3b6411e5f573f7b6c2bd13c3883d24e4389570`.
3. `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` — 70941 B, SHA-256
   `23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad`.
4. `WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py` + `PATHSCOPE_RUN_2026-08-10.log` — the
   prover and its recorded run. Treat its output as **input evidence, not as ground
   truth**: it is itself under review, and its unresolved counts (RP6 1 resolved / 37
   unresolved, RP7 4 resolved / 65 unresolved) mean most paths still need your own reading
   of the block source.

## What to produce

One row per distinct host path reachable by either block. Derive the list yourself from
the block sources; use the prover output to cross-check that you have not missed one.

| # | Path (or path family) | Block(s) | How it is reached (function + line) | Read or write | Covered by §10.1 today? | Recommendation: EXTEND / CHANGE-BLOCK / ALREADY-COVERED | Justification |

Rules for the recommendation column:

- **EXTEND** only when the path is genuinely required for the block's stated read-only
  purpose, is read-only in practice, and cannot leak information or authority. Write the
  one-sentence justification exactly as it should appear in §10.1.
- **CHANGE-BLOCK** when the path is incidental, replaceable, or wider than needed. Say
  concretely what the block should do instead.
- Flag separately, in their own section, any path that is **written** rather than read,
  and any path outside the run's own evidence tree. Those are the ones that matter most.
- Where a path is constructed dynamically and you cannot pin it to a finite set, say so
  explicitly — an unresolvable path family is a finding, not a table row to guess at.

Also state whether §10.1's current grammar (exact path vs subtree vs terminal) is
expressive enough for what you found, and propose the minimal grammar change if not.

## Output

Write **only** `WPI_PREREG_DRAFT_ROUND1/SEC101_RECONCILIATION_CODEX_2026-08-10.md`:
a one-paragraph summary, the full table, the written-path section, the unresolvable-family
section, and a closing count (paths total / already covered / extend / change-block /
unresolvable). Do not edit `WPI_PREREGISTRATION_DRAFT.md` — the Lead applies the decisions.
