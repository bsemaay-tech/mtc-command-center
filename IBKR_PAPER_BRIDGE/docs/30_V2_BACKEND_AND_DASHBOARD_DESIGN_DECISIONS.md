# 30 — V2 Backend and Dashboard Design Decisions

**Date:** 2026-08-16
**Status:** Living decision record (documentation only)
**Scope:** Backend V2 and Dashboard V2 design direction

---

## 0. Purpose and Authority

This document is **documentation only**. It records design direction and open
questions. It **authorizes no implementation, no deployment, no TESTNET or
mainnet activity, no ARM, no order placement, no credential handling, and no
economic action of any kind.** The current authorized baseline V1 scope and
build are unchanged by this document, and remain the only currently authorized
Bridge scope. Nothing here claims V1 is already running, and nothing here
changes V1 behavior, configuration, deployment status, or risk posture.

### Definitions

- **RECORDED** — an established current fact or boundary taken from the repo or
  owner discussion. It describes what already exists or what is already decided
  and in force. It is not an instruction to build or run anything new.
- **DIRECTION** — a preferred design not yet approved for implementation. It is
  the approach we intend to evaluate, subject to reverification and policy.
- **OPEN** — an unresolved question that must be answered before any
  implementation of that item proceeds.

### Why every topic below has the same six fields

Earlier versions of this record kept only the conclusions. A conclusion without
its cause is unusable to a later agent: it cannot tell whether the reasoning
still holds, whether the rejected options were rejected for good reasons, or
what still has to be answered. So every substantive topic now carries:

1. **Status** — RECORDED / DIRECTION / OPEN, unchanged in meaning.
2. **Problem or question discovered** — what actually forced the topic open.
3. **Evidence and reasoning** — what we observed, and why it leads where it does.
4. **Decision / offered direction** — the call, or the preferred route if the
   call is not owner-approved yet.
5. **Alternatives and trade-offs** — the other routes and what each costs.
6. **Open points / implementation gate** — what is still unanswered, and the
   explicit statement that nothing here is approved to build.

Field 6 never grants approval. If a topic's gate is not written as satisfied by
a separate owner decision recorded elsewhere, it is not satisfied.

---

## 1. Context

- **research/QuantLens** is operationally separate from the Bridge. It hands
  the Bridge a **frozen, approved strategy package**. The Bridge does not
  develop strategies; it consumes approved packages.
- **Keltner** is a **plumbing test**, not proof of edge. Passing Keltner
  validates ingestion, normalization, and execution plumbing — it says nothing
  about whether a strategy is profitable.
- **V1** is one strategy, one symbol, one timeframe. V2 is the direction toward
  multiple strategies.

---

## 2. Architecture Overview (ASCII)

```
                    research/QuantLens (separate)
                          |  frozen approved strategy package
                          v
   +--------------------------------------------------------------+
   |                    IBKR_PAPER_BRIDGE (V2)                    |
   |                                                              |
   |   Hyperliquid (raw candles / fills / account truth)          |
   |        ^                                                     |
   |        | safe ingestion / warmup / normalization /           |
   |        | reconnect / staleness / reconciliation              |
   |        |                                                     |
   |   +----+--------+   +--------+----+   +----+--------+        |
   |   | Worker A    |   | Worker B    |   | Worker N    |        |
   |   | (strategy)  |   | (strategy)  |   | (strategy)  |        |
   |   +-------------+   +-------------+   +-------------+        |
   |        ^                 ^                 ^                 |
   |        +-----------------+-----------------+                 |
   |                          |                                   |
   |              Portfolio Guardian (above workers)              |
   |        total exposure / loss / leverage / concentration /    |
   |        correlation controls                                  |
   +--------------------------------------------------------------+
                          |
                          v
              Execution Dashboard (combined, per-strategy drill-down)
```

---

## PART A — BACKEND V2

### A1. Data and Truth

**Status:** RECORDED — Hyperliquid as the data/truth source and the Bridge's
safe-layer role are established facts of the current architecture.

**Problem or question discovered.** A trading system needs one answer to
"what is actually true right now" — what the price is, what filled, what the
account holds. If two components each believe their own copy, they will act on
different worlds and neither will be wrong locally.

**Evidence and reasoning.** The current architecture already names Hyperliquid
as the origin of raw candles, fills, and account truth. Exchange feeds
disconnect, arrive late, arrive out of order, and go stale silently. Raw
exchange data is therefore trustworthy as *origin* but not trustworthy as
*input to an order* until it has been checked.

**Decision / offered direction.**

- **Hyperliquid** supplies raw candles, fills, and account truth.
- The **Bridge** codes the safe layer around that data: ingestion, warmup,
  normalization, reconnect, staleness detection, and reconciliation.
- The Bridge does not invent data; it makes Hyperliquid data safe to act on.

**Alternatives and trade-offs.**

- *Trust the raw feed directly* — simplest, and unacceptable: a stale or
  partial feed becomes an order with no one to catch it.
- *A second independent data vendor as cross-check* — real accuracy gain, but
  it adds cost, a second failure mode, and a reconciliation policy for the case
  where the two vendors disagree. Not chosen; not ruled out forever.

**Open points / implementation gate.** None open for the boundary itself. This
is a description of what exists, not authorization to change it.

### A2. Multi-Strategy Goal

**Status:** DIRECTION — preferred future design, not yet approved for
implementation.

**Problem or question discovered.** The current authorized V1 baseline is
scoped to one strategy, one symbol, and one timeframe. Running more than one
strategy means choosing *how* they coexist — and that choice is made once and
is expensive to reverse.

**Evidence and reasoning.** The obvious route is to give every strategy its own
machine and its own master account, which does give perfect isolation. It also
multiplies the number of hosts, deployments, releases, and monitoring surfaces
by the number of strategies, and every one of those is a place to make a
mistake. Isolation is the goal; a separate host per strategy is only one way
to get it, and the most expensive one.

**Decision / offered direction.**

- V2 direction is **multiple strategies** running concurrently.
- Preferred deployment is **one VPS / one shared release** with **isolated
  workers** — not one VPS / one master account per strategy.

**Alternatives and trade-offs.**

- *One VPS + one master account per strategy* — strongest isolation, highest
  operational cost, and N releases to keep in step.
- *One process running all strategies with shared in-process state* — cheapest,
  and rejected: one strategy's bug becomes every strategy's bug.
- *Shared release, isolated workers* (preferred) — one deployment to get right,
  isolation enforced by worker boundaries and by A3/A6.

**Open points / implementation gate.** Worker isolation strength is not yet
specified (see A12). Nothing here authorizes building V2 workers.

### A3. Subaccount Direction (Signum lesson)

**Status:** DIRECTION — preferred future design, not yet approved for
implementation.

**Problem or question discovered.** If several strategies share one exchange
account, whose position is whose? The exchange has no concept of "strategy" —
it holds one balance and one position per symbol.

**Evidence and reasoning.** The Signum lesson is that isolation must exist at
the level the exchange itself recognises, not only inside our own bookkeeping.
Hyperliquid exposes sub-accounts and separate API/agent wallets, which is the
level at which the exchange will keep the books apart for us.

**Decision / offered direction.**

- Preferred direction: **one independent strategy / risk bucket per Hyperliquid
  subaccount** when available, each with a **separate API / agent wallet**.
- This is the preferred Signum lesson: isolation of strategy and risk.
- **Eligibility and policy must be reverified** before relying on it. Subaccount
  availability, limits, and wallet rules are subject to change.

**Alternatives and trade-offs.**

- *Single account + internal virtual books* — no exchange-side eligibility
  question, but every ownership guarantee then rests on our own code, and A4
  shows exactly how that fails.
- *Separate top-level accounts instead of sub-accounts* — stronger separation,
  more funding/transfer friction and more credentials to hold safely.
- *Subaccounts* (preferred) — separation the exchange enforces, at the cost of
  a dependency on exchange policy that can change under us.

**Open points / implementation gate.** Subaccount eligibility, limits, and
wallet rules must be reverified against live exchange documentation before any
design depends on them, and the fallback when subaccounts are unavailable is
still open (A12). No credential creation or account action is authorized here.

### A4. Same-Symbol Strategies

**Status:** RECORDED (problem) / DIRECTION (response) — the collapse risk is an
established fact of Hyperliquid account mechanics; the mitigation is preferred
design not yet approved.

**Problem or question discovered.** Two strategies that both trade BTC in the
same account: does the system hold two positions, or one?

**Evidence and reasoning.** It holds one. The exchange nets them. Strategy A
going long 1 BTC and strategy B going short 1 BTC produces a flat account, and
each strategy's own book still claims an open position. Exits then close the
wrong exposure, and stops protect a position that is not there. This is
account mechanics, not a bug we can patch around. Note in particular that a
Portfolio Guardian does **not** fix this: it can refuse or cap, but refusing is
not the same as saying which strategy owns what.

**Re-verification caveat (same standard as A3).** This netting description is
stated from general account mechanics; **no authoritative Hyperliquid citation
for it is present in this repository** — the Official References below cover
sub-accounts and API wallets, not position netting, and no exchange
documentation was browsed for this record. Hyperliquid's exact per-symbol
netting, position-mode, and margin-mode behavior must therefore be
**reverified against live exchange documentation** before any design depends on
it, exactly as A3's subaccount eligibility must be.

**Decision / offered direction.**

- **RECORDED problem:** Two strategies trading the same symbol in one
  Hyperliquid account can collapse into **one net exchange position**. Portfolio
  Guardian alone does **not** create ownership separation between strategies;
  it is a risk-control layer, not an ownership boundary.
- **DIRECTION response:** Require **separate subaccounts** for same-symbol
  strategies, or an explicitly designed and validated **virtual-book / netting
  model** that proves ownership separation before any same-symbol concurrency is
  permitted.

**Alternatives and trade-offs.**

- *Forbid same-symbol concurrency entirely* — safest and simplest, and it
  permanently costs us strategy combinations we may want.
- *Virtual book inside the Bridge* — keeps one account, and must prove
  ownership through partial fills, liquidations, funding, and restarts before
  it can be trusted. That proof is the whole cost.
- *Separate subaccounts* (preferred, per A3) — the exchange keeps the books
  apart, subject to A3's eligibility question.

**Open points / implementation gate.** Same-symbol concurrency stays closed
until either separate subaccounts are confirmed available or a virtual-book
model is designed *and validated*, **and** until the netting mechanics above
are reverified against live exchange documentation. Nothing here authorizes
either.

### A5. Portfolio Guardian

**Status:** DIRECTION — preferred future design, not yet approved for
implementation.

**Problem or question discovered.** Each worker can be individually well
behaved and the account can still be destroyed — five workers each risking a
"small" amount, all long, all correlated, is one large undiversified bet that
no single worker can see.

**Evidence and reasoning.** No worker has portfolio-level information by
construction: a worker sees its own strategy, not the sum. Therefore the limit
that matters — total exposure — has to live somewhere above the workers, and it
has to be able to say no.

**Decision / offered direction.**

- A **Portfolio Guardian** sits **above the workers**.
- It controls **total exposure, loss, leverage, concentration, and correlation**
  across all workers.
- Workers manage their own strategy; the Guardian manages the portfolio.

**Alternatives and trade-offs.**

- *Per-worker limits only* — simple, and blind to the aggregate, which is the
  failure being prevented.
- *Guardian that silently resizes orders* — feels helpful, and breaks the link
  between what was tested and what trades (see A10).
- *Guardian that vetoes but does not mutate* (preferred) — the portfolio stays
  bounded and each strategy stays recognisable; the cost is that a veto is a
  blunt instrument, so veto reasons must be logged and visible.

**Open points / implementation gate.** Exact thresholds and the Guardian's
interaction with worker-level risk are unresolved (A12). Whether a veto may
ever become a resize is answered in A10 as *not without an explicit parity
contract*. No Guardian implementation is authorized.

### A6. Identity and State Separation

**Status:** DIRECTION — preferred future design, not yet approved for
implementation.

**Problem or question discovered.** When several strategies run under one
release, which orders, which P&L, and which state belong to which strategy —
particularly after a restart?

**Evidence and reasoning.** Shared state is the classic failure: one strategy's
order recognised as another's, one strategy's loss counted against another's
limits, one strategy's restart clearing another's protective state. Every
correctness claim in A4, A5, and A10 assumes we can name the owner of a row.
If we cannot, none of them hold.

**Decision / offered direction.**

- Each worker keeps **separate P&L, state, order identity, version, symbol, and
  timeframe**.
- No cross-contamination of state between strategies.

**Alternatives and trade-offs.**

- *Shared state with a strategy tag column* — cheap, and one missing filter
  silently mixes strategies.
- *Fully separate stores per worker* — strongest isolation, harder aggregate
  reporting and more moving parts to back up and reconcile.
- The store question itself (per-worker SQLite vs. central Postgres) is
  deliberately left open in A12; the *separation requirement* is decided
  regardless of which store wins.

**Open points / implementation gate.** Worker identity granularity — is a
worker a strategy, a strategy+symbol, or a strategy+symbol+timeframe? — is open
(A12). No implementation is authorized.

### A7. What We Retain / Do Not Copy

**Status:** DIRECTION — preferred future design, not yet approved for
implementation.

**Problem or question discovered.** Studying a working vendor system (Signum)
raises the question of how much of it to adopt. Copying a system that works is
tempting precisely because it works.

**Evidence and reasoning.** Per
[07_BROKER_DECISION.md](./07_BROKER_DECISION.md), Signum's order size supports
**several modes**, not one: a `100%` (all-in) mode, a "let strategy decide"
absolute-size mode, and a fully custom developer JSON that can carry percentage
sizing. So all-in is an *available option* there, not Signum's only behavior,
and "Signum sizes all-in" would be an inaccurate reason to reject it.

The reason Signum is unsuitable for us is recorded in the same source and is
about **execution granularity**, not about which sizing modes exist. Signum
places **market orders only**; SL/TP are synthetic — the strategy fires an alert
and Signum sends a market exit, so a dead automation or connection leaves a
leveraged position unprotected. That same market-only granularity cannot carry
our exact-qty + resting-SL + TP + trailing-modify + reduce-only model *even
when* the "let strategy decide" mode is used. Its all-in mode is separately
unsuitable for us because it would remove the stop-based risk budget, but that
is one optional mode we decline, not a description of the product.

**Decision / offered direction.**

- **Retain** Bridge sizing and native protective orders.
- **Do not copy** Signum's **optional** all-in (`100%`) sizing mode, its
  market-only execution with synthetic SL/TP, its vendor dependency, or its
  vendor architecture.
- This is **not** a claim that all-in is Signum's only sizing mode. Signum's
  absolute "let strategy decide" and custom-JSON percentage modes exist; they
  are simply not what makes it suitable or unsuitable here — the market-only,
  no-native-resting-stop execution model is.

**Alternatives and trade-offs.**

- *Adopt the vendor architecture wholesale* — fastest, and inherits risk
  choices we did not make and cannot audit.
- *Cherry-pick specific mechanisms* — what A3 already does with the subaccount
  isolation lesson; the cost is judgement, exercised case by case.

**Open points / implementation gate.** "Bridge sizing" as retained here is the
*execution-side* sizing envelope. Who owns the *strategy* quantity is the
subject of A10 and is not settled by this topic. No implementation authorized.

### A8. Staged Path

**Status:** DIRECTION — preferred future design, not yet approved for
implementation.

**Problem or question discovered.** How many strategies do we turn on first,
and how do we find out whether multi-strategy actually works before it is
handling real money?

**Evidence and reasoning.** Two workers is the **minimum configuration that can
exercise multi-strategy netting (A4), aggregate-risk control (A5), and
state-isolation (A6)** — each of those needs at least two concurrent strategies
to be observable at all, so two workers is the cheapest configuration in which
they can be tested.

That is a statement about *those three*, not about every failure mode in this
document. In particular, **the A10 sizing-ownership conflict does not wait for a
second worker.** It exists as soon as the *first* MTC-connected worker exists,
because it is a conflict between two components — MTC and the Bridge — each
originating a quantity, not a conflict between two strategies. It must
therefore be resolved **before any MTC-to-Bridge integration**, including a
single-worker one, and it cannot be deferred to the two-worker step.

**Decision / offered direction.**

1. Prove V1 within the current authorized baseline V1 scope.
2. Testnet with **two workers**.
3. Expand gradually as confidence and controls allow.

Resolve A10's sizing-ownership contract before **any** MTC-to-Bridge
integration, independently of this staging — it is a precondition of step 1
being connected to MTC at all, not an item for step 2.

**Alternatives and trade-offs.**

- *Go straight to N workers* — fastest on paper, and discovers all failure
  modes simultaneously, entangled, at maximum cost.
- *Stay single-strategy* — safest, and forgoes the diversification that is the
  point of V2.

**Open points / implementation gate.** "Prove V1" has no acceptance definition
written in this document. TESTNET activity is explicitly **not** authorized
here; step 2 requires its own separate owner authorization.

### A9. V2 Must Not Delay V1

**Status:** DIRECTION — preferred future design, not yet approved for
implementation.

**Problem or question discovered.** Design work on a more capable V2 tends to
pull attention and changes into the current authorized baseline.

**Evidence and reasoning.** V1 is the only currently authorized Bridge scope.
Any change made to the V1 build "so that V2 will fit later" spends the
stability of that authorized baseline on a system that does not exist yet —
including changes that look purely preparatory. This is a statement about
authorized scope and build stability; consistent with §0, it makes **no claim
about whether V1 is running anywhere**.

**Decision / offered direction.**

- V2 work must **never delay or destabilize the current authorized baseline V1
  scope or build**. That baseline remains the authorized Bridge scope until
  explicitly superseded.

**Alternatives and trade-offs.**

- *Refactor V1 toward V2 now* — less rework later, and risks the only
  authorized baseline scope/build for a design that is still open.
- *Build V2 separately and cut over once* (preferred) — some duplicated effort,
  V1 stays untouched.

**Open points / implementation gate.** This document is itself V2 design work
and changes nothing in V1. No V1 change is authorized here.

### A10. Position-Sizing Ownership — MTC vs. Bridge (newly discovered conflict)

**Status:** RECORDED (the facts and the conflict) / DIRECTION (the preferred
ownership split) / OPEN (the contract that would make it real). **Preferred
design direction only — no implementation is approved.**

**Problem or question discovered.** MTC_V2 and the Bridge each compute a
position size, independently, with different policies and different defaults.
Neither knows the other exists. If MTC_V2 were ever wired to the Bridge as a
signal source, *two* components would each believe they own the quantity — and
the number that reached the exchange would not be the number that was
backtested.

**Evidence and reasoning.**

*MTC_V2 already owns sizing, in both of its implementations — but the two
implementations are **not** byte-for-byte the same contract.*

- Pine: [MTC_V2.pine](../../MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine)
  exposes a "04 Position Sizing" input group — `risk_per_long_pct` and
  `risk_per_short_pct` (**default 1.0** each, lines 90–91), `fallback_size_pct`
  (default 10.0, line 92) and `max_leverage_cap` (default 1.0, line 94) — and
  computes quantity in `calc_l6_qty` from entry, stop, a frozen equity
  snapshot, and the instrument's contract multiplier (lines 339–361). Rounding
  uses `syminfo.mincontract` as the quantity step (line 252) and as the minimum
  quantity (line 341); below-minimum sizes return `0.0`. When no stop-based
  risk distance exists, it falls back to a percent-of-equity notional
  (line 354).
- Python: [position_sizer.py](../../MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_sizer.py)
  covers the same *intent* in code — `PositionSizer.calc_qty(entry, sl, equity,
  is_long, instrument, …)` applies the direction-specific risk percent, the
  no-stop fallback, the leverage cap
  (`equity * max_leverage_cap / (entry * contract_multiplier)`), the
  instrument's quantity step (`floor_qty`), `min_qty`, and `min_notional`,
  returning `0.0` rather than an unsafe size. Its own docstring calls it the
  "L6 risk-based quantity owner".

*OPEN parity gaps between the two MTC implementations.* They are **not**
identical implementations of one frozen contract. Two differences are visible in
the source as read on 2026-08-16:

1. **Stop-risk raw quantity divides by different denominators.**
   - Pine (`MTC_V2.pine` line 351):
     `raw_qty := risk_amount / (per_unit_risk * contract_multiplier)` — it
     divides by **stop distance × `contract_multiplier`**.
   - Python (`position_sizer.py` line 47):
     `raw_qty = risk_amount / per_unit_risk` — it currently divides by
     **stop distance only**, with no `contract_multiplier` in this branch —
     even though the *same function* does use `contract_multiplier` in its
     leverage cap (lines 52–54) and in its notional check (line 66). So the
     multiplier is present in that file's caps and absent from its stop-risk
     quantity.
   - Consequence: for any instrument whose `contract_multiplier != 1`, Pine and
     Python produce **different stop-risk quantities** from identical inputs.
2. **Python applies a `min_notional` gate that Pine does not.** Python rejects
   to `0.0` when `rounded_qty * entry * contract_multiplier <
   instrument.min_notional` (lines 66–68). Pine's `calc_l6_qty` gates only on
   the minimum quantity (`syminfo.mincontract`, lines 341 and 360) and has no
   equivalent minimum-notional gate. So one side can return a size where the
   other returns zero.

Both are recorded here as **OPEN parity gaps**, not as settled behavior. They
must be **closed, or explicitly bounded and documented** (for example: the
contract is declared valid only for `contract_multiplier = 1` instruments, and
`min_notional` semantics are stated for both sides), **before** the Python
engine can be appointed production canonical and before MTC is integrated with
the Bridge. Which side is correct is itself open and is not decided here.
- [runner.py](../../MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py)
  freezes an equity snapshot per bar (`_frozen_sizing_equity_snapshot`, used at
  line 348) and passes it into `calc_qty`. Sizing is therefore taken against a
  defined, reproducible equity value, not against a moving one.
- [MTC_V2_ARCHITECTURE.md §7](../../MTC_COMMAND_CENTER/01_MTC_PROJECT/03_DOCS/MTC_V2_ARCHITECTURE.md)
  states the contract explicitly: "% risk means risk at stop, not position size
  as a percent of account", "if stop distance is small, requested qty may be
  large", and `max_leverage_cap` is an internal sizing cap, not broker margin.
- MTC_V2 also carries strategy state that can change what a position *is*: the
  Pine strategy declares `pyramiding=100` (line 7) and merges stops across adds
  (`merge_pyramid_stop`, line 283). **`pyramiding=100` is only a deliberately
  generous broker-level ceiling, not the add permission.** The script's own
  comment (lines 5–6) says to keep that ceiling generous and let script-level
  `max_entries` remain the sole owner of add permission, and `max_entries` is an
  input that **defaults to 1** (line 19), enforced at line 1800. So with default
  settings MTC does **not** pyramid. Basket/add behavior is therefore
  **conditional on `max_entries > 1`** — a quantity is an instruction about a
  basket over time only in that configuration, and about a single order
  otherwise. The intent schema must still handle both cases.

*The Bridge currently sizes independently, and differently.*

- [types.py](../bridge/engine/types.py) — the `Signal` model (lines 27–34)
  carries `ts`, `symbol`, `direction`, `reason`, `ref_price`, `stop_loss`,
  `take_profit`. **There is no `qty` field.** A quantity first appears on
  `OrderPlan` (lines 37–47), which the Bridge itself creates.
- [risk.py](../bridge/engine/risk.py) — `RiskConfig.risk_pct_per_trade`
  defaults to **0.005** (line 37), and `RiskEngine` computes
  `risk_dollars = equity * risk_pct_per_trade`, then
  `qty = round(risk_dollars / stop_distance, size_decimals)` (lines 379–381)
  before its own minimum-order, notional, and margin gates. The Bridge is not
  validating someone else's number; it is originating one.

*The numbers actually diverge.* Take $10,000 equity, entry $60,000, stop
$58,000 — a stop distance of $2,000:

| Owner | Default risk | Risk dollars | Quantity (before other caps/rounding) |
|---|---|---|---|
| MTC_V2 | 1.0 % | $100 | **0.05 BTC** |
| Bridge `RiskEngine` | 0.5 % | $50 | **0.025 BTC** |

A factor of two, from defaults alone, before either side's caps, steps, or
rounding are applied.

*What that arithmetic assumes.* The 0.05 / 0.025 BTC figures are illustrative
and hold only under stated assumptions: **`contract_multiplier = 1`**, and a
quantity step, rounding mode, and minimum quantity/notional that do not alter
the raw values. On an instrument with `contract_multiplier != 1` the numbers
change — and, per the parity gaps above, they change *differently* on the Pine
and Python sides, which is precisely why the multiplier gap must be closed
before these figures can be treated as a contract rather than an illustration.

*What the Bridge's own notional cap does with the MTC number.* On the same
inputs the Bridge's `max_position_notional_pct` of 0.20 with `max_leverage` of 1
(risk.py lines 41 and 44) caps notional at **$2,000**. MTC's 0.05 BTC at
$60,000 is **$3,000** of notional, which **exceeds that current numeric $2,000
cap**. Stated precisely, and without overclaiming:

- Today's Bridge **cannot receive an MTC-requested quantity at all** — `Signal`
  has no `qty` field and the Bridge evaluates **its own** computed quantity
  (0.025 BTC = $1,500 here), which passes the cap. No rejection of an MTC
  number happens today because no MTC number arrives.
- A **future** validator that accepted an MTC-requested quantity and retained
  this $2,000 threshold **would reject** the 0.05 BTC / $3,000 request.

So this is not "MTC's order would be rejected today"; it is a numeric
incompatibility between MTC's default sizing and the Bridge's currently
configured envelope that would surface the moment the two are wired. That is
the envelope behaving correctly — and it is also the concrete shape of the
conflict.

*There is no runtime clash today.* MTC_V2 and the current Keltner Bridge
candidate are **not connected**. The Bridge's strategy module is
`bridge/engine/strategies/keltner_trail_ema8.py`; no Bridge engine module
imports MTC_V2, and **within the `bridge/` package** the only occurrences of
"MTC" are the state-database environment variable `MTC_BRIDGE_STATE_DB` and the
`/var/lib/mtc-bridge/bridge.db` deployment path, both in `bridge/app.py` (lines
32 and 35). That scope is deliberate: it is a statement about the `bridge/`
package only, **not** about the whole `IBKR_PAPER_BRIDGE` tree, which does
mention MTC elsewhere (docs, this file included).
**This is a future integration conflict, not a present double-order problem.**
Nothing is mis-sizing right now because nothing is wired.

*A separate, unresolved parity issue.* The MTC Pine WunderTrading alert
(MTC_V2.pine line 2020) sends a **fixed `wt_amount`** — an input defaulting to
100.0 (line 183) — and not the quantity MTC computed internally. So MTC's live
alert path today does not carry MTC's own sizing. This is recorded as its own
open parity/integration question; it is not the same problem as the MTC↔Bridge
ownership conflict, and solving one does not solve the other.

**Decision / offered direction.** *Preferred direction, not approved
implementation.*

- The **MTC Python engine should become the canonical strategy-sizing owner.**
  That is the preferred direction and it is unchanged. It emits an **exact
  requested quantity** together with the **frozen policy and provenance
  inputs** that produced it — risk percent, equity snapshot, instrument
  metadata, caps, rounding mode.
  **Gate on this appointment:** Python is *not* canonical yet. The appointment
  takes effect only once (a) the Pine↔Python parity gaps recorded above — the
  `contract_multiplier` denominator and the `min_notional` gate — are closed or
  explicitly bounded, and (b) a **frozen sizing contract is written and
  accepted**. Until both hold, calling Python canonical would freeze a contract
  that its own reference implementation does not match.
- The **Bridge is an independent execution-safety envelope**, not a second
  sizing brain. On receiving a requested quantity it should:
  1. **recompute and validate** the quantity from the supplied inputs;
  2. **check live account truth** — margin, exposure, daily loss, leverage,
     liquidation distance, and current positions;
  3. **execute the exact quantity, or reject and log** with a reason.
- The Bridge **must not silently resize.** A silently resized order breaks the
  identity between what was backtested and what trades: performance, risk, and
  every parity claim then describe a strategy that never ran.
- The **Portfolio Guardian may veto globally** (see A5) but **should not
  silently mutate size**. Any policy that permits resizing requires an explicit
  parity contract *and* re-backtesting under that contract.

**Alternatives and trade-offs.**

| Route | What it buys | What it costs | Verdict |
|---|---|---|---|
| **Bridge as sole sizing owner** | One sizing implementation; the Bridge already sees live account truth | Discards MTC's tested sizing, its direction-specific risk, fallback, and instrument rules; backtests no longer describe live behavior | Viable, not preferred |
| **Shared canonical packaged sizing library** | One implementation used by both sides; removes drift by construction | Couples Bridge releases to MTC releases; needs versioning, packaging, and a joint upgrade discipline; Pine remains a third implementation regardless | Viable; strong long-term candidate, higher coordination cost |
| **`min(MTC, Bridge)` silent clamp** | Always "safe"; never exceeds either limit | Silently changes the tested strategy — smaller size changes exit behavior, compounding, and every performance figure. Fails quietly, which is the worst failure mode | **Not preferred** |
| **Reject-on-mismatch** | Divergence becomes a loud, logged event instead of a silent drift; tested == live or nothing trades | Rejected trades are missed trades; needs explicit tolerances so that rounding noise is not treated as a mismatch | **Preferred** |

**Open points / implementation gate — OPEN.** Before any of this could be
built, a formal **Sizing Ownership Contract / `OrderIntent` schema** must be
specified and agreed. The earlier draft below was incomplete: it named the
sizing *numbers* but not the identity, time, venue, unit, and versioning fields
without which two systems cannot agree on what a single number even refers to.
The schema must carry at least:

*Identity and provenance*

- [ ] `intent_id` / `decision_uid` — a unique, idempotent identifier for this
      decision, so a retry or duplicate delivery cannot become a second order
- [ ] `strategy` identifier **and** `version`
- [ ] **sizing-policy / config version, or an immutable hash of the sizing
      config** — so a validator can prove both sides used the *same* policy,
      not merely the same field names
- [ ] `reason` / decision provenance

*Time*

- [ ] **creation timestamp** (when the intent was produced)
- [ ] **signal timestamp** (the bar/event the decision was made from) — these
      are not the same value and must not be collapsed
- [ ] **expiry / freshness bound** — after which the intent must be rejected
      rather than executed late

*Instrument, venue, account, and direction*

- [ ] `symbol` / instrument identifier
- [ ] `venue` / exchange
- [ ] `account` / `subaccount` (ties the intent to the A3/A6 isolation boundary)
- [ ] `side` (long/short, open/close intent)
- [ ] `timeframe`

*Quantity semantics — what the number means*

- [ ] `requested_qty` — the exact strategy-owned quantity
- [ ] **quantity unit** — base, quote, or contracts. A bare number is
      unusable without it
- [ ] **whether `requested_qty` is a delta (order size to send) or a target
      total position** — the two produce different orders from the same number,
      and this is the single most dangerous ambiguity in the schema

*Sizing policy inputs*

- [ ] **sizing branch actually taken** — stop-risk vs. no-stop fallback
- [ ] `fallback_size_pct` when the fallback branch was used
- [ ] `risk_pct` used, **plus its scale/convention stated explicitly** — whether
      `1.0` means one percent (MTC's Pine/Python convention, `risk_pct / 100.0`)
      or `0.01` means one percent (the Bridge's `risk_pct_per_trade = 0.005`
      convention). The two live systems currently use *different* conventions,
      so the contract must name the one it uses
- [ ] entry reference (price and its meaning — e.g. close of signal bar)
- [ ] `stop_loss` and `take_profit`
- [ ] equity snapshot: **value, id, timestamp, and source**
- [ ] `contract_multiplier`
- [ ] quantity step
- [ ] minimum quantity **and** minimum notional
- [ ] leverage cap
- [ ] rounding mode

*Add / basket lifecycle*

- [ ] **add/basket lifecycle identity** — which position lifecycle this intent
      belongs to, so adds and a fresh entry are distinguishable
- [ ] **entry/add sequence number** within that lifecycle
- [ ] **existing position context and target position context** at decision time
- [ ] **exact requested-quantity semantics under pyramiding** — for an add, is
      `requested_qty` the add size or the resulting total? (Recall
      `max_entries` defaults to 1, so the common case is a single entry; the
      schema must still be unambiguous when it is greater than 1)

*Validation*

- [ ] tolerances and explicit reject rules (what counts as a mismatch)
- [ ] parity evidence: **Pine == Python == Bridge-validated**, plus exchange
      precision (the exchange's own step/minimum must be satisfied by the same
      number)

Also open, and not answered by the contract above:

- [ ] Closing the Pine↔Python parity gaps (the `contract_multiplier`
      denominator and the `min_notional` gate), or explicitly bounding the
      contract's validity — this gates appointing Python canonical.
- [ ] How adds/pyramiding are expressed — one intent per add, or an intent that
      describes the target basket (Pine's `pyramiding=100` is a broker ceiling;
      `max_entries`, default 1, is the actual add permission).
- [ ] The `wt_amount` parity issue above — whether the MTC alert path should
      carry MTC's computed quantity, and what that would change downstream.
- [ ] Whether a Guardian veto may ever become a resize, and under what parity
      contract and re-backtest evidence.

**No implementation, wiring, configuration change, or connection between
MTC_V2 and the Bridge is authorized by this document.** The current Bridge
behavior described above is unchanged, and this section changes nothing in
either system.

### A11. Order and Exit Lifecycle Ownership — MTC vs. Bridge

**Status:** RECORDED (current behavior and incompatibilities) / DIRECTION (the
preferred ownership split) / OPEN (the contract and implementation needed to
make it real). **Preferred design direction only — no implementation is
approved.**

**Problem or question discovered.** MTC_V2 and the Bridge both contain concepts
named entry, stop-loss, take-profit, trailing stop, and position lifecycle. If
they are connected without an explicit ownership contract, both components can
believe they control the same economic decision. A stop, target, or close in
live trading could then differ from the strategy that was backtested.

**Evidence and reasoning.**

*There is no runtime clash today.* MTC_V2 and the current Keltner Bridge
candidate are not connected. The current Keltner strategy is explicitly a
plumbing test. It produces the initial stop, supplies an EMA8 trail, and returns
`take_profit=None`; the current `bridge.yaml` also sets `tp_mode: none`. Today,
therefore, the candidate uses entry + native stop protection + a tightening
trail, not an MTC-controlled lifecycle and not a configured take-profit.

*OrderManager is the execution custodian, not the strategy author.* The current
Bridge `OrderManager` receives an `OrderPlan`; it does not choose the original
entry signal or invent the plan's original SL/TP. Its responsibilities include:

- durably reserving an intent before broker submission so a retry does not
  become a duplicate order;
- submitting and verifying the expected ENTRY / SL / optional TP roles and
  their identities and quantities;
- recording actual fills, detecting conflicts and overfills, and closing a
  trade only from actual exchange-fill truth;
- protecting a partially filled entry, reconciling exchange truth after
  reconnect/restart, and re-protecting an owned live position if its protection
  is missing;
- applying a requested stop update only when it tightens protection; and
- cancelling/replacing protection and safely flattening when an accepted close
  instruction requires it.

The Hyperliquid adapter expresses SL and optional TP as native, reduce-only
trigger orders. This matters because exchange-side protection can remain in
force when the Bridge process or VPS is unavailable. It does **not** make the
Bridge the owner of the strategy's chosen stop or target.

*MTC_V2 carries the richer strategy lifecycle.* Its Pine and Python paths
calculate or simulate entry/exit conditions, initial stops, break-even and
trailing-stop ownership, TP modes including fractional TP1 plus a TP2 remainder,
and conditional same-side additions/basket state. That state describes the
strategy's desired economic behavior. It is not proof that Hyperliquid accepted
or filled a real order, and this section does not claim that Pine and Python
exit behavior already has accepted parity.

*Some overlap is necessary.* The Bridge must receive the desired quantity, SL,
TP legs, and later stop/exit updates so it can validate and execute them safely.
That is intentional duplication of **data and validation**, not permission for
two independent strategy brains. The harmful clash begins if the Bridge silently
recalculates or substitutes a different strategy lifecycle after MTC is
connected.

*Current Multi-TP and basket incompatibility.* MTC can describe a fractional TP1
and a remaining TP2. The current Bridge `OrderPlan` has only one optional
`take_profit`, and its bracket validation/submission expects the same full plan
quantity for ENTRY, SL, and TP. It cannot faithfully express two target legs of
different quantities. Its present lifecycle is also not equivalent to MTC's
conditional add/basket lifecycle. Both the intent schema and execution model
must be extended and accepted before Multi-TP or basket/add behavior can be
enabled through the Bridge.

*Native-stop versus strategy-stop parity must be explicit.* Two valid designs
have materially different fills:

1. the MTC stop is itself the continuously active native exchange stop; or
2. MTC uses a synthetic/bar-evaluated strategy exit while the Bridge maintains
   a separately named emergency native safety stop.

The second route preserves an independent last-resort safety fence but can exit
at a different price or time than the backtest. These meanings cannot share one
field or be mixed silently. A live position must retain durable native
protection; the accepted contract must say whether that protection is the
strategy stop itself or a separate emergency stop, and parity evidence must be
produced for the chosen semantics.

**Decision / offered direction.** *Preferred direction, not approved
implementation.*

- After an accepted Pine/Python strategy-lifecycle contract exists, the **MTC
  Python engine should own desired economic intent**: entry action; the exact
  quantity subject to A10; initial SL; every TP leg and quantity; break-even and
  trailing desired updates; close reason; and add/basket identity.
- The **Bridge should own real exchange execution and truth**: idempotent
  identity; submission; reduce-only flags; broker acknowledgements; fill
  accounting; partial-fill protection; reconciliation; restart recovery;
  missing-stop re-protection; cancel/replace; and safe flattening.
- The Bridge should **execute the exact accepted intent, or reject and log it**.
  It must not silently change quantity, SL, TP, or TP-leg allocation; widen a
  stop; independently rerun MTC exit logic; or treat an MTC simulated close as
  proof of an exchange fill.
- MTC may request a new tighter stop. The Bridge validates that the update is
  authorized, fresh, correctly versioned, and monotonic before modifying the
  real native order. A request to widen protection is rejected.
- The Portfolio Guardian may veto an unsafe intent, but it must not silently
  mutate the strategy's economic intent. A different-size or different-exit
  policy would require its own explicit parity contract and re-testing.
- The dashboard should show three separate states: **desired by MTC**, **accepted
  or rejected by Bridge**, and **actually acknowledged/filled at the exchange**.
  Combining them into one "current order" value would hide the exact divergence
  this contract is intended to expose.

This split preserves the behavior that was researched while keeping independent
host/exchange safety and actual-fill authority at the execution boundary.

**Alternatives and trade-offs.**

| Route | What it buys | What it costs | Verdict |
|---|---|---|---|
| **MTC owns economic intent; Bridge owns execution/truth** | Backtest intent remains identifiable; Bridge still validates live account/exchange safety and owns recovery | Requires a versioned intent contract, parity work, and Bridge support for TP legs/baskets | **Preferred** |
| **Bridge owns the whole lifecycle** | One live component decides and executes everything | Duplicates/discards MTC lifecycle rules; live behavior can stop matching the researched strategy | Viable only if Bridge becomes the tested canonical strategy engine; not preferred |
| **MTC directly controls exchange orders** | Minimal translation between strategy and exchange | Couples research logic to broker state, credentials, retries, reconciliation, and recovery; weakens the independent safety boundary | Rejected for the planned architecture |
| **Shared packaged lifecycle library** | Pine-adjacent Python and Bridge could call one implementation, reducing code drift | Couples releases and still does not solve Pine parity or actual exchange-truth ownership by itself | Strong future option, not a substitute for the ownership contract |

**Open points / implementation gate — OPEN.** Before any MTC-to-Bridge order or
exit integration, an accepted **Order and Exit Lifecycle Contract** must define
and evidence at least:

- [ ] accepted Pine ↔ Python entry/exit, break-even, trail, TP, and add/basket
      semantics, including any deliberately bounded differences;
- [ ] a versioned `OrderIntent` / `ExitIntent` schema, tied to A10's identity,
      timing, account, quantity-unit, policy-version, and provenance fields;
- [ ] TP-leg identity, price, quantity/fraction, order, activation, OCO or
      cancellation behavior, and what happens when TP1 only partly fills;
- [ ] add/basket lifecycle identity and whether each quantity is a delta or a
      target total position;
- [ ] stop-update authority, freshness, ordering, idempotency, and the exact
      monotonic/tightening rule;
- [ ] whether the strategy stop is native or synthetic, and the separate name,
      level, authority, and reporting of any emergency native safety stop;
- [ ] same-bar stop/target collision behavior in simulation versus continuously
      active real exchange orders;
- [ ] partial-entry, partial-TP, partial-close, late-fill, and overfill behavior;
- [ ] restart/reconciliation authority and which component may re-create,
      cancel, replace, or flatten each owned order;
- [ ] exact validation tolerances and loud reject reasons — never silent
      mutation on mismatch;
- [ ] dashboard fields that keep desired, accepted/rejected, acknowledged,
      partially filled, and actually closed state visibly separate; and
- [ ] regression, falsification, integration, restart, and exchange-adapter
      evidence required before activation.

**No implementation, wiring, configuration change, deployment, TESTNET/mainnet
activity, order placement, ARM, or economic action is authorized by this
section.**

### A12. Backend OPEN Questions

- [ ] Shared feed vs. per-worker feed.
- [ ] **Worker isolation strength** (referenced by A2) — what boundary a
      "worker" actually is: separate OS process, separate container, or
      in-process task with enforced state separation, and what each guarantees
      when one worker fails.
- [ ] Per-worker SQLite vs. central Postgres.
- [ ] Worker identity granularity.
- [ ] Subaccount fallback when subaccounts are unavailable.
- [ ] Aggregate risk rules (exact thresholds and interaction with Guardian).
- [ ] Sizing Ownership Contract / `OrderIntent` schema (full checklist in A10).
- [ ] Order and Exit Lifecycle Contract (full checklist in A11), including
      Multi-TP/basket representation and native-vs-synthetic stop semantics.

---

## PART B — DASHBOARD V2

### B1. One Combined Execution Dashboard

**Status:** DIRECTION — preferred future design, not yet approved for
implementation.

**Problem or question discovered.** With several workers running, where does
the owner look to see what is happening — one screen per strategy, or one
screen for everything?

**Evidence and reasoning.** One screen per strategy makes the aggregate
invisible, which is exactly the blind spot the Portfolio Guardian exists to
cover (A5). A single screen that also tried to run backtests would blur the
line between research and execution, and that line is what keeps unapproved
strategies out of live trading (see §1).

**Decision / offered direction.**

- A **single execution dashboard** with **per-strategy drill-down**.
- The **research dashboard remains separate**. The execution dashboard does
  **not** backtest and does **not** promote strategies.

**Alternatives and trade-offs.**

- *One dashboard per worker* — simple to build, no aggregate view.
- *One dashboard for research and execution together* — fewer tools, and it
  puts a "promote this" button next to a live account.
- *Combined execution view + separate research view* (preferred) — two
  surfaces to maintain, one clear boundary.

**Open points / implementation gate.** Same-VPS placement is settled in B8;
the detailed access and service-isolation model remains open in B9. No
dashboard implementation is authorized.

### B2. Frozen Packages Only

**Status:** DIRECTION — preferred future design, not yet approved for
implementation.

**Problem or question discovered.** If the dashboard can prepare a strategy for
execution, what stops preparation from *being* execution — a mis-click that
starts trading?

**Evidence and reasoning.** Selecting, preparing, and arming are three separate
intentions and they must be three separate actions. Anything else means the
system can start trading as a side effect of someone looking at it. The
research boundary in §1 supplies the other half: only frozen, approved packages
are eligible to be prepared at all.

**Decision / offered direction.**

- Only **frozen, approved packages** may be prepared for execution.
- Choosing or preparing an approved package **never ARMs and never trades**;
  activation is a **separate gated action**.

**Alternatives and trade-offs.**

- *Prepare-and-arm in one step* — fewer clicks, and no recovery from a
  mis-click.
- *Allow non-frozen packages in "test mode"* — flexible, and creates a path by
  which unapproved code reaches an execution surface.

**Open points / implementation gate.** How to stage a change without arming it
is explicitly open (B9). No activation mechanism is authorized here.

### B3. Overview Content

**Status:** DIRECTION — preferred future design, not yet approved for
implementation.

**Problem or question discovered.** What must be visible at a glance for the
owner to know the system is healthy — and, when it is not trading, *why* it is
not trading?

**Evidence and reasoning.** "Nothing is happening" has two very different
causes: no signal, or a blocked signal. Without a **block reason** on screen,
those look identical, and a silently blocked system can be mistaken for a
quiet one for days. Freshness matters for the same reason — a frozen feed also
looks like a quiet market.

**Decision / offered direction.** The overview shows:

- Aggregate equity, P&L, exposure, and risk.
- Each worker's **ARM/DISARM/KILL state** and **account/subaccount label**,
  plus health, freshness, version, symbol, timeframe, positions, orders, last
  decision, and block reason.

**Alternatives and trade-offs.**

- *Minimal overview (P&L only)* — clean, and hides exactly the diagnostic
  fields that matter during an incident.
- *Everything on one screen* — complete, and unreadable; the drill-down in B4
  exists so the overview does not have to carry detail.

**Open points / implementation gate.** Alerting on these fields is open (B9).
No implementation is authorized.

### B4. Drill-Down Views

**Status:** DIRECTION — preferred future design, not yet approved for
implementation.

**Problem or question discovered.** When one worker misbehaves, what does the
owner need in order to understand it without reading logs on a server?

**Evidence and reasoning.** The questions asked during an incident are
predictable and distinct: what is it holding, what did risk block, what
happened in sequence, is the machine healthy. Grouping the answers by question
means the answer is one click away instead of one search away.

**Decision / offered direction.** Per-strategy drill-down includes:

- **Overview**
- **Trading**
- **Risk/Gates**
- **Journal**
- **System**
- **AI Assistant**

**Alternatives and trade-offs.**

- *One long page per worker* — no navigation to design, hard to scan under
  pressure.
- *Logs only* — complete and unfiltered; unusable for a non-technical owner,
  which defeats the purpose.

**Open points / implementation gate.** Retention policy for journal/history is
open (B9). No implementation is authorized.

### B5. Access Control

**Status:** RECORDED — established current boundary.

**Problem or question discovered.** A dashboard that can see a live trading
account is a target. What is the minimum before it may be reachable from
outside the machine?

**Evidence and reasoning.** Loopback-only access has no remote attack surface
at all, which is why it is the starting position. Any step beyond loopback
turns the dashboard into an internet-facing surface attached to money, and the
identity controls have to exist *before* that step, not after.

**Decision / offered direction.**

- **Private loopback access first.**
- **Login, 2FA, and roles** are required before any public exposure.

**Alternatives and trade-offs.**

- *Public with a password only* — convenient, and one credential leak from
  full access.
- *VPN / tunnel instead of public exposure* — strong and practical; it does not
  remove the need for login and roles once more than one person can reach it.

**Open points / implementation gate.** Same-VPS placement is settled in B8;
the exact private-access topology and remote-control scope remain open (B9).
This records a boundary in force; it authorizes no exposure.

### B6. AI Assistant (Read-Only Start)

**Status:** DIRECTION — preferred future design, not yet approved for
implementation.

**Problem or question discovered.** An assistant that can read the trading
system is useful. What may it be allowed to *do*, and when?

**Evidence and reasoning.** Reading is recoverable; acting is not. An assistant
with order, ARM, risk-config, or fund authority can cause economic loss from a
single bad inference, and the same inference in read-only mode produces a wrong
sentence the owner can ignore. There is also no way to grant "a little" order
authority — the capability either exists or it does not.

**Decision / offered direction.**

- AI starts **read-only**.
- It may **explain, summarize, query, report, and alert**.
- It **cannot** order, ARM, change risk/config, move funds, widen stops, or
  increase leverage.
- **Later AI authority is separate, explicit, gated work** — not implied by
  this document.

**Alternatives and trade-offs.**

- *Assistant with write authority behind a confirmation* — faster operations,
  and confirmation prompts are approved reflexively by tired humans.
- *No assistant at all* — no new risk surface, and no help interpreting a
  multi-worker system.
- *Read-only first* (preferred) — full explanatory value, zero economic
  authority; the cost is that the owner still performs every action.

**Open points / implementation gate.** AI provider, model, cost, and memory
policy are open (B9); the *sourcing route* for the initial assistant is settled
in B7. Any write authority is separate, explicit, gated work and is **not**
authorized here.

### B7. AI Sourcing — Subscription vs. API, Dashboard Assistant vs. Bridge Gate

**Status:** DIRECTION — preferred future design, not yet approved for
implementation. Records a decided *sourcing boundary*; it authorizes no
implementation, no account use, no credential creation, and no activation.

**Problem or question discovered.** Two separate questions were being answered
as if they were one: (1) what should power the dashboard's read-only assistant
(B6), and (2) what should power a possible future LLM gate on the VPS Bridge.
Treating them as one component invites a single AI identity with both an
explanatory role and a trading-path role. A third question rode along with
them: whether **Hermes** is needed for any of this, and whether the owner's
existing **Codex/ChatGPT subscription** can serve as application AI access.

**Evidence and reasoning.**

- **Hermes is not needed for the dashboard.** The dashboard's B6 role is
  explanatory and read-only. Nothing in that role requires an agent harness.
- **A subscription is not application API access.** The owner's Codex/ChatGPT
  subscription entitles *interactive* use through the Codex app/CLI under a
  personal login. An **embedded, automatic, server-side dashboard chat** — one
  that the dashboard calls on its own behalf — normally requires **separately
  billed API access**, not the subscription. These are different products with
  different terms, and the distinction is the reason the initial route avoids
  embedded chat entirely.
- **Current OpenAI product facts are re-verifiable, not frozen.** Plan
  entitlements, Codex CLI capabilities, and API terms change. Everything stated
  here about them must be **reverified against live vendor documentation before
  implementation** — the same standard A3 and A4 apply to exchange mechanics.
- **The trading path has different requirements from the dashboard.** A Bridge
  gate must run unattended and predictably, answer in a strict structured form,
  return quickly, hold its own credentials, and stay inside enforced rate and
  cost limits. An interactive subscription login — with its own quota rules,
  session/auth renewal, and coding-agent tooling — carries none of those
  guarantees and puts a login state in the trading path.

**Decision / offered direction.**

*Dashboard assistant (initial route).*

- The dashboard **does not need Hermes**.
- Initial owner analysis uses the **owner's existing Codex/ChatGPT subscription
  through the Codex app/CLI**, driven **manually** by the owner against a
  **dashboard-produced read-only analysis package** or an equivalent controlled
  read-only context.
- This route **avoids initial API cost** and grants the AI **no write and no
  economic authority** — the assistant reads a package the owner hands it and
  returns sentences.
- **Embedded automatic server-side dashboard chat is not part of the initial
  route**, precisely because it would need separately billed API access.

*Future VPS Bridge LLM gate (optional, initially OFF).*

- If a Bridge LLM gate is ever enabled, it uses a **narrowly scoped provider
  API with independent service credentials** — **not** Codex CLI and **not** an
  interactive subscription login.
- The gate is **initially OFF**, so **initially there is no LLM API usage and no
  LLM API cost** on the Bridge side.
- **No claim is made that the Bridge currently calls OpenAI or any LLM
  provider.** It does not. This describes an optional future component only.
- Reasons for the API route: unattended predictable operation; a strict
  structured **PASS / VETO / NO_TRADE** (or direction-restriction) response
  contract; low latency; independent credentials; enforceable rate and cost
  limits; **no shell, filesystem, Git, or coding tools**; and keeping
  subscription login/quota changes out of the trading path.

*Hard fence on the gate.* If enabled, the gate **never** changes Bridge code or
configuration, **never** ARMs, **never** originates an order, **never**
increases size or leverage, and **never** widens a stop. Its only possible
effect is to **withhold or restrict** — consistent with B6's read-only posture
and A5's veto-not-mutate rule.

*Codex subscription on a headless machine.* Running Codex CLI under the owner's
subscription on a trusted headless machine is **technically possible** and is
**rejected for the Bridge hot path** for the reasons above. It is acceptable
only as **separate, owner-initiated maintenance or analysis work outside the
trading path**.

*Two components, not one.* The **dashboard assistant** and the **Bridge gate**
are **separate logical components**. They may later share a provider or model,
but they require **separate prompts, separate identities and credentials,
separate permissions, separate budgets, and separate logs**. Anything they
exchange is an **audited structured or read-only record** — **not** unrestricted
agent-to-agent chat.

**Alternatives and trade-offs.**

| Route | What it buys | What it costs | Verdict |
|---|---|---|---|
| **Hermes as the dashboard assistant** | An existing agent harness | Agent capability far beyond a read-only explainer; another surface to constrain | **Not needed** |
| **Embedded API chat from day one** | Best UX; no manual package step | Separately billed API access, credentials, budgets, and retention policy — all before any value is proven | Deferred, not rejected |
| **Codex CLI inside the trading path** | Reuses a subscription already paid for | Interactive login and quota state in the trading path; coding/shell tools next to money; unpredictable unattended behavior | **Rejected** |
| **One shared AI component for dashboard and gate** | One thing to build | Merges an explanatory identity with a trading-path identity; one prompt, one credential, one budget, one log for two different risk classes | **Rejected** |
| **Manual read-only package + Codex subscription** (preferred initially) | Zero initial API cost; no AI write or economic authority; usable now | Manual step for the owner each time; no automatic in-dashboard answers | **Preferred initially** |

**Open points / implementation gate — OPEN.**

- [ ] Read-only analysis package / controlled context **format** (what it
      contains, how it is generated, how it is bounded).
- [ ] **When**, if ever, embedded dashboard chat is introduced, and what would
      justify the API cost.
- [ ] **Exact API provider and model** for the future Bridge gate.
- [ ] **Credential handling** for independent service credentials.
- [ ] **Budgets** and enforced rate/cost limits.
- [ ] **Retention** of prompts, responses, and gate decisions.
- [ ] **Activation criteria** for turning the Bridge gate from OFF to ON.
- [ ] Reverification of current OpenAI product facts (plan entitlements, Codex
      CLI capability, API terms) against live vendor documentation.

**Documentation only.** No implementation and no activation is authorized by
this section — not the package generator, not embedded chat, not the Bridge
gate, and not any account, credential, or spend.

### B8. Same-VPS Dashboard Placement

**Status:** RECORDED — owner-approved hosting direction; not an implementation
or deployment authorization.

**Problem or question discovered.** Was the dashboard always intended to run
with the Bridge on the Hostinger VPS, or was that suggested only after the
owner asked about PC and phone access? If it is on the same VPS, does
"separate logical component" mean a second service already exists?

**Evidence and reasoning.** Dashboard V1 and the local-to-small-VPS direction
predate this conversation: the current V1 ships static dashboard assets inside
the Bridge and the same FastAPI application serves them on loopback
`127.0.0.1:8790`. It is therefore a separate *responsibility and permission
surface*, but **not a separate deployed process or service today**. On
2026-08-16 the owner made dashboard availability completion-critical for the
KVM2 package; that added a pinned private SSH-tunnel launcher and D3 dashboard
verification. It strengthened the deployment acceptance criteria rather than
inventing the underlying dashboard.

Running the dashboard beside the Bridge means it remains available while the
owner's Windows PC is off, reads Bridge state locally without a cross-host API,
and avoids paying for and operating a second server. The owner's PC or phone
only renders the browser interface. Colocation also creates a shared-resource
and shared-failure concern: dashboard load must not starve or destabilize the
execution path, and V1's same-process packaging must not be described as if
process isolation already existed.

**Decision / offered direction.**

- Host the **execution dashboard on the same Hostinger VPS as the Bridge**.
- Keep Bridge/dashboard traffic private and local; **port 8790 is never
  exposed directly to the public internet**.
- Treat the dashboard as a separate logical responsibility/security boundary:
  it observes and requests permitted owner actions, while the Bridge backend
  remains the authority that validates or rejects them. The dashboard cannot
  invent strategy decisions or bypass state, risk, reconciliation, or broker
  gates.
- Preserve the exact V1 fact: dashboard assets are bundled into and served by
  the same loopback FastAPI Bridge process. Whether Dashboard V2 remains there
  or becomes a separately limited loopback service is an OPEN implementation
  choice, not a completed feature.
- Private PC/phone access is the direction; the exact tunnel/VPN/identity-proxy
  and login/2FA/role design remains separately gated. AI remains read-only.
- This decision makes **no claim that Bridge or Dashboard V1 is currently
  installed or running on KVM2**, and authorizes no host contact or change.

**Alternatives and trade-offs.**

| Placement | Benefit | Cost / risk | Direction |
|---|---|---|---|
| **Dashboard on the owner's Windows PC** | No extra VPS UI process | Unavailable when the PC is off; requires a remote Bridge API and splits operations | Rejected for execution monitoring |
| **Dashboard on a second VPS** | Stronger host-level separation | Extra cost, credentials, networking, monitoring and cross-host attack surface | Deferred unless measured isolation needs justify it |
| **Same VPS, same FastAPI process** | Already matches V1; simplest local data path | Dashboard and Bridge share a process and resources | Current V1 fact, not a permanent V2 mandate |
| **Same VPS, separate loopback service** | Better process/resource separation while keeping traffic local | More deployment, authentication, health-check and upgrade complexity | OPEN V2 option |

**Open points / implementation gate — OPEN.**

- [ ] Keep V2 in the V1 FastAPI process or introduce a separately constrained
      loopback dashboard service after measuring load and failure behaviour.
- [ ] Prove that dashboard requests, refreshes and history queries cannot
      starve or materially delay the Bridge execution path; set resource and
      query limits appropriate to the chosen process model.
- [ ] Choose the exact private access topology and its authentication: pinned
      SSH tunnel, VPN, or an identity-aware HTTPS gateway. This section selects
      none of them as the permanent answer.
- [ ] Define login, 2FA, roles, session expiry, audit logging and remote-control
      scope before any non-loopback or phone control is enabled.
- [ ] Verify responsive phone monitoring separately; mobile support is not
      implied merely by same-VPS placement.

**Documentation only.** No Dashboard V2 service split, login, network exposure,
deployment, KVM2 action, ARM, order, credential or economic action is
authorized by this section.

### B9. Dashboard OPEN Questions

- [x] Host placement: same Hostinger VPS as the Bridge (B8). Exact service and
      private-access topology remain open.
- [ ] Remote control scope.
- [ ] AI provider / model / cost / memory. *(The sourcing boundary is decided in
      B7 — Hermes not needed; initial route is the owner's Codex/ChatGPT
      subscription used manually against a read-only package; a future Bridge
      gate would use a separately credentialed provider API and starts OFF.
      What remains open here is the exact provider and model, actual cost and
      budgets, and the assistant's memory/retention policy.)*
- [ ] Alerts.
- [ ] Mobile support.
- [ ] Retention policy.
- [ ] Prepare-but-not-activate changes (how to stage without arming).

---

## 3. Change Log

| Date       | Change |
|------------|--------|
| 2026-08-16 | Initial record: Backend V2 and Dashboard V2 design direction. Documentation only; no implementation authorized. |
| 2026-08-16 | **Rationale-preserving rewrite.** Every substantive topic (A1–A9, B1–B6) restructured into six explicit fields — Status; Problem or question discovered; Evidence and reasoning; Decision / offered direction; Alternatives and trade-offs; Open points / implementation gate — so a later agent can see *why* each call was made, not only what was decided. RECORDED / DIRECTION / OPEN semantics and the documentation-only authority fence are unchanged. Rationale for the six-field shape added to §0. |
| 2026-08-16 | **New A10 — Position-Sizing Ownership (MTC vs. Bridge).** Records a newly discovered future integration conflict: MTC_V2 already owns sizing in Pine and Python (direction-specific risk %, frozen equity snapshot, contract multiplier, leverage cap, quantity step, minimums, no-stop fallback, adds/pyramiding state) while the Bridge's `Signal` carries no `qty` and its `RiskEngine` originates its own quantity at a different default (1.0 % vs 0.5 % — 0.05 BTC vs 0.025 BTC on $10,000 equity / $60,000 entry / $58,000 stop). No present runtime clash: MTC_V2 and the Keltner Bridge candidate are not connected. Preferred DIRECTION recorded (MTC Python engine canonical sizing owner; Bridge as independent execution-safety envelope that validates and then executes exactly or rejects and logs; no silent resize; Guardian may veto but not silently mutate), plus four alternatives with trade-offs and an OPEN Sizing Ownership Contract / `OrderIntent` schema checklist. Preferred design direction only — **no implementation approved.** The fixed `wt_amount` in the MTC WunderTrading alert is recorded as a separate unresolved parity issue. |
| 2026-08-16 | Renumbering: former A10 "Backend OPEN Questions" is now **A11** (A10 is the new sizing-ownership section) and gains one entry for the Sizing Ownership Contract. Dashboard sections B1–B7 keep their numbers. Related links extended with the MTC and Bridge sources cited as evidence. |
| 2026-08-16 | **Accuracy and contract-completeness repair round.** Corrections to statements that were imprecise or overclaimed against source, plus a materially expanded intent schema. Six-field structure and the documentation-only / no-implementation authority fence unchanged; no verdicts recorded here. (1) **A7** no longer implies all-in is Signum's only sizing mode — `07_BROKER_DECISION.md` records all-in, "let strategy decide" absolute sizing, and custom-JSON percentage sizing; the section now declines Signum's *optional* all-in mode and states that the disqualifying property is market-only execution with synthetic SL/TP, not its sizing menu. (2) **A8** no longer claims every failure mode first appears with the second worker: two workers is stated as the minimum configuration for testing netting (A4), aggregate risk (A5), and state isolation (A6), while the A10 sizing conflict is recorded separately as existing with the *first* MTC-connected worker and required to be resolved before any MTC-to-Bridge integration. (3) **A8/A9 and §0** runtime wording tightened to "current authorized baseline V1 scope or build" — the "unchanged, current", "operating system", and "only working system" phrasings are removed so no sentence implies V1 runtime status, while the do-not-destabilize/delay requirement is preserved. (4) **A10** no longer calls Pine and Python the same contract/identical implementations. Two OPEN parity gaps are recorded from source: Pine's stop-risk raw qty divides by `stop_distance * contract_multiplier` (line 351) while Python divides by `stop_distance` only (line 47) despite using `contract_multiplier` in its leverage cap (52–54) and notional check (66); and Python gates on `min_notional` (66–68) where Pine has no equivalent gate. Both must be closed or explicitly bounded (e.g. multiplier = 1) before Python is appointed production canonical or MTC is integrated — the preferred DIRECTION that Python *should become* canonical is kept but now gated on gap closure plus an accepted frozen sizing contract. The BTC arithmetic is marked as assuming `contract_multiplier = 1` and a step/rounding/minimum that does not change the raw values. `pyramiding=100` is recorded as a deliberately generous broker ceiling only, with script-level `max_entries` (default 1) as the actual add permission, making basket/add behavior conditional. Pine sizing range corrected to lines 339–361. (5) **A10** Bridge-cap wording replaced: 0.05 BTC = $3,000 exceeds the current numeric $2,000 cap; today's Bridge cannot receive an MTC-requested quantity and evaluates its own quantity; a future validator retaining this threshold would reject the MTC request. (6) **A10** `OrderIntent` checklist expanded, preserving every prior field and adding `intent_id`/`decision_uid`; creation, signal, and expiry/freshness timestamps; symbol, venue, account/subaccount, side, timeframe; quantity unit and delta-vs-target-position semantics; sizing branch and `fallback_size_pct`; risk-percent scale convention (1.0 = one percent vs 0.01); sizing-policy version or immutable hash; and add/basket lifecycle identity, sequence, position context, and pyramiding quantity semantics. Also: A2's worker-isolation-strength question added to A11 so the cross-reference resolves; the "only MTC occurrences" claim scoped to the `bridge/` package (`bridge/app.py` lines 32 and 35); A4's Hyperliquid netting mechanics given the same reverification caveat as A3, since no authoritative local exchange citation exists and nothing was browsed. |
| 2026-08-16 | **New B7 — AI Sourcing (subscription vs. API; dashboard assistant vs. Bridge gate).** Records that the dashboard does **not** need Hermes and that initial owner analysis uses the owner's existing Codex/ChatGPT subscription through the Codex app/CLI, driven manually against a dashboard-produced read-only analysis package or controlled read-only context — avoiding initial API cost and granting the AI no write or economic authority. Distinguishes a subscription from application API access: embedded automatic server-side dashboard chat normally requires separately billed API access, and current OpenAI product facts are marked re-verifiable before implementation. Records that a future VPS Bridge optional LLM gate, if enabled, would use a narrowly scoped provider API with independent service credentials — not Codex CLI, not an interactive subscription — for unattended predictable operation, a strict structured PASS/VETO/NO_TRADE or direction-restriction contract, low latency, independent credentials, rate/cost limits, no shell/filesystem/Git/coding tools, and to keep subscription login/quota changes out of the trading path; the gate is initially OFF, so initially no LLM API usage or cost, and **no claim is made that the Bridge calls OpenAI today**. Hard fence recorded: the gate never changes Bridge code or config, never ARMs, never originates orders, never increases size or leverage, never widens stops — it can only withhold or restrict. Codex subscription on a trusted headless machine is noted as technically possible for Codex CLI but rejected for the Bridge hot path, acceptable only as separate owner-initiated maintenance/analysis outside the trading path. Dashboard assistant and Bridge gate are recorded as separate logical components that may later share provider/model but need separate prompts, identities/credentials, permissions, budgets, and logs, exchanging audited structured/read-only records rather than unrestricted agent-to-agent chat. Alternatives table covers Hermes (not needed), embedded API chat day one (deferred), Codex CLI in the trading path (rejected), one shared AI component (rejected), and the preferred initial manual read-only package + subscription route. OPEN: package/context format, embedded-chat timing, exact API provider/model, credential handling, budgets, retention, activation criteria, and OpenAI-fact reverification. Renumbering: former B7 "Dashboard OPEN Questions" is now **B8**, and the B7 cross-references in B1–B6 gates now point to B8; the B8 AI entry notes the decided sourcing boundary while keeping provider/model/cost/memory genuinely open. Documentation only; **no implementation or activation authorized.** |
| 2026-08-16 | **New A11 — Order and Exit Lifecycle Ownership (MTC vs. Bridge).** Records why similarly named entry/SL/TP/trailing/close concepts must not become two competing strategy brains. No present runtime clash: MTC_V2 and the Keltner plumbing candidate are not connected; current Keltner supplies its own initial stop and EMA8 trail, with TP disabled. Preferred DIRECTION: after accepted Pine/Python lifecycle parity, MTC Python owns exact desired economic intent; Bridge validates and either executes it exactly or rejects it, while owning real exchange identity, native protection, fills, reconciliation, restart recovery, and safe flattening. No silent mutation, stop widening, or simulated-fill substitution. Records the current blocking incompatibility: MTC fractional TP1/TP2 and conditional basket/add semantics cannot be represented by the Bridge's single full-quantity optional TP model. Leaves native-strategy-stop versus separately labelled emergency-native-stop semantics OPEN because the choice changes fills and parity. Adds the full Order/Exit Lifecycle Contract gate and desired/accepted/actual dashboard separation. Former A11 Backend OPEN Questions becomes **A12**. Documentation only; **no implementation or trading action approved.** |
| 2026-08-16 | **New B8 — Same-VPS Dashboard Placement.** Owner-approved direction: the execution dashboard lives on the same Hostinger VPS as the Bridge, remains private, and stays a separate logical responsibility/security boundary. Records the pre-existing V1 fact precisely: static assets are served by the same loopback FastAPI Bridge process, not a separate service. Records that the owner's 2026-08-16 completion-critical requirement added the pinned SSH-tunnel launcher and D3 verification rather than inventing the dashboard. Reasons: available while the PC is off, local state access, no second-server cost; shared-resource/failure risk must be tested. Alternatives cover owner-PC, second-VPS, current same-process V1, and possible separate-loopback-service V2. Exact service split, resource limits, private-access technology, login/2FA/roles, phone support and remote controls remain OPEN. Former Dashboard OPEN Questions is B9; cross-references updated. Gemini 3.7 Flash High supplied an isolated draft, and Codex corrected its separate-service assumption and premature technology selections before transfer. Documentation only; no deployment or live action authorized. |

---

## 4. Related Links

### Bridge documents

- [README.md](../README.md)
- [00_PREREG.md](./00_PREREG.md)
- [01_ARCHITECTURE.md](./01_ARCHITECTURE.md)
- [07_BROKER_DECISION.md](./07_BROKER_DECISION.md)

### Sources cited as evidence in A10

- [bridge/engine/types.py](../bridge/engine/types.py) — `Signal` (no `qty`),
  `OrderPlan` (`qty` created Bridge-side).
- [bridge/engine/risk.py](../bridge/engine/risk.py) — `RiskConfig`
  (`risk_pct_per_trade = 0.005`) and `RiskEngine` quantity computation.
- [MTC_V2.pine](../../MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine) —
  "04 Position Sizing" inputs, `calc_l6_qty` (lines 339–361, with the
  `contract_multiplier` denominator at line 351), the `pyramiding=100` broker
  ceiling (line 7) against the `max_entries` add permission (line 19, default
  1; enforced line 1800), and the fixed-`wt_amount` WunderTrading alert.
- [mtc_v2/core/position_sizer.py](../../MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_sizer.py)
  — `PositionSizer.calc_qty`, the "L6 risk-based quantity owner"; stop-risk
  denominator at line 47, `contract_multiplier` in the leverage cap (lines
  52–54) and notional check (line 66), `min_notional` gate (lines 66–68).
- [07_BROKER_DECISION.md](./07_BROKER_DECISION.md) — Signum's supported order-
  size modes and the market-only / synthetic-SL-TP reason it was not chosen
  (cited in A7).
- [mtc_v2/core/runner.py](../../MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py)
  — frozen per-bar equity snapshot feeding `calc_qty`.
- [MTC_V2_ARCHITECTURE.md](../../MTC_COMMAND_CENTER/01_MTC_PROJECT/03_DOCS/MTC_V2_ARCHITECTURE.md)
  — §7 Position Sizing Contract.

### Sources cited as evidence in A11

- [bridge/engine/orders.py](../bridge/engine/orders.py) — `OrderManager`
  submission reservation, role/quantity validation, fill ingestion, partial-fill
  recovery, reconciliation, re-protection, tightening-only stop updates, and
  close/flatten lifecycle.
- [bridge/broker/hyperliquid.py](../bridge/broker/hyperliquid.py) — native
  reduce-only SL/TP trigger construction, positioned-order verification,
  stop modification, re-protection, and flattening.
- [bridge/engine/engine.py](../bridge/engine/engine.py) — current strategy signal,
  risk-plan, trailing update, close, and `OrderManager` submission flow.
- [bridge/engine/types.py](../bridge/engine/types.py) — current `Signal` and
  single-`take_profit` `OrderPlan` shapes.
- [bridge/engine/strategies/keltner_trail_ema8.py](../bridge/engine/strategies/keltner_trail_ema8.py)
  — plumbing-test strategy, initial stop, `take_profit=None`, and EMA8 trail.
- [config/bridge.yaml](../config/bridge.yaml) — current `tp_mode: none` baseline.
- [25_PARTIAL_FILL_PROTECTION_CONTRACT.md](./25_PARTIAL_FILL_PROTECTION_CONTRACT.md)
  — exact live partial-entry protection and recovery contract.
- [MTC_V2.pine](../../MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine) —
  strategy entry/exit, stop, break-even, trailing, TP/Multi-TP, and conditional
  add/basket lifecycle.
- [mtc_v2/core/exits.py](../../MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py)
  — Python stop/TP book, break-even/trail ownership, Multi-TP, and simulated
  price-exit semantics.
- [mtc_v2/core/position_manager.py](../../MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_manager.py)
  — Python entry legs, same-side adds, partial exits, and basket lifecycle state.

### Official References

- Hyperliquid Sub-Accounts:
  https://hyperliquid.gitbook.io/hyperliquid-docs/trading/sub-accounts
- Hyperliquid Nonces and API Wallets:
  https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets
