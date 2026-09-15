# WP-P0-26 LOCAL SCOPE DECISION PACKET — smallest local G1-IA corrective/build slice (rev 2)

Date: 2026-09-07
Source proposal: `C:\tmp\P026_OPERATIONAL_COMPLETION_PROPOSAL_20260907.md` — **evidence/background only. It confers no authority.** Only the owner decision on this packet authorizes anything, and only within sections 2-5.
Controlling contract: `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:577-588`
Rev 2 replaces the rejected overbroad packet. Supersedes it entirely.

**Status: PREPARATION ONLY. This packet is not an authorization.** During preparation: no file outside this packet was written, no source was modified, no test ran, no credential was read, no message was sent, no host was contacted, no schedule/config was changed, no provider was invoked, no Git action was taken. Nothing below authorizes any operational action.

## 1. What this decision covers

Exactly one YES/NO: exact G1-IA for **one bounded local corrective/build slice** that fixes only the concrete contract defects named in section 3. Smallest scope: **5 existing files modified, 0 new files**. No templates, no operational action. Everything else waits for separate future owner decisions.

## 2. Source-path ceiling (5 MODIFY, 0 ADD; nothing else may be created or changed)

1. MODIFY `MTC_COMMAND_CENTER/tools/opsa/backup.py`
2. MODIFY `MTC_COMMAND_CENTER/tools/opsa/restore.py`
3. MODIFY `MTC_COMMAND_CENTER/tools/opsa/opsa_common.py`
4. MODIFY `MTC_COMMAND_CENTER/tools/opsa/watchdog.py`
5. MODIFY `MTC_COMMAND_CENTER/tools/opsa/test_opsa.py`

No new file is authorized. All test additions live in the enumerated `test_opsa.py`. Any file outside this list requires a new exact authorization.

## 3. Defects fixed — the only reasons these files change

- **backup.py / restore.py / opsa_common.py — completed-run identity is missing.** The contract requires automated second-location copying of every evidence store (`plan:577-588`), but current code emits no per-run completion marker, and `restore.py --latest` selects the greatest *started* run, not a verified complete run (`proposal:32,46`). A later cross-location copy could therefore ship a partial run as if complete. This defect must be fixed locally before any verified transfer slice can be proposed. This is the only backup/restore change; **all other existing backup/restore interfaces are preserved** (same CLI entry points, store layout, hash algorithm, append-only global manifest, heartbeat emission unchanged).
- **watchdog.py — dedupe suppresses the second real incident.** The state never records `ok`; `silent → ok → silent` fails to re-alert, and no recovery transition exists (`watchdog.py:175-211,252-253`; `proposal:29`). Notifier-agnostic correctness defect; fix does not add any notifier.
- **watchdog.py — unratified value presented as contract.** The CLI embeds a 900-second default and claims it comes from #39; no such value is ratified (`watchdog.py:217-218`; `proposal:19,30`).

## 4. Behavior ceiling

### Completed-run manifests and explicit-run restore (`backup.py`, `restore.py`, `opsa_common.py`)

- Each successful backup run emits a per-run immutable `RUN_MANIFEST.jsonl` (file list, sizes, hashes) plus `COMPLETE.json`, written atomically and only after every readback hash passes. A partial/interrupted run has no completion marker. Once written, manifest and marker are never rewritten.
- Restore consumes an explicit completed run ID and fails closed: no run without a matching `COMPLETE.json` + `RUN_MANIFEST.jsonl`, no execution on hash mismatch. `--latest` (greatest-started-run selection) is removed; restore without an explicit run ID errors.
- Additive only: every existing interface not named above stays as-is.

### Watchdog (`watchdog.py`)

- Silence bound becomes required explicit CLI/config input; no default; absent bound errors. Remove the 900-second default and the false #39 provenance claim.
- Dedupe becomes a full transition ledger keyed by watch ID recording last transition: `alert → recovery → later alert` emits all three transitions, each exactly once, to registered channels — `local_log` remains the only registered channel in this slice. Corrupt/unknown dedupe state fails safe (re-alert).
- No notifier is added, no Telegram path, no network send, no new channel registration, no threshold value introduced.

### Hard constraints

- No Bridge/Pine/trading behavior change. Existing heartbeat emission unchanged. Thresholds (detect-to-phone, recovery, drift, restore interval, storage budget) remain `[OPEN]` and unratified.
- No fixture result may be claimed as WP-P0-26 acceptance, operational readiness, or a satisfied contract condition.

## 5. Test ceiling — fake/fixture only, inside `test_opsa.py`

All tests use injected fake transports, temporary fixtures, and a local HTTP stub where needed. Required falsifications:

1. Interrupted/partial backup run has no `COMPLETE.json` and is refused by restore.
2. A completed run restores by explicit run ID, including a copied run directory.
3. Tampered or mismatched marker/manifest is refused; hash mismatch is refused.
4. Restore without an explicit run ID fails closed; greatest-started-run selection no longer exists.
5. Watchdog without an explicit silence bound errors; the 900-second default is gone.
6. `alert → recovery → second alert` produces all three transitions, each exactly once, to a fake local channel.
7. Corrupt dedupe state fails safe (re-alert, no crash-and-pass).

Forbidden in implementation and tests: any real environment/credential read; any real network call (local stub only); any SSH/SFTP; any schedule/task/service creation; any host contact, provider call, or config mutation outside the 5 files; any Git action; any drill or external send. Existing suite stays green; new falsifications extend it. No new test file.

## 6. Exclusions — not requested, not sequenced, not batched

Every item below is outside this decision. None is approved, requested, or queued for approval here; each needs its own separate owner decision when actually proposed:

- Telegram/notifier implementation; `@MTCHyperbot` variables; any credential handling, including presence checks.
- `Invoke-OpsaExternalCheck.ps1`, `Invoke-OpsaBackupSync.ps1` (external checker and backup-sync wrappers).
- `ntp_check.py`.
- `watchdog_config.example.json`; `config.example.json` and `README.md` updates.
- All 11 `deploy/linux/*` and `deploy/windows/*` templates — **optional template preparation only**, and even that drafting is not authorized by this packet.
- Scheduler/task/systemd work, installs, host contact (KVM2 or otherwise), provider calls, external checker deployment, phone/restore drills.
- Git actions. Policy ratification (all thresholds stay `[OPEN]`).

Phase Watch authorization does not transfer: `WATCH_ACTIVE` is still `NO`; its one supervised fake-WARN send was consumed 2026-08-16.

**Operational boundary:** every operational phase (preflight, install, scheduling, sends, drills, publication) is owner-only, later, and separately authorized per session. This packet does not convert that work into a batch of approvals.

## 7. Rollback / stop conditions

Local rollback: revert the 5 enumerated files to their pre-change state (hashes recorded before first edit); no Git commit; leave all evidence artifacts, the `MTC-HermesPhaseWatch` task, credentials, and existing config untouched.

Stop immediately and report if: work drifts outside the 5-file or behavior ceiling; a real credential/environment value is read or nearly exposed; a real Telegram/SSH/SFTP/network call becomes possible or attempted; the fixture boundary cannot be maintained; or a required change falls outside section 4.

## 8. Owner answer

**Recommended: YES.** Effect if YES: later local implementation work may write exactly the 5 enumerated files with exactly the behaviors in section 4 and the tests in section 5 — fake transports and local fixtures only, no operational action, no templates. Effect if NO: no local work proceeds; the source proposal stays preparation-only.

Owner decision: ______ (YES / NO)   Date: ______

NEXT ACTION: Owner answers this single YES/NO only. If YES: later local implementation is bound to sections 2-5; optional template preparation and every operational item remain separate future owner decisions, each proposed and decided on its own — nothing is requested for them here.

WAITING FOR OWNER: the single YES/NO above. Nothing else is requested by this packet.

P026_LOCAL_SCOPE_DECISION_COMPLETE
