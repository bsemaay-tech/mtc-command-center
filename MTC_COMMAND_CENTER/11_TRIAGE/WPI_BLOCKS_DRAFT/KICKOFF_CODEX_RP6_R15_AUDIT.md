# KICKOFF — Codex T0 audit: RP6-P0 round 15 (policy-read, NO mutant construction)

Date: 2026-08-12. Codex `gpt-5.6-sol` xhigh, AUDITOR of record, fresh session. Read-only:
edit nothing except your verdict file, no git mutation, no host, no network. T0.

## Policy-read only (constructed evasion shell trips the filter). Run ONLY the published
harnesses (they extract their own mutants from their own heredocs) and reason by class. Do NOT
author/echo/execute any new emitter mutant. Quote only summary/`ASSERT_MET`/`killed_by=`/
`funcdef_census_reconciled`/`UNDEFINED_EMPTY_INVENTORY` lines. Verdict first.

## Bytes — commit `957ab798`. `RP6-P0.sh` UNCHANGED `5132bacd…` (census is QA-layer).

## Your r14 findings (REQUEST_CHANGES ×2, Pattern 12/13)
F1 the function-definition census was line-conserving not definition-conserving (cmp on line
numbers succeeds while the actual name differs — continuation-separated name / same-line
multiplicity). F2 the inventory conservation omitted append-style assignments and `sort -u`
collapsed duplicate composition.

## Round-15 dispositions (Lead ran R15_GRAMMAR VERBATIM, 44/44 rc 0)
- F1: each raw definition gets a STABLE IDENTITY (line+ordinal+form+normalized name), compared
  ONE-FOR-ONE without `uniq`; empty/quoted/expanded/escaped name tokens refused as UNMODELED.
  Mutants killed: `defcont` (killed_by=funcdef_census_reconciled raw=29,tok=28), `defmulti`
  (raw=27,tok=28).
- F2: append-style assignments get an inventory disposition; composition reconciled in ORDER
  with multiplicity (no `sort -u` collapse). Mutants killed: `invappend`
  (inventory_half_assignments), `invdup` (inventory_composition_unmodeled).
- A 3rd finding Max caught while sweeping: an undeclared emitter appended to a wrapper-definition
  line was invisible to the four line-based exclusions — closed as assertion 18; mutant
  `wrapline` killed (wrapper_definition_line_not_closed).
- The carried mutants (cmdquote/expand/continuation/alias/shadow/toolshadow/funckw/prefixkw/
  aliasopt/aliasdef/invpartial/invempty/handle) all still killed. `R15_F1_RED` (Lead: fences
  verified; slow behavioral RED demonstration).
- NOTE: the Max session ended mid-transcript-paste; the Lead's verbatim R15_GRAMMAR run (44/44)
  is the evidence of record. Confirm by re-running yourself.

## Audit contract (execution + reading only, NO construction)
1. Run the published `R15_GRAMMAR`, `R15_F1_RED`, `R11_GUARDS`, `R10_F4`, `R11_R9RED` VERBATIM
   (output to files; report only summaries). Confirm defcont/defmulti/invappend/invdup/wrapline
   killed and the funcdef census reconciles raw↔tokenizer by IDENTITY not line number.
2. **Policy-soundness READ (no examples):** is the census now DEFINITION-conserving and
   inventory-MULTISET-conserving? Does the stable-identity one-for-one comparison catch a
   definition whose name the tokenizer mis-dispositions while the raw line matches? Does the
   ordered-multiset inventory reconciliation fail closed on append / duplicate / unmodeled
   assignment shapes? Does assertion 18 close the wrapper-definition-line append class? If any
   extractor can STILL silently miss a construct already in the detection vocabulary, name the
   extractor and class IN WORDS. If none, the RP6 census hardening cycle (r10→r15) is a
   fail-closed fixpoint and the Codex flagship slot closes.
3. Confirm the property claims are narrowed to the true fail-closed property.
4. 13 patterns. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK.

Write ONE new file: `RP6_CODEX_T0_AUDIT_R15_2026-08-12.md`.
