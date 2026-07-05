import sys
import unittest
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))


class TestVerticalSliceConstants(unittest.TestCase):
    def test_route_constants_are_locked_to_system_test_only(self):
        from vertical_slice import constants

        self.assertEqual(
            constants.BANNER,
            "SYSTEM_TEST_ONLY / NOT STRATEGY_APPROVED / NO REAL MONEY",
        )
        self.assertEqual(constants.CANDIDATE_ID, "QL_ALPHA_LINK_8EMA_1H")
        self.assertEqual(
            constants.ENGINE_STRATEGY_ID,
            "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL",
        )
        self.assertEqual(constants.SYMBOL, "LINKUSDT")
        self.assertEqual(constants.TIMEFRAME, "1h")
        self.assertEqual(constants.ALLOWED_ENVIRONMENTS, ("paper",))
        for label in ("live", "testnet", "broker", "TradingView", "WunderTrading"):
            self.assertIn(label, constants.FORBIDDEN_LABELS)

    def test_constants_do_not_embed_default_auth_token(self):
        from vertical_slice import constants

        names = {name.lower() for name in dir(constants)}
        self.assertNotIn("auth_token", names)
        self.assertNotIn("default_auth_token", names)


class TestVerticalSliceContracts(unittest.TestCase):
    def make_entry_payload(self, **overrides):
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

    def test_complete_entry_payload_validates(self):
        from vertical_slice import contracts

        payload = self.make_entry_payload()
        result = contracts.validate_signal_payload(payload, expected_auth_token="synthetic-token")

        self.assertTrue(result.ok, result.errors)

    def test_live_and_testnet_are_rejected(self):
        from vertical_slice import contracts

        for environment in ("live", "testnet"):
            payload = self.make_entry_payload(environment=environment)
            result = contracts.validate_signal_payload(
                payload, expected_auth_token="synthetic-token"
            )
            self.assertFalse(result.ok)
            self.assertTrue(any(environment in error for error in result.errors))

    def test_missing_idempotency_key_is_rejected(self):
        from vertical_slice import contracts

        payload = self.make_entry_payload()
        del payload["idempotency_key"]

        result = contracts.validate_signal_payload(payload, expected_auth_token="synthetic-token")

        self.assertFalse(result.ok)
        self.assertTrue(any("idempotency_key" in error for error in result.errors))

    def test_malformed_checksum_is_rejected(self):
        from vertical_slice import contracts

        payload = self.make_entry_payload()
        payload["checksum"] = "not-a-sha256"

        result = contracts.validate_signal_payload(payload, expected_auth_token="synthetic-token")

        self.assertFalse(result.ok)
        self.assertTrue(any("checksum" in error for error in result.errors))

    def test_unrecognized_extra_field_is_rejected(self):
        from vertical_slice import contracts

        payload = self.make_entry_payload(unrecognized_field="nope")

        result = contracts.validate_signal_payload(payload, expected_auth_token="synthetic-token")

        self.assertFalse(result.ok)
        self.assertTrue(any("unrecognized" in error for error in result.errors))

    def test_auth_token_is_required_and_redacted(self):
        from vertical_slice import contracts

        payload = self.make_entry_payload()
        payload_without_token = dict(payload)
        del payload_without_token["auth_token"]

        result = contracts.validate_signal_payload(
            payload_without_token, expected_auth_token="synthetic-token"
        )
        redacted = contracts.redact_sensitive_fields(payload)

        self.assertFalse(result.ok)
        self.assertEqual(redacted["auth_token"], "<REDACTED>")

    def test_timestamp_variants_canonicalize_and_share_signal_id(self):
        from vertical_slice import contracts
        from vertical_slice.constants import CANDIDATE_ID, SYMBOL, TIMEFRAME

        ids = {
            contracts.make_signal_id(
                CANDIDATE_ID,
                SYMBOL,
                TIMEFRAME,
                value,
                "ENTRY",
            )
            for value in (
                "2026-05-01T09:00:00+0000",
                "2026-05-01T09:00:00+00:00",
                "2026-05-01T09:00:00Z",
            )
        }

        self.assertEqual(len(ids), 1)
        self.assertEqual(
            contracts.canonicalize_timestamp("2026-05-01T09:00:00+0000"),
            "2026-05-01T09:00:00Z",
        )

    def test_entry_and_exit_intents_are_action_specific(self):
        from vertical_slice import contracts

        bad_entry = self.make_entry_payload(current_position_intent="LONG_TO_FLAT")
        bad_exit = self.make_entry_payload(
            action="EXIT",
            current_position_intent="FLAT_TO_LONG",
            entry_price=None,
            stop_loss=None,
            exit_price=10.8,
            exit_reason="trail",
        )

        self.assertFalse(
            contracts.validate_signal_payload(
                bad_entry, expected_auth_token="synthetic-token"
            ).ok
        )
        self.assertFalse(
            contracts.validate_signal_payload(
                bad_exit, expected_auth_token="synthetic-token"
            ).ok
        )

    def test_semantic_sanity_rejects_impossible_prices(self):
        from vertical_slice import contracts

        negative = self.make_entry_payload(entry_price=-1.0)
        stop_above_entry = self.make_entry_payload(entry_price=10.0, stop_loss=10.0)

        self.assertFalse(
            contracts.validate_signal_payload(
                negative, expected_auth_token="synthetic-token"
            ).ok
        )
        self.assertFalse(
            contracts.validate_signal_payload(
                stop_above_entry, expected_auth_token="synthetic-token"
            ).ok
        )


if __name__ == "__main__":
    unittest.main()
