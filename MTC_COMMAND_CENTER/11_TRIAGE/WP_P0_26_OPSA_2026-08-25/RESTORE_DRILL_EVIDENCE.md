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
{"mode": "check-only", …, "status": "failed", "verified_against_manifest": 2, "restored": 0, "dirs_recreated": 0, "errors": 1, …}
rc=1 (tampered backup REFUSED; the two untampered files still verified — honest partial report)
```

> **R1 nit-4 correction (2026-08-25):** the original run of this step printed
> `"dirs_recreated": 1` even in `--check-only` mode, where nothing is created — the
> summary counted dir *records* instead of dirs *created*. Fixed in repair round 1:
> `dirs_recreated` now counts only directories actually created, so `--check-only`
> always reports 0. The value above is corrected to match the fixed tool; the fresh
> reproduction with real output is in the R1 repair section (§ C4).

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

---

# Repair round 1 (2026-08-25) — D026 RED/GREEN for the audit-R1 repairs

**Trigger:** fresh T1 claude-opus-5 audit of commit `73b72bd0` returned REQUEST_CHANGES
(2 required repairs + scope revert; 5 nits). This section records the new tests and
falsifications with commands + real output. Environment unchanged (Windows 11, Python
3.14.2, Git Bash). All RED runs execute against **pre-fix copies in `%TEMP%`** — the
worktree was never reverted; `73b72bd0` remains the base of these demonstrations
(`git show 73b72bd0:…` supplies the pre-fix file). Temp scratch dirs were removed
after this section captured their output.

## C1. Required repair 1 — directory-level check-failures must reach the notifier

**Defect:** with a missing state dir or an empty state dir and no `--expect`,
`check()` returned empty `ids`, the notify loop iterated nothing, and rc 3 was the
only trace — the evidence-store-vanished scenario produced ZERO notifier events.

**Fix:** `_notify_outcome()` in `watchdog.py` — when an `alert`/`check_failed`
outcome carries no per-id events, exactly one synthetic checker-level event
(id `_watchdog_check`, state `check_failed`, error text) is delivered. New tests:
`test_missing_state_dir_yields_rc3_and_exactly_one_notifier_event`,
`test_empty_state_dir_no_expect_notifies_check_failed`, plus non-regression guard
`test_per_id_outcomes_still_notify_per_id` (normal silent beat still notifies per id).

### RED — new tests vs pre-fix watchdog.py (temp copy)

```bash
RED=/tmp/opsa_r1_red   # maps to %TEMP%\opsa_r1_red
rm -rf "$RED" && mkdir -p "$RED"
cp MTC_COMMAND_CENTER/tools/opsa/*.py "$RED"/
git show 73b72bd0:MTC_COMMAND_CENTER/tools/opsa/watchdog.py > "$RED/watchdog.py"
cd "$RED"
python -m unittest \
  test_opsa.WatchdogTests.test_missing_state_dir_yields_rc3_and_exactly_one_notifier_event \
  test_opsa.WatchdogTests.test_empty_state_dir_no_expect_notifies_check_failed \
  test_opsa.WatchdogTests.test_invalid_now_is_check_failed_not_traceback \
  test_opsa.WatchdogTests.test_per_id_outcomes_still_notify_per_id
```

```text
ERROR: test_missing_state_dir_yields_rc3_and_exactly_one_notifier_event
  File "…\opsa_r1_red\test_opsa.py", line 254, in test_missing_state_dir_yields_rc3_and_exactly_one_notifier_event
    events = self._events()
  FileNotFoundError: [Errno 2] No such file or directory: '…\opsa_wd_u6bh6dsb\alerts.jsonl'
ERROR: test_empty_state_dir_no_expect_notifies_check_failed
  FileNotFoundError: [Errno 2] No such file or directory: '…\opsa_wd_fi4t900j\alerts.jsonl'
ERROR: test_invalid_now_is_check_failed_not_traceback
  File "…\opsa_r1_red\watchdog.py", line 172, in run_check
    now = parse_utc_iso(args.now) if args.now else utc_now()
  ValueError: Invalid isoformat string: 'not-a-timestamp'
Ran 4 tests in 0.048s
FAILED (errors=3)
```

(Tracebacks trimmed to the decisive frames. `FileNotFoundError` on the notifier log
IS the defect: rc 3 was returned but no event was ever written. The 4th test — the
per-id non-regression guard — passed on the old code, as expected.)

### GREEN — fixed tool, CLI level

```bash
cd MTC_COMMAND_CENTER/tools/opsa
python watchdog.py --state-dir "$TEMP/opsa_r1_vanished_dir" --silence-seconds 60 \
       --notifier-log "$TEMP/opsa_r1_vanished_alerts.jsonl" ; echo "rc=$?"
cat "$TEMP/opsa_r1_vanished_alerts.jsonl"
```

```text
error: state dir does not exist: C:\Users\…\Temp\opsa_r1_vanished_dir
{"overall": "check_failed", "ids": {}, "error": "state dir does not exist: …"}
rc=3
{"checked_at": "2026-08-24T19:32:09Z", "error": "state dir does not exist: …", "id": "_watchdog_check", "schema": "mtc.opsa_watchdog_event/v1", "silence_bound_seconds": 60.0, "state": "check_failed"}
```

One notifier event on the vanished-store scenario — the alert record the audit required.

## C2. Required repair 2 — delete-guard needles miss real delete forms

**Defect:** the banned list had `.unlink()` (exact call, no args), so
`dest.unlink(missing_ok=True)` passed the scan; `os.rmdir(`/`.rmdir(`/`os.truncate(`
were absent entirely. **Fix:** needles `.unlink(`, `os.rmdir(`, `.rmdir(`,
`os.truncate(` added (`shutil.move(` already present); `.write_bytes(`/`.write_text(`
deliberately NOT banned (legitimate overwrites; scope stays deletion/truncation/
removal of existing paths).

### Auditor's mutant A — `dest.unlink(missing_ok=True)` in restore.py (temp copy)

```bash
MUTA=/tmp/opsa_r1_mutant_a
rm -rf "$MUTA" && mkdir -p "$MUTA" && cp MTC_COMMAND_CENTER/tools/opsa/*.py "$MUTA"/
python - "$MUTA/restore.py" <<'PY'   # insert after: dest = Path(target) / ...
…dest.unlink(missing_ok=True)  # MUTANT(A)…
PY
cd "$MUTA" && python -m unittest test_opsa.NoDeleteGuaranteeTests -v
```

```text
First extra element 0:
'restore.py: .unlink('
- ['restore.py: .unlink(']
+ [] : delete code path found: ['restore.py: .unlink(']
Ran 1 test in 0.002s
FAILED (failures=1)          ← RED with the new needles
```

### Auditor's mutant B — `os.rmdir(dest.parent)` in restore.py (temp copy)

Same procedure, inserting `import os` + `os.rmdir(dest.parent)` after
`dest.parent.mkdir(...)`:

```text
- ['restore.py: os.rmdir(', 'restore.py: .rmdir(']
+ [] : delete code path found: ['restore.py: os.rmdir(', 'restore.py: .rmdir(']
Ran 1 test in 0.001s
FAILED (failures=1)          ← RED with the new needles
```

### Old needles were blind to BOTH mutants (pre-fix scan, same temp copies)

```bash
git show 73b72bd0:MTC_COMMAND_CENTER/tools/opsa/test_opsa.py > "$MUT/test_opsa.py"
cd "$MUT" && python -m unittest test_opsa.NoDeleteGuaranteeTests
```

```text
=== OLD test_opsa.py vs opsa_r1_mutant_a ===   Ran 1 test … OK
=== OLD test_opsa.py vs opsa_r1_mutant_b ===   Ran 1 test … OK
```

The old scan passed both delete mutants — the blind spot is proven, not asserted.

### GREEN — clean worktree

```text
test_no_delete_calls_in_opsa_tools … ok
Ran 1 test in 0.001s
OK
```

## C3. Nit 6 — unparseable `--now` must be rc 3, not a traceback

### RED — pre-fix CLI (temp copy, old watchdog.py)

```bash
cd /tmp/opsa_r1_red
python watchdog.py --state-dir … --silence-seconds 60 --now "garbage-timestamp" ; echo "OLD_rc=$?"
```

```text
  File "…\opsa_common.py", line 68, in parse_utc_iso
    ts = datetime.fromisoformat(str(value).strip().replace("Z", "+00:00"))
ValueError: Invalid isoformat string: 'garbage-timestamp'
OLD_rc=1                     ← raw traceback, rc 1
```

### GREEN — fixed CLI

```text
error: invalid --now value: Invalid isoformat string: 'garbage-timestamp'
{"overall": "check_failed", "ids": {}, "error": "invalid --now value: …"}
NEW_rc=3
{"checked_at": "2026-08-24T19:32:03Z", "error": "invalid --now value: …", "id": "_watchdog_check", "schema": "mtc.opsa_watchdog_event/v1", "silence_bound_seconds": 60.0, "state": "check_failed"}
```

Check-failed record on stdout, one notifier event, rc 3 — never a traceback.

## C4. Nit 4 — `--check-only` no longer reports `dirs_recreated` it did not create

### RED — new unit assertion vs pre-fix restore.py (temp copy)

```bash
RED2=/tmp/opsa_r1_red2
rm -rf "$RED2" && mkdir -p "$RED2" && cp MTC_COMMAND_CENTER/tools/opsa/*.py "$RED2"/
git show 73b72bd0:MTC_COMMAND_CENTER/tools/opsa/restore.py > "$RED2/restore.py"
cd "$RED2" && python -m unittest test_opsa.BackupRestoreTests.test_check_only_detects_corruption_writes_nothing
```

```text
    self.assertEqual(summary["dirs_recreated"], 0)
AssertionError: 1 != 0
Ran 1 test in 0.058s
FAILED (failures=1)
```

### GREEN — fixed tool, CLI reproduction of the A5 scenario

```bash
S=/tmp/opsa_r1_nit4   # fixture: one protected store with ledger.jsonl + empty_dir
python backup.py --config "$S/config.json"           # rc=0
printf 'tampered' > "$S"/backups/runs/*/ledger_store/ledger.jsonl
python restore.py --config "$S/config.json" --latest --check-only
```

```text
{"mode": "check-only", "run_id": "opsa-20260824T193507.812Z", "status": "failed", "verified_against_manifest": 0, "restored": 0, "overwritten": 0, "dirs_recreated": 0, "errors": 1, "finished_at": "2026-08-24T19:35:07Z"}
```

`dirs_recreated: 0` in check-only mode (restore mode still counts what it actually
creates — see A4, where the empty dir was genuinely recreated).

## C5. Full suite after all R1 changes (GREEN)

```bash
cd MTC_COMMAND_CENTER/tools/opsa && python -m unittest test_opsa
```

```text
Ran 23 tests in 0.525s
OK
```

19 original tests + 4 new watchdog tests (notifier coverage ×2, invalid-`--now`,
per-id non-regression guard); the nit-4 assertion was folded into the existing
check-only test.

## C6. Continuation after interrupted WIP — fresh verification (2026-08-25)

The continuing Codex implementer treated every R1 item as unverified. The inherited
worktree was clean at WIP commit `40b31e0a`; scratch stayed outside the repo under
`%TEMP%`. No tracked file was checked out, reset, or stashed.

### C6.1 Required #1 — fresh RED on the exact pre-fix watchdog

The archive supplies the `73b72bd0` package; only the current regression test is
copied over:

```powershell
$scratch = Join-Path $env:TEMP 'opsa_r1_fresh_20260825_codex'
New-Item -ItemType Directory -Path $scratch
git archive --format=zip --output="$scratch\old.zip" 73b72bd0 MTC_COMMAND_CENTER/tools/opsa
Expand-Archive -LiteralPath "$scratch\old.zip" -DestinationPath "$scratch\old_tree"
$old = "$scratch\old_tree\MTC_COMMAND_CENTER\tools\opsa"
Copy-Item MTC_COMMAND_CENTER\tools\opsa\test_opsa.py "$old\test_opsa.py" -Force
cd $old
python -m pytest -q test_opsa.py::WatchdogTests::test_missing_state_dir_yields_rc3_and_exactly_one_notifier_event
```

Real output (the decisive failure is retained):

```text
F                                                                        [100%]
================================== FAILURES ===================================
_ WatchdogTests.test_missing_state_dir_yields_rc3_and_exactly_one_notifier_event _
>       events = self._events()
test_opsa.py:260:
...
E       FileNotFoundError: [Errno 2] No such file or directory:
E       'C:\Users\BARSEM~1\AppData\Local\Temp\opsa_wd_ghiha3je\alerts.jsonl'
---------------------------- Captured stderr call -----------------------------
error: state dir does not exist: C:\Users\BARSEM~1\AppData\Local\Temp\opsa_wd_ghiha3je\gone
FAILED test_opsa.py::WatchdogTests::test_missing_state_dir_yields_rc3_and_exactly_one_notifier_event
1 failed in 0.14s
```

This is the required RED: the old checker returns rc 3, but zero notifier events
are delivered and the notifier file does not exist.

### C6.2 Required #2 — fresh RED on both auditor mutants

Each mutant began as a separate copy of the current `tools/opsa` directory. These
exact diffs were applied to the temp copies:

```diff
--- mutant_a/restore.py
+++ mutant_a/restore.py
@@
         dest = Path(target) / record["store_id"] / record["rel"]
+        dest.unlink(missing_ok=True)  # D026 MUTANT A

--- mutant_b/restore.py
+++ mutant_b/restore.py
@@
 import json
+import os
 import shutil
@@
             dest.parent.mkdir(parents=True, exist_ok=True)
+            os.rmdir(dest.parent)  # D026 MUTANT B
```

Exact command, run once in each mutant directory:

```powershell
python -m pytest -q test_opsa.py::NoDeleteGuaranteeTests::test_no_delete_calls_in_opsa_tools
```

Real mutant-A output:

```text
E       AssertionError: Lists differ: ['restore.py: .unlink('] != []
E       - ['restore.py: .unlink(']
E       + [] : delete code path found: ['restore.py: .unlink(']
FAILED test_opsa.py::NoDeleteGuaranteeTests::test_no_delete_calls_in_opsa_tools
1 failed in 0.13s
```

Real mutant-B output:

```text
E       AssertionError: Lists differ: ['restore.py: os.rmdir(', 'restore.py: .rmdir('] != []
E       - ['restore.py: os.rmdir(', 'restore.py: .rmdir(']
E       + [] : delete code path found: ['restore.py: os.rmdir(', 'restore.py: .rmdir(']
FAILED test_opsa.py::NoDeleteGuaranteeTests::test_no_delete_calls_in_opsa_tools
1 failed in 0.12s
```

The pre-fix `73b72bd0` scanner was copied over each unchanged mutant and the same
test was re-run. Real output proves the old fence was blind to both forms:

```text
=== PRE-FIX SCAN vs mutant_a ===
.                                                                        [100%]
1 passed in 0.04s
rc=0
=== PRE-FIX SCAN vs mutant_b ===
.                                                                        [100%]
1 passed in 0.04s
rc=0
```

### C6.3 Clean-tree GREEN for both required repairs

```powershell
python -m pytest -q `
  MTC_COMMAND_CENTER/tools/opsa/test_opsa.py::WatchdogTests::test_missing_state_dir_yields_rc3_and_exactly_one_notifier_event `
  MTC_COMMAND_CENTER/tools/opsa/test_opsa.py::NoDeleteGuaranteeTests::test_no_delete_calls_in_opsa_tools
```

```text
..                                                                       [100%]
2 passed in 0.04s
```

### C6.4 Scope item #3 — byte equality to base

```powershell
foreach ($p in 'MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md',
               'MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md') {
  $base = git rev-parse "0aa57ef6:$p"
  $current = git hash-object -- $p
  "$p base=$base current=$current equal=$($base -eq $current)"
}
```

```text
MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md base=e85635fe9e437b5bf41aa1e3e58877ba01c21028 current=e85635fe9e437b5bf41aa1e3e58877ba01c21028 equal=True
MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md base=d422d9445d1fb156d4a983821c1a43a25ec85f3e current=d422d9445d1fb156d4a983821c1a43a25ec85f3e equal=True
```

Both files are byte-identical to base `0aa57ef6`.

### C6.5 Watchdog return-code checks

A fresh heartbeat was emitted under `%TEMP%`, checked fresh, then checked against
a far-future deterministic `--now`; missing-directory and invalid-`--now` arms
followed. Real terminal summary:

```text
feed: state=ok emitted_at=2026-08-24T20:21:05Z age_seconds=0.2
FRESH_RC=0
feed: state=silent emitted_at=2026-08-24T20:21:05Z age_seconds=2283305935.0 bound_seconds=900.0
SILENT_RC=2
{"overall": "check_failed", "ids": {}, "error": "state dir does not exist: ...\\gone"}
MISSING_DIR_RC=3
MISSING_DIR_EVENT_COUNT=1
{"overall": "check_failed", "ids": {}, "error": "invalid --now value: Invalid isoformat string: 'not-a-timestamp'"}
BAD_NOW_RC=3
BAD_NOW_EVENT_COUNT=1
```

### C6.6 Mandated full pytest suite

```powershell
python -m pytest -q MTC_COMMAND_CENTER/tools/opsa/test_opsa.py
```

```text
.......................                                                  [100%]
23 passed in 0.57s
```

### C6.7 Eight-item continuation assessment

| R1 item | Current implementation check | Fresh evidence/status |
|---|---|---|
| Required 1 | Synthetic `_watchdog_check` event on empty-id check-failures | RED C6.1; GREEN C6.3; rc matrix C6.5 |
| Required 2 | `.unlink(`, `os.rmdir(`, `.rmdir(`, `shutil.move(`, `os.truncate(` banned; `.write_bytes(` remains allowed | Both mutants RED and old fence blind in C6.2; clean GREEN C6.3 |
| Scope 3 | Both memory-file blob IDs equal base `0aa57ef6` | Exact blob equality C6.4 |
| Nit 4 | `dirs_recreated` increments only inside the real-create branch | Existing RED/GREEN C4; full suite C6.6 |
| Nit 5 | Docs identify rc 3 as this package's extension | Source inspection + full suite C6.6 |
| Nit 6 | Invalid `--now` produces record/event and rc 3 | C6.5 (`BAD_NOW_RC=3`, one event) |
| Nit 7 | Config contains only neutral `C:/EXAMPLE` / `D:/EXAMPLE` placeholders | Source inspection; no canonical-checkout path hit |
| Nit 8 | Backup import absent; no `BaseException` no-op; `line_number` docs/code aligned | Source inspection + full suite C6.6 |

## R1 verdict table

| Repair/nit | RED shown | GREEN shown |
|---|---|---|
| R1 #1 notifier coverage (missing/empty state dir) | C1 (2 errors: zero events written) | C1 (rc 3 + exactly 1 `_watchdog_check` event) + C5 |
| R1 #2 delete-guard needles | C2 (both mutants FAILED) + old-needles-blind proof | C2 (clean scan OK) + C5 |
| R1 #3 scope revert | n/a (git revert; `git diff 0aa57ef6 -- <2 files>` empty) | LANE_REPORT R1 section |
| Nit 4 `dirs_recreated` | C4 (`AssertionError: 1 != 0`) | C4 (`dirs_recreated: 0`) + C5 |
| Nit 6 invalid `--now` | C3 (traceback rc 1) + C1 | C3 (rc 3 + event) + C5 |
| Nits 5/7/8 | doc/config only — no executable behaviour changed | inspection (README/opsa_common/config diff) |

## C7. Owner-authorized closure after the T1 cap (2026-08-25)

The closure repairs two Lead-reproduced defects only: empty-success restore outcomes
and unconfined store/manifest/heartbeat identifiers. Production files from exact
pre-fix HEAD `f6c2c3da` were copied to
`%TEMP%\opsa_closure_red_154691eabe2d412ab8c70b3f78ceb62b` before implementation.
After the regression tests were finalized, only the current `test_opsa.py` was copied
over that preserved pre-fix implementation.

### C7.1 RED — final tests against exact pre-fix implementation

```powershell
$red = "$env:TEMP\opsa_closure_red_154691eabe2d412ab8c70b3f78ceb62b"
Copy-Item MTC_COMMAND_CENTER\tools\opsa\test_opsa.py "$red\test_opsa.py" -Force
python -m pytest -q --tb=short `
  "$red\test_opsa.py::BackupRestoreTests::test_nonexistent_run_is_check_failure_not_empty_success" `
  "$red\test_opsa.py::BackupRestoreTests::test_partial_run_declaring_files_but_having_no_records_fails_closed" `
  "$red\test_opsa.py::BackupRestoreTests::test_restore_rejects_plain_parent_store_id_before_any_outside_write" `
  "$red\test_opsa.py::BackupRestoreTests::test_backup_rejects_percent_encoded_parent_store_id_without_writes" `
  "$red\test_opsa.py::HeartbeatPathTests::test_heartbeat_rejects_traversal_absolute_and_drive_ids_without_writes"
```

Real decisive output (path prefixes shortened only in this record):

```text
test_nonexistent_run_is_check_failure_not_empty_success
E   AssertionError: 0 != 3
{"mode": "restore", "run_id": "opsa-19000101T000000.000Z", "status": "ok",
 "verified_against_manifest": 0, "restored": 0, "errors": 0, ...}

test_partial_run_declaring_files_but_having_no_records_fails_closed
  check_only=False: E   AssertionError: 0 != 3
  check_only=True:  E   AssertionError: 0 != 3

test_restore_rejects_plain_parent_store_id_before_any_outside_write
E   AssertionError: True is not false

test_backup_rejects_percent_encoded_parent_store_id_without_writes
E   AssertionError: 0 != 3

test_heartbeat_rejects_traversal_absolute_and_drive_ids_without_writes
  ../escaped:      escaped.hb.json was written beside state/
  ..%2Fescaped:    state/..%2Fescaped.hb.json was written
  absolute path:   absolute.hb.json was written outside state/
  C:drive_escape:  state/drive_escape.hb.json was written

9 failed, 2 passed in 0.33s
```

This RED directly falsifies every closure claim: both restore modes falsely returned
success with zero verified/restored files, plain traversal wrote outside the restore
target, encoded traversal was accepted, and every unsafe heartbeat-id class wrote a
heartbeat file.

### C7.2 GREEN — closure regressions on the repaired tree

```powershell
python -m pytest -q `
  MTC_COMMAND_CENTER/tools/opsa/test_opsa.py::BackupRestoreTests::test_nonexistent_run_is_check_failure_not_empty_success `
  MTC_COMMAND_CENTER/tools/opsa/test_opsa.py::BackupRestoreTests::test_partial_run_declaring_files_but_having_no_records_fails_closed `
  MTC_COMMAND_CENTER/tools/opsa/test_opsa.py::BackupRestoreTests::test_restore_rejects_plain_parent_store_id_before_any_outside_write `
  MTC_COMMAND_CENTER/tools/opsa/test_opsa.py::BackupRestoreTests::test_backup_rejects_percent_encoded_parent_store_id_without_writes `
  MTC_COMMAND_CENTER/tools/opsa/test_opsa.py::HeartbeatPathTests::test_heartbeat_rejects_traversal_absolute_and_drive_ids_without_writes
```

```text
.....                                                              [100%]
5 passed, 6 subtests passed in 0.17s
```

The fixed outcomes are rc 3 with explicit errors. Restore preflights every selected
source and destination before making a target write; the tests prove the outside
paths and all heartbeat files remain absent.

### C7.3 GREEN — complete OPSA suite and syntax check

```powershell
python -m pytest -q MTC_COMMAND_CENTER/tools/opsa/test_opsa.py
python -m compileall -q MTC_COMMAND_CENTER/tools/opsa
```

```text
............................                                       [100%]
28 passed, 6 subtests passed in 0.84s
compileall rc=0 (no output)
```

The prior 23 tests remain green; five closure tests were added. No live evidence
store, host, credential, notifier service, trading logic, Pine, parity, schema, or
deployment surface was touched.

## C8. Closure iteration 2 — non-empty manifest fields before confinement (2026-08-25)

The closure-audit finding was reproduced against exact pre-fix HEAD `eaaf5e07`.
`resolve_confined_path()` converted `None` to the literal child name `None`, so a
file record missing `store_id` passed the first confinement preflight and later
raised `KeyError`. An empty path (`rel`) returned rc 3, but emitted only the generic
path-safety line rather than the structured invalid-record check-failure.

### C8.1 RED — `eaaf5e07` implementation + `bbd3fb99` final tests

Closure-3 replay materialized a new isolated TEMP tree file-by-file. The five
executable implementation files came from exact pre-fix commit
`eaaf5e073d3157f779c00145048bd7305fd697ad`; the final regression test came from
`bbd3fb99946d0a1b726d46a6c50be06837ab878a`. Nothing was copied from the working
tree, and no mutable `HEAD` expression was used. These are the verbatim commands
executed from repository root (`cmd.exe` redirection preserves the raw bytes emitted
by each required `git show <sha>:<path>` invocation):

```powershell
$redRoot = Join-Path $env:TEMP 'opsa_d026_red_eaaf5e07_impl_bbd3fb99_test_20260825T3'
New-Item -ItemType Directory -Path $redRoot | Out-Null
$implFiles = @('backup.py','heartbeat.py','opsa_common.py','restore.py','watchdog.py')
function Export-GitBlob([string]$sha, [string]$name, [string]$root) {
  $repoPath = "MTC_COMMAND_CENTER/tools/opsa/$name"
  $dest = Join-Path $root $name
  $spec = "$sha`:$repoPath"
  $cmdLine = "git show $spec > `"$dest`""
  & cmd.exe /d /s /c $cmdLine
  if ($LASTEXITCODE -ne 0) { throw "git show failed rc=$LASTEXITCODE spec=$spec" }
}
foreach ($name in $implFiles) { Export-GitBlob 'eaaf5e07' $name $redRoot }
Export-GitBlob 'bbd3fb99' 'test_opsa.py' $redRoot
foreach ($name in @($implFiles + 'test_opsa.py')) {
  $sourceSha = if ($name -eq 'test_opsa.py') { 'bbd3fb99' } else { 'eaaf5e07' }
  $expected = git rev-parse "$sourceSha`:MTC_COMMAND_CENTER/tools/opsa/$name"
  $actual = git hash-object (Join-Path $redRoot $name)
  $match = $expected -eq $actual
  Write-Output "RED_BLOB $name source=$sourceSha expected=$expected actual=$actual match=$match"
  if (-not $match) { throw "RED blob mismatch: $name" }
}
python -m pytest -q --tb=no `
  "$redRoot\test_opsa.py::BackupRestoreTests::test_restore_cli_missing_store_id_is_structured_check_failure_without_writes" `
  "$redRoot\test_opsa.py::BackupRestoreTests::test_restore_cli_empty_path_is_structured_check_failure_without_writes"
$redRc = $LASTEXITCODE
Write-Output "RED_RC=$redRc"
```

Real blob-identity and pytest output:

```text
RED_BLOB backup.py source=eaaf5e07 expected=e0eaea869b046cb7aadfee064d81ad0173569a40 actual=e0eaea869b046cb7aadfee064d81ad0173569a40 match=True
RED_BLOB heartbeat.py source=eaaf5e07 expected=44f8c1a77a14f4d2d288a39ed05febc5f73e190d actual=44f8c1a77a14f4d2d288a39ed05febc5f73e190d match=True
RED_BLOB opsa_common.py source=eaaf5e07 expected=f704ff09782cb604108eff04f06cc0a376f73e2e actual=f704ff09782cb604108eff04f06cc0a376f73e2e match=True
RED_BLOB restore.py source=eaaf5e07 expected=d4c1bb6b55d6ab16f6e9f3eb01ca66459d579630 actual=d4c1bb6b55d6ab16f6e9f3eb01ca66459d579630 match=True
RED_BLOB watchdog.py source=eaaf5e07 expected=02ae96b01a184159d6d02c4f507bb993b4868797 actual=02ae96b01a184159d6d02c4f507bb993b4868797 match=True
RED_BLOB test_opsa.py source=bbd3fb99 expected=c37e17efb026c25f1dbdb0105fffdb19331729f2 actual=c37e17efb026c25f1dbdb0105fffdb19331729f2 match=True
FF                                                                       [100%]
=========================== short test summary info ===========================
FAILED ..\Users\BARSEM~1\AppData\Local\Temp\opsa_d026_red_eaaf5e07_impl_bbd3fb99_test_20260825T3\test_opsa.py::BackupRestoreTests::test_restore_cli_missing_store_id_is_structured_check_failure_without_writes
FAILED ..\Users\BARSEM~1\AppData\Local\Temp\opsa_d026_red_eaaf5e07_impl_bbd3fb99_test_20260825T3\test_opsa.py::BackupRestoreTests::test_restore_cli_empty_path_is_structured_check_failure_without_writes
2 failed in 0.25s
RED_RC=1
```

A CLI-level summary from the same preserved temp copy retained the decisive real
values (the tests also assert that the restore target was never created):

```text
MISSING_STORE_ID_RC=1
MISSING_STORE_ID_STDERR_FIRST=Traceback (most recent call last):
MISSING_STORE_ID_STDERR_LAST=KeyError: 'store_id'
MISSING_STORE_ID_TRACEBACK=True
MISSING_STORE_ID_TARGET_EXISTS=False
EMPTY_PATH_REL_RC=3
EMPTY_PATH_REL_STDERR_FIRST=error: unsafe manifest path for run opsa-20260825T020000.000Z: unsafe empty/NUL path component: ''
EMPTY_PATH_REL_STDERR_LAST=error: unsafe manifest path for run opsa-20260825T020000.000Z: unsafe empty/NUL path component: ''
EMPTY_PATH_REL_TRACEBACK=False
EMPTY_PATH_REL_TARGET_EXISTS=False
```

This is the required D026 RED: the missing field reproduces the audited rc-1
traceback, and the empty field proves the prior rc 3 was not the required structured
invalid-record outcome.

### C8.2 GREEN — exact `bbd3fb99` HEAD blobs

The two regression tests drive `restore.py` through its public CLI. The repaired
preflight uses the shared non-empty-string validator for `record`, `run_id`,
`store_id`, `rel`, and file `sha256` before any path confinement.

At replay time `HEAD` was `bbd3fb99946d0a1b726d46a6c50be06837ab878a`.
The GREEN TEMP tree was nevertheless materialized from that literal commit rather
than from the working tree or symbolic `HEAD`, so later commits cannot change its
inputs. Verbatim commands and real output:

```powershell
$greenRoot = Join-Path $env:TEMP 'opsa_d026_green_bbd3fb99_20260825T3'
New-Item -ItemType Directory -Path $greenRoot | Out-Null
foreach ($name in @($implFiles + 'test_opsa.py')) {
  Export-GitBlob 'bbd3fb99' $name $greenRoot
}
foreach ($name in @($implFiles + 'test_opsa.py')) {
  $expected = git rev-parse "bbd3fb99`:MTC_COMMAND_CENTER/tools/opsa/$name"
  $actual = git hash-object (Join-Path $greenRoot $name)
  $match = $expected -eq $actual
  Write-Output "GREEN_BLOB $name source=bbd3fb99 expected=$expected actual=$actual match=$match"
  if (-not $match) { throw "GREEN blob mismatch: $name" }
}
python -m pytest -q --tb=no `
  "$greenRoot\test_opsa.py::BackupRestoreTests::test_restore_cli_missing_store_id_is_structured_check_failure_without_writes" `
  "$greenRoot\test_opsa.py::BackupRestoreTests::test_restore_cli_empty_path_is_structured_check_failure_without_writes"
$greenRc = $LASTEXITCODE
Write-Output "GREEN_RC=$greenRc"
```

```text
GREEN_BLOB backup.py source=bbd3fb99 expected=e0eaea869b046cb7aadfee064d81ad0173569a40 actual=e0eaea869b046cb7aadfee064d81ad0173569a40 match=True
GREEN_BLOB heartbeat.py source=bbd3fb99 expected=20bc8f71813dc13b4e0ce2015a6c722258626cbf actual=20bc8f71813dc13b4e0ce2015a6c722258626cbf match=True
GREEN_BLOB opsa_common.py source=bbd3fb99 expected=faef1ad173501a5a220559feda9b5c6f538e5358 actual=faef1ad173501a5a220559feda9b5c6f538e5358 match=True
GREEN_BLOB restore.py source=bbd3fb99 expected=97e9051319c95772c4b104ac9a4f4e9522259405 actual=97e9051319c95772c4b104ac9a4f4e9522259405 match=True
GREEN_BLOB watchdog.py source=bbd3fb99 expected=02ae96b01a184159d6d02c4f507bb993b4868797 actual=02ae96b01a184159d6d02c4f507bb993b4868797 match=True
GREEN_BLOB test_opsa.py source=bbd3fb99 expected=c37e17efb026c25f1dbdb0105fffdb19331729f2 actual=c37e17efb026c25f1dbdb0105fffdb19331729f2 match=True
..                                                                       [100%]
2 passed in 0.25s
GREEN_RC=0
```

Real CLI summaries from the repaired tree:

```text
MISSING_STORE_ID_RC=3
MISSING_STORE_ID_STDERR={"status": "check_failed", "error": "invalid_manifest_record", "field": "store_id", "detail": "manifest file record field 'store_id' must be a non-empty string", "run_id": "opsa-20260825T020000.000Z"}
MISSING_STORE_ID_TRACEBACK=False
MISSING_STORE_ID_TARGET_EXISTS=False
EMPTY_PATH_REL_RC=3
EMPTY_PATH_REL_STDERR={"status": "check_failed", "error": "invalid_manifest_record", "field": "rel", "detail": "manifest file record field 'rel' must be a non-empty string", "run_id": "opsa-20260825T020000.000Z"}
EMPTY_PATH_REL_TRACEBACK=False
EMPTY_PATH_REL_TARGET_EXISTS=False
```

### C8.3 Uniform sweep and full-suite GREEN

`opsa_common.py` no longer stringifies arbitrary confinement components: only real
strings and `Path` objects enter path analysis. Backup config `backup_root` and every
store `id`/`path`/`class` use the same shared validator. Heartbeat ids use it before
filename interpolation (the empty-id case joined the existing confinement subtests).
`backup.py` already reaches paths only through validated config and generated tree
entries. `watchdog.py` contains no equivalent `None`-to-path coercion: its optional
notifier/state paths are guarded before `Path(...)`, so no production change was
required there.

```powershell
python -m pytest -q MTC_COMMAND_CENTER/tools/opsa/test_opsa.py
python -m compileall -q MTC_COMMAND_CENTER/tools/opsa
```

```text
..............................                                    [100%]
30 passed, 7 subtests passed in 1.08s
COMPILEALL_RC=0
```

No live evidence store, host, credential, notifier service, trading logic, Pine,
parity, schema, or deployment surface was touched.
