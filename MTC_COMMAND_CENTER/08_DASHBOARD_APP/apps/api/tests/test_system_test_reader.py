from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from mcc_readonly.system_test_reader import (
    FIREWALL_BANNER,
    build_system_test_status,
)


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _make_run(root: Path, run_id: str, *, manifest: dict | None, recon: dict | None) -> Path:
    run_dir = root / "03_QUANTLENS" / "system_test" / run_id
    run_dir.mkdir(parents=True)
    if manifest is not None:
        _write_json(run_dir / "emitter_manifest.json", manifest)
    if recon is not None:
        _write_json(run_dir / "reconciliation_summary.json", recon)
    return run_dir


_OK_MANIFEST = {
    "banner": FIREWALL_BANNER,
    "benchmark_role": "SYSTEM_TEST_ONLY",
    "candidate_id": "QL_ALPHA_LINK_8EMA_1H",
    "engine_strategy_id": "QL_2026_INTRADAY",
    "expected_payload_count": 888,
    "promotable": False,
    "strategy_approval_status": "NOT_APPROVED",
    "symbol": "LINKUSDT",
    "timeframe": "1h",
    "robustness_note": "robust_final = 0.",
}
_OK_RECON = {
    "status": "OK",
    "expected_count": 888,
    "received_count": 888,
    "filled_count": 888,
    "rejected_count": 0,
    "duplicates_dropped": 0,
    "unexplained_count": 0,
    "expected_not_received": [],
    "received_not_expected": [],
    "received_not_filled": [],
}


class SystemTestReaderTests(unittest.TestCase):
    def test_reads_clean_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_run(root, "stg002_ok", manifest=_OK_MANIFEST, recon=_OK_RECON)

            status = build_system_test_status(root)

            self.assertEqual(status["firewall_banner"], FIREWALL_BANNER)
            self.assertEqual(status["summary"]["run_count"], 1)
            self.assertEqual(status["summary"]["ok_runs"], 1)
            self.assertTrue(status["summary"]["all_reconciled_clean"])
            self.assertFalse(status["summary"]["any_promotable"])

            run = status["runs"][0]
            self.assertEqual(run["status"], "OK")
            self.assertEqual(run["benchmark"]["candidate_id"], "QL_ALPHA_LINK_8EMA_1H")
            self.assertFalse(run["benchmark"]["promotable"])
            self.assertEqual(run["reconciliation"]["round_trips_approx"], 444)
            self.assertEqual(run["reconciliation"]["unexplained_count"], 0)

    def test_mismatch_when_unexplained(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bad = dict(_OK_RECON, unexplained_count=3, received_not_filled=["sig_42"])
            _make_run(root, "stg002_bad", manifest=_OK_MANIFEST, recon=bad)

            status = build_system_test_status(root)
            self.assertEqual(status["runs"][0]["status"], "MISMATCH")
            self.assertEqual(status["summary"]["mismatch_runs"], 1)
            self.assertFalse(status["summary"]["all_reconciled_clean"])

    def test_incomplete_when_no_reconciliation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_run(root, "stg002_partial", manifest=_OK_MANIFEST, recon=None)

            status = build_system_test_status(root)
            self.assertEqual(status["runs"][0]["status"], "INCOMPLETE")

    def test_honest_empty_state_when_no_runs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            status = build_system_test_status(Path(tmp))
            self.assertEqual(status["summary"]["run_count"], 0)
            self.assertIsNone(status["summary"]["latest_run_id"])
            self.assertFalse(status["summary"]["all_reconciled_clean"])
            # Firewall banner + gate ladder always present, even with no runs.
            self.assertEqual(status["firewall_banner"], FIREWALL_BANNER)
            self.assertTrue(status["gate_ladder"])

    def test_gate_ladder_and_next_action_are_reference_constants(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            status = build_system_test_status(Path(tmp))
            legs = {g["leg"] for g in status["gate_ladder"]}
            self.assertEqual(legs, {"V1.1", "V2", "V3", "V4", "V5"})
            self.assertIn("V1.1 CLOSED", status["next_approved_action"])


if __name__ == "__main__":
    unittest.main()
