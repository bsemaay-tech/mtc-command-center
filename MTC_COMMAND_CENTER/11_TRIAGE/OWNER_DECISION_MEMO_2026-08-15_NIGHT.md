# W11 — Owner decision memo: three open questions

**For:** Barış · **From:** Lane W11 · **Date:** 2026-08-15 (night)
Each item needs one sentence from you. This memo decides nothing and authorizes nothing.

**Sources** (cited as `KEY:line`). PAR and DEC are in the repo working copy. ADP and CTT are **not** in the checked-out copy — they exist only on branch `codex/rp7-r1-r4-repair-20260815` (ADP at commit `32e28889`, CTT at `885ea979`), read via read-only `git show`:

- **PAR** `MTC_COMMAND_CENTER/11_TRIAGE/PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md`
- **ADP** `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md`
- **CTT** `MTC_COMMAND_CENTER/11_TRIAGE/CUTOVER_TABLETOP_AND_CLEAN_START_PROOF_2026-08-15.md`
- **DEC** `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md`

## 1 — Which plan governs the deployment

Two plans describe the same server deployment: the 50-hour plan you approved on July 31, and the older July 25 KVM2 plan family. Neither says it replaces the other, and no owner decision on record picks a winner (PAR:11, PAR:86). Until you ratify one reading, the team may only do read-only analysis — no checkpoint may be declared closed (PAR:160).

**Option A — follow both plans together.** Costs you more sign-offs and elapsed time, possibly two final reviews where one cannot be worded to satisfy both contracts; no combined hour total exists (PAR:136). Its known failure mode: someone claims one piece of evidence closes a check in both plans when it does not (PAR:138) — the reply sentence below forbids exactly that.

**Option B — follow only the KVM2 plan.** Not guaranteed cheaper (PAR:154). You lose the 50-hour plan's protections — its Audit 1/2/3 review checkpoints, the final freeze-and-review before installation, and owner acceptance at the end; reaching installation without those reviews is its stated risk (PAR:152, PAR:156).

**Recommendation: Option A.** Single strongest reason: it is the only reading in which no safety check from either plan can be silently dropped — the extra price is your attention and calendar, not safety (PAR:132-136).

**Reply with (verbatim, PAR:164):**
> "I ratify the cumulative reading: the 50-hour §23a sequence and KVM2 Phases 0–4 plus all ten Bridge VPS Deploy Task List items are jointly mandatory, and one artifact, test, audit, or owner sentence may close gates in both only when its record explicitly names and satisfies both contracts."

Plain words: both checklists apply; shared evidence counts for both only when the record explicitly says so.

## 2 — The six-hour audit budget

The plan reserves 6 hours total for every independent review of the deployment — Audit 2, Audit 3, Gate 6, and any re-audit. If the pool empties while a review is still needed, work stops and returns to you (a BLOCK) (ADP:7). Current rules require four review sessions before launch — Claude and Codex each for Audit 2, then each for the combined Audit 3/Gate 6, all at the most thorough setting (ADP:156). Six hours across four sessions is an arithmetic 1.5 hours each, with nothing left for any re-audit (ADP:156). Tonight's two real audits produced 361- and 373-line reports but recorded no running times, so **no honest replacement number exists — NO SOURCED ESTIMATE**; metering the Audit 2 sessions would settle it (ADP:154, ADP:162). UNKNOWN: whether the 6 h counts total work-hours or elapsed time; a written ledger interpretation would settle that (ADP:158).

**Option A — keep 6 h as a hard cap.** Cost: a real chance of a stop-and-ask moment mid-review.
**Option B — authorize a larger audit-only reserve.** Cost: no honest size can be named tonight; any figure would be invented (ADP:154). Repair money is a separate pool and must not be borrowed (ADP:162).

**Recommendation: Option A now, then re-price from measurements.** Strongest reason: a hard cap that trips fails visibly and is recoverable, while a number written tonight would repeat the invented-estimate error; the dispatch plan itself says to meter both Audit 2 sessions and price Audit 3/Gate 6 from those actuals (ADP:162).

**Reply with:**
> "The six-hour pool stays a hard cap and I accept BLOCK if it is exhausted; meter both Audit 2 sessions and bring me the measured actuals before Audit 3/Gate 6 so I can set that reserve on evidence, not a guess."

## 3 — Save the paper-period record before the fresh start?

You chose "start clean": the new server begins with empty history — no loss counters, no order history (DEC:93-101). That choice opened one question: before the fresh start, should the old PC's trading record (every paper trade, the loss ledgers, the order history) be copied somewhere safer first, or left where it is? (DEC:112-116; CTT:443-446.)

**Option A — archive it off the old machine first.** Cost: one capture, one verification, one copy — the tooling exists and is tested — plus choosing an encrypted storage place (CTT:465-466, CTT:458-459).
**Option B — leave it on the old PC.** Costs nothing now and is explicitly not a blocker for pre-cutover work (CTT:478-479) — but the old PC's disk becomes the only copy of the paper period, on the machine being retired precisely because its reliability is in doubt (CTT:450-456). UNKNOWN: no decommission date for that machine exists in any document read (CTT:480-481).

**Recommendation: Option A.** Single strongest reason: the asymmetry is total — an extra copy can be deleted later; a lost only-copy cannot be recovered once the old machine goes (CTT:492-493).

**Reply with (verbatim, CTT:495-497):**
> "Archive the pre-cutover risk-state bundle and raw cutover captures off-host, encrypted, before the fresh start; the recorded bundle and invariants hashes live in the cutover record."

Plain words: "risk-state bundle" is the verified saved copy of the old machine's risk record; the "invariants hashes" are its two tamper-check numbers, kept in your cutover paperwork.
