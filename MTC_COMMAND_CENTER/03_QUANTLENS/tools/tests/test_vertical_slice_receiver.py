import sys
import unittest
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))


def signed_payload(**overrides):
    from vertical_slice import contracts
    from vertical_slice.constants import CANDIDATE_ID, ENGINE_STRATEGY_ID, SYMBOL, TIMEFRAME

    payload = {
        "schema": "mtc.signal/v1",
        "strategy_id": CANDIDATE_ID,
        "strategy_version": "system-test-v1",
        "candidate_id": CANDIDATE_ID,
        "engine_strategy_id": ENGINE_STRATEGY_ID,
        "environment": "paper",
        "symbol": SYMBOL,
        "exchange": "BINANCE",
        "timeframe": TIMEFRAME,
        "timestamp_utc": "2026-05-01T10:00:00Z",
        "bar_time_utc": "2026-05-01T09:00:00Z",
        "side": "LONG",
        "action": "ENTRY",
        "qty_model": "none",
        "risk_ref": "system_test_replay",
        "stop_loss": 9.5,
        "take_profit": None,
        "current_position_intent": "FLAT_TO_LONG",
        "entry_price": 10.5,
    }
    payload.update(overrides)
    return contracts.sign_payload(payload, auth_token="synthetic-token")


class TestLocalReceiver(unittest.TestCase):
    def test_valid_payload_is_accepted_and_filled(self):
        from vertical_slice.local_receiver import LocalReceiver, ReceiverState

        receiver = LocalReceiver(ReceiverState(expected_auth_token="synthetic-token"))
        row = receiver.process(signed_payload())

        self.assertEqual(row["disposition"], "accepted")
        self.assertEqual(len(receiver.state.received_rows), 1)
        self.assertEqual(len(receiver.state.fills), 1)
        self.assertTrue(receiver.state.fills[0]["simulated"])
        self.assertIsNotNone(receiver.state.position)

    def test_duplicate_idempotency_key_is_dropped_without_fill(self):
        from vertical_slice.local_receiver import LocalReceiver, ReceiverState

        receiver = LocalReceiver(ReceiverState(expected_auth_token="synthetic-token"))
        payload = signed_payload()

        receiver.process(payload)
        row = receiver.process(payload)

        self.assertEqual(row["disposition"], "duplicate_dropped")
        self.assertEqual(len(receiver.state.fills), 1)

    def test_wrong_auth_and_wrong_checksum_are_rejected(self):
        from vertical_slice.local_receiver import LocalReceiver, ReceiverState

        receiver = LocalReceiver(ReceiverState(expected_auth_token="other-token"))
        self.assertIn("auth_token", receiver.process(signed_payload())["reason"])

        receiver = LocalReceiver(ReceiverState(expected_auth_token="synthetic-token"))
        payload = signed_payload()
        payload["checksum"] = "0" * 64
        row = receiver.process(payload)

        self.assertEqual(row["disposition"], "rejected(checksum)")
        self.assertEqual(len(receiver.state.fills), 0)

    def test_live_environment_is_rejected_loudly(self):
        from vertical_slice.local_receiver import LocalReceiver, ReceiverState

        receiver = LocalReceiver(ReceiverState(expected_auth_token="synthetic-token"))
        row = receiver.process(signed_payload(environment="live"))

        self.assertEqual(row["disposition"], "rejected(environment)")
        self.assertIn("live", row["reason"])
        self.assertEqual(len(receiver.state.fills), 0)

    def test_exit_while_flat_is_rejected(self):
        from vertical_slice.local_receiver import LocalReceiver, ReceiverState

        receiver = LocalReceiver(ReceiverState(expected_auth_token="synthetic-token"))
        exit_payload = signed_payload(
            action="EXIT",
            current_position_intent="LONG_TO_FLAT",
            entry_price=None,
            stop_loss=None,
            exit_price=11.2,
            exit_reason="trail",
            timestamp_utc="2026-05-01T14:00:00Z",
            bar_time_utc="2026-05-01T14:00:00Z",
        )
        row = receiver.process(exit_payload)

        self.assertEqual(row["disposition"], "rejected(exit_with_no_position)")
        self.assertEqual(len(receiver.state.fills), 0)

    def test_entry_while_open_is_rejected(self):
        from vertical_slice.local_receiver import LocalReceiver, ReceiverState

        receiver = LocalReceiver(ReceiverState(expected_auth_token="synthetic-token"))
        receiver.process(signed_payload())
        second_entry = signed_payload(
            timestamp_utc="2026-05-01T11:00:00Z",
            bar_time_utc="2026-05-01T10:00:00Z",
            entry_price=11.0,
            stop_loss=10.0,
        )

        row = receiver.process(second_entry)

        self.assertEqual(row["disposition"], "rejected(entry_while_open)")
        self.assertEqual(len(receiver.state.fills), 1)

    def test_accepted_exit_closes_position_and_fills_once(self):
        from vertical_slice.local_receiver import LocalReceiver, ReceiverState

        receiver = LocalReceiver(ReceiverState(expected_auth_token="synthetic-token"))
        receiver.process(signed_payload())
        exit_payload = signed_payload(
            action="EXIT",
            current_position_intent="LONG_TO_FLAT",
            entry_price=None,
            stop_loss=None,
            exit_price=11.2,
            exit_reason="trail",
            timestamp_utc="2026-05-01T14:00:00Z",
            bar_time_utc="2026-05-01T14:00:00Z",
        )

        row = receiver.process(exit_payload)

        self.assertEqual(row["disposition"], "accepted")
        self.assertIsNone(receiver.state.position)
        self.assertEqual(len(receiver.state.fills), 2)
        self.assertTrue(receiver.state.fills[-1]["simulated"])


if __name__ == "__main__":
    unittest.main()
