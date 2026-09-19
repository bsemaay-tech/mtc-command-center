# Supplemental Read-Only Detection Review: WP-P0-26 OPS-A NIT Slice (`505af399`)

**Reviewer:** `gemini-3.8-flash-high` (SUPPLEMENTAL_UNEXECUTED; read-only detection pass)  
**Subject:** Commit `505af399` on top of `e114ed31` (+46/-6 across exactly 5 files)  
**Packet Root:** `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_NIT_20260918`  
**Verdict:** **PASS** (0 REQUIRED, 0 NIT)

---

## (a) Traces and Adversarial Analysis

### 1. Gate Execution Order and Refusal Tracing on HEAD (`restore.py:72-124`)
In [`verify_completion_evidence`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_NIT_20260918/subject/restore.py_HEAD_complete.py#L72-L124), validation proceeds in strict serial order:
1. `load_complete_marker`: validates pair file existence, valid JSON, schema, run ID matching, and streaming SHA-256 digest binding (`run_manifest_sha256 == sha256(RUN_MANIFEST.jsonl)`).
2. Global manifest `run_end` count and status: exactly one `run_end` for `run_id`, requiring `status == "ok"` and `errors == []`.
3. Per-run manifest syntax and header: checks for `_malformed` records and `record == "run_manifest_header"`.
4. Global vs per-run file record equivalence: sorted `(store_id, rel, sha256, size)` match.
5. Declared file count: `marker["files"]` is a non-bool integer matching `len(per_run_files)`.
6. Global `run_end` file count match: `end["files"] == declared`.
7. Per-run file readback: all `file` records have `readback == "match"`.
8. **Marker self-claims (NIT-1, lines 118–123):**
   - `marker.get("readback") == "all_match"`
   - `marker.get("run_manifest") == RUN_MANIFEST_NAME`

#### Tracing Specified Cases:
- **Case (i) — Hand-made marker lacking both fields on a run whose global `run_end` is partial:**
  - Step 1 (`load_complete_marker`) passes if internal pair hash matches.
  - Step 2 fires first at line 86 (`if end.get("status") != "ok" or end.get("errors") != []:`).
  - **Fires first:** `RunNotComplete("run <id>: global manifest run_end is status='partial' with ... error(s); only a run the backup tool closed successfully may be restored")`. The missing marker self-claims are never evaluated, preserving the F-01 fence precedence.
- **Case (ii) — Hand-made marker lacking both fields on a successful run (`run_end` ok):**
  - Steps 1–7 pass.
  - Step 8 line 118 evaluates `None != "all_match"` (True).
  - **Fires first:** `RunNotComplete("run <id>: completion marker declares readback=None; the backup tool writes 'all_match'")`.
- **Case (iii) — Marker with `readback: "all_match"` but `run_manifest: "RUN_MANIFEST.jsonl "` (trailing space):**
  - Line 118 passes (`"all_match" == "all_match"`).
  - Line 121 evaluates `"RUN_MANIFEST.jsonl " != "RUN_MANIFEST.jsonl"` (True).
  - **Fires:** `RunNotComplete("run <id>: completion marker names run_manifest='RUN_MANIFEST.jsonl '; expected 'RUN_MANIFEST.jsonl'")`.
- **Case (iv) — `readback` present but `True` (bool):**
  - In Python, `True != "all_match"` evaluates to `True` without error.
  - Line 118 fires: `RunNotComplete("run <id>: completion marker declares readback=True; the backup tool writes 'all_match'")`.
- **Marker declares `readback: "all_match"` but per-run manifest file records carry `readback: "mismatch"`:**
  - Step 7 (lines 111–112) precedes Step 8.
  - **Fires first:** `RunNotComplete("run <id>: per-run manifest carries a non-matching readback record")`.
- **Marker with extra unknown fields:**
  - The dictionary payload is parsed via standard `json.loads`. Unchecked extraneous fields do not fail validation; they are ignored, matching standard JSON object behavior in OPS-A.

### 2. Test Suite Arm Traces
- **Tampered-marker test (`test_tampered_marker_or_run_manifest_is_refused`, lines 384–395):**
  - Sub-arm `payload["readback"] = "partial"`: fails line 118, raising `RunNotComplete("... declares readback='partial'...")`. Tested via `refused("declares readback='partial'")`.
  - Sub-arm `payload["run_manifest"] = "OTHER.jsonl"`: fails line 121, raising `RunNotComplete("... names run_manifest='OTHER.jsonl'...")`. Tested via `refused("names run_manifest='OTHER.jsonl'")`.
  - Restoring marker: line 395 immediately rewrites `good_marker` to disk, preventing subsequent test corruption before sub-arm (e) checks bit-rot detection.
- **Partial-run forged helper (`test_partial_run_declaring_files_but_having_no_records_fails_closed`, lines 450–464):**
  - Why it needs both fields: with NIT-1 active, any forged marker lacking `"readback": "all_match"` and `"run_manifest": "RUN_MANIFEST.jsonl"` is stopped at Step 8 with `rc 3` `run_not_complete`. Supplying both fields permits the second test arm (empty run with `files: 0`, `status: "ok"`) to pass the completion gate and exercise the older "nothing to verify" fence behind the gate (lines 233–243), confirming it still prints `ERROR run ... has nothing to verify: selected zero file records` and returns `RC_CHECK_FAILED`.

### 3. Constant and Bypass Audits
- **`RUN_MANIFEST_NAME`:** Imported into [`restore.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_NIT_20260918/subject/restore.py_HEAD_complete.py#L41) directly from [`opsa_common.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_NIT_20260918/sources/opsa_common_HEAD.py#L46), where it is defined as `"RUN_MANIFEST.jsonl"`. In [`backup.py:253,274`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_NIT_20260918/subject/backup.py_HEAD_complete.py#L253), `manifest = run_manifest_path(run_dir)` uses `RUN_MANIFEST_NAME`, and `payload["run_manifest"] = manifest.name` writes identical bytes.
- **Restore bypass sweep:** Module-wide audit of [`restore.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_NIT_20260918/subject/restore.py_HEAD_complete.py) confirms that all entry points (`--to` and `--check-only` inside `run_restore`) call `verify_completion_evidence` at lines 200–206 before any file hashing or destination writing occurs. The P0-30 adapter also invokes `run_restore`. No bypass exists.

---

## (b) NIT-5 and Documentation Honesty Audits

### 1. NIT-5 Dead Condition Removal ([`backup.py:237`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_NIT_20260918/subject/backup.py_HEAD_complete.py#L237))
- In `backup.py` line 227, `status` is assigned: `status = "ok" if not errors else "partial"`.
- Therefore, `status == "ok"` is logically identical to `not errors`.
- In the return statement at line 237, `return RC_OK if not errors else RC_ERROR` removes the redundant condition `and status == "ok"`.
- Lines 228–232 prove that the global manifest `run_end` record still explicitly serializes `"status": status`. It is not omitted or changed.

### 2. Documentation Honesty and Scope
- **[`README.md:63-66`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_NIT_20260918/subject/README.md_HEAD_complete.md#L63-L66) (NIT-2 / `OD-20260918-P026-N2-DOC-1`):**
  - Accurately documents that `write_once_bytes` utilizes `O_EXCL` rather than atomic publication.
  - Correctly notes that the package has no delete primitive (tested by `NoDeleteGuaranteeTests`).
  - "is re-backed-up under a NEW run id": accurately describes the operational behavior of the backup tool (every invocation generates a fresh millisecond UTC run ID; there is no in-place overwrite or repair of existing runs). It does not claim an automated retry service exists. Fully honest.
- **[`RESTORE_DRILL_EVIDENCE.md:22-29`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P026_NIT_20260918/subject/RESTORE_DRILL_EVIDENCE.md_HEAD_complete.md#L22-L29) (NIT-4):**
  - Dated note accurately states the contract changes on this branch (`--latest` removed; exit code 2 on `--latest`; current-tool `COMPLETE.json` required).
  - Explains why the 2026-08-24 drill commands exit 2/3 and instructs how to reproduce. Preserves original transcripts without historical revisionism.
- **Record Verification:**
  - `LEAD_RED_P026_NIT1a_readback_claim_unchecked.txt`: confirmed 1 failure (`refused("declares readback='partial'")` -> `0 != 3`).
  - `LEAD_RED_P026_NIT1b_run_manifest_claim_unchecked.txt`: confirmed 1 failure (`refused("names run_manifest='OTHER.jsonl'")` -> `0 != 3`).
  - `LEAD_GREEN_test_opsa.txt`: 39 tests passed cleanly (`Ran 39 tests in 1.244s ... OK`).
  - `LEAD_GUARD_P026_NIT.txt`: clean repo guard (`RESULT: PASS`, staged = 5, dirty = 5).
  - Ruff findings per file identical to candidate HEAD (restore: 2, backup: 4, test_opsa: 7).
- **Scope:** Diffstat and patch confirm changes are strictly confined to exactly 5 files (+46/-6).

---

## (c) Findings

**No findings (0 REQUIRED, 0 NIT).**  
All carried NITs in scope (NIT-1, NIT-2 doc, NIT-4 doc, NIT-5) are correctly and honestly implemented. NIT-3 is properly deferred to branch P0-30.

---

## (d) Exact Read Coverage

All views performed using native `view_file` on files within `_gemini_packets_20260913/P026_NIT_20260918` obeying the 150-line window limit:
1. `PACKET_SHA256SUMS.txt`: lines 1–18 (complete)
2. `subject/DIFF_STAT_e114ed31_505af399.txt`: lines 1–7 (complete)
3. `subject/DIFF_e114ed31_505af399.patch`: lines 1–122 (complete)
4. `subject/COMMIT_505af399.txt`: lines 1–45 (complete)
5. `subject/BLOB_OIDS_HEAD.txt`: lines 1–6 (complete)
6. `subject/restore.py_HEAD_complete.py`: lines 1–150; continuation lines 151–300; continuation lines 301–323 (all 323 lines, complete)
7. `subject/backup.py_HEAD_complete.py`: lines 200–299 (covers lines 200–300 through EOF, complete)
8. `subject/test_opsa.py_HEAD_complete.py`: lines 330–420; lines 440–520 (tampered-marker & partial-run tests, complete)
9. `subject/README.md_HEAD_complete.md`: lines 50–75 (complete)
10. `subject/RESTORE_DRILL_EVIDENCE.md_HEAD_complete.md`: lines 1–40 (complete)
11. `sources/opsa_common_HEAD.py`: lines 30–60; lines 61–180; lines 181–280 (`load_complete_marker`, complete)
12. `sources/LEAD_ADJUDICATION_P026_T0.md`: lines 1–27 (complete)
13. `sources/LEAD_GREEN_test_opsa.txt`: lines 1–91 (complete)
14. `sources/LEAD_GUARD_P026_NIT.txt`: lines 1–23 (complete)
15. `sources/LEAD_RED_P026_BASELINE.txt`: lines 1–67 (complete)
16. `sources/LEAD_RED_P026_NIT1a_readback_claim_unchecked.txt`: lines 1–80 (complete)
17. `sources/LEAD_RED_P026_NIT1b_run_manifest_claim_unchecked.txt`: lines 1–80 (complete)
18. `sources/OPUS_T0_REPORT_e114ed31.md`: lines 1–150; lines 151–250; lines 251–400; lines 401–481 (all 481 lines, complete)

---

## (e) Nonempty NOT VERIFIED

1. **Live process execution / hardware fault injection:** Unexecuted environment per reviewer constraints; simulation arms in `test_opsa.py` and Lead records were verified analytically.
2. **Pre-existing master defects outside scope:** NIT-3 behavior under non-ASCII temporary directory paths was verified as fixed on the P0-30 branch and remained untouched here as instructed.
3. **Third-party tooling versions:** The specific runtime performance of ruff 0.16.4 was not re-executed directly.

---

```json
{
  "part": "P026_NIT_GEMINI",
  "verdict": "PASS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "nit1": "CLOSED",
  "nit2_doc": "HONEST",
  "nit4_doc": "HONEST",
  "nit5": "CLOSED",
  "findings": [],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
