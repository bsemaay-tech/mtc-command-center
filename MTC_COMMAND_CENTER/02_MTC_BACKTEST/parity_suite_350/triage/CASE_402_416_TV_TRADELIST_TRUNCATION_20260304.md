# Case 402/416 TV Trade List Truncation Check (2026-03-04)

## Summary
- Both cases show full overlap parity PASS when compared on common window (`--clip-overlap`).
- Both cases fail without overlap clip because TV trade list ends ~125-129 days before case end date.
- This pattern is consistent with an early TV trade-list end (candidate) rather than first-divergence logic mismatch inside overlap.

## Evidence Table
```
case   case_end_utc           last_tv_exit_utc        gap_days tv_unique
402    2026-02-01 00:00:00    2025-09-25 01:30:00       128.94       123
416    2026-02-01 00:00:00    2025-09-28 20:30:00       125.15       129
```

## Compare Outputs
### Case 402
- clip-overlap compare: `parity_suite_350/compare_runs/isolation_402_refresh.csv` -> strict PASS
- no-clip compare: `parity_suite_350/compare_runs/isolation_402_noclip.csv` -> strict FAIL (extra PY trades after TV cutoff)

### Case 416
- clip-overlap compare: `parity_suite_350/compare_runs/isolation_416_refresh.csv` -> strict PASS
- no-clip compare: `parity_suite_350/compare_runs/isolation_416_noclip.csv` -> strict FAIL (extra PY trades after TV cutoff)

## Practical Interpretation
- Inside the shared timeline, TV and Python are aligned.
- Remaining FAIL status is caused by TV list cutoff horizon, not by immediate lifecycle mismatch on compared bars.
- If parity policy requires full raw-count equality, these need fresh TV exports with non-truncated trade lists.
