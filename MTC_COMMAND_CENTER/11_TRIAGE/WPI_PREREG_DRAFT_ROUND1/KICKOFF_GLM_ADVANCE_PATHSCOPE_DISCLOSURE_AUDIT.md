# KICKOFF — GLM-5.2 ADVANCE audit: pathscope prover, the DISCLOSURE-HONESTY question

You are GLM-5.2 via the Z.AI route. **You are running UNATTENDED — do not ask for approval, do
not write a plan and stop. Execute directly and write your verdict file.** Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. Read-only: create nothing except your verdict file, no git
mutation, no host, no network.

## Read this framing carefully — this is NOT a repeat of your earlier read
You already produced a favorable read-audit of `pathscope_prover.py` r2
(`PATHSCOPE_GLM_T1_AUDIT_R2_2026-08-11.md`). **Do not re-run that analysis.** It was marked
SUPPLEMENTAL because you could not execute the suite, and the outstanding gap is an EXECUTION
audit — Claude Pro runs that tonight. Codex remains filter-blocked on this source (its provider
filter terminates while merely reading the attack-grammar tables), so it cannot cover it either.

This dispatch targets the one question a read CAN settle, which tonight's executing auditor will
have less time for: **are the disclosures honest, or does any of them function as a disguised
control?** That distinction is the single most load-bearing idea in this whole work package, and
today it went both ways — SEC102's residuals were judged honest, while an RP6 census line was
found to be a hardcoded literal presented as a measurement.

Prefix your verdict `ADVANCE-SUPPLEMENTAL`. Never fabricate a green run; mark any execution step
`PENDING-LEAD-EXECUTION`.

## Bytes
`WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py` — 122446 B, SHA-256
`890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d`. Re-derive and confirm.
Context: `SELF_QA_PATHSCOPE.md`, `STATUS_PATHSCOPE.md`, `PATHSCOPE_REPAIR_R2_REPORT.md`, the
round-1 Codex findings, and your own earlier read-audit.

## The seven disclosed residuals — adjudicate each one individually
Per `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md`, pathscope carries seven: **R1** lexical-vs-host
binding; **R2** function positional dataflow; **R3** alias expansion; **R4** deliberate
conservative over-reporting; **R5** inline-option provenance attribution; **R6** finite
registry / lower-bound resolved set on STOP; **R7** renamed output fields for downstream
consumers.

For each, answer in the verdict file:
1. **What exactly does the tool NOT do**, in source terms with a `file:line`?
2. **Is the published wording an honestly-scoped weaker claim, or does it read as coverage?**
   Quote the actual sentence. A disclosure that a reader could reasonably take as a control is a
   finding, not a nit.
3. **Does any output line present the residual as a measurement, a check, or a pass?** This is
   the specific failure mode found in RP6 today: `dynamic_targets=0` was a hardcoded literal
   sitting beside a genuinely measured field. **Sweep every emitted line of this prover for the
   same shape** — a constant, a default, or a not-established value formatted so it looks
   measured. Report the count you checked, not just what you found.
4. **Can the residual be reached silently?** i.e. is there an input for which the residual
   applies but no `UNRESOLVED` / `ALLOW-LEXICAL` / coverage record is emitted? A silent residual
   is a CRITICAL, not a disclosure.

## Specific target — finding 6
Round 2 repaired finding 6 as a DISCLOSURE: `ALLOW-LEXICAL` plus
`symlink_resolution=not_established mount_boundary=not_established`, with residual R1. The
question the Lead needs settled: **does any run still present lexical membership as an
unconditional host ALLOW?** Trace the emit paths, not the documentation.

## Verdict
Grammar: `PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK`, prefixed `ADVANCE-SUPPLEMENTAL`.
State plainly what you executed and what you did not. If every disclosure is honest, say so
clearly — a clean answer here is genuinely useful, not a non-result.

Write ONE new file: `PATHSCOPE_GLM_ADVANCE_DISCLOSURE_AUDIT_2026-08-12.md` in
`WPI_PREREG_DRAFT_ROUND1`.
