from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from mcc_readonly.scorecard_reader import build_scorecards


class ScorecardReaderTests(unittest.TestCase):
    def test_discovers_nested_scorecard_runs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            top_run = root / "03_QUANTLENS" / "05_BACKTEST_RESULTS" / "top_run"
            nested_run = root / "03_QUANTLENS" / "05_BACKTEST_RESULTS" / "night_run" / "iter_05"
            _write_scorecard(top_run, "GEN_TOP|BTCUSDT|1h")
            _write_scorecard(nested_run, "GEN_NESTED|ETHUSDT|4h")

            payload = build_scorecards(root)

            run_paths = {run["run_path"] for run in payload["runs"]}
            strategy_ids = {card["strategy_id"] for card in payload["cards"]}
            first_sub_score = payload["cards"][0]["gate2"]["sub_scores"][0]
            self.assertEqual(payload["count"], 2)
            self.assertIn("03_QUANTLENS/05_BACKTEST_RESULTS/top_run", run_paths)
            self.assertIn("03_QUANTLENS/05_BACKTEST_RESULTS/night_run/iter_05", run_paths)
            self.assertIn("GEN_TOP|BTCUSDT|1h", strategy_ids)
            self.assertIn("GEN_NESTED|ETHUSDT|4h", strategy_ids)
            self.assertEqual(first_sub_score["max_points"], 4)
            self.assertIn("Partial credit", first_sub_score["deduction_reason"])


def _write_scorecard(run_dir: Path, strategy_id: str) -> None:
    scorecard_dir = run_dir / "scorecard_v2"
    scorecard_dir.mkdir(parents=True, exist_ok=True)
    stem = strategy_id.replace("|", "_")
    payload = {
        "scorecard_version": "v2",
        "strategy_id": strategy_id,
        "gate_summary": {
            "statuses": {"gate2": "FAIL"},
            "blocking": ["test"],
            "promotable": False,
        },
        "gate2": {
            "status": "FAIL",
            "score": 10,
            "sub_scores": [
                {
                    "criterion": "profit_factor",
                    "points_max": 4,
                    "metric_status": "OK",
                    "points_awarded": 2,
                }
            ],
        },
    }
    (scorecard_dir / f"{stem}.scorecard.json").write_text(json.dumps(payload), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
