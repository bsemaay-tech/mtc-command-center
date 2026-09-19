| evidence item from the packet | observed | file:line or artefact path | GREEN / RED-as-expected / NOT OBSERVED |
| --- | --- | --- | --- |
| `run_end.status != ok` refuses with "restore requires one complete successful P026 run" | `status: ERROR ValueError: restore requires one complete successful P026 run` | `C:/tmp/P026_DRILLS_TA_20260914/drills/D-7/stdout.txt:1` | RED-as-expected |
| `errors` non-empty refuses with the same complete-run message | `errors: ERROR ValueError: restore requires one complete successful P026 run` | `C:/tmp/P026_DRILLS_TA_20260914/drills/D-7/stdout.txt:2` | RED-as-expected |
| `files` count disagreeing with `file` records | `files: ERROR ValueError: restore requires one complete successful P026 run` | `C:/tmp/P026_DRILLS_TA_20260914/drills/D-7/stdout.txt:3` | RED-as-expected |
| `skipped` record inside the run | `skipped: ERROR ValueError: restore requires one complete successful P026 run` | `C:/tmp/P026_DRILLS_TA_20260914/drills/D-7/stdout.txt:4` | RED-as-expected |
| third `file` member (member-set check) | `third: ERROR ValueError: restore requires one complete successful P026 run` (adapter uses the same complete-run string at `:525`) | `C:/tmp/P026_DRILLS_TA_20260914/drills/D-7/stdout.txt:5` | RED-as-expected |
| malformed JSONL line refuses at `_decode_strict_jsonl` (`:99-120`) | `malformed: ERROR ValueError: invalid P026 manifest line 13` | `C:/tmp/P026_DRILLS_TA_20260914/drills/D-7/stdout.txt:6` `C:/tmp/P026_DRILLS_TA_20260914/wt/p030_closed_partition_backup_adapter.py:115` | RED-as-expected |
