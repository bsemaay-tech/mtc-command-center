# KICKOFF — Codex flagship T0 audit slot: RP7-WPI-RO.sh round-3 bytes (read-only, xhigh)

You are the Codex flagship slot of the T0 contract: fresh session, `gpt-5.6-sol`,
xhigh. Claude's slot ran rounds 1–2 (BLOCK 13 → 13/13 closed + BLOCK 6) and round 3
closed all six. You are the SECOND flagship — acceptance requires your verdict too.
Audit adversarially; you are not bound by the Claude findings lists. Report only.

**Owner amendment A2/A2a in force: do the audit yourself, no sub-delegation.**

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`)

1. `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` — round-3 bytes (claimed SHA-256
   `1d118d1581534f5d16b3730efbe642e80e5232fbf8a245d238574907166a7f4e`, 58012 B, commit
   `1c1c9ed1`).
2. `WPI_BLOCKS_DRAFT/SELF_QA_RP7.md` — QA (GNU coreutils/Git Bash environment; three
   narrow fixture substitutions tabulated for MSYS limits).
3. `WPI_BLOCKS_DRAFT/STATUS_RP7.md`, `RP7_REPAIR_R3_REPORT.md` — state + dispositions.
4. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — current draft (§8.2 rows
   10–24 + all binding rule paragraphs + projection-v2 attestation definition).
5. `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — attack with all ten patterns.
6. Prior audit trail for context (do not treat as exhaustive):
   `RP7_CLAUDEPRO_AUDIT_2026-08-10.md`, `RP7_CLAUDEPRO_REAUDIT_R2_2026-08-10.md`.

## Contract

- Full row-by-row conformance (rows 10–24) at exact FAIL/STOP grammar; ordering rules;
  path-object binding incl. projection v2 (attack it: subtree blindness, tie-breaks,
  record grammar, escaped-character handling); STOP-vs-FAIL truthfulness on every
  branch; probe execution-environment (timeout inversion included); structured
  parsing; read-only scope.
- RE-RUN the QA fence yourself from the published bytes; re-derive hash + bytes;
  `bash -n`. Execute your own falsification fixtures where practical — a finding with
  an executed falsification outranks a code-read claim.
- Known freeze-gate items (not findings): the accepting `wpi_validate_inputs` arm and
  the `<PIN-AT-FREEZE>` attestation digest.

Output: write `WPI_BLOCKS_DRAFT/RP7_CODEX_T0_AUDIT_2026-08-10.md` — verdict first
(`PASS`/`PASS-WITH-NITS`/`REQUEST_CHANGES`/`BLOCK: <n>`), V-rows with evidence,
findings most severe first. Touch ONLY that file.
