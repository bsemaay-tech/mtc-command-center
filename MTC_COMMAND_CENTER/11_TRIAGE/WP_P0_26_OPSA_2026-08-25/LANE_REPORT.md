# Lane J Report — WP-P0-26 OPS-A local backup/restore + dead-man watchdog tooling

## Status

**TOOLING DELIVERED / ACCEPTANCE OPEN.** The T1 local tooling half of WP-P0-26 is
implemented, self-QA'd, and D026 RED/GREEN-proven on fixtures. Package acceptance is
**NOT claimable**: it requires a real phone-push drill plus the KVM2 host-install
step, both gated behind G9 and owner authorization — deliberately not tonight's
work. Audit tier **T1** (local, non-economic tooling; no host/credential/live
surface). Lead owns acceptance/audit/git sequencing.

**Scope-fence compliance:** no contact with KVM2 or any host; no credential; no
phone-push signup or message; no schedule/system-task installation; no live evidence
store touched (all drill inputs were fixtures created inside this worktree and
removed after the evidence document captured them); no Docker/WSL; no access to the
dirty checkout `C:\LAB\Tradingview_LAB_CLEAN` or other worktrees. One stray
drill-artifact file briefly created at the worktree root by a mistyped drill command
(`_watchdog_alerts.jsonl`) was removed; see the honest detour record in
`RESTORE_DRILL_EVIDENCE.md`.

## Delivered

All under `MTC_COMMAND_CENTER/tools/opsa/` (new directory; nothing else in `tools/`
touched) and `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/`:

- `tools/opsa/opsa_common.py` — shared invariants: atomic writes (tmp + replace),
  UTC-Z-only timestamps, streaming SHA-256, append-only JSONL, config validation,
  exit-code contract (0 ok / 2 alert / 3 check-failed).
- `tools/opsa/backup.py` — config-driven copy of evidence stores to a second
  location; per-file SHA-256; read-back verification (`readback=match`); append-only
  `manifest.jsonl`; dry-run mode that writes nothing; empty-dir preservation;
  symlink/junction entries recorded as skipped, never followed; honest partial-failure
  reporting (rc 1). **No delete code path exists at all** (see guarantee below).
- `tools/opsa/restore.py` — manifest-driven restore to a target dir with three-layer
  hash verification (backup vs manifest, written bytes vs manifest); `--check-only`
  isolated integrity proof; `--latest`/`--run` selection; `--store` filter; empty-dir
  recreation; tampered backup REFUSED with per-file reporting.
- `tools/opsa/heartbeat.py` — dead-man heartbeat emitter (`emit` single, `loop`
  recurring); payload timestamp UTC-Z (staleness measured from payload, never mtime);
  atomic writes; deliberately NO graceful-stop marker (silence is silence).
- `tools/opsa/watchdog.py` — one-shot checker: `ok` / `silent` / `missing` (ALERT,
  rc 2) vs `unreadable` / `bad_timestamp` / `clock_skew` (CHECK-FAILED, rc 3);
  configurable silence bound; `--expect` ids; fail-closed on empty/absent state dir;
  pluggable `Notifier` interface + `NOTIFIERS` registry with ONLY a `local_log`
  notifier shipped; optional notify-once-per-(id,state) dedupe state file.
- `tools/opsa/test_opsa.py` — 19-test suite incl. automated falsifications
  (tampered backup refused; stale beat → silent; corrupt beat → unreadable; dry-run
  writes nothing; append-only manifest regression; no-delete source scan).
- `tools/opsa/README.md` + `tools/opsa/config.example.json` — usage, guarantees,
  state/exit-code table, notifier extension point, gated-absent list.
- `11_TRIAGE/WP_P0_26_OPSA_2026-08-25/RESTORE_DRILL_EVIDENCE.md` — D026 drill:
  exact commands + real output for backup, RED (damaged live copy proven
  unrecoverable without backup: 0/3 baseline hashes remain), GREEN (restore
  byte-identical: 3/3 hashes == baseline, CRLF + binary + empty dir), tampered-backup
  refusal, watchdog kill/silence RED/GREEN, corrupt-heartbeat check-failed.
- `11_TRIAGE/WP_P0_26_OPSA_2026-08-25/NOTIFIER_PROPOSAL.md` — ntfy self-hosted vs
  ntfy.sh public vs Telegram bot vs Pushover against the package criteria
  (no signup, no credential, checker-on-second-location fit, stdlib client, no
  secrets in payloads); recommendation: self-hosted ntfy on the owner PC, honest
  iOS APNS-relay and home-uplink caveats, Telegram as contingency, Pushover
  rejected; detect-to-delivery bound stays `[OPEN]` pending the gated real drill.
- This report.

**No-delete guarantee:** no `os.remove(`/`os.unlink(`/`shutil.rmtree(` call exists in
any shipped tool; enforced mechanically by
`test_opsa.py::NoDeleteGuaranteeTests::test_no_delete_calls_in_opsa_tools`.
Protected classes cannot be deleted by this tooling by construction. Deletions
remain owner-approved-exact-list-only, outside this tooling (plan §12.6.2(b)). A
failed atomic write may leave a `*.tmp` file — deliberate, because a cleanup path
would be a delete path.

## Reuse record (OSS-first / reuse-first)

| Harvested asset | What was reused | What was rejected & why |
|---|---|---|
| `02_MTC_BACKTEST/scripts/backup_restore.py` (read-only, protected scope) | CLI shape (subcommands), UTC-stamped run naming | The tar.gz format: monolithic archive gives no per-file hashes, no append-only manifest, no byte-level restore verification, and is opaque without tooling. Replaced by copied tree + JSONL manifest. |
| `03_QUANTLENS/tools/progress_emitter.py` | `_atomic_write_json` pattern (tmp + `os.replace`), UTC-Z timestamp format, age-from-timestamp math | — |
| `03_QUANTLENS/tools/run_watchdog.py` | One-shot poll design, injected-notifier pattern, local-log notifier, notify-once dedupe state file, never-crash-the-poll notifier contract | Its run-state machine (done/failed/stalled) — dead-man silence detection is a different contract (no terminal states; silence IS the signal). |
| `02_MTC_BACKTEST/scripts/health_alerts.py` | Exit-code convention (0 ok / non-zero alert) extended to 0/2/3 | — |

No new third-party dependency: standard library only, per the lane contract.

## Test evidence

- Unit suite: `Ran 19 tests in 0.530s — OK` (final run; full transcript summary in
  `RESTORE_DRILL_EVIDENCE.md`).
- D026 drill verdicts (commands + real output in `RESTORE_DRILL_EVIDENCE.md`):
  dry-run-writes-nothing PASS; backup+readback PASS; RED unrecoverable-without-backup
  PASS (0/3 baseline hashes remain in damaged live tree); GREEN restore PASS (3/3
  byte-identical, empty dir preserved); tampered-backup refused PASS (rc 1);
  watchdog fresh-beat PASS (rc 0); killed-beat flagged+notified PASS (rc 2, one
  alert event); corrupt-beat check-failed PASS (rc 3).
- Repo guard (preflight, before this report): `RESULT: PASS` (branch clean, fresh,
  in sync with upstream, no protected/untracked findings).

## Commands and self-QA

- Verified worktree clean on `feature/wp-p0-26-opsa-tooling-20260825` at `0aa57ef6`
  (= local `origin/master` tip) before any edit; repo guard preflight PASS.
- All tool invocations recorded verbatim in `RESTORE_DRILL_EVIDENCE.md`; every
  claimed check has its real output captured there.
- Drill fixtures were created and destroyed inside this worktree only; no read of
  any store outside the worktree.
- `python -m unittest test_opsa` green (19/19) before staging.

## Commit inventory and staged paths

Single commit on this branch after its `origin/master` base `0aa57ef6`:

- `HEAD` — `feat(wp-p0-26): OPS-A local backup/restore + watchdog tooling (T1 partial, lane J 2026-08-25)`.
  `HEAD` is referenced because a commit cannot embed its own SHA without changing
  that SHA; the exact hash is printed in the implementer handoff and below in this
  report after committing (see "Final report" in the handoff message).

Exact paths staged:

```text
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/LANE_REPORT.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/NOTIFIER_PROPOSAL.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/RESTORE_DRILL_EVIDENCE.md
MTC_COMMAND_CENTER/tools/opsa/README.md
MTC_COMMAND_CENTER/tools/opsa/backup.py
MTC_COMMAND_CENTER/tools/opsa/config.example.json
MTC_COMMAND_CENTER/tools/opsa/heartbeat.py
MTC_COMMAND_CENTER/tools/opsa/opsa_common.py
MTC_COMMAND_CENTER/tools/opsa/restore.py
MTC_COMMAND_CENTER/tools/opsa/test_opsa.py
MTC_COMMAND_CENTER/tools/opsa/watchdog.py
```

Handoff files (`_AI_MEMORY/GLOBAL_HANDOFF.md`, `_AI_MEMORY/NEXT_STEPS.md`) are
updated per repo rules as part of the same commit.

## Open issues / gated next steps

1. **Lead T1 Gate 5 review** of this delivery (tooling + evidence), then authorized
   git sequencing. Repair cap T1 = 2.
2. **Phone-push notifier choice** (owner decision; `NOTIFIER_PROPOSAL.md`) → one
   `Notifier` implementation behind the existing registry.
3. **Real phone drill** (kills heartbeat, receives push, measures detect→delivery) —
   required for package acceptance; gated behind G9 + owner authorization.
4. **KVM2 host-install step** (heartbeat wiring, checker scheduling, NTP/drift
   check per #45, retention policy, cross-location backup automation) — T0 for that
   step under host-access authorization; explicitly NOT tonight.
5. Retention/size-budget policy and bulk-log archive-then-verify (plan §12.6.2(b))
   — owner-approved exact lists, future package work.
6. Nothing was pushed or merged.
