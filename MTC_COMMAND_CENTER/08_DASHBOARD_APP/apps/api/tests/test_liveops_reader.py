from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from mcc_readonly.liveops_reader import build_liveops_status


SOURCE_MCC_ROOT = Path(__file__).resolve().parents[4]


class LiveOpsReaderTests(unittest.TestCase):
    def test_reads_disabled_status_and_paper_plans(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            mtc = Path(tmp) / "mtc"
            promoted = mtc / "06_QUANTLENS_LAB" / "06_PROMOTED_TO_PARITY" / "QL_ALPHA"
            (root / "00_CONFIG").mkdir(parents=True)
            (root / "03_STATUS").mkdir(parents=True)
            promoted.mkdir(parents=True)
            _write_paths(root, mtc)
            _write_json(
                root / "03_STATUS" / "LIVEOPS_STATUS.json",
                {
                    "schema_version": "1.0",
                    "generated_at": "2026-05-30T00:00:00+03:00",
                    "mode": "disabled",
                    "dry_run": True,
                    "live_trading_enabled": False,
                    "events": [],
                },
            )
            (promoted / "FORWARD_PAPER_TRADE_PLAN.md").write_text("# Forward Paper Trade Plan\n", encoding="utf-8")

            status = build_liveops_status(root)
            self.assertTrue(status["summary"]["all_safety_gates_ok"])
            self.assertEqual(status["summary"]["paper_trade_plan_count"], 1)
            self.assertEqual(status["summary"]["live_order_count"], 0)
            self.assertEqual(status["summary"]["webhook_send_count"], 0)

    def test_real_config_returns_liveops_shape(self) -> None:
        status = build_liveops_status(SOURCE_MCC_ROOT)
        self.assertIn("summary", status)
        self.assertIn("safety_gates", status)
        self.assertFalse(status["live_trading_enabled"])

    def test_explicit_execution_signals_fail_safety_gates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            mtc = Path(tmp) / "mtc"
            (root / "00_CONFIG").mkdir(parents=True)
            (root / "03_STATUS").mkdir(parents=True)
            _write_paths(root, mtc)
            _write_json(
                root / "03_STATUS" / "LIVEOPS_STATUS.json",
                {
                    "schema_version": "1.0",
                    "generated_at": "2026-05-30T00:00:00+03:00",
                    "mode": "dry_run",
                    "dry_run": True,
                    "live_trading_enabled": False,
                    "webhook_sending_enabled": True,
                    "events": [{"event_type": "WEBHOOK_SENT"}, {"event_type": "LIVE_ORDER_SENT"}],
                },
            )

            status = build_liveops_status(root)
            self.assertFalse(status["summary"]["all_safety_gates_ok"])
            self.assertFalse(status["safety_gates"]["webhook_sending_disabled"])
            self.assertFalse(status["safety_gates"]["broker_integration_disabled"])
            self.assertEqual(status["summary"]["webhook_send_count"], 1)
            self.assertEqual(status["summary"]["live_order_count"], 1)


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
