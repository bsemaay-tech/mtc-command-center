# KICKOFF — Codex T0 audit: RP6-P0 round 14 (policy-read, NO mutant construction)

Date: 2026-08-11. Codex `gpt-5.6-sol` xhigh, AUDITOR of record, fresh session. Read-only:
edit nothing except your verdict file, no git mutation, no host, no network. T0.

## Policy-read only (your r12 audit filter-tripped twice on constructed evasion shell; the
no-construction run cleared it). Run ONLY the already-published harnesses (they extract their
own mutants from their own heredocs) and reason by construct CLASS. Do NOT author/echo/execute
any new emitter mutant. Refer to classes by name. Quote only summary/`ASSERT_MET`/`killed_by=`/
`UNDEFINED_EMPTY_INVENTORY` lines. Verdict first.

## Bytes — commit `0f6b3ec9`. `RP6-P0.sh` UNCHANGED `5132bacd…` (census is QA-layer).

## Your r13 findings (REQUEST_CHANGES ×3, Pattern 12/13)
F1 function-definition recognition incomplete (a form the FUNCDEF inventory misses can shadow a
builtin emitter/prefix name). F2 tool-shadow coverage can become empty without failing closed.
F3 alias absence checked lexically not semantically.

## Round-14 dispositions (Lead ran R14_GRAMMAR VERBATIM, 38/38 rc 0)
- F1: tokenizer models both definition shapes (`form=paren`/`form=keyword`), refuses unreadable
  declarators + nameless `function`, binds the three prefix words (`prefix_shadow`); assertion 16
  requires a raw line census and the FUNCDEF set to name the SAME lines via `cmp` (exactly one
  disposition per definition). Mutants killed: `funckw`, `prefixkw`.
- F2: assertion 17 conservation chain binds declared tool inventory ↔ extracted names ↔ runtime
  handles; the `n_sht=0` branch is GONE — empty now reads `UNDEFINED_EMPTY_INVENTORY` and fails
  closed. Mutants killed: `invpartial` (inventory_half_unextracted), `invempty`.
- F3: alias refused semantically (the `alias` builtin classified at the command position bash
  resolves, through prefix strip + inside command substitutions) + a fail-closed `shopt` operand
  grammar (any expansion/escape operand is UNMODELED). Mutants killed: `aliasopt`, `aliasdef`.
  The lexical check is carried unchanged and runs first.
- `R14_F1_RED` 57/57; `R11_GUARDS` 19→21/21; RP6-P0.sh untouched.

## Audit contract (execution + reading only, NO construction)
1. Run the published `R14_GRAMMAR`, `R14_F1_RED`, `R11_GUARDS`, `R10_F4`, `R11_R9RED` VERBATIM
   (output to files; report only summaries). Confirm the funckw/prefixkw/aliasopt/aliasdef/
   invpartial/invempty mutants are killed and empty inventory → `UNDEFINED_EMPTY_INVENTORY`.
2. **Policy-soundness READ (no examples):** the r13→r14 principle was "fail closed on any
   unmodeled function-def / tool-inventory / alias syntax." For EACH extractor (FUNCDEF, tool
   inventory, alias/shopt), decide whether it is now genuinely fail-closed: does assertion 16's
   `cmp` catch every raw definition the FUNCDEF set misses? Does the conservation chain (assertion
   17) fail closed on partial/empty/duplicate/unrecognized inventory shape? Does the alias
   semantic check + UNMODELED shopt grammar cover every alias-introduction path? If any extractor
   can still silently miss a construct already in the detection vocabulary, name the extractor and
   the class IN WORDS — do not write shell. That is a residual finding.
3. Confirm the r13 property overclaims are now narrowed to the true fail-closed property.
4. 13 patterns. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK. If you find no residual,
   note this closes the RP6 census hardening cycle (r10→r14) and the Codex flagship slot.

Write ONE new file: `RP6_CODEX_T0_AUDIT_R14_2026-08-11.md`.
