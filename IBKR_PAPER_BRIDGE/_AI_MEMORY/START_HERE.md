# START_HERE - Crypto Paper Bridge Component

Component: `IBKR_PAPER_BRIDGE/` (product: Crypto Paper Bridge on Hyperliquid)
Root router: [COMPONENT_ROUTER.md](../../MTC_COMMAND_CENTER/_AI_MEMORY/COMPONENT_ROUTER.md)

## Cold-start read order

1. Root `AGENTS.md`
2. This file
3. `CURRENT.md` (verify operational state before acting)
4. `NEXT_STEPS.md`
5. `docs/03_STATUS.md` - verified bridge status (always read before any bridge action)
6. `docs/01_ARCHITECTURE.md` - system design
7. `docs/17_DEPLOYMENT.md` - deployment runbook

Do NOT read root volatile histories for this component unless cross-component coordination is needed.

## Component purpose

Live/paper execution bridge connecting MTC V2 strategy signals to Hyperliquid (testnet/mainnet).
Paper (testnet) is the default and only operating environment without the triple-lock.

## Key files

- `docs/03_STATUS.md` - verified gate status; read before any action
- `docs/01_ARCHITECTURE.md` - stack decisions (final; do not re-litigate)
- `docs/17_DEPLOYMENT.md` - deployment instructions
- `bridge/` - Python source (protected execution logic)
- `config/` - YAML configuration
- `tests/` - test suite
- `_AI_MEMORY/CURRENT.md` - live session state

## CRITICAL safety gates

- Mainnet (real money) is FORBIDDEN without triple-lock: `--enable-live` + `HL_LIVE_ACK` env + `live_allowed: true`.
- API keys/secrets: environment variables ONLY, never in repo.
- Verify `docs/03_STATUS.md` before any claim about armed state, run IDs, or bridge status.
- Running against exchange (even testnet) requires explicit Barış approval.

## Gate 7

Update `CURRENT.md` + `NEXT_STEPS.md` always. `DECISIONS.md` / `ACTIVE_FILES.md` if applicable.
Do not touch root volatile histories.
