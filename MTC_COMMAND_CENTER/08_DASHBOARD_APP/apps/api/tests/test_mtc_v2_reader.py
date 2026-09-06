from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from mcc_readonly.mtc_v2_reader import build_mtc_v2_readiness


class MtcV2ReaderTests(unittest.TestCase):
    def test_builds_readiness_rows_from_configured_mtc_v2_root(self) -> None:
        # D12: mtc_v2_root must come from 00_CONFIG (paths.example.json /
        # paths.local.json), the same way every other reader resolves it —
        # not from an unconditional root.parent / "01_MASTER TEMPLATE_V2".
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            mtc_root = Path(tmp) / "01_MTC_PROJECT"
            (root / "00_CONFIG").mkdir(parents=True)
            (mtc_root / "01_PINE").mkdir(parents=True)
            (mtc_root / "01_PINE" / "MTC_V2.pine").write_text("// pine", encoding="utf-8")
            (mtc_root / "05_PARITY").mkdir(parents=True)
            (mtc_root / "05_PARITY" / "MTC_V2_PARITY_CASES.csv").write_text(
                "case_id,status,parity_verdict\nAUTO_001,DONE,PASS\nAUTO_002,DONE,FAIL\n",
                encoding="utf-8",
            )
            _write_paths(root, mtc_root)

            readiness = build_mtc_v2_readiness(
                root,
                candidate_pipeline={
                    "rows": [
                        {
                            "id": "QL_READY",
                            "stg_code": "Stg001",
                            "score": 90,
                            "current_stage_key": "pre_parity",
                            "next_action": "Finish: Start forward paper-trade (collect new trades)",
                            "paper_trade_detail": {
                                "plan_summary": ["Minimum NEW forward trades before evaluation: 30"],
                                "forward_trades": 0,
                                "forward_status": "WAITING_FOR_FORWARD_RESULTS",
                            },
                        },
                        {
                            "id": "QL_PROMOTED",
                            "score": 78,
                            "current_stage_key": "promoted",
                            "next_action": "Run PineTS Pine=Python parity",
                        },
                    ]
                },
                candidate_audit={
                    "rows": [
                        {
                            "id": "QL_READY",
                            "eligible_for_backtest": True,
                            "has_deterministic_rules": True,
                            "has_source_url_transcript": True,
                            "source_quality": "HIGH",
                        },
                        {
                            "id": "QL_PROMOTED",
                            "eligible_for_backtest": True,
                            "has_deterministic_rules": True,
                            "has_source_url_transcript": True,
                            "source_quality": "HIGH",
                        },
                    ]
                },
            )

            rows = {row["id"]: row for row in readiness["rows"]}
            # mtc_v2_root must equal the *configured* path, not the legacy
            # root.parent / "01_MASTER TEMPLATE_V2" sibling-of-root guess.
            self.assertEqual(readiness["mtc_v2_root"], str(mtc_root))
            self.assertTrue(readiness["pine_exists"])
            self.assertEqual(readiness["parity_tracker"]["path"], str(mtc_root / "05_PARITY" / "MTC_V2_PARITY_CASES.csv"))
            self.assertEqual(readiness["parity_tracker"]["total_cases"], 2)
            self.assertEqual(readiness["parity_tracker"]["pass_cases"], 1)
            self.assertEqual(rows["QL_READY"]["status"], "NEEDS_FORWARD_EVIDENCE")
            self.assertEqual(rows["QL_READY"]["forward_progress"]["target_trades"], 30)
            self.assertIn("0/30 trades", rows["QL_READY"]["decision_sentence"])
            self.assertEqual(rows["QL_PROMOTED"]["status"], "NEEDS_PINETS_PARITY")
            self.assertEqual(readiness["summary"]["needs_pinets_parity"], 1)
            self.assertIn("forward paper-trade", readiness["summary"]["calibration_note"])

    def test_unconfigured_mtc_v2_root_is_fail_closed(self) -> None:
        # No 00_CONFIG/paths.example.json at all -> mtc_v2_root cannot be
        # resolved. Readiness rows must still be produced (they only depend
        # on the pipeline/audit candidates), but every MTC_V2-root-derived
        # field must render the same explicit "missing" shape other readers
        # use for an unconfigured mtc_v2_root, never a guessed legacy path.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            root.mkdir(parents=True)

            readiness = build_mtc_v2_readiness(root, candidate_pipeline={"rows": []}, candidate_audit={"rows": []})

            self.assertEqual(readiness["mtc_v2_root"], "")
            self.assertEqual(readiness["pine_path"], "")
            self.assertFalse(readiness["pine_exists"])
            self.assertEqual(readiness["architecture_path"], "")
            self.assertFalse(readiness["architecture_exists"])
            self.assertEqual(
                readiness["parity_tracker"],
                {"path": "", "exists": False, "total_cases": 0, "pass_cases": 0},
            )
            # Readiness rows still compute from the pipeline/audit candidates
            # independently of mtc_v2_root — an unconfigured root must not
            # blank out the rest of the payload.
            self.assertEqual(readiness["rows"], [])
            self.assertEqual(readiness["summary"]["total_rows"], 0)


def _write_paths(root: Path, mtc_v2_root: Path) -> None:
    (root / "00_CONFIG").mkdir(parents=True, exist_ok=True)
    (root / "00_CONFIG" / "paths.example.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "mcc_root": str(root),
                "mtc_v2_root": str(mtc_v2_root),
                "mtc_v2_python_exe": None,
                "pinets_root": str(mtc_v2_root / "05_PARITY"),
                "tradingview_exports_dir": None,
                "reports_root": str(root / "04_REPORTS"),
            }
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    unittest.main()
