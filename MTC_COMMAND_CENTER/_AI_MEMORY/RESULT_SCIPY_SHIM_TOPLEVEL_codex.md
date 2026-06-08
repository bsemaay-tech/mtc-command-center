# SciPy Shim Top-Level Import Fix - Codex GPT-5 - 2026-06-08

Scope: safety fix discovered while preparing MCC night-run enrichment.
No trading logic, Pine logic, MTC behavior, parity files, signal code, or scoring rules changed.

## Problem

`run_python_clean.py` injects `_scipy_shim.py`, but the shim only pre-seeded `scipy.stats`.
Some tools import with:

```python
from scipy import stats
```

When running under the Codex bundled Python, `numpy` is available but `scipy` is not installed. That import style failed before the shim could satisfy it:

```text
ModuleNotFoundError: No module named 'scipy'
```

This blocked CPCV generation in `mcc_night_tail.sh`.

## Fix

`03_QUANTLENS/tools/_scipy_shim.py` now also creates a fake top-level `scipy` module and attaches the fake `stats` namespace to it.

Supported import styles now include:

```python
import scipy.stats
from scipy import stats
```

## Verification

```powershell
C:\Users\bsema\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe MTC_COMMAND_CENTER\03_QUANTLENS\tools\run_python_clean.py -c "from scipy import stats; import numpy; print('shim', round(stats.norm.cdf(0),3), numpy.__version__)"
```

PASS:

```text
shim 0.5 2.3.5
```

Focused CPCV smoke with Codex runtime Python:

```text
Wrote ...\cpcv_debug_full\cpcv_results.json
Wrote ...\cpcv_debug_full\CPCV_VALIDATION_REPORT.md
```

Git Bash syntax check for `mcc_night_tail.sh`: PASS.
