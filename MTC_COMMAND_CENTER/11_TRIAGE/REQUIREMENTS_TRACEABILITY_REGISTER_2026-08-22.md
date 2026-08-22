# REQUIREMENTS TRACEABILITY REGISTER — CANONICAL

**Date:** 2026-08-22
**Status:** **Canonical requirements appendix.** Planning only — **implementation authorized: NO · audit acceptance of the technical brief: PENDING.**
**Governs:** `PROJECT_STARTING_POINT_AND_MAIN_OBJECTIVE_2026-08-22.md` (the owner's starting point and canonical outcome list), `OWNER_MASTER_PLAN_2026-08-22.md` (the owner-facing plain-English plan), `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md` (the canonical work-package IDs), `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md` (v2.1, repaired, **not yet accepted**).

**Correction note, 2026-08-22.** An earlier drafting pass populated this register from a *reconstructed* list of 44 outcomes that did not match the owner's canonical wording or order. That reconstruction has been replaced. §2 below now carries the canonical O-01 … O-44 in the owner's exact order and meaning, and every mapping in this file was rebuilt against it.

**Reconciliation note, 2026-08-22.** An earlier draft of this register carried its own coarse work-package scheme alongside the delivery plan's finer one. That duplicate scheme has been removed. **The `Work packages` column now cites the exact `WP-…` IDs defined in `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md`, and nothing else.** The requirement IDs themselves were not touched by this change.

**Owner acknowledgement note, 2026-08-22.** The owner has **acknowledged all twelve derived safeguards, D-01 through D-12**. D-01, D-03 through D-06 and D-08 through D-12 were acknowledged as written; D-02 and D-07 were acknowledged **with the clarifications recorded in their rows in §3**. **Acknowledgement does not change their source type: they remain DERIVED, and they were never original owner requirements.** The count is unchanged — **56 = 44 original owner outcomes (O-01…O-44) + 12 owner-acknowledged derived safeguards (D-01…D-12)**. **Acknowledgement is not implementation authorization, not audit acceptance, and not deployment or live authorization** (D-12); none of those has been given.

---

## 1. Why the number is 56

**56 = 44 original owner outcomes + 12 owner-acknowledged derived safeguards.**

- **O-01 to O-44 — OWNER.** The outcomes the owner asked for, preserved in his exact order and meaning (`PROJECT_STARTING_POINT_AND_MAIN_OBJECTIVE_2026-08-22.md` §3). **They are never renumbered and never rewritten into a different history.**
- **D-01 to D-12 — DERIVED, and acknowledged by the owner on 2026-08-22.** Safeguards produced by the architecture and audit work. They are enforceable engineering constraints. **The owner has now acknowledged all twelve — D-02 and D-07 with the clarifications recorded in §3 — but he did not originate them: they stay DERIVED permanently, and no document may present them back to him as if he had requested them.**

**Repository findings are not requirements.** The audit produced findings about the current state of the repository (five trade-logic implementations, an empty promotion registry, zero tags, and so on). They explain *why* some work exists; they are evidence, not requests. They are listed separately in §5 and are deliberately excluded from the count of 56.

### 1.1 Column definitions

| Column | Meaning |
|---|---|
| **ID** | Permanent identifier. Never reused, never renumbered |
| **Requirement** | Concise restatement. The canonical wording lives in the starting-point file §3; where the two differ, **§3 governs** |
| **Source** | `OWNER` or `DERIVED`. Where a ratified decision in brief §21.1 covers the same ground, its `Q` number is cited |
| **Brief §** | Section(s) of `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md` (v2.1) that carry the design |
| **Owner-plan §** | Numbered section of `OWNER_MASTER_PLAN_2026-08-22.md` that speaks to this requirement in the owner's own words. The nine section headings are listed in §1.3 below |
| **Work packages** | The exact `WP-…` IDs from `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md` that carry this requirement. Naming a package here is **not** authorization to start it |
| **State** | `COVERED` / `OPEN DECISION` / `FUTURE`, defined in §1.4 |
| **Acceptance / evidence pointer** | Brief acceptance criterion (`A-n`), migration milestone (`M-n`), decision-log id (`DL-n`), brief open item (`§21.2 O-n`), or approval gate — the gate set is **`G1`, `G1-IA`, `G2`…`G9`** in the delivery plan §9. **`G1-IA` — package implementation authorization — was inserted after `G1` on 2026-08-22 (brief §0.4 RF-T2-2) and applies to every package; `G2`…`G9` were not renumbered** |

### 1.2 Where work-package IDs come from

**There is one work-package scheme, and this register does not own it.** The canonical carriers are the exact `WP-…` IDs defined in `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md` — `WP-P0-01` … `WP-P0-19` (§4), `WP-V2A-01` … `WP-V2A-09` (§5), `WP-V2B-01` … `WP-V2B-09` (§6), `WP-V3-01` … `WP-V3-10` (§7), and `WP-V4-01` … `WP-V5-04` (§8).

Three rules govern the column:

1. **Every ID cited in this register must literally exist in that plan.** An ID that does not appear there is a defect in this register and is corrected here, not invented there.
2. **The plan owns scope; this register owns coverage.** If a package's objective changes, the plan is authoritative and this register's mapping is updated to match.
3. **A carrier is not a commitment.** Every package in that plan is a proposal, no package is authorized to start, and citing one here changes none of that.

Where a requirement is carried by governance rather than by a deliverable — the plan document itself, or an approval gate — the column says so explicitly and names the gate from the set **`G1`, `G1-IA`, `G2`…`G9`** (plan §9). **Citing a package or a gate is never authorization to start it: `G1-IA` requires the owner's explicit implementation authorization for every package, protected or not.**

### 1.3 Owner-plan section pointers

The `Owner-plan §` column points at these nine sections of `OWNER_MASTER_PLAN_2026-08-22.md`:

| § | Heading |
|---|---|
| **1** | Where I stand today |
| **2** | What I want the platform to be |
| **3** | What I want to see on screen |
| **4** | One strategy brain, one set of rules |
| **5** | Money safety: risk buckets, sizing and the Guardian |
| **6** | How a strategy earns its way to real money |
| **7** | Research I can look at |
| **8** | Tools, repository and AI context |
| **9** | Phases, decisions and what I have to approve |

### 1.4 State vocabulary

| State | Meaning |
|---|---|
| **COVERED** | A design exists in the technical brief **and** at least one named work package in the delivery plan carries it. Not "done" — designed and packaged |
| **OPEN DECISION** | Something must still be decided — by the owner, or by a measurement or inventory that has not run |
| **FUTURE** | Deliberately deferred to a later phase; carried, not forgotten |

**Naming collision, stated once.** Brief §21.2 numbers its *open items* `O-1 … O-10`. This register's `O-` IDs are *owner requirements*. They are unrelated. Cite them as "brief §21.2 O-n" and "register O-nn". Brief §3's `D-n` are *documentation drift* rows; this register's `D-n` are *derived safeguards*. Also unrelated.

---

## 2. Owner requirements — O-01 to O-44

Canonical order and meaning per `PROJECT_STARTING_POINT_AND_MAIN_OBJECTIVE_2026-08-22.md` §3.

| ID | Requirement | Source | Brief § | Owner-plan § | Work packages | State | Acceptance / evidence pointer |
|---|---|---|---|---|---|---|---|
| **O-01** | Modern dashboard presenting the whole system clearly | OWNER | §12.1, §12.5 | 3 | WP-V2B-05, WP-P0-14, WP-V3-01 | COVERED | A-15 |
| **O-02** | TradingView-like charting application inside the dashboard, showing positions, entries, exits, SL, TP, Multi-TP and trailing stops | OWNER | §12.2, §12.4 | 3 | WP-P0-18 (POC), WP-P0-14 (basic chart), WP-V2B-05 | FUTURE (V3) | Library choice is brief §21.2 O-3; A-19 covers Multi-TP execution, not the chart |
| **O-03** | Draggable SL/TP levels, staged simulation → testnet/paper → live under strict controls | OWNER | §12.4 | 3 | WP-V2B-08 (simulation), WP-V3-07 (paper/testnet), WP-V4-03 (live) | FUTURE (staged) | A-20 (eight paper invariants + chaos drill), A-22 (live step-up); gates G4, G5 |
| **O-04** | Find all overlaps and conflicts between MTC_V2, QuantLens, the backtest engines and Crypto Paper Bridge | OWNER | §2 F-1, §4.2, §4.3 | 4 | WP-P0-01, WP-P0-06, WP-P0-07, WP-P0-08, WP-P0-09 | COVERED | §4.3 overlap matrix; the parity-corpus, run-result and writer inventories |
| **O-05** | Simplify MTC_V2: essential strategy and position management in the core; advanced filters, exits, transforms optional or retired | OWNER | §5.3, §7.1, §7.2 | 4 | WP-P0-09, WP-P0-11, WP-P0-12 | COVERED | A-4; the module split is **DL-23, proposed and not owner-ratified** |
| **O-06** | Decide clearly where each responsibility belongs, so behaviour is not implemented repeatedly | OWNER | §4.1, §4.2, §5.1 | 4 | WP-P0-04, WP-P0-09, WP-V2A-03 | COVERED | §4.2 responsibility matrix; A-4 |
| **O-07** | One authoritative Python Strategy Kernel used by backtest, forward test, paper and live | OWNER (Q1) | §5.3, §7, §16 | 4 | WP-P0-09, WP-P0-10, WP-P0-11, WP-P0-12 | COVERED | A-4 (`mtc_v2` and `02_MTC_BACKTEST/src/engine` referenced by no runtime import) |
| **O-08** | Prevent Pine/TradingView from acting as a second order controller; monitoring and divergence warnings only | OWNER (Q3) | §8.1–§8.3 | 4 | WP-P0-19 (design only), WP-V4-07 (divergence alarm), then gate G2 | **OPEN DECISION — authorization** | G2. The decision exists (Q3/DL-07); **the edit is not authorized**; F-8 stands until then |
| **O-09** | Separate strategy-level rules from account/portfolio protection; centralize account controls in a Portfolio Guardian | OWNER | §7.1, §10.2 | 5 | WP-V2B-01 | COVERED | A-13; behavioural limits stay in the kernel so they remain simulated (documented split, §10.2) |
| **O-10** | Versioned contracts for signals, size requests, approved quantity, stops, targets and order instructions | OWNER (Q2a) | §5.4, §14.3 | 4 | WP-P0-04; runtime wiring is WP-V2A-05 | COVERED | A-1 — Phase 0 is **schema/consumer compatibility only**; Bridge runtime wiring is A-9 in V2A |
| **O-11** | Bridge runs multiple strategies simultaneously with isolated identity, state, positions and evidence | OWNER (Q4) | §6.7, §10.2 | 4 | WP-V2A-01, WP-V2A-02, WP-V2B-03 | COVERED | A-8 |
| **O-12** | Risk buckets (day, swing, position) with separate views, capital budgets and risk limits | OWNER | §10.1 | 5 | WP-V2B-01, WP-V2B-05, WP-V4-05 | COVERED — **values not set** | A-11; values are brief §21.2 O-5, O-6 |
| **O-13** | Every risk bucket starts at 1x leverage; increases require evidence | OWNER (Q18) | §10.1 | 5 | WP-V2B-01, WP-V2B-02, WP-V4-05 | COVERED | DL-21; 30/50/20 is a simulation hypothesis only. Any increase is a new owner decision |
| **O-14** | Hyperliquid first, with the broker boundary designed for later IBKR and equity swing trading | OWNER | §13.2, §17.2, §17.5 | 5 | WP-V2B-07, WP-V5-01, WP-V5-02 | COVERED (crypto) — IBKR FUTURE | Gates G4, G6. **F-9: the documented adapter layer does not exist today** |
| **O-15** | Bounded POCs of frameworks such as NautilusTrader; do not replace the hardened Bridge for feature count | OWNER (Q12) | §2 F-13, §13.2, §17.3 | 4 | WP-V3-08 | FUTURE (V3) | DL-16; integration-mode licensing review required (DL-36) |
| **O-16** | Permanent open-source-first policy with license, quality, maintenance, security and integration review | OWNER | §13.1 | 8 | WP-P0-16, WP-P0-17, WP-P0-18, WP-V3-08 | COVERED | §13.1 policy gates; DL-36, DL-38 |
| **O-17** | Prefer libraries and narrow adapters over importing a whole platform; custom code stays on strategy, risk, execution safety, reconciliation, operator workflow | OWNER | §13.1, §13.3 | 8 | WP-P0-18, WP-V3-08, WP-V5-01 | COVERED | §13.3 build-in-house list; operational-cost gate |
| **O-18** | One connected lifecycle: discovery → extraction → testing → validation → promotion → shadow → paper/testnet → portfolio → limited live → scale/suspend/retire | OWNER | §6.3 | 6 | WP-P0-13, WP-V2A-08, WP-V2B-07, WP-V3-03, WP-V4-02 | COVERED | §6.3 lifecycle; A-17, A-18 |
| **O-19** | QuantLens research improved so candidates pass early stages with fewer unnecessary steps | OWNER | §6.8 | 7 | WP-P0-07, WP-P0-13, WP-P0-14, WP-P0-16 | COVERED | §6.8 — step reduction without weakening gates. **F-21: do not rebuild the intake pipeline** |
| **O-20** | Test original source rules separately from the MTC-enriched version; show where the edge comes from | OWNER | §6.1 | 6 | WP-V3-01, WP-V3-03, WP-V3-09 | COVERED | A-17 (`SIGNAL_EDGE` / `SOURCE_COMPLETED_BASELINE` / `MTC_ENRICHED` comparison); DL-24 |
| **O-21** | Record missing source rules; complete them only from a small versioned standard catalogue; never silently invent | OWNER | §6.2 | 6 | WP-V3-03, WP-V3-09 | COVERED | Missing-Rule Ledger in every promotion packet (A-17) |
| **O-22** | Missing SL/TP must not auto-block forward observation; no live capital until substitutes have evidence | OWNER | §6.2, §6.5 | 6 | WP-V2A-08, WP-V3-09, WP-V4-01 | COVERED | DL-24, DL-28; §6.5 eligibility states; gate G5 |
| **O-23** | Start forward-shadow observation early, in parallel with slower statistical validation | OWNER | §6.3, §6.6 | 6 | WP-V2A-08 | COVERED | §6.6 shadow leakage rules; DL-26 |
| **O-24** | Freeze every version before forward evidence; any code, parameter or module change creates a new package hash and evidence period | OWNER | §6.3 freeze rule, §6.7 | 6 | WP-P0-02, WP-P0-04, WP-V2A-01, WP-V2A-08 | COVERED | DL-25, DL-26; `package_hash` / `evaluation_run_hash` split |
| **O-25** | Many candidates into forward shadow; exchange testnet/live-paper kept to a smaller capacity-controlled cohort | OWNER (Q4) | §6.4, §6.5, §10.2 | 6 | WP-V2A-08, WP-V2B-03, WP-V2B-07 | COVERED | DL-27, DL-28; A-8 |
| **O-26** | Testnet fleet size set by measured exchange limits, reconciliation performance and reliability | OWNER (Q17) | §6.5 | 6 | WP-V2B-07 | COVERED | DL-20 reliability stop condition; gate G4 |
| **O-27** | A TradingView-like visual Backtest and Optimization Explorer | OWNER | §11.4 | 7 | WP-P0-14 (minimum), WP-V3-01 (full) | COVERED | A-7 (Minimum Explorer renders `TrialRecord`), A-16 |
| **O-28** | 100,000-trial runs filterable and inspectable without manual TradingView entry | OWNER | §11.2, §11.4 | 7 | WP-P0-13, WP-V3-01, WP-V3-02 | FUTURE (V3) | A-16 |
| **O-29** | Show parameters, search space, candles, trades, SL/TP movement, equity vs buy-and-hold, drawdown, statistics, walk-forward, robustness and rejection reasons | OWNER | §11.1, §11.4 | 7 | WP-P0-13, WP-P0-14, WP-V3-01 | COVERED | A-7 (`rejection_reasons`, `search_regime`, `family_size`, `simulator_class`) |
| **O-30** | One compact record per trial; full artifacts for selected candidates; deterministic replay for the rest | OWNER (Q9) | §11.2, §11.3 | 7 | WP-P0-13, WP-V3-02 | COVERED | A-7, A-16; replay-time target is brief §21.2 O-8 |
| **O-31** | Experiment and artifact formats optimizer-independent; compare Optuna before adopting it | OWNER | §11.1, §13.2 | 7 | WP-P0-04, WP-P0-13, WP-P0-16, WP-P0-17 | **OPEN DECISION** | DL-29; brief §21.2 O-2. **F-11: two optimizers already exist side by side** |
| **O-32** | Immutable candidate identity across the lifecycle; statistical, shadow, paper and live evidence bound to the exact package hash | OWNER | §6.7 | 6 | WP-P0-04, WP-V2A-01, WP-V3-03 | COVERED | DL-25; A-18 (loader accepts only hashes traceable to a decision artifact) |
| **O-33** | Separate research and execution trust domains: research read-only and credential-free, execution authenticated and independently audited | OWNER | §12.1, §14.2 | 8 | WP-P0-14, WP-V2B-05, WP-V2B-06 | COVERED | DL-32, DL-33; one owner-facing entry point permitted, execution independently reachable |
| **O-34** | Chart-library POC before permanent selection — draggable levels, Multi-TP, trailing history, touch support | OWNER (Q19) | §12.2 | 7 | WP-P0-18 | **OPEN DECISION** | DL-22; the selection is brief §21.2 O-3 and closes on the POC |
| **O-35** | Redesign project AI context and AI_MEMORY for token efficiency before large V2 work | OWNER | §15, §2 F-18 | 8 | WP-P0-05 | COVERED | A-3 — numeric before/after required, not an assertion |
| **O-36** | Stage-local instructions, inputs, outputs, tests and current handoff; history searchable but not loaded by default | OWNER | §15.2, §15.3 | 8 | WP-P0-05 | COVERED | A-3; §15.3 history-available-never-loaded rule |
| **O-37** | Record the clean-repository/archive idea and its refinement: implement and measure stage routing in the current repository first | OWNER (Q2b) | §14.1, §14.4, §15.1 | 8 | WP-P0-05, WP-V5-04 | COVERED as a recorded decision | DL-05; the topology answer is brief §21.2 O-1 |
| **O-38** | Contracts package defined in place now; one-vs-multiple repository topology deferred until measured | OWNER (Q2a, Q2b) | §14.3, §14.4 | 8 | WP-P0-04, WP-P0-05 (measurement), WP-V5-04, then gate G7 | **OPEN DECISION — topology** | A-1 for the package; G7 and brief §21.2 O-1 for the topology |
| **O-39** | Any later migration selective and reversible; inventory and preserve the existing repository as a read-only archive, never delete | OWNER (Q13) | §14.2, §16 M11, §16 M12 | 8 | WP-P0-01, WP-P0-02, WP-P0-03, WP-V2B-09, WP-V5-04 | COVERED as a binding constraint | G8 — owner-approved exact deletion list, every target tagged first; M12 exit criteria |
| **O-40** | Kernel built as `LEGACY_COMPATIBLE` exact reproduction, then separately documented and tested `CORRECTED_VNEXT` fixes | OWNER (Q15) | §16 M7a/M7b | 4 | WP-P0-10, WP-P0-11, WP-P0-12 | COVERED | A-5, A-6 — no undocumented behavioural difference between the two |
| **O-41** | Classify historical backtest results by what their simulator modelled; keep useful evidence without treating signal screens as live-profit estimates | OWNER (Q14) | §9.4 | 7 | WP-P0-06, WP-P0-07, WP-P0-13, WP-V3-09 | COVERED | DL-31 lineage classes; A-17 (`simulator_class`, `UNSIMULATED_CONTROLS`) |
| **O-42** | One Master Plan divided into bounded subprojects, dependencies, decisions, acceptance gates and parallel workstreams | OWNER | §17, §22 | 9 | Governance — the delivery plan itself (§2 dependencies, §3 lanes, §9 gates); no single work package carries it | COVERED — **the plan itself is not accepted** | `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md` §2 dependencies, §3 lanes, §9 gates; gate G1 |
| **O-43** | Define what belongs in Phase 0, Bridge V2, V3, V4 and later; do not force every future feature into V2 | OWNER | §17.1–§17.5 | 9 | Governance — the phase assignment of every package from WP-P0-01 to WP-V5-04 in the delivery plan §4–§8 | COVERED | §17.2 V2A-then-V2B split; DL-37 (live Multi-TP is not a V2 acceptance requirement) |
| **O-44** | Answer the owner decisions affecting kernel, contracts, Pine, sizing, migration, risk buckets, testnet capacity and chart selection before implementation | OWNER | §21.1, §21.2 | 9 | Governance — gate G1; the measurements the open items wait on are WP-P0-05, WP-P0-06, WP-P0-07, WP-P0-16, WP-P0-18, WP-V2B-07 | **OPEN DECISION** | §21.1 Q1–Q19 answered and binding; **§21.2 O-1…O-10 still open**; G1 brief acceptance PENDING |

**Count check: O-01 … O-44 = 44 rows. No gaps, no duplicates, no renumbering.**

---

## 3. Derived safeguards — D-01 to D-12

**Source type for every row below: DERIVED.** None was requested by the owner. They are recorded as audit-derived safeguards, and the owner **acknowledged all twelve on 2026-08-22** — D-01, D-03…D-06 and D-08…D-12 as written, D-02 and D-07 with the clarifications stated in their rows. **Acknowledgement does not convert a derived safeguard into an owner requirement, and it authorizes nothing to be built, accepted or deployed.**

| ID | Safeguard | Source | Brief § | Owner-plan § | Work packages | State | Acceptance / evidence pointer |
|---|---|---|---|---|---|---|---|
| **D-01** | Keep `FORWARD_SHADOW`, `INTERNAL_PAPER`, `EXCHANGE_TESTNET` and `LIMITED_LIVE` distinct, and label what each proves | DERIVED | §6.4 | 6 | WP-V2A-08, WP-V2B-07, WP-V3-03, WP-V4-02 | COVERED | DL-27; every promotion record names its environment |
| **D-02** | One shared Risk Allocator computes quantity; the Guardian only authorizes or rejects; no silent resizing; the same allocator and policy run in the portfolio backtest. **Owner clarification, 2026-08-22: the no-resizing rule governs NEW-ORDER SIZING. It does not prohibit a separately authorized emergency reduction or closure of EXISTING exposure, which would be a distinct, explicit, tested safety policy — never silent resizing. This clarification authorizes neither the implementation nor the use of such a policy** | DERIVED (aligns with brief Q16), **acknowledged with clarification 2026-08-22** | §5.5, §9.2, §10.2 | 5 | WP-V2A-03, WP-V2A-04, WP-V2B-01, WP-V2B-02 | COVERED | A-10, A-10b, **A-11** — an unsimulated allocator fails acceptance (R-4). The existing-exposure distinction is brief Appendix E **O-11**, carried by **WP-V3-10** as design only |
| **D-03** | Native reduce-only exchange stop as the V2 protection baseline | DERIVED (aligns with brief Q7) | §5.4, §9.2 | 5 | **WP-V2A-06** (contract + **local** proof: emulator/replay placement, amend, cancel and a local process-kill/restart harness, **no credentials, no venue contact**) · **WP-V2B-07** (the **real** exchange-native protective-order and process-kill drill on **testnet**, under gate G4) | COVERED | DL-11; simulated as a continuously active protective order. **The process-kill proof is staged: local in WP-V2A-06, real-venue in WP-V2B-07 — V2A contacts no venue, and an emulated result is never presented as a real-venue result** (brief §0.4 RF-T2-3) |
| **D-04** | Promotion Authority separate from the Explorer; approval creates an immutable decision artifact | DERIVED | §11.5 | 6 | WP-V3-03 | FUTURE (V3) | A-18; DL-35 |
| **D-05** | Mark every operator intervention; separate pure-strategy from operator-modified performance | DERIVED | §12.4 | 6 | WP-V4-03, WP-V4-04 | FUTURE (V4) | A-23 |
| **D-06** | Show desired, authorized and actual execution state separately | DERIVED | §12.5 | 3 | WP-V2B-05 | COVERED | A-15 — three separate columns, never merged |
| **D-07** | First limited-live cohort: one strategy, ≤ 1 % of account equity. **Owner clarification, 2026-08-22: the 1 % is the MAXIMUM CAPITAL ALLOCATED to that first `LIMITED_LIVE` strategy. Loss-at-stop / risk-to-stop is a SEPARATE and LOWER cap, which must be defined and evidenced before any live authorization; no number for it is invented here** | DERIVED (aligns with brief Q11), **acknowledged with clarification 2026-08-22** | §17.4 | 6 | WP-V4-01, WP-V4-02 | FUTURE (V4) | A-24; DL-15; gate G5. **The separate lower loss-at-stop cap is an open item on the WP-V4-01 evidence pack and must carry a stated, evidenced value before G5** |
| **D-08** | Economic golden scenarios and D026 RED/GREEN falsification required for migration and parity claims | DERIVED | §9.3, §9.6, §16 M6 | 4 | WP-P0-10, WP-P0-11, WP-P0-12, WP-V2A-04, WP-V2A-07 | COVERED | A-5, A-6, A-10b, A-12; **25** golden families |
| **D-09** | Freshness, idempotency, acknowledgement, reconciliation and emergency-recovery controls for money-moving operations | DERIVED | §12.3, §12.4 | 5 | WP-V2B-05, WP-V2B-08, WP-V3-07, WP-V4-03 | COVERED (V2B) / FUTURE (V3 drag-and-drop) | A-15, A-20; the eight §12.4 invariants |
| **D-10** | Prevent false diversification via family, overlap, correlation and portfolio-cap controls **that are also simulated** | DERIVED | §10.3 | 5 | WP-V2B-02, WP-V3-04 | FUTURE (V3) | Correlation breach **rejects**, never trims (DL-34); simulated in `PortfolioSimulator` |
| **D-11** | Bind migration and deployment claims to exact accepted commits, package identities, simulator lineage and evidence | DERIVED | §6.7, §9.4, §16 M9 | 9 | WP-P0-03, WP-V2A-09, WP-V2B-04 | COVERED | M9 exit criteria; `package_hash` / `evaluation_run_hash` split |
| **D-12** | Distinguish owner decision approval, implementation authorization, audit acceptance, and deployment/live authorization | DERIVED | STATUS block, §0.3, **§0.4**, §8.3, §22 | 9 | Governance — gates **`G1`, `G1-IA`, `G2`…`G9`** in the delivery plan §9; no work package carries it. **`G1-IA` carries the implementation-authorization axis explicitly and applies to every package, protected or not** | COVERED | Gate table in the work-package plan §9, including **G1-IA — package implementation authorization** |

**Count check: D-01 … D-12 = 12 rows.**
**Canonical total: 44 + 12 = 56 tracked requirements.**

---

## 4. Coverage summary

| State | Owner (O) | Derived (D) | Total |
|---|---|---|---|
| COVERED | 35 | 8 | 43 |
| OPEN DECISION | 5 — O-08, O-31, O-34, O-38, O-44 | 0 | 5 |
| FUTURE | 4 — O-02, O-03, O-15, O-28 | 4 — D-04, D-05, D-07, D-10 | 8 |
| **Total** | **44** | **12** | **56** |

**COVERED never means done.** It means a design exists and a named work package in the delivery plan carries it. Nothing in this register has passed an acceptance criterion, because no implementation is authorized.

**One of the five OPEN DECISION rows — O-08 — is open only on *authorization*, not on the decision.** The owner has decided Pine should stop routing orders (Q3); nobody has authorized the edit. That distinction is exactly what D-12 exists to protect.

---

## 5. Repository findings — **evidence, NOT requirements**

These are what the audit found in the repository, cited to files and lines in brief §2 and Appendix A. **They must never be converted into requirement IDs, counted in the 56, or presented to the owner as things he asked for.** Where a finding motivates work, that work appears above under an existing requirement.

| Finding | What it is | Which requirement it motivates |
|---|---|---|
| **F-1** | Five independent implementations of trade lifecycle logic | O-04, O-07 |
| **F-2** | Position sizing computed three times with three different answers, plus a shipped-default hazard that floors crypto quantities to zero | O-06, O-07, O-10 |
| **F-3** | The promotion-deciding research engine simulates almost none of the production control set | O-18, O-41 |
| **F-4** | `mega_walk_forward.py` computes and discards per-trial data; other writers persist partial data under other names | O-29, O-30 |
| **F-5** | ~2.2 GB of unmanaged whole-file JSON artifacts | O-30 |
| **F-6** | The promotion registry has never been used — it is empty | O-18, O-32 |
| **F-7** | Parity status is corpus-dependent and the corpora are not comparable as they stand | O-04, O-40 |
| **F-8** | A live WunderTrading order path exists only in Pine, armed by typing one string, with no counterparty visibility | O-08 |
| **F-9** | The documented adapter layer does not exist | O-14, O-17 |
| **F-10** | The parity result **payload** is duplicated across two directories; the directories themselves differ | O-04, O-39 |
| **F-11** | Two optimizers side by side; Optuna already a dependency | O-31 |
| **F-12** | MTC_V2 is dormant; all active development is in the Bridge | O-05, O-07 |
| **F-13** | The Bridge's engineering quality is high and its dependency surface small | O-15 |
| **F-14** | Several accepted Bridge capabilities are not enabled by the default init path; deployed state unverified | D-11 |
| **F-15** | The LLM gate is dormant in the audited default init path; deployed state unknown | D-11 |
| **F-16** | The live-trading gate is an unsigned draft | O-22, D-07 |
| **F-17** | 137 local branches, 237 refs, **zero tags**, 8,031 tracked files, 8.7 GB working tree | O-24, O-39 |
| **F-18** | ~709,001 bytes ≈ 180,000 tokens of mandatory AI onboarding | O-35, O-36 |
| **F-19** | The working checkout is 60 commits behind master | O-39 |
| **F-20** | Bridge V1 dashboard surface — seven pages plus KILL | O-01 |
| **F-21** | The research intake pipeline works and is the healthiest part of the stack — **do not rebuild it** | O-19 |
| **F-22** | In the 2026-05-30 ~93k-configuration sweep, zero configurations survived the strict gates; the best DSR recorded anywhere is 0.492 against a 0.95 threshold | O-19, O-41 |

Drift items in brief §3 are documentation contradictions — also evidence, also not requirements. See the naming-collision note in §1.4 before citing them.

---

## 6. Change control

**These rules bind every document, agent and session that touches this register.**

1. **No new requirement without provenance and owner acknowledgement.** A new ID may be added only with: the exact source (a quoted owner statement with its date, or a named derivation), the source type, and — for anything presented as OWNER — the owner's explicit acknowledgement. An architecture conclusion is never promoted to an owner requirement.
2. **The 44 are never silently renumbered.** O-01 to O-44 keep their IDs permanently. If wording is corrected, it is corrected **in place** with a dated note recording the previous wording and the reason. Reordering, merging or splitting them is forbidden. The canonical wording lives in `PROJECT_STARTING_POINT_AND_MAIN_OBJECTIVE_2026-08-22.md` §3; if this register's concise restatement drifts from it, **§3 governs and this register is corrected**.
3. **New derived safeguards continue sequentially after the current D-01 … D-12 range.** **No future identifier is reserved, printed or referenced in advance: the next number is assigned only at the moment a safeguard is actually added**, and until then the range ends at D-12. New safeguards never take an O- number, and they are always labelled DERIVED in every document that repeats them.
4. **Findings never become requirements.** A repository finding may motivate work under an existing requirement; it may not acquire an ID here.
5. **Work-package references cite the delivery plan's IDs, and only those.** Every `WP-…` token in the mapping column must exist in `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md`. This register never defines a work-package scheme of its own. If a package there is renamed, split or merged, this register's mapping column is updated to match and the requirement IDs are untouched. **Citing a package is never authorization to start it.**
6. **State changes need evidence.** Moving a row to COVERED requires a named work package and a named acceptance pointer. Moving one to a "done" claim requires the acceptance criterion to have actually passed, with the command and output recorded — never an assertion.
7. **A decision is not an authorization.** Recording an owner decision (a `Q` or `DL` entry) never changes an OPEN DECISION row to COVERED on the authorization axis. D-12 governs; the gate table in the work-package plan §9 is where authorization is tracked.
8. **This register is the single source of truth for the count.** If any document states a different total than **56 = 44 + 12**, that document is wrong and is corrected against this one.
