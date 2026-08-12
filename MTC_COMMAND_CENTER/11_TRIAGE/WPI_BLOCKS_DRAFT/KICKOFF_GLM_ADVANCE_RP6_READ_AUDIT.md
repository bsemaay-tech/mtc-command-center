# KICKOFF — GLM-5.2 ADVANCE read-audit: RP6-P0 census, with RP6-11 as the priority target

You are GLM-5.2 via the Z.AI route. **You are running UNATTENDED — do not ask for approval, do
not write a plan and stop. Execute directly and write your verdict file.** Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. Read-only: create nothing except your verdict file, no git
mutation, no host, no network.

## What this dispatch is, and honestly is not
This is an **ADVANCE, SUPPLEMENTAL read-audit**, not the second-flagship audit. RP6 holds a Codex
flagship acceptance (`RP6_CODEX_T0_AUDIT_R16`, PASS-WITH-NITS); the required second flagship is
Claude `claude-opus-5`, which runs tonight. **Your verdict cannot close that slot and must not
claim to.** Its value is timing: if you find something now, the repair starts hours earlier.
Write your verdict as `ADVANCE-SUPPLEMENTAL` in the verdict line itself.

Known constraint from today: unattended GLM dispatches on this host are execution-gated. If you
cannot run a harness, **do not fabricate a green run** — mark those steps
`PENDING-LEAD-EXECUTION` and make your opinion source-level. A source-level adversarial read is
exactly what is wanted here.

## Bytes
`WPI_BLOCKS_DRAFT/RP6-P0.sh` — UNCHANGED since round 10a: 110817 B, SHA-256
`5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330`. Re-derive and confirm.
Evidence: `SELF_QA_RP6.md` §ROUND 16, `STATUS_RP6_P0.md`, `RP6_R16_REPORT_2026-08-11.md`,
and the Codex audit chain `RP6_CODEX_T0_AUDIT_R15/R16`.

## PRIORITY TARGET — RP6-11, the one open D026 gap in the whole current cycle
`AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md` row **RP6-11**: the
round-15 audit (F3) named a **dynamically-resolved inventory-mutation target** — an admitted
variable-mutating builtin whose target is resolved at runtime and contains no literal protected
inventory name — and **no executed RED/GREEN pair was ever located for it.** Round 16 reports
only the clean-byte structural assertion `inventory_variable_targets … dynamic_targets=0`, and
its `R16_F1_RED` offers only the `inbody` and `spandecoy` closures.

**The question:** does the r16 exact-byte-span census actually CLOSE the dynamic-target class, or
does `dynamic_targets=0` merely report that the clean block happens to contain none? Read the
census implementation and decide by construction. Describe, in source terms, exactly what a
variable-mutating builtin with a runtime-resolved target would have to look like, then trace what
the census would do with it. If the census would refuse it (fail-closed), say so and show the
mechanism. If it would report zero and pass, that is a finding at the same severity as the
r10→r15 evasion classes.

## The rest of the audit
1. Confirm the block identity and that no block byte changed r10a→r16 (the whole r10→r16 cycle
   was QA-layer).
2. Read the census structurally: it dispositions every function definition and every result
   producer by **exact source span** (line AND column); the wrapper exclusion is bound to
   DECLARED EXACT BYTES (`wrapper_definition_bytes_bound`); records at different spans are
   arithmetically incapable of comparing equal (`funcdef_census_reconciled`). Try to defeat that
   claim — encoding tricks, here-docs, eval-constructed producers, anything that survives
   byte-span disposition.
3. Adjudicate the Codex r16 NITS: are they honestly nits?
4. Verdict grammar: `PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK`, prefixed
   `ADVANCE-SUPPLEMENTAL`. State plainly what you executed and what you did not.

Write ONE new file: `RP6_GLM_ADVANCE_READ_AUDIT_2026-08-12.md` in `WPI_BLOCKS_DRAFT`.
