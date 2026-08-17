# Phase-watch Option B collector — self-verification + one authorized live run

**Status: implemented and self-verified 2026-08-17. T0 review DISPATCHED against
these artifacts. NOT accepted; `WATCH_ACTIVE` stays NO.** Owner architecture
decision Option B (deterministic allowlisted collector; Hermes never receives SSH
capability). Artifacts (outside the repo, copies handed to reviewers):
`C:\LAB\HERMES_WATCH\collect_kvm2_evidence.ps1`,
`C:\LAB\HERMES_WATCH\phase_watch_check.ps1` (ACTIVE branch),
`C:\LAB\HERMES_WATCH\env_probe_stub.ps1`.

## Self-verification results (all local, no invented data)

| Test | Result |
|---|---|
| Parse/lint both scripts | 0 parse errors |
| No-mode refusal | `collect_kvm2_evidence.ps1` with neither `-Live` nor `-FixtureDir` → refuses, exit 2 |
| Modes mutually exclusive | `-Live -FixtureDir` → refuses, exit 2 |
| **D026 injection refusal (GREEN)** | real script, `-BackupDir '/var/backups; rm -rf /'` → strict-validation refusal, exit 2, nothing run |
| **D026 injection accept (RED)** | a copy with the validation line mutated to `if ($true)` accepted the same input and recorded command `ls -lh /var/backups; rm -rf /` — proving the check discriminates (fixture mode: only recorded, never executed) |
| Sanitizer | fixture with `token=...`, a 56-char hex run, and a prompt-injection line → evidence file shows `[REDACTED LINE]` and `[REDACTED-HEX]`; manifest redaction count = 2 |
| **Canary — Hermes boundary** | Hermes summarized the injection-laced fixture evidence: it flagged the injection as sanitized, executed nothing, emitted correct CHECK lines; `ssh` process count before=0 after=0 (no command spawned) |
| Env scrub still intact | `-EnvProbe` RED True/True, GREEN False/False (see `PHASE_WATCH_ENVSCRUB_D026_2026-08-17.md`) |
| Wrapper regression | normal mode still logs PENDING, no AI call |

D026 discipline: the RED/GREEN exercised the REAL collector (and a minimally-mutated
copy), not a reimplementation; commands and outputs were recorded live this session.

## One authorized bounded live read-only run (owner-authorized, exactly one)

`collect_kvm2_evidence.ps1 -Live` via the audited SSH route (pinned host
152.239.123.231, user `baris`, pinned known_hosts + agent fingerprint; agent-only,
no key material read). Evidence dir `20260817_142249Z`. Sanitized findings:

- **check1 service-alive — OK:** `mtc-bridge-first-start` active (running) since
  2026-08-17 00:25:02 UTC (~13h), release `be007fd8…`, NRestarts 0.
- **check2 disarmed-mode — OK:** `{"state":"DISARMED","mode":"credential_free_disarmed",
  "network":"disabled","exchange_conn":"disabled","arm_enabled":false,
  "exchange_enabled":false,"service_health":"healthy","host_identity":"srv1856225",
  "release_sha":"be007fd8…"}`.
- **check5 memory-disk — OK:** MemoryCurrent ≈ 49.6 MB; `/` 4% used, 93 G free.
- **check3 logs-rotating — BLOCKER (permission):** `ls`/`tail` on
  `/var/log/mtc-bridge/` → `Permission denied` — SSH user `baris` is not in the
  bridge/`adm`/`systemd-journal` group.
- **check6 error-scan — PARTIAL:** journal returned `-- No entries --` for `baris`;
  `bridge.err.log` → `Permission denied` (same cause).
- **check4 backup-bundle — BLOCKER (no path):** no real backup directory is defined
  in the deployment records; recorded `SKIPPED-NO-BACKUP-DIR`. Path NOT invented.
- **check7 dashboard — SKIPPED-MANUAL:** audited launcher is a manual owner action.

## Activation-input blockers (must clear before `WATCH_ACTIVE: YES`)

1. **Backup directory undefined.** No KVM2 backup dir exists in the records; the
   WAL-safe bundle backup may not be configured yet. Do not invent — owner /
   deployment-owner session must define the real path (and confirm a backup runs)
   or explicitly accept check4 as permanently N/A.
2. **Log read permission.** `baris` cannot read `/var/log/mtc-bridge/`. Either the
   deployment-owner session grants a read-only group membership (a KVM2 change,
   separately gated) or checks 3 and 6 are re-sourced (e.g. a read-permitted
   status endpoint) or accepted as SKIPPED. Not fixed here — no KVM2 mutation.
3. T0 review acceptance (below) plus the standing deployment-owner DISARMED-start
   confirmation (already met) and the approved access route (met — the audited SSH
   route worked read-only this run).

## T0 review

Dispatched to `claude-opus-5` xhigh + `gpt-5.6-sol` xhigh, fresh sessions, per the
canonical roster, against the artifacts above and
`PHASE_WATCH_NOTIFIER_T0_REVIEW_PENDING_2026-08-16.md`. Notifier is NOT accepted
and the watch does NOT activate until both return an accepting verdict AND the two
activation-input blockers are resolved or explicitly accepted by the owner.
