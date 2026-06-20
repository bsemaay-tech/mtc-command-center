from __future__ import annotations

import json
import threading
import tempfile
import unittest
from http.client import HTTPConnection
from pathlib import Path
from urllib.parse import quote

from mcc_readonly.health import build_health_report
from mcc_readonly.json_io import read_json_file
from mcc_readonly.read_model import build_dashboard_snapshot, build_dashboard_snapshot_cached, build_read_model
from mcc_readonly.server import make_server


MCC_ROOT = Path(__file__).resolve().parents[4]


class ReadOnlyCoreTests(unittest.TestCase):
    def test_health_report_contract(self) -> None:
        report = build_health_report(MCC_ROOT)
        self.assertTrue(report["api_ok"])
        self.assertTrue(report["schema_validation_ok"])
        self.assertTrue(report["paths_resolvable"])
        self.assertIn("lock_dir_writable", report)
        self.assertIn("mtc_v2_root_reachable", report)

    def test_read_model_contains_mvp1_files(self) -> None:
        model = build_read_model(MCC_ROOT)
        self.assertTrue(model["summary"]["required_files_ok"])
        self.assertTrue(model["summary"]["schema_validation_ok"])
        self.assertIn("current_status", model["files"])
        self.assertIn("task_queue", model["files"])
        self.assertIn("liveops_status", model["files"])
        self.assertIn("backtest_status", model["files"])
        self.assertIn("optimization_status", model["files"])
        self.assertIn("pine_builder_status", model["files"])
        self.assertIn("report_manifest", model["files"])
        self.assertIn("strategy_registry", model["files"])

    def test_dashboard_snapshot_is_read_only_payload(self) -> None:
        snapshot = build_dashboard_snapshot(MCC_ROOT)
        self.assertEqual(snapshot["mode"], "read_only")
        self.assertIn("current_status", snapshot)
        self.assertIn("file_diagnostics", snapshot)

    def test_dashboard_snapshot_cache_can_be_forced(self) -> None:
        first = build_dashboard_snapshot_cached(MCC_ROOT, force_refresh=True)
        second = build_dashboard_snapshot_cached(MCC_ROOT)
        forced = build_dashboard_snapshot_cached(MCC_ROOT, force_refresh=True)
        self.assertEqual(first["snapshot_cache"]["status"], "REFRESH")
        self.assertEqual(second["snapshot_cache"]["status"], "HIT")
        self.assertEqual(forced["snapshot_cache"]["status"], "REFRESH")

    def test_invalid_json_returns_diagnostic_not_exception(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bad_file = root / "bad.json"
            bad_file.write_text("{not valid", encoding="utf-8")
            result = read_json_file(root, "bad.json", required=True)
            self.assertFalse(result.ok)
            self.assertIn("json parse error", result.error or "")

    def test_http_contract_is_read_only(self) -> None:
        server = make_server("127.0.0.1", 0, MCC_ROOT)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        host, port = server.server_address
        try:
            health = _request_json(host, port, "GET", "/healthz")
            self.assertEqual(health["status"], 200)
            self.assertTrue(health["body"]["api_ok"])

            read_model = _request_json(host, port, "GET", "/api/read-model")
            self.assertEqual(read_model["status"], 200)
            self.assertTrue(read_model["body"]["summary"]["required_files_ok"])

            snapshot = _request_json(host, port, "GET", "/api/snapshot")
            self.assertEqual(snapshot["status"], 200)
            self.assertEqual(snapshot["body"]["mode"], "read_only")
            self.assertIn(snapshot["body"]["snapshot_cache"]["status"], {"HIT", "MISS", "REFRESH"})
            self.assertIn("liveops_status", snapshot["body"])
            # Low-risk payload slimming (SNAPSHOT_PAYLOAD_PERFORMANCE_AUDIT_2026-06-16):
            # candidate_audit is omitted from the HTTP snapshot (CLI/tests still build it).
            self.assertNotIn("candidate_audit", snapshot["body"])
            # scorecards.cards preserved; by_strategy duplicate dropped from HTTP snapshot.
            scorecards = snapshot["body"]["scorecards"]
            self.assertIn("cards", scorecards)
            self.assertNotIn("by_strategy", scorecards)
            # candidate_pipeline rows expose scorecard_v2_cases as a count (int) or None,
            # never the heavy embedded array.
            for row in snapshot["body"]["candidate_pipeline"].get("rows", []):
                if "scorecard_v2_cases" in row:
                    self.assertNotIsInstance(row["scorecard_v2_cases"], list)
                    self.assertTrue(
                        row["scorecard_v2_cases"] is None
                        or isinstance(row["scorecard_v2_cases"], int)
                    )
            self.assertIn("backtest_status", snapshot["body"])
            self.assertIn("optimization_status", snapshot["body"])
            self.assertIn("pine_builder_status", snapshot["body"])
            self.assertIn("strategy_registry", snapshot["body"])
            self.assertIn("task_lifecycle", snapshot["body"])
            self.assertIn("summary", snapshot["body"]["liveops_status"])
            self.assertIn("summary", snapshot["body"]["parity_status"])
            self.assertIn("summary", snapshot["body"]["backtest_status"])
            self.assertIn("summary", snapshot["body"]["optimization_status"])
            self.assertIn("summary", snapshot["body"]["pine_builder_status"])
            self.assertIn("candidates", snapshot["body"]["strategy_registry"])

            # M1 lazy-load slim: scorecard cards keep gate scores/statuses but drop the
            # verbose gate sub_scores and notes (served on demand by /api/scorecard-detail).
            sc_cards = snapshot["body"]["scorecards"]["cards"]
            self.assertIsInstance(sc_cards, list)
            for card in sc_cards:
                for gk in ("gate1", "gate1B", "gate2", "gate3"):
                    gate = card.get(gk)
                    if isinstance(gate, dict):
                        self.assertNotIn("sub_scores", gate)
                self.assertNotIn("notes", card)
            self.assertTrue(
                any(
                    isinstance(c.get("gate_summary"), dict) and "statuses" in c["gate_summary"]
                    for c in sc_cards
                )
            )
            # pipeline rows also drop scorecard_v2 gate sub_scores but keep scores/statuses.
            for row in snapshot["body"]["candidate_pipeline"].get("rows", []):
                v2 = row.get("scorecard_v2")
                if isinstance(v2, dict):
                    for gk in ("gate1", "gate1B", "gate2", "gate3"):
                        if isinstance(v2.get(gk), dict):
                            self.assertNotIn("sub_scores", v2[gk])

            refresh_snapshot = _request_json(host, port, "GET", "/api/snapshot?refresh=1")
            self.assertEqual(refresh_snapshot["status"], 200)
            self.assertEqual(refresh_snapshot["body"]["snapshot_cache"]["status"], "REFRESH")

            dashboard = _request_text(host, port, "GET", "/dashboard")
            self.assertEqual(dashboard["status"], 200)
            self.assertIn("MTC Command Center", dashboard["body"])

            asset = _request_text(host, port, "GET", "/web/app.js")
            self.assertEqual(asset["status"], 200)
            self.assertIn("/api/snapshot", asset["body"])

            report = _request_json(
                host,
                port,
                "GET",
                "/api/report?path=04_REPORTS/ai_handoffs/MCC_BOOT_006_COMPLETION_REPORT.md",
            )
            self.assertEqual(report["status"], 200)
            self.assertEqual(report["body"]["mode"], "read_only")
            self.assertIn("MCC-BOOT-006 Completion Report", report["body"]["content"])

            blocked_report = _request_json(host, port, "GET", "/api/report?path=../README.md")
            self.assertEqual(blocked_report["status"], 404)

            blocked = _request_json(host, port, "POST", "/api/snapshot")
            self.assertEqual(blocked["status"], 405)
            self.assertIn("read-only", blocked["body"]["error"])

            # --- /api/scorecard-detail lazy-load endpoint ---
            sid = "GEN_ATR_PULLBACK_TREND"
            detail = _request_json(host, port, "GET", "/api/scorecard-detail?strategy_id=" + quote(sid))
            self.assertEqual(detail["status"], 200)
            self.assertEqual(detail["body"]["mode"], "read_only")
            self.assertEqual(detail["body"]["strategy_id"], sid)
            self.assertGreater(detail["body"]["count"], 0)
            # full detail restores gate sub_scores for at least one gate.
            self.assertTrue(
                any(
                    isinstance(card.get(gk), dict) and "sub_scores" in card[gk]
                    for card in detail["body"]["cards"]
                    for gk in ("gate1", "gate1B", "gate2", "gate3")
                )
            )

            missing = _request_json(host, port, "GET", "/api/scorecard-detail?strategy_id=NO_SUCH_STRATEGY_XYZ")
            self.assertEqual(missing["status"], 404)
            self.assertEqual(missing["body"]["count"], 0)
            self.assertEqual(missing["body"]["cards"], [])

            # no arbitrary file read: path-like / traversal / missing params rejected.
            traversal = _request_json(host, port, "GET", "/api/scorecard-detail?strategy_id=" + quote("../../etc/passwd"))
            self.assertEqual(traversal["status"], 400)
            no_param = _request_json(host, port, "GET", "/api/scorecard-detail")
            self.assertEqual(no_param["status"], 400)

            # write methods blocked on the new endpoint too.
            blocked_detail = _request_json(host, port, "POST", "/api/scorecard-detail?strategy_id=" + quote(sid))
            self.assertEqual(blocked_detail["status"], 405)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


def _request_json(host: str, port: int, method: str, path: str) -> dict:
    connection = HTTPConnection(host, port, timeout=30)
    try:
        connection.request(method, path)
        response = connection.getresponse()
        raw = response.read().decode("utf-8")
        return {"status": response.status, "body": json.loads(raw)}
    finally:
        connection.close()


def _request_text(host: str, port: int, method: str, path: str) -> dict:
    connection = HTTPConnection(host, port, timeout=30)
    try:
        connection.request(method, path)
        response = connection.getresponse()
        raw = response.read().decode("utf-8")
        return {"status": response.status, "body": raw}
    finally:
        connection.close()


if __name__ == "__main__":
    unittest.main()
