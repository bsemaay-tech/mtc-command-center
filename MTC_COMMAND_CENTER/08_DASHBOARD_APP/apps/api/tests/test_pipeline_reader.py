from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from mcc_readonly.pipeline_reader import build_candidate_pipeline


class PipelineReaderTests(unittest.TestCase):
    def test_promoted_strategy_includes_parity_paper_and_equity_detail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            strategy_id = "QL_ALPHA_LINK_8EMA_1H"
            strategy_dir = (
                Path(tmp)
                / "01_MASTER TEMPLATE_V2"
                / "06_QUANTLENS_LAB"
                / "06_PROMOTED_TO_PARITY"
                / strategy_id
            )
            strategy_dir.mkdir(parents=True)
            triage_map = (
                Path(tmp)
                / "MTC_COMMAND_CENTER"
                / "11_TRIAGE"
                / "strategies"
            )
            triage_map.mkdir(parents=True)
            (triage_map / "_stg_code_map.json").write_text(
                json.dumps({strategy_id: "Stg042", "QL_CAND_LINK_8EMA": "Stg042"}),
                encoding="utf-8",
            )
            _write_json(
                strategy_dir / "producer_spec.json",
                {
                    "candidate_id": strategy_id,
                    "direction": "long_only",
                    "long_signal_definition": "(close > ema8) AND (slope > 0)",
                    "short_signal_definition": None,
                },
            )
            _write_json(
                strategy_dir / "PINETS_PARITY_RESULT.json",
                {
                    "bars_compared": 100,
                    "signal_agreement_pct": 100.0,
                    "pine_long_signals": 4,
                    "python_long_signals": 4,
                    "long_both": 4,
                    "long_only_pine": 0,
                    "long_only_python": 0,
                    "ema8_max_rel_diff": 0.0,
                    "atr14_max_rel_diff": 0.0001,
                    "warmup_excluded": 20,
                    "verdict": "PASS",
                },
            )
            (strategy_dir / "FORWARD_PAPER_TRADE_PLAN.md").write_text(
                "# Forward Paper Trade Plan\n"
                "- **Minimum observation period:** 12 weeks\n"
                "- **Minimum NEW forward trades before evaluation:** 30\n",
                encoding="utf-8",
            )
            (strategy_dir / f"{strategy_id}_trades.csv").write_text(
                "entry_time,ret_net_pct\n2026-01-01,1.0\n2026-01-02,-0.5\n2026-01-03,2.0\n",
                encoding="utf-8",
            )

            registry = {
                "candidates": [
                    {"candidate_id": "QL_CAND_LINK_8EMA", "source_url": "https://youtu.be/example123"}
                ],
                "strategies": [
                    {
                        "strategy_id": strategy_id,
                        "candidate_id": "QL_CAND_LINK_8EMA",
                        "name": "LINK 8EMA",
                        "status": "PROMOTE_TO_PARITY_CANDIDATE",
                        "evidence_level": "promoted_to_parity",
                        "symbol": "LINKUSDT",
                        "timeframe": "1h",
                        "return_pct_compound": 12.5,
                        "profit_factor": 1.4,
                        "trades": 3,
                    }
                ],
            }
            liveops = {
                "paper_trade_plans": [
                    {
                        "candidate_id": strategy_id,
                        "status": "PAPER_PLAN_ONLY",
                        "live_orders_enabled": False,
                        "webhook_enabled": False,
                        "relative_path": "06_QUANTLENS_LAB/06_PROMOTED_TO_PARITY/QL_ALPHA_LINK_8EMA_1H/FORWARD_PAPER_TRADE_PLAN.md",
                    }
                ]
            }

            pipeline = build_candidate_pipeline(root, registry, {}, liveops, {}, {})
            row = pipeline["rows"][0]

            self.assertEqual(row["id"], strategy_id)
            self.assertEqual(row["stages"]["pre_parity"]["status"], "done")
            self.assertEqual(row["stages"]["paper_trade"]["status"], "active")
            self.assertEqual(row["next_stage_key"], "paper_trade")
            self.assertIn("Finish:", row["next_action"])
            self.assertEqual(row["pinets_parity_proof"]["summary"]["verdict"], "PASS")
            self.assertEqual(row["pinets_parity_proof"]["raw"]["bars_compared"], 100)
            self.assertGreater(len(row["equity_curve"]), 2)
            self.assertEqual(row["paper_trade_detail"]["status"], "PAPER_PLAN_ONLY")
            self.assertEqual(row["paper_trade_detail"]["forward_status"], "WAITING_FOR_FORWARD_RESULTS")
            self.assertTrue(row["paper_trade_detail"]["plan_summary"])
            self.assertEqual(row["source_url"], "https://youtu.be/example123")
            self.assertEqual(row["stg_code"], "Stg042")
            self.assertIsNotNone(row["scorecard"])
            self.assertGreaterEqual(row["score"], 0)
            self.assertEqual(row["scorecard"]["max"], 100)
            self.assertIsNotNone(row["producer_spec"])
            self.assertEqual(row["producer_spec"]["path"].endswith("producer_spec.json"), True)
            self.assertEqual(row["producer_spec"]["source_candidate"], None)
            self.assertEqual(row["directional_research"]["current_direction"], "long_only")
            self.assertEqual(row["directional_research"]["status"], "SHORT_UNTESTED")
            self.assertIn("ema8", row["directional_research"]["suggested_short_research_rule"])
            self.assertIn("own evidence", row["directional_research"]["warning"])
            self.assertEqual(row["classification"]["kind"], "candidate")
            self.assertIn("backtest-ready", row["classification"]["reason"])

    def test_salvage_candidate_requires_indicator_split(self) -> None:
        registry = {
            "candidates": [
                {
                    "candidate_id": "QL_SALVAGE_TV_BUYSELL",
                    "title": "Five TradingView buy/sell signal indicators",
                    "status": "SALVAGE_ONLY",
                    "timeframe": "mixed",
                }
            ],
            "strategies": [],
        }

        with tempfile.TemporaryDirectory() as tmp:
            pipeline = build_candidate_pipeline(Path(tmp) / "MTC_COMMAND_CENTER", registry, {}, {}, {}, {})
            row = pipeline["rows"][0]

            self.assertEqual(row["stages"]["backtested"]["status"], "na")
            self.assertEqual(row["stages"]["promoted"]["status"], "na")
            self.assertIsNone(row["next_stage_key"])
            self.assertIn("Split into indicator cases", row["next_action"])
            self.assertIsNone(row["pinets_parity_proof"])
            self.assertIsNone(row["paper_trade_detail"])
            self.assertEqual(row["directional_research"]["status"], "DIRECTION_UNKNOWN")
            self.assertEqual(row["classification"]["kind"], "split_required")
            self.assertIn("each open formula", row["classification"]["reason"])

    def test_discovers_extra_quantlens_jsonl_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            extra_path = (
                Path(tmp)
                / "01_MASTER TEMPLATE_V2"
                / "06_QUANTLENS_LAB"
                / "research"
                / "batch"
                / "FINAL_LLM_KNOWLEDGE_BASE.jsonl"
            )
            extra_path.parent.mkdir(parents=True)
            extra_path.write_text(
                json.dumps(
                    {
                        "record_type": "final_candidate_classification",
                        "candidate_id": "QLR_EXTRA_PULLBACK",
                        "title": "Extra pullback candidate",
                        "source_url": "https://www.youtube.com/watch?v=abc123",
                        "summary": "SWING_TRADE_STRATEGY with final action MANUAL_VISUAL_REVIEW_ONLY_NO_BACKTEST_YET.",
                        "recommended_next_action": "MANUAL_VISUAL_REVIEW_ONLY_NO_BACKTEST_YET",
                        "timeframe": "1D",
                        "direction": "long",
                    }
                )
                + "\n"
                + json.dumps(
                    {
                        "record_type": "final_candidate_classification",
                        "candidate_id": "QLR_BLOCKED",
                        "title": "Blocked candidate",
                        "summary": "DATA_BLOCKED with final action DO_NOT_TEST_UNTIL_SOURCE_RESOLVED.",
                        "recommended_next_action": "DO_NOT_TEST_UNTIL_SOURCE_RESOLVED",
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            pipeline = build_candidate_pipeline(root, {"candidates": [], "strategies": []}, {}, {}, {}, {})
            rows = {row["id"]: row for row in pipeline["rows"]}

            self.assertIn("QLR_EXTRA_PULLBACK", rows)
            self.assertEqual(rows["QLR_EXTRA_PULLBACK"]["stages"]["discovered"]["status"], "done")
            self.assertEqual(rows["QLR_EXTRA_PULLBACK"]["stages"]["backtested"]["status"], "na")
            self.assertEqual(rows["QLR_EXTRA_PULLBACK"]["source_url"], "https://www.youtube.com/watch?v=abc123")
            self.assertEqual(rows["QLR_EXTRA_PULLBACK"]["discovery_source"], "research\\batch\\FINAL_LLM_KNOWLEDGE_BASE.jsonl")
            self.assertEqual(rows["QLR_EXTRA_PULLBACK"]["classification"]["kind"], "wiki")
            self.assertIn("QLR_BLOCKED", rows)
            self.assertEqual(rows["QLR_BLOCKED"]["stages"]["backtested"]["status"], "na")
            self.assertEqual(rows["QLR_BLOCKED"]["classification"]["kind"], "rejected")

    def test_discovers_promoted_producer_specs_without_registry_strategy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            spec_dir = (
                Path(tmp)
                / "01_MASTER TEMPLATE_V2"
                / "06_QUANTLENS_LAB"
                / "06_PROMOTED_TO_PARITY"
                / "QL_NEW_PROMOTED_SPEC"
            )
            spec_dir.mkdir(parents=True)
            _write_json(
                spec_dir / "producer_spec.json",
                {
                    "candidate_id": "QL_NEW_PROMOTED_SPEC",
                    "source_url": "https://www.youtube.com/watch?v=abc123",
                    "source_candidate": "QLR_SOURCE",
                    "title": "New promoted producer spec",
                    "kind": "strategy",
                    "direction": "long_only",
                    "long_signal_definition": "close > high[1]",
                },
            )

            pipeline = build_candidate_pipeline(root, {"candidates": [], "strategies": []}, {}, {}, {}, {})
            rows = {row["id"]: row for row in pipeline["rows"]}

            self.assertIn("QL_NEW_PROMOTED_SPEC", rows)
            row = rows["QL_NEW_PROMOTED_SPEC"]
            self.assertEqual(row["current_stage_key"], "promoted")
            self.assertEqual(row["stages"]["promoted"]["status"], "done")
            self.assertEqual(row["source_url"], "https://www.youtube.com/watch?v=abc123")
            self.assertEqual(row["classification"]["next_action"], "Run PineTS parity")
            self.assertIsNotNone(row["producer_spec"])
            self.assertEqual(row["producer_spec"]["title"], "New promoted producer spec")
            self.assertEqual(row["producer_spec"]["source_url"], "https://www.youtube.com/watch?v=abc123")
            self.assertEqual(row["producer_spec"]["param_grid_size_planned"], None)
            self.assertEqual(row["directional_research"]["current_direction"], "long_only")


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
