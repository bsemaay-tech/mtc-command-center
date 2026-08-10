# KICKOFF — RP7 round-5: delta verification only (no fixture construction)

Fresh `gpt-5.6-sol` session, effort high. **Reading and diffing only.** Do not build test
fixtures, do not create temporary trees, do not run the block or any part of it. This run is
deliberately confined to comparing two versions of a shell file and checking claims against
the text. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network, no commit.

## Why this run is narrow

Two earlier full reviews of this file were terminated by the provider mid-run. This one is
scoped so that it needs no constructed test material at all — only `git`, `diff`, `sed`,
`sha256sum` and reading.

## Subject

`WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh`:

- round-5 bytes: SHA-256 `393a16ce264b467bec180a2106390e6dcee4dc2605fd019871270fda11d3b0ee`,
  77179 B, commit `1143a9ff`
- round-4 bytes: SHA-256 `23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad`,
  70941 B, commit `d6a976aa`

Retrieve the round-4 version with `git cat-file blob d6a976aa:<path> > <tmp>`. Never
`git checkout` — it rewrites line endings and would invalidate the comparison.

## The single claim to test

`RP7_REPAIR_R5_REPORT.md` states: *"The whole executable delta is `+93/-7` lines, of which
the non-comment part is exactly the five repairs below and nothing else. No other production
line changed."*

Verify that claim precisely.

1. Produce the actual diff and its line counts. Do they match `+93/-7`?
2. Classify **every** changed hunk into one of six buckets: repair 1 (bind `python3` in the
   production main loop), repair 2 (adjudicate package identity before parity), repair 3
   (published QA command), repair 4 (remove `/dev/null` write opens), repair 5 (bind the
   evidence root), or **unexplained**.
3. For each hunk, quote the changed lines and name the bucket with one sentence of
   reasoning. Comment-only and whitespace hunks are their own bucket — count them, do not
   ignore them.
4. Report every hunk you place in **unexplained**. That list is the point of this run.
5. Separately: does any hunk *weaken* a check that existed in round 4 — a condition removed,
   a comparison loosened, a STOP turned into a warning, an error path made non-fatal? Quote
   it if so.

## Two text-level checks

- `grep` the round-5 file for `/dev/null`. The repair claims all three write opens are gone.
  Report every remaining occurrence with its line and context.
- `grep` `SELF_QA_RP7.md` for absolute line-number ranges in evidence commands (patterns
  like `sed -n '123,456p'` or `Select-Object -Skip <n> -First <n>`). The evidence contract
  requires content anchors instead, because the file grows every round. Report any survivor.

## Output

Write **only** `WPI_BLOCKS_DRAFT/RP7_CODEX_DELTA_REVIEW_R5_2026-08-10.md`: the measured diff
statistics, the per-hunk classification table, the unexplained list (or an explicit
statement that it is empty), the weakening list, and the two grep results. State plainly
that no behavioural testing was performed in this run and that this is a text-level
verification only.
