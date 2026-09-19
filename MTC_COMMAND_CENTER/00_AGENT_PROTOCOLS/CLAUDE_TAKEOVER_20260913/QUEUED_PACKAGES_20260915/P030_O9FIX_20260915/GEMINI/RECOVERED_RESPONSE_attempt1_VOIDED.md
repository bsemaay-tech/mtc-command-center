# Supplemental Read-Only Delta Review: WP-P0-30 Shape-B Archive Exporter (O9FIX)

**Reviewer Model**: Gemini (gemini-3.8-flash-high)  
**Role**: Independent Read-Only Delta Reviewer (`SUPPLEMENTAL_UNEXECUTED`)  
**Scope**: Packet `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915` (Commit `daf6a43b` → HEAD `153edee97c008b36548cfb0c5bfaf5d7615a91d1` in [`subject/COMMIT_HEAD.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/COMMIT_HEAD.txt)).

---

## (a) Finding-Closure Table K-01..K-05

| Finding ID | Previous State (`daf6a43b`) | Resolution in O9FIX (`153edee9`) | Code Location (HEAD) | Test Location (HEAD) | Status |
|---|---|---|---|---|---|
| **K-01** | `_reject_nonfinite_numbers` was invoked outside the `json.loads` try/except block; float overflow (`1e999`) leaked raw `ValueError` | `_reject_nonfinite_numbers` is wrapped in `try...except ValueError` mapping to `ExportRefused("source_line_invalid", "… carries a non-finite number")` | [`p030_archive_exporter_HEAD.py:159-167`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/p030_archive_exporter_HEAD.py#L159-L167) | [`check_p030_archive_exporter_HEAD.py:352-363`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/check_p030_archive_exporter_HEAD.py#L352-L363) | **CLOSED** |
| **K-02** | `dataset_content_hash(_descriptor(rows), rows)` call was unwrapped; whole-slice contract failures leaked raw `ContractRefused` | Call wrapped in `try...except ContractRefused` mapping to `ExportRefused("contract_refused", str(exc))`; `_descriptor`'s `mixed_dataset_descriptor` passes through | [`p030_archive_exporter_HEAD.py:287-292`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/p030_archive_exporter_HEAD.py#L287-L292) | [`check_p030_archive_exporter_HEAD.py:389-406`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/check_p030_archive_exporter_HEAD.py#L389-L406) | **CLOSED** |
| **K-03** | `_utc_z` validated ISO UTC Z format but permitted sub-second timestamps (`parsed.microsecond != 0`), diverging from backup adapter | Added whole-second check `if parsed.microsecond: _refuse("invalid_timestamp", "exported_at_utc must use whole seconds")` | [`p030_archive_exporter_HEAD.py:109-113`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/p030_archive_exporter_HEAD.py#L109-L113) | [`check_p030_archive_exporter_HEAD.py:301-316`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/check_p030_archive_exporter_HEAD.py#L301-L316) | **CLOSED** |
| **K-04** | 11 of 16 `ExportRefused` codes lacked dedicated negative tests in the test suite | Added `ArchiveExporterRefusalCodeTests` suite covering all 16 codes with explicit negative tests; test suite expanded from 8 to 20 tests | [`check_p030_archive_exporter_HEAD.py:263-452`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/check_p030_archive_exporter_HEAD.py#L263-L452) | Entire class `ArchiveExporterRefusalCodeTests` | **CLOSED** |
| **K-05** | Previous `REPORT.md:19` had minor line citation offsets for row projection return and field preservation assertion | Corrected in [`DISPOSITION_O9FIX.md:12`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/sources/DISPOSITION_O9FIX.md#L12) without altering predecessor's `REPORT.md` | [`DISPOSITION_O9FIX.md:12`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/sources/DISPOSITION_O9FIX.md#L12) | Verified against HEAD line numbers | **CLOSED** |

### Detailed Technical Verification of K-01..K-05:
1. **K-01 Breakdown**:
   - `nan.jsonl` (`{"open":NaN}`): `NaN` is a non-standard JSON literal; `json.loads` calls `parse_constant=_reject_nonfinite_json`, which raises `ValueError("non-finite JSON constant: NaN")`. This is caught by the primary `try...except (..., ValueError)` block at lines 147–156, raising `ExportRefused("source_line_invalid", "source line 1 is not parseable JSON")`.
   - `overflow.jsonl` (`{"open":1e999}`) & `nested.jsonl` (`{"a":{"b":[1,-1e999]}}`): Standard Python `json.loads` converts overflowing numeric literals directly to `inf` / `-inf` without invoking `parse_constant`. The post-parse recursive traversal `_reject_nonfinite_numbers(record)` detects `math.isfinite(value) is False` and raises `ValueError("non-finite JSON number")`. This is caught by the new guard at lines 159–167, raising `ExportRefused("source_line_invalid", "source line 1 carries a non-finite number")`.
2. **K-02 Breakdown**:
   - Inside `export_partition`, lines 287–292 wrap `dataset_content_hash(_descriptor(rows), rows)`.
   - `_descriptor(rows)` is executed within the `try` block. If venue, track, or proxy_source diverge across rows, it raises `ExportRefused("mixed_dataset_descriptor", ...)`. Because `ExportRefused` inherits from standard `ValueError` and not `ContractRefused`, it bypasses `except ContractRefused:` and surfaces with code `"mixed_dataset_descriptor"`.
   - Fixture arm 1 (duplicate rows): hits `sources/p030_market_data_contracts_HEAD.py:366-367` (`raise ContractRefused("duplicate observation_id in dataset")`), mapped to `ExportRefused("contract_refused", ...)`.
   - Fixture arm 2 (`bar_close_time == bar_open_time`): `dataset_content_hash` calls `_validate_dataset_row(row)`, hitting `sources/p030_market_data_contracts_HEAD.py:322-323` (`raise ContractRefused("dataset row bar_close_time must be after bar_open_time")`), mapped to `ExportRefused("contract_refused", ...)`.
3. **K-03 Breakdown**:
   - Matches adapter rule in [`sources/p030_closed_partition_backup_adapter_HEAD.py:138-139`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/sources/p030_closed_partition_backup_adapter_HEAD.py#L138-L139): `if parsed.microsecond: raise ValueError(f"{field} must use whole seconds")`.
   - Test `test_invalid_timestamp_refusals_including_sub_second` contains 6 distinct arms correctly partitioned:
     - 2 whole-second refusals: `"2026-09-14T00:00:00.500Z"`, `"2026-09-14T00:00:00.000001Z"` (match message regex `"whole seconds"`).
     - 4 UTC Z timestamp refusals: `"2026-09-14T00:00:00+00:00"`, `"2026-09-14T00:00:00"` (missing `Z`), `"not-a-time"`, `20260914` (integer) (match message regex `"UTC Z timestamp"`).
4. **K-05 Breakdown**:
   - `p030_archive_exporter_HEAD.py:223`: `return {field: candidate[field] for field in DATASET_ROW_FIELDS}`.
   - `check_p030_archive_exporter_HEAD.py:151-153`: `for key, value in raw.items(): if key not in {"observation_id", "producer_payload_hash"}: self.assertEqual(exported[key], value)`.
   - Both line citations in `DISPOSITION_O9FIX.md:12` are exact. Predecessor's `REPORT.md` remained unedited.

---

## (b) The 16-Code Coverage Verification Table

Every `ExportRefused` code raised in [`subject/p030_archive_exporter_HEAD.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/p030_archive_exporter_HEAD.py) was checked against [`subject/check_p030_archive_exporter_HEAD.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/check_p030_archive_exporter_HEAD.py):

| # | `ExportRefused` Code | Exporter Raise Line(s) | Test Name & Class | Test Assertion Line | Verified? | Notes & Mock Integrity |
|---|---|---|---|---|---|---|
| 1 | `target_exists` | `:258, :299` | `ArchiveExporterTests.test_target_exists_refusal` | `:168` | **VERIFIED** | Real file placed at target; asserts `code == "target_exists"` |
| 2 | `receipt_exists` | `:261, :337` | `ArchiveExporterRefusalCodeTests.test_receipt_exists_refusal` | `:298` (via `_refused`) | **VERIFIED** | Target `.p030export.json` created in advance; verifies target not created |
| 3 | `invalid_timestamp` | `:99, :104, :108, :112` | `ArchiveExporterRefusalCodeTests.test_invalid_timestamp_refusals_including_sub_second` | `:298` (via `_refused`) | **VERIFIED** | 6 arms tested; asserts `code == "invalid_timestamp"` across all |
| 4 | `source_outside_root` | `:122` | `ArchiveExporterRefusalCodeTests.test_source_outside_root_refusal` | `:298` (via `_refused`) | **VERIFIED** | Disjoint `source_root` supplied; asserts `code == "source_outside_root"` |
| 5 | `source_unreadable` | `:135` | `ArchiveExporterRefusalCodeTests.test_source_unreadable_refusal` | `:298` (via `_refused`) | **VERIFIED** | Non-existent path passed as source; catches `OSError` |
| 6 | `short_read` | `:137, :141` | `ArchiveExporterRefusalCodeTests.test_short_read_refusals` | `:298` (via `_refused`) | **VERIFIED** | Arm 1: missing `\n`. Arm 2: `_StatWithSize` mocks `Path.stat().st_size + 1` for `source` only; real `Path.stat` restored cleanly |
| 7 | `empty_partition` | `:139, :272` | `ArchiveExporterTests.test_empty_partition_refusal` | `:196` | **VERIFIED** | 0-byte source partition; asserts `code == "empty_partition"` |
| 8 | `source_line_invalid` | `:154, :158, :165` | `ArchiveExporterTests.test_malformed_line_refusal` & `ArchiveExporterRefusalCodeTests.test_source_line_invalid_for_overflow_and_nan_literals` | `:182`, `:298` | **VERIFIED** | Malformed JSON syntax, `1e999` overflow, `NaN` literal, and nested `-1e999` |
| 9 | `source_line_noncanonical` | `:179, :183` | `ArchiveExporterRefusalCodeTests.test_source_line_noncanonical_refusal` | `:298` (via `_refused`) | **VERIFIED** | Uncompacted JSON `{"open": 1}\n`; asserts `code == "source_line_noncanonical"` |
| 10 | `source_fields_mismatch` | `:191` | `ArchiveExporterRefusalCodeTests.test_source_fields_mismatch_refusal` | `:298` (via `_refused`) | **VERIFIED** | Injected extraneous field `unexpected`; asserts `extra=['unexpected']` |
| 11 | `contract_refused` | `:200, :213, :292` | `ArchiveExporterRefusalCodeTests.test_contract_refused_from_row_identity` & `ArchiveExporterRefusalCodeTests.test_contract_refused_from_slice_validation` | `:298` (via `_refused`) | **VERIFIED** | Row-level: non-decimal string. Slice-level: duplicate row & `close <= open` |
| 12 | `identity_mismatch` | `:204, :206, :218, :220` | `ArchiveExporterTests.test_prefixed_identity_mismatch_is_refused` | `:259` | **VERIFIED** | Tampered prefixed observation ID; asserts `code == "identity_mismatch"` |
| 13 | `mixed_dataset_descriptor` | `:240` | `ArchiveExporterRefusalCodeTests.test_mixed_dataset_descriptor_refusal` | `:298` (via `_refused`) | **VERIFIED** | Venue mismatch on row 2; asserts `code == "mixed_dataset_descriptor"` |
| 14 | `target_unwritable` | `:301` | `ArchiveExporterRefusalCodeTests.test_target_and_receipt_unwritable_refusals` | `:298` (via `_refused`) | **VERIFIED** | `Path.open` raises `PermissionError` on target path only; delegates others to `original_open`; clean context unpatch |
| 15 | `target_verify_failed` | `:305, :307` | `ArchiveExporterTests.test_target_reread_byte_identity_refusal` | `:219` | **VERIFIED** | `Path.read_bytes` appends tampering bytes on target re-read; asserts `code == "target_verify_failed"` |
| 16 | `receipt_unwritable` | `:339` | `ArchiveExporterRefusalCodeTests.test_target_and_receipt_unwritable_refusals` | `:298` (via `_refused`) | **VERIFIED** | `Path.open` raises `PermissionError` on receipt path only; target created, receipt absent; clean context unpatch |

**Coverage Summary**: 16 out of 16 codes (100%) have explicit negative tests asserting `caught.exception.code == <code>`. All stubs/mocks (`Path.stat`, `Path.open`, `Path.read_bytes`) are tightly conditioned on specific paths, delegate all other filesystem operations to original callables, and restore originals cleanly.

---

## (c) New Findings

### [K-06] NIT: Loose message regex alternation in numeric overflow test
- **Location**: [`subject/check_p030_archive_exporter_HEAD.py:362`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/check_p030_archive_exporter_HEAD.py#L362)
- **Description**: In `test_source_line_invalid_for_overflow_and_nan_literals`, the test verifies `overflow.jsonl` (`1e999`), `nan.jsonl` (`NaN`), and `nested.jsonl` (`-1e999`) using the single disjunctive regex `"non-finite|not parseable"`. While `nan.jsonl` fails at parse time with message `"source line 1 is not parseable JSON"` and the overflow cases fail post-parse with `"source line 1 carries a non-finite number"`, grouping them under the broad alternation would allow a regression that misclassifies an overflow token as an unparseable JSON error to still pass.
- **Severity**: NIT (informational test-tightness suggestion; both errors correctly assert `caught.exception.code == "source_line_invalid"`).

### [K-07] NIT: CRLF / LF line-ending divergence in auxiliary checksum file
- **Location**: [`sources/SHA256SUMS.txt:2`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/sources/SHA256SUMS.txt#L2) vs [`PACKET_SHA256SUMS.txt:15`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/PACKET_SHA256SUMS.txt#L15)
- **Description**: `sources/SHA256SUMS.txt` records `8195157c490e3be6da5069ac6a5f9ff40e66001f26618bb2753f144c238024c5` for `check_p030_archive_exporter.py` (computed on LF bytes in builder worktree), whereas `PACKET_SHA256SUMS.txt` reports `b0f0112a105094a4e2d177372d3542812b977c86f92a9044b5c7611e7286fe55` due to Windows CRLF worktree checkout. (Meanwhile, `p030_archive_exporter.py` matched identically in both: `7571bafc...`).
- **Severity**: NIT (harmless environment line-ending artifact; git blob SHA in `DELTA_daf6a43b_HEAD.diff:2` index `42fcee28` is authoritative).

---

## (d) Scope, Delta & Evidence Verification

1. **Ceiling Compliance**:
   - [`subject/DELTA_STAT_daf6a43b_HEAD.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/subject/DELTA_STAT_daf6a43b_HEAD.txt) confirms exactly 2 files modified: `check_p030_archive_exporter.py` (+203) and `p030_archive_exporter.py` (+21, -2).
   - Zero modifications to `market_data_collector.py`, `p030_closed_partition_backup_adapter.py`, or `p030_market_data_contracts.py`.
2. **RED Arm Validation**:
   - [`sources/LEAD_RED_ARM_new_checker_old_exporter.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915/sources/LEAD_RED_ARM_new_checker_old_exporter.txt) shows the new 20-test checker run against the old exporter (`daf6a43b`) produced `FAILED (failures=1, errors=2)`:
     - K-01: ERROR `ValueError: non-finite JSON number` (raw leak)
     - K-02: ERROR raw `ContractRefused` (unwrapped leak)
     - K-03: FAIL `AssertionError: ExportRefused not raised` (accepted sub-second timestamp)
     - 17 other tests PASSED.
   - This proves test sharpness and verifies that the new tests genuinely isolate and fail on the exact bugs fixed in O9FIX.
3. **Execution Evidence Honesty**:
   - `LEAD_check_p030_archive_exporter.txt`: `Ran 20 tests in 0.336s ... OK` (D-13 RED/GREEN confirmed).
   - `LEAD_check_p030_closed_partition_backup_adapter_TAIL.txt`: `Ran 44 tests ... OK`, exit 0.
   - `LEAD_check_market_data_collector.txt`: 51 assertions / invariants verified, exit 0.
   - `LEAD_check_p030_market_data_contracts.txt`: 37 contract / mutant checks verified, exit 0.
   - `LEAD_RUFF_O9FIX.txt`: `All checks passed!` under `--select E9,F821,F811,F401,F841`.
   - `ruff format` omission: Deliberately preserving base line formatting rather than running broad formatters is appropriate and standard engineering practice for surgical fix lanes, preventing extraneous diff churn across non-modified code blocks.

---

## (e) EXACT Read Coverage

All 20 native read slices were executed strictly within `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915` (at most 150 lines per view; zero external reads):

| # | File Path Viewed | Line Range | Slices & Continuations | Status |
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
| 15 | `sources/p030_closed_partition_backup_adapter_HEAD.py` | L120–160 | Slice 1: 120–160 | Target range complete (41 lines) |
| 16 | `sources/p030_market_data_contracts_HEAD.py` | L300–380 | Slice 1: 330–380; Slice 2: 300–330 | Target range complete (81 lines) |
| 17 | `sources/LEAD_check_market_data_collector.txt` | L1–51 | Initial: 1–51 | Complete (51 lines) |
| 18 | `sources/LEAD_check_p030_market_data_contracts.txt` | L1–37 | Initial: 1–37 | Complete (37 lines) |
| 19 | `sources/SHA256SUMS.txt` | L1–3 | Initial: 1–3 | Complete (3 lines) |
| 20 | `sources/LEAD_GUARD_O9FIX.txt` | L1–6 | Initial: 1–6 | Complete (6 lines) |

---

## (f) NOT VERIFIED

- **Execution**: As a read-only supplemental reviewer (`SUPPLEMENTAL_UNEXECUTED`), no commands, test suites, or python scripts were executed by this reviewer; all test results and exit codes are evaluated strictly from committed lead evidence transcripts.
- **Git / Repository Mutation**: No repository mutations, branching, commits, or push actions were performed.
- **Production Venue Data**: Verification was conducted against committed unit tests, synthetic fixtures, and deterministic contracts; no live exchange or production archives were touched.
- **Package Acceptance**: This review confirms the technical closure of findings K-01..K-05 within the scoped packet; it does not claim or constitute canonical package acceptance.

---

```json
{
  "part": "P030_O9FIX_GEMINI",
  "verdict": "PASS-WITH-NITS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "closed": ["K-01", "K-02", "K-03", "K-04", "K-05"],
  "findings": [
    {
      "id": "K-06",
      "severity": "NIT",
      "path": "subject/check_p030_archive_exporter_HEAD.py:362",
      "description": "test_source_line_invalid_for_overflow_and_nan_literals uses an alternating message regex 'non-finite|not parseable' across both overflow and NaN literal cases rather than validating the specific message string for each branch."
    },
    {
      "id": "K-07",
      "severity": "NIT",
      "path": "sources/SHA256SUMS.txt:2",
      "description": "Auxiliary hash file records LF checksum for check_p030_archive_exporter.py whereas PACKET_SHA256SUMS.txt records CRLF checksum due to Windows worktree checkout; authoritative git index blob sha in diff header is clean."
    }
  ],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
