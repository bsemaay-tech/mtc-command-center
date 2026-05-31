# Optimizer Infrastructure Rules

## 2026-04-28 Optimization Consolidation

- Infrastructure hardening is ready, including Runner metrics adapter, resume/de-dup registry, and coverage-aware scoring.
- Big overnight output remains partial: `168337 / 6615000` split evaluations, `144` robust medium candidates, `0` robust strict candidates.
- Detached producer-only seed extraction first completed `282255 / 378000` evaluations, then the 2026-05-01 resume completed the remaining `95745`; registry status is now `378000 / 378000`, with `0` failed evaluations and `0` duplicate conflicts.
- Current seed output under `reports/optimization/12h_backtesting_session/` emits `200` per-asset/timeframe research seed rows, top `5` for each of `40` groups, with `114` unique hashes in the emitted rows.
- The resume/de-dup smoke proved `skipped_already_completed > 0`; before the next big resume, validate detached-runner process survival.
- Medium candidates may seed second-pass research but must not be written into Pine defaults.
- Use `evaluation_key` as the resume and de-dup identity for every completed row.
- Optimization output does not claim TradingView release parity.
- Worker scaling benchmark verdict is `WORKER_SCALING_READY_RECOMMEND_16_WORKERS`; next big resume should use explicit `--max-workers 16`.
- Big overnight optimization must run through a detached PowerShell process, not as a foreground Codex UI terminal command.
- Thread pinning is required for large runs: `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1`.
- Detached launch reports must verify PID/process survival after launcher exit, stdout/stderr paths, status JSON, heartbeat, checkpoint path, configured worker count, and thread pinning before claiming success.
- Resource-heavy apps should be closed or paused before overnight work.
- Benchmark evidence: `reports/optimization/worker_scaling_benchmark/WORKER_SCALING_BENCHMARK_REPORT.md`.

## Official Result Interface

- Optimizers must consume MTC V2 Python engine metrics through `mtc_v2.core.results` structures or `tools.runner_metrics_adapter`.
- Result rows must preserve `config_hash`, `dataset_hash`, `dataset_id`, and `run_id` where available.
- Unavailable metrics must remain `None` with warning codes; optimizers must not fabricate profit factor, entry time, or exposure metrics.

## Resume And De-duplication

- Overnight optimizers must create an `evaluation_key` before scheduling work.
- The `evaluation_key` must include profile, dataset, dataset hash, symbol, timeframe, walk-forward window, split type, normalized params, runner version, optimizer version, and mapper version.
- Completed `evaluation_key` rows must not be scheduled again on resume.
- Duplicate completed result rows must be merged as one logical evaluation.
- Duplicate keys with different result hashes are conflicts and must be reported, not silently resolved.
- `resume_registry.sqlite` is mandatory for overnight resume runs and must be preserved across detached-process restarts.

## Coverage-Aware Scoring

- Robust candidates require positive train, validation, and test/OOS behavior.
- Walk-forward consistency must be at least `0.70`.
- Validation and test positive ratios must be at least `0.50`.
- If multiple timeframes exist, at least two timeframes must be positive.
- If multiple symbols exist, at least two symbols must be positive.
- Single-symbol optimization must be marked `INSUFFICIENT_SYMBOL_COVERAGE` and must not be called production robust.
- Global seed summaries must distinguish high-average-return candidates from defensive candidates with low worst-split loss and low drawdown.
- Resumed ranking outputs must state whether they are cumulative or current-invocation only; do not treat a resume-slice CSV as a full-run global ranking.

## Reporting Requirements

- Optimization reports must include `evaluation_key`.
- Final merged CSVs must contain unique `evaluation_key` rows only.
- Runtime summaries must include planned, scheduled, completed, skipped already completed, duplicate conflicts, and failed evaluations.
- Research optimization output must not claim live profitability, production readiness, or TradingView release parity.
- TradingView release/audit claims require separate workbook `Properties` validation and local symbol/timeframe routing validation.

## Search-Space Reduction Infrastructure Rule

- New optimization features must use staged smart sampling instead of blindly expanding the full exhaustive grid.
- Producer-only seed extraction is required before expensive filter/gate optimization.
- Research seeds live under `optimization/parameter_library/` and must preserve source reports, params, metrics, warnings, and status.
- All future producers must follow `docs/optimization/SEARCH_SPACE_REDUCTION_AND_SMART_SAMPLING.md`.

## Per-Asset/Timeframe Seed Output Rule

- Optimizer/scorer outputs used for staged refinement must include asset/symbol, timeframe, dataset_id/source_type, evaluation_key or parameter_hash, producer params, and train/validation/test metrics where available.
- Tools must mark insufficient rows explicitly instead of fabricating missing metrics.
- Seed-ranking outputs are research artifacts only and must not write to Pine defaults or production configuration.
