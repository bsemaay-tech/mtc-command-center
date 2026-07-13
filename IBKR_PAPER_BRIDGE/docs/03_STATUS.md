# 03_STATUS - Crypto Paper Bridge

Date: 2026-07-13. Branch: `feature/ibkr-bridge-final`.

## Gate status

- **P0: MET** (attempt 7; `docs/p0_smoke_log.json`).
- **P1: PASS**; B6 real fill/native-stop lifecycle PASS.
- **P2: ARMED — NEW DAY 0 STARTED 2026-07-13T15:17:05.383618Z.**
- Runtime: Hyperliquid TESTNET, paper, BTC 1h, LLM regime/veto OFF.
- Pinned deployment: `C:\P2RT`, commit `f209acd2`, Task Scheduler `MTC-Bridge-P2`.
- Tests: **121 passed, 1 warning** from both supported working directories.

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

Phase D3: monitor continuously for at least 10 calendar days. Daily read-only checks:

- `/api/status`: ARMED, `reconcile_ready=true`, recent `last_reconcile_ts`, no error;
- WARN/ERROR events and every disconnect/reconnect/data-restored chain;
- exchange positions and orders; every owned position must have a valid native stop;
- equity continuity and unexplained order-state checks;
- process/supervisor stability and pinned commit identity.

Do not change code or frozen P2 config during the new window except for a critical safety incident.
Any DISARM or critical runtime change requires investigation and resets the uninterrupted window.
Mainnet remains forbidden.

## Deferred (post-P2)
- Store-chain proof of a full engine trade (P2 first real trade will provide it).
- QuantLens I4 registration and the real golden fixture are **COMPLETE**: 858/858 entry signals
  match over 48,077 BTCUSD 1h bars; run id
  `QL_MEGA_KELTNER_TRAIL_EMA8_BTCUSD_1h_2026-06-28_01a3f1255e29`. Evidence:
  [`18_GOLDEN_REPORT.md`](18_GOLDEN_REPORT.md).
- The later bridge correction `f209acd2` aligns the trail calculation with QuantLens EMA-8.
  The golden still proves entry-signal parity only; broader exit-execution parity is not claimed.
- P3's slippage and operational parity report remains post-P2 and requires at least 30 days.
