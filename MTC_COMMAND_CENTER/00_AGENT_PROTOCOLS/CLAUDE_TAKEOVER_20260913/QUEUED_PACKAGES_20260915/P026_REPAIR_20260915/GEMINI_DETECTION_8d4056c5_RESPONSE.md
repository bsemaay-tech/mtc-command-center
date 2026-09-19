# DETECTION REVIEW REPORT: WP-P0-26 CANDIDATE `8d4056c5`
**Reviewer:** Gemini 3.8 Flash (High) (Supplemental Read-Only Detection Reviewer; `SUPPLEMENTAL_UNEXECUTED`)  
**Corpus / Context:** `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_CAND_20260915`  
**Candidate Commits:** `6ac9cfb7` (Slice 1: OPS-A completion-marker repair) + `8d4056c5` (Slice 2: P0-30 adapter slice)  
**Authorities:** Owner rulings `OD-20260915-P026-REPAIR-LEAD-1` ("A") & `OD-20260915-P026-ADAPTER-LEAD-1` ("A")

---

## (a) Conformance Table

Conformance against scope packet `P026_LOCAL_SCOPE_DECISION_20260907.md` §2, §4, and §5 (extended by `OD-20260915-P026-ADAPTER-LEAD-1`):

| Scope Section / Clause | Specification | Status | Location in Packet Copies | Notes / Falsification Test |
|---|---|---|---|---|
| **§2 File Ceiling** | Exactly 5 MODIFY files in tools/opsa, 0 ADD; Slice 2 authorized extending by 2 repo-root files (`p030_closed_partition_backup_adapter.py`, `check_p030_closed_partition_backup_adapter.py`). `watchdog.py` was landed in `53d33dbc`. | **IMPLEMENTED-AS-WRITTEN** | `subject/DIFFSTAT_fcac0ac6_8d4056c5.txt:1-8` | 6 files modified, 0 files added. Diffstat confirms 6 files changed (+555, −51). |
| **§4 Completed-run manifest & marker** | Immutable per-run `RUN_MANIFEST.jsonl` + `COMPLETE.json` written exclusively and atomically only after every readback hash passes. Once written, never rewritten. | **IMPLEMENTED-AS-WRITTEN** | `subject/backup_8d4056c5.py:106-111`, `:236-280`; `subject/opsa_common_8d4056c5.py:153-165` | `write_once_bytes` uses `open(..., 'xb')` (exclusive creation, `O_EXCL`), flush + fsync. Tested in `test_completed_run_restores_by_explicit_id_including_copied_run_directory`. |
| **§4 Partial / interrupted runs** | A partial or interrupted run leaves no completion marker or per-run manifest. | **IMPLEMENTED-AS-WRITTEN** | `subject/backup_8d4056c5.py:43-46`, `:105-112`, `:247-248` | `run_records` accumulate in memory; `write_completion_evidence` skipped if `errors` is non-empty. Tested in `test_interrupted_run_has_no_completion_marker_and_restore_refuses`. |
| **§4 Explicit-run restore & fail-closed** | Restore requires an explicit completed run ID; fails closed if marker/manifest missing, tampered, digest mismatched, or record mismatch. | **PARTIAL** | `subject/restore_8d4056c5.py:71-95`, `:129-177`; `subject/opsa_common_8d4056c5.py:221-251` | Refuses missing marker/manifest, record mismatch, declared count mismatch, and digest mismatch. **Defect:** Bare `restore.py` fails open on hand-made completion files for runs lacking `run_end` when file records exist (Finding F-01). |
| **§4 Removal of `--latest`** | Greatest-started-run selection removed; restore without explicit run ID errors. | **IMPLEMENTED-AS-WRITTEN** | `subject/restore_8d4056c5.py:58-59`, `:129-132`, `:276-278` | Argument removed from CLI parser; `select_run(None)` raises `ValueError`; `run_restore(..., run_id=None)` returns `RC_CHECK_FAILED` (3). Tested in `test_restore_without_explicit_run_id_fails_closed`. |
| **§4 Additive only** | Global `manifest.jsonl` record formats unchanged; backup CLI preserved; dry-run writes nothing; heartbeat untouched. | **IMPLEMENTED-AS-WRITTEN** | `subject/backup_8d4056c5.py:88-117`, `:282-291`; `subject/DELTA_fcac0ac6_8d4056c5.diff:1-165` | Global manifest records (`run_start`, `file`, `dir`, `skipped`, `run_end`) unchanged. Dry run writes nothing. |
| **§5 Test 1** | Interrupted/partial backup run has no `COMPLETE.json` and is refused by restore. | **IMPLEMENTED-AS-WRITTEN** | `subject/test_opsa_8d4056c5.py:535-568` | Named `test_interrupted_run_has_no_completion_marker_and_restore_refuses`. Tested both check-only and full restore. |
| **§5 Test 2** | Completed run restores by explicit ID, including copied run directory. Marker and manifest immutable. | **IMPLEMENTED-AS-WRITTEN** | `subject/test_opsa_8d4056c5.py:569-599` | Named `test_completed_run_restores_by_explicit_id_including_copied_run_directory`. Verifies copied tree and asserts `FileExistsError` on rewrite. |
| **§5 Test 3** | Tampered/mismatched marker or manifest is refused; backed-up file bit-rot refused behind gate. | **IMPLEMENTED-AS-WRITTEN** | `subject/test_opsa_8d4056c5.py:600-657` | Named `test_tampered_marker_or_run_manifest_is_refused` (5 mutation arms). |
| **§5 Test 4** | Restore without explicit run ID fails closed; latest-run selection no longer exists. | **IMPLEMENTED-AS-WRITTEN** | `subject/test_opsa_8d4056c5.py:515-534`, `:495-514` | Named `test_restore_without_explicit_run_id_fails_closed` and `test_newest_run_is_restored_only_by_its_explicit_id`. |
| **§5 Tests 5–7** | Watchdog silence bound required; dedupe transition ledger (`alert → recovery → alert`); corrupt dedupe state fail-safe. | **IMPLEMENTED-AS-WRITTEN** | Untouched in this diff; landed in `53d33dbc` | Retained and verified green in `LEAD_UNITTEST_312_slice2.txt:100-104, 122-123`. |
| **Slice 2 Extension** | Reserved store IDs (`RUN_MANIFEST.jsonl`, `COMPLETE.json`) rejected without writes. | **IMPLEMENTED-AS-WRITTEN** | `subject/opsa_common_8d4056c5.py:314-316`; `subject/test_opsa_8d4056c5.py:705-720` | Named `test_backup_rejects_store_ids_reserved_for_completion_evidence_without_writes`. |
| **Slice 2 Extension** | Adapter carries completion evidence byte-for-byte; tampered evidence refused through adapter. | **IMPLEMENTED-AS-WRITTEN** | `subject/adapter_8d4056c5_EXCERPT_restore_path_441-780.txt:566-596`; `subject/checker_8d4056c5_EXCERPT_mutants_and_new_fence_1130-1265.txt:1194-1262` | Named `test_isolated_restore_carries_the_runs_own_completion_evidence`. |

---

## (b) Fail-Open Hunt Table (Attack Shapes a–l)

| Attack Shape | Verdict | Refusing Line / Verification Citation | Analysis & Mechanism |
|---|---|---|---|
| **(a) Marker of another run ID copied into `runs/<id>/`** | **REFUSED** | `subject/opsa_common_8d4056c5.py:244-245` | `load_complete_marker` asserts `payload.get("run_id") == run_id`, raising `RunNotComplete(f"run {run_id}: completion marker names run {payload.get('run_id')!r}")`. Additionally, `verify_completion_evidence` in `subject/restore_8d4056c5.py:80-81` asserts `header.get("run_id") == run_id`. |
| **(b) `RUN_MANIFEST.jsonl` edited after marker written** | **REFUSED** | `subject/opsa_common_8d4056c5.py:248-250` | `load_complete_marker` calculates `sha256_file(manifest)` and compares against `payload.get("run_manifest_sha256")`. Mismatch raises `RunNotComplete(f"run {run_id}: per-run manifest hash mismatch...")`. |
| **(c) Marker digest matches per-run manifest listing fewer/different files than global manifest** | **REFUSED** | `subject/restore_8d4056c5.py:88` | `verify_completion_evidence` compares `per_run_files = sorted(_key(r) for r in run_records if r.get("record") == "file")` with `global_files = sorted(_key(r) for r in global_records if r.get("record") == "file" and r.get("run_id") == run_id)`. Mismatch raises `RunNotComplete(f"run {run_id}: per-run manifest file records differ from the global manifest")`. |
| **(d) Run with `errors > 0` or dry-run obtaining a marker** | **REFUSED** | `subject/backup_8d4056c5.py:100`, `:105`, `:247-248` | In `backup.py:run_backup`, `write_completion_evidence` is strictly gated behind `if not dry_run:` (line 100) and `if not errors:` (line 105). Inside `write_completion_evidence`, line 247 checks `if errors: return "refused: run had errors"`. |
| **(e) Hand-made `runs/<id>/` with marker but no `run_end` in global manifest** | **NOT REFUSED** | **FAIL-OPEN in bare `restore.py`** (Refused in adapter: `subject/adapter_8d4056c5_EXCERPT_restore_path_441-780.txt:485-486`) | **CRITICAL:** If an interrupted run wrote `run_start` and file records to `manifest.jsonl` but died before `run_end`, or if an attacker fabricated `run_start` and file records without `run_end`: `verify_completion_evidence` (`restore.py:71-95`) **never checks `global_records` for `run_end`**. In `run_restore` (`restore.py:204`), `incomplete_empty_run` is guarded by `if not file_records and ...`. For non-empty runs, `not file_records` is `False`, bypassing the check completely. Bare `restore.py` restores the files with `RC_OK` (0). |
| **(f) Run ID matched by prefix or case** | **REFUSED** | `subject/restore_8d4056c5.py:127-135`; `subject/opsa_common_8d4056c5.py:244` | Exact string equality is enforced against `available_run_ids` set (`restore.py:133`), in marker payload check (`opsa_common.py:244`), and per-run manifest header (`restore.py:80`). Prefix or case-altered IDs fail exact match. |
| **(g) `COMPLETE.json` declared files count disagrees with per-run manifest** | **REFUSED** | `subject/restore_8d4056c5.py:90-92` | `verify_completion_evidence` checks `if not isinstance(declared, int) or isinstance(declared, bool) or declared != len(per_run_files):`, raising `RunNotComplete`. |
| **(h) `readback != "match"` in per-run manifest** | **REFUSED** | `subject/restore_8d4056c5.py:93-94` | `verify_completion_evidence` checks `if any(r.get("readback") != "match" for r in run_records if r.get("record") == "file"):`, raising `RunNotComplete`. |
| **(i) Adapter path restoring a run bare `restore.py --run` would refuse** | **REFUSED** | `subject/adapter_8d4056c5_EXCERPT_restore_path_441-780.txt:737-738`, `:767-768` | Adapter executes bare `restore.run_restore` twice (check-only and restore) inside isolated roots. Any condition causing bare `restore.py` to return non-zero raises `ValueError("P026 check-only failed; restore withheld")` or `ValueError("P026 restore failed")`. Additionally, adapter enforces `_complete_p026_run` which strictly requires `run_end`. |
| **(j) Adapter fabricating or regenerating completion evidence instead of copying** | **REFUSED** | `subject/adapter_8d4056c5_EXCERPT_restore_path_441-780.txt:571-575`, `:594-595` | `_isolated_restore_inputs` reads raw bytes via `(source_run_dir / COMPLETE_MARKER_NAME).read_bytes()` and writes them unchanged via `write_bytes`. It never calls `write_completion_evidence` or constructs JSON. Fence in `check_p030_...py:803-804` verifies byte equality. |
| **(k) Store ID colliding with reserved file names** | **REFUSED** | `subject/opsa_common_8d4056c5.py:314-316` | `load_backup_config` checks `if store["id"] in (RUN_MANIFEST_NAME, COMPLETE_MARKER_NAME): raise ValueError(...)`. Called during config load in `backup.py` and `restore.py`. Refuses with rc 3 before any write. |
| **(l) `write_once_bytes` leaving a partial marker mistaken for complete** | **REFUSED** | `subject/opsa_common_8d4056c5.py:232-239` | If interrupted before marker write, `COMPLETE_MARKER_NAME absent` raises `RunNotComplete` (line 233). If marker write is torn/corrupted, `json.loads` raises `JSONDecodeError` or missing schema raises `RunNotComplete` (line 239). Unique millisecond run IDs prevent collisions across runs. |

---

## (c) Regression Findings

1. **Global Manifest Record Shapes:**  
   Records emitted to `<backup_root>/manifest.jsonl` (`run_start`, `file`, `dir`, `skipped`, `run_end`) remain byte-for-byte schema-identical to the pre-repair implementation (`backup_8d4056c5.py:113-117, 149-153, 158-162, 202-207, 218-221`). No field was removed, renamed, or restructured.

2. **Backup CLI & Dry-Run Behaviour:**  
   `backup.py` CLI parser retains `--config`, `--dry-run`, and repeatable `--store` options (`backup_8d4056c5.py:282-291`). When `--dry-run` is active, it walks/hashes sources, emits plan records to stdout, and writes zero bytes to disk—creating neither run directories, manifest records, nor completion evidence (`backup_8d4056c5.py:100, 148, 157, 182`). Verified by `test_dry_run_writes_nothing`.

3. **No-Delete Guarantee:**  
   No destructive primitive (`os.remove`, `os.unlink`, `Path.unlink`, `os.rmdir`, `Path.rmdir`, `shutil.rmtree`, `shutil.move`, `os.truncate`) exists in any operational code path under `MTC_COMMAND_CENTER/tools/opsa`. New primitive `write_once_bytes` uses `open(..., "xb")` with flush + fsync; failed writes do not invoke cleanup routines. `NoDeleteGuaranteeTests.test_no_delete_calls_in_opsa_tools` passes clean.

4. **Path Confinement:**  
   Strict path confinement via `resolve_confined_path` is preserved across all user- and manifest-supplied store IDs and relative paths. Tightened in `opsa_common_8d4056c5.py:314-316` to reject reserved completion marker names (`RUN_MANIFEST.jsonl`, `COMPLETE.json`), preventing store paths from masking or colliding with per-run completion files.

5. **Heartbeat Tooling:**  
   `heartbeat.py` and `check_p030_opsa_heartbeat_adapter.py` remain intact and exit 0. `opsa_common.py` preserves `HEARTBEAT_SCHEMA` and related helpers.

6. **Adapter Isolation & Mutant Detection:**  
   The tightened shared-archive mutant test in `check_p030_closed_partition_backup_adapter.py:1173-1193` specifically catches the isolation mutant for the correct architectural reason. Under the repaired P0-26 explicit-run gate, a shared archive swap causes `restore.py` to compare isolated per-run manifest files against the swapped global manifest. This triggers refusal `per-run manifest file records differ from the global manifest`, which the adapter surfaces as `P026 restore failed`. The test asserts that `stderr.getvalue()` contains this exact refusal string (lines 1188–1193). A generic restore failure or crash cannot pass this mutant test.

---

## (d) D026 Evidence Table

Verification of D026 defect-closure evidence (RED on pre-fix behavior, GREEN on candidate) across all arms:

| Refusal / Feature Gate | Test Name | Pre-Fix Module Result (RED) | Candidate Result (GREEN) | Evidence Log Source |
|---|---|---|---|---|
| **Interrupted Run Refusal** | `test_interrupted_run_has_no_completion_marker_and_restore_refuses` | `FAIL` (3 sub-arms fail; pre-fix restored incomplete run) | `OK` (refused with `run_not_complete`) | `sources/LEAD_RED_ARMS_PREFIX_BACKUP_RESTORE.txt:24-26`; `sources/LEAD_UNITTEST_312_slice2.txt:12-14` |
| **Explicit Run Restoration** | `test_completed_run_restores_by_explicit_id_including_copied_run_directory` | `ERROR` (pre-fix did not write completion files) | `OK` (evidence verified from copy) | `sources/LEAD_RED_ARMS_PREFIX_BACKUP_RESTORE.txt:20`; `sources/LEAD_UNITTEST_312_slice2.txt:8-9` |
| **Tampered Evidence Refusal** | `test_tampered_marker_or_run_manifest_is_refused` | `ERROR` (pre-fix had no gate to verify markers) | `OK` (5 mutation arms refused) | `sources/LEAD_RED_ARMS_PREFIX_BACKUP_RESTORE.txt:23`; `sources/LEAD_UNITTEST_312_slice2.txt:93-94` |
| **No-Run-ID Refusal** | `test_restore_without_explicit_run_id_fails_closed` | `FAIL` (pre-fix defaulted to `--latest`) | `OK` (fails closed, exit 2/3) | `sources/LEAD_RED_ARMS_PREFIX_BACKUP_RESTORE.txt:27`; `sources/LEAD_UNITTEST_312_slice2.txt:89-90` |
| **Roundtrip Marker Verification** | `test_roundtrip_byte_identical` | `FAIL` (asserted marker existence on pre-fix) | `OK` | `sources/LEAD_RED_ARMS_PREFIX_BACKUP_RESTORE.txt:28`; `sources/LEAD_UNITTEST_312_slice2.txt:91-92` |
| **Partial Manifest Empty Refusal** | `test_partial_run_declaring_files_but_having_no_records_fails_closed` | `ERROR` (2 sub-arms: check-only & restore) | `OK` | `sources/LEAD_RED_ARMS_PREFIX_BACKUP_RESTORE.txt:21-22`; `sources/LEAD_UNITTEST_312_slice2.txt:24-25` |
| **Reserved Store ID Rejection** | `test_backup_rejects_store_ids_reserved_for_completion_evidence_without_writes` | `FAIL` (2 sub-arms: `RUN_MANIFEST.jsonl` & `COMPLETE.json`, `1 != 3`) | `OK` (exits rc 3 without writes) | `sources/LEAD_RED_ARM_old_common_reserved_ids.txt:9-25`; `sources/LEAD_UNITTEST_312_slice2.txt:3-4` |
| **Adapter Completion Evidence Copy** | `test_isolated_restore_carries_the_runs_own_completion_evidence` | `ERROR` (old adapter lacked completion files in isolated root) | `OK` | `sources/LEAD_RED_ARM_old_adapter_new_checker.txt:26`; `sources/check_p030_closed_partition_backup_adapter_slice2_TAIL.txt:8-10` |

### Audit of Output Counts in `LEAD_VERIFICATION_P026_REPAIR.md`
- **Unit Tests Count:** Stated as `37 → 38 unit tests`. Verified in `sources/LEAD_UNITTEST_312_slice2.txt:130` (`Ran 38 tests ... OK`). **Exact match.**
- **Pre-Fix RED-Arm Failure Count:** Stated as `FAILED (failures=5, errors=4)`. Verified in `sources/LEAD_RED_ARMS_PREFIX_BACKUP_RESTORE.txt:30` (`Ran 37 tests ... FAILED (failures=5, errors=4)`). **Exact match.**
- **Reserved-ID RED Count:** Stated as `reserved-id test FAILED (failures=2) (AssertionError: 1 != 3)`. Verified in `sources/LEAD_RED_ARM_old_common_reserved_ids.txt:29` (`FAILED (failures=2)`). **Exact match.**
- **Old Adapter vs New Checker RED Count:** Stated as `Ran 45 tests, FAILED (failures=6, errors=3)`. Verified in `sources/LEAD_RED_ARM_old_adapter_new_checker.txt:341` (`Ran 45 tests in 5.834s ... FAILED (failures=6, errors=3)`). **Exact match.**
- **Checker Pre-Slice-2 vs Post-Slice-2 Count:** Stated as `Ran 44 tests, FAILED (failures=7, errors=2)` moving to `45 OK, exit 0`. Verified in `sources/check_p030_closed_partition_backup_adapter_TAIL.txt:124` (`Ran 44 tests ... FAILED (failures=7, errors=2)`) and `sources/check_p030_closed_partition_backup_adapter_slice2_TAIL.txt:8-10` (`Ran 45 tests in 6.650s ... OK`). **Exact match.**

---

## (e) Numbered Findings

### [F-01] REQUIRED: Bare `restore.py` fails open on hand-made completion evidence for runs lacking `run_end` in global manifest
- **File & Line:** `subject/restore_8d4056c5.py:71-95`, `:193-215` (diff lines 336-360, 386-391)
- **Description:**  
  `verify_completion_evidence` checks that `COMPLETE.json` and `RUN_MANIFEST.jsonl` are internally consistent, bind to each other's SHA-256, and that the per-run manifest's file records match the global manifest's file records for that run (`per_run_files == global_files`). However, **`verify_completion_evidence` never checks that a `run_end` record exists in `global_records`**, nor does it check `run_end.status == "ok"` or `run_end.errors == []`.
  
  In `run_restore`:
  ```python
  193: file_records = [record for record in selected if record.get("record") == "file"]
  194: run_end = next((record for record in reversed(records)
  195:                 if record.get("record") == "run_end"
  196:                 and record.get("run_id") == resolved), {})
  ...
  202: incomplete_empty_run = (not run_end or run_end.get("status") != "ok"
  203:                         or not declared_files_valid)
  204: if not file_records and (check_only or not selected or declares_files or incomplete_empty_run):
  205:     msg = (f"run {resolved} has nothing to verify: selected zero file records ...")
  ...
  214:     return RC_CHECK_FAILED
  ```
  Notice that line 204 evaluates `incomplete_empty_run` **only when `not file_records` is true** (i.e., an empty run). If a run has 1 or more files, `not file_records` evaluates to `False`, completely skipping the check!
  
  If a real backup process is interrupted after copying one or more files (leaving `run_start` and `file` records in `manifest.jsonl`, but no `run_end`), `backup.py` deliberately refrains from writing completion files. However, if an operator or attacker creates a hand-made `RUN_MANIFEST.jsonl` and `COMPLETE.json` inside `runs/<run_id>/` matching those recorded files, bare `restore.py` **will restore the incomplete run with RC_OK (0)**.
  
  In contrast, the P0-30 adapter (`p030_closed_partition_backup_adapter.py:480-491`) explicitly enforces `len(ends) == 1`, `end["status"] == "ok"`, and `end["errors"] == []`. Bare `restore.py` fails open against this attack shape (Attack Shape (e)).
- **Remediation:** In `verify_completion_evidence` (`restore.py`), require that `global_records` contains exactly one `run_end` record for `run_id` with `status == "ok"` and `errors == []`, matching the validation performed in `p030_closed_partition_backup_adapter.py`.

---

### [F-02] NIT: Global `manifest.jsonl` logs `run_end` with `status: ok` before `write_completion_evidence` executes
- **File & Line:** `subject/backup_8d4056c5.py:101-112`
- **Description:**  
  In `backup.py`, lines 101–104 append the `run_end` record to `manifest.jsonl` with `"status": "ok"` *before* calling `write_completion_evidence` at line 106. If `write_completion_evidence` fails (for example, due to an unexpected `FileExistsError` or disk exhaustion / permission failure when writing `RUN_MANIFEST.jsonl`), line 111 sets local `status = "partial"`, stdout emits `status: "partial"` with `completion_marker: "failed: ..."`, and `run_backup` returns `RC_ERROR`. However, `manifest.jsonl` is left with a durable record declaring `status: ok` for a run that lacks valid completion evidence.
  
  While restore fails closed because `COMPLETE.json` is missing, the global append-only log records an inaccurate terminal status.
- **Remediation:** Either record `run_end` after `write_completion_evidence` succeeds, or record completion evidence status in the `run_end` manifest payload.

---

### [F-03] NIT: `load_complete_marker` leaves field-level type validation to callers
- **File & Line:** `subject/opsa_common_8d4056c5.py:236-251`
- **Description:**  
  `load_complete_marker` validates JSON parseability, schema string, `run_id` match, and SHA-256 integrity against `RUN_MANIFEST.jsonl`. However, validating that `files` is a non-boolean integer and `readback == "match"` is implemented inside `restore.py:verify_completion_evidence`. External consumers relying solely on `load_complete_marker` must re-implement these field checks.
- **Remediation:** Move the `isinstance(declared, int) and not isinstance(declared, bool)` and `readback == "match"` validations directly into `load_complete_marker` in `opsa_common.py`.

---

## (f) Exact Read Coverage with Ranges and Continuations

All reads were conducted using the native, read-only file viewing tool within `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_CAND_20260915` (plus the router `C:/LAB/Tradingview_LAB_CLEAN/AGENTS.md` per instructions), with at most 150 lines per view call:

1. `C:/LAB/Tradingview_LAB_CLEAN/AGENTS.md`: lines 1–64 (complete)
2. `PACKET_SHA256SUMS.txt`: lines 1–29 (complete)
3. `subject/DIFFSTAT_fcac0ac6_8d4056c5.txt`: lines 1–8 (complete)
4. `subject/COMMITS_fcac0ac6_to_8d4056c5.txt`: lines 1–85 (complete)
5. `subject/DELTA_fcac0ac6_8d4056c5.diff`: lines 1–887 (complete across 6 continuation views: 1–150, 151–300, 301–450, 451–600, 601–750, 751–887)
6. `subject/backup_8d4056c5.py`: lines 1–295 (complete across 2 continuation views: 1–150, 151–295)
7. `subject/restore_8d4056c5.py`: lines 1–294 (complete across 2 continuation views: 1–150, 151–294)
8. `subject/opsa_common_8d4056c5.py`: lines 1–321 (complete across 3 continuation views: 1–150, 151–300, 301–321)
9. `subject/adapter_8d4056c5_EXCERPT_imports_1-60.txt`: lines 1–62 (complete)
10. `subject/adapter_8d4056c5_EXCERPT_restore_path_441-780.txt`: lines 1–342 (complete across 3 continuation views: 1–150, 151–300, 301–342)
11. `subject/adapter_6ac9cfb7_PREFIX_EXCERPT_isolated_inputs_561-625.txt`: lines 1–67 (complete)
12. `subject/checker_8d4056c5_EXCERPT_fixtures_1-75.txt`: lines 1–77 (complete)
13. `subject/checker_8d4056c5_EXCERPT_isolation_test_904-1002.txt`: lines 1–101 (complete)
14. `subject/checker_8d4056c5_EXCERPT_mutants_and_new_fence_1130-1265.txt`: lines 1–138 (complete)
15. `sources/P026_LOCAL_SCOPE_DECISION_20260907.md`: lines 1–96 (complete)
16. `sources/DECISIONS_rows_P026.md`: lines 1–3 (complete)
17. `sources/LEAD_VERIFICATION_P026_REPAIR.md`: lines 1–66 (complete)
18. `sources/LEAD_RED_ARMS_PREFIX_BACKUP_RESTORE.txt`: lines 1–35 (complete)
19. `sources/LEAD_RED_ARM_old_common_reserved_ids.txt`: lines 1–30 (complete)
20. `sources/check_p030_closed_partition_backup_adapter_slice2_TAIL.txt`: lines 1–14 (complete)
21. `sources/BASE_SHA256SUMS_fcac0ac6.txt`: lines 1–6 (complete)
22. `sources/LEAD_RED_ARM_old_adapter_new_checker.txt`: lines 1–150, 300–352 (continuation on failure summary)
23. `sources/check_p030_closed_partition_backup_adapter_TAIL.txt`: lines 1–132 (complete)
24. `sources/LEAD_UNITTEST_312_slice2.txt`: lines 1–150, 151–152 (complete across 2 continuation views)
25. `sources/BASE_SHA256SUMS_6ac9cfb7_adapter_slice.txt`: lines 1–5 (complete)
26. `sources/SHA256SUMS_8d4056c5_adapter_slice.txt`: lines 1–5 (complete)

---

## (g) Nonempty NOT VERIFIED

The following boundaries and items were not executed or verified directly:
- **No execution:** Operating in `SUPPLEMENTAL_UNEXECUTED` read-only mode, no commands, subagents, tests, Python interpreters, or shell executions were run. Test passes, failures, and exit codes are verified strictly from the recorded output transcripts and source bytes in the candidate packet.
- **Unexcerpted code in adapter & checker:** `p030_closed_partition_backup_adapter.py` and `check_p030_closed_partition_backup_adapter.py` are present in the packet as excerpts covering specific line ranges (adapter lines 1–60 and 441–780; checker lines 1–75, 904–1002, 1130–1265). Unexcerpted lines (adapter lines 61–440, 781–827; checker lines 76–903, 1003–1129, 1266–1879) were not inspected.
- **Host, Hardware, & Live Infrastructure:** Operational phases, real KVM2 host contacts, scheduled cron/systemd services, live trading engines, remote Git state, network transfers, and credentials were not inspected or verified.

---

## (h) Machine-Readable Verdict

```json
{
  "part": "P026_CAND_GEMINI",
  "verdict": "REQUEST_CHANGES",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "not_refused": [
    "e"
  ],
  "findings": [
    {
      "id": "F-01",
      "severity": "REQUIRED",
      "file": "subject/restore_8d4056c5.py:71-95,202-215",
      "title": "Bare restore.py does not verify run_end in global manifest for non-empty runs (fail-open on hand-made completion evidence for interrupted runs)"
    },
    {
      "id": "F-02",
      "severity": "NIT",
      "file": "subject/backup_8d4056c5.py:101-112",
      "title": "Global manifest.jsonl records run_end with status: ok before write_completion_evidence executes"
    },
    {
      "id": "F-03",
      "severity": "NIT",
      "file": "subject/opsa_common_8d4056c5.py:240-251",
      "title": "load_complete_marker leaves declared files count and readback validation to callers"
    }
  ],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
