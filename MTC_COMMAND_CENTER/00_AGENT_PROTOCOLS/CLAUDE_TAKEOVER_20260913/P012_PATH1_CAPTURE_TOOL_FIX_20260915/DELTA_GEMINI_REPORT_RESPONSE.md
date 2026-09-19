# DELTA REVIEW REPORT — WP-P0-12 "Path 1" Read-Only Own-Account Evidence Capture Tool
**Candidate Commit**: [`af921d75`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/COMMIT_af921d75.txt#L1-L43)  
**Correction Author**: Claude Opus 5 Lead (disclosed under owner ruling `OD-20260915-P012-P1FIX-LEAD-1`)  
**Reviewer Role**: `gemini-3.8-flash-high` Independent DELTA Reviewer  
**Evidence Class**: `SUPPLEMENTAL_UNEXECUTED` (Strictly read-only; no execution, no network, no write, no subprocess)  
**Packet Root**: `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/`

---

## (a) F-1..F-11 and L-1..L-6 Disposition Table

| Finding ID | Severity | Disposition Status | af921d75 Location (file:line) | Fencing Test Function |
|---|---|---|---|---|
| **F-1** | REQUIRED | **RESOLVED** | [`subject/capture_own_account_evidence_af921d75.py:577-587`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/capture_own_account_evidence_af921d75.py#L577-L587) | [`test_signature_without_run_id_refuses_before_network_and_writes_nothing`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/test_capture_own_account_evidence_af921d75.py#L480-L502) |
| **F-2** | REQUIRED | **RESOLVED** | [`subject/capture_own_account_evidence_af921d75.py:52, 357-371, 656-662`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/capture_own_account_evidence_af921d75.py#L357-L371) | [`test_half_open_window_excludes_row_at_end_but_keeps_inside_rows`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/test_capture_own_account_evidence_af921d75.py#L226-L241), [`test_row_before_requested_start_refuses`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/test_capture_own_account_evidence_af921d75.py#L243-L252), [`test_row_after_requested_end_refuses`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/test_capture_own_account_evidence_af921d75.py#L254-L263) |
| **F-3 / L-4** | NIT | **RESOLVED** | [`subject/capture_own_account_evidence_af921d75.py:585-587`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/capture_own_account_evidence_af921d75.py#L585-L587) | [`test_wrong_ownership_signature_refuses_before_network_and_writes_nothing`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/test_capture_own_account_evidence_af921d75.py#L504-L537) |
| **F-4 / L-3** | NIT | **RESOLVED** | [`subject/capture_own_account_evidence_af921d75.py:243-259`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/capture_own_account_evidence_af921d75.py#L243-L259) | [`test_funding_identity_includes_coin`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/test_capture_own_account_evidence_af921d75.py#L289-L320) |
| **F-5 / L-5** | NIT | **RESOLVED** | [`subject/capture_own_account_evidence_af921d75.py:134-149`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/capture_own_account_evidence_af921d75.py#L134-L149) | [`test_write_once_refuses_an_existing_output`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/test_capture_own_account_evidence_af921d75.py#L334-L345) |
| **F-6 / L-5** | NIT | **RESOLVED** | [`subject/capture_own_account_evidence_af921d75.py:196-208, 393-424`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/capture_own_account_evidence_af921d75.py#L393-L424) | [`test_error_response_bytes_are_kept_before_refusal`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/test_capture_own_account_evidence_af921d75.py#L357-L387), [`test_capturing_info_post_keeps_pre_parse_bytes_and_error_bytes`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/test_capture_own_account_evidence_af921d75.py#L389-L417) |
| **F-7 / L-6** | NIT | **RESOLVED** | [`subject/capture_own_account_evidence_af921d75.py:54-55, 75, 186, 296`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/capture_own_account_evidence_af921d75.py#L296) | [`test_capture_writes_manifest_sidecars_extraction_and_requery_identities`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/test_capture_own_account_evidence_af921d75.py#L172), [`test_capturing_info_post_keeps_pre_parse_bytes_and_error_bytes`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/test_capture_own_account_evidence_af921d75.py#L404) |
| **F-8** | NIT | **RESOLVED** | [`subject/test_capture_own_account_evidence_af921d75.py:389-417`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/test_capture_own_account_evidence_af921d75.py#L389-L417) | [`test_capturing_info_post_keeps_pre_parse_bytes_and_error_bytes`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/test_capture_own_account_evidence_af921d75.py#L389-L417) |
| **F-9 / L-2** | NIT | **RESOLVED** | [`subject/test_capture_own_account_evidence_af921d75.py:193-224, 504-537`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/test_capture_own_account_evidence_af921d75.py#L193-L224) | [`test_multi_page_success_dedups_the_inclusive_boundary`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/test_capture_own_account_evidence_af921d75.py#L193-L224), [`test_wrong_ownership_signature_refuses_before_network_and_writes_nothing`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/test_capture_own_account_evidence_af921d75.py#L504-L537) |
| **F-10 / L-1** | NIT | **RESOLVED** | [`subject/test_capture_own_account_evidence_af921d75.py:1-12`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/test_capture_own_account_evidence_af921d75.py#L1-L12), [`subject/capture_own_account_evidence_af921d75.py:199`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/capture_own_account_evidence_af921d75.py#L199) | Lint clean (`F401`, `RUF100`, `F841`) and `ruff format` applied |
| **F-11** | NIT | **RESOLVED** | [`subject/capture_own_account_evidence_af921d75.py:550-565, 642-643`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/capture_own_account_evidence_af921d75.py#L550-L565) | [`test_requery_content_mismatch_refuses`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/subject/test_capture_own_account_evidence_af921d75.py#L276-L288) |
| **L-1** | NIT | **RESOLVED** | As F-10 | As F-10 |
| **L-2** | NIT | **RESOLVED** | As F-8, F-9 | As F-8, F-9 |
| **L-3** | NIT | **RESOLVED** | As F-4 | As F-4 |
| **L-4** | NIT | **RESOLVED** | As F-3 | As F-3 |
| **L-5** | NIT | **RESOLVED** | As F-5, F-6 | As F-5, F-6 |
| **L-6** | NIT | **RESOLVED** | As F-7 | As F-7 |

---

## (b) RED-Arm Evaluation Table (Lead Reported 12 Pre-Fix Failures)

| Test Function Name | Fails Pre-Fix for RIGHT Reason? | Analysis & Mechanism |
|---|---|---|
| `test_capture_writes_manifest_sidecars_extraction_and_requery_identities` | **INCIDENTALLY** | Fails pre-fix because newly added manifest contract assertions (`window.start_ms`, `window.semantics`, and `raw_bytes_source`) were absent in `e77af1c8`. The test is an end-to-end happy path asserting new metadata fields, not an adversarial failure-mode defect arm. |
| `test_half_open_window_excludes_row_at_end_but_keeps_inside_rows` | **RIGHT REASON** | Pre-fix tool admitted the row at `END_MS` into `derived["fills"]` (`[1, 2]`). The test asserts `[1]`, catching defect F-2. |
| `test_row_before_requested_start_refuses` | **RIGHT REASON** | Pre-fix tool accepted `t < start_ms` without checking; test catches the missing boundary validation defect (F-2). |
| `test_row_after_requested_end_refuses` | **RIGHT REASON** | Pre-fix tool accepted `t > end_ms` without checking; test catches the missing boundary validation defect (F-2). |
| `test_requery_identity_mismatch_refuses` | **INCIDENTALLY** | Pre-fix tool **already refused** on mismatched identity sets (`REFUSED_REQUERY_MISMATCH`), but returned detail `"fills"` instead of `"fills identity only in one pass: ..."`. Failed pre-fix solely due to the stricter detail string assertion. |
| `test_requery_content_mismatch_refuses` | **RIGHT REASON** | Pre-fix tool compared identity sets only (`{ident}`) and ignored content differences between pass 1 and pass 2; test catches defect F-11. |
| `test_funding_identity_includes_coin` | **RIGHT REASON** | Pre-fix tool omitted `coin` (`hash:time`), causing multi-coin hourly funding events to collide and raise `funding identity conflict`; test catches defect F-4 / L-3. |
| `test_write_once_refuses_an_existing_output` | **INCIDENTALLY** | Pre-fix tool **already refused** on pre-existing files (`if path.exists(): raise ...`), but with detail `"refusing to overwrite x.json"` instead of `"output exists: x.json"`. Failed pre-fix due to detail message change, not lack of refusal. |
| `test_error_response_bytes_are_kept_before_refusal` | **RIGHT REASON** | Pre-fix tool dropped error response bytes on exception; test asserts `<name>_ERROR.json` and sidecar exist, catching defect F-6 / L-5. |
| `test_capturing_info_post_keeps_pre_parse_bytes_and_error_bytes` | **RIGHT REASON** | Pre-fix had no test exercising `CapturingInfo.post` directly, lacked `capture.source`, and did not attach `error_capture` to `CaptureRefused`; test catches defects F-8 and F-6. |
| `test_signature_without_run_id_refuses_before_network_and_writes_nothing` | **RIGHT REASON** | Pre-fix tool defaulted dynamic `run_id` without error, performed network queries, created output directory, and failed at the end; test catches defect F-1. |
| `test_wrong_ownership_signature_refuses_before_network_and_writes_nothing` | **RIGHT REASON** | Pre-fix tool verified signatures after 5 network queries and file creation; test asserts `fake.fill_calls == 0` and `not out.exists()`, catching defect F-3 / L-4. |

---

## (c) Window Rule Walk Table (`paged_query`)

Interval: `[start_ms, end_ms)` half-open. Venue Info API `endTime`: inclusive.

| Point in Time | Query Context | Derived View Inclusion | Identity Set Inclusion | Stored Bytes Inclusion | Refusal Behavior | Cursor / Pagination Impact |
|---|---|---|---|---|---|---|
| `t < start_ms` | Any page | **EXCLUDED** | **EXCLUDED** | **STORED** (in raw page JSON) | **REFUSES** `CAPTURE_REFUSED_MALFORMED` (`"row before requested start"`) | Execution aborts immediately; no partial state accepted. |
| `t == start_ms` | Page 1 (`cursor = start_ms`) | **INCLUDED** | **INCLUDED** | **STORED** | **NONE** (Valid row) | `page_max = max(cursor, start_ms)`; advances cursor. |
| `t == end_ms - 1` | Page $k$ | **INCLUDED** | **INCLUDED** | **STORED** | **NONE** (Valid row) | `page_max = max(page_max, end_ms - 1)`; advances cursor. |
| `t == end_ms` | Final/boundary page | **EXCLUDED** (`t >= end_ms -> continue`) | **EXCLUDED** | **STORED** (in raw page JSON) | **NONE** (Legitimate return from inclusive API) | `page_max = max(page_max, t)` executes **before** `continue`, advancing `page_max = end_ms > cursor`. Cursor advances to `end_ms`, preventing cursor stall. If page is full of rows at `end_ms`, next page with `cursor = end_ms` either returns `< limit` (clean stop) or stalls if $\ge \text{limit}$ rows all at `end_ms` (refuses `REFUSED_TRUNCATED`). |
| `t == end_ms + 1` | Any page | **EXCLUDED** | **EXCLUDED** | **STORED** (in raw page JSON) | **REFUSES** `CAPTURE_REFUSED_MALFORMED` (`"row after requested end"`) | Execution aborts immediately. |
| `t == cursor` (inclusive restart) | Page 2 restart | **DEDUPLICATED** (`rows_by_id[ident]["row"] == row`) | **PRESERVED** (exact 1 entry in dict) | **STORED** (in page 2 raw JSON) | **NONE** (Duplicate identical row skipped; content mismatch refuses) | Allows pagination to seamlessly pick up from boundary millisecond without duplicating rows or missing multi-row millisecond events. |

**Stop Condition & Cursor Advances Confirmation**:
- `page_max` updates at line 368 **before** `if t >= end_ms: continue` at line 370. Cursor advances past an excluded `end_ms` row, preventing stall.
- Stop condition `if len(parsed) < limit:` (line 386) counts **raw returned rows** (`parsed`), never the post-filtering or deduplicated counts. Pagination never terminates prematurely due to excluded `end_ms` rows or deduplication.

---

## (d) Findings

- **Finding G-D-01 (NIT)**: [`sources/DISPOSITION_P1FIX.md:26`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/sources/DISPOSITION_P1FIX.md#L26), [`sources/LEAD_RED_ARMS_PREFIX_TOOL.txt:5,8`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_DELTA_20260915/sources/LEAD_RED_ARMS_PREFIX_TOOL.txt#L5)  
  - **Severity**: **NIT**  
  - **Description**: The Lead reported that all 12 failed tests on `e77af1c8` were exact defect closures. However, `test_requery_identity_mismatch_refuses` and `test_write_once_refuses_an_existing_output` were already rejecting invalid inputs on `e77af1c8` and failed pre-fix solely due to refined exception detail string assertions (`"only in one pass"` and `"output exists"`).
  - **One-line Repair**: Note in future disposition tables that tests with sharpened assertion strings fail pre-fix incidentally rather than from missing rejection logic.

---

## (e) EXACT Native Read Coverage

All reads were native [`view_file`](file:///C:/LAB/Tradingview_LAB_CLEAN/AGENTS.md) calls on canonical repository files; at most 150 lines per view; zero external reads, commands, or agents:

1. `C:/LAB/Tradingview_LAB_CLEAN/AGENTS.md`: lines 1–64 (complete)
2. `PACKET_SHA256SUMS.txt`: lines 1–22 (complete)
3. `sources/GEMINI_REPORT_e77af1c8_F01_F11.md`:
   - lines 1–150
   - lines 151–300 (continuation 1)
   - lines 301–376 (continuation 2, complete)
4. `sources/DISPOSITION_P1FIX.md`: lines 1–34 (complete)
5. `sources/DECISIONS_rows_P1FIX.md`: lines 1–2 (complete)
6. `sources/TASK_P1FIX.md`: lines 1–28 (complete)
7. `sources/REAL_OBSERVATION_INTAKE.md`: lines 1–49 (complete; line 31 verified)
8. `sources/hyperliquid_sdk_info_excerpt.md`:
   - lines 1–150
   - lines 151–160 (continuation 1, complete)
9. `sources/hyperliquid_sdk_api_excerpt.md`: lines 1–48 (complete)
10. `subject/COMMIT_af921d75.txt`: lines 1–43 (complete)
11. `sources/LEAD_RED_ARMS_PREFIX_TOOL.txt`: lines 1–14 (complete)
12. `sources/LEAD_FOCUSED_PY312.txt`: lines 1–2 (complete)
13. `sources/LEAD_FULL_SUITE_PY312.txt`: lines 1–5 (complete)
14. `subject/DELTA_e77af1c8_af921d75.diff`:
    - lines 1–150
    - lines 151–300 (continuation 1)
    - lines 301–450 (continuation 2)
    - lines 451–600 (continuation 3)
    - lines 601–750 (continuation 4)
    - lines 751–907 (continuation 5, complete)
15. `subject/capture_own_account_evidence_af921d75.py`:
    - lines 1–150
    - lines 151–300 (continuation 1)
    - lines 301–450 (continuation 2)
    - lines 451–600 (continuation 3)
    - lines 601–717 (continuation 4, complete)
16. `subject/test_capture_own_account_evidence_af921d75.py`:
    - lines 1–150
    - lines 151–300 (continuation 1)
    - lines 301–450 (continuation 2)
    - lines 451–544 (continuation 3, complete)
17. `subject/path1_sign_ownership.html`: lines 1–59 (complete; message equality verified)
18. `subject/capture_own_account_evidence_e77af1c8_PREFIX.py`:
    - lines 100–150 (write_once, consume_capture, call_info)
    - lines 151–250 (identities, record_response)
    - lines 251–310 (paged_query pre-fix behavior)
    - lines 420–505 (run_capture pre-fix verification order and requery)

---

## (f) NOT VERIFIED

- **No Execution**: Neither `test_capture_own_account_evidence_af921d75.py` nor the test suite was executed by this reviewer (`SUPPLEMENTAL_UNEXECUTED`).
- **Lead's Execution Counts**: The reported test counts (21 passed focused; 1619 + 30 passed full suite; 12 failed / 9 passed pre-fix) are quoted directly from Lead logs (`LEAD_FOCUSED_PY312.txt`, `LEAD_FULL_SUITE_PY312.txt`, `LEAD_RED_ARMS_PREFIX_TOOL.txt`) and were not independently run.
- **No Network Activity**: No network call was made to Hyperliquid mainnet or testnet.
- **Real Account Data**: No real account private keys, balances, or live API credentials were used or inspected.

---

## (g) Machine-Readable Verdict Object

```json
{
  "part": "P1CAP_DELTA_GEMINI",
  "verdict": "PASS-WITH-NITS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "dispositions": {
    "F-1": "RESOLVED",
    "F-2": "RESOLVED",
    "F-3": "RESOLVED",
    "F-4": "RESOLVED",
    "F-5": "RESOLVED",
    "F-6": "RESOLVED",
    "F-7": "RESOLVED",
    "F-8": "RESOLVED",
    "F-9": "RESOLVED",
    "F-10": "RESOLVED",
    "F-11": "RESOLVED",
    "L-1": "RESOLVED",
    "L-2": "RESOLVED",
    "L-3": "RESOLVED",
    "L-4": "RESOLVED",
    "L-5": "RESOLVED",
    "L-6": "RESOLVED"
  },
  "lead_authorship": "NOTED",
  "findings": [
    {
      "id": "G-D-01",
      "severity": "NIT",
      "location": "sources/DISPOSITION_P1FIX.md:26",
      "description": "Two pre-fix RED test arms (requery identity mismatch and write_once existing output) failed pre-fix due to tightened exception detail assertions rather than missing rejection logic."
    }
  ],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
