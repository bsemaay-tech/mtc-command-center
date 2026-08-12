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

## SECOND PRIORITY TARGET — unresolved evidence placeholders, and a report that says otherwise
A round-report claim audit (`WPI_ROUND_REPORT_CLAIM_AUDIT_2026-08-12.md`) found that the **r16
report states the evidence placeholders were resolved, while the files still contain them.**
**EIGHT** unresolved placeholder slots survive in `SELF_QA_RP6.md`, plus one in the status file.
*(The Lead's first grep reported three — the pattern omitted digits and missed five. Corrected
against a full-document audit that read all 18,799 lines and checked 1,863 output lines.)*

- `:15341` — `@@R15_GRAMMAR_TRANSCRIPT@@`
- `:15651` — `@@R15_F1_RED_TRANSCRIPT@@`
- `:15763` — `@@R11_GUARDS_TRANSCRIPT@@`
- `:15807` — `@@RERUN_BLOCK@@`
- `:18241` — `@@R16_GRAMMAR_TRANSCRIPT@@`
- `:18524` — `@@R16_F1_RED_TRANSCRIPT@@`
- `:18645` — `@@R11_GUARDS_TRANSCRIPT@@`
- `:18690` — `@@RERUN_BLOCK@@`
- `STATUS_RP6_P0.md:284` — `@@STATUS_EXEC_BLOCK@@`

(Other `@@…@@` occurrences are prose *describing* the placeholders — do not count those.)

**These are not peripheral slots.** They are the transcripts for the round-15 closure, the
**round-16 discriminating-power proof**, the guard census, and the mandated rerun vector — i.e.
the document-local execution support for the very fixpoint claim you are auditing. Meanwhile
`:13492-13505` and `:15995-16000` state that these transcripts are real captured output and that
the placeholders were resolved.

**Important counterweight — the evidence exists, just not in this document.** The Lead ran
`R16_GRAMMAR` verbatim (50/50) and `R17_DYNAMIC_TARGETS` verbatim (15/15, carried r16 grammar
50/50) from outside the repo, and the Codex r16 audit independently reproduced its run. So the
question is not "was this ever proven" but "does the self-QA document carry its own proof".

These are positions where a transcript should be pasted and **nothing is**. The GLM advance
read-audit characterised them as recovered-session artefacts and "a LOW documentary nit"; the
round-report audit says the r16 report claims they were resolved. Both cannot be right.

**What the Lead needs from you:** decide whether these are cosmetic or load-bearing. Specifically —
does any acceptance claim in the r16/r17 chain depend on evidence that should have been pasted at
those three positions? If yes, that evidence does not exist in the record and a gate is
unsupported. If no, this is a documentation repair and should be stated as one rather than left
as a contradiction between the report and the files.

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
