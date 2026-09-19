# GROK_DRILLB_REPORT — lane GKDRILLB (independent detection audit of the corrected package)

Auditor: grok-4.6. Subject copy: `C:/tmp/GROK_SCRATCH_GKDRILLB_20260914/pkg/` (copied from `C:/tmp/P026_DRILLS_TA_20260914/`, excluding `.git` / `.agents` / `.codex`). Re-runs: `C:/tmp/GROK_SCRATCH_GKDRILLB_20260914/rerun/` with `LANE` and JSON `C:\\tmp\\P026_DRILLS_TA_20260914` retargeted; `TEMP`/`TMP` bound to `rerun/tmp`. Authority: `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/P030_P026_CONFIG_DRILL_CHOICES_20260913_V3.md` §3 lines 341–497. Interpreter: `C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe` (3.12.12). No git. No network.

This report does not accept the lane's claims. Every row below was opened in the copy. Prior findings are from `C:/tmp/CLAUDE_P0_RUN_20260913/laneGKDRILL_grok_audit/GROK_DRILL_REPORT.md`. Disposition claims are from `C:/tmp/P026_DRILLS_TA_20260914/DISPOSITION_FIX1.md` (same bytes in the copy).

Encoding note: every `drills/D-*/stdout.txt` is UTF-8 **without BOM** (not UTF-16; the prior audit's UTF-16 observation does not hold on this package). Every `stderr.txt` is empty (0 bytes, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).

---

## Prior findings (1–13)

Disposition claimed FIXED (finding 2 FIXED/REBUTTED). This audit opened the named artefacts and re-ran the newly added variants. Status is this auditor's, not the corrector's.

| # | prior finding | disposition claimed | this audit | evidence |
| --- | --- | --- | --- | --- |
| 1 | `Deviations: None` is false | FIXED | **RESOLVED** | `DRILL_RESULTS.md` has no `None` cell. Section `Deviations from the packet steps` lists eight items (D-6 named-P026 unreachability, D-13 GREEN not run, D-14 stub, D-11 OR-branch, D-14 cursor Mapping, D-7 `dir` not run, leftover D-4 runs, D-9 `ok` has no notifier). |
| 2 | D-6 claimed the packet-named P026 string; snapshot-only hit `:347`; receipt-tamper not run | FIXED / REBUTTED | **RESOLVED** (rebuttal holds) | Re-run D-6 PATH_NORM EQUAL. `pkg/drills/D-6/stdout.txt:1` `snapshot prefix hash mismatch`; `:2` `target_written=[]`; `:4` `stable-prefix receipt state does not match contract`; `:5` `target_written=[]`. Adapter `:347` is the hash check; `:315` is `state != "stable_prefix"`; `:727-728` is after `_restore_manifest_snapshot` (`:538`) which already called `_verify_stable_receipt`. Named string still absent; EVIDENCE row 1 now says `NOT OBSERVED at the named P026 layer`. |
| 3 | D-1 (a) wrapped field error not printed | FIXED | **RESOLVED** | `pkg/drills/D-1/stdout.txt:1-3`: outer `backup config is not runnable`; inner `backup config field 'backup_root' must be a non-empty string`; wrap site `p030_closed_partition_backup_adapter.py:388`. `opsa_common.py:232` is `require_non_empty_string_field(config, "backup_root", "backup config")`. Re-run D-1 PATH_NORM EQUAL. |
| 4 | D-3b aligned was full-file; truncated-high-water not run | FIXED | **RESOLVED** | `pkg/drills/D-3/stdout.txt:4` `file_size=1860 high_water_bytes=620 inside_file=True`; `:5` `aligned-OK … record_count=1`; `:7` `high-water prefix must end with newline`; `:9` `source prefix is truncated below high water`. Aligned receipt `high_water_bytes=620` `record_count=1`. `run.py:70` uses first newline+1, not `len(raw)`. Re-run D-3 PATH_NORM EQUAL. |
| 5 | D-8 leftover hb was falsified; UTC-Z not isolated; `available` sidecar not shown | FIXED | **RESOLVED** | Isolated dirs `heartbeats_extra` / `heartbeats_fractional` / `heartbeats_recon` / `heartbeats_late`. `stdout.txt:2` `heartbeat emitted_at must use exact emitter UTC-Z grammar`. `:8` `availability=available age_seconds=0`. Leftover `fixtures/heartbeats/p030_market_data_collector.hb.json` keys `emitted_at,id,pid,schema,seq` (no `extra`). Fractional leftover keeps `"emitted_at": "2026-09-14T05:00:00.123Z"` and no extra field. Re-run D-8 PATH_NORM EQUAL. |
| 6 | D-14 named RED refusals absent (empty page only) | FIXED | **RESOLVED** | `pkg/drills/D-14/stdout.txt:3` `snapshot did not fill gap starting at 3600000`; `:4` `snapshot cursor made no progress`; `:5` `snapshot left 1 bar(s) missing`; `:2` `OK lines=4`. Stub `SnapshotSource` at `run.py:19-42`; `CursorStuckRow` at `:45-51`. Re-run D-14 PATH_NORM EQUAL. GREEN ledger has 4 lines (WS_LIVE 0, CANDLE_SNAPSHOT 3600000, CANDLE_SNAPSHOT 7200000, WS_LIVE 10800000). |
| 7 | D-7 malformed JSONL not run | FIXED | **RESOLVED** | `pkg/drills/D-7/stdout.txt:6` `malformed: ERROR ValueError: invalid P026 manifest line 13`. `run.py:143` appends `b"{not-json\n"`. Adapter `_decode_strict_jsonl` `:115`. Re-run D-7 PATH_NORM EQUAL. |
| 8 | EVIDENCE `file:line` missed UTF-16 stdout; packet items not tabulated | FIXED | **RESOLVED** | Stdout is UTF-8. Spot-check: D-4 `run_id` is `stdout.txt:6`; `manifest_exists` `:10`; record types `:11`; byte comparisons `:1,:7,:8`; member-set `:15`. D-5 receipt path `:10`; six identity fields `:14-19`; type checks `:21-22`; byte equality `:23`. All match decoded text. |
| 9 | D-9 notifier not in EVIDENCE; later cases shared leftover `bad.hb.json` | FIXED | **RESOLVED** | One state dir per case (`watchdog_state/{ok,silent,missing_expect,unreadable,bad_timestamp,clock_skew,empty,absent,invalid_now}`). EVIDENCE rows name notifier events. `stdout.txt:7,56,63` `_watchdog_check`. Isolated JSON: unreadable only `bad`; bad-ts only `good2`; clock-skew only `skewed`. Re-run D-9 PATH_NORM EQUAL. |
| 10 | `SHA256SUMS.txt` omitted fixtures/`wt/` | FIXED | **RESOLVED** | 213 listed files, 213/213 digests match, LF, no CR, 0 unlisted files under `pkg/` excluding `tmp/` and `SHA256SUMS.txt` itself. `wt/` 12/12 also match `COPIED_SOURCES_SHA256SUMS.txt`. |
| 11 | Trailing EVIDENCE rows omitted `observed` | FIXED | **RESOLVED** | D-3, D-4, D-8, D-11, D-12, D-14 (and the rest) are 4-column tables including `observed`. |
| 12 | `run.py` did not bind `TEMP`/`TMP` | FIXED | **RESOLVED** | Every `drills/D-*/run.py` sets `os.environ["TEMP"]` and `["TMP"]` to `LANE/tmp` before work. Recorded D-5 isolated path `C:\tmp\P026_DRILLS_TA_20260914\tmp\p030-isolated-restore-_s9sdp8j\…` (`stdout.txt:1`). Adapter `TemporaryDirectory` still has no `dir=`; the env bind is what fences it. |
| 13 | Whole-drill `GREEN` for mixed packets | FIXED | **RESOLVED** | `DRILL_RESULTS.md` outcome column is per-case (`3 RED-as-expected + 1 GREEN`, `1 GREEN + 3 RED-as-expected`, etc.). |

No REGRESSED row. No NOT RESOLVED row.

---

## Fence

| check | result | evidence |
| --- | --- | --- |
| Write outside the original lane directory | NOT OBSERVED in recorded artefacts | Configs, stdout, manifests, isolated restore, notifier logs all under `C:\tmp\P026_DRILLS_TA_20260914\`. D-5 isolated restore `C:\tmp\P026_DRILLS_TA_20260914\tmp\p030-isolated-restore-_s9sdp8j\…`. |
| Network call | NOT OBSERVED | No `http`, `https`, `requests`, `urllib.request`, `socket`, `ntfy`, `smtp`, or `webhook` in any `run.py`. `urllib.parse.unquote` in `p030_closed_partition_backup_adapter.py:13` and `opsa_common.py:35` is path decoding. Subprocess targets are the pinned interpreter + copied `wt/` scripts (`backup.py`, `watchdog.py`, `market_data_collector.py`). |
| Real root `C:/LAB` | NOT OBSERVED as a data root | Hits only TASK.md's prohibition. No config `backup_root` / archive / state path under `C:/LAB`. |
| KVM2 | NOT OBSERVED | TASK.md prohibition only. |
| Real archive/backup path | NOT OBSERVED | Configs point at `…/fixtures/backup_root`, `…/fixtures/d2_store`, `…/fixtures/contract_partition/…`. |
| Schedule or send | NOT OBSERVED | D-9/D-10 notifier is `local_log` into `fixtures/watchdog_notifier/*.jsonl` or `watchdog_state/recovery_notifier.jsonl`. No Task Scheduler, no phone notifier. |
| Imports from outside `wt/` | NOT OBSERVED (code) | Every `sys.path.insert` is `LANE / "wt"`. Adapters then add `wt/MTC_COMMAND_CENTER/tools/opsa` via `__file__`. Collector imports are stdlib only. |
| Pinned interpreter outside cwd | AUTHORIZED, execute-only | Hardcoded in D-2/D-9/D-10/D-12 `run.py`. TASK.md names this interpreter. Not a data root. |
| `tempfile.TemporaryDirectory` | OBSERVED, now self-fenced in `run.py` | Adapter still uses `TemporaryDirectory(prefix="p030-isolated-restore-")` with no `dir=` (`p030_closed_partition_backup_adapter.py:580`). Each `run.py` binds `TEMP`/`TMP` to `LANE/tmp` before imports that matter for later calls. Recorded D-5 path is inside cwd. |

### Filesystem roots the drills used

| root | role |
| --- | --- |
| `C:/tmp/P026_DRILLS_TA_20260914/` | Authorized original cwd: `wt/`, `fixtures/`, `drills/`, `tmp/` (bound configs + isolated restore). Every `run.py` hardcodes this as `LANE`. |
| `C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe` | Pinned interpreter (TASK.md). |
| Interpreter stdlib (`…/AppData/Roaming/uv/python/cpython-3.12-windows-x86_64-none/Lib`) | Runtime only; not a drill data root. |

No `run.ps1` exists; every drill is `run.py`.

---

## Per-drill coverage

Packet evidence is from V3 §3. `covered` counts EVIDENCE.md rows that name the packet item **and** whose observed value is in decoded `stdout.txt` or the named artefact. `re-run` is from `C:/tmp/GROK_SCRATCH_GKDRILLB_20260914/rerun/` with the pinned interpreter. Timestamps / `run_id`s / isolated temp names / `pid` / `emitted_at` are allowed to differ.

| drill | packet evidence items | covered | missing/partly | artefact check | re-run |
| --- | --- | --- | --- | --- | --- |
| D-1 | (a) `require_non_empty_string_field` on `backup_root`; (b) "P030 backup store class must be protected"; (c) "P030 backup store path must equal the stable prefix"; (d) parsed config | 4/4 | — | (a) inner + wrap present `stdout.txt:1-3`; (b)(c) exact strings `:4-5`; (d) `OK p030_closed_partition protected …\stable_prefix` `:6` | PATH_NORM EQUAL (cwd path on L6) |
| D-2 | PLAN lines with size + SHA-256 prefix; JSON header+footer; **no** run dir; **no** manifest record | 4/4 | — | Header `mode: dry-run`; two PLAN lines sizes 17/10; footer `status: ok, files: 0, bytes: 0`; `listing=[]` `has_runs=False` `has_manifest=False`. `fixtures/backup_root_d2` is an empty directory | PATH_NORM EQUAL except `run_id`/`started_at`/`finished_at` (allowed) |
| D-3 | New stable-prefix dir; byte-identical snapshot; six receipt fields; mid-capture / snapshot-mismatch refusals | 2/3 | Mid-capture (`:270-273`) and snapshot-mismatch (`:274-275`) refusals **not driven** (not claimed in EVIDENCE) | Receipt has all six fields + `state=stable_prefix`. Snapshot size 1860 = `high_water_bytes`. stdout L1–L3 match | PATH_NORM EQUAL |
| D-3b (in D-3) | GREEN on a **boundary-aligned offset inside the file**; RED `high-water prefix must end with newline`; RED `source prefix is truncated below high water` | 3/3 | — | `inside_file=True` 620/1860, `record_count=1`; mid-record exact message; truncated exact message. Aligned receipt artefact `high_water_bytes=620` | PATH_NORM EQUAL (same D-3 run) |
| D-4 | `run_id`; manifest `run_start` + two `file` + `run_end status: ok, errors: []`; `readback=match` both; three adapter byte comparisons; member-set `{_P030_STABLE_PREFIX.json, snapshot}` | 5/5 | Leftover earlier runs remain in the same `manifest.jsonl` (documented deviation 7) | `run_id=opsa-20260914T061919.156Z`; types `['run_start','file','file','run_end']`; both `readback=match`; before/after/archived equal; `member_set=['_P030_STABLE_PREFIX.json','source.jsonl']`. Manifest artefact contains those records **and** leftover `opsa-20260914T053757.349Z` / `opsa-20260914T054757.529Z` | DIFFERENT allowed volatiles (`run_id` this re-run `opsa-20260914T063152.665Z`). SHA-256 prefixes and `readback=match` EQUAL |
| D-5 | Receipt with `run_id`, `store_id`, `restored_prefix` + six identity fields; exact members; symlink/junction/type checks; restored bytes = archived; check-only then write | 5/5 | — | Check-only then restore both `status: ok`. Receipt artefact has `run_id` / `store_id` / `restored_prefix` + six fields. Type lines `is_symlink=False is_junction=False is_file=True`. `restored_bytes_equal_archived receipt=True snapshot=True` with sha256 `b34427fa…` / `371f9ffc…` | PATH_NORM EQUAL except isolated temp name (`_s9sdp8j` vs `6u8adn93`) and `finished_at`. Same `run_id`. Same sha256 |
| D-6 | Tampered snapshot → `sha256 mismatch` + `run_restore` non-zero → **"P026 check-only failed; restore withheld"** before target write; second variant tamper `_P030_STABLE_PREFIX.json` at `_verify_stable_receipt` | 1/2 named strings; 2/2 variants run | Named P026 string **NOT OBSERVED** (earlier gate `:347`). EVIDENCE states this | Snapshot: `snapshot prefix hash mismatch`, `target_written=[]`. Receipt: `stable-prefix receipt state does not match contract`, `target_written=[]`. `d6_restore_target*` dirs empty | PATH_NORM EQUAL |
| D-7 | `run_end.status != ok`; `errors` non-empty; `files` count disagree; `skipped` or `dir`; third `file` member; malformed JSONL at `_decode_strict_jsonl` | 6/6 (`skipped` taken, not `dir`) | `dir` record not run (packet OR; documented) | Five complete-run messages + `invalid P026 manifest line 13`. `third` uses the same complete-run string (`:525`) | PATH_NORM EQUAL |
| D-8 | P026-shaped `<id>.hb.json`; verifier `{schema,id,seq,emitted_at,pid}` + optional `note`; UTC-Z regex; health sidecar `p030.health_sidecar/v1` with availability + non-negative `age_seconds`; four falsifications | 8/8 | — | Extra / fractional UTC-Z / recon / late-accepted exact RED strings. GREEN emit+verify+`availability=available age_seconds=0`. Leftover hb is P026-shaped | PATH_NORM EQUAL (`emitted_at`/`pid` volatile-normalized) |
| D-9 | Six states `ok/silent/missing/unreadable/bad_timestamp/clock_skew`; three dir failures; rc 0 / 2 / 3; notifier event for every alert/check-failed including `_watchdog_check`; invalid `--now` is check-failed not traceback | 9/9 cases | `ok` has no notifier (packet asks for alert/check-failed only; documented) | rc: absent=3, ok=0, silent=2, missing=2, unreadable=3, bad-ts=3, clock-skew=3, empty=3, invalid-now=3. `_watchdog_check` present. No traceback on invalid `--now` | PATH_NORM EQUAL (JSON-escaped cwd path) |
| D-10 | `silent` then exactly one `recovered` with `recovered_from: "silent"` then second `silent` | 3/3 | — | rc 2 / 0 / 2. Notifier JSON `state=recovered` `recovered_from=silent` then second `silent` (`stdout.txt:11-13`) | not re-run |
| D-11 | (i) `IDENTICAL_REPLAY_NOOP`, nothing appended, cursor seeded; (ii) `CollectionRefused("same observation_id has different producer bytes")` **or** same-slot correction; (iii) WS_LIVE-only gap scan refuses | 4/4 | (ii) took the OR branch (documented) | (i) `IDENTICAL_REPLAY_NOOP lines=1 cursor={('BTC', '1h'): 3600000}`; (ii) `differing same-producer bar requires an approved correction contract`; (iii) `persisted WS_LIVE sequence has a gap at 1970-01-01T01:00:00Z` | not re-run |
| D-12 | One `GAP …` line per hole with first/last missing UTC; `GAPS: <n>` | 2/2 | — | `GAP symbol=BTC interval=1h first_missing=1970-01-01T02:00:00Z last_missing=1970-01-01T02:00:00Z` and `GAPS: 1`. Extra `gap-report-rc=0` | not re-run |
| D-13 | RED on raw collector partition — `observation_id must match p030obs-v1 identity` **or** `prefix record is not canonical JSONL`; GREEN after transform (**not authorized**) | 1/1 (RED) | GREEN half correctly not claimed | stdout L1: `D13-RED: ERROR ValueError: prefix record is not canonical JSONL`. `run.py` has no `producer_payload_hash`, no `sort_keys`, no second capture. One `capture_stable_prefix(` call. `fixtures/d13_capture` exists empty | RAW EQUAL |
| D-14 | Gap detected; backfill via `CANDLE_SNAPSHOT`; post-fill completeness; RED: empty page; non-advancing cursor (`snapshot cursor made no progress`); residual missing bar (`snapshot left N bar(s) missing`) | 4/4 | Cursor RED uses `CursorStuckRow` Mapping (documented deviation 5), not a well-behaved dict | GREEN `lines=4` + three named RED strings. Stub class present | PATH_NORM EQUAL |

---

## Findings

| # | severity | file:line | what is wrong | why it matters |
| --- | --- | --- | --- | --- |
| 1 | NIT | `fixtures/d14/forced_disconn_bad_row/` ; `fixtures/d14/forced_disconn_partial/` ; `fixtures/watchdog_state/caseA/` ; `drills/tmp_d4cfg.py` | Pre-fix leftover fixtures / helper remain and are hashed. Current `D-14/run.py` does not run `bad_row` or `partial`; current `D-9/run.py` does not use `caseA`. | They do not contradict the corrected stdout. They are leftover population, not a false GREEN. |
| 2 | NIT | `DRILL_RESULTS.md` deviation 1 + `drills/D-6/EVIDENCE.md:3` | Packet-named string `P026 check-only failed; restore withheld` is still not produced. This is disclosed, not upgraded. | Residual of the adapter design (`:347` before `:727`). Not a claim error on this package. |

No BLOCKING finding. No CORRECTION finding: the thirteen prior corrections either match the artefacts or are honestly rebutted; `Deviations: None` is gone; RED messages that the packet names (except the disclosed D-6 P026 layer) are present; SHA-256 of every listed file matches.

---

## D-13 / D-14 / `wt/` hashes (detect items 4–5)

**D-13 RED half only.** `pkg/drills/D-13/run.py` copies a collector-written D-11 fixture partition into `capture_stable_prefix` and prints the exception. No transform, no `producer_payload_hash()`, no `sort_keys=True` reserialize, no second capture, no GREEN string. Re-run reproduced `D13-RED: ERROR ValueError: prefix record is not canonical JSONL` exactly. `DRILL_RESULTS.md:20` residual line is `RED half only; GREEN half not run (O-9)`.

**D-14 stub + RED variants.** Stub class `SnapshotSource` is in `pkg/drills/D-14/run.py:19-42` (`connect` / `candles_snapshot` / `subscribe` / `wait` / `close`). GREEN backfill `forced_disconn_ok: OK lines=4` is present. RED empty page, non-advancing cursor, and residual-missing-bar **named** refusals are present (finding 6 RESOLVED). Non-advancing case uses `CursorStuckRow` so `.get("t")` is eligible and `["t"]` does not advance (`run.py:45-51,167-169`) — documented deviation, but the collector check at `market_data_collector.py:467-468` did fire.

**`wt/` copied sources.** `COPIED_SOURCES_SHA256SUMS.txt` lists 12 files. All 12 digests match the files in `pkg/wt/`. No extra source files. No listed file missing. Drills import only from that `wt/` tree (plus stdlib and the pinned interpreter). This audit did **not** re-hash against `C:/tmp/P030_INTEGRATION_20260913` (see NOT VERIFIED).

**`SHA256SUMS.txt`.** 213/213 digests match. LF, no CR. 0 files on disk (excluding `tmp/` and the sums file) are unlisted. Spark-broken sibling `SHA256SUMS.txt.spark_broken_20260914` is hashed as a preserved artefact.

---

## Claims vs artefacts (detect item 6)

| claim | holds? |
| --- | --- |
| `DRILL_RESULTS.md` outcomes GREEN / RED-as-expected for D-1..D-14 all ran | Ran: yes. Per-case labels match stdout (D-6 named P026 string explicitly not reached). |
| `Deviations: None` | **No longer claimed.** Deviations section is non-empty and matches what this audit still sees (D-6 P026 layer, D-13 GREEN, D-14 stub, D-11 OR, D-14 Mapping, D-7 `dir`, leftover D-4 runs, D-9 `ok` notifier). |
| REPORT.md "D-13 RED half completed; GREEN transform not executed" | True (stdout + run.py). |
| REPORT.md "D-14 uses a stub source (`SnapshotSource`)" | True. |
| REPORT.md "No real archive/backups roots were used" | True in configs/stdout. |
| REPORT.md line-range citations for stdout | Hold on UTF-8 files (no UTF-16). Spot-checked D-1..D-14 against decoded text. |
| D-6 `RED-as-expected` | Holds for the **observed** earlier-gate messages. Does not hold as a claim that the packet-named P026 string appeared — and the package no longer claims that it did. |

---

## Commands run (observed output)

Working copy: `C:/tmp/GROK_SCRATCH_GKDRILLB_20260914/pkg/` (unmodified after copy; hashes taken here). Re-runs: `…/rerun/` with `TEMP=TMP=…/rerun/tmp`. Interpreter as pinned.

### Hash verification (pkg, unmodified)

```
SHA256SUMS.txt entries=213 ok=213 mismatch=0 missing_listed=0 unlisted=0 lf_only=True crlf=False
COPIED_SOURCES_SHA256SUMS.txt n=12 ok=12 mismatch=[] missing=[] extra=[]
```

### Encoding

Every `drills/D-*/stdout.txt`: `utf-8` (no BOM). Every `stderr.txt`: empty. D-13 `stdout.txt` is 64 bytes UTF-8, not UTF-16-LE.

### Fence grep (pkg)

`run.py` network/LAB/KVM2/schedule/send: NONE. `run.ps1`: NONE. `sys.path.insert` only `LANE/wt`.

### Re-runs (pinned interpreter, cwd `rerun/`)

First D-1/D-4 attempt used a path retarget that missed JSON `C:\\tmp\\P026_DRILLS_TA_20260914` (double-backslash in config files). D-1 (d) then failed `P030 backup store path must equal the stable prefix`; D-4 aborted in `_validate_config_scope` **before** writing a run. That was an auditor retarget bug, not a subject defect. JSON configs were then patched in `rerun/` only; `pkg/` was not touched. D-1/D-4/D-5/D-2 were re-run after that patch.

```
python.exe rerun/drills/D-1/run.py   rc=0
python.exe rerun/drills/D-2/run.py   rc=0
python.exe rerun/drills/D-3/run.py   rc=0
python.exe rerun/drills/D-4/run.py   rc=0
python.exe rerun/drills/D-5/run.py   rc=0
python.exe rerun/drills/D-6/run.py   rc=0
python.exe rerun/drills/D-7/run.py   rc=0
python.exe rerun/drills/D-8/run.py   rc=0
python.exe rerun/drills/D-9/run.py   rc=0
python.exe rerun/drills/D-13/run.py  rc=0
python.exe rerun/drills/D-14/run.py  rc=0
```

D-1 decoded stdout (path is the copy):

```
a: ERROR ValueError: backup config is not runnable
a: inner RequiredFieldError: backup config field 'backup_root' must be a non-empty string
a: wrapped_at p030_closed_partition_backup_adapter.py:388
b: ERROR ValueError: P030 backup store class must be protected
c: ERROR ValueError: P030 backup store path must equal the stable prefix
d: OK p030_closed_partition protected C:\tmp\GROK_SCRATCH_GKDRILLB_20260914\rerun\fixtures\contract_partition\stable_prefix
```

D-3 / D-3b (PATH_NORM EQUAL):

```
D3b-aligned: file_size=1860 high_water_bytes=620 inside_file=True
D3b: aligned-OK high_water_bytes=620 record_count=1 last_observation_id=p030obs-v1:e3de15b667caa7f38d61abe23f2255ba6d253fc593deef45d6023bc2e20160eb
D3b: mid-ERROR ValueError: high-water prefix must end with newline
D3b: truncated-ERROR ValueError: source prefix is truncated below high water
```

D-6 (PATH_NORM EQUAL):

```
D6-snapshot: restore_verified_prefix=ERROR ValueError: snapshot prefix hash mismatch
D6-snapshot: target_written=[]
D6-receipt: restore_verified_prefix=ERROR ValueError: stable-prefix receipt state does not match contract
D6-receipt: target_written=[]
```

D-7 (PATH_NORM EQUAL):

```
status: ERROR ValueError: restore requires one complete successful P026 run
errors: ERROR ValueError: restore requires one complete successful P026 run
files: ERROR ValueError: restore requires one complete successful P026 run
skipped: ERROR ValueError: restore requires one complete successful P026 run
third: ERROR ValueError: restore requires one complete successful P026 run
malformed: ERROR ValueError: invalid P026 manifest line 13
```

D-8 (PATH_NORM EQUAL; `emitted_at` this re-run `2026-09-14T06:30:16Z`):

```
verify-extra: ERROR ValueError: heartbeat fields do not match P026
verify-fractional: ERROR ValueError: heartbeat emitted_at must use exact emitter UTC-Z grammar
health-recon: ERROR ValueError: reconciliation_progress must remain null in this slice
health-late-accepted: ERROR ValueError: last accepted timestamp cannot follow observed_at_utc
health-available: schema=p030.health_sidecar/v1 availability=available age_seconds=0
hb-on-disk-fields=['emitted_at', 'id', 'pid', 'schema', 'seq']
```

D-13 (RAW EQUAL):

```
D13-RED: ERROR ValueError: prefix record is not canonical JSONL
```

D-14 (PATH_NORM EQUAL):

```
D14
forced_disconn_ok: OK lines=4
forced_disconn_no_snapshot: ERROR CollectionRefused: snapshot did not fill gap starting at 3600000
forced_disconn_no_progress: ERROR CollectionRefused: snapshot cursor made no progress
forced_disconn_residual: ERROR CollectionRefused: snapshot left 1 bar(s) missing
```

D-9: 63 lines, PATH_NORM EQUAL to recorded stdout (state-dir paths only; JSON-escaped). rc sequence 3,0,2,2,3,3,3,3,3 as recorded.

D-5: same `run_id=opsa-20260914T061919.156Z`, same two VERIFIED / two RESTORED sha256 prefixes `b34427fa5b68c05b…` / `371f9ffc2db7f32b…`, `receipt_exists=True`, same `target_entries`, type checks, `restored_bytes_equal_archived receipt=True snapshot=True`. Isolated directory name and `finished_at` differ (allowed).

D-4: `readback=match` both members, sizes 524/1860, same sha256 prefixes, `manifest_exists=True`, same record types and member-set. `run_id` this re-run `opsa-20260914T063152.665Z` vs recorded `opsa-20260914T061919.156Z` (allowed).

D-2: PLAN lines identical sizes/sha256 prefixes; footer `files: 0, bytes: 0`; empty listing. `run_id` this re-run `opsa-20260914T063152.924Z` (allowed).

---

## NOT VERIFIED

- Byte-identity of `pkg/wt/` against worktree `C:/tmp/P030_INTEGRATION_20260913` at HEAD `f42fd5400b2c2ecb805644d406999cb55c8178c8`. LEAD_NOTE claims 12/12; this lane did not touch that tree (TASK: no git there; this brief: no git of any kind).
- Whether any tempfile leaked to the user TEMP on the **original** Spark run before `run.py` grew the `TEMP`/`TMP` bind. The recorded D-5 isolated path is inside cwd, so the **recorded** corrected run was bound.
- Spark `stream.jsonl` beyond a grep for `C:/LAB`, KVM2, and `https?://`. Hits were TASK/packet reads under `C:/CT13/…` (read of the authority packet, required by TASK.md), not data-root writes.
- D-13 GREEN transform (O-9; out of authorization).
- D-15 / D-16 / D-17 (T-B/T-C; not in scope).
- Packet "Does NOT prove" residuals (paths exist/writable, second device, venue completeness, phone delivery, coordinated manifest+bytes tamper, unreadable ledger, real disconnect). The lane correctly left these unproven; this audit does not promote them.
- D-3 mid-capture and snapshot-mismatch refusals (packet Evidence names them; they were not driven; the adapter functions exist at `:270-275`).
- Whether a well-behaved dict can make `snapshot cursor made no progress` without the `CursorStuckRow` Mapping split (documented deviation 5).
- First auditor D-5 attempt (before JSON retarget) **read** the original lane `backup_root` as the config still pointed there; restore target and isolated temp were under `rerun/`. This audit did not re-hash the original `C:/tmp/P026_DRILLS_TA_20260914/` tree to prove it was unmodified by that read.

Nothing in this report is acceptance, authorization, or a C-4/C-5/C-12 ratification.

GROK_DRILLB_VERDICT: CLEAN
