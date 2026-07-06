# Crypto Paper Bridge (Hyperliquid) — standalone live/paper execution dashboard

**Status: DESIGN ONLY. No code yet. Running anything against the exchange (even testnet) requires Barış approval per `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MTC_REPO_GUARD_PROTOCOL.md`.**

> Directory is named `IBKR_PAPER_BRIDGE/` for git-history continuity only. The broker decision was
> finalized on 2026-07-06 to **Hyperliquid** (testnet = paper). IBKR and Signum were evaluated and
> NOT chosen — see `docs/07_BROKER_DECISION.md`.

Standalone app (independent from MTC Command Center) that takes ONE formal strategy and runs it
against a **Hyperliquid** account (testnet first), with a professional web dashboard for
configuration (strategy, coin, direction, risk %, leverage, SL/TP, money management) and live
monitoring. LLM layer is **veto/regime-only** — it never originates orders.

## Read order (for the builder — Opus/Codex)

1. `docs/00_PREREG.md` — pre-registration: goals, gates, success/abort criteria. Binding.
2. `docs/01_ARCHITECTURE.md` — full system design: components, schemas, safety rails, API.
3. `docs/05_AUDIT_RESOLUTION.md` — what the 7 external audits changed and why.
4. `docs/02_BUILD_PLAN_1DAY.md` — ordered task list with acceptance criteria (now a 2-day plan).
5. `docs/06_HYPERLIQUID_SETUP.md` — how to prepare the testnet account + API wallet.
6. `docs/07_BROKER_DECISION.md` — why Hyperliquid; why not IBKR / Signum.

## Non-negotiable principles (from Barış)

1. **Formal rule decides.** Strategy engine produces signal + size + SL/TP. Deterministic, config-driven.
2. **LLM can only reduce risk, never increase it.** Allowed LLM outputs: regime directive
   (LONG_ONLY / SHORT_ONLY / BOTH / NO_TRADE), pre-trade veto, flags. LLM cannot open trades,
   increase size, raise leverage, or widen stops. LLM unavailable → fail-open to formal rule.
3. **Paper (testnet) first.** `network: testnet` is the default; `mainnet` (real money) requires a
   triple-lock (`--enable-live` CLI + `HL_LIVE_ACK` env + strategy `live_allowed: true`).
4. **API wallet cannot withdraw** — use a Hyperliquid agent/API wallet, never the main key.
5. **Native resting SL/TP** — stops are real orders on the exchange (protect even if the bridge dies).
6. **Every decision logged as JSON** (signal, risk check, LLM directive, order, fill) — auditable.
7. **Kill switch always one click away** — cancels all open orders, optionally flattens, disarms.
8. **Independent from MCC** — no runtime imports; strategy parameters are *copied* from research,
   never live-linked.
