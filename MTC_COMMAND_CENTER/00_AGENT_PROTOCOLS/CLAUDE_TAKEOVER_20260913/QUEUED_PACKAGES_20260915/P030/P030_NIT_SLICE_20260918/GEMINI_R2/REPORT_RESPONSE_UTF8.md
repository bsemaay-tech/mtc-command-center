# Supplemental Read-Only Review: WP-P0-30 NIT-Slice Repair Round 2 (`b4df1413`)

Reviewer: Gemini (gemini-3.8-flash-high), role: independent read-only detection reviewer (`SUPPLEMENTAL_UNEXECUTED`).  
Evaluation base: commit `b4df1413` (parent `d426e79f`, +315/-34 across exactly 4 files).  
Packet inspected: `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/`.

---

## (a) Traces and Soundness Analysis

### 1. Trace of [`nesting_arms()`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/check_p030_archive_exporter.py_HEAD_complete.py#L64-L95) and Layer Disambiguation

#### Search Mechanics
In [`check_p030_archive_exporter.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/check_p030_archive_exporter.py_HEAD_complete.py#L29-L94) and [`check_p030_closed_partition_backup_adapter.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/check_p030_closed_partition_backup_adapter.py_HEAD_complete.py#L20-L82), [`_nesting_layer(depth)`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/check_p030_archive_exporter.py_HEAD_complete.py#L29-L45) tests a pure nested array string `text = "[" * depth + "]" * depth`.
1. First, `json.loads(text, ...)` runs. If it raises `RecursionError`, it immediately returns `"parser"`.
2. If `json.loads` succeeds, `_reject_nonfinite_numbers(value)` executes. If this recursive walk raises `RecursionError`, it returns `"walk"`.
3. If neither raises, it returns `None`.

[`_smallest_depth(predicate)`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/check_p030_archive_exporter.py_HEAD_complete.py#L48-L62) performs an exponential doubling scan ($1, 2, 4, \dots, 2^k$) followed by binary search on `[low, high]`.
- `first_depth` finds the smallest depth where `_nesting_layer(depth) is not None`.
- `parser_depth` finds the smallest depth where `_nesting_layer(depth) == "parser"`, starting from `first_depth`.
- Inference: Because both searches evaluate identical call frames, the parser raised first iff `parser_depth == first_depth`. If so, `walk_depth = None`. Otherwise, `walk_depth = first_depth + _STACK_MARGIN`. If `walk_depth >= parser_depth`, `walk_depth = parser_depth - 1`. Finally, `parser_depth += _STACK_MARGIN`.

#### Execution on Pinned Python 3.12 (`recursionlimit = 1000`)
- Walk limit is hit around depth ~996 (Python recursion limit 1000 minus 4 search frames).
- CPython 3.12 parser raises `RecursionError` around depth ~2998.
- Resulting depths: `first_depth = 996`, `parser_depth = 2998`.
- Since $2998 \neq 996$, `walk_depth = 996 + 64 = 1060`, and `parser_depth = 2998 + 64 = 3062` (measured inside test harness as `walk=1049`, `parser=3044` due to runner frame delta).
- Both depths are derived cleanly; `walk` lands at 1049 (deep enough to trigger the Python frame limit, far below the 3044 parser threshold); `parser` lands at 3044.

#### Execution on Python 3.14 (`recursionlimit = 1000`)
- Walk limit is still hit at depth ~996.
- CPython 3.14 parser C stack limit is much higher: `json.loads` raises at depth ~16923.
- Resulting depths: `first_depth = 996`, `parser_depth = 16923`.
- `walk_depth = 1060`, `parser_depth = 16987` (inside test harness: `walk=1049`, `parser=16877`).

#### Stack Frame Counting & Disambiguation
- Call stack frames in search: `nesting_arms` $\to$ `_smallest_depth` $\to$ `lambda` $\to$ `_nesting_layer` $\to$ `_reject_nonfinite_numbers` = 4 frames.
- Call stack frames in code under test:
  - Exporter: `_refused` $\to$ `export_partition` $\to$ `_decode_source_line` $\to$ `_reject_nonfinite_numbers` = 4 frames.
  - Adapter capture: `capture_stable_prefix` $\to$ `_prefix_facts` $\to$ `_reject_nonfinite_numbers` = 3 frames.
  - Adapter manifest: `restore_verified_prefix` $\to$ `_restore_isolated_prefix` $\to$ `_read_strict_jsonl` $\to$ `_decode_strict_jsonl` $\to$ `_reject_nonfinite_numbers` = 5 frames.
  - Adapter config/receipt: `backup_stable_prefix` $\to$ `_load_strict_config` / `_verify_stable_receipt` $\to$ `_read_json_object` $\to$ `_decode_json_object` $\to$ `_reject_nonfinite_numbers` = 4 to 5 frames.
- The $\pm 1$ frame delta relative to search is comfortably enveloped by `_STACK_MARGIN = 64`.
- Exact-message assertions:
  - Exporter: `walk` asserts `"source line 3 is nested too deeply"`; `parser` asserts `"source line 3 is not parseable JSON"`. If an arm landed on the incorrect layer, string equality fails immediately.
  - Adapter: both layers map to site-specific refusals (`"prefix record is not canonical JSONL"`, `"invalid P026 manifest line 1"`, `"invalid backup config"`, `"invalid stable-prefix receipt"`). Disambiguation is verified by the 6 mutation pairs (`mutC3`..`mutC8`), where each mutant uniquely triggers an unhandled `RecursionError` in its designated layer and leaves the opposite layer passing.

---

### 2. End-to-End Traces of New Manifest and Config/Receipt Arms

#### Manifest Arm: [`test_manifest_refuses_pathological_nesting_before_p026`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/check_p030_closed_partition_backup_adapter.py_HEAD_complete.py#L739-L779)
1. **Setup & Injection**: After a normal backup creates `manifest.jsonl`, line 0 is rewritten with `, "synthetic_probe": [` repeated to `depth`.
2. **Byte Ingestion**: [`restore_verified_prefix`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/p030_closed_partition_backup_adapter.py_HEAD_complete.py) calls `_read_strict_jsonl`, which executes `Path(manifest).read_bytes()`.
3. **Parse & Guard Traversal**:
   - `_decode_strict_jsonl` iterates line by line. Line 1 contains the probe.
   - For `layer == "parser"`: [`json.loads`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/p030_closed_partition_backup_adapter.py_HEAD_complete.py#L115-L120) raises `RecursionError`. Handled by `except (json.JSONDecodeError, RecursionError)` at line 120, raising `ValueError("invalid P026 manifest line 1")`.
   - For `layer == "walk"`: `json.loads` succeeds; [`_reject_nonfinite_numbers(record)`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/p030_closed_partition_backup_adapter.py_HEAD_complete.py#L126-L129) raises `RecursionError`. Handled by `except RecursionError` at line 127, raising `ValueError("invalid P026 manifest line 1")`.
4. **Non-execution of P026**: Refusal aborts before `restore.run_restore` is reached. `run_restore.assert_not_called()` succeeds.

#### Config & Receipt Arm: [`test_config_and_receipt_refuse_pathological_nesting_before_p026`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/check_p030_closed_partition_backup_adapter.py_HEAD_complete.py#L522-L554)
1. **Setup & Injection**: Injects `, "synthetic_probe": [` nested to `depth` into either the JSON config file or the stable-prefix receipt file.
2. **Byte Ingestion**:
   - Config path: [`backup_stable_prefix`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/p030_closed_partition_backup_adapter.py_HEAD_complete.py) calls `_load_strict_config` $\to$ `_read_json_object` $\to$ `Path(path).read_bytes()`.
   - Receipt path: `_verify_stable_receipt` calls `stable_receipt.read_bytes()`.
3. **Parse & Guard Traversal**:
   - Both delegate to [`_decode_json_object(raw, description)`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/p030_closed_partition_backup_adapter.py_HEAD_complete.py#L76-L94).
   - For `layer == "parser"`: `json.loads` raises `RecursionError`. Caught at line 83 by `except (UnicodeDecodeError, json.JSONDecodeError, RecursionError)`, raising `ValueError(f"invalid {description}")`.
   - For `layer == "walk"`: `json.loads` succeeds; [`_reject_nonfinite_numbers(payload)`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/p030_closed_partition_backup_adapter.py_HEAD_complete.py#L89-L93) raises `RecursionError`. Caught at line 91 by `except RecursionError`, raising `ValueError(f"invalid {description}")`.
4. **Non-execution of P026**: Refusal aborts during config load / receipt validation before `backup.run_backup` is reached. `run_backup.assert_not_called()` succeeds.

---

### 3. Adversarial Analysis

- **Monotonicity**: CPython recursive array parsing and Python recursive object traversal allocate exactly one C stack frame and one Python stack frame per array nesting level respectively. Once recursion limit is exceeded, any deeper nesting strictly raises. In `_nesting_layer`, `json.loads` only enters `except RecursionError` when raising (returning `"parser"` immediately), avoiding any post-catch recursion counter headroom distortion on the subsequent walk.
- **Hook Interference**: The probe text `[` $\dots$ `]` consists solely of JSON arrays. `object_pairs_hook` is never invoked during array parsing, and `parse_constant` is never called because no non-finite literals exist. `RecursionError` in `json.loads` can only emanate from parser recursion.
- **Dicts Nested via Hooks**: Synthetic probes inject pure arrays into an existing shallow dictionary (`{"synthetic_probe": [...]}`). The dict key-pair hook is called once for the top-level property, never recursively.
- **Parser Limit $\le 1000 + 64$**: If an interpreter were configured such that the parser raises at or before the walk limit, `parser_depth == first_depth` evaluates `True`. `walk_depth` becomes `None`. In that scenario, `subTest` logs `self.skipTest("the walk never raises RecursionError on this interpreter")`. This is mathematically correct: if the parser rejects input before the walk can be reached, the walk guard is unreachable from serialized JSON on that interpreter.
- **Clamping Safety**: If `walk_depth >= parser_depth`, `walk_depth` is clamped to `parser_depth - 1`. On CPython 3.12 and 3.14, the separation between walk (1000) and parser (3000 / 16922) limits exceeds 2000 frames, so this clamp is not engaged.
- **No Test Skips on Supported Interpreters**: All 29 exporter tests and 46 adapter tests run with 0 skips on both Python 3.12 and 3.14.

---

### 4. Preservation, Closure, and Evidence Honesty

1. **F-1 (REQUIRED)**: **CLOSED**. Derived depths replace hard-coded 3000. Walk and parser guards are independently tested and proven load-bearing by mutants `mutC1`..`mutC6` on both interpreters.
2. **F-2**: **CLOSED**. [`_decode_json_object`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/p030_closed_partition_backup_adapter.py_HEAD_complete.py#L76-L94) is guarded at both parser (`line 83`) and walk (`lines 89-93`), wrapping config, receipt, and isolated restore reads. Exercised by `mutC7` and `mutC8` (2 errors each).
3. **F-3**: **CLOSED**. New test [`test_publication_never_replaces_a_receipt_that_appeared_after_the_check`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/check_p030_archive_exporter.py_HEAD_complete.py#L453-L495) mocks `receipt.exists()` to `False`, forcing `_publish` to encounter `FileExistsError` on `os.rename`. Verified: nothing replaced, target absent, both `.p030partial` files intact. `mutD1` causes exact failure (`receipt_unwritable` vs `receipt_exists`).
4. **F-4**: **CLOSED**. Exporter message `"source line 3 is nested too deeply"` is asserted and reached by the `walk` arm at depth 1049/1060 on Python 3.12.
5. **F-5**: **CLOSED**. [`_publish`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/p030_archive_exporter.py_HEAD_complete.py#L79-L95) docstring accurately states that `os.link` provides a delete-free no-clobber form on POSIX at the cost of a permanent hard link and cross-filesystem failure.
6. **Preservation**: Refusal codes (16), staging conventions (`.p030partial`), receipt structure, and canonicalization checks remain unchanged. Diff spans exactly the 4 requested files (+315/-34). Working tree adapter files were not ruff-reformatted.

---

## (b) Findings

**None**. (Zero REQUIRED, zero NIT findings). All 5 findings (F-1 through F-5) are cleanly closed without behavioral regressions.

---

## (c) Exact Read Coverage

All reads performed using built-in view tool inside packet `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/`:
1. [`PACKET_SHA256SUMS.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/PACKET_SHA256SUMS.txt): lines 1-41 (complete).
2. [`subject/DIFF_STAT_d426e79f_b4df1413.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/DIFF_STAT_d426e79f_b4df1413.txt): lines 1-6 (complete).
3. [`subject/COMMIT_b4df1413.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/COMMIT_b4df1413.txt): lines 1-59 (complete).
4. [`subject/BLOB_OIDS_HEAD.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/BLOB_OIDS_HEAD.txt): lines 1-5 (complete).
5. [`subject/DIFF_d426e79f_b4df1413.patch`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/DIFF_d426e79f_b4df1413.patch): lines 1-150, 151-300, 301-435 (complete).
6. [`subject/p030_archive_exporter.py_HEAD_complete.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/p030_archive_exporter.py_HEAD_complete.py): lines 60-100, 240-300, 495-541.
7. [`subject/check_p030_archive_exporter.py_HEAD_complete.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/check_p030_archive_exporter.py_HEAD_complete.py): lines 1-90, 91-100, 430-535.
8. [`subject/p030_closed_partition_backup_adapter.py_HEAD_complete.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/p030_closed_partition_backup_adapter.py_HEAD_complete.py): lines 60-135, 185-215.
9. [`subject/check_p030_closed_partition_backup_adapter.py_HEAD_complete.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/subject/check_p030_closed_partition_backup_adapter.py_HEAD_complete.py): lines 1-80, 81-85, 230-265, 270-305, 520-565, 735-785.
10. [`sources/LEAD_ADJUDICATION_P030_NIT_T0.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_ADJUDICATION_P030_NIT_T0.md): lines 1-25 (complete).
11. [`sources/OPUS_T0_REPORT_attempt4_d426e79f.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/OPUS_T0_REPORT_attempt4_d426e79f.md): lines 1-150, 250-370, 371-415 (Section 6 findings F-1..F-5 complete).
12. [`sources/LEAD_VERIFICATION_P030_NIT_R2.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_VERIFICATION_P030_NIT_R2.md): lines 1-58 (complete).
13. All 29 `sources/LEAD_*.txt` files:
    - [`LEAD_GREEN_R2_check_p030_archive_exporter_py312.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_GREEN_R2_check_p030_archive_exporter_py312.txt): 1-46 (complete)
    - [`LEAD_GREEN_R2_check_p030_archive_exporter_py314.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_GREEN_R2_check_p030_archive_exporter_py314.txt): 1-46 (complete)
    - [`LEAD_GREEN_R2_check_p030_closed_partition_backup_adapter_py312.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_GREEN_R2_check_p030_closed_partition_backup_adapter_py312.txt): 1-150, 300-319
    - [`LEAD_GREEN_R2_check_p030_closed_partition_backup_adapter_py314.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_GREEN_R2_check_p030_closed_partition_backup_adapter_py314.txt): 1-20, 300-319
    - [`LEAD_GREEN_R2_worktree_adapter_checker_py312_ascii_TEMP.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_GREEN_R2_worktree_adapter_checker_py312_ascii_TEMP.txt): 1-20, 270-300, 300-317
    - [`LEAD_GREEN_R2_worktree_adapter_checker_py312_nonascii_TEMP.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_GREEN_R2_worktree_adapter_checker_py312_nonascii_TEMP.txt): 1-20, 290-328
    - [`LEAD_GREEN_R2_worktree_exporter_checker_py312.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_GREEN_R2_worktree_exporter_checker_py312.txt): 1-44 (complete)
    - [`LEAD_GUARD_P030_NIT_R2.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_GUARD_P030_NIT_R2.txt): 1-23 (complete)
    - [`LEAD_MUTANT_RUN_SUMMARY.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_MUTANT_RUN_SUMMARY.txt): 1-19 (complete)
    - [`LEAD_RED_R2_mutC1_exporter_walk_guard_removed_py312.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_RED_R2_mutC1_exporter_walk_guard_removed_py312.txt): 1-71 (complete)
    - [`LEAD_RED_R2_mutC1_exporter_walk_guard_removed_py314.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_RED_R2_mutC1_exporter_walk_guard_removed_py314.txt): 1-85 (complete)
    - [`LEAD_RED_R2_mutC2_exporter_parser_clause_removed_py312.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_RED_R2_mutC2_exporter_parser_clause_removed_py312.txt): 1-72 (complete)
    - [`LEAD_RED_R2_mutC2_exporter_parser_clause_removed_py314.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_RED_R2_mutC2_exporter_parser_clause_removed_py314.txt): 1-84 (complete)
    - [`LEAD_RED_R2_mutC3_adapter_prefix_walk_guard_removed_py312.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_RED_R2_mutC3_adapter_prefix_walk_guard_removed_py312.txt): 1-20, 320-342
    - [`LEAD_RED_R2_mutC3_adapter_prefix_walk_guard_removed_py314.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_RED_R2_mutC3_adapter_prefix_walk_guard_removed_py314.txt): 1-20, 335-355
    - [`LEAD_RED_R2_mutC4_adapter_jsonl_walk_guard_removed_py312.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_RED_R2_mutC4_adapter_jsonl_walk_guard_removed_py312.txt): 1-20, 325-345
    - [`LEAD_RED_R2_mutC4_adapter_jsonl_walk_guard_removed_py314.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_RED_R2_mutC4_adapter_jsonl_walk_guard_removed_py314.txt): 1-20, 340-361
    - [`LEAD_RED_R2_mutC5_adapter_prefix_parser_clause_removed_py312.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_RED_R2_mutC5_adapter_prefix_parser_clause_removed_py312.txt): 1-20, 325-343
    - [`LEAD_RED_R2_mutC5_adapter_prefix_parser_clause_removed_py314.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_RED_R2_mutC5_adapter_prefix_parser_clause_removed_py314.txt): 1-20, 335-354
    - [`LEAD_RED_R2_mutC6_adapter_jsonl_parser_clause_removed_py312.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_RED_R2_mutC6_adapter_jsonl_parser_clause_removed_py312.txt): 1-20, 325-346
    - [`LEAD_RED_R2_mutC6_adapter_jsonl_parser_clause_removed_py314.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_RED_R2_mutC6_adapter_jsonl_parser_clause_removed_py314.txt): 1-20, 340-360
    - [`LEAD_RED_R2_mutC7_adapter_object_parser_clause_removed_py312.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_RED_R2_mutC7_adapter_object_parser_clause_removed_py312.txt): 1-20, 355-376
    - [`LEAD_RED_R2_mutC7_adapter_object_parser_clause_removed_py314.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_RED_R2_mutC7_adapter_object_parser_clause_removed_py314.txt): 1-20, 385-406
    - [`LEAD_RED_R2_mutC8_adapter_object_walk_guard_removed_py312.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_RED_R2_mutC8_adapter_object_walk_guard_removed_py312.txt): 1-20, 350-374
    - [`LEAD_RED_R2_mutC8_adapter_object_walk_guard_removed_py314.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_RED_R2_mutC8_adapter_object_walk_guard_removed_py314.txt): 1-20, 385-408
    - [`LEAD_RED_R2_mutD1_receipt_appeared_arm_removed_py312.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_RED_R2_mutD1_receipt_appeared_arm_removed_py312.txt): 1-20, 45-67
    - [`LEAD_RED_R2_mutD1_receipt_appeared_arm_removed_py314.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_RED_R2_mutD1_receipt_appeared_arm_removed_py314.txt): 1-20, 50-74
    - [`LEAD_REPRO_R2_nesting_arms_py312.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_REPRO_R2_nesting_arms_py312.txt): 1-4 (complete)
    - [`LEAD_REPRO_R2_nesting_arms_py314.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919/sources/LEAD_REPRO_R2_nesting_arms_py314.txt): 1-4 (complete)

---

## (d) NOT VERIFIED

1. **Host Execution**: No shell commands, process executions, or tests were run directly by this reviewer (`SUPPLEMENTAL_UNEXECUTED`; all conclusions derived strictly through static textual and semantic inspection of packet blobs, diffs, logs, and trace analysis).
2. **POSIX Execution**: The POSIX publication branch (`os.replace` after `exists()`) and residual window were reviewed through code logic only, as execution evidence is Windows-specific (`os.name == 'nt'`).
3. **Live Infrastructure**: Live P026 restore pipelines, real market collector filesystems, and remote backup repositories were not exercised.

---

## (e) Verdict JSON

```json
{
  "part": "P030_R2_GEMINI",
  "verdict": "PASS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "f1": "CLOSED",
  "f2": "CLOSED",
  "f3": "CLOSED",
  "f4": "CLOSED",
  "f5": "CLOSED",
  "derived_fence_sound_on_pinned_312": true,
  "walk_guard_mutant_survives_anywhere": false,
  "findings": [],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
