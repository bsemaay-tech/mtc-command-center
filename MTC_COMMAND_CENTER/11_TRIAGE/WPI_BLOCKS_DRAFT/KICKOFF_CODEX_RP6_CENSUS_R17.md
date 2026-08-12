# KICKOFF — Codex: RP6 census round 17, close the dynamic-target class (RP6-11)

You are Codex `gpt-5.6-sol` xhigh, IMPLEMENTER. Working dir `C:\LAB\Tradingview_LAB_CLEAN`.
No host, no network, no commit. Scope fence: touch ONLY `SELF_QA_RP6.md` (the §ROUND 17 section
you add), `STATUS_RP6_P0.md`, and a new `RP6_R17_REPORT_2026-08-12.md`.

**`RP6-P0.sh` MUST NOT CHANGE — not one byte.** Expected identity, re-derive and confirm before
and after: 110817 B, SHA-256
`5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330`. This is a QA/census-layer
round exactly like r10→r16. Do not touch RP7, the transport set, `composite_pathproof.py`,
`pathscope_prover.py`, or prereg drafts. Never git checkout/reset/stash any tracked file.

**Auditor routing:** you implement, so a DIFFERENT model audits — Claude Pro `claude-opus-5`
xhigh tonight. Write for that reader. Do not assume your own r16 audit's conclusions carry.

## The finding (RP6-11) — confirmed three ways
Raised as the sole OPEN row in `AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md`
(the r15 F3 dynamic-target class never got an executed RED/GREEN pair), answered by construction
in `RP6_GLM_ADVANCE_READ_AUDIT_2026-08-12.md`, and **independently confirmed by the Lead's direct
source read**:

1. `vartarget()` (`SELF_QA_RP6.md:16498-16524`) is genuinely fail-closed — a target that is not a
   bare literal identifier is UNMODELED — **but it is only reached for the enumerated builtins**
   at `:16453-16455` (`declare typeset local readonly export read mapfile readarray getopts unset
   let`) plus `printf -v` at `:16434`.
2. **`eval` is admissible as a bare command word** (`admissible_bare.txt`, `:16684`) and is **not**
   in that enumerated set. So an `eval` whose assignment target is resolved at runtime reaches
   `vartarget()` never: no `VARTARGET` record, no `UNMODELED`, and the lexical
   `p0_r16_name_misuse` check (`:16777-16787`) is defeated as soon as the inventory name is not a
   literal (e.g. built by concatenation). GLM traced a two-line mutant through every assertion and
   the fence certifies it CLOSED/CLEAN.
3. `dynamic_targets=0` at `:17571` is a **hardcoded string literal** in the pass format, sitting
   beside a genuinely measured `variable_targets=$n_vt`. It asserts "no enumerated-builtin target
   named an inventory var", not "zero dynamic targets exist". A reader is entitled to read it as
   a measurement; it is not one.

**Not a live defect:** the shipped clean block uses no `eval` and its arithmetic uses literal
lvalues. This is a census-completeness gap, and it is the same shape as every r10→r15 residual.

## Required repair — invert, do not enumerate
The r10→r16 lesson is explicit in `STATUS_RP6_P0.md`: the regress ended when the census stopped
patching classes and moved to a fail-closed structural construction. **Do not simply add `eval` to
the enumerated list** — that is one more class, and the next admissible construct that can mutate
a variable through a non-literal target (a function wrapper, `source` of a constructed string,
`builtin`, `command`, a future addition to the admissible set) reopens it.

Required properties:

1. **Fail-closed on the whole class.** Any admissible construct capable of mutating a variable
   whose target this fence cannot resolve to a bare literal identifier must produce an explicit
   `UNMODELED` record and refuse — not silence. State precisely how you decide "capable of
   mutating a variable" and why that decision is itself closed rather than another enumeration.
   If the honest construction is "any admissible bare word that is not in a proven-inert set is
   UNMODELED unless its full argument grammar is modelled", say so and build that.
2. **`dynamic_targets` becomes a MEASURED count**, derived like `variable_targets`. Every literal
   zero in that pass line must either become a real measurement or be deleted. Audit the whole
   pass format for other hardcoded values presented as measurements and fix every one you find —
   report the count.
3. **Conserve every r16 property.** The exact-byte-span disposition, `wrapper_definition_bytes_bound`,
   `funcdef_census_reconciled` and all carried r10→r15 mutants must still pass unchanged.

## D026 evidence (required)
- **RED under r16:** GLM's constructed mutant class — a variable-mutating `eval` with a
  runtime-resolved target that names a protected inventory variable non-literally. Show the r16
  fence certifying it CLEAN (that is the finding, executed rather than traced).
- **GREEN under r17:** the same mutant refused with an explicit `UNMODELED`/STOP record.
- At least one **second, structurally different** member of the class (not another `eval`
  spelling) also RED under r16 and GREEN under r17 — this is what distinguishes a class closure
  from an `eval` patch.
- Re-run `R16_GRAMMAR`'s full carried mutant set (the Lead's r16 run was 50/50) and report the
  r17 counts; no previously-killed mutant may survive.

## Deliverables
`SELF_QA_RP6.md` §ROUND 17 (evidence + the published fence, runnable verbatim by the Lead),
`STATUS_RP6_P0.md` (r17 section; state plainly that the r16 Codex acceptance was scoped to
constructs in the detection vocabulary and that this round closes the class it disclosed),
`RP6_R17_REPORT_2026-08-12.md`. Re-derive `RP6-P0.sh` identity and confirm it is UNCHANGED.
No commit — the Lead commits and runs the published fence verbatim before dispatching the audit.

If you conclude the class **cannot** be closed by construction at this layer, say so plainly with
the reason — the Lead will then take an accept-with-disclosure recommendation to the owner rather
than open round 18, exactly as SEC102 was handled today.
