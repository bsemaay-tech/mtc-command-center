# KICKOFF — Codex flagship T0 audit slot: RP6-P0.sh full block (read-only, xhigh)

You are the Codex flagship slot of the T0 contract: fresh session, `gpt-5.6-sol`, xhigh.
The Claude flagship ran the full block (BLOCK 7 → all closed → BLOCK 3 residuals → round
3). You are the SECOND flagship — acceptance needs your verdict. Earlier Codex rounds on
this block audited ONLY the C13 getent arm at high effort; the whole block at flagship
xhigh has never been Codex-audited. Attack the entire block. Report only.

**Owner amendment A2/A2a in force: do the audit yourself, no sub-delegation.**

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`)

1. `WPI_BLOCKS_DRAFT/RP6-P0.sh` — final bytes (claimed SHA-256
   `2d9b166eacfc39ebe0d8d89edb5860876ccc4d9f0ff97f9e10a228dbcf96289e`, 71743 B, commit
   `bbb40ab6`).
2. `WPI_BLOCKS_DRAFT/SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, `RP6_FULLBLOCK_REPAIR_REPORT.md`,
   `RP6_REPAIR_R3_REPORT.md`.
3. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — §8.1 P0 rows 1–9 (current).
4. `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — attack with all ten patterns.
5. Prior audit trail for context (not exhaustive): `RP6_CLAUDE_T0_AUDIT_2026-08-10.md`,
   `RP6_CLAUDE_REAUDIT_R2_2026-08-10.md`, `RP6_C13_CODEX_AUDIT_2026-08-10.md`.

## Contract

Verify every §8.1 row 1–9 at exact FAIL/STOP grammar; STOP-vs-FAIL truthfulness on every
branch; numeric identity; capability ledger; getent arm incl. the R4 sentinel + NUL
handling; the row-8 execution-domain gate (attested namespace + root-mount identities,
`<PIN-AT-FREEZE>` constants, rc-3 pre-check + `:?`, the two named STOP tokens, and that it
actually gates row 9 — the Claude side proved it load-bearing; re-verify by removing the
comparison and the call); the argv[0]-prefix filesystem classifier (verify it matches on
GNU and note the uutils fail-closed residual); tool inventory; read-only scope.
RE-RUN the C13 harnesses (16+4+27 cases) and the full-block fence; re-derive hash + bytes;
`bash -n`. Execute your own falsification fixtures where practical. Known freeze-gate items
(NOT findings): the row-8 accepting arm and the `<PIN-AT-FREEZE>` attestation constants.

Output: write `WPI_BLOCKS_DRAFT/RP6_CODEX_T0_AUDIT_2026-08-10.md` — verdict first
(`PASS`/`PASS-WITH-NITS`/`REQUEST_CHANGES`/`BLOCK: <n>`), V-rows with evidence, findings
most severe first. Touch ONLY that file.
