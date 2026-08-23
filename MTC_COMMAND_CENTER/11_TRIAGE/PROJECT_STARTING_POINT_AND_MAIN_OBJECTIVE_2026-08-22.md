# PROJECT STARTING POINT AND MAIN OBJECTIVE

**Date:** 2026-08-22
**Voice:** mine — the owner. Written in plain English, first person, so that any person or AI joining this project knows what I want before they read anything technical.
**Status:** planning document — **planning only · implementation UNAUTHORIZED · every work package NOT STARTED.** **Audit acceptance of the technical brief: DONE on 2026-08-23**, for the exact version recorded as commit `c81aacb8` and for nothing else. **That accepts a document; it authorizes no implementation, no deployment, no trading and no spending, and this file authorizes none of those either.**
**Status update, 2026-08-23:** I was shown D-13 to D-16 and **acknowledged all four as written**. All sixteen safeguards are now acknowledged — see §4.
**Companions:** `OWNER_MASTER_PLAN_2026-08-22.md` (my short plan in plain English, nine sections — it exists and sits alongside this file) · `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md` (the technical brief, v2.1, **repaired, and accepted at that one commit — its §0.7 holds the current status**) · `REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md` (the canonical list of **60** tracked requirements) · `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md` (how the work divides).

---

## 1. Where I am standing right now

**Bridge V1 is reported DISARMED on my Hostinger VPS, and Bridge V2 is about to begin. The runtime remains unverified locally.**

I want that sentence read carefully, because two of its three parts are weaker than they look.

- **"Reported"** means the repository records say the Bridge was deployed and is running disarmed. Nobody has contacted the host to confirm it as part of this work, because host contact was not authorized. The *record* is confirmed. The *running process* is not.
- **"DISARMED"** means it places no orders. That is the state I want it in until I say otherwise.
- **"Unverified locally"** means that from this machine, nobody has proven what version, what configuration or what database schema the deployed process is actually using.

So my honest starting position is: I have a well-built execution component that is very probably running safely and doing nothing, a large amount of research work behind it, and no independent confirmation of the live state. Everything below is built on that.

## 2. My original goal, unchanged

I want **one trading platform that carries an idea all the way from research to live trading, where the numbers I see in a backtest actually mean something about what will happen with real money.**

I am not a programmer. I need to be able to run this, understand it, and stop it, without typing commands. I trade on bar close, on timeframes from 15 minutes to daily, one position at a time per strategy. I am not building a high-frequency system and I do not want the complexity of one.

---

## 3. The 44 outcomes I asked for

These are my requirements, numbered **O-01 to O-44**. They are the outcomes I want, not instructions on how to build them. The technical brief and the work-package plan explain the *how*; this list is the *what*.

**Correction note, 2026-08-22.** An earlier drafting pass of this file printed a *different* list of 44 items, reconstructed from scattered sources. That reconstruction was wrong and has been removed. The list below is the canonical set of owner outcomes, preserved in the exact order and meaning in which I stated them. **This numbering is now fixed and must never be silently changed.** If a requirement is worded wrongly, it gets corrected in place with a dated note — it does not get renumbered, and no new requirement is added without my acknowledgement. The grouping headings below are for readability only; they do not change the order or the meaning.

### The platform I want to see and use (O-01 to O-03)

| ID | What I want |
|---|---|
| **O-01** | Build a modern dashboard that presents the whole system clearly. |
| **O-02** | Include a TradingView-like charting application inside the dashboard to display positions, entries, exits, SL, TP, Multi-TP and trailing stops. |
| **O-03** | Eventually allow SL and TP levels to be adjusted by dragging them on the chart, first in simulation, then testnet/paper, and only much later in live trading with strict safety controls. |

### One system instead of several overlapping ones (O-04 to O-10)

| ID | What I want |
|---|---|
| **O-04** | Find all overlaps and conflicts between MTC_V2, QuantLens, the existing backtest engines and Crypto Paper Bridge. |
| **O-05** | Simplify MTC_V2 by keeping only essential strategy and position-management capabilities in the core; make advanced filters, exits, transforms and experimental features optional or retire them. |
| **O-06** | Decide clearly where each responsibility belongs so strategy behaviour, account protection, order execution and broker-specific rules are not repeatedly implemented. |
| **O-07** | Create one authoritative Python Strategy Kernel used by backtesting, forward testing, paper trading and live trading. |
| **O-08** | Prevent TradingView/Pine from becoming a second order controller; allow visual monitoring and divergence warnings only. |
| **O-09** | Separate strategy-level rules from account- and portfolio-level protection; centralize account controls in a Portfolio Guardian. |
| **O-10** | Introduce versioned contracts defining signals, position-size requests, approved quantity, stops, targets and order instructions. |

### Running many strategies, and where they trade (O-11 to O-14)

| ID | What I want |
|---|---|
| **O-11** | Allow Crypto Paper Bridge to run multiple strategies simultaneously with isolated identities, state, positions and evidence. |
| **O-12** | Group strategies into risk buckets such as day, swing and position trading, with separate views, capital budgets and risk limits. |
| **O-13** | Start every risk bucket at 1x leverage; increases require evidence. |
| **O-14** | Trade crypto through Hyperliquid initially while designing the broker boundary for later IBKR and equity swing trading. |

### What we build versus what we adopt (O-15 to O-17)

| ID | What I want |
|---|---|
| **O-15** | Evaluate existing broker/trading frameworks such as NautilusTrader through bounded proofs of concept; do not replace the hardened Bridge merely for feature count. |
| **O-16** | Establish a permanent open-source-first policy with license, quality, maintenance, security and integration review. |
| **O-17** | Prefer libraries and narrow adapters over importing an entire trading platform; custom code focuses on our strategy, risk, execution safety, reconciliation and operator workflow. |

### The lifecycle from idea to real money (O-18 to O-26)

| ID | What I want |
|---|---|
| **O-18** | Redesign the complete lifecycle as one connected pipeline from discovery through source extraction, testing, validation, promotion, shadow, paper/testnet, portfolio testing, limited live, scaling/suspension/retirement. |
| **O-19** | Improve QuantLens strategy research so candidates pass early stages with fewer unnecessary steps. |
| **O-20** | Test original strategy rules separately from the MTC-enriched version and show where the edge comes from. |
| **O-21** | Record missing source rules and complete them only from a small versioned standard catalogue; never silently invent them. |
| **O-22** | Do not let missing SL/TP rules automatically block forward observation; do not grant live capital until substitutes have evidence. |
| **O-23** | Start forward-shadow observation early while slower statistical validation continues in parallel. |
| **O-24** | Freeze every strategy version before forward evidence collection; any code, parameter or module change creates a new package hash and evidence period. |
| **O-25** | Advance many suitable candidates into forward shadow while keeping exchange testnet/live-paper to a smaller capacity-controlled cohort. |
| **O-26** | Determine testnet fleet size from measured exchange limits, reconciliation performance and reliability, not an arbitrary count. |

### Seeing the research, and trusting what I see (O-27 to O-34)

| ID | What I want |
|---|---|
| **O-27** | Build a TradingView-like visual Backtest and Optimization Explorer. |
| **O-28** | Make 100,000-trial runs filterable and inspectable without manually entering settings into TradingView. |
| **O-29** | Show parameters, search space, candles, trades, SL/TP movement, equity versus buy-and-hold, drawdown, key statistics, walk-forward, robustness and rejection reasons. |
| **O-30** | Store one compact record for every trial; retain full artifacts for selected candidates and deterministically replay others. |
| **O-31** | Keep experiment and artifact formats optimizer-independent; compare Optuna before adopting it. |
| **O-32** | Maintain immutable candidate identity through the lifecycle; bind statistical, shadow, paper and live evidence to the exact package hash. |
| **O-33** | Create separate research and execution trust domains; research is read-only/no credentials and execution is authenticated and independently audited. |
| **O-34** | Run a chart-library proof of concept before permanent selection, especially for draggable levels, Multi-TP, trailing history and touch support. |

### Context, repository and migration (O-35 to O-39)

| ID | What I want |
|---|---|
| **O-35** | Redesign project AI context and AI_MEMORY for token efficiency before large V2 work. |
| **O-36** | Give every stage small local instructions, inputs, outputs, tests and current handoff; historical material remains searchable but is not loaded by default. |
| **O-37** | Record the original clean-repository/archive idea and its refinement: first implement and measure stage routing in the current repository before deciding topology. |
| **O-38** | Define the shared contracts package in place now; defer one-versus-multiple Git repository topology until measured. |
| **O-39** | Make any later migration selective and reversible; inventory and preserve the existing repository as a read-only archive, never delete it. |

### Consolidation, and honesty about history (O-40 to O-41)

| ID | What I want |
|---|---|
| **O-40** | Build the authoritative kernel through LEGACY_COMPATIBLE exact reproduction followed by separately documented and tested CORRECTED_VNEXT fixes. |
| **O-41** | Classify historical backtest results by what their simulator actually modelled; preserve useful evidence without treating signal screens as live-profit estimates. |

### The plan itself (O-42 to O-44)

| ID | What I want |
|---|---|
| **O-42** | Create one overall Master Plan divided into bounded subprojects, dependencies, decisions, acceptance gates and parallel workstreams. |
| **O-43** | Define what belongs in Phase 0, Bridge V2, V3, V4 and later; do not force every future feature into V2. |
| **O-44** | Before implementation, answer the owner decisions that materially affect kernel, contracts, Pine, sizing, migration, risk buckets, testnet capacity and chart selection. |

---

## 4. Sixteen audit-derived safeguards — all sixteen now acknowledged

**These are audit-derived safeguards. They are not requirements I asked for, and they are not part of my 44.** They came out of the architecture, audit and peer-review work. They are recorded as **D-01 to D-16**.

**On 2026-08-22 I acknowledged the first twelve.** D-01, D-03 to D-06 and D-08 to D-12 I acknowledged as written. D-02 and D-07 I acknowledged **with the clarifications printed in their rows below**. Acknowledging them does not make them mine: **they stay derived, they were never part of my original 44, and no document may present them back to me as if I had requested them.**

**Four more were added later the same day. I was shown them on 2026-08-23 and acknowledged all four AS WRITTEN.** A further review found seventeen problems in the document set, and closing four of them needed safeguards that no existing requirement covered. They are **D-13, D-14, D-15 and D-16**, printed at the end of the table below. **Nothing in their wording was softened or altered to get my word on them, and it does not change now.** They are enforceable as engineering constraints in the same way as the others, and — like the others — **they stay derived. They never become part of my 44, and no document may present them back to me as things I asked for.**

**So all sixteen are acknowledged: D-01 to D-12 on 2026-08-22, D-13 to D-16 on 2026-08-23.**

**And acknowledging a safeguard is not authorizing anything.** It does not authorize an implementation, it does not start any work package, and it does not authorize any deployment or live trading. It is also not the same as the technical brief being accepted — that is a separate act, which happened separately on 2026-08-23 for one exact version of the brief, and which likewise starts nothing.

| ID | Safeguard |
|---|---|
| **D-01** | Keep FORWARD_SHADOW, INTERNAL_PAPER, EXCHANGE_TESTNET and LIMITED_LIVE distinct, and label what each one actually proves. |
| **D-02** | In V2, one shared Risk Allocator computes quantity and the Guardian only authorizes or rejects; no silent resizing; the same allocator and policy run in the portfolio backtest. **My clarification: "no resizing" is about sizing a NEW order. It does not forbid a separately authorized emergency reduction or closure of exposure I already hold. That would be its own explicit, tested safety policy, never a silent resize — and saying this here neither builds it nor permits its use.** |
| **D-03** | Use a native reduce-only exchange stop as the V2 protection baseline. |
| **D-04** | Keep Promotion Authority separate from the Explorer; approval creates an immutable decision artifact. |
| **D-05** | Mark every operator intervention, and separate pure-strategy performance from operator-modified performance. |
| **D-06** | Show desired, authorized and actual execution state separately. |
| **D-07** | The first limited-live cohort is one strategy using no more than 1 percent of account equity. **My clarification: that 1 percent is the maximum CAPITAL ALLOCATED to that strategy. What I am willing to lose if the stop is hit is a SEPARATE and LOWER limit, and it has to be written down and evidenced before I authorize anything live. I am not putting a number on it here.** |
| **D-08** | Require economic golden scenarios and D026 RED/GREEN falsification for migration and parity claims. |
| **D-09** | Require freshness, idempotency, acknowledgement, reconciliation and emergency-recovery controls for money-moving operations. |
| **D-10** | Prevent false diversification through family, overlap, correlation and portfolio-cap controls that are also simulated. |
| **D-11** | Bind migration and deployment claims to exact accepted commits, package identities, simulator lineage and evidence. |
| **D-12** | Distinguish owner decision approval, implementation authorization, audit acceptance, and deployment/live authorization. |
| **D-13** *(added 2026-08-22 — **acknowledged by me AS WRITTEN on 2026-08-23; still DERIVED**)* | A research result only counts as evidence for promoting a strategy if it came out of the **one real simulator** — the kernel plus the shared risk allocator. Anything switched on must either be simulated by that same code or **listed by name as not simulated**, and if something important is on that list, **the strategy cannot be promoted.** *Why this was needed: the engine that currently produces my promotion numbers models almost none of the controls the live system enforces, and nothing in the plan was actually fixing it.* |
| **D-14** *(added 2026-08-22 — **acknowledged by me AS WRITTEN on 2026-08-23; still DERIVED**)* | Letting a strategy into shadow or testnet is its own **written, permanent decision**, made from **objective pass/fail checks** before anything is loaded, and it is **not** the same as approving it for real money — that stays with the Promotion Authority. If nothing has been admitted, **nothing loads**. *Why this was needed: the rules said only the Promotion Authority could admit a package, but the Promotion Authority arrives two phases after shadow and testnet need to run — so either nothing could start, or the rule would quietly be broken. And "acceptable repaint" is not a check anybody can fail.* |
| **D-15** *(added 2026-08-22 — **acknowledged by me AS WRITTEN on 2026-08-23; still DERIVED**)* | Watching one version of a strategy must not secretly shape its siblings. Family relationships are **recorded**, every human or machine look at forward data goes in an **append-only log**, and the "nobody looked at this" window is **calculated from that log, not claimed**. This has to be in place **before the first strategy is ever declared a live candidate.** *Why this was needed: this was written down as a known hole and left open, with its only owner being a design study scheduled after promotion.* |
| **D-16** *(added 2026-08-22 — **acknowledged by me AS WRITTEN on 2026-08-23; still DERIVED**)* | The way I stop the system must not have a single point of failure: **at least two separately registered security keys**, not both on the same device, each proven to work on its own — plus a **written and rehearsed way to close positions directly at the exchange** when my own software cannot be reached at all, timed against the five-minute target my own live gate sets. *Why this was needed: one lost or broken key would have left me unable to kill or flatten anything, on a machine with no public access.* |

Together with my 44, that makes **60 tracked requirements — 44 original owner outcomes plus 16 derived safeguards, all 16 of which I have now acknowledged and all 16 of which stay derived**. The register that tracks all of them is `REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md`.

---

## 5. What the repository audit discovered

**These are findings about the state of my repository. They are not requirements, and they must never be counted as requirements.** They are the reason some of the work below exists. Each one is verifiable from the technical brief, which cites the exact files and lines.

**Five separate implementations of trade logic.** The Pine strategy, the MTC_V2 Python kernel, a second Python backtest engine, the research simulator and the live Bridge each contain their own version of what a trade is. Nothing forces them to agree, and nothing tests end to end that they do.

**The engine that decides promotion does not simulate the controls the production system enforces.** The research simulator that produces my promotion-deciding numbers has no position sizing, no leverage, no break-even, no multi-target exits, no daily-loss guard, no drawdown guard, no cooldown, no entry filters. It fills stops exactly at the stop price with no gap modelling, and applies slippage only after the fact. So its results describe a different economic system from the one that would actually trade.

**The detail I want to look at is computed and thrown away.** The main research engine keeps the winning parameter set and some aggregate statistics per cell, and discards the individual trials and all the trade detail. Some other tools do save trades and per-evaluation rows — that part was overstated in an earlier draft and has been corrected — but there is no single queryable record of what was tried and why it was rejected. That is why no visual explorer could be built from today's artifacts at any price: the data does not exist yet.

**Position sizing disagrees between components.** The Pine strategy, the Python kernel and the Bridge each compute size differently — a contract-multiplier difference, a minimum-notional difference, a different source of instrument data, and a risk appetite of 1.0 % against 0.5 %. Nothing is wired together today, so nothing has gone wrong. It is a loaded gun, not a fired one.

**Parity status is uncertain and corpus-dependent.** One parity corpus reports 27 of 58 strict matches; another reports 437 of 439. They may be testing different Python implementations — the leading hypothesis — or one may be a serious regression on the other. Until that inventory is done, no honest single number for "our parity" exists, and neither figure may be quoted as if it were repository-wide.

**The promotion registry has never been used.** It is empty. Meanwhile there are 63 structured strategy folders, 172 triage candidates and 159 transcripts. The ladder has never been walked end to end, so candidate identity has no permanent home.

**The repository and context burden is real.** Roughly 8.7 GB and 67,105 files in the working tree, 8,031 tracked files, 137 local branches, **zero tags**, and about 709,000 bytes — roughly 180,000 tokens — of mandatory reading before any AI can start work. Zero tags matters more than it sounds: my own live-trading gate requires a "frozen, tagged commit", and the repository currently has no way to produce one.

**Some "dead" settings in the kernel are not dead at all.** *(Added 2026-08-22; stated setting by setting later the same day.)* Seven `tw_*` settings were described — in my own code comment and then in the technical brief — as having no runtime effect, and the plan listed them for deletion as harmless cleanup. **That was wrong.** All seven are settings the kernel requires and validates, so **none of them is deleted in a batch**.

**Six of them are genuinely live:** they are read by the position sizer, the exit logic and the runner, and switching them on changes how quantities are rounded, which bar arms break-even and the trailing stop, how margin calls are handled, and whether a reversal may re-enter. Deleting those would have been a silent change to how my strategies trade, disguised as tidying. They go through the kernel consolidation like any other economic behaviour, **with both settings tested**.

**The seventh is a separate case, and the first correction overshot by lumping it in.** `tw_margin_call_split_entries` is read (`runner.py:133`) and written into the run record (`runner.py:1057`), but **nobody has found anything in the main kernel that actually behaves differently because of it.** So it is recorded as **unknown / dormant in the code as verified**, and it is routed to the capability, golden-suite and parity investigation — **not** to a demand for a two-way behavioural test. **I do not want a test written for behaviour nobody can show exists**; that is the kind of check that can only pass by inventing its own subject. If the investigation finds a consumer, it gets tested both ways then. **Nothing in the code was changed to record any of this.**

**A broker boundary already exists — the plan was about to invent a second one.** *(Added 2026-08-22.)* One finding says the documented adapter folder is empty, which is true. The plan then used that to justify designing a fresh broker interface. But the Bridge already has three — a main one and two opt-in ones for partial recovery and full reconciliation — with working Hyperliquid and mock implementations behind them. Building another beside it would recreate, at the broker layer, exactly the five-versions-of-the-same-thing problem this whole project exists to fix. So the first step is now a **decision** about reusing, extending or deliberately replacing what is there — **on paper, with no code written.**

**The Bridge is genuinely good.** Idempotent order identity, reconciliation, partial-fill protection, native reduce-only stops, fail-closed gates, a small pinned dependency surface, and safety contracts that exist as documents *and* code *and* tests. It is the strongest engineering asset I have, and it is the reason O-15 says it must not be replaced merely for feature count. A caveat that belongs with it: several accepted capabilities are not switched on by the default startup path, and the deployed database's schema version has not been independently verified.

**My own live-trading gate has fourteen conditions, and this document set said six.** *(Corrected 2026-08-22.)* `LIVE_TRADING_GATE.md` lists **fourteen** hard preconditions and states plainly that **all of them are required and there is no partial credit**. The brief, the acceptance criteria and the approval gates all said "six". That is not a rounding error — it is more than half the gate missing from every plan built on top of it. All fourteen must now be evidenced **together, in one dated decision, against the exact configuration that will trade**.

**Some of the reports these documents cite are not in the repository.** *(Added 2026-08-22.)* Including the audit verdict that the whole repair history of the technical brief is built on. The **findings** in that audit were each re-checked against real code and still stand — they do not depend on the missing file. But the claims *about the audit itself*, and several cited proposals and addenda, cannot be verified from the repository as it stands, and they are now marked as such rather than presented as reproducible. **Nothing was recreated to paper over this.**

**Including the most recent review — the one that produced the current corrections.** *(Added 2026-08-22.)* **Its transcripts and reports are not in the repository at the frozen starting commit either, and none was written to fix that**, because the round was permitted to change five documents and nothing else. The **seventeen problems it found are each recorded against real files and lines** and can be re-checked by anyone, so they stand on the code rather than on the report. Anything said about **the review as an event** — that it happened, who performed it, at what depth — is a claim from that working session, **cannot be checked from this repository, and carries no requirement, count, tier, gate or acceptance criterion on its own.** I would rather have the gap stated than have a file produced to close it.

---

## 6. My main objective, and what I expect to get

**Main objective:** build **Bridge V2 around one authoritative strategy kernel, one shared risk allocator, and one honest evidence trail**, so that a number I look at in research means something about what would happen with real money — and so that I can operate the whole thing myself, safely, without being a programmer.

**What I expect to have when this is done:**

1. **One place where strategy logic lives**, imported by the backtest, the shadow runs, the paper runs and the live worker — instead of five versions that quietly disagree.
2. **One risk allocator**, running the same code in a backtest and in production, with the portfolio guardian only ever approving or refusing.
3. **A record of every trial** — parameters, results, and the reason for rejection — that I can search, sort and look at visually, including the equity curve and the trades on a chart.
4. **A promotion ladder that is actually walked**, where approving a strategy produces a permanent decision record, and only approved frozen packages can ever be loaded for execution.
5. **Forward evidence accumulating on real clocks**, safely, on strategies that risk nothing, while the statistical work continues in parallel — because both the search for a credible candidate and the passage of calendar time are constraints, and neither can be skipped.
6. **A dashboard I can read at a glance**, on my desk or my phone, that shows me what the strategy wanted, what was authorized, and what actually happened at the exchange — as three separate things, never merged into one comforting number.
7. **A first live deployment that is deliberately tiny** — one strategy, at most 1 % of the account **as allocated capital, with a separate and lower limit on what a stop-out may cost me, written down and evidenced first** — behind a gate I sign myself only when the evidence is complete. **To be exact: my gate has fourteen hard conditions, all of them required, with no partial credit, all evidenced together in one dated decision against the exact configuration that will trade. The two caps above sit alongside those fourteen; they replace none of them.** **And two of those fourteen are a *paper soak* and a *testnet proof*, which are two separate conditions on two separate environments** *(named 2026-08-22)*. **The paper soak runs on my own machine with simulated fills** — a plan fixed in writing before the clock starts, an immutable start date, eight to sixteen weeks minimum, at least thirty new trades taken in that window, not one unexplained reconciliation break, and no resuming a stopped window without a newly approved plan. **The testnet proof is the real order lifecycle at the exchange test environment.** Until now only the testnet half had anybody's name against it; **the same existing piece of work now carries both, with separate clocks, separate counts, separate records and separate claims, and neither may be offered in place of the other.** No requirement, safeguard or work package was created to say this — the count stays at 60 — and **neither environment is being run.**
8. **A way to stop it that cannot itself fail** — at least two separately registered security keys, and a rehearsed way to close positions directly at the exchange when my own software cannot be reached at all.

**And one thing I expect not to happen:** none of this starts because this document exists, and none of it starts because the technical brief has now been accepted. **This document authorizes nothing.** The brief passed its independent architecture check on 2026-08-23 for one exact version of itself; that ticks the document-acceptance box and no other. **Every work package is still NOT STARTED.** Implementation, deployment, schema changes, credentials, testnet, live trading and any destructive Git operation each require my explicit approval at the time, separately, for the specific thing being done.
