# WP-P0-20 · allocator stages lane report — 2026-09-07

Claude Lead, remote Linux container, branch `claude/oauth-token-expired-bocby8` from
`master` `fe35b7c`. Owner authorized unattended work for this window.

**Outcome: three of four outstanding acceptance items delivered as non-accepting
candidates; the fourth is proven impossible here and instrumented instead. The package is
not accepted and cannot be while `WP-P0-12` is stopped.**

## Starting point

PR #161 landed the reviewed P0-20 shared-risk-calculator seed on `master`. Its own
docstrings named what it did not do: *"Policy caps are not applied by this synthetic
seed"* and *"Caps, venue lot/tick quantisation and runtime allocation remain out of
scope"*. PR #161 named four items still owed for acceptance: **caps**, **quantisation**,
**import identity into `simulate_slice`**, and **`UNSIMULATED_CONTROLS`**.

## Item 1 and 2 — caps and quantisation · DELIVERED (non-accepting)

`shared_risk_calculator.py`, commit `146eaa4`. Brief §5.5 line 1160 fixes the order:
resolve, then `precision`/`min_qty`/`min_notional` from frozen package metadata, then the
bound allocation-policy caps, *"either proposes the requested economic result in full or
rejects — a cap breach is REJECTED, never a quietly smaller order"*.

- `quantise_position_size` rounds **down** to `qty_step`, refuses below `min_qty`.
- `apply_allocation_policy_caps` returns `None` **by design** — no return value a caller
  could mistake for a trimmed proposal. Checks the risk-at-stop ceiling, leverage and
  exposure caps; refuses on breach; refuses when the caps' bound policy identity differs
  from the request's.
- `resolve_proposed_qty` composes the three stages in the contract's order and checks
  `min_notional` once a notional exists.

**No economic value was introduced.** Every bound, step and minimum arrives as an
argument from frozen metadata or bound policy; the module holds no venue rule and no cap
value, preserving the seed's existing "no default" discipline.

Ten new mutation controls beside the original eleven; all twenty-one `DETECTED`, and the
original eleven pass unchanged. The load-bearing one is **`CAP TRIMS INSTEAD OF
REJECTING`**: it mutates *conduct*, proposing a halved order where the contract requires
a rejection. A prohibition can only be checked by proving the forbidden behaviour is
caught.

D026, run in this container:

```
RED   new checker vs the fe35b7c seed -> exit 1, AttributeError:
      module 'shared_risk_calculator' has no attribute 'resolve_proposed_qty'
GREEN new checker vs 146eaa4          -> exit 0, 21/21 DETECTED, PASS
```

## Item 4 — computed `UNSIMULATED_CONTROLS` · DELIVERED (non-accepting)

`unsimulated_controls.py` + `check_unsimulated_controls.py`, commit `b2159fd`.

The design is set by the gate's harder sentence: *"An empty `UNSIMULATED_CONTROLS`
manifest that was not computed fails acceptance."* An authored empty manifest and a
computed empty one are indistinguishable if the manifest records only its conclusion, so
`UnsimulatedControls` carries its **inputs** and `promotion_block` **re-derives** the
entries, refusing anything that is not exactly `enabled - simulated`. Verification is
re-derivation, never a stamp.

Ten mutation controls, all `DETECTED`. The fixture the gate names by name:

```
fixture: 'funding_cost' is REQUIRED and appears in the computed manifest
         entries = [('funding_cost', 'REQUIRED')]
RED   (gate removed): PROMOTED -- a REQUIRED unsimulated control passed
GREEN (real gate)   : BLOCKED -- required_control_unsimulated: funding_cost
```

## Item 3 — import identity into `simulate_slice` · NOT POSSIBLE HERE · INSTRUMENTED

`check_allocator_import_identity.py`, commit `61ac1d0`.

Reading the canonical path settles it: **`simulate_slice` performs no position sizing at
all.** It simulates percent returns (`trades_pct`) with a flat `COST_BPS` and never
computes a quantity, a notional or an account figure. There is no sizing stage to bind
to. Binding one is not an edit but the canonical-simulator migration this package is
named for — T0, on a protected surface, changing research economics for every dependent
tool, and requiring the `WP-P0-12` `CORRECTED_VNEXT` kernel that `OD-20260826-1` and
`OD-20260826-8` stop.

What was delivered instead is the mechanical proof the gate demands (*"proven by import,
not asserted"*). Object identity is the only test that separates the delivered
implementation from a copy pasted into the engine — the exact failure D-13 exists to
prevent — so the runtime tier compares objects with `is`, and a local definition under
the same name is deliberately **not** a binding. `--self-test` proves it cannot be fooled:

```
SELF TEST (genuine import): BOUND_IDENTICAL as expected
SELF TEST (same-named re-implementation): BOUND_NOT_IDENTICAL as expected
SELF TEST (no binding at all): NOT_BOUND as expected
IMPORT IDENTITY SELF TEST: PASS
```

Against the real tree it reports `NOT_BOUND`. `--require-bound` makes that a non-zero
exit, so an acceptance run cannot pass this criterion by omission; it flips to `PASS` on
its own once the migration lands and binds the delivered object.

## Two things a reader must not misread

1. **Nothing here is accepted.** `WP-P0-20` is T0 and its acceptance gate requires the
   canonical path to run the kernel together with the allocator. That is unreachable
   while `WP-P0-12` is stopped, and no work in this lane changes that.
2. **The review verdicts no longer transfer to two of these files.** The three panels
   read exact blobs (`e0b0ae58d49d`, `4614d356dc31`). `shared_risk_calculator.py` and
   `check_shared_risk_calculator.py` are no longer those blobs. The verdicts stand for
   what they reviewed; they must be re-earned for the current content.

## Coverage gap, recorded rather than left implicit

`ci.yml` runs `compileall` and `pytest` **against `IBKR_PAPER_BRIDGE` only**. None of
these root-level modules or their checkers is executed by protected CI, so the checkers
are the only fence and they are run by hand. `WP-P0-27` is the CI-home carrier and is
planned, not built.

## Remaining for acceptance

- `WP-P0-12` unstopped and its `CORRECTED_VNEXT` kernel present in this repository.
- The canonical-simulator migration itself, then `--require-bound` passing.
- The control-parity checklist v1 and the statistical-battery definition v1, which exist
  today only as prose in the planning set, never as artifacts.
- Dependent-tool disposition record per class; before/after comparison on a real frozen
  candidate; the measured full-kernel trials-per-hour figure and the O-28-scale
  feasibility statement.
- Exact audits and independent Lead acceptance; none is claimed by this lane.

---

# Second run — 2026-09-07, definition artifacts and the acceptance harness

Same lane, same branch, after the owner lifted the WP-P0-11 / WP-P0-12 STOP
(`OD-20260907-1`) and authorized unattended overnight work (`OD-20260907-2`).

**Outcome: both of WP-P0-20's named definition artifacts now exist, plus the cost-model
registry, the evidence-class enforcement, and a harness that probes the acceptance gate
instead of reading it. 6 of 13 criteria MET. The package is still not acceptable, and the
seven outstanding rows now trace to a single fact rather than a policy.**

## What the lifted STOP did and did not change

It removed the bar on kernel work. It did not move any code: `WP-P0-12`'s Item-2 packet is
still `C:/tmp/P012_ITEM2_VERIFIER_SCOPE_DECISION_20260906_0056.md` on the Windows host, and
`CORRECTED_VNEXT` is not in this repository. Every blocked acceptance row below is blocked
on that absence, not on an owner decision. **Lifting a stop does not import the work.**

## Artifacts built

| Commit | Artifact | Prohibition it mechanises |
|---|---|---|
| `4af33bd` | **Control-parity checklist v1** (`control_parity_checklist.py`) | a REQUIRED control absent from a sim run ⇒ BLOCKED evidence; a tolerated row cannot exist without its metric, D026 fixture and `evaluation_run_hash` membership; the table cannot be edited without moving the version |
| `b12e7fa` | **Statistical-battery definition v1** (`statistical_battery.py`) | none of the seven elements is skippable; a verdict cannot be read against another run or battery version; an opened lockbox era is SPENT |
| `46890cc` | **Cost-model registry** (`cost_model_registry.py`) | an unregistered or provenance-broken cost model cannot produce acceptance-bearing evidence; a recalibration is event-driven, never calendar-driven, and rotates both lineage and `deployment_identity_hash` |
| `e201a82` | **Evidence class** (`evidence_class.py`) | a stand-in run is SIGNAL_SCREEN_ONLY and nothing converts it; `ALLOCATOR_NOT_YET_SHARED` is refused on sight; the gate signature carries no stamp or override parameter |
| `5e5e4e2` | **Acceptance harness** (`check_p020_acceptance.py`) | a criterion cannot be MET without a probe that executes; the package is never reported acceptable while a row is unmet |
| `28a3258` | **Dependent-tool disposition** (`11_TRIAGE/WP_P0_20_DEPENDENT_TOOL_DISPOSITION.md`) | — records all eight tools, class-verified against source |

Two integration properties are worth more than any single artifact:

- **`check_gate_agreement`** sweeps subsets of simulated controls and asserts the
  checklist's BLOCKED-evidence verdict and the manifest's promotion verdict match exactly.
  Two gates over one fact that disagree would be the silent gap D-13 exists to prevent.
- **`check_signature_has_no_conversion`** is structural: it reads
  `assert_acceptance_bearing`'s signature and fails if a `stamp`, `label`, `override` or
  `force` parameter ever appears. The gate's sentence is a claim about the shape of the
  code, so a behavioural test alone would not hold it.

## Verification, this container, `master` `fe35b7c` + this branch

Eight checkers, every one exit 0; **70 mutation controls, all DETECTED**; `generate_index.py
--check` GREEN.

```
check_shared_risk_calculator.py 21   check_statistical_battery.py     10
check_unsimulated_controls.py   10   check_cost_model_registry.py     11
check_control_parity_checklist.py 9  check_evidence_class.py           9
check_market_data_collector.py  PASS check_allocator_import_identity  --self-test PASS
```

## Acceptance state, probed rather than asserted

```
MET  (6)  checklist_v1_exists, battery_v1_exists, promotion_block_d026,
          computed_manifest, cost_model_provenance, standin_prohibition
BLOCKED   import_identity, kernel_present, required_tier_implemented, before_after,
          throughput
UNMET     dependent_disposition (proposed, not performed), audits (not self-certifiable)
```

`check_p020_acceptance.py` exits 1 and will keep exiting 1 until every row is MET.

## The one thing that unblocks the rest

`WP-P0-12` `CORRECTED_VNEXT` in this repository. Five of the seven outstanding rows resolve
behind it, `dependent_disposition` moves from proposed to performed with it, and only
`audits` remains — and that one is deliberately not self-certifiable.

## Self-review of this run's own code — two defects found and fixed

Written unattended with no external audit, so the branch was reviewed against itself.

1. **`bf682f3` — one number, two caps.** `apply_allocation_policy_caps` computed
   `notional / account_size` and compared it against **both** `max_leverage` and
   `max_exposure_fraction`. On a single flat account the two coincide, so every test passed
   and whichever bound was tighter fired first while the other read as dead code. The defect
   only surfaces once a second position exists: exposure would still report this proposal
   alone and wave through a nearly fully committed book. A cap that is correct exactly until
   the system does the thing it guards against is worse than an absent one, because it reads
   as covered. Exposure is now gross — `existing_gross_notional` is required with no default,
   validated non-negative because zero is a legitimate book — and
   `EXPOSURE IGNORES EXISTING BOOK` reproduces the original defect as a DETECTED mutant.
2. **`18d73c0` — a mention is not a kernel.** `probe_kernel_present` tested
   `"CORRECTED_VNEXT" in source`, so a comment or a TODO would have flipped the row to MET.
   It now walks the AST for real imports; a mention with no import reports UNMET and says so.
   Proven against a synthetic canonical path: comment-only → UNMET, `import mtc_v2.core.kernel`
   → MET, real tree → BLOCKED.

Both are the same class of error as the one the R1 correction pass records about the
stand-in: a check that reads correct while measuring the wrong thing.

## CI gap closed

`11bddf3` adds `.github/workflows/research-gates.yml`, running all eight checkers plus the
index check on Python 3.12. Every module is stdlib-only so the job installs nothing. The
acceptance harness runs as a **report**, not a gate — it exits non-zero by design until
acceptance, and wiring that as a failure would leave the workflow permanently red. The
workflow is **not** a required check: ruleset 21444962 still requires exactly
`Bridge suite (Python 3.12)`, and `WP-P0-27` is still the unbuilt carrier for progressive CI
activation. Twenty-two mutation controls in the allocator checker now: 71 across the modules this lane
authored or extended, and 84 across the whole suite counting the thirteen the collector
checkers brought with #161.
