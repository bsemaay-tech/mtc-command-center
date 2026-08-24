# WP-P0-26 OPS-A — D026 RED/GREEN restore + watchdog drill evidence (LOCAL HALF)

**Date:** 2026-08-25 (overnight lane J) · **Worktree:** `C:\WPP026_20260825`
· **Branch:** `feature/wp-p0-26-opsa-tooling-20260825`
· **Environment:** Windows 11, Python 3.14.2, Git Bash. All commands run from the
worktree root. Tooling: `MTC_COMMAND_CENTER/tools/opsa/` (standard library only).

**Scope-fence compliance:** every path below is a FIXTURE inside this worktree's
scratch directory (`…/WP_P0_26_OPSA_2026-08-25/_drill_scratch/`, removed after this
document was written — the drill is reproducible from the commands below). No live
evidence store was read beyond this worktree, nothing was copied from any host, no
credential, no network call, no schedule installed. The drill scratches were created
by this lane and deleted by this lane.

**D026 statement:** every check offered as evidence below is shown BOTH failing to be
defeated (RED / falsification) and passing (GREEN), with commands and real output.

---

## Part A — backup → damage → RED (no backup = unrecoverable) → GREEN (restore byte-identical)

### A0. Fixture store (copies in worktree scratch)

```bash
mkdir -p .../_drill_scratch/live/ledger_store/sub .../_drill_scratch/live/ledger_store/empty_dir \
         .../_drill_scratch/live/admission_records
# ledger.jsonl  : 3 JSONL rows with CRLF line endings (CRLF variance matters for byte-identity)
# sub/blob.bin  : bytes(range(256)) * 4   (1024 binary bytes, includes 0x00/0x0A/0x0D/0xFF)
# empty_dir/    : intentionally empty directory
# admission_records/D026_admission.json : CRLF JSON, second protected store class
```

Config (`_drill_scratch/config.json`, schema `mtc.opsa_backup_config/v1`): two
protected stores → `backup_root = …/_drill_scratch/backups`.

Baseline hashes BEFORE any tool runs (the ground truth the drill defends):

```
27ea1e91bc70aa990a0be55d490ee3a6e92ee595e228a91d63e6b7ba568ec960  admission_records/D026_admission.json
35986f22e096b7af20001a32abd6d0f0338b3d786cd657a1326a900c9089cd32  ledger_store/ledger.jsonl
785b0751fc2c53dc14a4ce3d800e69ef9ce1009eb327ccf458afe09c242c26c9  ledger_store/sub/blob.bin
```

### A1. Dry-run writes NOTHING (no manifest, no run dir)

```bash
python MTC_COMMAND_CENTER/tools/opsa/backup.py --config .../_drill_scratch/config.json --dry-run
ls .../_drill_scratch/backups
```

```text
{"mode": "dry-run", "run_id": "opsa-20260824T190931.709Z", "backup_root": "MTC_COMMAND_CENTER\\11_TRIAGE\\WP_P0_26_OPSA_2026-08-25\\_drill_scratch\\backups", "stores": ["ledger_store", "admission_records"], "started_at": "2026-08-24T19:09:31Z"}
PLAN  ledger_store/ledger.jsonl size=128 sha256=35986f22e096b7af…
PLAN  ledger_store/sub/blob.bin size=1024 sha256=785b0751fc2c53dc…
PLAN  admission_records/D026_admission.json size=70 sha256=27ea1e91bc70aa99…
{"run_id": "opsa-20260824T190931.709Z", "status": "ok", "files": 0, "bytes": 0, "errors": 0, "finished_at": "2026-08-24T19:09:31Z"}
rc=0
ls: cannot access 'MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/_drill_scratch/backups': No such file or directory
```

### A2. Real backup: copies + hashes + append-only manifest + read-back verify

```bash
python MTC_COMMAND_CENTER/tools/opsa/backup.py --config .../_drill_scratch/config.json
```

```text
{"mode": "backup", "run_id": "opsa-20260824T190936.992Z", "backup_root": "…\\_drill_scratch\\backups", "stores": ["ledger_store", "admission_records"], "started_at": "2026-08-24T19:09:36Z"}
OK    ledger_store/ledger.jsonl size=128 sha256=35986f22e096b7af… readback=match
OK    ledger_store/sub/blob.bin size=1024 sha256=785b0751fc2c53dc… readback=match
OK    admission_records/D026_admission.json size=70 sha256=27ea1e91bc70aa99… readback=match
{"run_id": "opsa-20260824T190936.992Z", "status": "ok", "files": 3, "bytes": 1222, "errors": 0, "finished_at": "2026-08-24T19:09:37Z"}
rc=0
```

Manifest (append-only `backups/manifest.jsonl`, verbatim, 6 lines — `run_start`,
`dir` (empty_dir preserved), 3× `file` with per-file SHA-256, `run_end`):

```json
{"config": "C:\\WPP026_20260825\\…\\_drill_scratch\\config.json", "dry_run": false, "record": "run_start", "run_id": "opsa-20260824T190936.992Z", "schema": "mtc.opsa_manifest/v1", "started_at": "2026-08-24T19:09:36Z"}
{"class": "protected", "record": "dir", "rel": "empty_dir", "run_id": "opsa-20260824T190936.992Z", "store_id": "ledger_store"}
{"class": "protected", "copied_at": "2026-08-24T19:09:37Z", "readback": "match", "record": "file", "rel": "ledger.jsonl", "run_id": "opsa-20260824T190936.992Z", "sha256": "35986f22e096b7af20001a32abd6d0f0338b3d786cd657a1326a900c9089cd32", "size": 128, "src": "…\\live\\ledger_store\\ledger.jsonl", "store_id": "ledger_store"}
{"class": "protected", "copied_at": "2026-08-24T19:09:37Z", "readback": "match", "record": "file", "rel": "sub/blob.bin", "run_id": "opsa-20260824T190936.992Z", "sha256": "785b0751fc2c53dc14a4ce3d800e69ef9ce1009eb327ccf458afe09c242c26c9", "size": 1024, "src": "…\\live\\ledger_store\\sub\\blob.bin", "store_id": "ledger_store"}
{"class": "protected", "copied_at": "2026-08-24T19:09:37Z", "readback": "match", "record": "file", "rel": "D026_admission.json", "run_id": "opsa-20260824T190936.992Z", "sha256": "27ea1e91bc70aa990a0be55d490ee3a6e92ee595e228a91d63e6b7ba568ec960", "size": 70, "src": "…\\live\\admission_records\\D026_admission.json", "store_id": "admission_records"}
{"bytes": 1222, "errors": [], "files": 3, "finished_at": "2026-08-24T19:09:37Z", "record": "run_end", "run_id": "opsa-20260824T190936.992Z", "status": "ok"}
```

### A3. RED — deliberate damage; recovery WITHOUT the backup is impossible

Damage: `ledger.jsonl` overwritten with garbage text; `blob.bin` truncated to 200 of
1024 bytes (bytes physically lost — truncation is unrecoverable from the file itself).

```bash
printf 'CORRUPTED BY DRILL - RED PHASE\r\nGARBAGE ROW\r\n' > …/live/ledger_store/ledger.jsonl
python -c "…p.write_bytes(p.read_bytes()[:200])…"   # truncate blob.bin
find …/live -type f -exec sha256sum {} \;
find …/live -type f -exec sha256sum {} + | grep -c -E "<baseline-hash-ledger>|<baseline-hash-blob>"
```

```text
blob.bin truncated to 200 bytes
--- live tree hashes AFTER damage:
27ea1e91bc70aa990a0be55d490ee3a6e92ee595e228a91d63e6b7ba568ec960 *admission_records/D026_admission.json
b1a74ced04355845ae536884a69aad4202a4b2b87d1b44f7415b2d60fb74eb4e *ledger_store/ledger.jsonl
1901da1c9f699b48f6b2636e65cbf73abf99d0441ef67f5c540a42f7051dec6f *ledger_store/sub/blob.bin
--- do ANY files in the live tree still match the baseline hashes?
0
(0 = neither damaged file's original bytes exist anywhere in the live tree)
```

**RED verdict:** both damaged files' original bytes exist NOWHERE in the live tree
(exhaustive hash scan = 0 matches). Without the backup copy there is nothing to
recover FROM — any "recovery" would be fabrication, not restoration. The admission
record is still intact, proving the damage was bounded to the two files.

### A4. GREEN — restore from backup; every file byte-identical to baseline

```bash
python MTC_COMMAND_CENTER/tools/opsa/restore.py --config .../_drill_scratch/config.json \
       --latest --to .../_drill_scratch/live
find …/live -type f -exec sha256sum {} \;    # compare against A0 baseline
```

```text
{"mode": "restore", "run_id": "opsa-20260824T190936.992Z", "manifest": "…\\backups\\manifest.jsonl", "target": "…\\_drill_scratch\\live", "records_selected": 4, "manifest_malformed_lines": 0}
RESTORED ledger_store/ledger.jsonl sha256=35986f22e096b7af… (overwrote existing)
RESTORED ledger_store/sub/blob.bin sha256=785b0751fc2c53dc… (overwrote existing)
RESTORED admission_records/D026_admission.json sha256=27ea1e91bc70aa99… (overwrote existing)
{"mode": "restore", "run_id": "opsa-20260824T190936.992Z", "status": "ok", "verified_against_manifest": 3, "restored": 3, "overwritten": 3, "dirs_recreated": 1, "errors": 0, "finished_at": "2026-08-24T19:09:51Z"}
rc=0
--- live tree hashes AFTER restore:
27ea1e91bc70aa990a0be55d490ee3a6e92ee595e228a91d63e6b7ba568ec960 *admission_records/D026_admission.json
35986f22e096b7af20001a32abd6d0f0338b3d786cd657a1326a900c9089cd32 *ledger_store/ledger.jsonl
785b0751fc2c53dc14a4ce3d800e69ef9ce1009eb327ccf458afe09c242c26c9 *ledger_store/sub/blob.bin
--- byte-identity check vs baseline (all three must match):
3
…/live/ledger_store/empty_dir
(empty_dir preserved)
```

**GREEN verdict:** all 3/3 files hash-identical to the A0 baseline (CRLF and binary
content included), the empty directory was recreated, rc=0. The restore verified the
backup against the manifest AND the written bytes before declaring success.

### A5. Falsification — tamper ONE byte in the BACKUP; the verifier must refuse it

(D026: a verification step is not evidence until it is shown to fail. Automated twin:
`test_opsa.py::test_restore_refuses_tampered_backup`.)

```bash
python -c "…data[7] ^= 0xFF…"      # flip one byte at offset 7 of the BACKUP copy of blob.bin
python MTC_COMMAND_CENTER/tools/opsa/restore.py --config ... --latest --check-only
```

```text
FAIL  ledger_store/sub/blob.bin: sha256 mismatch: manifest=785b0751fc2c53dc… actual=82327d431835e86d…
error: ledger_store/sub/blob.bin: sha256 mismatch: manifest=785b0751fc2c53dc… actual=82327d431835e86d…
{"mode": "check-only", …, "status": "failed", "verified_against_manifest": 2, "restored": 0, "dirs_recreated": 1, "errors": 1, …}
rc=1 (tampered backup REFUSED; the two untampered files still verified — honest partial report)
```

---

## Part B — dead-man watchdog: kill a heartbeat → checker flags it

### B0/B1. Fresh heartbeat → checker GREEN (rc 0)

```bash
python MTC_COMMAND_CENTER/tools/opsa/heartbeat.py emit --state-dir …/state2 --id quantlens_runner --note "single beat for drill"
python MTC_COMMAND_CENTER/tools/opsa/watchdog.py --state-dir …/state2 --silence-seconds 60
```

```text
heartbeat written: …\_drill_scratch\state2\quantlens_runner.hb.json
{
  "emitted_at": "2026-08-24T19:10:45Z",
  "id": "quantlens_runner",
  "note": "single beat for drill",
  "pid": 43936,
  "schema": "mtc.opsa_heartbeat/v1",
  "seq": 1
}
quantlens_runner: state=ok emitted_at=2026-08-24T19:10:45Z age_seconds=0.8
{"overall": "ok", "ids": {"quantlens_runner": {"state": "ok", "emitted_at": "2026-08-24T19:10:45Z", "age_seconds": 0.8}}}
rc=0
```

### B2. RED — live loop emitter, then KILLED; silence flagged (rc 2)

```bash
python MTC_COMMAND_CENTER/tools/opsa/heartbeat.py loop --state-dir …/state3 --id feed_collector --interval 1 &
PID=$!                                   # 3 beats written
python MTC_COMMAND_CENTER/tools/opsa/watchdog.py --state-dir …/state3 --silence-seconds 5 --expect feed_collector   # while alive
kill $PID
sleep 7                                  # past the 5s bound
python MTC_COMMAND_CENTER/tools/opsa/watchdog.py --state-dir …/state3 --silence-seconds 5 --expect feed_collector   # after kill
cat …/state3/_watchdog_alerts.jsonl
```

```text
=== emitter PID=844 alive; beats so far: 3 ===
=== watchdog WHILE ALIVE (bound 5s, expect feed_collector) ===
feed_collector: state=ok emitted_at=2026-08-24T19:11:42Z age_seconds=0.5
{"overall": "ok", "ids": {"feed_collector": {"state": "ok", "emitted_at": "2026-08-24T19:11:42Z", "age_seconds": 0.5}}}
rc=0
=== kill 844 ===
process gone
last beat:
  "emitted_at": "2026-08-24T19:11:42Z",
=== wait 7s (past the 5s bound) ===
=== watchdog AFTER kill (bound 5s) ===
feed_collector: state=silent emitted_at=2026-08-24T19:11:42Z age_seconds=8.7 bound_seconds=5.0
{"overall": "alert", "ids": {"feed_collector": {"state": "silent", "emitted_at": "2026-08-24T19:11:42Z", "age_seconds": 8.7, "bound_seconds": 5.0}}}
rc=2 (silence flagged)
=== notifier log ===
{"age_seconds": 8.7, "bound_seconds": 5.0, "checked_at": "2026-08-24T19:11:50Z", "emitted_at": "2026-08-24T19:11:42Z", "id": "feed_collector", "schema": "mtc.opsa_watchdog_event/v1", "silence_bound_seconds": 5.0, "state": "silent"}
```

**RED verdict:** while alive rc=0; after `kill` + 7 s (bound 5 s) the checker returned
`silent` with rc 2 and the local-log notifier recorded exactly one alert event
carrying no secrets and no controls.

### B3. Corrupt heartbeat → CHECK-FAILED (rc 3), never OK, never conflated with silence

```bash
printf '{ this is not json' > …/state3/feed_collector.hb.json
python MTC_COMMAND_CENTER/tools/opsa/watchdog.py --state-dir …/state3 --silence-seconds 5 --expect feed_collector
```

```text
feed_collector: state=unreadable error=Expecting property name enclosed in double quotes: line 1 column 3 (char 2)
{"overall": "check_failed", "ids": {"feed_collector": {"state": "unreadable", "error": "…"}}}
rc=3 (check-failed: cannot evaluate — never OK, never conflated with silence)
```

---

## Unit suite (automated layer under the drill)

```
$ cd MTC_COMMAND_CENTER/tools/opsa && python -m unittest test_opsa
Ran 19 tests in 0.530s
OK
```

Includes the automated falsification twins of A5/B2/B3 (tampered backup refused;
stale beat → silent; corrupt beat → unreadable), the append-only-manifest
regression (second run is a pure append; first-run lines byte-identical), the
dry-run-writes-nothing regression, and the no-delete-code-path source scan
(`NoDeleteGuaranteeTests`).

## Honest detour record (drill orchestration, not a tool defect)

The first B2 attempt backgrounded `ST=… && python … & ` as one chain: `kill $!`
killed the wrapper subshell, orphaning the python emitter, which kept beating and
polluted one intermediate reading (`feed_collector: ok` after the kill). Detected
because the beat timestamp kept advancing post-kill; the orphan (PID 523) was
killed, quiescence proven (frozen `emitted_at=2026-08-24T19:11:24Z`), and B2 was
re-run cleanly in a fresh state dir (`state3`, transcript above). The mistyped
`--state-dir ""` in that attempt also produced one stray `_watchdog_alerts.jsonl`
at the worktree root (correct fail-closed alert for `missing`), which was removed.
Lesson recorded for the host deployment: schedule/check EMITTER processes so their
teardown is provable — the dead-man checker itself behaved correctly throughout.

## Verdict table

| Drill | Outcome | Evidence |
|---|---|---|
| Dry-run writes nothing | PASS | A1 (no manifest, no run dir) |
| Backup + readback verify + append-only manifest | PASS | A2 |
| RED: damaged live copy unrecoverable without backup | PASS | A3 (0/3 baseline hashes remain) |
| GREEN: restore byte-identical | PASS | A4 (3/3 hashes == baseline; empty dir preserved) |
| Falsification: tampered backup refused | PASS | A5 (rc 1, mismatch named) |
| Watchdog GREEN: fresh beat | PASS | B1 (rc 0) |
| Watchdog RED: killed beat flagged + notified | PASS | B2 (rc 2, one alert event) |
| Corrupt beat → check-failed, not OK/silent | PASS | B3 (rc 3) |
| Unit suite | PASS | 19/19 OK |
