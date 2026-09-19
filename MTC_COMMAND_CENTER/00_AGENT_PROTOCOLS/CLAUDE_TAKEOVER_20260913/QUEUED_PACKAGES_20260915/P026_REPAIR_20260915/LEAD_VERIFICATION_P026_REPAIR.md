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

---
# Slice 2 — adapter + checker + reserved store ids, candidate `8d4056c5b7b42e2273ecce6cc393987976871f6f` — 2026-09-15 11:00Z

**Authority:** owner "A" ~10:50Z = `OD-20260915-P026-ADAPTER-LEAD-1` (extend the slice by the two repo-root files). **Result: built by the Lead (disclosed), green, committed as `8d4056c5` on `feature/p026-completion-marker-20260915` (parent `6ac9cfb7`), pushed; NOT reviewed, NOT accepted. The former blocker is closed: both adapter checks exit 0.**

| Item | Done |
|---|---|
| Files | `p030_closed_partition_backup_adapter.py` (+16/−6), `check_p030_closed_partition_backup_adapter.py` (+88/−2), `MTC_COMMAND_CENTER/tools/opsa/opsa_common.py` (+3), `MTC_COMMAND_CENTER/tools/opsa/test_opsa.py` (+20/−2); 0 added. Base hashes at `6ac9cfb7`: `BASE_SHA256SUMS_6ac9cfb7_adapter_slice.txt`; result hashes: `SHA256SUMS_8d4056c5_adapter_slice.txt`. |
| Adapter | `_isolated_restore_inputs` reads the run's own `COMPLETE.json` + `RUN_MANIFEST.jsonl` from `runs/<run_id>/` (fail-closed `ValueError("P026 completion evidence is unavailable")` when either is missing) and writes them byte-for-byte into the isolated `runs/<run_id>/` before the check-only call; nothing is fabricated; the marker's digest keeps binding the same per-run manifest bytes; the isolated global manifest is still the validated snapshot, so the gate's per-run/global record comparison holds. |
| Checker | new fence `test_isolated_restore_carries_the_runs_own_completion_evidence`: observes the isolated root through the patched `restore.run_restore` call (root differs from the shared archive; marker + per-run manifest bytes equal the originals; restored bytes equal the captured prefix); then a marker with a broken `run_manifest_sha256` and one naming another run id are each refused through the adapter path (`P026 check-only failed; restore withheld`) with the target left empty. The shared-archive reversion mutant test now accepts `P026 restore failed` only when restore's stderr names `per-run manifest file records differ from the global manifest` (a generic restore failure would no longer pass it). |
| opsa_common | `load_backup_config` refuses store ids equal to `RUN_MANIFEST.jsonl` / `COMPLETE.json` (a store of that name would occupy the marker's path inside `runs/<run_id>/`); `test_opsa.py` adds the write-free refusal test (rc 3, no manifest, no `runs/`). Lead-found while writing the adapter fix; within the original packet's file ceiling (opsa_common + test_opsa are MODIFY files) and the same defect ("completed-run identity"). |

## Evidence (pinned Python 3.12.12; Ruff 0.16.4 from `C:/tmp/wp_p0_04_tooling_20260825/Scripts/ruff.exe`)
| Check | Observed |
|---|---|
| `python -m unittest test_opsa -v` | `Ran 38 tests … OK` (`LEAD_UNITTEST_312_slice2.txt`; was 37) |
| `check_p030_closed_partition_backup_adapter.py` | `Ran 45 tests … OK`, exit 0 (`check_p030_closed_partition_backup_adapter_slice2.txt`; was 44 tests, `FAILED (failures=7, errors=2)`); the three remaining `run_not_complete` lines in the output are the new fence's two tampered arms and the mutant test's gate refusal |
| `check_p030_opsa_heartbeat_adapter.py` | exit 0 (`check_p030_opsa_heartbeat_adapter_slice2.txt`) |
| Ruff `--select E9,F821,F811,F401,F841` on `tools/opsa`, the adapter and the checker | `All checks passed!` (`LEAD_RUFF_slice2.txt`) |
| `git diff --check` | clean |
| repo guard (worktree) | `RESULT: PASS` (`LEAD_GUARD_slice2.txt`) |
| **RED arm (a)** — the NEW checker against the `6ac9cfb7` adapter (scratch `C:/tmp/P026_RED_SLICE2/a`: old adapter file + new checker + the candidate's `tools/opsa`) | `Ran 45 tests`, `FAILED (failures=6, errors=3)`: the 8 slice-1 failures return and the new fence ERRORs (restore refused) — `LEAD_RED_ARM_old_adapter_new_checker.txt`. The mutant test passes on both adapters by design: it mutates isolation away, so the isolated-root copy is never exercised by it. |
| **RED arm (b)** — the NEW `test_opsa.py` against the `6ac9cfb7` `opsa_common.py` (scratch `…/b`) | reserved-id test `FAILED (failures=2)` (`AssertionError: 1 != 3` per subtest — the old config loader accepts the reserved names) — `LEAD_RED_ARM_old_common_reserved_ids.txt`; full suite there: 38 run, the same 2 subtest failures only (`LEAD_RED_ARM_old_common_full_suite.txt`) |

## Next
Gemini delta corroboration of `6ac9cfb7..8d4056c5` (packet from this record); exact Opus (Wednesday lane 4, re-pinned to `8d4056c5`) and exact Sol (Sep 19). The Lead never accepts its own code.

Recorded by Claude Opus 5 Lead (743291).

---
# Slice 3 — Gemini detection findings, candidate `d81b07f62569996edb20dc96f83e7d7029406cdd` — 2026-09-15 11:40Z

**Trigger:** Gemini 3.8 flash-high DETECTION review of `8d4056c5` (counted attempt 1, 11:23Z): **REQUEST_CHANGES** — F-01 REQUIRED, F-02/F-03 NITs; adjudication `LEAD_ADJUDICATION_GEMINI_DETECTION_8d4056c5.md`. All three confirmed against the bytes by the Lead and fixed in one commit `d81b07f6` (parent `8d4056c5`), pushed. Same authorization as slices 1-2 (a correction to the Lead-built repair under the owner's "A" rulings); authorship disclosed; NOT reviewed, NOT accepted.

| Finding | Change |
|---|---|
| F-01 REQUIRED — bare restore accepted a hand-made completion pair for a run the tool never closed | `restore.verify_completion_evidence` now requires exactly one `run_end` for the run in the global manifest with `status == "ok"`, `errors == []`, and `files` equal to the marker's declared count (refusals: "global manifest carries N run_end records", "run_end is status='partial' with 1 error(s)", "run_end declares files=…"). New fence `test_hand_made_completion_evidence_cannot_revive_a_run_the_tool_did_not_close`: interrupted arm (run_end partial) and crashed arm (no run_end; global manifest rebuilt without it in a second root), each check-only and restore → rc 3, `run_not_complete`, detail names `run_end`, target never created. `test_partial_run_declaring_files_but_having_no_records_fails_closed` reworked: the forged pair on the partial run is refused by the run_end rule; the "nothing to verify" fence is kept alive through a tool-closed zero-file run. |
| F-02 NIT — global `run_end ok` written before the evidence | `backup.run_backup` writes `RUN_MANIFEST.jsonl` + `COMPLETE.json` first; a failed evidence write is appended to the run's errors and the `run_end` says `partial`. Record shapes unchanged. |
| F-03 NIT — loader leaves field validation to callers | `load_complete_marker` docstring names it the pair-integrity half and `restore.verify_completion_evidence` the single gate (no second validation path). |
| adapter checker | `test_partial_run_that_p026_check_only_accepts_never_reaches_restore` asserted the OLD fail-open (`run_restore(...) == RC_OK` on a partial run) as a precondition; it now expects `RC_CHECK_FAILED` and keeps the adapter's own envelope fence. |

## Evidence (pinned Python 3.12.12; Ruff 0.16.4)
| Check | Observed |
|---|---|
| `python -m unittest test_opsa -v` | `Ran 39 tests … OK` (`LEAD_UNITTEST_312_slice3.txt`; was 38) |
| `check_p030_closed_partition_backup_adapter.py` | `Ran 45 tests … OK`, exit 0 (`check_p030_closed_partition_backup_adapter_slice3.txt`) |
| `check_p030_opsa_heartbeat_adapter.py` | exit 0 (`check_p030_opsa_heartbeat_adapter_slice3.txt`) |
| Ruff `--select E9,F821,F811,F401,F841` | `All checks passed!` (`LEAD_RUFF_slice3.txt`) |
| `git diff --check` / repo guard | clean / `RESULT: PASS` (`LEAD_GUARD_slice3.txt`) |
| **RED arm** — the slice-3 `test_opsa.py` against the `8d4056c5` `restore.py` + `backup.py` (scratch `C:/tmp/P026_RED_SLICE3`) | `Ran 39 tests`, `FAILED (failures=3, errors=1)`: the hand-made-evidence fence fails in 3 subtests (the slice-2 restore verified/restored the un-closed run) and the reworked partial-manifest test errors — `LEAD_RED_ARM_slice2_restore_backup_new_tests.txt` |
| Hashes | `SHA256SUMS_d81b07f6_slice3.txt` |

## Next
Gemini DELTA of `8d4056c5..d81b07f6` (root `P026_DELTA_GEMINI`) → exact Opus (lane 4, re-pinned to `d81b07f6`) → exact Sol (Sep 19). The Lead never accepts its own code.

Recorded by Claude Opus 5 Lead (743291).
