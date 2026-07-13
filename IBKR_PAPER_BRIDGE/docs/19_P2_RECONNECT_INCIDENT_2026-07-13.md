# P2 Reconnect Incident Resolution and ARM Report

Date: 2026-07-13 UTC. Environment: Hyperliquid TESTNET only.

## Final verdict

**ALREADY ARMED — SAFE AND VERIFIED**

Official P2 Day 0 start: **2026-07-13T13:00:28.6218649Z**.

Exactly one ARM request was issued after fresh Baris approval and after every repaired reconnect
gate passed. Immediate and post-reconcile checks found zero exchange positions and zero open
orders. Mainnet was never enabled or contacted.

## Incident and containment

The earlier process repeatedly lost its WebSocket with `Expired`. The pre-fix reconnect path
rebuilt the SDK clients, subscribed user channels in `connect()`, then subscribed `userEvents`
again in `resubscribe()`. Installed Hyperliquid SDK code rejects that duplicate at
`websocket_manager.py:148` with `NotImplementedError`.

Telegram later showed two ARMED transitions separated by a process restart, but the old runtime
did not persist HTTP mutation records. The bridge was therefore treated as an active incident.
Evidence was captured first; the live API then proved `DISARMED`, positions `[]`, and orders `[]`.
The Task Scheduler supervisor was stopped. Windows left PID 65384 orphaned; it was terminated only
after the zero-exposure proof. Port 8790 then closed.

## Corrective implementation

Deployment is isolated from the parallel-agent research worktree:

- runtime worktree: `C:\P2RT`;
- branch: `feature/ibkr-bridge-final`;
- reconnect base fix: `29d9879f`;
- incident hardening commit: `59c334c065b0b88e66d2cdcedf8337fa1fc76e86`;
- Task Scheduler action now points to
  `C:\P2RT\IBKR_PAPER_BRIDGE\tools\run_bridge_p2.ps1`;
- the supervisor script resolves its root from `$PSScriptRoot`, not a shared absolute checkout.

Commit `59c334c0` adds:

- a persistent reconciler exception boundary and retry loop;
- fail-closed DISARM on reconciler failure;
- `last_reconcile_ts` and `reconcile_error` status evidence;
- ARM rejection when reconcile evidence is stale;
- sanitized traceback callsites in `RECONCILE_FAILED` events;
- auditable `ARM_REQUEST`, `DISARM_REQUEST`, and `STATE_TRANSITION` events;
- explicit Telegram-visible `RECONNECT` and `DATA_RESTORED` success events;
- a 60-second fresh-data deadline after reconnect, otherwise `DATA_STALE` and DISARM;
- thread-safe scheduling of async bar callbacks from the SDK WebSocket thread.

The original reconciler stopped after one unhandled broker exception while the old boolean stayed
true. Its exact exception traceback was not retained by the old code. The new code preserves a
sanitized call stack and keeps retrying while disarmed.

## Verification

Targeted safety suite: **73 passed**.

Full suite:

- repo root: **119 passed, 1 warning**;
- `IBKR_PAPER_BRIDGE/`: **119 passed, 1 warning**.

The only warning is the existing Starlette/httpx test-client deprecation.

Pinned process:

- supervisor PID 95724;
- bridge child PID 81788;
- run `paper-20260713124604`;
- mode `paper`, network `testnet`, broker `hyperliquid`, BTC 1h;
- startup state `DISARMED`;
- startup exchange positions/orders: `[]` / `[]`.

Real natural reconnect gate:

| Evidence | UTC |
|---|---|
| DISCONNECT | 2026-07-13T12:57:21.934878Z |
| RECONNECT attempt=1 | 2026-07-13T12:57:29.844827Z |
| DATA_RESTORED | 2026-07-13T12:57:39.924260Z |
| Fresh market-data timestamp | 2026-07-13T12:57:39.488108Z |
| Post-restore reconcile 1 | 2026-07-13T12:58:29.107810Z |
| Post-restore reconcile 2 | 2026-07-13T12:59:30.309495Z |

There were no `RECONNECT_RETRY`, `NotImplementedError`, `DATA_STALE`, or `RECONCILE_FAILED`
events. Positions and orders remained empty.

## ARM record

Pre-ARM check at `2026-07-13T13:00:28.6021648Z`:

- state `DISARMED`;
- state version 2;
- reconcile ready, age 58.2 seconds;
- one pinned child and one running supervisor;
- clean runtime worktree at `59c334c0`;
- positions `[]`, orders `[]`;
- no failure event.

One `POST /api/arm` was sent at `2026-07-13T13:00:28.6218649Z`. The response was `ARMED`,
state version 4. The event database contains exactly one `ARM_REQUEST` followed by exactly one
`STATE_TRANSITION` with `DISARMED->ARMED`.

Post-ARM:

- reconcile `2026-07-13T13:01:32.783888Z`: ARMED, ready, positions/orders empty;
- reconcile `2026-07-13T13:02:34.431911Z`: ARMED, ready, positions/orders empty;
- supervisor and child remained running;
- no order was created merely by ARM.

## Next operation

D3 monitoring is active for at least 10 calendar days. Daily read-only checks must verify status,
WARN/ERROR events, reconcile freshness, equity continuity, positions, orders, and native stop
protection for any bridge-owned position. Any DISARM, critical code/config change, stale reconcile,
missing data restoration, or unexplained order state invalidates the uninterrupted Day 0 claim and
must be investigated before a newly approved restart/ARM.

