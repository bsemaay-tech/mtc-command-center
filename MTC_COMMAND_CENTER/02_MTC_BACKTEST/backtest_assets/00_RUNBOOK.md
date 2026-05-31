# 00_RUNBOOK.md
Last Updated: 2026-03-05

## Command Governance
All command entrypoints are sourced from:
- `100_PROJECT_MEMORY_FİLE/20_BACKTEST_WORKFLOW/01_CURRENT_STATE.md`

This runbook does not redefine engine commands. It orchestrates existing commands.

## Standards References
- `100_PROJECT_MEMORY_FİLE/20_BACKTEST_WORKFLOW/03_RESULTS_SCHEMA.md`
- `100_PROJECT_MEMORY_FİLE/20_BACKTEST_WORKFLOW/04_RUN_MANIFEST_STANDARD.md`
- `100_PROJECT_MEMORY_FİLE/20_BACKTEST_WORKFLOW/07_REPORTING_STANDARD.md`
- `100_PROJECT_MEMORY_FİLE/20_BACKTEST_WORKFLOW/05_OPTIMIZATION_PLAYBOOK.md`

## Single Source of Truth
- Runtime defaults: `mtc_backtest/backtest_assets/autorun.yaml`
- Staged spaces: `mtc_backtest/backtest_assets/param_space.yaml`
- Module registry: `mtc_backtest/backtest_assets/module_registry.yaml`

## No-Questions Autopilot Flow
0. Preflight data QC + catalog (`download_datasets_autopilot.py`)
1. Optional parity smoke (RAW + CLIP) if TV exports exist
2. Baseline backtest (`scripts/run_case.py`)
3. Tiny optimization (`python -m src.optimizer_v0 run ... iters 30`) if enabled
4. Staged optimization (`scripts/staged_optimize.py`) if enabled
5. Walk-forward (`scripts/walk_forward_validate.py`) if enabled
6. Robustness (`scripts/robustness_runner.py`) if enabled

## SKIP Policies
- Missing TV export CSV: parity smoke => `SKIP_REASON=TV_EXPORT_MISSING`
- Missing optimizer candidate JSON: robustness => `SKIP_REASON=CANDIDATE_MISSING`
- Disabled step in `autorun.yaml`: `SKIP_REASON=DISABLED_IN_AUTORUN`
- Optional dataset job fails: `SKIP_REASON=OPTIONAL_DATA_JOB_FAILED`

Required dataset job failures remain `FAIL`.

## Run Index Output
Each autopilot run writes:
- main run artifacts under `mtc_backtest/results/autopilot_runs/<RUN_DIR>/`
- run index under `mtc_backtest/backtest_assets/runs/<RUN_ID>/INDEX.md`

`INDEX.md` links to actual artifacts created by existing scripts (backtest/parity/optimizer/staged/wf/robustness outputs).

## Main Command
From repository root:

```bash
python mtc_backtest/scripts/autopilot_run.py --autorun mtc_backtest/backtest_assets/autorun.yaml --param-space mtc_backtest/backtest_assets/param_space.yaml
```

## Future-Proof Extension Rule
When adding new signal/filter/SLTP/guard/confirmation blocks:
1. Register in `module_registry.yaml`
2. Add params to `param_space.yaml` (`module_registry` section)
3. Rebuild module cases via `scripts/build_autopilot_cases.py`
4. Re-run autopilot

