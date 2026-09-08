# W342 — contract self-test alignment and provenance prose correction

## Verdict

**COMPLETE.** The nine stale failing cases identified by W279C were aligned to owner-bound design expectations without changing `verify_bceg.py`, kernel code, sealed inputs, catalog, goldens, manifests, anchors, probes, or baseline bytes. The intentionally open `test_probe_driver_refuses_unclosed_base_before_variant_comparison` case remains unchanged and red. The post-change suite measured `1 failed, 312 passed in 6.70s`; the frozen legacy replay measured `SURFACES_EQUAL=34 MISMATCH=0`; and the canonical gate's six-entry refusal list is byte-identical to W316D. The changed expectations and their authority comments are at `test_results_corrected.py:156-161` and `test_verify_bceg.py:712-717,1431-1459,1741-1744,2080-2097,2220-2226,2254-2261`. The provenance machine fields remain `PRESENT_AT_BASE`, blob `b811ce9d...`, and base `5e8e5794...` at `expected_provenance_exceptions.json:5-6,19`; only the false sentence in `reason` changed (`:16`).

Worktree: `C:\WP012BUILD`. Branch: `feature/wp-p0-12-corrected-vnext-20260831`. Starting HEAD: `de7c5c0105fdb54bea94597cb1532c565327e8fa`. Gate-1 tier: T1 because executable contract tests changed; live-dependency status: none. The owner approvals are recorded at `C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:1150-1165,1225-1234,1255-1265`.

## Initial suite — ten failures quoted verbatim

Command, from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
10 failed, 303 passed in 7.73s
```

The ten failure names and assertion lines were:

1. `test_results_corrected.py::test_corrected_manifest_marks_an_unconsumed_cost_schedule_without_padding_digest`

   ```text
   >       assert manifest["cost_schedule_id"] == "NOT_CONSUMED"
   E       AssertionError: assert 'SYNTH-COST-RULE2-07-RED-V1' == 'NOT_CONSUMED'
   ```

2. `test_verify_bceg.py::test_w305_item3_committed_record_states_it_is_not_evidence`

   ```text
   >       assert record["exceptions"][0]["lane_ids"] == ["W156", "W167", "W172"]
   E       AssertionError: assert ['W156', 'W16...172', 'W316D'] == ['W156', 'W167', 'W172']
   ```

3. `test_verify_bceg.py::test_probe_driver_refuses_unclosed_base_before_variant_comparison`

   ```text
   >       assert identity_receipt["measured_failed_check"] == "CLOSED_SET_VIOLATION"
   E       AssertionError: assert 'CORRECTED_EXPECTATION' == 'CLOSED_SET_VIOLATION'
   ```

4. `test_verify_bceg.py::test_probe_cannot_claim_target_membership_when_base_is_refused`

   ```text
   >       assert probe["comparator_first_differing_node"] == comparator_first_node
   E       AssertionError: assert '/EVENT_SURFA.../signed_delta' == '/EVENT_SURFA.../signed_delta'
   ```

5. `test_verify_bceg.py::test_raw_kernel_decision_trail_contains_each_evaluated_closed_reason[RULE2-08-RED-expected_decisions14]`

   ```text
   >       assert [member["decision"] for member in decisions] == expected_decisions
   E       AssertionError: assert ['SEMANTICS_V..._ELIGIBILITY'] == ['SEMANTICS_VALIDATED']
   ```

6. `test_verify_bceg.py::test_raw_kernel_decision_trail_contains_each_evaluated_closed_reason[RULE2-08-GREEN-expected_decisions15]`

   ```text
   >       assert [member["decision"] for member in decisions] == expected_decisions
   E       AssertionError: assert ['SEMANTICS_V..._ELIGIBILITY'] == ['SEMANTICS_VALIDATED']
   ```

7. `test_verify_bceg.py::test_rule2_08_raw_kernel_is_not_seeded_from_legacy_state[RULE2-08-RED]`

   ```text
   >       assert result["run_manifest"]["cost_schedule_id"] == "NOT_CONSUMED"
   E       AssertionError: assert 'SYNTH-COST-RULE2-07-RED-V1' == 'NOT_CONSUMED'
   ```

8. `test_verify_bceg.py::test_rule2_08_raw_kernel_is_not_seeded_from_legacy_state[RULE2-08-GREEN]`

   ```text
   >       assert result["run_manifest"]["cost_schedule_id"] == "NOT_CONSUMED"
   E       AssertionError: assert 'SYNTH-COST-RULE2-07-GREEN-V1' == 'NOT_CONSUMED'
   ```

9. `test_verify_bceg.py::test_w305_item6_refuses_missing_sealed_equal_price_target_book`

   ```text
   >       with pytest.raises(GateRefusal) as caught:
   E       Failed: DID NOT RAISE <class 'mtc_v2.tests.corrected_vnext.verify_bceg.GateRefusal'>
   ```

10. `test_verify_bceg.py::test_all_declared_corrected_scenarios_execute_or_refuse_missing_input`

    ```text
    >       assert [member["scenario_id"] for member in observed] == [
    E       AssertionError: assert ['RULE2-01-RE...3-GREEN', ...] == ['RULE2-01-RE...3-GREEN', ...]
    ```

The third case above is the W314B-reverted 02-A owner question. Its assertions remain byte-identical to starting HEAD at `test_verify_bceg.py:1367-1419`; it is the sole post-change failure.

## Nine expectation alignments

| Case | Before → after assertion | Owner decision | Design authority | Final source |
|---|---|---|---|---|
| corrected manifest, RULE2-08-RED | `cost_schedule_id == NOT_CONSUMED`; digest absent → exact RED RULE2-07 id and SHA-256 | 137/144 | `P012_FRESH_DESIGN_V1.md:490,932` | `test_results_corrected.py:156-161` |
| provenance exception record | lanes W156/W167/W172; absent base; null blob → add W316D; `PRESENT_AT_BASE`; exact base blob | 134/135 | `P012_FRESH_DESIGN_V1.md:701` | `test_verify_bceg.py:709-717` |
| probe 08-A membership and outcome | catalog comparator `/cash_events/0/signed_delta`, receipt `NOT_DETECTED/CLOSED_SET_VIOLATION` → `/cash_events/1/signed_delta`, `DETECTED/CORRECTED_EXPECTATION`, traversal-first `/cash_events`, target changed | 144 | `P012_FRESH_DESIGN_V1.md:498,558-560` | `test_verify_bceg.py:1431-1459` |
| RULE2-08-RED decision trail | `[SEMANTICS_VALIDATED]` → add `FUNDING_ELIGIBILITY` | 136/137/144 | `P012_FRESH_DESIGN_V1.md:1278,1420-1425` | `test_verify_bceg.py:1741-1742` |
| RULE2-08-GREEN decision trail | `[SEMANTICS_VALIDATED]` → add `FUNDING_ELIGIBILITY` | 136/137/144 | `P012_FRESH_DESIGN_V1.md:1278,1420-1425` | `test_verify_bceg.py:1743-1744` |
| RULE2-08-RED raw kernel | unconsumed cost, empty cash/funding, cumulative 0 → RED RULE2-07 cost, cash/funding `[-0.1]`, cumulative `-0.1` | 137/144 | `P012_FRESH_DESIGN_V1.md:488-492,1107` | `test_verify_bceg.py:2080-2097` |
| RULE2-08-GREEN raw kernel | unconsumed cost → GREEN RULE2-07 cost; in-window cash/funding remain empty and cumulative remains 0 | 137/144 | `P012_FRESH_DESIGN_V1.md:490,494,1107` | `test_verify_bceg.py:2080-2097` |
| equal-price target book | `INPUT_DECLARATION_MISSING` refusal → no result refusal and exact `TARGET-FAR`, `TARGET-NEAR` order | 139/142 | `P012_FRESH_DESIGN_V1.md:402` | `test_verify_bceg.py:2218-2226` |
| all declared scenarios | exclude/refuse equal-price row → execute every RED/GREEN row and refuse none | 139/142/144 | `P012_FRESH_DESIGN_V1.md:402,488-494` | `test_verify_bceg.py:2254-2261` |

These are fixed values or independent structural predicates, not expectations computed from the observed value. The comments cite the decision and design line directly at each changed expectation site (`test_results_corrected.py:156`; `test_verify_bceg.py:712,1432,1451,1455,1741,1743,2080,2085,2220,2254`).

## Per-case RED/GREEN evidence

Every RED quote below comes from the single initial suite command above; every GREEN quote comes from a focused invocation of the exact node after the expectation change.

| Case | RED quote | GREEN quote |
|---|---|---|
| corrected manifest | `FAILED ...::test_corrected_manifest_marks_an_unconsumed_cost_schedule_without_padding_digest` / `assert ... == "NOT_CONSUMED"` | `1 passed in 0.06s` |
| provenance record | `FAILED ...::test_w305_item3_committed_record_states_it_is_not_evidence` / `assert ...["lane_ids"] == ["W156", "W167", "W172"]` | `1 passed in 0.12s` |
| probe 08-A membership | `FAILED ...::test_probe_cannot_claim_target_membership_when_base_is_refused` / `assert probe["comparator_first_differing_node"] == comparator_first_node` | `1 passed in 0.54s` |
| RULE2-08-RED decision trail | `FAILED ...::test_raw_kernel_decision_trail_contains_each_evaluated_closed_reason[RULE2-08-RED-expected_decisions14]` | `1 passed in 0.07s` |
| RULE2-08-GREEN decision trail | `FAILED ...::test_raw_kernel_decision_trail_contains_each_evaluated_closed_reason[RULE2-08-GREEN-expected_decisions15]` | `1 passed in 0.07s` |
| RULE2-08-RED raw kernel | `FAILED ...::test_rule2_08_raw_kernel_is_not_seeded_from_legacy_state[RULE2-08-RED]` / `cost_schedule_id == "NOT_CONSUMED"` | `1 passed in 0.08s` |
| RULE2-08-GREEN raw kernel | `FAILED ...::test_rule2_08_raw_kernel_is_not_seeded_from_legacy_state[RULE2-08-GREEN]` / `cost_schedule_id == "NOT_CONSUMED"` | `1 passed in 0.07s` |
| equal-price target book | `FAILED ...::test_w305_item6_refuses_missing_sealed_equal_price_target_book` / `Failed: DID NOT RAISE` | `1 passed in 0.08s` |
| all declared scenarios | `FAILED ...::test_all_declared_corrected_scenarios_execute_or_refuse_missing_input` / `assert [member["scenario_id"] ...] == [...]` | `1 passed in 0.11s` |

The intentionally retained 02-A case is not claimed as closed. Its RED assertion is quoted in the initial-suite section, and its open status is recorded in the owner ledger at `OWNER_DECISIONS_2026-08-29_EVENING.md:1243-1250`.

## Provenance record prose

The false sentence was replaced with exactly this true statement at `expected_provenance_exceptions.json:16`:

```text
Present at the M5 base 5e8e5794 as blob b811ce9d9d4efe574828c6d3fc2703bea71b71a8; the decision-134 authorization covers the post-base revisions W156/W167/W172.
```

The surrounding owner-decision explanation, W316D re-measurement sentence, schema, statement, and all machine fields are unchanged. The base blob and state are visible at `expected_provenance_exceptions.json:5-6`, the lanes at `:8-12`, the decision at `:14`, and the base SHA at `:19`.

## Frozen legacy replay

The W249 no-write method imported the frozen driver, ran all RED/GREEN rows through KERNEL_1, canonicalized both surfaces, and compared them in memory with the frozen baseline bytes. The method is documented in `W276C_REPORT.md:207-229`; the frozen driver/corpus identities remain recorded in `W342_GATE_RECEIPT.json:634-639,2418-2422`.

```text
SURFACES_EQUAL=34 MISMATCH=0
```

No baseline file was generated or changed.

## Full suite after

Command:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
FAILED mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_probe_driver_refuses_unclosed_base_before_variant_comparison
1 failed, 312 passed in 6.70s
```

The assertion remains `identity_receipt["measured_failed_check"] == "CLOSED_SET_VIOLATION"` at `test_verify_bceg.py:1393`, while the measured value is `CORRECTED_EXPECTATION`; this is the owner-held 02-A/Q-B case.

## Canonical gate — invoked once

Command, invoked exactly once from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:/tmp/P012_BASELINE_RUN --output C:/WP012BUILD/W342_GATE_RECEIPT.json
exit=1
claim_label=BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_REFUSED
```

The receipt is 93,689 bytes with SHA-256 `0b0d1e2c53dd846da3cf613f550fa7e25a7fe07aee5ffdac818f1c246ae5485d`, exactly byte-identical to `W316D_GATE_RECEIPT.json`. Its `legacy_reproduction` is `MATCH`, 17 scenarios, 34 surfaces (`W342_GATE_RECEIPT.json:634-639`). The refusal list below is quoted verbatim from `W342_GATE_RECEIPT.json:1091-1142`:

```json
  "refusals": [
    {
      "check_id": "SEMANTIC_COVERAGE_REVIEW_MISSING",
      "detail": "C:\\WP012BUILD\\MTC_COMMAND_CENTER\\01_MTC_PROJECT\\00_PYTHON\\mtc_v2\\tests\\corrected_vnext\\contracts\\semantic_coverage_review.json"
    },
    {
      "check_id": "EXPECTED_PATH_CHANGED_AFTER_BASE",
      "count": 18,
      "detail": "18 expected paths changed after the implementation base",
      "pointer": "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-RED.json",
      "pointers": [
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-RED.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-02-GREEN.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-02-RED.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-03-GREEN.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-03-RED.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-04-GREEN.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-04-RED.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-05-GREEN.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-05-RED.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-06-EQUAL-PRICE-RED.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-06-GREEN.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-06-RED.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-07-GREEN.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-07-RED.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-08-GREEN.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-08-RED.json",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/DERIVATIONS.md",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json"
      ]
    },
    {
      "check_id": "PROBE_NOT_DETECTED",
      "comparator_first_differing_node": "/RESULT_SURFACE/admitted",
      "measured_failed_check": "CLOSED_SET_VIOLATION",
      "scenario_id": "PROBE-P012-02-A"
    },
    {
      "check_id": "OBSERVED_EXTRA_MEMBER",
      "pointer": "/RESULT_SURFACE/run_manifest/cost_schedule_digest",
      "scenario_id": "RULE2-08-RED"
    },
    {
      "check_id": "CORRECTED_EXPECTATION_MISMATCH",
      "pointer": "/EVENT_SURFACE/cash_events",
      "scenario_id": "RULE2-08-RED"
    },
    {
      "check_id": "OBSERVED_EXTRA_MEMBER",
      "pointer": "/RESULT_SURFACE/run_manifest/cost_schedule_digest",
      "scenario_id": "RULE2-08-GREEN"
    }
  ],
```

The six objects, their order, their members, and their values are unchanged from `W316D_GATE_RECEIPT.json:1091-1142`. This lane fixed no gate refusal.

## Scope and diff verification

`git diff --check` passed before report creation. The substantive diff before this report was exactly three tracked files plus the required new receipt: one prose line in `expected_provenance_exceptions.json`; expectation-only changes in the two self-test files; and `W342_GATE_RECEIPT.json`. The names of two functions still describe the superseded behavior (`test_corrected_manifest_marks_an_unconsumed...` and `test_w305_item6_refuses_missing...`) because the lane explicitly authorized expectation changes only, not renaming tests. No other model, CLI assistant, network endpoint, host, broker, venue, deploy, or trading action was used.

## Discrepancies

1. The lane title and commit message summarize authority as decisions 136/137/144, but W279C's binding per-case table assigns the provenance-record case to decision 135 and the equal-price cases to decisions 139/142 (`C:\tmp\LANE_PROMPTS_20260828\W279C_REPORT.md:259-270`). The repository-backed expectations therefore cite 135 and 139/142 where applicable (`test_verify_bceg.py:712,2220,2254`) rather than falsely attributing every change to 136/137/144.
2. `expected_provenance_exceptions.json:20` names `MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-29_EVENING.md`, but that path is absent in this worktree. The record exists in the documentation worktree at `C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md`, where decisions 134-144 were read at `:969-974,1150-1174,1225-1235,1255-1265`. The stale reference was left unchanged because the lane requires every byte other than the false provenance sentence to remain fixed.
