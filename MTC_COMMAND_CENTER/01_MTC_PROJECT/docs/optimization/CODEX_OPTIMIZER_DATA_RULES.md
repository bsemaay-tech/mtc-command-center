# Codex Optimizer Data Rules

## 2026-04-28 Optimization Consolidation

- Infrastructure hardening, data bundle creation, and dataset usage rules are ready.
- Big overnight optimization is partial: `168337 / 6615000` split evaluations completed.
- Confirmed ranked output has `144` robust medium candidates and `0` robust strict candidates.
- Resume/de-dup smoke passed; next action is detached-runner smoke/process-survival validation, then resume the exhaustive core grid.
- Do not promote medium candidates to Pine defaults.
- Do not place `MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427` or heavy worker/all_evaluations outputs in portable handoff.
- Use dataset manifest IDs and `evaluation_key` for all optimizer continuation work.
- Codex UI is not a reliable process host for long overnight optimization; launch big runs through a detached PowerShell runner.
- Use explicit `--max-workers 16` for the next big resume based on `reports/optimization/worker_scaling_benchmark/WORKER_SCALING_BENCHMARK_REPORT.md`.
- Do not exceed `16` workers without a new benchmark.
- Pin numeric library threads to 1 for large runs: `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1`.
- Pause resource-heavy apps before overnight work.
- Preserve `resume_registry.sqlite` for every resume.

- Before optimization, read `docs/optimization/DATASET_AND_REGIME_USAGE_RULES.md`.
- Use `dataset_id`, not direct CSV paths.
- Load datasets from `dataset_manifest.yml` or `dataset_manifest.json`.
- Verify SHA256 before every run.
- Do not use XLSX Strategy Tester workbooks as chart data.
- Do not use `unknown_csv` unless explicitly approved.
- Do not claim robust if only one symbol was tested.
- Use walk-forward train/validation/test splits.
- Report per-symbol, per-timeframe, and per-regime metrics.
- Save outputs under `reports/optimization/<run_id>/`.
- Do not modify `01_PINE/MTC_V2.pine`.
- Do not use live keys, exchange API keys, or live trading.

## Search-Space Reduction Rules For AI Workers

- Do not launch broad feature/filter sweeps across all producer settings.
- Use staged optimization: producer-only, exit/risk, filter/gate, regime mitigation, cross-asset/timeframe validation, walk-forward robustness, then candidate promotion.
- Use `optimization/parameter_library/README.md` for research seeds.
- Medium candidates are research seeds only and must not change Pine defaults.
- Optimization output does not claim TradingView release parity.
