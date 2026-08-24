# WP-P0-25 Pointer Re-verification

**Verified:** 2026-08-25

**Worktree:** `C:\WPP025_20260825`

**Branch:** `feature/wp-p0-25-broker-boundary-20260825`

**Fresh HEAD:** `4691a9dd843f05948b271a88972c94a3bdce13a7`

**Planning candidate used by the package:** `01e0725890e456d079bca8967625ccb09c66b889`

The planning candidate is an ancestor of fresh HEAD. A scoped `git diff --stat` from the planning candidate to fresh HEAD was empty for `base.py`, `hyperliquid.py`, `mock.py`, and contracts 25/26. The candidate anchors therefore remain current, but every pointer below was independently read and re-located at fresh HEAD rather than copied forward.

## 1. Old pointer to fresh pointer

| Artefact | Original 2026-08-22 pointer recorded as stale | Planning-candidate pointer in WP-P0-25 | Fresh pointer at `4691a9dd` | Fresh evidence |
|---|---:|---:|---:|---|
| `Broker(Protocol)` | `base.py:154` | `base.py:156` | **`base.py:156`** | Complete declaration `:156-212` |
| `PartialRecoveryUnavailable` | `base.py:222` | `base.py:226` | **`base.py:226`** | Default reason code at `:229`; class ends `:231` |
| `PartialRecoveryBroker(Protocol)` | `base.py:230` | `base.py:234` | **`base.py:234`** | Complete declaration `:234-275` (last method body ellipsis at `:275`; the individual `flatten_reduce_only` method remains `:271-274`) |
| `FullReconciliationUnavailable` | `base.py:285` | `base.py:339` | **`base.py:339`** | Default reason code at `:342`; class ends `:344` |
| `FullReconciliationBroker(Protocol)` | `base.py:293` | `base.py:347` | **`base.py:347`** | Complete declaration `:347-378` |
| `FullReconciliationBroker.funding_evidence` | `base.py:320-323` | `base.py:374-378` | **`base.py:374-378`** | Fifth method, after `fills_evidence` |
| `HyperliquidBroker` | `hyperliquid.py:105` | `hyperliquid.py:115` | **`hyperliquid.py:115`** | Concrete class declaration |
| `MockBroker` | `mock.py:68` | `mock.py:70` | **`mock.py:70`** | Concrete class declaration |

The stale and planning-candidate values are recorded in the canonical brief and plan (`MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:205`, `:623-636`; `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:564-572`).

## 2. Fresh method-set evidence

An AST inventory at fresh HEAD found no missing implementation method in either concrete broker.

| Protocol | Complete fresh declaration set | Hyperliquid implementation anchors | Mock implementation anchors |
|---|---|---|---|
| `Broker` | `connect:159`; `account:162`; `positions:165`; `open_orders:168`; `historical_bars:171`; `subscribe_bars:174`; `subscribe_user_events:177`; `planned_cloids:180`; `place_bracket:183`; `submission_recovery_evidence:188`; `modify_stop:193`; `cancel:196`; `cancel_all:199`; `flatten:202`; `reprotect_position:205` | `152,212,247,259,265,284,297,360,370,630,856,893,899,904,924` | `143,146,153,156,180,185,204,207,216,276,324,332,338,344,352` |
| `PartialRecoveryBroker` | `lot_unit:243`; `symbol_snapshot:247`; `query_order:251`; `cancel_order_by_cloid:255`; `place_protective_stop:259`; `flatten_reduce_only:271` | `975,1040,1171,1348,1418,1466` | `377,394,457,499,571,618` |
| `FullReconciliationBroker` | `lot_unit:356`; `portfolio_evidence:360`; `open_orders_evidence:364`; `fills_evidence:368`; **`funding_evidence:374`** | `975,1597,1780,1880,1894` | `377,907,989,1050,1147` |

All source paths in this table are under `IBKR_PAPER_BRIDGE/bridge/broker/`.

## 3. Fresh contract and test anchors

| Package input | Fresh anchor | Evidence |
|---|---:|---|
| TS-P1-004 contract | `IBKR_PAPER_BRIDGE/docs/25_PARTIAL_FILL_PROTECTION_CONTRACT.md:1` | Boundary modules and named tests `:3-15`; separate protocol and fail-closed absence `:340-348` |
| TS-P1-004 primary regression | `IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py:900-911` | Missing recovery surface produces `UNPROTECTED_ABORT` and zero mutation |
| TS-P1-005 contract | `IBKR_PAPER_BRIDGE/docs/26_FULL_RECONCILIATION_CONTRACT.md:1` | Protocol/unavailable behavior `:455-460`; test inventory `:479-482` |
| TS-P1-005 bounded surface test | `IBKR_PAPER_BRIDGE/tests/test_reconciliation.py:557-572` | The four evidence reads include `funding_evidence` |
| Full-reconciler feature detection | `IBKR_PAPER_BRIDGE/bridge/engine/reconcile.py:486-494` | Exact five-method surface includes `funding_evidence` |
| Partial-recovery feature detection | `IBKR_PAPER_BRIDGE/bridge/engine/orders.py:79-86`, `:3754-3759` | Exact six-method surface, callable structural detection |

## 4. Fresh planning-section anchors

| Requested semantic pointer | Fresh anchor |
|---|---:|
| F-9 / F-9a | `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:619-640` |
| Brief section 4.1, layer A | `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:853-865` |
| Brief section 5.4 protection semantics | `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:1049-1108` |
| Brief section 17.5 | `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:3021-3029` |
| WP-P0-25 full package contract | `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:564-575` |
| V2A account snapshot | `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:707-715` |
| V2A Bridge intent seam | `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:717-725` |
| V2A protection semantics | `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:727-734` |
| V5 broker expansion | `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:1040-1042` |
| O-17 minimum-code / OSS-first requirement | `REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:140` |

## 5. Verification limits

These are repository-source pointers at fresh HEAD. They do not establish deployed runtime version, configuration, schema, or behavior; those remain `UNVERIFIED` pending G9 (`MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:636`; plan `:567`). No host, network, Docker, WSL, broker, or exchange was contacted.
