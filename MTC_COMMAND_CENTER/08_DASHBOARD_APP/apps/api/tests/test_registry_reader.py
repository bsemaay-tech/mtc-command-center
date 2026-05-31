from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from mcc_readonly.registry_reader import build_strategy_registry


SOURCE_MCC_ROOT = Path(__file__).resolve().parents[4]


class RegistryReaderTests(unittest.TestCase):
    def test_reads_candidate_csv_and_promoted_specs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            mtc = Path(tmp) / "mtc"
            lab = mtc / "06_QUANTLENS_LAB"
            registry = lab / "_registry"
            backtests = lab / "05_BACKTEST_RESULTS"
            promoted = lab / "06_PROMOTED_TO_PARITY" / "QL_ALPHA"
            (root / "00_CONFIG").mkdir(parents=True)
            registry.mkdir(parents=True)
            backtests.mkdir(parents=True)
            promoted.mkdir(parents=True)
            candidate_folder = lab / "01_TRIAGED_CANDIDATES" / "QL_ONE"
            candidate_folder.mkdir(parents=True)
            _write_paths(root, mtc)
            (registry / "quantlens_candidate_registry.csv").write_text(
                "\n".join(
                    [
                        "candidate_id,status,title,source_url,market_type,timeframe,candidate_kind,commercial_value_score,complexity_score,repaint_risk,lookahead_risk,closed_source_risk,mtc_overlap,next_action,candidate_folder,created_at,updated_at",
                        "QL_ONE,PROTOTYPED,One,,CRYPTO,1h,entry|exit,7,3,LOW,LOW,LOW,overlap,next,06_QUANTLENS_LAB/01_TRIAGED_CANDIDATES/QL_ONE,2026-05-01,2026-05-30",
                    ]
                ),
                encoding="utf-8",
            )
            (candidate_folder / "00_raw_quantlens_report.md").write_text(
                "# Candidate\n"
                "Source URL: https://youtu.be/example123\n",
                encoding="utf-8",
            )
            _write_json(backtests / "QL_ONE_results.json", {"summary": {}})
            _write_json(
                promoted / "producer_spec.json",
                {
                    "candidate_id": "QL_ALPHA",
                    "engine_strategy_id": "QL_ONE",
                    "strategy_family": "Family",
                    "symbol": "BTCUSDT",
                    "timeframe": "1h",
                    "promotion_status": ["PROMOTE_TO_PARITY_CANDIDATE"],
                    "metrics_lockbox": {"return_pct_compound": 10.0, "profit_factor": 1.2, "trades": 5},
                },
            )

            registry_payload = build_strategy_registry(root)
            self.assertEqual(len(registry_payload["candidates"]), 1)
            self.assertEqual(len(registry_payload["strategies"]), 1)
            self.assertEqual(registry_payload["candidates"][0]["evidence_level"], "backtested")
            self.assertEqual(registry_payload["candidates"][0]["source_url"], "https://youtu.be/example123")
            self.assertEqual(registry_payload["strategies"][0]["evidence_level"], "promoted_to_parity")

    def test_real_config_returns_registry_shape(self) -> None:
        registry = build_strategy_registry(SOURCE_MCC_ROOT)
        self.assertIn("candidates", registry)
        self.assertIn("strategies", registry)
        self.assertGreaterEqual(len(registry["candidates"]), 0)


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
