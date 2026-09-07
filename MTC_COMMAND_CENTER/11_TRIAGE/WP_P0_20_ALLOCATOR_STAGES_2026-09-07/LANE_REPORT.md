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
