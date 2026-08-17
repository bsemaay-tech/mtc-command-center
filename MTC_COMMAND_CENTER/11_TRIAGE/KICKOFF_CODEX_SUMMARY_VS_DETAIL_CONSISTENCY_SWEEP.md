# KICKOFF — Codex: summary-versus-detail consistency sweep across the WP-I records

You are Codex, ANALYST. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host, no network, no
commit, no block-byte edits. Write exactly ONE new file:
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_SUMMARY_VS_DETAIL_CONSISTENCY_SWEEP_2026-08-12.md`.
Do not edit any of the swept files. Never git checkout/reset/stash.

## Why this exists — a defect class found twice today, both times by chance
The WP-I records were edited heavily on 2026-08-12 as rounds landed. Twice, an edit updated a
**summary** while leaving the corresponding **detail** stale:

1. `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md` — the Lead updated the summary block when round
   17 resolved `RP6-11`, but the table row still read `UNLOCATED — supplemental` / `OPEN`. Found
   only because an independent count re-derivation was dispatched.
2. `STATUS_RP6_P0.md` and `RP6_R17_REPORT_2026-08-12.md` — both named the round-17 implementer as
   `gpt-5.6-sol` when the run log recorded `gpt-5.5`. Found only by a Lead spot-check.

**Neither was found by an auditor.** A document whose summary and detail disagree will be read by
tonight's second-flagship auditors, and whichever half they read becomes what they believe. This
sweep makes the check systematic instead of lucky.

## What to sweep
Every file in `MTC_COMMAND_CENTER/11_TRIAGE` modified on 2026-08-12 (use `git log --since` /
`git diff --name-only` against the 08-11 tip to enumerate them — do not guess the list). For each:

1. **Summary-vs-detail agreement.** Where a file states a count, a status, a verdict or a
   disposition in more than one place — a header line, a summary block, a table row, a
   conclusion — do all instances agree? Report every internal contradiction with both line
   numbers and both readings.
2. **Status-label currency.** Does the top-of-file status label match the newest round the file
   actually documents? A file whose body describes round 17 but whose header says round 16 is a
   finding.
3. **Struck-through / superseded text.** Several files now carry `~~old~~ → new` corrections.
   Confirm each correction is complete: the old value must not survive unstruck anywhere else in
   the same file.
4. **Cross-file agreement on shared facts.** These specific facts appear in many files and must
   read identically everywhere: the RP6 block identity (110817 B, `5132bacd…`, unchanged r10a→r17);
   the `SELF_QA_RP6.md` identity (1038848 B, `07cf843d…` post-r17); the D026 counts (39 rows / 29
   closed / 10 supplemental / 15 residuals / 0 open, as corrected); SEC102's status
   (ACCEPTED-WITH-DISCLOSURE, freeze blocker #4 cleared); the freeze-literal count (17 distinct
   definitions, 27 raw occurrences); and the second-flagship state (all four blocks PENDING
   Claude Pro). Report every file that states any of these differently.

## Rules
- Every finding carries `file:line` for **both** the summary and the detail, plus which one you
  believe is correct and why.
- Distinguish **stale** (was true, superseded) from **wrong** (never true).
- Do not fix anything. Report; the Lead edits.
- A clean file is worth recording — list files swept and found consistent, so the sweep's coverage
  is provable rather than implied.

Print: files swept, internal contradictions found, cross-file disagreements found, and the single
most consequential inconsistency.
