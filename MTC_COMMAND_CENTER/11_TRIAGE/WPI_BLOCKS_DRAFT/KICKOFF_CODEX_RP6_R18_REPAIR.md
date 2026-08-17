# KICKOFF — RP6 round-18 repair (Codex implementer)

Tier T0 implementer round. Model `gpt-5.6-sol` (Codex `fourth`), effort xhigh. Dispatched by the
Lead 2026-08-12 ~22:05 after the fresh Codex r17 audit returned REQUEST_CHANGES. **No git
mutation. The block `RP6-P0.sh` must remain byte-identical: 110817 B, SHA-256
`5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330` — this is harness/evidence
work only, like every round since r11.**

## Input — read first

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_CODEX_T0_AUDIT_R17_2026-08-12.md` (16843 B).
Its four "Minimum required repairs" are the work order. The Lead has independently verified F1's
premises (`wait` admitted in the allow-list; absent from the vartarget dispatch at the
`declare/typeset/.../let` branch) and the r10→r11 blob change (107252 B `3c7b7d26` → 110817 B
`4729b8fa`).

## The four required repairs — binding, from the verdict

1. **F1 — fail-closed assigning-option grammar.** `wait -p` and every other assigning option
   reachable from the admitted builtin set must enter a fail-closed target grammar. Audit the
   full admitted non-function bare-word list for assigning options (`printf -v` class included if
   admitted) — do not merely add the one spelling found. Add an executed RED against the
   delivered r17 bytes (or an equivalent deliberate mutation, explicitly labelled) and GREEN
   after repair, with real commands and summary output. **This is the structural-inversion
   round: the effect model must refuse what it does not model, not enumerate what it fears.**
2. Replace the self-certifying pass-format assertion (`SELF_QA_RP6.md:13417-13419` region) with
   a real measured scan: publish the derived count, and make the assertion fail when a new
   uncomputed result field appears.
3. Resolve the eleven transcript contradictions (eight SELF_QA slots, `STATUS_RP6_P0.md:299`,
   `RP6_R15_REPORT_2026-08-11.md:180`, `RP6_R16_REPORT_2026-08-11.md:277`): paste exact
   provenance-backed output where it exists, or truthfully mark the local evidence absent and
   cite the external execution record. **Never invent or reconstruct output.** The two round
   reports are historical — for those two, prefer the truthful-absence marker over editing
   history into them.
4. Narrow the `SELF_QA_RP6.md:5-7` every-fence/no-temp sentence to what is true; label
   whole-session negatives as author attestations; correct the block stability boundary from
   r10a to **r11** wherever the RP6 lane files state it.

## Rule 8 boundary — binding

r17 was already billed as the inversion and reopened. If while implementing the fail-closed
grammar you find the property still cannot close structurally (another class survives that the
grammar cannot refuse without unbounded enumeration), **STOP: do not iterate**. Write an honest
accept-with-disclosure recommendation in your report instead, naming the residual class. The
boundary decision belongs to the owner.

## Files you own (disjoint — no other lane touches these tonight)

1. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP6.md`
2. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md`
3. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_R15_REPORT_2026-08-11.md` (repair 3 marker only)
4. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_R16_REPORT_2026-08-11.md` (repair 3 marker only)
5. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_R18_REPORT_2026-08-12.md` (new — your round report)
6. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md` —
   repoint to r18 AFTER the repair is complete: new SELF_QA identity, r18 round references, the
   corrected `r11→r18` span, and the r17 REQUEST_CHANGES disclosed as a known prior verdict with
   its four findings listed as settled-or-not.

## Authoring rules (binding, Rule 9b)

1. No unfilled slot under a "resolved" claim — grep for `@@`, `PENDING`, empty fences before
   publishing.
2. Absolutes and numbers need pasted-line evidence or an explicit `External evidence:` label.
3. Re-derive every carried-forward identity from current bytes after your final edit; the round
   report must carry a current identity table (SELF_QA bytes+SHA, block bytes+SHA unchanged).

## Output hygiene (content-filter protection)

Work in narrow bands; redirect harness output to scratch files outside the repo; quote only
summary lines; symbolic fixture names; no large fixture bodies in the report.

## Report

`RP6_R18_REPORT_2026-08-12.md`: per-repair evidence with exact RED/GREEN summary lines, the
published exact command, the identity table, delta-gate proof (porcelain before/after, delta =
only your owned paths), and your session-header model/effort.
