# 03_STATUS - Crypto Paper Bridge

Date: 2026-07-13. Branch: `feature/ibkr-bridge-final`.

## Gate status

- **P0: MET** (attempt 7; `docs/p0_smoke_log.json`).
- **P1: PASS**; B6 real fill/native-stop lifecycle PASS.
- **P2: ARMED — DAY 0 STARTED 2026-07-13T13:00:28.6218649Z.**
- Runtime: Hyperliquid TESTNET, paper, BTC 1h, LLM regime/veto OFF.
- Pinned deployment: `C:\P2RT`, commit `59c334c0`, Task Scheduler `MTC-Bridge-P2`.
- Tests: **119 passed, 1 warning** from both supported working directories.

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

Do not change code or frozen P2 config during the window except for a critical safety incident.
Any DISARM or critical runtime change requires investigation and resets the uninterrupted window.
Mainnet remains forbidden.

