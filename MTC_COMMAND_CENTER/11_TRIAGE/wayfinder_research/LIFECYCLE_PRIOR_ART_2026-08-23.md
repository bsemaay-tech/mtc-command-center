# Research: How Systematic Trading Shops Run the Strategy Lifecycle

Wayfinder ticket: [#57](https://github.com/bsemaay-tech/mtc-command-center/issues/57) (parent map: #54)
Date: 2026-08-23
Method: public, unauthenticated web research (practitioner books/blogs, quant-fund engineering writing, academic capacity/decay literature, one official broker incubation program). No logins, no paywalled/authenticated sources used.

## Question

How do serious systematic-trading operations structure the strategy lifecycle — incubation, production, suspension/demotion, retirement, re-entry, and succession (replacing a live strategy with a refreshed version) — and what governance sits at each boundary?

---

## Recurring Patterns

### 1. A near-universal staged pipeline, even when firms never write it down as one diagram

Every source describes some version of the same shape, whether it's an internal quant-fund research pipeline or a retail-facing broker program:

**Research/backtest → validation (capacity, decay, correlation, regime checks) → paper/shadow trading (live data, no real capital) → staged live deployment (small capital, scales up) → continuous monitoring → weight reduction on underperformance → decommission.**

The `Quant Enthusiasts` Substack pipeline description and FTMO's own two-stage program (Challenge → Verification → Funded Account) are structurally the same idea wearing different clothes: neither lets a strategy/trader touch full size until it has cleared a prior, cheaper-to-fail gate. The expensive resource (real capital, real market impact) is always the last thing granted, not the first thing tested.

### 2. Demotion/suspension triggers split into two families: statistical (automatic) and narrative (human-judged)

- **Statistical/automatic triggers**: breach of a pre-committed loss limit (FTMO: 5% max daily loss / 10% max total loss on the 2-step program — breach is evaluated mechanically against pre-set numbers, no discretion described in the official rules page), or a live Sharpe/drawdown falling outside the distribution implied by the backtest. The Bayesian stop-loss literature (Zambelli, arXiv:1609.00869) formalizes this: fit the historical distribution of maximum drawdown vs. subsequent return, and treat "further outside that distribution than history supports" as the trigger, rather than an arbitrary round number.
- **Narrative/judged triggers**: the practitioner consensus (Harbourfront Quantitative Finance newsletter, "When Trading Systems Break Down") is that a raw drawdown number alone cannot distinguish *normal variance* from *genuine decay* — you need to ask *why* returns degraded. They name four decay mechanisms explicitly: **alpha crowding** (slow Sharpe decline as costs rise), **regime drift** (slow Sharpe decline, costs stable), **microstructure change** (sharp step-down), and **capacity saturation** (the fund's own growth eating the edge). Each mechanism implies a different response — crowding/saturation may mean cutting size, not killing the strategy; microstructure step-down usually means killing it fast.
- The **honest failure mode named everywhere** is treating a strategy that's "just in a drawdown" as broken (premature kill, throws away real edge) or treating a genuinely broken strategy as "just a drawdown" (rides it to zero). Every source that addresses this explicitly says the distinction is the whole problem, not a solved one.

### 3. A successor version is validated *next to* the incumbent, not *instead of* it

This is not a trading-specific pattern — it's the general "champion/challenger" pattern from production ML/decisioning systems (DataRobot's MLOps writeup is the clearest public description), and it maps directly onto strategy succession:

- The incumbent ("champion") keeps running and keeps being the thing whose track record is being written.
- The candidate ("challenger") runs in **shadow mode** on the same live data/market conditions, producing decisions that are logged and compared but never executed with capital.
- Promotion requires a **designated approver** to authorize the swap, based on a comparison window with defined metrics — not an automatic cutover the moment the challenger looks better on a few days of data.
- Critically: **the incumbent's historical record is never overwritten** — the old evidence stays queryable as its own row/series after the swap, so a wrong promotion decision is unwindable and auditable after the fact.

The direct trading-domain equivalent of this is: never edit a live strategy's Pine/code in place and call it "the same strategy" — a genuine v2 is a new strategy ID with its own equity curve, run in parallel (paper or shadow) against the still-live v1 for a defined window, promoted only when it clears an explicit bar, with v1's own track record left intact and separately queryable afterward.

### 4. Re-testing a previously rejected idea is treated as *normal*, gated by *what changed*, not by embarrassment

None of the sources found describe a formal "cool-off period" or committee process specifically for resurrecting rejected ideas. What they describe instead is a **standing regime-stability check that is already part of the normal validation pipeline** — the same "does this hold up across regimes/time periods" step that screens new ideas also naturally re-admits an old, previously-failed idea if the regime that killed it has since changed (rate regime, market microstructure, a specific competitor's capital flow). The implicit rule found across sources: re-testing is legitimate exactly when you can name the specific external condition that changed since the rejection — not on a schedule, and not because someone "has a feeling."

### 5. Governance concentrates at two boundaries: entry-to-real-capital, and kill/demote — everything else can be automatic

Across every source, the two moments that reliably get a human/committee decision (rather than a pure numeric rule) are: (a) **first dollar of real capital** (moving from paper/shadow to live, or from Challenge to Funded), and (b) **judgment calls on ambiguous decay** (is this crowding, regime drift, or genuinely broken — see pattern 2). Everything in between — position sizing via volatility targeting, forecast/signal weighting, mechanical stop-limit breaches — is described by Carver and the Quant Enthusiasts pipeline as something firms deliberately push into automatic, rules-based execution specifically *so that* the scarce human judgment budget is reserved for the two boundaries above. FTMO is the cleanest illustration of a fully mechanical version of trigger (a): the published rules give exact numeric thresholds with no discretion described.

---

## Sources

1. **Bailey, D. H., Borwein, J., López de Prado, M., & Zhu, Q. J. (2017), "The Probability of Backtest Overfitting"** (SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253 ; also https://scholarworks.wmich.edu/math_pubs/42/). Academic (Journal of Computational Finance). Formalizes why testing many strategy variants and picking the backtest winner degrades expected out-of-sample rank, and proposes Combinatorially Symmetric Cross-Validation (CSCV) to estimate the probability a given backtest is overfit. Relevant to: how a shop should discount backtest evidence before ever letting a strategy into incubation, and why "it beat the old one in backtest" is not sufficient grounds for succession.

2. **Frazzini, A., Israel, R., & Moskowitz, T. J. (AQR Capital Management), "Trading Costs of Asset Pricing Anomalies"** (AQR working paper: https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies ; SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2294498). Practitioner/academic, ~$1T of live AQR trading data. Shows real trading costs are far below prior academic estimates and that strategy *capacity* (how much a strategy can scale before it eats its own edge) varies hugely by style — directly relevant to "capacity saturation" as a decay/demotion trigger named in pattern 2.

3. **Harbourfront Quantitative Finance (newsletter/Substack), "When Trading Systems Break Down: Causes of Decay and Stop Criteria"** (https://harbourfrontquant.substack.com/p/when-trading-systems-break-down-causes ; mirrored at https://derivvaluation.medium.com/when-trading-systems-break-down-causes-of-decay-and-stop-criteria-3c9e13cbd56d), Sept 22, 2025. Practitioner quant-engineering blog. Names the four decay mechanisms (alpha crowding, regime drift, microstructure change, capacity saturation) and states explicitly that a decommissioned strategy's own post-mortem is "the most informative dataset about the decay process" — i.e. retirement should feed back into the research process, not just end it.

4. **Robert Carver, *Systematic Trading: A Unique New Method for Designing Trading and Investing Systems*** (Harriman House, 2015; publisher page https://harriman-house.com/authors/robert-carver/systematic-trading/9780857194459) plus his ongoing practitioner blog **"This Blog is Systematic"** (https://qoppac.blogspot.com/). Carver is a single, non-institutional systematic futures trader (ex-AHL) who publishes his actual forecast-weighting, volatility-targeting, and risk-reduction rules in public. This is the closest published analogue to a one-person owner-gated operation: no committee, but explicit written rules that stand in for one.

5. **FTMO, official "Trading Objectives" page** (https://ftmo.com/en/trading-objectives/). Primary source, broker-run trader/strategy evaluation ("incubation") program. Publishes exact numeric stage gates (10% profit target, 5% max daily loss, 10% max total loss, minimum 4 trading days) across a 1-step or 2-step Challenge → Verification → Funded Account structure, with breach of a loss limit stated as grounds for termination. Useful as the cleanest public example of a **fully mechanical, non-discretionary** stage-gate design — no human committee sits between the numbers and the consequence.

6. **DataRobot, "Introducing MLOps Champion/Challenger Models"** (https://www.datarobot.com/blog/introducing-mlops-champion-challenger-models/), June 19, 2020. Engineering/MLOps blog (general production-model governance, not trading-specific, but the pattern is domain-general and is the clearest public description of the succession mechanism). Describes shadow-mode candidate evaluation, a designated-approver promotion gate, and preserved historical comparison data for the outgoing model — the mechanism referenced in pattern 3 above.

Supplementary (used for cross-checking, not separately relied on as load-bearing): "How Quant Hedge Funds Actually Build and Vet Trading Signals," Quant Enthusiasts (Substack), Apr 13, 2026 (https://youngandcalculated.substack.com/p/how-quant-hedge-funds-actually-build) — describes the same research→validation→paper→staged-live→monitor→decommission pipeline as pattern 1, with a note that continuous monitoring triggers "automatic reduction of weight" before full decommission; and Zambelli, A., "Determining Optimal Stop-Loss Thresholds via Bayesian Analysis of Drawdown Distributions" (arXiv:1609.00869, https://ar5iv.labs.arxiv.org/html/1609.00869) — the drawdown-distribution method cited in pattern 2.

---

## What maps to a one-person owner-gated operation

The owner here is a single non-technical person, not a committee. Every source above assumes either a firm with multiple staff (research team, risk desk, an "approver" role distinct from the researcher) or a broker enforcing rules on someone else's account. None of that structure exists here, and it shouldn't be faked. What *does* transfer is the underlying logic, translated:

- **Stage structure transfers directly, roles do not.** Incubation → paper/shadow → small-live → full-live → watch → retire is a sound shape regardless of who runs it. What changes for a one-person operation is that every stage transition needs to be a **pre-written, numeric gate the owner can eyeball and approve with one glance**, not a debate. If the gate can't be reduced to "yes/no, here's the number," it isn't ready to be a gate for a non-technical single owner — write it as a checklist item with a single pass/fail number, the way FTMO's rules page does, not as a narrative judgment call.

- **Split triggers into "automatic" and "owner must decide," and keep the second bucket as small as possible.** Pattern 5 above is the direct translation target: a committee's job splits into (a) mechanical, rules-based triggers that don't need a human at all — max daily loss, max total loss, minimum live-days-before-scaling, correlation/decay-metric breach past a stated number — and (b) the ambiguous "is this crowding/regime-drift or is it actually broken" judgment call. For a solo owner, (a) should be fully automated (the dashboard/bridge enforces it, no click required) and (b) should be the *only* thing that ever produces a "the owner needs to look at this" notification. If everything is escalated to the owner, the gate structure has failed at its one job — reducing decision load for a non-technical person.

- **Succession without destroying evidence = literally just "give v2 its own ID and let it run next to v1."** The champion/challenger mechanism (pattern 3) needs no committee to work — it needs exactly one discipline: never overwrite a live strategy's own record. A v2 is a new row (new strategy ID, own equity curve, own trade log) that runs in shadow/paper against the still-live v1 for a pre-agreed window; only the owner's explicit "promote" action swaps which one gets capital, and v1's full history stays queryable afterward whether it's promoted, demoted, or retired. This is a data-modeling requirement (don't let a "strategy" record be mutable in place across a material logic change) more than a governance requirement, and it's cheap to build in from the start and expensive to retrofit.

- **Re-testing a rejected idea needs one written rule, not a process.** Translate pattern 4 as: a previously rejected strategy is eligible to be re-run through incubation only when the owner can name, in one sentence, the specific external thing that changed (a new data source, a materially different regime, a fixed bug in the original test) — logged next to the old rejection note. This keeps re-testing possible without turning into "I have a feeling this will work now," which is the actual risk for a solo, non-technical owner who might otherwise re-try a dead idea out of optimism rather than evidence.

- **The one place a single owner cannot substitute for a committee: catching their own blind spots on judgment calls.** Firms use a second desk/committee partly because one person's read on "is this really decayed" is unreliable. A solo owner has no equivalent second opinion available in the moment. The practical mitigation implied by the decay-mechanism literature (pattern 2) is procedural, not organizational: force the ambiguous case through the same four-mechanism checklist (crowding / regime drift / microstructure change / capacity saturation) every time, in writing, before deciding — a poor-man's second opinion that at least prevents a snap judgment from skipping the reasoning a committee would have forced.

---

## Open questions this research does not resolve

- No source gives a concrete, generalizable numeric threshold for "how much drawdown beyond backtest-implied is a hard stop" outside of retail prop-firm rules (which are calibrated to protect the *broker's* capital, not necessarily to correctly classify decay vs. variance) and one thin academic method (Zambelli) with a stated ~43% underperformance rate against the base strategy in testing. Any concrete numeric bar adopted here will be a judgment call dressed as a number, not a proven constant — worth stating explicitly rather than implying false precision.
- Nothing found describes a formal "cool-off" period before re-testing a rejected idea at any real shop; the "re-test when something specific changed" rule above is this researcher's synthesis of the regime-stability-check pattern, not a directly cited practice.
