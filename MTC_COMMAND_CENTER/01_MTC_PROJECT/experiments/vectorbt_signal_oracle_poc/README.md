# vectorbt Signal Oracle POC

Purpose: consume normalized signal CSV files and run a fast signal-array approximation.

This is not exact MTC strategy execution parity. It is useful for coarse parameter sweeps and sanity checks after PineTS or the Python engine has produced normalized signals.

Runner:

```powershell
python parity_oracles/engines/vectorbt_runner.py --case cases/synthetic_multi_oracle_case.json --out-dir reports/parity/SYNTH_001/vectorbt --signals reports/parity/SYNTH_001/pinets/normalized_signals.csv
```
