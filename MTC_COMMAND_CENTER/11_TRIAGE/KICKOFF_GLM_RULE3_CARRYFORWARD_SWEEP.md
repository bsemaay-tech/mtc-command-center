# KICKOFF — apply authoring RULE 3 (carry-forward re-derivation) as a detection pass

**Unattended — do not ask for approval, do not write a plan and stop. Execute directly and write
your verdict file.** Working dir `C:\LAB\Tradingview_LAB_CLEAN`. Read-only: create nothing except
your verdict file, no git mutation, no host, no network. Never git checkout/reset/stash.

**Do not write to any path that already exists.** Your output path is new; if it somehow exists,
stop and say so rather than overwriting a prior lane's record.

## Why
Rule 3 of `WPI_CLAIM_AUDIT_SYNTHESIS_2026-08-12.md`: *any carried-forward section must be
re-derived after the final artifact edit — old bytes, hashes, round labels and denominators
replaced from a current identity table, and scope wording must use the exact denominator the
transcript shows.*

Today's evidence that this is the live failure mode: `SELF_QA_RP7.md` carries three **stale byte
identities** (`92853/e695a67b`, `20050 B`, `77179/393a16ce`) in carried-forward sections while
every transcript in the same document shows the current `108301/0e93f90d…`. Six carried-fence
summaries in that file also say "round-8 bytes" when the transcripts show round-9.

**Only RP7 has been checked this way.** The other documents carry forward too.

## What to sweep
`WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md`, `WPI_PREREG_DRAFT_ROUND1/SELF_QA_PATHSCOPE.md`, and
`WPI_PREREG_DRAFT_ROUND1/SELF_QA_SEC102_R11.md`. **Skip `SELF_QA_RP6.md` and `SELF_QA_RP7.md`** —
both already have dedicated audits, and skipping them keeps this lane completable.

In each, find every **carried-forward** section (any section describing a round earlier than the
document's current round) and check:

1. **Byte identities and hashes.** Does the carried section quote an identity that the document's
   own current transcripts contradict? Report both values.
2. **Round labels.** Does it say evidence was run against round *N* bytes when the transcript
   shows round *M*?
3. **Denominators in scope wording.** Does it say "every block", "all files", "each fixture" where
   the transcript shows a narrower set — e.g. `10/11 plus one self-exclusion`, `seven targets plus
   the harness`? Report the claimed denominator and the transcript's actual one.

## Rules
- `file:line` for **both** the carried claim and the transcript line that contradicts it.
- **A carried section that correctly labels itself historical is NOT a finding.** The defect is a
  carried value presented as current. Say which you excluded on that basis.
- Do not edit anything. Report; the Lead edits.
- A clean document is a useful result — say so plainly.
- State coverage honestly. If you cannot finish a document, say which sections you covered.
- Never fabricate a run; mark anything unexecutable `PENDING-LEAD-EXECUTION`.

## Current-identity reference (use this as the truth table)
`RP6-P0.sh` 110817 / `5132bacd…` · `RP7-WPI-RO.sh` 108301 / `0e93f90d…` ·
`composite_pathproof.py` 129658 / `adbf27fd…` · `pathscope_prover.py` 122446 / `890016f0…` ·
`SELF_QA_RP6.md` 1038848 / `07cf843d…`

Write ONE new file: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_RULE3_CARRYFORWARD_SWEEP_2026-08-12.md`.
Print: documents covered, carried sections examined, findings by type, and the most consequential.
