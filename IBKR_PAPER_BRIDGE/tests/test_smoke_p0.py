from __future__ import annotations

import asyncio

import pytest

from bridge.broker.hyperliquid import HyperliquidOrderError
from bridge.engine.types import BrokerOrder
from tools.smoke_p0 import _deterministic_cleanup, _failure_data, _validate_credentials


def test_validate_credentials_accepts_expected_formats(monkeypatch):
    monkeypatch.setenv("HL_API_WALLET_KEY", "0x" + "ab" * 32)
    monkeypatch.setenv("HL_ACCOUNT_ADDRESS", "0x" + "cd" * 20)

    _validate_credentials()


@pytest.mark.parametrize(
    "key",
    ["", "0x" + "ab" * 20, "0x" + "zz" * 32],
)
def test_validate_credentials_rejects_invalid_key_without_exposing_it(monkeypatch, key):
    monkeypatch.setenv("HL_API_WALLET_KEY", key)
    monkeypatch.setenv("HL_ACCOUNT_ADDRESS", "0x" + "cd" * 20)

    with pytest.raises(RuntimeError, match="must be a 32-byte hexadecimal private key") as exc_info:
        _validate_credentials()

    assert not key or key not in str(exc_info.value)


@pytest.mark.parametrize(
    "account",
    ["", "0x" + "ab" * 19, "0x" + "zz" * 20, "ab" * 20],
)
def test_validate_credentials_rejects_invalid_account_without_exposing_it(monkeypatch, account):
    monkeypatch.setenv("HL_API_WALLET_KEY", "0x" + "ab" * 32)
    monkeypatch.setenv("HL_ACCOUNT_ADDRESS", account)

    with pytest.raises(RuntimeError, match="must be a 20-byte 0x-prefixed hexadecimal address") as exc_info:
        _validate_credentials()

    assert not account or account not in str(exc_info.value)


def test_failure_data_preserves_redacted_raw_exchange_response():
    secret_like = "ab" * 32
    payload = _failure_data(
        HyperliquidOrderError(f"unexpected status; raw_response={{'wallet': '{secret_like}'}}")
    )

    assert secret_like not in str(payload)
    assert "[redacted]" in payload["raw_response"]
    assert "raw_response" in payload


def test_deterministic_cleanup_cancels_owned_resting_order_after_mid_parse_failure():
    owned_cloid = "0x" + "1" * 32
    foreign_cloid = "0x" + "2" * 32

    class FakeBroker:
        connected = True

        def __init__(self):
            self.orders = [
                BrokerOrder(cloid=owned_cloid, coin="BTC", side="BUY", size=0.0002),
                BrokerOrder(cloid=foreign_cloid, coin="BTC", side="BUY", size=0.0002),
            ]
            self.cancelled: list[str] = []
            self.flattened: list[str] = []

        async def open_orders(self):
            return list(self.orders)

        async def cancel(self, cloid):
            self.cancelled.append(cloid)
            self.orders = [order for order in self.orders if order.cloid != cloid]

        async def positions(self):
            return []

        async def flatten(self, coin):
            self.flattened.append(coin)

    broker = FakeBroker()
    log = {"steps": []}

    asyncio.run(_deterministic_cleanup(broker, [owned_cloid], {}, log))

    assert broker.cancelled == [owned_cloid]
    assert [order.cloid for order in broker.orders] == [foreign_cloid]
    assert broker.flattened == []
    assert log["steps"][-1]["name"] == "deterministic_cleanup"
    assert log["steps"][-1]["status"] == "PASS"
