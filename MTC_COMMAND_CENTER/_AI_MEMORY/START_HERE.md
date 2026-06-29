# START_HERE

> **▶ CURRENT STATE: read `_AI_MEMORY/GLOBAL_HANDOFF.md` (newest section first) + `NEXT_STEPS.md` for live work.** The older `_AI_MEMORY/CODEX_PICKUP_2026-06-08.md` is historical (most items DONE) — read only for back-context. Everything below is standing reference.

Read order: `AGENTS.md`, this file, `AI_RULES.md`, `PROJECT_MEMORY.md`, `GLOBAL_HANDOFF.md` if needed, `NEXT_STEPS.md`, then project handoff files.

> **Naming:** "QuantLens" = the research backtest engine/lab under `03_QUANTLENS/` AND the AI **expert-verdict** layer (labels-only opinions; the Scorecard owns all numbers). The old "QuantLens" Gemini pre-screen was renamed "Gemini Pre-Screen" — ignore that usage in pre-2026-06-08 handoff entries.

Workflow gates and prompt templates: see `AI_RULES.md` and `..\04_SHARED\prompts\05_ai_workflow\00_index.md`.

Per-job procedures (so every agent does a job the same way): backtest data+launch → `AGENTS.md` "DATA & LAUNCH"; results → dashboard → `..\11_TRIAGE\RESULTS_TO_DASHBOARD_MAP_2026-06-29.md`; AI/QuantLens verdict authoring → `..\03_QUANTLENS\_user_guide\13_AI_VERDICT_AUTHORING_PROCEDURE.md`.

AI tool auto-use (MarkItDown for binary docs, Graphify for impact questions, CodeBurn for cost/routing): see the `AI TOOL AUTO-USE` section in `AGENTS.md` and `..\09_DOCS\AI_TOOLING\AI_TOOL_INTEGRATION_PLAN.md`. Use them automatically at their triggers; don't wait to be told.

HER backtest / optimizasyon için (in-day tek strateji, sprint, overnight — fark etmez) **zorunlu pre-read iki dosya:**
1. Canonical kurallar: `..\03_QUANTLENS\_user_guide\07_BACKTEST_AND_OPTIMIZATION_RULES.md` (4 gate, buy&hold + alpha, DSR, BH-FDR, classification, promotion levels, antigravity checklist)
2. Operasyonel runbook: `..\11_TRIAGE\BACKTEST_OPTIMIZATION_RUNBOOK.md`

Akış: `..\04_SHARED\prompts\05_ai_workflow\08_backtest_launch.md`. Single-strategy 5dk run dahi 4-gate (rolling WF + bootstrap+BH-FDR + DSR + multi-window) + buy&hold karşılaştırması olmadan promotable değil.

**Veri + çalıştırma (kanonik):** Hangi datayı kullanacağını bilmeden backtest çalıştırma. Otorite envanter: `..\03_QUANTLENS\data\README.md` (tüm native bundle'lar — sembol/timeframe/asset-class/bar sayısı + crypto data konumları). US equities / ETF / multi-asset / 10m **var**; engine'in hardcoded default manifest'i eski crypto arşivi, güncel data DEĞİL. Engine data seçimi: `MEGA_BUNDLE_MANIFEST` env → bir bundle'ın `manifests\dataset_manifest.json`'u + `--symbol`/`--tf`. Kanonik tek-koşu: `python ..\03_QUANTLENS\tools\mega_walk_forward.py --strategy <id> --symbol <SYM> --tf <tf>` (research engine; `walk_forward_processor.py` alt-seviye/custom). Birincil bundle: `native_multiasset_alpaca_2026-06-28`.

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
