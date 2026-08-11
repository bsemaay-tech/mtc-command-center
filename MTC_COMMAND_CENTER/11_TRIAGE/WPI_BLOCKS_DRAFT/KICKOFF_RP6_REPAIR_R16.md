# KICKOFF — RP6-P0 round 16: exact-byte-span census (the structural fixpoint, ends the line-granularity regress)

You are `claude-opus-5` xhigh via the Max account, IMPLEMENTER. Codex audits r16 (policy-read).
Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host, no network, no commit. UNIX LF, zero CR.
Never `git checkout` a block file — use `git cat-file blob <sha>:<path>`. Scope fence: touch
ONLY `SELF_QA_RP6.md`, `STATUS_RP6_P0.md`, the new report (RP6-P0.sh is UNCHANGED/sound — census
is QA-layer). Concurrent Max lane owns SEC102/prereg — do NOT touch. Never git
checkout/reset/stash any tracked file.

## Input — commit `2fdcdc5e`. `RP6-P0.sh` UNCHANGED `5132bacd…`.

## WHY r16 is a structural restructure, not another patch
The census has now taken r10→r15 closing evasion classes ONE AT A TIME, and Codex keeps finding
a subtler one. The ROOT CAUSE, made explicit by the r15 audit, is that the census works at
PHYSICAL-LINE granularity: it excludes whole wrapper lines and keys definition/emitter identity
on `(line, form, name)`. That loses column/byte information, so (F1) an additional emitter inside
a one-line wrapper body and (F2) a same-line decoy with matching `(line,form,name)` both slip
through. Patching each line-granularity symptom invites the next. r16 ends the regress by moving
the census to EXACT-BYTE-SPAN granularity — the same fail-closed-by-construction move that closed
the SEC102 command-word regress via a whitelist.

## Required repair — exact-byte-span census (close F1 + F2 + the whole line-granularity class)
1. **Bind each wrapper's exact body.** For every declared wrapper, capture its EXACT expected
   byte span (start offset, end offset, and the exact bytes) and assert the block's bytes at that
   span equal the one declared result producer — nothing else on the line, nothing extra inside
   the body. Any additional emitter or result producer within the wrapper region is a mismatch,
   not an excluded line.
2. **Disposition every result producer by exact source span, not by line.** Replace line-keyed
   identity/exclusion with byte-offset (or line+column) source spans, so two records at different
   positions never compare equal. A raw candidate and a tokenizer record reconcile ONLY when their
   source spans coincide — a same-line decoy at a position the raw scanner misses can no longer
   cancel a real definition.
3. **Fail closed on any span the census cannot resolve** (ambiguous quoting/comment/command-
   position state at byte level) → UNMODELED, never silently excluded.
Keep every carried assertion; do not weaken a fence without a per-change discriminating-power
proof (old + new assertion executed on the same deviant output, both quoted).

## Deliverables
Repaired `SELF_QA_RP6.md` (census restructured to exact-byte-span) + `STATUS_RP6_P0.md` (narrow
the property to the true span-level fail-closed claim; re-state residuals) +
`RP6_R16_REPORT_2026-08-11.md`. Publish + execute D026 RED/GREEN for BOTH residual classes:
(F1) an additional emitter INSIDE a one-line wrapper body — current census silently passes,
repaired census fails nonzero; (F2) a same-line decoy matching `(line,form,name)` — current
census's multiset compares equal, repaired span-based census fails nonzero. Plus the carried
R15 mutants still killed. Because the harnesses are slow, if your session runs low on time,
finish the FENCES and the report and mark the transcript paste `PENDING-LEAD-EXECUTION` — the
Lead runs the published fences verbatim as the evidence of record; do NOT fabricate transcripts.
No commit — the Lead commits.
