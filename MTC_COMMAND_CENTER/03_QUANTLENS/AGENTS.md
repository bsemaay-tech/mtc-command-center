# AGENTS.md - QuantLens Research Component

Inherits root two-tier model, canonical audit roster, safety gates, and parallel-agent safety
from [root AGENTS.md](../../AGENTS.md). Read root AGENTS.md first.

## Routing

This component's onboarding chain:
`03_QUANTLENS/AGENTS.md` -> `_AI_MEMORY/START_HERE.md` -> `_AI_MEMORY/CURRENT.md` -> `_AI_MEMORY/NEXT_STEPS.md`

Do NOT load root volatile histories for component-scoped tasks.

## Scope

QuantLens research engine: walk-forward backtesting, CPCV, DSR, strategy research, overnight sweeps.
- Canonical engine: `tools/mega_walk_forward.py`
- User guide: `_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md` (four gates, classification, promotion)
- Operational runbook: `../11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md`

## Protected surfaces

- [`_AI_MEMORY/STRATEGY_REGISTRY.md`](_AI_MEMORY/STRATEGY_REGISTRY.md): do not edit.
- Backtest rules, promotion gates, DSR/BH-FDR thresholds: require explicit Barış approval to change.
- Pine logic and MTC strategy behaviour: never change without explicit Barış approval.
- Do not hand-edit generated registries; regenerate via `tools/build_strategy_research_registry.py`.

## Non-negotiables

1. Every backtest (any duration) requires Gate 0 pre-read: canonical rules + operational runbook.
2. Single-strategy results without buy-and-hold + DSR + BH-FDR + multi-window are not promotable.
3. Held-out data virginity check (Stage 1.1) is mandatory before freezing any scope.
4. Log every variant in `VARIANT_LOG_REGISTRY.json`; save runs under `research/<run_id>/`.
5. Explicit Barış approval required before ANY backtest, optimization, or artifact generation — not only exchange or paper/live execution. Consistent with root `DO_NOT_TOUCH.md`.
6. Exchange, paper, and live execution require separate explicit Barış approval in addition to #5.

## Backtest data and canonical run command

See root `AGENTS.md` "DATA & LAUNCH" section for authoritative data inventory and run command.
Primary bundle: `native_multiasset_alpaca_2026-06-28`.

## Gate 7 write-back (component-scoped)

Update `_AI_MEMORY/CURRENT.md` and `_AI_MEMORY/NEXT_STEPS.md` (always).
Update `_AI_MEMORY/DECISIONS.md` / `_AI_MEMORY/ACTIVE_FILES.md` if applicable.
Do NOT touch root volatile histories.
