# Chaos-Drill Design — MockBroker Fault Injection (DESIGN ONLY)

Package 5a — Local Observability Toolkit, first increment (T1).
Gate-1 record: `MTC_COMMAND_CENTER/11_TRIAGE/GATE1_PACKAGE5A_OBSERVABILITY_TOOLKIT_2026-08-18.md`.

> ## Implementation is explicitly DEFERRED
>
> This document is a **specification, not an implementation**. Per the Gate-1
> record (§1 item 4): wiring these drills into the live test harness
> approaches protected behavior surfaces and deserves its own increment and
> its own Gate-1 slot. **Nothing in this package executes any drill.** There
> is no drill code, no harness change, no broker/mock change in this
> increment — only this matrix. The recorded trim is intentional, not an
> omission.

## Purpose

When a later increment implements them, these drills inject specific faults
into a **MockBroker + fixture-store** environment and check that the accepted
contracts' invariants hold under adversity. The contracts under test:

- `docs/21_WINDOW_STATE_CONTRACT.md` — honest monitoring-window state
- `docs/22_ORDER_STATE_CONTRACT.md` — canonical order-state machine
  (incl. the TS-P1-004 amendment)
- `docs/23_ORDER_IDENTITY_CONTRACT.md` — durable order identity

Every drill runs **locally, loopback-only, DISARMED by default**, against a
fixture store built by `fixtures/build_fixture_store.py` (or a drill-specific
variant of it). No drill contacts any exchange, network, or live path.

## Lifecycle stages referenced by the matrix

S1 `PENDING_NEW → SUBMITTING` — intent created, submission in flight
S2 `SUBMITTED / OPEN` — acknowledged, resting on the (mock) book
S3 `PARTIALLY_FILLED` — owned partial entry, recovery machinery engaged
S4 `PENDING_CANCEL` — cancel requested, awaiting confirmation
S5 terminal (`FILLED / CANCELED / REJECTED / EXPIRED`) — lifecycle ended
S6 process restart — any of the above cut by a process death

## Drill matrix

| Drill | Fault injected | Stage(s) | Expected invariants (with citations) |
| --- | --- | --- | --- |
| **D1-a** Disconnect during submission | MockBroker connection drops after send, before ack | S1 | Submission outcome is `UNKNOWN_SUBMISSION` — frozen, never blindly retried (`22:82`, `22:157-164`); reservation stays `RESERVED`, no trade/order rows created (`23:138-149`); no second broker submission on reconnect — exact intent+request is BLOCKED (`23:127-137`) |
| **D1-b** Disconnect with resting order | Connection drops while an order is OPEN | S2 | Order's durable state unchanged by the disconnect itself; liveness gap rules apply to the window, not the order (`21:26-35`); duplicate delivery of the same identity on reconnect creates no second submission (`23:8-10`, `23:127-137`) |
| **D1-c** Disconnect during cancel | Connection drops after cancel request, before confirmation | S4 | Order remains `PENDING_CANCEL`; the uncertainty lives in `PartialProtectionState.CANCEL_UNKNOWN`, and no raw exchange status is invented to express doubt (`22:355-360`); authoritative terminal evidence later wins (`22:138-141`) |
| **D1-d** Disconnect during partial recovery | Connection drops mid recovery run | S3 | The whole recovery run serializes through the per-symbol lock; the run asserts the lock before snapshot or send (`22:362-372`); cleanup cancels are durably reserved before I/O and proved terminal/absent before any accepting state (`22:374-384`) |
| **D2-a** First partial fill on owned entry | Fill arrives for part of the ordered qty while ARMED | S2→S3 | First detection writes `PARTIALLY_FILLED`, opens the recovery row, and latches `app_state=DISARMED` in one transaction (`22:333-338`) |
| **D2-b** Unknown cancel during recovery | Cancel sent for the remainder; outcome unknown | S3/S4 | Order stays `PENDING_CANCEL`; `CANCEL_UNKNOWN` in the separate recovery state machine; never a fabricated raw status (`22:355-360`); UNKNOWN cancellation evidence is query-only — only a proved `NOT_APPLIED` may resend the same immutable identity (`22:380-383`) |
| **D2-c** Fill races the flatten | Additional fill lands after protect/flatten initiated | S3/S4→S5 | Authoritative race outcomes always win: `PENDING_CANCEL` may still receive `FILLED / PARTIALLY_FILLED / CANCELED / EXPIRED` (`22:138-141`, `22:176-184`) |
| **D2-d** Overfill / lot violation | Evidence shows `filled > ordered`, or a non-lot-multiple size | S3 | Quantity-integrity failure (`22:323`); exact integer lot units only, no epsilon — `LotQuantizationError` rather than a lifecycle state, and the engine records a durable integrity event + `DISARMED` (`22:346-353`) |
| **D3-a** Stale fill ack | Delayed fill acknowledgment arrives after cancel confirmed | S4→S5 late | Terminal states have no outgoing edges; same-state replay is the only idempotent re-observation (`22:165-172`); late evidence must not resurrect or rewrite the terminal outcome — post-recovery generations never downgrade a terminal entry order (`22:342-344`) |
| **D3-b** Cancel-reject race | Exchange declines the cancel after `PENDING_CANCEL` | S4→S2 | `PENDING_CANCEL → OPEN` is the declared cancel-reject edge; the order remains exactly as live as before (`22:151-156`) |
| **D3-c** Ack after safe-flat | Acknowledge arrives for an order the engine already moved past | S5 | Terminal durability holds: `FILLED/CANCELED/REJECTED/EXPIRED` accept no new lifecycle edges (`22:140-142`, `22:170-172`); collision-safe persistence preserves the original row and raises rather than overwrites (`23:156-160`) |
| **D3-d** Duplicate submission ack | The same submission is acknowledged twice (replay) | S1/S2 | Duplicate delivery never creates a second broker submission (`23:8-10`); exact intent+request → BLOCKED with no broker I/O (`23:127-137`); same cloid + same identity updates mutable fields only (`23:151-158`) |
| **D4-a** Restart after reservation | Process dies after identity RESERVED, before broker send | S1 | Reservation is durable and RESERVED; no trade/order rows exist; no submission without a committed reservation (`23:126-137`, `23:148-149`) |
| **D4-b** Restart before ack | Process dies after send, before acknowledgment | S1 | Attempt state `UNKNOWN_SUBMISSION`; resolution only via reconciliation evidence cycles (`CONFIRMED_PRESENT` / `CONFIRMED_ABSENT`), never blind retry (`22:157-164`, `bridge/store/db.py:1125-1129`) |
| **D4-c** Restart mid recovery | Process dies during an open partial-fill recovery | S3 | Recovery row and `DISARMED` latch survive the restart (durable persistence, `22:333-345`); restart recovery re-serializes through the per-symbol lock (`22:362-372`) |
| **D4-d** Restart mid-window | Process dies during a soak window, restarts after a gap | S6 | Gap > `stale_after_s` (300 s) stamps a sticky interruption; re-arming never clears it; gap ≤ 300 s stamps nothing while disarmed-live still reads INTERRUPTED (`21:44-52`); RUNNING still requires fresh liveness + ARMED + no interruption — a dead bridge never presents as an active window (`21:36-42`) |

## Expected invariant classes (what "pass" means)

1. **Fail-closed**: every ambiguous outcome ends in an explicit unknown/error
   state, never a guessed live or terminal state.
2. **No double execution**: duplicate/replayed intent never reaches the broker
   twice.
3. **Terminal durability**: no late or stale evidence mutates a terminal
   outcome.
4. **Disarm on owned partial**: partial-fill detection latches DISARMED
   atomically and survives restart.
5. **Window honesty**: the monitoring window never claims RUNNING from a dead
   bridge, and gaps stay visible until an explicit reset.
6. **Sanitized events**: every persisted event during a drill carries
   structured IDs/codes only — no raw exception text (`23:178-186`).

## Evidence format (per drill run)

Each drill run produces, at minimum:

1. **Drill header** — drill id (e.g. `D2-a`), operator-supplied timestamp,
   fixture store path, tool versions.
2. **Audit pack** — `export_audit_pack.py` output against the fixture store
   AFTER the drill (this package's Markdown pack; schema version, row counts,
   state, bounded recent orders/events, and any REPORTED gaps).
3. **Event excerpt** — the `events` rows emitted during the drill window,
   showing codes (and demonstrating sanitization).
4. **Ledger rows** — relevant `order_identity` / `submission_attempts` /
   `submission_recovery_evidence` rows for the drilled order.
5. **Verdict table** — one row per expected invariant: `invariant id ·
   observed · PASS/FAIL`, citing the contract line(s) judged.

All artifacts are local files; nothing is transmitted. A drill run against
anything other than a fixture store is out of scope by construction (the
export tool takes an explicit path and has no default).

## Non-goals / boundaries (inherited from Gate-1)

- No broker/exchange interaction of any kind in this increment.
- No test-harness modifications, no changes under `bridge/`.
- Drill execution, MockBroker fault-injection hooks, and any harness wiring:
  deferred to a later, separately gated increment.
