# KICKOFF — Codex T0 audit: RP6-P0 round 12 (OUTPUT-HYGIENE retry)

Date: 2026-08-11. Codex `gpt-5.6-sol` xhigh, AUDITOR of record, fresh session. Read-only:
edit nothing except your verdict file, no git mutation, no host, no network. T0 surface.

## Why this is a retry

A prior run did the full audit (~149k tokens, constructed the adversarial census-evasion
mutants) but the provider content filter terminated it before it wrote the verdict, because
your OWN OUTPUT echoed shell fragments that construct a filesystem-touching wrapper command.
This retry keeps your output clean so the verdict persists.

## OUTPUT-HYGIENE RULES (mandatory)

1. When you build/run a census mutant, write the mutant and the harness output to FILES under
   your temp dir. Do NOT echo the mutant's shell body or the emitter line into your own
   assistant output or the verdict file.
2. Refer to every mutant form by SHORT NAME only — `cmdquote`, `expand`, `continuation`,
   `handle`, `arith`, `ansic`, `paramdefault`, `procsubst`, `aliased`, `cmdprefix` — never the
   literal shell text. Report each form's result as: `<name>: bash_n=<0|1>,
   census_unmodeled=<N>, r12_fence_rc=<n>, emits_at_runtime=<yes|no>`. Those tokens carry no
   attack payload.
3. Quote only SUMMARY lines from the harnesses (`R12_GRAMMAR_SUMMARY`, `R12_F1_RED_SUMMARY`,
   `census_lines=`, `unmodeled=`, `ASSERT_MET ...`). Never the per-fragment shell.
4. Write the verdict + findings FIRST, evidence after.

## Bytes under audit — commit `4343199b`

`RP6-P0.sh` UNCHANGED, SHA-256
`5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330` (round-12 fix is QA-census
layer). `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, `RP6_R12_REPORT_2026-08-11.md`.

## Your round-11 findings (REQUEST_CHANGES ×2)

(1) HIGH: line-census missed constructed emitter command words (a wrapper word assembled from
adjacent quoted+unquoted segments resolves to the emitter but the census reported
`unmodeled=0` PASS — Pattern 12). (2) MEDIUM: a stale F4 overclaim comment.

## Round-12 dispositions (Lead already ran the core harnesses VERBATIM, rc 0)

- `R12_GRAMMAR` 23/23 — a tokenizer now precedes the grep (quote-state, backslash,
  line-continuation, expansion collapse, recursion into `$( )` + `trap`), then a fail-closed
  policy: a command word is admissible ONLY as BARE / one complete QUOTED_LITERAL / whole-word
  PURE_EXPANSION from a declared six-handle RO-tool set; every other or unmodeled construct
  fails. Load-bearing assertion: tokenizer emitter line set == grep census line set via `cmp`.
  Mutants killed: cmdquote, expand, continuation (tokenizer), handle (declared-set).
- `R12_F1_RED` 33/33 — R11 fence blind (`unmodeled=0`, RED) vs R12 fence nonzero (GREEN) for
  cmdquote / expand / continuation.
- `R11_GUARDS` 17/17; `R10_F4` 16/16 (comment fixed).

## Audit contract

- Re-run the published R12 commands VERBATIM (output to files); report only the summary lines.
- **Core adversarial test (the whole point):** try to construct ANOTHER wrapper command word
  that reaches a P0_STOP/P0_FAIL emitter at runtime while the R12 tokenizer census still
  reports `unmodeled=0`/PASS. Cover at least: arith-expansion word, `$'...'` ANSI-C quoting,
  parameter-default `${x:-...}`, process substitution, alias/function indirection,
  `command`/`builtin` prefix. Report each ONLY as `<name>: census_unmodeled=<N>,
  r12_fence_rc=<n>, emits=<yes|no>` per rule 2 — never the shell body. Any form that emits at
  runtime while the census stays `unmodeled=0` is a repeat of finding 1 and CRITICAL.
- Confirm the `cmp` tokenizer-vs-grep equality is load-bearing.
- Confirm finding 2's comment fix + STATUS/report overclaim corrections.
- Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK.

Write ONE new file: `RP6_CODEX_T0_AUDIT_R12_2026-08-11.md`.
