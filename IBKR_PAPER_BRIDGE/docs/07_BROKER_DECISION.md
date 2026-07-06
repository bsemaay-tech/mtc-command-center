# 07 — Broker Decision Record (2026-07-06)

Decision: **the live/paper broker for v1 is Hyperliquid (testnet = paper).** IBKR and Signum were
evaluated and NOT chosen. TradingView as a live-signal source was considered and rejected. This
record exists so the choice is not re-litigated on build day.

Decided by Barış after examining the Signum product (site + FAQ + 3 walkthrough videos) and testing
IBKR account signup. Broker abstraction (`Broker` protocol, `01_ARCHITECTURE §6.1`) means this is a
connector choice, not a redesign.

---

## Options evaluated

### IBKR (Interactive Brokers) — CLOSED
- **Blocker:** North-Cyprus (KKTC) address verification failed at signup. IBKR is a regulated broker
  with strict KYC; the "Cyprus" designation is the Republic of Cyprus (south), and KKTC addresses do
  not clear.
- **Also against:** requires the TWS / IB Gateway desktop terminal running alongside the bridge
  (ports, nightly restarts, order-precaution popups) — the source of most of the original design's
  complexity. Equities are not the current priority.
- **Status:** not pursued. Re-evaluate only if the user obtains a workable IBKR account and
  specifically wants US equities.

### Signum (signum.money) — EVALUATED, NOT CHOSEN
- **What it is:** a $25/mo execution-relay service (14-day free trial). Signal-source-agnostic:
  triggers bots from TradingView, an AI/MCP prompt, or your own API/webhook. Supports Binance,
  Hyperliquid, and many others. Provides a "Trend Radar" (breakout scan) and sells prompt
  strategies. **You CAN run your own strategy** (TradingView alert or webhook); order size supports
  both "100%" (all-in) and "let strategy decide" (absolute size), and developers can send a fully
  custom JSON (including % sizing).
- **Why not chosen for OUR design:**
  1. **No native resting stop.** Signum places **MARKET orders only**; SL/TP are "synthetic" — your
     strategy fires an alert and Signum sends a market exit (5–10 s latency, single point of
     failure). Our design's #1 safety rail is a real resting stop order on the exchange. If the
     automation/connection dies while in a position, Signum leaves you unprotected. On leveraged
     crypto that is a liquidation risk.
  2. **Routing our engine through it neuters the risk engine.** Even with "let strategy decide"
     sizing, Signum's execution granularity (market-only, no native bracket/trigger) cannot carry
     our exact-qty + resting-SL + TP + trailing-modify + reduce-only model. We'd end up paying
     $25/mo to downgrade our design to a plain long/short/flat relay.
  3. Vendor dependency + monthly fee + an autonomous cloud path that (in its marketed mode) hands an
     LLM order authority — the opposite of our veto-only principle.
- **Where Signum still has value (NOT part of this design):** as a separate, cheap, fast way to SEE
  live crypto execution and learn the Claude-MCP-routine pattern with bounded risk (free trial,
  minimum funds, low leverage). That is an optional side experiment, not the bridge.
- **Status:** not chosen. Kept in mind as a possible quick-start experiment only.

### TradingView as a live-signal source — REJECTED
- Our design has the **Python engine as the signal source**; TradingView/Pine stays a **parity /
  control layer** (offline comparison), never the live signal path. Using TV alerts as the live
  trigger is the older, simpler architecture we deliberately moved past.

### Hyperliquid (direct API) — CHOSEN
- **API-first:** official `hyperliquid-python-sdk`, REST + WebSocket. **No desktop terminal** — the
  engine talks straight to the exchange. This deletes the entire IBKR TWS/Gateway complexity class
  (ports, nightly restart recovery, order-precaution popups, session/RTH bar handling).
- **Native resting SL/TP triggers:** real reduce-only trigger orders on the book (`positionTpsl`
  grouping) — the position stays protected even if the bridge process dies. This is the exact safety
  property Signum lacks.
- **Testnet = paper:** a full fake-money environment for P0-P3 gates.
- **24/7:** no market hours, no holiday/half-day calendar, no session-end bar special case → the
  design and the P2 "unattended days" gate both simplify, and live execution is visible sooner
  (the motivation goal).
- **API wallet cannot withdraw:** the agent-wallet model means a compromised bridge still cannot
  move funds — a strong built-in money-safety rail.
- **Already available to the user** (has a Hyperliquid account), crypto-only is acceptable for now,
  and it fits the broker-abstracted design with the least loss of the risk engine.
- **Deployment win:** because it is a pure API, the engine later runs directly on a ~$5/mo VPS 24/7
  — no hybrid local-bridge needed (unlike IBKR).

---

## What this changes in the design docs (all AMENDED in place 2026-07-06)

- `README.md`, `00_PREREG.md`, `01_ARCHITECTURE.md`, `02_BUILD_PLAN_1DAY.md` rewritten from
  IBKR/TWS/AAPL/RTH/ports → Hyperliquid/testnet/BTC/24-7/API-wallet/native-triggers.
- `06_TWS_SETUP.md` → replaced by `06_HYPERLIQUID_SETUP.md`.
- Broker abstraction unchanged; `IBKRBroker` notes → `HyperliquidBroker` contract.
- Binance connector remains a v2 roadmap item (same `Broker` seam) if a second venue is wanted.

Directory name `IBKR_PAPER_BRIDGE/` is kept for git continuity only; the product is the **Crypto
Paper Bridge**.
