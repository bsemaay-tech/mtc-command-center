import json
import sys
import tempfile
import unittest
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))


class TestReconciler(unittest.TestCase):
    def test_matching_ledgers_have_zero_unexplained_orphans(self):
        from vertical_slice.reconciler import reconcile_ledgers

        summary = reconcile_ledgers(
            expected_signals=[{"signal_id": "s1"}, {"signal_id": "s2"}],
            received_rows=[
                {"signal_id": "s1", "disposition": "accepted"},
                {"signal_id": "s2", "disposition": "accepted"},
            ],
            fills=[{"signal_id": "s1"}, {"signal_id": "s2"}],
        )

        self.assertEqual(summary["status"], "OK")
        self.assertEqual(summary["unexplained_count"], 0)

    def test_missing_received_row_is_reported(self):
        from vertical_slice.reconciler import reconcile_ledgers

        summary = reconcile_ledgers(
            expected_signals=[{"signal_id": "s1"}, {"signal_id": "s2"}],
            received_rows=[{"signal_id": "s1", "disposition": "accepted"}],
            fills=[{"signal_id": "s1"}],
        )

        self.assertEqual(summary["status"], "HALT")
        self.assertEqual(summary["expected_not_received"], ["s2"])

    def test_accepted_received_without_fill_is_reported(self):
        from vertical_slice.reconciler import reconcile_ledgers

        summary = reconcile_ledgers(
            expected_signals=[{"signal_id": "s1"}],
            received_rows=[{"signal_id": "s1", "disposition": "accepted"}],
            fills=[],
        )

        self.assertEqual(summary["status"], "HALT")
        self.assertEqual(summary["received_not_filled"], ["s1"])

    def test_unknown_received_row_is_reported(self):
        from vertical_slice.reconciler import reconcile_ledgers

        summary = reconcile_ledgers(
            expected_signals=[{"signal_id": "s1"}],
            received_rows=[
                {"signal_id": "s1", "disposition": "accepted"},
                {"signal_id": "s2", "disposition": "accepted"},
            ],
            fills=[{"signal_id": "s1"}, {"signal_id": "s2"}],
        )

        self.assertEqual(summary["status"], "HALT")
        self.assertEqual(summary["received_not_expected"], ["s2"])

    def test_rejected_unknown_received_row_is_explained_not_unexplained(self):
        from vertical_slice.reconciler import reconcile_ledgers

        summary = reconcile_ledgers(
            expected_signals=[{"signal_id": "s1"}],
            received_rows=[
                {"signal_id": "s1", "disposition": "accepted"},
                {"signal_id": "suppressed-signal", "disposition": "rejected(entry_while_open)"},
            ],
            fills=[{"signal_id": "s1"}],
        )

        self.assertEqual(summary["status"], "OK")
        self.assertEqual(summary["received_not_expected"], [])
        self.assertEqual(summary["explained_rejections"], 1)
        self.assertEqual(summary["unexplained_count"], 0)

    def test_accepted_unknown_received_row_still_halts(self):
        from vertical_slice.reconciler import reconcile_ledgers

        summary = reconcile_ledgers(
            expected_signals=[{"signal_id": "s1"}],
            received_rows=[
                {"signal_id": "s1", "disposition": "accepted"},
                {"signal_id": "unexpected-accepted", "disposition": "accepted"},
            ],
            fills=[{"signal_id": "s1"}, {"signal_id": "unexpected-accepted"}],
        )

        self.assertEqual(summary["status"], "HALT")
        self.assertEqual(summary["received_not_expected"], ["unexpected-accepted"])

    def test_report_writer_includes_banner(self):
        from vertical_slice.constants import BANNER
        from vertical_slice.reconciler import write_reconciliation_report

        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)
            summary = {
                "status": "OK",
                "unexplained_count": 0,
                "explained_rejections": 1,
            }
            report_path = write_reconciliation_report(run_dir, summary)
            text = report_path.read_text(encoding="utf-8")

        self.assertIn(BANNER, text)
        self.assertIn("Explained rejections: 1", text)


class TestFailureDrills(unittest.TestCase):
    def signed_payload(self, **overrides):
        from test_vertical_slice_receiver import signed_payload

        return signed_payload(**overrides)

    def test_d1_duplicate_signal_is_dropped(self):
        from vertical_slice.local_receiver import LocalReceiver, ReceiverState

        receiver = LocalReceiver(ReceiverState(expected_auth_token="synthetic-token"))
        payload = self.signed_payload()

        receiver.process(payload)
        duplicate = receiver.process(payload)

        self.assertEqual(duplicate["disposition"], "duplicate_dropped")
        self.assertEqual(len(receiver.state.fills), 1)

    def test_d2_dropped_signal_halts_reconciliation(self):
        from vertical_slice.reconciler import reconcile_ledgers

        summary = reconcile_ledgers(
            expected_signals=[{"signal_id": "s1"}, {"signal_id": "s2"}],
            received_rows=[{"signal_id": "s1", "disposition": "accepted"}],
            fills=[{"signal_id": "s1"}],
        )

        self.assertEqual(summary["status"], "HALT")
        self.assertEqual(summary["expected_not_received"], ["s2"])

    def test_d3_exit_with_no_position_is_explained_rejection(self):
        from vertical_slice.local_receiver import LocalReceiver, ReceiverState

        receiver = LocalReceiver(ReceiverState(expected_auth_token="synthetic-token"))
        row = receiver.process(
            self.signed_payload(
                action="EXIT",
                current_position_intent="LONG_TO_FLAT",
                entry_price=None,
                stop_loss=None,
                exit_price=10.2,
                exit_reason="trail",
                timestamp_utc="2026-05-01T14:00:00Z",
                bar_time_utc="2026-05-01T14:00:00Z",
            )
        )

        self.assertEqual(row["disposition"], "rejected(exit_with_no_position)")
        self.assertEqual(len(receiver.state.fills), 0)

    def test_d4_wrong_environment_is_rejected(self):
        from vertical_slice.local_receiver import LocalReceiver, ReceiverState

        receiver = LocalReceiver(ReceiverState(expected_auth_token="synthetic-token"))
        row = receiver.process(self.signed_payload(environment="live"))

        self.assertEqual(row["disposition"], "rejected(environment)")

    def test_d5_malformed_payload_is_rejected(self):
        from vertical_slice.local_receiver import LocalReceiver, ReceiverState

        receiver = LocalReceiver(ReceiverState(expected_auth_token="synthetic-token"))
        payload = self.signed_payload()
        payload["checksum"] = "broken"

        row = receiver.process(payload)

        self.assertEqual(row["disposition"], "rejected(checksum)")
        self.assertEqual(len(receiver.state.fills), 0)

    def test_d8_out_of_order_exit_before_entry(self):
        from vertical_slice.local_receiver import LocalReceiver, ReceiverState

        receiver = LocalReceiver(ReceiverState(expected_auth_token="synthetic-token"))
        exit_payload = self.signed_payload(
            action="EXIT",
            current_position_intent="LONG_TO_FLAT",
            entry_price=None,
            stop_loss=None,
            exit_price=10.2,
            exit_reason="trail",
            timestamp_utc="2026-05-01T14:00:00Z",
            bar_time_utc="2026-05-01T14:00:00Z",
        )

        row = receiver.process(exit_payload)

        self.assertEqual(row["disposition"], "rejected(exit_with_no_position)")

    def test_d9_suppressed_signal_candidate_entry_while_open(self):
        from vertical_slice.local_receiver import LocalReceiver, ReceiverState

        suppressed_signal_candidate = {
            "timestamp_utc": "2026-05-01T11:00:00Z",
            "open": "10",
            "high": "11",
            "low": "9",
            "close": "10.8",
            "atr14": "1",
            "ema8": "10",
            "long_entry": "1",
            "stop_at_signal": "9.8",
        }
        receiver = LocalReceiver(ReceiverState(expected_auth_token="synthetic-token"))
        receiver.process(self.signed_payload())

        row = receiver.process(
            self.signed_payload(
                timestamp_utc=suppressed_signal_candidate["timestamp_utc"],
                bar_time_utc=suppressed_signal_candidate["timestamp_utc"],
                entry_price=float(suppressed_signal_candidate["close"]),
                stop_loss=float(suppressed_signal_candidate["stop_at_signal"]),
            )
        )

        self.assertEqual(row["disposition"], "rejected(entry_while_open)")

    def test_d10_semantic_sanity_rejects_impossible_payloads(self):
        from vertical_slice.local_receiver import LocalReceiver, ReceiverState

        receiver = LocalReceiver(ReceiverState(expected_auth_token="synthetic-token"))
        negative = receiver.process(self.signed_payload(entry_price=-1))
        stop_above_entry = receiver.process(self.signed_payload(entry_price=10, stop_loss=10))

        self.assertEqual(negative["disposition"], "rejected(semantic)")
        self.assertEqual(stop_above_entry["disposition"], "rejected(semantic)")


if __name__ == "__main__":
    unittest.main()
