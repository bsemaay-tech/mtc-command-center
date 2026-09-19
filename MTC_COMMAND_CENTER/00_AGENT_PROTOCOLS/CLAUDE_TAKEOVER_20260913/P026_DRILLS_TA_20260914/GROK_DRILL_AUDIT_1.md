# GROK_DRILL_REPORT — lane GKDRILL (independent detection audit)

Auditor: grok-4.6. Subject copy: `C:/tmp/GROK_SCRATCH_GKDRILL_20260914/pkg/` (copied from `C:/tmp/P026_DRILLS_TA_20260914/`, excluding `.git` / `.agents` / `.codex`). Authority: `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/P030_P026_CONFIG_DRILL_CHOICES_20260913_V3.md` §3 lines 341–497. Interpreter: `C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe` (3.12.12). No git. No network.

This report does not accept the lane's claims. Every row below was opened in the copy.

Encoding note: every `drills/D-*/stdout.txt` is UTF-16-LE with BOM (`ff fe`). `stderr.txt` files are empty (0 bytes, SHA-256 `e3b0c442…`). EVIDENCE.md / DRILL_RESULTS.md / REPORT.md are UTF-8 with BOM.

---

## Fence

| check | result | evidence |
| --- | --- | --- |
| Write outside the original lane directory | NOT OBSERVED in recorded artefacts | All fixture/config/tmp paths in stdout and configs are under `C:\tmp\P026_DRILLS_TA_20260914\`. D-5 isolated restore path is `C:\tmp\P026_DRILLS_TA_20260914\tmp\p030-isolated-restore-b011xo22\…` (`drills/D-5/stdout.txt` decoded L1, L5). |
| Network call | NOT OBSERVED | No `http`, `https`, `requests`, `urllib.request`, `socket`, `ntfy`, `smtp`, or `webhook` in any `run.py`. `urllib.parse.unquote` in the adapter is path decoding, not a call. Subprocess targets are the pinned interpreter + copied `wt/` scripts. |
| Real root `C:/LAB` | NOT OBSERVED as a data root | Grep of `pkg/` hits only TASK.md's prohibition. No config `backup_root` / archive / state path under `C:/LAB`. |
| KVM2 | NOT OBSERVED | Same: TASK.md prohibition only. |
| Real archive/backup path | NOT OBSERVED | Configs point at `…/fixtures/backup_root`, `…/fixtures/d2_store`, `…/fixtures/contract_partition/…`. |
| Schedule or send | NOT OBSERVED | D-9/D-10 notifier is `local_log` into `fixtures/watchdog_notifier/*.jsonl`. No Task Scheduler, no phone notifier. |
| Imports from outside `wt/` | NOT OBSERVED (code) | Every `sys.path.insert` is `…/P026_DRILLS_TA_20260914/wt`. Adapters then add `wt/MTC_COMMAND_CENTER/tools/opsa` via `__file__`. Collector imports are stdlib only. |
| Pinned interpreter outside cwd | AUTHORIZED, execute-only | Hardcoded in D-2/D-9/D-10/D-12 `run.py`. TASK.md names this interpreter. Not used as a data root. |
| `tempfile.TemporaryDirectory` | OBSERVED bound to cwd on the recorded run; scripts are not self-fencing | Adapter uses `tempfile.TemporaryDirectory(prefix="p030-isolated-restore-")` with no `dir=`. `run_codex.ps1:4` set `$env:TEMP/$env:TMP = "$cwd\tmp"`. Recorded D-5 path is inside cwd. Re-running `run.py` without that env would write to the process TEMP (outside cwd). |

### Filesystem roots the drills used

| root | role |
| --- | --- |
| `C:/tmp/P026_DRILLS_TA_20260914/` | Authorized original cwd: `wt/`, `fixtures/`, `drills/`, `tmp/` (bound configs + isolated restore). |
| `C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe` | Pinned interpreter (TASK.md). |
| Interpreter stdlib (`…/AppData/Roaming/uv/python/cpython-3.12-windows-x86_64-none/Lib`) | Runtime only; not a drill data root. |

No `run.ps1` exists; every drill is `run.py`.

---

## Per-drill coverage

Packet evidence is from V3 §3. `covered` counts EVIDENCE.md rows that actually name the packet item. `artefact check` is whether the claimed observed value is in decoded `stdout.txt` or the named artefact (not whether EVIDENCE.md's `file:line` is correct). `re-run` is from the copy at `C:/tmp/GROK_SCRATCH_GKDRILL_20260914/rerun/` with the pinned interpreter; paths retargeted; `TEMP/TMP` bound to `rerun/tmp`. Timestamps / `run_id`s / isolated temp names are allowed to differ.

| drill | packet evidence items | covered | missing/partly | artefact check | re-run |
| --- | --- | --- | --- | --- | --- |
| D-1 | (a) `require_non_empty_string_field` on `backup_root`; (b) "P030 backup store class must be protected"; (c) "P030 backup store path must equal the stable prefix"; (d) parsed config | 3/4 | (a) PARTLY: refusal happened but message is wrapped `backup config is not runnable`, not the named field error (`opsa_common.py:232` / adapter `p030_closed_partition_backup_adapter.py:388`) | (a)(b)(c)(d) values present in decoded `stdout.txt` L1–L4. EVIDENCE (d) paraphrases `result store_id=` — actual is `d: OK p030_closed_partition protected <path>` | PATH_NORM EQUAL (only cwd path on L4 differs) |
| D-2 | PLAN lines with size + SHA-256 prefix; JSON header+footer; **no** run dir; **no** manifest record | 2/4 | No independent listing of `backup_root_d2`. Inferred from footer `files: 0, bytes: 0` | Header `mode: dry-run`, two PLAN lines, footer `status: ok, files: 0, bytes: 0` present. `fixtures/backup_root_d2` exists and is empty (no `runs/`, no `manifest.jsonl`) | not re-run |
| D-3 | New stable-prefix dir; byte-identical snapshot; receipt fields `high_water_bytes`, `record_count`, `last_observation_id`, `prefix_sha256`, `captured_at_utc`, `dataset_content_hash` | 2/3 | Receipt field list PARTLY (EVIDENCE says "with counts"; does not name the six fields). Mid-capture / snapshot-mismatch refusals not exercised | Receipt artefact has all six fields. Snapshot `source.jsonl` size 1860 = `high_water_bytes`. stdout L1–L2 match | not re-run |
| D-3b (in D-3) | GREEN on a **boundary-aligned offset inside the file**; RED `high-water prefix must end with newline`; RED `source prefix is truncated below high water` | 1/3 | Aligned run used `high_water_bytes=len(raw)` (full file, same as D-3), not an inside-file record boundary (`drills/D-3/run.py:54`). Truncated-high-water variant **not run** | Mid-record RED message is exact in stdout L5. `aligned-OK` is a full-file recapture, not the packet step | not re-run |
| D-4 | `run_id`; manifest `run_start` + two `file` + `run_end status: ok, errors: []`; `readback=match` both; three adapter byte comparisons; member-set `{_P030_STABLE_PREFIX.json, snapshot}` | 2/5 | Manifest record types not tabulated. Three byte comparisons not logged. Member-set not asserted. Last EVIDENCE row is a 3-column stub. Line citations: `run_id` cited as `stdout.txt:4` but decoded L4 is the footer JSON; `run_id` is L5; `manifest_exists` cited `:5` is actually the `run_id` line | `run_id=opsa-20260914T054757.529Z`, both `readback=match`, `manifest_exists=True` present. Manifest artefact **does** contain `run_start`, two `file` with `readback=match`, `run_end status=ok errors=[]` for that `run_id` (and an earlier leftover run `opsa-20260914T053757.349Z`) | DIFFERENT allowed volatiles (`run_id`/`started_at`/`finished_at`/cwd). SHA-256 prefixes and `readback=match` EQUAL |
| D-5 | Receipt with `run_id`, `store_id`, `restored_prefix` + six identity fields; exact members; symlink/junction/type checks; restored bytes = archived; check-only then write | 2/5 | Six identity fields not named in EVIDENCE. Symlink/junction/type checks NOT OBSERVED. Explicit byte-equality not logged (only restore sha256 prefixes). Line citations `:8`/`:9` for receipt are footer/`run_id`, not the receipt path (decoded L10–L11) | Receipt artefact **has** `run_id`, `store_id`, `restored_prefix`, and the six fields. `target_entries` is exactly receipt + prefix dir + two members. stdout shows check-only then restore, both `status: ok` | PATH+volatile EQUAL except isolated temp name `b011xo22` vs re-run `nbsh7vc9` and `finished_at`. Same `run_id`. Same sha256 prefixes |
| D-6 | Tampered snapshot → `sha256 mismatch` + `run_restore` non-zero → **"P026 check-only failed; restore withheld"** before target write; second variant tamper `_P030_STABLE_PREFIX.json` at `_verify_stable_receipt` | 0/2 | Observed message is `snapshot prefix hash mismatch` (`p030_closed_partition_backup_adapter.py:347`) — the receipt/snapshot check, **not** the packet-named P026 check-only refusal (`:727-728`). Receipt-tamper variant **not run** | stdout L1 is exactly `D6: restore_verified_prefix=ERROR ValueError: snapshot prefix hash mismatch`. `fixtures/d6_restore_target` empty (nothing written) | RAW EQUAL |
| D-7 | `run_end.status != ok`; `errors` non-empty; `files` count disagree; `skipped` or `dir`; third `file` member; malformed JSONL at `_decode_strict_jsonl` | 5/6 | Malformed JSONL **not run**. `dir` record not run (`skipped` was). All five printed the same string `restore requires one complete successful P026 run` (including `third`, so member-set vs complete-run is not distinguished in output) | All five lines present and match the named complete-run message | not re-run |
| D-8 | P026-shaped `<id>.hb.json`; verifier `{schema,id,seq,emitted_at,pid}` + optional `note`; UTC-Z regex; health sidecar `p030.health_sidecar/v1` with availability + non-negative `age_seconds`; four falsifications | 5/6 | GREEN health path with `availability=available` and numeric `age_seconds` **not run** (only `unavailable` / `age_seconds: null`). Fractional-second case still had `extra` set, so it hit `heartbeat fields do not match P026` rather than `heartbeat emitted_at must use exact emitter UTC-Z grammar` (`p030_opsa_heartbeat_adapter.py:109-110`) | stdout L1–L7 match EVIDENCE quotes. Leftover `fixtures/heartbeats/p030_market_data_collector.hb.json` is **not** P026-shaped: it still has `"extra": "x"` and fractional `emitted_at`. Health artefact schema is correct, `availability=unavailable`, `age_seconds=null` | not re-run |
| D-9 | Six states `ok/silent/missing/unreadable/bad_timestamp/clock_skew`; three dir failures; rc 0 / 2 / 3; notifier event for every alert/check-failed including synthetic `_watchdog_check`; invalid `--now` is check-failed not traceback | 5/6 | EVIDENCE.md does **not** mention notifier events or `_watchdog_check`. Later cases are contaminated: `bad.hb.json` is never removed, so `bad-ts` and `clock-skew` overall `check_failed` include leftover `unreadable`/`bad_timestamp` | All six states appear in stdout JSON. rc values match packet (ok=0, silent/missing=2, unreadable/bad_ts/clock_skew/dir=3). Notifier artefacts **do** contain `_watchdog_check` for absent/empty/invalid-now, and per-id events for silent/missing/unreadable/bad_timestamp/clock_skew. Duplicate JSONL lines show the drill was executed more than once | PATH_NORM EQUAL |
| D-10 | `silent` then exactly one `recovered` with `recovered_from: "silent"` then second `silent` | 3/3 | EVIDENCE cites recovered at `stdout.txt:10`; decoded L10 is `notifier-entries`, recovered JSON is L12 | Sequence rc 2 / 0 / 2 present. Notifier JSON has `state=recovered`, `recovered_from=silent`, then second `silent` | not re-run |
| D-11 | (i) `IDENTICAL_REPLAY_NOOP`, nothing appended, cursor seeded; (ii) `CollectionRefused("same observation_id has different producer bytes")` **or** same-slot correction; (iii) WS_LIVE-only gap scan refuses | 3/4 | Cursor seeding NOT OBSERVED in stdout. (ii) took the OR branch: `differing same-producer bar requires an approved correction contract` (not the `same observation_id` string) | (i) `IDENTICAL_REPLAY_NOOP lines=1`; (ii)(iii) CollectionRefused messages present | not re-run |
| D-12 | One `GAP …` line per hole with first/last missing UTC; `GAPS: <n>` | 2/2 | — | `GAP symbol=BTC interval=1h first_missing=1970-01-01T02:00:00Z last_missing=1970-01-01T02:00:00Z` and `GAPS: 1` present. `gap-report-rc=0` extra | not re-run |
| D-13 | RED on raw collector partition — `observation_id must match p030obs-v1 identity` **or** `prefix record is not canonical JSONL`; GREEN after transform (**not authorized**) | 1/1 (RED) | GREEN half correctly not claimed | stdout L1: `D13-RED: ERROR ValueError: prefix record is not canonical JSONL`. `run.py` has no `producer_payload_hash`, no `sort_keys`, no second capture. One `capture_stable_prefix(` call. `fixtures/d13_capture` exists empty | RAW EQUAL |
| D-14 | Gap detected; backfill via `CANDLE_SNAPSHOT`; post-fill completeness; RED: empty page; non-advancing cursor (`snapshot cursor made no progress`); residual missing bar (`snapshot left N bar(s) missing`) | 2/4 | Stub `SnapshotSource` is present (GREEN for "stub source"). Empty page YES (`forced_disconn_no_snapshot`). Non-advancing cursor **not run**. Residual-missing-bar named message **not observed**: `forced_disconn_partial` fails as `snapshot did not fill gap starting at 7200000`. `forced_disconn_bad_row` returns `[None]`, which the stub filters to an empty page before the collector's non-object-row check | stdout L2–L5 match EVIDENCE quotes. GREEN `lines=4` present | not re-run |

---

## Findings

| # | severity | file:line | what is wrong | why it matters |
| --- | --- | --- | --- | --- |
| 1 | CORRECTION | `DRILL_RESULTS.md:26` | `Deviations from the packet steps` / `None` is false. D-3b aligned is a full-file recapture; D-3b truncated-high-water not run; D-6 second variant not run; D-7 malformed JSONL not run; D-14 non-advancing cursor not run; D-8 UTC-Z grammar not isolated. | The results table tells a later reviewer the packet was executed exactly. It was not. |
| 2 | CORRECTION | `drills/D-6/EVIDENCE.md:3` + `drills/D-6/stdout.txt:1` | Packet RED is `P026 check-only failed; restore withheld` after `sha256 mismatch`. Observed RED is `snapshot prefix hash mismatch`. Tampering the snapshot without changing the receipt is caught by `_verify_stable_receipt` (`p030_closed_partition_backup_adapter.py:347`) **before** P026 `run_restore`. The named P026 path and the receipt-tamper variant were not shown. | D-6 is claimed `RED-as-expected` for a message the artefact does not contain. |
| 3 | CORRECTION | `drills/D-1/stdout.txt:1` vs packet D-1 (a) | Packet names `require_non_empty_string_field` on `backup_root` (`opsa_common.py:232` → `backup config field 'backup_root' must be a non-empty string`). Adapter wraps that as `backup config is not runnable` (`p030_closed_partition_backup_adapter.py:388`). Inner exception is not printed. | The cheapest drill does not show the field-level refusal the packet listed. |
| 4 | CORRECTION | `drills/D-3/run.py:54-57` | D-3b "aligned" passes `high_water_bytes=len(raw)` (entire file). Packet: offset **inside** the file ending on a record boundary, plus a short-read truncated-high-water RED (`:262-263`). | D-3b is called out as C-5's cadence precondition. The inside-file GREEN and truncated RED are not in the evidence. |
| 5 | CORRECTION | `drills/D-8` leftover `fixtures/heartbeats/p030_market_data_collector.hb.json` | EVIDENCE claims a P026-shaped hb artefact. The file on disk is the **falsified** payload (`extra` + fractional `emitted_at`). Emit succeeded (stdout L1–L2) then the script overwrote the file and never restored it. Fractional falsification also never reached the UTC-Z regex because `extra` was still present. `available` + non-negative `age_seconds` not demonstrated. | The surviving artefact contradicts the GREEN artefact claim. |
| 6 | CORRECTION | `drills/D-14/run.py:160-170` + `market_data_collector.py:462-479` | Packet RED variants are empty page, non-advancing cursor, residual missing bar. Only empty-page (`did not fill gap starting at …`) is actually produced. `bad_row` is filtered by the stub to `[]`. Completeness-check message `snapshot left N bar(s) missing` and `snapshot cursor made no progress` never appear. | D-14 is claimed GREEN with three RED variants; two of the named refusals are absent. |
| 7 | CORRECTION | `drills/D-7/run.py` (no malformed mutator) | Packet: a malformed JSONL line refuses at `_decode_strict_jsonl` (`:99-120`), stricter than P026 `read_jsonl`. Not executed. | Incomplete-run acceptance predicate is only half-shown. |
| 8 | CORRECTION | `drills/D-4/EVIDENCE.md:3,5` ; `drills/D-5/EVIDENCE.md:3-4` | Several `file:line` citations do not match decoded UTF-16 stdout. D-4 `run_id` is L5 not L4; `manifest_exists` is L7 not L5. D-5 receipt path is L10 not L8/L9. Packet items (manifest record types, three byte comparisons, symlink/type checks, six identity fields) are not in the EVIDENCE tables even when the artefact has some of them. | A reviewer following the citations lands on the wrong lines. Coverage tables overstate what EVIDENCE.md recorded. |
| 9 | CORRECTION | `drills/D-9/EVIDENCE.md` (whole table) | Packet requires a notifier event for every alert/check-failed, including `_watchdog_check`. Artefacts have those events; EVIDENCE.md never mentions them. `unreadable`/`bad-ts`/`clock-skew` share one state dir without cleanup, so later cases are not isolated. | The matrix was driven, but not as six clean states, and the notifier evidence the packet named is not in the drill's evidence table. |
| 10 | CORRECTION | `SHA256SUMS.txt` (61 entries) vs TASK.md deliverable list | All 61 listed digests match. Fixtures (84 files), `wt/` sources (hashed separately in `COPIED_SOURCES_SHA256SUMS.txt`), and per-drill artefacts that live under `fixtures/` are not in `SHA256SUMS.txt`. Lead note says the Spark builder died and the Lead hashed 61 files. | TASK asked for SHA-256 over every deliverable. Manifests, receipts, sidecars, ledgers are unhashed at the top level. |
| 11 | NIT | several `EVIDENCE.md` last rows | Trailing rows omit the `observed` column (D-3, D-4, D-8, D-11, D-12, D-14). | Table contract broken; not a false GREEN. |
| 12 | NIT | `drills/D-*/run.py` tempfile env | Scripts do not set `TEMP/TMP` themselves. Fence held on the recorded run because `run_codex.ps1:4` bound them to `cwd\tmp`. | Re-running a `run.py` outside that launcher can write isolated restore dirs to the user TEMP. |
| 13 | NIT | `DRILL_RESULTS.md:5,16,19` | Whole-drill outcome `GREEN` for D-1 / D-14 (and similar) while most cases are RED-as-expected. Convention, but it upgrades a mixed packet. | A skim of DRILL_RESULTS looks cleaner than the evidence tables. |

No BLOCKING finding: no write outside the original cwd on the recorded run, no network, no real `C:/LAB`/KVM2/archive root, no D-13 GREEN half, no SHA-256 mismatch on listed files, no outcome that claims GREEN when stdout shows unexpected success on a RED case.

---

## D-13 / D-14 / `wt/` hashes (detect items 4–5)

**D-13 RED half only.** `drills/D-13/run.py` copies a collector-written D-11 fixture partition into `capture_stable_prefix` and prints the exception. No transform, no `producer_payload_hash()`, no `sort_keys=True` reserialize, no second capture, no GREEN string. Re-run reproduced `D13-RED: ERROR ValueError: prefix record is not canonical JSONL` exactly. DRILL_RESULTS D-13 residual line is the required `RED half only; GREEN half not run (O-9)`.

**D-14 stub + RED variants.** Stub class `SnapshotSource` is in `drills/D-14/run.py:12-34` (the three PublicMarketSource methods `connect` / `candles_snapshot` / `subscribe`/`wait`/`close`). GREEN backfill `forced_disconn_ok: OK lines=4` is present. RED empty page is present. Non-advancing cursor and residual-missing-bar **named** refusals are not present (finding 6).

**`wt/` copied sources.** `COPIED_SOURCES_SHA256SUMS.txt` lists 12 files. All 12 digests match the files in `pkg/wt/`. No extra source files. No listed file missing. Drills import only from that `wt/` tree (plus stdlib and the pinned interpreter). This audit did **not** re-hash against `C:/tmp/P030_INTEGRATION_20260913` (see NOT VERIFIED).

**`SHA256SUMS.txt`.** 61/61 digests match. LF, no CR. Spark-broken sibling is the literal-`` `n `` single-line file the Lead described.

---

## Claims vs artefacts (detect item 6)

| claim | holds? |
| --- | --- |
| `DRILL_RESULTS.md` outcomes GREEN / RED-as-expected for D-1..D-14 all ran | Ran: yes. Outcome labels: mixed drills marked GREEN (NIT). D-6 `RED-as-expected` does not match the packet-named message (CORRECTION). |
| `Deviations: None` | **False.** |
| REPORT.md "D-13 RED half completed; GREEN transform not executed" | True (stdout + run.py). |
| REPORT.md "D-14 uses a stub source (`SnapshotSource`)" | True. |
| REPORT.md "No real archive/backups roots were used" | True in configs/stdout. |
| REPORT.md line-range citations for stdout | Unsafe: files are UTF-16; several cited lines do not contain the quoted claim. |

---

## Commands run (observed output)

Working copy: `C:/tmp/GROK_SCRATCH_GKDRILL_20260914/pkg/`. Re-runs: `…/rerun/` with `TEMP=TMP=…/rerun/tmp`. Interpreter as pinned.

### Hash verification (pkg, unmodified)

All 61 `SHA256SUMS.txt` entries: **OK**. All 12 `wt/COPIED_SOURCES_SHA256SUMS.txt` entries: **OK**. `SHA256SUMS.txt` is LF, 61 lines.

### Encoding

Every `drills/D-*/stdout.txt`: `utf-16-le` BOM `fffe`. Every `stderr.txt`: empty.

### Re-runs (pinned interpreter)

```
python.exe rerun/drills/D-1/run.py   rc=0
python.exe rerun/drills/D-6/run.py   rc=0
python.exe rerun/drills/D-9/run.py   rc=0
python.exe rerun/drills/D-13/run.py  rc=0
python.exe rerun/drills/D-5/run.py   rc=0
python.exe rerun/drills/D-4/run.py   rc=0
```

D-1 decoded stdout (path is the copy):

```
a: ERROR ValueError: backup config is not runnable
b: ERROR ValueError: P030 backup store class must be protected
c: ERROR ValueError: P030 backup store path must equal the stable prefix
d: OK p030_closed_partition protected C:\tmp\GROK_SCRATCH_GKDRILL_20260914\rerun\fixtures\contract_partition\stable_prefix
```

D-6:

```
D6: restore_verified_prefix=ERROR ValueError: snapshot prefix hash mismatch
```

D-13:

```
D13-RED: ERROR ValueError: prefix record is not canonical JSONL
```

D-9: 52 lines, PATH_NORM EQUAL to recorded stdout (state-dir paths only). rc sequence 3,0,2,2,3,3,3,3,3 as recorded.

D-5: same `run_id=opsa-20260914T054757.529Z`, same two VERIFIED / two RESTORED sha256 prefixes `b34427fa5b68c05b…` / `371f9ffc2db7f32b…`, `receipt_exists=True`, same `target_entries`. Isolated directory name and `finished_at` differ (allowed).

D-4: `readback=match` both members, sizes 524/1860, same sha256 prefixes, `manifest_exists=True`. `run_id` this re-run `opsa-20260914T060105.779Z` vs recorded `opsa-20260914T054757.529Z` (allowed).

First D-6/D-5 attempt in this audit failed after a CRLF-doubling rewrite of JSONL (`json.decoder.JSONDecodeError: Expecting value: line 1 column 1`). That was an auditor rewrite bug, not a subject defect. Fixtures were restored from `pkg/` with a binary path patch and re-run successfully. `pkg/` itself was not modified.

---

## NOT VERIFIED

- Byte-identity of `pkg/wt/` against worktree `C:/tmp/P030_INTEGRATION_20260913` at HEAD `f42fd5400b2c2ecb805644d406999cb55c8178c8`. LEAD_NOTE claims 12/12; this lane did not touch that tree (TASK: no git there; this brief: no git of any kind).
- Whether any tempfile leaked to the user TEMP **before** `run_codex.ps1` bound `TEMP/TMP`. The recorded D-5 isolated path is inside cwd, so the **recorded** run was bound.
- Spark `stream.jsonl` beyond a grep for `C:/LAB`, KVM2, and `https?://`. Hits were TASK/packet reads under `C:/CT13/…` (read of the authority packet, required by TASK.md), not data-root writes.
- D-13 GREEN transform (O-9; out of authorization).
- D-15 / D-16 / D-17 (T-B/T-C; not in scope).
- Packet "Does NOT prove" residuals (paths exist/writable, second device, venue completeness, phone delivery, coordinated manifest+bytes tamper, unreadable ledger, real disconnect). The lane correctly left these unproven; this audit does not promote them.
- Whether `clock_skew` in isolation would still be overall `check_failed` (D-9 later cases are contaminated).
- Original `stdout.txt` line numbers as the Spark agent counted them inside UTF-16 files; citations are checked against decoded text.

Nothing in this report is acceptance, authorization, or a C-4/C-5/C-12 ratification.

GROK_DRILL_VERDICT: CORRECTIONS_NEEDED
