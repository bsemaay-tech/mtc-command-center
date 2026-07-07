# 03_STATUS - Crypto Paper Bridge corrective build status

Date: 2026-07-07
Branch: `feature/ibkr-bridge-final`
Builder: Codex GPT-5

## Fix status from `09_CODEX_FIX_PROMPT.md`

- FIX 1 - DONE: `BridgeEngine` and `OrderManager` now depend on the `Broker` protocol, not `MockBroker`. Replay consumes bars through `subscribe_bars`; acceptance test uses a fake broker without `.bars`.
- FIX 2 - DONE: Engine reads broker positions at bar start, passes the live position into the strategy, blocks new entries while positioned, and uses strategy-provided `stop_loss` / `take_profit`. Keltner now emits a channel-band initial stop.
- FIX 3 - DONE: MockBroker now has resting entry/SL/TP orders, next-bar entry fills, later-bar SL/TP triggers, reduce-only flatten, same-cloid stop modification, OrderManager reconciliation, store fill sync, and persisted signal-fingerprint duplicate protection.
- FIX 4 - DONE: `meta.app_state` persists DISARMED/ARMED/KILLED. API KILL survives restart until `/api/kill/ack`; engine re-reads persisted state and live position after awaited LLM gate before submit.
- FIX 5 - DONE: Hyperliquid adapter uses deterministic cloids, native `positionTpsl` trigger orders for SL/TP, trigger-shaped stop modify, and reduce-only market flatten through fake SDK tests. No exchange call was run.
- FIX 6 - PARTIAL: Dashboard now renders real rows, status metrics, `/api/bars` candles, WS snapshot rerender path, and verified screenshots at `docs/screenshots/overview.png` and `docs/screenshots/trading.png`. Remaining gap: the verified visible candle plot uses the local SVG fallback because the browser screenshot runtime rendered the Lightweight Charts CDN path as effectively blank; the CDN import remains but actual visible Lightweight rendering still needs a follow-up.
- FIX 7 - DONE: Removed the old exact scaffold chain assertion. Tests now assert required lifecycle stages and include a forced-close replay that records `TRADE_CLOSED`. Persisted duplicate guard is covered across DB reopen.

## Corrective commits

- `d431dfab` - `fix(bridge): decouple engine from mock broker`
- `3287f05c` - `fix(bridge): use strategy stops and live positions`
- `f1a7b6d1` - `fix(bridge): implement order lifecycle and duplicate guard`
- `873c44dc` - `fix(bridge): persist app state and guard submits`
- `ad361301` - `fix(bridge): place hyperliquid native triggers`
- `0a26ad9e` - `fix(bridge): render live dashboard data`
- `0f6e241d` - `test(bridge): assert real decision lifecycle`

## Verification

- `python -m pytest IBKR_PAPER_BRIDGE/tests -q`: 37 passed, 1 FastAPI/Starlette TestClient deprecation warning.
- Dry-run dashboard verification: patched app served on `127.0.0.1:8791`; `/api/status` returned numeric equity, day P&L, and next-bar; screenshots captured from the live page.
- Screenshots verified visually:
  - `IBKR_PAPER_BRIDGE/docs/screenshots/overview.png`
  - `IBKR_PAPER_BRIDGE/docs/screenshots/trading.png`

## Remaining gaps

- FIX 6 Lightweight Charts rendering should be repaired or replaced with a bundled/local chart asset so the visible chart does not depend on a CDN path that was blank in screenshot verification.
- `golden_signals.json` remains provisional; it was generated from the local fixture/reference flow, not a real QuantLens BTC 1h source run.
- P0 Hyperliquid testnet smoke remains approval-gated and was not run.
- No exchange API, LLM API, backtest, Pine, parity, or protected MCC strategy behavior was touched in this corrective pass.

## Human next steps

1. Review this status and the corrective commits before merge/continue.
2. Decide whether the SVG candle fallback is acceptable for P1 mock demo, or schedule a focused chart-library fix.
3. Prepare Hyperliquid testnet API wallet per `docs/06_HYPERLIQUID_SETUP.md`.
4. Approve or reject the separate P0 testnet smoke run.
