# KICKOFF — WP-I staging-verification preregistration DRAFT (round 1)

You are the counterpart implementer (Claude Max) drafting the WP-I preregistration for
an authorized private-repo staging-verification work package. DRAFT only: nothing you
write authorizes or performs any host contact. Write outputs ONLY into this directory.
ASCII only. English only.

## Inputs (read these, nothing else)

- This file.
- `../GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md` — Groups A3
  (static security inventory), B (read-only host checks), C (mutating checks): the
  WP-I check universe.
- `../WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/02_PREREG/PREREGISTRATION.md` —
  the rigor template your draft must match (RUNIDs, evidence contract, pinned argv,
  expectations table, immutability, safety state).
- `../WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/03_TRANSPORT/B3_STOP_ADJUDICATION.md`
  — tonight's hard lesson; see constraint 1.
- `../WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/EVIDENCE_INDEX.md` — what is
  already banked (do not re-plan checks whose evidence exists).

## Deliverables (into this directory)

1. `WPI_PREREGISTRATION_DRAFT.md` — same section skeleton as the Stage 2 template:
   run identifiers + evidence tree (placeholder RUNIDs marked `<ALLOCATE-AT-DISPATCH>`,
   never concrete — a draft must not mint one-use identifiers), preregistered inputs,
   per-check expectations table with exact predicted first divergence, exact remote
   argv pattern (same pinned fail-closed ssh options), operator-side evidence contract,
   what is deliberately NOT preregistered, immutability rules, safety state.
2. `WPI_CHECK_FEASIBILITY.tsv` — one row per Group A3/B/C check: check id, brief
   description, feasible-as-unprivileged-gatea (yes/no/partial + why), classification
   (INCLUDE-READ-ONLY / DEFER-ROOT-SIDE / BLOCKED-UPSTREAM / ALREADY-BANKED with the
   EVIDENCE_INDEX citation).
3. `SELF_QA.md` — how you verified each feasibility call and each expectation row.

## Hard constraints

1. **Unprivileged feasibility is a design gate, not an afterthought.** Tonight B3
   STOPped because an accepted check assumed `stat` inside a `750 root:root` directory
   as the unprivileged user. For EVERY check you include, state why it works as
   `gatea` without sudo; anything needing privilege goes to DEFER-ROOT-SIDE, following
   the RPD-VERIFY pattern (root-side deploy-time verify), not into the run plan.
2. Group C (mutating) checks: preregister NOTHING executable — list them in "NOT
   preregistered" with their blocking dependency, exactly as the Stage 2 template does
   for C1-C5.
3. No concrete RUNID, no date-stamped unit id, no record-root path that could collide
   with an existing one: placeholders with `<ALLOCATE-AT-DISPATCH>` markers.
4. Do not weaken the Stage 2 conventions: create-once, first-FAIL, three-outcome rc,
   evidence closed by a separate invocation, remote-vs-local binding.
5. Do not touch any file outside this directory. No host contact of any kind.
