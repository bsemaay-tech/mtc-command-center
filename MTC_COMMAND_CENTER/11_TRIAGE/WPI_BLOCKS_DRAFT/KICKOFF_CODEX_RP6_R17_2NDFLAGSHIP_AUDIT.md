# KICKOFF — Codex T0 audit of the RP6 round-17 evidence (current bytes)

Tier T0 audit. Model `gpt-5.6-sol` (Codex `fourth`), effort xhigh. Dispatched by the Lead
2026-08-12 ~21:45. Read-only except your verdict file. **No git mutation.**

## Why this audit exists

Your own r16 verdict (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_CODEX_T0_AUDIT_R16_2026-08-12.md`,
PASS-WITH-NITS) covered the unchanged block `RP6-P0.sh` and the **historical r16 evidence
document** (1024538 B, `897a5a4d…`). The evidence document has since moved to **round 17**
(`SELF_QA_RP6.md`, 1038848 B, SHA-256
`07cf843d5f00bef7f980017cbe01e0dc63ddb95dce5c7253d9e9a351b0d449ac`). **The r16 acceptance does
not carry to those bytes.** Dual flagship acceptance of RP6 requires a fresh `gpt-5.6-sol` xhigh
verdict on the r17 evidence AND a Claude `claude-opus-5` xhigh verdict on the same bytes. The
Claude lane runs tonight in parallel (verdict file disjoint from yours). You are the Codex half.

## Scope and contract — identical to the Claude lane's

Read `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md`
(post-correction bytes: 17558 B, SHA-256
`66ed271b6eda1d09a284592aee53e9a51d0712cfa7e6b87e86041d6ced3951ce`) and adopt its **entire audit
contract**: the target identities, the reading order, the disclosed known defects (the
dynamic-target class; the unpasted transcript placeholders; the r17 self-certifying literal whose
current count is indeterminate pending a measured scan; S-1 every-fence contradiction; U-4
author-attested negatives), the first-class questions, and the verbatim-run requirement. Ignore
only its Claude-specific dispatch mechanics (model flags, effort flags) and its verdict path.

Judge, do not rediscover: the known defects are disclosed so your verdict must settle whether
they change the acceptance, not re-find them.

## Differences from the Claude lane — binding

1. **Your verdict file (the ONLY file you may write):**
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_CODEX_T0_AUDIT_R17_2026-08-12.md`
2. **Delta gate adapted to that path:** capture `git status --porcelain` before you start, again
   after you finish, and prove the delta contains only your exact verdict path. Include both
   captures (or their diff) in the verdict.
3. **Output hygiene (content-filter protection, learned 2026-08-12):** work in narrow bands of
   the evidence document; redirect any harness output to a scratch file outside the repo and
   quote only summary lines; use symbolic names for fixture content; never paste large fixture
   bodies into your reasoning or verdict.
4. State your session-header model and effort in the verdict. If any published command must run,
   run it verbatim per the kickoff's contract and quote only the summary lines.

## Verdict form

PASS / PASS-WITH-NITS / REQUEST_CHANGES, with: the exact r17 evidence identity you audited
(re-derive bytes + SHA-256 yourself); per-known-defect adjudication; per-first-class-question
answer; any new findings with exact citations; the delta-gate proof; model/effort line.
