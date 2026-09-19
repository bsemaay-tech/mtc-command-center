| evidence item from the packet | observed | file:line or artefact path | GREEN / RED-as-expected / NOT OBSERVED |
| --- | --- | --- | --- |
| first check `silent`, rc 2 | `step1-silent: rc=2`; JSON `state=silent` | `C:/tmp/P026_DRILLS_TA_20260914/drills/D-10/stdout.txt:1` `C:/tmp/P026_DRILLS_TA_20260914/drills/D-10/stdout.txt:3` | RED-as-expected |
| then exactly one `recovered` with `recovered_from: "silent"` | notifier line `state=recovered` `recovered_from=silent`; step2 `rc=0` | `C:/tmp/P026_DRILLS_TA_20260914/drills/D-10/stdout.txt:4` `C:/tmp/P026_DRILLS_TA_20260914/drills/D-10/stdout.txt:12` | GREEN |
| then a second `silent` event | `step3-silent: rc=2`; notifier third line `state=silent` | `C:/tmp/P026_DRILLS_TA_20260914/drills/D-10/stdout.txt:7` `C:/tmp/P026_DRILLS_TA_20260914/drills/D-10/stdout.txt:13` `C:/tmp/P026_DRILLS_TA_20260914/fixtures/watchdog_state/recovery_notifier.jsonl` | RED-as-expected |
