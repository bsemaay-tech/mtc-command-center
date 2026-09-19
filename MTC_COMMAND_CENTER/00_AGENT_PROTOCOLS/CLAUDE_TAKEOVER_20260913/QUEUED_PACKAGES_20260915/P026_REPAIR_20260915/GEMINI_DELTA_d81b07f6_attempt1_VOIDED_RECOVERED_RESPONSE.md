# SUPPLEMENTAL READ-ONLY DELTA REVIEW: WP-P0-26 SLICE 3 (`d81b07f6`)

**Reviewer:** Gemini 3.8 Flash (High) (Supplemental Read-Only Delta Reviewer; `SUPPLEMENTAL_UNEXECUTED`)  
**Packet Context:** `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_DELTA_20260915`  
**Candidate Commits:** `8d4056c5` → `d81b07f6` (Slice 3 repair by Claude Opus 5 Lead; disclosed; Lead does not accept own code)  
**Authorities:** `OD-20260915-P026-REPAIR-LEAD-1` ("A") & `OD-20260915-P026-ADAPTER-LEAD-1` ("A")

---

## (a) Finding-Closure Table (F-01, F-02, F-03)

| Finding ID | Prior Severity | Status | File & Line Citations | Analysis & Verification Against the Bytes |
|---|---|---|---|---|
| **F-01** | **REQUIRED** | **CLOSED** | [restore_d81b07f6.py](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_DELTA_20260915/subject/restore_d81b07f6.py#L71-L89), [:107-109](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_DELTA_20260915/subject/restore_d81b07f6.py#L107-L109);<br>[DELTA_8d4056c5_d81b07f6.diff](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_DELTA_20260915/subject/DELTA_8d4056c5_d81b07f6.diff#L68-L90), [:101-175](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_DELTA_20260915/subject/DELTA_8d4056c5_d81b07f6.diff#L101-L175) | `restore.verify_completion_evidence` now queries `global_records` for `record == "run_end"` and `run_id == run_id`. It enforces: (1) `len(ends) == 1`; (2) `end.get("status") == "ok"`; (3) `end.get("errors") == []`; and (4) `end.get("files") == declared`. A hand-made completion marker/manifest pair cannot revive a run without the backup tool's own successful terminal record. Refuses with `RunNotComplete` (exit `RC_CHECK_FAILED` = 3). Covered by new test `test_hand_made_completion_evidence_cannot_revive_a_run_the_tool_did_not_close`. |
| **F-02** | **NIT** | **CLOSED** | [backup_d81b07f6.py](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_DELTA_20260915/subject/backup_d81b07f6.py#L216-L233);<br>[DELTA_8d4056c5_d81b07f6.diff](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_DELTA_20260915/subject/DELTA_8d4056c5_d81b07f6.diff#L17-L33) | In `backup.run_backup`, `write_completion_evidence` executes *before* `run_end` is appended to `manifest.jsonl`. If writing evidence fails (`completion != "written"`), the failure reason is appended to `errors`, causing `status = "partial"`. The global log never writes `"status": "ok"` for a run that failed to write its completion marker/manifest. |
| **F-03** | **NIT** | **CLOSED** | [opsa_common_d81b07f6.py](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_DELTA_20260915/subject/opsa_common_d81b07f6.py#L193-L199);<br>[DELTA_8d4056c5_d81b07f6.diff](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_DELTA_20260915/subject/DELTA_8d4056c5_d81b07f6.diff#L45-L52) | `load_complete_marker` docstring explicitly clarifies that it performs only pair-integrity validation (`COMPLETE.json` schema, `run_id`, and `run_manifest_sha256` binding). Field-level checks (`files` non-bool int, `readback == "match"`, and `run_end` consistency) intentionally live in `restore.verify_completion_evidence`, which acts as the single authoritative gate through which all restore paths (including the P0-30 adapter) must pass. |

---

## (b) Variant Table for Attack Shape (e)

### 1. New Rule in `restore.verify_completion_evidence`
Quoted from [restore_d81b07f6.py](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_DELTA_20260915/subject/restore_d81b07f6.py#L79-L89) and [:107-109](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_DELTA_20260915/subject/restore_d81b07f6.py#L107-L109):
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

### 2. Mental Execution of Attack Shape (e) and Variants

| Attack Variant | Evaluation & Mechanics | Verdict | Refusing Line in `restore_d81b07f6.py` |
|---|---|---|---|
| **Arm 1: Interrupted run** (`run_end status: partial`, 1 error) | `ends` has 1 item. `end.get("status") == "partial" != "ok"` and `end.get("errors") != []`. Triggers line 75. | **REFUSED** | `restore.py:75-79` |
| **Arm 2: Crashed run** (no `run_end` in global manifest) | `ends` has 0 items. `len(ends) != 1` (0 != 1). Triggers line 71. | **REFUSED** | `restore.py:71-73` |
| **Variant 1: Two `run_end` records** for run (e.g. 1 ok, 1 partial) | `ends` has 2 items. `len(ends) != 1` (2 != 1). Triggers line 71. | **REFUSED** | `restore.py:71-73` |
| **Variant 2: `run_end ok` whose `files` differs from marker** | `ends` has 1 item, status ok, errors empty. At line 107, `end.get("files") != declared` evaluates to `True`. Triggers line 108. | **REFUSED** | `restore.py:107-109` |
| **Variant 3a: `run_end ok` with `errors` missing** (key absent) | `end.get("errors")` returns `None`. `None != []` evaluates to `True`. Triggers line 75. | **REFUSED** | `restore.py:75-79` |
| **Variant 3b: `run_end ok` with `errors: 0`** (integer, not empty list) | `end.get("errors")` returns `0`. `0 != []` evaluates to `True`. Triggers line 75. | **REFUSED** | `restore.py:75-79` |
| **Variant 4: `run_end` for another `run_id`** | Filter `r.get("run_id") == run_id` rejects records for other IDs; `len(ends)` is 0. Triggers line 71. | **REFUSED** | `restore.py:71-73` |
| **Variant 5: Global manifest with malformed line among records** | If a file line is malformed, `read_jsonl` creates `_malformed`, so `global_files` differs from `per_run_files`, triggering line 101-102 (`RunNotComplete`, rc 3). Any malformed line in the manifest populates `errors` at line 204, triggering `RC_ERROR` (1) at line 285. | **REFUSED** | `restore.py:101-102` (rc 3) / `restore.py:285` (rc 1) |

### 3. Evaluation of New & Reworked Test Fences
- **Attacker Forgery Fidelity:** `forge()` in [test_opsa.py:129-140](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_DELTA_20260915/subject/DELTA_8d4056c5_d81b07f6.diff#L129-L140) accurately models a sophisticated attacker: it writes valid JSONL headers, includes genuine run records matching the global manifest, computes the authentic SHA-256 digest of the per-run manifest bytes, and constructs `COMPLETE.json` binding to that SHA-256 with matching file counts and `readback: "all_match"`.
- **Coverage of Arms & Modes:** `assert_refused` iterates over `check_only in (True, False)` across both `interrupted` (arm 1) and `crashed` (arm 2) scenarios, asserting `rc == 3`, `report["error"] == "run_not_complete"`, `"run_end" in report["detail"]`, and `target.exists() == False`. All 4 combinations are tested.
- **Consistency of RED-Arm Evidence:** In `sources/LEAD_RED_ARM_slice2_restore_backup_new_tests.txt:83-114`, running the new test suite against `8d4056c5` produced **3 failures and 1 error**:
  - Failure 1 & 2: `test_hand_made_completion_evidence_...` (arm='interrupted', `check_only=True` and `False`) yielded `AssertionError: 0 != 3` (old restore returned success).
  - Failure 3: `self.assertFalse(target.exists())` yielded `AssertionError: True is not false` (old restore actually restored the files to disk).
  - Error 1: In `test_partial_run_declaring_files_but_having_no_records_fails_closed`, the test expected a structured JSON error on stderr from the gate; the old restore passed the gate and hit plain text `ERROR run ... has nothing to verify` on stderr, triggering a `JSONDecodeError`.  
  This matches the exact defect mechanism identified in F-01.
- **Reworked "Nothing to Verify" Fence:** Lines 221–243 of the diff synthesize a tool-closed zero-file run (`status: "ok"`, `files: 0`, `errors: []`) with a forged zero-file completion marker. This run cleanly passes the new `run_end` checks and proceeds directly to the `restore.py` "nothing to verify" branch, asserting rc 3 and `"nothing to verify"` in stderr. The fence remains active and independently verified.

---

## (c) Findings F-02, F-03, Adapter Checker, Scope, and Report Honesty

### 1. F-02 Confirmation (`backup.py`)
- In `backup_d81b07f6.py:221-232`, `write_completion_evidence` is called at line 221 before `append_jsonl(manifest_path, {"record": "run_end", ...})` at line 229.
- If `write_completion_evidence` fails (`completion != "written"`), lines 226–227 append the error message to `errors` and set `status = "partial"`. The subsequent `run_end` record durable on disk records `"status": "partial"`, `"errors": errors`.
- `--dry-run` bypasses all writes (`if not dry_run:` guards both evidence write and `run_end` append).
- Manifest record shapes (`run_start`, `file`, `dir`, `skipped`, `run_end`) and CLI flags (`--config`, `--dry-run`, `--store`) are unchanged.
- **Crash window analysis:** If a crash occurs after `write_completion_evidence` completes but before `append_jsonl` writes `run_end`, the run directory contains valid completion evidence, but `manifest.jsonl` lacks a `run_end` record. Under the repaired `restore.verify_completion_evidence` gate, `len(ends)` evaluates to 0, which raises `RunNotComplete` (refused with rc 3). Restore strictly fails closed.

### 2. F-03 Confirmation (`opsa_common.py`)
- The docstring at `opsa_common_d81b07f6.py:193-199` accurately documents that `load_complete_marker` is solely for pair integrity, while `restore.verify_completion_evidence` is the sole unified validation gate.
- The P0-30 adapter (`p030_closed_partition_backup_adapter.py`) executes `restore.run_restore` for both check-only and full restore, ensuring all restores pass through this unified gate.

### 3. Adapter Checker Change
- In `check_p030_closed_partition_backup_adapter.py:1384-1387`, `test_partial_run_that_p026_check_only_accepts_never_reaches_restore` formerly expected `subject.RC_OK` because bare check-only had the F-01 fail-open bug.
- With F-01 closed, bare check-only refuses the partial run with `subject.restore.RC_CHECK_FAILED` (3). The test update directly reflects this correction while preserving the adapter's own envelope assertion (`_complete_p026_run` raising `ValueError` before restore).

### 4. Scope Compliance
- The diff touches exactly 5 files (`backup.py`, `opsa_common.py`, `restore.py`, `test_opsa.py`, `check_p030_closed_partition_backup_adapter.py`), all within the authorized ceiling of `OD-20260915-P026-REPAIR-LEAD-1` and `OD-20260915-P026-ADAPTER-LEAD-1`.
- 0 files added.
- No destructive primitives (`os.remove`, `unlink`, `rmdir`, `truncate`, etc.) introduced.
- Global manifest record schemas remain strictly backwards compatible.

### 5. Report Honesty Audit
- Stated unit tests: `39 OK` in `LEAD_VERIFICATION_P026_REPAIR.md:82`. Matches `LEAD_UNITTEST_312_slice3_TAIL.txt:35-37` (`Ran 39 tests ... OK`).
- Stated adapter checker tests: `45 OK, exit 0` in `LEAD_VERIFICATION_P026_REPAIR.md:83`. Matches `check_p030_closed_partition_backup_adapter_slice3_TAIL.txt:1-12`.
- Stated RED arm count: `Ran 39 tests, FAILED (failures=3, errors=1)` in `LEAD_VERIFICATION_P026_REPAIR.md:87`. Matches `LEAD_RED_ARM_slice2_restore_backup_new_tests.txt:112-114` exactly.

---

## (d) Exact Read Coverage with Ranges and Continuations

All reads were conducted using native file viewing strictly within `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_DELTA_20260915`, keeping views to ≤ 150 lines:

1. `PACKET_SHA256SUMS.txt`: lines 1–18 (complete)
2. `subject/DELTA_fcac0ac6_d81b07f6_STAT.txt`: lines 1–8 (complete)
3. `subject/COMMIT_d81b07f6.txt`: lines 1–37 (complete)
4. `subject/DELTA_8d4056c5_d81b07f6.diff`: lines 1–266 (complete across 2 continuation views: 1–150, 151–266)
5. `subject/restore_d81b07f6.py`: lines 1–311 (complete across 3 continuation views: 1–150, 151–300, 301–311)
6. `subject/backup_d81b07f6.py`: lines 1–299 (complete across 2 continuation views: 1–150, 151–299)
7. `subject/opsa_common_d81b07f6.py`: lines 1–328 (complete across 3 continuation views: 1–150, 151–300, 301–328)
8. `sources/GEMINI_DETECTION_REPORT_8d4056c5.md`: lines 1–221 (complete across 2 continuation views: 1–150, 151–221)
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

- **Operating Mode:** Operating strictly in `SUPPLEMENTAL_UNEXECUTED` read-only mode, no commands, test suites, Python interpreters, subagents, or shell scripts were executed. All verifications derive from packet source code, diffs, and test output transcripts.
- **External and Parent Trees:** Zero files outside `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_DELTA_20260915` were opened (including `AGENTS.md` and repo-root files).
- **Live Infrastructure:** Live trading engines, remote Git refs, credentials, scheduled tasks, and remote hosts were not accessed.

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
