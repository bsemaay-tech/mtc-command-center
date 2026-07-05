# IBKR Paper Bridge — standalone live/paper execution dashboard

**Status: DESIGN ONLY. No code yet. Running anything against a broker (even paper) requires Barış approval per `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MTC_REPO_GUARD_PROTOCOL.md`.**

Standalone app (independent from MTC Command Center dashboard) that takes ONE formal strategy,
runs it against Interactive Brokers **paper** account (TWS port 7497), with a professional
web dashboard for configuration (strategy, symbol, direction, risk %, SL/TP, money management)
and live monitoring. LLM layer is **veto/regime-only** — it never originates orders.

## Read order (for the builder — Opus/Codex)

1. `docs/00_PREREG.md` — pre-registration: goals, gates, success/abort criteria. Binding.
2. `docs/01_ARCHITECTURE.md` — full system design: components, schemas, safety rails, API.
3. `docs/02_BUILD_PLAN_1DAY.md` — ordered task list with acceptance criteria. Build in this order.

## Non-negotiable principles (from Barış, 2026-07-05)

1. **Formal rule decides.** Strategy engine produces signal + size + SL/TP. Deterministic, config-driven.
2. **LLM can only reduce risk, never increase it.** Allowed LLM outputs: regime directive
   (LONG_ONLY / SHORT_ONLY / BOTH / NO_TRADE), pre-trade veto, flags. LLM cannot open trades,
   increase size, or widen stops. LLM unavailable → fail-open to formal rule (configurable to fail-closed).
3. **Paper first.** Port 7497 hardcoded default; live port 7496 refuses to connect unless
   `IBKR_LIVE_ACK=I_UNDERSTAND_THIS_IS_REAL_MONEY` env var AND dashboard double-confirm.
4. **Every decision logged as JSON** (signal, risk check, LLM directive, order, fill) — auditable.
5. **Kill switch always one click away** — cancels all open orders, optionally flattens, disarms.
6. **Independent from MCC** — no runtime imports from `MTC_COMMAND_CENTER/`; strategy parameters
   are *copied* from research results, never live-linked.
