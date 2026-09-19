### Review Report: WP-P0-12 Funding Intake Adapter (Detection Pass, Attempt 2)

**Evaluator Role:** `gemini-3.8-flash-high` (Independent Supplemental Read-Only Detection Reviewer; `SUPPLEMENTAL_UNEXECUTED`).  
**Commit Inspected:** [`65c4bc40`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/COMMIT_HEAD.txt#L1) (tightened no-wall-clock assertion; adapter bytes identical to `004a0711`).  
**Target Under Review:** [`subject/funding_intake_adapter.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/funding_intake_adapter.py), [`subject/test_funding_intake_adapter.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/test_funding_intake_adapter.py), [`subject/P012_FUNDING_INTAKE_DESIGN_20260915.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/P012_FUNDING_INTAKE_DESIGN_20260915.md).

---

### 1. Fabrication Audit (Field by Field)

Audit of all fields in [`r1_binding_packet_draft.json`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/r1_binding_packet_draft.json) (`bindings[*]` and `coverage`):

| Scope / Path | Value in `r1_binding_packet_draft.json` | Classification | Basis & Provenance Citation |
|---|---|---|---|
| `bindings[*].event_timestamp` | `"2026-09-14T17:00:00.041Z"`, `"2026-09-14T18:00:00.060Z"` | **COPIED** | Exact UTC conversion of venue millisecond timestamp (`time: 1789405200041`, `1789408800060`) in [`r1_DERIVED_EXTRACTION.json`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/r1_DERIVED_EXTRACTION.json#L1). |
| `bindings[*].funding_event_id` | `"hl-funding:0x1E26…AC49:BTC:1789405200041"`, `"...:1789408800060"` | **DERIVED-LABELLED** | Constructed via proposed rule `hl-funding:<account-short>:<coin>:<time_ms>` ([`funding_intake_adapter.py:209`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/funding_intake_adapter.py#L209)). Accompanied by explicit rule label. |
| `bindings[*].funding_event_id_rule` | `"PROPOSED:D-2 hl-funding:<account-short>:<coin>:<time_ms>"` | **DERIVED-LABELLED** | Explicit metadata disclosing proposed D-2 decision rule. |
| `bindings[*].observed.szi` | `"0.00058"` | **COPIED** | Verbatim from [`r1_DERIVED_EXTRACTION.json`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/r1_DERIVED_EXTRACTION.json#L1) (`szi`). |
| `bindings[*].observed.usdc` | `"-0.000571"`, `"-0.000572"` | **COPIED** | Verbatim from [`r1_DERIVED_EXTRACTION.json`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/r1_DERIVED_EXTRACTION.json#L1) (`usdc`). |
| `bindings[*].observed.venue_hash` | `"0x0000000000000000000000000000000000000000000000000000000000000000"` | **COPIED** | Verbatim from [`r1_DERIVED_EXTRACTION.json`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/r1_DERIVED_EXTRACTION.json#L1) (`hash`). |
| `bindings[*].oracle_price` | `"UNRESOLVED:D-4"` | **UNRESOLVED** | Gapped; not in captured row. Arithmetic derivation explicitly refused. |
| `bindings[*].oracle_price_source` | `"UNRESOLVED:D-4"` | **UNRESOLVED** | Gapped; not in captured row. |
| `bindings[*].positive_rate_payer` | `"LONG"` | **TOOL-RULE** | Verbatim constant [`export_mtc_funding_fcac0ac6.py:122`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L122) (`APPROVED_PAYER = "LONG"`). |
| `bindings[*].positive_rate_payer_basis` | `"export_mtc_funding.APPROVED_PAYER (tool constant)"` | **TOOL-RULE** | Explicit citation of export tool constant. |
| `bindings[*].provenance.evidence_kind` | `"REAL_CAPTURE_READ_ONLY"` | **DERIVED-LABELLED** | Proposed new evidence kind under D-5. |
| `bindings[*].provenance.evidence_kind_status` | `"UNRESOLVED:D-5"` | **UNRESOLVED** | Gapped; export tool currently only admits `SYNTHETIC_FIXTURE`. |
| `bindings[*].provenance.extraction_method` | `"capture_own_account_evidence.py tool_sha256=00b3b8f69f0e4870 user_funding_history"` | **COPIED** | Composed from manifest `responses[0].tool_sha256[:16]` + capture extraction method. |
| `bindings[*].provenance.source_locator` | `"funding_pass1_page001.json#/0"`, `"...#/1"` | **COPIED** | Manifest pass 1 file + `json_pointer` in [`r1_DERIVED_EXTRACTION.json`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/r1_DERIVED_EXTRACTION.json#L1). |
| `bindings[*].provenance.source_sha256` | `"6f25ba294ae96dd333f6938bfe103f283559a960463ddfd2ce8757806563578f"` | **COPIED** | Verbatim `capture_sha256` in [`r1_DERIVED_EXTRACTION.json`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/r1_DERIVED_EXTRACTION.json#L1). |
| `bindings[*].provenance.source_title` | `"Hyperliquid userFunding 0x1E26…AC49 run p012-path1-20260914T1500Z-1900Z-r1"` | **COPIED** | Composed from short address + manifest `run_id`. |
| `bindings[*].raw_rate` | `"0.0000125"` | **COPIED** | Verbatim `fundingRate` from [`r1_DERIVED_EXTRACTION.json`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/r1_DERIVED_EXTRACTION.json#L1). |
| `bindings[*].source_event_digest` | `"UNRESOLVED:D-1"` | **UNRESOLVED** | Gapped; byte domain not defined for production. |
| `coverage.account_scope` | `"0x1E26…AC49"` | **COPIED** | Short form of manifest `address`. |
| `coverage.complete` | `true` | **DERIVED-LABELLED** | Boolean output of proposed witness rule D-6 ([`funding_intake_adapter.py:145-171`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/funding_intake_adapter.py#L145-L171)). Accompanied by `witness_rule`. |
| `coverage.evidence_kind` | `"REAL_CAPTURE_READ_ONLY"` | **DERIVED-LABELLED** | Proposed kind under D-5. |
| `coverage.expected_event_ids` | `["hl-funding:0x1E26…AC49:BTC:1789405200041", "hl-funding:0x1E26…AC49:BTC:1789408800060"]` | **DERIVED-LABELLED** | Matches `bindings[*].funding_event_id`. |
| `coverage.interval_end_exclusive` | `"2026-09-14T19:00:00Z"` | **COPIED** | Verbatim manifest `window.end`. |
| `coverage.interval_start_inclusive` | `"2026-09-14T15:00:00Z"` | **COPIED** | Verbatim manifest `window.start`. |
| `coverage.source_witnesses` | `[{"file": "funding_pass1_page001.json", "sha256": "..."}, {"file": "funding_pass2_page001.json", "sha256": "..."}]` | **COPIED** | Verbatim from manifest `responses`. |
| `coverage.symbol` | `"BTC"` | **COPIED** | Verbatim from manifest `coin`. |
| `coverage.unattributed_event_ids` | `[]` | **TOOL-RULE** | Export tool closed domain `COVERAGE_KEYS`; empty for single-account capture. |
| `coverage.witness_identity` | `"capture_own_account_evidence.py tool_sha256=00b3b8f69f0e4870 run ...; ownership OWNERSHIP_EVIDENCE: VERIFIED 0x1E26…AC49"` | **COPIED** | Composed from manifest `responses[0].tool_sha256`, `run_id`, and `ownership_evidence`. |
| `coverage.witness_reasons` | `[]` | **DERIVED-LABELLED** | Evaluation output from `completeness()`. |
| `coverage.witness_rule` | `"hour-aligned window AND two byte-identical funding passes (proposed D-6)"` | **DERIVED-LABELLED** | Explicit definition of the proposed witness rule. |

* **Oracle Price Check:** CONFIRMED. No oracle price is fabricated or back-derived. The arithmetic derivation `usdc / (szi × rate)` ≈ `78758.6` does not appear anywhere in `binding_packet_draft.json`, `retained_rows_expected.json`, or `intake_gap_report.json`. Both `oracle_price` and `oracle_price_source` carry `"UNRESOLVED:D-4"`.
* **Positive Rate Payer Check:** CONFIRMED. `positive_rate_payer = "LONG"` is an exact match for [`export_mtc_funding_fcac0ac6.py:122`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L122) (`APPROVED_PAYER = "LONG"`).

---

### 2. Design-Note Honesty

All claims in [`P012_FUNDING_INTAKE_DESIGN_20260915.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/P012_FUNDING_INTAKE_DESIGN_20260915.md) were verified against [`export_mtc_funding_fcac0ac6.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py):
1. **No `--mode` argument:** CONFIRMED. The CLI specification ([`export_mtc_funding_fcac0ac6.py:59-63`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L59-L63)) defines only `--snapshot`, `--bindings`, `--symbol`, `--start`, `--end`, `--schedule-id`, and `--staging`. Production mode is fixed as `PRODUCTION_MODE_UNAVAILABLE = "UNAVAILABLE_PENDING_SOURCE_EVENT_DIGEST_DOMAIN"` ([`:116`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L116)), and docstrings confirm no mode switch exists ([`:23-28`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L23-L28)).
2. **Only accepts `SYNTHETIC_FIXTURE`:** CONFIRMED. `ACCEPTED_EVIDENCE_KINDS = (SYNTHETIC_EVIDENCE_KIND,)` where `SYNTHETIC_EVIDENCE_KIND = "SYNTHETIC_FIXTURE"` ([`:109-110`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L109-L110)).
3. **Refuses other evidence with `CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE`:** CONFIRMED. Explicitly raised in coverage validation ([`:468-473`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L468-L473)) and provenance validation ([`:569-575`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L569-L575)).
4. **Decisions D-1..D-6 map to real gaps in closed domains:**
   - **D-1 (`source_event_digest` domain):** Tool requires `source_event_digest` in `BINDING_KEYS` ([`:175`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L175)), but defines only `SYNTHETIC_SOURCE_EVENT_DIGEST_V1` ([`:111`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L111)). Real gap.
   - **D-2 (`funding_event_id` rule):** Tool requires `funding_event_id` in `BINDING_KEYS` ([`:169`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L169)), but Hyperliquid returns zero hashes (`0x00...0`) for funding rows ([`capture_own_account_evidence_af921d75.py:497`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/capture_own_account_evidence_af921d75.py#L497)). Real gap.
   - **D-3 (`event_timestamp` verbatim vs hour boundary):** Venue stamps are offset past the hour (+41 to +60 ms); tool expects ISO-8601 instant ([`:168`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L168)). Real gap.
   - **D-4 (`oracle_price` source):** Required in `BINDING_KEYS` ([`:170-171`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L170-L171)), but absent from venue funding payload. Real gap.
   - **D-5 (`evidence_kind` admission):** Only `SYNTHETIC_FIXTURE` is admitted ([`:110`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L110)). Real gap.
   - **D-6 (whole-interval completion witness):** `_validate_coverage` requires `complete: True` ([`:474-479`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L474-L479)), but provides no rule for certifying a real read-only capture. Real gap.

---

### 3. Completeness Rule Analysis

1. **Soundness & Labelling:** `completeness()` ([`funding_intake_adapter.py:145-171`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/funding_intake_adapter.py#L145-L171)) requires `start_ms % 3_600_000 == 0`, `end_ms % 3_600_000 == 0`, `end_ms > start_ms`, and at least two passes with identical sha256 digests. It is explicitly labelled as `"hour-aligned window AND two byte-identical funding passes (proposed D-6)"` and reported under `unresolved_fields` in `intake_gap_report.json` as an adapter proposal, never as the export tool's approved witness.
2. **Boundary Jitter Edge Case:** Venue funding timestamps sit 41–60 ms past the hour (e.g., `1789405200041` for 17:00Z). In `r1`, the query interval is half-open `[15:00:00Z, 19:00:00Z)` exclusive. If a funding event occurred for the 19:00 hour, Hyperliquid stamps it at `19:00:00.041Z`. Because `19:00:00.041Z > 19:00:00.000Z`, it is excluded by the half-open exclusive upper bound. `completeness()` checks window boundary alignment and pass equality, but does not assert expected event counts. This edge case is discussed under decision D-3 in the design note ([`P012_FUNDING_INTAKE_DESIGN_20260915.md:20`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/P012_FUNDING_INTAKE_DESIGN_20260915.md#L20)), confirming that the adapter does not claim or finalize production settlement semantics.

---

### 4. Leakage Audit

1. **Address Obfuscation:** The full 42-character mainnet address (`0x1e26...ac49`) is converted to 12-character short form (`address[:6] + "…" + address[-4:]` → `0x1E26…AC49`) in [`funding_intake_adapter.py:87-96`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/funding_intake_adapter.py#L87-L96). In `test_funding_intake_adapter.py:121`, `assert ADDRESS not in json.dumps(intake)` explicitly asserts that the full address never leaves the adapter. All output files carry only `0x1E26…AC49`.
2. **Credentials & Secrets:** The adapter imports only standard libraries (`argparse`, `hashlib`, `json`, `sys`, `datetime`, `pathlib`, `typing`). It performs no network I/O, does not access environment variables or keys, and reads only `CAPTURE_MANIFEST.json` and `DERIVED_EXTRACTION.json` from the provided `--run-dir`. No credential leakage is possible.

---

### 5. Test Suite Verification

1. **`test_build_fills_only_what_the_bytes_supply_and_labels_the_rest`:** Proves valid mapping of fillable fields, `UNRESOLVED:D-n` labels for unfillable fields, address truncation, and refusal code formatting.
2. **`test_unresolved_fields_are_never_fabricated`:** Proves no unresolved field is filled and asserts that arithmetic back-derivation numbers (`78758` / `78759`) are completely absent from serialized output.
3. **`test_completeness_rule_hour_alignment_and_identical_passes`:** Proves `complete=False` when window bounds are unaligned or when funding passes differ in sha256.
4. **`test_refuses_foreign_coin_malformed_rows_and_bad_labels`:** Proves rejection of coin mismatches, non-integer timestamps, and invalid row kinds.
5. **`test_load_refuses_wrong_kinds_and_duplicate_keys`:** Proves strict rejection of non-v1 manifests and duplicate JSON members.
6. **`test_outputs_are_deterministic_write_once_and_clock_free`:** Proves bit-for-bit output determinism, write-once directory enforcement, and absence of current wall-clock dates (`set(re.findall(rb"\d{4}-\d{2}-\d{2}T", raw)) <= {b"2026-09-14T"}`).
   - *Attempt 2 Verification:* [`LEAD_RED_ARM_nit01_wall_clock.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/LEAD_RED_ARM_nit01_wall_clock.txt) proves that a mutant injecting `generated_at=2026-09-15T17:00:00+00:00` fails at line 203 (`1 failed, 6 passed`).
7. **`test_main_end_to_end`:** Proves full CLI invocation returns 0 on fresh output directory and 3 (`INTAKE_OUTPUT_EXISTS`) on re-run.
8. **Fabrication Fence Mutant Arm:** If a mutant fills `oracle_price` via arithmetic, both `test_build_fills_only_what_the_bytes_supply_and_labels_the_rest` and `test_unresolved_fields_are_never_fabricated` fail on the literal value and absence checks.

---

### 6. Scope & Repository Integrity

Inspection of [`DIFF_STAT_fcac0ac6_HEAD.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/DIFF_STAT_fcac0ac6_HEAD.txt):
* Exactly two files added: `IBKR_PAPER_BRIDGE/tests/test_funding_intake_adapter.py` (212 lines) and `IBKR_PAPER_BRIDGE/tools/funding_intake_adapter.py` (366 lines).
* `export_mtc_funding.py` is untouched (0 changes).
* No protected paths, config files, or live database scripts were modified.
* [`LEAD_GUARD_nit01.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/LEAD_GUARD_nit01.txt) confirms `RESULT: PASS` with 0 protected files touched.

---

### 7. Non-Accepting Boundaries

For `export_mtc_funding.py` to become an accepting tool for real evidence, the following 6 changes would be required:
1. Admitting a new evidence kind (e.g., `REAL_CAPTURE_READ_ONLY`) in `ACCEPTED_EVIDENCE_KINDS` ([`:110`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L110)).
2. Defining a production byte domain for `SOURCE_EVENT_DIGEST_DOMAIN` ([`:111`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L111)).
3. Introducing a `--mode` CLI parameter ([`:59-63`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L59-L63)).
4. Removing or replacing the refusal checks in `_validate_coverage` ([`:470`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L470)) and `_validate_provenance` ([`:572`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L572)).
5. Emitting production records admitted by `EconomicRecords.funding_schedule_id` ([`:19-25`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L19-L25)).
6. Reading or writing active database instances ([`:30-38`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L30-L38)).

**None of these changes exist in the diff.** The adapter acts strictly as a non-accepting staging tool.

---

### Findings

* **`NIT-01` (Resolved in HEAD `65c4bc40`):** Determinism test previously exempted `binding_packet_draft.json` from wall-clock checks; resolved by asserting all output date stamps match `{b"2026-09-14T"}` ([`test_funding_intake_adapter.py:203`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/test_funding_intake_adapter.py#L203)).
* **`NIT-02` (Documentation / Specification Clarity):** [`subject/P012_FUNDING_INTAKE_DESIGN_20260915.md:27`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/P012_FUNDING_INTAKE_DESIGN_20260915.md#L27) states that window boundaries being hour-aligned ensures "no funding instant can fall outside the captured range". Because venue funding timestamps jitter +31 to +60 ms past the hour, a half-open window `[T0, T1)` ending at `T1 = HH:00:00Z` excludes the funding event stamped at `HH:00:00.041Z`. When D-6 and D-3 are formally resolved for production, the specification should document whether boundary funding events belong to the preceding or succeeding interval.

---

### Exact Read Coverage

All reads performed within `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915`:
1. `PACKET_SHA256SUMS.txt`: lines 1–21 (complete).
2. `subject/funding_intake_adapter.py`: lines 1–150; continuation lines 151–300; continuation lines 301–367 (complete, 367 lines).
3. `subject/test_funding_intake_adapter.py`: lines 1–150; continuation lines 151–213 (complete, 213 lines).
4. `subject/P012_FUNDING_INTAKE_DESIGN_20260915.md`: lines 1–49 (complete, 49 lines).
5. `subject/COMMIT_HEAD.txt`: lines 1–16 (complete).
6. `subject/DIFF_STAT_fcac0ac6_HEAD.txt`: lines 1–4 (complete).
7. `sources/export_mtc_funding_fcac0ac6.py`: lines 1–150; continuation lines 151–215; lines 440–520; continuation lines 521–600.
8. `sources/capture_own_account_evidence_af921d75.py`: lines 440–510 (complete range).
9. `sources/r1_DERIVED_EXTRACTION.json`: line 1 (complete, 2141 bytes).
10. `sources/r1_binding_packet_draft.json`: lines 1–82 (complete).
11. `sources/r1_retained_rows_expected.json`: lines 1–34 (complete).
12. `sources/r1_intake_gap_report.json`: lines 1–42 (complete).
13. `sources/LEAD_PYTEST_focused.txt`: lines 1–2 (complete).
14. `sources/LEAD_INTAKE_r1_stdout.txt`: lines 1–5 (complete).
15. `sources/LEAD_RUFF.txt`: lines 1–2 (complete).
16. `sources/LEAD_GUARD.txt`: lines 1–5 (complete).
17. `sources/DECISIONS_rows_P012.md`: lines 1–5 (complete).
18. `sources/LEAD_RED_ARM_nit01_wall_clock.txt`: lines 1–10 (complete).
19. `sources/LEAD_GUARD_nit01.txt`: lines 1–14 (complete).
20. `sources/LEAD_RED_ARM_fabrication_fence.txt`: Read attempted via `view_file` (failed with cortex environment error: `unsupported mime type text/plain; charset=utf-8`).

---

### Nonempty NOT VERIFIED

1. **No Execution:** As a `SUPPLEMENTAL_UNEXECUTED` reviewer, no pytest suite, CLI commands, git mutations, or Python scripts were executed. Results rely on verbatim lead artifact logs and static code analysis.
2. **Unread Tool Artifact:** `sources/LEAD_RED_ARM_fabrication_fence.txt` could not be viewed due to cortex tool permission/mime-type conversion error (`unsupported mime type text/plain; charset=utf-8`). Fence test mechanics were verified by source inspection of `test_funding_intake_adapter.py:114-115, 135-145`.

---

```json
{
  "part": "P012_INTAKE_GEMINI",
  "verdict": "PASS-WITH-NITS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "fabricated_fields": [],
  "findings": [
    {
      "finding_id": "NIT-02",
      "severity": "NIT",
      "path": "subject/P012_FUNDING_INTAKE_DESIGN_20260915.md:27",
      "description": "The D-6 completeness rule assumes hour-alignment ensures no funding event falls outside the window. Due to ~41-60ms venue funding timestamp jitter, a half-open window ending at HH:00:00Z excludes the boundary funding event stamped at HH:00:00.041Z. The production specification should formally document boundary allocation semantics."
    }
  ],
  "required_scope_unread": [
    "sources/LEAD_RED_ARM_fabrication_fence.txt"
  ]
}
```

GEMINI_READ_ONLY_OK
