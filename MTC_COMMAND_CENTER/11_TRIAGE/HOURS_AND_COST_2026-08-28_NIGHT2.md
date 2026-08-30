# Hours and cost per package — night of 2026-08-28 into 2026-08-29

Owner asked for time spent per package. Markdown only, per his standing instruction — no JSON ledger.

## ⚠️ Read the accuracy caveat before using these numbers

**Wall-clock times are measured, but with a known drift.** The audit of this session's ledger
(`AUDIT_P1_LEDGER.md`, Claude Pro) found that recorded times reconcile exactly against
`N_TIMES.txt`, run-log mtimes and git commit timestamps **for roughly the first fifteen lanes**, and
that **from lane N14 onward prose and table end-times run 2-11 minutes ahead of every independent
witness.** That drift is not corrected below — correcting 40+ rows by hand would introduce more error
than it removes.

**Treat per-package totals as accurate to about ±10%, and biased slightly high.**

**USD is NOT MEASURED.** See the cost section.

---

## Wall-clock per package

Route-hours in the costing documents are *engineering* estimates and are a different unit; these are
elapsed lane times.

| Package | Lanes | Wall clock | Note |
|---|---:|---:|---|
| **WP-P0-10** | 7 | **~65 min** | build, Lead finish, 2 flagship audits, nit closure, merge, post-merge verify |
| **WP-P0-11** | 19 | **~6 h 40 min** | 4 build/repair commits, 3 designs, 9 audits/reviews — the bulk of the night |
| **Promotion decision** | 5 | **~42 min** | recast, detection audit, corrections, correction re-check |
| **Investigations (unasked)** | 11 | **~2 h 15 min** | Range Filter, seventh pattern, queue-inert, bridge/CI census, v3/v4 gap, dashboard, QuantLens, schema migration |
| **Owner-doc audits** | 6 | **~1 h 20 min** | morning report ×2, ledger, ready-specs, decision pages |
| **Lead in-session** | — | **~2 h** | Pine de-fang, merge execution, 19 corrections, all specs, ledger |

**Session span: 21:14 → 07:00, ~9 h 45 min**, of which **~4 h were idle** (02:35-06:26, the missed
waiter — Lead error 19). **Productive span ≈ 5 h 45 min.**

## Measured token spend — Codex lanes only

These are the only routes that report token counts in their logs. **Measured, not estimated.**

| Lane | Package | Tokens (k) |
|---|---|---:|
| N1 | WP-P0-10 build | 265 |
| N3 | WP-P0-11 stage 1 (stopped, false conflict) | 181 |
| N3b | WP-P0-11 stage 1 | 550 |
| N8 | WP-P0-11 stage 2 | 767 |
| N22 | stage-3 design | 324 |
| N23 | repair round 1 | 649 |
| N24 | stage-3 design revision | 382 |
| N25 | stage-4 design | 325 |
| N26 | repair round 2 | 353 |
| **Codex subtotal** | | **~3.8 M** |

**Claude Pro, Claude Max and Grok do not report token counts in their run logs**, so their share is
**NOT MEASURED**. By lane count they carried **26 of 48** lanes, so total spend is materially higher
than the Codex figure alone.

## USD — NOT MEASURED

**I cannot measure dollar cost from inside this session and will not estimate it.** Producing an
unsourced number here would be the exact defect this whole night was about.

What is known:

- **Session-start baseline**, reported by CodeBurn at 21:14: **Today $181.34 / 1,163 calls;
  Month $4,735.87 / 28,221 calls.**
- **No end-of-session figure was captured.** The delta is the night's cost.

**What would establish it:** the CodeBurn dashboard's current "Today" figure minus $181.34. That is a
one-line lookup the owner can do, and it is the only honest source.

**Rough shape, stated as shape not as a number:** the night ran 48 lanes across 6 route families,
~3.8 M measured Codex tokens plus an unmeasured Claude/Grok share across 26 lanes. Grok's balance was
**fully exhausted** (402), which was the owner's explicit goal for that route.

## Route consumption

| Route | Lanes | End state |
|---|---:|---|
| Codex `third` (Plus) | 3 | capped 21:39-23:56, then live again |
| Codex `free` (Pro) | 7 | live |
| Codex `secondary` | 1 | **live** — was recorded as capped until Aug 31; that record was wrong |
| Codex `fourth` | 1 | **live** — same correction |
| Claude Pro | 17 | capped 21:44-23:50, then live again |
| Claude Max | 8 | live, spent under the owner's dated authorization |
| Grok | 12 | **exhausted (402)** |

## What the money bought

| | |
|---|---|
| Merged to `master` | 1 package (WP-P0-10), dual-flagship PASS |
| Committed, not merged | 4 commits on WP-P0-11, currently BLOCKED on repair 3 |
| Owner decision pages | 4, all audited and corrected |
| Designs | stage-3 (revised, re-audited clean), stage-4 (9 blockers found) |
| Defects found in owner-facing docs | 25 + 21 + 12 + 13 + 8 across five audits |
| Lead errors caught and corrected | **19** |
| Safety claims corrected before reaching the owner | **3** |


---

## Addendum 2026-08-29 09:00 - morning batch and final package state

Ten lanes ran in parallel after the owner asked for maximum throughput. Added time:

| Package | Additional wall clock | What |
|---|---:|---|
| WP-P0-11 | **~2 h 15 min** | repair round 3 (`fcfa7483`, ten findings closed), stage-4 design audit, two repair audits |
| Verification of prior claims | **~1 h 30 min** | QuantLens census, dashboard census, P0-10 merged state, migration design |
| Censuses | **~1 h** | `07_ADAPTERS` + contracts, `01_MTC_PROJECT` parity oracles |

**Revised package totals:** WP-P0-10 ~65 min (unchanged, closed); WP-P0-11 **~8 h 55 min**;
promotion ~42 min; investigations and verification **~4 h 45 min**.

**Why the verification time was worth its cost:** both censuses were **inflated** and neither had
reached the owner. QuantLens claimed 13 DECISION findings - verified 9, with 3 re-banded and 1
refuted. The dashboard claimed 6 - **1 survived**. Relaying either unverified would have handed the
owner 19 overstated claims, which is exactly how Lead error 17 happened.

**A census is a hypothesis until a second party re-bands it.** Severity inflates more quietly than
counts do.
