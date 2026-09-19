# Independent Read-Only Detection Review: WP-P0-21 S1 Catalogue-Only Slice

**Commit Under Review:** `701c5ddde347dfb6a939ddf0c88378d1e31453a0` on `feature/p021-s1-policy-v1-numbers-20260915`  
**Base:** `origin/master` (`fcac0ac67cf2682693ad28138b1a56e15a0846f2`)  
**Reviewer Role:** Gemini 3.8 Flash (High) — Independent Supplemental Read-Only Detection Reviewer (`SUPPLEMENTAL_UNEXECUTED`)  
**Authorization / Provenance:** `OD-20260915-P021-S2-RECOMMENDED-1` answering `P021_OPTIONS_PACKET_S2_20260915.md`  

---

## 1. Fidelity Table

| Decision / Blocker | Owner's Recorded Word (`DECISIONS_rows_P021.md`) | Packet Text Option Definition (`P021_OPTIONS_PACKET_S2_20260915.md`) | Exact Code Lines in `p021_readiness_rules_HEAD.py` | Comparison |
|---|---|---|---|:---:|
| **B-02 Value** (`gap_ratio_max`) | Row `OD-20260915-P021-S2-RECOMMENDED-1`: `P021_DECISION_3 = T`: `gap_ratio_max = 0.0001` on `gap_ratio_metric = "m2_missing_bar_ratio"` (B-02 CLOSED as a value; coverage stays a separate rule). | §1: `T one-bar tolerance — RECOMMENDED`: `0.0001` (≈ 24 missing bars in a 245,873-bar 5m series; ≈ 2 h of 5m data); `gap_ratio_metric = "m2_missing_bar_ratio"` pinned explicitly; coverage is a separate rule (`requested_period_coverage`). | Lines 58 (`"P021_DECISION_3": "T"`), 173–184 (`ClosedNumber("gap_ratio_max", 0.0001, ...)`), 241–242 (`("gap_ratio_max", CLOSED_NUMBER_VALUES["gap_ratio_max"])`, `("gap_ratio_metric", "m2_missing_bar_ratio")`), 246 (removed from `missing_numbers` and `missing_rules`). | **EQUAL** |
| **B-17 Pin** (`gap_ratio_formula_id`) | Row `OD-20260915-P021-S2-RECOMMENDED-1`: `gap_ratio_formula_id = "m2_missing_bar_ratio@data_gap_ratio.py v1 (fixed-step 24/7, half-open span, leading/trailing absence excluded)"`. | §2: Ratify `gap_ratio_formula_id = "m2_missing_bar_ratio@data_gap_ratio.py v1 (fixed-step 24/7, half-open span, leading/trailing absence excluded)"` — recommended; formula the code already has in `data_gap_ratio.py`. | Lines 199–202 (`GAP_RATIO_FORMULA_ID = (...)`), 243 (`("gap_ratio_formula_id", GAP_RATIO_FORMULA_ID)`), 246 (`gap_ratio_formula.B17` removed from `missing_rules`). | **EQUAL** |
| **B-13 Pin** (`dataset_hash_contract`) | Row `OD-20260915-P021-S2-RECOMMENDED-1`: `P021.DATA_QUALITY.dataset_hash_required` is satisfied by the `ds-v1` digest of the bundle the check scanned (`dataset_manifest_hash = <ds-v1 digest>`, contract named; P0-20/P0-30 hashes stay separate fields). | §3: Ratify that `P021.DATA_QUALITY.dataset_hash_required` is satisfied by the `ds-v1` digest of the bundle the check actually scanned (recommended; P0-20/P0-30 hashes identify other objects and stay separate fields). | Lines 244 (`("dataset_hash_contract", "ds-v1")`), 246 (`dataset_hash_contract.B13` removed from `missing_rules`). | **EQUAL** |
| **B-05 Metric** (`divergence_metric`) | Row `OD-20260915-P021-S2-RECOMMENDED-1`: `P021_DIVERGENCE_METRIC = M-C` (both failure modes recorded in the shadow window; B-05 definition CLOSED; B-06/B-07 stay measure-first). | §4: Option M-C: `both — M-B as the gate on signal fidelity, M-A as the economic divergence, each with its own tolerance`; separates "different decisions" from "same decisions, different economics". | Lines 59 (`"P021_DIVERGENCE_METRIC": "M-C"`), 206–212 (`DIVERGENCE_METRIC_DEFINITION = (...)`), 274 (`("divergence_metric", "M-C")`, `("divergence_metric_definition", DIVERGENCE_METRIC_DEFINITION)`), 276 (`divergence_metric.B05` removed from `missing_rules`). | **EQUAL** |

### Fidelity Analysis Points
1. **Value & Metric (B-02):** `gap_ratio_max` is strictly `0.0001` (neither `0.0` nor `0.001`). `gap_ratio_metric` is explicitly set to `"m2_missing_bar_ratio"`.
2. **Formula Identity & Computation Match (B-17):** The pinned string `"m2_missing_bar_ratio@data_gap_ratio.py v1 (fixed-step 24/7, half-open span, leading/trailing absence excluded)"` matches exactly what `data_gap_ratio.py` computes:
   - **Numerator:** `missing_bars = sum(missing_by_gap)` (bars missing within internal intervals where `delta > 1.5 * step`, lines 69–71).
   - **Denominator:** `expected_bars = round(span / step) + 1` (line 65).
   - **Span & Boundaries:** `span = values[-1] - values[0]` (line 62); only timestamps from first to last observed entry are evaluated, excluding unrequested leading and trailing absence.
   - **Calendar/Step:** `step = TIMEFRAME_SECONDS[timeframe]` enforces fixed-step 24/7 semantics (line 54).
3. **Dataset Hash Identity (B-13):** `dataset_hash_contract` is pinned to `"ds-v1"`. It is not equated with P0-20's `evaluation_run_hash`/`dataset_manifest_sha` or P0-30's provenance manifest.
4. **Divergence Metric & Definition (B-05):** `DIVERGENCE_METRIC_DEFINITION` records BOTH failure modes verbatim: (a) decision-level divergence (backtest intents with no forward counterpart or different side/size class) and (b) outcome-level divergence (mean absolute difference of realized R-multiples over matched pairs). Tolerances (`divergence_tolerance`), window length (`divergence_window_length`), and minimum pairs (`divergence_min_paired_observations`) remain properly in `OPEN_NUMBERS`.

---

## 2. Fence Integrity Table

| Invariant / Check | Code Location in `p021_readiness_rules_HEAD.py` | Implementation Verification | Status |
|---|---|---|:---:|
| **All rules retain engine prerequisite** | Lines 219, 225, 231, 246, 263, 269, 276 | `accepted_corrected_engine.B01` is present in `missing_rules` across all 7 rules in `RULES`. | **PASS** |
| **`validate_catalog` blocks ready-looking rules** | Lines 336–338 | Loop raises `ValueError(f"{rule.check_id} could be presented as ready")` if `not rule.missing_numbers and not rule.missing_rules`. | **PASS** |
| **`readiness_record()["ready"]` cannot be True** | Lines 357–362 | `"ready": False`, `"status": "REFUSED"`, and all checks carry `"status": "REFUSED"` with `_refusal(rule)`. | **PASS** |
| **`EXPECTED_OPEN_NUMBER_NAMES` set size & members** | Lines 190–196 | Exactly 3 numbers: `divergence_tolerance`, `divergence_window_length`, `divergence_min_paired_observations`. | **PASS** |
| **`self_check()` modified-copy arm detection** | Lines 395–403 | Re-targeted from `RULES[3]` (`gap_ratio_max`) to `RULES[6]` (`divergence_tolerance`). Replacing `missing_numbers=()` causes `validate_catalog` to raise `ValueError("open-number refusal wiring changed...")`, caught and asserted on `"divergence_tolerance" in str(error)`. | **PASS** |

No fence weakening detected.

---

## 3. Policy-Set Artifact Statement

1. **Untouched Artifact:** `MTC_COMMAND_CENTER/03_QUANTLENS/tools/strategy_type_policy_set.py` is absent from `subject/DELTA_fcac0ac6_HEAD.diff` and `subject/DELTA_STAT_fcac0ac6_HEAD.txt`. The accepted fixture `ACCEPTED_ARTIFACT_FIXTURE` in tests retains `"gap_ratio_max": None` and hash `p021pol-v1:4a807136e78650ef393556f91d3448855fc397ee9f0eee6efb7594c9dbdf69f2`.
2. **Test Change Scope:** `test_strategy_type_policy_set_HEAD.py` diff contains only:
   - Added explanatory comment at lines 94–95 documenting that the accepted artifact retains `None` until B-22 ratification.
   - Removal of `"gap_ratio_max"` from `test_current_readiness_catalogue_stays_refused` (line 181 of diff), aligning the expected open set to the 3 divergence numbers.
3. **Contradiction Analysis:** The catalogue holding `gap_ratio_max = 0.0001` while the policy-set artifact holds `shared.gap_ratio_max = None` creates **no actionable contradiction for consumers**. First, `readiness_record()["ready"]` remains unconditionally `False` (due to `accepted_corrected_engine.B01`). Second, `shared.gap_ratio_max` is defined as nullable in `strategy_type_policy_set.py`. Any attempt by an engine consumer to inject `0.0001` into the policy set without recomputing and ratifying the hash would cause `validate_policy_set` to raise `PolicySetError: version mismatch`.
4. **Honest Scope Disclosure:** `POLICY_SET["s2_scope"]` (lines 67–70 of `p021_readiness_rules_HEAD.py`) explicitly states:  
   `"catalogue only: gap_ratio_max closed here; the hashed strategy_type_policy_set artifact still carries gap_ratio_max = None until the whole set is ratified (B-22)"`.  
   The gap is documented honestly and accurately.

---

## 4. Tests and RED Arms Verification

1. **RED Arm 1 (New Tests on Old Catalogue):**  
   - In `test_p021_eligibility_HEAD.py`, `assert_readiness_fence()` is invoked in both `setUp()` (line 112) and `tearDown()` (line 115) of `P021ContractTestCase`.
   - The updated fence asserts `len(record["open_numbers"]) == 3` (line 90) and asserts limits for `gap_ratio_max = 0.0001` on `P021.DATA_QUALITY` (line 94).
   - On the old catalogue (`fcac0ac6`), `record["open_numbers"]` had length 4 and lacked those limits. Thus, every test case inheriting from `P021ContractTestCase` fails in `setUp()`.
   - `sources/LEAD_RED_ARM_1_new_tests_old_catalogue.txt` confirms: **47 failed, 5 passed, 3 subtests passed**.
2. **RED Arm 2 (Old Tests on New Catalogue):**  
   - The old `test_p021_eligibility.py` asserted `len(record["open_numbers"]) == 4` and included `"gap_ratio_max"` in `_EXPECTED_OPEN_NUMBERS`.
   - On the new catalogue (`701c5ddd`), `open_numbers` has length 3, causing the old `setUp()` fence and `test_current_readiness_catalogue_stays_refused` to fail.
   - `sources/LEAD_RED_ARM_2_old_tests_new_catalogue.txt` confirms: **47 failed, 5 passed, 3 subtests passed**.
3. **RED Arm 3 (Mutant with Dropped `accepted_corrected_engine.B01`):**  
   - When a mutant drops `accepted_corrected_engine.B01` from `P021.DATA_QUALITY`, both `missing_numbers` and `missing_rules` become empty.
   - `validate_catalog()` executes lines 337–338:
     ```python
     if not rule.missing_numbers and not rule.missing_rules:
         raise ValueError(f"{rule.check_id} could be presented as ready")
     ```
   - `sources/LEAD_RED_ARM_3_mutant_b01_dropped.txt` confirms: `ValueError: P021.DATA_QUALITY could be presented as ready`, exit code 1.
   - This is the exact correct mutant demonstrating catalogue fail-closed behavior.
4. **Vacuity Assessment:**  
   - All assertions test substantive invariant values (set memberships, exact strings, float values, exception catches). None are vacuous.

---

## 5. Scope Statement

1. **Touched Files:** Exactly 3 files are modified in commit `701c5ddd`:
   - `MTC_COMMAND_CENTER/03_QUANTLENS/tools/p021_readiness_rules.py` (+62, -10)
   - `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p021_eligibility.py` (+18, -1)
   - `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_strategy_type_policy_set.py` (+3, -1)
2. **Protected Trees:** No modifications in `02_MTC_BACKTEST`, `07_ADAPTERS`, `01_PINE`, or `MTC_V2`. Confirmed by `sources/LEAD_GUARD.txt` (`[protected] none`, `[pine-alert] PASS files=21 matches=0 allowlist=0`).
3. **Pre-existing Ruff F401:**  
   - `sources/LEAD_RUFF.txt` reports one fixable issue: `json` unused in `test_strategy_type_policy_set.py:4`.
   - In `subject/DELTA_fcac0ac6_HEAD.diff`, the diff hunks for `test_strategy_type_policy_set.py` begin at line 91. Lines 1–90 were completely untouched by commit `701c5ddd`.
   - Inspection of `subject/test_strategy_type_policy_set_HEAD.py` line 4 confirms `import json` was present on `origin/master` (`fcac0ac6`) prior to this commit. The slice neither introduced nor modified this import.

---

## 6. Exact Read Coverage

All reads performed via native `view_file` calls (each chunk ≤ 150 lines):

1. `PACKET_SHA256SUMS.txt`: lines 1–22 (complete)
2. `subject/DELTA_STAT_fcac0ac6_HEAD.txt`: lines 1–5 (complete)
3. `subject/COMMIT_HEAD.txt`: lines 1–29 (complete)
4. `subject/DELTA_fcac0ac6_HEAD.diff`:
   - Chunk 1: lines 1–150
   - Continuation 1: lines 151–185 (complete)
5. `subject/p021_readiness_rules_HEAD.py`:
   - Chunk 1: lines 1–150
   - Continuation 1: lines 151–300
   - Continuation 2: lines 301–450
   - Continuation 3: lines 451–467 (complete)
6. `subject/test_p021_eligibility_HEAD.py`:
   - Chunk 1: lines 1–110 (the fence)
   - Continuation 1: lines 111–150 (setUp/tearDown and test harnesses)
7. `subject/test_strategy_type_policy_set_HEAD.py`: lines 1–127 (complete)
8. `sources/p021_readiness_rules_fcac0ac6.py`:
   - Chunk 1: lines 40–75 (policy set and open/closed definitions)
   - Chunk 2: lines 160–240 (rules and wiring prior to slice)
9. `sources/strategy_type_policy_set_fcac0ac6.py`: lines 20–60 (shared keys and constants)
10. `sources/data_gap_ratio_fcac0ac6.py`: lines 1–117 (complete)
11. `sources/P021_OPTIONS_PACKET_S2_20260915.md`: lines 1–43 (complete)
12. `sources/P021_S1_CATALOGUE_SLICE_BRIEF_20260915.md`: lines 1–24 (complete)
13. `sources/DECISIONS_rows_P021.md`: lines 1–4 (complete)
14. `sources/DIFF_STAT_fcac0ac6_701c5ddd.txt`: lines 1–2 (complete)
15. `sources/LEAD_GUARD.txt`: lines 1–16 (complete)
16. `sources/LEAD_PYTEST.txt`: lines 1–3 (complete)
17. `sources/LEAD_RED_ARM_1_new_tests_old_catalogue.txt`: lines 1–8 (complete)
18. `sources/LEAD_RED_ARM_2_old_tests_new_catalogue.txt`: lines 1–4 (complete)
19. `sources/LEAD_RED_ARM_3_mutant_b01_dropped.txt`: lines 1–3 (complete)
20. `sources/LEAD_RUFF.txt`: lines 1–2 (complete)
21. `sources/LEAD_SELF_CHECK.txt`: lines 1–9 (complete)
22. `sources/LEAD_VERIFICATION_P021_S1.md`: lines 1–20 (complete)

### Non-Empty NOT VERIFIED
As an unexecuted reviewer (`SUPPLEMENTAL_UNEXECUTED`), the following could not be independently executed or verified:
- Live terminal execution of `pytest`, `python p021_readiness_rules.py --self-check`, or `ruff`.
- Evaluation of any real market bundle or data feed (no engine evaluator exists under B-01).
- Canonical acceptance of the slice or verification of unmerged repository state outside packet `P021_S1_20260915`.

---

## 7. Findings

1. **NIT-1** (`subject/test_p021_eligibility_HEAD.py:96`):  
   The assertion `self.assertTrue(data_quality["limits"]["gap_ratio_formula_id"].startswith("m2_missing_bar_ratio@data_gap_ratio.py v1"))` verifies prefix conformance rather than testing strict equality against the full 97-character `GAP_RATIO_FORMULA_ID` string. While sufficient to verify formula version binding, exact equality would be stricter.
2. **NIT-2** (`subject/test_p021_eligibility_HEAD.py:105`):  
   The assertion `self.assertEqual({n["name"] for n in record["closed_numbers"] if n["name"] == "gap_ratio_max"}, {"gap_ratio_max"})` uses a comprehension filter. It is non-vacuous and ensures presence, but testing `"gap_ratio_max" in {n["name"] for n in record["closed_numbers"]}` would be more idiomatic.
3. **NIT-3** (`subject/test_strategy_type_policy_set_HEAD.py:4`):  
   Pre-existing unused import `import json` (Ruff F401) was inherited unchanged from `origin/master` (`fcac0ac6`).

---

```json
{
  "part": "P021_S1_GEMINI",
  "verdict": "PASS-WITH-NITS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "fidelity": {
    "B-02": "EQUAL",
    "B-17": "EQUAL",
    "B-13": "EQUAL",
    "B-05": "EQUAL"
  },
  "findings": [
    {
      "id": "NIT-1",
      "severity": "NIT",
      "path": "MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p021_eligibility.py:96",
      "description": "Assertion uses startswith on gap_ratio_formula_id rather than full string equality comparison."
    },
    {
      "id": "NIT-2",
      "severity": "NIT",
      "path": "MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p021_eligibility.py:105",
      "description": "Set comprehension filter used to assert presence of gap_ratio_max in closed_numbers rather than direct membership test."
    },
    {
      "id": "NIT-3",
      "severity": "NIT",
      "path": "MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_strategy_type_policy_set.py:4",
      "description": "Unused import 'json' (F401) pre-exists on master fcac0ac6 and remains unreferenced."
    }
  ],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
