# KICKOFF — Codex T1 re-audit: path-scope prover round 2

Date: 2026-08-11. Codex `gpt-5.6-sol` xhigh, AUDITOR of record (you wrote the round-1 T1
audit), fresh session. Read-only: edit nothing, no git mutation, no host, no network. T1
surface (non-economic tool).

## Bytes under audit — commit `e7a670b3`

`pathscope_prover.py` 122446 B, SHA-256
`890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d` (was 49820 B).
`SELF_QA_PATHSCOPE.md`, `STATUS_PATHSCOPE.md`, `PATHSCOPE_REPAIR_R2_REPORT.md` same commit.

## Your round-1 findings (REQUEST_CHANGES ×9, four CRITICAL)

`PATHSCOPE_CODEX_T1_AUDIT_2026-08-10.md` — CRITICAL silent-sink classes 1–4 (each reached a
filesystem/network primitive while the prover emitted no path, no UNRESOLVED, and
`verdict=PASS rc=0`); HIGH 5 (tilde false-ALLOW), 6 (lexical membership presented as
unconditional host ALLOW), 7; plus 8, 9.

## Round-2 evidence

`PATHSCOPE_REPAIR_R2_REPORT.md` — finding→disposition→evidence. Structural change:
`NO_PATH_COMMANDS`/`nonoption_operands()` removed; one explicit `Spec` registry declares per
command every accepted option and its value role; unlisted option / unregistered command →
specific rc-3 coverage record. Finding 6 is repaired as DISCLOSURE only (`ALLOW-LEXICAL`
token + `semantics=lexical_argv_scope symlink_resolution=not_established
mount_boundary=not_established`), with the symlink/mount binding recorded as residual R1
that a static reader cannot perform. Five further silent-pass classes were found and fixed
(`python3 -c`, `alias`, `hash -p`, `mapfile -C`, `systemctl link`, `jobs -x`).

The Lead has re-run the published harness verbatim; its stdout matched the document exactly
(R2 sha256, both block digests, RED 511 / GREEN 644 lines, determinism `equal=True` for
find_exec, RP6-P0, RP7-WPI-RO).

## Audit contract

- Try to defeat the tool: construct NEW Bash fragments that reach a filesystem or network
  primitive while the prover still emits no path / no coverage record / `PASS rc=0`. The
  round-1 findings were exactly such constructions — repeat that adversarial method against
  the new `Spec` registry. Any surviving silent sink is CRITICAL.
- Re-run the harness yourself; confirm the 62 fixtures + 4 real-block runs and the RED/GREEN
  transcripts. Non-execution is not acceptance (D025 rule 1); RED must precede GREEN (D026).
- Judge finding 6's disclosure: is `ALLOW-LEXICAL` + residual R1 an honest limit, or does any
  run still present a lexical membership as an unconditional host ALLOW (the original defect)?
  A disclosure is not a control — but an honestly-scoped weaker claim, explicitly labelled,
  is acceptable for a T1 tool whose composite proof lives in SEC102.
- Hunt new defects with the 13 patterns (`../DESIGN_DEFECT_PATTERNS_2026-08-10.md`).
- Verdict grammar: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK.

Write ONE new file: `PATHSCOPE_CODEX_T1_AUDIT_R2_2026-08-11.md`.
