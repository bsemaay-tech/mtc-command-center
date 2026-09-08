# Governance stage handoff

## [Claude Lead] 2026-09-07 — P0-20 definition artifacts built; one blocker left

- **Owner decisions recorded** (`c2cd955`): `OD-20260907-1` lifts the WP-P0-11 / WP-P0-12
  STOP; `OD-20260907-2` records the unattended overnight authorization with its stated
  reading — repository work, not irreversible outward acts.
- **Lifting the stop moved no code.** `WP-P0-12` `CORRECTED_VNEXT` is still absent from this
  repository and its Item-2 packet is still on the Windows host. Every blocked acceptance
  row below is blocked on that absence, not on a decision.
- **Built this run**, all on `claude/oauth-token-expired-bocby8`, full evidence in
  `11_TRIAGE/WP_P0_20_ALLOCATOR_STAGES_2026-09-07/LANE_REPORT.md`:
  `4af33bd` control-parity checklist v1 · `b12e7fa` statistical-battery definition v1 —
  WP-P0-20's two named definition artifacts, which existed only as prose until now ·
  `46890cc` the versioned research-side cost-model registry · `e201a82` evidence class,
  derived from a run's facts rather than a label it carries · `5e5e4e2` an acceptance
  harness that probes the gate instead of reading it · `28a3258` all eight dependent tools
  located and class-verified against source.
- **Verification:** eight checkers, every one exit 0; **84 mutation controls, all
  DETECTED**; `generate_index.py --check` GREEN. Two controls carry more weight than the
  rest: `check_gate_agreement` proves the checklist and the manifest never disagree about
  one run, and `check_signature_has_no_conversion` is structural — it fails if a `stamp`,
  `override` or `force` parameter ever appears on the evidence gate, because "there is no
  manifest stamp that converts it" is a claim about the shape of the code.
- **Acceptance state, probed** (`python3 check_p020_acceptance.py`, exits 1 at **6/13**):
  MET — `checklist_v1_exists`, `battery_v1_exists`, `promotion_block_d026`,
  `computed_manifest`, `cost_model_provenance`, `standin_prohibition`. BLOCKED —
  `import_identity`, `kernel_present`, `required_tier_implemented`, `before_after`,
  `throughput`. UNMET — `dependent_disposition` (proposed, not performed), `audits`.
- **Self-review found two real defects, both fixed** (`bf682f3`, `18d73c0`): the cap stage
  compared one number, `notional / account_size`, against both the leverage and the exposure
  cap — correct on a flat account and silently wrong the moment a second position exists, so
  exposure is now gross and `existing_gross_notional` is a required argument; and the
  harness's kernel probe was a substring search a comment could satisfy, so it now walks the
  AST for a real import.
- **CI now runs the research gates** (`11bddf3`, `.github/workflows/research-gates.yml`).
  It is **not** a required check — ruleset 21444962 still requires exactly `Bridge suite
  (Python 3.12)` — and `WP-P0-27` is still the carrier for progressive CI activation.
- **Nothing is accepted, and nothing here claims to be.** No exact audit ran; the container
  cannot reach the audit models.
- **NEXT ACTION:** bring the Windows-host `P012` packet into this repository — **not** a
  fresh kernel start here. `11_TRIAGE/WP_P0_12_SCOPE_ASSESSMENT_2026-09-07.md` measures why:
  the `mtc_v2/core` seed is present, but four of P0-12's eight outputs are absent from it —
  fees, funding, in-path slippage and gap-aware stop fills — and those four are **exactly**
  the checklist's REQUIRED tier, five for five with the allocator. Writing them here would
  collide with whatever that packet holds, in the scope where silent divergence costs most.
  Then run `check_p020_acceptance.py` and work whatever it still reports.
- **WAITING FOR OWNER:** the WP-P0-12 import from the Windows host. Nothing else.

## History

The superseded 2026-09-07 section is in
`_AI_MEMORY/history/00_AGENT_PROTOCOLS_HANDOFF_20260907_2339.md`; the three before it in
`..._20260907_2251.md`, and earlier narrative in `..._20260906_2257.md` and
`..._20260905_2202.md`.
