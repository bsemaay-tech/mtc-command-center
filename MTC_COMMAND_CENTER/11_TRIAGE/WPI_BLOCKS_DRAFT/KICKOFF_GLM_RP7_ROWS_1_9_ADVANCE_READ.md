# KICKOFF — GLM advance read-audit of the RP7 rows 1-9 extension

You are GLM, unattended, `-PermissionMode acceptEdits`. **Do not ask for approval; never
fabricate an execution result.** Source-level only; verdict label `ADVANCE-SUPPLEMENTAL` —
you close no flagship slot. Read-only except your single report file. No git mutation.

## Subject

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh`, current identity
126182 B, SHA-256 `8355cb00fda8af2140d99ff9e97fe458376215dbd39267b2f2958d29fb9aba85`
(re-derive before reading). The rows 1-9 extension (sections `B2_rows_1_7`, `B4_rows_8_9`)
was implemented tonight by a gpt-5.5-class lane against the design of record
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/ROWS_1_9_OPTIONS_CODEX_2026-08-10.md` §D)
and will face flagship audits later; your advance read reduces their risk.

## Scope — bounded on purpose (SMALL/MEDIUM reads only)

1. The two new sections in the block (locate `RP7_SECTION B2_rows_1_7` and
   `RP7_SECTION B4_rows_8_9`), against §D.1/§D.4 of the design of record: presence proven
   before value for every `show` record; absent record → STOP not default; the two bounded
   captures reuse `wpi_capture` unchanged; no name-based leaf addressing anywhere (the
   `wpi_alloc_leaf` discipline); the row-6 parser is invoked `python3 -I -S` over a
   descriptor, not a re-resolved name.
2. The rows 1-9 D026 matrix section in
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md` (the rebuild fence
   section only — search `RP7_ROWS_1_9_REBUILD_FENCE_BEGIN`): does the fence really extract
   and invoke the block's own functions; are any expected values literals formatted as
   measurements; does every row's RED fail for the row's own reason.
3. The terminal-claim change (`rows_1_23…`) and the pin class in
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_RP7.md`.

Do NOT sweep the whole 1MB+ SELF_QA; a partial with honest coverage boundaries beats a
timeout. Stop when context runs low and state exactly what you reached.

## Output — the ONLY file you may write

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_ROWS_1_9_GLM_ADVANCE_READ_2026-08-13.md`

Findings with exact citations, classified required/nit; identities you re-derived; coverage
boundary; closing statement: no execution, no git mutation, `ADVANCE-SUPPLEMENTAL`.
