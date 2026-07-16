# 03_STATUS - Crypto Paper Bridge

Date: 2026-07-16. Branch: `feature/ibkr-bridge-final`.

## Gate status

- **P0: MET** (attempt 7; `docs/p0_smoke_log.json`).
- **P1: PASS**; B6 real fill/native-stop lifecycle PASS.
- **P2: DISARMED — Day 0 v4 ended 2026-07-15T20:22:44Z; timeout fix built, audit locked.**
- Runtime: Hyperliquid TESTNET, paper, BTC 1h, LLM regime/veto OFF.
- Pinned deployment: `C:\P2RT`, detached commit `1465f8f0`, Task Scheduler `MTC-Bridge-P2`.
- Runtime remains pinned at `1465f8f0`; build commit `79976577` is not deployed.
- Build tests: **132 passed, 1 warning** from both supported working directories.

## Data-restore timeout build; deployment locked

Day 0 v4 failed closed on `DATA_STALE reconnect_no_fresh_data` after a successful reconnect
did not produce a fresh bar within the unchanged 60-second restore deadline. Barış approved
raising only the application/configured deadline to 300 seconds. Commit `79976577` adds the
broker config value, wires it through `create_app` and `BridgeEngine`, clamps it to at least
30 seconds, and passes it to `BarFeed`; `bars.py`, notifications, reconcile behavior, and
trading logic are unchanged.

New deterministic tests prove a first fresh bar at 240 seconds restores without stale under
the 300-second setting, the explicit legacy 60-second setting still stales/disarms, a never-
fresh feed stales/disarms exactly once after 300 seconds, and YAML reaches the live `BarFeed`
instance. The final focused tests fail on pre-fix code (`1 failed, 2 passed`) and pass after the
fix (`3 passed`). Both full suites pass `132 passed, 1 warning` from both supported CWDs.

`C:\P2RT` is still clean and detached at `1465f8f0`. No deploy, restart, API call, or ARM was
performed. Fable audit PASS is required before the already-approved deploy window can begin.
Evidence: `MTC_COMMAND_CENTER/11_TRIAGE/P2_DATA_RESTORE_TIMEOUT_REPORT_2026-07-16.md`.

## Outage-tolerance deployment and Day 0 v4

Fable audited the outage-tolerance build PASS, and Barış authorized one deploy/re-ARM. Runtime
commit `1465f8f0` contains three-consecutive-failure reconcile tolerance, a config-driven
nine-attempt reconnect budget (315 seconds), and routine feed-event Telegram suppression.
The process was already down and port 8790 closed; `C:\P2RT` was checked out detached at the
audited tip. Both deployed-runtime suites passed `130 passed, 1 warning` before startup.

Run `paper-20260715105547` started DISARMED and reconcile-ready. The observation baseline was
`2026-07-15T10:56:23.8748664Z`; positions and orders were `[]`. The required natural cycle was:

`11:07:13.425338Z DISCONNECT -> 11:07:20.454025Z RECONNECT attempt=1 -> 11:07:21.465900Z DATA_RESTORED`.

The current run recorded no ERROR, `RECONCILE_FAILED`, or `DATA_STALE` event during the gate.
Fresh-bar proof was explicit: `/api/bars` advanced from the `10:00Z` bar (epoch `1784109600`)
to the newly persisted `11:00Z` bar (epoch `1784113200`) at `12:00:37.9423549Z`.

Exactly one ARM call used `X-Confirm: 2`:

`12:02:42.853744Z ARM_REQUEST state=DISARMED -> 12:02:42.856537Z DISARMED->ARMED`.

Clean post-ARM reconciles completed at `12:03:27.534022Z` and `12:04:28.442119Z`. The API
remained ARMED and reconcile-ready with positions/orders `[]`, exactly one ARM request, and
exactly one ARMED transition. The state transition invoked the existing `state -> ARMED`
Telegram path; the runtime does not expose a delivery receipt, so delivery is not claimed.

This Day 0 v4 window is policy validation, not definitive D3. The planned July 18 PC-off is an
expected window boundary, not a safety incident. The definitive uninterrupted D3 clock starts
after the end-of-month VPS migration.

## Reconnect/reconciler race fix and Day-0 reset

The 2026-07-13 Day-0 run auto-disarmed at `16:46:42Z` when the periodic reconciler landed
inside the dead-websocket SDK rebuild window. The old reconnect path temporarily set
`self.info`/`self.exchange` to `None`, so `positions()` raised
`HyperliquidNotConfigured` and the correct single-strike fail-closed handler disarmed the
otherwise healthy run. Fable audited the fix PASS and Barış approved one deploy/re-arm window,
including the PR #16 push.

Runtime commit `cc4ce67d` includes race-fix commit `da44d1ff`, the Telegram test-isolation
fixture, and the entry golden. The fix builds replacement clients locally, restores candle
subscriptions before one tuple swap, and disconnects the old dead websocket only afterward.
Defense in depth defers only `HyperliquidNotConfigured` while `broker.rebuilding`; all other
exceptions retain single-strike fail-closed behavior.

Before shutdown the API was DISARMED with positions/orders `[]`. `Stop-ScheduledTask` stopped
the supervisor but left Python child PID `54192` listening, so that identified orphan child was
terminated once before checkout. Port 8790 was confirmed closed; `C:\P2RT` was then checked out
detached at `cc4ce67d` with no diff. Both deployed-runtime suites passed `127 passed, 1 warning`.

New run `paper-20260715063657` started DISARMED and reconcile-ready. The observation window ran
from `06:37:13Z` through `06:47:42Z`, stayed flat, and recorded no ERROR,
`RECONCILE_FAILED`, or `RECONCILE_DEFERRED` event. The required natural cycle was:

`06:47:06.153686Z DISCONNECT -> 06:47:14.370206Z RECONNECT attempt=1 -> 06:47:39.560468Z DATA_RESTORED`.

A clean reconcile at `06:47:26.646538Z` landed inside that reconnect interval, directly
exercising the repaired race window without failure or defer.

Exactly one ARM call used `X-Confirm: 2`:

`06:48:16.616853Z ARM_REQUEST state=DISARMED -> 06:48:16.619336Z DISARMED->ARMED`.

The Telegram notifier was enabled and the state transition invoked the existing
`state -> ARMED` notification path; the bridge does not persist a delivery receipt. Clean
post-ARM reconciles completed at `06:48:28.376718Z` and `06:49:29.975312Z`. At the final
deployment check the API remained ARMED and reconcile-ready with positions/orders `[]`, one
ARM request, one ARMED transition, and zero ERROR/reconcile-failure/defer events. The
`DISARMED->ARMED` transition timestamp above resets the P2 monitoring clock to Day 0.

## EMA-8 correction and Day-0 reset

Approved bridge-only correction `f209acd2` replaced the mislabeled SMA-8 trail with the exact
QuantLens EMA convention from `mega_walk_forward.py`: `span=8`, `adjust=False`,
`min_periods=8`, alpha `2/(8+1)`, first-close recursive seed, and the full available close
history. Entry-band logic and the entry golden were unchanged. A fixed synthetic case proves
EMA `68.64558996000855` versus last-eight SMA `65.0`; long, short, and insufficient-history
guards are covered. The changed-file 64+-hex secret scan returned zero matches.

The prior Day-0 run had already auto-disarmed at `13:29:59Z` after
`DATA_STALE reconnect_no_fresh_data`; positions and orders were `[]` before deployment. One
approved deploy cycle was performed: `DISARM_REQUEST` at `15:06:33Z`, supervised child PID
`81788` stopped, new run `paper-20260713150651` started DISARMED, and reconcile was ready at
`15:06:59Z`. The new run then remained DISARMED, flat, and reconcile-clean for ten minutes.

Exactly one ARM call used `X-Confirm: 2`:

`15:17:05.377321Z ARM_REQUEST state=DISARMED -> 15:17:05.383618Z DISARMED->ARMED`.

Telegram visibly recorded `[INFO] state -> ARMED`. The first post-ARM natural cycle passed:
`15:18:06Z DISCONNECT -> 15:18:13Z RECONNECT attempt=1 -> 15:18:14Z DATA_RESTORED`.
Afterward the API remained ARMED and reconcile-ready with fresh reconcile `15:18:13Z`, no
reconcile error, positions `[]`, and orders `[]`. This ARM timestamp resets the P2 monitoring
clock to Day 0.

## Reconnect incident resolution

The earlier duplicate-user-subscription `NotImplementedError`, ambiguous ARM history, and dead
reconciler incident was contained while DISARMED with zero exchange exposure. The fixed pinned
runtime passed a real natural cycle:

`12:57:21Z DISCONNECT -> 12:57:29Z RECONNECT -> 12:57:39Z DATA_RESTORED`, followed by two
successful reconciles. ARM was then called exactly once. Two post-ARM reconciles remained ARMED
with positions/orders empty.

Full evidence: `docs/19_P2_RECONNECT_INCIDENT_2026-07-13.md`.

## Active phase

Fable audit of build commit `79976577`. Keep the runtime DISARMED and `C:\P2RT` pinned at
`1465f8f0`. Do not deploy, restart, or ARM before an independent PASS. After PASS, use the
existing single-window testnet deploy runbook with both-CWD tests, a full fresh-bar gate, and
exactly one authorized ARM. Definitive D3 begins on the VPS; mainnet remains forbidden.

## Deferred (post-P2)
- Store-chain proof of a full engine trade (P2 first real trade will provide it).
- QuantLens I4 registration and the real golden fixture are **COMPLETE**: 858/858 entry signals
  match over 48,077 BTCUSD 1h bars; run id
  `QL_MEGA_KELTNER_TRAIL_EMA8_BTCUSD_1h_2026-06-28_01a3f1255e29`. Evidence:
  [`18_GOLDEN_REPORT.md`](18_GOLDEN_REPORT.md).
- The later bridge correction `f209acd2` aligns the trail calculation with QuantLens EMA-8.
  The golden still proves entry-signal parity only; broader exit-execution parity is not claimed.
- P3's slippage and operational parity report remains post-P2 and requires at least 30 days.
