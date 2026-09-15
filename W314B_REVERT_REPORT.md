# W314B Revert Report

**Verdict: PASS.** The one underived case-1 assertion hunk was restored to its `191637e2` state; the verifier accepted cases 2-5 and requested changes only for case 1 (`C:\tmp\LANE_PROMPTS_20260828\_packets_V314\V314_REPORT.md:29-58`, `C:\tmp\LANE_PROMPTS_20260828\_packets_V314\V314_REPORT.md:156-167`).

## Scope and authority

- Preflight measured branch `feature/wp-p0-12-corrected-vnext-20260831`, HEAD `59c81d116e43ec4c0f0192fa3b864a93e6fd9ab9`, and an empty short status before editing, matching the required gate (`C:\tmp\LANE_PROMPTS_20260828\LANE_W314B_REVERT_PROBE_CASE.md:3-5`).
- The lane authorizes restoration of case 1 from `191637e2` and forbids changes to cases 2-5 or any other content (`C:\tmp\LANE_PROMPTS_20260828\LANE_W314B_REVERT_PROBE_CASE.md:15-21`).
- The design states that comparator traversal order is an implementation fact it did not specify (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:491-493`). W314 therefore required a DESIGN-GAP stop rather than a guessed expected check or node (`C:\tmp\LANE_PROMPTS_20260828\LANE_W314_SELFTEST_F02.md:19-25`).

## Change

Case 1 now again expects `CLOSED_SET_VIOLATION` and `/RESULT_SURFACE/cumulative_funding` for the identity receipt (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1389-1395`). Its modified receipt assertions remain unchanged (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1410-1416`).

Cases 2-5 remain in their verifier-accepted W314 state: declared `DEF-P012-08` adds `cumulative_funding` to expected result membership, and both RULE2-08 cases require its zero value (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1900-1918`, `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:2060-2075`; `C:\tmp\LANE_PROMPTS_20260828\_packets_V314\V314_REPORT.md:62-92`).

Code commit: `0c44a4477287a197f47be8ddea748dfc1081edfb`.

## Required diff from `191637e2`

Measured with:

```text
git diff 191637e2 -- MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py
```

The output contains only the accepted cases 2-5 hunks required by the lane (`C:\tmp\LANE_PROMPTS_20260828\LANE_W314B_REVERT_PROBE_CASE.md:15-18`):

```diff
diff --git a/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py b/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py
index ddc872a7..b9fbaecc 100644
--- a/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py
+++ b/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py
@@ -1912,6 +1912,8 @@ def test_raw_kernel_result_membership_follows_declared_contract(
         expected.add("admitted")
     if row["owning_def_ids"][0] == "DEF-P012-07":
         expected.add("guards")
+    if "DEF-P012-08" in row["owning_def_ids"]:
+        expected.add("cumulative_funding")
     assert set(result) == expected
     assert result["metrics"] is None

@@ -2070,7 +2072,7 @@ def test_rule2_08_raw_kernel_is_not_seeded_from_legacy_state(
     assert result["run_manifest"]["cost_schedule_id"] == "NOT_CONSUMED"
     assert event["cash_events"] == []
     assert event["funding_events"] == []
-    assert "cumulative_funding" not in result
+    assert result["cumulative_funding"] == 0
```

## Pytest evidence

Command, run from `C:\WP012BUILD\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON` as prescribed (`C:\tmp\LANE_PROMPTS_20260828\LANE_W314B_REVERT_PROBE_CASE.md:18-21`):

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
```

Quoted failure names:

```text
FAILED mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_legacy_reproduction_refuses_one_ulp_actual
FAILED mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_receipt_accounts_for_every_blocked_expected_node
FAILED mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_probe_driver_refuses_unclosed_base_before_variant_comparison
```

The first two are the pipeline tests that call `run_comparison_pipeline` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1304-1325`, `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1334-1343`). The third is the deliberately restored open probe-driver case (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1364-1395`).

Quoted summary:

```text
3 failed, 308 passed in 5.61s
```

This is exactly the expected failure set and count (`C:\tmp\LANE_PROMPTS_20260828\LANE_W314B_REVERT_PROBE_CASE.md:18-21`).

## Discrepancies

None. Repository evidence agreed with the lane specification; this section is present as required by C-2 (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:9-13`).
