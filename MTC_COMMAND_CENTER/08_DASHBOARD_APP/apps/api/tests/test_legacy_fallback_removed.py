from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from mcc_readonly.backtest_reader import build_backtest_status
from mcc_readonly.registry_reader import build_strategy_registry


class LegacyFallbackRemovedTests(unittest.TestCase):
    def test_registry_does_not_fall_back_to_legacy_quantlens_lab(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            mtc = Path(tmp) / "mtc"
            registry = mtc / "06_QUANTLENS_LAB" / "_registry"
            registry.mkdir(parents=True)
            _write_paths(root, mtc)
            (registry / "quantlens_candidate_registry.csv").write_text(
                "\n".join(
                    [
                        "candidate_id,status,title,source_url,market_type,timeframe,candidate_kind,commercial_value_score,complexity_score,repaint_risk,lookahead_risk,closed_source_risk,mtc_overlap,next_action,candidate_folder,created_at,updated_at",
                        "QL_LEGACY,PROTOTYPED,Legacy,,CRYPTO,1h,entry|exit,7,3,LOW,LOW,LOW,overlap,next,06_QUANTLENS_LAB/01_TRIAGED_CANDIDATES/QL_LEGACY,2026-05-01,2026-05-30",
                    ]
                ),
                encoding="utf-8",
            )

            payload = build_strategy_registry(root)

            self.assertEqual(payload["candidates"], [])
            self.assertEqual(payload["strategies"], [])

    def test_backtest_status_does_not_fall_back_to_legacy_quantlens_lab(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            mtc = Path(tmp) / "mtc"
            backtests = mtc / "06_QUANTLENS_LAB" / "05_BACKTEST_RESULTS"
            backtests.mkdir(parents=True)
            _write_paths(root, mtc)
            (backtests / "QL_ONE_results.json").write_text(
                json.dumps(
                    {
                        "backtest_run_at": "2026-05-30T00:00:00+00:00",
                        "candidate_id": "QL_ONE",
                        "summary": {
                            "BTCUSDT": {"trades": 10, "win_rate_pct": 50, "net_return_sum_pct": 4.5}
                        },
                    }
                ),
                encoding="utf-8",
            )

            status = build_backtest_status(root)

            self.assertEqual(status["summary"]["total_runs"], 0)
            self.assertEqual(
                [run for run in status["runs"] if run.get("source_type") == "quantlens_result"],
                [],
            )


def _write_paths(root: Path, mtc: Path) -> None:
    config = root / "00_CONFIG"
    config.mkdir(parents=True)
    (config / "paths.local.json").write_text(
        json.dumps({"mtc_v2_root": str(mtc)}),
        encoding="utf-8",
    )


if __name__ == "__main__":
    unittest.main()
