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

## PRIORITY TARGET — one open D026 gap the Lead found after this kickoff was written
`AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md` row **RP6-11** is the
single OPEN freeze-relevant finding in the whole current cycle: the round-15 audit (F3) named a
**dynamically-resolved inventory-mutation target** — an admitted variable-mutating builtin whose
target is resolved at runtime and contains no literal protected inventory name — and **no
executed RED/GREEN pair was ever located for it.** Round 16 reports only the clean-byte
structural assertion `inventory_variable_targets … dynamic_targets=0`, and `R16_F1_RED` offers
only the `inbody` and `spandecoy` closures. So the claim rests on an assertion over clean bytes,
not on a demonstrated falsification.

**Make this your first-class question:** does the r16 exact-byte-span census actually close the
dynamic-target class, or does `dynamic_targets=0` merely report that the clean block happens to
contain none? Construct the missing RED — a harmless variable-mutating builtin whose target
resolves at runtime to a protected inventory name — and determine whether the census catches it
or silently reports zero. If it is caught, say so and the row closes. If it is not, that is a
finding at the same level as the r10→r15 evasion classes.

## Audit contract
1. Confirm the block identity (size + SHA-256) and that no block byte changed r10a→r16.
2. Run `R16_GRAMMAR` VERBATIM — the Lead's run was 50/50 (wrapline + spandecoy killed, all
   r15 mutants carried). Record real counts.
2b. Resolve **RP6-11** above, with executed evidence either way.
3. Adversarially seek a census evasion the fixpoint still admits — you are auditing the
   claim that exact-byte-span granularity is STRUCTURALLY closed, not one more class. If
   you find a hiding place (encoding tricks, here-docs, eval-constructed producers,
   anything that survives byte-span disposition), that is the finding.
4. Adjudicate the Codex r16 NITS: are they honestly nits?
5. Thirteen-pattern adjudication table. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES /
   BLOCK. If accepting, state that RP6 reaches DUAL FLAGSHIP ACCEPTANCE.

Write ONE new file: `RP6_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md` (this directory).
Prove `git status --porcelain` shows only that file at the end.
