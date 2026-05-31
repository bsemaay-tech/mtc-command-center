# Optimization Next Steps

## Ordered Steps

1. Finalize the detached runner script for the big overnight resume.
2. Validate the detached runner with a tiny 5-20 evaluation smoke, not the full grid.
3. Verify `heartbeat.log` continues to update if the Codex UI is closed.
4. Verify the Python optimizer process remains active after Codex UI closure.
5. Run the big resume with explicit `--max-workers 16`.
6. Do not exceed `16` workers until a new scaling benchmark proves a higher count is safe.
7. After resume completes or the time budget ends, review strict robust candidates, medium candidates, regime collapse, 1D weakness, and CHOPPY/CONSOLIDATING weakness.
8. Only then consider an `exits_refinement_v1` optimization pass.
9. Only after a strict robust candidate exists, prepare a TradingView release-audit candidate package.
10. Refresh the portable handoff package after docs and code stabilize.

## Stop Conditions

- Stop before overnight resume if post-run patch validation fails.
- Stop before overnight resume if resume/de-dup smoke fails.
- Stop before overnight resume if the detached-runner smoke or process-survival check fails.
- Stop before promotion if strict robust candidate count remains 0.
- Stop before package refresh if the package would include the external data bundle or heavy optimization outputs.

## 2026-04-28 Search-Space Reduction Update

- Full exhaustive grid is no longer the preferred default path for new feature/filter research.
- Staged optimization is required for search-space control.
- Producer-only seed extraction must happen before expensive exit, filter, gate, or regime-mitigation optimization.
- Use `optimization/parameter_library/README.md` as the source of research seeds.
- Medium candidates may seed second-pass refinement but cannot become Pine defaults.
- `1D` may require separate profile handling.
- CHOPPY/CONSOLIDATING weakness should be addressed through the regime-mitigation stage.
- Methodology: `docs/optimization/SEARCH_SPACE_REDUCTION_AND_SMART_SAMPLING.md`.

## 2026-04-28 Per-Asset/Timeframe Seed Ranking Update

1. Use `tools/build_per_asset_timeframe_seed_rankings.py` for all future staged optimization outputs.
2. Require `ranked/per_asset_timeframe_seed_candidates.csv` before exit/risk or filter/gate refinement.
3. Consume `optimization/parameter_library/<producer>/` seeds in the next refinement jobs.
4. Treat current Supertrend granular smoke seeds as schema proof only; run a proper producer-only seed extraction job before drawing parameter conclusions.
5. Keep medium candidates and smoke seeds out of Pine defaults.
