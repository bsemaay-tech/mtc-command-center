# Supplemental Detection Review: WP-P0-12 Funding Intake Slice 4

**Reviewer Role:** Independent Supplemental Read-Only Detection Reviewer (`SUPPLEMENTAL_UNEXECUTED`; no execution capability).  
**Review Target:** WP-P0-12 Funding Intake Slice 4 (`9ef072a8` on `feature/p012-funding-intake-adapter-20260915`), parent `b667dbcc` (format-only), authority `OD-20260916-P012-INTAKE-D1-D6-R-1`.  
**Packet Location:** `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_S4_20260916/`.

---

## 1. Explicit Admission, Not a Toggle (Fence Integrity)

From the semantic patch (`subject/DIFF_semantic_b667dbcc_9ef072a8.patch`) and HEAD inspects of `IBKR_PAPER_BRIDGE/tools/export_mtc_funding.py`:

1. **Profile Selection (CLI & Pure Function):**
   - **CLI:** Selected via `--evidence-kind {REAL_CAPTURE_READ_ONLY,SYNTHETIC_FIXTURE}` (`_parse_args` lines 2120–2129). Defaults strictly to `SYNTHETIC_EVIDENCE_KIND`. No `--mode` argument exists (using `--mode` triggers an argparse error / `SystemExit`).
   - **Pure Function:** Selected via keyword-only parameter `evidence_kind: str = SYNTHETIC_EVIDENCE_KIND` on `build_funding_candidate` (line 1425/2146).
2. **Behavior on Mismatches & Unknown Kinds:**
   - **Caller omits profile (default synthetic) on real packet:** CLI checks `packet["packet_version"] != profile.packet_version` in `_load_packet` (line 1937/2437) and raises `CANDIDATE_PACKET_INVALID`. In the pure function, `_validate_coverage` calls `_require_evidence_kind` (lines 620–636/1518–1534), raising `CANDIDATE_EVIDENCE_KIND_MISMATCH` because `coverage.evidence_kind` is `"REAL_CAPTURE_READ_ONLY"` while caller admitted `"SYNTHETIC_FIXTURE"`.
   - **Caller names real profile on synthetic packet:** `_load_packet` rejects packet version (`CANDIDATE_PACKET_INVALID`). In the pure function, `_require_evidence_kind` raises `CANDIDATE_EVIDENCE_KIND_MISMATCH` because the witness declares `"SYNTHETIC_FIXTURE"` while caller declared `"REAL_CAPTURE_READ_ONLY"`.
   - **One binding's provenance carries another kind:** `_validate_binding` calls `_validate_provenance` (lines 829–844/1678–1697), which calls `_require_evidence_kind(provenance["evidence_kind"], profile)`. Any disagreement immediately refuses with `CANDIDATE_EVIDENCE_KIND_MISMATCH`.
   - **Unknown declared kind:** In pure function, `_resolve_profile` (lines 1403–1415/2123–2136) raises `CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE`. In CLI, argparse rejects it against `choices=sorted(_EVIDENCE_PROFILES)`. In packet coverage/provenance, `_require_evidence_kind` raises `CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE`.
3. **Carried Fence Integrity:**
   - `ACCEPTED_EVIDENCE_KINDS` remains strictly `(SYNTHETIC_EVIDENCE_KIND,)` (unchanged from parent).
   - In `sources/test_mtc_funding_export_carried_fences.py`, lines 1347–1364 (`test_no_literal_evidence_kind_unlocks_production` and `test_the_module_exposes_no_production_switch`) are byte-for-byte unchanged and remain active fences asserting that no literal kind unlocks production and that `ACCEPTED_EVIDENCE_KINDS == (SYNTHETIC_EVIDENCE_KIND,)`.
4. **No Inferencing:**
   - There is **no code path** where `evidence_kind` is inferred from the packet. The caller must explicitly admit the kind; any divergence between caller admission and packet declarations refuses.

---

## 2. D-1..D-6 Fidelity Table

| Rule | Owner Row Text (`sources/DECISIONS_rows_P012.md`) | Implementing Lines (`DIFF_semantic` hunk + HEAD `export_mtc_funding.py`) | Producer A (Packet Field) | Producer B (Tool Re-derivation & Byte Source) | Failing Input Test (`test_mtc_funding_export_real_capture.py`) | Status |
|---|---|---|---|---|---|---|
| **D-1** | `source_event_digest = sha256 over the exact captured bytes of that row, tagged HL_USERFUNDING_ROW_V1, written as <tag>:<hex>` | Hunk `@@ -715,6 +1036,300 @@` lines 1733–1741, 1785–1790, 2068–2079; HEAD lines 897–905, 958–963, 1284–1296 | `binding.source_event_digest`, `coverage.source_witnesses[event_id]` | Re-hashes raw bytes from `extras["funding_pass_bytes"]` indexed by `locator.index`. Verified byte-identical to `source_witnesses` and hashes to `digest_hex`. | `test_d1_digest_must_hash_the_exact_captured_row_bytes_not_a_reserialization`, `test_d1_digest_must_carry_the_ruled_domain_tag`, `test_d1_row_bytes_must_be_the_located_span_of_the_funding_pass` | **VERIFIED** |
| **D-2** | `funding_event_id = hl-funding:<account-short>:<coin>:<time_ms>` | Hunk `@@ -715,6 +1036,300 @@` lines 1935, 2086–2091, 2233–2248; HEAD lines 1152, 1303–1308, 1587–1602 | `binding.funding_event_id` | Re-derived as `f"{REAL_EVENT_ID_PREFIX}:{witness['account_scope']}:{row.coin}:{row.time_ms}"` from the decoded JSON element of the located row span. Checked per-binding and at inventory disposition. | `test_d2_event_id_must_rederive_from_scope_coin_and_stamp`, `test_d2_a_binding_that_locates_another_captured_row_is_refused` | **VERIFIED** |
| **D-3** | `keep the venue stamp verbatim as event_timestamp + interval_hour_utc (floor to the hour) as the schedule key` | Hunk `@@ -715,6 +1036,300 @@` lines 1705–1712, 1791–1801, 2092–2098; HEAD lines 870–876, 964–974, 1309–1315 | `binding.event_timestamp`, `binding.interval_hour_utc` | `_millisecond_text(row.time_ms)` formatted verbatim from venue millisecond integer; `_hour_text(...)` computes floor hour `YYYY-MM-DDTHH:00:00Z`. Required 9th binding key. | `test_d3_stamp_is_verbatim_and_the_hour_key_is_its_floor`, `test_d3_the_hour_key_is_a_required_ninth_binding_field` | **VERIFIED** |
| **D-4** | `production requires an oracle capture at each funding instant, DERIVED_FROM_PAYMENT only as labelled research evidence, never admitted` | Hunk `@@ -715,6 +1036,300 @@` lines 1714–1731; HEAD lines 878–895; Limitations: lines 1375–1378 / 175–178 | `binding.oracle_price_source`, `binding.oracle_price` | Regex `^[0-9a-f]{64}#/\S+$` enforces `<sha256>#<json-pointer>`. Refuses `UNRESOLVED` and any case-insensitive `derived` substring. Tool does not open oracle capture (disclosed naming check). | `test_r1_without_a_named_oracle_capture_refuses_under_d4` (parametrized on `UNRESOLVED:D-4`, `DERIVED_FROM_PAYMENT`, derived formulas, prose, unpointed hex) | **VERIFIED** |
| **D-5** | `REAL_CAPTURE_READ_ONLY admitted only together with D-1 and a witness identity naming the ownership-signature record` | Hunk `@@ -460,17 +617,108 @@` lines 1558–1576; HEAD lines 656–675 | `coverage.witness_identity` | Regex pattern matching `run <id>`, `manifest_sha256=<64hex>`, and `ownership OWNERSHIP_EVIDENCE: VERIFIED <scope>`. Must match `coverage.account_scope`. | `test_d5_witness_identity_must_name_the_ownership_record_for_this_scope` (5 parametrized failure cases) | **VERIFIED** |
| **D-6** | `whole-interval witness = two byte-identical funding passes + hour-aligned window + 1-second end-boundary tolerance + expected-count check fed by fills pass` | Hunk `@@ -460,17 +617,108 @@` lines 1538–1610, 1941–2049, 2215–2251; HEAD lines 639–709, 1158–1264, 1568–1605 | `coverage.funding_witness_passes`, `coverage.fills_witness`, `coverage.interval_*` | Verifies: (a) start/end on whole hours; (b) >= 2 passes byte-identical; (c) pass sha256 equals `provenance.source_sha256`; (d) 1-s end tolerance (`end + 1s`); (e) terminal disposition of all pass rows; (f) fills history continuity; (g) fills-predicted open hours == observed payment hours; (h) row `szi` == fills position. | `test_d6_the_window_must_be_aligned_to_whole_hours`, `test_d6_two_byte_identical_funding_passes_are_required`, `test_d6_the_pass_digest_must_be_the_provenance_source_digest`, `test_d6_one_second_end_tolerance_admits_the_venue_late_stamp`, `test_d6_a_stamp_more_than_one_second_past_the_end_is_out_of_interval`, `test_d6_fills_that_leave_the_position_open_demand_the_missing_payment`, `test_d6_a_row_position_that_disagrees_with_the_fills_refuses`, `test_d6_a_gap_in_the_fills_history_refuses`, `test_d6_fills_that_are_not_venue_fill_rows_refuse`, `test_d6_every_row_inside_the_captured_pass_needs_a_disposition`, `test_d6_a_foreign_coin_row_inside_the_pass_refuses`, `test_d6_an_empty_inventory_cannot_be_witnessed` | **VERIFIED** |

### Specific Rule Checks:
- **D-1 byte span:** `_json_array_spans` (lines 1059–1106) decodes element boundaries and slices exact UTF-8 byte spans `text[index:end].encode("utf-8")`. The raw bytes are directly SHA256 hashed without re-serialization or normalization.
- **D-2 re-derivation:** Derived as `f"{REAL_EVENT_ID_PREFIX}:{account_scope}:{coin}:{time_ms}"` and verified against every binding and pass row.
- **D-3 verbatim stamp & hour key:** Verbatim milliseconds string preserved; `interval_hour_utc` floored to hour.
- **D-4 oracle check:** Enforces `<sha256>#<json-pointer>`, rejects all `UNRESOLVED` and `derived` variants with `CANDIDATE_ORACLE_EVIDENCE_UNAVAILABLE`. Limitation is stated in `REAL_CAPTURE_EVIDENCE_LIMITATIONS`.
- **D-5 tokens:** Enforces `run <id>`, `manifest_sha256=<64hex>`, and `ownership OWNERSHIP_EVIDENCE: VERIFIED <scope>` tied to `account_scope`.
- **D-6 edge cases:** Hour alignment checked; >=2 byte-identical passes checked; pass digest checked against provenance; 1-second late stamp tolerance verified; every captured row given terminal disposition (Pattern 13); fills position checked for continuity and matches each row's `szi`; expected funding hours match observed; empty inventory and uninventoried rows refuse.

---

## 3. Real-Capture Candidate and Report

1. **Root Keys:**
   The real candidate dictionary root has exactly 9 keys:
   `['admission_status', 'artifact_kind', 'bridge_payload_digest_domain', 'evidence_kind', 'not_a_production_record', 'numeric_representation', 'real_capture_candidate', 'source_event_digest_domain', 'synthetic_only']`.
   Confirmed: **No** `events`, `schedule_id`, or `settlement_currency` exist at the candidate root.
2. **Fixed Attributes:**
   - `synthetic_only`: `False`
   - `artifact_kind`: `"REAL_CAPTURE_FUNDING_CANDIDATE_V1"`
   - `admission_status`: `"REFUSED_REAL_CAPTURE_READ_ONLY_NOT_A_PRODUCTION_RECORD"`
   - `evidence_kind`: `"REAL_CAPTURE_READ_ONLY"`
   - `source_event_digest_domain`: `"HL_USERFUNDING_ROW_V1"`
3. **No Overclaim:**
   - `REAL_CAPTURE_NOT_A_PRODUCTION_RECORD`: explicitly affirms that this is not an accepted economic record, not an admitted production input, that `OD-20260914-P012-ADMISSION-Q3` ("Wait") stands, and that it must never be installed as an MTC funding schedule.
   - `REAL_CAPTURE_EVIDENCE_LIMITATIONS`: explicitly discloses that D-4 (oracle capture) and D-5 (manifest/ownership) are naming/digest checks that the tool does not re-open, that completeness applies only to the captured window, and that production admission is refused.
4. **`production_mode` Wording:**
   In `_report`, `production_mode` remains `"UNAVAILABLE_PENDING_SOURCE_EVENT_DIGEST_DOMAIN"`. The constant value's prose is now technically stale because the source event digest domain has been ruled (`HL_USERFUNDING_ROW_V1`), but preserving this exact string is necessary because carried fence `test_no_literal_evidence_kind_unlocks_production` asserts it, and production mode genuinely remains unavailable under Q3. (Noted as a non-blocking wording follow-up).

---

## 4. Adapter Real Packet Field Table (`sources/r1_s4_binding_packet_real_capture.json`)

| JSON Path | Value | Classification | Basis / Ruling Reference |
|---|---|---|---|
| `packet_version` | `"REAL_CAPTURE_FUNDING_BINDING_PACKET_V1"` | TOOL-RULE | `export_mtc_funding.py:150` / `adapter.py:53` |
| `bindings[0].event_timestamp` | `"2026-09-14T17:00:00.041Z"` | DERIVED-UNDER-RULING | D-3; verbatim venue stamp from raw element 0 `time: 1789405200041` |
| `bindings[0].funding_event_id` | `"hl-funding:0x1E26…AC49:BTC:1789405200041"` | DERIVED-UNDER-RULING | D-2; `hl-funding:<short_addr>:<coin>:<time_ms>` |
| `bindings[0].interval_hour_utc` | `"2026-09-14T17:00:00Z"` | DERIVED-UNDER-RULING | D-3; floor hour of event timestamp |
| `bindings[0].oracle_price` | `"UNRESOLVED:D-4"` | UNRESOLVED | D-4; r1 capture carries no oracle read |
| `bindings[0].oracle_price_source` | `"UNRESOLVED:D-4"` | UNRESOLVED | D-4; r1 capture carries no oracle read |
| `bindings[0].positive_rate_payer` | `"LONG"` | TOOL-RULE | `export_mtc_funding.APPROVED_PAYER` |
| `bindings[0].provenance.evidence_kind` | `"REAL_CAPTURE_READ_ONLY"` | DERIVED-UNDER-RULING | D-5; ruled profile name |
| `bindings[0].provenance.extraction_method` | `"capture_own_account_evidence.py tool_sha256=00b3b8f69f0e4870 user_funding_history"` | COPIED | Verbatim manifest response tool metadata |
| `bindings[0].provenance.source_locator` | `"funding_pass1_page001.json#/0"` | COPIED / TOOL-RULE | Manifest response filename + JSON pointer |
| `bindings[0].provenance.source_sha256` | `"6f25ba294ae96dd333f6938bfe103f283559a960463ddfd2ce8757806563578f"` | COPIED | SHA256 of `funding_pass1_page001.json` |
| `bindings[0].provenance.source_title` | `"Hyperliquid userFunding 0x1E26…AC49 run p012-path1-20260914T1500Z-1900Z-r1"` | COPIED | Run and address metadata from manifest |
| `bindings[0].raw_rate` | `"0.0000125"` | COPIED | Verbatim `fundingRate` text from raw pass element 0 |
| `bindings[0].source_event_digest` | `"HL_USERFUNDING_ROW_V1:c45c2b59f2abc06f2710d45af91b6b553ca4019c37ad64d84cbf4f753f894314"` | DERIVED-UNDER-RULING | D-1; `HL_USERFUNDING_ROW_V1:` + SHA256 of exact byte span of raw row 0 |
| `bindings[1].event_timestamp` | `"2026-09-14T18:00:00.060Z"` | DERIVED-UNDER-RULING | D-3; verbatim venue stamp from raw element 1 `time: 1789408800060` |
| `bindings[1].funding_event_id` | `"hl-funding:0x1E26…AC49:BTC:1789408800060"` | DERIVED-UNDER-RULING | D-2; `hl-funding:<short_addr>:<coin>:<time_ms>` |
| `bindings[1].interval_hour_utc` | `"2026-09-14T18:00:00Z"` | DERIVED-UNDER-RULING | D-3; floor hour of event timestamp |
| `bindings[1].oracle_price` | `"UNRESOLVED:D-4"` | UNRESOLVED | D-4; r1 capture carries no oracle read |
| `bindings[1].oracle_price_source` | `"UNRESOLVED:D-4"` | UNRESOLVED | D-4; r1 capture carries no oracle read |
| `bindings[1].positive_rate_payer` | `"LONG"` | TOOL-RULE | `export_mtc_funding.APPROVED_PAYER` |
| `bindings[1].provenance.evidence_kind` | `"REAL_CAPTURE_READ_ONLY"` | DERIVED-UNDER-RULING | D-5; ruled profile name |
| `bindings[1].provenance.extraction_method` | `"capture_own_account_evidence.py tool_sha256=00b3b8f69f0e4870 user_funding_history"` | COPIED | Verbatim manifest response tool metadata |
| `bindings[1].provenance.source_locator` | `"funding_pass1_page001.json#/1"` | COPIED / TOOL-RULE | Manifest response filename + JSON pointer |
| `bindings[1].provenance.source_sha256` | `"6f25ba294ae96dd333f6938bfe103f283559a960463ddfd2ce8757806563578f"` | COPIED | SHA256 of `funding_pass1_page001.json` |
| `bindings[1].provenance.source_title` | `"Hyperliquid userFunding 0x1E26…AC49 run p012-path1-20260914T1500Z-1900Z-r1"` | COPIED | Run and address metadata from manifest |
| `bindings[1].raw_rate` | `"0.0000125"` | COPIED | Verbatim `fundingRate` text from raw pass element 1 |
| `bindings[1].source_event_digest` | `"HL_USERFUNDING_ROW_V1:4b3708109b64afa02188783294759b9b928407d7eb9b8ec9971d709244bad6ca"` | DERIVED-UNDER-RULING | D-1; `HL_USERFUNDING_ROW_V1:` + SHA256 of exact byte span of raw row 1 |
| `coverage.account_scope` | `"0x1E26…AC49"` | COPIED / DERIVED-UNDER-RULING | Short-form address from manifest |
| `coverage.complete` | `true` | TOOL-RULE | Adapter completeness rule assessment |
| `coverage.evidence_kind` | `"REAL_CAPTURE_READ_ONLY"` | DERIVED-UNDER-RULING | D-5; ruled profile name |
| `coverage.expected_event_ids` | `["hl-funding:0x1E26…AC49:BTC:1789405200041", "hl-funding:0x1E26…AC49:BTC:1789408800060"]` | DERIVED-UNDER-RULING | D-2 list of bound event IDs |
| `coverage.fills_witness` | Hex string (length 2356) | COPIED | Exact bytes of raw `fills_pass1_page001.json` |
| `coverage.funding_witness_passes` | `[Hex (433 B), Hex (433 B)]` | COPIED | Exact bytes of raw `funding_pass1` & `funding_pass2` |
| `coverage.interval_end_exclusive` | `"2026-09-14T19:00:00Z"` | COPIED | Verbatim `manifest.window.end` |
| `coverage.interval_start_inclusive` | `"2026-09-14T15:00:00Z"` | COPIED | Verbatim `manifest.window.start` |
| `coverage.source_witnesses` | Mapping of 2 event IDs to hex row bytes | COPIED / DERIVED-UNDER-RULING | D-1 exact raw row byte spans encoded as hex |
| `coverage.symbol` | `"BTC"` | COPIED | Verbatim `manifest.coin` |
| `coverage.unattributed_event_ids` | `[]` | TOOL-RULE | Default empty list |
| `coverage.witness_identity` | `"capture_own_account_evidence.py tool_sha256=00b3b8f69f0e4870 run p012-path1-20260914T1500Z-1900Z-r1; manifest_sha256=c837cf1237e9c2d8dfdad250815ee17fbd28e1cd0f98b901ec508f9ed6c2c9cb; ownership OWNERSHIP_EVIDENCE: VERIFIED 0x1E26…AC49"` | DERIVED-UNDER-RULING | D-5 rule tokens |

**Confirmatory Findings:**
- Oracle fields are strictly `"UNRESOLVED:D-4"`.
- The back-derived price (~`78758.6`) appears **nowhere** in `r1_s4_binding_packet_real_capture.json`, `r1_s4_intake_gap_report.json`, or the adapter output writing paths.
- D-1 digests in the packet match `HL_USERFUNDING_ROW_V1:<sha256>` of the raw row byte spans.
- `witness_identity` carries all required D-5 tokens and exclusively the short-form address `0x1E26…AC49`.

---

## 5. Retained-Row Label Change Review

In `retained_rows_expected.json` and `funding_intake_adapter.py`, `payload_digest` was changed from `"UNRESOLVED:D-1"` to `"UNAVAILABLE:BRIDGE_OBSERVATION_REQUIRED"`.

1. **Correctness:**
   The change is correct. The Bridge's `payload_digest` is the internal digest computed by `FundingEventRecord.digest` (domain `MTC_BRIDGE_FUNDING_PAYLOAD_V1`). This is a normalized Bridge database observation, not a venue source domain. The owner's ruling `OD-20260916-P012-INTAKE-D1-D6-R-1` under D-1 specifically governs `source_event_digest` (`HL_USERFUNDING_ROW_V1`), not the Bridge's internal reconcile digest. Furthermore, `export_mtc_funding.py` enforces `CANDIDATE_DIGEST_DOMAIN_CONFLATION` (lines 1618–1622) if `source_event_digest` ever equals `payload_digest`.
2. **Fence Status:**
   This is a **disclosed correction**, not a silent fence change. The carried fence suite (`tests/test_mtc_funding_export.py`) was not touched, and the change was explicitly documented in the commit message, verification log, and gap report.

---

## 6. Test Suite and Mutant Analysis

1. **Pre-slice RED Arm:**
   `sources/LEAD_RED_ARM_new_tests_vs_4c802e9b.txt` confirms that running the 57 new tests against the pre-slice codebase (`4c802e9b`) results in **57 failures** in 2.00s.
2. **Mutant Discrimination:**
   - **M1 (Tolerance):** Setting `REAL_END_TOLERANCE_SECONDS = 0` triggers failures in `test_d6_one_second_end_tolerance_admits_the_venue_late_stamp` and `test_r1_with_a_named_oracle_capture_materializes_a_labelled_candidate` (`LEAD_MUTANT_M1_tolerance.txt`).
   - **M2 (szi Cross-Check):** Disabling the row position vs. fills check causes `test_d6_a_row_position_that_disagrees_with_the_fills_refuses` to fail (`LEAD_MUTANT_M2_szi.txt`).
   - **M3 (D-1 Raw vs. Canonical):** Comparing canonical re-serialization instead of raw byte span triggers 11 test failures (`LEAD_MUTANT_M3_d1_canonical.txt`), including `test_d1_digest_must_hash_the_exact_captured_row_bytes_not_a_reserialization`.
     *Sharpening Note:* In `test_d1_digest_must_hash_the_exact_captured_row_bytes_not_a_reserialization`, both row bindings are replaced with canonical serialization hashes. The test discriminates on its own and cannot pass for the wrong reason.
   - **M4 (D-5 Identity):** Dropping the D-5 witness identity check triggers 5 failures across all parametrized cases in `test_d5_witness_identity_must_name_the_ownership_record_for_this_scope` (`LEAD_MUTANT_M4_d5.txt`).
3. **Adapter Suite:**
   4 new tests in `test_funding_intake_adapter.py` verify raw byte parsing, D-4 refusal and candidate validation with fixture oracle, missing raw bytes handling, and output determinism.

---

## 7. Leakage, Scope, and Format-Only Commit

1. **Leakage Audit:**
   - Address forms in all outputs and fixtures: Only the short-form address `0x1E26…AC49` / `0x1e26…ac49` (or synthetic `0x1234…5678`) appears. The full 42-character mainnet address is absent.
   - Fills fixture hashes: Synthetic hashes generated via `hashlib.sha256(f"fixture-fill-{seed}".encode()).hexdigest()`.
   - Imports: Clean standard library and local module imports. No network (`urllib`, `requests`, `httpx`), no subprocess, and no credentials or private keys.
2. **Scope:**
   `DIFF_STAT_semantic_b667dbcc_9ef072a8.txt` shows exactly 4 files modified (2 tools, 2 test files) under `IBKR_PAPER_BRIDGE/`. No `bridge/` runtime engine files touched. Repo guard shows `[protected] none`.
3. **Format-Only Commit (`b667dbcc`):**
   Inspection of `subject/DIFF_format_only_4c802e9b_b667dbcc.patch` across 3 complete ranges (lines 1–150, 151–250, 251–301) confirms **pure whitespace and line-reflow formatting** by `ruff format`. No semantic alterations.

---

## 8. Honest Limits

All operational boundaries identified by the Lead are prominently documented in user-facing artifacts:
1. **Schema-v10 Bridge Store Absence:** Clearly stated in `test_mtc_funding_export_real_capture.py` docstring (lines 14–18, 309–313) and `export_mtc_funding.py` docstring (lines 27–31).
2. **D-4 Oracle Naming Check:** Documented in `REAL_CAPTURE_EVIDENCE_LIMITATIONS` item 3 (lines 175–178 in `export_mtc_funding.py`) and emitted into candidate reports.
3. **D-5 Witness Identity Check:** Documented in `REAL_CAPTURE_EVIDENCE_LIMITATIONS` item 2 (lines 171–174 in `export_mtc_funding.py`) and docstrings.
4. **Stale Prose on `PRODUCTION_MODE_UNAVAILABLE`:** Documented in verification log §3 and docstrings.

---

## 9. Findings

- **NIT-1** (`IBKR_PAPER_BRIDGE/tools/export_mtc_funding.py:133`):  
  The constant `PRODUCTION_MODE_UNAVAILABLE = "UNAVAILABLE_PENDING_SOURCE_EVENT_DIGEST_DOMAIN"` has stale prose because the digest domain for real captures has now been ruled under D-1 (`HL_USERFUNDING_ROW_V1`). The constant string was correctly preserved to prevent breaking the carried fence `test_no_literal_evidence_kind_unlocks_production`. Recommend updating wording in a future coordinated fence cleanup.
- **NIT-2** (`IBKR_PAPER_BRIDGE/tools/export_mtc_funding.py:277-284`):  
  Pre-existing `ruff` ISC004 warnings (unparenthesized implicit string concatenation in `EVIDENCE_LIMITATIONS`) were appropriately left unfixed to preserve synthetic candidate byte pins.

*(No REQUIRED findings; no changes requested).*

---

## 10. Exact Read Coverage

All reads performed using native read tools inside `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_S4_20260916/`:

1. `PACKET_SHA256SUMS.txt`: lines 1–34 (complete)
2. `subject/COMMITS_HEAD_and_parent.txt`: lines 1–73 (complete)
3. `subject/DIFF_STAT_semantic_b667dbcc_9ef072a8.txt`: lines 1–6 (complete)
4. `subject/BLOB_OIDS_HEAD.txt`: lines 1–5 (complete)
5. `sources/DECISIONS_rows_P012.md`: lines 1–6 (complete)
6. `sources/P012_INTAKE_DECISIONS_OWNER_PACKET_20260915.md`: lines 1–17 (complete)
7. `sources/LEAD_EXPORTER_r1_real_packet.txt`: lines 1–10 (complete)
8. `sources/LEAD_GUARD_commit1_format.txt`: lines 1–18 (complete)
9. `sources/LEAD_GUARD_commit2_slice.txt`: lines 1–21 (complete)
10. `sources/LEAD_INTAKE_r1_s4_stdout.txt`: lines 1–7 (complete)
11. `sources/LEAD_MUTANT_M1_tolerance.txt`: lines 1–4 (complete)
12. `sources/LEAD_MUTANT_M2_szi.txt`: lines 1–3 (complete)
13. `sources/LEAD_MUTANT_M3_d1_canonical.txt`: lines 1–13 (complete)
14. `sources/LEAD_MUTANT_M4_d5.txt`: lines 1–7 (complete)
15. `sources/LEAD_PYTEST_focused_post_commit_9ef072a8.txt`: lines 1–2 (complete)
16. `sources/LEAD_PYTEST_full_bridge_suite.txt`: lines 1–33 (complete)
17. `sources/LEAD_RED_ARM_new_tests_vs_4c802e9b.txt`: lines 1–9 (complete)
18. `sources/LEAD_RUFF_s4.txt`: lines 1–12 (complete)
19. `sources/test_mtc_funding_export_carried_fences.py`: lines 1–70 and 1330–1375 (ranges complete)
20. `sources/r1_s4_binding_packet_real_capture.json`: lines 1–63 (complete)
21. `sources/r1_s4_intake_gap_report.json`: lines 1–61 (complete)
22. `sources/r1_DERIVED_EXTRACTION.json`: line 1 (complete)
23. `subject/DIFF_format_only_4c802e9b_b667dbcc.patch`: lines 1–150, 151–250, 251–301 (3 ranges, complete)
24. `subject/LEAD_VERIFICATION_P012_INTAKE_S4.md`: lines 1–57 (complete)
25. `subject/DIFF_semantic_b667dbcc_9ef072a8.patch`: lines 1–150, 151–300, 301–450, 451–600, 601–750, 751–900, 901–1050, 1051–1200, 1201–1350, 1351–1500, 1501–1650, 1651–1800, 1801–1950, 1951–2100, 2101–2250, 2251–2400, 2401–2550, 2551–2700, 2701–2900 (19 continuations, 2900 lines complete)
26. `subject/test_mtc_funding_export_real_capture.py`: lines 1–150, 151–300, 301–450, 451–600, 601–750, 751–900, 901–1015 (7 continuations, 1015 lines complete)
27. `subject/funding_intake_adapter.py`: lines 1–150, 151–300, 301–450, 451–622 (4 continuations, 622 lines complete)
28. `subject/export_mtc_funding.py` at HEAD: lines 130–220, 265–330, 615–765, 870–980, 1030–1150, 1151–1250, 1251–1340, 1560–1660, 2110–2215 (9 ranges confirming cited line numbers)

---

## 11. NOT VERIFIED

- **Live Code Execution:** Supplemental reviewer is strictly unexecuted (`SUPPLEMENTAL_UNEXECUTED`). Pytest run outputs, mutant run logs, repo-guard dry runs, and ruff outputs were audited from lead evidence files; no live shell or test command was executed by this reviewer.
- **Production Venue Completeness / Live Database Interaction:** KVM2 live SQLite database interaction, cryptographic signature recovery of the venue ownership record, and live Hyperliquid network checks were not performed.

---

## 12. Review Summary Object

```json
{
  "part": "P012_INTAKE_S4_GEMINI",
  "verdict": "PASS-WITH-NITS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "rules": {
    "D-1": "VERIFIED",
    "D-2": "VERIFIED",
    "D-3": "VERIFIED",
    "D-4": "VERIFIED",
    "D-5": "VERIFIED",
    "D-6": "VERIFIED"
  },
  "fence_changes": [],
  "fabricated_fields": [],
  "findings": [
    {
      "severity": "NIT",
      "location": "IBKR_PAPER_BRIDGE/tools/export_mtc_funding.py:133",
      "description": "PRODUCTION_MODE_UNAVAILABLE constant string carries stale prose ('UNAVAILABLE_PENDING_SOURCE_EVENT_DIGEST_DOMAIN') following D-1 ruling, preserved intentionally to avoid breaking pinned fence assertions."
    },
    {
      "severity": "NIT",
      "location": "IBKR_PAPER_BRIDGE/tools/export_mtc_funding.py:277-284",
      "description": "Pre-existing ruff ISC004 formatting warnings in EVIDENCE_LIMITATIONS tuple preserved intentionally to maintain candidate byte reproducibility."
    }
  ],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
