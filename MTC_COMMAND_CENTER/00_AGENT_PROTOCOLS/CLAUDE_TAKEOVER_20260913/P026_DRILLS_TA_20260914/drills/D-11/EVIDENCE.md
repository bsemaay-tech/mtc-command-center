| evidence item from the packet | observed | file:line or artefact path | GREEN / RED-as-expected / NOT OBSERVED |
| --- | --- | --- | --- |
| (i) `IDENTICAL_REPLAY_NOOP`, nothing appended | `case-i-first: status=APPENDED lines=1`; `case-i-replay: status=IDENTICAL_REPLAY_NOOP lines=1` | `C:/tmp/P026_DRILLS_TA_20260914/drills/D-11/stdout.txt:2` `C:/tmp/P026_DRILLS_TA_20260914/drills/D-11/stdout.txt:3` | GREEN |
| (i) cursor seeded to the replayed bar | `cursor={('BTC', '1h'): 3600000}` | `C:/tmp/P026_DRILLS_TA_20260914/drills/D-11/stdout.txt:3` | GREEN |
| (ii) same-slot correction refusal (packet OR branch) | `case-ii: ERROR CollectionRefused: differing same-producer bar requires an approved correction contract` | `C:/tmp/P026_DRILLS_TA_20260914/drills/D-11/stdout.txt:5` | RED-as-expected |
| (iii) WS_LIVE-only gap scan refuses after snapshot-filled history | `case-iii: ERROR CollectionRefused: persisted WS_LIVE sequence has a gap at 1970-01-01T01:00:00Z` | `C:/tmp/P026_DRILLS_TA_20260914/drills/D-11/stdout.txt:7` `C:/tmp/P026_DRILLS_TA_20260914/fixtures/d11/restart_gap/bars/HYPERLIQUID/BTC/1h/1970-01.jsonl` | RED-as-expected |
