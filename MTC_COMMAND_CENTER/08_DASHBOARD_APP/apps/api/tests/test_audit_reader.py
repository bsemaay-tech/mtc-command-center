from __future__ import annotations

import json
import unittest
import tempfile
from pathlib import Path

from mcc_readonly.audit_reader import build_candidate_audit


class CandidateAuditTests(unittest.TestCase):
    def test_audit_classifies_duplicate_blocked_and_eligible_rows(self) -> None:
        with self.subTest("audit row classification"):
            triage_map = Path("C:/TEMP/MTC_COMMAND_CENTER/11_TRIAGE/strategies")
            triage_map.mkdir(parents=True, exist_ok=True)
            (triage_map / "_stg_code_map.json").write_text(
                json.dumps({"A": "Stg001", "B": "Stg002", "C": "Stg003"}),
                encoding="utf-8",
            )
            audit = build_candidate_audit(
                Path("C:/TEMP/MTC_COMMAND_CENTER"),
                candidate_pipeline={
                    "rows": [
                        _row(
                            "A",
                            "Alpha Setup",
                            "backtested",
                            "https://youtu.be/a1",
                            "close > ema8 AND slope > 0",
                            "8 EMA Pullback",
                        ),
                        _row(
                            "B",
                            "Alpha Setup",
                            "discovered",
                            "https://youtu.be/a1",
                            "close > ema8 AND slope > 0",
                            "8 EMA Pullback",
                        ),
                        _row(
                            "C",
                            "Blocked Flow",
                            "discovered",
                            "",
                            "",
                            "Workflow only",
                        ),
                    ]
                },
                strategy_registry={"candidates": [], "strategies": []},
            )

            rows = {row["id"]: row for row in audit["rows"]}
            self.assertEqual(audit["summary"]["total_rows"], 3)

            self.assertEqual(rows["A"]["audit_status"], "CANONICAL")
            self.assertEqual(rows["A"]["canonical_id"], "A")
            self.assertTrue(rows["A"]["eligible_for_backtest"])
            self.assertEqual(rows["A"]["recommended_next_pipeline_step"], "Build promotion packet")
            self.assertEqual(rows["A"]["stg_code"], "Stg001")
            self.assertIsNotNone(rows["A"]["scorecard"])
            self.assertEqual(rows["A"]["scorecard"]["max"], 100)

            self.assertEqual(rows["B"]["audit_status"], "DUPLICATE")
            self.assertEqual(rows["B"]["duplicate_of"], "A")
            self.assertEqual(rows["B"]["recommended_next_pipeline_step"], "Merge into canonical record")
            self.assertTrue(rows["B"]["has_deterministic_rules"])

            self.assertEqual(rows["C"]["audit_status"], "BLOCKED")
            self.assertFalse(rows["C"]["eligible_for_backtest"])
            self.assertIn("source URL", rows["C"]["blocked_reason"])
            self.assertEqual(rows["C"]["recommended_next_pipeline_step"], "Source audit / park")
            self.assertEqual(rows["C"]["stg_code"], "Stg003")

    def test_audit_recovers_source_url_from_transcript_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            transcript_rel = "06_QUANTLENS_LAB/00_INBOX_REPORTS/Transcrips/Recovered URL.md"
            transcript_path = root / transcript_rel
            transcript_path.parent.mkdir(parents=True)
            transcript_path.write_text(
                "# Transcript\n"
                "Source URL: https://www.youtube.com/watch?v=abc123XYZ\n"
                "Some notes.\n",
                encoding="utf-8",
            )

            map_dir = root / "12_LLM_WIKI" / "test_import"
            map_dir.mkdir(parents=True)
            (map_dir / "quantlens_source_map.csv").write_text(
                "candidate_id,source_url,source_title,transcript_path,intake_path,corrected_intake_path,source_quality,rule_clarity_score,mechanical_testability_score,trader_credibility_context_score,data_availability_score,expected_edge_plausibility_score,MTC_compatibility_score,visual_review_priority,final_priority_score,classification,next_action,do_not_test_yet_reason\n"
                f"QLR_RECOVERED,,Recovered URL,{transcript_rel},,,,,,,,,,,,,\n",
                encoding="utf-8",
            )

            audit = build_candidate_audit(
                root,
                candidate_pipeline={
                    "rows": [
                        {
                            "id": "QLR_RECOVERED",
                            "name": "Recovered URL",
                            "symbol": "",
                            "timeframe": "1h",
                            "source_url": "",
                            "current_stage_key": "discovered",
                            "next_stage_key": None,
                            "next_action": "Review",
                            "description": {"family": "Test", "what": "Test"},
                            "directional_research": {
                                "status": "DIRECTION_UNKNOWN",
                                "long_signal_definition": "close > ema8 AND slope > 0",
                                "short_signal_definition": None,
                                "next_action": "Define long/short direction explicitly before backtest or parity.",
                            },
                            "notes": "close > ema8 AND slope > 0",
                        }
                    ]
                },
                strategy_registry={"candidates": [], "strategies": []},
            )

            row = audit["rows"][0]
            self.assertEqual(row["source_url_source"], "transcript")
            self.assertEqual(row["source_url"], "https://www.youtube.com/watch?v=abc123XYZ")
            self.assertTrue(row["has_source_url_transcript"])
            self.assertIn("transcript", row["source_quality_explanation"].lower())
            self.assertIn("eligible", row["eligibility_explanation"].lower())

    def test_audit_recovers_source_url_from_source_file_intake_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            intake_rel = "3 Mayıs/2026-05-03_NGyE4YIgGpU_quantlens_tito_adhikary_options_momentum_intake_report.md"
            intake_path = (
                Path(tmp)
                / "01_MASTER TEMPLATE_V2"
                / "06_QUANTLENS_LAB"
                / "00_INBOX_REPORTS"
                / intake_rel
            )
            intake_path.parent.mkdir(parents=True)
            intake_path.write_text(
                "# Intake report\n"
                "source_url: \"https://youtu.be/NGyE4YIgGpU?si=gj_6ZcIyjUFAEGhk\"\n",
                encoding="utf-8",
            )

            research_dir = (
                Path(tmp)
                / "01_MASTER TEMPLATE_V2"
                / "06_QUANTLENS_LAB"
                / "research"
                / "batch"
            )
            research_dir.mkdir(parents=True)
            (research_dir / "AUDITED_CANDIDATE_EXTRACTION.jsonl").write_text(
                json.dumps(
                    {
                        "candidate_id": "QL_TITO_OPTIONS_AWARE_RISK_OVERLAY_v0",
                        "title": "Options aware risk overlay",
                        "source_file": intake_rel,
                        "source_url": "",
                        "summary": "Risk overlay module.",
                        "recommended_next_action": "Define deterministic rules.",
                        "verdict": "UNKNOWN",
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            audit = build_candidate_audit(
                root,
                candidate_pipeline={
                    "rows": [
                        {
                            "id": "QL_TITO_OPTIONS_AWARE_RISK_OVERLAY_v0",
                            "name": "Options aware risk overlay",
                            "symbol": "",
                            "timeframe": "unknown",
                            "source_url": "",
                            "current_stage_key": "discovered",
                            "next_stage_key": None,
                            "next_action": "Review",
                            "description": {"family": "Risk module", "what": "Risk module"},
                            "directional_research": {
                                "status": "DIRECTION_UNKNOWN",
                                "long_signal_definition": "",
                                "short_signal_definition": None,
                                "next_action": "Define direction explicitly before backtest or parity.",
                            },
                            "notes": "Risk overlay module.",
                        }
                    ]
                },
                strategy_registry={"candidates": [], "strategies": []},
            )

            row = audit["rows"][0]
            self.assertEqual(row["source_url_source"], "source_file")
            self.assertEqual(row["source_url"], "https://youtu.be/NGyE4YIgGpU?si=gj_6ZcIyjUFAEGhk")
            self.assertTrue(row["has_source_url_transcript"])
            self.assertEqual(row["source_record"]["source_file"], intake_rel)

    def test_audit_marks_multi_setup_intake_as_split_required(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            intake_rel = "00_INBOX_REPORTS/Multi Setup Intake.md"
            intake_path = root / intake_rel
            intake_path.parent.mkdir(parents=True)
            intake_path.write_text(
                "# Multi setup intake\n"
                "The video contains three setups: breakout setup, reversal setup, and trend pullback setup.\n"
                "Long setup: price closes above VWAP after pullback.\n"
                "Short setup: price rejects VWAP after rally.\n",
                encoding="utf-8",
            )

            map_dir = root / "12_LLM_WIKI" / "test_import"
            map_dir.mkdir(parents=True)
            (map_dir / "quantlens_source_map.csv").write_text(
                "candidate_id,source_url,source_title,transcript_path,intake_path,corrected_intake_path,source_quality,rule_clarity_score,mechanical_testability_score,trader_credibility_context_score,data_availability_score,expected_edge_plausibility_score,MTC_compatibility_score,visual_review_priority,final_priority_score,classification,next_action,do_not_test_yet_reason\n"
                f"QL_MULTI_SETUP,https://www.youtube.com/watch?v=multi123,Multi setup,,{intake_rel},,,,,,,,,,,,,\n",
                encoding="utf-8",
            )

            audit = build_candidate_audit(
                root,
                candidate_pipeline={
                    "rows": [
                        {
                            "id": "QL_MULTI_SETUP",
                            "name": "Multi setup",
                            "symbol": "",
                            "timeframe": "1h",
                            "source_url": "https://www.youtube.com/watch?v=multi123",
                            "current_stage_key": "classified",
                            "next_stage_key": None,
                            "next_action": "Review",
                            "description": {"family": "VWAP", "what": "VWAP playbook"},
                            "directional_research": {
                                "status": "DIRECTION_UNKNOWN",
                                "long_signal_definition": "price closes above VWAP",
                                "short_signal_definition": None,
                                "next_action": "Define direction explicitly.",
                            },
                            "notes": "VWAP playbook",
                        }
                    ]
                },
                strategy_registry={"candidates": [], "strategies": []},
            )

            row = audit["rows"][0]
            self.assertEqual(row["audit_status"], "SPLIT_REQUIRED")
            self.assertEqual(row["blocked_reason"], "needs indicator split")
            self.assertGreaterEqual(row["split_candidate_count"], 2)
            self.assertEqual(row["recommended_next_pipeline_step"], "Split into indicator cases")


def _row(
    row_id: str,
    name: str,
    stage_key: str,
    source_url: str,
    rule_text: str,
    family: str,
) -> dict[str, object]:
    return {
        "id": row_id,
        "name": name,
        "symbol": "TEST",
        "timeframe": "1h",
        "source_url": source_url,
        "current_stage_key": stage_key,
        "next_stage_key": None,
        "next_action": "Review",
        "description": {"family": family, "what": f"{family} test"},
        "directional_research": {
            "status": "SHORT_UNTESTED",
            "long_signal_definition": rule_text,
            "short_signal_definition": None,
            "next_action": "Create a separate short candidate and run walk-forward / OOS before trusting it.",
        },
        "notes": rule_text,
    }


if __name__ == "__main__":
    unittest.main()
