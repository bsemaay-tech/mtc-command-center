# WP-P0-12 scope assessment — what the lifted STOP actually opened

Read-only assessment written the night `OD-20260907-1` lifted the WP-P0-11 / WP-P0-12 STOP,
so the decision about where to start is made against evidence rather than against the plan's
prose. **No kernel code was written or changed.**

## The seed is here; the Windows work still is not

`mtc_v2/core` — the seed the map-#67 fold names, whose behaviour is the `LEGACY_COMPATIBLE`
baseline — is present at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/`: fifteen modules
(`runner.py`, `position_sizer.py`, `position_manager.py`, `exits.py`, `instrument.py`,
`rounding.py`, `gates.py`, `confirmation.py`, `htf.py`, `indicators.py`, `ma.py`,
`config.py`, `results.py`, `types.py`) with fifteen test files beside them.

What is still absent is the WP-P0-12 work itself — the Item-2 verifier scope recorded in
`C:/tmp/P012_ITEM2_VERIFIER_SCOPE_DECISION_20260906_0056.md` on the Windows host. Lifting
the stop did not import it, and starting fresh here would duplicate it.

## P0-12's eight outputs against the seed

Presence measured by grep across `mtc_v2/core/`; presence of a term is not implementation of
the control, so read this as "there is something to migrate" versus "there is nothing yet".

| P0-12 output | Files mentioning it | Reading |
|---|---|---|
| contract multiplier | 5 | present to migrate |
| frozen instrument metadata | 5 | present to migrate |
| minimum notional | 3 | present to migrate |
| named same-bar collision policy | 3 | present, needs naming |
| **gap-aware stop fills** | **0** | **absent** |
| **in-path slippage** | **0** | **absent** |
| **real fee schedule** | **0** | **absent** |
| **funding-cost model (brief §9.2)** | **0** | **absent** |

## The finding worth acting on

The four absent outputs are not a random half. Set them beside control-parity checklist v1's
REQUIRED tier, built earlier tonight from the same fold's §4:

| Checklist REQUIRED control | P0-12 output | State |
|---|---|---|
| Risk Allocator | — delivered by WP-P0-20 | seed landed #161, stages added this run |
| Fees | real fee schedule | **absent from the kernel seed** |
| Funding | funding-cost model | **absent from the kernel seed** |
| Slippage | in-path slippage | **absent from the kernel seed** |
| Protective-order semantics | gap-aware stop fills | **absent from the kernel seed** |

**The correspondence is exact, five for five.** The checklist's REQUIRED tier and P0-12's
missing outputs are the same work seen from two sides: the checklist says which controls
must be simulated for evidence to count, and the kernel is missing precisely those four,
with the fifth being the allocator WP-P0-20 delivers. Neither package is a prerequisite for
understanding the other — they are one economic gap described twice.

That is why `check_p020_acceptance.py` reports `required_tier_implemented` BLOCKED rather
than merely unmeasured. There is nothing to measure yet.

## What a start here would and would not be

- **Would be:** implementing four new economic behaviours in the strategy kernel — fees,
  funding, slippage and gap-aware stop fills — each needing its own defect record,
  before/after evidence, D026 RED/GREEN falsification and new expected golden artifacts,
  against a `LEGACY_COMPATIBLE` baseline that WP-P0-11's own gate report records as **not
  executable** ("Fresh baseline is not executable until publication authorization and
  diagnostics exist").
- **Would not be:** acceptable. WP-P0-12 is T0 on a protected surface, and T0 acceptance
  needs exact audits by the canonical models plus independent Lead acceptance. **The exact
  audit models are unreachable from this container**, as the 2026-09-07 overnight record
  already noted. Work done here can be evidenced but not accepted.

**Recommendation, for the owner:** import the Windows-host `P012` work before any fresh
kernel implementation starts. Four new economic behaviours written here would collide with
whatever that packet already contains, and the collision would be in the one scope where a
silent divergence is most expensive.
