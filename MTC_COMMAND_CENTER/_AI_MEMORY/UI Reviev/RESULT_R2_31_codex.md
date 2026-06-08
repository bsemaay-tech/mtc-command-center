# R2-31 Scorecard Freshness - Codex GPT-5 - 2026-06-08

Scope: display-only freshness fix for Strategy Detail header.
No trading logic, Pine logic, MTC behavior, parity files, or score math changed.

## Problem

The Strategy Detail header used `snapshotFreshness()` with only snapshot/current-status timestamps.
That could imply the displayed Gate score was fresh when the selected `scorecard_v2` artifact was older.

Real smoke after the fix showed the mismatch clearly:

```text
row scorecard_v2.updated_at = 2026-06-06T07:29:46.924238+00:00
snapshot_ts                 = 2026-05-30T00:00:00+03:00
```

## Fix

- `08_DASHBOARD_APP/apps/api/mcc_readonly/scorecard_reader.py`
  - Adds normalized `updated_at` to each scorecard display card from the scorecard JSON file mtime.
  - The scorecard JSON schema has no internal generated/updated timestamp fields, so file mtime is the honest artifact timestamp.

- `08_DASHBOARD_APP/apps/web/app.js`
  - Passes the selected `scorecard_v2` into `snapshotFreshness(scorecardV2)`.
  - Displays `Scorecard: <timestamp>` in the Strategy Detail header when a scorecard is linked.
  - Falls back to `Snapshot: <timestamp>` only when no scorecard artifact is linked.
  - Tooltip distinguishes the scorecard file timestamp from the snapshot refresh timestamp.

## Verification

```powershell
python -m py_compile MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\scorecard_reader.py
```

PASS.

```powershell
node --check MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js
```

PASS.

```powershell
$env:PYTHONPATH='C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api'
python -m unittest discover -s MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\tests -p 'test_*.py'
```

PASS: 35 tests.

Snapshot smoke:

```text
scorecards count: 360
all scorecard cards have updated_at: True
candidate_pipeline row has scorecard_v2.updated_at: True
```

Browser tool note: the in-app Browser tool was not exposed in this turn by tool discovery, so verification used API snapshot smoke plus JS syntax check instead of visual screenshot.
