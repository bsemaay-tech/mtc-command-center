# DELTA REVIEW REPORT: WP-P0-26 SLICE 3 (`8d4056c5..d81b07f6`)

**Reviewer:** Gemini 3.8 Flash (High) (Supplemental Read-Only Delta Reviewer; `SUPPLEMENTAL_UNEXECUTED`)  
**Packet Context:** `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_DELTA_20260915`  
**Candidate Commits:** `8d4056c5` (Slice 2) $\to$ `d81b07f6` (Slice 3 repair)  
**Authorities:** Owner rulings `OD-20260915-P026-REPAIR-LEAD-1` ("A") & `OD-20260915-P026-ADAPTER-LEAD-1` ("A")

---

## (a) Finding-Closure Table (F-01 / F-02 / F-03)

| Finding ID & Severity | Original Defect in `8d4056c5` | Resolution in `d81b07f6` | Citation in Packet Copies | Status |
|---|---|---|---|---|
| **F-01 REQUIRED** | `verify_completion_evidence` never checked `global_records` for `run_end`. Hand-made completion evidence matching recorded file records revived an un-closed run (interrupted or crashed) with exit code 0. | `restore.verify_completion_evidence` now checks `global_records` for exactly one `run_end` record for `run_id`, asserting `status == "ok"`, `errors == []`, and `end.get("files") == declared`. Refuses with `RunNotComplete` before any hash check or restore. Tested in `test_hand_made_completion_evidence_cannot_revive_a_run_the_tool_did_not_close`. | `subject/restore_d81b07f6.py:69-89`, `:107-109`; `subject/test_opsa_d81b07f6.py` (via `subject/DELTA_8d4056c5_d81b07f6.diff:101-175`) | **CLOSED** |
| **F-02 NIT** | `backup.py` appended `run_end status: ok` to global `manifest.jsonl` *before* `write_completion_evidence` executed, leaving a durable `"ok"` entry even if evidence creation failed. | In `backup.run_backup`, `write_completion_evidence` runs *before* `run_end` is appended. If evidence creation does not return `"written"`, the failure is appended to `errors`, and `status` is set to `"partial"`. The global log never records `"ok"` for a run lacking completion files. | `subject/backup_d81b07f6.py:216-233`; `subject/DELTA_8d4056c5_d81b07f6.diff:17-33` | **CLOSED** |
| **F-03 NIT** | `load_complete_marker` in `opsa_common.py` left field-level validation (`files` non-bool int, `readback == "match"`) to callers, creating ambiguity about whether callers must re-validate. | Docstring of `load_complete_marker` explicitly specifies that it is the pair-integrity half only. Field validation and global cross-checks live strictly in `restore.verify_completion_evidence` as the single canonical gate across all paths. No redundant second gate added. | `subject/opsa_common_d81b07f6.py:193-199`; `subject/DELTA_8d4056c5_d81b07f6.diff:46-52` | **CLOSED** |

---

## (b) Variant Table for Attack Shape (e)

### New Rule in `restore.verify_completion_evidence`
```python
    ends = [r for r in global_records
            if r.get("record") == "run_end" and r.get("run_id") == run_id]
    if len(ends) != 1:
        raise RunNotComplete(f"run {run_id}: global manifest carries {len(ends)} run_end "
                             "records for the run (exactly one successful run_end is required)")
    end = ends[0]
    if end.get("status") != "ok" or end.get("errors") != []:
        raise RunNotComplete(f"run {run_id}: global manifest run_end is status="
                             f"{end.get('status')!r} with {len(end.get('errors') or [])} "
                             "error(s); only a run the backup tool closed successfully "
                             "may be restored")
...
    if end.get("files") != declared:
        raise RunNotComplete(f"run {run_id}: global manifest run_end declares files="
                             f"{end.get('files')!r}, completion marker declares {declared}")
```

### Evaluation of Base Arms and Attack Variants

| Variant / Arm | Execution State & Inputs | Verdict | Refusing Line in `subject/restore_d81b07f6.py` | Mechanism / Refusal Message |
|---|---|---|---|---|
| **Base Arm 1: Interrupted run** | Global manifest has `run_end` with `status: "partial"` and `errors: [err]`. | **REFUSED** | `restore_d81b07f6.py:75-76` | `len(ends) == 1`, but `end.get("status") != "ok"` and `end.get("errors") != []`. Raises `RunNotComplete("... run_end is status='partial' with 1 error(s)...")`. |
| **Base Arm 2: Crashed run** | Process killed mid-run; global manifest has `run_start` and `file` records, but no `run_end`. | **REFUSED** | `restore_d81b07f6.py:71-72` | `len(ends) == 0 != 1`. Raises `RunNotComplete("... global manifest carries 0 run_end records for the run (exactly one successful run_end is required)")`. |
| **Variant 1: Duplicate `run_end`** | Global manifest carries two `run_end` records for the run (e.g., one `"ok"`, one `"partial"`). | **REFUSED** | `restore_d81b07f6.py:71-72` | `len(ends) == 2 != 1`. Raises `RunNotComplete("... carries 2 run_end records for the run ...")`. |
| **Variant 2: File count mismatch** | Global `run_end` is `"ok"`, but declares `files` differing from marker's `files`. | **REFUSED** | `restore_d81b07f6.py:87-88` | `end.get("files") != declared`. Raises `RunNotComplete("... global manifest run_end declares files=..., completion marker declares ...")`. |
| **Variant 3a: `errors` key absent** | Global `run_end` has `status: "ok"`, but `errors` key is omitted entirely. | **REFUSED** | `restore_d81b07f6.py:75-76` | `end.get("errors")` returns `None`. `None != []` evaluates to `True`. Raises `RunNotComplete`. |
| **Variant 3b: `errors: 0` (int)** | Global `run_end` has `status: "ok"`, but `errors` is set to integer `0` instead of `[]`. | **REFUSED** | `restore_d81b07f6.py:75-76` | `end.get("errors")` is `0`. `0 != []` evaluates to `True`. Raises `RunNotComplete`. |
| **Variant 4: Foreign `run_end`** | Global manifest has `run_end` for another `run_id`, but none for the target run. | **REFUSED** | `restore_d81b07f6.py:71-72` | Filter `r.get("run_id") == run_id` yields `len(ends) == 0 != 1`. Raises `RunNotComplete`. |
| **Variant 5: Malformed global line among run's records** | JSON syntax error on a line belonging to the run in `manifest.jsonl`. | **REFUSED** | `restore_d81b07f6.py:71-72`, `:101-102`, `:150-152` | If malformed line is `run_end` $\to$ `len(ends) == 0` (refused line 71); if a `file` record $\to$ `per_run_files != global_files` (refused line 101); if `run_start` $\to$ `run_id not in available_run_ids` (refused line 150). In all cases, restore fails closed before write. |

### Analysis of New and Reworked Tests
1. **`test_hand_made_completion_evidence_cannot_revive_a_run_the_tool_did_not_close`:**
   - **Attacker Forgery Fidelity:** Accurately mimics an attacker or operator crafting evidence: generates `RUN_MANIFEST.jsonl` matching the global `run_records`, hashes the UTF-8 bytes to compute SHA-256, writes `COMPLETE.json` binding that hash with `files: len(files)` and `readback: "all_match"`.
   - **Coverage:** Exercises both arms (`arm="interrupted"` and `arm="crashed"`) across both execution modes (`check_only=True` and `check_only=False`) for 4 distinct sub-tests. Asserts return code `RC_CHECK_FAILED` (3), structured stderr `error: "run_not_complete"`, detail citing `"run_end"`, and `assertFalse(target.exists())`.
   - **RED-Arm Consistency:** On the slice-2 modules (`8d4056c5`), `LEAD_RED_ARM_slice2_restore_backup_new_tests.txt:83-110` records 3 failures for `test_hand_made_...` (interrupted check-only returned `0 != 3`, interrupted restore returned `0 != 3`, target was created `True is not false`). Arm 2 crashed run is stopped at line 106 because arm 1 failed first. This confirms the exact fail-open behavior identified in F-01.
2. **`test_partial_run_declaring_files_but_having_no_records_fails_closed`:**
   - The test was reworked to separate the F-01 gate from the "nothing to verify" fence.
   - It first confirms that forged evidence on the partial run fails at the new `run_end` gate (lines 212–220).
   - It then constructs a valid, tool-closed zero-file run (`empty_run`, `status: "ok"`, `files: 0`, `errors: []`), which successfully passes `verify_completion_evidence`, allowing execution to reach line 221 of `restore.py`. It proves that `run_restore` rejects a zero-file run with `"nothing to verify"` on stderr and returns exit code 3.
   - In the RED run, this test accounted for the 1 error (`JSONDecodeError` at lines 65–80) because the old slice-2 code did not emit the expected `run_end is status='partial'` JSON error to stderr on the forged partial run.

---

## (c) Analysis of F-02, F-03, Adapter Checker, Scope, and Report Honesty

### F-02: Completion Evidence Ordering and Crash Safety
- **Order of Execution:** In `backup.run_backup` (`backup_d81b07f6.py:220-232`), `write_completion_evidence` executes *before* `append_jsonl(manifest_path, {"record": "run_end", ...})`.
- **Failure Handling:** If `write_completion_evidence` returns anything other than `"written"`, line 226 appends `f"completion evidence not written: {completion}"` to `errors`. Line 227 sets `status = "partial"`, which is logged in the `run_end` record along with the error description.
- **Dry-Run Integrity:** Dry-run bypasses both `write_completion_evidence` and `run_end` logging (`if not dry_run:` at line 216 and line 228); zero files and zero manifest lines are written.
- **Record Shapes & CLI:** The payload for `run_end` retains identical fields (`record`, `run_id`, `finished_at`, `files`, `bytes`, `errors`, `status`). CLI flags (`--config`, `--dry-run`, `--store`) are untouched.
- **Crash Between Evidence Write and `run_end`:** Leaves `COMPLETE.json` and `RUN_MANIFEST.jsonl` on disk, but no `run_end` record in `manifest.jsonl`. Under the F-01 rule in `restore.verify_completion_evidence` (`restore_d81b07f6.py:71-72`), `len(ends) == 0 != 1`, raising `RunNotComplete`. Restore exits `RC_CHECK_FAILED` (3) and writes nothing.

### F-03: Single Gate Integrity
- **Docstring Accuracy:** The docstring for `load_complete_marker` (`opsa_common_d81b07f6.py:193-199`) accurately states that it performs pair-integrity validation only.
- **Single Gate Enforcement:** All restore paths—including the P0-30 adapter (`p030_closed_partition_backup_adapter.py:737-738, 767-768`)—invoke `restore.run_restore`, which funnels through `restore.verify_completion_evidence`. Consolidating file count checks, readback validation, and global manifest cross-checks in `verify_completion_evidence` eliminates dual-maintenance divergence while ensuring complete fail-closed protection.

### Adapter Checker Change
- In `check_p030_closed_partition_backup_adapter.py:1376-1387`, `test_partial_run_that_p026_check_only_accepts_never_reaches_restore` was updated from asserting `subject.RC_OK` to `subject.restore.RC_CHECK_FAILED`.
- This is the expected and necessary consequence of closing F-01: the partial run lacks a successful `run_end`, so the bare check-only fails closed. The adapter's own envelope fence (`_complete_p026_run`) continues to be asserted directly below.

### Scope and Ceiling Verification
- **Files Modified:** Exactly 5 files modified between `8d4056c5` and `d81b07f6` (`backup.py`, `opsa_common.py`, `restore.py`, `test_opsa.py`, `check_p030_closed_partition_backup_adapter.py`). Cumulative delta from `fcac0ac6` touches exactly 6 files (including `p030_closed_partition_backup_adapter.py` modified in Slice 2), matching the ceiling granted by `OD-20260915-P026-REPAIR-LEAD-1` and `OD-20260915-P026-ADAPTER-LEAD-1`.
- **Zero Added Files:** No files created.
- **Zero Banned Primitives:** No deletion, renaming, or unlinking primitives (`os.remove`, `unlink`, `rmdir`, `rmtree`, `truncate`) added.
- **Additive Only:** Global `manifest.jsonl` record schemas remain untouched.

### Report Honesty
- `LEAD_VERIFICATION_P026_REPAIR.md` claims:
  - `python -m unittest test_opsa`: 39 tests OK (was 38). Verified in `sources/LEAD_UNITTEST_312_slice3_TAIL.txt:35-37` (`Ran 39 tests in 2.161s ... OK`).
  - `check_p030_closed_partition_backup_adapter.py`: 45 tests OK, exit 0. Verified in `sources/check_p030_closed_partition_backup_adapter_slice3_TAIL.txt` and `subject/COMMIT_d81b07f6.txt:31`.
  - RED arm on slice-2 modules: 3 failures, 1 error. Verified in `sources/LEAD_RED_ARM_slice2_restore_backup_new_tests.txt:114` (`FAILED (failures=3, errors=1)`).
- All numbers match the raw log files exactly.

---

## (d) Exact Read Coverage with Ranges and Continuations

All reads were conducted strictly inside `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_DELTA_20260915` using the native read tool, observing the $\le 150$ lines per view limit:

1. `PACKET_SHA256SUMS.txt`: lines 1–18 (complete)
2. `subject/DELTA_fcac0ac6_d81b07f6_STAT.txt`: lines 1–8 (complete)
3. `subject/COMMIT_d81b07f6.txt`: lines 1–37 (complete)
4. `subject/DELTA_8d4056c5_d81b07f6.diff`: lines 1–150, 151–266 (complete across 2 views; 266 lines total)
5. `subject/restore_d81b07f6.py`: lines 1–150, 151–300, 301–311 (complete across 3 views; 311 lines total)
6. `subject/backup_d81b07f6.py`: lines 1–150, 151–299 (complete across 2 views; 299 lines total)
7. `subject/opsa_common_d81b07f6.py`: lines 1–150, 151–300, 301–328 (complete across 3 views; 328 lines total)
8. `sources/GEMINI_DETECTION_REPORT_8d4056c5.md`: lines 1–150, 151–221 (complete across 2 views; 221 lines total)
9. `sources/LEAD_ADJUDICATION_of_the_detection_report.md`: lines 1–20 (complete)
10. `sources/LEAD_VERIFICATION_P026_REPAIR.md`: lines 1–94 (complete)
11. `sources/LEAD_RED_ARM_slice2_restore_backup_new_tests.txt`: lines 1–138 (complete)
12. `sources/LEAD_UNITTEST_312_slice3_TAIL.txt`: lines 1–62 (complete)
13. `sources/check_p030_closed_partition_backup_adapter_slice3_TAIL.txt`: lines 1–14 (complete)
14. `sources/DECISIONS_rows_P026.md`: lines 1–3 (complete)
15. `sources/LEAD_RUFF_slice3.txt`: lines 1–2 (complete)
16. `sources/LEAD_GUARD_slice3.txt`: lines 1–18 (complete)
17. `sources/SHA256SUMS_d81b07f6_slice3.txt`: lines 1–6 (complete)
18. `sources/SHA256SUMS_8d4056c5_adapter_slice.txt`: lines 1–5 (complete)

---

## (e) Nonempty NOT VERIFIED

- **No live execution:** Per operating mode `SUPPLEMENTAL_UNEXECUTED`, no shell commands, tests, or subagents were run. Test execution counts, failures, and exit codes are verified from logs and source bytes provided in the packet.
- **External repository code:** Any files outside `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_DELTA_20260915` (including `AGENTS.md` and live git trees) were strictly unread and not opened.
- **Hardware & Host Infrastructure:** Live file locks, real POSIX/Windows filesystem race conditions during crash scenarios, and multi-process concurency were analyzed by inspection rather than hardware execution.

---

## (f) Machine-Readable Verdict

```json
{
  "part": "P026_DELTA_GEMINI",
  "verdict": "PASS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "closed": [
    "F-01",
    "F-02",
    "F-03"
  ],
  "not_refused": [],
  "findings": [],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
