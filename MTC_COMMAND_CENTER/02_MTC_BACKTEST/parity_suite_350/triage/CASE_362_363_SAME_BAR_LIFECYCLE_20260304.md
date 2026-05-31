# Case 362/363 Same-Bar Lifecycle Isolation (2026-03-04)

## Scope
- Target bar: `2025-10-03 17:00 UTC` (`18:00` in TV CSV local time, `Europe/London`).
- Problem to isolate: `TRAIL` exit and same-direction reentry on same bar.

## Result
- Case 362: strict parity `PASS` (177/177) via `compare_runs/isolation_362.csv`
- Case 363: strict parity `PASS` (177/177) via `compare_runs/isolation_363.csv`

## TV Trade Evidence
### 362 - parity_core_194_mode_v01
```
 Trade #       Type       Date and time Signal  Price USDT  Position size (qty)
     135  Exit long 2025-10-03 17:00:00    TP1    122884.9             0.207886
     135 Entry long 2025-10-03 10:45:00   Long    120258.3             0.207886
     136  Exit long 2025-10-03 18:00:00  TRAIL    122147.1             0.207887
     136 Entry long 2025-10-03 10:45:00   Long    120258.3             0.207887
     137  Exit long 2025-10-05 10:30:00     BE    123184.9             0.086162
     137 Entry long 2025-10-03 18:00:00   Long    122953.3             0.086162
     138  Exit long 2025-10-05 10:30:00     BE    123184.9             0.086163
     138 Entry long 2025-10-03 18:00:00   Long    122953.3             0.086163
```

### 363 - parity_bnd_194_mode_v02
```
 Trade #       Type       Date and time Signal  Price USDT  Position size (qty)
     135  Exit long 2025-10-03 17:00:00    TP1    122884.9             0.207886
     135 Entry long 2025-10-03 10:45:00   Long    120258.3             0.207886
     136  Exit long 2025-10-03 18:00:00  TRAIL    122147.1             0.207887
     136 Entry long 2025-10-03 10:45:00   Long    120258.3             0.207887
     137  Exit long 2025-10-05 10:30:00     BE    123184.9             0.086162
     137 Entry long 2025-10-03 18:00:00   Long    122953.3             0.086162
     138  Exit long 2025-10-05 10:30:00     BE    123184.9             0.086163
     138 Entry long 2025-10-03 18:00:00   Long    122953.3             0.086163
```

## Python Same-Bar Signal Lifecycle (16:30-17:30 UTC)
### 362 - parity_core_194_mode_v01
```
                timestamp  bar_index  longSignal_raw  shortSignal_raw  longSignal  shortSignal exitReason  exit_fired  exited_this_bar  same_bar_reentry_allowed same_bar_exit_trail_active_start  same_bar_exit_trailing_stop same_bar_exit_trail_start_hit  finalLongEntry  finalShortEntry entry_diag_reason
2025-10-03 16:30:00+00:00      43728            True            False       False        False        NaN       False            False                     False                              NaN                          NaN                           NaN           False            False               NaN
2025-10-03 16:45:00+00:00      43729            True            False       False        False        NaN       False            False                     False                              NaN                          NaN                           NaN           False            False               NaN
2025-10-03 17:00:00+00:00      43730            True            False        True        False      TRAIL        True             True                      True                             True                122147.625104                          True            True            False           entered
2025-10-03 17:15:00+00:00      43731            True            False       False        False        NaN       False            False                     False                              NaN                          NaN                           NaN           False            False               NaN
2025-10-03 17:30:00+00:00      43732            True            False       False        False        NaN       False            False                     False                              NaN                          NaN                           NaN           False            False               NaN
```

### 363 - parity_bnd_194_mode_v02
```
                timestamp  bar_index  longSignal_raw  shortSignal_raw  longSignal  shortSignal exitReason  exit_fired  exited_this_bar  same_bar_reentry_allowed same_bar_exit_trail_active_start  same_bar_exit_trailing_stop same_bar_exit_trail_start_hit  finalLongEntry  finalShortEntry entry_diag_reason
2025-10-03 16:30:00+00:00      43728            True            False       False        False        NaN       False            False                     False                              NaN                          NaN                           NaN           False            False               NaN
2025-10-03 16:45:00+00:00      43729            True            False       False        False        NaN       False            False                     False                              NaN                          NaN                           NaN           False            False               NaN
2025-10-03 17:00:00+00:00      43730            True            False        True        False      TRAIL        True             True                      True                             True                122147.625104                          True            True            False           entered
2025-10-03 17:15:00+00:00      43731            True            False       False        False        NaN       False            False                     False                              NaN                          NaN                           NaN           False            False               NaN
2025-10-03 17:30:00+00:00      43732            True            False       False        False        NaN       False            False                     False                              NaN                          NaN                           NaN           False            False               NaN
```

## Lifecycle Conclusion
- On `17:00 UTC`, Python records `exitReason=TRAIL`, `exited_this_bar=True`, and `same_bar_reentry_allowed=True`.
- The same bar also shows `same_bar_exit_trail_active_start=True` and `same_bar_exit_trail_start_hit=True`.
- `finalLongEntry=True` at `17:00 UTC`; at `17:15 UTC` no new entry attempt (`same_bar_reentry_allowed=False`).
- This confirms same-direction reentry is resolved on the **same bar lifecycle** and not deferred to next bar for 362/363.

## Code Anchor (Python)
- `src/engine/mtc_runner.py:1442-1453` same-direction TRAIL reopen gate uses `trail_was_active_start` and `trail_start_hit`.
- `src/engine/mtc_runner.py:2293-2296` / `2333-2336` exports trail stop and start-hit flags to debug signals.

## Note
- Historical mismatch symptom (reentry at next bar) was tied to TRAIL same-bar gating. Current lifecycle evidence shows 362/363 aligned with TV.