# DRILL_RESULTS

Per-drill summary. Outcome cells are composite; per-case rows follow. Nothing here is acceptance.

| drill | tier | ran? | outcome (GREEN / RED-as-expected / FAILED / SKIPPED) | evidence dir | residual (from "Does NOT prove") |
| --- | --- | --- | --- | --- | --- |
| D-1 | T-A | YES | 3 RED-as-expected + 1 GREEN | drills/D-1/EVIDENCE.md | Does not prove real path existence, writability, separate devices, or owner-ratified roots. |
| D-2 | T-A | YES | GREEN | drills/D-2/EVIDENCE.md | Does not prove a real copy would succeed, destination space, or read-back. Dry-run only. |
| D-3 | T-A | YES | GREEN | drills/D-3/EVIDENCE.md | Does not prove the partition was genuinely closed or that rows are the collector's rows. |
| D-3b | T-A | YES | 1 GREEN + 2 RED-as-expected | drills/D-3/EVIDENCE.md | Does not prove any production offset is the right high-water. |
| D-4 | T-A | YES | GREEN | drills/D-4/EVIDENCE.md | Does not prove restorability, second-device placement, or venue completeness. |
| D-5 | T-A | YES | GREEN | drills/D-5/EVIDENCE.md | Does not prove PLAN reconciliation or a production recovery procedure. Isolated restore used `cwd/tmp`. |
| D-6 | T-A | YES | 2 RED-as-expected (named P026 string not reached on snapshot-only; see deviations) | drills/D-6/EVIDENCE.md | Does not prove detection of a coordinated manifest+bytes tamper. |
| D-7 | T-A | YES | 6 RED-as-expected | drills/D-7/EVIDENCE.md | Does not prove a real interrupted backup produces exactly these manifests. |
| D-8 | T-A | YES | 3 GREEN + 4 RED-as-expected | drills/D-8/EVIDENCE.md | Does not prove anything watches the heartbeat or that a dead process is noticed remotely. |
| D-9 | T-A | YES | 1 GREEN + 8 RED-as-expected | drills/D-9/EVIDENCE.md | `--now` is a test hook. `local_log` is not phone delivery. |
| D-10 | T-A | YES | silent / recovered / silent as specified | drills/D-10/EVIDENCE.md | Does not prove behaviour when the ledger file itself is unreadable. |
| D-11 | T-A | YES | 2 GREEN + 2 RED-as-expected | drills/D-11/EVIDENCE.md | Fixture-level coded semantics only; not a real venue restart. |
| D-12 | T-A | YES | GREEN | drills/D-12/EVIDENCE.md | Compares stored bars against the interval grid only; not venue completeness. |
| D-13 | T-A | YES | RED-as-expected | drills/D-13/EVIDENCE.md | **RED half only; GREEN half not run (O-9)** |
| D-14 | T-A | YES | 1 GREEN + 3 RED-as-expected | drills/D-14/EVIDENCE.md | Stub `PublicMarketSource`; not the P030 venue acceptance gate. |
| D-15 | T-B | NOT RUN | SKIPPED | Not run | T-B/T-C out of lane. |
| D-16 | T-C | NOT RUN | SKIPPED | Not run | T-C + notifier + phone not authorized. |
| D-17 | T-C | NOT RUN | SKIPPED | Not run | T-C not authorized. |

## Per-case outcomes

### D-1
- (a) null `backup_root`: RED-as-expected. Outer `backup config is not runnable`; inner `backup config field 'backup_root' must be a non-empty string` (`stdout.txt:1-3`).
- (b) bulk store class: RED-as-expected (`stdout.txt:4`).
- (c) path ≠ stable prefix: RED-as-expected (`stdout.txt:5`).
- (d) intended config: GREEN (`stdout.txt:6`).

### D-2
- PLAN + header/footer: GREEN (`stdout.txt:1-4`).
- No `runs/` and no `manifest.jsonl` under `fixtures/backup_root_d2`: GREEN (`stdout.txt:5-7`).

### D-3
- Full-file capture, six receipt fields, snapshot size = high water: GREEN (`stdout.txt:1-3`).

### D-3b
- Inside-file record-boundary offset 620/1860, `record_count=1`: GREEN (`stdout.txt:4-5`).
- Mid-record offset 309: RED-as-expected `high-water prefix must end with newline` (`stdout.txt:7`).
- Truncated high water 1924 > 1860: RED-as-expected `source prefix is truncated below high water` (`stdout.txt:9`).

### D-4
- `run_id=opsa-20260914T061919.156Z`: GREEN (`stdout.txt:6`).
- Manifest types `run_start, file, file, run_end` with `status=ok errors=[]`: GREEN (`stdout.txt:11,14`).
- `readback=match` both members: GREEN (`stdout.txt:3-4,12-13`).
- Three byte comparisons before/after/archived all equal: GREEN (`stdout.txt:1,7,8`).
- Member set `{_P030_STABLE_PREFIX.json, source.jsonl}`: GREEN (`stdout.txt:15`).

### D-5
- Check-only then restore, both `status: ok`: GREEN (`stdout.txt:1-8`).
- Receipt `run_id` / `store_id` / `restored_prefix` + six identity fields: GREEN (`stdout.txt:13-19`).
- Members are regular files, not symlink/junction: GREEN (`stdout.txt:21-22`).
- Restored bytes = archived bytes: GREEN (`stdout.txt:23`).

### D-6
- Snapshot-byte tamper: RED-as-expected at `_verify_stable_receipt` (`snapshot prefix hash mismatch`, `stdout.txt:1`). Named P026 string not produced (see deviations). Target empty (`stdout.txt:2`).
- Receipt tamper (`state=tampered`): RED-as-expected `stable-prefix receipt state does not match contract` (`stdout.txt:4`). Target empty (`stdout.txt:5`).

### D-7
- status / errors / files / skipped / third: each RED-as-expected `restore requires one complete successful P026 run` (`stdout.txt:1-5`).
- malformed JSONL: RED-as-expected `invalid P026 manifest line 13` (`stdout.txt:6`).

### D-8
- Extra field (isolated dir): RED-as-expected (`stdout.txt:1`).
- Fractional `emitted_at` only: RED-as-expected UTC-Z grammar (`stdout.txt:2`).
- Non-null `reconciliation_progress`: RED-as-expected (`stdout.txt:3`).
- Late `last_accepted_timestamp_utc`: RED-as-expected (`stdout.txt:4`).
- Emit + verify + available sidecar `age_seconds=0`: GREEN (`stdout.txt:5-8`). Surviving `fixtures/heartbeats/*.hb.json` is P026-shaped (`stdout.txt:9-10`).

### D-9
Each case used its own state dir.
- `ok` rc=0: GREEN (`stdout.txt:8`).
- `silent` rc=2 + notifier: RED-as-expected (`stdout.txt:15,21`).
- `missing` rc=2 + notifier: RED-as-expected (`stdout.txt:22,28`).
- `unreadable` rc=3 + notifier: RED-as-expected (`stdout.txt:29,35`).
- `bad_timestamp` rc=3 + notifier: RED-as-expected (`stdout.txt:36,42`).
- `clock_skew` rc=3 + notifier: RED-as-expected (`stdout.txt:43,49`).
- absent dir rc=3 + `_watchdog_check`: RED-as-expected (`stdout.txt:1,7`).
- empty dir no `--expect` rc=3 + `_watchdog_check`: RED-as-expected (`stdout.txt:50,56`).
- invalid `--now` rc=3 + `_watchdog_check`, not a traceback: RED-as-expected (`stdout.txt:57,63`).

### D-10
- silent rc=2, then recovered with `recovered_from=silent`, then second silent rc=2: as specified (`stdout.txt:1,4,7,11-13`).

### D-11
- (i) append then `IDENTICAL_REPLAY_NOOP` lines=1, cursor seeded to 3600000: GREEN (`stdout.txt:2-3`).
- (ii) correction-contract refusal (packet OR): RED-as-expected (`stdout.txt:5`).
- (iii) persisted WS_LIVE gap: RED-as-expected (`stdout.txt:7`).

### D-12
- one GAP line and `GAPS: 1`, rc=0: GREEN (`stdout.txt:1-3`).

### D-13
- RED half: `prefix record is not canonical JSONL` (`stdout.txt:1`). GREEN half not run (O-9).

### D-14
- GREEN backfill `lines=4` (`stdout.txt:2`).
- empty page: `snapshot did not fill gap starting at 3600000` (`stdout.txt:3`).
- non-advancing cursor: `snapshot cursor made no progress` (`stdout.txt:4`).
- residual missing: `snapshot left 1 bar(s) missing` (`stdout.txt:5`).

## Deviations from the packet steps

1. **D-6 first variant does not produce the packet-named string `P026 check-only failed; restore withheld`.** Flipping one archived snapshot byte is caught by `_verify_stable_receipt` at `C:/tmp/P026_DRILLS_TA_20260914/wt/p030_closed_partition_backup_adapter.py:347` (`snapshot prefix hash mismatch`) via `_complete_p026_run` during `_restore_manifest_snapshot` (`:538`), before `restore.run_restore` and before `:727-728`. This is by design of the adapter; a snapshot-only tamper cannot reach the P026 check-only layer without also rewriting the receipt so the receipt check passes. The second packet variant (tamper `_P030_STABLE_PREFIX.json`) was run and refused at `:315`.
2. **D-13 GREEN half not executed.** Authorized residual (O-9). RED half only.
3. **D-14 uses a stub `PublicMarketSource`, not a live venue.** Authorized residual (T-A fixture; T-C for the acceptance gate).
4. **D-11 case (ii) took the packet OR branch** `differing same-producer bar requires an approved correction contract` rather than `same observation_id has different producer bytes`. Both are listed as acceptable evidence.
5. **D-14 non-advancing cursor** was driven so `market_data_collector.py:467-468` fired, but a well-behaved dict with interval `1h` cannot make `int(t)+step <= cursor` once `t` has passed the eligible filter (`t >= cursor` and `step > 0`). The stub returned a `Mapping` whose `.get("t")` is in-range and `["t"]` does not advance. Empty-page and residual-missing-bar variants used ordinary dicts.
6. **D-7 `dir` record variant not run.** Packet allows `skipped` **or** `dir`; `skipped` was run. The `third` member uses the same complete-run message as the other incomplete-run checks (`:525`), so member-set vs complete-run is not distinguished in the printed string.
7. **D-4 leftover earlier runs remain in `fixtures/backup_root/manifest.jsonl`.** The drill appended `opsa-20260914T061919.156Z` and cited that run; prior `opsa-20260914T053757.349Z` / `opsa-20260914T054757.529Z` rows were kept (do not delete existing artefacts).
8. **D-9 `ok` produces no notifier event.** Packet requires a notifier event for every *alert/check-failed* outcome, including `_watchdog_check`. `ok` is neither; `stdout.txt:14` records `notifier-missing` for that case.

No other T-A step was skipped. D-15/D-16/D-17 were not in scope.
