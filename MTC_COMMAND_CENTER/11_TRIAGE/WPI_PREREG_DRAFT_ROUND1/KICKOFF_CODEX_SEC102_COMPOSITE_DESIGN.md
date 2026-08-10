# KICKOFF — design note: what the §10.2 Stage-1 proof must actually analyse

Fresh `gpt-5.6-sol` session, effort high. **Design analysis only** — reading, reasoning and
writing one document. Do not build fixtures, do not run the blocks, do not modify the
prover. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network, no commit.

## The problem

§10.2 requires Stage 1 to emit, per frozen block, the complete set of host paths that block
can reach, and to show every one inside the §10.1 allowlist. Two findings tonight show the
current design cannot deliver that:

1. The prover under-reports (`PATHSCOPE_CODEX_T1_AUDIT_2026-08-10.md`, REQUEST_CHANGES 9,
   four CRITICAL silent-sink classes). That is a soundness bug and has its own repair round.
2. **Even a sound prover cannot close either block from the block source alone.** RP6's
   unresolved set begins at the evidence-allocation boundary — `RUNID`, `EV_STAGE_ID`, and
   `rp0_require_safe_component` having no registered path-argument contract. The paths are
   produced by the composition of wrapper + RP0-LIB + RP0-BOOTSTRAP + block, not by the
   block in isolation. Evidence: `PATHSCOPE_LEAD_RERUN_2026-08-10.md`,
   `SEC101_RECONCILIATION_CODEX_2026-08-10.md` unresolved family 3.

This note is about problem 2. It is a design question, and getting it wrong means building
the wrong tool twice.

## Inputs (relative to `MTC_COMMAND_CENTER\11_TRIAGE\`)

1. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` §10.1 and §10.2 — quote §10.2's
   requirement verbatim; it is what any design must satisfy.
2. `WPI_PREREG_DRAFT_ROUND1/SEC101_RECONCILIATION_CODEX_2026-08-10.md` — the 20 bounded
   families and 3 unresolved families.
3. `WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_CODEX_T1_AUDIT_2026-08-10.md` — what a sound analyzer
   must do.
4. `WPI_BLOCKS_DRAFT/RP6-P0.sh`, `RP7-WPI-RO.sh`, `run_p0.sh`, `run_ro.sh` — the block and
   wrapper halves of the composition.
5. The RP0-LIB and RP0-BOOTSTRAP sources the wrappers depend on. **Locate them yourself and
   record their exact paths, byte counts and SHA-256** — establishing what the composite
   input actually consists of is part of the deliverable, and if a component cannot be
   located, say so plainly rather than assuming.

## Questions to answer

1. **What exactly is the composite input?** Enumerate every file whose text can affect a
   path the run reaches, in load order, with the mechanism by which each contributes
   (sourced, exec'd, passed as argv, exported as environment).
2. **Where does each currently-unresolved value become determinate?** For `RUNID`,
   `EV_STAGE_ID`, `EV_DIR`, `EV_LOG`, `REMOTE_BASE` and the tool pins: is it a frozen
   constant, a Stage-1 fill, a dispatch-time allocation, or genuinely runtime? Say which,
   per value. A value that is only determinate at runtime cannot be proved statically, and
   that must be stated rather than engineered around.
3. **What is the smallest analysis that satisfies §10.2 honestly?** Options to weigh, with
   the cost and the residual risk of each: analyse the concatenated composite; analyse each
   component and compose the results with an explicit interface contract per boundary;
   require the blocks to declare their reachable set and prove the declaration; or narrow
   §10.2 to what is provable and state the remainder as an accepted, named limitation.
4. **What must change in the blocks or wrappers** to make the composite analysable at all —
   for instance binding `EV_DIR` to a frozen root, or requiring a finite pin table? Note
   where round 5 and round 7 have already moved in that direction.
5. **What would make this proof worthless?** Name the failure modes: a component excluded
   from the composite, an interface contract asserted but unchecked, a runtime value
   silently defaulted at analysis time.

## Output

Write **only** `WPI_PREREG_DRAFT_ROUND1/SEC102_COMPOSITE_DESIGN_CODEX_2026-08-10.md`: the
composite inventory with measured identities, the per-value determinacy table, the weighed
options with a single recommendation, the required block/wrapper changes, and the
failure-mode list. End with a short section stating what Stage 1 can honestly claim under
your recommendation, and what it cannot. Do not edit the draft or the prover.
