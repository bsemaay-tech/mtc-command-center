# KICKOFF — §8.2 rows 1–9: what implementing them costs, and what deferring them costs

Fresh `gpt-5.6-sol` session, effort high. **Analysis only**, one output file, no commit, no
host contact, no network, no source edits. Working dir `C:\LAB\Tradingview_LAB_CLEAN`.

## Why this exists

The successor-preregistration review found that **no current executable implements §8.2
rows 1–9**. `RP6-P0.sh` says every §8.2 row is out of scope; `RP7-WPI-RO.sh` claims only
rows 10–23. Nothing checks active state, restart count/policy, MainPID equality, candidate
binding, fragment `[Install]` absence/identity, sandbox properties, or start mode. Freeze
is therefore blocked on a decision only the owner can make: **build them, or formally defer
them and narrow every downstream claim.**

The owner is non-technical. This analysis exists so the choice can be put to him in one
short page with honest costs on both sides. Write for that purpose.

## Inputs (relative to `MTC_COMMAND_CENTER\11_TRIAGE\`)

1. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` §8.2 — quote rows 1–9 verbatim,
   with their preregistered first-divergence order and their exact result grammar.
2. `WPI_PREREG_DRAFT_ROUND1/SKELETON_REVIEW_CODEX_2026-08-10.md` gap 8.
3. `WPI_BLOCKS_DRAFT/RP6-P0.sh`, `RP7-WPI-RO.sh` — confirm for yourself that no function
   implements any of the nine, and say precisely where each block disclaims them.
4. `WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv` — ops 04 and 05, which would carry them.
5. `AUDIT2_READINESS_PACKAGE/` — what Audit 2 has been told to expect.

## Produce three things

**1. Per-row table.** For each of rows 1–9: what it asserts, what host observation would
establish it, whether that observation is read-only, whether it needs root, whether the
existing pinned tool set can make it, and the honest difficulty (LOW / MEDIUM / HIGH) with
one sentence of reasoning. Flag any row that cannot be established read-only at all — that
row changes the authorisation question, not just the workload.

**2. Option A — build them.** The smallest correct shape: which block gains them (extend
RP7, or a new RP-8.2 block), how many repair-plus-two-flagship-review rounds it plausibly
costs given that RP7 took four rounds and RP6 six, what it adds to the plan, and what could
go wrong. Give a range, not a point estimate, and say what drives the spread.

**3. Option B — defer them.** Exactly which claims, closure criteria, and Audit-2 inputs
must be narrowed, quoted as before-and-after sentences. Then state plainly: with rows 1–9
deferred, **what does the WP-I run still actually prove, and what does it stop proving?**
Name anything downstream (Audit 2, WP-A, Gate B) that would inherit a weaker premise.

## Output

Write **only** `WPI_PREREG_DRAFT_ROUND1/ROWS_1_9_OPTIONS_CODEX_2026-08-10.md`. End it with
a section headed `## For the owner, in plain language` — at most 200 words, no jargon, no
identifiers, stating the choice, the honest cost of each side, and which one you would pick
and why. Do not edit the draft or any block.
