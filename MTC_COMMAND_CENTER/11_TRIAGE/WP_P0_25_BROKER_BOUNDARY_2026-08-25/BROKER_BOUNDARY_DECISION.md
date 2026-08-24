# WP-P0-25 Broker-Boundary Decision

**Date:** 2026-08-25

**Audit tier / protected gate:** T0 / G3, decision-only

**Decision:** **Reuse the existing structural `Protocol` family as-is. Do not rename it, do not add a parallel boundary, and do not add methods to the three accepted protocols in this package.**

This is an architecture decision, not implementation authority. Any V2A or V5 code remains separately gated, and WP-V5-01 remains the implementation carrier for a future IBKR adapter (`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:564-575`, `:1040-1042`).

## 1. Starting point: the boundary already exists

The starting point is the structural `typing.Protocol` seam in `IBKR_PAPER_BRIDGE/bridge/broker/base.py`, not a new adapter abstraction. The family consists of the broad `Broker` protocol and two deliberately separate opt-in capability protocols, `PartialRecoveryBroker` and `FullReconciliationBroker` (`IBKR_PAPER_BRIDGE/bridge/broker/base.py:156-212`, `:216-222`, `:234-274`, `:329-335`, `:347-378`). `HyperliquidBroker` and `MockBroker` structurally implement every method in all three protocols (`IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py:115`, `IBKR_PAPER_BRIDGE/bridge/broker/mock.py:70`; implementation anchors in section 2).

This resolves the apparent F-9/F-9a conflict: F-9 describes the empty `07_ADAPTERS` scaffolding, while F-9a records the working Bridge boundary (`MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:619-640`). Layer A already defines that family as the broker-adapter boundary rather than a new protocol (`MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:853-865`).

## 2. Complete existing method inventory

### `Broker`

Declared at `IBKR_PAPER_BRIDGE/bridge/broker/base.py:156`. Its complete method set is:

| Method | Declaration |
|---|---:|
| `connect` | `base.py:159` |
| `account` | `base.py:162` |
| `positions` | `base.py:165` |
| `open_orders` | `base.py:168` |
| `historical_bars` | `base.py:171` |
| `subscribe_bars` | `base.py:174` |
| `subscribe_user_events` | `base.py:177` |
| `planned_cloids` | `base.py:180` |
| `place_bracket` | `base.py:183-186` |
| `submission_recovery_evidence` | `base.py:188-191` |
| `modify_stop` | `base.py:193` |
| `cancel` | `base.py:196` |
| `cancel_all` | `base.py:199` |
| `flatten` | `base.py:202` |
| `reprotect_position` | `base.py:205-212` |

Concrete implementation anchors, in the same order, are `hyperliquid.py:152,212,247,259,265,284,297,360,370,630,856,893,899,904,924` and `mock.py:143,146,153,156,180,185,204,207,216,276,324,332,338,344,352`.

### `PartialRecoveryBroker`

Declared at `IBKR_PAPER_BRIDGE/bridge/broker/base.py:234`. Its complete method set is:

| Method | Declaration | Hyperliquid | Mock |
|---|---:|---:|---:|
| `lot_unit` | `base.py:243` | `hyperliquid.py:975` | `mock.py:377` |
| `symbol_snapshot` | `base.py:247` | `hyperliquid.py:1040` | `mock.py:394` |
| `query_order` | `base.py:251` | `hyperliquid.py:1171` | `mock.py:457` |
| `cancel_order_by_cloid` | `base.py:255` | `hyperliquid.py:1348` | `mock.py:499` |
| `place_protective_stop` | `base.py:259-268` | `hyperliquid.py:1418` | `mock.py:571` |
| `flatten_reduce_only` | `base.py:271-274` | `hyperliquid.py:1466` | `mock.py:618` |

The capability is feature-detected from exactly these six callable methods (`IBKR_PAPER_BRIDGE/bridge/engine/orders.py:79-86`, `:3754-3759`). Missing capability fails closed to `UNPROTECTED_ABORT` with no broker mutation, as the accepted TS-P1-004 contract and regression test require (`IBKR_PAPER_BRIDGE/docs/25_PARTIAL_FILL_PROTECTION_CONTRACT.md:340-348`, `IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py:900-911`).

### `FullReconciliationBroker`

Declared at `IBKR_PAPER_BRIDGE/bridge/broker/base.py:347`. Its complete method set is:

| Method | Declaration | Hyperliquid | Mock |
|---|---:|---:|---:|
| `lot_unit` | `base.py:356` | `hyperliquid.py:975` | `mock.py:377` |
| `portfolio_evidence` | `base.py:360` | `hyperliquid.py:1597` | `mock.py:907` |
| `open_orders_evidence` | `base.py:364` | `hyperliquid.py:1780` | `mock.py:989` |
| `fills_evidence` | `base.py:368-371` | `hyperliquid.py:1880` | `mock.py:1050` |
| **`funding_evidence`** | **`base.py:374-378`** | **`hyperliquid.py:1894`** | **`mock.py:1147`** |

`funding_evidence` is therefore present in the protocol and both concrete implementations. The full reconciler checks exactly these five methods and maps a missing one to the non-accepting `FULL_RECONCILE_API_UNAVAILABLE` result (`IBKR_PAPER_BRIDGE/bridge/engine/reconcile.py:277-289`, `:486-494`). The nominal bounded-read test also calls all four evidence methods, including `funding_evidence` (`IBKR_PAPER_BRIDGE/tests/test_reconciliation.py:557-572`).

### Unavailable types and reason codes

| Type | Location | Default machine-readable reason code |
|---|---:|---|
| `PartialRecoveryUnavailable` | `base.py:226-231` | `PARTIAL_RECOVERY_API_UNAVAILABLE` (`base.py:229`) |
| `FullReconciliationUnavailable` | `base.py:339-344` | `FULL_RECONCILE_API_UNAVAILABLE` (`base.py:342`) |

The full-reconciliation contract expressly treats the latter as a non-accepting attempt (`IBKR_PAPER_BRIDGE/docs/26_FULL_RECONCILIATION_CONTRACT.md:455-460`).

## 3. The three options, priced against minimum-code and OSS-first O-17

O-17 prefers libraries and narrow adapters over importing a whole platform, while retaining custom code where local risk, execution safety, reconciliation, and operator workflow encode owner policy (`REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:140`; `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2643-2645`).

| Option | Minimum-code price | OSS-first price | Contract and operational price | Verdict |
|---|---|---|---|---|
| **Reuse as-is** | **Lowest.** Zero broker-boundary code or rename in WP-P0-25. V2A composes existing typed evidence and protection primitives; V5 wraps a selected OSS client behind the same narrow family. | Best fit. An OSS venue client remains an implementation detail rather than exporting its object model into Bridge consumers. | TS-P1-004/005 protocols, tests, reason codes, fail-closed feature detection, and Hyperliquid/Mock implementations remain unchanged. | **Chosen.** |
| **Extend** | Moderate. Even an additive capability would require at least the protocol declaration, Hyperliquid and Mock implementations, a feature-detecting consumer, fixtures/tests, and contract documentation. | Still compatible if the addition is a narrow capability, but speculative additions before a reproduced gap violate minimum-code. | Additive extension can avoid breaking old fakes, but it creates another accepted surface and another parity obligation for every venue. | Reject now. Reconsider only from a separately authorized package with a demonstrated missing primitive. |
| **Deliberately replace or rename** | Highest. Every adapter, consumer, fake, contract, test, reason code, documentation pointer, and migration/compatibility path must move together; a transition period risks two boundaries. | Weakest fit. Replacing the local safety seam with a platform ontology risks importing a whole framework or maintaining a translation layer around local safety semantics. | It would disturb accepted TS-P1-004/005 behavior and require explicit compatibility and evidence migration. There is no reproduced defect that justifies that cost. | Reject. |

## 4. Exact V2A mapping onto the chosen boundary

The broker boundary owns venue mechanics and typed venue evidence. Snapshot identity, bucket policy, allocation policy, sizing, and authorization remain outside it, consistent with the layer ownership table (`MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:855-865`).

| V2A need | Existing broker surface used as-is | Ownership outside the broker | Fail-closed condition |
|---|---|---|---|
| Immutable account snapshot for WP-V2A-04 | `FullReconciliationBroker.portfolio_evidence()` (`base.py:360-362`), whose `PortfolioEvidence` contains positions, balances, and margin from one account observation (`bridge/engine/types.py:1135-1145`). Each component already carries status, observation time, exactness, completeness, and a reason code (`bridge/engine/types.py:1061-1090`). | The V2A Account Snapshot Service/Decision Orchestrator constructs and content-hashes the immutable snapshot, binds `snapshot_id`, `snapshot_taken_at`, deadline, bucket/exposure state, and allocation-policy identity. The adapter does not invent these account-policy fields (`MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:1082-1089`; `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:707-715`). | Any component not accepted, or any mismatch/staleness/reference divergence, rejects with no order (`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:707-715`). |
| Legacy account read | `Broker.account()` remains unchanged (`base.py:162`). Its current value has only `equity`, `available_margin`, and `withdrawable` (`bridge/engine/types.py:60-63`). | It is not promoted into the canonical V2A immutable snapshot authority; the snapshot service uses evidence-carrying input above. | A legacy three-float read cannot satisfy snapshot identity by assertion. |
| Authorized-intent submission seam for WP-V2A-05 | `Broker.planned_cloids`, `place_bracket`, and `submission_recovery_evidence` (`base.py:180-191`). | Bridge maps an already authorized `OrderIntent` to the existing `OrderPlan`; the adapter executes venue mechanics and returns typed submission evidence. It does not compute or alter quantity (`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:717-725`). | A Bridge-originated quantity in the presence of an authorized intent is rejected by WP-V2A-05's required fence (`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:724`). |
| Native reduce-only stop semantics for WP-V2A-06 | `PartialRecoveryBroker.lot_unit`, `symbol_snapshot`, `query_order`, `cancel_order_by_cloid`, and `place_protective_stop` (`base.py:243-268`). Existing `Broker.modify_stop` remains available at `base.py:193`, but acceptance must come from fresh typed evidence, not its `None` return. | WP-V2A-06 owns the local emulator/replay semantics and D026 proof for placement, amendment, cancellation, process death, and re-attachment. It does not add venue contact (`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:727-734`). | Missing capability, inexact snapshot, unknown outcome, or inability to verify the one exact reduce-only stop is non-accepting. No untyped return is treated as proof. |
| Local zero-venue proof | `MockBroker` is the existing local concrete implementation (`bridge/broker/mock.py:70`) and implements all three method sets (section 2). | The emulator/replay harness remains V2A-owned; real-venue survival remains WP-V2B-07, not this decision (`MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:1102-1104`). | Any reachable credential or venue path fails WP-V2A-06 acceptance (`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:733-734`). |

This mapping requires no new broker method. If implementation evidence later proves that the existing typed primitives cannot express one required operation safely, the only permitted reconsideration is a separately authorized **additive, narrow opt-in capability** in the existing family. It must not enlarge `Broker` speculatively or create a parallel top-level boundary.

## 5. Exact V5 mapping onto the chosen boundary

WP-V5-01 implements a future IBKR concrete adapter behind the same family. It must implement `Broker`; it opts into the complete `PartialRecoveryBroker` and `FullReconciliationBroker` capabilities only where the venue/client can meet their evidence and fail-closed contracts. A missing opt-in surface stays explicitly unavailable rather than silently absent, using the existing capability detection and reason-code semantics (`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:1040`).

WP-V5-02 owns the genuinely new equity concerns—calendar, sessions, corporate actions, and halts—rather than pretending they are generic adapter parity (`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:1041`; `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:3021-3029`). WP-V5-03 consumes canonical, reconciled portfolio truth across venues and must not merge venue-specific risk semantics (`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:1042`). An OSS IBKR client may therefore be wrapped behind this boundary, but its SDK types and risk assumptions do not become Bridge contracts, matching O-17 (`REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:140`).

No IBKR class, protocol, method, adapter, SDK selection, or code is authorized or created by this decision.

## 6. Consequences for TS-P1-004 and TS-P1-005

- TS-P1-004's separate `PartialRecoveryBroker` surface, its fail-closed feature detection, and all named test suites remain unchanged (`IBKR_PAPER_BRIDGE/docs/25_PARTIAL_FILL_PROTECTION_CONTRACT.md:3-15`, `:340-348`).
- TS-P1-005's separate read-only `FullReconciliationBroker`, all five methods including `funding_evidence`, the `FullReconciliationUnavailable` behavior, and all named test suites remain unchanged (`IBKR_PAPER_BRIDGE/docs/26_FULL_RECONCILIATION_CONTRACT.md:455-482`).
- `PARTIAL_RECOVERY_API_UNAVAILABLE` and `FULL_RECONCILE_API_UNAVAILABLE` remain the canonical default unavailability reason codes (`base.py:226-231`, `:339-344`). No alias, translation, deprecation, or migration is introduced.
- No existing test is deleted, renamed, weakened, or reclassified. A future venue implementation inherits the applicable existing conformance surface and must add venue-specific tests without changing the accepted behavior.

The work-package plan calls TS-P1-004/005 accepted inputs (`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:566`). The older TS-P1-004 document still self-labels its implementation `PROPOSED` at `docs/25:17-18`; this lane does not rewrite that out-of-scope status line and does not use it to weaken the plan's explicit accepted-input contract.

## 7. Nonexistent-protocol sweep

A repository-wide exact-token sweep found **eight** pre-decision occurrences of `BrokerAdapter`, all in three planning documents:

- `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:205,625,638,3025`
- `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:572,1040`
- `REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:137,140`

Every occurrence is corrective, historical, or the acceptance rule itself: none declares, imports, or promises a protocol by that name. The current positive architecture names `Broker`, `PartialRecoveryBroker`, and `FullReconciliationBroker` (`MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:623-640`, `:853-865`; plan `:1040`). This decision creates no protocol with the nonexistent name and does not use that name for the chosen boundary.

Broader case-insensitive prose such as “broker adapter” describes the layer or a concrete adapter, not a Python protocol. Those ordinary-language references do not conflict with this decision.

## 8. Decision boundary and reversal

This record changes no runtime, trading behavior, Pine logic, parity logic, schema, broker, adapter, reason code, or test. Reversal requires a later superseding owner decision; implementation requires its own package authorization and T0 gates. Deployed runtime identity and behavior remain `UNVERIFIED` pending G9, exactly as the planning source cautions (`MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:636`; `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:567`).
