# SUPPLEMENTAL READ-ONLY DETECTION AUDIT: WP-P0-12 FUNDING INTAKE ADAPTER

**Reviewer**: `gemini-3.8-flash-high` (Supplemental Detection Reviewer; `SUPPLEMENTAL_UNEXECUTED`)  
**Commit Inspected**: `65c4bc4012adb528c2ac6a228b3f067bda298aa9` (`subject/COMMIT_HEAD.txt`)  
**Scope**: Packet `_gemini_packets_20260913/P012_INTAKE_20260915`  

---

## 1. Field-by-Field Fabrication Audit

Every key in `sources/r1_binding_packet_draft.json` (`bindings[*]`, `coverage`, and root) has been inspected against `sources/r1_DERIVED_EXTRACTION.json`, `sources/capture_own_account_evidence_af921d75.py`, and `sources/export_mtc_funding_fcac0ac6.py`.

### Classification Taxonomy
- **COPIED**: Verbatim from captured bytes / derived view / manifest.
- **TOOL-RULE**: Constant or fixed requirement explicitly defined by `export_mtc_funding.py` (line cited).
- **DERIVED-LABELLED**: Computed / transformed, but carrying an explicit proposed rule label (e.g. `PROPOSED:D-2`).
- **UNRESOLVED**: Explicit sentinel `UNRESOLVED:D-n` marking an unapproved domain or missing production input.

| Location | Key | Value in Draft | Classification | Provenance / Evidence & Notes |
|---|---|---|---|---|
| Root | `label` | `"NONACCEPTING_INTAKE_DRAFT"` | TOOL-RULE | `funding_intake_adapter.py:31`, prevents downstream acceptance |
| Root | `adapter_version` | `"p012-funding-intake/v1"` | DERIVED-LABELLED | Adapter software version identifier |
| Root | `packet_version` | `"SYNTHETIC_FUNDING_BINDING_PACKET_V1"` | TOOL-RULE | `export_mtc_funding.py:108` (`PACKET_VERSION`) |
| `bindings[*]` | `event_timestamp` | `"2026-09-14T17:00:00.041Z"`, `"2026-09-14T18:00:00.060Z"` | COPIED | ISO 8601 UTC Z formatting of `time` ms from derived view (`1789405200041`, `1789408800060`); ms preserved verbatim (D-3) |
| `bindings[*]` | `funding_event_id` | `"hl-funding:0x1E26…AC49:BTC:1789405200041"`, `"hl-funding:0x1E26…AC49:BTC:1789408800060"` | DERIVED-LABELLED | Deterministic synthetic ID derived from short address, coin, and time ms (venue `hash` is zero) |
| `bindings[*]` | `funding_event_id_rule` | `"PROPOSED:D-2 hl-funding:<account-short>:<coin>:<time_ms>"` | DERIVED-LABELLED | Explicit label naming proposed decision D-2 rule |
| `bindings[*]` | `observed.szi` | `"0.00058"` | COPIED | Verbatim from `r1_DERIVED_EXTRACTION.json` `funding[*].szi` |
| `bindings[*]` | `observed.usdc` | `"-0.000571"`, `"-0.000572"` | COPIED | Verbatim from `r1_DERIVED_EXTRACTION.json` `funding[*].usdc` |
| `bindings[*]` | `observed.venue_hash` | `"0x0000000000000000000000000000000000000000000000000000000000000000"` | COPIED | Verbatim from `r1_DERIVED_EXTRACTION.json` `funding[*].hash` |
| `bindings[*]` | `oracle_price` | `"UNRESOLVED:D-4"` | UNRESOLVED | **Zero fabrication**: Arithmetic back-calculation (`usdc / (szi × rate) ≈ 78758.6`) is **not** performed |
| `bindings[*]` | `oracle_price_source` | `"UNRESOLVED:D-4"` | UNRESOLVED | Marked unresolved under decision D-4 |
| `bindings[*]` | `positive_rate_payer` | `"LONG"` | TOOL-RULE | Verbatim constant `APPROVED_PAYER = "LONG"` from `export_mtc_funding.py:122` |
| `bindings[*]` | `positive_rate_payer_basis` | `"export_mtc_funding.APPROVED_PAYER (tool constant)"` | TOOL-RULE | Explicit citation of export tool constant |
| `bindings[*]` | `provenance.evidence_kind` | `"REAL_CAPTURE_READ_ONLY"` | DERIVED-LABELLED | Proposed evidence kind for read-only captures |
| `bindings[*]` | `provenance.evidence_kind_status` | `"UNRESOLVED:D-5"` | UNRESOLVED | Marked unresolved under decision D-5 (refused by export tool) |
| `bindings[*]` | `provenance.extraction_method` | `"capture_own_account_evidence.py tool_sha256=00b3b8f69f0e4870 user_funding_history"` | DERIVED-LABELLED | Constructed from tool SHA-256 prefix in manifest and capture method |
| `bindings[*]` | `provenance.source_locator` | `"funding_pass1_page001.json#/0"`, `"funding_pass1_page001.json#/1"` | COPIED | Pass 1 filename resolved via digest from manifest + `json_pointer` |
| `bindings[*]` | `provenance.source_sha256` | `"6f25ba294ae96dd333f6938bfe103f283559a960463ddfd2ce8757806563578f"` | COPIED | Verbatim from `r1_DERIVED_EXTRACTION.json` `funding[*].capture_sha256` |
| `bindings[*]` | `provenance.source_title` | `"Hyperliquid userFunding 0x1E26…AC49 run p012-path1-20260914T1500Z-1900Z-r1"` | DERIVED-LABELLED | Short address + manifest `run_id` |
| `bindings[*]` | `raw_rate` | `"0.0000125"` | COPIED | Verbatim from `r1_DERIVED_EXTRACTION.json` `funding[*].fundingRate` |
| `bindings[*]` | `source_event_digest` | `"UNRESOLVED:D-1"` | UNRESOLVED | Marked unresolved under decision D-1 (production domain undefined) |
| `coverage` | `account_scope` | `"0x1E26…AC49"` | DERIVED-LABELLED | `short_address(manifest["address"])` |
| `coverage` | `complete` | `true` | DERIVED-LABELLED | Proposed D-6 rule evaluation (hour-aligned window + byte-identical passes) |
| `coverage` | `evidence_kind` | `"REAL_CAPTURE_READ_ONLY"` | DERIVED-LABELLED | Proposed evidence kind |
| `coverage` | `expected_event_ids` | `["hl-funding:0x1E26…AC49:BTC:1789405200041", "hl-funding:0x1E26…AC49:BTC:1789408800060"]` | DERIVED-LABELLED | Derived event IDs matching `bindings[*].funding_event_id` |
| `coverage` | `interval_end_exclusive` | `"2026-09-14T19:00:00Z"` | COPIED | Verbatim from `manifest["window"]["end"]` |
| `coverage` | `interval_start_inclusive` | `"2026-09-14T15:00:00Z"` | COPIED | Verbatim from `manifest["window"]["start"]` |
| `coverage` | `source_witnesses` | Pass 1 and Pass 2 files + SHA-256s | COPIED | Verbatim file and digest pairs from manifest `responses` |
| `coverage` | `symbol` | `"BTC"` | COPIED | Verbatim from `manifest["coin"]` |
| `coverage` | `unattributed_event_ids` | `[]` | TOOL-RULE | Required closed field `COVERAGE_KEYS` (`export_mtc_funding.py:201`) |
| `coverage` | `witness_identity` | `"capture_own_account_evidence.py tool_sha256=00b3b8f69f0e4870 run p012-path1-20260914T1500Z-1900Z-r1; ownership OWNERSHIP_EVIDENCE: VERIFIED 0x1E26…AC49"` | DERIVED-LABELLED | Tool SHA, run ID, and verified ownership status with short address |
| `coverage` | `witness_reasons` | `[]` | DERIVED-LABELLED | Reason list from completeness check |
| `coverage` | `witness_rule` | `"hour-aligned window AND two byte-identical funding passes (proposed D-6)"` | DERIVED-LABELLED | Explicit proposed witness rule declaration |

### Retained Rows Shape (`sources/r1_retained_rows_expected.json`)
- `attribution`: `"0x1E26…AC49"` (DERIVED-LABELLED, short address).
- `event_id`: `"hl-funding:0x1E26…AC49:BTC:..."` (DERIVED-LABELLED, proposed D-2).
- `ledger_effective_ts`: Preserved venue timestamp ISO string (COPIED).
- `payload`: Normalized dict containing `coin`, `fundingRate`, `szi`, `usdc` (COPIED).
- `payload_digest`: `"UNRESOLVED:D-1"` (UNRESOLVED).
- `payload_reason`: `"FUNDING_PAYLOAD_RETAINED"` (TOOL-RULE, `export_mtc_funding.py:126`).
- `symbol`: `"BTC"` (COPIED).

**Fabrication Audit Verdict**: **ZERO FABRICATION DETECTED**. No oracle price was guessed or computed. No unlabelled values exist.

---

## 2. Design-Note Honesty

The claims in `subject/P012_FUNDING_INTAKE_DESIGN_20260915.md` were checked against `sources/export_mtc_funding_fcac0ac6.py`:
1. **No `--mode` argument**: Verified. `_parse_args` (`export_mtc_funding.py:1358-1374`) accepts only `--snapshot`, `--bindings`, `--symbol`, `--start`, `--end`, `--schedule-id`, and `--staging`. No `--mode` option exists.
2. **Production mode unavailable**: Verified. `export_mtc_funding.py:116` defines `PRODUCTION_MODE_UNAVAILABLE = "UNAVAILABLE_PENDING_SOURCE_EVENT_DIGEST_DOMAIN"`.
3. **Accepts only `SYNTHETIC_FIXTURE`**: Verified. Line 109 defines `SYNTHETIC_EVIDENCE_KIND = "SYNTHETIC_FIXTURE"`, and line 110 fixes `ACCEPTED_EVIDENCE_KINDS = (SYNTHETIC_EVIDENCE_KIND,)`.
4. **Refuses all other evidence kinds with `CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE`**: Verified. Both coverage validation (`export_mtc_funding.py:468-473`) and provenance validation (`export_mtc_funding.py:569-575`) reject any evidence kind not in `ACCEPTED_EVIDENCE_KINDS` with `CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE`.
5. **Mapping of Decisions D-1..D-6 to Real Gaps**:
   - **D-1 (`source_event_digest` byte domain)**: Export tool only defines `SYNTHETIC_SOURCE_EVENT_DIGEST_V1` (`:111`). No production byte domain exists.
   - **D-2 (`funding_event_id` rule)**: Real venue returns `0x000...0` for funding row hashes (`capture_own_account_evidence.py:497`). The export tool requires unique event IDs (`:160, :169`), but defines no rule for synthesizing IDs from zero-hash venue events.
   - **D-3 (`event_timestamp` alignment)**: Real funding events have ms offsets (e.g. `17:00:00.041Z`). The export tool requires ISO timestamps (`:161, :168`), but does not specify whether to retain venue physical timestamps or floor to schedule boundaries.
   - **D-4 (`oracle_price` & source)**: Required by export tool (`:170-171`), but absent from Hyperliquid `userFunding` API rows.
   - **D-5 (`evidence_kind` admission)**: Export tool is closed to anything outside `SYNTHETIC_FIXTURE` (`:110`).
   - **D-6 (Whole-interval witness)**: Export tool specifies no verification mechanism for live API captures (`:208`).

All design-note claims are strictly honest and faithfully reflect repository realities.

---

## 3. Completeness Rule Analysis

In `subject/funding_intake_adapter.py:145-171`, `completeness()` asserts `complete: true` when:
1. `start_ms % HOUR_MS == 0` and `end_ms % HOUR_MS == 0` (bounds are hour-aligned);
2. `end_ms > start_ms` (non-empty window);
3. Two or more funding passes exist (`len(passes) >= 2`);
4. All funding passes share identical SHA-256 digests (`len(set(passes.values())) == 1`).

### Soundness and Labelling
- The rule is clearly labelled in both code and outputs as proposed: `"rule": "hour-aligned window AND two byte-identical funding passes (proposed D-6)"` (`funding_intake_adapter.py:165, :273`) and in the gap report under `unresolved_fields` (`:292`). It makes no pretense of being an export-tool-approved witness.

### Boundary Jitter Vulnerability
- Hyperliquid stamps funding 30–60 ms after the hour (e.g., `17:00:00.041Z`).
- The window semantics in the manifest are half-open: `[start_ms, end_ms)` (`window.semantics = "half_open_start_inclusive_end_exclusive_ms"`).
- For the r1 capture ending at `19:00:00.000Z`, a venue funding event occurring at `19:00:00.041Z` falls outside `1789412400000 ms`. In an hourly schedule model, 19:00 funding belongs to the `[19:00, 20:00)` interval. However, at the start boundary, an event stamped at `15:00:00.041Z` would fall inside `[15:00:00.000, 19:00:00.000)`.
- **Finding (NIT-01)**: The proposed completeness rule does not verify the count of funding events against `(end_ms - start_ms) / HOUR_MS` or check event timestamps against expected interval slots. A query that omitted an hourly event due to boundary jitter would still be marked `complete: true` if the two query passes returned identical bytes. This limitation is noted in the design note under D-3/D-6, but should be formally addressed when D-6 is resolved.

---

## 4. Leakage Audit

1. **Address Truncation**:
   - `funding_intake_adapter.py:87-96` defines `short_address()` which truncates 42-character `0x` addresses to 11 characters (`address[:6] + "…" + address[-4:]`).
   - Inspected all emitted files (`r1_binding_packet_draft.json`, `r1_retained_rows_expected.json`, `r1_intake_gap_report.json`): only `0x1E26…AC49` appears. The full 42-character address (`0x1e26...ac49`) does not appear anywhere in the output artifacts.
   - `test_funding_intake_adapter.py:121` explicitly tests: `assert ADDRESS not in json.dumps(intake)`.
2. **Credential Cleanliness**:
   - `funding_intake_adapter.py` imports only standard library modules (`argparse`, `hashlib`, `json`, `sys`, `datetime`, `pathlib`, `typing`).
   - No environment access (`os.environ`), credential storage, private key files, or network requests exist in the adapter.

---

## 5. Test Suite and Red Arm Verification

The 7 unit tests in `subject/test_funding_intake_adapter.py` were audited:
1. `test_build_fills_only_what_the_bytes_supply_and_labels_the_rest`: Validates exact draft structure, labels, truncated addresses, and export refusal code.
2. `test_unresolved_fields_are_never_fabricated`: Enforces that `oracle_price`, `oracle_price_source`, `source_event_digest`, and `payload_digest` start with `UNRESOLVED:D-`, and scans output text to ensure `78758` and `78759` do not appear.
3. `test_completeness_rule_hour_alignment_and_identical_passes`: Checks unaligned windows and differing pass hashes return `complete: False`.
4. `test_refuses_foreign_coin_malformed_rows_and_bad_labels`: Verifies input validation rejects mismatched coins, string timestamps, and incorrect row kinds.
5. `test_load_refuses_wrong_kinds_and_duplicate_keys`: Verifies manifest kind validation and strict RFC 8259 duplicate-key rejection.
6. `test_outputs_are_deterministic_write_once_and_clock_free`: Verifies byte-level determinism, write-once directory enforcement, `.sha256` sidecars, and ensures no wall-clock timestamp prefix leaks into any output (verified tightened regex `re.findall(rb"\d{4}-\d{2}-\d{2}T", raw)` matching `2026-09-14T`).
7. `test_main_end_to_end`: Exercises CLI entry point, exit codes (0 for success, 3 for existing directory), and stdout formatting.

### Red Arm Evidence
- `sources/LEAD_RED_ARM_fabrication_fence.txt`: Mutating the adapter to calculate `oracle_price` by arithmetic caused 2 tests to fail (`test_build_fills_only_what_the_bytes_supply_and_labels_the_rest` and `test_unresolved_fields_are_never_fabricated`), with 5 passing.
- `sources/LEAD_RED_ARM_nit01_wall_clock.txt`: Mutating the adapter to inject a wall-clock timestamp (`generated_at: 2026-09-15T17:00:00+00:00`) caused `test_outputs_are_deterministic_write_once_and_clock_free` to fail with `AssertionError: binding_packet_draft.json` (1 failed, 6 passed).

---

## 6. Scope Audit

- `subject/DIFF_STAT_fcac0ac6_HEAD.txt` shows:
  ```text
   .../tests/test_funding_intake_adapter.py           | 212 ++++++++++++
   IBKR_PAPER_BRIDGE/tools/funding_intake_adapter.py  | 366 +++++++++++++++++++++
   2 files changed, 578 insertions(+)
  ```
- Exactly two new files created under `IBKR_PAPER_BRIDGE/`.
- `export_mtc_funding.py` is **untouched** (0 insertions, 0 deletions).
- No protected files modified (`sources/LEAD_GUARD_nit01.txt` confirmed `[protected] none`, `RESULT: PASS`).

---

## 7. What Would Make This the Accepting Half?

To make an intake tool the accepting half of production evidence, the following changes would be required:
1. **CLI / Mode modification**: Adding `--mode PRODUCTION` to `export_mtc_funding.py` (currently hardcoded as `PRODUCTION_MODE_UNAVAILABLE`).
2. **Evidence Kind Admission**: Modifying `export_mtc_funding.py:110` `ACCEPTED_EVIDENCE_KINDS` to include real capture evidence (e.g. `REAL_CAPTURE_READ_ONLY`).
3. **Digest Domain Approval**: Implementing a production byte domain for `source_event_digest` in `export_mtc_funding.py:111` to replace `SYNTHETIC_SOURCE_EVENT_DIGEST_V1`.
4. **Resolution of Decisions D-1 through D-6**: Defining formal rules for ID derivation without venue hashes, oracle price sourcing, and completion witnesses.
5. **Real Database Snapshot**: Generating an actual SQLite schema-v10 database with retained records rather than an expected JSON report.

**Confirmation**: **None** of these changes are present in this commit. The adapter strictly acts as the non-accepting staging draft producer.

---

## Findings

### [NIT-01] Proposed completeness witness does not check interval event count against hourly schedule
- **Location**: `subject/funding_intake_adapter.py:145-171`
- **Description**: `completeness()` verifies hour-aligned window bounds and two byte-identical passes, but does not verify that the number of captured funding events matches `(end_ms - start_ms) / HOUR_MS` or check that event timestamps align with expected schedule hours. In the presence of venue millisecond boundary jitter (D-3), an event occurring at `HH:00:00.041` could theoretically fall outside a window boundary without failing the two-pass identity check. Because this rule is explicitly labelled as proposed `D-6` and not an approved witness, this is advisory.

### [NIT-02] Unicode character in test failure output file
- **Location**: `sources/LEAD_RED_ARM_fabrication_fence.txt:5`
- **Description**: The unicode horizontal ellipsis character (`…` / `\u2026`) in the test failure output triggered a mime/charset error in the native read tool, requiring inspection via `grep_search`. Future test assertion logs should use ascii or standard utf-8 sanitization.

---

## Exact Read Coverage

| File | Read Ranges / Continuations | Status |
|---|---|---|
| `PACKET_SHA256SUMS.txt` | Lines 1–21 | Complete |
| `subject/funding_intake_adapter.py` | Lines 1–140, 141–280, 281–367 (2 continuations) | Complete (367 lines) |
| `subject/test_funding_intake_adapter.py` | Lines 1–130, 131–213 (1 continuation) | Complete (213 lines) |
| `subject/P012_FUNDING_INTAKE_DESIGN_20260915.md` | Lines 1–49 | Complete (49 lines) |
| `subject/COMMIT_HEAD.txt` | Lines 1–16 | Complete (16 lines) |
| `subject/DIFF_STAT_fcac0ac6_HEAD.txt` | Lines 1–4 | Complete (4 lines) |
| `sources/export_mtc_funding_fcac0ac6.py` | Lines 1–120, 121–215; 440–530, 531–600; 1350–1449 | Complete required ranges |
| `sources/capture_own_account_evidence_af921d75.py` | Lines 440–510 | Complete required range |
| `sources/r1_DERIVED_EXTRACTION.json` | Line 1 | Complete (2,141 bytes) |
| `sources/r1_binding_packet_draft.json` | Lines 1–82 | Complete (82 lines) |
| `sources/r1_retained_rows_expected.json` | Lines 1–34 | Complete (34 lines) |
| `sources/r1_intake_gap_report.json` | Lines 1–42 | Complete (42 lines) |
| `sources/LEAD_PYTEST_focused.txt` | Lines 1–2 | Complete (2 lines) |
| `sources/LEAD_RED_ARM_fabrication_fence.txt` | Lines 1–9 (read via directory regex search) | Complete (9 lines, 589 bytes) |
| `sources/LEAD_RED_ARM_nit01_wall_clock.txt` | Lines 1–10 | Complete (10 lines) |
| `sources/LEAD_INTAKE_r1_stdout.txt` | Lines 1–5 | Complete (5 lines) |
| `sources/LEAD_RUFF.txt` | Lines 1–2 | Complete (2 lines) |
| `sources/LEAD_RUFF_nit01.txt` | Lines 1–2 | Complete (2 lines) |
| `sources/LEAD_GUARD.txt` | Lines 1–5 | Complete (5 lines) |
| `sources/LEAD_GUARD_nit01.txt` | Lines 1–14 | Complete (14 lines) |
| `sources/DECISIONS_rows_P012.md` | Lines 1–5 | Complete (5 lines) |

---

## Nonempty NOT VERIFIED

As an independent, read-only detection reviewer operating under `SUPPLEMENTAL_UNEXECUTED`:
1. **Dynamic Execution Not Executed**: No test suite, pytest runner, python command, or lint tool was executed. All test results, red arms, and guard outputs were audited strictly from recorded evidence files.
2. **External / Live Hyperliquid Network Behavior Not Executed**: Live venue interaction, timestamp jitter distributions across hundreds of funding events, and API error states were not observed directly; evaluation relied on the recorded r1 capture bytes.
3. **Write-Once Filesystem Enforcement on Host OS Not Executed**: Operating system-level atomic file creation semantics (`open("xb")`) and directory permissions were verified by source inspection, not runtime OS execution.

---

```json
{
  "part": "P012_INTAKE_GEMINI",
  "verdict": "PASS-WITH-NITS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "fabricated_fields": [],
  "findings": [
    {
      "code": "NIT-01",
      "severity": "NIT",
      "file_line": "subject/funding_intake_adapter.py:145-171",
      "description": "Proposed completeness rule verifies window hour-alignment and pass identity, but does not check funding event count against interval duration or match timestamps to hourly schedule slots"
    },
    {
      "code": "NIT-02",
      "severity": "NIT",
      "file_line": "sources/LEAD_RED_ARM_fabrication_fence.txt:5",
      "description": "Unicode ellipsis character in test output log caused native view_file charset failure, requiring directory grep inspection"
    }
  ],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
