"""Synthetic-only checks for the P030 adapter over unchanged P026 heartbeat tools."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import p030_opsa_heartbeat_adapter as subject


class HeartbeatAdapterTests(unittest.TestCase):
    ID = "fixture-p030-collector"

    def test_exact_p026_heartbeat_round_trip_and_extra_field_refusal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            state_dir = Path(temporary) / "state"
            with self.assertRaises(ValueError):
                subject.emit_process_heartbeat(state_dir, "", seq=1)
            self.assertFalse(state_dir.exists())

            path = subject.emit_process_heartbeat(state_dir, self.ID, seq=7, note="fixture")
            payload = subject.verify_process_heartbeat(path, expected_id=self.ID)
            self.assertEqual(
                set(payload), {"schema", "id", "seq", "emitted_at", "pid", "note"}
            )
            self.assertEqual(payload["schema"], "mtc.opsa_heartbeat/v1")
            self.assertEqual(payload["seq"], 7)
            payload["market_freshness"] = {}
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "heartbeat fields do not match P026"):
                subject.verify_process_heartbeat(path, expected_id=self.ID)

    def test_emitter_refuses_values_its_verifier_would_reject(self) -> None:
        for kwargs in ({"seq": True}, {"seq": 1, "note": {"truthy": True}}):
            with self.subTest(kwargs=kwargs), mock.patch.object(
                subject.heartbeat, "emit"
            ) as emit:
                with self.assertRaises(ValueError):
                    subject.emit_process_heartbeat("synthetic-state", self.ID, **kwargs)
            emit.assert_not_called()

    def test_entry_points_refuse_raw_empty_or_whitespace_state_dir(self) -> None:
        for state_dir in ("", "   "):
            with self.subTest(entry="heartbeat", state_dir=repr(state_dir)), mock.patch.object(
                subject.heartbeat, "emit"
            ) as emit:
                with self.assertRaisesRegex(ValueError, "state_dir"):
                    subject.emit_process_heartbeat(state_dir, self.ID, seq=1)
            emit.assert_not_called()
            with self.subTest(entry="health", state_dir=repr(state_dir)), mock.patch.object(
                subject, "atomic_write_json"
            ) as write_json:
                with self.assertRaisesRegex(ValueError, "state_dir"):
                    subject.write_health_sidecar(
                        state_dir,
                        self.ID,
                        observed_at_utc="2026-09-12T00:02:00Z",
                        last_accepted_timestamp_utc=None,
                        reconciliation_progress=None,
                    )
            write_json.assert_not_called()

    def test_verifier_refuses_duplicate_keys_and_nonfinite_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = subject.emit_process_heartbeat(
                Path(temporary), self.ID, seq=1
            )
            payload = path.read_text(encoding="utf-8")
            duplicate = payload.replace('"seq": 1', '"seq": 1, "seq": 1')
            path.write_text(duplicate, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                subject.verify_process_heartbeat(path, expected_id=self.ID)

            nonfinite = payload.replace('"seq": 1', '"seq": NaN')
            path.write_text(nonfinite, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "non-finite JSON constant"):
                subject.verify_process_heartbeat(path, expected_id=self.ID)

    def test_health_sidecar_binds_observed_time_raw_timestamp_and_derived_age(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            state_dir = Path(temporary) / "state"
            heartbeat_path = subject.emit_process_heartbeat(state_dir, self.ID, seq=1)
            subject.verify_process_heartbeat(heartbeat_path, expected_id=self.ID)

            sidecar_path = subject.write_health_sidecar(
                state_dir,
                self.ID,
                observed_at_utc="2026-09-12T00:02:00Z",
                last_accepted_timestamp_utc="2026-09-12T00:00:00Z",
                reconciliation_progress=None,
            )
            sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
            self.assertEqual(
                set(sidecar),
                {
                    "schema",
                    "id",
                    "observed_at_utc",
                    "market_freshness",
                    "reconciliation_progress",
                },
            )
            self.assertEqual(sidecar["schema"], "p030.health_sidecar/v1")
            self.assertEqual(sidecar["observed_at_utc"], "2026-09-12T00:02:00Z")
            self.assertEqual(
                sidecar["market_freshness"],
                {
                    "availability": "available",
                    "last_accepted_timestamp_utc": "2026-09-12T00:00:00Z",
                    "age_seconds": 120,
                },
            )
            self.assertIsNone(sidecar["reconciliation_progress"])
            self.assertNotIn(
                "market_freshness",
                subject.verify_process_heartbeat(heartbeat_path, expected_id=self.ID),
            )

    def test_health_sidecar_declares_unavailable_and_rejects_fabricated_reconciliation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            state_dir = Path(temporary) / "state"
            path = subject.write_health_sidecar(
                state_dir,
                self.ID,
                observed_at_utc="2026-09-12T00:02:00Z",
                last_accepted_timestamp_utc=None,
                reconciliation_progress=None,
            )
            sidecar = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(
                sidecar["market_freshness"],
                {
                    "availability": "unavailable",
                    "last_accepted_timestamp_utc": None,
                    "age_seconds": None,
                },
            )
            with self.assertRaisesRegex(ValueError, "reconciliation_progress must remain null"):
                subject.write_health_sidecar(
                    state_dir,
                    self.ID,
                    observed_at_utc="2026-09-12T00:03:00Z",
                    last_accepted_timestamp_utc=None,
                    reconciliation_progress={"completed": "fabricated"},
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
