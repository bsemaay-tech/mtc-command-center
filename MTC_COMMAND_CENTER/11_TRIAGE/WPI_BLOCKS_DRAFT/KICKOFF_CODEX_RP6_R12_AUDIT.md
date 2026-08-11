# KICKOFF — Codex T0 audit: RP6-P0 round 12 bytes

Date: 2026-08-11. Codex `gpt-5.6-sol` xhigh, AUDITOR of record, fresh session. Read-only:
edit nothing except your verdict file, no git mutation, no host, no network. T0 surface.

## Bytes under audit — commit `7fb228ce`

`RP6-P0.sh` UNCHANGED at SHA-256
`5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330` (the round-12 fix is in
the QA census layer, not block source). `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`,
`RP6_R12_REPORT_2026-08-11.md`.

## Your round-11 findings (REQUEST_CHANGES ×2)

`RP6_CODEX_T0_AUDIT_R11_2026-08-11.md` — (1) HIGH: the line-oriented census missed valid
constructed emitter command words (`p0_s""top` resolves to `p0_stop`, `bash -n` 0, emits at
rc 3, but census reports `unmodeled=0` PASS — Pattern 12); (2) MEDIUM: a stale F4 overclaim
comment inside the live R10_F4 harness.

## Round-12 dispositions to verify

The Lead ran the core harnesses VERBATIM (rc 0):
- `R12_GRAMMAR` 23/23 — supersedes R11_GRAMMAR (all 8 R11 assertions + 7 mutants carried), adds
  a tokenizer BEFORE the grep: quote-state tracking, backslash resolution, line-continuation
  joining, expansion collapsing, recursion into every `$( )` and the `trap` action, then
  command-position analysis. Fail-closed policy: a command word is admissible ONLY as BARE, a
  single complete QUOTED_LITERAL, or a whole-word PURE_EXPANSION from a declared six-handle
  RO-tool set; everything else and every unmodeled construct (heredoc, backtick, eval,
  unterminated quote) fails. New load-bearing assertion: tokenizer emitter line set == grep
  census line set via `cmp`. Mutants killed: `cmdquote`, `expand`, `continuation` (tokenizer),
  `handle` (declared-runtime-set).
- `R12_F1_RED` 33/33 — extracts the whole published R11 AND R12 fences + the mutant insertions
  from R12's own heredocs, runs both over the same bytes. For `p0_s""top`,
  `${P0_R12_EXPHEAD}top`, and the line-continuation split: `bash -n` 0, real emission rc 3,
  **R11 fence rc 0 `unmodeled=0` (RED)**, **R12 fence nonzero (GREEN)**.
- `R11_GUARDS` 17/17 (extended 15→17), `R10_F4` 16/16 (comment now "unreachable for the three
  input classes this fence executes", guard_at_line=162 preserved).

## Audit contract

- Re-run each published R12 command VERBATIM; confirm summaries + statuses.
- **The core test:** try to construct ANOTHER emitter form that reaches a P0_STOP/P0_FAIL
  wrapper at runtime while the R12 tokenizer census still reports `unmodeled=0`/PASS. Try:
  arithmetic-expansion command words, `$'...'` ANSI-C quoting, a command split across a
  parameter-expansion default (`${x:-p0_stop}`), an aliased/functioned wrapper, a `command`/
  `builtin` prefix, process substitution. Any surviving silent emitter is a repeat of finding
  1 and CRITICAL. If the fail-closed policy genuinely rejects every unmodeled construct, say so.
- Confirm the `cmp` tokenizer-vs-grep equality assertion is load-bearing (would a divergence
  actually fail the fence?).
- Confirm finding 2's comment fix and that STATUS/report overclaim corrections are complete.
- 13 defect patterns. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK.

Write ONE new file: `RP6_CODEX_T0_AUDIT_R12_2026-08-11.md`.
