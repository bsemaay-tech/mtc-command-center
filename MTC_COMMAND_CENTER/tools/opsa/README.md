# OPS-A survivability tooling (WP-P0-26, local half)

Local backup / restore / dead-man-watchdog tooling for the MTC evidence stores.
Delivered 2026-08-25 (lane J, T1 partial). **Package acceptance is OPEN**: the
phone-push drill and any host installation are gated (G9) and are NOT part of this
delivery — see `../../11_TRIAGE/WP_P0_26_OPSA_2026-08-25/LANE_REPORT.md`.

Standard library only (Python ≥ 3.12). PowerShell is not required.

## Files

| File | Role |
|---|---|
| `opsa_common.py` | Shared invariants: atomic writes, UTC-Z stamps, SHA-256, append-only JSONL |
| `backup.py` | Copy configured evidence stores → second location, hashed, append-only manifest |
| `restore.py` | Restore a manifest run to a target dir with byte-hash verification |
| `heartbeat.py` | Dead-man heartbeat emitter (single shot or loop) |
| `watchdog.py` | Dead-man checker: silence detection + pluggable notifier (only `local_log` ships) |
| `test_opsa.py` | Unit + falsification suite (`python -m unittest test_opsa -v`) |
| `config.example.json` | Backup config schema example (`mtc.opsa_backup_config/v1`) |

## Hard guarantees

1. **No delete code path at all.** No destructive call (`os.remove(`, `os.unlink(`,
   `.unlink(` in any form — including `missing_ok=`, `os.rmdir(`, `.rmdir(`,
   `shutil.rmtree(`, `.rmtree(`, `shutil.move(`, `os.truncate(`, `send2trash(`)
   exists in any shipped tool (enforced by `test_opsa.py::NoDeleteGuaranteeTests`;
   `.write_bytes(`/`.write_text(` overwrites are deliberately not banned — scope is
   deletion/truncation/removal of existing paths).
   Protected evidence classes cannot be deleted by this tooling — by construction,
   not by intent. Deletions happen only by owner-approved exact lists, outside this
   tooling (plan §12.6.2(b)). A failed atomic write may leave a `*.tmp` file behind;
   that leftover is deliberate — a cleanup path would be a delete path.
2. **Append-only manifest.** `manifest.jsonl` is only ever opened in append mode.
   Runs never rewrite or truncate history.
3. **UTC only.** Every persisted timestamp is ISO-8601 UTC ending in `Z` (plan #45
   time discipline). The watchdog measures staleness against the heartbeat's payload
   timestamp, never filesystem mtime.
4. **Inability to evaluate is its own outcome** (DESIGN_DEFECT_PATTERNS pattern 1).
   The watchdog distinguishes `silent`/`missing` (ALERT, rc 2) from
   `unreadable`/`bad_timestamp`/`clock_skew` (CHECK-FAILED, rc 3) and never reports OK
   when it could not actually check. Exit-code convention harvested from
   `health_alerts.py` (0 ok / non-zero alert); the three-way extension — rc 2 alert
   vs rc 3 check-failed — is this package's own, not `health_alerts.py`'s.
5. **Verification is real, not decorative.** Backup re-hashes every file at its
   backup location (`readback=match`); restore re-verifies the backup against the
   manifest AND the restored bytes. The falsification (tampered backup → restore
   refuses) is proven in the drill evidence and automated in `test_opsa.py`.

## Usage

```bash
cd MTC_COMMAND_CENTER/tools/opsa

# 1. Write a config (see config.example.json): backup_root + list of stores.
# 2. Dry-run (writes NOTHING — no manifest records, no run dir):
python backup.py --config opsa_config.json --dry-run
# 3. Backup (append-only manifest + read-back verified copies):
python backup.py --config opsa_config.json
# 4. Isolated integrity proof (no writes):
python restore.py --config opsa_config.json --latest --check-only
# 5. Restore to a target dir (byte-hash verified):
python restore.py --config opsa_config.json --latest --to D:/recovered

# Dead-man watchdog (NO schedule is installed by this package):
python heartbeat.py emit --state-dir D:/hb --id my_process
python heartbeat.py loop --state-dir D:/hb --id my_process --interval 60
python watchdog.py --state-dir D:/hb --silence-seconds 900 --expect my_process
```

## Watchdog states and exit codes

| State | Meaning | Class | rc contribution |
|---|---|---|---|
| `ok` | fresh heartbeat (age ≤ bound; ≤60 s future skew tolerated) | healthy | 0 |
| `silent` | heartbeat older than the bound | **ALERT** | 2 |
| `missing` | `--expect` id with no heartbeat file | **ALERT** | 2 |
| `unreadable` | file present but unparseable | CHECK-FAILED | 3 |
| `bad_timestamp` | `emitted_at` missing/unparseable | CHECK-FAILED | 3 |
| `clock_skew` | `emitted_at` far in the future | CHECK-FAILED | 3 |

Process rc: `2` if any ALERT (loudest actionable signal), else `3` if any
CHECK-FAILED, else `0`. The full per-id truth is always the JSON summary on stdout.
Empty/absent state dir = CHECK-FAILED (watching nothing cannot be OK — fail-closed).
An unparseable `--now` value is itself a CHECK-FAILED record (rc 3), never an
unhandled traceback.

**Every `alert` and `check_failed` outcome produces at least one notifier event.**
Directory-level check-failures (missing state dir; nothing to watch; invalid `--now`)
have no per-id events, so the checker delivers one synthetic checker-level event —
id `_watchdog_check`, state `check_failed`, carrying the error text — instead of
leaving rc 3 as the only trace. Alert payloads carry no secrets and no controls
(plan §12.6.2(f)).

## Notifier extension point (post-G9)

Implement the `Notifier` protocol, add a factory to `NOTIFIERS` in `watchdog.py`, and
the `--notifier` flag picks it up — nothing else changes. Candidate technologies and
the recommendation for the owner: `../../11_TRIAGE/WP_P0_26_OPSA_2026-08-25/NOTIFIER_PROPOSAL.md`.

## Deliberately NOT here (gated or out of scope)

- Phone-push notifier of any kind (owner decision + G9-gated host step).
- Any scheduler/system-task installation (same gate).
- Retention/size-budget policy (owner-approved exact deletion lists — plan §12.6.2(b)).
- NTP/drift check (#45) — host-side, arrives with the G9-gated host step; the
  heartbeat payload already carries UTC timestamps so drift is measurable from the
  checker side (`clock_skew` state).
- tar.gz archive format — replaced by manifest + copied tree (per-file hashes,
  byte-verification, inspectable without tooling).
