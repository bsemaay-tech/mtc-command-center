# KICKOFF — rows 1-9 round-2 repair (GLM advance-read findings)

Codex `-Account free`, xhigh. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No git mutation.
No sub-delegation. State your session-header model in the report.

## Input

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_ROWS_1_9_GLM_ADVANCE_READ_2026-08-13.md`
(ADVANCE-SUPPLEMENTAL, 4 REQUIRED + 2 NIT). Verify each finding against the bytes before
acting on it (a GLM finding is worth cross-checking, not trusting — one was false on 08-12).
For each: FIX, or REFUTE with citation, in your report.

- **R1** — row-8 rendered sandbox literals confirmed only against author-supplied fixtures:
  add the §D.4 #2 derivation disclosure (the pins are asserted renderings, their host
  derivation is a freeze-time act) wherever the fence claims coverage.
- **R2** — `wpi_assert_unit_execstart` false-STOPs on richer real-systemd `ExecStart`
  rendering (extra runtime fields, tokens without `=`). Make the parser tolerate unknown
  fields fail-open-to-STOP only on grammar violations, not on unknown keys — presence and
  exact match still required for `path`, `argv[]`, `ignore_errors`. Add a RED/GREEN pair
  driving the block's own function with a realistic started-unit rendering.
- **R3** — row 1 implemented via `ActiveState` instead of the verbatim `systemctl is-active`:
  do NOT silently amend the preregistration. Record it as an explicit, labelled
  preregistration-amendment note in `SELF_QA_RP7.md` + `STATUS_RP7.md` (property-based read
  with rationale), flagged for the flagship auditor and the owner-visible record.
- **R4** — add the §D.5 row-5 decoy fixture to the rebuild fence (executed, block's own code).
- **N1** — align the B2 capture-level parse-error reason label with §D.5 row 5
  (`unit_definition_unreadable`) or document the divergence explicitly.
- **N2** — make the row-6 Install-section match case-insensitive to match systemd's section
  parsing, with a RED fixture (`[install]` variant flips from control to RED).

## Rules

Same as the rebuild round: every new/changed D026 line produced by executing the block's own
extracted functions (no re-implementation, no literal result tuples); re-derive and loudly
declare the block identity change; update the fence + pasted transcript; Rule 9b authoring
rules; repo-wide grep on any changed identity.

## Files you own

`RP7-WPI-RO.sh`, `SELF_QA_RP7.md`, `STATUS_RP7.md`, and append a round-2 section to
`RP7_ROWS_1_9_REPORT_2026-08-13.md`. Nothing else.
