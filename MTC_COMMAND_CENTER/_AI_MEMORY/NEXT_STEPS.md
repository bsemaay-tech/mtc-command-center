# NEXT_STEPS

## Immediate
- Review Phase 1 verification output (`docs/migration_manifests/phase1_apply_summary.json`, `phase1_residual_inventory.csv`) — sign-off pending.
- Decide hardcoded path rewrite policy for the 18 active scripts (Barış approval).
- Decide CHECK 1 legacy re-freeze approach: NTFS DACL deny-write on `C:\LAB\tradingview-lab` vs accept divergence + document.

## Waiting On
- Barış approval for post-copy path rewrites.
- Barış decision on legacy re-freeze (NTFS DACL).

## Recently Closed (2026-05-31)
- Phase 6 audit artifacts committed (`2a38d19`).
- CHECK 9 manifest hash format fixed — full SHA256 + Phase 5 divergence notes (`c3e78f4`).
- CHECK 8 xlsx-missing warning suppressed (CSV-only mode) — smoke re-verified PASS (`d35e620`).
- `update_tracker.py` documented as deferred one-shot in hardcoded path TODO (`1b7caff`).
