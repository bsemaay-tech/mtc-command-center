# KICKOFF — Codex T1 re-audit: path-scope prover round 2 (OUTPUT-HYGIENE retry)

Date: 2026-08-11. Codex `gpt-5.6-sol` xhigh, AUDITOR of record, fresh session. Read-only:
edit nothing except your one verdict file, no git mutation, no host, no network. T1 surface.

## Why this is a retry

A prior run did the full audit (executed the fixtures, reached the adversarial construction)
but the provider content filter terminated it before it wrote the verdict, because your OWN
STDOUT echoed the prover's per-path FORBID lines, which contain sensitive system-path
literals (the fixtures deliberately reference protected paths — that IS the tool under test).
This retry keeps your output clean so the verdict persists.

## OUTPUT-HYGIENE RULES (mandatory — the whole point of this retry)

1. When you run the harness, REDIRECT its stdout/stderr to files under your temp dir. Do NOT
   echo the harness's per-path lines (`PATH value=... verdict=FORBID ...`) into your own
   assistant output or into the verdict file.
2. In everything you write, refer to sensitive fixtures by SYMBOLIC NAME only — e.g.
   `SENSITIVE_SYS_FILE`, `SENSITIVE_SHADOW`, `EXFIL_URL`, `REMOTE_HOST` — never the raw
   `/etc/...` or URL literal. Quote only the prover's SUMMARY lines
   (`PATHSCOPE verdict=... rc=...`, `PATHSCOPE ..._count=...`, `PATHSCOPE_SUMMARY`) and
   counts, which contain no sensitive literal.
3. Report fixture results as counts and pass/fail per case-id, not as reproduced attack
   bodies. "Case find_exec: RED rc as expected, GREEN rc as expected" — not the fixture text.
4. Write your verdict file INCREMENTALLY (verdict + findings first, evidence appended), so a
   late termination still leaves a usable verdict on disk.

## Bytes under audit — commit `71a62cc8`

`pathscope_prover.py` 122446 B, SHA-256
`890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d`.
`SELF_QA_PATHSCOPE.md`, `STATUS_PATHSCOPE.md`, `PATHSCOPE_REPAIR_R2_REPORT.md` same commit.

## What to audit (unchanged from v1, minus the echo)

Round-1 findings: `PATHSCOPE_CODEX_T1_AUDIT_2026-08-10.md` (9, four CRITICAL silent-sink).
Round-2 evidence: `PATHSCOPE_REPAIR_R2_REPORT.md`. Structural change: `NO_PATH_COMMANDS`/
`nonoption_operands()` removed; explicit `Spec` registry; unlisted option / unregistered
command → rc-3 coverage record. Finding 6 repaired as DISCLOSURE (`ALLOW-LEXICAL` +
`symlink_resolution=not_established mount_boundary=not_established`), symlink/mount binding
recorded as residual R1. Five more silent-pass classes fixed. Lead re-ran the harness
verbatim; summary output matched the document exactly (RED 511 / GREEN 644 lines,
determinism `equal=True` for all three targets).

Audit contract:
- Adversarially construct NEW Bash fragments that reach a filesystem/network primitive while
  the prover emits no path / no coverage record / `PASS rc=0`. Describe each construction by
  its MECHANISM (e.g. "option-value split across `=` with an unregistered long option"), and
  report only the resulting `PATHSCOPE` summary line + rc. Any surviving silent sink is
  CRITICAL. This is the core of the audit.
- Re-run the harness (output to files); confirm the 62 fixtures + 4 real-block runs and the
  RED-before-GREEN ordering (D026). Non-execution is not acceptance (D025 rule 1). Report
  counts, not bodies.
- Judge finding 6: is `ALLOW-LEXICAL` + residual R1 an honest, explicitly-labelled limit, or
  does any run still present lexical membership as an unconditional host ALLOW? A disclosure
  is not a control, but an honestly-scoped weaker claim is acceptable for a T1 tool whose
  composite proof lives in SEC102.
- 13 defect patterns (`../DESIGN_DEFECT_PATTERNS_2026-08-10.md`).
- Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK.

Write ONE new file: `PATHSCOPE_CODEX_T1_AUDIT_R2_2026-08-11.md`.
