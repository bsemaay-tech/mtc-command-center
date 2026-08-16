# Owner decision — winding down three paused evidence-programme leftovers — 2026-08-16

**STATUS: DECIDED 2026-08-16 (late evening) — owner answers: item 1 = A, item 2 = B,
item 3 = A. Binding record: `OWNER_DECISIONS_2026-08-16_HOUSEKEEPING.md`. Decision 2
executed same day as `AUDIT2_CLOSURE_NOTE_2026-08-16.md`. Body below kept unchanged
as the analysis the decision was made on.**

## Why this exists

The Bridge deployment to the KVM2 VPS is essentially done — the release is
built, tested, and independently double-checked; the only thing missing is
your one signed sentence authorizing the install. Three older pieces of
"evidence work" from the bigger audit programme never finished and are just
sitting there, unresolved. None of them block the pending install. This memo
gives you one clean decision per item: freeze it exactly as it is and spend
nothing more (**ARCHIVE**), or take the smallest possible step to close it
honestly (**FINISH-MINIMAL**).

**Where this record lives, in plain terms:** almost everything below is
recorded on a working branch called `codex/rp7-r1-r4-repair-20260815` — the
actual day-to-day line of work for the last two days — which has not yet been
folded into the main line of the project (`master`). It is 720 commits ahead
of `master` and not merged. That is normal mid-project housekeeping, not a
problem, but it means: if you or someone else looks at the "current" checked-
out copy of the repo, some of these files will not be there. I read them
directly out of that branch's history to write this memo. File paths below
are given relative to `MTC_COMMAND_CENTER/` and are on that branch unless
marked otherwise.

---

## Item 1 — the "chain lane" (two-commit chain / Stage-1 freeze design)

### What it is

A small, self-contained piece of engineering design: a way to record two
related git commits together so that a later automated check can trust they
belong to the same "frozen" package and weren't tampered with in between. It
was one design document, reviewed by AI several times, never accepted.

### Where it stands

- Three design revisions were written and independently reviewed: V1
  (`11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_TWO_COMMIT_CHAIN_DESIGN_V1_2026-08-16.md`,
  review in `TWO_COMMIT_CHAIN_CLAUDE_REVIEW_2026-08-16.md`), V2
  (`..._DESIGN_V2_2026-08-16.md`, two review rounds:
  `TWO_COMMIT_CHAIN_CLAUDE_REVIEW_R2_2026-08-16.md` +
  `TWO_COMMIT_CHAIN_R2_DISPOSITION_2026-08-16.md`), and V3
  (`..._DESIGN_V3_2026-08-16.md`, one review round:
  `TWO_COMMIT_CHAIN_V3_REVIEW_R1_2026-08-16.md`, verdict REQUEST_CHANGES: 2
  required fixes + 4 minor notes).
- **You personally stopped this on 2026-08-16 afternoon.** Record:
  `11_TRIAGE/OWNER_INSTRUCTIONS_KVM2_MULTITENANT_2026-08-16.md` §1. Your
  ruling: the review process had a two-round limit, V2 already used both
  rounds, and the AI Lead's claim that "V3 counts as a fresh cycle" was
  **rejected by you**. As a direct result: the next repair round (V4) that was
  already in flight got killed mid-run, its partial output was thrown into a
  quarantine folder and never used, and the V3 review that had just finished
  was downgraded to "informational only — does not count toward acceptance."
- **The rule you set, in the record's own words: "No further V3/V4 repair or
  review may start unless the Lead first demonstrates AND records a genuinely
  new [starting] scope, or the owner grants an explicit cap waiver in chat."**
  I searched every commit since that ruling (through the most recent one,
  2026-08-16 22:33) and found no such new scope and no waiver. The design has
  no accepted version today.
- Net effect: this design has never been used for anything and isn't wired
  into any running code. It exists purely as a paper design plus its own
  review paperwork.

### Option A — ARCHIVE

Leave it exactly as paused. Add one short "closed, not revisited" line to the
existing pause record. Spend: **nothing** — no AI hours, no further review.
The three design drafts and their reviews stay in the repo as a paper trail
of work already paid for; nobody looks at them again.

### Option B — FINISH-MINIMAL

Because this is under your own explicit pause with no waiver on record, **the
only honest "finish" step available today costs zero AI hours**: it is not a
repair or another review round (that is exactly what your ruling forbids
without a new waiver from you) — it is you saying, in one sentence, "this is
cancelled, don't revisit it" instead of leaving it in a paused/limbo state.
That single sentence is the entire task. Nothing else changes.

### Recommendation

**Option A (ARCHIVE).** It costs nothing either way, but "paused" already
behaves exactly like "cancelled" in practice — nobody is working on it and
nothing depends on it. A formal cancellation sentence is available any time
you want the record to say "done" instead of "paused"; there's no urgency to
decide that today.

---

## Item 2 — "Audit 2" (the second two-AI-flagship review programme)

### What it is

In the old project plan, before deploying, the whole system was supposed to
go through three big independent double-checks by two different AI models
working separately ("Audit 1", "Audit 2", "Audit 3"). Audit 2 was the middle
one — a review of the Linux server groundwork, capped by you at **6 hours of
review time**. A large amount of paperwork was assembled to get this review
ready to send out, but it was never actually sent.

### Where it stands

- A dedicated folder, `11_TRIAGE/AUDIT2_READINESS_PACKAGE/`, was built up over
  2026-08-09 through 2026-08-14 (roughly 20 documents: acceptance matrices,
  checklists, packet skeletons, gap maps). Its own status line has read
  **"NOT READY FOR DISPATCH"** through every refresh, most recently
  `AUDIT2_HANDOFF_PACKAGE.md` (2026-08-12 refresh): *"The package is still not
  dispatchable because WP-I is not closed."* That readiness folder is already
  present in the repo copy you're likely looking at (it doesn't need the
  other branch).
- On 2026-08-16 the underlying blocking checklist
  (`AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_PREREQUISITES.md`) was re-checked
  one more time: one of its six sub-checks ("Gate 2") was marked
  SATISFIED-WITH-DISCLOSURES, but the note is explicit — **"Gates 3–6 remain
  NOT SATISFIED"** — and Gate 3 is exactly the chain-lane freeze from Item 1
  above, which is paused with no accepted version. Source:
  `AUDIT2_READINESS_PACKAGE/AUDIT2_GATE2_REDERIVATION_2026-08-16.md`.
- The last full status table across the whole project
  (`11_TRIAGE/REMAINING_TASK_REGISTER_2026-08-16.md`, built the same
  afternoon) still lists Audit 2 as **"OPEN — Blocked behind freeze."**
- Separately, and more importantly for the actual deployment: the real Bridge
  release you're about to install already went through its own independent
  two-AI-flagship review and passed
  (`11_TRIAGE/BRIDGE_RELEASE_T0_ACCEPTANCE_2026-08-16.md`) — through a
  different, more direct route than the old Audit-2 plan. That's the review
  that actually matters for the pending install; Audit 2 was never on its
  critical path.

### Option A — ARCHIVE

Leave the readiness folder exactly as it is (it's already useful — it fed
directly into the Gate-2 re-check above and other accepted records, so
nothing already spent is wasted). Do nothing further. Spend: **nothing**.

### Option B — FINISH-MINIMAL

A single short paperwork note (roughly 1 hour of Lead time, no new AI review
dispatch, no host access) stating plainly: (1) Audit 2 as originally planned
will not run, because the deployment is no longer taking the route that
needed it; (2) the actual release got equivalent independent review through
the direct acceptance record cited above; (3) the handful of "carry forward"
disclosures the readiness work flagged (a few known caveats about RP6,
transport, and Pathscope evidence) get copied into wherever the standing
Bridge risk-disclosure list lives, so they aren't silently lost. This does
not reopen or resume anything — it only writes down what already happened.

### Recommendation

**Option B (FINISH-MINIMAL).** The closing note is close to free (an hour of
writing, no AI review spend, no dispatch) and removes a loose thread — right
now, anyone reading the readiness folder would reasonably think Audit 2 is
still "coming soon." If you'd rather not spend even that hour right now,
Option A is a completely reasonable "later" choice — nothing forces this
decision before the KVM2 install.

---

## Item 3 — "WP-A" (the DISARMED-VPS safety-evidence checklist pass)

### What it is

A bounded, 3-hour paperwork-and-testing task from the old plan: go through a
short list of safety requirements for running the Bridge un-armed on a server
(does it restart safely, can its data be backed up and restored, can a bad
update be rolled back, etc.) and confirm, one by one, that existing code and
tests already prove each one — flagging anything that's actually missing. It
was designed to run on a disposable practice server, one step before freezing
the final release for install.

### Where it stands

- Formally authorized as part of the 50-hour project plan you ratified on
  2026-07-30/31
  (`09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED
  IMPLEMENTATION PLAN.md` §19), budgeted 3 hours plus a shared 6-hour audit
  reserve, scheduled to run after Audit 2 (Item 2) and the chain-lane freeze
  (Item 1) both closed, on a disposable Ubuntu test server that was to be kept
  around specifically for this step.
- **It never started.** No practice-server run for this task exists in the
  records. `11_TRIAGE/REMAINING_TASK_REGISTER_2026-08-16.md` lists "WP-A +
  final freeze + Audit 3/Gate 6" as **OPEN**, tied to a "final freeze" step
  that, in the meantime, happened a completely different way (see below).
- The reason it never started isn't neglect — it's sequencing. WP-A needed
  Audit 2 to finish first, Audit 2 needed the chain-lane freeze to finish
  first, and the chain lane is the item you paused in Item 1. It was never
  reachable.
- Separately, and this is the important practical point: **the actual KVM2
  deployment plan you're about to sign already contains its own real safety
  checks that cover much of the same ground** — a rollback rehearsal, a
  backup/restore test, a monitoring baseline check, and a clean-inventory
  re-check, all run directly against the real target server instead of a
  disposable stand-in (`11_TRIAGE/KVM2_DEPLOYMENT_PLAN_62BF661B_V2_2026-08-16.md`
  §5, carried forward into the current plan version). This happened through
  the faster route the accelerated-completion decision put in place
  (`11_TRIAGE/OWNER_DECISION_ACCELERATED_COMPLETION_2026-08-16.md`), which
  explicitly deprioritized exactly this kind of extra formal audit layer for
  ordinary paperwork while keeping the full safety standard for anything that
  touches money, credentials, or the live host.

### Option A — ARCHIVE

Mark WP-A as "not run — superseded by the real deployment plan's own
verification steps." Nothing further happens. Spend: **nothing**.

### Option B — FINISH-MINIMAL

*After* the pending KVM2 install actually happens and passes its own checks,
one short pass (about 1 hour, one AI dispatch, no extra host access beyond
what's already granted) writes a short note matching WP-A's original safety
checklist against the operational evidence the real install produced — reusing
the checklist idea as a paperwork cross-check on real evidence, instead of
running new tests on a disposable stand-in server. This is a nice-to-have for
your own peace of mind; it doesn't gate or delay the install in any way.

### Recommendation

**Option A (ARCHIVE).** The real deployment plan's own verification steps
already cover the operational ground WP-A was meant to cover, on the actual
server rather than a practice one — which is stronger evidence, not weaker.
Option B is worth keeping in your back pocket only if you specifically want a
written "yes, we checked every safety box" document after the install; it
isn't needed to trust the install itself.

---

## OWNER ASK — plain language

Three quick decisions. Answer each with **A** or **B** whenever you get a
chance — none of these block the pending KVM2 install.

1. **The paused two-commit design work** — leave it paused forever as-is
   (**A — recommended**), or formally say "cancelled, don't revisit" in one
   sentence right now (**B**)?
2. **The unfinished second big double-check review** — leave the paperwork
   folder as-is and never touch it again (**A**), or spend about an hour
   writing one closing note saying it's not happening and why (**B —
   recommended**)?
3. **The unstarted safety-checklist pass** — mark it "not needed, the real
   install's own checks cover it" and stop (**A — recommended**), or, after
   the install succeeds, spend about an hour writing a short safety
   cross-check note for your own records (**B**)?
