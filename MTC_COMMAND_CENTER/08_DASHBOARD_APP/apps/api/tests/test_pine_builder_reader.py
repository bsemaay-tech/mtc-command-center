from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from mcc_readonly.pine_builder_reader import build_pine_builder_status


SOURCE_MCC_ROOT = Path(__file__).resolve().parents[4]


class PineBuilderReaderTests(unittest.TestCase):
    def test_classifies_review_drafts_and_compile_observations(self) -> None:
        # PINE_PARITY_PLAN.md lives under the migrated QuantLens root
        # (03_QUANTLENS/strategies/<id>/...), not under mtc_v2_root — see
        # OVERNIGHT_LANE_V_DASHBOARD_PATH_MODEL_DECISION_2026-09-07.md (row 18).
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            mtc = Path(tmp) / "mtc"
            candidate = mtc / "06_QUANTLENS_LAB" / "06_PROMOTED_TO_PARITY" / "QL_ALPHA"
            sandbox = mtc / "06_QUANTLENS_LAB" / "strategy_sandboxes" / "QLR_ONE"
            template = mtc / "parity_oracles" / "templates"
            promoted = root / "03_QUANTLENS" / "strategies" / "QL_ALPHA"
            (root / "00_CONFIG").mkdir(parents=True)
            (mtc / "01_PINE").mkdir(parents=True)
            candidate.mkdir(parents=True)
            sandbox.mkdir(parents=True)
            template.mkdir(parents=True)
            promoted.mkdir(parents=True)
            _write_paths(root, mtc)
            (mtc / "01_PINE" / "MTC_V2.pine").write_text("// protected", encoding="utf-8")
            (candidate / "ALPHA_REVIEW.pine").write_text("//@version=6\nstrategy('x')", encoding="utf-8")
            (promoted / "PINE_PARITY_PLAN.md").write_text(
                "2026-05-30: Pine v6 server compile = PASS (0 errors / 0 warnings).\n"
                "Chart-based trade parity PENDING.",
                encoding="utf-8",
            )
            (sandbox / "standalone_pine_visual_review.pine").write_text("// review", encoding="utf-8")
            (template / "pinets_feature_adapter_template.pine").write_text("// template", encoding="utf-8")

            status = build_pine_builder_status(root)
            self.assertEqual(status["summary"]["total_pine_files"], 4)
            self.assertEqual(status["summary"]["total_drafts"], 2)
            self.assertEqual(status["summary"]["compile_pass"], 1)
            self.assertEqual(status["summary"]["waiting_for_tradingview_compile"], 1)
            self.assertEqual(status["summary"]["protected_core_files"], 1)
            self.assertEqual(status["summary"]["supporting_pine_artifacts"], 1)
            self.assertEqual(status["drafts"][0]["protected_core"], False)

    def test_compile_observations_discovered_from_quantlens_strategies_root(self) -> None:
        # Regression for the migrated-layout fix: PINE_PARITY_PLAN.md under
        # <mcc_root>/03_QUANTLENS/strategies/<id>/ must join into compile_status,
        # even when mtc_v2_root has no 06_QUANTLENS_LAB at all (the canonical,
        # already-migrated layout). Must FAIL before the fix (compile_status
        # stayed UNKNOWN because only mtc_v2_root/06_QUANTLENS_LAB/
        # 06_PROMOTED_TO_PARITY was ever read) and PASS after.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            mtc = Path(tmp) / "mtc"
            draft_dir = mtc / "review_drafts" / "STG001"
            promoted = root / "03_QUANTLENS" / "strategies" / "STG001"
            (root / "00_CONFIG").mkdir(parents=True)
            draft_dir.mkdir(parents=True)
            promoted.mkdir(parents=True)
            _write_paths(root, mtc)
            (draft_dir / "STG001_REVIEW.pine").write_text("//@version=6\nstrategy('x')", encoding="utf-8")
            (promoted / "PINE_PARITY_PLAN.md").write_text(
                "2026-05-30: Pine v6 server compile = PASS (0 errors / 0 warnings).\n"
                "Live chart run PASS.",
                encoding="utf-8",
            )

            status = build_pine_builder_status(root)
            draft = next(d for d in status["drafts"] if d["candidate_id"] == "STG001")
            self.assertEqual(draft["compile_status"], "PASS")
            self.assertEqual(draft["chart_status"], "PASS")

    def test_compile_observations_empty_when_quantlens_strategies_root_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            mtc = Path(tmp) / "mtc"
            draft_dir = mtc / "review_drafts" / "STG001"
            (root / "00_CONFIG").mkdir(parents=True)
            draft_dir.mkdir(parents=True)
            _write_paths(root, mtc)
            (draft_dir / "STG001_REVIEW.pine").write_text("//@version=6\nstrategy('x')", encoding="utf-8")

            status = build_pine_builder_status(root)
            draft = next(d for d in status["drafts"] if d["candidate_id"] == "STG001")
            self.assertEqual(draft["compile_status"], "UNKNOWN")
            self.assertEqual(draft["chart_status"], "NOT_OBSERVED")

    def test_compile_observations_discovered_without_mtc_v2_root(self) -> None:
        # D18 follow-up regression: _compile_observations reads promoted-strategy
        # plans purely from <mcc_root>/03_QUANTLENS/strategies/<id>/ and no longer
        # depends on mtc_v2_root at all, so it must still run (and its
        # PINE_PARITY_PLAN.md timestamp must still surface via generated_at) even
        # when mtc_v2_root is unconfigured. Before this fix, build_pine_builder_status
        # short-circuited to _empty_status(...) (generated_at always None) as soon as
        # mtc_v2_root was None/missing, before _compile_observations ever ran.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            promoted = root / "03_QUANTLENS" / "strategies" / "STG009"
            (root / "00_CONFIG").mkdir(parents=True)
            promoted.mkdir(parents=True)
            (root / "00_CONFIG" / "paths.example.json").write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "mcc_root": str(root),
                        "mtc_v2_root": None,
                        "mtc_v2_python_exe": None,
                        "pinets_root": None,
                        "tradingview_exports_dir": None,
                        "reports_root": str(root / "04_REPORTS"),
                    }
                ),
                encoding="utf-8",
            )
            (promoted / "PINE_PARITY_PLAN.md").write_text(
                "2026-05-30: Pine v6 server compile = PASS (0 errors / 0 warnings).\n"
                "Live chart run PASS.",
                encoding="utf-8",
            )

            status = build_pine_builder_status(root)
            self.assertEqual(status["source"], "mtc_v2_root_not_configured")
            self.assertIsNotNone(status["generated_at"])

    def test_real_config_returns_pine_builder_shape(self) -> None:
        status = build_pine_builder_status(SOURCE_MCC_ROOT)
        self.assertIn("summary", status)
        self.assertIn("drafts", status)
        self.assertGreaterEqual(status["summary"]["total_drafts"], 0)


def _write_paths(root: Path, mtc: Path) -> None:
    (root / "00_CONFIG" / "paths.example.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "mcc_root": str(root),
                "mtc_v2_root": str(mtc),
                "mtc_v2_python_exe": None,
                "pinets_root": str(mtc / "05_PARITY"),
                "tradingview_exports_dir": None,
                "reports_root": str(root / "04_REPORTS"),
            }
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    unittest.main()
