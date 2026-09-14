| evidence item from the packet | observed | file:line or artefact path | GREEN / RED-as-expected / NOT OBSERVED |
| --- | --- | --- | --- |
| one `GAP …` line per hole with first/last missing UTC | `GAP symbol=BTC interval=1h first_missing=1970-01-01T02:00:00Z last_missing=1970-01-01T02:00:00Z` | `C:/tmp/P026_DRILLS_TA_20260914/drills/D-12/stdout.txt:1` | GREEN |
| `GAPS: <n>` total | `GAPS: 1` | `C:/tmp/P026_DRILLS_TA_20260914/drills/D-12/stdout.txt:2` | GREEN |
| command exit code 0 | `gap-report-rc=0` | `C:/tmp/P026_DRILLS_TA_20260914/drills/D-12/stdout.txt:3` | GREEN |
| synthetic archive fixture | month file written under `fixtures/d12/archive` | `C:/tmp/P026_DRILLS_TA_20260914/fixtures/d12/archive/bars/HYPERLIQUID/BTC/1h/1970-01.jsonl` | GREEN |
