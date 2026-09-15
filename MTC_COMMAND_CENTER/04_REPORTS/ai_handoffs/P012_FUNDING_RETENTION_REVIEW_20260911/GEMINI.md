# Supplemental Read-Only T0 Corroboration Review: WP-P012-FUNDING-RETENTION-20260911

- **Reviewer Role:** Supplemental Read-Only Corroborator (`SUPPLEMENTAL_UNEXECUTED`)
- **Reviewer Model:** Gemini 3.7 Flash (High)
- **Task ID:** `WP-P012-FUNDING-RETENTION-20260911`
- **Candidate Commit:** `8fe2ede61ca8bf6cd6c564063680542e6101b276`
- **Base Commit:** `d1485eee5b2cc02f85d81610d89b7ec7bbf46a6a`
- **Packet Root:** `C:/tmp/P012_FUNDING_PACKET_20260911`
- **Manifest SHA-256:** `16f14641b51ecc30a953605072f18784e665038c62fc3208a22d67850217c4a1`
- **Owner Authority:** Ratified under `OD-20260911-FUNDING-1` (`HIST-2026-0042`) with standing owner approval `ı approve`
- **Repository Protocol Compliance:** `AGENTS.md` inspected and obeyed; no writes, edits, terminal commands, Git mutations, MCP tools, network calls, sandbox escapes, or credential inspections performed.

---

## 1. Verdict

**PASS**

The candidate diff cleanly, atomically, and correctly implements the approved opt-in schema v10 retained funding payload capability. All required acceptance invariants, schema migration safety rules, verification decoders, transactional atomicity guarantees, and regression test suites are present, verified against the frozen packet diff, and free of contradictions.

---

## 2. Evaluation of Scope and Diff Invariants

### 2.1 Opt-in Schema v10 & Migration Topology
- **Target Schema Version:** Adds [`SCHEMA_VERSION_FUNDING_PAYLOAD = 10`](file:///C:/LAB/Tradingview_LAB_CLEAN/IBKR_PAPER_BRIDGE/bridge/store/db.py#L302) to `SUPPORTED_TARGET_SCHEMA_VERSIONS` ([`db.py:325`](file:///C:/LAB/Tradingview_LAB_CLEAN/IBKR_PAPER_BRIDGE/bridge/store/db.py#L325)).
- **Default Baseline Preserved:** Default target remains `SCHEMA_VERSION_BASELINE = 4`. Fresh initialization without parameters initializes at v4 and does not create the v10 payload table.
- **Migration & Reopen Safety:**
  - `_migrate_v9_to_v10()` ([`db.py:2998-3047`](file:///C:/LAB/Tradingview_LAB_CLEAN/IBKR_PAPER_BRIDGE/bridge/store/db.py#L2998-L3047)) executes within a single `BEGIN IMMEDIATE` transaction, enforces `schema_version == "9"`, checks for pre-existing payload tables, verifies before/after table census equality across all predecessor tables via `_all_table_census(exclude=self._FUNDING_PAYLOAD_OBJECTS)`, ensures 0 initial rows in `funding_event_payloads` (zero backfill), and updates `meta.schema_version` with `cursor.rowcount == 1`.
  - Migration failure safely rolls back and records a sanitized marker `FUNDING_PAYLOAD_MIGRATION_FAILED:<exc_type>` under meta key [`FUNDING_PAYLOAD_MIGRATION_FAILURE_KEY`](file:///C:/LAB/Tradingview_LAB_CLEAN/IBKR_PAPER_BRIDGE/bridge/store/db.py#L334).
  - `_initialize_v10_idempotent()` and `_validate_funding_payload_schema_v10()` ([`db.py:2958-2996`](file:///C:/LAB/Tradingview_LAB_CLEAN/IBKR_PAPER_BRIDGE/bridge/store/db.py#L2958-L2996)) validate schema DDL against an in-memory reference, run `PRAGMA integrity_check`, `PRAGMA foreign_key_check`, and call `_validate_funding_payload_rows_v10()` to fail closed on any store damage.
  - Reopening a v10 database with a lower target (`v4..v9`) never downgrades the schema.

### 2.2 Table Definition & Immutability Triggers
- **Table Definition:** `funding_event_payloads` ([`db.py:2849-2877`](file:///C:/LAB/Tradingview_LAB_CLEAN/IBKR_PAPER_BRIDGE/bridge/store/db.py#L2849-L2877)) has `event_id TEXT PRIMARY KEY REFERENCES funding_events(event_id)`, non-empty `payload_json`, 64-hex lowercase `payload_digest`, and non-empty `recorded_ts`.
- **Append-Only Enforcement:** Database triggers `trg_funding_payload_no_update` and `trg_funding_payload_no_delete` abort any `UPDATE` or `DELETE` operations with error message `'FUNDING_PAYLOAD_APPEND_ONLY'`.

### 2.3 Authoritative Domain & Verified Read Path
- **8-Field Authoritative Domain:** `_FUNDING_PAYLOAD_FIELDS` ([`db.py:2838-2847`](file:///C:/LAB/Tradingview_LAB_CLEAN/IBKR_PAPER_BRIDGE/bridge/store/db.py#L2838-L2847)) strictly lists:
  `("amount_usdc", "effective_ts", "event_id", "funding_rate", "n_samples", "position_szi", "source", "symbol")`.
  Locally derived `attribution` is strictly excluded from payload retention, matching `FundingEventRecord.authoritative()` in [`IBKR_PAPER_BRIDGE/bridge/engine/types.py:1010-1058`](file:///C:/LAB/Tradingview_LAB_CLEAN/IBKR_PAPER_BRIDGE/bridge/engine/types.py#L1010-L1058).
- **Strict Verification (`_decode_funding_payload`, [`db.py:2879-2936`](file:///C:/LAB/Tradingview_LAB_CLEAN/IBKR_PAPER_BRIDGE/bridge/store/db.py#L2879-L2936)):**
  - Digest match against ledger: `payload_digest == ledger_digest` (raises `FUNDING_PAYLOAD_DIGEST_MISMATCH` on mismatch).
  - JSON parse validation (raises `FUNDING_PAYLOAD_MALFORMED`).
  - Strict domain match: `tuple(sorted(parsed)) == _FUNDING_PAYLOAD_FIELDS` (raises `FUNDING_PAYLOAD_DOMAIN_MISMATCH`).
  - Canonical JSON string match: `canonical_reconcile_json(parsed) == payload_json` (raises `FUNDING_PAYLOAD_MALFORMED`).
  - Recomputed SHA-256 hash: `reconcile_digest(parsed) == ledger_digest` (raises `FUNDING_PAYLOAD_DIGEST_MISMATCH`).
  - Identity field match: `str(parsed["event_id"]) == str(event_id)` (raises `FUNDING_PAYLOAD_IDENTITY_MISMATCH`).
- **Read API (`get_funding_event_payload`, [`db.py:9886-9925`](file:///C:/LAB/Tradingview_LAB_CLEAN/IBKR_PAPER_BRIDGE/bridge/store/db.py#L9886-L9925)):**
  - Raises `FUNDING_PAYLOAD_SCHEMA_INACTIVE` if called when `funding_payload_retention_enabled()` is false.
  - Raises `FUNDING_PAYLOAD_EVENT_UNKNOWN` if the event does not exist in `funding_events`.
  - Returns `None` if the event exists in `funding_events` but has no entry in `funding_event_payloads` (explicit historical event representation; no synthesis/backfill).
  - Returns decoded verified mapping when valid; raises corresponding conflict error on damage.

### 2.4 Transactional Atomicity & Replay Semantics
- **Atomic Insertion:** In `_append_funding_event_locked` ([`db.py:9094-9104`](file:///C:/LAB/Tradingview_LAB_CLEAN/IBKR_PAPER_BRIDGE/bridge/store/db.py#L9094-L9104)), `_append_funding_payload_locked` is invoked inside the same database transaction immediately after the `funding_events` insert.
- **Idempotent Replay:** Exact replays return early before payload insertion, preventing duplicate insertions while preserving existing records.
- **Conflicting Identity:** Conflicting authoritative fields trigger `FUNDING_EVENT_IDENTITY_CONFLICT` and abort the reconcile finalize transaction before any rows commit.
- **Null Semantics:** Absent optional fields (`funding_rate`, `position_szi`, `n_samples`) are retained as JSON `null` / Python `None` and never coerced to `0`.

### 2.5 Predecessor Predicate Extensions
- `exposure_controls_enabled()`, `durable_risk_controls_enabled()`, `full_reconcile_enabled()`, and `kill_evidence_enabled()` ([`db.py:5097, 8240, 8248, 8256`](file:///C:/LAB/Tradingview_LAB_CLEAN/IBKR_PAPER_BRIDGE/bridge/store/db.py#L5097)) are updated to include `SCHEMA_VERSION_FUNDING_PAYLOAD = 10` as a valid additive successor.

### 2.6 Corrective Path & Governance Records
- **Test Target Bump:** `test_partial_fill_protection.py:2429` and `test_store.py:484` correctly update unsupported target version test fixtures from `10` to `11`.
- **Governance:** `DECISIONS.md` appends `OD-20260911-FUNDING-1` and `TASK_HISTORY.json` appends `HIST-2026-0042` with all 41 prior historical events preserved.

---

## 3. Findings

### 3.1 Concrete Required Findings
**None.** No blocking issues, regressions, or unauthorized scope expansions exist in the candidate diff.

### 3.2 Optional Observations & Nits
1. **Author Artifact Accounting:** The primary builder report discrepancy noted in `REVIEW_BRIEF.md` (initial 1462-test count vs final 1467-test count prior to Sol repair) and the CLI interruption after auto-memory writes are cleanly documented in `MTC_COMMAND_CENTER/_AI_MEMORY/P012_FUNDING_RETENTION_20260911.md`.
2. **Frozen Fixture Verification:** The synthetic fixture digest (`77fb9ccfc5d2dddf90d53b7e2c924b5b240e849cb934dc1633734c3a62bd4a73`) in `test_funding_payload_retention.py:530-555` independently validates canonical JSON serialization against pre-change hashing.

---

## 4. Contradictions, Limitations, and Boundaries

1. **Unexecuted Status:** This review is an independent, unexecuted evaluation of the candidate diff, test suites, and evidence logs within frozen packet `C:/tmp/P012_FUNDING_PACKET_20260911`. It does not replace the executing flagship reviews.
2. **Venue Invariants Unchanged:** Schema v10 retains normalized bridge data only. It makes no claim of venue authenticity, exchange settlement-oracle mapping, raw HTTP capture, or live trading readiness.
3. **Non-Acceptance Status:** The candidate remains `NONACCEPTED` pending Lead reconciliation of executing flagship reviews and current-head protected CI.

GEMINI_READ_ONLY_OK
