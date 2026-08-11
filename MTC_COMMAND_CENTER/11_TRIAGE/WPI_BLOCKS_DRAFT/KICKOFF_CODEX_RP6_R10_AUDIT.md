# KICKOFF — Codex T0 audit: RP6-P0 round 10 bytes

Date: 2026-08-11. Codex `gpt-5.6-sol` xhigh, AUDITOR of record, fresh session. Read-only:
edit nothing, no git mutation, no host, no network. T0 surface.

## Bytes under audit

`WPI_BLOCKS_DRAFT/RP6-P0.sh` at commit `c14c7992`, SHA-256
`a090ae736cbecd9973e8ae948b052504b21cbe8b61602f4b5ac592394fad0617`, 107252 B (unchanged
from the round-10a partial — the round-10b work confirmed the partial closes the findings
and wrote the missing report/status; the block bytes themselves did not change from 10a).
`SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, `RP6_R10_REPORT_2026-08-11.md` at the same commit.

## Your round-9 findings (REQUEST_CHANGES ×4)

`RP6_CODEX_T0_AUDIT_R9_2026-08-11.md` — F1 (published `R9_GRAMMAR` command ran the mutant
file, not the harness — piped stdin ignored when bash gets a filename arg), F2 (declared vs
executable grammar not closed — 136/159 emitters undeclared), F3 (malformed followed-target
reaches rc 1), F4 (an unreachable relabelled line).

## Round-10 evidence to audit

`RP6_R10_REPORT_2026-08-11.md` — per-finding dispositions. The Lead has already run all
three round-10 harnesses VERBATIM from the block directory (the exact published
`sed -n '/^# R10_..._HARNESS_BEGIN$/,/^# R10_..._HARNESS_END$/p' SELF_QA_RP6.md | bash
--noprofile --norc` form) and observed rc 0 with:
- `R10_GRAMMAR_SUMMARY cases=10 pass=10 fail=0 result=PASS` (declared 89 forms/161 sites ==
  derived 89/161; wrapper 160 + direct 1; five mutants killed),
- `R10_F3_QA_SUMMARY cases=14 pass=14 fail=0 result=PASS`,
- `R10_F4_QA_SUMMARY cases=16 pass=16 fail=0 result=PASS`.

## Audit contract

- Re-run each published R10 command VERBATIM yourself; confirm the summary line appears in
  the real output (F1's failure mode was a published command that ran the wrong program —
  this is the primary thing to re-verify). State which you executed; non-execution is not
  acceptance (D025 rule 1).
- F2 grammar closure: independently re-derive the emitter grammar from the block bytes and
  confirm the 89/161 declared==derived claim; hunt any emitter the fence misses.
- F3/F4: verify the repairs in the bytes, not from the report's claims (D026 — each new
  test RED against pre-fix/mutant, GREEN with fix).
- The report claims ten "own-status guard" fences and self-corrections of round-10a prose
  errors (17→19 published commands; a 57→172 wall-clock count it declined to publish as a
  measurement). Judge whether the corrections are complete and whether any residual overclaim
  remains — a disclosure is not a control.
- Hunt new defects with the 13 patterns (`DESIGN_DEFECT_PATTERNS_2026-08-10.md`).
- Verdict grammar: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK.

Write ONE new file: `RP6_CODEX_T0_AUDIT_R10_2026-08-11.md`.
