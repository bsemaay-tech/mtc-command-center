# START_HERE

Read order: `AGENTS.md`, this file, `AI_RULES.md`, `PROJECT_MEMORY.md`, `GLOBAL_HANDOFF.md` if needed, `NEXT_STEPS.md`, then project handoff files.

Workflow gates and prompt templates: see `AI_RULES.md` and `..\04_SHARED\prompts\05_ai_workflow\00_index.md`.

HER backtest / optimizasyon için (in-day tek strateji, sprint, overnight — fark etmez) **zorunlu pre-read iki dosya:**
1. Canonical kurallar: `..\03_QUANTLENS\_user_guide\07_BACKTEST_AND_OPTIMIZATION_RULES.md` (4 gate, buy&hold + alpha, DSR, BH-FDR, classification, promotion levels, antigravity checklist)
2. Operasyonel runbook: `..\11_TRIAGE\BACKTEST_OPTIMIZATION_RUNBOOK.md`

Akış: `..\04_SHARED\prompts\05_ai_workflow\08_backtest_launch.md`. Single-strategy 5dk run dahi 4-gate (rolling WF + bootstrap+BH-FDR + DSR + multi-window) + buy&hold karşılaştırması olmadan promotable değil.

Do not change trading logic, Pine logic, MTC behavior, or parity checks without explicit approval.

## Strategy research (combining existing strategies/indicators)

Before any strategy-research session, read in this order:
1. `STRATEGY_COMPONENT_LIBRARY.md` — what exists, what combines.
2. `05_REGISTRY/STRATEGY_RESEARCH_REGISTRY.json` + `INDICATOR_REGISTRY.json` +
   `COMPONENT_REGISTRY.json` + `TAG_DICTIONARY.json`.
3. `STRATEGY_RESEARCH_WORKFLOW.md` (16-step process) and
   `STRATEGY_CODE_REVIEW_CHECKLIST.md`.

During research: log every variant (`VARIANT_LOG_REGISTRY.json` +
`03_QUANTLENS/_templates/VARIANT_LOG_TEMPLATE.md`), save runs under
`03_QUANTLENS/research/<run_id>/`, register in `RESEARCH_RUN_REGISTRY.json`, and
confirm visibility in the **Strategy Research Lab** dashboard tab. Do not reinvent
these workflows or hand-edit generated registries (regenerate via
`03_QUANTLENS/tools/build_strategy_research_registry.py`).

User-supplied transcripts/screenshots go in `00_INBOX/USER_INTAKE/`; route them
with `03_QUANTLENS/tools/route_user_intake.py` into each strategy's `source_intake/`.
