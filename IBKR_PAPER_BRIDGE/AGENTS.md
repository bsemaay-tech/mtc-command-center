# AGENTS.md - Crypto Paper Bridge Component

Inherits root two-tier model, canonical audit roster, safety gates, and parallel-agent safety
from [root AGENTS.md](../AGENTS.md). Read root AGENTS.md first.

## Routing

This component's onboarding chain:
`IBKR_PAPER_BRIDGE/AGENTS.md` -> `_AI_MEMORY/START_HERE.md` -> `_AI_MEMORY/CURRENT.md` -> `_AI_MEMORY/NEXT_STEPS.md`

Do NOT load root volatile histories for component-scoped tasks.

## Identity

Directory named `IBKR_PAPER_BRIDGE/` for git-history continuity only.
Product: **Crypto Paper Bridge** running on **Hyperliquid** (testnet = paper environment).
IBKR and Signum were evaluated and NOT chosen (see `docs/07_BROKER_DECISION.md`).

## Scope

Live/paper execution bridge: FastAPI + asyncio, Hyperliquid WebSocket/REST, SQLite persistence,
vanilla HTML/JS/CSS dashboard, LLM veto/regime layer (optional).

## Hard safety rules (non-negotiable)

1. **Mainnet (real money) is FORBIDDEN** without the triple-lock:
   `--enable-live` CLI flag + `HL_LIVE_ACK` env + `live_allowed: true` in strategy config.
   Never suggest, set, or mention enabling mainnet unless all three locks are explicitly in scope
   and Barış has given explicit approval.
2. API keys, private keys, and wallet secrets NEVER go in the repo or in any file committed to git.
   `HL_API_WALLET_KEY`, `HL_ACCOUNT_ADDRESS`, `TELEGRAM_BOT_TOKEN` are environment variables only.
3. Each machine uses a separate named API wallet (agent wallet); the main wallet private key is
   NEVER on any machine.
4. Operational state MUST be verified from `docs/03_STATUS.md` and live runtime before any action.
   Do not act on stale run IDs, arm state, or bridge status from memory.
5. Running anything against the exchange (even testnet) requires Barış explicit approval per
   `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MTC_REPO_GUARD_PROTOCOL.md`.
6. LLM layer can only reduce risk, never increase it. LLM cannot open trades, increase size, or
   widen stops.

## Protected surfaces

- `bridge/` Python source: protected execution logic; changes require full gate sequence.
- `config/` YAML: do not change `network: testnet` default without triple-lock approval.
- No changes to order placement, SL/TP, or position sizing without explicit Barış approval.

## Gate 7 write-back (component-scoped)

Update `_AI_MEMORY/CURRENT.md` and `_AI_MEMORY/NEXT_STEPS.md` (always).
Update `_AI_MEMORY/DECISIONS.md` / `_AI_MEMORY/ACTIVE_FILES.md` if applicable.
Do NOT touch root volatile histories.
