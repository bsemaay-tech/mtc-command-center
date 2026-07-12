# 03_STATUS - Crypto Paper Bridge

Date: 2026-07-13 (early). Branch: `feature/ibkr-bridge-final`.

## Gate status
- **P0: MET** (attempt 7, all 12 steps; `docs/p0_smoke_log.json`).
- **P1: PASS** (audited). **B6 fill smoke: PASS** (real fill 64110 -> positionTpsl SL rested ->
  reduce-only close 64098; `docs/fill_smoke_log.json`).
- **P2: READY TO ARM.** All B and C tasks complete (see 16_GO_LIVE_PLAN.md checkboxes). The
  supervised paper instance is RUNNING via Task Scheduler `MTC-Bridge-P2` (crash-restart proven),
  DISARMED, reconcile clean, real warmup bars, live equity 998.99 USDC.
- Tests: **110 passed** both CWDs.

## Last step before ARM (D2)
Observe ONE live hourly bar close on the paper instance (expected 22:00 UTC 2026-07-12 or the
next boundary) via `/api/bars` gaining a new 64k-range bar -> then POST /api/arm (pre-approved,
plan §0-4). If this session ended, any model: verify the new bar exists, then ARM per plan D2.

## Operating notes for the P2 window
- Do NOT change config (`bridge.yaml` frozen C3 profile; LLM regime OFF).
- Supervisor: Task Scheduler `MTC-Bridge-P2` (logon trigger + crash loop). Logs:
  `IBKR_PAPER_BRIDGE/data/logs/bridge_YYYYMMDD.log`.
- Telegram notifier LIVE (state changes, WARN+ events, 6h heartbeat).
- Human items: I2 PC must stay awake 24/7 (Baris); mainnet forbidden (I3).

## Deferred (post-P2)
- Store-chain proof of a full engine trade (P2 first real trade will provide it).
- Golden/parity (P3): needs QuantLens registration (I4).
