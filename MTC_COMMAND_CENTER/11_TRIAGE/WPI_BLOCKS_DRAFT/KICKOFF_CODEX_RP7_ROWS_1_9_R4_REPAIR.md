# KICKOFF — rows 1-9 round-4 repair (three REQUIRED from the Codex T0 flagship audit)

Codex `-Account free`, xhigh, IMPLEMENTER (fourth is the extension's auditor of record — do
not use it). Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No git mutation. No sub-delegation.
State your session-header model in the report.

## Input

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CODEX_T0_EXT_AUDIT_2026-08-13.md`
(REQUEST_CHANGES: 3 REQUIRED, 1 NIT). Read it in full; its three REQUIRED findings are the
work order:

1. The block does not implement all inability arms of the row-1 preregistration amendment.
2. The row-6 parser mis-models a documented systemd continuation form.
3. The row-9 tokenizer silently drops an unmodeled token and still passes — silence is never
   a result; give it a terminal disposition (STOP/coverage), fail-closed.

Verify each finding against the bytes before repairing (findings have been wrong before);
FIX or REFUTE-with-citation per item. Adopt the NIT if cheap.

## Discipline — unchanged from rounds 2/3

Every new/changed D026 line produced by executing the block's own extracted functions via
the rebuild fence (no re-implementation, no literal result tuples, shipped-policy path only);
add executed RED/GREEN pairs for each repaired defect; re-derive and loudly declare the new
block identity; update the fence + pasted transcript + STATUS; Rule 9b authoring rules;
repo-wide grep on changed identities (fix echoes only in owned files, list the rest).

## Files you own

`RP7-WPI-RO.sh`, `SELF_QA_RP7.md`, `STATUS_RP7.md`, and append a round-4 section to
`RP7_ROWS_1_9_REPORT_2026-08-13.md`. Nothing else.
