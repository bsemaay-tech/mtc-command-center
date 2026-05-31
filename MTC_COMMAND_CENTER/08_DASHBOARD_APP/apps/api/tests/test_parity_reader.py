from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from mcc_readonly.parity_reader import build_parity_status


SOURCE_MCC_ROOT = Path(__file__).resolve().parents[4]


class ParityReaderTests(unittest.TestCase):
    def test_reads_manual_summary_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            parity = Path(tmp) / "parity"
            (root / "00_CONFIG").mkdir(parents=True)
            (parity).mkdir(parents=True)
            _write_paths(root, parity)
            (parity / "parity_results.json").write_text(
                json.dumps(
                    {
                        "timestamp": "2026-05-30T00:00:00+00:00",
                        "summary": {"cases_missing": 1},
                        "rows": [
                            {
                                "case": "case_001",
                                "title": "Strict",
                                "parity_classification": "STRICT_PASS",
                                "tw_vs_pine_strict": True,
                                "tw_vs_python_strict": True,
                                "pine_vs_python_strict": True,
                            },
                            {
                                "case": "case_002",
                                "title": "Fail",
                                "parity_classification": "FAIL",
                                "tw_vs_pine_strict": False,
                                "tw_vs_python_strict": False,
                                "pine_vs_python_strict": True,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            status = build_parity_status(root)
            self.assertEqual(status["summary"]["total_cases"], 2)
            self.assertEqual(status["summary"]["failed"], 1)
            self.assertEqual(status["summary"]["needs_user_export"], 1)

    def test_real_config_returns_status_shape(self) -> None:
        status = build_parity_status(SOURCE_MCC_ROOT)
        self.assertIn("summary", status)
        self.assertIn("cases", status)
        self.assertGreaterEqual(status["summary"]["total_cases"], 0)


def _write_paths(root: Path, parity: Path) -> None:
    shutil.copytree(SOURCE_MCC_ROOT / "06_SCHEMAS", root / "06_SCHEMAS")
    (root / "00_CONFIG" / "paths.example.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "mcc_root": str(root),
                "mtc_v2_root": str(root.parent / "mtc"),
                "mtc_v2_python_exe": None,
                "pinets_root": str(parity),
                "tradingview_exports_dir": None,
                "reports_root": str(root / "04_REPORTS"),
            }
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    unittest.main()
