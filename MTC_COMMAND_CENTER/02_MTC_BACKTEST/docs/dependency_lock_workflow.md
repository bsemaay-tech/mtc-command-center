# Dependency Lock Workflow

## Baseline
- Canonical dependency declaration: `pyproject.toml`
- Runtime install path remains `requirements.txt` compatible.

## Update process
1. Create a clean virtualenv.
2. Install baseline dependencies:
```powershell
pip install -r requirements.txt
```
3. Freeze exact versions:
```powershell
pip freeze | Sort-Object > requirements-lock.txt
```
4. Validate:
```powershell
python -m pytest mtc_backtest/tests -v
```
5. Commit both files when dependency changes are intentional:
- `requirements.txt`
- `requirements-lock.txt`
