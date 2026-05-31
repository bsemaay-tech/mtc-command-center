# Optimizer Quickstart

## Prerequisites
- Python 3.11+
- `pip install -r requirements.txt`

## 1) Run optimizer
```powershell
python -m src.optimizer_v0 run `
  --case configs/cases/aug2025_parity.json `
  --mode random `
  --iters 200 `
  --seed 42 `
  --workers 1 `
  --out reports/benchmarks/benchmark_aug2025_200.csv `
  --db reports/benchmarks/benchmark_aug2025_200.db
```

## 2) Export pareto + candidates
```powershell
python -m src.optimizer_v0 run --case configs/cases/aug2025_parity.json --mode random --iters 200 --pareto-out results/pareto.json
python -m src.optimizer_v0 export-candidates --pareto results/pareto.json --outdir results/candidates --top-k 10 --overwrite
```

## 3) Replay candidates on target windows
```powershell
python -m src.optimizer_v0 replay-candidates --case configs/cases/target_sep2025_dec2025.json --candidates-dir results/candidates --out results/replay_target1.csv --min-trades 10 --max-dd 40
python -m src.optimizer_v0 replay-candidates --case configs/cases/target_jan2026.json --candidates-dir results/candidates --out results/replay_target2.csv --min-trades 10 --max-dd 40
```
