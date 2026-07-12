# 03_STATUS - Crypto Paper Bridge P1 build

Date: 2026-07-12
Branch: `feature/ibkr-bridge-final`
Builder: Codex GPT-5

## Current verdict

- **P1 local MockBroker gate: PASS.** Continuous background replay, real Store/API/WS wiring,
  live dashboard, and all eight failure drills are verified locally.
- **P0 Hyperliquid testnet gate: FAIL before order acceptance.** Credential format, connection,
  account query, live candles, metadata, and bounded sizing passed. Perps equity was `0.0`; a
  read-only follow-up found all `999.0` mock USDC in Spot. No oid/cloid was returned, and the
  post-failure check found zero positions and zero open orders. See `14_P0_SMOKE_REPORT.md`.
- **Real QuantLens golden: BLOCKED.** The canonical engine does not register
  `keltner_trail_ema8`; the available `GEN_KELTNER_BREAKOUT` has materially different rules and was
  not substituted. The golden remains explicitly provisional.
- **P2: NOT STARTED / NOT APPROVED.** No autonomous testnet trading was run.

## Build task status

| Task | Status | Evidence |
|---|---|---|
| T1 SDK contract | DONE locally | Typed cloids; atomic `bulk_orders(positionTpsl)`; real modify/cancel signatures; SDK-autospec tests. |
| T2 typed normalization | DONE | `AccountSnapshot`, `Position`, and `BrokerOrder` parity tests across brokers. |
| T3 async safety | DONE | Sync SDK calls use `asyncio.to_thread`; thread-identity test. |
| T4 BarFeed | PARTIAL | Timer finalization, warmup, dedupe, staleness, and reconnect/resubscribe path implemented. Automatic SDK socket-drop notification remains unverified/unwired. |
| T5 order events/reconcile | PARTIAL | No mock-internal reads; typed fill/order events; cloid matching; owned re-protect/flatten and foreign ignore; equity snapshots. `order_ref` and conservative attribute fallback matching remain. |
| T6 continuous engine | DONE for P1 | Background runtime, safe startup, reconcile-before-ARM, trailing while disarmed, close-only opposite signal, risk disarm, preemptive KILL. |
| T7 API/WS | DONE for P1 | Runtime controls, Store-backed endpoints, persistent WS, snapshot resync, live decision stream. |
| T8 failure drills | DONE | Eight scripted drills pass. |
| T9 CWD robustness | DONE | 67 tests pass from repo root and bridge directory. |
| T10 chart | DONE | Local SVG candle renderer only; live screenshots verified. |
| T11 P0 smoke | FAIL / BLOCKED | Connected and fetched candles, but Perps collateral was zero; Spot held 999 mock USDC. No oids/cloids; zero open orders after failure. |
| T12 real golden | BLOCKED | `docs/12_GOLDEN_REGEN_ATTEMPT.md`; exact strategy ID absent. |
| T13 report/handoff | DONE | `docs/11_P1_BUILD_REPORT.md` plus canonical handoff entry. |

## Verification

- Repo-root suite: `67 passed, 1 warning`.
- Bridge-directory suite: `67 passed, 1 warning`.
- `node --check IBKR_PAPER_BRIDGE/bridge/static/app.js`: pass.
- Live mock UI: `DRY_RUN`, `ARMED`, `$100000.00`, 80 visible candle bodies, 10 decision rows,
  no CDN scripts.
- Secret scan: no 64-hex private key or private-key material found in bridge artifacts.
- Mainnet: never contacted; `HL_LIVE_ACK` was explicitly unset for the P0 attempt.

## Human next actions

1. On Hyperliquid **testnet**, manually move mock USDC from Spot to Perps using `Perps <-> Spot`.
   Do not place a manual trade and do not touch mainnet.
2. Confirm Perps collateral read-only, fix safe string-response handling and SDK disconnect, then
   separately approve a new P0 attempt. This failure was not transient, so no automatic retry is allowed.
3. P2 remains a later go/no-go decision and is not approved.
4. For a real golden, register the exact bridge Keltner signal semantics in QuantLens or approve a
   source-engine export adapter; do not relabel `GEN_KELTNER_BREAKOUT` as equivalent.
