# Phase 2D Outcome

## Result
- Restored only the minimal `pinets` package from legacy root `node_modules` into the clean backtest workspace.
- PineTS load blocker is resolved: `mtc_bridge.mjs` ran and generated `mtc_signals.json`.
- Smoke still failed and was not retried.
- New blocker: `pine_trades.py` is missing from `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\02_MTC_BACKTEST\pine_trades.py`.

## Smoke
- Command: `python parity_compare.py --fetch-fresh --tracker-case AUTO_061`.
- Exit code: `1`.
- Log: `C:\LAB\Tradingview_LAB_CLEAN\docs\migration_manifests\phase2d_smoke_AUTO_061.log`.

## Dependency Restore
- Source: `C:\LAB\tradingview-lab\node_modules\pinets`.
- Target: `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\02_MTC_BACKTEST\node_modules\pinets`.
- Files copied: `365`.
- Hash mismatches: `0`.

## Pine Safety
- Compared 24 `.pine` files against the Phase 1 Pine manifest.
- Pine mismatch count: `0`.
- Pine source was not modified.

## Diagnostic
- Legacy candidate found: `C:\LAB\tradingview-lab\pine_trades.py`.
- Clean expected path is absent: `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\02_MTC_BACKTEST\pine_trades.py`.

## Files Written
- `C:\LAB\Tradingview_LAB_CLEAN\docs\migration_manifests\phase2d_pinets_source_candidates.json`
- `C:\LAB\Tradingview_LAB_CLEAN\docs\migration_manifests\phase2d_pinets_restore_manifest.csv`
- `C:\LAB\Tradingview_LAB_CLEAN\docs\migration_manifests\phase2d_pinets_restore_summary.json`
- `C:\LAB\Tradingview_LAB_CLEAN\docs\migration_manifests\phase2d_smoke_AUTO_061.log`
- `C:\LAB\Tradingview_LAB_CLEAN\docs\migration_manifests\phase2d_smoke_AUTO_061_summary.json`
- `C:\LAB\Tradingview_LAB_CLEAN\docs\migration_manifests\phase2d_pine_trades_py_candidates.json`
- `C:\LAB\Tradingview_LAB_CLEAN\docs\migration_manifests\phase2d_pine_only_sha256_compare.json`
- `C:\LAB\Tradingview_LAB_CLEAN\docs\migration_manifests\phase2d_outcome.json`
- `C:\LAB\Tradingview_LAB_CLEAN\docs\migration_manifests\phase2d_outcome.md`

## Next Approval
- Recommended next command: `APPROVE_PHASE_2E_RESTORE_PINE_TRADES_HELPER_AND_RERUN_SMOKE`.
