# KICKOFF — Codex T2: repo-wide `.gitattributes` durability ANALYSIS (design note only)

You are Codex `gpt-5.6-sol` xhigh, ANALYST. Working dir `C:\LAB\Tradingview_LAB_CLEAN`.
No host, no network, no commit. Write exactly ONE new file:
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_GITATTRIBUTES_DURABILITY_ANALYSIS_2026-08-12.md`.

## HARD CONSTRAINT — analysis only, change nothing
**Do NOT create, edit or delete any `.gitattributes` file. Do NOT touch any fixture, block,
self-QA or status file.** Second-flagship audits are scheduled tonight and every one of them
re-runs published harnesses **verbatim against the current checkout identities**. Changing a
line-ending attribute now would silently change those identities mid-cycle and invalidate the
audits. This kickoff produces the *plan*; the Lead executes it after tonight's audits complete.
Never git checkout/reset/stash.

## The problem
`WPI_PREREG_DRAFT_ROUND1/.gitattributes` (scoped) pins the SEC102 fixtures `-text` and the two
Python tools `text eol=lf`, so a fresh Windows checkout cannot silently rewrite the bytes whose
SHA-256 values are frozen in the evidence. **That protection is scoped to one directory.** The
same risk applies to every fixture-based block — RP6, RP7 and the transport set — whose accepted
identities are also frozen SHA-256 values over files that Git will happily materialize with
different line endings on a fresh clone. The repo sets `* text=auto` with `core.autocrlf=true`.

This became concrete today: SEC102 round 8 was a real defect where the evidence harness rewrote
LF to CRLF before execution (110 LF written as 110 CRLF), and the r11 acceptance still carries
disclosed residual 41 — byte identity is asserted against the on-disk document, not a pinned
checkout.

## What to produce

1. **Inventory of at-risk artifacts.** Every file whose exact bytes or SHA-256 is quoted as a
   frozen/accepted identity anywhere in `MTC_COMMAND_CENTER/11_TRIAGE`. At minimum:
   `RP6-P0.sh`, `RP7-WPI-RO.sh`, the nine transport files, `composite_pathproof.py`,
   `pathscope_prover.py`, every `sec102_r*_fixtures` tree, and any RP6/RP7/transport fixture
   directory. For each: current on-disk LF/CRLF composition, current SHA-256, whether it is
   covered by an existing `.gitattributes` rule, and which document quotes its identity.
2. **Determine actual current coverage.** Read every `.gitattributes` in the repo and state
   precisely which paths each rule reaches. Do not assume a rule applies because it looks like it
   should — resolve the precedence.
3. **The exposure statement.** For each uncovered artifact, state what would change on a fresh
   Windows clone and which frozen identity would break. Distinguish LOUD breakage (a harness that
   fails and says so) from SILENT breakage (an identity that quietly no longer matches).
4. **The proposed rule set.** Exact `.gitattributes` lines, per directory, with a one-line
   justification each. Prefer the narrowest scoped files over one repo-wide rule; say why.
   Explicitly state, for each proposed line, whether applying it would CHANGE any current
   working-tree byte (that is the dangerous class — those need re-hashing and possibly
   re-auditing, so they must be identified before anything is applied).
5. **A safe application order** for the Lead to follow after tonight's audits: what to apply
   first, what to re-derive after each step, and how to prove no accepted identity moved. Include
   the exact verification command sequence.

## Rules
- Every claim carries a `file:line` or a real measured value.
- Compute real LF/CRLF counts and SHA-256 values; do not infer them.
- If applying a rule would change bytes that a flagship has already accepted, say so loudly —
  that artifact needs an explicit Lead decision, not a silent normalization.
- End with a short "what I would NOT do" section naming any change that looks tidy but risks a
  frozen identity.

Print the at-risk count and the change-bytes count when done.
