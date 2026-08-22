# OWNER MASTER PLAN

**Date:** 2026-08-22
**Voice:** mine — the owner. Plain English, first person, no technical schemas. This is the short version of what I want and in what order.
**Status:** **planning only.** The technical brief has been repaired but **audit acceptance is still PENDING**. **Implementation, deployment, trading and spending are UNAUTHORIZED.** This document authorizes nothing.
**Companions:** `PROJECT_STARTING_POINT_AND_MAIN_OBJECTIVE_2026-08-22.md` (my starting point and the canonical list of what I asked for) · `REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md` (all 56 tracked requirements, one row each) · `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md` (how the work divides into bounded packages) · `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md` (the technical brief, v2.1, repaired, not yet accepted).

---

## 1. Where I stand today

**Bridge V1 is reported DISARMED on my Hostinger VPS, and it stays that way until I say otherwise. That report has not been verified from this machine.** The repository records say the Bridge was deployed and is running disarmed. Nobody has contacted the host to confirm it, because host contact was not authorized. So the *record* is confirmed; the *running process* is not, and neither is its version, its configuration or its database schema version.

That is the honest starting line, and everything in this plan sits on top of it. **The goal comes before Bridge V2 begins, not after.** Writing down what I want — and getting it checked — is the last thing that happens before real work starts.

What else is true today:

- The trade logic that decides what a position is exists in **five separate places**: my Pine strategy, the MTC_V2 Python kernel, a second Python backtest engine, the research simulator and the live Bridge. Nothing forces them to agree.
- The research engine that produces my promotion numbers **does not simulate most of the controls the live system enforces**. Its results describe a different economic system from the one that would actually trade.
- The per-trial detail I want to look at is **computed and thrown away by the main promotion engine** — the one that produces the numbers I actually promote on. Other tools in the repository do persist parts of it, but **no single queryable catalog of trials exists**, and until one does, the explorer I want cannot be built from today's data.
- The repository has **zero tags**, and my own live-trading gate requires a frozen tagged commit. It currently cannot produce one.
- The Bridge itself is **genuinely well built**, and that is why the plan keeps it rather than replacing it.

**No live-capital authorization has been given, and the Bridge is reported DISARMED — but that is a record, not a verified fact: the deployed state has not been contacted or verified from this machine.** Nothing has gone wrong that I know of. This is the moment to fix the foundations, before real money is anywhere near it.

## 2. What I want the platform to be

**One trading platform that carries an idea from research all the way to live trading, where the numbers I see in a backtest actually mean something about what will happen with real money.**

I am not a programmer. I need to run this, understand it and stop it without typing commands. I trade on bar close, on timeframes from 15 minutes to daily, one position at a time per strategy. I am not building a high-frequency system and I do not want the complexity of one.

The whole plan reduces to three "one"s:

```
   IDEA -> RESEARCH -> FROZEN PACKAGE -> FORWARD SHADOW -> PAPER / TESTNET -> LIMITED LIVE
                        (permanent id)    (no orders)      (fake / test money)   (max 1% capital)
     |                        |                 |                  |                  |
     +--- ONE strategy brain -+-----------------+------------------+------------------+
     +--- ONE risk allocator -+-----------------+------------------+------------------+
     +--- ONE evidence trail -+-----------------+------------------+------------------+
```

**On the last step, "max 1% capital" means the maximum capital allocated to that one strategy — it is not a loss limit. How much a stop-out is allowed to cost me is a separate and lower limit, and it must be set and evidenced before anything goes live.**

**How the requirements are counted.** There are **56 tracked requirements = 44 original outcomes I asked for (O-01 to O-44) + 12 owner-acknowledged derived safeguards (D-01 to D-12)**. The 44 are mine, in my wording and my order. **The 12 are not mine.** They came out of the architecture and audit work. **On 2026-08-22 I acknowledged all twelve — ten as written, and D-02 and D-07 with clarifications recorded in the starting-point file §4 and the register §3.** Acknowledging them does not make them my requirements: they stay derived, and no document may present them back to me as if I had requested them. **Nor does acknowledging them authorize anything to be built, accept the technical brief, or permit any deployment or live trading** — those are the separate approvals in §9. Repository findings — what the audit discovered — are evidence, not requirements, and are never counted in the 56. The full row-by-row list lives in the traceability register; I do not repeat it here.

## 3. What I want to see on screen

Two separate surfaces, deliberately not merged:

**A research explorer.** Read-only, no credentials, no way to touch money. I want to filter and sort every trial that was ever run, see the exact parameters, the key statistics, the equity curve against buy-and-hold, the drawdown, the walk-forward and robustness results — and, above all, **the reason a candidate was rejected**, without asking an AI to summarize it for me. A small version of this comes early, because it is the first thing that gives me something to look at. The advanced version comes later.

**An execution dashboard.** Authenticated, and audited separately from research. It must show me **what the strategy wanted, what was authorized, and what actually happened at the exchange as three separate columns** — never merged into one comforting number. It shows how stale each panel is, why anything is blocked, and it carries ARM, DISARM and KILL behind proper protection. I want to read it on my desk and later on my phone.

**A TradingView-like chart inside it**, showing positions, entries, exits, stop loss, take profit, Multi-TP and trailing stops as they actually moved. Eventually I want to **drag those levels with the mouse** — first in pure simulation, then on paper/testnet, and only much later on live money behind strict controls. The chart library gets chosen by a small proof of concept, not by preference.

## 4. One strategy brain, one set of rules

**One authoritative Python strategy kernel**, imported by the backtest, the forward runs, paper and live. Not five versions that quietly disagree.

Getting there in the right order matters more than getting there fast:

1. **Map the overlaps first** between MTC_V2, QuantLens, the backtest engines and the Bridge, and decide where each responsibility belongs — strategy behaviour, account protection, order execution, broker-specific rules — so nothing is implemented twice again.
2. **Simplify MTC_V2**: essential strategy and position management in the core; advanced filters, exits and experiments become optional or retire.
3. **Build the kernel in two steps.** First an exact reproduction of the current behaviour, **including its known defects**, proven bit-for-bit. Then, separately and under a new version, the deliberate fixes — each with a record of what was wrong, evidence of before and after, and a test that is shown able to fail. No undocumented difference between the two steps is allowed.
4. **Versioned contracts** for signals, size requests, approved quantity, stops, targets and order instructions, so components agree by definition instead of by hope.
5. **Pine stops being a second order controller.** I have decided this; it is monitoring and divergence warnings only. **The decision is not the authorization** — the actual edit is prepared as a package I can approve or refuse, and until I approve it the old live order path stands.

## 5. Money safety: risk buckets, sizing and the Guardian

I want strategy-level rules and account-level protection kept apart.

- **Risk buckets** — day, swing, position — each with its own view, capital budget and risk limits. **The actual numbers are not set yet**; any split proposed so far is a simulation hypothesis, not my decision.
- **Every bucket starts at 1x leverage.** Increases require evidence, and each one is a new decision by me.
- **One shared risk allocator** computes quantity, and **the same code runs in the backtest and in production**. If the allocator is built but never simulated, the design is worse than what I have now — that is the single failure I most want prevented.
- **The Portfolio Guardian only authorizes or rejects.** It never silently resizes an order. Every rejection carries a readable reason.
- **What "no resizing" does and does not mean.** It is a rule about **sizing a new order**: the Guardian may not quietly hand the exchange a different quantity from the one the allocator proposed. It is **not** a ban on ever reducing or closing a position I already hold in an emergency. If such a thing is ever built, it is **its own explicit, separately authorized, tested safety policy with a visible reason** — never a silent resize. **Writing this down authorizes neither building it nor using it**, and the detailed design belongs to later work.
- **The stop is a real reduce-only order at the exchange**, so protection survives the trading process being killed — and the backtest models it the same way.
- **Fail closed.** If the account picture the system sized against is stale or inconsistent, nothing is submitted.
- **No false diversification.** Family, overlap and correlation caps, applied at promotion and at runtime — and simulated, not just enforced live. A breach rejects; it never quietly trims.

## 6. How a strategy earns its way to real money

One connected ladder, walked in order, with no shortcuts:

**Discovery → source extraction → testing → statistical validation → freeze → forward shadow → paper/testnet → portfolio test → limited live → scale, suspend or retire.**

The rules I care about most:

- **Test the original source rules separately from my enriched version**, so I can see where the edge actually comes from.
- **Missing rules get written down, not invented.** They may be completed only from a small standard catalogue, and the gaps travel with the candidate in a ledger.
- **A missing stop or target does not automatically block forward observation** — but it does block live capital until the substitute has evidence.
- **Freeze before the forward clock starts.** Any code, parameter or module change creates a new package identity and a new evidence period. No exceptions, because that is the only thing that makes forward evidence mean anything.
- **Forward shadow starts early and runs in parallel** with the slower statistical work. Two constraints bind at once — finding a statistically credible candidate, and the passage of calendar time — and neither can substitute for the other.
- **Many candidates into shadow; far fewer onto exchange testnet**, and the testnet fleet size is set by measured exchange limits and reconciliation reliability, not by a number someone picked.
- **Promotion produces a permanent decision record**, created on its own screen, separate from the explorer. Execution can load **only** frozen packages traceable to such a record.
- **First live deployment is deliberately tiny**: one strategy, at most 1% of the account, behind a gate I sign myself. **To be exact: the 1% is the maximum capital allocated to that strategy. How much a stop-out is allowed to cost me is a separate and lower limit, and it must be defined and evidenced before I authorize anything live. No number is invented for it here.**

## 7. Research I can look at

- **One compact record per trial** — parameters, results, rejection reasons — written in a format that does not depend on which optimizer produced it. Full artifacts kept for selected candidates; the rest reproducible on demand.
- **Storage is budgeted**, with a retention rule and protected classes, so this cannot grow without limit.
- **The optimizer choice is decided by measurement**, comparing what I have now against the alternative, not by what happens to be installed.
- **Historical backtest results get classified by what their simulator actually modelled.** Useful evidence is kept; a signal screen is never treated as a live-profit estimate.
- **The parity question gets answered before any parity number is quoted.** One corpus says 27 of 58 strict matches, another says 437 of 439. Until an inventory establishes what each one tested, neither figure may be presented as "our parity".

## 8. Tools, repository and AI context

- **Cut the AI onboarding cost first.** Roughly 180,000 tokens of mandatory reading is charged before any AI does any work here. Each stage gets small local instructions, inputs, outputs, tests and a current handoff; history stays searchable but is not loaded by default. **The saving is measured before and after, numerically** — not asserted.
- **The shared contracts package is defined in place now.** Whether this becomes one repository or several is **deferred until the routing measurement exists**, and it is a separate decision.
- **Freeze points before anything moves**: tag namespaces, tags on everything that carries evidence, and a migration ledger where every move resolves in both directions.
- **Nothing is deleted.** Legacy code is frozen and tagged, the old structure survives as a read-only archive, and any branch cleanup needs an exact target list approved by me, with every target tagged first.
- **Open-source first, with review** — licence, quality, maintenance, security, integration cost. I prefer libraries and narrow adapters over importing an entire trading platform. Custom code stays where it earns its keep: strategy, risk, execution safety, reconciliation and operator workflow. Frameworks like NautilusTrader get bounded proofs of concept; **the hardened Bridge is not replaced for feature count.**

## 9. Phases, decisions and what I have to approve

**Phase 0 — Foundation.** Inventory and classify the repository; tags and migration ledger; contracts package; AI-context routing with measurement; kernel consolidation (exact reproduction, then documented fixes); the per-trial record and its writer; the Minimum Explorer; chart-library and optimizer proofs of concept; the Pine change prepared as a design only. *Non-goals: no new trading features, no Bridge behaviour change, no repository split, and the V1 soak is untouched.*

**V2A — the intent seam and one worker.** Frozen-package loading, one worker with its own identity and state, the shared risk allocator imported by the backtest on day one, fail-closed account snapshots, the Bridge executing an authorized instruction instead of inventing a quantity, **the native stop — written and proved on my own machine only, against a fake exchange, including killing the process and showing the protective order is still there**, and forward shadow on real feeds with **zero orders anywhere**. *Non-goals: no schema activation, no testnet orders, no contact with any exchange at all, no dashboard replacement, no dragging.*

**V2B — portfolio, fleet and operator surface.** Portfolio Guardian and risk buckets, portfolio backtesting on the same code, multiple workers, the live database schema activation behind its own separate authorization, Execution Dashboard V2, zero-trust access with step-up authentication, the exchange testnet fleet — **and this is where the native stop is finally tested against a real exchange, on testnet, with the process killed for real** — and dragging **in simulation only**. *Non-goals: no live capital, no resizing, no paper or live dragging.*

**V3 — evidence and promotion.** Advanced explorer, full artifact tiering and replay, Promotion Authority with a real registry, correlation and family controls, live-versus-backtest divergence reporting, Multi-TP on testnet, dragging on paper/testnet, the NautilusTrader proof of concept. *Non-goals: no live dragging, no new brokers in production.*

**V4 — real money, deliberately small.** The signed live gate, one strategy at 1% or less **of allocated capital — with the separate, lower loss-at-stop limit defined and evidenced as part of the live-gate evidence pack** — live dragging with the full safety chain, human-override accounting, calibrated multi-bucket operation, mobile monitoring. *Non-goals: no IBKR, no second live strategy until the first has a full evidence cycle.*

**V5+ — more venues.** IBKR behind the same broker boundary, an equity swing bucket with its genuinely new failure modes, a multi-venue portfolio view, and the repository split **only if the measurement says so**.

**What runs in parallel.** Phase 0 is organized into six workstreams — inventory and evidence; freezing and structure; AI context; kernel consolidation; research data and the viewer; isolated proofs of concept — but **they do not all start together.** Only work whose dependencies are already met runs at the same time. In practice the first wave is the independent inventories, the contracts package, the AI-context measurement and design, and the isolated proofs of concept. **The AI-context change touches shared governance and lands on its own**, once, measured before and after. **Kernel work waits for the contracts and the parity truth, and never runs in parallel with itself** — two people editing trading semantics at once is exactly how an accidental blend of two engines gets created. The research-data work uses the contracts as they are defined; it does not redefine them. The main dependency chain is: contracts and parity truth → kernel → allocator → intent seam → equivalence test → forward shadow → Guardian → dashboard → promotion → live gate.

**The four approvals, which are not the same thing.** This distinction is the one I most want protected:

1. **Decision approval** — I answer a question (for example, that Pine stops routing orders). **My acknowledgement of the twelve derived safeguards on 2026-08-22 sits on this axis and only this one.** It records that I have read them and accept them as constraints; it does not build them, accept any document, or permit any deployment.
2. **Audit acceptance** — an independent review accepts a document as sound. *Currently PENDING for the technical brief.*
3. **Implementation authorization** — I authorize a specific package to be built. **Every package needs this, not only the dangerous ones**, and an accepted document never supplies it. *None given.*
4. **Host, testnet and live authorization** — separate again, one act each: contacting the VPS; changing the live database schema; using testnet credentials; committing real capital; and any destructive Git operation. *None given.*

**A decision is never an authorization, and a document is never an approval.** Nothing in this plan starts because this plan exists. The technical brief is repaired but still waiting on acceptance; implementation, deployment, schema changes, credentials, testnet, live trading and spending each require my explicit word at the time, separately, for the specific thing being done.
