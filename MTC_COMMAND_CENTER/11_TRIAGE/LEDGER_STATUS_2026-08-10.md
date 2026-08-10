# 50-hour plan — where we actually are (2026-08-10 morning)

## The numbers

| Line | Hours | Basis |
|---|---:|---|
| Ratified baseline used at WP-L P2 start | 20.5 | `OWNER_DECISION_AUDIT_TIERS_2026-08-09.md` §1, owner-ratified |
| WP-L Phase 2 unit (Stage 1+2, Stage 3+3B, repair/audit/re-freeze) | 2.6 | `WPL_P2_STAGING_.../UNIT_CLOSURE_RECORD.md` §7 |
| **Other overnight units — NEW booking, see below** | **1.8** | booked here, prospectively |
| **Total used** | **24.9** | |
| **Remaining against the 50 h ceiling** | **25.1** | |

Last night consumed **4.4 h** of plan time in total: 2.6 h inside the WP-L P2 unit plus
1.8 h across units that unit did not cover.

### The 1.8 h being booked now

The WP-L P2 closure record booked only that unit. These ran the same night and were not
booked anywhere, so they are booked here rather than left invisible:

| Work | Hours |
|---|---:|
| WP-I draft cycle — rounds 1.1/1.2/1.3, Codex adversarial audit, GLM independent verification | 0.8 |
| Audit 2 checklist v2 (GLM review applied) + Audit 2 readiness package | 0.4 |
| Defect-pattern catalogue + independent evidence-chain integrity verification | 0.3 |
| RP6-P0 partial block, its audit, and the Lead adjudication | 0.3 |

Prospective, per the standing rule — no retroactive reconstruction. Owner adjusts at
ratification if these read high or low.

## Big picture — the roadmap and what is left

```
WP-0 / WP-S / WP-L P1 / Gate A   DONE      ┐
WP-L Phase 2                     DONE      ├─ 24.9 h spent
overnight cross-unit work        DONE      ┘
                                              ← we are here
WP-I staging verification        NEXT      ┐
Audit 2 (two-flagship, T0)       blocked by WP-I
WP-A                             blocked by Audit 2
Gate B                           later      ├─ 25.1 h remain
WP-V                             later     ┘
```

**Just over half the plan is spent (49.8%), and the hard part of the remaining work is
now unblocked.** Both gates that were holding WP-I — host-contact authority and the budget
lift — were granted this morning, and root for `RPD-VERIFY` was granted alongside them.

## What that buys, concretely

- **WP-I is dispatchable** once its preregistration is finalized: identifiers allocated,
  `<PIN-BEFORE-DISPATCH>` values filled, Stage 1 freeze done. The draft itself is
  audit-clean (six findings applied, independently verified).
- **`RPD-VERIFY` can finally run.** It closes the three checks B3 defers *and* the
  `bridge.env` naming question, which no unprivileged block could ever settle because
  permission denial is name-independent. That question has been open since the first host
  contact.
- **Audit 2 unblocks the moment WP-I closes** — its readiness package is already assembled,
  so dispatch is immediate rather than a fresh research effort.

## Honest caveats

- The 20.5 h baseline is a **ratified** figure, not a reconstructed one; the ledger record
  states the exact balance was NOT reproducible from primary evidence, which is why the
  owner ratified it rather than deriving it. Everything after it is prospective per-unit
  booking.
- The budget lift applies to **WP-I**. It does not convert the 50 h ceiling into an open
  budget for WP-A, Gate B or WP-V — those still sit inside the remaining 25.1 h unless
  separately lifted.
- Hours measure plan consumption, not wall-clock or token spend. Last night's 4.4 h of plan
  time ran across **13 h 11 min of wall clock** — first commit `7e9d1c4a` at 2026-08-09
  18:05, last commit `4a1d2948` at 2026-08-10 07:16, 53 commits. (An earlier draft of this
  file said "roughly eleven hours"; that was an unmeasured estimate and is corrected here
  from git timestamps.)

  **Ratio: about 3 hours of wall clock per 1 hour of plan credit.** That is not waste — the
  plan hour measures the deliverable, while the wall clock includes the six adversarial
  audit rounds, the failed first B3 attempt, and the waiting. The six largest idle gaps
  were 111, 80, 60, 51, 47 and 38 minutes, almost all of them heartbeat waits while a
  delegated agent was running or while the non-gated backlog was exhausted and everything
  left needed owner authority.
