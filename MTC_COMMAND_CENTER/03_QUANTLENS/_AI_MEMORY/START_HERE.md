# START_HERE - QuantLens Research Component

Component: `MTC_COMMAND_CENTER/03_QUANTLENS/`
Root router: [COMPONENT_ROUTER.md](../../_AI_MEMORY/COMPONENT_ROUTER.md)

## Cold-start read order

1. Root `AGENTS.md` (two-tier model, DATA & LAUNCH section)
2. This file
3. `CURRENT.md`
4. `NEXT_STEPS.md`
5. `DECISIONS.md` (if relevant)
6. `ACTIVE_FILES.md` (if relevant)
7. `_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md` (mandatory before any backtest)
8. `../../11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md` (mandatory before any backtest)

Do NOT read root volatile histories for this component unless cross-component coordination is needed.

## Component purpose

Research engine for strategy walk-forward validation, CPCV, DSR, BH-FDR, multi-window analysis,
and strategy promotion decisions. Also houses the AI expert-verdict layer (labels-only opinions;
the Scorecard owns all numbers).

## Key files

- `tools/mega_walk_forward.py` - canonical research engine
- `_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md` - four gates, classification, promotion
- `_user_guide/13_AI_VERDICT_AUTHORING_PROCEDURE.md` - verdict authoring
- `data/README.md` - authoritative data inventory
- `research/<run_id>/` - run outputs
- `_AI_MEMORY/CURRENT.md` - live session state

## Protected surfaces

- [`STRATEGY_REGISTRY.md`](STRATEGY_REGISTRY.md): read-only, do not edit.
- Promotion gates, DSR/BH-FDR thresholds: explicit Barış approval required.
- Pine logic and MTC strategy behaviour: explicit Barış approval required.

## Approval gate

ANY backtest, optimization, or artifact generation requires explicit Barış approval before proceeding. Exchange/paper/live execution requires separate explicit approval. Consistent with root `DO_NOT_TOUCH.md`.

## Gate 7

Update `CURRENT.md` + `NEXT_STEPS.md` always. `DECISIONS.md` / `ACTIVE_FILES.md` if applicable.
Do not touch root volatile histories.
