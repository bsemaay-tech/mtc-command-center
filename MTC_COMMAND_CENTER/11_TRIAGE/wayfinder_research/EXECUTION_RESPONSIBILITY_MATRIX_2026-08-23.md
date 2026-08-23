# Execution-Path Responsibility Matrix

**Date:** 2026-08-23
**Wayfinder:** map [#79](https://github.com/bsemaay-tech/mtc-command-center/issues/79), research ticket [#88](https://github.com/bsemaay-tech/mtc-command-center/issues/88)
**Method:** document analysis only — no code executed, no source files opened. Every claim below is cited to `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md` (brief) and `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md` (WP plan), both at master `ab35ca66`, focused on brief §5, §9.7, §10, §11.5, §17.2/17.2a/17.2b and WP plan §5 (V2A) / §6 (V2B), with supporting reads of brief §6.2–6.9 and §12.3–12.5a and WP plan §7–§9 where an execution-path duty's owner could only be confirmed or ruled out there.
**Status of everything named below:** per WP plan §0, **no package is authorized**; "owner" in this matrix means "the document names this component as the responsible owner," not "this exists in running code."

---

## 1. How to read this matrix

For each macro responsibility on the frozen-package-to-broker-fill path, the table names:
- **Owner** — the component/role the documents assign the duty to, and the work package (WP) that builds it, where one exists.
- **Citation** — section(s) and, where useful, WP IDs.
- **Flag** — `CLEAN` (single named owner, no contradiction found), `DUPLICATED` (two components both claim it), `UNOWNED` (no WP or named role carries it), or `COUPLING` (one component's failure can silently corrupt another's duty without a named guard).

Three responsibilities turned out cleanly staged across multiple owners by design (K→OR→RA→P→B in sizing; local-proof-then-venue-proof in protection placement) — these are marked `CLEAN (staged)` rather than `DUPLICATED`, because the brief explicitly separates what each stage may and may not do (brief §5.5 "the ownership words, defined exactly," lines 1122–1134).

---

## 2. The matrix

| # | Responsibility | Owner(s) | Citation | Flag |
|---|---|---|---|---|
| 1 | **Loading** (verify `package_hash` + `deployment_identity_hash`, refuse unverified) | Frozen-package loader — **WP-V2A-01** | Brief §11.5 (lines 2107–2111, 2123); WP plan WP-V2A-01 (line 574) | CLEAN |
| 2 | **Admission check** (may this identity run in this environment) | Two-tier: **Environment Admission Authority — WP-V2A-10** issues `SHADOW_ELIGIBLE` (V2A) / `TESTNET_ELIGIBLE` (V2B); **Promotion Authority — WP-V3-03** is the *only* issuer of `PROMOTED` (mainnet/`LIMITED_LIVE`). The loader (WP-V2A-01) only **consults** records; it never issues one | Brief §11.5 "Two admission authorities" (lines 2093–2124); WP plan WP-V2A-10 (line 672), WP-V3-03 (line 846) | CLEAN (staged, deliberately two authorities to avoid a circularity — brief §0.6 R5) |
| 3 | **Sizing — stage 1, request** | Strategy Kernel (K) — **WP-P0-12** (kernel consolidation, referenced as an input at WP-V2A-03 line 599) | Brief §5.5 stage table (lines 1083–1089) | CLEAN (staged) |
| 3a | **Sizing — stage 2, bind (snapshot + policy identity)** | Decision Orchestrator (OR) — **not a separate WP**; explicitly "part of WP-V2A-03/04/05" | Brief §5.5 (line 1081, 1086); WP plan WP-V2A-03 "Added 2026-08-22" row (line 601, 604 mid) | UNOWNED-as-a-package (see §3.2 below) |
| 3b | **Sizing — stage 3, propose `proposed_qty`** (the only quantity computation in the system) | Risk Allocator (RA) — **first delivered by WP-P0-20** (research domain, canonical simulator migration); **wired into runtime, with import-identity proof, by WP-V2A-03** | Brief §5.5 stage table (line 1087), §9.1a (lines 1663–1669); WP plan WP-V2A-03 (lines 596–608) | CLEAN (staged, and the plan is explicit that WP-V2A-03 is *not* first delivery — R1 correction, line 598) |
| 3c | **Sizing — stage 4, authorize (final executable quantity is created here and nowhere else)** | Portfolio Guardian (P) — **WP-V2B-01** | Brief §5.5 stage table (line 1088); WP plan WP-V2B-01 (line 695) | CLEAN |
| 4 | **Order construction** (assemble the `OrderIntent` — identity, timing, economics, protection fields) | RA constructs the *candidate* `OrderIntent {proposed_qty}`; Guardian stamps it `AUTHORIZED_AS_REQUESTED` / `REJECTED`, which is what makes it final | Brief §5.4 `OrderIntent` schema (lines 1031–1040); §10.2 sequence diagram (lines 1840–1853, esp. "RA→P: candidate OrderIntent", "P→B: OrderIntent AUTHORIZED_AS_REQUESTED") | CLEAN (staged, same RA→P split as sizing) |
| 5 | **Authorization** (economic authority to let an order proceed) | Portfolio Guardian — **WP-V2B-01** (per-order authorize/reject) | Brief §10.2 (lines 1861–1869); WP plan WP-V2B-01 | CLEAN |
| 6 | **Protection placement** (native reduce-only stop: place/amend/cancel) | **Contract + local proof only, zero venue contact — WP-V2A-06.** Real-venue placement and the process-kill/restart survival drill — **WP-V2B-07 Lane B**. Live-environment day-to-day placement thereafter has **no named WP** — it is implicitly the existing Bridge Order Manager (brief §5.2 component E5), carried forward under the WP-V2A-05 intent seam | Brief §5.4 (lines 1042–1044); WP plan WP-V2A-06 (lines 630–637), WP-V2B-07 outputs Lane B (lines 774, 778) | CLEAN (staged local→venue) **but see COUPLING flag in §3.3** for the unnamed live-operation carrier |
| 7 | **Reconciliation** (confirm venue truth matches intended/authorized/accepted state) | Split across: WP-V2A-06 (local restart re-attachment fixture); WP-V2B-10 (KILL's two-part reconcile obligation, `PROTECTION_DRIFT`); WP-V2B-07 Lane A (daily three-way reconciliation for the paper soak, but it **consumes** "the three-way reconciliation tooling" as a pre-existing input, not something it builds); WP-V2B-05 (reconciliation *view* + drift alarm — display only); WP-V3-05 (live-vs-backtest divergence *reporting*). **No WP's Objective/Outputs is "build the reconciliation engine" itself** | Brief §9.6 test 3 (line 1780, "the Bridge already stores enough... it is not surfaced"); §10.2a (lines 1883, table row "Simulation / reconciliation / evidence"); §12.4 rule 7 (line 2263); WP plan WP-V2A-06 (line 633), WP-V2B-10 (line 811), WP-V2B-07 (lines 771, 777), WP-V2B-05 (line 742), WP-V3-05 (line 848) | **UNOWNED** (mechanism) / **COUPLING** — see §3.3 |
| 8 | **Event capture** (decision stream, observation ledger, audit logs, lifecycle-ledger appends) | Decision/intent stream: contracts package + WP-V2A-03/05. Shadow observations: **WP-V2A-08** + **WP-P0-22** (leakage ledger). Command audit records (DISARM/KILL/FLATTEN): **WP-V2B-10**. Drag-and-drop audit log: **WP-V2B-08 / WP-V3-07 / WP-V4-03**. Lifecycle Ledger appends: **Registrar** (funnel transitions) and **"the supervisor"** (post-live tail) — **both named as ledger writers in the brief with no corresponding WP anywhere in the plan** | Brief §11.5 fold paragraph (lines 2123, "Its only writers: the research-side Registrar... the Environment Admission Authority... the Promotion Authority... and the supervisor"); §12.4 rule 8 (line 2264); WP plan WP-V2A-08 (line 652), WP-V2B-10 (line 819) | **DUPLICATED-language / UNOWNED for two of four writers** — see §3.1 |
| 9 | **State persistence** (worker state, supervisor registry, lifecycle state) | Per-worker: **WP-V2A-02** (per-worker SQLite, hybrid store decision, wayfinder #41). Supervisor-side aggregate: **WP-V2B-03** ("central store holding only the worker registry/identity tuples and the derived aggregate portfolio snapshot — never an independent truth"). Lifecycle state: the **Lifecycle Ledger** itself (brief §11.5) — no WP builds the ledger's storage/append infrastructure | Brief §11.5 (lines 2123); WP plan WP-V2A-02 (line 588), WP-V2B-03 (line 716) | CLEAN for worker/supervisor state; **UNOWNED** for the Lifecycle Ledger's own storage — see §3.1 |
| 10 | **Feed handling** (market-data / order-state / fills / account-truth freshness: FRESH/AGING/STALE/UNKNOWN/DRIFT/DEGRADED/RECOVERING) | Market-data collection and the live/shadow feed itself: **WP-P0-30 (VEN-E)**. The seven-state **freshness state machine that blocks or warns on staleness (brief §12.3) has no WP that builds or enforces it** — only the narrower `AccountSnapshot` freshness check (`SNAPSHOT_STALE`, sizing-only) is owned, by **WP-V2A-04** | Brief §12.3 (lines 2179–2212, esp. line 2181 "Every authoritative domain... feeds a state machine"); WP plan WP-P0-30 (line 554), WP-V2A-04 (lines 610–618) | **UNOWNED** (general feed-freshness machine) — see §3.2 |
| 11 | **Restart recovery** | Worker-level: **WP-V2A-02** (restart/recovery fixture). Protective-order re-attachment: **WP-V2A-06** (local, emulator) then **WP-V2B-07 Lane B** (real venue). Shadow missed-decision catch-up: **WP-V2A-08** (state catch-up by replay, per wayfinder ticket #45). Bridge process/deployment rollback: **WP-V2B-11** (rehearsed rollback, walked not asserted) | WP plan WP-V2A-02 (line 588), WP-V2A-06 (line 633), WP-V2B-07 (line 774), WP-V2A-08 (line 653), WP-V2B-11 (line 827) | CLEAN — well distributed by layer, each with its own fixture |
| 12 | **Evidence reporting upward** (execution evidence flowing back to research/promotion) | Per-live-trade divergence: **WP-V3-05**. Promotion packet contents (Missing-Rule Ledger, A/B, `UNSIMULATED_CONTROLS`): **WP-V3-09** / **WP-V3-03**. Backtest-vs-forward divergence check that **blocks further promotion** (map #67 fold, brief §9.7): named as "a standing measured check per identity (§6.5 row)" with **no WP explicitly cited for it** in the sections read — closest candidates are **WP-P0-21** (objective eligibility criteria, §6.5) and **WP-V3-03** (Promotion Authority, which enforces the block) | Brief §9.7 (line 1790, "Backtest-vs-forward divergence is a standing measured check per identity... breach blocks further promotion and notifies the owner"); WP plan WP-V3-05 (line 848), WP-V3-09 (line 852), WP-V3-03 (line 846) | **AMBIGUOUS / likely UNOWNED as a distinct package** — see §3.4 |

---

## 3. Flags, expanded

### 3.1 Owned-by-none: the Lifecycle Ledger's own writers

Brief §11.5 (the map #54 fold paragraph, line 2123) names the Lifecycle Ledger's **only four writers**:

1. the research-side **Registrar** (all funnel transitions),
2. the **Environment Admission Authority** → mapped to **WP-V2A-10**,
3. the **Promotion Authority** → mapped to **WP-V3-03**,
4. **"the supervisor"** (post-live tail: "execution interlocks act first, the ledger append is automatic and mandatory — a suspension missing from the ledger is a defect").

A repo-wide grep of the WP plan (`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md`) for `Registrar` returns **zero matches**. The word "supervisor" appears exactly once as a WP output — **WP-V2B-03**, "Multi-worker supervisor (hybrid isolation, Q4)" — but WP-V2B-03's stated Objective and Outputs are **fault containment among concurrently running workers** ("run two or more strategy workers concurrently... without letting a fault in one reach another"; "a fault-injection drill showing containment," lines 714–722). Nothing in WP-V2B-03's inputs, outputs or acceptance gate mentions the Lifecycle Ledger, `SUSPENDED` state, or an automatic-append obligation.

A further grep of the same file for `SUSPENDED`, `suspension`, `demotion`, `retirement`, `succession` and `§6.9` returns **no matches anywhere in the delivery plan** — not in V2A/V2B, and not in V3, V4 or V5 either. The entire post-live tail state machine ratified in map #54 (brief §6.9: suspend on trigger, asymmetric resume, demote, retire, re-enter, succeed) is **fully specified normatively in the brief but carried by no work package at all.** This is not scoped-out-of-V2A/V2B — it is scoped out of the plan entirely as currently written.

**Verdict for the ticket's explicit check:** the lifecycle-ledger supervisor duties named in the map #54 fold do **not** have a named carrier among the V2A/V2B packages, nor elsewhere in the plan. `WP-V2B-03` is the only plausible candidate by name-proximity and is not a match by scope.

### 3.2 Owned-by-none: the cost-fill feeding duty (map #67 fold, brief §9.7)

Brief §9.7 ("The economic-honesty bar," line 1790) states: *"Costs are measured, never invented: fees from the venue schedule, funding from venue history, slippage calibrated from our own accumulated fills (testnet then live), each versioned as §6.7 cost lineage in a research-side cost-model registry; recalibration is event-driven, never calendar."*

This requires a duty that does not exist elsewhere in the architecture: **someone must take fills produced in the execution domain (WP-V2B-07's testnet fleet, later V4 live fills) and feed them into a research-domain cost-model registry**, crossing the trust-domain boundary the brief is otherwise strict about (§12.1: "Research holds no credentials... one owner-facing entry point is permitted").

A grep of the WP plan for `cost model`, `cost-model`, `fee schedule`, `funding schedule`, `slippage model` and `recalibrat` returns **zero matches**. The nearest-adjacent package, **WP-P0-30 (VEN-E)**, owns venue **market-data** (candle) collection and the live/shadow **price feed** — not fills, and not a cost-model registry. No WP's Objective or Outputs mentions calibrating slippage from accumulated fills, or building/maintaining a cost-model registry of any kind.

**Verdict for the ticket's explicit check:** the cost-fill feeding duty ratified in map #67 does **not** have a named carrier among the V2A/V2B packages, nor elsewhere in the plan (Phase 0 §4, V3 §7, V4/V5 §8 were also checked and none references it).

### 3.3 Coupling: reconciliation is a pervasive dependency with no owned mechanism

Four separate protected-surface packages *depend on* "the next reconcile cycle" or "reconciliation tooling" existing and being correct, without any package's Objective being "build/prove the reconciliation engine":

- **WP-V2A-06** requires the local process-kill/restart harness to show the worker "re-attaches to \[the protective order\] rather than duplicating or orphaning it" (line 633) — this is a reconciliation act, proven only against a deterministic emulator.
- **WP-V2B-10**'s KILL acceptance gate requires "the next reconcile cycle must confirm... zero risk-increasing working orders remain... and every expected reduce-only protective order for existing exposure is still live," raising `PROTECTION_DRIFT` on failure (line 811) — this is safety-critical (it is what stops KILL from silently leaving a position unprotected) and the reconcile mechanism itself is assumed to exist, not built here.
- **WP-V2B-07 Lane A** requires "the daily three-way reconciliation record... with zero unexplained reconciliation breaks" across an 8–16 week window (a live-gate precondition), but lists "the three-way reconciliation tooling" as an **input**, not an output (line 771) — implying it is inherited from the existing (V1) Bridge rather than re-verified for the V2 multi-worker/multi-bucket shape.
- **WP-V2B-05** renders "a reconciliation view with a drift alarm and last-reconcile timestamp" (line 742) — a display, explicitly not the mechanism.

Brief §9.6 test 3 states plainly: *"The Bridge already stores enough to produce \[the execution divergence report\]; it is not surfaced"* (line 1780) — confirming the documents themselves treat reconciliation as pre-existing V1 Bridge capability, carried forward by assumption rather than re-specified or re-proven for V2's new shape (multiple workers, multiple buckets, a new Guardian, a new intent seam).

**Why this is an unsafe coupling, not just a gap:** if the inherited reconciliation mechanism has a defect, or does not extend correctly to concurrent multi-worker state (which WP-V2B-03 introduces) or multi-bucket state (WP-V2B-01), that defect silently corrupts *every one* of the above duties at once — KILL's protection-drift detection could give a false all-clear, the paper-soak's "zero unexplained reconciliation breaks" precondition could pass on a broken diff, and the restart-recovery re-attachment claim could go unverified. No package in V2A or V2B carries an acceptance gate that proves the reconciliation mechanism itself is correct under the new multi-worker/multi-bucket conditions; each downstream package only proves *its own* consumption of reconciliation output.

### 3.4 Ambiguous: who blocks promotion on backtest-vs-forward divergence

Brief §9.7 states the backtest-vs-forward divergence check "blocks further promotion and notifies the owner — never auto-demotes" (line 1790), citing "§6.5 row" (the objective eligibility criteria table, whose falsifiable checks are built by **WP-P0-21**, brief §0.6 R13). The **enforcement** of a promotion block is squarely **WP-V3-03**'s territory (Promotion Authority — "it alone admits to mainnet and `LIMITED_LIVE`," line 846), but WP-V3-03's own listed acceptance gate (line 846) does not mention a standing backtest-vs-forward divergence check as one of its inputs; it lists `leakage_record_id` and `UNSIMULATED_CONTROLS` explicitly but not this divergence metric. This reads as a real duty (declared "standing" and "measured" in the governance fold) whose enforcement point is inferable but not explicitly named at the same level of specificity as its neighbors (e.g., leakage, which *is* named down to the acceptance-gate line in WP-V3-03). Flagged as **ambiguous, leaning unowned-as-a-distinct-package** rather than a confirmed gap, since WP-P0-21 and WP-V3-03 were read only in the WP-plan summary rows, not their full nine-field contracts (WP-P0-21's full contract sits earlier in WP plan §4, outside the sections this ticket scoped to §5/§6).

### 3.5 Not a flag, but worth recording: staged ownership done correctly

Sizing (responsibility #3) and protection placement (#6) are the two places the brief goes out of its way to name **exactly one owner per stage** and explicitly forbid every other component from touching that stage's output (brief §5.5 "ownership words" table, lines 1126–1132: K/OR/RA/P/B each get a "Never does" column). This is the opposite of the failure mode the ticket is hunting for, and is called out here so the matrix isn't read as uniformly bleak — the architecture's most money-adjacent path (sizing) is also its most carefully single-owned path.

---

## 4. Summary counts

| Category | Count | Items |
|---|---|---|
| Clean (single or deliberately staged owner) | 7 of 12 | Loading, admission check, sizing (all 4 stages as one), order construction, authorization, protection placement (as staged), restart recovery |
| Duplicated (two components both claim the full duty) | 0 confirmed | — (the near-miss is event capture's Lifecycle Ledger writers, which is better classified as unowned for 2 of 4 roles, not duplicated) |
| Unowned (no WP or named role) | 3 confirmed, 1 ambiguous | Lifecycle-ledger Registrar + supervisor writers (§3.1); cost-fill-to-cost-model-registry feed (§3.2); general feed-freshness state machine (§12.3, item 10); backtest-vs-forward promotion-block enforcement point (ambiguous, §3.4) |
| Unsafe coupling | 1 confirmed | Reconciliation mechanism — four safety-critical duties (KILL drift detection, paper-soak precondition, restart re-attachment, divergence reporting) all silently depend on an unspecified, unproven, inherited-from-V1 reconciliation engine (§3.3) |

**The worst three, in order:**

1. **Reconciliation as an unsafe coupling (§3.3).** This is the most dangerous finding because it is load-bearing under the live-trading gate itself: WP-V2B-07 Lane A's 8–16-week, ≥30-trade paper soak — one of the fourteen hard preconditions the owner signs against (brief §17.4, WP-V4-01) — rests on "zero unexplained reconciliation breaks" measured by tooling no package proves correct for the V2 shape.
2. **The post-live tail's ledger-writing "supervisor" has no carrier (§3.1).** Map #54 was ratified specifically to give the post-live tail (suspend/resume/demote/retire/re-enter/succeed) a normative design; that design's own enforcement mechanism — the component that appends `SUSPENDED` to the Lifecycle Ledger when a trigger fires — is undefined as a work package anywhere in the plan, V2A/V2B or otherwise.
3. **The cost-model registry feed has no carrier (§3.2).** Map #67 was ratified specifically to make costs "measured, never invented"; the one step that turns a real fill into a measured cost (crossing from the execution domain into the research-side registry) is the one step with no owner, which risks the economic-honesty bar becoming aspirational exactly where map #67 intended it to be mechanical.

---

## 5. Sections read (for reproducibility)

Brief (`MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md`): §5 (887–1182), §6.1–6.3/6.9 (1184–1487), §9.1a/9.2–9.7 (1644–1798), §10 (1800–1936), §11.1–11.5 (1938–2126), §12.1–12.5a (2129–2340), §17.1–17.5 (2629–2714), §18–19 A-section (2717–2759).

WP plan (`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md`): §0 (1–40), §5 V2A (570–688), §6 V2B (691–837), §7 V3 (840–855), §8 V4/V5 (858–874), §9 gates (878–910), plus targeted greps for `LIFECYCLE_LEDGER`, `Registrar`, `cost model`/`cost-model`, `SUSPENDED`/`succession`/`demotion`/`retirement`, `FRESH`/`STALE`/`DEGRADED`, `WP-P0-30`, confirming no additional matches outside the ranges above.
