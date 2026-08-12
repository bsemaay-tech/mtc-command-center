# KICKOFF — Codex T0 audit: RP6-P0 round 16 (policy-read, NO mutant construction)

Date: 2026-08-12. Codex `gpt-5.6-sol` xhigh, AUDITOR of record, fresh session. Read-only:
edit nothing except your verdict file, no git mutation, no host, no network. T0.

## Policy-read only (constructed evasion shell trips the filter). Run ONLY the published
harnesses; reason by class. Do NOT author/echo/execute a new emitter mutant. Quote only
summary/`ASSERT_MET`/`killed_by=`/`funcdef_census_reconciled`/`wrapper_definition_bytes_bound`
lines. Verdict first.

## Bytes — commit `753894ba`. `RP6-P0.sh` UNCHANGED `5132bacd…` (census is QA-layer).

## Your r15 findings (REQUEST_CHANGES ×2, Pattern 12/13)
The census was LINE-granular: F1 an intra-body additional emitter in a one-line wrapper was
line-excluded (assertion 18 only covered after-closing-brace); F2 `(line,form,name)` identity
permitted correlated same-line decoy cancellation. Root cause: line granularity loses column/
byte information.

## Round-16 disposition — the EXACT-BYTE-SPAN structural fixpoint (Lead ran R16_GRAMMAR
VERBATIM, 50/50 rc 0)
The census is restructured to byte/span granularity:
- **F1:** each declared wrapper's EXACT expected body bytes are bound (`wrapper_definition_bytes_bound`);
  any additional emitter/result-producer within the wrapper region is a mismatch, not an
  excluded line. Mutant `wrapline` killed by
  `wrapper_definition_bytes_bound(...occurrences(0))` + `census_covers_every_emitter(164!=165)`.
- **F2:** identity/exclusion is keyed on source SPAN (column recorded), so records at different
  positions never compare equal. Mutant `spandecoy` killed by
  `funcdef_census_reconciled(raw=27,tok=27)`.
- All carried r10→r15 mutants still killed.
- NOTE: r16 was recovered after a process exit; its report was written pre-exit and the Lead's
  verbatim R16_GRAMMAR run (50/50) is the evidence of record. Confirm by re-running.

## Audit contract (execution + reading only, NO construction)
1. Run the published `R16_GRAMMAR`, `R16_F1_RED`, `R11_GUARDS`, `R10_F4`, `R11_R9RED` VERBATIM
   (output to files; report only summaries). Confirm wrapline + spandecoy killed and the census
   reconciles by SPAN (column), not line number, and binds each wrapper's exact body bytes.
2. **Policy-soundness READ (no examples) — is this the fixpoint?** The r10→r16 arc moved the
   census from line-granularity to exact-byte-span. Decide: can ANY construct already in the
   detection vocabulary still be lost — i.e. is there a wrapper region whose exact bytes are not
   bound, a producer whose source span the span-census cannot resolve (and does that case fail
   closed as UNMODELED rather than silently pass), or a decoy/real pair the span identity still
   conflates? If none, the RP6 census hardening cycle (r10→r16) is a fail-closed fixpoint and the
   Codex flagship slot closes. If one exists, name the class IN WORDS (no shell).
3. Confirm the property claims are narrowed to the true span-level fail-closed property.
4. 13 patterns. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK.

Write ONE new file: `RP6_CODEX_T0_AUDIT_R16_2026-08-12.md`.
