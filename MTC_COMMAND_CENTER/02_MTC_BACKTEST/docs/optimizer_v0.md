# Optimizer v0 Documentation

Optimizer v0 runs repeatable parameter searches (random/grid) over a TradingView-parity backtest engine.
Primary goals: determinism, crash-safe CSV persistence, and resume support.

---

## CLI Usage

### Basic Run

```bash
# Random search (default)
python -m src.optimizer_v0 run --case configs/cases/full_jul2025_jan2026_parity.json --mode random --iters 200 --seed 42 --workers 1 --out ../results/run_200.csv

# Grid search
python -m src.optimizer_v0 run --case configs/cases/full_jul2025_jan2026_parity.json --mode grid --seed 42 --workers 1 --out ../results/grid.csv

External Search Space (JSON)

Use --space-file <path> to define parameters in an external JSON file.

python -m src.optimizer_v0 run \
  --case configs/cases/full_jul2025_jan2026_parity.json \
  --mode random --iters 200 --seed 42 \
  --space-file configs/space_example.json \
  --out ../results/space_run.csv \
  --workers 4

Precedence Rules

Parameter definition priority:

DEFAULT_PARAMS (fallback)

--space-file (overrides defaults)

--params JSON override (highest priority; legacy)

JSON Schema (--space-file)

A single file can define both grid and random sections.
Each section is a JSON object where keys are parameter paths (dot-notation) and values describe the distribution/range.

Top-level
{
  "grid": { ... },
  "random": { ... }
}

Grid parameters

Grid entries support either explicit values or a numeric range.

Option A: explicit values

{
  "grid": {
    "supertrend.factor": { "values": [5.5, 6.0, 6.5] }
  }
}


Option B: range

{
  "grid": {
    "supertrend.atr_len": { "low": 10, "high": 50, "step": 2, "dtype": "int" }
  }
}


Fields:

values: array (explicit values)

low, high, step: range definition

dtype: "int" or "float" (optional; default "float")

Random parameters

Random entries support:

dist: choice with values

dist: uniform_int with low/high

dist: uniform_float with low/high and optional step

choice

{
  "random": {
    "take_profit.atr_mult": { "dist": "choice", "values": [2.0, 2.5, 3.0, 3.5] }
  }
}


uniform_int

{
  "random": {
    "supertrend.atr_len": { "dist": "uniform_int", "low": 10, "high": 50 }
  }
}


uniform_float (optional step)

{
  "random": {
    "supertrend.factor": { "dist": "uniform_float", "low": 3.0, "high": 8.0, "step": 0.2 }
  }
}


Notes:

When step is provided for uniform_float, values are snapped/quantized to the step grid within bounds.

If dtype is omitted, floats are assumed.

Determinism & Resume
Determinism

Determinism means: same --seed + same search space + same case ⇒ identical CSV results across different --workers counts (ignoring runtime_s).

Determinism is maintained by:

Seeded RNG (--seed)

Canonical parameter-key formatting (e.g., float normalization used in resume keys)

Stable CSV persistence order (by idx)

Resume

If you re-run with the same --out file and same search settings, the optimizer detects completed trials and runs only missing ones.

You should see:

Resuming with <N> already completed trials.

Executing 0 trials ... when nothing is missing.

## Dry-run: print resolved search space
Example command:
```bash
python -m src.optimizer_v0 run --case configs/cases/full_jul2025_jan2026_parity.json --mode random --space-file configs/space_example.json --print-space
```

PowerShell verification example
cd C:\LAB\tradingview-lab\mtc_backtest
.\venv\Scripts\Activate.ps1
$env:PYTHONPATH = (Get-Location).Path

$OUTDIR="..\results"
mkdir $OUTDIR -Force | Out-Null
Remove-Item -Force $OUTDIR\space_seq.csv,$OUTDIR\space_par.csv -ErrorAction SilentlyContinue

python -m src.optimizer_v0 run --case .\configs\cases\full_jul2025_jan2026_parity.json --mode random --iters 20 --seed 42 --space-file .\configs\space_example.json --out $OUTDIR\space_seq.csv --workers 1
python -m src.optimizer_v0 run --case .\configs\cases\full_jul2025_jan2026_parity.json --mode random --iters 20 --seed 42 --space-file .\configs\space_example.json --out $OUTDIR\space_par.csv --workers 4

python -c "import pandas as pd; s=pd.read_csv(r'$OUTDIR\space_seq.csv').drop(columns=['runtime_s'], errors='ignore').sort_values('idx'); p=pd.read_csv(r'$OUTDIR\space_par.csv').drop(columns=['runtime_s'], errors='ignore').sort_values('idx'); pd.testing.assert_frame_equal(s.reset_index(drop=True), p.reset_index(drop=True)); print('Determinism Check: PASS')"

### 6. Replay Candidates (v2.3)
Re-run a set of exported candidate JSON files to verify results or generate a consolidated CSV summary.

```bash
python -m src.optimizer_v0 replay-candidates \
  --case configs/cases/full_jul2025_jan2026_parity.json \
  --candidates-dir ../results/candidates \
  --out ../results/replay_summary.csv \
  --min-trades 5 --max-dd 20
```

This command:
1. Loads all `.json` files from `candidates-dir`.
2. Runs a single backtest for each candidate (sequentially).
3. Writes a deterministic summary CSV to `--out`.

### 7. Workflow Automation (v2.3)
A PowerShell runbook is available to automate candidate filtering and targeted validation.

**Run from the `mtc_backtest` folder:**
```powershell
cd mtc_backtest
.\runbook.ps1
```

This script:
1. Shortlists top 3 candidates by score from `replay_summary.csv`.
2. Copies them to `results/shortlist`.
3. Replays them against target cases (Sep-Dec 2025, Jan 2026).
4. Reports a unified summary table.

## Runbook

To validate top candidates across multiple targets and generate a ranked report:

```powershell
# From mtc_backtest/ root
powershell -ExecutionPolicy Bypass -File .\runbook.ps1
```

This workflow:
1. Shortlists top 3 candidates from `replay_summary.csv`.
2. Replays them against Sep-Dec 2025 and Jan 2026 targets.
3. Outputs a deterministic ranking based on combined net profit and max drawdown.



