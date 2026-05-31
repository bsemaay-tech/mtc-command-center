from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from mcc_readonly.pine_builder_reader import build_pine_builder_status


SOURCE_MCC_ROOT = Path(__file__).resolve().parents[4]


class PineBuilderReaderTests(unittest.TestCase):
    def test_classifies_review_drafts_and_compile_observations(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            mtc = Path(tmp) / "mtc"
            candidate = mtc / "06_QUANTLENS_LAB" / "06_PROMOTED_TO_PARITY" / "QL_ALPHA"
            sandbox = mtc / "06_QUANTLENS_LAB" / "strategy_sandboxes" / "QLR_ONE"
            template = mtc / "parity_oracles" / "templates"
            (root / "00_CONFIG").mkdir(parents=True)
            (mtc / "01_PINE").mkdir(parents=True)
            candidate.mkdir(parents=True)
            sandbox.mkdir(parents=True)
            template.mkdir(parents=True)
            _write_paths(root, mtc)
            (mtc / "01_PINE" / "MTC_V2.pine").write_text("// protected", encoding="utf-8")
            (candidate / "ALPHA_REVIEW.pine").write_text("//@version=6\nstrategy('x')", encoding="utf-8")
            (candidate / "PINE_PARITY_PLAN.md").write_text(
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
