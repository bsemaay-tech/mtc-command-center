# Phase 2B Smoke Case Diagnostic

## Result
- `case_110` is not a valid `--tracker-case` value for `parity_compare.py`.
- `case_110` exists in the export-suite CSV and `TW_EXPORT_CASES_V2`, but it is absent from `MTC_V2_PARITY_CASES.csv`.
- `parity_compare.py --tracker-case` loads only `MTC_V2_PARITY_CASES.csv` by `case_id`, so the failure happened before the smoke comparison could run.

## Recommended Smoke Case
- Use `AUTO_061` for the corrected Phase 2 smoke.
- Evidence: `AUTO_061` is the newest dated tracker-backed PASS row, with `llm_last_run_utc=2026-05-29T18:26:37.347324+00:00`.
- Fallback: `AUTO_001` is the baseline tracker case if a lower-risk baseline smoke is preferred.

## Exact Retry Command
```powershell
Set-Location -LiteralPath 'C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\02_MTC_BACKTEST'
python parity_compare.py --fetch-fresh --tracker-case AUTO_061 *> 'C:\LAB\Tradingview_LAB_CLEAN\docs\migration_manifests\phase2b_smoke_AUTO_061.log'
```

## Case Evidence
| Case | Valid for `--tracker-case` | Evidence | Recommendation |
|---|---:|---|---|
| `AUTO_061` | Yes | Newest dated PASS row in `MTC_V2_PARITY_CASES.csv`; status `DONE`; parity verdict `PASS`. | Use for corrected smoke. |
| `AUTO_001` | Yes | Baseline PASS tracker row and default case. | Fallback only. |
| `case_110` | No | Present in export-suite CSV, absent from tracker CSV `case_id`. | Do not use with `--tracker-case`. |

## Caveats
- Existing copied `AUTO_061` artifact is stale/inconsistent (`override_source=AUTO_050`, bars `8760` while tracker row says bars `1000`); a fresh smoke should regenerate clean artifacts.
- Archived machine-readable `case_110` report found at `C:\LAB\tradingview-lab_ARCHIVE_2026-05-31\reports\tracker_cases\case_110\parity_compare.json` reports `MISMATCH` from 2026-04-09.
- The 2026-05-29 `case_110` PASS claim is present in handoff text, but not represented as a runnable `--tracker-case` row.

## Files Written
- `C:\LAB\Tradingview_LAB_CLEAN\docs\migration_manifests\phase2b_smoke_case_diagnostic.json`
- `C:\LAB\Tradingview_LAB_CLEAN\docs\migration_manifests\phase2b_smoke_case_diagnostic.md`
- `C:\LAB\Tradingview_LAB_CLEAN\docs\migration_manifests\phase2b_smoke_case_candidates.csv`

## Safety
- Legacy archive was inspected read-only only.
- No Pine files were modified.
- No smoke rerun was performed in this diagnostic step.
