# Independent Read-Only Detection Review: WP-P0-30 Archive-Exporter T0 Repair Round 1 (`0be0a8aa`)

**Reviewer Class:** `SUPPLEMENTAL_UNEXECUTED` (Gemini 3.8 Flash High, read-only inspection)  
**Packet Evaluated:** `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R1_20260916`  
**Commit Evaluated:** `0be0a8aa` (parent `53b43c21`, grandparent `153edee9`)  
**Verdict:** **PASS-WITH-NITS**

---

## 1. Finding 1 Closure (Staging, Verify, Publish Sequence & Leftover Invariants)

In `153edee9`, the exporter wrote directly to `target_jsonl`, meaning a mid-write abort (e.g. ENOSPC) or post-write refusal (`target_unwritable`, `target_verify_failed`, `receipt_unwritable`) left a consumable or truncated partition that `p030_closed_partition_backup_adapter.py` accepted.

### Trace of the New Sequence (`subject/p030_archive_exporter.py:389-481`):
1. **Staging Names:**  
   `staging_target = Path(str(target_jsonl) + STAGING_SUFFIX)` (`.p030partial`, lines 73, 389).  
   `staging_receipt = Path(str(receipt_path) + STAGING_SUFFIX)` (line 390).
2. **Staging Pre-Check:**  
   `if staging_target.exists() or staging_receipt.exists(): _refuse("target_exists", ...)` (lines 396–401). Staging leftovers from previous aborts are never silently adopted or overwritten.
3. **Partition Write & Fsync:**  
   `with staging_target.open("xb") as handle:` -> `handle.write(exported)` -> `handle.flush()` -> `os.fsync(handle.fileno())` (lines 405–408).
4. **Byte Re-Read Verification:**  
   `reread = staging_target.read_bytes()` checked against `exported` (lines 420–421).
5. **Receipt Write & Fsync:**  
   `with staging_receipt.open("xb") as handle:` -> `handle.write(receipt_raw)` -> `handle.flush()` -> `os.fsync(handle.fileno())` (lines 451–454).
6. **Publication Order & Atomic Replace:**  
   - Receipt published **first**: `if receipt_path.exists(): _refuse("receipt_exists")` -> `os.replace(staging_receipt, receipt_path)` (lines 463–470). A receipt without its partition is inert.
   - Target published **second**: `if target_jsonl.exists(): _refuse("target_exists")` -> `os.replace(staging_target, target_jsonl)` (lines 471–480).
7. **Invariants Confirmed by the Bytes:**
   - **Nothing under the target name on refusal:** `target_jsonl` is touched only at line 474 by `os.replace`, the final step before `return receipt`. Any prior refusal leaves `target_jsonl` uncreated.
   - **Leftovers never consumable:** Leftovers carry `.p030partial`, which the backup adapter and consumers reject (expecting `.jsonl`).
   - **Zero deletes:** No `os.remove`, `unlink`, `rmtree`, `rmdir`, or `shutil.move` exists across `p030_archive_exporter.py` (preserving the `opsa_common.py` invariant).
   - **Residual window stated:** Lines 452–453, 468–471 and `LEAD_VERIFICATION_P030_R1.md:14` explicitly document the window where receipt is published but target replace fails.
8. **Checker Test Exhibition:**
   - Mid-write ENOSPC: [`test_mid_write_failure_publishes_nothing_under_the_target_name`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R1_20260916/subject/check_p030_archive_exporter.py#L565-L611)
   - Receipt-write refusal: [`test_target_and_receipt_unwritable_refusals`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R1_20260916/subject/check_p030_archive_exporter.py#L517-L564)
   - Verify refusal: [`test_target_reread_byte_identity_refusal`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R1_20260916/subject/check_p030_archive_exporter.py#L211-L243)
   - Target-publish refusal: [`test_publish_failure_of_the_target_leaves_receipt_without_partition`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R1_20260916/subject/check_p030_archive_exporter.py#L613-L644)
   - Staging leftover triggers `target_exists`: asserted at [`check_p030_archive_exporter.py:603-610`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R1_20260916/subject/check_p030_archive_exporter.py#L603-L610).

### (a) Refusal-Path State Table
| Refusal Trigger & Line | Refusal Code | Files Remaining After Refusal | File Names & Consumability |
|---|---|---|---|
| Target exists at start (`:348`) | `target_exists` | None new; pre-existing target unchanged | Target exists; no staging files |
| Receipt exists at start (`:351`) | `receipt_exists` | None new; pre-existing receipt unchanged | Receipt exists; no staging files |
| Pre-write checks (timestamp, source read, json decoding, schema, descriptors) (`:354-385`) | Various (`invalid_timestamp`, `source_outside_root`, `source_unreadable`, etc.) | None | No files created on disk |
| Prior staging file detected (`:396`) | `target_exists` | Pre-existing staging file remains untouched | `<target>.p030partial` (inert, non-partition name) |
| Staging target `open("xb")` fails (`:409,:411`) | `target_exists` / `target_unwritable` | None (if open failed) or partial staging target (if write/flush/fsync failed) | `<target>.p030partial` (never consumable); nothing under target name |
| Staging target verify re-read fails (`:414,:419`) | `target_verify_failed` | Complete staging target partition | `<target>.p030partial` (inert); nothing under target name |
| Staging receipt `open("xb")` fails (`:455,:457`) | `receipt_exists` / `receipt_unwritable` | Complete staging target, optional partial staging receipt | `<target>.p030partial` (inert); nothing under target or receipt name |
| Receipt publish collision / failure (`:463,:467`) | `receipt_exists` / `receipt_unwritable` | Staging target and staging receipt | Both `<path>.p030partial` (inert); nothing under target or receipt name |
| Target publish collision / failure (`:471,:476`) | `target_exists` / `target_unwritable` | Published receipt + staging target partition | Receipt published at final name (inert without partition); target partition remains `<target>.p030partial` |

---

## 2. Finding 2 Closure (Source Root Containment Parity)

In `153edee9`, `_source_rel` used lexical `source_abs.relative_to(source_root_abs).as_posix()` without resolving or component-checking, allowing `..` traversal and symlink/junction escapes.

### Trace of the New `_source_rel` (`subject/p030_archive_exporter.py:129-185`):
1. **Lexical Relative Check:** `source_abs.relative_to(source_root_abs)` raises `source_outside_root` if outside (lines 142–147).
2. **Canonical Relative POSIX Rule:** Validates that `rel` is non-empty, stripped, contains no `\\`, no `\0`, is not absolute, has no drive/root, `posix.as_posix() == rel`, and has no `""`, `"."`, or `".."` in `rel.split("/")` (lines 150–164).
3. **Symlink and Junction Walk:** `current = source_root_abs.joinpath(*posix.parts)`. Loops upward to filesystem root (`parent == current`): if `current.is_symlink() or current.is_junction(): _refuse("source_outside_root", ...)` (lines 165–175).
4. **Resolved Ancestor Check:** `Path(source_jsonl).resolve().relative_to(Path(source_root).resolve())` (lines 176–184). Non-strict `resolve()` (Python 3.12 default) allows a missing leaf file to pass through to `_read_source_once` to fail with `source_unreadable` rather than an escape error, while all existing path components are fully resolved and checked.
5. **Dangling Symlink/Junction Behavior:** Because `is_symlink()` and `is_junction()` inspect directory reparse point / link metadata directly on `current` before `resolve()` is evaluated, a dangling symlink or junction cannot bypass the check.

### (b) Exporter vs. Adapter Rule Comparison Table
| Rule Check | Backup Adapter (`p030_closed_partition_backup_adapter.py`) | Archive Exporter (`p030_archive_exporter.py:129-185`) | Discrepancy / Parity Analysis |
|---|---|---|---|
| Literal Containment | `source_literal.relative_to(source_root_literal)` (`:234`) | `source_abs.relative_to(source_root_abs)` (`:143`) | **Exact parity** |
| Whitespace & Stripping | `value != value.strip()` (`:143`) | `rel != rel.strip()` (`:152`) | **Exact parity** |
| Backslash & NUL | `"\\"` in value (`:143`) | `"\\"` in rel, `"\0"` in rel (`:153-154`) | **Parity** (Exporter adds explicit NUL check) |
| Drive / Root / Absolute | `posix.is_absolute()`, `windows.drive`, `windows.root` (`:157-159`) | `posix.is_absolute()`, `windows.drive`, `windows.root` (`:155-157`) | **Exact parity** |
| Normalised POSIX Form | `posix.as_posix() != candidate` (`:161`) | `posix.as_posix() != rel` (`:158`) | **Exact parity** |
| `.` and `..` Segments | `any(part in {".", ".."} for part in posix.parts)` (`:162`) | `any(part in {"", ".", ".."} for part in rel.split("/"))` (`:159`) | **Parity** (Exporter also checks `""` across `split("/")`) |
| URL Unquoting | `unquote` loop up to 5 times; rejects if `decoded != value` (`:146-152`) | Not present | **Minor difference (NIT):** Adapter rejects percent-encoding (e.g. `%20`); Exporter does not check URL encoding. |
| Link / Junction Walk | `_refuse_source_links`: walks `current = source_root.joinpath(*parts)` up to root (`:168-178`) | Walks `source_root_abs.joinpath(*posix.parts)` up to root (`:165-175`) | **Exact parity** (Identical walk from target to root) |
| Resolved Containment | `source_literal.resolve().relative_to(source_root_literal.resolve())` (`:239-240, 254`) | `Path(source_jsonl).resolve().relative_to(Path(source_root).resolve())` (`:179`) | **Exact parity** |

- **Checker Tests Exhibiting Parity:**
  - `..` traversal: [`test_dotdot_traversal_is_refused_even_when_lexically_under_root`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R1_20260916/subject/check_p030_archive_exporter.py#L680-L708) (asserts adapter parity via `capture_stable_prefix`).
  - Junction component: [`test_junction_component_is_refused_like_the_adapter`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R1_20260916/subject/check_p030_archive_exporter.py#L709-L746) (asserts adapter parity via `capture_stable_prefix`).

---

## 3. Codes, Counts, and Fence Integrity

1. **Refusal Codes Table (16/16 preserved):**
   No refusal code was added, removed, or renamed. The 16 codes remain:
   `invalid_timestamp`, `source_outside_root`, `source_unreadable`, `short_read`, `empty_partition`, `source_line_invalid`, `source_line_noncanonical`, `source_fields_mismatch`, `contract_refused`, `identity_mismatch`, `mixed_dataset_descriptor`, `target_exists`, `receipt_exists`, `target_unwritable`, `target_verify_failed`, `receipt_unwritable`.
2. **K-06 Message Split:**
   In [`check_p030_archive_exporter.py:412-420`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R1_20260916/subject/check_p030_archive_exporter.py#L412-L420), `test_source_line_invalid_for_overflow_and_nan_literals` replaced regex alternation `"non-finite|not parseable"` with exact per-arm expectations:
   - `overflow.jsonl` -> `"non-finite"`
   - `nan.jsonl` -> `"not parseable"`
   - `nested.jsonl` -> `"non-finite"`
3. **Fence Integrity (Assertions Strengthened):**
   - [`test_target_reread_byte_identity_refusal`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R1_20260916/subject/check_p030_archive_exporter.py#L239-L243): tightened to assert `assertFalse(target.exists())`, `assertFalse(receipt.exists())`, and `assertTrue(staging.exists())`.
   - [`test_target_and_receipt_unwritable_refusals`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R1_20260916/subject/check_p030_archive_exporter.py#L538-L564): previously asserted `self.assertTrue(target.exists())` on receipt refusal; now strictly asserts `assertFalse(target.exists())`, `assertFalse(receipt.exists())`, and `assertTrue(staging_target.exists())`.
   - No tests were removed or weakened; suite expanded from 20 to 25 tests.
4. **NIT 5 (`exporter_sha256` LF-Normalised):**
   - `p030_archive_exporter.py:433` computes `hashlib.sha256(Path(__file__).read_bytes().replace(b"\r\n", b"\n")).hexdigest()`.
   - [`test_exporter_sha256_is_the_lf_form_on_any_checkout`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R1_20260916/subject/check_p030_archive_exporter.py#L645-L679) mocks `Path.read_bytes` to convert `\n` to `\r\n` and asserts the resulting digest matches `lf_digest`. Because Git checkouts on Windows alter newlines between `\r\n` and `\n`, replacing `\r\n` with `\n` ensures identity with the git blob across all platforms.
5. **Format-Only Commit Reflow (`53b43c21`):**
   - Verified across ranges [`1-150`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R1_20260916/subject/DIFF_format_only_153edee9_53b43c21.patch#L1-L150) and [`350-500`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R1_20260916/subject/DIFF_format_only_153edee9_53b43c21.patch#L350-L500) of `subject/DIFF_format_only_153edee9_53b43c21.patch`. All edits consist solely of wrapping long expressions onto multiple lines according to standard `ruff` formatting; zero semantic changes.

---

## 4. Record Honesty Verification

Every item in `LEAD_VERIFICATION_P030_R1.md` §3 was audited against evidence files:
- **GREEN:** `LEAD_CHECKER_R1_GREEN.txt` shows `Ran 25 tests in 0.447s ... OK`. Matches §3.
- **RED Arm (7 of 25 fail):** `LEAD_RED_ARM_new_checker_vs_153edee9.txt` confirms `FAILED (failures=3, errors=4)`. The 4 errors are on the missing `STAGING_SUFFIX` constant in the pre-repair exporter; the 3 failures are behavioral on `..` traversal, junction rejection, and CRLF exporter digest. Matches §3.
- **Guard:** `LEAD_GUARD_R1.txt` confirms `RESULT: PASS` with 2 files staged (`p030_archive_exporter.py`, `check_p030_archive_exporter.py`). Matches §3.
- **Ruff Findings:** `LEAD_RUFF_R1.txt` records `Found 5 errors. [*] 2 fixable with the --fix option`. (See Finding NIT 1 below).

---

## 5. (c) Findings

### [P030_R1_NIT_1] Discrepancy between Ruff error count and record description
- **Severity:** NIT
- **Location:** [`subject/LEAD_VERIFICATION_P030_R1.md:24`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R1_20260916/subject/LEAD_VERIFICATION_P030_R1.md#L24)
- **Description:** `LEAD_VERIFICATION_P030_R1.md` states `ruff check: the three pre-existing findings only (I001, SIM117, RUF059 at the old test) — 0 new`, whereas `LEAD_RUFF_R1.txt` states `Found 5 errors.` While the 3 cited lint rules likely account for the 5 occurrences across the files, the evidence artifact omitted the individual warning lines.

### [P030_R1_NIT_2] Exporter `_source_rel` omits URL unquote validation
- **Severity:** NIT
- **Location:** [`subject/p030_archive_exporter.py:150-164`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R1_20260916/subject/p030_archive_exporter.py#L150-L164)
- **Description:** The adapter's `_canonical_relative_posix` unquotes paths up to 5 times and refuses if `unquote(s) != s`. `p030_archive_exporter.py` enforces canonical POSIX naming, absence of backslashes/NUL, and resolved containment, but does not perform URL unquoting. If a path contains `%20`, the exporter accepts it while the adapter refuses. Partition names do not exhibit this in standard operation, but exact parity would include the unquote check.

### [P030_R1_NIT_3] Inherent TOCTOU window during `os.replace` publication
- **Severity:** NIT
- **Location:** [`subject/p030_archive_exporter.py:463-475`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R1_20260916/subject/p030_archive_exporter.py#L463-L475)
- **Description:** The publication sequence re-checks `target_jsonl.exists()` before calling `os.replace(staging_target, target_jsonl)`. A microscopic TOCTOU window exists between the existence check and `os.replace` where an externally created target could be overwritten. Given Python standard library limitations and the no-delete invariant, this is an acceptable design constraint under single-writer assumptions.

---

## 6. (d) Exact Read Coverage

All views obeyed the <= 150 lines per view rule and were read natively:
1. `PACKET_SHA256SUMS.txt`: lines 1–17 (complete)
2. `subject/COMMITS.txt`: lines 1–96 (complete)
3. `subject/BLOB_OIDS_HEAD.txt`: lines 1–3 (complete)
4. `subject/DIFF_semantic_53b43c21_0be0a8aa.patch`: lines 1–150; continued lines 151–300; continued lines 301–450; continued lines 451–473 (complete, 4 ranges)
5. `subject/p030_archive_exporter.py`: lines 1–150; continued lines 151–300; continued lines 301–450; continued lines 451–482 (complete, 4 ranges)
6. `subject/check_p030_archive_exporter.py`: lines 1–150; continued lines 151–300; continued lines 301–450; continued lines 451–600; continued lines 601–750; continued lines 751–761 (complete, 6 ranges)
7. `subject/LEAD_VERIFICATION_P030_R1.md`: lines 1–37 (complete)
8. `sources/OPUS_T0_REPORT_attempt1_153edee9.md`: lines 1–60; lines 216–300; lines 367–417 (all 3 mandated ranges complete)
9. `sources/p030_archive_exporter_153edee9_pre_repair.py`: lines 110–130; lines 280–340 (both mandated ranges complete)
10. `sources/p030_closed_partition_backup_adapter_HEAD.py`: lines 140–180; lines 220–250 (both mandated ranges complete)
11. `sources/opsa_common_HEAD.py`: lines 1–40 (complete)
12. `sources/LEAD_CHECKER_R1_GREEN.txt`: lines 1–3 (complete)
13. `sources/LEAD_GUARD_R1.txt`: lines 1–18 (complete)
14. `sources/LEAD_RED_ARM_new_checker_vs_153edee9.txt`: lines 1–10 (complete)
15. `sources/LEAD_REPRO_lane3_F1_F2.txt`: lines 1–10 (complete)
16. `sources/LEAD_RUFF_R1.txt`: lines 1–4 (complete)
17. `subject/DIFF_format_only_153edee9_53b43c21.patch`: lines 1–150; lines 350–500 (skimmed 2 ranges)

---

## 7. (e) NOT VERIFIED (Unexecuted Scope)

1. **No Live Execution:** Per reviewer class `SUPPLEMENTAL_UNEXECUTED`, no Python code, unit test runners, or OS commands were executed directly by this reviewer. Pass/fail results rely on static byte analysis and review of committed Lead run logs.
2. **Real Filesystem Reparse Points:** NTFS junction creation and resolution were not triggered on this host; validation is based on the logic of `is_junction()` / `is_symlink()` and `LEAD_REPRO_lane3_F1_F2.txt`.
3. **Multi-process Concurrency:** True concurrency races between multiple exporter processes targeting identical outputs were not dynamically simulated.
4. **Non-Windows Repositories:** Behavior of `PureWindowsPath` handling on non-Windows hosts was evaluated purely from code semantics.

---

## 8. (f) Review Summary JSON

```json
{
  "part": "P030_R1_GEMINI",
  "verdict": "PASS-WITH-NITS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "finding_1": "CLOSED",
  "finding_2": "CLOSED",
  "new_holes": [],
  "fence_changes": [
    "check_p030_archive_exporter.py:239-243 tightened test_target_reread_byte_identity_refusal to assert target and receipt do not exist, staging exists",
    "check_p030_archive_exporter.py:538-542,560-564 tightened test_target_and_receipt_unwritable_refusals to assert target does not exist on receipt failure and staging files checked",
    "check_p030_archive_exporter.py:412-420 split K-06 test_source_line_invalid_for_overflow_and_nan_literals into exact per-arm message assertions",
    "check_p030_archive_exporter.py: added 5 new tests (mid-write failure, publish failure residual window, LF digest checkout, dotdot traversal, junction component)"
  ],
  "findings": [
    {
      "finding_id": "P030_R1_NIT_1",
      "severity": "NIT",
      "file_line": "subject/LEAD_VERIFICATION_P030_R1.md:24",
      "description": "Lead verification record states 'the three pre-existing findings only (I001, SIM117, RUF059) — 0 new' whereas LEAD_RUFF_R1.txt records 'Found 5 errors', reflecting 3 rule types across 5 error instances without itemized diagnostic lines."
    },
    {
      "finding_id": "P030_R1_NIT_2",
      "severity": "NIT",
      "file_line": "subject/p030_archive_exporter.py:150-164",
      "description": "_source_rel lacks the adapter's URL unquote check from _canonical_relative_posix; percent-encoded characters like %20 or %2e%2e are rejected by the adapter but not by exporter lexical check."
    },
    {
      "finding_id": "P030_R1_NIT_3",
      "severity": "NIT",
      "file_line": "subject/p030_archive_exporter.py:463-475",
      "description": "Existence checks prior to os.replace possess a theoretical microsecond TOCTOU race if an external process creates the target concurrently, an inherent property of os.replace under standard library constraints."
    }
  ],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
