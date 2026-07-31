# TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN

> **Plan revision 2026-07-30.** Replaces Windows/local paper-candidate scope with Ubuntu KVM2 VPS deployed-DISARMED readiness. Corrects stale TS-P1-009B status. ARM and actual TESTNET paper-order processing are outside this budget and require separate owner gates. This edit/audit authorises no implementation, deploy, TESTNET, ARM, or runtime action.

---

## Executive Summary

The current Trading System roadmap is estimated at **400–600 hours** of implementation and verification work.

The primary reason is not the amount of coding alone. The roadmap currently attempts to deliver, within one continuous programme:

1. Order-management hardening.
2. Risk-management hardening.
3. Reconciliation and restart recovery.
4. Security and supply-chain hardening.
5. Strategy architecture refactoring.
6. A new validation and backtesting architecture.
7. Database and storage architecture improvements.
8. Paper-operation hardening.
9. Operations dashboard development.
10. Live-release governance.
11. Multi-symbol execution.
12. Multi-exchange execution.
13. Linux/Ubuntu VPS qualification.

The objective of this plan is therefore **not to complete the entire roadmap within 50 hours**.

The new objective is:

> Deliver a tightly scoped, safety-focused Trading System MVP: one Ubuntu KVM2 VPS installed and verified safely **DISARMED** (non-trading, state-safe, private/loopback-only, restartable, reconcilable, observable), ready for later separately-approved activation — delivered within approximately 50 active AI engineering hours.

**DISARMED** means: deployed, running, all safety controls active, no orders submitted, no ARM gate passed, no real or simulated capital at risk. The ARM gate and first TESTNET paper-order processing are outside this 50-hour budget and require an explicit separate owner authorisation.

The existing long-term roadmap remains valid and should not be deleted.

Instead, development is split into two layers:

* **Master Roadmap:** the existing Phase 0–7 programme (preserved in full).
* **Active Delivery Plan:** the 50-Hour Safety MVP defined in this document.

### TS-P1-009B Actual Status (verified 2026-07-30)

**TS-P1-009B is NOT complete.** Verified state:

| Stage | Status |
|-------|--------|
| S1 | Accepted at `8d004590` |
| S2 | Terminally BLOCKED after repair round 3 at branch HEAD `678e8b946e34` — two open blockers (sub-1e-12 trade exit_px/pnl tampering can evade detection and permit ACK/DISARM; stale recovery can commit lifecycle close before post-ingestion evidence-epoch rejection) |
| S3 | Unstarted |

S2 closure and minimum S3 completion are mandatory prerequisites inside this 50-hour budget. No claims that TS-P1-009B is complete are valid until a new independent Gate-5 accepting verdict exists for both S2 and S3.

**Baseline:** `origin/master` at `3cccc4c283cd1faa78bab2dbc4ae90fc72733d13`; P0-001..004 and P1-001..008 merged.

**KVM2 Linux package note:** A Linux package exists at old-base commit `6fe0130f45f3c821e230ee30d1e61f548741a6a1` (builder-self-QA only, independently unaccepted, not Ubuntu-staged). It must not be wholesale merged or cherry-picked. Port only necessary semantic paths and revalidate independently.

---

# 1. Primary Objective

The target is a:

# Trading System Safety MVP — Ubuntu KVM2 VPS DISARMED-Ready Candidate

The MVP will support:

* one exchange (Hyperliquid);
* one execution adapter (existing native Hyperliquid SDK path);
* one strategy;
* one symbol;
* one timeframe;
* one operational database (SQLite);
* one Ubuntu KVM2 VPS runtime (private/loopback-only, no public surface);
* testnet/paper-simulated funds only; mainnet and real capital **forbidden**;
* deterministic recovery;
* deterministic reconciliation;
* hardened risk controls;
* hardened order-state handling;
* controlled failure injection;
* independent adversarial audit;
* deployed DISARMED state verifiable by the owner.

The MVP will **not** attempt to become the final general-purpose trading platform.

The in-budget definition of done is:

> One Ubuntu KVM2 VPS is deployed, non-trading (DISARMED), safety controls active, private/loopback-only, state-safe, restartable, reconcilable, observable, and independently verified — ready for a later separately-authorised ARM gate. ARM, first TESTNET paper order, and long soak observation are outside this budget.

---

# 2. Core Principle

The 400-hour plan should not be accelerated mainly by adding more coding agents.

The main reductions must come from:

1. **Scope reduction.**
2. **Architecture freeze.**
3. **Deferring non-critical platform work.**
4. **Bundling related tasks into work packages.**
5. **Reducing repeated audit and documentation overhead.**
6. **Parallelising only work that is genuinely independent.**
7. **Avoiding repeated full-repository rediscovery by every agent.**

The goal is to reduce unnecessary engineering work without weakening the safety-critical execution core.

---

# 3. Lessons from the Adversarial Review

The adversarial review identified an important distinction:

> A feature being present in code does not prove that the operational execution path actually uses it correctly.

A relevant example was the daily-loss and consecutive-loss control path.

The later roadmap was updated to state that the operational daily-loss gate had effectively been inert because the engine path did not provide the necessary realised-PnL and consecutive-loss values.

This leads to a critical rule for the accelerated plan:

> Safety controls must be validated through their real execution paths, not only through isolated unit tests or documentation.

Therefore, the following areas must **not** be removed merely to achieve the 50-hour target:

* duplicate-order protection;
* unknown-submission handling;
* partial-fill protection;
* reconciliation;
* authoritative risk inputs;
* daily-loss / equity / exposure protection;
* kill/disarm behaviour;
* restart recovery;
* database recovery;
* stale-data protection;
* failure injection.

The accelerated plan reduces breadth, not core safety.

---

# 4. Architecture Freeze for the 50-Hour Sprint

During the accelerated sprint, the following decisions are frozen.

| Area                              | V1 Decision                                                      |
| --------------------------------- | ---------------------------------------------------------------- |
| Exchange                          | Hyperliquid                                                      |
| Execution adapter                 | Existing native / official Hyperliquid SDK path                  |
| Environment                       | Testnet / paper-simulated funds (DISARMED until ARM gate)        |
| Real capital / mainnet            | **Forbidden** — hard block in this budget and beyond until separately authorised |
| Strategy count                    | 1                                                                |
| Concurrent strategy portfolio     | Not supported                                                    |
| Symbol count                      | 1                                                                |
| Timeframe count                   | 1                                                                |
| Multi-symbol scheduler            | Deferred Delivery Stage 2                                        |
| Runtime OS                        | **Ubuntu (KVM2 VPS)** — private/loopback-only                   |
| Windows local runtime             | Development/test reference only; production runtime is Ubuntu VPS |
| Operational database              | SQLite                                                           |
| Database migration                | Deferred Delivery Stage 2                                        |
| Dashboard                         | Existing interfaces/logging only                                 |
| New dashboard                     | Deferred Delivery Stage 2                                        |
| Alerting                          | Existing notification mechanisms                                 |
| Backtesting                       | Existing QuantLens stack                                         |
| VectorBT integration              | Deferred Delivery Stage 2                                        |
| hftbacktest integration           | Deferred Delivery Stage 2                                        |
| CCXT execution path               | Deferred Delivery Stage 2                                        |
| Docker qualification              | Deferred Delivery Stage 2                                        |
| Multi-exchange support            | Deferred Delivery Stage 2                                        |
| LLM execution authority           | None                                                             |
| Automatic live promotion          | None                                                             |
| Live capital                      | Blocked (requires full live-release governance gate, separate programme) |
| ARM gate                          | Outside this budget — separate owner authorisation required      |
| TESTNET paper-order processing    | Outside this budget — separate owner authorisation required      |

These decisions should not be reopened during the 50-hour sprint unless a safety-critical blocker proves that one of them is impossible.

No agent should spend time redesigning these choices.

---

# 5. What the 50-Hour MVP Must Prove

At the end of the engineering sprint, the system should demonstrate the following properties.

## 5.1 Order Safety

The system must prove:

* deterministic request identity;
* no blind retry after ambiguous submission;
* duplicate requests cannot create duplicate exposure;
* partial fills are protected or safely flattened;
* order-state transitions are deterministic;
* unknown order state blocks new risk where required;
* kill/disarm operations are idempotent;
* killed/disarmed state survives restart.

---

## 5.2 Reconciliation

The system must prove:

* local and exchange state can be compared deterministically;
* orders are reconciled;
* fills are reconciled;
* positions are reconciled;
* balances/equity are reconciled where required;
* pending actions are represented;
* incomplete snapshots are considered unhealthy;
* stale reconciliation blocks new risk;
* unexpected foreign state is not automatically mutated.

---

## 5.3 Risk

The system must prove that the operational execution path uses valid risk inputs for:

* realised PnL;
* equity;
* daily-loss limits;
* drawdown limits where currently implemented;
* exposure;
* leverage;
* position state;
* liquidation-distance controls where applicable.

Risk evaluation must fail closed when authoritative information is incomplete or stale.

---

## 5.4 Recovery

The system must prove deterministic behaviour for:

* process restart;
* restart during submission;
* restart during unknown submission;
* restart during partial fill;
* reconnect;
* stale WebSocket data;
* REST fallback;
* database backup;
* database restore;
* malformed or corrupted database copies;
* recovery checkpoints.

---

## 5.5 Security and Provenance

The system must provide:

* dependency locking;
* dependency inventory;
* SBOM or equivalent dependency evidence;
* secret scanning;
* outbound-network inventory;
* credential-handling rules;
* release/runtime identity;
* deterministic evidence showing which code/configuration is being tested.

---

# 6. Work Explicitly Deferred from the MVP (Deferred Delivery Stage 2)

**Deferred Delivery Stage 2** is the owner's second delivery stage — work that remains valid on the Master Roadmap but is outside the 50-hour active implementation programme. It is distinct from and broader than the canonical Master Roadmap Phase 2 architecture layer.

**Deferred Delivery Stage 2 summary list:**

* Multi-symbol / multi-exchange / multi-strategy orchestration.
* Portfolio allocation and correlation controls.
* Docker qualification and container deployment.
* VectorBT, hftbacktest, CCXT integration.
* New research/validation architecture.
* Full operations dashboard redesign.
* Enhanced alerting and incident-quality layer.
* Live-capital governance and live-release programme.
* ARM gate and TESTNET paper-order processing.
* Long soak paper-observation evidence.
* AI-lab cohosting on the VPS.
* General infrastructure scaling.
* Any VPS security hardening beyond minimum required for DISARMED readiness.

Do not delete the master roadmap.

## 6.1 Binding Terminology

| Term | Meaning |
|------|---------|
| `WP-L Phase 2 — Ubuntu revalidation` | The post-Gate-A Ubuntu revalidation phase of work package WP-L. |
| `Deferred Delivery Stage 2` | Work deferred beyond this 50-hour plan. |
| `canonical Master Roadmap Phase 2` | The genuine Master Roadmap Phase 2 architecture layer. |

These three terms are binding and never interchangeable. A bare "Phase 2" must not be used anywhere in this document.

---

# 7. Phase 3 — Validation Architecture

## Decision

**Defer the complete Phase 3 implementation.**

Deferred work includes:

* validation-tier redesign;
* VectorBT integration;
* new event-driven validation framework;
* hftbacktest integration;
* broad cost-model redesign;
* unified research/ranking lineage framework.

The existing QuantLens and current validation infrastructure should be used during the MVP.

This decision does **not** mean that strategy validation is unimportant.

It means:

> Building a better validation platform is a separate project from making the execution runtime safe.

---

# 8. Canonical Master Roadmap Phase 2 — Reduce to Minimum Required Infrastructure

The canonical Master Roadmap Phase 2 should not be eliminated completely.

Only the parts needed for Phase 4 safety and recovery should be implemented.

---

## 8.1 TS-P2-001 — Versioned Strategy Contract

### Decision

**DEFER**

Reason:

The MVP contains only one strategy.

A generic strategy factory, broad strategy versioning architecture, and multi-strategy abstraction are not required to prove execution safety for the current runtime.

The existing strategy integration should remain unchanged unless a safety or recovery requirement makes a small modification unavoidable.

---

## 8.2 TS-P2-002 — Market-Data Quality Contract

### Decision

**IMPLEMENT LITE VERSION**

Only implement or verify what is necessary for safe execution:

* stale-data state;
* timestamp/gap detection;
* reconnect state;
* restoration state;
* REST fallback;
* health status.

Do not add:

* L2 collectors;
* broad trades collectors;
* liquidation collectors;
* funding infrastructure unrelated to current strategy requirements;
* general historical-data redesign.

---

## 8.3 TS-P2-003 — Exchange Adapter Qualification

### Decision

**DEFER GENERAL QUALIFICATION**

Do not add a second CCXT execution path.

Continue using the existing Hyperliquid native/official SDK implementation.

However, the existing adapter must still be tested for:

* timeouts;
* ambiguous responses;
* rate-limit errors;
* reconnect conditions;
* unsupported behaviour;
* submission uncertainty;
* failure classification.

This verification belongs inside the failure and recovery packages rather than a new adapter architecture project.

---

## 8.4 TS-P2-004 — Durable Portfolio State

### Decision

**DEFER FULL PORTFOLIO ARCHITECTURE**

Do not build a generic multi-strategy portfolio engine.

Implement only the durable state required for:

* current position;
* account balance/equity where required;
* exposure;
* PnL state;
* risk checkpoints;
* reconciliation checkpoints;
* restart recovery.

---

## 8.5 TS-P2-005 — Event and Failure-State Definitions

### Decision

**DEFER GENERAL EVENT REDESIGN**

Do not build a broad domain-event platform.

Existing event structures should remain in place unless the failure/recovery suite requires a narrowly scoped safety event.

Any additions must be minimal.

---

## 8.6 TS-P2-006 — Storage Benchmark and Migration Design

### Decision

**REPLACE WITH LITE RECOVERY TASK**

The database decision is frozen:

> SQLite remains the operational database for the MVP.

Do not benchmark alternative databases.

Do not migrate.

Instead prove:

* backup;
* restore;
* corruption detection;
* schema compatibility;
* recovery behaviour;
* failure-safe startup.

---

## 8.7 TS-P2-007 — Mode and Configuration Isolation

### Decision

**IMPLEMENT LITE VERSION**

The MVP only needs to prove that:

* wrong environment fails closed;
* state/configuration cannot silently cross environments;
* testnet identity is explicit;
* production/live mode cannot be accidentally entered;
* credential source is unambiguous without exposing secrets.

No new live environment should be created.

---

# 9. Phase 4 — Scope Clarification

**Full TS-P4-001..004 are NOT delivered** in the 50-hour MVP. Full failure-injection and deterministic incident injection suites remain Deferred Delivery Stage 2.

What is in-budget is the minimal set of named DISARMED restart, reconnect, and state checks documented in WP-A (§19) and evidence-mapped against existing P1-001..008 code paths. Each required invariant is classified under the three-class §19 model: COVERED requires no new work; SMALL-GAP may use contingency only after explicit Lead sign-off; FULL-TASK routes to Deferred Delivery Stage 2 or BLOCK. None becomes a new in-budget Phase 4 task.

For reference, the full Phase 4 tasks and their status:

* TS-P4-001 Restart Recovery Drill — full version: **Deferred Delivery Stage 2**.
* TS-P4-002 Reconnect / Gap / REST Fallback Drill — full version: **Deferred Delivery Stage 2**.
* TS-P4-003 Backup / Restore / Corruption Drill — full version: **Deferred Delivery Stage 2**.
* TS-P4-004 Deterministic Incident Injection Suite — full version: **Deferred Delivery Stage 2**.

The safety properties these tasks validate (§5.1–5.5) remain required. They are addressed through WP-A invariant mapping against existing evidence, contingency-funded SMALL-GAP repairs (Lead sign-off required), and WP-R independent audit — not through new full Phase 4 task implementations within this budget.

---

# 10. TS-P4-005 — Paper Monitoring Evidence

## Decision

**Keep on the Master Roadmap, but outside the 50-hour active engineering budget.**

Paper monitoring is elapsed operational time, not active AI engineering effort. It also requires the ARM gate, which is a separate owner authorisation outside this budget.

The plan tracks two independent measurements that must not be conflated:

### Engineering effort (this budget)

```text
≤50 active hours → Ubuntu KVM2 VPS deployed DISARMED, verified
```

### ARM + Paper observation (separate budget, separate owner gates)

```text
Explicit owner ARM authorisation
  ↓
First TESTNET paper order
  ↓
7–10+ days monitored paper operation
  ↓
Paper evidence conclusion
```

The monitoring period may last many days. That elapsed time is not AI engineering hours and is not counted against the 50-hour ceiling.

---

# 11. Phase 5 — Operations Dashboard

## TS-P5-001 — Operations Read Model

### Decision

**DEFER FULL VERSION**

Only add a minimal status payload if current interfaces cannot expose essential safety information.

Minimum useful fields may include:

* mode;
* commit;
* runtime identity;
* reconciliation health;
* reconciliation age;
* market-data freshness;
* risk state;
* kill/disarm state.

Do not redesign the operations architecture.

---

## TS-P5-002 — MTC Read-Only Operations Page

### Decision

**DEFER**

The existing dashboard or logs are sufficient for the MVP.

A redesigned UI does not make the execution engine safer.

---

## TS-P5-003 — Alert and Incident Quality Layer

### Decision

**DEFER GENERAL REDESIGN**

Continue using existing Telegram/logging infrastructure.

A narrow fix is permitted only if critical events can currently occur silently.

---

# 12. Phase 6 — Live Release

## Decision

**Completely outside the 50-hour sprint.**

The in-budget MVP stops at:

> Ubuntu KVM2 VPS DISARMED-Ready Candidate (verified, non-trading, no ARM passed).

Paper eligibility, live release, and limited-live-ready are subsequent gates requiring separate owner authorisation, outside this budget.

No live-capital or mainnet implementation is included in this sprint.

---

# 13. Phase 7 — Controlled Expansion

## Decision

**Completely deferred to Deferred Delivery Stage 2.**

Do not implement:

* multi-symbol scheduling;
* portfolio allocation;
* correlation-based risk allocation;
* multi-exchange support;
* Docker deployment;
* AI-lab cohosting;
* infrastructure scaling (beyond single KVM2 VPS).

Note: essential Linux/Ubuntu VPS qualification for the single DISARMED runtime is **in-budget** (WP-L + WP-V). General Linux migration of non-essential components, Docker, and horizontal scaling remain Deferred Delivery Stage 2.

These expansion features are meaningful only after the single-runtime safety core has produced strong paper evidence.

---

# 14. New Work-Package Execution Model

The existing task-by-task process should be replaced for this sprint by:

> One safety-coherent work package per implementation cycle.

A work package may contain several tightly related roadmap tasks.

The purpose is to reduce repeated:

* repository inspection;
* planning;
* agent onboarding;
* documentation updates;
* test runs;
* audit passes;
* memory updates;
* status reports.

Safety evidence remains required.

The administrative unit changes from **task** to **work package**.

---

# 15. WP-0 — Scope and Baseline Review

## Scope

* Owner accepts this revised plan.
* New Gate-1 follow-up: exhausted S2 loop authorisation.
* Immutable integration/release plan agreed.
* Exact Linux semantic-port manifest agreed.
* Baseline commit `3cccc4c2` confirmed; exact allowed/forbidden path allowlist frozen.
* DISARMED VPS invariant map produced: each required invariant (§5.1–5.5) mapped to existing code/test evidence from P1-001..008; gaps classified (COVERED / SMALL-GAP / FULL-TASK per §19).

## Budget

**2 hours**

## Output

Owner-signed revised plan + Gate-1 authorisation for S2 new loop + semantic-port manifest + DISARMED VPS invariant map with gap classification.

---

# 16. WP-S — TS-P1-009B S2 Closure + Minimum S3

## Scope

Close the two S2 terminal blockers:

1. Sub-1e-12 `trades.exit_px`/`pnl` tampering can evade detection and permit ACK/DISARM.
2. Stale recovery can commit lifecycle close before post-ingestion evidence-epoch rejection.

Then implement and independently audit minimum S3 (initial liveness/lifecycle proof).

## Budget

**12 hours**

S2 blocker repair (implementer): 4 h
S2 independent Gate-5 audit: 2 h
S3 minimum implementation: 4 h
S3 independent Gate-5 audit: 2 h

The two 2 h audit allocations fund only the first pass of Audit 1: the S2 accepting verdict and the S3 accepting verdict. Every re-audit at checkpoint 1, plus Audit 2, Audit 3, and Gate-6, is funded from WP-R (§20); no audit activity is funded from two sources.

## Hard Stop

This is a new owner-authorised repair/re-audit cycle for S2; prior exhausted rounds are closed. In this new cycle, maximum three non-accepting rounds are permitted. If the third round of the new cycle yields a non-accepting verdict, stop and report to owner. Do not enter a fourth round of the new cycle. Do not proceed to WP-L.

## Evidence Required

* Gate-5 (Codex `gpt-5.6-sol`, effort `xhigh`) accepting verdict for S2 closure.
* Gate-5 accepting verdict for minimum S3.
* Both verdicts in independent sessions (never `--resume` implementer session).

---

# 17. WP-L — Essential Linux Semantic Port

## Scope

Port only the semantic paths necessary for Ubuntu KVM2 operation from the old-base package at `6fe0130f`. No wholesale merge or cherry-pick. WP-L is split into two phases by the Gate-A boundary.

Minimum paths to evaluate for porting:

* systemd service unit (startup, restart, graceful shutdown);
* signal-handler integration (SIGTERM → DISARMED shutdown path);
* path and file-permission assumptions (Linux filesystem layout);
* environment isolation differences (env vars, config loading);
* dependency installation on Ubuntu (pip lockfile, apt packages).

### WP-L Phase 1 — pre-Gate-A (non-executed / local checks only)

Before Gate-A owner approval, WP-L may prepare, select, port, and package the Linux semantic paths using **non-executed / local checks only** (static review, local build, manifest authoring). **No Ubuntu execution is permitted in WP-L Phase 1.** No executed-Ubuntu evidence may precede Gate A.

### WP-L Phase 2 — Ubuntu revalidation (post-Gate-A; during the one named expendable Ubuntu staging action, before WP-A)

**All Ubuntu execution / revalidation in WP-L** — including the budgeted 2 h independent revalidation and any evidence that the ported paths actually function on Ubuntu — occurs **only after Gate-A owner approval**, on the single Gate-A-authorised expendable Ubuntu staging host that is retained through WP-I staging verification and WP-A, and **before WP-A begins**. Each ported path is independently revalidated on Ubuntu here, and only here.

## Budget

**8 hours**

WP-L Phase 1 — pre-Gate-A (non-executed):
Port assessment and selection: 2 h
Implementation (Linux path corrections; local/static checks only): 3 h
Lightweight invariant review: 1 h

WP-L Phase 2 — Ubuntu revalidation (post-Gate-A; during the one named expendable Ubuntu staging action):
Independent revalidation on Ubuntu: 2 h

## Non-Goals

Do not port Docker packaging, orchestration scripts, multi-adapter configs, or any experimental feature from old-base. Port only what is needed to run DISARMED on Ubuntu.

## Evidence Required

WP-L Phase 1 — pre-Gate-A (non-executed artifacts only):
* Semantic-port manifest (each candidate ported path listed, rationale, static/local verification result — no Ubuntu execution).
* Lightweight invariant review pass (single-writer protected-core ownership preserved).

WP-L Phase 2 — Ubuntu revalidation (post-Gate-A; during the staging action, before WP-A):
* All ported paths verified functional on Ubuntu KVM2 staging environment — revalidation evidence produced only here, after Gate A.

---

# 18. WP-I — Reproducible Deps, systemd, State, Rollback, Ubuntu Staging

## Scope

* Reproducible dependency lockfile (pip freeze + hash pinning for Ubuntu).
* systemd service file: DISARMED-only mode, restart-on-failure (non-trading states only), watchdog.
* State continuity: SQLite backup/restore verified on Ubuntu.
* Rollback procedure: documented and tested (previous known-good state restore).
* Expendable Ubuntu staging: one fresh Gate-A-authorised staging deploy, smoke-tested and retained through WP-L Phase 2 — Ubuntu revalidation, WP-I staging verification, and WP-A Ubuntu invariant verification; discard occurs only after WP-A completes and all required staging evidence has been captured. Nothing persists to the production VPS until the owner authorises.
* Minimum security baseline (within the 6 h): minimum pinned-dependency/SBOM-equivalent inventory; repository and artifact secret scan; outbound-network inventory. Broad security platform hardening is deferred.

## Staging Host Lifecycle

1. Local/static port implementation may occur before Gate A.
2. No Ubuntu execution of any kind may occur before Gate A.
3. The single Gate-A-authorised expendable Ubuntu staging host must remain available through, in order: WP-L Phase 2 — Ubuntu revalidation, WP-I staging verification, and WP-A Ubuntu invariant verification.
4. The staging host is discarded only after WP-A completes and all required staging evidence has been captured.

## Budget

**6 hours**

## Non-Goals

* No public network surface.
* No advanced VPS security hardening beyond minimum DISARMED readiness (firewall loopback-only, no SSH key sprawl) — rest is Deferred Delivery Stage 2.
* No AI-lab cohosting.
* No monitoring infrastructure beyond existing logs/alerts.

## Evidence Required

* Pinned lockfile committed and verified installable on Ubuntu.
* systemd unit verified: starts DISARMED, survives reboot DISARMED, SIGTERM → clean shutdown.
* SQLite backup/restore verified on Ubuntu staging.
* Rollback procedure tested on staging.

---

# 19. WP-A — DISARMED VPS Invariant Evidence Overlay

## Scope

WP-A is a bounded **evidence-mapping and verification overlay** — not a new feature implementation work package.

Its purpose is to map each DISARMED VPS safety invariant (§5.1–5.5) to existing code/test evidence already present in merged P1-001..008, the newly closed S2/S3 (WP-S), and the Linux/staging work (WP-L + WP-I).

**WP-0 must produce the invariant map before WP-A work begins.** For each required invariant, the map records the invariant, existing evidence (code path + test), and a gap class:

| Gap Class | Meaning | Disposition |
|-----------|---------|-------------|
| COVERED | Existing code + test prove the invariant on Ubuntu | No new work |
| SMALL-GAP | Narrow missing test or trivial wiring fix, verifiable in isolation | Contingency hours only, after explicit Lead sign-off per gap |
| FULL-TASK | Requires a new P1-010..012, canonical Master Roadmap Phase 2 (P2), or Phase 4 (P4) full task | Deferred Delivery Stage 2, or BLOCK if indispensable to safe DISARMED deployment |

**No new P1-010..012, canonical Master Roadmap Phase 2 (P2), or Phase 4 (P4) full-task implementation is scheduled inside WP-A.** Any such requirement discovered here moves to Deferred Delivery Stage 2 or causes BLOCK. WP-R is audit-only: Audit 3 within WP-R independently re-derives and accepts the invariant map from the frozen artifact and captured WP-A staging evidence package, without Ubuntu re-execution or a live staging host; WP-R reserve hours are never used as WP-A implementation time. SMALL-GAP repair uses contingency hours only, after explicit Lead sign-off per gap. FULL-TASK → Deferred Delivery Stage 2 or BLOCK.

## Budget

**3 hours**

WP-A's 3 h Ubuntu invariant verification runs on the retained Gate-A-authorised staging host. It covers: invariant-map finalization (refining gap classifications produced by WP-0); existing Ubuntu-test execution (running already-existing tests against each COVERED/SMALL-GAP invariant on Ubuntu); and evidence capture/classification (recording pass/fail results per invariant, classifying residual gaps). SMALL-GAP repair work is not funded here — it uses contingency hours after explicit Lead sign-off. WP-R is audit-only and its hours are never used as WP-A implementation time. The staging host remains available until WP-A completes and all required staging evidence has been captured.

## Verification Pass

After the invariant map is produced and any SMALL-GAP items are closed (contingency hours, Lead-approved), run a verification pass on Ubuntu confirming all COVERED and SMALL-GAP invariants pass across §5.1–5.5.

## DISARMED Deployment Check — Minimum Restart Invariants

These checks must be confirmed COVERED by existing evidence. Any item not already covered is a FULL-TASK gap (Deferred Delivery Stage 2 or BLOCK), not a new in-budget task.

This is a deliberate tightening of the general COVERED / SMALL-GAP / FULL-TASK model for these four minimum restart invariants: SMALL-GAP treatment is not available for them.

```text
restart while flat and DISARMED: system starts DISARMED, no order submitted
restart with killed/disarmed state persistent after restart
database state-file integrity after restart
SIGTERM: clean DISARMED shutdown (no dangling state)
```

## DISARMED Deployment Check — Minimum Reconnect/Stale-Data Invariants

```text
WebSocket disconnect while DISARMED: no order submitted
stale feed/timestamp gap while DISARMED: no order submitted
reconciliation after reconnect: clean output (no positions in DISARMED)
```

## Safety Rule

Never intentionally corrupt the active runtime database. All destructive tests use temporary copies, fixtures, or isolated test databases.

## Explicit Non-Goals

* No new P1-010..012, canonical Master Roadmap Phase 2 (P2), or Phase 4 (P4) full-task implementation here.
* No new portfolio platform, database, or event architecture.
* No multi-strategy infrastructure or second execution adapter.
* WP-R audit reserve hours are never used as WP-A implementation time.

---

# 20. WP-R — Independent Audit Reserve

## Budget

**6 hours**

Reserved for independent Gate-5 (Codex `gpt-5.6-sol` effort `xhigh`) and Gate-6 (Codex `gpt-5.6-sol` effort `xhigh`) review and re-audit. **WP-R is strictly audit-only.** WP-R's 6 h audit reserve funds Audit 2, Audit 3, Gate-6, and all re-audit rounds at all three checkpoints, including re-audits at checkpoint 1. The first pass of Audit 1 is funded from WP-S's internal 2 h + 2 h allocation per §16; no audit activity is funded twice. WP-R funds no implementation, no remediation, and no fix work — there is no `bounded remediation` or any other implementation/repair funding inside WP-R. If the WP-R audit reserve is exhausted while a further required audit or re-audit remains, the outcome is BLOCK: WP-R overrun is not contingency-funded, and no other work package may fund it. If the exact model or effort level is unavailable, stop as BLOCK unless the owner explicitly waives it.

## Required-Repair Routing

Any required repair identified by a Gate-5/Gate-6 audit returns to the **Claude CLI implementer**. It is funded only from the 5 h contingency (per §22), after explicit Codex Lead sign-off, and never from WP-R hours. If the contingency is exhausted and the repair is required for safety, BLOCK — do not cut the safety requirement and do not borrow WP-R audit hours. The contingency funds repairs and WP-S/WP-L/WP-I/WP-V overruns only; it never funds an audit or re-audit.

Before staging-host discard, and after discard only for Case 1 below, a contingency-funded repair that changes code or artifacts requires a new exact release SHA/artifact and re-run of the affected audit — Gate-5 Audit 1, Audit 2, or Audit 3, and Gate-6 where applicable — on that exact new frozen SHA/artifact. Acceptance of a previous SHA/artifact never carries forward. The re-audit consumes WP-R, not contingency. Maximum three non-accepting repair/re-audit rounds per audit checkpoint; after the third non-accepting verdict, stop and report to the owner — do not enter a fourth round.

After the expendable staging host has been discarded, required repairs split into two cases:

* **Case 1 — executed-Ubuntu evidence remains valid:** for documentation, artifact metadata, or a change provably outside the runtime paths covered by the WP-A invariant map, the implementer must state which invariants the change cannot affect and the Lead must confirm that assessment. Apply the normal loop: repair from contingency → freeze a new exact SHA/artifact → re-run the affected audit on that exact artifact from WP-R. This is an artifact- and evidence-level loop; no host is needed.
* **Case 2 — executed-Ubuntu evidence would be invalidated:** BLOCK and report to the owner with the concrete remediation path. The single Gate-A staging authorisation is spent, Gate B authorises no staging action, and no hours in this 50-hour budget fund a second staging action. Restoring valid evidence requires a new explicit owner staging authorisation (a new Gate-A-class approval) whose hours are outside this budget. Do not proceed to Gate B or WP-V on stale or partially invalidated evidence, and do not fabricate or extrapolate evidence.

## Three Primary Audit Checkpoints

**Audit 1:** After WP-S (S2/S3 closure).
**Audit 2:** After WP-L Phase 2 — Ubuntu revalidation + WP-I staging verification (Linux port + staging), before WP-A.
**Audit 3:** After the exact final release SHA/artifact is frozen (containing accepted WP-S / WP-L / WP-I / WP-A plus any contingency repairs) and the WP-A invariant-map verification pass completes; the auditor independently re-derives and accepts the WP-A DISARMED VPS invariant map from that frozen artifact and the captured WP-A staging evidence package — every COVERED/SMALL-GAP invariant required for DISARMED VPS readiness confirmed with passing Ubuntu evidence. Audit 3 and Gate-6 are artifact- and evidence-level reviews requiring no Ubuntu execution and no live staging host; “independently reproduces the invariant map” never means re-executing the Ubuntu tests.

Each auditor receives: scope contract, architecture decisions, actual diff, test evidence, rollback procedure, known risks. Never fed implementer session context.

## Auditor Mission

Search primarily for:

* safety defects; incorrect state transitions; missing execution-path wiring;
* false-positive tests; unsafe retry behaviour; restart defects;
* reconciliation gaps; stale-state acceptance; duplicate-exposure paths;
* secret exposure; missing rollback paths; undocumented scope expansion;
* Linux-specific path or permission assumptions not caught in staging.

---

# 21. WP-V — VPS DISARMED Deployment and Verification

## Budget

**8 hours**

Owner must explicitly authorise the deployment action before WP-V begins. This reservation does not itself authorise deployment.

## Scope

* One Ubuntu KVM2 VPS: install runtime, dependencies (locked lockfile), systemd service.
* Private/loopback-only network surface confirmed.
* Start in DISARMED state; confirm no orders submitted, no ARM gate passed.
* State safety verified: SQLite state-file integrity, backup/restore tested on production VPS.
* Restartable: VPS reboot → service restarts → DISARMED (verified).
* Reconcilable: reconciliation run produces clean output against TESTNET state (no positions).
* Observable: logs/alerts reachable, existing UI shows DISARMED status.
* Rollback documented and tested on the live VPS.

## Immutable Release Baseline

WP-V deploys the exact final immutable commit accepted after WP-S, WP-L, WP-I, WP-A, and any contingency repairs. Before deployment, the release record must capture: commit ancestry, exact path manifest, artifact hash, test evidence, Gate-5/6 verdicts. Any code or artifact change after audit acceptance invalidates that acceptance and requires the applicable §20/§22 Case 1 re-freeze/re-audit loop; if the change would invalidate executed-Ubuntu evidence, §20/§22 Case 2 applies and deployment is BLOCKED pending new owner staging authorisation outside this budget.

## In-Budget Definition of Done

> One Ubuntu KVM2 VPS is deployed, non-trading (DISARMED), safety controls active, private/loopback-only, state-safe, restartable, reconcilable, observable, and independently verified by the owner — ready for a later separately-authorised ARM gate.

## ARM and TESTNET Are Outside

ARM gate, first TESTNET paper order, and long soak observation are separate owner-authorised actions not included in this budget.

---

# 22. Contingency

**5 hours** reserved. Scope, in priority order:

1. **Lead-approved required repairs returned to the Claude CLI implementer** — this explicitly includes **SMALL-GAP repairs from WP-A** (per §19 gap table) **and any required repair identified by WP-R Gate-5/Gate-6 audits** (per §20). These are funded first and exclusively from this contingency, after explicit Codex Lead sign-off per item. No other funding source exists for them (WP-R funds no repair work itself).
2. **Overruns on WP-S, WP-L, WP-I, or WP-V** (e.g. S2 repair complexity, Linux port surprises, staging issues, VPS provisioning) — funded only from whatever contingency remains after the required-repair uses above.

WP-0 and WP-A overruns, distinct from the explicitly eligible WP-A SMALL-GAP repairs in item 1, have no funding source and route to BLOCK + owner report under the hard-ceiling rule.

Contingency never funds Gate-5/Gate-6 audit or re-audit activity. A contingency-funded WP-S overrun may cover implementation and self-QA overrun only; it never covers WP-S's internal Audit-1 allocation or any re-audit.

Audit 3 and Gate-6 use the exact frozen SHA/artifact plus the captured WP-A staging evidence package. Both are artifact- and evidence-level reviews requiring no Ubuntu execution and no live staging host; independent reproduction means re-deriving the invariant map from those frozen inputs, not re-executing Ubuntu tests.

Before staging-host discard, and after discard only for Case 1 below, a contingency-funded repair that changes code or artifacts requires a **new exact release SHA/artifact** and the affected audit (Gate-5 Audit 1 / Audit 2 / Audit 3, and Gate-6 where applicable) must be **re-run on that exact new frozen SHA/artifact**. Acceptance of a previous SHA/artifact never carries forward. Re-audits are funded only from WP-R's 6 h audit reserve; if that reserve is exhausted while a required audit or re-audit remains, BLOCK. Maximum three non-accepting repair/re-audit rounds per audit checkpoint; after the third non-accepting verdict, stop and report to the owner — do not enter a fourth round.

For a repair after the staging host is discarded, apply §20's two-case rule. **Case 1:** if the implementer states, and the Lead confirms, that the change cannot affect specified WP-A invariants or any executed-Ubuntu evidence, the normal repair → new exact SHA/artifact → affected artifact-and-evidence-level re-audit loop applies and requires no host. **Case 2:** if the change would invalidate executed-Ubuntu evidence, BLOCK and report the concrete remediation path to the owner; the spent Gate-A authorisation cannot be reused, Gate B authorises no staging, and no hours in this 50-hour budget fund a second staging action. A new explicit owner Gate-A-class staging authorisation and its hours are outside this budget. Do not proceed to Gate B or WP-V on stale or partially invalidated evidence, and do not fabricate or extrapolate evidence.

**Hard ceiling rule:** The contingency is a hard 5 h ceiling. It does not auto-extend. If it is exhausted (whether by required repair or by overrun) and a further safety requirement remains unfunded:

* stop and BLOCK;
* never cut the safety requirement;
* never fabricate evidence;
* never borrow time from Deferred Delivery Stage 2 scope to compensate;
* never use WP-R audit hours as implementation/repair funding (per §20).

Report the blocker to the owner with a concrete remediation path.

---

# 23. Total Engineering Budget

| Work Package                                        |   Budget |
| --------------------------------------------------- | -------: |
| WP-0 — Scope / Baseline Review                      |      2 h |
| WP-S — TS-P1-009B S2 Closure + Minimum S3          |     12 h |
| WP-L — Essential Linux Semantic Port                |      8 h |
| WP-I — Deps / systemd / State / Rollback / Staging |      6 h |
| WP-A — DISARMED VPS Invariant Evidence Overlay      |      3 h |
| WP-R — Independent Audit Reserve (audit-only)       |      6 h |
| WP-V — VPS DISARMED Deployment + Verification       |      8 h |
| Contingency                                         |      5 h |
| **TOTAL**                                           | **50 h** |

> Arithmetic check: 2 + 12 + 8 + 6 + 3 + 6 + 8 + 5 = **50**. Hard ceiling.

> This is a hard ceiling, not a guarantee. Safety gate overrun → stop/BLOCK. Never cut safety, fabricate evidence, or borrow from Deferred Delivery Stage 2.

The 50 hours covers **active AI engineering, staging, independent audit, and — only after separate owner approval — one DISARMED VPS deployment and verification (WP-V)**. The owner's approval decision and any wait time are an external gate and are not counted as engineering hours. WP-V execution is inside the 50h ceiling. Elapsed paper observation time, long soak, and ARM are outside this budget.

---

# 23a. Gated Exit Evidence — Three Sequential Gates

The following gates must be cleared in the exact order below. Each approval authorises only the named action — nothing else, and no approval carries forward to authorise the next.

**Exact sequence:**

1. **Audit 1 (Gate-5), immediately after WP-S** — freeze the exact checkpoint SHA/artifact and obtain an accepting S2/S3-closure verdict before proceeding.
2. **Gate-A approval** (PRE-STAGING) — see the Gate A checklist. Requires only non-executed readiness; **no executed-Ubuntu evidence** before this point (WP-L Phase 1 is non-executed; its Ubuntu revalidation is deferred to step 3).
3. **One named expendable Ubuntu staging action** (authorised only by Gate A): perform the initial WP-I staging deploy + smoke test, retain that host for WP-L Phase 2 — Ubuntu revalidation of all ported paths (2 h), then complete WP-I staging verification. The same host is retained for WP-A; it is not discarded at this step.
4. **Audit 2 (Gate-5), immediately after WP-L Phase 2 — Ubuntu revalidation + WP-I staging verification** — freeze the exact checkpoint SHA/artifact and obtain an accepting Linux-port/staging verdict before WP-A.
5. **WP-A 3 h Ubuntu invariant verification** on the retained Gate-A-authorised staging host, including capture of all required staging evidence.
6. **Discard the expendable staging host** only after WP-A completes and all required staging evidence has been captured.
7. **Freeze the exact final release SHA/artifact** containing accepted WP-S / WP-L / WP-I / WP-A plus any contingency repairs.
8. **Audit 3 (Gate-5) + Gate-6** performed as artifact- and evidence-level reviews on that exact frozen SHA/artifact plus the captured staging evidence package; they require no Ubuntu execution and no live staging host. Audit 3 independently re-derives and accepts the invariant map from those frozen inputs rather than re-executing Ubuntu tests.
9. **Gate-B approval** (PRE-PRODUCTION-DEPLOY) — requires staging/systemd/SQLite/rollback/WP-A/security/final-SHA/audit evidence and requests the separate WP-V deployment approval.
10. **WP-V** production deployment (after the separate WP-V deployment approval).
11. **Gate-C** POST-DEPLOY acceptance.

At Audit 1, Audit 2, and Audit 3/Gate-6, before staging-host discard and after discard only for Case 1 below, a contingency-funded repair that changes code or artifacts triggers this explicit loop: **repair (contingency) → freeze a new exact release SHA/artifact → re-run the affected audit on that exact new frozen SHA/artifact (WP-R)**. Acceptance of a previous SHA/artifact never carries forward. Maximum three non-accepting repair/re-audit rounds per audit checkpoint; after the third non-accepting verdict, stop and report to the owner — do not enter a fourth round. If WP-R's audit reserve is exhausted while a required audit or re-audit remains, BLOCK.

After step 6 discards the staging host, that loop has two cases. **Case 1:** a documentation, artifact-metadata, or other change provably outside the WP-A runtime paths may proceed only after the implementer states and the Lead confirms which invariants it cannot affect; freeze the new exact artifact and perform the affected artifact-and-evidence-level re-audit from WP-R, with no host required. **Case 2:** a change that would invalidate any executed-Ubuntu evidence is BLOCK. Report the concrete remediation path to the owner: a new Gate-A-class staging authorisation is required and its hours are outside this 50-hour budget. Gate B authorises no staging action. Do not proceed to Gate B or WP-V on stale or partially invalidated evidence, and do not fabricate or extrapolate evidence.

---

## Gate A — PRE-STAGING Readiness

All items below must be satisfied before owner staging approval is requested. Gate A requires only artifacts and readiness evidence that do not execute on Ubuntu — no Ubuntu install results, no systemd start/reboot evidence, no SQLite backup/restore evidence, no WP-A Ubuntu-test execution, and no completed staging.

- [ ] Two S2 blockers closed (Gate-5 accepting verdict, independent Codex session).
- [ ] Minimum S3 complete (Gate-5 accepting verdict, independent Codex session).
- [ ] Exact candidate release SHA and artifact path manifest produced and recorded.
- [ ] Essential Linux semantic-port (WP-L Phase 1) complete — non-executed only: all paths from `6fe0130f` identified, ported, and statically verified; semantic-port manifest with rationale produced as artifact. WP-L Ubuntu revalidation is NOT yet performed (deferred to the Gate-A-authorised staging action); no executed-Ubuntu evidence precedes Gate A.
- [ ] Pinned dependency lockfile committed (pip freeze + hash pinning for Ubuntu; Ubuntu install not yet executed).
- [ ] SBOM-equivalent dependency inventory produced (local; no Ubuntu execution required).
- [ ] Local repository and artifact secret scan completed (clean result; no Ubuntu execution required).
- [ ] Outbound-network inventory produced.
- [ ] Staging test plan documented.
- [ ] Rollback plan documented (procedure written; Ubuntu staging execution not yet performed).
- [ ] Named expendable Ubuntu 24.04 host identified (not yet deployed).
- [ ] systemd service unit designed masked/inactive (unit file written and reviewed; not yet deployed, enabled, or started on Ubuntu).
- [ ] No secrets present in candidate artifact or lockfile.

**Owner approval — Gate A:** Authorises one named expendable Ubuntu 24.04 staging action only. Staging approval authorises nothing else.

---

## Gate B — PRE-PRODUCTION-DEPLOY Readiness

All items below must be satisfied, in this order, before owner production-deploy approval is requested. Executed-Ubuntu staging/systemd/SQLite/rollback/WP-A evidence (from the Gate-A-authorised staging action) is a prerequisite.

- [ ] Audit 1 Gate-5 accepting verdict: S2/S3 closure (Codex `gpt-5.6-sol` xhigh, independent session).
- [ ] Expendable Ubuntu staging deploy completed and smoke-tested as the Gate-A-authorised action; the host is retained through WP-L Phase 2 — Ubuntu revalidation, WP-I staging verification, and WP-A.
- [ ] WP-L Phase 2 — Ubuntu revalidation evidence confirms every ported path functions on the retained staging host.
- [ ] systemd start / reboot / SIGTERM verified on the expendable staging host.
- [ ] SQLite backup/restore verified on the expendable staging host.
- [ ] Rollback procedure tested on the expendable staging host.
- [ ] Audit 2 Gate-5 accepting verdict: Linux port + staging (Codex `gpt-5.6-sol` xhigh, independent session).
- [ ] Every COVERED/SMALL-GAP invariant required for DISARMED VPS readiness has passing Ubuntu evidence from WP-A on the retained staging host (per WP-A invariant map).
- [ ] Expendable staging host discard recorded only after WP-A completed and all required staging evidence was captured.
- [ ] Exact final release SHA/artifact frozen: containing accepted WP-S / WP-L / WP-I / WP-A plus any contingency repairs; commit ancestry, exact path manifest, and artifact hash recorded.
- [ ] Audit 3 Gate-5 accepting verdict performed on the exact frozen SHA/artifact plus the captured staging evidence package: Codex independently re-derives and accepts the WP-A DISARMED VPS invariant map without Ubuntu re-execution or a live staging host (Codex `gpt-5.6-sol` xhigh, independent session).
- [ ] Gate-6 security review accepting verdict on the exact frozen SHA/artifact plus the captured staging evidence package; this is an artifact- and evidence-level review requiring no Ubuntu execution or live staging host (Codex `gpt-5.6-sol` xhigh, independent session).
- [ ] No post-audit code or artifact change has invalidated any executed-Ubuntu evidence captured before the staging host was discarded. If any change has, Gate B is BLOCKED pending a new explicit owner Gate-A-class staging authorisation whose hours are outside this 50-hour budget; do not proceed on stale or partially invalidated evidence.

**Owner approval — Gate B:** Confirms PRE-PRODUCTION-DEPLOY readiness and requests the separate WP-V deployment approval. It does not itself deploy or authorise staging. Staging approval (Gate A) authorises nothing else and does not carry forward to authorise Gate B. A post-audit change that leaves executed-Ubuntu evidence valid follows the §20/§22 Case 1 re-freeze/re-audit loop; a change that invalidates it follows Case 2 and BLOCKS Gate B pending new owner staging authorisation outside this budget.

---

## Gate C — POST-DEPLOY Acceptance

All items below must be confirmed after WP-V completes.

- [ ] Deployed VPS confirmed DISARMED: no orders submitted, no ARM gate passed.
- [ ] Private/loopback-only network surface confirmed.
- [ ] VPS reboot → service restarts → DISARMED confirmed.
- [ ] Reconciliation run produces clean output against TESTNET state (no positions).
- [ ] Logs/alerts reachable; existing UI shows DISARMED status.
- [ ] Rollback tested on the production VPS.
- [ ] Owner verifies DISARMED Definition of Done (§30 Statement B).

**DISARMED Definition of Done satisfied.** ARM gate and first TESTNET paper order remain outside this budget and require separate owner authorisation.

---

# 23b. Recommended Next Move

After owner accepts this revised plan:

1. **New owner-authorised Gate-1 follow-up** for exhausted S2 loop (new repair round authorisation).
2. **Agree exact Linux semantic-port manifest** (list of paths from `6fe0130f` to port).
3. **Immutable integration/release plan** committed to repo.
4. **WP-0 execution:** baseline confirmed, Gate-1 signed, manifest agreed (2 h).
5. **WP-S:** implementer begins S2 repair; auditor in independent session after each round.
6. **Audit 1 (Gate-5):** freeze the exact WP-S checkpoint SHA/artifact and obtain an accepting S2/S3-closure verdict.
7. After Audit 1 accepts: proceed to **WP-L Phase 1** (semantic port: assess, select, port, package — non-executed/local checks only).
8. Complete **WP-I readiness** artifacts (lockfile, masked/inactive systemd unit design, rollback plan, staging test plan, security baseline) — **no Ubuntu execution**.
9. **Gate-A approval** (PRE-STAGING): request owner approval on non-executed readiness only (WP-L Phase 1 is non-executed; WP-L Phase 2 — Ubuntu revalidation is NOT yet executed).
10. After Gate A: execute the **one named expendable Ubuntu staging action** — perform the initial WP-I staging deploy + smoke test, retain that host for WP-L Phase 2 — Ubuntu revalidation (2 h), then complete WP-I staging verification. Retain the same host for WP-A.
11. **Audit 2 (Gate-5):** freeze the exact Linux-port/staging checkpoint SHA/artifact and obtain an accepting verdict before WP-A.
12. **WP-A:** run the 3 h Ubuntu invariant verification pass on the retained Gate-A-authorised staging host and capture all required staging evidence.
13. **Discard the expendable staging host** only after WP-A completes and all required staging evidence has been captured.
14. **Freeze the exact final release SHA/artifact** (accepted WP-S / WP-L / WP-I / WP-A + contingency repairs).
15. **Audit 3 (Gate-5) + Gate-6** on the exact frozen SHA/artifact.
16. **Gate-B approval** (PRE-PRODUCTION-DEPLOY): request owner approval on staging/systemd/SQLite/rollback/WP-A/security/final-SHA/audit evidence; Gate B requests the separate WP-V deployment approval.
17. **WP-V:** deploy only after the separate owner WP-V deployment approval. Verify DISARMED. No ARM.
18. **Gate-C** POST-DEPLOY acceptance: owner verifies DISARMED Definition of Done (§30 Statement B).

At each audit checkpoint, before staging-host discard and after discard only for §20/§22 Case 1, a contingency-funded repair that changes code or artifacts requires a new exact release SHA/artifact freeze and re-run of the affected audit on that exact new artifact. Re-audits draw only from WP-R. After discard, a Case 2 repair that would invalidate executed-Ubuntu evidence is BLOCK and requires new owner Gate-A-class staging authorisation outside this budget. Acceptance never carries forward; maximum three non-accepting repair/re-audit rounds per checkpoint, then stop and report to the owner.

**No ARM authorisation is contained in or implied by this plan.**

---

# 23c. Revised Multi-Agent Development Model

**Role assignment (per AGENTS.md two-tier model):** Codex is the task recipient, Lead, and sole independent acceptance authority; Claude CLI is the flagship implementer and self-QA owner (Gates G2–G4). In this plan, protected Bridge / core-runtime implementation remains with the **Claude CLI flagship implementer** and **may not be reassigned to any other model** — Gate-1 does not authorise moving protected Bridge/core work off Claude. The previous **GLM-5.2 edit of this plan document** was a **docs-only and non-precedential exception**, authorised by the owner for documentation editing of this file only. It does not authorise GLM, DeepSeek, Grok, NVIDIA, Cline, or any other secondary model to perform protected Bridge or core-runtime implementation, nor to perform canonical Gate-5 or Gate-6 audits. Canonical Gate-5/Gate-6 audits remain restricted to the AGENTS.md canonical audit roster: Claude `claude-opus-5` effort `xhigh`, or Codex `gpt-5.6-sol` effort `high`/`xhigh` as applicable. Secondary models remain limited to bounded unprotected mechanics and read-only supplemental checks; supplemental secondary-model output is never acceptance evidence. Codex Lead never implements counterpart work.

The recommended implementation structure:

```text
                    ┌─────────────────────────────┐
                    │   Codex — Lead / Acceptance  │
                    │  Gate ownership / Audit G5-6 │
                    └──────────────┬───────────────┘
                                   │ delegates implementation
                                   ▼
                    ┌─────────────────────────────┐
                    │  Claude CLI — Implementer   │
                    │    Self-QA (Gates G2–G4)    │
                    └──────────────┬───────────────┘
                                   │ may sub-delegate bounded unprotected work only
            ┌──────────────────────┼──────────────────────┐
            │                      │                      │
            ▼                      ▼                      ▼
     Test Engineer       Mechanical/Security        Documentation
                            Worker                    Worker
            │                      │                      │
            └──────────────────────┼──────────────────────┘
                                   ▼
                        Package Integration (Claude CLI)
                                   │
                                   ▼
                   Independent Auditor (Codex gpt-5.6-sol xhigh)
```

---

# 24. Agent Responsibilities

## Implementer — Claude CLI

Claude CLI is the flagship implementer for this sprint. Codex is the Lead and independent acceptance authority; Codex never implements counterpart work.

Responsible for:

* safety architecture;
* order logic;
* reconciliation logic;
* risk logic;
* persistence integration;
* recovery behaviour;
* package integration;
* resolving conflicting worker changes.

---

## Agent B — Test Engineer

Responsible for:

* unit tests;
* property tests;
* fixtures;
* failure scenarios;
* restart matrices;
* reconnect matrices;
* corruption fixtures;
* deterministic incident tests.

The Test Engineer should avoid simultaneous edits to core implementation files being modified by the Implementer (Claude CLI).

---

## Agent C — Mechanical / Security Worker

Responsible for:

* dependency locking;
* SBOM generation;
* static inventories;
* security scans;
* secret checks;
* manifest generation;
* repetitive deterministic updates;
* report scaffolding.

This agent should not make architecture, trading-risk, order-state, or financial-policy decisions.

---

## Agent D — Independent Auditor

Starts read-only.

Responsible for detecting:

* requirement violations;
* unsafe assumptions;
* execution-path gaps;
* restart problems;
* test gaps;
* false readiness;
* missing evidence;
* scope creep.

The auditor should remain independent of the main implementation reasoning wherever possible.

---

# 25. Audit Frequency

Do not perform a complete repository-wide audit after every small edit.

Use three primary audit checkpoints.

## Audit 1

After:

> Immediately after WP-S — S2 closure and minimum S3.

## Audit 2

After:

> Immediately after WP-L Phase 2 — Ubuntu revalidation + WP-I staging verification, and before WP-A.

## Audit 3

After:

> The exact final release SHA/artifact is frozen (containing accepted WP-S / WP-L / WP-I / WP-A plus any contingency repairs) and the WP-A invariant-map verification pass completes — COVERED and SMALL-GAP invariants confirmed passing on Ubuntu; Audit 3 independently re-derives and accepts the map from that exact frozen artifact plus the captured WP-A staging evidence package. It is an artifact- and evidence-level review requiring no Ubuntu execution and no live staging host.

**Funding:** Audit 1 first pass is funded from WP-S (§16); Audit 2, Audit 3, Gate-6, and every re-audit are funded from WP-R (§20); required repairs are funded from contingency (§22); contingency never funds audit work.

Additional targeted audits are allowed when:

* a high-risk defect is discovered;
* protected logic changes unexpectedly;
* an architectural assumption must be changed.

At each checkpoint, before staging-host discard and after discard only for §20/§22 Case 1, a contingency-funded repair that changes code or artifacts requires a **new exact release SHA/artifact freeze** and re-run of the affected Gate-5 audit, and Gate-6 where applicable, on that exact new artifact. After discard, Case 2 BLOCKS pending new owner Gate-A-class staging authorisation outside this budget. Acceptance of the previous artifact never carries forward. Re-audits are funded from WP-R's audit-only reserve; repairs are funded from contingency. Maximum three non-accepting repair/re-audit rounds per checkpoint; after the third, stop and report to the owner without entering a fourth round. If WP-R is exhausted while a required audit or re-audit remains, BLOCK.

---

# 26. Testing Frequency

The current tiered testing philosophy should remain.

What changes is how frequently the broadest suites are run.

---

## During Individual Edits

Run:

* affected unit tests;
* affected property tests;
* very narrow component tests.

---

## At Work-Package Completion

Run:

* relevant component suite;
* relevant integration tests;
* package-specific restart/failure tests.

---

## At Recovery Checkpoint

Run:

* restart suite;
* reconnect suite;
* reconciliation suite;
* database recovery subset;
* failure injection subset.

---

## At Final Sprint Verification

Run:

* complete relevant bridge suite;
* complete safety suite;
* recovery suite;
* failure suite;
* security checks;
* static checks;
* identity/drift validation.

This replaces repeatedly running every possible suite after every small task.

---

# 27. Context Management

A major source of AI development time is repeated repository rediscovery.

Every work package should therefore receive a compact:

# Context Pack

Example:

```text
CURRENT_STATE.md
WORK_PACKAGE.md
INVARIANTS.md
ALLOWED_FILES.md
RELEVANT_ARCHITECTURE.md
TEST_COMMANDS.md
KNOWN_RISKS.md
ROLLBACK.md
```

The package worker should not be required to reread:

* the complete 43-task backlog;
* every ADR;
* every historical report;
* all project documentation;

unless directly relevant to the package.

The final auditor may receive broader context.

Context Pack preparation (§27) and the per-package documentation, memory, and run-report work (§28) are absorbed inside each work package's stated hours and add nothing to the 50 h total.

---

# 28. Documentation Policy

Documentation, memory and run-report requirements should remain.

However, the recording unit should change from:

> every tiny task

to:

> every safety-coherent work package.

Instead of:

```text
Task A
→ docs
→ memory
→ report

Task B
→ docs
→ memory
→ report

Task C
→ docs
→ memory
→ report
```

use:

```text
Work Package
├── Task A
├── Task B
└── Task C

→ one governing documentation update
→ one memory update
→ one run report
```

Individual task evidence can remain as subsections inside the package report.

This preserves traceability while removing repeated administrative overhead.

---

# 29. Critical Stop Conditions

The 50-hour objective must never override a safety failure.

Stop the current work package immediately if any of the following becomes possible.

## Order Safety

* duplicate exposure can occur;
* ambiguous submission can be blindly retried;
* order identity changes across restart;
* partial position can remain naked.

## Reconciliation

* incomplete reconciliation can still show healthy;
* stale reconciliation can allow new risk;
* foreign exchange state can be automatically mutated incorrectly;
* local state can silently override exchange truth.

## Risk

* stale/incomplete inputs can authorise a trade;
* operational PnL is not actually connected to the risk engine;
* exposure limits can be bypassed;
* kill/disarm state is not persistent.

## Recovery

* restart can duplicate an order;
* restart can lose unknown-submission state;
* restart can lose protective state;
* database recovery is non-deterministic.

## Security

* secret material appears in logs, reports or diffs;
* credential identity is ambiguous;
* runtime/environment identity is ambiguous.

In these cases:

> Time budget loses priority to correctness.

---

# 30. Final MVP Completion Criteria (In-Budget Definition of Done)

The MVP is complete when both statements below can be supported by evidence:

**Statement A (Safety Core):**
> The single-strategy, single-symbol Hyperliquid testnet/paper runtime behaves deterministically and fail-safely under duplicate, unknown-submission, partial-fill, stale-data, reconciliation, risk, restart, reconnect, database, and kill/disarm failure scenarios — verified on Ubuntu KVM2.

**Statement B (DISARMED VPS Readiness):**
> One Ubuntu KVM2 VPS is deployed, non-trading (DISARMED), safety controls active, private/loopback-only, state-safe, restartable, reconcilable, and observable — verified by the owner.

Evidence must include:

* deterministic tests (Ubuntu runtime);
* execution-path tests (real execution path, not isolated unit mocks);
* integration tests;
* restart tests (Ubuntu systemd + signal handling);
* failure injection;
* recovery proof (SQLite backup/restore on Ubuntu);
* dependency/security evidence (pinned lockfile, secret scan, outbound inventory);
* independent adversarial audit (Gate-5 Codex `gpt-5.6-sol` xhigh + Gate-6 Codex `gpt-5.6-sol` xhigh);
* DISARMED VPS state verified by owner (no orders, loopback-only, reboot-safe).

---

# 31. What the 50-Hour Sprint Does Not Deliver

The sprint does **not** deliver:

* a final general-purpose trading platform;
* ARM gate or TESTNET paper-order processing;
* long soak paper-observation evidence;
* multi-symbol execution;
* multi-strategy portfolio allocation;
* multi-exchange support;
* full dashboard redesign;
* new research architecture;
* VectorBT platform integration;
* hftbacktest integration;
* Docker deployment;
* AI-lab cohosting on the VPS;
* general infrastructure scaling;
* advanced VPS security hardening (beyond minimum DISARMED readiness);
* live-capital approval.

Those remain Deferred Delivery Stage 2 or later Master Roadmap items.

---

# 32. After the Engineering Sprint (Outside 50-Hour Budget)

After DISARMED VPS verification and the gated exit evidence checklist:

```text
[IN-BUDGET END STATE]
Ubuntu KVM2 VPS deployed DISARMED, verified
        │
        ▼ (separate owner gate)
Explicit ARM Authorisation
        │
        ▼ (outside budget)
First TESTNET Paper Order
        │
        ▼
Bounded TESTNET Drills
        │
        ▼
Pre-Registered Paper Observation
        │
        ▼
Daily Evidence
        │
        ▼
Paper Conclusion
        │
        ▼ (separate live-release programme)
Live Capital Gate
```

During paper observation, feature development should be frozen.

Only the following should normally interrupt the paper period:

* Critical safety bug;
* High-severity execution defect;
* false-green monitoring problem;
* reconciliation defect;
* data-integrity defect.

Normal feature requests should go into the deferred backlog.

---

# 33. Deferred Delivery Roadmap

## V1.1 — Operations Improvements

Possible work:

* richer operations read model;
* improved alerting;
* improved health reporting;
* stronger strategy version attribution;
* market-data quality improvements.

---

## V2 — Research and Validation Architecture

Possible work:

* VectorBT integration;
* event-driven validation architecture;
* hftbacktest qualification;
* cost-model expansion;
* unified validation manifests;
* enhanced reproducibility/ranking infrastructure.

---

## V3 — Operations UI

Possible work:

* full MTC operations dashboard;
* incident views;
* reconciliation views;
* risk dashboards;
* enhanced alert management.

---

## V4 — Scale

Possible work:

* multi-symbol scheduler;
* portfolio-level allocation;
* correlation controls;
* multi-strategy support;
* additional exchanges.

---

## V5 — Infrastructure Expansion

Possible work:

* Docker qualification;
* multi-VPS / horizontal scaling;
* advanced VPS security hardening beyond DISARMED minimum;
* AI-lab cohosting;
* production infrastructure qualification (beyond single DISARMED VPS).

---

## Future Live Release

Only after:

* paper evidence is complete;
* unresolved Critical/High safety issues are closed;
* live governance is approved;
* explicit owner approval exists.

---

# 34. Revised Critical Path

```text
CONFIRMED MERGED TO origin/master (3cccc4c2)
──────────────────────────────────────────────
Phase 0
P1-001 ... P1-008
──────────────────────────────────────────────
NOTE: TS-P1-009B is NOT complete.
  S1: accepted (8d004590)
  S2: BLOCKED after repair round 3 (678e8b94)
  S3: unstarted
──────────────────────────────────────────────
             │
             ▼

==================================================
          50-HOUR SAFETY MVP
     (Ubuntu KVM2 VPS DISARMED-Ready)
==================================================

             │
             ▼
WP-0 (2h)
Owner plan acceptance
Gate-1 S2-loop authorisation
Linux semantic-port manifest
DISARMED VPS invariant-map compilation (§5.1–5.5 mapped to P1-001..008 evidence; gaps classified COVERED/SMALL-GAP/FULL-TASK)

SIDE-CAR FUNDING (not sequential stages):
WP-R (6h) = AUDIT-ONLY reserve for Audit 2, Audit 3, Gate-6, and all re-audits at all three checkpoints; the Audit-1 first pass is excluded and funded from WP-S (§16).
  If a required audit/re-audit remains after WP-R is exhausted → BLOCK; no contingency or other work package may fund it.
Contingency (5h) = funding source for Lead-approved repairs at whichever checkpoint produces them, plus eligible WP-S/WP-L/WP-I/WP-V overruns.
  Contingency never funds audits/re-audits. Required repairs return to the Claude CLI implementer.

             │
             ▼
WP-S (12h)
S2 blocker repairs
Minimum S3 implementation
[HARD STOP if round 3 of new cycle non-accepting → report to owner; no fourth round of new cycle]

             │
             ▼
AUDIT 1 — Gate-5 immediately after WP-S (first pass funded from WP-S internal 2 h + 2 h allocation (§16); re-audits at this checkpoint draw down WP-R)
Freeze exact WP-S checkpoint SHA/artifact; independently accept S2/S3 closure.
  Accept → continue.
  Non-accepting → repair (Contingency) → re-freeze new exact SHA/artifact → re-audit that exact artifact (WP-R).
  [Maximum three non-accepting rounds at this checkpoint; after the third → STOP/report owner; no fourth round.]

             │
             ▼
WP-L Phase 1 (pre-Gate-A; part of 8h; NON-EXECUTED — local/static checks only)
Essential Linux semantic port: assess, select, port, package (NO Ubuntu execution)
Lightweight invariant review
Semantic-port manifest produced (rationale, static/local verification — no Ubuntu execution)

             │
             ▼
WP-I readiness (part of 6h; NON-EXECUTED — no Ubuntu execution)
Reproducible lockfile (Ubuntu; install not yet executed)
systemd unit designed masked/inactive (not started)
SQLite backup/restore + rollback + staging-test plans documented
Minimum security baseline (lockfile/SBOM-equivalent, secret scan, outbound inventory)

             │
             ▼
GATE A — PRE-STAGING owner approval
(non-executed readiness only; NO executed-Ubuntu evidence may precede Gate A; authorises ONE named expendable Ubuntu 24.04 staging action)

             │
             ▼
ONE NAMED EXPENDABLE UBUNTU STAGING ACTION (Gate-A-authorised; host retained)
Initial WP-I staging deploy + smoke test (part of 6h); retain the host.
WP-L Phase 2 — Ubuntu revalidation (part of 8h): independently revalidate ported paths on the retained host (2 h).
WP-I staging verification (part of 6h): SQLite backup/restore, systemd start/reboot/SIGTERM, rollback tested.
Retain this same host through WP-A; no discard yet.

             │
             ▼
AUDIT 2 — Gate-5 immediately after WP-L Phase 2 — Ubuntu revalidation + WP-I staging verification, before WP-A (draw down WP-R)
Freeze exact Linux-port/staging checkpoint SHA/artifact; independently accept the Linux port + staging evidence.
  Accept → continue.
  Non-accepting → repair (Contingency) → re-freeze new exact SHA/artifact → re-audit that exact artifact (WP-R).
  [Maximum three non-accepting rounds at this checkpoint; after the third → STOP/report owner; no fourth round.]

             │
             ▼
WP-A on the retained Gate-A-authorised staging host (3 h; invariant-map finalization, existing Ubuntu-test execution, evidence capture/classification; SMALL-GAP repair uses contingency after Lead sign-off; FULL-TASK → Deferred Delivery Stage 2 or BLOCK)
Verification pass: confirm COVERED and SMALL-GAP invariants pass on Ubuntu
Classify gaps: COVERED / SMALL-GAP (contingency, Lead-approved) / FULL-TASK (Deferred Delivery Stage 2 or BLOCK)
No new P1-010..012, canonical Master Roadmap Phase 2 (P2), or Phase 4 (P4) full tasks scheduled here
[Audit 3 independent reproduction/acceptance is AFTER the SHA freeze below — not inside WP-A]

             │
             ▼
CAPTURE ALL REQUIRED STAGING EVIDENCE

             │
             ▼
DISCARD EXPENDABLE STAGING HOST
(only after WP-A completes and all required staging evidence has been captured)

             │
             ▼
FREEZE EXACT FINAL RELEASE SHA / ARTIFACT
(containing accepted WP-S / WP-L / WP-I / WP-A + contingency repairs; any later change invalidates acceptance)

             │
             ▼
AUDIT 3 — Gate-5 + GATE-6 on the exact frozen final SHA/artifact (draw down WP-R)
Artifact- and evidence-level only: independently re-derive/accept the DISARMED VPS invariant map and complete the security review from that exact artifact plus the captured staging evidence package; no Ubuntu execution or live staging host is required.
  Accept → continue.
  Non-accepting, Case 1 (implementer states and Lead confirms specified WP-A invariants/evidence cannot be affected) → repair (Contingency) → re-freeze new exact SHA/artifact → artifact/evidence-level re-audit of Audit 3 and Gate-6 as applicable on that exact artifact (WP-R); no host required.
  Non-accepting, Case 2 (repair would invalidate executed-Ubuntu evidence) → BLOCK (owner report; new Gate-A-class staging authorisation is OUTSIDE this 50 h budget); do not proceed to Gate B or WP-V on stale or partially invalidated evidence.
  Acceptance of any previous SHA/artifact never carries forward.
  [Maximum three non-accepting rounds at this checkpoint; after the third → STOP/report owner; no fourth round.]

             │
             ▼
GATE B — PRE-PRODUCTION-DEPLOY owner approval
(requires staging/systemd/SQLite/rollback/WP-A/security/final-SHA/audit evidence; requests SEPARATE WP-V deployment approval; does not itself deploy)

             │
             ▼
WP-V owner deployment approval (separate external gate; WP-V execution hours inside the 50h ceiling)

             │
             ▼
WP-V (8h, within budget if approved)
Ubuntu KVM2 VPS deployed
DISARMED verified: no orders, loopback-only
Restartable / reconcilable / observable
Rollback tested on production VPS

             │
             ▼
GATE C — POST-DEPLOY acceptance
(owner verifies DISARMED Definition of Done — §30 Statement B)

             │
             ▼
IN-BUDGET DEFINITION OF DONE SATISFIED

══════════════════════════════════════════════════
             OUTSIDE 50-HOUR BUDGET
══════════════════════════════════════════════════

ARM gate (separate owner authorisation)
First TESTNET paper order
Long soak paper observation
P4-005 Paper Observation period
```

---

# 35. Parallel Work Strategy

Parallelisation should be conservative.

The main rule is:

> Parallelise independent evidence and tests, not conflicting modifications to safety-critical core files.

Recommended streams:

```text
STREAM A
Claude CLI Implementer / Core Runtime

orders
risk
reconciliation
restart
persistence integration


STREAM B
Testing

fixtures
property tests
restart matrix
failure injection
corruption cases


STREAM C
Security / Mechanical

dependency locks
SBOM
scans
manifests
reports
```

Claude CLI implementer performs package integration; Codex Lead independently inspects and accepts or rejects it.

No two agents should concurrently modify the same protected core module without an explicit handoff.

---

# 36. Why 50 Hours Is Achievable via Fixed-Scope Selection

The reduction comes from removing entire categories of work from the first delivery.

The full Trading System roadmap is estimated at **400–600 hours**. The **50h budget is a fixed owner-set ceiling**, achieved by selecting a minimal conditional scope — not by mathematically subtracting overlapping category estimates from a 400h baseline. No arithmetic derivation from a subtraction table is claimed or supportable.

The important conclusion is:

> 50 hours is feasible only for the minimal-scope Safety MVP (Ubuntu KVM2 DISARMED-ready). It is not derivable from the full roadmap by subtraction.

---

# 36a. Feasibility Verdict

**CONDITIONAL GO.**

Risks that could invalidate the 50-hour ceiling:

| Risk | Mitigation |
|------|-----------|
| S2 blockers require more than 3 repair rounds | Hard stop after round 3; report to owner; budget does not auto-extend |
| Old-base Linux port reveals deep incompatibilities | Port only minimum semantic paths; validate each before proceeding |
| Ubuntu staging exposes environment assumptions not caught in testing | Follow the §18 Staging Host Lifecycle: retain the single Gate-A-authorised host through WP-L Phase 2 — Ubuntu revalidation, WP-I staging verification, and WP-A evidence capture before discard and before WP-V |
| Independent audit availability (Codex `gpt-5.6-sol` xhigh) | Gate is blocked if exact model/effort unavailable; owner must waive explicitly |
| VPS provisioning or network-isolation issues | Expendable staging deploy in WP-I validates assumptions before production VPS |

If any risk materialises into a safety blocker: stop, report, do not borrow time from Deferred Delivery Stage 2 or cut safety requirements.

---

# 37. Success Metric

The project should no longer measure success primarily as:

> Number of roadmap tasks completed.

For the accelerated programme, success is:

> One Ubuntu KVM2 VPS running a single-strategy, single-symbol Hyperliquid runtime is deployed DISARMED with deterministic and independently audited behaviour under the safety-critical failure scenarios that could otherwise create unknown, duplicated, naked, stale, or uncontrolled exposure — ready for a later separately-authorised ARM gate.

This is a substantially narrower goal than completing the full platform.

It is more useful than completing large amounts of platform infrastructure before the execution core and its Ubuntu deployment have proved themselves.

---

# 38. Recommended Governance Change

The existing `10_PHASE_EXECUTION_PROTOCOL.md` should be amended for the accelerated programme.

The current concept:

> One task per implementation session.

should be replaced, for approved Safety-MVP work, with:

> One bounded safety-coherent work package per implementation session.

The protocol should still require:

* explicit scope;
* protected-file rules;
* no opportunistic refactoring;
* tests;
* rollback;
* independent review at defined checkpoints;
* no unauthorised external action;
* no testnet/live activity without approval.

The change concerns execution granularity, not safety policy.

---

# 39. Final Recommendation

Keep the existing Master Roadmap as the long-term architectural plan. Do not delete it.

Do not attempt to complete it before the execution core and Ubuntu VPS deployment have proved themselves.

Create a new active-delivery layer containing only the 50-Hour Safety MVP.

The most important changes from the prior plan version:

1. **Ubuntu KVM2 VPS replaces Windows local runtime as the production target.**
2. **DISARMED readiness is the in-budget end state; ARM and orders are outside.**
3. **TS-P1-009B is NOT complete — S2 BLOCKED, S3 unstarted. Do not claim otherwise.**
4. **S2 closure + minimum S3 are mandatory first work packages before any Linux port.**
5. **Linux port is selective semantic paths from old-base only — no wholesale merge.**
6. **50h is a hard ceiling: safety gate overrun → BLOCK, never borrow from Deferred Delivery Stage 2.**
7. **Keep order, risk, reconciliation, and recovery safety work.**
8. **Defer research-platform, dashboard, Docker, multi-symbol, live, and scaling work to Deferred Delivery Stage 2.**
9. **Replace task-by-task execution with safety-coherent work packages.**
10. **Role model: Codex is Lead/sole independent acceptance authority; Claude CLI is flagship implementer/self-QA (Gates G2–G4). Protected Bridge/core-runtime implementation remains with the Claude CLI flagship implementer and is not reassigned by Gate-1. The previous GLM-5.2 edit of this plan document was a docs-only and non-precedential exception, authorised by the owner for documentation editing of this file only. It does not authorise GLM, DeepSeek, Grok, NVIDIA, Cline, or any other secondary model to perform protected Bridge or core-runtime implementation or canonical Gate-5/Gate-6 audits. Those audits remain restricted to the AGENTS.md canonical audit roster: Claude `claude-opus-5` effort `xhigh`, or Codex `gpt-5.6-sol` effort `high`/`xhigh` as applicable. Secondary models remain limited to bounded unprotected mechanics and read-only supplemental checks; supplemental secondary-model output is never acceptance evidence. Codex Lead never implements counterpart work.**
11. **Parallelise testing and mechanical/security work only where streams are independent.**
12. **Three independent audit checkpoints (Gate-5 Codex xhigh, Gate-6); never resume implementer session.**
13. **Separate active engineering hours from elapsed ARM/observation time.**

The target:

> **At most 50 active engineering hours to reach one Ubuntu KVM2 VPS deployed DISARMED, verified, and ready for a later separately-authorised ARM gate. ARM, first TESTNET paper order, and long soak observation are separate owner-gated actions outside this budget.**

The remainder of the Master Roadmap is not cancelled.

It is intentionally deferred until the single DISARMED VPS deployment has demonstrated that the execution core is safe, recoverable, observable, and worth expanding.
