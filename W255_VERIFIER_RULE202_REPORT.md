# W255 Verifier RULE2-02 Projection Report

## Gate verdict

**BOUNDED_CORRECTION_EVIDENCE_REFUSED.** The canonical full-gate loop produced all 17 scenario rows with the expected RED/GREEN disposition and corrected-expectation MATCH, but the gate receipt remained non-accepting because 22 package refusals were present. The first refusal was SEMANTIC_COVERAGE_REVIEW_MISSING. This is the controlling stop required by the lane at C:\tmp\LANE_PROMPTS_20260828\LANE_W255_VERIFIER_RULE202_PROJECTION.md:47-51.

Finding count: **4** — three stale verifier-projection findings repaired (RULE2-02-RED, RULE2-06-RED, RULE2-06-EQUAL-PRICE-RED) and one canonical full-gate refusal remaining. The permitted edit scope and forbidden kernel/golden/catalog/manifest/baseline/seal surfaces are stated at C:\tmp\LANE_PROMPTS_20260828\LANE_W255_VERIFIER_RULE202_PROJECTION.md:4-9.

## Scope and identity

- Worktree: C:\WP012BUILD.
- Branch: feature/wp-p0-12-corrected-vnext-20260831, not master.
- Initial implementation parent: 2426bb83ca81f3058d426bbdc0bbdc6f54c9d9cc.
- Harness-fix commit: ff95304effab743d99324e5fd3bb418011c440c3.
- Report commit: SELF; its SHA cannot be embedded in its own bytes and is supplied in the chat close.
- No push, merge, pull request, live dependency, host, broker, venue, credential, deploy, backtest, optimization, server, launcher, artifact-generation, kernel, golden, catalog, manifest, baseline, or seal write was performed. The lane fence is C:\tmp\LANE_PROMPTS_20260828\LANE_W255_VERIFIER_RULE202_PROJECTION.md:4-9 and the shared execution fence is C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:25-36.

## Authority

Design quote:

> “Legacy opens; corrected emits REFUSED_MIN_NOTIONAL with observed notional 100 and required 101, and opens no position.”

Source: C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:246-250. The design's computability row names “the exact runtime-versus-record minimum-notional preflight,” not a fourth decision selector, at C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:567-571; the section-22 embedding repeats only the runtime 0 versus corrected 101 threshold at C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:849-862.

Sealed golden quote:

> “NO ROW ADDED under owner Reading Y. The minimum-notional predicate terminates in refusal on this row, so section 8's evaluation is already carried by REFUSED_MIN_NOTIONAL at sequence 2; MIN_NOTIONAL_ADMITTED would be the wrong terminal reason and adding both would be the row-count padding :1033-1034 forbids.”

Source: MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-02-RED.json:68-70. The artifact has exactly the three decision rows at the same file:21-24.

Owner ledger quote:

> “a decision_events row is required for every closed reason whose named decision is actually evaluated on that scenario” and “a reason is emitted because its named decision was evaluated, never to equalize row counts.”

Source: C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:494-505.

These sources agree. The design terminates the corrected path in REFUSED_MIN_NOTIONAL with no position; the golden records that the evaluated predicate is already represented by that terminal refusal; Reading Y admits only actually evaluated closed reasons and forbids padding. Therefore corrected decision_events[3].decision is absent by design, not a divergent node. Pairing it with legacy ABSENT made an equal ABSENT/ABSENT pair and was stale. This is exactly the conflict check required at C:\tmp\LANE_PROMPTS_20260828\LANE_W255_VERIFIER_RULE202_PROJECTION.md:22-37.

## Repair and exact diff

The RULE2-02-RED branch now contains exactly the refusal-code, fill-container, and final-position pairs plus the required authority comment at MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1186-1193. The exact-selector and all-unequal regression is at MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:709-739.

The class sweep exposed two demonstrably identical stale-selector cases. Design v1.9 makes COLLISION_RESOLVED the decision receipt at C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1029-1039 and closes RESULT_SURFACE without a collision member at the same file:1131-1156. The sealed RULE2-06-RED golden records removal of RESULT_SURFACE.collision at MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-06-RED.json:97-102; the equal-price golden records the same at MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-06-EQUAL-PRICE-RED.json:101-105. The worksheet explicitly marks the old result selectors superseded at MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/DERIVATIONS.md:622-640 and :680-690. The verifier therefore now selects decision_events[2].ordered_chosen_exit_ids and removes the obsolete is_pessimistic pair at MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1238-1249. No economic value or protected artifact was edited.

Committed diff (blank context lines normalized for Markdown):

~~~diff
commit ff95304effab743d99324e5fd3bb418011c440c3
Author:     Codex GPT-5 <codex@openai.com>
AuthorDate: Wed Sep 2 12:24:36 2026 +0300
Commit:     Codex GPT-5 <codex@openai.com>
CommitDate: Wed Sep 2 12:24:36 2026 +0300

    fix corrected-vnext RED projections
---
 .../contracts/selftests/test_verify_bceg.py        | 48 ++++++++++++++++++----
 .../mtc_v2/tests/corrected_vnext/verify_bceg.py    |  9 ++--
 2 files changed, 46 insertions(+), 11 deletions(-)

diff --git a/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py b/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py
index 0afa749c..37ebdf31 100644
--- a/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py
+++ b/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py
@@ -706,26 +706,60 @@ def test_rule2_08_null_cost_is_not_consumed_and_funding_is_projected(
     assert result["cumulative_funding"] == expected_cumulative


-def test_missing_decision_projection_resolves_absent() -> None:
+def test_rule2_02_red_projection_matches_design_and_all_pairs_diverge() -> None:
     scenario_id = "RULE2-02-RED"
-    selector = "/EVENT_SURFACE/decision_events/3/decision"
+    expected_selectors = [
+        "/RESULT_SURFACE/refusals/0/code",
+        "/EVENT_SURFACE/fill_events",
+        "/RESULT_SURFACE/final_position",
+    ]
     catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
     row = next(member for member in catalog if member["scenario_id"] == scenario_id)
     input_document = load_json_exact(MTC_V2_ROOT / row["input"]["path"])
     legacy = load_json_exact(
-        MTC_V2_ROOT / "tests/corrected_vnext/observed/1.0.0" / f"{scenario_id}.json"
+        Path(r"C:\tmp\P012_BASELINE_RUN")
+        / "out"
+        / scenario_id
+        / "result_surface.json"
+    )
+    corrected = load_json_exact(
+        MTC_V2_ROOT / row["expected_artifacts"]["2.0.0"]["path"]
     )
-    corrected = execute_corrected_scenario(MTC_V2_ROOT, row)

     projections = build_projection_results(
         scenario_id,
         input_document,
-        legacy["RESULT_SURFACE"],
+        legacy,
         corrected,
     )

-    selected = next(member for member in projections if member["selector"] == selector)
-    assert selected["corrected"] == {"tag": "ABSENT"}
+    assert [member["selector"] for member in projections] == expected_selectors
+    assert [member["equal"] for member in projections] == [False] * len(
+        expected_selectors
+    )
+
+
+def test_all_red_projection_pairs_resolve_on_sealed_goldens_and_diverge() -> None:
+    baseline_root = Path(r"C:\tmp\P012_BASELINE_RUN")
+    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
+
+    for row in catalog:
+        if row["role"] != "RED":
+            continue
+        scenario_id = row["scenario_id"]
+        projections = build_projection_results(
+            scenario_id,
+            load_json_exact(MTC_V2_ROOT / row["input"]["path"]),
+            load_json_exact(
+                baseline_root / "out" / scenario_id / "result_surface.json"
+            ),
+            load_json_exact(
+                MTC_V2_ROOT / row["expected_artifacts"]["2.0.0"]["path"]
+            ),
+        )
+
+        assert all(member["corrected"]["tag"] != "ABSENT" for member in projections)
+        assert all(not member["equal"] for member in projections)


 def test_all_cataloged_corrected_scenarios_are_executable() -> None:
diff --git a/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py b/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py
index e6d4cd34..5d4bebc3 100644
--- a/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py
+++ b/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py
@@ -1186,10 +1186,11 @@ def build_projection_results(
     elif scenario_id.startswith("RULE2-02-"):
         corrected_refusals = result["refusals"]
         if scenario_id.endswith("RED"):
+            # Design v1.8 line 248 declares refusal/no position; Reading Y
+            # (owner addendum 26) and the golden w172 note forbid a padded fourth decision row.
             pair("/RESULT_SURFACE/refusals/0/code", _absent(), _present(corrected_refusals[0]["code"]))
             pair("/EVENT_SURFACE/fill_events", _present([None] * len(legacy_events)), _present(event["fill_events"]))
             pair("/RESULT_SURFACE/final_position", _present({"side": "LONG", "quantity": 1}), _present(result["final_position"]))
-            pair("/EVENT_SURFACE/decision_events/3/decision", _absent(), _projection_value(event, "decision_events", 3, "decision"))
         else:
             pair("/RESULT_SURFACE/admitted", _present(position["present"]), _present(result["final_position"] is not None))
             pair("/EVENT_SURFACE/fill_events/0/quantity", _present(_decode_legacy_number(legacy_events[0]["qty"]), "I"), _present(event["fill_events"][0]["quantity"], "I"))
@@ -1242,9 +1243,9 @@ def build_projection_results(
             pair("/EVENT_SURFACE/fill_events/0/final_fill_price", _present(_decode_legacy_number(legacy_fill["price"]), "I"), _present(corrected_fills[0]["final_fill_price"], "I"))
             if len(corrected_fills) > 1:
                 pair("/EVENT_SURFACE/fill_events/1/final_fill_price", _absent(), _present(corrected_fills[1]["final_fill_price"], "I"))
-            pair("/RESULT_SURFACE/collision/ordered_chosen_exit_ids", _absent(), _present(result["collision"]["ordered_chosen_exit_ids"]))
-            if scenario_id == "RULE2-06-RED":
-                pair("/RESULT_SURFACE/collision/is_pessimistic", _present(True), _present(result["collision"]["is_pessimistic"]))
+            # Design v1.9 lines 1038 and 1133-1156 put the sole collision receipt
+            # on decision_events; both sealed v18 goldens record removal of RESULT collision.
+            pair("/EVENT_SURFACE/decision_events/2/ordered_chosen_exit_ids", _absent(), _projection_value(event, "decision_events", 2, "ordered_chosen_exit_ids"))
             pair("lifecycle gross realized PnL", _present(_decode_legacy_number(legacy_fill["realized_pnl"]), "I"), _present(corrected_gross, "I"))
     elif scenario_id.startswith("RULE2-07-"):
         legacy_equity = _decode_legacy_number(legacy_result["account"]["equity"])
~~~

## RED and GREEN evidence

### RULE2-02-RED exact selector regression — RED before verifier edit

Command:

~~~text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_rule2_02_red_projection_matches_design_and_all_pairs_diverge -q
~~~

Exit: 1.

~~~text
F                                                                        [100%]
================================== FAILURES ===================================
______ test_rule2_02_red_projection_matches_design_and_all_pairs_diverge ______

>       assert [member["selector"] for member in projections] == expected_selectors
E       AssertionError: assert ['/RESULT_SUR...s/3/decision'] == ['/RESULT_SUR...nal_position']
E
E         Left contains one more item: '/EVENT_SURFACE/decision_events/3/decision'
E         Use -v to get more diff

mtc_v2\tests\corrected_vnext\contracts\selftests\test_verify_bceg.py:736: AssertionError
=========================== short test summary info ===========================
FAILED mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_rule2_02_red_projection_matches_design_and_all_pairs_diverge
1 failed in 0.14s
~~~

The failure discriminates on the exact extra selector required by the lane; the durable assertion is at MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:709-739.

### RULE2-02-RED — GREEN after verifier edit

Command: same targeted pytest command.

Exit: 0.

~~~text
.                                                                        [100%]
1 passed in 0.08s
~~~

### All-RED class regression — RED before RULE2-06 repair

Command:

~~~text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_all_red_projection_pairs_resolve_on_sealed_goldens_and_diverge -q
~~~

Exit: 1.

~~~text
F                                                                        [100%]
================================== FAILURES ===================================
_____ test_all_red_projection_pairs_resolve_on_sealed_goldens_and_diverge _____

scenario_id = 'RULE2-06-RED'

>               pair("/RESULT_SURFACE/collision/ordered_chosen_exit_ids", _absent(), _present(result["collision"]["ordered_chosen_exit_ids"]))
E               KeyError: 'collision'

mtc_v2\tests\corrected_vnext\verify_bceg.py:1246: KeyError
=========================== short test summary info ===========================
FAILED mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_all_red_projection_pairs_resolve_on_sealed_goldens_and_diverge
1 failed in 0.17s
~~~

The retained class regression is at MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:742-762.

### Both regressions — GREEN after both repairs

Command:

~~~text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_rule2_02_red_projection_matches_design_and_all_pairs_diverge mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::test_all_red_projection_pairs_resolve_on_sealed_goldens_and_diverge -q
~~~

Exit: 0.

~~~text
..                                                                       [100%]
2 passed in 0.07s
~~~

## Nine-RED class sweep

The sweep loaded every RED catalog row's sealed 2.0.0 golden and C:\tmp\P012_BASELINE_RUN result, then called build_projection_results. The persistent version of that measurement is at MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:742-762.

| Scenario | Selector | Corrected tag | Equal |
|---|---|---|---|
| RULE2-01-RED | /EVENT_SURFACE/fill_events/0/quantity | PRESENT | false |
| RULE2-01-RED | /RESULT_SURFACE/final_position/quantity | PRESENT | false |
| RULE2-01-RED | /RESULT_SURFACE/order_notional | PRESENT | false |
| RULE2-02-RED | /RESULT_SURFACE/refusals/0/code | PRESENT | false |
| RULE2-02-RED | /EVENT_SURFACE/fill_events | PRESENT | false |
| RULE2-02-RED | /RESULT_SURFACE/final_position | PRESENT | false |
| RULE2-03-RED | /RESULT_SURFACE/refusals/0/code | PRESENT | false |
| RULE2-03-RED | /EVENT_SURFACE/decision_events/1/decision | PRESENT | false |
| RULE2-03-RED | /EVENT_SURFACE/fill_events | REFUSAL | false |
| RULE2-03-RED | consumed price_tick | REFUSAL | false |
| RULE2-04-RED | /EVENT_SURFACE/fill_events/0/reference_price | PRESENT | false |
| RULE2-04-RED | /EVENT_SURFACE/fill_events/0/final_fill_price | PRESENT | false |
| RULE2-04-RED | /EVENT_SURFACE/fill_events/0/fill_trigger | PRESENT | false |
| RULE2-05-RED | /EVENT_SURFACE/fill_events/0/reference_price | PRESENT | false |
| RULE2-05-RED | /EVENT_SURFACE/fill_events/0/slippage_impact | PRESENT | false |
| RULE2-05-RED | /EVENT_SURFACE/fill_events/0/final_fill_price | PRESENT | false |
| RULE2-05-RED | /EVENT_SURFACE/fill_events/0/slippage_application_count | PRESENT | false |
| RULE2-06-RED | /EVENT_SURFACE/fill_events/0/exit_id | PRESENT | false |
| RULE2-06-RED | /EVENT_SURFACE/fill_events | PRESENT | false |
| RULE2-06-RED | /EVENT_SURFACE/fill_events/0/final_fill_price | PRESENT | false |
| RULE2-06-RED | /EVENT_SURFACE/fill_events/1/final_fill_price | PRESENT | false |
| RULE2-06-RED | /EVENT_SURFACE/decision_events/2/ordered_chosen_exit_ids | PRESENT | false |
| RULE2-06-RED | lifecycle gross realized PnL | PRESENT | false |
| RULE2-06-EQUAL-PRICE-RED | /EVENT_SURFACE/fill_events/0/exit_id | PRESENT | false |
| RULE2-06-EQUAL-PRICE-RED | /EVENT_SURFACE/fill_events/1/exit_id | PRESENT | false |
| RULE2-06-EQUAL-PRICE-RED | /EVENT_SURFACE/fill_events | PRESENT | false |
| RULE2-06-EQUAL-PRICE-RED | /EVENT_SURFACE/fill_events/0/final_fill_price | PRESENT | false |
| RULE2-06-EQUAL-PRICE-RED | /EVENT_SURFACE/fill_events/1/final_fill_price | PRESENT | false |
| RULE2-06-EQUAL-PRICE-RED | /EVENT_SURFACE/decision_events/2/ordered_chosen_exit_ids | PRESENT | false |
| RULE2-06-EQUAL-PRICE-RED | lifecycle gross realized PnL | PRESENT | false |
| RULE2-07-RED | /EVENT_SURFACE/fee_events | PRESENT | false |
| RULE2-07-RED | /RESULT_SURFACE/trades/0/net_trade_pnl | PRESENT | false |
| RULE2-07-RED | /RESULT_SURFACE/guards/guard_pnl_basis | PRESENT | false |
| RULE2-07-RED | /RESULT_SURFACE/guards/last_closed_guard_pnl | PRESENT | false |
| RULE2-07-RED | /RESULT_SURFACE/guards/consecutive_loss_count | PRESENT | false |
| RULE2-07-RED | /RESULT_SURFACE/guards/guard_blocked_raw | PRESENT | false |
| RULE2-07-RED | /RESULT_SURFACE/equity_curve/last | PRESENT | false |
| RULE2-08-RED | /EVENT_SURFACE/funding_events | PRESENT | false |
| RULE2-08-RED | /EVENT_SURFACE/cash_events | PRESENT | false |
| RULE2-08-RED | /RESULT_SURFACE/cumulative_funding | PRESENT | false |
| RULE2-08-RED | /RESULT_SURFACE/equity_curve/last | PRESENT | false |

Measured summary: **9 RED scenarios, 41 pairs, 0 corrected ABSENT operands, 0 equal pairs**. Thus no stale corrected selector remains in the nine RED branches measured by this class fence.

## “18/18 expected check dispositions” receipt

The built-in run_selftests receipt does **not** pin the projection list. It records parser, schema, input-envelope, digest, and record-reference dispositions at MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1378-1429; build_projection_results is used by the comparison pipeline at the same file:1315-1362, not by run_selftests. No receipt fixture was changed.

Current built-in receipt count: **NOT VERIFIED** after the canonical refusal, because the lane says STOP at a repeated refusal before the later contract-self-test step (C:\tmp\LANE_PROMPTS_20260828\LANE_W255_VERIFIER_RULE202_PROJECTION.md:47-52). Current full pytest contract-suite count: **NOT VERIFIED** for the same reason. Measured targeted counts are the RED/GREEN counts above: 1 failed, 1 passed, 1 failed, then 2 passed.

## Canonical gate

Working directory:

~~~text
C:\WP012BUILD\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON
~~~

Exact command, run once:

~~~text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:\tmp\P012_BASELINE_RUN
~~~

The command completed the loop and printed the receipt below. The execution transport surfaced outer status 1 rather than the child status. The verifier-defined child exit for a non-accepting full-gate receipt is 2 at MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1473-1480; the separately surfaced OS child exit is **NOT VERIFIED** and is recorded under Discrepancies rather than silently equated with the transport status.

Full stdout:

~~~json
{
  "acceptance_blockers": [
    {
      "check_id": "LEGACY_EVENT_ORDER_MAP_PIN_MISSING",
      "detail": "no seal-pinned map/digest exists in the supplied bundle"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modified_copy",
      "scenario_id": "PROBE-P012-01-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modification_manifest",
      "scenario_id": "PROBE-P012-01-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modified_copy",
      "scenario_id": "PROBE-P012-01-B"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modification_manifest",
      "scenario_id": "PROBE-P012-01-B"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modified_copy",
      "scenario_id": "PROBE-P012-02-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modification_manifest",
      "scenario_id": "PROBE-P012-02-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modified_copy",
      "scenario_id": "PROBE-P012-03-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modification_manifest",
      "scenario_id": "PROBE-P012-03-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modified_copy",
      "scenario_id": "PROBE-P012-04-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modification_manifest",
      "scenario_id": "PROBE-P012-04-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modified_copy",
      "scenario_id": "PROBE-P012-05-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modification_manifest",
      "scenario_id": "PROBE-P012-05-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modified_copy",
      "scenario_id": "PROBE-P012-05-B"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modification_manifest",
      "scenario_id": "PROBE-P012-05-B"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modified_copy",
      "scenario_id": "PROBE-P012-06-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modification_manifest",
      "scenario_id": "PROBE-P012-06-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modified_copy",
      "scenario_id": "PROBE-P012-07-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modification_manifest",
      "scenario_id": "PROBE-P012-07-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modified_copy",
      "scenario_id": "PROBE-P012-08-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modification_manifest",
      "scenario_id": "PROBE-P012-08-A"
    }
  ],
  "acceptance_reachable": true,
  "catalog_counts": {
    "GREEN": 8,
    "PROBE": 10,
    "RED": 9
  },
  "claim_label": "BOUNDED_CORRECTION_EVIDENCE_REFUSED",
  "computed_legacy_event_order_map_digest": "0c8a04ddd671b1c9c5585b93369a1341d93bd50f01a4fa14dd8d74beab179862",
  "legacy_event_order_map": {
    "RULE2-01-GREEN/event_surface/0/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-01-GREEN/event_surface/1/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-01-GREEN/result_surface/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-01-RED/event_surface/0/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-01-RED/event_surface/1/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-01-RED/result_surface/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-02-GREEN/event_surface/0/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-02-GREEN/event_surface/1/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-02-GREEN/result_surface/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-02-RED/event_surface/0/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-02-RED/event_surface/1/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-02-RED/result_surface/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-03-GREEN/event_surface/0/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-03-GREEN/result_surface/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-03-RED/event_surface/0/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-03-RED/result_surface/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-04-GREEN/event_surface/0/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-04-GREEN/event_surface/1/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-04-GREEN/event_surface/2/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-04-GREEN/event_surface/3/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-04-GREEN/result_surface/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-04-RED/event_surface/0/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-04-RED/event_surface/1/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-04-RED/event_surface/2/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-04-RED/event_surface/3/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-04-RED/result_surface/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-05-GREEN/event_surface/0/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-05-GREEN/event_surface/1/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-05-GREEN/result_surface/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-05-RED/event_surface/0/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-05-RED/event_surface/1/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-05-RED/result_surface/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-06-EQUAL-PRICE-RED/event_surface/0/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-06-EQUAL-PRICE-RED/event_surface/1/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-06-EQUAL-PRICE-RED/event_surface/2/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-06-EQUAL-PRICE-RED/result_surface/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-06-GREEN/event_surface/0/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-06-GREEN/event_surface/1/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-06-GREEN/event_surface/2/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-06-GREEN/result_surface/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-06-RED/event_surface/0/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-06-RED/event_surface/1/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-06-RED/event_surface/2/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-06-RED/result_surface/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-07-GREEN/event_surface/0/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-07-GREEN/result_surface/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-07-RED/event_surface/0/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-07-RED/event_surface/1/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-07-RED/event_surface/2/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-07-RED/result_surface/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-08-GREEN/event_surface/0/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-08-GREEN/event_surface/1/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-08-GREEN/event_surface/2/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-08-GREEN/event_surface/3/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-08-GREEN/result_surface/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-08-RED/event_surface/0/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-08-RED/event_surface/1/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-08-RED/event_surface/2/events": "LEGACY_EVENT_ORDINAL_V1",
    "RULE2-08-RED/result_surface/events": "LEGACY_EVENT_ORDINAL_V1"
  },
  "mode": "full-gate",
  "refusals": [
    {
      "check_id": "SEMANTIC_COVERAGE_REVIEW_MISSING",
      "detail": "C:\\WP012BUILD\\MTC_COMMAND_CENTER\\01_MTC_PROJECT\\00_PYTHON\\mtc_v2\\tests\\corrected_vnext\\contracts\\semantic_coverage_review.json"
    },
    {
      "check_id": "LEGACY_EVENT_ORDER_MAP_PIN_MISSING",
      "detail": "no seal-pinned map/digest exists in the supplied bundle"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modified_copy",
      "scenario_id": "PROBE-P012-01-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modification_manifest",
      "scenario_id": "PROBE-P012-01-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modified_copy",
      "scenario_id": "PROBE-P012-01-B"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modification_manifest",
      "scenario_id": "PROBE-P012-01-B"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modified_copy",
      "scenario_id": "PROBE-P012-02-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modification_manifest",
      "scenario_id": "PROBE-P012-02-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modified_copy",
      "scenario_id": "PROBE-P012-03-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modification_manifest",
      "scenario_id": "PROBE-P012-03-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modified_copy",
      "scenario_id": "PROBE-P012-04-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modification_manifest",
      "scenario_id": "PROBE-P012-04-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modified_copy",
      "scenario_id": "PROBE-P012-05-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modification_manifest",
      "scenario_id": "PROBE-P012-05-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modified_copy",
      "scenario_id": "PROBE-P012-05-B"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modification_manifest",
      "scenario_id": "PROBE-P012-05-B"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modified_copy",
      "scenario_id": "PROBE-P012-06-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modification_manifest",
      "scenario_id": "PROBE-P012-06-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modified_copy",
      "scenario_id": "PROBE-P012-07-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modification_manifest",
      "scenario_id": "PROBE-P012-07-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modified_copy",
      "scenario_id": "PROBE-P012-08-A"
    },
    {
      "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
      "member": "modification_manifest",
      "scenario_id": "PROBE-P012-08-A"
    }
  ],
  "scenarios": [
    {
      "corrected_expectation": "MATCH",
      "first_changed_node": "/EVENT_SURFACE/fill_events/0/quantity",
      "first_corrected_mismatch": null,
      "projections": [
        {
          "corrected": {
            "canonical_value": "I:5",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "canonical_value": "I:10",
            "tag": "PRESENT"
          },
          "selector": "/EVENT_SURFACE/fill_events/0/quantity"
        },
        {
          "corrected": {
            "canonical_value": "I:5",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "canonical_value": "I:10",
            "tag": "PRESENT"
          },
          "selector": "/RESULT_SURFACE/final_position/quantity"
        },
        {
          "corrected": {
            "canonical_value": "I:1000",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "canonical_value": "I:2000",
            "tag": "PRESENT"
          },
          "selector": "/RESULT_SURFACE/order_notional"
        }
      ],
      "role": "RED",
      "scenario_id": "RULE2-01-RED",
      "status": "REFUSED_DECLARED_DIVERGENCE"
    },
    {
      "corrected_expectation": "MATCH",
      "first_changed_node": null,
      "first_corrected_mismatch": null,
      "projections": [
        {
          "corrected": {
            "canonical_value": "I:1",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "I:1",
            "tag": "PRESENT"
          },
          "selector": "/EVENT_SURFACE/fill_events/0/quantity"
        },
        {
          "corrected": {
            "canonical_value": "I:1",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "I:1",
            "tag": "PRESENT"
          },
          "selector": "/RESULT_SURFACE/final_position/quantity"
        },
        {
          "corrected": {
            "canonical_value": "I:100",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "I:100",
            "tag": "PRESENT"
          },
          "selector": "/RESULT_SURFACE/order_notional"
        }
      ],
      "role": "GREEN",
      "scenario_id": "RULE2-01-GREEN",
      "status": "GREEN_SHARED_PROJECTION_EQUAL"
    },
    {
      "corrected_expectation": "MATCH",
      "first_changed_node": "/RESULT_SURFACE/refusals/0/code",
      "first_corrected_mismatch": null,
      "projections": [
        {
          "corrected": {
            "canonical_value": "S:20:UkVGVVNFRF9NSU5fTk9USU9OQUw=",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "tag": "ABSENT"
          },
          "selector": "/RESULT_SURFACE/refusals/0/code"
        },
        {
          "corrected": {
            "canonical_value": "A:0",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "canonical_value": "A:1",
            "tag": "PRESENT"
          },
          "selector": "/EVENT_SURFACE/fill_events"
        },
        {
          "corrected": {
            "canonical_value": "N",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "canonical_value": "O:2",
            "tag": "PRESENT"
          },
          "selector": "/RESULT_SURFACE/final_position"
        }
      ],
      "role": "RED",
      "scenario_id": "RULE2-02-RED",
      "status": "REFUSED_DECLARED_DIVERGENCE"
    },
    {
      "corrected_expectation": "MATCH",
      "first_changed_node": null,
      "first_corrected_mismatch": null,
      "projections": [
        {
          "corrected": {
            "canonical_value": "B:1",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "B:1",
            "tag": "PRESENT"
          },
          "selector": "/RESULT_SURFACE/admitted"
        },
        {
          "corrected": {
            "canonical_value": "I:1",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "I:1",
            "tag": "PRESENT"
          },
          "selector": "/EVENT_SURFACE/fill_events/0/quantity"
        },
        {
          "corrected": {
            "canonical_value": "I:1",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "I:1",
            "tag": "PRESENT"
          },
          "selector": "/RESULT_SURFACE/final_position/quantity"
        }
      ],
      "role": "GREEN",
      "scenario_id": "RULE2-02-GREEN",
      "status": "GREEN_SHARED_PROJECTION_EQUAL"
    },
    {
      "corrected_expectation": "MATCH",
      "first_changed_node": "/RESULT_SURFACE/refusals/0/code",
      "first_corrected_mismatch": null,
      "projections": [
        {
          "corrected": {
            "canonical_value": "S:41:UkVGVVNFRF9JTlNUUlVNRU5UX09WRVJSSURFX09OX0VWQUxVQVRJT04=",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "tag": "ABSENT"
          },
          "selector": "/RESULT_SURFACE/refusals/0/code"
        },
        {
          "corrected": {
            "canonical_value": "S:41:UkVGVVNFRF9JTlNUUlVNRU5UX09WRVJSSURFX09OX0VWQUxVQVRJT04=",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "tag": "ABSENT"
          },
          "selector": "/EVENT_SURFACE/decision_events/1/decision"
        },
        {
          "corrected": {
            "refusal_code": "REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION",
            "tag": "REFUSAL"
          },
          "equal": false,
          "legacy": {
            "canonical_value": "A:0",
            "tag": "PRESENT"
          },
          "selector": "/EVENT_SURFACE/fill_events"
        },
        {
          "corrected": {
            "refusal_code": "REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION",
            "tag": "REFUSAL"
          },
          "equal": false,
          "legacy": {
            "canonical_value": "F:0x1.0000000000000p-2",
            "tag": "PRESENT"
          },
          "selector": "consumed price_tick"
        }
      ],
      "role": "RED",
      "scenario_id": "RULE2-03-RED",
      "status": "REFUSED_DECLARED_DIVERGENCE"
    },
    {
      "corrected_expectation": "MATCH",
      "first_changed_node": null,
      "first_corrected_mismatch": null,
      "projections": [
        {
          "corrected": {
            "canonical_value": "A:0",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "A:0",
            "tag": "PRESENT"
          },
          "selector": "/RESULT_SURFACE/refusals"
        },
        {
          "corrected": {
            "canonical_value": "F:0x1.0000000000000p-1",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "F:0x1.0000000000000p-1",
            "tag": "PRESENT"
          },
          "selector": "consumed price_tick"
        },
        {
          "corrected": {
            "canonical_value": "N",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "N",
            "tag": "PRESENT"
          },
          "selector": "/RESULT_SURFACE/final_position"
        }
      ],
      "role": "GREEN",
      "scenario_id": "RULE2-03-GREEN",
      "status": "GREEN_SHARED_PROJECTION_EQUAL"
    },
    {
      "corrected_expectation": "MATCH",
      "first_changed_node": "/EVENT_SURFACE/fill_events/0/reference_price",
      "first_corrected_mismatch": null,
      "projections": [
        {
          "corrected": {
            "canonical_value": "I:90",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "canonical_value": "I:92",
            "tag": "PRESENT"
          },
          "selector": "/EVENT_SURFACE/fill_events/0/reference_price"
        },
        {
          "corrected": {
            "canonical_value": "I:90",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "canonical_value": "I:92",
            "tag": "PRESENT"
          },
          "selector": "/EVENT_SURFACE/fill_events/0/final_fill_price"
        },
        {
          "corrected": {
            "canonical_value": "S:8:R0FQX09QRU4=",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "tag": "ABSENT"
          },
          "selector": "/EVENT_SURFACE/fill_events/0/fill_trigger"
        }
      ],
      "role": "RED",
      "scenario_id": "RULE2-04-RED",
      "status": "REFUSED_DECLARED_DIVERGENCE"
    },
    {
      "corrected_expectation": "MATCH",
      "first_changed_node": null,
      "first_corrected_mismatch": null,
      "projections": [
        {
          "corrected": {
            "canonical_value": "A:0",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "A:0",
            "tag": "PRESENT"
          },
          "selector": "/EVENT_SURFACE/exit_events"
        },
        {
          "corrected": {
            "canonical_value": "A:0",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "A:0",
            "tag": "PRESENT"
          },
          "selector": "/EVENT_SURFACE/fill_events"
        },
        {
          "corrected": {
            "canonical_value": "I:1",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "I:1",
            "tag": "PRESENT"
          },
          "selector": "/RESULT_SURFACE/final_position/quantity"
        }
      ],
      "role": "GREEN",
      "scenario_id": "RULE2-04-GREEN",
      "status": "GREEN_SHARED_PROJECTION_EQUAL"
    },
    {
      "corrected_expectation": "MATCH",
      "first_changed_node": "/EVENT_SURFACE/fill_events/0/reference_price",
      "first_corrected_mismatch": null,
      "projections": [
        {
          "corrected": {
            "canonical_value": "I:100",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "tag": "ABSENT"
          },
          "selector": "/EVENT_SURFACE/fill_events/0/reference_price"
        },
        {
          "corrected": {
            "canonical_value": "I:1",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "tag": "ABSENT"
          },
          "selector": "/EVENT_SURFACE/fill_events/0/slippage_impact"
        },
        {
          "corrected": {
            "canonical_value": "I:101",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "canonical_value": "I:100",
            "tag": "PRESENT"
          },
          "selector": "/EVENT_SURFACE/fill_events/0/final_fill_price"
        },
        {
          "corrected": {
            "canonical_value": "I:1",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "tag": "ABSENT"
          },
          "selector": "/EVENT_SURFACE/fill_events/0/slippage_application_count"
        }
      ],
      "role": "RED",
      "scenario_id": "RULE2-05-RED",
      "status": "REFUSED_DECLARED_DIVERGENCE"
    },
    {
      "corrected_expectation": "MATCH",
      "first_changed_node": null,
      "first_corrected_mismatch": null,
      "projections": [
        {
          "corrected": {
            "canonical_value": "I:100",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "I:100",
            "tag": "PRESENT"
          },
          "selector": "/EVENT_SURFACE/fill_events/0/final_fill_price"
        }
      ],
      "role": "GREEN",
      "scenario_id": "RULE2-05-GREEN",
      "status": "GREEN_SHARED_PROJECTION_EQUAL"
    },
    {
      "corrected_expectation": "MATCH",
      "first_changed_node": "/EVENT_SURFACE/fill_events/0/exit_id",
      "first_corrected_mismatch": null,
      "projections": [
        {
          "corrected": {
            "canonical_value": "S:11:VEFSR0VULU5FQVI=",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "canonical_value": "S:4:U1RPUA==",
            "tag": "PRESENT"
          },
          "selector": "/EVENT_SURFACE/fill_events/0/exit_id"
        },
        {
          "corrected": {
            "canonical_value": "A:2",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "canonical_value": "A:1",
            "tag": "PRESENT"
          },
          "selector": "/EVENT_SURFACE/fill_events"
        },
        {
          "corrected": {
            "canonical_value": "I:105",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "canonical_value": "I:90",
            "tag": "PRESENT"
          },
          "selector": "/EVENT_SURFACE/fill_events/0/final_fill_price"
        },
        {
          "corrected": {
            "canonical_value": "I:110",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "tag": "ABSENT"
          },
          "selector": "/EVENT_SURFACE/fill_events/1/final_fill_price"
        },
        {
          "corrected": {
            "canonical_value": "A:2",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "tag": "ABSENT"
          },
          "selector": "/EVENT_SURFACE/decision_events/2/ordered_chosen_exit_ids"
        },
        {
          "corrected": {
            "canonical_value": "I:15",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "canonical_value": "I:-20",
            "tag": "PRESENT"
          },
          "selector": "lifecycle gross realized PnL"
        }
      ],
      "role": "RED",
      "scenario_id": "RULE2-06-RED",
      "status": "REFUSED_DECLARED_DIVERGENCE"
    },
    {
      "corrected_expectation": "MATCH",
      "first_changed_node": "/EVENT_SURFACE/fill_events/0/exit_id",
      "first_corrected_mismatch": null,
      "projections": [
        {
          "corrected": {
            "canonical_value": "S:10:VEFSR0VULUZBUg==",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "canonical_value": "S:4:U1RPUA==",
            "tag": "PRESENT"
          },
          "selector": "/EVENT_SURFACE/fill_events/0/exit_id"
        },
        {
          "corrected": {
            "canonical_value": "S:11:VEFSR0VULU5FQVI=",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "tag": "ABSENT"
          },
          "selector": "/EVENT_SURFACE/fill_events/1/exit_id"
        },
        {
          "corrected": {
            "canonical_value": "A:2",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "canonical_value": "A:1",
            "tag": "PRESENT"
          },
          "selector": "/EVENT_SURFACE/fill_events"
        },
        {
          "corrected": {
            "canonical_value": "I:105",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "canonical_value": "I:90",
            "tag": "PRESENT"
          },
          "selector": "/EVENT_SURFACE/fill_events/0/final_fill_price"
        },
        {
          "corrected": {
            "canonical_value": "I:105",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "tag": "ABSENT"
          },
          "selector": "/EVENT_SURFACE/fill_events/1/final_fill_price"
        },
        {
          "corrected": {
            "canonical_value": "A:2",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "tag": "ABSENT"
          },
          "selector": "/EVENT_SURFACE/decision_events/2/ordered_chosen_exit_ids"
        },
        {
          "corrected": {
            "canonical_value": "I:10",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "canonical_value": "I:-20",
            "tag": "PRESENT"
          },
          "selector": "lifecycle gross realized PnL"
        }
      ],
      "role": "RED",
      "scenario_id": "RULE2-06-EQUAL-PRICE-RED",
      "status": "REFUSED_DECLARED_DIVERGENCE"
    },
    {
      "corrected_expectation": "MATCH",
      "first_changed_node": null,
      "first_corrected_mismatch": null,
      "projections": [
        {
          "corrected": {
            "canonical_value": "S:4:U1RPUA==",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "S:4:U1RPUA==",
            "tag": "PRESENT"
          },
          "selector": "/EVENT_SURFACE/fill_events/0/exit_id"
        },
        {
          "corrected": {
            "canonical_value": "I:2",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "I:2",
            "tag": "PRESENT"
          },
          "selector": "/EVENT_SURFACE/fill_events/0/quantity"
        },
        {
          "corrected": {
            "canonical_value": "I:90",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "I:90",
            "tag": "PRESENT"
          },
          "selector": "/EVENT_SURFACE/fill_events/0/final_fill_price"
        },
        {
          "corrected": {
            "canonical_value": "I:-20",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "I:-20",
            "tag": "PRESENT"
          },
          "selector": "lifecycle gross realized PnL"
        }
      ],
      "role": "GREEN",
      "scenario_id": "RULE2-06-GREEN",
      "status": "GREEN_SHARED_PROJECTION_EQUAL"
    },
    {
      "corrected_expectation": "MATCH",
      "first_changed_node": "/EVENT_SURFACE/fee_events",
      "first_corrected_mismatch": null,
      "projections": [
        {
          "corrected": {
            "canonical_value": "A:2",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "tag": "ABSENT"
          },
          "selector": "/EVENT_SURFACE/fee_events"
        },
        {
          "corrected": {
            "canonical_value": "F:-0x1.999999999999ap-3",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "tag": "ABSENT"
          },
          "selector": "/RESULT_SURFACE/trades/0/net_trade_pnl"
        },
        {
          "corrected": {
            "canonical_value": "S:16:R1JPU1MtTUlOVVMtRkVFUw==",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "tag": "ABSENT"
          },
          "selector": "/RESULT_SURFACE/guards/guard_pnl_basis"
        },
        {
          "corrected": {
            "canonical_value": "F:-0x1.999999999999ap-3",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "tag": "ABSENT"
          },
          "selector": "/RESULT_SURFACE/guards/last_closed_guard_pnl"
        },
        {
          "corrected": {
            "canonical_value": "I:1",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "canonical_value": "I:0",
            "tag": "PRESENT"
          },
          "selector": "/RESULT_SURFACE/guards/consecutive_loss_count"
        },
        {
          "corrected": {
            "canonical_value": "B:1",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "canonical_value": "B:0",
            "tag": "PRESENT"
          },
          "selector": "/RESULT_SURFACE/guards/guard_blocked_raw"
        },
        {
          "corrected": {
            "canonical_value": "F:0x1.f3e6666666666p+9",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "canonical_value": "I:1000",
            "tag": "PRESENT"
          },
          "selector": "/RESULT_SURFACE/equity_curve/last"
        }
      ],
      "role": "RED",
      "scenario_id": "RULE2-07-RED",
      "status": "REFUSED_DECLARED_DIVERGENCE"
    },
    {
      "corrected_expectation": "MATCH",
      "first_changed_node": null,
      "first_corrected_mismatch": null,
      "projections": [
        {
          "corrected": {
            "canonical_value": "I:1000",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "I:1000",
            "tag": "PRESENT"
          },
          "selector": "/RESULT_SURFACE/equity_curve/last"
        },
        {
          "corrected": {
            "canonical_value": "I:0",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "I:0",
            "tag": "PRESENT"
          },
          "selector": "/RESULT_SURFACE/guards/consecutive_loss_count"
        },
        {
          "corrected": {
            "canonical_value": "A:0",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "A:0",
            "tag": "PRESENT"
          },
          "selector": "/EVENT_SURFACE/fill_events"
        },
        {
          "corrected": {
            "canonical_value": "N",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "N",
            "tag": "PRESENT"
          },
          "selector": "/RESULT_SURFACE/final_position"
        }
      ],
      "role": "GREEN",
      "scenario_id": "RULE2-07-GREEN",
      "status": "GREEN_SHARED_PROJECTION_EQUAL"
    },
    {
      "corrected_expectation": "MATCH",
      "first_changed_node": "/EVENT_SURFACE/funding_events",
      "first_corrected_mismatch": null,
      "projections": [
        {
          "corrected": {
            "canonical_value": "A:1",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "tag": "ABSENT"
          },
          "selector": "/EVENT_SURFACE/funding_events"
        },
        {
          "corrected": {
            "canonical_value": "A:1",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "tag": "ABSENT"
          },
          "selector": "/EVENT_SURFACE/cash_events"
        },
        {
          "corrected": {
            "canonical_value": "F:-0x1.999999999999ap-4",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "tag": "ABSENT"
          },
          "selector": "/RESULT_SURFACE/cumulative_funding"
        },
        {
          "corrected": {
            "canonical_value": "F:0x1.f3f3333333333p+9",
            "tag": "PRESENT"
          },
          "equal": false,
          "legacy": {
            "canonical_value": "I:1000",
            "tag": "PRESENT"
          },
          "selector": "/RESULT_SURFACE/equity_curve/last"
        }
      ],
      "role": "RED",
      "scenario_id": "RULE2-08-RED",
      "status": "REFUSED_DECLARED_DIVERGENCE"
    },
    {
      "corrected_expectation": "MATCH",
      "first_changed_node": null,
      "first_corrected_mismatch": null,
      "projections": [
        {
          "corrected": {
            "canonical_value": "I:1000",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "I:1000",
            "tag": "PRESENT"
          },
          "selector": "/RESULT_SURFACE/equity_curve/last"
        },
        {
          "corrected": {
            "canonical_value": "A:0",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "A:0",
            "tag": "PRESENT"
          },
          "selector": "/EVENT_SURFACE/fill_events"
        },
        {
          "corrected": {
            "canonical_value": "N",
            "tag": "PRESENT"
          },
          "equal": true,
          "legacy": {
            "canonical_value": "N",
            "tag": "PRESENT"
          },
          "selector": "/RESULT_SURFACE/final_position"
        }
      ],
      "role": "GREEN",
      "scenario_id": "RULE2-08-GREEN",
      "status": "GREEN_SHARED_PROJECTION_EQUAL"
    }
  ],
  "sealed_producer_identities": {
    "baseline_driver_sha256": "b7648f71cc089d683f54fe9a82c7dc95302bc2cb3481288c2c99313944f56d53",
    "catalog_sha256": "f8e788d808f26c427eaefdd3f521998b0fdcea57a469792792abab260efea603",
    "expected_seal_sha256": "4ebcdfc5ad42e5f209f6cda6f3c5ef5b39dde510bf8b0ffaf3555d692ae23461",
    "implementation_anchor_sha256": "343aa91b2bcd5f3087f3d4170f330047ab72c6992f38f253e1376904b0859ce8"
  }
}
~~~

### Seventeen-row table

| Scenario | Role | Gate status | Corrected expectation | First changed node |
|---|---|---|---|---|
| RULE2-01-RED | RED | REFUSED_DECLARED_DIVERGENCE | MATCH | /EVENT_SURFACE/fill_events/0/quantity |
| RULE2-01-GREEN | GREEN | GREEN_SHARED_PROJECTION_EQUAL | MATCH | null |
| RULE2-02-RED | RED | REFUSED_DECLARED_DIVERGENCE | MATCH | /RESULT_SURFACE/refusals/0/code |
| RULE2-02-GREEN | GREEN | GREEN_SHARED_PROJECTION_EQUAL | MATCH | null |
| RULE2-03-RED | RED | REFUSED_DECLARED_DIVERGENCE | MATCH | /RESULT_SURFACE/refusals/0/code |
| RULE2-03-GREEN | GREEN | GREEN_SHARED_PROJECTION_EQUAL | MATCH | null |
| RULE2-04-RED | RED | REFUSED_DECLARED_DIVERGENCE | MATCH | /EVENT_SURFACE/fill_events/0/reference_price |
| RULE2-04-GREEN | GREEN | GREEN_SHARED_PROJECTION_EQUAL | MATCH | null |
| RULE2-05-RED | RED | REFUSED_DECLARED_DIVERGENCE | MATCH | /EVENT_SURFACE/fill_events/0/reference_price |
| RULE2-05-GREEN | GREEN | GREEN_SHARED_PROJECTION_EQUAL | MATCH | null |
| RULE2-06-RED | RED | REFUSED_DECLARED_DIVERGENCE | MATCH | /EVENT_SURFACE/fill_events/0/exit_id |
| RULE2-06-EQUAL-PRICE-RED | RED | REFUSED_DECLARED_DIVERGENCE | MATCH | /EVENT_SURFACE/fill_events/0/exit_id |
| RULE2-06-GREEN | GREEN | GREEN_SHARED_PROJECTION_EQUAL | MATCH | null |
| RULE2-07-RED | RED | REFUSED_DECLARED_DIVERGENCE | MATCH | /EVENT_SURFACE/fee_events |
| RULE2-07-GREEN | GREEN | GREEN_SHARED_PROJECTION_EQUAL | MATCH | null |
| RULE2-08-RED | RED | REFUSED_DECLARED_DIVERGENCE | MATCH | /EVENT_SURFACE/funding_events |
| RULE2-08-GREEN | GREEN | GREEN_SHARED_PROJECTION_EQUAL | MATCH | null |

Measured scenario summary: **17/17 expected dispositions** — nine RED rows REFUSED_DECLARED_DIVERGENCE, eight GREEN rows GREEN_SHARED_PROJECTION_EQUAL, and all 17 corrected expectations MATCH. This is the scenario-loop prediction in C:\tmp\LANE_PROMPTS_20260828\LANE_W255_VERIFIER_RULE202_PROJECTION.md:49-51; it does not override the gate's own refused claim.

### Gate summary object

- claim_label: BOUNDED_CORRECTION_EVIDENCE_REFUSED.
- acceptance_reachable: true.
- catalog_counts: RED 9, GREEN 8, PROBE 10.
- acceptance_blockers: 21.
- refusals: 22 — SEMANTIC_COVERAGE_REVIEW_MISSING, LEGACY_EVENT_ORDER_MAP_PIN_MISSING, and two PROBE_ARTIFACT_NOT_MATERIALIZED rows for each of ten probes.
- computed_legacy_event_order_map_digest: 0c8a04ddd671b1c9c5585b93369a1341d93bd50f01a4fa14dd8d74beab179862.
- sealed identities: baseline driver b7648f71cc089d683f54fe9a82c7dc95302bc2cb3481288c2c99313944f56d53; catalog f8e788d808f26c427eaefdd3f521998b0fdcea57a469792792abab260efea603; expected seal 4ebcdfc5ad42e5f209f6cda6f3c5ef5b39dde510bf8b0ffaf3555d692ae23461; implementation anchor 343aa91b2bcd5f3087f3d4170f330047ab72c6992f38f253e1376904b0859ce8.

All values above are present in the full stdout object in this section. No flag was used and no second gate run was made, as required at C:\tmp\LANE_PROMPTS_20260828\LANE_W255_VERIFIER_RULE202_PROJECTION.md:47-51.

## Discrepancies

1. **The repository exposed two additional same-class stale projection branches.** The prompt anticipated RULE2-02-RED and allowed another repair only if demonstrably the same defect (C:\tmp\LANE_PROMPTS_20260828\LANE_W255_VERIFIER_RULE202_PROJECTION.md:43-46). RULE2-06-RED and RULE2-06-EQUAL-PRICE-RED still selected a removed RESULT_SURFACE.collision object, while the current design and goldens put the receipt on decision_events. The supersession is explicit at MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/DERIVATIONS.md:622-640 and :680-690, so both were repaired under the prompt's stated exception.
2. **The 17/17 prediction held only for scenario dispositions, not for the full-gate claim.** All 17 scenario rows matched, but 22 package refusals kept claim_label BOUNDED_CORRECTION_EVIDENCE_REFUSED. The prompt labels 17/17 a prediction rather than a target at C:\tmp\LANE_PROMPTS_20260828\LANE_W255_VERIFIER_RULE202_PROJECTION.md:49-51.
3. **The repeated-refusal STOP conflicts with the later unconditional-looking self-test request.** The prompt says STOP at a repeated refusal at line 49, then asks for contract self-tests and counts at line 52. The STOP controlled; complete-suite counts are NOT VERIFIED, while the already-executed targeted regression counts are reported.
4. **The execution transport did not surface the child exit code separately.** It presented outer status 1 after the complete stdout receipt. Source control flow establishes that this non-accepting full-gate branch returns 2 at MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1473-1480, but a separately measured OS child code is NOT VERIFIED because the STOP clause forbids rerunning the gate.
5. **The built-in 18-check receipt does not pin projections.** Static inspection shows run_selftests ends without calling build_projection_results at MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1378-1429. The projection list is instead pinned by the pytest contract at MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:709-762.
6. **The report cannot contain its own final commit SHA without changing that SHA.** The implementation commit is recorded above; the report commit SHA is supplied in chat after the separate report commit required at C:\tmp\LANE_PROMPTS_20260828\LANE_W255_VERIFIER_RULE202_PROJECTION.md:52-59.
7. **The checked ownership mirror has no W255 row.** SESSION_LOCK says unlisted workstreams add a row before writing at MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOCK.md:52-58, while the lane grants exclusive worktree ownership and forbids unnamed-path edits at C:\tmp\LANE_PROMPTS_20260828\LANE_W255_VERIFIER_RULE202_PROJECTION.md:4-9. The external lane assignment controlled; SESSION_LOCK was not edited because it is outside the lane's exact write scope.

## Commit handoff

- Harness fix plus tests: ff95304effab743d99324e5fd3bb418011c440c3.
- Report: SELF; final SHA in chat.
- Staged paths were explicit; no git add dot or add-all was used, consistent with C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:25-31.
- No push, merge, pull request, or protected-artifact write was performed.
