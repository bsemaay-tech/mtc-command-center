# LEAD_VERIFICATION — WP-P0-26 completion-marker repair candidate `6ac9cfb7b923e8d86b8546f7c0117fbb0553d0a3` — 2026-09-15 08:47Z

**Authority:** owner `OD-20260915-P026-REPAIR-LEAD-1` ("A") on the 2026-09-12 queue decision and the scope packet `C:/tmp/P026_LOCAL_SCOPE_DECISION_20260907.md` (§2 five MODIFY files, §4 behaviour, §5 tests). **Result: candidate built by the Lead (disclosed), green in isolation, committed on `feature/p026-completion-marker-20260915` from `origin/master` `fcac0ac6`, backup-pushed; NOT reviewed, NOT accepted; ONE KNOWN BLOCKER outside the packet's file ceiling (§4 below) — stopped and reported per packet §7.**

## Scope kept
| Packet item | Done |
|---|---|
| §2 files | 4 of the 5 enumerated files modified: `backup.py`, `restore.py`, `opsa_common.py`, `test_opsa.py`; `watchdog.py` untouched (its half — explicit silence bound, no 900 s default, alert→recovery→alert ledger, corrupt-state fail-safe — already landed in `53d33dbc` with tests 5-7 of §5). 0 files added. Base hashes before the first edit: `BASE_SHA256SUMS_fcac0ac6.txt` (`backup.py c2aecdac…`, `restore.py 4c415719…`, `opsa_common.py 7136c42a…`, `watchdog.py 0d4ba79d…`, `test_opsa.py 69054441…`). |
| §4 completed-run manifests | `RUN_MANIFEST.jsonl` (header + every file/dir/skipped record) then `COMPLETE.json` (schema, run_id, started/finished, config, files/bytes/skipped/dirs, `run_manifest_sha256`, `readback=all_match`) written exclusively inside `runs/<run_id>/` only when the run ended with zero errors; both immutable (`write_once_bytes`: `open(..., "xb")`, flush, fsync; no tmp, no rename, no delete). A partial/interrupted run leaves neither. |
| §4 explicit-run restore | `--run` required; `--latest` removed (argparse) and `select_run(None)` raises; `verify_completion_evidence` gate after field/confinement validation and before any hash check or write: refuses missing/unreadable/foreign-run marker, digest mismatch of the per-run manifest, per-run file records differing from the global manifest, declared count mismatch, non-matching readback; structured stderr `{"status":"check_failed","error":"run_not_complete",…}`, rc 3. Hash-mismatch refusal (rc 1) unchanged behind the gate. |
| §4 additive only | global `manifest.jsonl` records unchanged (`run_start`/`file`/`dir`/`skipped`/`run_end`); `backup.py` CLI unchanged; dry-run writes nothing (existing test); heartbeat untouched. |
| §5 tests (fixture-only) | 1 interrupted run → no marker, restore refuses (both modes); 2 completed run restores by explicit id, also from a copied backup root; marker + manifest immutable; 3 tampered/mismatched marker or manifest refused (five arms) + bit-rot still refused; 4 restore without run id fails closed (API / `select_run` / CLI); 5-7 = watchdog tests already present (`test_silence_bound_is_required…`, `test_alert_recovery_alert…`, `test_corrupt_dedupe_state…`). Forbidden things: no environment/credential read, no network, no SSH/SFTP, no scheduling, no host contact, no git action by the tools. |
| No-delete guarantee | `NoDeleteGuaranteeTests` still pass (no banned call in any shipped tool). |

## Evidence (pinned Python 3.12.12 `C:/tmp/P020_IMPL_20260912/…/.venv/Scripts/python.exe`)
| Check | Observed |
|---|---|
| `python -m unittest test_opsa` (worktree) | `Ran 37 tests … OK` (`LEAD_UNITTEST_312.txt`) |
| **RED on the pre-fix `backup.py` + `restore.py`** (scratch: base modules + the new `opsa_common.py` helpers so the module imports + the new tests) | `FAILED (failures=5, errors=4)` — exactly the new arms: roundtrip marker assertions, interrupted-run refusal (3 sub-arms), no-run-id refusal, completed-run/copied-root test, tampered-evidence test, the partial-manifest gate (2 sub-arms); the 28 unchanged fences pass on both (`LEAD_RED_ARMS_PREFIX_BACKUP_RESTORE.txt`) |
| Ruff 0.16.4 `--select E9,F821,F811,F401,F841` on `tools/opsa/*.py` | `All checks passed!` |
| `git diff --check` | clean |
| repo guard (worktree) | `RESULT: PASS` (`LEAD_GUARD.txt`) |
| `check_p030_opsa_heartbeat_adapter.py` (imports `opsa_common`) | exit 0 |
| **`check_p030_closed_partition_backup_adapter.py`** | **exit 1 — `Ran 44 tests`, `FAILED (failures=7, errors=2)` on 13 `run_not_complete` refusals** (`check_p030_closed_partition_backup_adapter.txt`; 12 refusals = `COMPLETE.json absent` in the isolated root; 1 = `test_shared_archive_reversion_mutant_is_detected`, where the new gate refuses first with `per-run manifest file records differ from the global manifest` and the test's expected error text no longer matches — the mutant is still refused). The same check: `Ran 44 tests … OK`, exit 0 on the base (`…_BASE_ct13.txt`). Precision correction 09:59Z: an earlier wording said "13 tests refuse"; it is 13 refusals / 9 failing tests. |

## 4. The blocker (packet §7: outside the file ceiling → stop and report)
`p030_closed_partition_backup_adapter.py` (WP-P0-30, merged to master 2026-09-13 — six days AFTER the P0-26 scope packet was written) restores through `restore.py` from an **isolated snapshot root it builds itself** (`_isolated_restore_inputs`, `:560-620`): it copies the stable-prefix receipt, the snapshot file and a validated global `manifest.jsonl` into a temp root — and, naturally, not the two completion files that did not exist when it was written. Under the repaired gate that isolated run has no `COMPLETE.json` → refused. This is the exact interaction the decision packet flagged ("the P0-26 repair must keep those adapters' interfaces unchanged"); the interfaces are unchanged, but restore's CONTRACT is now stricter by design, and the adapter's isolated root must carry the completion evidence too.

Fix size: ~6 lines in `_isolated_restore_inputs` — read `COMPLETE.json` and `RUN_MANIFEST.jsonl` from `runs/<run_id>/` and write them into the isolated `runs/<run_id>/` (the marker's digest still binds the same manifest bytes; the isolated global manifest must still contain the run's file records, which it does). Plus any adapter tests that fabricate runs by hand. Outside the five-file ceiling → **owner word needed**: (A) extend today's slice by that one file (the Lead does it now, same disclosure, adapter check must return to exit 0); (B) leave the candidate parked on its branch and have a P0-30 lane adapt the adapter (Codex Sep 19). Master is unaffected either way (the adapter check is not in CI — P0-27 reconciliation R10).

## Next
1. Owner: A / B above.
2. Gemini corroboration of the candidate (packet vs bytes; fixture RED/GREEN); exact Opus (Wednesday queue, addendum) and exact Sol (Sep 19) — T1 roster; the Lead never accepts its own code.
3. Only after acceptance: the drills of the decision packet §3 (owner-scoped, G9 for the host).

Recorded by Claude Opus 5 Lead (743291).
