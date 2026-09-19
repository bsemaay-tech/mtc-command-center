# Detection Review: WP-P0-12 Funding Intake Adapter (`IBKR_PAPER_BRIDGE/tools/funding_intake_adapter.py`)

**Reviewer Identity:** Gemini 3.8 Flash (High) (acting as independent read-only detection reviewer)  
**Role & Mode:** `SUPPLEMENTAL_UNEXECUTED` (Read-only review within packet `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915`; zero execution, zero writes, zero network access)  
**Scope Under Review:** `subject/funding_intake_adapter.py`, `subject/test_funding_intake_adapter.py`, `subject/P012_FUNDING_INTAKE_DESIGN_20260915.md`, and supporting provenance sources.

---

## 1. Field-by-Field Fabrication Audit

Every field in [sources/r1_binding_packet_draft.json](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/r1_binding_packet_draft.json) (`bindings[*]` and `coverage`) is audited below against its origin:
- **COPIED:** Transcribed directly from the capture manifest or `DERIVED_EXTRACTION.json`.
- **TOOL-RULE:** Derived from an explicit constant or requirement in `export_mtc_funding_fcac0ac6.py`.
- **DERIVED-LABELLED:** Computed / formatted by the adapter but explicitly annotated as a proposed rule.
- **UNRESOLVED:** Explicitly set to `UNRESOLVED:D-n`.

| Target Path / Key | Value in `r1_binding_packet_draft.json` | Classification | Origin / Basis |
|---|---|---|---|
| `adapter_version` | `"p012-funding-intake/v1"` | TOOL-RULE | Adapter module constant (`funding_intake_adapter.py:30`). |
| `label` | `"NONACCEPTING_INTAKE_DRAFT"` | TOOL-RULE | Draft fence constant (`funding_intake_adapter.py:31`). |
| `packet_version` | `"SYNTHETIC_FUNDING_BINDING_PACKET_V1"` | TOOL-RULE | Verbatim tool constant `export_mtc_funding_fcac0ac6.py:108`. |
| `bindings[*].event_timestamp` | `"2026-09-14T17:00:00.041Z"`, `"2026-09-14T18:00:00.060Z"` | COPIED | Formatted via `utc_z()` from `derived["funding"][*]["time"]` (`1789405200041`, `1789408800060`); venue stamp kept verbatim per D-3. |
| `bindings[*].funding_event_id` | `"hl-funding:0x1E26…AC49:BTC:1789405200041"` | DERIVED-LABELLED | Deterministic ID formatted under proposed rule D-2 (`funding_intake_adapter.py:209`). |
| `bindings[*].funding_event_id_rule` | `"PROPOSED:D-2 hl-funding:<account-short>:<coin>:<time_ms>"` | DERIVED-LABELLED | Explicit annotation marking rule proposal D-2 (`funding_intake_adapter.py:215`). |
| `bindings[*].observed.szi` | `"0.00058"` | COPIED | Verbatim from `derived["funding"][*]["szi"]`. |
| `bindings[*].observed.usdc` | `"-0.000571"`, `"-0.000572"` | COPIED | Verbatim from `derived["funding"][*]["usdc"]`. |
| `bindings[*].observed.venue_hash` | `"0x0000000000000000000000000000000000000000000000000000000000000000"` | COPIED | Verbatim from `derived["funding"][*]["hash"]`. |
| `bindings[*].oracle_price` | `"UNRESOLVED:D-4"` | UNRESOLVED | `UNRESOLVED:D-4`; not in venue funding row. Back-derivation fenced out. |
| `bindings[*].oracle_price_source` | `"UNRESOLVED:D-4"` | UNRESOLVED | `UNRESOLVED:D-4`. |
| `bindings[*].positive_rate_payer` | `"LONG"` | TOOL-RULE | Verbatim constant from `export_mtc_funding_fcac0ac6.py:122` (`APPROVED_PAYER = "LONG"`). |
| `bindings[*].positive_rate_payer_basis` | `"export_mtc_funding.APPROVED_PAYER (tool constant)"` | TOOL-RULE | Metadata annotation of rule provenance (`funding_intake_adapter.py:219`). |
| `bindings[*].provenance.evidence_kind` | `"REAL_CAPTURE_READ_ONLY"` | DERIVED-LABELLED | Proposed evidence kind string for D-5 (`funding_intake_adapter.py:33`). |
| `bindings[*].provenance.evidence_kind_status` | `"UNRESOLVED:D-5"` | UNRESOLVED | `UNRESOLVED:D-5`. |
| `bindings[*].provenance.extraction_method` | `"capture_own_account_evidence.py tool_sha256=00b3b8f69f0e4870 user_funding_history"` | COPIED / DERIVED-LABELLED | Composed from tool name + prefix of `responses[0]["tool_sha256"]`. |
| `bindings[*].provenance.source_locator` | `"funding_pass1_page001.json#/0"`, `...#/1` | COPIED | Resolved from pass 1 file in manifest matching `capture_sha256` + `json_pointer`. |
| `bindings[*].provenance.source_sha256` | `"6f25ba294ae96dd333f6938bfe103f283559a960463ddfd2ce8757806563578f"` | COPIED | Verbatim from `derived["funding"][*]["capture_sha256"]`. |
| `bindings[*].provenance.source_title` | `"Hyperliquid userFunding 0x1E26…AC49 run p012-path1-20260914T1500Z-1900Z-r1"` | COPIED / DERIVED-LABELLED | Composed from venue title + short address + manifest `run_id`. |
| `bindings[*].raw_rate` | `"0.0000125"` | COPIED | Verbatim from `derived["funding"][*]["fundingRate"]`. |
| `bindings[*].source_event_digest` | `"UNRESOLVED:D-1"` | UNRESOLVED | `UNRESOLVED:D-1`. Production digest domain not approved. |
| `coverage.account_scope` | `"0x1E26…AC49"` | COPIED | Short form of manifest `address` (`funding_intake_adapter.py:87-96`). |
| `coverage.complete` | `true` | DERIVED-LABELLED | Computed by adapter's proposed witness rule D-6 (`funding_intake_adapter.py:145-171`). |
| `coverage.evidence_kind` | `"REAL_CAPTURE_READ_ONLY"` | DERIVED-LABELLED | Proposed evidence kind string for D-5. |
| `coverage.expected_event_ids` | `["hl-funding:0x1E26…AC49:BTC:1789405200041", ...]` | DERIVED-LABELLED | List of derived `funding_event_id` strings from bindings. |
| `coverage.interval_end_exclusive` | `"2026-09-14T19:00:00Z"` | COPIED | Verbatim from manifest `window["end"]`. |
| `coverage.interval_start_inclusive` | `"2026-09-14T15:00:00Z"` | COPIED | Verbatim from manifest `window["start"]`. |
| `coverage.source_witnesses` | `[{"file": "funding_pass1...", "sha256": ...}, ...]` | COPIED | Verbatim response file names and hashes from manifest `responses`. |
| `coverage.symbol` | `"BTC"` | COPIED | Verbatim from manifest `coin`. |
| `coverage.unattributed_event_ids` | `[]` | TOOL-RULE / COPIED | Empty list satisfying `COVERAGE_KEYS` (`export_mtc_funding_fcac0ac6.py:201`). |
| `coverage.witness_identity` | `"capture_own_account_evidence.py ... ownership OWNERSHIP_EVIDENCE: VERIFIED 0x1E26…AC49"` | COPIED / DERIVED-LABELLED | Composed from tool sha prefix, run_id, ownership status, and short address. |
| `coverage.witness_reasons` | `[]` | DERIVED-LABELLED | Reasons list from proposed `completeness()` function. |
| `coverage.witness_rule` | `"hour-aligned window AND two byte-identical funding passes (proposed D-6)"` | DERIVED-LABELLED | Explicit annotation defining proposed D-6 rule. |

**Confirmation:**
- **No oracle price fabrication:** The back-derived calculation (`0.000571 / (0.00058 * 0.0000125) ≈ 78758.6`) appears nowhere in any output JSON or code. Both `oracle_price` and `oracle_price_source` are strictly set to `"UNRESOLVED:D-4"`.
- **`positive_rate_payer = "LONG"`:** Matches exactly `export_mtc_funding_fcac0ac6.py:122` (`APPROVED_PAYER = "LONG"`).

---

## 2. Design-Note Honesty

Verification of claims in [subject/P012_FUNDING_INTAKE_DESIGN_20260915.md](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/P012_FUNDING_INTAKE_DESIGN_20260915.md) against [sources/export_mtc_funding_fcac0ac6.py](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py):

1. **Claim: No `--mode` CLI argument and production mode is unavailable.**
   - Verified: The docstring (lines 23–28) states: *"There is no mode switch, callback, boolean gate or magic literal that turns a synthetic candidate into a production record... production mode stays PRODUCTION_MODE_UNAVAILABLE"*.
   - Verified: CLI invocation (lines 59–63) defines only `--snapshot`, `--bindings`, `--symbol`, `--start`, `--end`, `--schedule-id`, `--staging`.
   - Verified: Line 116 states `PRODUCTION_MODE_UNAVAILABLE = "UNAVAILABLE_PENDING_SOURCE_EVENT_DIGEST_DOMAIN"`.
2. **Claim: Only accepts `SYNTHETIC_FIXTURE` evidence; refuses everything else with `CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE`.**
   - Verified: Line 109–110: `SYNTHETIC_EVIDENCE_KIND = "SYNTHETIC_FIXTURE"`, `ACCEPTED_EVIDENCE_KINDS = (SYNTHETIC_EVIDENCE_KIND,)`.
   - Verified: Lines 468–473 (`_validate_coverage`):
     ```python
     if kind not in ACCEPTED_EVIDENCE_KINDS:
         raise _Refusal(CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE, ...)
     ```
   - Verified: Lines 570–575 (`_validate_provenance`):
     ```python
     if kind not in ACCEPTED_EVIDENCE_KINDS:
         raise _Refusal(CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE, ...)
     ```
3. **Claim: Decisions D-1 through D-6 each map to a genuine gap in the export tool's closed domains.**
   - **D-1 (`source_event_digest`):** Required in `BINDING_KEYS` (line 175). Tool defines only `SYNTHETIC_SOURCE_EVENT_DIGEST_V1` (line 111) and notes production domain is unresolved (line 212). Gap verified.
   - **D-2 (`funding_event_id`):** Required in `BINDING_KEYS` (line 169). Venue returns zero hash (`0x000...0`) for all funding events (`capture_own_account_evidence_af921d75.py:497`), causing collisions unless derived via a rule. Gap verified.
   - **D-3 (`event_timestamp`):** Required in `BINDING_KEYS` (line 168). Hyperliquid stamps funding 31–60 ms past the hour; tool leaves settlement time authority unresolved (lines 47–50, 209). Gap verified.
   - **D-4 (`oracle_price` & `oracle_price_source`):** Required in `BINDING_KEYS` (lines 170–171). Venue `userFunding` response does not provide oracle prices (`capture_own_account_evidence_af921d75.py:489–506`). Gap verified.
   - **D-5 (`evidence_kind`):** Required in `PROVENANCE_KEYS` and `COVERAGE_KEYS` (lines 178, 195). Only `SYNTHETIC_FIXTURE` is accepted (line 110); real read-only capture kinds are unadmitted. Gap verified.
   - **D-6 (`complete` witness rule):** Required in `COVERAGE_KEYS` (line 194). Tool requires `complete: True` and witness identities (lines 474–513), but specifies no rule for read-only capture verification. Gap verified.

---

## 3. Completeness Rule Analysis

In [subject/funding_intake_adapter.py](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/funding_intake_adapter.py) (lines 145–171):
- `completeness()` asserts `complete: True` if and only if:
  1. Window bounds `start_ms` and `end_ms` are exact multiples of `3_600_000` ms (`HOUR_MS`);
  2. `end_ms > start_ms`;
  3. At least two funding pass responses exist, and all captured funding passes have identical SHA256 hashes.
- **Labelling:** The rule is explicitly labelled as proposed:
  - `coverage.witness_rule = "hour-aligned window AND two byte-identical funding passes (proposed D-6)"`
  - `intake_gap_report.json:37`: `"coverage.complete (adapter rule, not the tool's approved witness)": "D-6"`
- **Boundary & Missed Instant Soundness (Adversarial Assessment):**
  - The r1 capture window is defined as `[15:00:00Z, 19:00:00Z)` with half-open semantics (`start_ms` inclusive, `end_ms` exclusive).
  - Hyperliquid funding events are stamped with latency past the hour (e.g. `17:00:00.041Z`, `18:00:00.060Z`, `19:00:00.041Z`).
  - If a 19:00 funding event occurred at `19:00:00.041Z`, it strictly exceeds `19:00:00.000Z` (`1789412400000`). If that payment represents the 18:00–19:00 funding interval, an intake interval ending at `19:00:00.000Z` would exclude it. Yet `completeness()` would still report `complete: True` because the window endpoints are hour-aligned and both passes match.
  - Furthermore, `completeness()` does not verify whether the expected number of funding events (e.g., 4 events for a 4-hour window) matches the returned count (r1 had 2 events because the position was opened at ~16:03Z).
  - The Lead honestly surfaced this in the design doc (lines 20, 27) as open decisions D-3 and D-6. Because the adapter is non-accepting, this proposal is acceptable for a draft, but is flagged as a NIT regarding future production witness requirements.

---

## 4. Leakage Assessment

- **Address Redaction:**
  - `short_address()` ([funding_intake_adapter.py:87-96](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/funding_intake_adapter.py#L87-L96)) strictly redacts 42-char addresses to `address[:6] + "…" + address[-4:]` (`0x1E26…AC49`).
  - Audited `r1_binding_packet_draft.json`, `r1_retained_rows_expected.json`, and `r1_intake_gap_report.json`: no full 42-character Ethereum/EVM account address appears. The only full 66-character hex strings are SHA256 digests and the venue's zero transaction hash (`0x000...0`).
  - [test_funding_intake_adapter.py:120](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/test_funding_intake_adapter.py#L120) explicitly asserts:
    ```python
    assert ADDRESS not in json.dumps(intake)
    ```
- **Credential & Secret Protection:**
  - Audited imports in `funding_intake_adapter.py` (lines 20–29): standard library modules only (`argparse`, `hashlib`, `json`, `sys`, `datetime`, `pathlib`, `typing`).
  - No `os.environ`, no HTTP/network client libraries (`urllib`, `requests`, `socket`), no disk writing into the capture directory, and no credential-handling modules.
  - Leakage check: **CLEAN**.

---

## 5. Test Suite and Red-Arm Audit

Each of the 7 tests in [subject/test_funding_intake_adapter.py](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/test_funding_intake_adapter.py) was reviewed:
1. `test_build_fills_only_what_the_bytes_supply_and_labels_the_rest` (lines 104–132): Proves exact field mappings, verbatim numeric strings, draft labels, short-address redaction, and `UNRESOLVED:D-n` tagging. Cannot easily pass on a broken implementation due to strict field-level assertions.
2. `test_unresolved_fields_are_never_fabricated` (lines 134–144): Proves that all unresolved fields start with `"UNRESOLVED:D-"` and that back-derived oracle prices (`78758`, `78759`) do not appear.
3. `test_completeness_rule_hour_alignment_and_identical_passes` (lines 146–157): Proves both positive and negative cases for hour alignment and pass hash identity.
4. `test_refuses_foreign_coin_malformed_rows_and_bad_labels` (lines 159–172): Proves input validation rejecting coin mismatches, non-integer timestamps, and unexpected row kinds.
5. `test_load_refuses_wrong_kinds_and_duplicate_keys` (lines 174–188): Proves strict JSON parsing rejecting duplicate keys and unrecognized manifest kinds.
6. `test_outputs_are_deterministic_write_once_and_clock_free` (lines 190–204): Proves byte-for-byte determinism, `.sha256` sidecar correctness, and write-once collision protection. (Contains a minor NIT on the clock assertion disjunction; see findings).
7. `test_main_end_to_end` (lines 206–213): Proves CLI exit code 0 on valid execution and exit code 3 on existing directory collision.

**Red-Arm Verification:**
- [sources/LEAD_RED_ARM_fabrication_fence.txt](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/LEAD_RED_ARM_fabrication_fence.txt) shows exact output from a mutant injecting arithmetic oracle prices:
  - `FAILED tests/test_funding_intake_adapter.py::test_build_fills_only_what_the_bytes_supply_and_labels_the_rest`
  - `FAILED tests/test_funding_intake_adapter.py::test_unresolved_fields_are_never_fabricated`
  - Summary: `2 failed, 5 passed in 0.18s`.
  - Confirmed: The test suite actively fails when fabrication occurs.

---

## 6. Scope & Diff Verification

[subject/DIFF_STAT_fcac0ac6_HEAD.txt](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/DIFF_STAT_fcac0ac6_HEAD.txt) confirms:
```
 .../tests/test_funding_intake_adapter.py           | 212 ++++++++++++
 IBKR_PAPER_BRIDGE/tools/funding_intake_adapter.py  | 366 +++++++++++++++++++++
 2 files changed, 578 insertions(+)
```
- Exactly two new files added under `IBKR_PAPER_BRIDGE/`.
- `export_mtc_funding.py` is completely untouched.
- No protected runtime paths, trading modules, databases, or execution economics files were modified.

---

## 7. Accepting Half Analysis: What Would Be Required vs. What Is Present

To transform this into the accepting half of production intake, the following changes would be required in `export_mtc_funding.py` and downstream pipelines:
1. **Admitting Real Evidence Kind:** Adding `REAL_CAPTURE_READ_ONLY` to `ACCEPTED_EVIDENCE_KINDS` in `export_mtc_funding.py:110`.
2. **Production Digest Domain:** Defining a production `SOURCE_EVENT_DIGEST_DOMAIN` and replacing `PRODUCTION_MODE_UNAVAILABLE` (line 116).
3. **CLI Production Switch:** Adding and parsing `--mode PRODUCTION` or an equivalent flag.
4. **Production Selection Admission:** Adapting `ExecutionEconomics._resolve_funding` and `EconomicRecords` to consume real captured schedules without raising missing schedule/event errors.
5. **Database Store Ingestion:** Creating schema-v10 Bridge database stores with real historical events.

**Presence in current diff:**
**Zero.** None of these changes exist in the diff. The adapter remains strictly the non-accepting staging draft, labelling every output `NONACCEPTING_INTAKE_DRAFT` and reporting `CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE`.

---

## Findings

- **NIT-01 (subject/test_funding_intake_adapter.py:201–203):** Vacuous clock assertion disjunction.
  `assert (b"2026-09-15T" not in raw or name == "binding_packet_draft.json")` evaluates unconditionally to `True` for `binding_packet_draft.json` due to short-circuit boolean logic. In practice, `funding_intake_adapter.py` never calls `datetime.now()` and uses only captured venue timestamps (`2026-09-14T`), but the test does not actively check `binding_packet_draft.json`. Severity: `NIT`.
- **NIT-02 (subject/funding_intake_adapter.py:145–171):** Proposed completeness witness D-6 does not account for boundary latency or missing events.
  `completeness()` verifies only that boundary ms are multiples of 3,600,000 and that two passes match. It does not account for venue timestamp offsets (+31 to +60 ms) against exclusive end boundaries, nor does it verify that all hours within the window produced an event. Acceptable as a draft proposal, but must be resolved before production admission. Severity: `NIT`.

---

## Read Coverage & Continuations

All 17 files in [PACKET_SHA256SUMS.txt](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/PACKET_SHA256SUMS.txt) were read using native tools with maximum ranges <= 150 lines:
1. `PACKET_SHA256SUMS.txt`: lines 1–18
2. `subject/funding_intake_adapter.py`:
   - Range 1: lines 1–150
   - Range 2: lines 151–300 (continuation 1)
   - Range 3: lines 301–367 (continuation 2)
3. `subject/test_funding_intake_adapter.py`:
   - Range 1: lines 1–150
   - Range 2: lines 151–213 (continuation 1)
4. `subject/P012_FUNDING_INTAKE_DESIGN_20260915.md`: lines 1–49
5. `subject/COMMIT_HEAD.txt`: lines 1–41
6. `subject/DIFF_STAT_fcac0ac6_HEAD.txt`: lines 1–4
7. `sources/export_mtc_funding_fcac0ac6.py`:
   - Range 1: lines 1–150
   - Range 2: lines 151–215 (continuation 1)
   - Range 3: lines 440–589
   - Range 4: lines 590–600 (continuation 2)
8. `sources/capture_own_account_evidence_af921d75.py`: lines 440–510
9. `sources/r1_DERIVED_EXTRACTION.json`: lines 1–1 (complete JSON)
10. `sources/r1_binding_packet_draft.json`: lines 1–82
11. `sources/r1_retained_rows_expected.json`: lines 1–34
12. `sources/r1_intake_gap_report.json`: lines 1–42
13. `sources/LEAD_PYTEST_focused.txt`: lines 1–2
14. `sources/LEAD_RED_ARM_fabrication_fence.txt`: lines 1–9 (`view_file` rejected by cortex mime type check; read completely via native `grep_search` lines 1–9)
15. `sources/LEAD_INTAKE_r1_stdout.txt`: lines 1–5
16. `sources/LEAD_RUFF.txt`: lines 1–2
17. `sources/LEAD_GUARD.txt`: lines 1–5
18. `sources/DECISIONS_rows_P012.md`: lines 1–5

Required scope unread: `[]`.

---

## Non-Empty Not Verified (No Execution)

Because this audit is strictly read-only and unexecuted (`SUPPLEMENTAL_UNEXECUTED`), the following items were not verified through live execution:
1. Live execution of `pytest tests/test_funding_intake_adapter.py` on the host Python interpreter.
2. Live CLI execution of `funding_intake_adapter.py --run-dir ... --out ...`.
3. Independent live run of the red-arm mutation test.
4. Independent execution of repository guard (`LEAD_GUARD.txt`) and linter (`LEAD_RUFF.txt`).
5. Live generation or cryptographic verification of SQLite snapshots and SHA256 sidecars.

---

```json
{
  "part": "P012_INTAKE_GEMINI",
  "verdict": "PASS-WITH-NITS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "fabricated_fields": [],
  "findings": [
    {
      "finding_id": "NIT-01",
      "severity": "NIT",
      "file_path": "subject/test_funding_intake_adapter.py",
      "line_range": "201-203",
      "description": "Vacuous disjunction in clock assertion for binding_packet_draft.json (`b'2026-09-15T' not in raw or name == 'binding_packet_draft.json'`) trivially short-circuits to True."
    },
    {
      "finding_id": "NIT-02",
      "severity": "NIT",
      "file_path": "subject/funding_intake_adapter.py",
      "line_range": "145-171",
      "description": "Proposed completeness witness rule (D-6) checks hour alignment of bounds and pass SHA equality, but does not verify expected event count per hour or venue timestamp offset (+31 to +60 ms) against half-open interval boundaries."
    }
  ],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
