# MCC Night Tail D009/D008 Guard - Codex GPT-5 - 2026-06-08

Scope: safety fix before running finished night-run enrichment into MCC.
No trading logic, Pine logic, MTC behavior, parity files, signal code, or scoring rules changed.

## Fix

`03_QUANTLENS/tools/mcc_night_tail.sh` now routes every Python step through:

```bash
python run_python_clean.py ...
```

This satisfies D009-revised by injecting `_scipy_shim.py` and using a cleaned process environment before scripts can import `scipy.stats`.

The PBO step now uses:

```bash
--max-combinations 100000
```

instead of `--max-combinations 0`, satisfying D008 / NIGHT_BATCHES guidance.

## Verification

```powershell
python run_python_clean.py -c "import _scipy_shim; print('RUNPY_OK')"
```

PASS: `RUNPY_OK`.

```powershell
& "C:\Program Files\Git\bin\bash.exe" -n MTC_COMMAND_CENTER/03_QUANTLENS/tools/mcc_night_tail.sh
```

PASS: exit code 0.

```powershell
rg -n "python |--max-combinations 0|run_python_clean|RUNPY" MTC_COMMAND_CENTER\03_QUANTLENS\tools\mcc_night_tail.sh
```

PASS: no bare `python` launch remains except the `RUNPY` definition; no uncapped PBO remains.

## Next

Run `mcc_night_tail.sh` on eligible finished runs with `MEGA_walk_forward_results.json`:

- `full_sweep_2026-06-07`
- `batch023_034_2026-06-07`

`night_1m_2026-06-07` still needs export diagnosis because the run directory does not currently contain top-level `MEGA_walk_forward_results.json`.
