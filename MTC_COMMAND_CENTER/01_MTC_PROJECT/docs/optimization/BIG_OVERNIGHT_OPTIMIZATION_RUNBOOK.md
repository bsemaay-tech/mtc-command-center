# Big Overnight Optimization Runbook

## Scope

This runbook is for resuming `reports/optimization/big_overnight_multiasset` without restarting the exhaustive core grid from scratch.

## Pre-Run Checklist

- Verify the latest data bundle manifest exists at `C:\LAB\tradingview-lab\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\manifests\dataset_manifest.json`.
- Verify the regime registry exists at `C:\LAB\tradingview-lab\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\regimes\regime_registry.json`.
- Verify `reports/optimization/big_overnight_multiasset/resume_registry.sqlite` exists for a resume run.
- For producer-only seed extraction resumes, verify `reports/optimization/12h_backtesting_session/resume_registry.sqlite` exists and resume the same output root instead of starting a new folder.
- Verify the `tp_mode=None` / `tp_r_multiple=null` post-run patch has passed validation.
- Verify the keep-awake script parses before overnight use.
- Verify the worker scaling benchmark report exists at `reports/optimization/worker_scaling_benchmark/WORKER_SCALING_BENCHMARK_REPORT.md`.
- Verify the benchmark recommendation is `16` workers.
- Set thread pinning environment variables before launching the optimizer.
- Close or pause resource-heavy apps: Chrome tabs, TradingView, AutoCAD, Excel, Teams, Outlook, OneDrive sync, and unnecessary WebView/Copilot apps.
- Confirm there is enough free disk space on the repo/output drive.

## Required Worker Policy

- The next big resume must use explicit `--max-workers 16`.
- The minimum recommended worker count for the big resume is `16` based on the completed worker scaling benchmark.
- Do not exceed `16` workers until a new worker scaling benchmark proves a higher value is safe.
- `20` and `24` workers are not approved on the current hardware.
- The old auto worker cap of `6` is outdated for this machine and this run.

## Detached PowerShell Execution Policy

- Do not run the big optimization directly inside the Codex UI terminal.
- Codex should launch a detached PowerShell runner script and then monitor logs/status.
- The optimization must run as an independent process so Codex UI closure does not stop it.
- The detached runner must write `heartbeat.log`, checkpoints, `resume_registry.sqlite`, stdout/stderr logs, and a run-status artifact.
- A launch is not successful until the launcher exits, the detached PID still exists, logs exist, status JSON exists, the heartbeat/checkpoint path is active or expected, and worker/thread settings are visible in status/config.
- PowerShell launchers must quote paths containing spaces; prefer writing an inner runner `.ps1` and starting that file with a quoted `-File` argument.
- Use `scripts/start_big_overnight_resume_detached.ps1` as the launch template and `scripts/check_big_overnight_resume_status.ps1` for read-only status checks.

## Thread Pinning

Set these environment variables for the detached optimizer process:

```powershell
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:NUMEXPR_NUM_THREADS='1'
```

## Recommended Big Resume Command

The real overnight resume command belongs inside the detached runner script, not directly in the Codex UI terminal. It must use the same output folder so `resume_registry.sqlite` can skip completed `evaluation_key` rows:

```powershell
python tools/run_big_overnight_multiasset_optimization.py `
  --manifest C:\LAB\tradingview-lab\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\manifests\dataset_manifest.json `
  --regimes C:\LAB\tradingview-lab\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\regimes\regime_registry.json `
  --out reports/optimization/big_overnight_multiasset `
  --max-workers 16 `
  --time-budget-minutes 480 `
  --max-assets 8
```

## Resume Registry Verification

- Confirm `reports/optimization/big_overnight_multiasset/resume_registry.sqlite` exists before resume.
- Inspect `reports/optimization/big_overnight_multiasset/reports/RESUME_DEDUP_REPORT.md`.
- Runtime summaries must show `duplicate_conflicts=0`.
- On a restart smoke, `skipped_already_completed` must be greater than 0.
- Merged result rows must remain unique by `evaluation_key`.

## Checkpointing

- The big runner writes runtime summaries under `logs/runtime_summary.json`.
- It writes registry status under `reports/RESUME_DEDUP_REPORT.md`.
- It writes checkpoints under `checkpoints/` during longer runs.
- If interrupted, restart with the same `--out` folder rather than creating a new output root.

## Time Budget

- The prior run used an 8-hour budget and completed 168,337 of 6,615,000 planned split evaluations.
- The producer-only 12h detached seed run first completed `282255 / 378000` evaluations with `0` failed and `0` duplicate conflicts before reaching its time budget.
- The 2026-05-01 detached resume then completed the remaining `95745` evaluations and the registry reached `378000 / 378000` completed with `0` failed and `0` duplicate conflicts.
- Resume ranking caveat: after the 2026-05-01 resume, `ranked/all_evaluations.csv` represented the current resume slice (`95745` rows), not a merged full-run `378000` row export. Run a cumulative rerank before final global seed promotion decisions.
- A resume should be time-boxed explicitly with `--time-budget-minutes`.
- Do not infer completion from a time-budget stop; check planned vs completed counts in the report.

## Keep-Awake

Run the keep-awake script in a separate PowerShell session before the long run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/keep_awake_big_overnight_optimization.ps1
```

Do not run the keep-awake loop as part of a short smoke. Syntax-check it instead for validation tasks.

## Reports To Inspect After Resume

- `BIG_OVERNIGHT_OPTIMIZATION_REPORT.md`
- `BIG_OVERNIGHT_OPTIMIZATION_INDEX.md`
- `reports/RESUME_DEDUP_REPORT.md`
- `logs/runtime_summary.json`
- `ranked/ranked_candidates.csv`
- `ranked/robust_medium_candidates.csv`
- `ranked/robust_strict_candidates.csv`
- `reports/PROBLEM_DISCOVERY_REPORT.md`
- `reports/REGIME_PERFORMANCE_REPORT.md`
- `reports/CROSS_ASSET_REPORT.md`
- `reports/CROSS_TIMEFRAME_REPORT.md`

## Search-Space Reduction Policy

- Resume of the existing exhaustive grid is allowed as a controlled baseline, but new feature/filter research must not default to full exhaustive crossing.
- Producer-only seed extraction must precede filter/gate/refinement stages.
- Use `optimization/parameter_library/README.md` for research seeds and `docs/optimization/SEARCH_SPACE_REDUCTION_AND_SMART_SAMPLING.md` for methodology.
- `1D` may need separate profile handling; CHOPPY/CONSOLIDATING weakness belongs in the regime-mitigation stage.

## Per-Asset/Timeframe Output Requirement

- Any resumed or future big optimization must generate `ranked/per_asset_timeframe_seed_candidates.csv` and `ranked/per_asset_timeframe_summary.csv` before downstream refinement.
- Aggregate ranked candidates are acceptable for top-level reporting, but not sufficient for exit/filter refinement decisions.
- After each large run, refresh `optimization/parameter_library/` with `tools/extract_parameter_library_seeds.py` and keep research seeds separate from Pine defaults.
- After a broad run, report at least two global seed views: highest average return and most defensive/worst-split seed. Do not present either as production defaults.
