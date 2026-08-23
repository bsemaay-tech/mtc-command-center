# Failure-Mode Catalog vs. Safety Mechanisms (Wayfinder Ticket #105)

Research ticket: `bsemaay-tech/mtc-command-center#105` (parent #96, blocking #111).
Branch: `research/failure-mode-catalog`. Base: `origin/master` @ `ab35ca66`.
Scope: read-only repo research. No connection to KVM2 or any host; no ssh.

## Method and sources

Primary sources read directly (not summarized secondhand):

- `IBKR_PAPER_BRIDGE/bridge/**` — engine, order, window, store, API, broker source.
- `IBKR_PAPER_BRIDGE/docs/00…31*.md` — the numbered contract series, especially
  `19_P2_RECONNECT_INCIDENT_2026-07-13.md`, `21_WINDOW_STATE_CONTRACT.md`,
  `25_PARTIAL_FILL_PROTECTION_CONTRACT.md`, `30_TSP1009_KILL_EVIDENCE_RECOVERY.md`,
  `31_KILL_EVIDENCE_EPOCH_CONTRACT.md`.
- `IBKR_PAPER_BRIDGE/tools_v2/observability/CHAOS_DRILLS_DESIGN.md` — the drill spec.
- `IBKR_PAPER_BRIDGE/tests/test_p1_failure_drills.py` — the *implemented* failure-drill
  test suite (distinct from the chaos-drill design doc, which is explicitly not implemented).
- `IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md` — secret-scan and credential handling.
- `IBKR_PAPER_BRIDGE/docs/17_DEPLOYMENT.md`, `07_BROKER_DECISION.md`, `06_HYPERLIQUID_SETUP.md`
  — credential/wallet architecture.
- `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md`
  (OPS-A / WP-P0-26, OPS-C / WP-P0-27 package definitions).
- `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md` — the most recent
  (2026-08-17) evidence-backed statement of which schema-gated capabilities are active.
- GitHub issues (via `gh`, read-only): #38, #39, #45 (closed, ratified 2026-08-23 — backup/
  restore/retention, hosting + dead-man watchdog, kernel/NTP edge policies) as the current
  state of maps #37/#54/#67/#78/#79's fold decisions relevant to this scope.

No file outside the worktree was modified. Issues #95/#96/#97 were not touched.

## Central finding — a schema gate, not a feature gate

The single most important fact for this catalog: **the deployed bridge runs on the
default schema, `SCHEMA_VERSION_BASELINE = 4`** (`bridge/store/db.py:263-264,523-524`;
`bridge/app.py:108` calls `store.initialize()` with no target). Per the most recent
evidence-backed status record (`BRIDGE_V2_DEFERRAL_BACKLOG_2026-08-17.md`, table row 3–4),
**every capability built under schema v5–v9 is code-complete, self-QA'd, and covered by
tests, but structurally inert on the currently-deployed database**:

| Schema | Capability | Status on v4 runtime |
|---|---|---|
| v5 | Partial-fill protect-or-flatten (`25_PARTIAL_FILL_PROTECTION_CONTRACT.md`) | inert |
| v6 | Full reconciliation / authoritative risk snapshot (`26`, `27`) | inert |
| v7 | Daily-loss / max-drawdown risk-control latches (`28_FULL_TSP1007_RISK_CONTROLS.md`) | inert |
| v8 | Exposure / leverage / liquidation controls (`29_TSP1008...md`) | inert |
| v9 | Kill-evidence episode ledger, idempotent cancel/flatten (`30`, `31`) | inert |

The sharpest concrete consequence, read directly from `bridge/engine/engine.py:450-455`:

```python
if not self.store.kill_evidence_enabled():
    # v9 is explicitly opt-in. Older stores latch KILLED but perform
    # no best-effort broad mutation and can never acknowledge without
    # the durable evidence contract.
    await self._publish("status", self.status())
    return
```

On the schema the runtime actually uses, `POST /api/kill?flatten=true` **stops new order
submissions and latches `app_state=KILLED`, but does not cancel any resting order or
flatten any position.** The cancel-and-flatten machinery this ticket was scoped to matrix
(cancel-and-latch, exact-lot verified flatten, `FLATTEN_PARTIAL` handling) only runs once
`kill_evidence_enabled()` — i.e. schema v9 — is active. This gate is a deliberate safety
choice (avoid legacy best-effort mutation without the evidence contract), not an oversight,
but it means the matrix below has to be read at two layers: **what the code proves under
test**, and **what actually executes on the deployed unit today**. Every row is marked
accordingly. No evidence was found in this worktree of a v4→v5+ migration having been
performed on the runtime database (searched `BRIDGE_V2_DEFERRAL_BACKLOG*`,
`WPI_ARTIFACT_RETENTION_INVENTORY_2026-08-17.md`, `GLOBAL_HANDOFF*`); this is a
**documentation gap for a future ticket to close by direct host inspection**, not a claim
that migration definitely never happened.

## Matrix

Status legend: **HANDLED** = built, tested, and active on the deployed (v4) runtime.
**PARTIAL** = either (a) code-complete/tested but gated behind an inactive schema or an
unbuilt ops package, or (b) baseline coverage exists but a known sub-case is uncovered.
**UNHANDLED** = no code path and no ratified plan found.

### The ten failure modes named in the ticket

| # | Failure mode | Status | Mechanism(s) | Pointers |
|---|---|---|---|---|
| 1 | **Host death mid-position** | PARTIAL | Window-state contract makes a dead bridge structurally unable to present as `RUNNING` (liveness-staleness rule, `stale_after_s=300`). Kill/partial-fill recovery state is durable and survives restart *when the owning schema is active*. Ratified plan (ticket #39, 2026-08-23): external dead-man watchdog with phone push within ~15 min, and a host-outage-vs-clock rule that treats clean-recovery restart as logged incident, not window death. | `bridge/engine/window.py` (`compute_window_state`, `detect_interruption`); `docs/21_WINDOW_STATE_CONTRACT.md`; `docs/25_PARTIAL_FILL_PROTECTION_CONTRACT.md` §6 "restart semantics"; `docs/30_TSP1009_KILL_EVIDENCE_RECOVERY.md` "Restart and acknowledgment"; issue #39 resolution comment (OPS-A / WP-P0-26). | 
| | | | **Gap:** the watchdog (OPS-A, `WP-P0-26`) is a ratified *decision*, not yet built — "a decision is not an authorization" (issue #38 resolution). No dead-man's-switch order exists at the exchange itself; between host death and either auto-restart-recovery or a human reacting to a watchdog page, an open position sits unmanaged. Issue #39's own text notes the V1 unit on KVM2 (deployed 2026-08-17) "not re-verified live since" — i.e. no confirmed active watchdog protects the currently running unit today. | |
| 2 | **Venue outage / degradation** | PARTIAL | Consecutive-order-reject auto-disarm and reconcile-failure tolerance (`reconcile_max_consecutive_failures`, default 3) are baseline v1/v4 behavior, always active. DATA_STALE auto-disarm after a configurable reconnect budget is deployed baseline (03_STATUS.md's "outage-tolerance" build, `1465f8f0`). | `bridge/engine/engine.py:82,113-114,168-169` (`reconcile_max_consecutive_failures`, `_consecutive_order_rejects`); `tests/test_p1_failure_drills.py::test_drill_three_order_rejects_auto_disarm`, `::test_drill_data_stale_auto_disarms`; `docs/03_STATUS.md` "Outage-tolerance deployment". | 
| | | | **Gap:** no distinct handling for a venue that is *slow or degraded but technically responsive* (wide spreads, delayed fills, partial API functionality) — only binary reject/stale counters. No venue-status feed integration. | |
| 3 | **Credential loss / leak** | PARTIAL | Strong architectural bound: Hyperliquid **agent/API-wallet model — a fully compromised bridge cannot withdraw funds**, only trade within the account. Per-machine distinct named agent wallet so a compromised host costs revocation of one agent only; the main wallet key is never placed on any host. Static, content-redacted secret scanning of the source tree and built payload (zero hits at freeze) plus credential-scrubbed test runs. Mainnet is hardcoded unreachable (`network="testnet"` only) and `HL_LIVE_ACK` must never be defined. | `docs/07_BROKER_DECISION.md:65`; `docs/06_HYPERLIQUID_SETUP.md:46`; `docs/01_ARCHITECTURE.md:758`; `docs/17_DEPLOYMENT.md` §0 "her makineye AYRI API cüzdanı"; `deploy/linux/SECURITY_BASELINE.md` §2–3. | 
| | | | **Gap:** revocation is a manual, undocumented-in-tooling step (no key-rotation script/runbook found); no scheduled rotation cadence; no anomaly/misuse detection if a leaked key is used from an unexpected location. | |
| 4 | **Bridge crash while ARMED** | PARTIAL | Baseline (always active): startup forces non-`KILLED` state to `DISARMED`; `arm()` refuses on submission quarantine, active partial recovery/`UNPROTECTED_ABORT`, stale reconcile evidence, or an unresolved re-arm proof. Code-complete but schema-gated: kill-evidence v9's restart law ("restart never acknowledges, disarms, or arms" a reserved/unknown action) and partial-fill recovery's restart-preserving deadline/generation logic. | `docs/19_P2_RECONNECT_INCIDENT_2026-07-13.md` ("Startup also resets non-KILLED state to DISARMED"); `bridge/engine/engine.py:238-310` (`arm()`); `docs/30_TSP1009_KILL_EVIDENCE_RECOVERY.md` "Restart and acknowledgment"; `docs/25_PARTIAL_FILL_PROTECTION_CONTRACT.md` §6; chaos-drill spec D4-a…d (`CHAOS_DRILLS_DESIGN.md`). | 
| | | | **Gap:** see Central Finding — the crash-during-KILL evidence/idempotency guarantees are v9-gated and inert on the deployed schema; only the coarse `app_state=KILLED` memory/meta latch is active. | |
| 5 | **Partial fills during KILL / FLATTEN** | PARTIAL | Fully specified and adversarially tested (135 tests) contract: 10.0 s protect deadline, 5.0 s flatten deadline, exact-lot verified single stop, `UNPROTECTED_ABORT` fail-closed on any ambiguity, `FLATTEN_PARTIAL` retained rather than re-issuing a second full-size close. | `docs/25_PARTIAL_FILL_PROTECTION_CONTRACT.md` (status: "PROPOSED — implemented and self-QA'd offline; pending independent audit and owner acceptance. Not deployed" — doc line 18); `docs/30_TSP1009_KILL_EVIDENCE_RECOVERY.md` "Cancellation and protection law" (the `FLATTEN_PARTIAL` step); chaos-drill D2-a/b/c/d. | 
| | | | **Gap:** confirmed inert on the deployed v4 schema — see Central Finding. `POST /api/kill?flatten=true` on the running unit does not flatten a partial position at all today; it only blocks new risk. | |
| 6 | **Clock drift** | PARTIAL | `compute_window_state` already fails closed on future-dated liveness (`error: future_liveness`) — an existing, active baseline guard against one drift symptom. Ratified plan (issue #45, 2026-08-23): NTP-synced host with a drift-alarm threshold checked by the OPS-A watchdog; UTC-only internal timestamps; venue candle timestamp is the authoritative bar identity (never local clock). | `docs/21_WINDOW_STATE_CONTRACT.md` (decision-order step 3, "future-dated liveness"); `bridge/engine/window.py:85` (`age_s < 0 or age_s > stale_after_s`); issue #45 resolution item 2. | 
| | | | **Gap:** the NTP/drift-alarm mechanism itself does not exist yet — it rides on OPS-A (`WP-P0-26`), not yet built. Beyond the future-dated-liveness edge case, there is no runtime drift monitor. | |
| 7 | **Disk full** | UNHANDLED | No code path anywhere in `bridge/store/db.py` or the test suite references disk space, `ENOSPC`, or a SQLite "database or disk is full" condition (verified by grep across the whole `IBKR_PAPER_BRIDGE` tree — zero matches). A write failure from a full disk mid-KILL/FLATTEN is not a modeled or tested case, unlike disconnects and crashes. | (absence of evidence — searched `bridge/store/db.py`, `tests/*`, `IBKR_PAPER_BRIDGE` tree-wide for `disk`, `ENOSPC`, `OperationalError`, `IOError`, `OSError`). | 
| | | | OPS-A's log-retention/size-budget policy ("bulky forward logs carry a size budget and move to compressed cold archive when it is hit" — issue #38 resolution item 4) reduces *evidence-store growth-driven* disk exhaustion, but that is a distinct concern from a live SQLite write failing mid-trade, and OPS-A is itself not yet built. | |
| 8 | **Network partition** (bridge ↔ venue) | HANDLED | WebSocket reconnect with a config-driven retry budget (nine attempts / 315 s per `03_STATUS.md`); `DATA_STALE` auto-disarm once the budget is exhausted; a real production incident (duplicated user-channel subscription causing a hard `NotImplementedError` loop) was root-caused and fixed, including a reconciler/reconnect race-condition repair. All covered by dedicated tests. | `tests/test_p1_failure_drills.py::test_drill_ws_death_triggers_auto_reconnect`, `::test_drill_ws_death_survives_three_minute_outage_within_retry_budget`, `::test_drill_ws_death_reconnect_failure_goes_stale_after_full_budget`, `::test_drill_disconnect_reconnect_dedupes_to_one_order`; `docs/19_P2_RECONNECT_INCIDENT_2026-07-13.md`; `docs/03_STATUS.md` "Reconnect/reconciler race fix". | 
| | | | **Caveat:** the 2026-07-13 incident's root observation — "`reconcile_ready=true` is not proof the recurring reconciler task is alive" — is exactly the gap `21_WINDOW_STATE_CONTRACT.md` was built to close for the *window read-model*. Whether the underlying reconciler-liveness fix also landed for the reconciler task itself (not just its status presentation) was not independently re-verified in this pass. | |
| 9 | **Data-feed stall** (no disconnect, bars stop advancing) | HANDLED | `DATA_STALE reconnect_no_fresh_data` is detected distinctly from a hard disconnect, with a configurable, clamped restore deadline (default raised to 300 s, minimum 30 s). Ratified missed-decision policy (issue #45): on restart the kernel always replays missed bars to keep indicator state correct, but only acts on a recovered decision if it is still within the freshness bound — otherwise it is skipped and logged as an explained divergence, never acted on late. | `docs/03_STATUS.md` "Data-restore timeout build"; `tests/test_p1_failure_drills.py::test_drill_data_stale_auto_disarms`; issue #45 resolution item 1. | 
| 10 | **Operator error** (mis-click, stale UI, accidental live-mode) | PARTIAL | Baseline (always active): optimistic-concurrency `X-Confirm`/`state_version` guard rejects a stale confirm with HTTP 409, so a stale dashboard tab cannot silently re-trigger a state change; `KILLED` requires an explicit operator acknowledgement and is never auto-cleared; mainnet is hardcoded unreachable and `HL_LIVE_ACK` must stay unset; per-host distinct low-privilege agent wallets bound the blast radius of a key placed on the wrong machine. | `bridge/api/routes.py:228-234` (`X-Confirm`/`state_version`, HTTP 409 on mismatch); `bridge/engine/engine.py:242-243` (`"KILLED requires operator acknowledgement"`); `deploy/linux/SECURITY_BASELINE.md` §3 "Forbidden / unselected" row; `docs/17_DEPLOYMENT.md` §0. | 
| | | | **Gap:** the deeper risk-control layer that would catch an operator's bad *sizing/strategy* config — daily-loss and max-drawdown latches — is gated behind `durable_risk_controls_enabled()` (schema v7) and is therefore **inert on the deployed runtime** (same Central Finding pattern). A 2026-07-05 audit (`docs/audits/AUDIT_Cursor-Composer_2026-07-05.md`, finding F-27) flagged that `X-Confirm` nonce rotation/staleness was under-specified at the time; this pass did not re-verify whether the recommended 30 s nonce-age fix is the version currently live. | |

### Additional failure modes surfaced by the code/docs, beyond the ticket's base list

| # | Failure mode | Status | Mechanism(s) | Pointers |
|---|---|---|---|---|
| 11 | Duplicate / replayed order submission (idempotency under retry) | HANDLED | Deterministic `cloid = blake2s(action_id)` identity; reservation commits in one transaction before any broker I/O; a duplicate delivery of the same identity never creates a second submission. | `docs/23_ORDER_IDENTITY_CONTRACT.md`; chaos-drill D1-a, D3-d. | 
| 12 | Overfill / non-lot-quantity fill | HANDLED | Exact-integer-lot comparison with no epsilon; any overfill or non-lot quantity raises `LotQuantizationError`, latches `DISARMED`, and emits a durable integrity event rather than silently rounding. | `docs/25_PARTIAL_FILL_PROTECTION_CONTRACT.md` §5; chaos-drill D2-d. | 
| 13 | Stale/late evidence resurrecting a terminal order | HANDLED | Terminal states (`FILLED/CANCELED/REJECTED/EXPIRED`) accept no new lifecycle edges; late evidence is recorded but never rewrites a terminal outcome. | `docs/22_ORDER_STATE_CONTRACT.md` (cited at `22:140-142,170-172` in the chaos-drill matrix); chaos-drill D3-a, D3-c. | 
| 14 | Environment / dependency drift silently changing behavior mid-soak | PARTIAL (ratified plan, unbuilt) | Ticket #45 resolution item 3: Python version/lockfile/OS excluded from identity hashes (to not force a clock reset on routine patching), compensated by mandatory environment-lineage recording on every evidence artifact and a bit-identical golden-suite re-run required before evidence continues after any environment change. | Issue #45 resolution item 3 (amendment to `WP-P0-04`/`WP-P0-11`, not yet implemented). | 
| 15 | Evidence-store loss / corruption (ledger/DB loss, not process death) | PARTIAL (ratified plan, unbuilt) | Ratified standard: automated cross-copy backup (VPS ↔ owner PC), daily bulk / hourly critical-ledger sync while a watch window is active, a proven RED/GREEN restore drill required **before any forward clock may start**, protected classes never deleted. | Issue #38 resolution (OPS-A / `WP-P0-26`). | 
| | | | **Gap:** as of this research pass there is no evidence a cross-location backup exists for the currently-running bridge database — OPS-A has not been built. | |
| 16 | Fault-injection test harness execution (the drills themselves) | UNHANDLED (explicitly deferred by design) | `CHAOS_DRILLS_DESIGN.md` is a specification only: "Nothing in this package executes any drill... Drill execution, MockBroker fault-injection hooks, and any harness wiring: deferred to a later, separately gated increment." The *underlying* invariants it specifies are separately exercised by the hand-written `tests/test_p1_failure_drills.py` suite (rows 2, 8, 9 above), but the systematic MockBroker fault-injection harness against the full v9/partial-fill contract matrix does not exist yet. | `tools_v2/observability/CHAOS_DRILLS_DESIGN.md` (entire doc, esp. lines 6-14, 96-101). | |
| 17 | Continuous-check / CI regression protection | UNHANDLED (ratified plan, unbuilt) | The repository "currently has no functioning CI at all (no root workflows...)." A Phase-0 package (OPS-C / `WP-P0-27`) is planned to run the Bridge suite on every PR and page on a red master, but is not yet built. | `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md` WP-P0-27 (OPS-C) section, lines 518-528. | |

## Counts

Across all 17 rows catalogued (the ticket's 10 named modes + 7 additional modes surfaced
by the sources):

- **HANDLED: 5** — #8 network partition, #9 data-feed stall, #11 duplicate submission,
  #12 overfill/lot violation, #13 stale/late terminal-order evidence.
- **PARTIALLY HANDLED: 9** — #1 host death, #2 venue degradation, #3 credential loss/leak,
  #4 crash while ARMED, #5 partial fills during KILL/FLATTEN, #6 clock drift, #10 operator
  error, #14 environment drift, #15 evidence-store loss.
- **UNHANDLED: 3** — #7 disk full, #16 fault-injection harness execution, #17 CI.

Total: 5 + 9 + 3 = 17 rows.

Restricted to just the ten failure modes the ticket named: **HANDLED 2 / PARTIAL 7 /
UNHANDLED 1** (disk full).

## What this means for the owner, in plain terms

1. The bridge's newest and most sophisticated safety machinery — the exact-lot partial-fill
   protection, the kill-evidence episode ledger, full reconciliation, and the daily-loss/
   drawdown latches — is real, well-tested code that **is not currently switched on**. The
   deployed unit runs on the older, coarser schema. Anyone assuming "kill switch = flattens
   the position" should re-check that assumption against the currently deployed schema
   before relying on it.
2. The two work packages that close the largest structural gaps in this catalog — OPS-A
   (backup/restore + dead-man watchdog + NTP drift-alarm) and OPS-C (CI) — are both ratified
   *decisions*, already scoped as Phase-0 packages, but neither has been built yet.
3. Disk-full is the one failure mode with **no ratified plan at all**, not just an unbuilt
   one — it does not appear anywhere in the contracts, the tests, or the OPS-A scope as
   currently written.

## Suggested next steps (for a follow-up ticket, not acted on here)

1. Confirm — by an owner-authorized, gated host check (out of scope for this research
   ticket) — the actual `meta.schema_version` on the currently-deployed bridge database, to
   turn the Central Finding from a documentation-derived inference into a verified fact.
2. When OPS-A (`WP-P0-26`) is scoped for build, add an explicit disk-space/ENOSPC failure
   mode to its acceptance gate — it is currently absent from both the code and the plan.
3. Before any schema-activation gate for v5–v9 is opened, re-surface this catalog's Central
   Finding as a pre-condition check, since it changes what KILL actually does at runtime.
