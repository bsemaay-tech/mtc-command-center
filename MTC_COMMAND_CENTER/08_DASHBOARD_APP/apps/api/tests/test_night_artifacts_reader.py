from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from mcc_readonly.night_artifacts_reader import build_night_artifacts


SOURCE_MCC_ROOT = Path(__file__).resolve().parents[4]


def _make_root(tmp: str) -> Path:
    root = Path(tmp) / "MTC_COMMAND_CENTER"
    (root / "00_CONFIG").mkdir(parents=True)
    shutil.copytree(SOURCE_MCC_ROOT / "06_SCHEMAS", root / "06_SCHEMAS")
    return root


def _results_dir(root: Path, run_id: str) -> Path:
    d = root / "03_QUANTLENS" / "05_BACKTEST_RESULTS" / run_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


class NightArtifactsReaderTests(unittest.TestCase):
    def test_missing_all_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _make_root(tmp)
            # No 05_BACKTEST_RESULTS at all.
            model = build_night_artifacts(root)
            self.assertEqual(model["mode"], "read_only")
            self.assertEqual(model["profile_results"], [])
            self.assertEqual(model["run_plans"], [])
            self.assertFalse(model["summary"]["has_profile_separated_results"])
            self.assertIn("run_plan.json", model["missing"])
            self.assertIn("backtest_profile_result.json", model["missing"])
            self.assertEqual(model["summary"]["usable"], 0)

    def test_valid_run_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _make_root(tmp)
            run = _results_dir(root, "night_demo_run")
            _write_json(
                run / "run_plan.json",
                {
                    "schema_version": "1.0",
                    "run_id": "night_demo_run",
                    "read_only": True,
                    "no_execution": True,
                    "status": "draft_pending_approval",
                    "strategy_ids": ["QL_DEMO"],
                    "profiles": ["SOURCE_NAKED", "MTC_LIGHT"],
                    "symbols": ["BTCUSDT"],
                    "timeframes": ["4h"],
                    "case_count": 240,
                    "approval_state": "PENDING",
                    "approval": {"human_review_required": True, "approved": False, "execution_allowed": False},
                    "expected_artifacts": ["backtest_profile_result.json", "top_results.json"],
                    "output_dir": "03_QUANTLENS/05_BACKTEST_RESULTS/night_demo_run",
                },
            )
            model = build_night_artifacts(root)
            self.assertEqual(len(model["run_plans"]), 1)
            rec = model["run_plans"][0]
            self.assertEqual(rec["state"], "usable")
            self.assertEqual(rec["run_id"], "night_demo_run")
            self.assertEqual(rec["data"]["case_count"], 240)
            self.assertNotIn("run_plan.json", model["missing"])

    def test_valid_profile_result_populates_official_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _make_root(tmp)
            run = _results_dir(root, "night_demo_run")
            _write_json(
                run / "backtest_profile_result.json",
                {
                    "schema_version": "1.0",
                    "run_id": "night_demo_run",
                    "results": [
                        {
                            "strategy_id": "QL_DEMO",
                            "profile": "SOURCE_NAKED",
                            "symbol": "BTCUSDT",
                            "timeframe": "4h",
                            "score_method": "scorecard_v2",
                            "score": 82.5,
                            "metrics": {"net_profit": 41.2, "profit_factor": 1.6, "max_drawdown": 12.4, "trade_count": 38},
                            "promotion_status": "CANDIDATE",
                        },
                        {
                            "strategy_id": "QL_DEMO",
                            "profile": "NOT_A_PROFILE",
                            "symbol": "BTCUSDT",
                            "timeframe": "4h",
                        },
                    ],
                },
            )
            model = build_night_artifacts(root)
            self.assertTrue(model["summary"]["has_profile_separated_results"])
            rows = model["profile_results"]
            # Only the official-profile row is kept.
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["profile"], "SOURCE_NAKED")
            self.assertEqual(rows[0]["strategy_id"], "QL_DEMO")
            self.assertEqual(rows[0]["metrics"]["net_profit"], 41.2)

    def test_invalid_json_reported_not_crash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _make_root(tmp)
            run = _results_dir(root, "bad_run")
            (run / "run_status.json").write_text("{ not valid json ", encoding="utf-8")
            model = build_night_artifacts(root)
            self.assertEqual(len(model["run_status"]), 1)
            self.assertEqual(model["run_status"][0]["state"], "invalid")
            self.assertTrue(model["run_status"][0]["issues"])
            self.assertGreaterEqual(model["summary"]["invalid"], 1)

    def test_incomplete_when_schema_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _make_root(tmp)
            run = _results_dir(root, "partial_run")
            # Missing required strategy_ids / profiles -> incomplete.
            _write_json(run / "run_plan.json", {"run_id": "partial_run", "read_only": True})
            model = build_night_artifacts(root)
            rec = model["run_plans"][0]
            self.assertEqual(rec["state"], "incomplete")
            self.assertTrue(rec["issues"])

    def test_reader_does_not_write_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _make_root(tmp)
            _results_dir(root, "night_demo_run")
            before = sorted(p for p in (root / "03_QUANTLENS").rglob("*"))
            build_night_artifacts(root)
            after = sorted(p for p in (root / "03_QUANTLENS").rglob("*"))
            self.assertEqual(before, after)

    def test_real_root_returns_structure(self) -> None:
        model = build_night_artifacts(SOURCE_MCC_ROOT)
        for key in ("run_plans", "run_status", "profile_results", "top_results", "missing", "warnings", "summary"):
            self.assertIn(key, model)
        self.assertIsInstance(model["profile_results"], list)


if __name__ == "__main__":
    unittest.main()
