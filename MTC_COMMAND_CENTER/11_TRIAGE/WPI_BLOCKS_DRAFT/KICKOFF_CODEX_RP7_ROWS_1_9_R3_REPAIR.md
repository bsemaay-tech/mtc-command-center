# KICKOFF — rows 1-9 round-3 repair (two REQUIRED from the Claude flagship audit)

Codex `-Account free`, xhigh. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No git mutation.
No sub-delegation. State your session-header model in the report.

## Input

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CLAUDE_T0_EXT_AUDIT_2026-08-13.md`
(REQUEST_CHANGES: 2 REQUIRED, 4 NIT; the auditor states an accepting verdict was otherwise
available and expects PASS/PASS-WITH-NITS on repair). Read it in full.

1. **REQUIRED-1** — revert the row-6 Install match to case-SENSITIVE (the round-2 change was
   built on a factually false justification: systemd treats `[install]` as an unknown section
   and ignores it, so flagging it is a wrong verdict). Reclassify the `[install]` fixture back
   to a control (ignored ≠ Install section), remove the false justification sentence wherever
   it appears in the lane files, and re-run the fence. This is the round-2 lane's
   verify-before-fix failure — say so plainly in the report.
2. **REQUIRED-2** — carry the row-1 amendment into the preregistration properly: the auditor
   ACCEPTS the `ActiveState` predicate on engineering grounds (§D.4 option b; defeats
   Pattern 1) but the preregistration still declares `systemctl is-active` and the STOP token
   `operation=is-active` while the block emits `operation=show`. Add a **labelled amendment
   block** to `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md`
   at the row-1 site (quote the original text, state the amended predicate + STOP token, cite
   the design-of-record option and the Claude verdict) — do NOT silently rewrite the original
   sentence. Mirror the amendment note in `SELF_QA_RP7.md`/`STATUS_RP7.md` where they discuss
   row 1.
3. Adopt the four NITs where cheap; list each done/skipped with reason.

## Discipline

Executed evidence only (block's own functions, shipped-policy path); re-derive + loudly
declare the new block identity; repo-wide grep on changed values; Rule 9b rules.

## Files you own

`RP7-WPI-RO.sh`, `SELF_QA_RP7.md`, `STATUS_RP7.md`,
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md`
(amendment block only), and append a round-3 section to
`RP7_ROWS_1_9_REPORT_2026-08-13.md`. Nothing else.
