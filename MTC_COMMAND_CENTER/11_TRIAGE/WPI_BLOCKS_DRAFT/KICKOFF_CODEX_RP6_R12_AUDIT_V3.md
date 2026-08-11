# KICKOFF — Codex T0 audit: RP6-P0 round 12 (V3 — policy-read, NO mutant construction)

Date: 2026-08-11. Codex `gpt-5.6-sol` xhigh, AUDITOR of record, fresh session. Read-only:
edit nothing except your verdict file, no git mutation, no host, no network. T0 surface.

## Why this V3 exists

Two prior runs did the full audit but the provider content filter terminated BOTH before
writing the verdict — the trigger is you CONSTRUCTING fresh shell mutants that reach a
filesystem-touching emitter. So V3 forbids constructing any new attack shell. You verify the
round-12 census by (a) running the ALREADY-PUBLISHED harnesses that live in the file, and (b)
reasoning about the fail-closed POLICY at the level of construct CLASSES, never writing an
example. Do NOT author, echo, or execute any new emitter mutant of your own.

## HARD OUTPUT RULES
- Do not write any shell that calls or resolves to `p0_stop`/`p0_fail` or any RO tool.
- Refer to construct classes by name only: arithmetic-expansion, ANSI-C-quoting,
  parameter-default, process-substitution, alias/function-indirection, command/builtin-prefix.
- Quote only harness SUMMARY lines and `ASSERT_MET`/`unmodeled=`/`census_lines=` tokens.
- Verdict + findings FIRST.

## Bytes — commit `0259b4a4`
`RP6-P0.sh` UNCHANGED `5132bacd…` (round-12 fix is QA-census layer). `SELF_QA_RP6.md`,
`STATUS_RP6_P0.md`, `RP6_R12_REPORT_2026-08-11.md`.

## Round-11 findings (REQUEST_CHANGES ×2)
(1) HIGH: line-census missed constructed emitter command words (Pattern 12). (2) MEDIUM:
stale F4 comment.

## Round-12 fix (Lead ran the core harnesses VERBATIM, rc 0: R12_GRAMMAR 23/23, R12_F1_RED
33/33, R11_GUARDS 17/17, R10_F4 16/16)
R12_GRAMMAR puts a tokenizer before the grep (quote-state, backslash, line-continuation,
expansion collapse, recursion into `$( )` + `trap`), then a fail-closed policy: a command word
is admissible ONLY as BARE, one complete QUOTED_LITERAL, or a whole-word PURE_EXPANSION from a
declared six-handle RO-tool set; every other or unmodeled construct fails the fence.
Load-bearing: tokenizer emitter line set == grep census line set via `cmp`.

## Audit contract (execution + reading only, NO construction)
1. Run the PUBLISHED `R12_GRAMMAR`, `R12_F1_RED`, `R11_GUARDS`, `R10_F4` commands VERBATIM
   (they extract their own mutants from their own heredocs — you are running existing bytes,
   not authoring). Output to files; report only the summary lines and pass counts.
2. **Policy-soundness READ (no examples):** read the tokenizer + admissibility policy in
   `SELF_QA_RP6.md`. For EACH construct class named above, state whether the policy's
   "admissible only as BARE / complete QUOTED_LITERAL / declared PURE_EXPANSION, else fail"
   rule rejects it BY DESIGN — reasoning about how the tokenizer classifies that class, WITHOUT
   writing an instance. If any class could produce an admissible-looking word that still
   resolves to an emitter, name the class and the gap in words; do NOT write the shell. That
   is a finding (Pattern 12 residual).
3. Confirm the `cmp` tokenizer-vs-grep equality is load-bearing (a divergence fails the fence).
4. Confirm finding 2's F4 comment fix + the STATUS/report overclaim corrections are complete.
5. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK. If your only reservation is a
   construct class you could not verify by reading, record it as a NIT or a REQUEST_CHANGES
   with the class named — do not attempt to prove it by construction.

Write ONE new file: `RP6_CODEX_T0_AUDIT_R12_2026-08-11.md`.
