# 22 — Canonical Order-State Machine (TS-P1-001)

Module: `bridge/engine/types.py` (`OrderState`, `ORDER_STATE_TRANSITIONS`,
`TERMINAL_ORDER_STATES`, `can_transition`, `validate_order_transition`,
`normalize_raw_order_status`, `RAW_ORDER_STATUS_ALIASES`,
`IllegalOrderTransitionError`, `UnknownRawOrderStatusError`). Tests:
`tests/test_order_state.py`. Governing: ADR-0023.

**Status: PROPOSED** — pending independent Codex Gate-5 audit, then Barış
acceptance. Not yet wired into persistence, broker adapters, or the engine
(see Scope boundary below).

**Repair history:** commit `5140e062` was BLOCKed by independent Codex audit
(`11_TRIAGE/CODEX_TSP1001_AUDIT_2026-07-20.md`) for a mutable policy-map
backing surface (F1) and an unsafe exception contract (F2); repair commit
`851d88a0` fixed the named-seed and hostile-`repr` examples
(`11_TRIAGE/CLAUDE_TSP1001_REPAIR_REPORT_2026-07-20.md`) but was itself
BLOCKed on re-audit (`11_TRIAGE/CODEX_TSP1001_REAUDIT_2026-07-20.md`) for two
residual findings: F1-R — `MappingProxyType`'s backing `dict` is still a
mutable object reachable via `gc.get_referents()` regardless of naming; F2-R
— `type(raw).__name__` is not safe against a hostile metaclass overriding
class attribute lookup. Both are fixed in the second repair described in
`11_TRIAGE/CLAUDE_TSP1001_REPAIR2_REPORT_2026-07-20.md`. The immutability and
exception sections below describe the twice-repaired behavior.

## Problem

ADR-0023 requires "Accepted, resting, partially filled, filled,
pending-cancel, canceled, rejected, expired, and unknown outcomes... [to be]
represented explicitly," but before this task the bridge had no authoritative
state model — only ad hoc string literals (`"OPEN"`, `"SUBMITTED"`,
`"FILLED"`, `"CANCELLED_BY_ENGINE"`) produced/consumed inconsistently across
`db.py`, `mock.py`, `hyperliquid.py`, and `orders.py`, no declared transition
legality, and a permissive `"OPEN"` default for unrecognized values.

## Raw-status inventory (read-only survey of `bridge/` + `tests/`)

| Raw spelling | Producer(s) | Consumer(s) | Notes |
| --- | --- | --- | --- |
| `"OPEN"` | `BrokerOrder.status` default; `MockBroker._order`; `HyperliquidBroker` fallback/default | `db.py` live-set; `orders.py`; `mock.py`; tests | Also used today as a **permissive fallback default** for missing/unrecognized exchange status — a known existing risk this task does not fix (see Scope boundary). |
| `"SUBMITTED"` | test fixtures only (`test_store.py`, `test_interim_risk_wiring.py`) | `db.py` live-set; `orders.py` pending-grace check | No current broker/mock producer; exercised only via direct store/test injection. |
| `"PENDING"` | none found | `db.py` live-set membership check only (`{"OPEN","SUBMITTED","PENDING"}`) | Referenced but never assigned by any producer in this repo. Treated as a reserved/legacy alias (rationale below). |
| `"FILLED"` | `MockBroker.process_bar` / `_fill_exit`; `orders.py._ingest_fill` (on completion) | tests; `db.py` | Terminal. |
| `"CANCELLED_BY_ENGINE"` | `MockBroker.cancel` / `cancel_all` | tests | Terminal; British-spelling raw literal (double L) — canonical uses single-L `CANCELED`. Not a silent reinterpretation: the alias is explicit in the mapping table below. |
| `"WAITING_CHILD"` | `HyperliquidBroker` open-orders reconciliation (raw exchange `"waitingForFill"` / `"waitingForTrigger"` child statuses) | `tools/smoke_p0.py`, `test_hyperliquid_broker.py` | **Excluded from this contract.** Never assigned to `BrokerOrder.status` or persisted via `update_order_status`; it is an out-of-band field on an adapter-internal reconciliation dict describing a child SL/TP order awaiting parent trigger. A future task must decide its canonical representation when child-order lifecycle is formalized. |
| Decision `"stage"` values `"SUBMITTED"` / `"REJECTED"` (`engine.py` `insert_decision`, `Rejection.stage`) | `engine.py` | `test_p1_failure_drills.py`, `test_engine_dryrun.py` | **Different axis, same coincidental spelling.** Describes whether a *decision* produced an order at all (risk/LLM/state rejection before submission), not the lifecycle of an *order* that reached the exchange. Not part of this contract. |

## Canonical model

`OrderState` (`str` Enum, JSON/Pydantic round-trippable) — 11 states:

| State | Meaning |
| --- | --- |
| `PENDING_NEW` | Intent created locally; not yet sent to the broker. |
| `SUBMITTING` | Submission call in flight; no acknowledgment yet. |
| `SUBMITTED` | Broker acknowledged/accepted the order; existence confirmed. |
| `OPEN` | Resting/working on the book. |
| `PARTIALLY_FILLED` | Nonzero fill progress; remainder still live. |
| `PENDING_CANCEL` | Cancel requested; not yet confirmed. |
| `FILLED` | Terminal — fully filled. |
| `CANCELED` | Terminal — canceled, no further fills. |
| `REJECTED` | Terminal — broker/exchange rejected. |
| `EXPIRED` | Terminal — time-in-force expiry. |
| `UNKNOWN_SUBMISSION` | Submission outcome ambiguous (timeout/disconnect, no ack). Frozen pending reconciliation — never terminal, never blindly retryable. |

`TERMINAL_ORDER_STATES = {FILLED, CANCELED, REJECTED, EXPIRED}`.

## Raw → canonical mapping

`normalize_raw_order_status(raw)` is case/whitespace-tolerant on known
aliases (`.strip().upper()`, matching the existing `hyperliquid.py`
normalization behavior) and fail-closed on everything else:

| Raw (any case/whitespace) | Canonical |
| --- | --- |
| `OPEN` | `OrderState.OPEN` |
| `SUBMITTED` | `OrderState.SUBMITTED` |
| `PENDING` | `OrderState.SUBMITTED` (see rationale) |
| `FILLED` | `OrderState.FILLED` |
| `CANCELLED_BY_ENGINE` | `OrderState.CANCELED` |

Rationale for `PENDING → SUBMITTED`: every existing occurrence of
`"PENDING"` groups it identically with `"OPEN"` and `"SUBMITTED"` in a "live"
membership check and never distinguishes it from either; no producer exists
to observe real semantics. Mapped to the more conservative of the two live
buckets (`SUBMITTED`, not `OPEN`), since `OPEN` specifically asserts
confirmed-resting, which an unqualified `PENDING` does not evidence.

Anything else — non-string input (`bool`, `None`, `bytes`, list, dict,
including hostile objects with a leaking or raising `__repr__`),
empty/whitespace-only strings, and unrecognized strings (`"OPENN"`,
`"waitingForFill"`, `"WAITING_CHILD"`) — raises
`UnknownRawOrderStatusError(raw, reason_code)` with `reason_code` one of
`NON_STRING_RAW_STATUS`, `EMPTY_RAW_STATUS`, `UNRECOGNIZED_RAW_STATUS`.
**Never** defaults to `OPEN`/`SUBMITTED`/`FILLED` or any other live/terminal
state. The error message is a constant string per `reason_code` — it never
accesses any attribute of `raw` or `type(raw)` at all, not `repr()`/`str()`
and not even `type(raw).__name__` (a class's `__name__` lookup is dispatched
through its metaclass, so a caller-controlled metaclass can intercept and
raise on that specific access — audit F2-R). So neither a hostile
`__repr__` nor a hostile metaclass can leak text into the message or escape
this exception. The original `raw` object is still available unmodified on
the `.raw` attribute for a caller who chooses to inspect it themselves.

`IllegalOrderTransitionError` (raised by `validate_order_transition`) always
carries `reason_code == "ILLEGAL_ORDER_TRANSITION"` alongside the structured
`from_state`/`to_state` fields — every instance, not conditional on which
pair was illegal.

## Transition table

33 state-change edges + 11 idempotent same-state edges = **44 legal ordered
pairs of 121 possible** (11 × 11).

| From | Legal To (excluding self) |
| --- | --- |
| `PENDING_NEW` | `SUBMITTING` |
| `SUBMITTING` | `SUBMITTED`, `REJECTED`, `UNKNOWN_SUBMISSION` |
| `SUBMITTED` | `OPEN`, `REJECTED`, `FILLED`, `PARTIALLY_FILLED`, `EXPIRED`, `PENDING_CANCEL`, `CANCELED` |
| `OPEN` | `PARTIALLY_FILLED`, `FILLED`, `PENDING_CANCEL`, `CANCELED`, `EXPIRED` |
| `PARTIALLY_FILLED` | `FILLED`, `PENDING_CANCEL`, `CANCELED`, `EXPIRED` |
| `PENDING_CANCEL` | `CANCELED`, `FILLED`, `PARTIALLY_FILLED`, `OPEN`, `EXPIRED` |
| `UNKNOWN_SUBMISSION` | `SUBMITTED`, `OPEN`, `PARTIALLY_FILLED`, `PENDING_CANCEL`, `FILLED`, `CANCELED`, `REJECTED`, `EXPIRED` |
| `FILLED` / `CANCELED` / `REJECTED` / `EXPIRED` | *(none — terminal)* |

Design notes:

- **Direct terminal edges from `SUBMITTED`/`OPEN`** (e.g. `OPEN → CANCELED`
  without passing through `PENDING_CANCEL`; `OPEN → FILLED` without
  `PARTIALLY_FILLED`) are intentional, not an oversight: `MockBroker.cancel()`
  and `_fill_exit()` already perform exactly this atomic transition today,
  and some venues confirm cancels/fills synchronously. `PENDING_CANCEL`
  models the *client-observable awaiting-confirmation window* where one
  exists; it is not mandated on every cancel path.
- **`PENDING_CANCEL → OPEN`** models a cancel-reject race (exchange declines
  the cancel; the order remains exactly as live as before). This is not a
  regression of `PARTIALLY_FILLED` — that regression is separately and
  explicitly forbidden (see Invariants).
- **`UNKNOWN_SUBMISSION` never reaches `PENDING_NEW` or `SUBMITTING`.** Per
  ADR-0023, resolving an ambiguous submission requires reconciliation
  evidence (TS-P1-003), which this task does not implement. A pure
  two-state transition relation cannot encode "with evidence" as a distinct
  edge, so the edge is simply absent — categorically illegal here. A retry
  after real reconciliation creates a **new** order/decision_uid; it is
  never modeled as this same order mutating backward.

## Invariants (tested exhaustively in `test_order_state.py`, 85 cases)

1. Every one of the 121 ordered `(from, to)` pairs has one deterministic
   legal/illegal answer — `can_transition` is a total pure function over
   `OrderState × OrderState`.
2. `FILLED`, `CANCELED`, `REJECTED`, `EXPIRED` are terminal: zero outgoing
   edges except self. Same-state replay (`X → X` for every state, including
   terminal) is always legal — an idempotent observation, not a new
   lifecycle transition.
3. `UNKNOWN_SUBMISSION → {PENDING_NEW, SUBMITTING}` is illegal
   unconditionally — no blind-retry path exists in this model.
4. `PARTIALLY_FILLED` never transitions to `PENDING_NEW`, `SUBMITTING`,
   `SUBMITTED`, or `OPEN` (no regression to a lower-progress ordinary
   state). `PENDING_CANCEL` may still receive `FILLED`/`PARTIALLY_FILLED`/
   `CANCELED`/`EXPIRED` (authoritative race outcomes always win over a
   pending cancel request).
5. Unrecognized raw statuses fail closed via `UnknownRawOrderStatusError`,
   reason-coded; never default to a live/filled state.
6. `ORDER_STATE_TRANSITIONS` and `RAW_ORDER_STATUS_ALIASES` are instances of
   a private `_ImmutableMapping` class (implements `collections.abc.Mapping`
   over a `tuple` of `(key, value)` pairs), not `MappingProxyType` over a
   `dict`. This distinction is load-bearing: `MappingProxyType(d)` blocks
   writes *through the proxy*, but `d` remains a plain mutable `dict` and is
   returned directly by Python's standard `gc.get_referents(proxy)` — so
   mutating it changes later `can_transition`/`normalize_raw_order_status`
   decisions regardless of whether `d` is bound to any module-level name
   (audit F1-R). A `tuple` cannot be mutated in place at all, so the entire
   object graph reachable from either export — checked transitively via
   `gc.get_referents`, not just one hop — contains only tuples, `frozenset`s,
   and `OrderState`/`str` values; no `dict`, `list`, or other mutable
   container exists anywhere in it. `can_transition`/
   `validate_order_transition`/`normalize_raw_order_status` perform no
   mutation and no I/O. A caller can still take
   `dict(ORDER_STATE_TRANSITIONS)`/`dict(RAW_ORDER_STATUS_ALIASES)` to get
   their own independent mutable copy, but mutating that copy cannot affect
   the original.
7. `IllegalOrderTransitionError` and `UnknownRawOrderStatusError` are safe to
   construct from untrusted input: neither ever accesses any attribute of a
   caller-supplied object when building its message.
   `IllegalOrderTransitionError` only ever receives `OrderState` members
   (our own closed enum, never externally supplied raw data) and formats
   them via `.value`. `UnknownRawOrderStatusError`'s message is a constant
   string per `reason_code` and does not reference `raw` at all — not
   `repr()`/`str()`, and not even `type(raw).__name__` (accessing a class's
   `__name__` is dispatched through its metaclass, so a caller-controlled
   metaclass can intercept that specific lookup and raise — audit F2-R).
   Both exceptions carry a stable `reason_code` attribute.
8. All pre-existing `bridge/engine/types.py` models/imports are unchanged;
   `OrderState` and its supporting symbols are additive only.

## Quantity limitation (explicit)

This is a **state-only** model: it has no concept of order quantity, filled
quantity, or VWAP, and cannot by itself prove fill arithmetic. Concretely,
existing production code (`orders.py._ingest_fill`) already keeps an order's
raw `status` column at its pre-fill value (e.g. `"OPEN"`) through partial
fills, disambiguating progress purely via the separate `filled_qty` column —
today's real data does not always populate a distinct `PARTIALLY_FILLED` raw
status even though the canonical model declares one. Wiring
`PARTIALLY_FILLED` detection into `orders.py` (comparing `filled_qty`
against order quantity) is out of scope here and belongs to a later task
(TS-P1-004 per the backlog).

## Scope boundary — what this task does NOT do

- Does not modify `orders.py`, `db.py`, `broker/mock.py`,
  `broker/hyperliquid.py`, `api/routes.py`, `engine/engine.py`, or any
  schema/migration.
- Does not wire `OrderState`, `normalize_raw_order_status`, or
  `validate_order_transition` into persistence, broker adapters, or the
  engine. `BrokerOrder.status` and `OrderUpdateEvent.status` remain plain
  `str` fields.
- Does not fix the existing permissive `"OPEN"` fallback default in
  `BrokerOrder.status` / `hyperliquid.py` — flagged here as a known
  pre-existing risk for the task that does the wiring.
- Does not implement identity/idempotency (TS-P1-002), unknown-submission
  reconciliation/recovery (TS-P1-003), or partial-fill protect-or-flatten
  policy (TS-P1-004). This contract only supplies the state vocabulary and
  legality relation those tasks will consume.
- No exchange call, server, backtest, or deploy action of any kind.

## Rollback

Purely additive: one new block in `types.py` plus two new files (this doc
and the test file). Revert = `git revert` the single commit, or delete the
added block from `types.py` and the two new files. No migration, no
persisted data, no running system depends on this yet.

## Acceptance

Status: **PROPOSED.** Awaiting independent Codex Gate-5 audit on the real
diff, then Barış acceptance of the invariant contract (per the TS-P1-001
backlog row: "Barış accepts invariant contract"). Not to be treated as
ratified until Barış signs off in `_AI_MEMORY/DECISIONS.md`.
