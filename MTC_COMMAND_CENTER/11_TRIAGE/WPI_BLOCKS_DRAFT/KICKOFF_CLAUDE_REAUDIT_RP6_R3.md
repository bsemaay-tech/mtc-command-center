# KICKOFF — Claude flagship re-audit of RP6-P0 round-3 residuals (read-only, xhigh)

You are `claude-opus-5` xhigh, fresh session — the returning Claude flagship. Your
round-2 re-audit (`RP6_CLAUDE_REAUDIT_R2_2026-08-10.md`) returned REQUEST_CHANGES on 3
MEDIUM residuals (F1 fabricated rc=126 / dropped path; F2 stale D026 transcripts pinned
to HEAD; F3 undisclosed procfs assumption) + 2 nits. Round 3 claims all closed. Verify.
Report only. No host/network; local Git Bash fixture execution expected.

Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`): `WPI_BLOCKS_DRAFT/RP6-P0.sh` (final
`2d9b166e…`, 71743 B, `bbb40ab6`), `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`,
`RP6_REPAIR_R3_REPORT.md`, `RP6_FULLBLOCK_REPAIR_REPORT.md`, your R2 report (closure
contract), `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md`,
`DESIGN_DEFECT_PATTERNS_2026-08-10.md`.

Verify:
- **F1** `tool_not_evaluable` now emits `path=<p> rc=na … mechanism=…`, no `rc=126`, path
  restored; §8.1 row 1 amended to match. Re-run the non-executable-tool fixture.
- **F2** all four D026 transcripts (full-block fence + C13 R3 arm + R3 backstop + C13 R4
  arm) now reproduce: RED side pinned to an immutable blob, re-run and `cmp`-identical.
  Re-run at least the full-block fence and one C13 harness yourself.
- **F3** row-8 procfs discrimination present (ns-link device vs root) and load-bearing —
  drive the crafted-`/proc` fixture; the comparison-only mutant must admit it.
- **Nits** os-error-2 attribution corrected; producer-assumption header present.
- **Regression**: no round-1/2 closure reopened; diff vs `bbb40ab6^` confined to the 3
  residuals + 2 nits; re-derive hash+bytes; `bash -n`; C13 harnesses still green.

Output: print the full report — verdict first (`PASS`/`PASS-WITH-NITS`/`REQUEST_CHANGES`/
`BLOCK: <n>`), V-rows with evidence, findings most severe first.
