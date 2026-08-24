# Lane J Report — WP-P0-26 OPS-A local backup/restore + dead-man watchdog tooling

## Status

**TOOLING DELIVERED / ACCEPTANCE OPEN — repair round 1 of max 2 applied
(2026-08-25), awaiting re-audit.** The T1 local tooling half of WP-P0-26 is
implemented, self-QA'd, and D026 RED/GREEN-proven on fixtures; a fresh T1
claude-opus-5 audit of `73b72bd0` returned REQUEST_CHANGES (2 required + scope
revert + 5 nits), all addressed in repair round 1 (see Repair section). Package
acceptance is **NOT claimable**: it requires a real phone-push drill plus the KVM2
host-install step, both gated behind G9 and owner authorization — deliberately not
tonight's work. Audit tier **T1** (local, non-economic tooling; no
host/credential/live surface). Lead owns acceptance/audit/git sequencing.

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

**No-delete guarantee:** no destructive call (`os.remove(`, `os.unlink(`, `.unlink(`
in any form including `missing_ok=`, `os.rmdir(`, `.rmdir(`, `shutil.rmtree(`,
`.rmtree(`, `shutil.move(`, `os.truncate(`, `send2trash(`) exists in any shipped
tool; enforced mechanically by
`test_opsa.py::NoDeleteGuaranteeTests::test_no_delete_calls_in_opsa_tools`
(needles extended in repair round 1 after the audit proved the old list blind to
`dest.unlink(missing_ok=True)` and `os.rmdir(...)` — both mutants now RED, see
`RESTORE_DRILL_EVIDENCE.md` § C2).
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
- Commands offered as D026 proof are recorded with their real output in
  `RESTORE_DRILL_EVIDENCE.md`.
- Round-0 drill fixtures stayed inside this worktree; continuation falsification
  copies stayed under `%TEMP%`. No real evidence store was read.
- Round-0 `python -m unittest test_opsa` was green (19/19). Continuation final
  validation uses the mandated command
  `python -m pytest -q MTC_COMMAND_CENTER/tools/opsa/test_opsa.py` (23/23).

## Commit inventory and staged paths

Branch history after its base `0aa57ef6`:

- `73b72bd0` — `feat(wp-p0-26): OPS-A local backup/restore + watchdog tooling (T1 partial, lane J 2026-08-25)`.
- `40b31e0a` — quota-interrupted WIP repair, preserved verbatim as required.
- `HEAD` — `fix(wp-p0-26): complete repair round 1 - notifier coverage, delete-guard needles`.
  `HEAD` is used because a commit cannot embed its own SHA without changing it;
  the exact final SHA is printed in the implementer handoff.

Original delivery paths:

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

Exact paths staged by the continuation completion commit:

```text
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/LANE_REPORT.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/RESTORE_DRILL_EVIDENCE.md
```

Handoff files (`_AI_MEMORY/GLOBAL_HANDOFF.md`, `_AI_MEMORY/NEXT_STEPS.md`) were
edited in the round-0 commit — **outside this lane's authorized output paths**; repair
round 1 reverted both to base `0aa57ef6` (see Repair section). This report is the
lane's handoff record; re-adding handoff entries is the Lead's call at acceptance.

## Repair round 1 (2026-08-25, T1 cap 2 — round 1 of max 2)

Fresh T1 claude-opus-5 audit of `73b72bd0`: REQUEST_CHANGES. All required repairs,
the scope revert, and all five nits are addressed below; every behavioural change is
D026-proven (RED on pre-fix copies in `%TEMP%`, GREEN on the fixed tree) with
commands + real output in `RESTORE_DRILL_EVIDENCE.md` § C1–C5.

### Required repair 1 — notifier coverage for directory-level check-failures

`watchdog.py`: an `alert`/`check_failed` outcome with empty per-id ids (missing
state dir; empty state dir with no `--expect`; invalid `--now`) previously produced
rc 3 with ZERO notifier events. New `_notify_outcome()` delivers exactly one
synthetic checker-level event (id `_watchdog_check`, state `check_failed`, error
text) whenever the outcome carries no per-id events — every `alert`/`check_failed`
outcome now leaves at least one alert record. Per-id delivery unchanged (guarded by
a non-regression test). RED: both new tests error on the pre-fix file (notifier log
never created); GREEN: rc 3 + exactly one event (§ C1). README + module docstring
document the synthetic event.

### Required repair 2 — delete-guard needles

`test_opsa.py` banned list extended with `.unlink(`, `os.rmdir(`, `.rmdir(`,
`os.truncate(` (`shutil.move(` already present); `.write_bytes(`/`.write_text(`
deliberately NOT banned — legitimate overwrites; scope remains deletion/truncation/
removal of existing paths. Both auditor mutants (`dest.unlink(missing_ok=True)`;
`os.rmdir(dest.parent)`) are RED under the new needles, and the OLD needle list is
shown passing both (blind spot proven, § C2). Clean-tree scan GREEN.

### Required repair 3 — scope revert

Round 0 edited `_AI_MEMORY/GLOBAL_HANDOFF.md` and `_AI_MEMORY/NEXT_STEPS.md`, which
were outside this lane's authorized output paths. Both reverted to base `0aa57ef6`
with the authorized exact command
(`git checkout 0aa57ef6 -- MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md
MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md`); `git diff 0aa57ef6 -- <those files>`
is empty. Factual content worth keeping, preserved here for the record (the
handoff entries said, in brief):

- **Status:** TOOLING DELIVERED / ACCEPTANCE OPEN on
  `feature/wp-p0-26-opsa-tooling-20260825` (worktree `C:\WPP026_20260825`), no
  push; stdlib-only `tools/opsa/` package + this evidence directory; 19/19 unit
  tests at round 0 (23/23 after R1); no delete code path (mechanically enforced);
  reuse record in this report. *(All of this is already stated above in this
  report — nothing new needed moving.)*
- **Next actions the NEXT_STEPS entry listed** (already covered by "Open issues /
  gated next steps" below, restated for the record): 1) [AI: Lead] T1 Gate 5
  review of this delivery (repair cap 2; round 1 used, one remains), then
  authorized merge sequencing per the parallel-lane plan. 2) [AI: Barış] notifier
  decision on `NOTIFIER_PROPOSAL.md` (self-hosted ntfy recommended; public ntfy.sh
  fallback; Telegram contingency; Pushover rejected). 3) [AI: Barış, gated behind
  G9] authorize the real phone-push drill + KVM2 host-install step (T0 for host
  execution); detect→delivery bound stays `[OPEN]` until that drill measures it.

### Nits (all fixed)

4. `restore.py --check-only` no longer reports `dirs_recreated` it did not create —
   the counter now increments only when a directory is actually created (check-only
   always reports 0; restore-mode count unchanged and still real). RED
   `AssertionError: 1 != 0` on pre-fix restore.py; GREEN reproduction
   `"dirs_recreated": 0` (§ C4); the A5 evidence line was corrected with a dated
   note pointing at § C4.
5. Provenance corrected in `opsa_common.py` (module docstring + RC comment) and
   `README.md`: health_alerts.py's convention is 0 ok / non-zero alert; the
   three-way extension (rc 2 alert vs rc 3 check-failed) is this package's own —
   matching this report's reuse table.
6. `watchdog.py --now` with an unparseable value now exits rc 3 with a
   check-failed record + one `_watchdog_check` notifier event instead of a raw
   ValueError traceback (rc 1). RED/GREEN at CLI level (§ C3) plus a unit test.
7. `config.example.json` now uses neutral placeholder paths
   (`C:/EXAMPLE/EVIDENCE/PATH/…`, `D:/EXAMPLE/BACKUP_ROOT_CHANGE_ME`) — no fenced
   canonical-checkout paths.
8. Unused `to_posix_rel` import removed from `backup.py`; the no-op
   `except BaseException: raise` in `opsa_common.atomic_write_bytes` deleted
   (failure propagates naturally; tmp leftovers still deliberately not cleaned);
   `read_jsonl` docstring now says `line_number`, matching the emitted key.

### Post-repair state

- Unit suite: **23 tests, OK**
  (`python -m pytest -q MTC_COMMAND_CENTER/tools/opsa/test_opsa.py`, § C6.6): 19 original
  + 4 new (notifier coverage ×2, invalid-`--now`, per-id non-regression guard);
  nit-4 assertion folded into the existing check-only test.
- Continuation state assessment: all 2 REQUIRED items, scope item 3, and all 5 nits
  independently rechecked; fresh D026 transcripts and the watchdog rc 0/2/3 matrix
  are in `RESTORE_DRILL_EVIDENCE.md` § C6.
- Completion commit (this branch, after WIP `40b31e0a`):
  `fix(wp-p0-26): complete repair round 1 - notifier coverage, delete-guard needles`.
  No push. Staged paths listed in the implementer handoff message and the final
  report.

## Open issues / gated next steps

1. **Lead T1 Gate 5 re-audit** of the repaired delivery (tooling + evidence),
   then authorized git sequencing. Repair cap T1 = 2 — round 1 used (this repair),
   one round remains.
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

## Codex CLI 2026-08-25 — owner-authorized closure after the T1 cap

The Claude Lead supplied an owner-authorized, bounded closure contract for the two
reproduced round-2 defects. This Codex counterpart implementer changed only the
five OPSA source/test files required by those defects and these two lane records.

### Closure repair 1 — restore now fails closed

- An explicit run id absent from the manifest returns check-failure rc 3 with
  `error: run id not found in manifest`; it can no longer become an empty rc-0 run.
- A failed/partial or declared-nonempty run with zero file records returns rc 3 and
  an explicit `nothing to verify` error in both restore and `--check-only` modes.
  The summary is `status=failed`, `verified_against_manifest=0`, `errors=1`; no
  restore directory is created.
- D026 proof is recorded in `RESTORE_DRILL_EVIDENCE.md` § C7: the exact pre-fix
  implementation returned rc 0 for the unknown run and for both empty-run modes;
  the repaired tree returns rc 3.

### Closure repair 2 — every derived path is root-confined

- `opsa_common.resolve_confined_path` canonicalizes the configured root and checks
  both literal and repeatedly URL-decoded path forms. It rejects parent components,
  absolute paths, UNC/Windows-rooted forms, drive prefixes, NUL/empty components,
  and any result that is not strictly below its configured root.
- Config store ids are validated before `backup.py` creates a manifest; backup
  destinations, restore backup-source and target destinations, and heartbeat files
  all use the same helper.
- Restore preflights every selected source/destination before its first target
  mutation, so one later malicious manifest record cannot follow an earlier valid
  write.
- D026 tests cover plain `../`, `..%2F`, absolute and `C:`-prefixed ids. The exact
  pre-fix tree wrote outside the restore/state roots (and accepted the encoded id);
  the repaired tree returns rc 3 and writes no heartbeat or outside restore file.

### Closure QA and impact statement

```text
Targeted closure regressions: 5 passed, 6 subtests passed in 0.17s
Full OPSA suite:              28 passed, 6 subtests passed in 0.84s
Python compileall:            rc 0
```

Parity/Pine/MTC/trading impact: none. This is local, non-economic OPSA tooling;
no live host, deployment, credential, schema, notifier, or external service action
was performed. Full RED/GREEN commands and real output are in the evidence record.

Exact closure paths prepared for the single owner-authorized commit:

```text
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/LANE_REPORT.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/RESTORE_DRILL_EVIDENCE.md
MTC_COMMAND_CENTER/tools/opsa/backup.py
MTC_COMMAND_CENTER/tools/opsa/heartbeat.py
MTC_COMMAND_CENTER/tools/opsa/opsa_common.py
MTC_COMMAND_CENTER/tools/opsa/restore.py
MTC_COMMAND_CENTER/tools/opsa/test_opsa.py
```

Commit message:
`fix(wp-p0-26): closure - fail-closed restore statuses, root-confined path validation`.
No push.
