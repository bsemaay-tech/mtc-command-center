# WP-P0-28 VEN-A — Account Binding and Virtual-Books Fallback Specification

**Status:** Q6 binding specification · documentation half only · T2

**Decision authority:** Q6/#40 is already decided and is not reopened here.

**Hard edge:** this specification and the venue verification record must be accepted **before `WP-V2B-03` starts**.

**Authorization boundary:** this document authorizes no implementation, account access, credential, subaccount, wallet, transfer, testnet action, mainnet action, or order.

## 1. Binding decision

The preferred binding unit is one **risk bucket**. Each risk bucket maps to:

1. one Hyperliquid subaccount;
2. one dedicated agent wallet used only for that subaccount/risk bucket; and
3. one worker identity at a time, except that the accepted hybrid-isolation design may assign multiple strategies to a bucket only through its owning worker/supervisor contract.

Per-strategy subaccounts are permitted only where accepted capacity remains after the required risk-bucket bindings. They are an optimization within Q6, not a replacement for the risk-bucket default.

The actual number of available subaccounts is **UNKNOWN** until the excluded owner-action `G6` / T0 eligibility read is separately authorized and completed. No implementation may assume that the published 10→50 capacity is available to this account. The preferred topology remains the decision; virtual books remain its specified fallback.

## 2. Binding registry contract

Each active binding is an immutable, versioned record containing at least:

| Field | Rule |
|---|---|
| `binding_id` | Globally unique, never reused. |
| `binding_mode` | Exactly `SUBACCOUNT` or `VIRTUAL_BOOK`. No implicit default. |
| `risk_bucket_id` | Required; points to the versioned bucket policy consumed by `WP-V2B-01`. |
| `strategy_id` | Optional refinement when capacity allows a per-strategy binding. |
| `worker_id` | Required active worker identity; never a credential. |
| `venue_account_address` | Public acting-account address used for venue reads and reconciliation. |
| `subaccount_address` | Required for `SUBACCOUNT`; absent for a virtual book inside the shared account. |
| `virtual_book_id` | Required for `VIRTUAL_BOOK`; absent for `SUBACCOUNT`. |
| `agent_wallet_address` | Public signer identity only. A secret/private key is forbidden from the registry, logs, evidence, docs, and prompts. |
| `agent_expiry_at` | Explicit timestamp. It must not rely on an undocumented default and must stay within the venue's verified 180-day custom-expiry maximum. The owner-approved operational rotation interval remains WP-P0-29 policy. |
| `allowlist_version` | Exact version of the per-bucket instrument allowlist. |
| `instrument_metadata_version` | Exact frozen venue metadata version used to validate the next order. |
| `deployment_identity_hash` | Binds the mapping to the admitted deployment identity. |
| `effective_at`, `retired_at`, `predecessor_binding_id` | Lifecycle and lineage. Mutation retires the binding and creates a successor. |

The registry contains identifiers and public addresses only. Credential provisioning and storage belong to the separately gated credential path; consumers verify presence/permissions without reading or printing values.

## 3. Preferred `SUBACCOUNT` mode

An active `SUBACCOUNT` binding MUST satisfy all of these conditions:

- accepted evidence establishes an available subaccount slot; no slot is inferred from the public threshold alone;
- the subaccount is bound to exactly one risk bucket, or to one strategy within that bucket where separately accepted capacity permits;
- the agent wallet is dedicated to that binding and is not shared with another concurrently active subaccount, virtual book, risk bucket, or worker;
- the agent expiry is explicit and monitored; a default expiry is never assumed;
- all venue reads query the actual master/subaccount address, never the agent-wallet address;
- the worker store and supervisor registry carry the same binding identity;
- changing subaccount, signer, risk bucket, allowlist, or binding mode is a material identity change: retire, create a successor, and apply the no-orphan disposition rule to any open exposure.

Subaccounts are treated as independent clearinghouse accounts by the venue, but they still share master-level governance and IP/WebSocket capacity. This spec therefore does not claim independent IP capacity, independent custody, or an agent-withdrawal safety boundary.

## 4. Fallback activation

`VIRTUAL_BOOK` is the specified fallback on exactly the decided triggers:

1. **volume-gate ineligibility** — accepted evidence says the required subaccount slot is unavailable;
2. **cap exhaustion** — accepted bindings consume the available subaccount capacity; or
3. **venue restriction** — a documented or observed venue rule prevents the required subaccount or dedicated-agent mapping.

An UNKNOWN is not silently converted into eligibility. Before the excluded account read, the system may design and validate virtual books, but it may instantiate no real binding under this document.

Fallback selection is explicit, versioned, logged, and identity-bound. It is never selected ad hoc during an incident. Switching an active unit between `SUBACCOUNT` and `VIRTUAL_BOOK` retires the old binding; if exposure is open, `WP-V2B-10`'s closed no-orphan menu applies before the successor may take new risk.

## 5. Virtual-book state

A virtual book is an internal accounting partition inside one venue account. It is **not** a Hyperliquid primitive and provides no venue-side isolation. Each book keeps, per symbol:

- signed position quantity and average entry basis;
- intended and Guardian-authorized quantity;
- durable order identities, remaining quantity, protection role, and reservations;
- every mapped fill, fee, realized P&L, and funding allocation;
- margin mode and leverage expectation;
- allowlist and instrument-metadata versions;
- reconciliation state, last accepted venue snapshot, and evidence-window identity.

Every order and fill belongs to exactly one virtual book through a durable identity. Unmapped or multiply mapped venue activity is a reconciliation break, never an allocation guess.

## 6. Same-symbol and opposing-intent rule

Hyperliquid's current public API is one-way/no-hedge and reports one signed size. Virtual books therefore obey these fail-closed rules:

1. Multiple books may carry the same symbol only while every non-zero book quantity has the **same sign** and every fill remains uniquely attributable.
2. An intent that would create an opposite-signed book position while another book for that symbol is non-zero is rejected as `VBOOK_OPPOSING_SYMBOL`.
3. A book may not reverse through zero in one action. It must close to zero, reconcile, release its reservations, and may open the opposite side only when every book for that symbol is flat.
4. A reducing order may reduce only its originating book. Aggregate reduce-only reservations across books may never exceed the reconciled venue-net quantity.
5. Because same-asset cross+isolated coexistence is UNKNOWN, every book sharing a symbol must use the same accepted margin mode and leverage expectation. A mismatch rejects before order construction.

These rules prevent an opposing book from silently closing, transferring, or disguising another book's exposure through venue netting.

## 7. Venue-net decomposition and accounting

For each symbol `s` and reconciliation instant `t`:

```text
venue_signed_qty(s,t) = sum(book_signed_qty(book,s,t))
```

All non-zero terms on the right must have one sign. The following allocation rules are deterministic:

- **Orders and partial fills:** attributed to the originating book's durable order identity. A partial fill changes only that book.
- **Fees:** attributed to the book whose fill generated the fee.
- **Funding:** allocated across non-zero same-symbol books by their absolute position notional at the funding timestamp. Rounding uses the venue precision; the deterministic remainder goes to the lexicographically first `virtual_book_id` and is recorded.
- **Liquidation or venue-forced reduction:** allocated pro rata by absolute same-symbol quantity immediately before the event, recorded as a venue-forced event, and causes the affected account/symbol to block new risk pending reconciliation. It is never represented as a strategy exit.
- **Transfers or unexplained balance changes:** remain account-level unallocated items until explicitly reconciled; they are never assigned to a profitable or losing book by convenience.

The sum of book cash effects plus explicitly recorded account-level items must reproduce the venue account change for the evidence window.

## 8. Reconciliation contract

### `SUBACCOUNT` binding

`WP-V2A-02` reconciles the worker store against the bound subaccount address. `WP-V2B-03` then aggregates the accepted per-binding results. No other bucket's state may repair a failed binding.

### `VIRTUAL_BOOK` binding

`WP-V2B-03` owns the portfolio-wide reconciliation and MUST prove, per symbol and evidence window:

- book signed quantities sum to the venue signed quantity;
- every owned venue order maps to one book and every recorded live book order exists at the venue;
- every venue fill maps exactly once, including partial fills;
- fees, funding, realized P&L, and account-level residuals reproduce the venue account delta;
- reduce-only reservations do not exceed either their book quantity or the venue-net quantity;
- all books for a shared symbol agree on sign, margin mode, leverage expectation, allowlist version, and current instrument metadata;
- restart reconstruction from durable stores reaches the same result before new risk is permitted.

Any mismatch is a machine-readable reconciliation break. It blocks new risk for the affected binding/symbol, preserves valid exits and protection, alerts through the accepted operations path, and requires evidence-backed reconciliation. It never auto-reassigns a fill, auto-transfers position ownership, auto-KILLs, or auto-FLATTENs.

## 9. Instrument universe policy

1. Every risk bucket has a **versioned symbol allowlist**. No symbol is allowed by implication or by presence in venue metadata.
2. `WP-V2B-01` is the Guardian consumer: it rejects any intent whose symbol is absent from the bound bucket's allowlist.
3. Risk-increasing allowlist edits require owner authorization, occur atomically at a bar boundary between evidence windows, are logged, and create the material identity consequence already required by the bucket risk-split rule. Risk-reducing emergency tightening may occur through the accepted authenticated step-up path and is always logged.
4. Delisting while a position is open is an identity-ending event. `WP-V2B-10` applies its closed no-orphan menu; absent an explicit choice, exits-only run-off is automatic and no new entries are allowed.
5. Venue instrument metadata is refreshed before the next order. The exact metadata version is frozen into the binding/order evidence.
6. A tick-size, size-decimal, price-decimal, minimum-notional, margin-mode, delisting, or other contract-spec mismatch refuses the order fail-closed. No rounding or stale fallback is invented to make it pass.

Named consumers of the universe policy:

| Consumer | Required use |
|---|---|
| `WP-P0-12` — Kernel `CORRECTED_VNEXT` | Kernel consumer row: uses frozen instrument metadata; research/runtime intent generation cannot silently substitute a different venue specification. |
| `WP-V2B-01` — Portfolio Guardian and Risk Buckets | Guardian consumer row: enforces the versioned per-bucket symbol allowlist and risk-split edit rule. |
| `WP-V2A-05` — Bridge intent seam | Execution-boundary consumer: refuses stale or mismatched instrument metadata before an order-shaped action exists. |
| `WP-V2B-03` — Multi-worker supervisor | Reconciliation consumer: checks binding, allowlist, metadata, book, store, and venue truth together. This package may not start until this spec is accepted. |
| `WP-V2B-10` — Emergency operations | Lifecycle consumer: handles delisting-with-open-position through the no-orphan disposition menu. |

## 10. Package acceptance checks

This documentation half is complete only if the accepting reviewer confirms:

- Q6 remains settled and no account topology is instantiated;
- the preferred subaccount binding and all three fallback triggers are explicit;
- no secret-bearing field exists in the registry;
- the same-symbol rule prevents opposing virtual exposure and implicit ownership transfer;
- the per-book-to-venue reconciliation invariants cover partial fills, fees, funding, forced reductions, restarts, and unexplained activity;
- `WP-V2B-03` is named as the hard-edge consumer;
- the kernel and Guardian consumers of the universe policy are named;
- account eligibility remains UNKNOWN / EXCLUDED and no authenticated act occurred.

Rollback is documentary: a future accepted record may supersede this spec, but this version is never edited away.
