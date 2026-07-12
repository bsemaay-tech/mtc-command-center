# 03_STATUS - Crypto Paper Bridge P1 build

Date: 2026-07-12
Branch: `feature/ibkr-bridge-final`
Builder: Codex GPT-5

## Current verdict

- **P1 local MockBroker gate: PASS.** Continuous background replay, real Store/API/WS wiring,
  live dashboard, and all eight failure drills are verified locally.
- **P0 Hyperliquid testnet gate: BLOCKED before connection.** `HL_API_WALLET_KEY` is present but
  the SDK reports that it decodes to 20 bytes rather than the required 32 bytes. No testnet query,
  order, modification, cancellation, fill, or flatten occurred.
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
| T9 CWD robustness | DONE | 54 tests pass from repo root and bridge directory. |
| T10 chart | DONE | Local SVG candle renderer only; live screenshots verified. |
| T11 P0 smoke | BLOCKED | `docs/p0_smoke_log.json`; invalid key length before connection; no oids/cloids. |
| T12 real golden | BLOCKED | `docs/12_GOLDEN_REGEN_ATTEMPT.md`; exact strategy ID absent. |
| T13 report/handoff | DONE | `docs/11_P1_BUILD_REPORT.md` plus canonical handoff entry. |

## Verification

- Repo-root suite: `54 passed, 1 warning`.
- Bridge-directory suite: `54 passed, 1 warning`.
- `node --check IBKR_PAPER_BRIDGE/bridge/static/app.js`: pass.
- Live mock UI: `DRY_RUN`, `ARMED`, `$100000.00`, 80 visible candle bodies, 10 decision rows,
  no CDN scripts.
- Secret scan: no 64-hex private key or private-key material found in bridge artifacts.
- Mainnet: never contacted; `HL_LIVE_ACK` was explicitly unset for the P0 attempt.

## Human next actions

1. Replace `HL_API_WALLET_KEY` with the dedicated `MTC-bridge-test` agent-wallet **private key**
   (32 bytes / 64 hex characters, normally `0x` plus 64 hex characters). Do not paste it into chat.
2. Start a fresh Codex process so the corrected Windows user variable is inherited.
3. Re-audit this build, then separately approve a P0 retry. P2 remains a later go/no-go decision.
4. For a real golden, register the exact bridge Keltner signal semantics in QuantLens or approve a
   source-engine export adapter; do not relabel `GEN_KELTNER_BREAKOUT` as equivalent.
