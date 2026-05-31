from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from mcc_readonly.backtest_reader import build_backtest_status


SOURCE_MCC_ROOT = Path(__file__).resolve().parents[4]


class BacktestReaderTests(unittest.TestCase):
    def test_reads_quantlens_and_status_shapes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            mtc = Path(tmp) / "mtc"
            backtests = mtc / "06_QUANTLENS_LAB" / "05_BACKTEST_RESULTS"
            optimization = mtc / "reports" / "optimization" / "run_a"
            (root / "00_CONFIG").mkdir(parents=True)
            backtests.mkdir(parents=True)
            (backtests / "nightly" / "detached").mkdir(parents=True)
            optimization.mkdir(parents=True)
            _write_paths(root, mtc)
            _write_json(
                backtests / "candidate_results.json",
                {
                    "backtest_run_at": "2026-05-30T00:00:00+00:00",
                    "candidate_id": "candidate",
                    "summary": {
                        "BTCUSDT": {"trades": 10, "win_rate_pct": 50, "net_return_sum_pct": 4.5},
                        "ETHUSDT": {"trades": 5, "win_rate_pct": 40, "net_return_sum_pct": -1.0},
                    },
                    "trades": [{"id": 1}],
                },
            )
            _write_json(
                backtests / "walk_forward_results.json",
                [
                    {"strategy": "s1", "symbol": "BTCUSDT", "timeframe": "1h", "status": "PASS"},
                    {"strategy": "s1", "symbol": "ETHUSDT", "timeframe": "1h", "status": "FAIL"},
                ],
            )
            _write_json(
                backtests / "MEGA_walk_forward_results.json",
                {
                    "generated_utc": "2026-05-30T01:00:00+00:00",
                    "runtime_seconds": 12,
                    "workers": 2,
                    "config": {"symbols": ["BTCUSDT", "ETHUSDT"], "timeframes": ["1h", "4h"]},
                    "results": [
                        {
                            "strategy": "s1",
                            "symbol": "BTCUSDT",
                            "timeframe": "1h",
                            "classification": "INSUFFICIENT_TRADES",
                            "summary": {"lockbox_oos": {"num_trades": 3}},
                            "robust_final": False,
                            "bh_fdr_survivor": False,
                        },
                        {
                            "strategy": "s2",
                            "symbol": "ETHUSDT",
                            "timeframe": "4h",
                            "classification": "PASS",
                            "summary": {"lockbox_oos": {"profit_factor": 1.4, "num_trades": 7}},
                            "robust_final": True,
                            "bh_fdr_survivor": True,
                        },
                    ],
                },
            )
            _write_json(
                backtests / "nightly" / "detached" / "run_status.json",
                {
                    "status": "stopped_by_user",
                    "completed_evaluations": 12,
                    "failed_evaluations": 0,
                    "symbols": ["BTCUSDT"],
                    "timeframes": ["1h"],
                },
            )
            _write_json(
                optimization / "metrics.json",
                {"completed_evaluations": 3, "failed_evaluations": 0, "worker_count": 2},
            )

            status = build_backtest_status(root)
            self.assertEqual(status["summary"]["total_runs"], 5)
            self.assertEqual(status["summary"]["failed_runs"], 1)
            self.assertEqual(status["summary"]["quantlens_result_runs"], 3)
            self.assertEqual(status["summary"]["detached_status_runs"], 1)
            self.assertEqual(status["summary"]["optimization_metric_runs"], 1)
            mega = next(run for run in status["runs"] if run["run_id"] == "MEGA_walk_forward")
            self.assertEqual(mega["status"], "COMPLETED")
            self.assertEqual(mega["classification_counts"]["INSUFFICIENT_TRADES"], 1)
            self.assertEqual(mega["strategy_count"], 2)
            self.assertEqual(mega["symbols_tested"], ["BTCUSDT", "ETHUSDT"])
            self.assertEqual(mega["timeframes_tested"], ["1h", "4h"])
            self.assertEqual(mega["trade_count"], 10)

    def test_real_config_returns_status_shape(self) -> None:
        status = build_backtest_status(SOURCE_MCC_ROOT)
        self.assertIn("summary", status)
        self.assertIn("runs", status)
        self.assertGreaterEqual(status["summary"]["total_runs"], 0)


def _write_paths(root: Path, mtc: Path) -> None:
    shutil.copytree(SOURCE_MCC_ROOT / "06_SCHEMAS", root / "06_SCHEMAS")
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
