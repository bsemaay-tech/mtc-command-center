# KICKOFF — FINAL T0 flagship audit: RP6-P0.sh round-4 bytes (read-only, xhigh)

You are a T0 flagship auditor, fresh session, xhigh. This is the acceptance audit for
`RP6-P0.sh`. Report only — modify nothing. No host/network; local Git Bash fixture
execution expected.

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`)

1. `WPI_BLOCKS_DRAFT/RP6-P0.sh` — final bytes: SHA-256
   `e93d07adcc9ae03ad15e0b0f10c76be54517251ab461c8fe789d160072d253c6`, 85540 B,
   commit `945e20f5`.
2. `WPI_BLOCKS_DRAFT/SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, `RP6_REPAIR_R4_REPORT.md`,
   `RP6_FULLBLOCK_REPAIR_REPORT.md`.
3. Round-4 closure contract: `WPI_BLOCKS_DRAFT/RP6_CODEX_T0_AUDIT_2026-08-10.md`
   (F1–F4). Earlier trail for context: `RP6_CLAUDE_T0_AUDIT_2026-08-10.md`,
   `RP6_CLAUDE_REAUDIT_R2_2026-08-10.md`, `RP6_CLAUDE_REAUDIT_R3_2026-08-10.md`.
4. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — §8.1 rows 1–9 (current).
5. `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — attack with all ten patterns.

## Verify

- **V1–V4** — the four round-4 findings closed, each re-driven by YOUR OWN fixture:
  F1 the interpreter probe runs `-I -S` and an executable `.pth` cannot execute or
  forge the accepted line; F2 the row-9 `systemctl` query is genuinely bounded (stall
  fixture must produce the block's own STOP, not need an external kill); F3 the RO
  inventory matches the FROZEN RP7 tool set (`23e55667…`: `stat readlink env find
  sha256sum systemctl ss curl timeout python3`) plus P0-only `id`/`getent`, accepts a
  complete RP7 pin set, and the drift test is real; F4 `identity_unresolvable` carries
  honest `rc=<n|na>` on both callers and the row-3 grammar matches the emitted token.
- **V5** Whole-block sweep independent of the finding lists — rows 1–9 exact grammar,
  STOP-vs-FAIL truthfulness on EVERY branch, numeric identity, capability ledger,
  execution-domain gate (verify it still gates row 9; try removing comparison and call),
  getent sentinel incl. NUL, read-only scope.
- **V6** QA integrity: re-run the mandated harnesses named in `STATUS_RP6_P0.md`
  (full-block fence, R4 D026, R4b C13 27-case, backstop, freeze). Note: two older C13
  fences at `SELF_QA_RP6.md` lines ~664-787 and ~1181-1346 are DELIBERATELY red as
  superseded round records — that disposition is documented; judge whether it is
  honest, do not treat it as an undisclosed failure.
- **V7** Re-derive SHA-256 + bytes; `bash -n`; LF-only.

Known freeze-gate items, NOT findings: `P0_FIXED_TRUSTED_PYTHON` and the five row-8
execution-domain attestation literals are `<PIN-AT-FREEZE>`, so no end-to-end GREEN can
exist before freeze.

Output: verdict first (`PASS` / `PASS-WITH-NITS` / `REQUEST_CHANGES` / `BLOCK: <n>`),
then V-rows with evidence, then findings most severe first with executed falsifications.
Codex slot: write to `WPI_BLOCKS_DRAFT/RP6_CODEX_FINAL_AUDIT_2026-08-10.md`.
Claude slot: print the full report as your final output.
