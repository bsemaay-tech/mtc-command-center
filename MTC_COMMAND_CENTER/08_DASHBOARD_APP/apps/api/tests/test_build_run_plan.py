from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MCC_ROOT = Path(__file__).resolve().parents[4]
TOOLS_ROOT = MCC_ROOT / "03_QUANTLENS" / "tools"
MODULE_PATH = TOOLS_ROOT / "build_run_plan.py"
SCHEMA_DIR = MCC_ROOT / "06_SCHEMAS"

SPEC = importlib.util.spec_from_file_location("build_run_plan", MODULE_PATH)
assert SPEC and SPEC.loader
brp = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(brp)

from mcc_readonly.schema import validate_json_schema  # noqa: E402


def _schema(name: str) -> dict:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


class BuildRunPlanTests(unittest.TestCase):
    def _plan(self) -> dict:
        return brp.build_run_plan(
            "QL_TEST_STRATEGY",
            {"strategy_display_name": "Test Strat", "source_url": "https://example.com"},
            list(brp.OFFICIAL_PROFILES),
            ["BTCUSDT"],
            ["4h"],
            5000,
            "draft_run_plan_test",
        )

    def test_run_plan_is_schema_valid(self) -> None:
        issues = validate_json_schema(self._plan(), _schema("run_plan.schema.json"))
        self.assertEqual(issues, [])

    def test_run_plan_is_review_only(self) -> None:
        plan = self._plan()
        self.assertEqual(plan["status"], "draft_pending_approval")
        self.assertTrue(plan["read_only"])
        self.assertTrue(plan["no_execution"])
        self.assertFalse(plan["approval"]["approved"])
        self.assertFalse(plan["approval"]["execution_allowed"])
        self.assertTrue(plan["approval"]["human_review_required"])

    def test_profiles_constrained_and_no_fake_kpis(self) -> None:
        plan = self._plan()
        for p in plan["profiles"]:
            self.assertIn(p, brp.OFFICIAL_PROFILES)
        # parameter space must not fabricate numeric sweeps for undefined rules.
        for spec in plan["parameter_space"]["params"].values():
            if spec["state"] == "needs_freeze":
                self.assertEqual(spec["values"], [])

    def test_artifact_index_is_schema_valid(self) -> None:
        idx = brp.build_artifact_index("draft_run_plan_test", Path("/nonexistent"))
        issues = validate_json_schema(idx, _schema("artifact_index.schema.json"))
        self.assertEqual(issues, [])
        self.assertEqual(idx["run_id"], "draft_run_plan_test")
        types = {a["type"] for a in idx["artifacts"]}
        self.assertIn("run_plan", types)
        self.assertIn("artifact_index", types)

    def test_dry_run_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            old_root = brp.BACKTEST_ROOT
            try:
                brp.BACKTEST_ROOT = Path(t) / "05_BACKTEST_RESULTS"
                rc = brp.main(["--strategy-id", "QL_TEST_STRATEGY", "--dry-run", "--apply",
                               "--run-id", "draft_run_plan_unittest_dryrun"])
                self.assertEqual(rc, 0)
                self.assertFalse((brp.BACKTEST_ROOT / "draft_run_plan_unittest_dryrun").exists())
            finally:
                brp.BACKTEST_ROOT = old_root

    def test_default_without_apply_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            old_root = brp.BACKTEST_ROOT
            try:
                brp.BACKTEST_ROOT = Path(t) / "05_BACKTEST_RESULTS"
                rc = brp.main(["--strategy-id", "QL_TEST_STRATEGY",
                               "--run-id", "draft_run_plan_unittest_default"])
                self.assertEqual(rc, 0)
                self.assertFalse((brp.BACKTEST_ROOT / "draft_run_plan_unittest_default").exists())
            finally:
                brp.BACKTEST_ROOT = old_root

    def test_apply_writes_inside_backtest_results(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            old_root = brp.BACKTEST_ROOT
            try:
                brp.BACKTEST_ROOT = Path(t) / "05_BACKTEST_RESULTS"
                rc = brp.main(["--strategy-id", "QL_TEST_STRATEGY",
                               "--run-id", "draft_run_plan_unittest_apply", "--apply"])
                self.assertEqual(rc, 0)
                run_dir = brp.BACKTEST_ROOT / "draft_run_plan_unittest_apply"
                self.assertTrue((run_dir / "run_plan.json").exists())
                self.assertTrue((run_dir / "artifact_index.json").exists())
                self.assertTrue((run_dir / "run_plan.md").exists())
            finally:
                brp.BACKTEST_ROOT = old_root

    def test_refuses_existing_outputs_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            old_root = brp.BACKTEST_ROOT
            try:
                brp.BACKTEST_ROOT = Path(t) / "05_BACKTEST_RESULTS"
                run_dir = brp.BACKTEST_ROOT / "draft_run_plan_unittest_existing"
                run_dir.mkdir(parents=True)
                target = run_dir / "run_plan.json"
                target.write_text("KEEP", encoding="utf-8")
                rc = brp.main(["--strategy-id", "QL_TEST_STRATEGY",
                               "--run-id", "draft_run_plan_unittest_existing", "--apply"])
                self.assertEqual(rc, 5)
                self.assertEqual(target.read_text(encoding="utf-8"), "KEEP")
            finally:
                brp.BACKTEST_ROOT = old_root

    def test_force_allows_existing_outputs_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            old_root = brp.BACKTEST_ROOT
            try:
                brp.BACKTEST_ROOT = Path(t) / "05_BACKTEST_RESULTS"
                run_dir = brp.BACKTEST_ROOT / "draft_run_plan_unittest_force"
                run_dir.mkdir(parents=True)
                target = run_dir / "run_plan.json"
                target.write_text("OLD", encoding="utf-8")
                rc = brp.main(["--strategy-id", "QL_TEST_STRATEGY",
                               "--run-id", "draft_run_plan_unittest_force", "--apply", "--force"])
                self.assertEqual(rc, 0)
                self.assertNotEqual(target.read_text(encoding="utf-8"), "OLD")
            finally:
                brp.BACKTEST_ROOT = old_root

    def test_refuses_output_root_outside_backtest_results(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            old_root = brp.BACKTEST_ROOT
            try:
                tmp = Path(t)
                brp.BACKTEST_ROOT = tmp / "05_BACKTEST_RESULTS"
                outside = tmp / "outside"
                rc = brp.main(["--strategy-id", "QL_TEST_STRATEGY",
                               "--run-id", "draft_run_plan_unittest_outside",
                               "--output-root", str(outside), "--apply"])
                self.assertEqual(rc, 5)
                self.assertFalse((outside / "draft_run_plan_unittest_outside").exists())
            finally:
                brp.BACKTEST_ROOT = old_root

    def test_unresolved_universe_does_not_default_btcusdt(self) -> None:
        # No symbols + no metadata symbol => unresolved universe, NOT a silent BTCUSDT default.
        plan = brp.build_run_plan(
            "QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK",
            {"strategy_display_name": "8 EMA Pullback"},
            list(brp.OFFICIAL_PROFILES), [], ["10m"], 5000, "draft_run_plan_test_eq",
        )
        self.assertEqual(plan["symbols"], [])
        self.assertNotIn("BTCUSDT", plan["symbols"])
        self.assertEqual(plan["universe"]["status"], "needs_freeze")
        self.assertIn("symbol universe unresolved (needs_freeze)", plan["missing_assumptions"])
        # Still schema-valid: unresolved universe is allowed but explicit.
        self.assertEqual(validate_json_schema(plan, _schema("run_plan.schema.json")), [])

    def test_explicit_symbols_are_used(self) -> None:
        plan = brp.build_run_plan(
            "QL_TEST_STRATEGY", None, list(brp.OFFICIAL_PROFILES),
            ["AAPL", "MSFT"], ["1D"], 5000, "draft_run_plan_test_sym", symbol_source="cli",
        )
        self.assertEqual(plan["symbols"], ["AAPL", "MSFT"])
        self.assertEqual(plan["universe"]["status"], "draft")
        self.assertEqual(plan["universe"]["source"], "cli")

    def test_main_unknown_strategy_never_injects_default_symbol(self) -> None:
        rc = brp.main(["--strategy-id", "QL_UNKNOWN_NONCRYPTO_XYZ", "--dry-run",
                       "--run-id", "draft_run_plan_unittest_nosym"])
        self.assertEqual(rc, 0)  # dry-run, unresolved universe is allowed
        self.assertFalse((brp.BACKTEST_ROOT / "draft_run_plan_unittest_nosym").exists())

    def test_schema_requires_safety_fields(self) -> None:
        schema = _schema("run_plan.schema.json")
        plan = self._plan()
        self.assertEqual(validate_json_schema(plan, schema), [])
        # read_only must be true
        bad = dict(plan); bad["read_only"] = False
        self.assertTrue(validate_json_schema(bad, schema))
        # no_execution must be true
        bad = dict(plan); bad["no_execution"] = False
        self.assertTrue(validate_json_schema(bad, schema))
        # approval block required
        bad = dict(plan); bad.pop("approval")
        self.assertTrue(validate_json_schema(bad, schema))
        # approval.execution_allowed must be false
        bad = dict(plan); bad["approval"] = dict(plan["approval"]); bad["approval"]["execution_allowed"] = True
        self.assertTrue(validate_json_schema(bad, schema))
        # approval.approved must be false
        bad = dict(plan); bad["approval"] = dict(plan["approval"]); bad["approval"]["approved"] = True
        self.assertTrue(validate_json_schema(bad, schema))
        # expected_artifacts required
        bad = dict(plan); bad.pop("expected_artifacts")
        self.assertTrue(validate_json_schema(bad, schema))


if __name__ == "__main__":
    unittest.main()
