# W344 harness correction report

## Verdict

**PASS for the scoped W344 correction; 0 new findings; 2 repository-over-prompt discrepancies recorded.** The closed-set validator now admits `/RESULT_SURFACE/admitted` exactly when the validated DEF-P012-02 terminal decision is `MIN_NOTIONAL_ADMITTED` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:879-899`). The canonical receipt records all ten probes DETECTED, including PROBE-P012-02-A at `CORRECTED_EXPECTATION`, and only the pre-existing section-16 review refusal remains (`W344_GATE_RECEIPT.json:479-655`).

The owner launch marker existed before work began, and the worktree was clean at required HEAD `5a178ca251e96fa2a915f59b110a7439b4439f51` on non-master branch `feature/wp-p0-12-corrected-vnext-20260831`; those were the lane's explicit preconditions (`C:\tmp\LANE_PROMPTS_20260828\LANE_W344_HARNESS_02A_ADMITTED.md:3-7`). No push, PR, merge, kernel, golden, input, catalog, manifest, anchor, probe, or design write was performed; the implementation diff is confined to the two authorized harness/test paths, plus the required receipt and this report (`C:\tmp\LANE_PROMPTS_20260828\LANE_W344_HARNESS_02A_ADMITTED.md:6-7`, `C:\tmp\LANE_PROMPTS_20260828\LANE_W344_HARNESS_02A_ADMITTED.md:22-25`).

## Design authority quoted exactly

Current design identity is `WP-P0-12 CORRECTED_VNEXT Fresh-Family Design v1.17` (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1`). Section 23.4 states (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1420-1427`):

> Only these conditional top-level members are admitted:
>
> | Member | Required exactly when | Forcing text |
> |---|---|---|
> | `order_notional` | DEF-P012-01, DEF-P012-02, or DEF-P012-05 declares the entry-sizing/notional projection | Sections 7-8 and section 11 expected changes. It is absent from RULE2-04/06/07/08 results. |
> | `admitted` | the DEF-P012-02 minimum-notional predicate terminates in admission | Section 8 GREEN admission/refusal projection. `AMENDMENT-CHOICE`: retain the positive boolean rather than infer admission from an empty refusal array. |
> | `guards` | a declared guard projection is evaluated | Section 13 and section 14's OPEN-10-controlled explicit comparison nodes. |
> | `cumulative_funding` | every DEF-P012-08 RESULT, whether the schedule event is eligible or ineligible | Section 14 names cumulative funding but is silent about RESULT-member presence when no position is eligible; section 15.3 requires a version-shaped RESULT without fixing this condition. `AMENDMENT-CHOICE`: require the member on both DEF-P012-08 rows as the minimal fixed shape. |

Section 23.5 gives the exact requested wording (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1537-1541`):

> 6. **G76-07:** re-derive the top-level RESULT member set on all 17 rows; retain `order_notional`
>    only on DEF-P012-01/02/05, `admitted` only on admitted DEF-P012-02, `guards` only when evaluated,
>    and unconditionally require `cumulative_funding` on both DEF-P012-08 rows under the labeled
>    section-23.4 choice. Remove the top-level `collision` object from every DEF-P012-06 result; its one
>    receipt is `decision_events.COLLISION_RESOLVED` with section 23.1's closed boolean domain.

Decision 143 re-targets PROBE-P012-02-A to the kernel-vs-contract-tables `CORRECTED_EXPECTATION` comparator, while preserving `/RESULT_SURFACE/admitted` as a required member of the changed-node set (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:273-303`).

## RED then GREEN

The named regression now loads the refused DEF-P012-02 corrected artifact, asserts that `admitted` is absent, sends its surfaces through the GREEN base row's closed-set validator, checks that `/RESULT_SURFACE/admitted` is a comparator difference, and then drives the actual PROBE-P012-02-A modified copy (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1367-1443`). Its terminal assertions require DETECTED at `CORRECTED_EXPECTATION`, first comparator difference `/EVENT_SURFACE/cash_events`, with the expected admitted node changed (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1445-1454`).

RED, after changing only the test and before changing the harness:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_probe_driver_refuses_unclosed_base_before_variant_comparison -q
FAILED test_probe_driver_refuses_unclosed_base_before_variant_comparison
E mtc_v2.tests.corrected_vnext.verify_bceg.GateRefusal: CLOSED_SET_VIOLATION: missing member admitted
1 failed in 0.30s
```

The RED reaches the old unconditional role-based requirement at the exact member named by the lane (`C:\tmp\LANE_PROMPTS_20260828\LANE_W344_HARNESS_02A_ADMITTED.md:9-18`).

Implementation: replace `role == "GREEN"` with the already-validated terminal decision condition. `admitted` is required only when a DEF-P012-02 row contains `MIN_NOTIONAL_ADMITTED`; a refused terminal decision therefore accepts absence and rejects `admitted` as an extra member (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:669-740`, `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:879-899`). No other harness rule changed.

GREEN, same test and command:

```text
.                                                                        [100%]
1 passed in 1.52s
```

The canonical receipt independently confirms the real modified copy reached the comparator: expected and measured checks are both `CORRECTED_EXPECTATION`, `/RESULT_SURFACE/admitted` changed, the first comparator difference is `/EVENT_SURFACE/cash_events`, and status is DETECTED (`W344_GATE_RECEIPT.json:514-528`).

## Complete contract suite

The exact scoped suite command required by prior harness lanes was run from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
7 failed, 306 passed in 6.67s
```

The seven failure names were:

```text
test_expected_source_provenance_refuses_expected_path_changed_after_base
test_w305_item3_recorded_exception_lifts_only_the_decision_134_path
test_w305_item3_wrong_current_oid_does_not_lift_the_refusal
test_w305_item3_wrong_base_state_does_not_lift_the_refusal
test_w305_item3_committed_record_states_it_is_not_evidence
test_w305_item8_provenance_refusal_reports_every_unlifted_path
test_probe_cannot_claim_target_membership_when_base_is_refused
```

These failures are not caused by the W344 harness edit: current gate evidence reports provenance `MATCH` with zero changed expected paths, while the stale tests still demand `EXPECTED_PATH_CHANGED_AFTER_BASE`; the committed record now includes W350 and the seal-16 base, while the test still pins the pre-W350 lane list and blob (`W344_GATE_RECEIPT.json:117-126`, `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:587-597`, `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:706-717`, `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/expected_provenance_exceptions.json:5-20`). The remaining 08-A test still asserts `funding_event_id`, while the current catalog/receipt value is `signed_delta` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1460-1493`, `W344_GATE_RECEIPT.json:632-647`). They were left unchanged to avoid unrelated test rewriting under the W344 correction fence.

## Frozen legacy replay

The W249 in-memory, no-baseline-write replay method cited by prior lanes was run against all 17 RED/GREEN rows and both surfaces. Output:

```text
SURFACES_EQUAL=34 MISMATCH=0
```

The canonical receipt corroborates `producer_id=KERNEL_1`, `scenario_count=17`, `status=MATCH`, and `surface_count=34` (`W344_GATE_RECEIPT.json:193-198`).

## Canonical gate - invoked once

Exactly one invocation was made from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`, using the required output path (`C:\tmp\LANE_PROMPTS_20260828\LANE_W344_HARNESS_02A_ADMITTED.md:22-23`):

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:/tmp/P012_BASELINE_RUN --output C:/WP012BUILD/W344_GATE_RECEIPT.json
```

Selected PROBE-P012-02-A receipt fields, quoted exactly (`W344_GATE_RECEIPT.json:514-528`):

```json
{
  "base_scenario_id": "RULE2-02-GREEN",
  "child_claim_label": "PROBE_BASE_SCENARIO_REFUSED",
  "child_returncode": 2,
  "comparator_first_differing_node": "/EVENT_SURFACE/cash_events",
  "digest_status": "PROBE_DIGEST_MATCH",
  "expected_failed_check": "CORRECTED_EXPECTATION",
  "expected_first_changed_node": "/RESULT_SURFACE/admitted",
  "expected_node_changed": true,
  "measured_failed_check": "CORRECTED_EXPECTATION",
  "measured_matches_expected": true,
  "probe_id": "PROBE-P012-02-A",
  "status": "DETECTED"
}
```

Final refusal list, quoted verbatim (`W344_GATE_RECEIPT.json:650-655`):

```json
[
  {
    "check_id": "SEMANTIC_COVERAGE_REVIEW_MISSING",
    "detail": "C:\\WP012BUILD\\MTC_COMMAND_CENTER\\01_MTC_PROJECT\\00_PYTHON\\mtc_v2\\tests\\corrected_vnext\\contracts\\semantic_coverage_review.json"
  }
]
```

The gate claim remains `BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_REFUSED` because that one owner-held review file is missing; acceptance remains reachable and there are no comparison blockers (`W344_GATE_RECEIPT.json:2-3`, `W344_GATE_RECEIPT.json:109-115`, `W344_GATE_RECEIPT.json:650-655`).

## Discrepancies

1. The lane asks to align the reverted W314B test to PROBE-P012-02-A and decision 143, but at required HEAD the named test had been changed to PROBE-P012-08-A by later W342B work; the lead ledger explicitly describes that 08-A reassignment (`C:\tmp\LANE_PROMPTS_20260828\LANE_W344_HARNESS_02A_ADMITTED.md:20-21`, `C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:2533-2536`). W344 restored the named regression to the owner-approved 02-A target, while leaving the separate 08-A regression in place (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1367-1454`, `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1457-1494`).
2. The lane predicts `313 passed`, but after later seal-16/re-anchor work the measured suite is `306 passed, 7 failed`; the exact failures and repository evidence are recorded in "Complete contract suite" above. The W344 target itself passes and the canonical gate proves all 10 probes DETECTED, so unrelated stale test assumptions were not silently rewritten (`C:\tmp\LANE_PROMPTS_20260828\LANE_W344_HARNESS_02A_ADMITTED.md:20-23`, `W344_GATE_RECEIPT.json:479-648`).

## Scope and handoff

The required one-commit message is:

```text
fix(mtc-v2): admit /RESULT_SURFACE/admitted only on admitted DEF-P012-02 per design 23.5 (decision Q-B, W344)
```

The next verification belongs to a family that did not write this correction (`C:\tmp\LANE_PROMPTS_20260828\LANE_W344_HARNESS_02A_ADMITTED.md:24-26`).
