# AUDIT KICKOFF — round 5 doc-only closure audit (Codex, narrow)

Round 5 was DOCUMENTATION-ONLY: the code was already CLOSED at audit 4 (finding 1),
and round 5 rewrites `SELF_QA.md` only to close audit-4 finding 2 (D026 exact-command
recording). Confirm both: (a) the code is genuinely frozen, and (b) the QA now records
literal exact commands.

## Scope — read ONLY

- `audit4/AUDIT4_REPORT.md` (finding 2 + nit 2), `ROUND5_KICKOFF_DOC_ONLY.md`,
  `round5/` (under audit), `round4/` (baseline).

## Audit questions

1. **Code freeze**: confirm `round5/RP1-B3.sh`, `round5/RPD-VERIFY.sh`,
   `round5/DESIGN_NOTES.md` are byte-identical to `round4/` (hash them;
   RP1-B3 must be `6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc`,
   RPD-VERIFY `3b9e78e87cecdc10ab1a10d14e79dbff530968e4075277117743c88976fa813c`). ANY
   code delta is an immediate BLOCK (round 5 had no code license).
2. **Finding 2 closure**: for every closure test in `round5/SELF_QA.md`, is the recorded
   command literal and exact (no `<FIX>`/`<CASE>`/`<PRE>` placeholders in any command
   block, no dependence on prior overwritten `arm.sh` state)? Pick at least 4 commands
   — including item-1 cwd RED, an item-4 constant, and an item-6 STUB_CASE — and run
   them EXACTLY as written; each must reproduce its stated output. A command that needs
   any edit to run is NOT closed.
3. **Nit 2 + arithmetic**: confirm the mid-table limitation wording is narrowed and the
   subcounts are exact (43 A / 119 B / 3 C).

## Output

`audit5/AUDIT5_REPORT.md`, verdict first: **PASS / PASS-WITH-NITS / BLOCK**. A residual
placeholder or non-runnable command in any closure block is a REQUIRED finding.
Documentation-only scope — do not re-litigate code paths audit 4 already closed unless
question 1 shows the code changed. English, ASCII only.
