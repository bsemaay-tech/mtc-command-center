# Search Space Reduction And Smart Sampling

Research seeds only; not Pine defaults; not production parameters.

## 1. Purpose

This document defines the optimization methodology for reducing wasted evaluations in MTC V2 research. It preserves parity-first discipline while moving future optimization work away from blind exhaustive expansion across weak producer settings.

## 2. Why Exhaustive Grid Is Not Enough

The current big overnight grid planned 6,615,000 split evaluations for only one producer family and a limited exit/risk surface. It completed only 168,337 evaluations before the time budget ended. Exhaustive grids are useful controlled baselines, but they are not sustainable when every new filter, gate, exit, regime rule, or producer feature multiplies the search space.

The central rule is: do not spend filter, gate, exit, and regime-mitigation budget on producer settings that are already weak.

## 3. General Staged Optimization Model

### Stage 0 ? Data And Parity Preconditions

- Dataset manifest exists.
- `source_type` is verified and preserved.
- SHA256 is verified before evaluation.
- Strategy feature parity is checked where applicable.
- Pine/Python/PineTS parity boundaries remain explicit.
- No optimization output claims TradingView release parity.

### Stage 1 ? Producer-Only Baseline

- Optimize only main producer parameters.
- Keep all filters/gates off.
- Keep guards off.
- Keep integrations off.
- Keep visualization/debug off.
- Use a simple, fixed exit/risk model.
- Output best producer settings per asset/timeframe.
- Save accepted producer seeds to `optimization/parameter_library/<producer>/`.

### Stage 2 ? Exit/Risk Refinement

- Use top producer seeds only.
- Optimize SL/TP/risk/trailing/break-even only if allowed by the research scope.
- Do not re-open the full producer grid.
- Save accepted exit/risk regions separately from producer regions.

### Stage 3 ? Filter/Gate Evaluation

- Use top producer+exit seeds only.
- Test filters one family at a time.
- Avoid testing filters on bad producer settings.
- Record whether each filter adds durable value or only overfits.
- Rejected filters must be listed with evidence.

### Stage 4 ? Regime Mitigation

- Test ADX, Chop, ATR floor, session, and volatility filters only after producer+exit baseline is stable.
- Specifically address CHOPPY and CONSOLIDATING weakness.
- Require a per-regime performance report.
- Do not treat regime mitigation as proof of production readiness.

### Stage 5 ? Cross-Asset/Timeframe Validation

- Test candidates across multiple assets and timeframes.
- Separate intraday from `1D` if needed.
- Report worst asset and worst timeframe.
- Report both high-return and defensive views: average return alone is not enough because the best average seed can carry unacceptable worst-split loss or drawdown.
- Candidates that only work on one symbol/timeframe remain research-only.

### Stage 6 ? Walk-Forward Robustness

- Use train/validation/test splits.
- Prefer rolling or anchored walk-forward windows.
- Require `walkforward_consistency` and positive validation/test ratios.
- Preserve `evaluation_key`, dataset hashes, source paths, and source labels.

### Stage 7 ? Candidate Promotion

- Only strict robust candidates can become promotion candidates.
- Medium candidates are research seeds only.
- Final TradingView audit is still required before any release claim.

## 4. Strategy-Agnostic Rule

This framework applies to Supertrend, Range Filter, and future producers. Each producer gets its own parameter library namespace under `optimization/parameter_library/<producer_id>/`. Shared exit, risk, filter, and regime templates live under `optimization/parameter_library/shared/`.

## 5. What Not To Optimize Early

Do not optimize these early unless the current stage explicitly targets them:

- guards
- integrations
- visualization/debug
- session logic
- HTF filters
- candle pattern filters
- complex MACD filters
- individual filter-exit toggles

Early stages should isolate producer signal quality before adding interaction-heavy components.

## 6. When To Use Random, Latin, Bayesian, Or Genetic Methods

- Use random sampling or Latin Hypercube Sampling for broad exploration when a full grid is too large.
- Use local grids around accepted seed regions for deterministic refinement.
- Use Bayesian/genetic methods only after deterministic baseline, resume/de-dup, and reporting are stable.
- Never use a black-box optimizer without recording exact parameter set, data, hashes, run metadata, and `evaluation_key`.

## 7. Required Outputs For Every Staged Run

Every staged run must produce:

- candidate CSV
- seed region YAML
- rejected region list
- per-asset/timeframe summary
- per-regime summary
- evidence path
- manifest/hash references
- resume/de-dup status

## Non-Negotiable Boundary

Research seeds only; not Pine defaults; not production parameters. Medium robust candidates may seed second-pass research but cannot change `01_PINE/MTC_V2.pine` defaults.

## Per-Asset/Timeframe Seed Ranking Requirement

- Per-asset/per-timeframe seed ranking is now required for staged optimization outputs; aggregate candidate rows are not enough for exit/filter refinement.
- Future producer-only runs must emit `ranked/per_asset_timeframe_seed_candidates.csv` and `ranked/per_asset_timeframe_summary.csv`.
- Refinement jobs must consume seeds from `optimization/parameter_library/`, not promote aggregate medium candidates directly.
- Smoke-derived asset/timeframe seeds are schema/pipeline proof only; they are not Pine defaults, not production parameters, and not final optimization conclusions.
- Reference: `docs/optimization/SEARCH_SPACE_REDUCTION_AND_SMART_SAMPLING.md`, `optimization/parameter_library/README.md`, and `reports/optimization/seed_granularity/PER_ASSET_TIMEFRAME_SEED_RANKING_REPORT.md`.

## 12h Seed Extraction Lesson

- The 12h producer-only run produced usable research seeds, but the top average-return seed and the most defensive seed were different.
- A global seed answer must state the selection criterion, for example highest average return, highest positive ratio, or best worst-split loss.
- A seed that wins only on one symbol/timeframe or wins by accepting extreme drawdown remains research-only.
- The 2026-05-01 resume finished the full producer-only registry: `378000 / 378000` split evaluations, `0` failed, `0` duplicate conflicts.
- The full producer grid was `720` unique parameter variants; after the final resume, the emitted research shortlist is `200` per-asset/timeframe rows with `114` unique hashes.
- The final resume slice did not clearly beat the previous global high-return seed or previous defensive seed; it mainly completed coverage.
- Resume outputs must be labeled carefully: current `ranked/all_evaluations.csv` is a `95745`-row resume slice, so cumulative global decisions need a merge/rerank over all completed rows.
