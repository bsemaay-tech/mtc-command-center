from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from mcc_readonly.liveops_reader import build_liveops_status


SOURCE_MCC_ROOT = Path(__file__).resolve().parents[4]


class LiveOpsReaderTests(unittest.TestCase):
    def test_reads_disabled_status_and_paper_plans(self) -> None:
        # FORWARD_PAPER_TRADE_PLAN.md lives under the migrated QuantLens root
        # (03_QUANTLENS/strategies/<id>/...), not under mtc_v2_root — see
        # OVERNIGHT_LANE_V_DASHBOARD_PATH_MODEL_DECISION_2026-09-07.md (row 20).
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            mtc = Path(tmp) / "mtc"
            promoted = root / "03_QUANTLENS" / "strategies" / "QL_ALPHA"
            (root / "00_CONFIG").mkdir(parents=True)
            (root / "03_STATUS").mkdir(parents=True)
            mtc.mkdir(parents=True)
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

    def test_paper_trade_plans_discovered_from_quantlens_strategies_root(self) -> None:
        # Regression for the migrated-layout fix: FORWARD_PAPER_TRADE_PLAN.md
        # under <mcc_root>/03_QUANTLENS/strategies/<id>/ must be discovered even
        # when mtc_v2_root has no 06_QUANTLENS_LAB at all (the canonical,
        # already-migrated layout). Must FAIL before the fix (paper_trade_plans
        # always [] because only mtc_v2_root/06_QUANTLENS_LAB/
        # 06_PROMOTED_TO_PARITY was ever read) and PASS after.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            mtc = Path(tmp) / "mtc"
            promoted = root / "03_QUANTLENS" / "strategies" / "STG002"
            (root / "00_CONFIG").mkdir(parents=True)
            (root / "03_STATUS").mkdir(parents=True)
            mtc.mkdir(parents=True)
            promoted.mkdir(parents=True)
            _write_paths(root, mtc)
            (promoted / "FORWARD_PAPER_TRADE_PLAN.md").write_text(
                "# Forward Paper Trade Plan\n", encoding="utf-8"
            )

            status = build_liveops_status(root)
            self.assertEqual(status["summary"]["paper_trade_plan_count"], 1)
            self.assertEqual(status["paper_trade_plans"][0]["candidate_id"], "STG002")

    def test_paper_trade_plans_empty_when_quantlens_strategies_root_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            mtc = Path(tmp) / "mtc"
            (root / "00_CONFIG").mkdir(parents=True)
            (root / "03_STATUS").mkdir(parents=True)
            mtc.mkdir(parents=True)
            _write_paths(root, mtc)

            status = build_liveops_status(root)
            self.assertEqual(status["summary"]["paper_trade_plan_count"], 0)
            self.assertEqual(status["paper_trade_plans"], [])

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
