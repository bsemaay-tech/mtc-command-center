# Owner decisions — Barış — 2026-08-15 night

> **Pathscope disclosure (owner decision 2026-08-16, section 6):** Pathscope is a supplemental aid only: its output may inform review, but it may never be cited as proof, a gate, or an acceptance input anywhere in WP-I or downstream, and no Pathscope PASS may close any gate.
> Governing record: MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_SUPPLEMENTAL_DISCLOSURE_V2_2026-08-16.md. Identity split: the prover in this repository is the older 137520-byte R5 code; the audited 185272-byte Option C prover is UNMERGED on codex/pathscope-accounting-redesign-20260815. Prerequisite gate 2 is UNKNOWN until the Lead re-derives it at freeze-prerequisite review.
> Note (2026-08-16): D1 Option C cycle is consumed (REQUEST_CHANGES). Section 6 of the 2026-08-16 record supersedes every acceptance dependency below; gate 2 is UNKNOWN pending Lead re-derivation.


Recorded verbatim in substance by the Lead immediately on receipt. These are
owner decisions, not Lead inferences. Where a decision's own wording contains a
precondition, that precondition is preserved and called out rather than treated
as satisfied.

## D1 — Pathscope: **Option C authorized**

> "Recommended — rebuild one layer so the whole class of hole becomes impossible.
> ~6–10 h, ends the cycle."

This authorizes, per
`WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_DECISION_OPTIONS_2026-08-15.md`:

- one **accounting-layer redesign** of `pathscope_prover.py` — every admitted
  member must reach exactly one terminal disposition, and any member without one
  fails the run closed; and
- **one fresh flagship execution audit** of the redesigned bytes.

It does **not** authorize an open-ended sequence of repair rounds. If the audit
returns a required finding, the lane returns to the owner boundary exactly as it
did on 2026-08-15 morning. The parser is kept; the reporting layer is replaced.
The existing fixtures and published harness remain valid regression evidence.

Scope limit carried forward: this closes F1, F2 and F3 by construction rather
than by patch. A redesign that merely adds three more recognised shapes does not
satisfy this decision.

## D2 — Narrow read-only host-and-credential confirmation: **approved**

Approved sentence, from
`AUDIT2_READINESS_PACKAGE/WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md` §3:

> "I authorize the exact preregistered and committed read-only grant-#6
> attestation capture and WP-I operations on `GATEA-STAGING`, including use of
> the pinned SSH identity solely for those actions; all other credential and host
> actions remain excluded."

**This grant is real but not yet spendable, and the Lead will not spend it
tonight.** Its own wording is conditional on artifacts that do not exist:

1. the **exact preregistration must be committed first** — that is Stage-1
   Commit 1, the read-only attestation-only preregistration with its producer,
   argv, environment, cwd and output grammar. It has not been written.
2. the Stage-1 allocation record — `BASE`, P0/RO RUNIDs, stage IDs,
   `REMOTE_BASE`, confirmation token, operator root — does not exist.

Until Commit 1 exists, there is nothing "preregistered and committed" for this
authorization to attach to, so any host contact would be outside the grant. The
correct order is: build the allocation record, commit the preregistration, then
spend this grant against those exact committed bytes.

Explicitly still excluded by this decision: the Hostinger KVM2 production server,
any write action on any host, any credential other than the pinned SSH identity,
any use of that identity for anything other than the named actions, broker or
exchange contact, ARM, orders, TESTNET or mainnet execution, deployment, and
merge to master.

`GATEA-STAGING` is the disposable staging host. It is **not** KVM2.

## D3 — Packet 11 hours ledger: **signed**

> "approved"

Ratified figure: **approximately 63.75 hours used**, being the ~55 h
owner-ratified anchor of 2026-08-13 plus 8 h 44 m 57 s of measured post-anchor
commit-session span across 38 commits in 10 sessions. Source and reproduction
commands: `AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET11_LEDGER_MEASUREMENT_2026-08-15.md`.

Honest carry-forward, unchanged by this signature: the measurement lane and the
authority consolidation both record that this figure will drift as remaining WP-I
work is booked, and that Packet 11's own scope asks for ratification at the
**freeze-time checkpoint**. This signature ratifies the figure as of 2026-08-15.
If the figure at the real freeze checkpoint differs, it must be re-presented
rather than silently carried.

Remaining work is still estimated by gates, not by subtracting from 50.

## D4 — KVM2-specific TESTNET wallet: **deferred**

> "this we will do later"

No wallet is provisioned, requested, or inferred. Deploy checklist item 4 stays
open and blocks the first start. Nothing in the deploy sequence may proceed past
the point that requires it. No agent may ask for, generate, store, or reference a
key value.

## D5 — Risk-state continuity at cutover: **start clean**

> "start clean"

The owner selects a **fresh-database reset** rather than a WAL-consistent
migration. Deploy checklist item 5 records that WAL migration was the
*recommended and supported* option, so this is a deliberate owner override of the
recommendation and is recorded as such.

What this means concretely, and what the Lead must now verify rather than assume:

- The destination bridge starts with no inherited daily-loss counter, no
  consecutive-loss counter, no order history and no foreign-position record.
- Checklist item 5's own wording requires that a conservative fresh reset
  **"preserves or blocks on"** lost daily-loss, consecutive-loss, order and
  foreign-position evidence. A clean start must therefore still be proven to
  either carry that evidence forward in some retrievable form, or to refuse to
  start if it would silently lose it. "Start clean" is not the same as "start
  blind", and the difference is a safety property.
- The single-writer cutover proof in item 6 is unchanged and still mandatory:
  raw empty positions and raw empty orders must be captured before and after the
  old writer is stopped, whatever happens to the database.

**Open sub-question for the owner, created by this decision and not decided
here:** whether the pre-cutover risk state must be *archived off-host* before the
fresh start, or may simply be left behind on the old machine. The Lead
recommends archiving it, because it is the only record of the paper period. This
is a one-sentence follow-up, not a blocker for the work that precedes cutover.

## Effect on the blocker map

| Item | Before | After |
|---|---|---|
| Pathscope | RED, owner boundary | **Authorized — Option C in progress** |
| Audit-2 gate 2 | open only on Pathscope | open until the Option-C audit accepts |
| Stage-1 host step | blocked on an unwritten authority | **granted, precondition unmet** — needs Commit 1 first |
| Packet 11 | awaiting signature | **signed at ~63.75 h**, re-present at freeze |
| Deploy item 4 (wallet) | owner decision | **deferred by owner** |
| Deploy item 5 (risk state) | owner decision | **decided: fresh reset** |

Owner decisions still outstanding: which plan authority governs — see
`PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md` when it lands — and the archive
sub-question in D5.

No host, network, deployment, service, credential, broker/exchange, ARM, order,
TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, or economic action
has been performed under these decisions.
