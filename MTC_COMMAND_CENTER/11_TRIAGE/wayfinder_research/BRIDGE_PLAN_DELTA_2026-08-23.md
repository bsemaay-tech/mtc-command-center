# Bridge V2A/V2B plan vs deployed code — delta (wayfinder #87)

**Scope:** read-only comparison of the deployed Bridge source tree (`IBKR_PAPER_BRIDGE/`) against the V2A (§5) and V2B (§6) package scopes in `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md`, both read at master `ab35ca66`. No code was run; no server was started. All line citations are `IBKR_PAPER_BRIDGE/...` paths at this commit unless stated otherwise.

**Reading key for the verdict column:**
- **IMPLEMENTED** — the package's outputs (or a materially equivalent mechanism) already exist in code, cited below.
- **MISSING** — no trace of the concept exists anywhere in the tree; this is greenfield work.
- **DIVERGES** — something exists that is related or partially overlapping, but its shape, scope, or semantics differ from what the package specifies; treating it as "done" would be wrong.

---

## 1. Headline finding

The deployed Bridge (V1) is a mature, single-account, single-worker, single-strategy execution engine with an unusually deep **evidence and identity layer** (deterministic order/request/reconcile/kill identities, an append-only reconciliation ledger, a durable kill-episode ledger) that already anticipates several V2 requirements. But it has **no V2 architecture concepts at all**: no frozen-package loader, no `SizingRequest`/`BoundSizingIntent` contracts, no Risk Allocator, no Portfolio Guardian, no multi-worker supervisor, no admission authority, no authentication of any kind. The plan's own text is aware of this split — it explicitly instructs several V2A/V2B packages to build **on top of** named V1 mechanisms (the soak-window machine, the kill/flatten baseline) rather than from scratch — and that framing checks out against the actual code.

The two claims the ticket asked to specifically verify:

- **§9.6 test 3 ("the Bridge already stores enough")** — **substantially true but incomplete.** See §2.
- **Schema v4→v9 vs the plan's "v4→v8 activation"** — **true, and v9 is the interesting gap the plan doesn't mention.** See §3.

---

## 2. Reconciliation machinery vs brief §9.6 test 3

Brief §9.6 test 3 claims: *"Execution divergence report. Per live trade: intended vs authorized vs accepted vs filled price/quantity/time, with slippage attribution. The Bridge already stores enough to produce this; it is not surfaced."*

**What exists, and is genuinely enough for three of the four stages:**

- `decisions` table (`bridge/store/db.py:942-952`) — the "intended" stage: `decision_uid`, `ts`, `coin`, `stage`, `trade_id`, `payload_json`.
- `orders` table (`:954-969`) — the "accepted/submitted" stage: `qty`, `filled_qty`, `avg_fill_px`, `status`, `ts_submit`, `ts_last`.
- `fills` table (`:971-980`) — the "filled" stage: per-fill `qty`, `px`, `fee`, `funding`, `fill_ts`.
- `trades` table (`:982-1008`) — an already-computed aggregate carrying `expected_px`, `entry_px`, `exit_px`, `entry_ts`, `exit_ts`, and **`slippage_bps_entry` is already a column** — i.e. entry-side slippage attribution is already computed somewhere in the write path, just not exposed as a report.
- `order_identity` (`:1072-1085` onward) and `submission_attempts` give a deterministic, collision-checked identity chain from request to submission.

**What is missing, and makes the claim overstated for the "authorized" stage specifically:** V1 has no Guardian/Orchestrator concept, so there is no persisted "authorized" quantity/price distinct from "intended." The Bridge computes its own order quantity directly inside `RiskEngine._evaluate` (`bridge/engine/risk.py:380-393`: `raw_qty = risk_dollars / stop_distance`, notional/leverage gates applied in the same call) and submits it — there is no separate authorization step to record. The V2 `BoundSizingIntent`/Guardian authorize-or-reject split (WP-V2A-03, WP-V2B-01) doesn't exist yet, so a genuine 4-stage (intended/authorized/accepted/filled) divergence report cannot be built from today's schema without first building the authorization stage itself. `trades.slippage_bps_entry` also only covers entry — there's no symmetric exit-slippage column, so "slippage attribution" per trade is one-sided today.

**Verdict:** the brief is right that no code needs to be added to *capture* intended/accepted/filled — that data is already durable and joinable (`decisions` → `orders` → `fills` → `trades`, all keyed by `decision_uid`/`cloid`/`trade_id`). It is not surfaced as a report anywhere (`tools_v2/analysis_package/generate_analysis_package.py` is a redacting file-bundler for external review, unrelated; `tools_v2/observability/export_audit_pack.py` is a schema/row-count/recent-rows health dump, not a per-trade divergence report — neither computes slippage or joins these tables). But "already stores enough" needs a footnote: the **authorized** stage of the four-stage report has nothing to read from until WP-V2A-03/WP-V2B-01 exist, and exit-side slippage isn't columnized yet either.

**Adjacent but distinct machinery — do not conflate with the above.** `bridge/engine/reconcile.py`'s `FullReconciler` (`:1-11` docstring) and the v6 `reconcile_attempts`/`reconcile_components`/`reconcile_diffs`/`reconcile_checkpoints`/`funding_events` tables (`db.py:1555-1730`) are a **two-way** reconciliation: local durable intent/order state vs. broker-reported truth (orders, fills, positions, balances, margin, funding), append-only and immutable by trigger. This is not the same thing as WP-V2B-07 Lane A's **"daily three-way reconciliation record across expected signals, bridge/executor log and simulated statement"** — that's a three-input comparison for the paper-soak lane specifically, and nothing in the current reconcile machinery ingests an independent "expected signals" feed or a "simulated statement" as a third input. The v6 ledger is real, tested (`tests/test_reconciliation.py`), and directly reusable as the bridge/executor-log leg of that three-way comparison — but it is not itself the three-way check the plan describes.

---

## 3. Schema versions v4–v9 vs the plan's "v4→v8 activation"

`bridge/store/db.py:268-309` defines six supported target schema versions, **all already implemented in code today**, all additive/opt-in behind an explicit `initialize(target_schema_version=N)` call, with the **operational default staying at v4**:

| Version | Constant | What it adds | Migration code |
|---|---|---|---|
| 4 | `SCHEMA_VERSION_BASELINE` | identity/submission ledger (default, always on) | `db.py:916-1354` |
| 5 | `SCHEMA_VERSION_PARTIAL_FILL` | partial-fill recovery ledger | `db.py:1464-1554`ish, guarded `:1471-1489` |
| 6 | `SCHEMA_VERSION_FULL_RECONCILE` | `reconcile_attempts`/`components`/`diffs`/`checkpoints`, `funding_events` | `db.py:1555-1730`, migration guard `:1964-2001` |
| 7 | `SCHEMA_VERSION_DURABLE_RISK` | `risk_day_checkpoints`, `risk_control_latches` | `db.py:2020-2105`, guard `:2144-2167` |
| 8 | `SCHEMA_VERSION_EXPOSURE_CONTROLS` | capability bump only — **no new business table**, revalidates v7 topology/FKs and bumps the meta row (`db.py:285-297` docstring says this explicitly) | guard `:2216-2236` |
| 9 | `SCHEMA_VERSION_KILL_EVIDENCE` | `kill_requests`, `kill_attempts`, `kill_actions`, `kill_action_events` — durable kill-episode ledger | `db.py:2277-2360`ish, guard `:2722-2754` |

**This directly confirms the plan's own framing of WP-V2B-04** ("switch on the accepted risk contracts that the default init path does not enable") — the work is activation of already-built, already-tested schema, not new schema authorship. `bridge/engine/engine.py`'s live kill path (`_run_kill_episode`, `:429-537`) already gates on `self.store.kill_evidence_enabled()` (`:450`) and no-ops the durable-evidence path when v9 isn't active — i.e. the code is already written to run correctly whether or not the schema has been activated, which is exactly the additive/rehearsable posture WP-V2B-04 asks for.

**The gap the plan doesn't mention:** the plan's dependency chain and every V2A/V2B package citation talk about **"schema activation v4 → v8"** (WP-V2B-04's own title). Schema v9 (`SCHEMA_VERSION_KILL_EVIDENCE`) exists, is wired into the live kill path today, and is not named anywhere in WP-V2B-04's scope, inputs, or outputs — the package as written would activate v8 and stop, leaving the kill-evidence ledger that the engine's own kill path already depends on for its richest evidence path un-activated. This is worth a disposition decision (fold v9 into WP-V2B-04's target, or add an explicit "and v9" line) rather than silently discovering it during the activation rehearsal.

---

## 4. Soak-window machine (`bridge/engine/window.py`) vs the `INTERNAL_PAPER` brownfield decision

Brief §6.4 (line 1311, map #54 fold, ticket #59) states: *"The `INTERNAL_PAPER` lane's carrier starts from the existing, tested Bridge soak-window machine (`bridge/engine/window.py`, RUNNING/DOWN/INTERRUPTED/RESET) and ADDS identity binding (`deployment_identity_hash`, `evidence_window_start`) — it is not built from scratch."*

Read against the actual file (`window.py`, all 209 lines read in full):

**What exists today, confirmed:**
- Exactly the four states named: `WINDOW_RUNNING`/`WINDOW_DOWN`/`WINDOW_INTERRUPTED`/`WINDOW_RESET` (`:32-35`).
- A pure decision function `compute_window_state()` (`:59-91`) with an explicit rule order, plus a read-model wrapper `window_status()` (`:94-166`) that fails safe (unreadable evidence → `DOWN`, never an active window).
- Meta-key persistence only (`window_started_ts`, `window_last_alive_ts`, `window_interrupted_ts`, `window_reset_ts`, `:37-40`) — a liveness pulse recorded on every successful reconcile cycle (`record_liveness`, `:178-180`), called from `engine.py`'s reconcile loop.
- A **single, global** window — one set of meta keys, no per-worker and no per-environment scoping anywhere in the file.

**Genuinely missing, exactly as the brief's own "ADDS" phrasing anticipates — this is not a criticism of window.py, it is the stated delta:**
- `deployment_identity_hash` and `evidence_window_start` — neither string appears anywhere in the repository (`grep -r` across `IBKR_PAPER_BRIDGE` returns zero hits for both). The window has no identity binding at all today; a schema/config change mid-window would not reset or even be visible to it.
- Environment scoping (`INTERNAL_PAPER` vs `EXCHANGE_TESTNET` vs `FORWARD_SHADOW`) — window.py has no concept of environment; it only reads `app_state` (ARMED/DISARMED/KILLED).
- The Lane A evidence artifacts WP-V2B-07 requires — pre-registered immutable plan, ≥30-forward-trade counter scoped to one environment, daily three-way reconciliation record — none of these exist in window.py or anywhere else searched.

**One substantive divergence, not just an absence — the outage rule.** WP-V2B-07 (line 771) specifies: *"a restart with clean recovery and an intact daily reconciliation chain continues the window and stands as restart/recovery evidence; only an unexplained or unbridgeable evidence break kills it."* `window.py`'s actual `detect_interruption()` (`:183-199`) does not implement this distinction: **any** liveness gap exceeding `stale_after_s` (default 300s, `:42`) stamps a sticky `META_INTERRUPTED` marker unconditionally — there is no check of whether the subsequent reconciliation was clean, and no code path that would let a "clean recovery" continue the window rather than mark it `INTERRUPTED`. The interruption is sticky until an explicit `reset_window()` call (`:202-208`), which per the module's own docstring (`:20-25`) is itself still `PROPOSED, pending Barış confirmation`. So the brownfield base is correctly identified, but the specific "evidence-based outage" semantics the wayfinder fold decided (ticket #39) are **not yet built on top of it** — today's rule is strictly stricter (any gap = interrupted) than the plan's target rule (only unexplained gaps = interrupted).

Also worth noting: the window is process-global, not per-worker. WP-V2A-08's phrasing "an unexplained evidence break kills that worker's window only" presumes a per-worker window, which requires WP-V2A-02's worker identity (also not yet built, see §5) before it can even be expressed — window.py as written has nothing to scope "that worker's window" to.

---

## 5. Worker/supervisor hooks

**Genuinely missing, no partial implementation found.** `grep -r` for `supervisor|Supervisor|multi.?worker|worker_id|WorkerIdentity` across `bridge/` returns exactly one hit, and it is unrelated (`bridge/engine/bars.py`, a variable name collision, not a supervisor concept). There is:
- No worker identity tuple anywhere.
- No per-worker isolated state store (WP-V2A-02's SQLite-per-worker decision, ticket #41, has no code yet).
- No supervisor process or registry (WP-V2B-03).
- `bridge/settings.py:31-37` confirms the single-account model directly: one `hl_account_address`/`hl_api_wallet_key` pair, no account list, no subaccount binding.
- `bridge/engine/strategy_base.py` (23 lines) defines one `Strategy` Protocol; only one concrete strategy exists (`bridge/engine/strategies/keltner_trail_ema8.py`), loaded directly, not through any frozen/hash-verified loader (no `package_hash`, no loader module, anywhere in `bridge/`).

The dashboard prototype (`dashboard_v2_prototype/`, see §7) already draws a "worker identity tuple" and "Guardian veto tiers" UI against **fixture JSON** (`fixtures/workers.json`), which is worth flagging precisely because it means the visual vocabulary is ahead of the backend that would produce it — nothing in `bridge/` computes any of what that prototype displays.

---

## 6. WP-V2A package-by-package delta

| Package | Verdict | Evidence |
|---|---|---|
| **V2A-01** Frozen package loader | **MISSING** | No `package_hash` verification, no admission-check module, no loader anywhere in `bridge/`. Strategy is loaded by direct import (`strategy_base.py` + one concrete strategy file), not a hash-verified package system. |
| **V2A-02** Worker identity, per-worker state | **MISSING** | No worker identity tuple, no per-worker store. Single-process, single-strategy, single-account today (`settings.py:31-33`). |
| **V2A-03** Risk Allocator + Decision Orchestrator wiring | **MISSING** (depends on WP-P0-20, itself not started) | Bridge computes its own quantity directly in `RiskEngine._evaluate` (`risk.py:380-393`); no allocator import, no `sizing_method` taxonomy (`RISK_AT_STOP`/`FIXED_QTY`/`FIXED_NOTIONAL`/`VOLATILITY_TARGET`/`SOURCE_DEFINED` — zero hits repo-wide), no Orchestrator concept. |
| **V2A-04** `AccountSnapshot` identity, fail-closed rejection | **DIVERGES** | `AccountSnapshot` already exists as a type (`bridge/engine/types.py:60-63`) but is a bare 3-field value object (`equity`, `available_margin`, `withdrawable`) with **no `snapshot_id`**, no immutability enforcement, and none of `SNAPSHOT_MISMATCH`/`SNAPSHOT_STALE`/`REFERENCE_DIVERGENCE` (only a related `RISK_SNAPSHOT_STALE` constant exists at `types.py:1269`, used for a narrower purpose inside `RiskEngine`, not the V2 rejection-path contract). |
| **V2A-05** Bridge intent seam | **MISSING**, and its precondition confirms today's opposite behaviour | The package's own goal is "the Bridge... never originates a quantity when an authorized intent is present" — confirmed today it always does (see V2A-03 row); no seam exists to reject a Bridge-originated quantity in favor of an external one. |
| **V2A-06** Native strategy stop semantics (local proof) | **DIVERGES (more built than the plan implies)** | Native reduce-only stop orders with `trigger_px` and amendment logic already exist in `bridge/engine/orders.py` (role-based `ENTRY` vs. protective-order handling, e.g. `:501-509, 550, 617, 683`; stop amendment comparison at `:3158-3161`; `kill_flatten_reduce_only` broker call at `:1564`). What's missing specifically is the package's **emulator/replay harness and the process-kill/restart re-attachment drill as a standalone falsifiable artifact** — that formal proof doesn't exist as its own module/test, even though the underlying live mechanism it would be proving is already in production use. |
| **V2A-07** Simulator↔Worker replay equivalence | **MISSING** | No harness comparing simulator output to worker replay output found; this requires WP-P0-20's canonical simulator migration first, which the plan itself notes hasn't started. |
| **V2A-08** `FORWARD_SHADOW` runtime | **MISSING** | Zero hits for `FORWARD_SHADOW` anywhere in `bridge/` (only in the dashboard prototype's fixture data and deploy docs, both non-runtime). |
| **V2A-09** Bridge migration record | **MISSING** (a documentation package; no evidence it has been produced) | No `deployment_identity_hash` exists yet for it to record (see §4); this package's own inputs (accepted V1 candidate identity, V2 audit statuses) presuppose work not yet done. |
| **V2A-10** Environment Admission Authority | **MISSING** | Zero hits for `SHADOW_ELIGIBLE`/`TESTNET_ELIGIBLE`/`admission` as a concept anywhere in `bridge/` runtime code. |

---

## 7. WP-V2B package-by-package delta

| Package | Verdict | Evidence |
|---|---|---|
| **V2B-01** Portfolio Guardian + Risk Buckets | **MISSING** | No `Guardian` class, no `RiskBucket` type anywhere in `bridge/` (the only "authorize"/"reject" hits repo-wide are `OrderState.REJECTED` order-lifecycle values in `types.py`, unrelated to a Guardian authorize-or-reject architecture). `config/bridge.yaml:21,26` does already carry the flat `max_leverage: 1` / `max_effective_leverage: 1.0` envelope the brief cites at §10.1 — that single-account risk ceiling exists, but not the per-bucket structure. |
| **V2B-02** `PortfolioSimulator` with shared Guardian objects | **MISSING** | Depends on V2B-01 and the not-yet-migrated canonical simulator (WP-P0-20); no portfolio-level simulator found. |
| **V2B-03** Multi-worker supervisor | **MISSING** | See §5 — no supervisor concept exists at all. |
| **V2B-04** Schema activation v4→v8 | **PARTIALLY IMPLEMENTED as a capability, activation itself not performed** | See §3 in full — all six schema versions including v9 are already coded, tested, and additive; what's missing is the actual rehearsed activation-on-a-copy and the go-live decision, which is explicitly gated (T0, separate authorization) and correctly not attempted here. Scope gap: the package as titled stops at v8 and doesn't name v9, which the live kill path already depends on. |
| **V2B-05** Execution Dashboard V2 | **DIVERGES** | A static, fixture-backed, read-only prototype exists (`dashboard_v2_prototype/`, `README.md:1-7`: "Package 3, Tier T1") implementing the visual vocabulary (three-layer desired/accepted/actual view, worker identity tuple, Guardian veto tiers) — but it is explicitly non-functional scaffolding ("no server, no build step... no request of any kind leaves the page") wired to hand-authored fixture JSON, not the runtime dashboard the package specifies. The real dashboard has no backend to render (Guardian, worker identity, command surface all missing per rows above). |
| **V2B-06** Zero-trust access, step-up auth | **MISSING** | Zero hits for `WebAuthn`/`FIDO2`/`authenticator`/`step-up` anywhere in the repo. Current API auth is a single `X-Confirm` header check (`bridge/api/routes.py:227-230`, `_require_confirm`) gating `PUT /api/config`, `POST /api/arm`, `POST /api/kill/ack` — a confirmation code, not authentication, and not the two-authenticator redundancy model. No login, session, or API-key check exists in `routes.py` at all; the deployed instance relies on network isolation (loopback-only per prior evidence), matching the "no public port" *target* but not the WebAuthn *requirement*. |
| **V2B-07** `INTERNAL_PAPER` soak + `EXCHANGE_TESTNET` fleet | **MISSING** (Lane A) / **DIVERGES-toward-existing** (Lane B groundwork) | Lane A: see §4 — the brownfield base (`window.py`) exists but lacks every Lane-A-specific artifact (immutable plan, identity binding, trade counter, three-way reconciliation). Lane B: `MockBroker` (`bridge/broker/mock.py:70-80`) matches the brief's own citation exactly ("the `INTERNAL_PAPER` fill source of §6.4") and is real, but this package's actual Lane B object is `EXCHANGE_TESTNET` venue proof — `bridge/broker/hyperliquid.py` exists as the live venue adapter, but no testnet-specific fleet/capacity harness was found. |
| **V2B-08** Drag-and-drop (simulation only) | **MISSING** | Not present in `dashboard_v2_prototype/` (which is read-only/non-interactive per its own README) or anywhere else. |
| **V2B-09** Workflow cutover | **N/A — not a code package** | Organizational/process package; nothing to verify against source. |
| **V2B-10** Emergency operations — DISARM/KILL/FLATTEN | **DIVERGES, and closer to the target than the plan's own baseline framing suggests** | The plan's own baseline description is accurate as a citation of the *API surface*: one `/api/kill` path with an optional `flatten` bool (confirmed: `bridge/api/routes.py:113-121`, `bridge/engine/engine.py:421` `kill(flatten: bool = False)`; no `/api/flatten` route exists) and a separate `/api/disarm` (`routes.py:102-103`, `engine.py:393-419`). *(Minor citation note: the plan cites `engine.py:391-404` for `kill`/`:406-412` for `acknowledge_kill`; at this exact commit `kill` is at `:421` and `acknowledge_kill` at `:539` — same functions, offset line numbers, likely a stale citation from an earlier revision of the file.)* But the underlying mechanics are considerably more built than "one path with a bool" implies: `_run_kill_episode` (`engine.py:429-537`) already does cancel-and-latch with a durable, evidence-backed kill episode (v9 schema: `kill_requests`/`kill_attempts`/`kill_actions`/`kill_action_events`), already discriminates `role == "ENTRY"` vs. protective/reduce-only orders in the cancellation path (`orders.py:501-509, 550, 617, 683`, plus a dedicated `kill_flatten_reduce_only` broker call), and already binds kill termination to a fresh reconcile checkpoint (`engine.py:510-534`) — i.e. much of "KILL scoped to risk-increasing orders, preserving protective orders" and "KILL's reconcile obligation" already exists as working code, not as a gap. What's genuinely missing: three separately-named API paths/audit records (today it's two paths, `kill`+`disarm`, with `flatten` as a parameter of `kill` rather than its own confirmed, step-up-authenticated operation), `human_override` field, the `PROTECTION_DRIFT` code name specifically, the out-of-band venue-side runbook document, and the no-orphan disposition-menu policy (adopt-under-successor / exits-only run-off) — none of those found anywhere. |
| **V2B-11** Bridge migration and deployment execution | **MISSING** (correctly — gated on V2A-09 and schema activation, neither done) | No `deployment_identity_hash`, no deployment record artifacts found. |

---

## 8. Notes for the tickets this feeds

- **Reconciliation ticket:** the two-way (`FullReconciler`) vs three-way (Lane A daily check) distinction in §2 is the load-bearing nuance — don't let "the bridge already has reconciliation" collapse into "Lane A's daily three-way check is done."
- **Failure-semantics ticket:** the sticky-vs-evidence-based outage rule gap in §4 is a concrete, small, well-scoped piece of work (a `detect_interruption` rewrite plus a reconciliation-cleanliness input) — worth carrying forward as a discrete finding rather than folding into the general "window.py needs identity binding" note.
- **Gap-disposition ticket:** schema v9's absence from WP-V2B-04's stated scope (§3) is a genuine plan gap, not a code gap — the code is ready for v9 activation, the package that would authorize it doesn't mention v9 by name.
- Every "MISSING" row above was checked by repo-wide `grep` for the concept's name/constants, not by absence-of-memory; each miss is stated with the search term that returned zero hits, so a future check can re-run the same grep to confirm the fold is still open.

---

*Read-only investigation. No bridge process, server, or test suite was executed. All citations are against `IBKR_PAPER_BRIDGE/` and `MTC_COMMAND_CENTER/11_TRIAGE/` at master `ab35ca66c574f051ae7f01173eafc1145a3f72cf`, from worktree `C:\WFB1` on branch `research/bridge-plan-delta`.*
