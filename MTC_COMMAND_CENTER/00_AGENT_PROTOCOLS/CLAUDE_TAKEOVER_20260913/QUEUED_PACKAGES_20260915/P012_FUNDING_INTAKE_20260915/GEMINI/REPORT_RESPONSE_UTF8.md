### 1. Fabrication Audit (Field-by-Field)

Every key present in [`sources/r1_binding_packet_draft.json`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/r1_binding_packet_draft.json#L1-L82) is audited below against the captured bytes ([`sources/r1_DERIVED_EXTRACTION.json`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/r1_DERIVED_EXTRACTION.json#L1)), the run manifest, and [`sources/export_mtc_funding_fcac0ac6.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L1-L215).

| Key Path in `r1_binding_packet_draft.json` | Sample Value | Classification | Basis / Provenance Citation |
|---|---|---|---|
| `adapter_version` | `"p012-funding-intake/v1"` | TOOL-RULE | Adapter metadata constant ([`subject/funding_intake_adapter.py:30`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/funding_intake_adapter.py#L30)) |
| `label` | `"NONACCEPTING_INTAKE_DRAFT"` | TOOL-RULE | Explicit draft label ([`subject/funding_intake_adapter.py:31`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/funding_intake_adapter.py#L31)) |
| `packet_version` | `"SYNTHETIC_FUNDING_BINDING_PACKET_V1"` | TOOL-RULE | Verbatim target packet version ([`sources/export_mtc_funding_fcac0ac6.py:108`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L108)) |
| `bindings[*].event_timestamp` | `"2026-09-14T17:00:00.041Z"` | COPIED | ISO-Z conversion of `time: 1789405200041` from `funding[0]` ([`sources/r1_DERIVED_EXTRACTION.json:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/r1_DERIVED_EXTRACTION.json#L1)) |
| `bindings[*].funding_event_id` | `"hl-funding:0x1E26…AC49:BTC:1789405200041"` | DERIVED-LABELLED | Proposed D-2 rule `hl-funding:<short_addr>:<coin>:<time_ms>`; accompanied by rule label |
| `bindings[*].funding_event_id_rule` | `"PROPOSED:D-2 hl-funding:<account-short>:<coin>:<time_ms>"` | DERIVED-LABELLED | Explicit proposal label for D-2 |
| `bindings[*].observed.szi` | `"0.00058"` | COPIED | Verbatim from `funding[0].szi` ([`sources/r1_DERIVED_EXTRACTION.json:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/r1_DERIVED_EXTRACTION.json#L1)) |
| `bindings[*].observed.usdc` | `"-0.000571"` | COPIED | Verbatim from `funding[0].usdc` ([`sources/r1_DERIVED_EXTRACTION.json:1`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/r1_DERIVED_EXTRACTION.json#L1)) |
| `bindings[*].observed.venue_hash` | `"0x0000000000000000000000000000000000000000000000000000000000000000"` | COPIED | Verbatim from `funding[0].hash` (zero hash on venue funding rows) |
| `bindings[*].oracle_price` | `"UNRESOLVED:D-4"` | UNRESOLVED | Explicit unresolved marker for decision D-4 |
| `bindings[*].oracle_price_source` | `"UNRESOLVED:D-4"` | UNRESOLVED | Explicit unresolved marker for decision D-4 |
| `bindings[*].positive_rate_payer` | `"LONG"` | TOOL-RULE | Verbatim tool constant `APPROVED_PAYER` ([`sources/export_mtc_funding_fcac0ac6.py:122`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py#L122)) |
| `bindings[*].positive_rate_payer_basis` | `"export_mtc_funding.APPROVED_PAYER (tool constant)"` | TOOL-RULE | Explicit citation of export tool constant |
| `bindings[*].provenance.evidence_kind` | `"REAL_CAPTURE_READ_ONLY"` | DERIVED-LABELLED | Proposed evidence kind for decision D-5 |
| `bindings[*].provenance.evidence_kind_status` | `"UNRESOLVED:D-5"` | UNRESOLVED | Explicit unresolved marker for decision D-5 |
| `bindings[*].provenance.extraction_method` | `"capture_own_account_evidence.py tool_sha256=00b3b8f69f0e4870 user_funding_history"` | COPIED | Formatted from manifest response metadata |
| `bindings[*].provenance.source_locator` | `"funding_pass1_page001.json#/0"` | COPIED | Captured pass file name + verbatim `json_pointer` (`/0`) |
| `bindings[*].provenance.source_sha256` | `"6f25ba294ae96dd333f6938bfe103f283559a960463ddfd2ce8757806563578f"` | COPIED | Verbatim `funding[0].capture_sha256` |
| `bindings[*].provenance.source_title` | `"Hyperliquid userFunding 0x1E26…AC49 run p012-path1-20260914T1500Z-1900Z-r1"` | COPIED | Formatted from short address and manifest `run_id` |
| `bindings[*].raw_rate` | `"0.0000125"` | COPIED | Verbatim from `funding[0].fundingRate` |
| `bindings[*].source_event_digest` | `"UNRESOLVED:D-1"` | UNRESOLVED | Explicit unresolved marker for decision D-1 |
| `coverage.account_scope` | `"0x1E26…AC49"` | COPIED | Short address derived from manifest `address` |
| `coverage.complete` | `true` | DERIVED-LABELLED | Computed by proposed D-6 rule; qualified by `witness_rule` |
| `coverage.evidence_kind` | `"REAL_CAPTURE_READ_ONLY"` | DERIVED-LABELLED | Proposed evidence kind for decision D-5 |
| `coverage.expected_event_ids` | `["hl-funding:0x1E26…AC49:BTC:1789405200041", ...]` | DERIVED-LABELLED | List of derived event IDs |
| `coverage.interval_end_exclusive` | `"2026-09-14T19:00:00Z"` | COPIED | Verbatim from manifest `window.end` |
| `coverage.interval_start_inclusive` | `"2026-09-14T15:00:00Z"` | COPIED | Verbatim from manifest `window.start` |
| `coverage.source_witnesses` | `[{"file": "funding_pass1_page001.json", ...}, ...]` | COPIED | Verbatim from manifest response filenames and sha256 digests |
| `coverage.symbol` | `"BTC"` | COPIED | Verbatim from manifest `coin` |
| `coverage.unattributed_event_ids` | `[]` | COPIED | Empty list |
| `coverage.witness_identity` | `"capture_own_account_evidence.py ..."` | COPIED | Formatted from tool SHA prefix, run ID, and verified ownership metadata |
| `coverage.witness_reasons` | `[]` | COPIED | Empty reasons list |
| `coverage.witness_rule` | `"hour-aligned window AND two byte-identical funding passes (proposed D-6)"` | DERIVED-LABELLED | Explicit proposed rule description |

**Fabrication Verification:**
- No arithmetic oracle price appears anywhere in `r1_binding_packet_draft.json`, `r1_retained_rows_expected.json`, or `r1_intake_gap_report.json`. The arithmetic back-derivation `usdc / (szi * rate) = 0.000571 / (0.00058 * 0.0000125) ≈ 78758.62` is completely absent (`"78758"` and `"78759"` do not appear in any output bytes).
- `positive_rate_payer = "LONG"` is identical to `export_mtc_funding.py:122` (`APPROVED_PAYER = "LONG"`).
- `fabricated_fields = []`.

---

### 2. Design-Note Honesty

The claims in [`subject/P012_FUNDING_INTAKE_DESIGN_20260915.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/P012_FUNDING_INTAKE_DESIGN_20260915.md#L1-L49) were checked against [`sources/export_mtc_funding_fcac0ac6.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/export_mtc_funding_fcac0ac6.py):
1. **No `--mode` argument**: Verified. CLI invocation (`:59-62`) accepts `--snapshot`, `--bindings`, `--symbol`, `--start`, `--end`, `--schedule-id`, `--staging`. There is no `--mode` option. Line 116 defines `PRODUCTION_MODE_UNAVAILABLE = "UNAVAILABLE_PENDING_SOURCE_EVENT_DIGEST_DOMAIN"`. Lines 23-28 affirm: *"There is no mode switch, callback, boolean gate or magic literal that turns a synthetic candidate into a production record..."*
2. **Accepts only `SYNTHETIC_FIXTURE`**: Verified. Line 109 defines `SYNTHETIC_EVIDENCE_KIND = "SYNTHETIC_FIXTURE"`, and line 110 sets `ACCEPTED_EVIDENCE_KINDS = (SYNTHETIC_EVIDENCE_KIND,)`.
3. **Refuses everything else with `CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE`**: Verified. Lines 468–473 in `_validate_coverage` and lines 570–575 in `_validate_provenance` explicitly raise `_Refusal(CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE, ...)` whenever `kind not in ACCEPTED_EVIDENCE_KINDS`.
4. **Decisions D-1 through D-6 map to genuine tool gaps**:
   - **D-1 (`source_event_digest` domain)**: Tool requires `source_event_digest` (`:175`) and `payload_digest` (`:163`), but defines only `SYNTHETIC_SOURCE_EVENT_DIGEST_V1` (`:111`) and forbids conflating them (`:44-46`). No domain exists for real Hyperliquid venue rows.
   - **D-2 (`funding_event_id` rule)**: Hyperliquid returns `hash: "0x000...0"` for funding rows. Tool requires unique `event_id` (`:160, 169`), but does not define an ID scheme for zero-hash funding events.
   - **D-3 (`event_timestamp` venue stamp vs hour boundary)**: Tool requires ISO-Z `event_timestamp` (`:168`), but does not specify whether sub-second venue offsets (e.g. 41–60 ms past the hour) are preserved or rounded to nominal funding hours.
   - **D-4 (`oracle_price` and source)**: Mandatory keys `oracle_price` and `oracle_price_source` (`:170-171`) are not present in Hyperliquid funding rows; the tool does not supply or derive them.
   - **D-5 (Admitting real capture evidence kind)**: `ACCEPTED_EVIDENCE_KINDS` (`:110`) accepts only `SYNTHETIC_FIXTURE`. Admitting `REAL_CAPTURE_READ_ONLY` requires a formal schema change.
   - **D-6 (Whole-interval completion witness)**: Tool requires `coverage.complete` (`:194, 474-479`) but leaves real-world interval verification unestablished (`:208`).

---

### 3. Completeness Rule

The rule in `completeness()` ([`subject/funding_intake_adapter.py:145-171`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/funding_intake_adapter.py#L145-L171)) checks:
1. `start_ms % HOUR_MS == 0` and `end_ms % HOUR_MS == 0` with `end_ms > start_ms`.
2. At least two funding pass responses recorded in manifest.
3. All funding pass response SHA256 digests are identical.

**Evaluation as a proposed witness (D-6):**
- **Labelling**: It is explicitly and unambiguously labelled as a proposal. In the packet output, `coverage.witness_rule` reads `"hour-aligned window AND two byte-identical funding passes (proposed D-6)"` ([`sources/r1_binding_packet_draft.json:77`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/r1_binding_packet_draft.json#L77)), and `gap_report.unresolved_fields` lists `"coverage.complete (adapter rule, not the tool's approved witness)": "D-6"` ([`sources/r1_intake_gap_report.json:37`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/r1_intake_gap_report.json#L37)).
- **Missed boundary instant hazard**: A capture missing a funding instant *can* pass this witness. In Hyperliquid, funding is stamped ~31–60 ms after the hour. In a half-open window `[15:00:00Z, 19:00:00Z)` (`end_ms = 1789412400000`), a funding event stamped at `19:00:00.041Z` falls outside the query window. Both passes return identical results omitting that payment, yet `completeness()` evaluates to `True`.
- **Status in design note**: This exact limitation and the need for an end-boundary tolerance or count witness are explicitly declared and recommended for owner decision under D-6 in [`subject/P012_FUNDING_INTAKE_DESIGN_20260915.md:45`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/P012_FUNDING_INTAKE_DESIGN_20260915.md#L45). The adapter does not overclaim it as an approved witness.

---

### 4. Leakage Audit

1. **Address Truncation**:
   - `short_address()` ([`subject/funding_intake_adapter.py:87-96`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/funding_intake_adapter.py#L87-L96)) strictly validates 42-character `0x` addresses and formats them as `address[:6] + "…" + address[-4:]` (e.g. `0x1E26…AC49`).
   - Every occurrence in `r1_binding_packet_draft.json` (`funding_event_id`, `source_title`, `account_scope`, `expected_event_ids`, `witness_identity`), `r1_retained_rows_expected.json` (`attribution`, `event_id`), and `r1_intake_gap_report.json` (`account_scope`) contains only the 11-character short form.
   - Asserted by test in [`subject/test_funding_intake_adapter.py:121`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/test_funding_intake_adapter.py#L121): `assert ADDRESS not in json.dumps(intake)`.
2. **Credential and Secret Inspection**:
   - Imports in `funding_intake_adapter.py:22-28` are limited to standard library modules (`argparse`, `hashlib`, `json`, `sys`, `datetime`, `pathlib`, `typing`). No network, socket, or OS environment (`os.environ`) access occurs.
   - The CLI takes only `--run-dir` and `--out`. No private keys, API secrets, or signing credentials are read, manipulated, or emitted.

---

### 5. Tests Analysis

The test suite in [`subject/test_funding_intake_adapter.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/test_funding_intake_adapter.py) contains 7 tests:
1. `test_build_fills_only_what_the_bytes_supply_and_labels_the_rest`: Proves mapping accuracy of fillable fields, presence of `UNRESOLVED:D-n` labels, constant correctness (`APPROVED_PAYER == "LONG"`), address masking, and refusal reporting.
2. `test_unresolved_fields_are_never_fabricated`: Proves unresolved fields retain `"UNRESOLVED:D-"` prefixes and verifies the back-calculated oracle price strings (`"78758"`, `"78759"`) do not appear anywhere in serialized output.
3. `test_completeness_rule_hour_alignment_and_identical_passes`: Proves proposed D-6 witness rejects unaligned window starts and differing pass hashes.
4. `test_refuses_foreign_coin_malformed_rows_and_bad_labels`: Proves intake rejects coin mismatches, non-integer timestamps, and incorrect row kinds.
5. `test_load_refuses_wrong_kinds_and_duplicate_keys`: Proves strict JSON validation rejects duplicate keys and incorrect manifest kinds.
6. `test_outputs_are_deterministic_write_once_and_clock_free`: Proves identical byte reproduction across runs, write-once safety, SHA256 sidecar validity, and absence of non-capture timestamps (tightened per NIT-01).
7. `test_main_end_to_end`: Proves CLI entry point, exit codes (0 on success, 3 on refusal), stdout reporting, and stderr emission.

**Mutation & RED Arm Verification:**
- [`sources/LEAD_RED_ARM_fabrication_fence.txt:1-10`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/LEAD_RED_ARM_fabrication_fence.txt#L1-L10) confirms that when a mutant calculates `oracle_price` by arithmetic, exactly two tests fail:
  - `FAILED tests/test_funding_intake_adapter.py::test_build_fills_only_what_the_bytes_supply_and_labels_the_rest`
  - `FAILED tests/test_funding_intake_adapter.py::test_unresolved_fields_are_never_fabricated`
- [`sources/LEAD_RED_ARM_nit01_wall_clock.txt:1-10`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/LEAD_RED_ARM_nit01_wall_clock.txt#L1-L10) confirms that a mutant injecting a wall-clock timestamp into `binding_packet_draft.json` is caught by `test_outputs_are_deterministic_write_once_and_clock_free`.

---

### 6. Scope Verification

- [`subject/DIFF_STAT_fcac0ac6_HEAD.txt:1-4`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/DIFF_STAT_fcac0ac6_HEAD.txt#L1-L4) confirms exactly 2 new files and 578 insertions:
  - `IBKR_PAPER_BRIDGE/tests/test_funding_intake_adapter.py` (+212 lines)
  - `IBKR_PAPER_BRIDGE/tools/funding_intake_adapter.py` (+366 lines)
- `IBKR_PAPER_BRIDGE/tools/export_mtc_funding.py` is completely untouched.
- No protected path is modified ([`sources/LEAD_GUARD.txt:8`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/sources/LEAD_GUARD.txt#L8)).

---

### 7. What Would Make This the Accepting Half — And Is Any Present?

For the export tool to accept real production captures, the repository would require:
1. Adding a `--mode PRODUCTION` CLI parameter to `export_mtc_funding.py`.
2. Updating `ACCEPTED_EVIDENCE_KINDS` to admit a real read-only capture kind (e.g. `REAL_CAPTURE_READ_ONLY`).
3. Defining and implementing an approved production `source_event_digest` byte domain (replacing `PRODUCTION_MODE_UNAVAILABLE`).
4. Removing or altering the hard validation checks in `_validate_coverage` and `_validate_provenance` that reject non-synthetic evidence.
5. Ingesting live database snapshots or approved production stores instead of synthetic offline fixtures.

**Presence in this diff:** None. Not a single accepting mechanism is implemented or modified. The intake adapter is strictly non-accepting, producing marked drafts that the export tool rejects by design.

---

### Findings

- **NIT-01**: [`subject/funding_intake_adapter.py:151`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/funding_intake_adapter.py#L151) — The proposed D-6 witness evaluates `complete = True` for hour-aligned windows, but does not apply end-boundary tolerance for Hyperliquid funding events stamped 31–60 ms after the hour. While explicitly acknowledged in design note §5 (`P012_FUNDING_INTAKE_DESIGN_20260915.md:45`) and labelled as proposed D-6, any future accepting tool adoption will require resolving this window boundary tolerance.
- **NIT-02**: [`subject/test_funding_intake_adapter.py:150`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915/subject/test_funding_intake_adapter.py#L150) — `test_completeness_rule_hour_alignment_and_identical_passes` tests unaligned `window_start`, but does not explicitly test unaligned `window_end`.

---

### Read Coverage

All reads performed natively via `view_file` within packet `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915`:
1. `PACKET_SHA256SUMS.txt`: lines 1–21 (complete).
2. `subject/funding_intake_adapter.py`: lines 1–150; continuation lines 151–300; continuation lines 301–367 (complete, 367 lines).
3. `subject/test_funding_intake_adapter.py`: lines 1–150; continuation lines 151–213 (complete, 213 lines).
4. `subject/P012_FUNDING_INTAKE_DESIGN_20260915.md`: lines 1–49 (complete).
5. `subject/COMMIT_HEAD.txt`: lines 1–16 (complete).
6. `subject/DIFF_STAT_fcac0ac6_HEAD.txt`: lines 1–4 (complete).
7. `sources/export_mtc_funding_fcac0ac6.py`: lines 1–150; continuation lines 151–215 (lines 1–215 complete); lines 440–580; continuation lines 581–600 (lines 440–600 complete).
8. `sources/capture_own_account_evidence_af921d75.py`: lines 440–510 (complete).
9. `sources/r1_DERIVED_EXTRACTION.json`: lines 1–1 (complete).
10. `sources/r1_binding_packet_draft.json`: lines 1–82 (complete).
11. `sources/r1_retained_rows_expected.json`: lines 1–34 (complete).
12. `sources/r1_intake_gap_report.json`: lines 1–42 (complete).
13. `sources/LEAD_PYTEST_focused.txt`: lines 1–2 (complete).
14. `sources/LEAD_RED_ARM_fabrication_fence.txt`: lines 1–10 (complete).
15. `sources/LEAD_INTAKE_r1_stdout.txt`: lines 1–5 (complete).
16. `sources/LEAD_RUFF.txt`: lines 1–2 (complete).
17. `sources/LEAD_GUARD.txt`: lines 1–5 (complete).
18. `sources/DECISIONS_rows_P012.md`: lines 1–5 (complete).
19. `sources/LEAD_RED_ARM_nit01_wall_clock.txt`: lines 1–10 (complete).
20. `sources/LEAD_GUARD_nit01.txt`: lines 1–14 (complete).

---

### Not Verified

- Dynamic execution of `funding_intake_adapter.py` or pytest (read-only audit; unexecuted review).
- Live API interaction or real-time query against Hyperliquid or other venue endpoints.
- External files outside the designated packet directory.

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
      "location": "subject/funding_intake_adapter.py:151",
      "description": "Proposed D-6 completeness rule checks window hour-alignment but does not account for venue funding stamps sitting 31-60 ms past the hour boundary without an explicit tolerance rule; acknowledged in design note §5."
    },
    {
      "code": "NIT-02",
      "severity": "NIT",
      "location": "subject/test_funding_intake_adapter.py:150",
      "description": "test_completeness_rule_hour_alignment_and_identical_passes verifies unaligned start_ms but omits a specific test case for unaligned end_ms."
    }
  ],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
