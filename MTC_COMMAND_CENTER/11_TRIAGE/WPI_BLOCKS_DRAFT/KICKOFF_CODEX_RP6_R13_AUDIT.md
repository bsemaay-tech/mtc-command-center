# KICKOFF — Codex T0 audit: RP6-P0 round 13 (policy-read, NO mutant construction)

Date: 2026-08-11. Codex `gpt-5.6-sol` xhigh, AUDITOR of record, fresh session. Read-only:
edit nothing except your verdict file, no git mutation, no host, no network. T0 surface.

## Why this is policy-read only
Your r12 audit tripped the content filter twice on constructed census-evasion shell; the third
run (no construction) cleared it. Keep that: run ONLY the ALREADY-PUBLISHED harnesses (they
extract their own mutants from their own heredocs) and reason about the policy by construct
CLASS. Do NOT author, echo, or execute any new emitter mutant. Refer to classes by name
(alias, function-shadow, tool-shadow, command/builtin/exec-prefix). Quote only summary/
`ASSERT_MET`/`unmodeled=`/`killed_by=` lines. Verdict first.

## Bytes — commit `0015a7fa`
`RP6-P0.sh` UNCHANGED `5132bacd…` (census is QA-layer). `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`,
`RP6_R13_REPORT_2026-08-11.md`.

## Your r12 findings (REQUEST_CHANGES ×2, both Pattern-12 census residuals)
(1) alias/function-indirection — a BARE command word admitted without binding its runtime
resolution. (2) command/builtin-prefix — the prefix consumes command position, effective
operand unclassified.

## Round-13 dispositions (Lead ran R13_GRAMMAR VERBATIM, 30/30 rc 0)
`ASSERT_MET mutant=alias killed_by=alias_indirection_impossible(expand_aliases not enabled)`;
`mutant=shadow killed_by=no_wrapper_shadow(p0_stop/p0_fail/builtin/tool)`;
`mutant=toolshadow killed_by=no_wrapper_shadow(...tool_shadow=1)`;
`mutant=cmdprefix killed_by=runtime_command_words_declared` (command/builtin/exec stripped +
operand classified). `R13_F1_RED` 35/35 (R12 fence PASS/rc0 → R13 nonzero for all 4 classes).
`R11_GUARDS` 19/19. RP6-P0.sh untouched.

## Audit contract (execution + reading only, NO construction)
1. Run the published `R13_GRAMMAR`, `R13_F1_RED`, `R11_GUARDS`, `R10_F4`, `R11_R9RED` commands
   VERBATIM (output to files; report only summaries). Confirm the alias/shadow/toolshadow/
   cmdprefix mutants are killed and R13_F1_RED shows R12-blind→R13-caught for all four classes.
2. **Policy-soundness READ (no examples):** for EACH of {alias, function-shadow, tool-shadow,
   command/builtin/exec-prefix} state whether the r13 policy closes it BY DESIGN —
   - alias: does asserting the block neither `shopt -s expand_aliases` nor defines an `alias`
     actually make alias indirection impossible for the block's own execution?
   - function/tool-shadow: does "no block function name equals or resolves to a
     p0_stop/p0_fail/builtin/tool" cover every shadowing path?
   - prefix: does stripping `command`/`builtin`/`exec` (and their option forms, e.g.
     `command -p`) and re-classifying the operand catch every prefix form?
   If any class leaves an admissible-looking word that still resolves to an emitter, name the
   class and the gap IN WORDS — do not write the shell. That is a Pattern-12 residual finding.
3. Confirm the r12 doc overclaim is now narrowed to the true property.
4. 13 defect patterns. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK.

Write ONE new file: `RP6_CODEX_T0_AUDIT_R13_2026-08-11.md`.
