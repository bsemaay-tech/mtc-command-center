from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from mcc_readonly.mtc_v2_reader import build_mtc_v2_readiness


class MtcV2ReaderTests(unittest.TestCase):
    def test_builds_readiness_rows_from_pipeline_and_audit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            mtc_root = Path(tmp) / "01_MASTER TEMPLATE_V2"
            (mtc_root / "01_PINE").mkdir(parents=True)
            (mtc_root / "01_PINE" / "MTC_V2.pine").write_text("// pine", encoding="utf-8")
            (mtc_root / "05_PARITY").mkdir(parents=True)
            (mtc_root / "05_PARITY" / "MTC_V2_PARITY_CASES.csv").write_text(
                "case_id,status,parity_verdict\nAUTO_001,DONE,PASS\nAUTO_002,DONE,FAIL\n",
                encoding="utf-8",
            )

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
            self.assertTrue(readiness["pine_exists"])
            self.assertEqual(readiness["parity_tracker"]["total_cases"], 2)
            self.assertEqual(readiness["parity_tracker"]["pass_cases"], 1)
            self.assertEqual(rows["QL_READY"]["status"], "NEEDS_FORWARD_EVIDENCE")
            self.assertEqual(rows["QL_READY"]["forward_progress"]["target_trades"], 30)
            self.assertIn("0/30 trades", rows["QL_READY"]["decision_sentence"])
            self.assertEqual(rows["QL_PROMOTED"]["status"], "NEEDS_PINETS_PARITY")
            self.assertEqual(readiness["summary"]["needs_pinets_parity"], 1)
            self.assertIn("forward paper-trade", readiness["summary"]["calibration_note"])


if __name__ == "__main__":
    unittest.main()
