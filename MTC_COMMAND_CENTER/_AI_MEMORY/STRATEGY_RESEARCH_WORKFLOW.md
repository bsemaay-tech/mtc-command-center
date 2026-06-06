# Strategy Research Workflow (permanent)

Standard process for an AI agent running **strategy research** — combining
existing matured strategies/indicators into new robust candidates. This does
**not** duplicate engine/backtest rules; it points to them.

> Canonical backtest rules (mandatory pre-read, Gate 0):
> - `03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md`
> - `11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md`

## Read first (limited-context order)
1. `_AI_MEMORY/STRATEGY_COMPONENT_LIBRARY.md` — what exists, what combines.
2. `05_REGISTRY/STRATEGY_RESEARCH_REGISTRY.json` — strategy taxonomy index.
3. `05_REGISTRY/INDICATOR_REGISTRY.json` + `COMPONENT_REGISTRY.json` + `TAG_DICTIONARY.json`.
4. The two backtest-rules files above.
5. `_AI_MEMORY/STRATEGY_CODE_REVIEW_CHECKLIST.md`.

## Process
1. Read the AI memory + registries (above). Do not re-derive the inventory.
2. Select components by **tags** (category / method / market_regime / component_type).
3. Define a one-sentence research hypothesis.
4. Choose an **architecture family**:
   - `regime_switching_strategy` — pick a sub-strategy per detected regime.
   - `signal_scoring_ensemble` — weighted score across signals; threshold to enter.
   - `specialist_strategy_portfolio` — allocate across specialist strategies.
   - `breakout_pullback_hybrid` — breakout trigger + pullback entry refinement.
5. Design the backtest using the permanent backtest rules (above).
6. Run baseline tests (single component / single asset first).
7. Create variants.
8. **Log every variant** — copy `03_QUANTLENS/_templates/VARIANT_LOG_TEMPLATE.md`
   and append a row to `05_REGISTRY/VARIANT_LOG_REGISTRY.json`.
9. Reject weak variants honestly (record the reason).
10. Check anti-overfitting rules (DSR, BH-FDR, multi-window, B&H alpha).
11. Review code safety with `STRATEGY_CODE_REVIEW_CHECKLIST.md`.
12. Write the final report from `03_QUANTLENS/_templates/STRATEGY_RESEARCH_REPORT_TEMPLATE.md`.
13. Save the run under `03_QUANTLENS/research/<research_run_id>/` (report + variants).
14. Register the run in `05_REGISTRY/RESEARCH_RUN_REGISTRY.json`; backtest summaries
    in `05_REGISTRY/RESEARCH_BACKTEST_REGISTRY.json`.
15. Confirm it shows in **Strategy Research Lab** tab (`/dashboard` → research).
16. Update `_AI_MEMORY/GLOBAL_HANDOFF.md` and `_AI_MEMORY/NEXT_STEPS.md`.

## Hard rules
- No new production strategy / no live trading in a research run.
- Do not modify `MTC_V2.pine` or production parity logic.
- Single-strategy 5-minute results are **not** promotable without the 4 gates
  + B&H comparison (see canonical rules).
- One canonical source of truth: per-strategy `01_candidate_metadata.yaml` /
  `producer_spec.json` feed the registry via
  `03_QUANTLENS/tools/build_strategy_research_registry.py` — edit the source,
  then regenerate; do not hand-edit the generated registries.
