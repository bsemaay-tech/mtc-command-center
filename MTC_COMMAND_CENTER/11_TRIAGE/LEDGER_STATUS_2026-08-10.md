# 50-hour plan — where we actually are (2026-08-10 morning)

> **RATIFIED 2026-08-11 (Barış, in chat).** The previously unratified time below is now
> owner-signed. See the running total at the bottom. Booking continues prospectively; the
> next owner flag is due only when the remaining balance drops below 10 h.

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

---

## RATIFICATION UPDATE — 2026-08-11 morning (owner-signed in chat)

| Line | Hours | Basis |
|---|---:|---|
| Ratified total at 2026-08-10 morning | 24.9 | above, owner-ratified |
| 2026-08-10 daytime WP-I work (RP6/RP7/transport draft rounds, prereg, tier/routing/tooling) | ~4.4 | booked 2026-08-10, **now ratified** |
| Overnight + morning 2026-08-10 19:00 → 2026-08-11 ~11:40 (RP6 r7–r10a, RP7 r5–r8, prover audit, §10.1/§10.2/skeleton/RUNID/transport analyses, defect-pattern amendment, ~55 commits) | ~5.5 | booked here, **now ratified** |
| **Total used, owner-ratified 2026-08-11** | **~34.8** | Barış, in chat 2026-08-11 |
| **Remaining against the 50 h ceiling** | **~15.2** | |

**Booking note.** The overnight figure is prospective per the standing rule — no retroactive
per-minute reconstruction. It covers ~16.5 h of wall clock at the usual ~3:1 wall-to-credit
ratio (dominated by adversarial audit rounds and account-window waits), which lands at ~5.5 h
of plan credit. Owner adjusts at any later ratification if it reads high or low.

**Next flag:** the standing rule says surface the ledger to the owner when the remaining
balance drops below 10 h. At ~15.2 h remaining, that flag is not yet due — but WP-I is not
close to freeze (see the freeze blocker map), so the sub-10 h flag is likely the next major
owner checkpoint. Rows 1–9 (owner chose BUILD ALL NINE, 2026-08-11) adds 3–6 rounds and will
consume a meaningful part of the remaining balance.

---

## BOOKING — 2026-08-11 afternoon burst (Fable overnight Lead, prospective)

| Line | Hours | Basis |
|---|---:|---|
| Ratified total at 2026-08-11 morning | ~34.8 | owner-signed above |
| 2026-08-11 ~12:00-15:20 WP-I burst | ~1.8 | booked here, prospective |
| **Total used (prospective)** | **~36.6** | |
| **Remaining against the 50 h ceiling** | **~13.4** | |

**What the ~1.8 h bought** (~3.3 h wall clock, unusually dense - 14 delegated agent runs
completed, ~20 commits, little idle): prereg successor draft R2->R3 (13 skeleton gaps + 6
RUNID changes + section 10.1 11-EXTEND application + two-commit attestation ordering, merged,
34/34 conserved, MC-01..03 collapsed to one owner ratification ask); SEC102 composite
pathproof round 1 (scaffold + allocate stage, Lead-reproduced); transport round 4 built +
two-band Codex audit (both REQUEST_CHANGES) + round 5 repair (F1->OPEN, BA-1/BA-2/BA-3) +
draft edits applied; RP6 round 10b (10a bytes confirmed, harnesses Lead-run verbatim) +
Codex r10 audit (REQUEST_CHANGES x4) + round 11 dispatched; pathscope prover round 2 (9+5
silent-sink classes closed, Lead-reproduced); process-invariant + SESSION_LOCK adoption.

**Flag status:** ~13.4 h remaining - the sub-10 h flag is NOT yet due but is now within one
more work burst. Expect to cross it overnight; the morning report will carry the exact figure
and an explicit owner flag if it lands below 10 h. Owner adjusts at any ratification.
