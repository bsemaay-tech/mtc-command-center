# KICKOFF — Claude flagship re-audit of the RP6-P0 full-block repair (round 2, xhigh)

You are `claude-opus-5` xhigh, fresh session — the returning Claude flagship slot. Your
round-1 audit (`RP6_CLAUDE_T0_AUDIT_2026-08-10.md`) returned BLOCK: 7 on `bff3c86e…`.
Codex repaired all seven (`RP6_FULLBLOCK_REPAIR_REPORT.md`) producing
`041c9da9769e36638c9785b54afc638fa8e7b475a6d24238fc10388916c048db` (commit `90d8d447`).
Verify closure adversarially. Report only — modify nothing. No host/network; local
Git Bash fixture execution expected.

Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`): the four RP6 files
(`WPI_BLOCKS_DRAFT/RP6-P0.sh`, `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`,
`RP6_FULLBLOCK_REPAIR_REPORT.md`), your round-1 report (closure contract),
`WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` (current), and
`DESIGN_DEFECT_PATTERNS_2026-08-10.md`.

Verify:
- **V1–V7**: one row per round-1 finding — closed/partial/not. RE-RUN your own round-1
  falsification fixtures against the repaired bytes; each must land on the repaired
  outcome. Row-8 gate: verify the execution-domain gate exists, uses `<PIN-AT-FREEZE>`
  constants with the rc-3 pre-check + `:?` pattern, emits the two named STOP tokens,
  and actually gates row 9; the accepting arm is a recorded freeze-gate item (not a
  finding).
- **V8** Regression: nothing that passed round 1 broke; diff vs `90d8d447^` confined
  to the seven findings' scope.
- **V9** Hash + bytes re-derived; `bash -n`; re-run the C13 harnesses (27 + 4 cases)
  and confirm still green on the new bytes.

Output: print the full report — verdict first (`PASS`/`PASS-WITH-NITS`/
`REQUEST_CHANGES`/`BLOCK: <n>`), V-rows with evidence, findings most severe first.
