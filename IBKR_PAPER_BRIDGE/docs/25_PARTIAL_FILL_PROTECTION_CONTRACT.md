# 25 — Partial-Fill Protect-or-Flatten Contract (TS-P1-004)

Modules: `bridge/engine/types.py` (`PartialProtectionState`,
`PARTIAL_STATE_TRANSITIONS`, `LotUnit`/`quantize_lots`, `ActionOutcome`,
typed broker results), `bridge/broker/base.py` (`PartialRecoveryBroker`),
`bridge/broker/hyperliquid.py` + `bridge/broker/mock.py` (adapters),
`bridge/engine/orders.py` (symbol lock, detection, state machine, shared
protection predicate), `bridge/engine/engine.py` (ARM / ordinary-path
participation), `bridge/store/db.py` (schema v5 ledger).
Tests: `tests/test_partial_fill_protection.py` plus the TS-P1-004 blocks in
`tests/test_order_state.py`, `tests/test_store.py`,
`tests/test_mock_broker.py`, `tests/test_hyperliquid_broker.py`,
`tests/test_engine_dryrun.py`.
Governing: Gate-1 contract `TS_P1_004_GATE1_FINAL.md` (all seven owner
decisions accepted), ADR-0022/0023.

**Status: PROPOSED** — implemented and self-QA'd offline; pending independent
audit and owner acceptance. Not deployed; see §9.

## 1. Problem

Before this task an owned entry order that filled only partially left the
bridge in a silently unsafe state: the protective stop was still sized to the
*planned* quantity, `reconcile()` accepted **any** matched `SL` order as
protection for a symbol regardless of its size, side, or reduce-only flag, and
there was no durable record that a partial had ever happened. A 1.0-lot stop
therefore "protected" a 2.0-lot position, and a restart lost the fact entirely.

## 2. Primary safety contract

For an unambiguously owned entry order with planned quantity `Q`, authoritative
entry filled quantity `f`, and authoritative live net position `q`, where
`0 < f < Q`:

1. The first partial observation and its **fixed** deadline are persisted
   before any broker mutation, and the application is latched `DISARMED`.
2. ARM and new entries are blocked; strategy trailing/close/flip for that
   symbol is suppressed. Only the recovery state machine may mutate owned
   orders or the position.
3. A bounded, complete symbol snapshot is obtained: the owned entry by stable
   cloid, the authoritative position, and the live orders. Incomplete, stale,
   conflicting or ambiguous evidence never counts as safe.
4. Exactly one exact-quantity, correct-side, owned, reduce-only stop-loss is
   established and **verified** for the current authoritative position.
   Two live owned stops never qualify, even when both are exact. Once the
   deterministic current-generation replacement is verified, every other
   lineage-owned live SL is cancelled under a reserved `CANCEL_PROTECTION`
   identity and proved terminal/absent by direct query before recovery may
   continue. Foreign, mixed, ambiguous, or unverified extras remain
   observe-only. Take-profit is optional and never counts as the safety stop.
5. The entry remainder is cancelled by its existing stable cloid, then proven
   terminal by direct query. A transport success alone is not proof.
6. After cancellation the symbol is re-snapshotted. Any authoritative quantity
   change on the accepted entry lineage is processed before the partial-only
   guard. This includes a fill reaching exactly `Q` after
   `PROTECTED_PARTIAL` or `SAFE_FLAT`; it opens a new generation and re-runs
   recovery **without** resetting the original deadline.
7. `PROTECTED_PARTIAL` requires: entry terminal, position nonzero, exact
   verified stop coverage, and no unresolved owned action.
   `SAFE_FLAT` requires: entry terminal, position authoritatively zero, and no
   surviving live owned entry/SL/TP order.
8. If the protected outcome cannot be proved by the **10.0 s** primary
   deadline, an owned reduce-only flatten action is reserved and submitted.
   Immediately before every new flatten reservation/send, recovery takes a
   fresh snapshot and reclassifies provenance while holding the symbol lock;
   only the exact proven `OWNED` quantity may be flattened. Flatten verification
   has its own **5.0 s** budget. An unknown flatten outcome remains query-only
   and can never become `SAFE_FLAT` from a zero position alone.
9. Any unresolved or ambiguous action/evidence ends in durable
   `UNPROTECTED_ABORT` with the application `DISARMED`, new risk blocked, an
   explicit `ERROR` event, and no false safe/green claim.
10. A later authoritative nonzero owned position after `SAFE_FLAT` opens a new
    recovery generation without resetting the original 10-second deadline;
    mixed/ambiguous exposure opens the new generation directly into persistent
    abort with zero broker mutation. Queued fill ingestion, periodic reconcile,
    and startup legacy scanning all enforce this rule.

## 3. Precedence and ownership

| Rule | Implementation |
| --- | --- |
| **TS-P1-003 quarantine dominates** | Detection and startup scan open no recovery while quarantined; every recovery cycle re-checks after awaited evidence and returns before any later reservation or mutation. It **defers** rather than creating a competing abort. |
| **Foreign/ambiguous state is observe-only** | `_classify` returns `FOREIGN`/`MIXED`/`AMBIGUOUS` before any reservation; the run aborts with zero broker calls. |
| **Risk authority is independent** | `engine.arm()` refuses while any recovery is non-terminal or any `UNPROTECTED_ABORT` is durable; `_app_state()` forces `DISARMED`. |
| **One writer per symbol** | `SymbolLockRegistry` — a reentrant per-symbol `asyncio.Lock`. Queued fills/updates, reconcile/restart, disarm/kill, trail/close/flip, and the whole recovery run hold it; ordinary mutations **re-check** recovery ownership after acquisition. The durable expression is the partial unique index `ux_partial_recovery_active_symbol`. |
| **No TS-P1-005 scope theft** | The snapshot is bounded to one symbol: position + live orders + one direct order query. No balances, margin, or portfolio reconciliation. |

The final ARM, quarantine, and active-recovery checks plus new-entry
reservation/send sequencing are one locked submission boundary. An awaited
position read cannot create a gap in which recovery opens after the last check
but before reservation or broker submission.

## 4. State and action model

`PartialProtectionState` is deliberately separate from the raw exchange
`OrderState`:

```
PARTIAL_DETECTED → PROTECTION_PENDING → PROTECTION_VERIFIED → CANCEL_PENDING → PROTECTED_PARTIAL
                                    ↘ CANCEL_UNKNOWN ↗
  any state ──(deadline / proven failure)──▶ FLATTEN_PENDING ⇄ FLATTEN_UNKNOWN → SAFE_FLAT
  any state ──(unresolved / foreign / mixed)──▶ UNPROTECTED_ABORT
```

`PARTIAL_STATE_TRANSITIONS` is the single declared policy table (immutable,
same `_ImmutableMapping` holder as TS-P1-001). All transitions are monotonic
inside one generation except that a newly observed authoritative fill may move
`PROTECTION_VERIFIED`, `PROTECTED_PARTIAL`, `CANCEL_PENDING` or
`CANCEL_UNKNOWN` back to `PARTIAL_DETECTED` for quantity recomputation.
`SAFE_FLAT` and `UNPROTECTED_ABORT` are final inside their generation.
Authoritative post-`SAFE_FLAT` owned exposure creates a new row/generation;
contradictory exposure creates a new aborted generation.

`PROTECTED_PARTIAL` is accepting and terminal for automatic recovery, but it
does **not** restore ordinary position handling. The row stays in
`partial_recoveries_awaiting_rearm()` until a human ARM request proves, under
the same symbol lock and against a fresh exact snapshot, that protection still
covers the live quantity exactly (`confirm_partial_rearm`).

### Canonical order state

`orders.status` now persists the canonical quantity/action-derived lifecycle
state. `db.py`'s live-status sets and pending-grace paths include both new live
states, preserving TS-P1-007 `ENTRY_REMAINDER_LIVE` behavior.
`canonical_order_state()` derives:

* `0 < filled < ordered` → `OrderState.PARTIALLY_FILLED`
* a cancel reserved before I/O → `OrderState.PENDING_CANCEL`
* an exchange-confirmed terminal raw status wins over both
* every derived value is validated against `ORDER_STATE_TRANSITIONS`

An unknown cancel remains `PENDING_CANCEL`; its uncertainty is carried by
`PartialProtectionState.CANCEL_UNKNOWN`, never by inventing a raw status.

### Action identities

Reservation and state transition commit in one transaction **before** any
broker I/O. `cloid = blake2s(action_id)` so a proven-not-applied retry reuses
the same exchange identity.

| Kind | Identity domain |
| --- | --- |
| `CANCEL_ENTRY` | entry request identity + entry cloid — quantity- and generation-independent, so a late-fill re-entry keeps the same pending/unknown cancel context |
| `INSTALL_STOP` | trade/entry identity + generation + target lots |
| `FLATTEN` | the above + resolved-attempt sequence |
| `CANCEL_PROTECTION` | trade/entry identity + the exact owned cloid removed |

Generation-independent cancel reservations remain attached to the immutable
row that first reserved them. Later recovery generations reuse that row and
its append-only evidence; they never attempt to insert the same identity under
a second recovery foreign key. Ownership queries include actions from every
generation of the exact trade/entry lineage.

`CANCEL_PROTECTION` is a Gate-1-consistent addition: stale lineage-owned SLs
are removed only after an exact replacement is authoritatively live, and §2.7
also requires every live owned entry/SL/TP order to be terminal or absent
before `SAFE_FLAT`. Each cancellation reserves before I/O and requires a
direct terminal/absence query; transport success alone is not accepting
evidence. It only ever targets a cloid already proven owned. A replay whose
outcome is `UNKNOWN` performs queries only. Direct evidence of `NOT_APPLIED`
may authorize one resend only under the same immutable action identity.

**Retry law.** `resolve_partial_action` folds append-only evidence in sequence.
`NOT_APPLIED` followed by `APPLIED` is the valid result of an exact-identity
resend and resolves to `APPLIED`; `APPLIED` followed by `NOT_APPLIED` is a
contradiction and resolves to `UNKNOWN`, the most restrictive verdict. Later
`UNKNOWN` evidence never downgrades a definitive outcome. An action may be
re-issued **only** when the fold is `NOT_APPLIED`; `UNKNOWN`, no outcome after
reservation, and already-`APPLIED` replays permit evidence queries only. A new
identity requires the prior outcome to be definitive *and* the target quantity
to have changed.

## 5. Quantity and protection definition

* Comparisons are in **exact integer lot units** (`quantize_lots`), read through
  the shortest exact decimal spelling. Binary-float residue such as `0.1 + 0.2`
  fails closed rather than rounding into a tradeable size. There is no epsilon.
* The quantum comes from exchange metadata (`szDecimals`) or an explicit test
  fixture. A missing/invalid quantum, any non-lot quantity, and any overfill
  (including a sub-epsilon non-lot overfill) raises a quantity-integrity
  failure, latches `DISARMED`, and emits an integrity event. No order-state
  decision falls back to raw float comparison.
* `f` (entry filled) triggers recovery; `q` (authoritative live net position
  after a complete bounded snapshot) sizes protection and flattening. `f` is
  never substituted for `q`.
* Provenance: `q` must equal the exact durable owned net
  (`local entry-fill lots − local exit-fill lots − definitively applied
  recovery-flatten lots`). More live size is `MIXED`;
  less is conflicting/`AMBIGUOUS`; an opposite-side position is `AMBIGUOUS`;
  any live order outside the same trade/action lineage is foreign or mixed,
  including a locally known order belonging to another trade. All abort with
  zero mutation.
* `SAFE_FLAT` persists the accepted entry-fill baseline and the same-identity
  applied flatten evidence. A later nonzero position is owned only when fresh
  durable fill/order evidence advances that lineage beyond the baseline.
  Same-size manual/foreign exposure with no fresh owned evidence is ambiguous
  and causes zero mutation.
* **A qualifying stop is exactly one live owned SL**: same symbol; opposite
  exit side; `role == "SL"`; `reduce_only == true`; owned by the same
  trade/action lineage; live; and size exactly `q` in lot units. A second live
  owned SL makes the decision non-qualifying even if one or both stops are
  exact. Under-sized, over-sized, wrong-side, non-reduce-only, stale, foreign,
  ambiguous, duplicate, and unverified stops do not qualify. Take-profit never
  substitutes.
* This predicate is **shared**: `qualifying_protection()` governs placement
  verification and `_position_is_protected()` governs `reconcile()`. The
  previously quantity-blind reconciliation is repaired by this task; ordinary
  reconcile and human re-ARM both reject duplicate live owned SLs. Missing or
  invalid quantum fails closed; no epsilon or raw-float fallback is used for an
  accepting protection decision.

## 6. Time and restart semantics

* The runtime deadline uses an **injected monotonic clock**
  (`OrderManager(..., monotonic=...)`), armed at the moment of detection.
  Monotonic values are process-local and are **never persisted**.
* An absolute UTC deadline is persisted in the same transaction as first
  detection. `open_partial_recovery` is idempotent, so no retry, reconnect,
  later fill, generation bump, or restart can rewrite it.
* Expiry is conservative: expired if **either** domain says expired. Wall-clock
  rollback (`now < first_observed_ts`), unparseable time, or missing evidence
  is treated as expired — never as a fresh 10-second window.
* On restart only the durable UTC domain exists; re-arming the monotonic domain
  uses the *remaining* budget, never a full one.
* Legacy/expired-at-start state: `legacy_partial_entry_candidates()` is a pure
  local query in `db.py` (**no broker I/O there**); `OrderManager` startup
  recovery proves ownership against a bounded snapshot, seeds the deadline from
  the earliest durable fill — so an old partial starts already expired — and
  runs one immediate protect-and-cancel cycle then the bounded flatten. Weak
  evidence (no durable fill, inexact snapshot, no recovery API) opens a durable
  `UNPROTECTED_ABORT` latch and performs zero broker mutation, preventing the
  ordinary reconciler from acting on the same ambiguous position.
* A restart scan treats a pending or archived `PROTECTED_PARTIAL` row as an
  existing accepting generation, not a legacy orphan. A pending human re-ARM
  row continues to own the symbol, so ordinary reconciliation cannot repair,
  flatten, trail, or close it before the exact locked re-ARM proof succeeds.
* The 5.0 s flatten budget starts at the first flatten entry and is written
  exactly once (`_transition_partial_in_tx` refuses to overwrite a non-NULL
  `flatten_deadline_ts`). Expiry without the full safe-flat proof ends
  `UNPROTECTED_ABORT`.

## 7. Persistence — schema v5

`meta.schema_version` remains the single database authority. TS-P1-004 adds an
atomic, additive `4 → 5` migration through that contract; SQLite
`PRAGMA user_version` is **not** used anywhere.

`initialize(target_schema_version=...)` defaults to **4**. v5 is an explicit
opt-in so that neither existing callers nor an existing runtime database are
upgraded merely by being opened. A database already at v5 reopens idempotently
regardless of the requested target and is never downgraded in place.
Unsupported or future versions still fail closed.

```
partial_fill_recoveries   -- one row per trade/entry/generation
  recovery_id TEXT PK      (pfr-v1:<sha256>)
  trade_id    INTEGER  REFERENCES trades(trade_id)     -- real v4 type
  entry_cloid TEXT     REFERENCES orders(cloid)        -- real durable key
  generation, flatten_seq, state, provenance,
  size_decimals, ordered_lots, filled_lots, position_lots,
  first_observed_ts, protect_deadline_ts, flatten_deadline_ts,
  reason_code, created_ts, updated_ts
  UNIQUE(trade_id, entry_cloid, generation)
  UNIQUE INDEX ux_partial_recovery_active_symbol(symbol) WHERE state NOT IN (terminal)

partial_fill_actions      -- immutable reservations (UPDATE/DELETE triggers)
  action_id TEXT PK (pfa-v1:<sha256>), recovery_id, trade_id, kind,
  generation, flatten_seq, qty_lots, target_cloid, reserved_ts
  UNIQUE(target_cloid, kind)

partial_fill_action_events -- append-only evidence (UPDATE/DELETE triggers)
  event_id, action_id, recovery_id, seq, status, evidence_source,
  reason_code, evidence_json, observed_ts
  UNIQUE(action_id, seq)
```

Transaction boundaries: first detection + DISARM latch; each state transition +
action reservation *before* broker I/O; broker result/evidence append; final
protected/flat/abort result; late-fill re-entry + generation bump with
unresolved action context preserved.

Migration rules: one `BEGIN IMMEDIATE` for DDL, evidence census, canonical
topology validation, and the version bump. Validation compares required
columns (including safety-relevant types, nullability, defaults, and primary
keys), unique/check/foreign-key constraints, indexes and predicates, triggers
and bodies, and the complete canonical table topology. The same validation
runs on every v5 reopen. A before/after row census over every v4 evidence table
refuses any migration that would alter existing rows. No speculative backfill.
Any malformed pre-existing residue or validation failure rolls back completely
— `schema_version` stays `4`, no new v5 residue survives, and v4 evidence
remains logically unchanged and reopenable.

Hyperliquid recovery parsing is independently fail-closed: malformed
collections/rows, missing required position/order fields, absent
`reduceOnly`, non-finite sizes, or an order status outside the explicit live
and terminal whitelists produce inexact/unknown evidence. `reduceOnly` is
never inferred.

## 8. Adversarial coverage

`tests/test_partial_fill_protection.py` (135 tests) plus the TS-P1-004 blocks
in the five touched suites cover: exact lot normalization and rounding
boundaries; missing/invalid quantum; the ten states and their illegal edges;
happy path; 1-lot and zero-position paths; active TS-P1-003 quarantine
(zero mutation, no competing abort); foreign order; mixed provenance; opposite
side; inexact snapshot before/after the deadline; missing stop price; missing
recovery API; unknown protect (zero re-place, evidence only); unknown-but-
applied resolved by evidence; proven-not-applied same-cloid retry; unknown
cancel; crash after reservation before send; deadline non-reset on later fill,
on restart, and in the monotonic domain alone; wall-clock rollback;
unparseable deadline; flatten deadline written once; flatten expiry →
`UNPROTECTED_ABORT`; unknown flatten freezing the sequence; proven-failed
flatten advancing it with a new identity; late fill during cancel → new
generation and re-protection at the new exact lots; identity determinism across
replay; `SAFE_FLAT` refused on remainder and on orphan owned protection;
new proven owned exposure after `SAFE_FLAT` opening a new generation;
same-size manual exposure remaining ambiguous with zero mutation; a full late
fill to exactly ordered quantity reopening recovery after both
`PROTECTED_PARTIAL` and `SAFE_FLAT`; foreign/manual quantity introduced before
or during flatten preventing reservation and I/O; UNKNOWN applied flatten
remaining non-accepting until same-identity evidence resolves; duplicate exact owned
stops failing closed; under/over-sized prior-generation stops reserved,
cancelled, directly proved absent, and only then accepted; UNKNOWN stale-stop
cancel replay remaining query-only until same-identity `NOT_APPLIED`; foreign
or unverified extras never cancelled; ordinary reconcile and human re-ARM
rejecting duplicates; the five other non-qualifying-stop shapes; unowned exact
stop; recovery suppressing ordinary repair, trail, and close; abort latch;
concurrent runs serialized by the lock;
store immutability/append-only triggers, CAS, replay reserve, conservative
outcome fold, flatten-sequence refusal; complete v5 topology; malformed-residue
migration rollback and noncanonical-reopen refusal; migration
rollback, evidence-preservation refusal, idempotent reopen, future/corrupt
version, unsupported target, v2→v5 chain; legacy strong/weak evidence; engine
DISARM latch, ARM refusal, pre-ARM trail/close suppression, and the re-ARM
proof (success, missing stop, inexact snapshot).

## 9. Scope boundary and deployment

* This code task touched no runtime database, no network, no exchange, no
  testnet, no P2RT, no Task Scheduler, and no configuration or API surface.
* `Broker` keeps its accepted `cancel` / `flatten` / `reprotect_position`
  shape; the new surface is the separate `PartialRecoveryBroker` protocol, so
  fake brokers outside the allow-list are untouched. `OrderManager`
  feature-detects it and treats absence as "recovery unavailable" —
  `UNPROTECTED_ABORT` with zero mutation.
* **Deployment prerequisite (open):** `bridge/app.py` calls
  `store.initialize()` with the default v4 target and is outside this task's
  allow-list. On a v4 database every TS-P1-004 path is inert and behaviour is
  byte-identical to the base commit. A separate, approved deployment gate must
  (a) take and verify an evidence-preserving DB/WAL/SHM backup, (b) wire the
  v5 target, and (c) confirm no old v4-only writer can open the v5 database.
* Runtime rollback means: stop the writer, preserve the v5 database and its
  audit evidence, restore the verified pre-migration v4 copy, then reconcile
  under a separately approved runbook. Never downgrade in place, delete v5
  rows, or rewrite historical events to make a rollback pass.
