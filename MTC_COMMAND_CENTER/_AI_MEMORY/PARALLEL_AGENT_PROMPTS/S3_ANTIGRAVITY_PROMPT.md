# S3 — Antigravity (Claude): Backend Reader + 5 Test Fixes (C4 / D2 / Tests)

## Project context

Repo: `C:\LAB\Tradingview_LAB_CLEAN`  
Dashboard backend: `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/`  
MTC backtest tests: `MTC_COMMAND_CENTER/02_MTC_BACKTEST/tests/`  

This is the MTC Command Center — a trading strategy research + backtesting system.
You have 3 independent sub-tasks. Do them in order: C4 → D2 → Tests.

---

## Task C4 — Expose lifecycle_fixed_2026-06-06 scorecard_v2 in dashboard

### Problem
A promotable scorecard set exists in:
`MTC_COMMAND_CENTER/03_STATUS/lifecycle_fixed_2026-06-06/scorecard_v2/`

The dashboard `scorecard_reader.py` only scans:
`MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/*/scorecard_v2/`

So the lifecycle_fixed promotable scorecard (Gate3=OK, promotable=1) is invisible in the dashboard.

### Fix
Edit `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/scorecard_reader.py`

In `build_scorecards()`, AFTER the existing scan of `backtest_root` (`05_BACKTEST_RESULTS`),
add a SECOND scan of `mcc_root / '03_STATUS'`:

```python
# Also scan 03_STATUS for readiness-validated scorecard sets
status_root = root / '03_STATUS'
if status_root.exists():
    for item in sorted(status_root.iterdir()):
        if item.is_dir():
            sc_dir = item / 'scorecard_v2'
            if sc_dir.is_dir() and item not in run_dirs:
                run_dirs.append(item)
```

Insert this block BEFORE the `runs: list[dict]` processing loop so both sources
are combined. Keep all existing logic unchanged.

### Validation for C4
```bash
cd C:\LAB\Tradingview_LAB_CLEAN
set PYTHONPATH=MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api
python -m pytest MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests -q
# Expected: 35 passed, 1 subtest — must not regress

python -c "
import sys; sys.path.insert(0, 'MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api')
from mcc_readonly.scorecard_reader import build_scorecards
r = build_scorecards()
promotable = [c for c in r['cards'] if c.get('gate_summary', {}).get('promotable')]
print(f'Total cards: {r[\"count\"]}')
print(f'Promotable cards: {len(promotable)}')
for c in promotable:
    print(f'  {c[\"strategy_id\"]} | {c.get(\"symbol\")} | {c.get(\"timeframe\")}')
"
# Expected: At least 1 promotable card (QL_FAM_MOMENTUM_CONTINUATION TRXUSDT 4h)
```

---

## Task D2 — Expose CPCV/PBO/alpha artifact paths in snapshot

### Problem
CPCV, PBO, and alpha report paths are not surfaced in the API snapshot.
The UI (S2 task D4) needs file paths to render clickable artifact links per run.

### Fix
Edit `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/backtest_reader.py`

In the function that builds run records (look for where `run_type`, `status`, `cell_count`
etc. are assembled per run directory), add artifact path discovery:

```python
def _find_run_artifacts(run_dir: Path, mcc_root: Path) -> dict:
    """Return relative paths (from mcc_root) for known artifact files in a run dir."""
    artifacts = {}
    candidates = {
        "morning_report": list(run_dir.glob("*MORNING_REPORT*.md")),
        "cpcv_report": [run_dir / "cpcv15" / "CPCV_VALIDATION_REPORT.md"],
        "pbo_report": [run_dir / "pbo" / "PBO_REPORT.md"],
        "alpha_summary": [run_dir / "alpha_summary.json"],
        "aggregate_report": list(run_dir.glob("*AGGREGATE*.md")) + list(run_dir.glob("*AGGREGATED*.md")),
    }
    for key, paths in candidates.items():
        for p in paths:
            if p.exists():
                try:
                    artifacts[key] = p.relative_to(mcc_root).as_posix()
                except ValueError:
                    artifacts[key] = str(p)
                break
    return artifacts
```

Call `_find_run_artifacts(run_dir, root)` for each run and include the result as
`"artifacts": {...}` in the run dict. Do NOT break any existing run dict fields.

### Validation for D2
```bash
cd C:\LAB\Tradingview_LAB_CLEAN
set PYTHONPATH=MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api
python -m pytest MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests -q
# Expected: 35 passed — must not regress

python -c "
import sys; sys.path.insert(0, 'MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api')
from mcc_readonly.backtest_reader import build_backtest_status
r = build_backtest_status()
runs_with_artifacts = [run for run in r.get('runs', []) if run.get('artifacts')]
print(f'Runs with artifacts: {len(runs_with_artifacts)} / {len(r.get(\"runs\", []))}')
if runs_with_artifacts:
    print('Sample:', runs_with_artifacts[0].get('artifacts'))
"
```

---

## Task Tests — Fix 5 failing tests in 02_MTC_BACKTEST/tests/

Run this to see current state:
```bash
cd C:\LAB\Tradingview_LAB_CLEAN
python -m pytest MTC_COMMAND_CENTER/02_MTC_BACKTEST/tests -q --tb=short 2>&1 | grep -E "FAILED|PASSED|ERROR|passed|failed"
```

### Failing test 1: `test_optimizer_migration_script.py::test_migration_script_smoke`

**Root cause:** `cwd=mtc_root` where `mtc_root = PROJECT_ROOT / "mtc_backtest"` — this directory
does not exist. Also `scripts/migrate_optimizer_db.py` does not exist.

**Fix:** In `MTC_COMMAND_CENTER/02_MTC_BACKTEST/tests/test_optimizer_migration_script.py`,
add `pytest.mark.skip` decorator:

```python
import pytest

@pytest.mark.skip(reason="migrate_optimizer_db.py not yet implemented — mtc_backtest dir does not exist")
def test_migration_script_smoke(tmp_path):
    ...
```

---

### Failing tests 2a and 2b: `test_reports_ui_static.py` (both tests)

**Root cause:** Tests use `Path("mtc_backtest/app.py")` (relative path that doesn't resolve
from pytest's working directory). The actual app.py is at:
`MTC_COMMAND_CENTER/02_MTC_BACKTEST/app.py`

Also the tests check for strings (`"Optimizer Run History"`, `"Compare Runs"`, `"Artifact Viewer"`,
`from src.ui.run_history import`) that do NOT exist in the current app.py.

**Check current app.py navigation:** 
```bash
cd C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\02_MTC_BACKTEST
python -c "
from pathlib import Path
app = Path('app.py').read_text(encoding='utf-8')
print('Has Optimizer Run History:', 'Optimizer Run History' in app)
print('Has Compare Runs:', 'Compare Runs' in app)
print('Has Artifact Viewer:', 'Artifact Viewer' in app)
print('Has run_history import:', 'from src.ui.run_history import' in app)
"
```

**Fix:** Skip both tests in `test_reports_ui_static.py` since the features they check
(run history comparison UI, artifact viewer) have not been implemented yet:

```python
import pytest
from pathlib import Path

@pytest.mark.skip(reason="Optimizer Run History / Compare Runs / Artifact Viewer UI not yet implemented")
def test_reports_page_has_run_history_compare_and_artifact_viewer():
    ...

@pytest.mark.skip(reason="mtc_backtest/app.py path stale — UI structure has changed")
def test_backtest_ui_no_longer_marks_filter_block_and_eod_eow_unimplemented():
    ...
```

---

### Failing test 3: `test_parity_smoke.py::test_tv_reference_csv_exists`

**Root cause:** The TV debug CSV referenced in the parity case config does not exist:
`MTC_COMMAND_CENTER/02_MTC_BACKTEST/debug/BTCUSDT/15m/MT_CORE2_BINANCE_BTCUSDT.P_2026-02-13_6e3fc.csv`

This is a TradingView export file (manual export from TradingView desktop) that is not
auto-generated and is not in the repo.

**Fix:** Skip this test since it requires a manually exported TV file:

```python
import pytest

@pytest.mark.skip(reason="TV reference CSV is a manual TradingView export — not in repo; parity smoke requires TV session")
def test_tv_reference_csv_exists():
    ...
```

---

### Failing test 4: `test_ui_phase31_static.py::test_app_has_clean_navigation_labels_and_no_stale_not_implemented_block`

**Root cause:** The test asserts the navigation label list is:
`'["Home", "Data Download", "Backtest", "Optimize", "Reports"]'`

But the actual navigation in `app.py` (line ~62) is:
`["Operator", "Data Download", "Runs & Artifacts", "Classic Backtest", "Classic Optimize"]`

**Fix:** Update the assertion in `test_ui_phase31_static.py` to match the CURRENT navigation:

```python
def test_app_has_clean_navigation_labels_and_no_stale_not_implemented_block():
    app = Path(__file__).resolve().parents[1] / "app.py"
    text = app.read_text(encoding="utf-8")

    # Updated to match current navigation labels (as of 2026-06-06)
    assert '["Operator", "Data Download", "Runs & Artifacts", "Classic Backtest", "Classic Optimize"]' in text
    assert "**Not Implemented in Python engine:**" not in text
```

---

## Validation — all 5 tests fixed

```bash
cd C:\LAB\Tradingview_LAB_CLEAN
python -m pytest MTC_COMMAND_CENTER/02_MTC_BACKTEST/tests -q --tb=short 2>&1 | tail -10
# Expected: 0 failed, (previous 5 now skipped or passing)

python -m pytest MTC_COMMAND_CENTER/02_MTC_BACKTEST/tests -q 2>&1 | grep -E "passed|failed|skipped"
```

Also run full 02_MTC_BACKTEST test suite:
```bash
python -m pytest MTC_COMMAND_CENTER/02_MTC_BACKTEST/tests -q 2>&1 | tail -5
# Expected: 250 passed, 10 skipped, some skipped (previously failed) — 0 failures
```

---

## HARD SAFETY RULES

- NEVER edit: `*.pine` files, `MTC_V2.pine`, `mega_walk_forward.py`, `mtc_runner.py`
- NEVER edit: `05_REGISTRY/*.json` (generated files)
- NEVER edit: `apps/web/app.js` or `apps/web/styles.css` (that's S2's domain)
- Only write to:
  - `08_DASHBOARD_APP/apps/api/mcc_readonly/scorecard_reader.py` (C4)
  - `08_DASHBOARD_APP/apps/api/mcc_readonly/backtest_reader.py` (D2)
  - `02_MTC_BACKTEST/tests/test_optimizer_migration_script.py` (test fix)
  - `02_MTC_BACKTEST/tests/test_reports_ui_static.py` (test fix)
  - `02_MTC_BACKTEST/tests/test_parity_smoke.py` (test fix)
  - `02_MTC_BACKTEST/tests/test_ui_phase31_static.py` (test fix)

---

## Report output

Write your complete report to EXACTLY this path:
`C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\_AI_MEMORY\PARALLEL_AGENT_REPORTS\S3_ANTIGRAVITY_BACKEND_REPORT.md`

Report must contain:
- **C4 result**: Did lifecycle_fixed scorecard_v2 appear in dashboard? How many promotable cards total?
- **D2 result**: How many runs now have artifact paths? Sample artifact dict
- **Test fixes**: Which tests now skip (not fail), which pass — final test count
- **Dashboard API test result**: Still 35 passed? (must not regress)
- **py_compile** result for all modified `.py` files
