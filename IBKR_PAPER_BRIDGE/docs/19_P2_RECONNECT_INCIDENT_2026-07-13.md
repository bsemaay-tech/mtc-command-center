# P2 Reconnect Safety Incident — 2026-07-13

> **RESOLVED / SUPERSEDED:** After this containment record was written, Barış approved the repair
> and first ARM. The pinned `C:\P2RT` runtime at `59c334c0` passed both full suites (`119 passed`)
> and was ARMED at `2026-07-13T13:00:28.6218649Z`, but that run auto-disarmed at `13:29:59Z` on
> `DATA_STALE`. Barış then approved the EMA-8 correction `f209acd2` and one deploy/re-ARM cycle.
> Both suites passed with `121 passed`; the current P2 Day 0 is
> **`2026-07-13T15:17:05.383618Z`**, recorded at the pre-consolidation branch tip `54278b66`.
> The historical containment narrative below is preserved unchanged.

## Final verdict

**INCIDENT CONTAINED — DISARMED**

No ARM request was issued during this investigation. At the final live check the bridge was
`DISARMED` on Hyperliquid testnet, and the exchange-backed position and open-order endpoints both
returned `[]`. No process was restarted or terminated.

ARM remains blocked. The currently loaded child contains the reconnect fix, but the shared
working tree no longer does; the next supervisor restart would load the pre-fix implementation.
The reconciler also stopped writing equity evidence while `reconcile_ready` remained true.

## Evidence capture

Captured before any mutation:

- Task Scheduler: one task, `MTC-Bridge-P2`, state `Running`.
- Supervisor: PID `89596`, started `2026-07-13 08:52:42 +03:00`, Windows PowerShell,
  `tools/run_bridge_p2.ps1`.
- Bridge child: PID `65384`, parent `89596`, started
  `2026-07-13 11:24:54 +03:00`, `C:\Python314\python.exe -m bridge.app`.
- Listener: PID `65384`, `127.0.0.1:8790`, created
  `2026-07-13 11:25:06 +03:00`.
- Working directory: the supervisor script executes `Set-Location` to
  `C:\LAB\Tradingview_LAB_CLEAN\IBKR_PAPER_BRIDGE` before starting the child.
- Runtime config: `config/bridge.yaml`; strategy config:
  `config/strategies/keltner_trail_ema8.yaml`.
- Runtime identity: `paper`, `testnet`, Hyperliquid, BTC, 1h; run
  `paper-20260713082455`, started `2026-07-13T08:24:56.304652Z`.
- No second bridge task, supervisor, child, or `:8790` listener was found. The other Python
  process was the unrelated read-only MCC dashboard.

Final live API response:

```json
{"state":"DISARMED","mode":"paper","network":"testnet","exchange_conn":"hyperliquid","regime":"BOTH","state_version":2,"reconcile_ready":true,"run_id":"paper-20260713082455","coin":"BTC","timeframe":"1h"}
```

`GET /api/positions` returned `[]`; `GET /api/orders` returned `[]`. These routes call the live
broker's `positions()` and `open_orders()` methods, so they cover bridge-owned and foreign
exchange state. Native protective-order validation is not applicable because there is no open
position.

## Loaded-code proof and restart hazard

Commit `29d9879ff8100a7ae104a1de55961da6f961046b` was committed at
`2026-07-13 11:24:31 +03:00`. The supervisor launched PID `65384` at `11:24:54`; the server was
listening by `11:25:06`. A parallel repo checkout then replaced
`bridge/broker/hyperliquid.py` at `11:25:23`.

Therefore PID `65384` imported the `29d9879f` implementation before the replacement. Runtime
behavior corroborates this: the prior child recorded `RECONNECT_RETRY ... NotImplementedError`,
whereas PID `65384` has recorded 18 first-attempt `RECONNECT` events and zero
`RECONNECT_RETRY`/`NotImplementedError` events.

The current file is not the fixed file:

- working-tree/current-HEAD blob: `47cca178c59a704c62eb27a92afddd667f571cb2`;
- `29d9879f` blob: `7f9da14c5493a3a62edcb9024c4f0b03e031d393`.

The active branch at capture was `feature/donchian-crypto-ladder`, HEAD
`51445a08fe3994226413eb269febc5681fe45e44`; that branch does not contain `29d9879f`. A future
supervisor restart is consequently unsafe for ARM until deployment is pinned to reviewed code.

## Exact NotImplementedError path

The application did not persist a Python traceback: `BarFeed.reconnect()` catches `Exception` and
stores only `type(exc).__name__`. The exact call chain is nevertheless proven from the pre-fix
source and installed SDK:

1. `BarFeed.reconnect()` calls `await broker.connect()` and then `await broker.resubscribe()`.
2. `connect()` rebuilt the client and subscribed the user channels.
3. The pre-fix `resubscribe()` called `Info.subscribe({"type":"userEvents", ...})` again.
4. Installed `hyperliquid/websocket_manager.py:148` raises
   `NotImplementedError("Cannot subscribe to userEvents multiple times")` when that identifier
   already has an active subscription.

`29d9879f` makes user-channel resubscription flag-guarded and moves candle restoration to the
fresh-client build path.

## Disconnect/reconnect reconstruction

The failed pre-fix run `paper-20260713055252` had two failed cycles:

- `08:04:33Z` disconnect; attempts 1–5 failed with `NotImplementedError`; `DATA_STALE` at
  `08:06:05Z`.
- `08:15:31Z` disconnect; attempts 1–5 failed with `NotImplementedError` through `08:17:02Z`.

Corrected run `paper-20260713082455`:

| Disconnect (UTC) | RECONNECT (UTC) | Delay s | Result |
|---|---|---:|---|
| 08:35:28.280944 | 08:35:40.211655 | 11.931 | attempt=1 |
| 08:47:08.673310 | 08:47:16.447796 | 7.774 | attempt=1 |
| 08:58:16.043579 | 08:58:23.182683 | 7.139 | attempt=1 |
| 09:09:21.746025 | 09:09:29.485340 | 7.739 | attempt=1 |
| 09:21:00.820760 | 09:21:12.643005 | 11.822 | attempt=1 |
| 09:32:29.553178 | 09:32:40.304358 | 10.751 | attempt=1 |
| 09:43:59.013479 | 09:44:07.021299 | 8.008 | attempt=1 |
| 09:55:05.378214 | 09:55:13.171799 | 7.794 | attempt=1 |
| 10:05:41.279551 | 10:05:50.272792 | 8.993 | attempt=1 |
| 10:16:35.613082 | 10:16:43.805335 | 8.192 | attempt=1 |
| 10:28:12.535479 | 10:28:20.008637 | 7.473 | attempt=1 |
| 10:38:31.984216 | 10:38:41.714758 | 9.731 | attempt=1 |
| 10:48:34.662633 | 10:48:46.409131 | 11.746 | attempt=1 |
| 10:59:01.453042 | 10:59:09.977275 | 8.524 | attempt=1 |
| 11:10:27.241502 | 11:10:35.521605 | 8.280 | attempt=1 |
| 11:22:05.423591 | 11:22:12.624403 | 7.201 | attempt=1 |
| 11:32:42.850546 | 11:32:51.614400 | 8.764 | attempt=1 |
| 11:43:51.958784 | 11:43:58.358528 | 6.400 | attempt=1 |

The corrected run has no `DATA_STALE`, retry, or NotImplemented event. Closed 1h bars exist at
`08:00Z`, `09:00Z`, and `10:00Z`, proving post-start market-data progress. The absence of a
Telegram success message is an observability defect: `RECONNECT` is classified INFO and
`_feed_event()` sends Telegram only for non-INFO events, while every `DISCONNECT` is WARN.

## ARM notification reconstruction

The two Telegram messages cannot be one notifier delivery retried twice: the notifier has no
retry loop, and `state -> ARMED` is emitted only when `_set_state()` sees an actual state change.
Startup also resets non-KILLED state to `DISARMED` and does not emit ARMED. The supervisor log
proves an old child exited at `11:24:44 +03:00` and PID `65384` started at `11:24:54`, between the
11:24 and 11:27 Telegram messages.

The most consistent reconstruction is two separate DISARMED-to-ARMED transitions—one on each
side of the restart, normally caused by two ARM API calls. However, Uvicorn access logs contain no
retained POST record and state transitions are not stored in the events table, so the caller and
request IDs cannot be proven. This observability gap prevents treating the ARM history as clean.
There is no evidence of two simultaneously running bridge children in the retained process and
supervisor records.

## Duplicate and scheduler checks

For corrected run `paper-20260713082455`:

- decisions: 0;
- signal fingerprints: 0;
- trades: 0;
- current-run orders: 0;
- duplicate stored bar keys: 0;
- duplicate decision UIDs/fingerprints: 0;
- duplicate equity timestamps: 0;
- active bridge schedulers/children: one each.

There is therefore no evidence of duplicate bars, signals, order requests, or repeated reconciler
actions. There is instead a reconciler liveness failure: equity rows stop at
`2026-07-13T10:47:34.360627Z`, over one hour before the incident check, while the status endpoint
still reports `reconcile_ready=true`. The readiness flag is not proof that the recurring task is
alive.

## Required next gate

Do not ARM. Before any new approval is requested:

1. Pin the supervisor to an isolated, reviewed deployment containing `29d9879f` or a reviewed
   descendant; eliminate shared-worktree branch flips from runtime deployment.
2. Diagnose and test the stopped reconciler task and make readiness reflect task liveness.
3. Persist state-transition request/audit records and emit explicit reconnect/data-restored
   notifications.
4. Restart only into `DISARMED`, confirm zero exchange exposure, and observe a complete natural
   expiry/reconnect cycle with fresh closed-bar data and continuing reconciler evidence.
5. Obtain fresh Baris approval before any ARM operation.
