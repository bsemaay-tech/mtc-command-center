# KICKOFF — Claude Pro T0 audit: RP6-P0.sh + r16 census, SECOND FLAGSHIP (dual-acceptance gate)

You are `claude-opus-5` xhigh via the default Claude Pro account, AUDITOR — the second
flagship. Codex `gpt-5.6-sol` closed its flagship slot on these bytes
(`RP6_CODEX_T0_AUDIT_R16`, PASS-WITH-NITS: the exact-byte-span census is a FAIL-CLOSED
FIXPOINT; the r10→r16 census regress is over). Claude MAX implemented rounds 10–16, so YOU
(a fresh Claude Pro session that implemented nothing on this block) are the required
independent second flagship. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. Read-only on the
repo: edit nothing except your verdict file, no git mutation, no remote host, no network.
Local execution of the published QA harness is permitted.

## Bytes under audit
`RP6-P0.sh` — UNCHANGED since r10a: 110817 B, SHA-256
`5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330`. Re-derive and confirm
this identity first. The audited work is the census QA harness in `SELF_QA_RP6.md`
(§ROUND 16) proving the block's result-grammar admits no smuggled emitter. Start from
`STATUS_RP6_P0.md`, then the r16 report and the Codex r16 verdict. Verify against bytes.

## What the census now claims (your target)
Every function definition and every result producer is dispositioned by its EXACT SOURCE
SPAN (line AND column); the wrapper exclusion is bound to DECLARED EXACT BYTES
(`wrapper_definition_bytes_bound` — each declared line occurs exactly once byte-for-byte,
carries exactly ONE result producer, is the only definition of that wrapper); two records
at different spans are arithmetically incapable of comparing equal
(`funcdef_census_reconciled` with column recorded). The r10→r16 classes closed:
cmdquote/expand/continuation, alias/function/tool-shadow/prefix, function-def shapes,
empty inventory/definition-identity, append-assign, intra-body emitter + same-line decoy.

## THE SUBJECT IS NOW ROUND 17, NOT ROUND 16 — read this first
Since this kickoff was first written, RP6 advanced to **round 17** (commit `671d9b40`). Audit the
**r17** bytes. `RP6-P0.sh` is still byte-identical (110817 B, `5132bacd…`) — r17 is a QA/census
round like r10→r16.

**Why r17 exists, including a correction you should scrutinise.** The D026 consolidation map
flagged row **RP6-11** — the r15 F3 dynamically-resolved inventory-mutation class never got an
executed RED/GREEN pair. A GLM advance read-audit then claimed the r16 fence *admits* a
variable-mutating `eval` and certifies it CLEAN. **That claim was false** and Codex said so in
its own r17 report: the checked-in fence already refuses `eval`, `source` and `.` as
`UNMODELED kind=indirect_execution_builtin:*` (`SELF_QA_RP6.md:16763-16765`). The Lead's own
intermediate confirmation was partial and is corrected in the blocker map.

What *was* real: `dynamic_targets=0` at `:17571` was a **hardcoded literal presented as a
measurement**, beside a genuinely measured `variable_targets=$n_vt`; r17's pass-format audit
found six such literal-zero fields across three r16 success lines.

**Your first-class questions:**
1. **Is the correction itself correct?** Verify independently that the r16 fence really does
   refuse `eval`/`source`/`.`, and that no *other* admissible construct can mutate a variable
   through a target the fence cannot resolve. Two models have now disagreed about this file; you
   are the tiebreaker with execution available.
2. **Is r17's effect model genuinely closed, or is it another enumeration in disguise?** It
   claims a bare command word is accepted only if it is a span-dispositioned block function,
   `rp0_require_safe_component`, a builtin with no named-variable target surface, or a
   variable-mutating builtin with modelled target grammar — everything else being an opaque
   execution surface that fails. Try to find an admissible word that slips between those cases.
3. **Is the weakened-r16 RED honest?** r17 could not produce a RED against the shipped fence
   (it already refuses these), so it removed *only* the indirect-execution refusal from a
   temporary extracted fence. Judge whether that is a legitimate D026 equivalent or whether it
   proves less than it appears to.
4. **Are all six literal-zero fields really gone?** `r17_literal_zero_measurements=0` is itself a
   claim — check it, and sweep for any other value presented as a measurement that is not one.

## Audit contract
1. Confirm the block identity (size + SHA-256) and that no block byte changed r10a→r16.
2. Run **`R17_DYNAMIC_TARGETS`** VERBATIM (published command in
   `RP6_R17_REPORT_2026-08-12.md`); the Lead's run was `cases=15 pass=15 fail=0`, outer rc 0,
   with the carried r16 grammar `50/50` inside it and block identity unchanged. Record real
   counts. Also run `R16_GRAMMAR` itself if you want the r16 baseline independently.
2b. Resolve the four questions above, with executed evidence either way.
3. Adversarially seek a census evasion the fixpoint still admits — you are auditing the
   claim that exact-byte-span granularity is STRUCTURALLY closed, not one more class. If
   you find a hiding place (encoding tricks, here-docs, eval-constructed producers,
   anything that survives byte-span disposition), that is the finding.
4. Adjudicate the Codex r16 NITS: are they honestly nits?
5. Thirteen-pattern adjudication table. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES /
   BLOCK. If accepting, state that RP6 reaches DUAL FLAGSHIP ACCEPTANCE.

Write ONE new file: `RP6_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md` (this directory).
Prove `git status --porcelain` shows only that file at the end.
