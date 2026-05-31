# Command Cookbook (PowerShell)

## Full test suite
```powershell
python -m pytest mtc_backtest/tests -v
```

## Runbook modes
```powershell
powershell -ExecutionPolicy Bypass -File .\mtc_backtest\runbook.ps1 -Mode optimize
powershell -ExecutionPolicy Bypass -File .\mtc_backtest\runbook.ps1 -Mode validate
powershell -ExecutionPolicy Bypass -File .\mtc_backtest\runbook.ps1 -Mode promote -DeterminismGate
```

## Walk-forward workflow
```powershell
python mtc_backtest/scripts/walk_forward_validate.py `
  --train-case mtc_backtest/configs/cases/aug2025_parity.json `
  --target-case-1 mtc_backtest/configs/cases/target_sep2025_dec2025.json `
  --target-case-2 mtc_backtest/configs/cases/target_jan2026.json `
  --iters 200 --seed 42 --workers 1 `
  --outdir mtc_backtest/results/walkforward
```

## Supertrend walk-forward setup
```powershell
python mtc_backtest/scripts/run_supertrend_walkforward.py `
  --profile high_atr `
  --mode grid `
  --top-k 10 `
  --outdir results/walkforward/supertrend_high_atr
```

```powershell
python mtc_backtest/scripts/run_supertrend_walkforward.py `
  --profile short_atr `
  --mode grid `
  --top-k 10 `
  --outdir results/walkforward/supertrend_short_atr
```

## Supertrend toggle sweep
```powershell
python mtc_backtest/scripts/evaluate_supertrend_candidate_toggle_sweep.py
```

## Supertrend SL mode sweep
```powershell
python mtc_backtest/scripts/run_supertrend_sl_walkforward.py `
  --profile all `
  --mode random `
  --iters 200 `
  --top-k 20 `
  --outdir results/walkforward/supertrend_sl_full_fix_20260308_i200
```

## Supertrend percent-SL + risk joint search
```powershell
python mtc_backtest/scripts/run_supertrend_sl_walkforward.py `
  --profile pct `
  --mode random `
  --iters 500 `
  --top-k 25 `
  --space-file configs/spaces/supertrend_sl_pct_risk_joint_20260309.json `
  --outdir results/walkforward/supertrend_sl_pct_risk_joint_20260309_r500
```

## Supertrend percent-SL + risk local refine
```powershell
python mtc_backtest/scripts/run_supertrend_sl_walkforward.py `
  --profile pct `
  --mode grid `
  --space-file configs/spaces/supertrend_sl_pct_risk_joint_refine_20260309.json `
  --top-k 25 `
  --outdir results/walkforward/supertrend_sl_pct_risk_joint_refine_20260309_grid
```

## Supertrend TP sweep on top of current SL+risk winner
```powershell
python mtc_backtest/scripts/run_supertrend_tp_walkforward.py `
  --profile all `
  --mode grid `
  --top-k 30 `
  --candidate-source train_top_score `
  --outdir results/walkforward/supertrend_tp_full_20260309_grid_topscore30
```

## Supertrend BE sweep on top of current TP winner
```powershell
python -m scripts.walk_forward_validate `
  --train-case configs/cases/supertrend_be_wf_train_20260309.json `
  --target-case-1 configs/cases/supertrend_be_wf_target1_20260309.json `
  --target-case-2 configs/cases/supertrend_be_wf_target2_20260309.json `
  --mode grid `
  --iters 200 `
  --top-k 30 `
  --candidate-source train_top_score `
  --space-file configs/spaces/supertrend_be_walkforward_20260309.json `
  --outdir results/walkforward/supertrend_be_full_20260309_grid_topscore30
```

## Supertrend trailing sweep on top of current TP+BE winner
```powershell
python -m scripts.walk_forward_validate `
  --train-case configs/cases/supertrend_trailing_wf_train_20260309.json `
  --target-case-1 configs/cases/supertrend_trailing_wf_target1_20260309.json `
  --target-case-2 configs/cases/supertrend_trailing_wf_target2_20260309.json `
  --mode grid `
  --iters 200 `
  --top-k 30 `
  --candidate-source train_top_score `
  --space-file configs/spaces/supertrend_trailing_walkforward_20260309.json `
  --outdir results/walkforward/supertrend_trailing_full_20260309_grid_topscore30
```

## Objective compare + pareto buckets
```powershell
python mtc_backtest/scripts/compare_objective_reports.py --run-a <trials_a.csv> --run-b <trials_b.csv> --out <summary.json>
python mtc_backtest/scripts/export_pareto_buckets.py --pareto <pareto.json> --outdir <bucket_dir> --top-k 5
```
