# Supplemental Read-Only Delta Review: WP-P0-30 Shape-B Exporter O9FIX

**Reviewer Model**: Gemini (gemini-3.8-flash-high)  
**Role**: Independent Read-Only Delta Reviewer (`SUPPLEMENTAL_UNEXECUTED`)  
**Scope**: Packet `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915`  
**Commit Under Review**: `daf6a43b` → `153edee97c008b36548cfb0c5bfaf5d7615a91d1` (HEAD in [`subject/COMMIT_HEAD.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/COMMIT_HEAD.txt))  

---

## (a) Finding-Closure Table (K-01 .. K-05)

| Finding | Predecessor Issue | Status | Delta Analysis & Evidence |
|---|---|---|---|
| **K-01** | Float overflow (`1e999`) raised raw `ValueError` outside the guard | **CLOSED** | In [`subject/p030_archive_exporter_HEAD.py:159-167`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/p030_archive_exporter_HEAD.py#L159-L167), `_reject_nonfinite_numbers(record)` is wrapped in `try ... except ValueError as exc:` mapping directly to `ExportRefused("source_line_invalid", f"source line {line_number} carries a non-finite number") from exc`.<br>In [`subject/check_p030_archive_exporter_HEAD.py:353-363`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/check_p030_archive_exporter_HEAD.py#L353-L363) (`test_source_line_invalid_for_overflow_and_nan_literals`), all 3 fixture arms reach `ExportRefused("source_line_invalid")`: <br>• `1e999`: Python's `json.loads` parses number token directly to `inf` bypassing `parse_constant`; caught during the post-parse `_reject_nonfinite_numbers` walk, hitting the new wrapper.<br>• `NaN` literal: `json.loads` encounters identifier constant and invokes `parse_constant=_reject_nonfinite_json`, raising `ValueError` caught at [:153](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/p030_archive_exporter_HEAD.py#L153) ("not parseable JSON").<br>• nested `-1e999`: parsed as `-inf` inside `{"a":{"b":[1,-1e999]}}`; caught during recursive traversal in `_reject_nonfinite_numbers`, hitting the new wrapper. |
| **K-02** | `dataset_content_hash` contract refusals leaked as raw `ContractRefused` | **CLOSED** | In [`subject/p030_archive_exporter_HEAD.py:287-292`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/p030_archive_exporter_HEAD.py#L287-L292), `dataset_content_hash(_descriptor(rows), rows)` is wrapped in `try ... except ContractRefused as exc: raise ExportRefused("contract_refused", str(exc)) from exc`.<br>Because `_descriptor` raises `ExportRefused("mixed_dataset_descriptor")` (subclass of `ValueError`, sibling to `ContractRefused`), its own refusal surfaces untouched.<br>In [`subject/check_p030_archive_exporter_HEAD.py:389-406`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/check_p030_archive_exporter_HEAD.py#L389-L406) (`test_contract_refused_from_slice_validation`), both fixture arms hit contracts validation: <br>• Duplicate rows: hits [`sources/p030_market_data_contracts_HEAD.py:367`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/sources/p030_market_data_contracts_HEAD.py#L367) (`raise ContractRefused("duplicate observation_id in dataset")`).<br>• `bar_close_time == bar_open_time`: hits [`sources/p030_market_data_contracts_HEAD.py:323`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/sources/p030_market_data_contracts_HEAD.py#L323) (`raise ContractRefused("dataset row bar_close_time must be after bar_open_time")`). |
| **K-03** | `_utc_z` accepted sub-second timestamps contrary to adapter rule | **CLOSED** | In [`subject/p030_archive_exporter_HEAD.py:109-112`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/p030_archive_exporter_HEAD.py#L109-L112), `if parsed.microsecond: _refuse("invalid_timestamp", "exported_at_utc must use whole seconds")`. This matches the backup adapter rule in [`sources/p030_closed_partition_backup_adapter_HEAD.py:138-139`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/sources/p030_closed_partition_backup_adapter_HEAD.py#L138-L139) (`if parsed.microsecond: raise ValueError(f"{field} must use whole seconds")`).<br>In [`subject/check_p030_archive_exporter_HEAD.py:301-316`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/check_p030_archive_exporter_HEAD.py#L301-L316) (`test_invalid_timestamp_refusals_including_sub_second`), all 6 arms are correctly classified: <br>• 2 whole-second arms: `.500Z` and `.000001Z` match regex `"whole seconds"`.<br>• 4 UTC Z arms: `+00:00` (non-Z), `2026-09-14T00:00:00` (no Z), `"not-a-time"` (non-ISO), and integer `20260914` (non-str) match regex `"UTC Z timestamp"`. |
| **K-04** | 11 of 16 `ExportRefused` codes lacked negative unit tests | **CLOSED** | Added [`ArchiveExporterRefusalCodeTests`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/check_p030_archive_exporter_HEAD.py#L263-L453) in `check_p030_archive_exporter_HEAD.py` (+203 lines). All 16 codes are explicitly tested with `self.assertEqual(caught.exception.code, code)`. All mock/stub branches (`Path.stat` and `Path.open`) isolate targets and safely restore real functions (see table b). |
| **K-05** | Line citation offsets in predecessor `REPORT.md:19` | **CLOSED** | Corrected in [`sources/DISPOSITION_O9FIX.md:12`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/sources/DISPOSITION_O9FIX.md#L12) without modifying historical `REPORT.md`. HEAD line numbers are verified: return projection statement is at [`subject/p030_archive_exporter_HEAD.py:223`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/p030_archive_exporter_HEAD.py#L223), and preservation loop is at [`subject/check_p030_archive_exporter_HEAD.py:151-153`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/check_p030_archive_exporter_HEAD.py#L151-L153). |

---

## (b) 16-Code Refusal Coverage Verification Table

Every code raised via `_refuse` or `ExportRefused` in [`subject/p030_archive_exporter_HEAD.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/p030_archive_exporter_HEAD.py) mapped to its test assertion in [`subject/check_p030_archive_exporter_HEAD.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/check_p030_archive_exporter_HEAD.py):

| # | `ExportRefused` Code | Source Lines Raised | Test Method & Assertion Line | Branch & Stub Analysis | Verified? |
|---|---|---|---|---|---|
| 1 | `target_exists` | :258, :299 | `test_target_exists_refusal:168` | Pre-existing target file verified. Pre-write check fires. | **VERIFIED** |
| 2 | `receipt_exists` | :261, :337 | `test_receipt_exists_refusal:422` | Pre-existing `.p030export.json` verified. Asserts target does not exist. | **VERIFIED** |
| 3 | `invalid_timestamp` | :99, :104, :108, :112 | `test_invalid_timestamp_refusals_including_sub_second:306,311` | 6 arms: 2 sub-second whole-second arms; 4 UTC Z format arms. | **VERIFIED** |
| 4 | `source_outside_root` | :123 | `test_source_outside_root_refusal:321` | Path outside source root raises `ValueError` in `relative_to`. | **VERIFIED** |
| 5 | `source_unreadable` | :135 | `test_source_unreadable_refusal:329` | Missing source file triggers `OSError` on `stat()`/`open()`. | **VERIFIED** |
| 6 | `short_read` | :137, :141 | `test_short_read_refusals:336,348` | Arm 1 tests stripped trailing newline. Arm 2 uses `_StatWithSize` patch inflating `st_size` by 1 only when `path == source` to cleanly exercise line 136; restores real `open`/`stat` on context exit. | **VERIFIED** |
| 7 | `empty_partition` | :139, :272 | `test_empty_partition_refusal:196` | 0-byte source file verified. | **VERIFIED** |
| 8 | `source_line_invalid` | :155, :158, :166 | `test_malformed_line_refusal:182` & `test_source_line_invalid_for_overflow_and_nan_literals:362` | Covers unparseable JSON, numeric float overflow (`1e999`), `NaN` literal, and nested `-1e999`. | **VERIFIED** |
| 9 | `source_line_noncanonical` | :180, :183 | `test_source_line_noncanonical_refusal:369` | Source line containing whitespace formatting (`b'{"open": 1}\n'`) rejected. | **VERIFIED** |
| 10 | `source_fields_mismatch` | :192 | `test_source_fields_mismatch_refusal:378` | Row with extra key (`"unexpected"`) rejected; regex verifies field difference. | **VERIFIED** |
| 11 | `contract_refused` | :200, :214, :292 | `test_contract_refused_from_row_identity:387` & `test_contract_refused_from_slice_validation:396,403` | Row level (`open` non-decimal) + slice level (duplicate row + `bar_close_time == bar_open_time`). | **VERIFIED** |
| 12 | `identity_mismatch` | :204, :206, :218, :220 | `test_prefixed_identity_mismatch_is_refused:259` | Tampered observation ID prefixed with `p030obs-v1:` rejected. | **VERIFIED** |
| 13 | `mixed_dataset_descriptor` | :240 | `test_mixed_dataset_descriptor_refusal:414` | Divergent `venue` across rows rejected; propagates past `ContractRefused` guard. | **VERIFIED** |
| 14 | `target_unwritable` | :301 | `test_target_and_receipt_unwritable_refusals:438` | `Path.open` patched to raise `PermissionError` when `path == target`; passes through all other paths to `original_open`; asserts `not target.exists()`. | **VERIFIED** |
| 15 | `target_verify_failed` | :305, :307 | `test_target_reread_byte_identity_refusal:219` | `Path.read_bytes` patched for target to return appended byte; asserts reread mismatch. | **VERIFIED** |
| 16 | `receipt_unwritable` | :339 | `test_target_and_receipt_unwritable_refusals:449` | `Path.open` patched to raise `PermissionError` when `path == receipt`; target write succeeds; asserts `target.exists()` and `not receipt.exists()`. | **VERIFIED** |

---

## (c) New Findings

- **[N-01] NIT: Hash divergence in build lane artifact `sources/SHA256SUMS.txt`**
  - **Location**: [`sources/SHA256SUMS.txt:2`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/sources/SHA256SUMS.txt#L2)
  - **Description**: `sources/SHA256SUMS.txt` lists `8195157c490e3be6da5069ac6a5f9ff40e66001f26618bb2753f144c238024c5 *check_p030_archive_exporter.py`, whereas [`PACKET_SHA256SUMS.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/PACKET_SHA256SUMS.txt) and [`subject/check_p030_archive_exporter_HEAD.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/check_p030_archive_exporter_HEAD.py) hash to `b0f0112a105094a4e2d177372d3542812b977c86f92a9044b5c7611e7286fe55`. This appears to stem from Windows CRLF normalization or the test adjustment noted in `DISPOSITION_O9FIX.md` note 1 prior to final commit. The commit itself contains only the two Python files, and `p030_archive_exporter.py` matches identically across all manifests (`7571bafc...`). Advisory only; non-blocking.

---

## (d) Scope, Delta Mechanics, & Evidence Analysis

1. **Exact Two-File Ceiling**: [`subject/DELTA_STAT_daf6a43b_HEAD.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/DELTA_STAT_daf6a43b_HEAD.txt) confirms exactly two files modified: `check_p030_archive_exporter.py` (+203) and `p030_archive_exporter.py` (+21, -2). Total 222 insertions, 2 deletions. `market_data_collector.py`, `p030_closed_partition_backup_adapter.py`, and `p030_market_data_contracts.py` remain byte-for-byte untouched.
2. **RED Arm Validation**: [`sources/LEAD_RED_ARM_new_checker_old_exporter.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/sources/LEAD_RED_ARM_new_checker_old_exporter.txt) confirms the new checker against `daf6a43b` fails on exactly K-01 (`ERROR: ValueError: non-finite JSON number`), K-02 (`ERROR: ContractRefused`), and K-03 (`FAIL: AssertionError: ExportRefused not raised`), with the remaining 17 test cases passing (`FAILED (failures=1, errors=2)`).
3. **Execution Evidence**:
   - `check_p030_archive_exporter.py`: 20 tests pass in 0.336s (`Ran 20 tests ... OK`, [`sources/LEAD_check_p030_archive_exporter.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/sources/LEAD_check_p030_archive_exporter.txt)).
   - `check_p030_closed_partition_backup_adapter.py`: 44 tests pass (`Ran 44 tests ... OK`, exit 0, [`sources/LEAD_check_p030_closed_partition_backup_adapter_TAIL.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/sources/LEAD_check_p030_closed_partition_backup_adapter_TAIL.txt)).
   - `check_market_data_collector.py`: exit 0, `MARKET DATA COLLECTOR CHECK: PASS` ([`sources/LEAD_check_market_data_collector.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/sources/LEAD_check_market_data_collector.txt)).
   - `check_p030_market_data_contracts.py`: exit 0, `P030 MARKET DATA CONTRACTS CHECK: PASS` ([`sources/LEAD_check_p030_market_data_contracts.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/sources/LEAD_check_p030_market_data_contracts.txt)).
   - Repo guard: `PINE_ALERT_GUARD PASS files=21 matches=0 allowlist=0` ([`sources/LEAD_GUARD_O9FIX.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/sources/LEAD_GUARD_O9FIX.txt)).
4. **Style & Ruff Formatting**: Linter check passes (`Ruff --select E9,F821,F811,F401,F841`: `All checks passed!`). Not running `ruff format` avoids sweeping reformatting churn over unmodified code and preserves historical blame lines. This conforms to task instructions and lane discipline.

---

## (e) EXACT Read Coverage Table

All 20 native read slices were executed strictly within `_gemini_packets_20260913/P030_O9FIX_20260915`:

| # | Packet-Relative File Path Viewed | Line Range Viewed | Slices & Continuations | Status |
|---|---|---|---|---|
| 1 | `PACKET_SHA256SUMS.txt` | L1–20 | Initial: 1–20 | Complete (20 lines) |
| 2 | `subject/DELTA_STAT_daf6a43b_HEAD.txt` | L1–4 | Initial: 1–4 | Complete (4 lines) |
| 3 | `subject/COMMIT_HEAD.txt` | L1–35 | Initial: 1–35 | Complete (35 lines) |
| 4 | `subject/DELTA_daf6a43b_HEAD.diff` | L1–260 | Initial: 1–150; Cont 1: 151–260 | Complete (260 lines) |
| 5 | `subject/p030_archive_exporter_HEAD.py` | L1–341 | Initial: 1–120; Cont 1: 121–240; Cont 2: 241–341 | Complete (341 lines) |
| 6 | `subject/check_p030_archive_exporter_HEAD.py` | L1–467 | Initial: 1–120; Cont 1: 121–240; Cont 2: 241–360; Cont 3: 361–467 | Complete (467 lines) |
| 7 | `sources/GEMINI_REPORT_daf6a43b_K01_K05.md` | L1–218 | Initial: 1–150; Cont 1: 151–218 | Complete (218 lines) |
| 8 | `sources/TASK_O9FIX.md` | L1–20 | Initial: 1–20 | Complete (20 lines) |
| 9 | `sources/DISPOSITION_O9FIX.md` | L1–52 | Initial: 1–52 | Complete (52 lines) |
| 10 | `sources/LEAD_check_p030_archive_exporter.txt` | L1–28 | Initial: 1–28 | Complete (28 lines) |
| 11 | `sources/LEAD_RED_ARM_new_checker_old_exporter.txt` | L1–8 | Initial: 1–8 | Complete (8 lines) |
| 12 | `sources/LEAD_RUFF_O9FIX.txt` | L1–2 | Initial: 1–2 | Complete (2 lines) |
| 13 | `sources/LEAD_check_p030_closed_partition_backup_adapter_TAIL.txt` | L1–14 | Initial: 1–14 | Complete (14 lines) |
| 14 | `sources/DECISIONS_rows_P030.md` | L1–5 | Initial: 1–5 | Complete (5 lines) |
| 15 | `sources/p030_closed_partition_backup_adapter_HEAD.py` | L120–160 | Initial: 120–160 | Partial/Rule Read (:131-140) |
| 16 | `sources/p030_market_data_contracts_HEAD.py` | L300–380 | Slice 1: 330–380; Slice 2: 300–333 | Partial/Contracts Read (:322-323, :365-371) |
| 17 | `sources/LEAD_check_market_data_collector.txt` | L1–51 | Initial: 1–51 | Complete (51 lines) |
| 18 | `sources/LEAD_check_p030_market_data_contracts.txt` | L1–37 | Initial: 1–37 | Complete (37 lines) |
| 19 | `sources/SHA256SUMS.txt` | L1–3 | Initial: 1–3 | Complete (3 lines) |
| 20 | `sources/LEAD_GUARD_O9FIX.txt` | L1–6 | Initial: 1–6 | Complete (6 lines) |

---

## (f) NOT VERIFIED

- **Execution**: Review performed strictly as a read-only supplemental reviewer (`SUPPLEMENTAL_UNEXECUTED`). No Python interpreter, test runner, or system command was invoked. Evidence citations rely on committed execution output tails.
- **Git State & Working Directory**: No branch switches, git checkouts, worktree modifications, index staging, or commit generation occurred.
- **External Network & MCP**: No external HTTP requests, package index lookups, or MCP tools were utilized.
- **Canonical Acceptance**: This review does not approve, merge, or alter package acceptance boundaries for WP-P0-30.

---

```json
{
  "part": "P030_O9FIX_GEMINI",
  "verdict": "PASS-WITH-NITS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "closed": [
    "K-01",
    "K-02",
    "K-03",
    "K-04",
    "K-05"
  ],
  "findings": [
    {
      "id": "N-01",
      "severity": "NIT",
      "path": "sources/SHA256SUMS.txt:2",
      "description": "Recorded hash for check_p030_archive_exporter.py (8195157c...) differs from packet subject/check_p030_archive_exporter_HEAD.py (b0f0112a...), likely attributable to Windows CRLF line ending conversion or pre-commit draft hashing."
    }
  ],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
