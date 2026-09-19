# Documentary Corroboration of WP-P0-31 Milestone-2 Design Half
**Reviewer:** Gemini 3.8 Flash (High) — Independent T2 Read-Only Corroborator (`SUPPLEMENTAL_UNEXECUTED`)  
**Subject:** WP-P0-31 Milestone-2 Design Half (Author: Claude Opus 5 Lead, 2026-09-16)  
**Governing Authority:** `OD-20260916-P031-M2-Q1-Q6-1` (Q1 = A: documentary + scratch only; Q6 = B: M2 build waits for full M1 package acceptance)  
**Operating Mode:** Strictly read-only native file inspection within `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_M2_DESIGN_20260916/`. No commands executed; no files modified; no external reads.

---

## 1. Census Arithmetic and Provenance

### (a) Census-Arithmetic Table (Store → Independent Reading vs. Census)

| Store | Field(s) Inspected | Reviewer Reading (Direct File Inspection) | Census Report (`census.json` & Census Doc) | Agreement |
|---|---|---|---|:---:|
| `STRATEGY_RESEARCH_REGISTRY.json` | `current_status`, `maturity_level` | **63** strategies (`STG001`..`STG063`). Values: `RESEARCH_BATCH`: 32, `READY_FOR_DETERMINISTIC_REVIEW`: 14, `READY_FOR_PYTHON_PROTOTYPE`: 7, `TRIAGED`: 7, `PROMOTE_TO_FORWARD_PAPER_TRADE\|PROMOTE_TO_PARITY_CANDIDATE`: 2, `PROMOTE_TO_FORWARD_PAPER_TRADE`: 1. | 63 strategies; identical distribution (32, 14, 7, 7, 2, 1). | **VERIFIED** |
| `producer_spec.json` (via listing txt) | `promotion_status`, `candidate_id` | **63** listing lines. Values: `RESEARCH_GRADE`: 24, `FORWARD_PAPER_CANDIDATE`: 17, `None`: 19, `['PROMOTE_TO_FORWARD_PAPER_TRADE', 'PROMOTE_TO_PARITY_CANDIDATE']`: 2, `['PROMOTE_TO_FORWARD_PAPER_TRADE']`: 1. (44 filled, 19 null). | 63 files, 44 filled / 19 null; identical distribution (24, 17, 19, 2, 1). | **VERIFIED** |
| `TRIAGE_CANDIDATE_REGISTRY.json` | `candidate_id`, `stg_code`, `eligible_for_retriage`, (decision field) | **172** candidates (`QLR_...` / `QL_...`). `summary.total = 172`, `eligible_for_retriage`: 90 True / 82 False. No extract-or-decline decision field present. `stg_code` format `Stg###`. | 172 candidates; `eligible_for_retriage`: 90 True / 82 False; no decision field. | **VERIFIED** |
| `AI_QUANTLENS_VERDICT_REGISTRY.json` | `decision`, `strategy_id` | **212** entries. Decisions: `NEEDS_CLARIFICATION`: 141, `RESEARCH_ONLY`: 46, `SALVAGE`: 25. Id formats: `CAND_...`, `GEN_...`, `QLR_...`, `QL_...`. | 212 entries; identical distribution (141, 46, 25). 169 join triage `candidate_id`, 43 orphans. | **VERIFIED** |
| `VARIANT_LOG_REGISTRY.json` | `variant_id`, `promotable` | **20** variants (`NEW_...`). All `promotable = false`. Zero strategy or family identity fields. | 20 variants, all `promotable: False`, no family identity. | **VERIFIED** |
| Table 4b Diagnostic Labels (outside 5 stores) | `label:<lowercased>` | 251 JSON files in checkout under `MTC_COMMAND_CENTER/`: `INSUFFICIENT_TRADES` (245), `NO_DATA` (218), `REJECTED` (6); remaining 6 labels appear in 0 files. | 251 files carrying 4b labels; 245 / 218 / 6 distribution. | **VERIFIED** |

### (b) Provenance Pinning and Baseline Honesty
- **Scratch Copy Pinning:** Every store in `subject/census.json` lines 109–138 is pinned by SHA-256 and blob OID at canonical commit `108ea066a710ff7ef5c09246903fe3d523da1d56` (`root/current-20260829`):
  - `STRATEGY_RESEARCH_REGISTRY.json`: SHA-256 `0024cd4f...`, blob OID `e01ce84d...`, generated 2026-06-06T20:48:34 UTC by `build_strategy_research_registry.py`.
  - `TRIAGE_CANDIDATE_REGISTRY.json`: SHA-256 `f9fe8aab...`, blob OID `bd2571de...`, generated 2026-06-04T09:23:36 UTC from `11_TRIAGE/2026-05-30_rejected_worklist.xlsx`.
  - `AI_QUANTLENS_VERDICT_REGISTRY.json`: SHA-256 `ca6bea7e...`, blob OID `88c2aa37...`, generated 2026-06-08T00:00:00 UTC (Codex GPT-5).
  - `VARIANT_LOG_REGISTRY.json`: SHA-256 `b85307c9...`, blob OID `49eacba0...`, generated 2026-07-13T08:25:46 UTC.
  - `producer_spec.json`: 63 files, digest of sorted SHA-256s `be069995...`.
- **Fold Comparison Honesty:** In `sources/FOLD_section4_to_6.md`, §4c line 27 explicitly states `producer_spec.json.promotion_status (44/63 filled, two independent writers)` and line 29 states `TRIAGE_CANDIDATE_REGISTRY.json (172 candidates)`. The Lead's comparison is completely faithful to the historical fold text.

---

## 2. The 60/63 Claim Corroboration

1. **Table 4a Vocabulary (`sources/FOLD_section4_to_6.md:7-16`):**
   Table 4a explicitly defines only seven legacy ladder values:
   - `REJECTED`
   - `KEEP_AS_RESEARCH_NOTE`
   - `PROMOTE_TO_SANDBOX`
   - `PROMOTE_TO_FORWARD_PAPER_TRADE`
   - `MTC_ENGINE_VALIDATED`
   - `PROMOTE_TO_PARITY_CANDIDATE`
   - `APPROVED_FOR_MTC_V2_INTEGRATION`
2. **Live Registry Statuses (`sources/scratch_STRATEGY_RESEARCH_REGISTRY.json`):**
   Across the 63 strategies:
   - `RESEARCH_BATCH` (32 strategies): **NOT** in Table 4a.
   - `READY_FOR_DETERMINISTIC_REVIEW` (14 strategies): **NOT** in Table 4a.
   - `READY_FOR_PYTHON_PROTOTYPE` (7 strategies): **NOT** in Table 4a.
   - `TRIAGED` (7 strategies): **NOT** in Table 4a.
   - `PROMOTE_TO_FORWARD_PAPER_TRADE|PROMOTE_TO_PARITY_CANDIDATE` (2 strategies, `STG001`, `STG002`): both components are in Table 4a.
   - `PROMOTE_TO_FORWARD_PAPER_TRADE` (1 strategy, `STG003`): in Table 4a.
3. **Conclusion:** Exactly **3 of 63** strategies have values admitted by Table 4a. Exactly **60 of 63** strategies carry statuses outside Table 4a. Under owner ruling Q5 A (`UNKNOWN` + listed), ruled import yields exactly 3 registry seeds, 0 conflicts (since no conflicting pair has both sides in-table), and 60 `UNKNOWN` blockers.  
**Central Claim Status: CONFIRMED.**

---

## 3. Dry-Run Rule Fidelity (Code Inspection)

### (b) Rule-Fidelity Table

| Rule / Mandate | Implementation Code (`subject/m2_dry_run.py`) | Review Finding & Fidelity Verdict |
|---|---|---|
| **Composite Fold (Q3 A)** | Lines 64–73 (`components`), Lines 75–90 (`map_ladder`) | **VERIFIED.** Splitting on `\|` or list parsing. Any unmapped component returns `NO_STATE` (`UNKNOWN`). Highest-ranked component row via `max(mapped, key=RANK_4A)` sets state; tags from all components are aggregated. |
| **Registry ↔ Producer-Spec Join** | Lines 132–136, 143–152 | **VERIFIED.** Joins producer_spec by regex extracting folder code `STG###` matching `strategy_id`. `candidate_id` of producer_spec is preserved as `candidate_id_alias` in provenance. |
| **Two-Writer Conflict (Q4 A)** | Lines 169–173 | **VERIFIED.** If mapped states differ, sets `conflict = {"registry": (reg_val, reg_st), "producer_spec": (ps_val, ps_st)}`, assigns lower state via `min((state, ps_state), key=lambda st: STATE_RANK[st])`, and appends tag `migrated-conflict`. |
| **Q5-Before-Q4 Ordering** | Lines 154–158, 163–167 | **VERIFIED.** If either registry state or producer_spec state is `NO_STATE`, the row is immediately disposed `UNKNOWN` and continues before conflict logic is reached. Out-of-table preempts conflict tagging. |
| **Triage Seeding Rule** | Lines 196–210 | **VERIFIED.** Disclosed finding that store contains no extract-or-decline decision field. `decision_recorded = False` literal applies the letter of Fold §4c ("otherwise -> CAPTURED"). All 172 candidates seeded to `CAPTURED`, 90 tagged `legacy:retriage_eligible`. |
| **Advisory Verdict Seeding** | Lines 213–226 | **VERIFIED.** Decisions mapped to `advisory:*` tags. Tag attached to existing host seed if present (169); unhosted IDs disposed `NOT_SEEDED` with reason "tag without a host record; never a state" (43). |
| **Variant Log Seeding** | Lines 187–194 | **VERIFIED.** `promotable = False` disposed `NOT_SEEDED` ("no tag, never a state", 20/20). `True` would dispose `UNKNOWN` due to absent family identity join. |
| **Fresh Balance & `--plant`** | Lines 96, 115–117, 228–246, 264–265 | **VERIFIED.** Re-enumerates lengths in memory directly against loaded stores. `--plant` injects synthetic `STG999`, yielding `measured_now = 64` vs. `censused = 63`, forcing `matches_census = false` and `balanced = false`. |
| **What-If Extension Isolation** | Lines 10, 105–110, 252 | **VERIFIED.** Extension applied only via `--table-extension`. Report label switches strictly to `"WHAT_IF_NOT_RULED"`. |
| **State Ordering for Q4 A** | Line 44: `STATE_RANK = {"REJECTED": 0, "PARKED": 1, "CAPTURED": 2, "TRIAGED": 3, "CANDIDATE": 4}` | **DECIDES-FOR-THE-OWNER (Disclosed).** Q4 A ruled "LOWER of the two mapped states" without ordering the 5 states. Lead assumed this specific lattice and disclosed it explicitly as Question Q12. |
| **Extension Row Ranks** | Line 109: `RANK_4A.setdefault(old, -1)` | **DECIDES-FOR-THE-OWNER (Disclosed).** Assigns rank `-1` to unruled extension entries in composite resolution. Disclosed in Q7 notes. |

---

## 4. Run Summaries Reconciliation

The three run summaries (`run_as_ruled_SUMMARY.json`, `run_planted_SUMMARY.json`, `run_whatif_4a_prime_SUMMARY.json`) reconcile completely with the census, the code, and the mapping document:

1. **`run_as_ruled_SUMMARY.json`:**
   - `balanced`: `true` (all stores: `measured_now` == `disposed` == `censused`).
   - `seed_count`: **175** (3 `CANDIDATE` from registry + 172 `CAPTURED` from triage).
   - `disposition_count`: **467** total:
     - `SEEDED`: **344** (3 registry seeds + 172 triage seeds + 169 advisory tags attached to host seeds).
     - `NOT_SEEDED`: **63** (20 `promotable=False` variants + 43 advisory orphan verdicts).
     - `UNKNOWN`: **60** (all 60 registry rows with out-of-table statuses).
   - `conflict_count`: **0** (no pairs have both writers inside Table 4a).
   - `unknown_target_count`: **60**.
   - `full_report_sha256`: `0fc6a0a6c2af8115f57bcc71b25f0ec730237b6cbdd1f3015eb3094a9c6cdebb` (matches `P031_M2_MAPPING_DRY_RUN_20260916.md:40` verbatim).

2. **`run_planted_SUMMARY.json`:**
   - Registry `measured_now`: **64** vs. `censused`: **63**.
   - `matches_census`: `false` → `balanced`: `false`.
   - `seed_count`: **176** (4 `CANDIDATE` including synthetic `STG999` + 172 `CAPTURED`).
   - `disposition_count`: **468** (`SEEDED`: 345, `NOT_SEEDED`: 63, `UNKNOWN`: 60).
   - `full_report_sha256`: `d0a5bf8decf6dc7a0b280cbcf1b2e6931494cc873b0332cbe49f488d8941196c` (matches `P031_M2_MAPPING_DRY_RUN_20260916.md:41` verbatim).

3. **`run_whatif_4a_prime_SUMMARY.json`:**
   - `label`: `"WHAT_IF_NOT_RULED"`.
   - `balanced`: `true`.
   - `seed_count`: **235** (3 `CANDIDATE` + 232 `CAPTURED` = 63 registry + 172 triage).
   - `disposition_count`: **467** (`SEEDED`: 404 [63 registry + 172 triage + 169 advisory], `NOT_SEEDED`: 63, `UNKNOWN`: 0).
   - `conflict_count`: **28** (exactly the 28 pairs where registry is `TRIAGED` / `READY_FOR_*` and producer_spec is `FORWARD_PAPER_CANDIDATE` or `RESEARCH_GRADE`).
   - All 28 conflicts resolve to lower state `CAPTURED` under Q4 A and Q12 A.
   - `full_report_sha256`: `9fbd9b7fb40b167e2c75848a1c80cd3072686988e8e96050834db26b1956318f` (matches `P031_M2_MAPPING_DRY_RUN_20260916.md:42` verbatim).

---

## 5. Identity Finding Corroboration

- **Triage `stg_code` vs. Registry `strategy_id`:**
  - In `scratch_TRIAGE_CANDIDATE_REGISTRY.json:15-18`, `stg_code = "Stg001"` belongs to candidate `QLR_9ZJK8175drM` titled `"2026-05-03_9ZJK8175drM_quantlens_canslim_detailed_intake"` (a YouTube video intake transcript).
  - In `scratch_STRATEGY_RESEARCH_REGISTRY.json:7-8`, `strategy_id = "STG001"` belongs to strategy `"STG001_ql_alpha_ada_two_candle_sr_1h"` (an algorithmic ADA/USDT trading strategy).
  - They are completely different artifacts. Exactly 0 exact matches exist between triage `stg_code` and registry `strategy_id`, but 62 case-folded collisions exist (`Stg001` vs `STG001`).
- **Producer-Spec `candidate_id`:**
  - `producer_spec.json.candidate_id` uses free-text names (`QL_ALPHA_ADA_TWO_CANDLE_SR_1H`, `KELL_WEDGE_POP_CROSSBACK`), matching 0 registry IDs directly. However, enclosing directory paths strictly follow `STG###_<name>` format across all 63/63 files.
- **Design Rule Characterization:**
  - The Lead formulates this strictly as a design rule in `P031_M2_SOURCE_CENSUS_20260916.md:29` (*"Design rule that follows (Pattern 8, 'the name is not the identity'): the importer joins by exact, case-sensitive identity only; `stg_code` is never an identity..."*). It is not smuggled in as an owner decision.

---

## 6. Inference Creep and Non-Goals Audit

1. **Owner Authority Boundary:**
   Every unruled decision point is formulated as an explicit question (Q7..Q13) rather than decided in place:
   - Extension of Table 4a is framed as Question Q7 with explicit options (A: adopt 4a′, B: `FORWARD_PAPER_CANDIDATE` → `UNKNOWN`, C: no extension / 60 stay `UNKNOWN`).
   - Triage decision proxy is framed as Question Q9.
   - State lattice ordering (`STATE_RANK`) is framed as Question Q12.
2. **"WHAT_IF_NOT_RULED" Labeling:**
   The proposed extension is visibly and unambiguously labelled `WHAT_IF_NOT_RULED` across all code paths, output JSON summaries, and documentation sections (`subject/m2_dry_run.py:110`, `subject/run_whatif_4a_prime_SUMMARY.json:43`, `subject/P031_M2_MAPPING_DRY_RUN_20260916.md:3,8,42`, `subject/P031_M2_SOURCE_CENSUS_20260916.md:37-38`).
3. **Milestone 2 Build Gating (Q6 = B):**
   All three design documents prominently state that the M2 build is blocked until full Milestone 1 acceptance (`P031_M2_SOURCE_CENSUS_20260916.md:3,51`, `P031_M2_MAPPING_DRY_RUN_20260916.md:44,52`, `P031_M2_FIXTURE_DESIGN_20260916.md:3,36`).
4. **Preservation of Legacy Stores (Non-Goals):**
   No text claims, plans, or authorizes editing, retiring, de-tracking, or deleting legacy stores. Non-goals are strictly preserved.

---

## 7. D026 Fixture Design Honesty

All five fixture designs in `subject/P031_M2_FIXTURE_DESIGN_20260916.md` specify authentic mutants and discriminating observables:

1. **Fixture 1 (Conflicting Pair):**
   - **Input:** `STG9A1` with `current_status = "PROMOTE_TO_FORWARD_PAPER_TRADE"`, producer_spec `promotion_status = ["KEEP_AS_RESEARCH_NOTE"]` (both in Table 4a).
   - **GREEN:** Exactly 1 seed `STG9A1`, `state = PARKED`, tag `migrated-conflict`, provenance carrying both values verbatim.
   - **RED Mutant A ("First writer wins"):** Drops disagreement branch → `CANDIDATE`, fails both tag and provenance assertions.
   - **RED Mutant B ("Higher wins"):** Replaces `min` with `max` → `CANDIDATE`, fails state assertion even with tag present.
   - **Discrimination:** Discriminating on multiple independent observables (state, tag, provenance dict).

2. **Fixture 2 (Planted-Row Detection):**
   - **Input:** Census JSON (`STRATEGY_RESEARCH_REGISTRY.json = 63`) + scratch store with 64 rows.
   - **GREEN:** Enumeration measures 64, `matches_census = false`, `balanced = false`, run aborts write.
   - **RED Mutant ("Count from census"):** Bypasses fresh enumeration → writes 64 seeds, fails refusal assertion.
   - **RED Mutant ("Skip malformed rows"):** Skips planted row → fails Pattern 13 terminal disposition requirement.
   - **Discrimination:** Discriminating on exit status, balance flag, and row inclusion.

3. **Fixture 3 (`UNKNOWN` on Ambiguity):**
   - **Input:** Unmapped status `RESEARCH_BATCH`, composite with unmapped part `PROMOTE_TO_SANDBOX|NOT_A_LADDER_VALUE`, malformed JSON object in producer_spec.
   - **GREEN:** 3 `UNKNOWN` dispositions quoting offending values in `reason`, 0 seeds.
   - **RED Mutant ("Prefix guess"):** Maps `RESEARCH_*` to `CAPTURED` → fails `unknown_target_count` and seed count assertions.
   - **Discrimination:** Discriminating on zero seeds, `UNKNOWN` count, and listed targets.

4. **Fixture 4 & Fixture 5 (Proposed Additions):**
   - Fixture 4 (Identity Collision) and Fixture 5 (Idempotent Re-Run) are explicitly headed as `"Fixture 4 (proposed addition)"` and `"Fixture 5 (proposed addition)"`, clearly distinguishing them from the plan's baseline three. Both feature discriminating RED/GREEN pairs.

---

## 8. Owner Questions (Q7..Q13) Corroboration

- **Structure and Traceability:** Questions Q7 through Q13 present structured options with explicit consequences tied directly to empirical numbers measured in the census:
  - Q7 is tied directly to the 60 unmapped registry statuses and 17 `FORWARD_PAPER_CANDIDATE` rows.
  - Q8 is tied to the 62 case-folded collisions and 43 advisory orphans.
  - Q9 is tied to the 172 triage rows and 12 potential proxy rows.
  - Q10 is tied to the 43 unhosted advisory verdicts.
  - Q11 is tied to the 251 JSON files bearing 4b diagnostic labels outside the stores.
  - Q12 is tied to the conflict resolution winner.
- **Q13 Verification against M1 Ledger Code (`sources/p031_lifecycle_ledger_48bd70de_lines1-230.py`):**
  - Line 62–64 confirms: `REGISTRAR_TRANSITIONS = frozenset({(None, "CAPTURED", "CAPTURED"), ...})`. The registrar admits initial candidates *only* through `(None, "CAPTURED", "CAPTURED")`. Seeding at `CANDIDATE`, `TRIAGED`, or `PARKED` cannot execute without an initial transition admission such as `(None, "SEED_IMPORT", <state>)`.
  - Line 197 confirms: `source_kind TEXT NOT NULL CHECK (source_kind = 'FIXTURE')`. The schema rejects any `source_kind` other than `'FIXTURE'`.
  - Q13 accurately reflects these exact code constraints and correctly identifies the schema and registrar widening required for Milestone 2.

---

## 9. Findings (Numbered by Severity)

- **Finding 1 (Severity: NIT) — `subject/m2_dry_run.py:44`:**  
  `STATE_RANK = {"REJECTED": 0, "PARKED": 1, "CAPTURED": 2, "TRIAGED": 3, "CANDIDATE": 4}` establishes an explicit state order for Q4 A (`min()`). While the owner ruled "lower of the two mapped states", the owner did not formally define the total ordering. The Lead correctly surfaced this as Question Q12 to the owner, but the dry-run code relies on this specific assumption to resolve its what-if conflicts.
- **Finding 2 (Severity: NIT) — `subject/m2_dry_run.py:109`:**  
  `RANK_4A.setdefault(old, -1)` defaults proposed extension entries to rank `-1` in composite ladder comparisons, placing them strictly below ruled Table 4a values. This is an engineering assumption for the what-if dry run; it is properly noted in Q7 documentation.
- **Finding 3 (Severity: NIT) — `subject/m2_dry_run.py:240`:**  
  `disposed["producer_spec.json"] += len(seen_ps)` balances `producer_spec.json` through its joined parent registry rows rather than via independent disposition records. This design pattern (terminal disposition on the parent with secondary writer in provenance `also`/`also_value`) is fully explained in `P031_M2_MAPPING_DRY_RUN_20260916.md:14-16`, but the synthetic counter increment is an implementation artifact of the dry-run script.

*(No findings of severity REQUIRED were identified; no change request is warranted.)*

---

## 10. Native Read Coverage and Continuations

All reads were native `view_file` calls restricted to `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_M2_DESIGN_20260916/` with line limits $\le 150$:

1. `PACKET_SHA256SUMS.txt`: lines 1–20 (complete in 1 range).
2. `subject/P031_M2_SOURCE_CENSUS_20260916.md`: lines 1–52 (complete in 1 range).
3. `subject/P031_M2_MAPPING_DRY_RUN_20260916.md`: lines 1–53 (complete in 1 range).
4. `subject/P031_M2_FIXTURE_DESIGN_20260916.md`: lines 1–37 (complete in 1 range).
5. `subject/census.json`: lines 1–150; continuation lines 151–209 (complete in 2 ranges).
6. `subject/m2_dry_run.py`: lines 1–150; continuation lines 151–294 (complete in 2 ranges).
7. `subject/m2_census.py`: lines 1–117 (complete in 1 range).
8. `subject/table_4a_prime_PROPOSED.json`: lines 1–9 (complete in 1 range).
9. `subject/run_as_ruled_SUMMARY.json`: lines 1–150; continuation lines 151–300; continuation lines 301–341 (complete in 3 ranges).
10. `subject/run_planted_SUMMARY.json`: lines 1–150; continuation lines 250–341 (complete in 2 ranges).
11. `subject/run_whatif_4a_prime_SUMMARY.json`: lines 1–150; continuation lines 400–468 (complete in 2 ranges).
12. `sources/FOLD_section4_to_6.md`: lines 1–64 (complete in 1 range).
13. `sources/DECISIONS_rows_P031.md`: lines 1–5 (complete in 1 range).
14. `sources/P031_M2_SCOPE_PACKET_DRAFT_20260915.md`: lines 1–63 (complete in 1 range).
15. `sources/producer_spec_promotion_status_listing.txt`: lines 1–64 (complete in 1 range).
16. `sources/p031_lifecycle_ledger_48bd70de_lines1-230.py`: lines 1–150; continuation lines 151–231 (complete in 2 ranges).
17. **Spot Checks:**
    - `sources/scratch_STRATEGY_RESEARCH_REGISTRY.json`: lines 1–100, 101–230, 1200–1300, 1800–1950, 2500–2650, 3350–3494.
    - `sources/scratch_TRIAGE_CANDIDATE_REGISTRY.json`: lines 1–100, 2000–2050.
    - `sources/scratch_AI_QUANTLENS_VERDICT_REGISTRY.json`: lines 1–100, 1000–1050, 3000–3050, 3850–3950.
    - `sources/scratch_VARIANT_LOG_REGISTRY.json`: lines 1–100.

---

## 11. Scope Not Verified (Execution Sandbox Boundary)

As a strictly read-only, non-executing documentary corroborator (`SUPPLEMENTAL_UNEXECUTED`), the following were not executed:
1. Dynamic execution of `subject/m2_census.py` or `subject/m2_dry_run.py`.
2. Git command execution against canonical repository `C:/LAB/Tradingview_LAB_CLEAN` to recalculate live blob OIDs.
3. Verification of full `reconciliation_report.json` byte payloads beyond the summary artifacts, digests, and code logic provided.

---

```json
{
  "part": "P031_M2_DESIGN_GEMINI",
  "verdict": "PASS-WITH-NITS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "census_60_of_63_claim": "CONFIRMED",
  "inference_creep": [],
  "findings": [
    {
      "finding_id": "NIT-01",
      "file_line": "subject/m2_dry_run.py:44",
      "severity": "NIT",
      "description": "STATE_RANK lattice (REJECTED < PARKED < CAPTURED < TRIAGED < CANDIDATE) is an assumed total order for Q4 A lower-state resolution; properly surfaced to owner as Q12."
    },
    {
      "finding_id": "NIT-02",
      "file_line": "subject/m2_dry_run.py:109",
      "severity": "NIT",
      "description": "Proposed extension entries defaulted to rank -1 in composite ladder comparisons, ranking below ruled Table 4a entries; noted in Q7 documentation."
    },
    {
      "finding_id": "NIT-03",
      "file_line": "subject/m2_dry_run.py:240",
      "severity": "NIT",
      "description": "producer_spec balance counter incremented via parent registry rows rather than separate disposition records, adhering to Pattern 13 design rules."
    }
  ],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
