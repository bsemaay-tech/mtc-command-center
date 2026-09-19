# WP-P0-26 T-A drills D-4/D-5/D-6/D-7 — PREVIEW on the candidate bytes (`d81b07f6`) — 2026-09-15 16:19Z

**Label: NONACCEPTING PREVIEW.** Run by the Claude Opus 5 Lead (session 5, `03c6c8`) — the author of the candidate. Nothing here accepts, merges or counts for P0-26; it exists so the Wednesday exact-Opus lane 4 and the owner's decision packet (draft 2 §3 "T-A re-run on the accepted bytes") can see how the repair behaves under the drill harness before acceptance. The 2026-09-14 run (`C:/tmp/P026_DRILLS_TA_20260914/`, Codex Spark + Grok audits) stays the only counted T-A execution and it ran on the PRE-repair bytes.

## Subject bytes
- `wt/` = file copies from the worktree `C:/tmp/P026_REPAIR_20260915` (branch `feature/p026-completion-marker-20260915`; HEAD verified `d81b07f62569996edb20dc96f83e7d7029406cdd` by reading `.git/worktrees/…/HEAD` at 16:12Z — no git command while `agy.exe` runs). Digests in `wt/COPIED_SOURCES_SHA256SUMS.txt`: `backup.py e7f74464…`, `restore.py 9836bfe5…`, `opsa_common.py e2b3d386…`, `p030_closed_partition_backup_adapter.py 60a0e7af…` (the four files the repair changes); `heartbeat.py`, `watchdog.py`, `config.example.json`, `README.md`, contracts, collector, heartbeat adapter, backup config byte-identical to the 09-14 lane copies.
- **Blob check against the commit: DONE 16:22Z** (`BLOB_VERIFICATION.txt`, run in a window with no `agy.exe` alive; `git rev-parse HEAD` = `d81b07f6…`, `git status --porcelain --untracked-files=no` empty): the four files the repair changes (`backup.py`, `restore.py`, `opsa_common.py`, `p030_closed_partition_backup_adapter.py`) are byte-equal to `git show d81b07f6:<path>`; the other eight copies equal their blobs after CRLF→LF (the worktree checkout is CRLF, the blobs LF; none of the eight is touched by the repair, and D-4..D-7 import only the adapter + the three opsa tools). Subject = commit `d81b07f6`.
- Interpreter: pinned 3.12.12 `C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe`; TEMP redirected to `tmp/`; fixtures = the 09-14 `contract_partition` fixture (stable prefix `drill_3`: receipt `b34427fa…`, snapshot `371f9ffc…`), fresh empty `backup_root`.

## Summary
| Drill | 09-14 result (pre-repair bytes) | PREVIEW result (candidate bytes) | New behaviour observed |
|---|---|---|---|
| D-4 backup manifests | GREEN | **GREEN** + completion pair | `runs/<run_id>/COMPLETE.json` + `RUN_MANIFEST.jsonl` written; marker `run_manifest_sha256` binds the per-run manifest; per-run file records == global records; global `run_end` carries `"completion_marker": "written"` |
| D-5 isolated restore | GREEN | **GREEN** | both `restore.run_restore` headers print `"completion_marker": "verified"` with the real run's `run_manifest_sha256` (`5694f5c3…`) — the isolated root carried the pair byte-for-byte; restored bytes == archived; target holds only the receipt + prefix (no completion pair leaks into the target) |
| D-6 tamper | 2 RED-as-expected | **7 RED-as-expected** (2 old + 5 new arms) | marker field tamper and per-run-manifest byte tamper now reach the named adapter message `P026 check-only failed; restore withheld` (restore.py rc 3 `run_not_complete` underneath); forged second `run_end` and a deleted marker refuse at the adapter layer; a forged per-run record with a re-hashed marker is caught by the global cross-check |
| D-7 interrupted / inconsistent runs | 6 RED-as-expected | **6 old + 3 new groups, all RED-as-expected** | a REAL interrupted backup leaves no `COMPLETE.json`/`RUN_MANIFEST.jsonl`, global `run_end status=partial`; `restore.py` refuses it rc 3 (`no completion marker`) in both modes; a hand-made pair on that run is still refused rc 3 (`run_end is status='partial'`); CLI: `--latest` → `unrecognized arguments`, missing `--run` → usage error rc 2; explicit run check-only rc 0 |

## Per-drill evidence (file:line = this lane)
### D-4 — `drills/D-4/stdout.txt`
| item | observed | line | outcome |
|---|---|---|---|
| run id returned | `run_id=opsa-20260915T161935.245Z` | :6 | GREEN |
| global manifest `run_start`, 2 × `file`, `run_end status=ok errors=[] files=2 bytes=2384` | `manifest_record_types=['run_start', 'file', 'file', 'run_end']`; `manifest_run_end status=ok errors=[] files=2 bytes=2384` | :10, :13 | GREEN |
| `readback=match` both files | :3, :4, :11, :12 | | GREEN |
| before/after/archived byte compare | `receipt_equal=True snapshot_equal=True` ×2 | :7, :8 | GREEN |
| member set | `['_P030_STABLE_PREFIX.json', 'source.jsonl']` | :14 | GREEN |
| **completion pair present** | `run_dir_entries=['COMPLETE.json', 'RUN_MANIFEST.jsonl', 'p030_closed_partition']`; `complete_marker_exists=True run_manifest_exists=True` | :15, :16 | GREEN (new) |
| **marker binds the per-run manifest** | `schema=mtc.opsa_run_complete/v1 run_id_match=True files=2 bytes=2384`; `run_manifest_sha256_binds=True` (`5694f5c3…`) | :18, :19 | GREEN (new) |
| **per-run manifest shape** | `['run_manifest_header', 'file', 'file']`, header `schema=mtc.opsa_run_manifest/v1 run_id_match=True`; `per_run_file_records_equal_global=True count=2` | :20, :21, :22 | GREEN (new) |
| tool's own run_end line | `"completion_marker": "written"` | :5 | GREEN (new) |
Note: the marker carries no `status`/`completed_at` fields (my probe printed `None` for both — a probe assumption, not a defect); its keys are `bytes, config, dirs, files, finished_at, readback, run_id, run_manifest, run_manifest_sha256, schema, skipped, started_at` (:17).

### D-5 — `drills/D-5/stdout.txt`
| item | observed | line | outcome |
|---|---|---|---|
| check-only then restore, both `status: ok` | headers :2 and :6, footers :5 and :9 | | GREEN |
| **isolated root carries the completion pair** | both headers: `"completion_marker": "verified", "run_manifest_sha256": "5694f5c3…"`; `real_run_manifest_sha256=5694f5c3…` equal | :2, :6, :24 | GREEN (new) |
| receipt + six identity fields | :11-:20 (values equal to the 09-14 run: `high_water_bytes=1860`, `record_count=3`, …) | | GREEN |
| exact members, no links | `type … is_symlink=False is_junction=False is_file=True` ×2; `target_entries` = receipt + prefix dir + 2 members | :21, :22, :14 | GREEN |
| restored == archived bytes | `restored_bytes_equal_archived receipt=True snapshot=True` | :23 | GREEN |
| no completion pair in the target | `target_has_no_completion_pair=True` | :25 | GREEN (new) |

### D-6 — `drills/D-6/stdout.txt` (+ `stderr.txt` for the restore.py refusal lines)
| arm | observed | line | outcome |
|---|---|---|---|
| (1) snapshot byte flip | `ValueError: snapshot prefix hash mismatch`; `target_written=[]` | :1-:2 | RED-as-expected (adapter `_verify_stable_receipt`, as on 09-14) |
| (2) receipt tamper | `stable-prefix receipt state does not match contract`; target empty | :3-:4 | RED-as-expected |
| **(3) marker `files` 2→3** | `P026 check-only failed; restore withheld`; stderr `run_not_complete … completion marker declares files=3, per-run manifest lists 2` | :5-:6; stderr :1 | RED-as-expected (new; reaches the named P026 message the 09-14 D-6 could not reach) |
| **(4) per-run manifest byte appended** | `P026 check-only failed; restore withheld`; stderr `per-run manifest hash mismatch (marker=5694f5c3… actual=fd335242…)` | :7-:8; stderr :2 | RED-as-expected (new) |
| **(5) forged second `run_end`** | `restore requires one complete successful P026 run` | :9-:10 | RED-as-expected (new; adapter `_complete_p026_run` `len(ends) != 1`) |
| **(6) `COMPLETE.json` deleted** | `P026 completion evidence is unavailable` | :11-:12 | RED-as-expected (new; adapter `_isolated_restore_inputs`) |
| **(7) forged per-run record, marker re-hashed** | `P026 check-only failed; restore withheld`; stderr `per-run manifest file records differ from the global manifest` | :13-:14; stderr :3 | RED-as-expected (new; `restore.verify_completion_evidence` global cross-check) |
Every arm: `target_written=[]`.

### D-7 — `drills/D-7/stdout.txt`
| arm | observed | line | outcome |
|---|---|---|---|
| a-e status / errors / files / skipped / third | `restore requires one complete successful P026 run` ×5, targets empty | :1-:10 | RED-as-expected (unchanged) |
| f malformed JSONL | `invalid P026 manifest line 5` | :11-:12 | RED-as-expected |
| **g real interrupted backup** | backup tool: `status: partial, files: 1, errors: 1, "completion_marker": "none"` (:15); adapter `P026 backup failed` (:16); global `run_end status=partial` with the copy error (:18); `run_dir_entries=['p030_closed_partition', '…\\_P030_STABLE_PREFIX.json']` — **no `COMPLETE.json`, no `RUN_MANIFEST.jsonl`** (:19-:20); `restore.run_restore` check-only **rc=3** and restore **rc=3**, `run_not_complete: no completion marker (COMPLETE.json absent)`, target not created (:21-:22); adapter refusal (:23-:24) | | RED-as-expected (new — the packet's "no `COMPLETE.json` and restore rc 3" expectation) |
| **h hand-made pair on the interrupted run** | pair written and self-consistent (`marker_binds=True`, :25); `restore.run_restore rc=3 … global manifest run_end is status='partial' with 1 error(s); only a run the backup tool closed successfully may be restored` (:26); adapter refusal (:27-:28) | | RED-as-expected (new — Gemini F-01 arm) |
| **i CLI surface** | `--latest --check-only` → rc 2 `required: --run` (:29); no `--run` → rc 2 (:30); `--run <id> --latest` → rc 2 `unrecognized arguments: --latest` (:31); `--run <id> --check-only` → rc 0 `status: ok, verified_against_manifest: 2` (:32) | | GREEN / RED-as-expected (new — `--latest` is gone; explicit run works) |

## NOT VERIFIED / limits
- Blob identity of `wt/` against commit `d81b07f6` — DONE (see above); the eight untouched files differ from their blobs only by CRLF.
- Nothing here is a T-B/T-C drill: no real store, no host, no notifier. The fixture is the 09-14 synthetic stable prefix (two files, 2 384 bytes).
- Reviewer independence: none — the Lead built the candidate and wrote these drills. A Grok delta audit (Sep 18) or the Wednesday exact-Opus lane is the first independent read. Codex Spark, which ran the 09-14 drills, is capped until Sep 19.
- D-13 GREEN half still not run (O-9 not given); D-1..D-3, D-8..D-14 not re-run (the repair does not touch their code paths — `heartbeat.py`, `watchdog.py`, the collector, the contracts are byte-identical to the 09-14 copies).
- The candidate's own 39 unit tests + 45 checker assertions were run by the Lead on 09-15 (`P026_REPAIR_20260915/LEAD_VERIFICATION_P026_REPAIR.md`); this preview does not re-run them.

`SHA256SUMS.txt` (LF) covers the drill scripts, outputs, config and the copied-source digest list. Recorded by Claude Opus 5 Lead (session 5, `03c6c8`).
