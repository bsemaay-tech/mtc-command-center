from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from mcc_readonly.optimization_reader import build_optimization_status


SOURCE_MCC_ROOT = Path(__file__).resolve().parents[4]


class OptimizationReaderTests(unittest.TestCase):
    def test_reads_runs_candidates_and_risk_notes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            mtc = Path(tmp) / "mtc"
            opt = mtc / "reports" / "optimization" / "sample_run"
            ranked = opt / "ranked"
            logs = opt / "logs"
            (root / "00_CONFIG").mkdir(parents=True)
            ranked.mkdir(parents=True)
            logs.mkdir(parents=True)
            _write_paths(root, mtc)
            _write_json(
                opt / "run_config.json",
                {
                    "run_id": "sample",
                    "planned_evaluations": 10,
                    "max_workers": 4,
                    "selected_dataset_count": 2,
                    "unique_parameter_variants": 5,
                    "walkforward_split_count": 2,
                    "started_at": "2026-05-01T00:00:00+00:00",
                    "warning": "Research seed only.",
                },
            )
            _write_json(logs / "runtime_summary.json", {"completed": 10, "failed": 0, "planned": 10})
            (ranked / "ranked_candidates.csv").write_text(
                "\n".join(
                    [
                        "parameter_hash,score,robust_level,median_test_profit_factor,median_test_net_profit_pct,worst_test_drawdown_pct,params_json,symbols_tested,timeframes_tested",
                        'abc,12.5,ROBUST_MEDIUM,1.2,3.4,8.0,"{""signal_mode"": ""Supertrend"", ""st_factor"": 3.5}",BTCUSDT,1h',
                    ]
                ),
                encoding="utf-8",
            )
            (opt / "KNOWN_OPTIMIZATION_ISSUES.md").write_text("# Known Optimization Issues\n", encoding="utf-8")

            status = build_optimization_status(root)
            self.assertEqual(status["summary"]["total_runs"], 1)
            self.assertEqual(status["summary"]["completed_runs"], 1)
            self.assertEqual(status["summary"]["top_candidate_count"], 1)
            self.assertEqual(status["top_candidates"][0]["parameter_hash"], "abc")
            self.assertEqual(status["summary"]["risk_note_count"], 1)

    def test_real_config_returns_optimization_shape(self) -> None:
        status = build_optimization_status(SOURCE_MCC_ROOT)
        self.assertIn("summary", status)
        self.assertIn("runs", status)
        self.assertIn("top_candidates", status)


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


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
