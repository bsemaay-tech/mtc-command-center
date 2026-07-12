from __future__ import annotations

import asyncio

import pytest

from bridge.broker.hyperliquid import HyperliquidOrderError
from bridge.engine.types import BrokerOrder
from bridge.settings import resolve_hyperliquid_credentials
from tools.smoke_p0 import (
    _deterministic_cleanup,
    _failure_data,
    _is_type_or_grouping_rejection,
    _validate_credentials,
)


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


# -----------------------------------------------------------------------
# monkeypatched-winreg tests for resolve_hyperliquid_credentials
# -----------------------------------------------------------------------

# Build fixture strings via repetition – never literal 64-hex.
_FIXTURE_KEY = "0x" + "ab" * 32
_FIXTURE_ACCOUNT = "0x" + "cd" * 20
_INVALID_KEY = "0x" + "zz" * 32
_INVALID_ACCOUNT = "0x" + "zz" * 20


class _FakeRegKey:
    """Minimal fake for :func:`winreg.OpenKey` context manager."""

    def __init__(self, values: dict[str, str]) -> None:
        self._values = values

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


def _fake_query_value_ex(key, name):
    """Drop-in replacement for :func:`winreg.QueryValueEx` that works with
    :class:`_FakeRegKey` instances."""
    return key._values[name], 1


def _patch_winreg_in_settings(monkeypatch, reg_values: dict[str, str]):
    """Monkeypatch the ``winreg`` reference **inside** :mod:`bridge.settings`
    so ``resolve_hyperliquid_credentials`` uses the fakes."""
    import bridge.settings as _s

    # Replace the entire winreg reference with a lightweight namespace whose
    # OpenKey returns our fake and whose QueryValueEx delegates to the fake.
    class _FakeWinreg:
        HKEY_CURRENT_USER = 0

        @staticmethod
        def OpenKey(hkey, subkey):
            assert subkey == "Environment"
            return _FakeRegKey(reg_values)

        @staticmethod
        def QueryValueEx(key, name):
            return _fake_query_value_ex(key, name)

    monkeypatch.setattr(_s, "winreg", _FakeWinreg, raising=True)
    monkeypatch.setattr(_s, "_HAS_WINREG", True, raising=True)


# --- absent process env → uses registry ----------------------------------


def test_resolver_absent_env_uses_registry(monkeypatch):
    monkeypatch.delenv("HL_ACCOUNT_ADDRESS", raising=False)
    monkeypatch.delenv("HL_API_WALLET_KEY", raising=False)

    _patch_winreg_in_settings(
        monkeypatch,
        {"HL_ACCOUNT_ADDRESS": _FIXTURE_ACCOUNT, "HL_API_WALLET_KEY": _FIXTURE_KEY},
    )

    account, key, source = resolve_hyperliquid_credentials()
    assert source == "user_registry"
    assert account == _FIXTURE_ACCOUNT
    assert key == _FIXTURE_KEY


# --- invalid process env + valid registry → wins --------------------------


def test_resolver_invalid_env_valid_registry_wins(monkeypatch):
    monkeypatch.setenv("HL_ACCOUNT_ADDRESS", _INVALID_ACCOUNT)
    monkeypatch.setenv("HL_API_WALLET_KEY", _INVALID_KEY)

    _patch_winreg_in_settings(
        monkeypatch,
        {"HL_ACCOUNT_ADDRESS": _FIXTURE_ACCOUNT, "HL_API_WALLET_KEY": _FIXTURE_KEY},
    )

    account, key, source = resolve_hyperliquid_credentials()
    assert source == "user_registry"
    assert account == _FIXTURE_ACCOUNT
    assert key == _FIXTURE_KEY


# --- invalid both → raises; fixture values do NOT appear in exception -----


def test_resolver_invalid_both_raises_without_exposing_values(monkeypatch):
    monkeypatch.delenv("HL_ACCOUNT_ADDRESS", raising=False)
    monkeypatch.delenv("HL_API_WALLET_KEY", raising=False)

    _patch_winreg_in_settings(
        monkeypatch,
        {"HL_ACCOUNT_ADDRESS": _INVALID_ACCOUNT, "HL_API_WALLET_KEY": _INVALID_KEY},
    )

    with pytest.raises(RuntimeError) as exc_info:
        resolve_hyperliquid_credentials()

    msg = str(exc_info.value)
    assert _FIXTURE_KEY not in msg
    assert _FIXTURE_ACCOUNT not in msg
    assert _INVALID_KEY not in msg
    assert _INVALID_ACCOUNT not in msg


# --- original tests below preserved exactly -------------------------------


def test_failure_data_preserves_redacted_raw_exchange_response():
    secret_like = "ab" * 32
    payload = _failure_data(
        HyperliquidOrderError(f"unexpected status; raw_response={{'wallet': '{secret_like}'}}")
    )

    assert secret_like not in str(payload)
    assert "[redacted]" in payload["raw_response"]
    assert "raw_response" in payload


def test_g2_type_or_grouping_classifier_rejects_only_concrete_exchange_errors():
    assert _is_type_or_grouping_rejection(
        HyperliquidOrderError("Trigger order has unexpected type.")
    )
    assert _is_type_or_grouping_rejection(HyperliquidOrderError("Invalid grouping normalTpsl"))
    assert _is_type_or_grouping_rejection(
        HyperliquidOrderError("Order type not supported for this grouping")
    )
    # C2 payloads carry response.type=order; that alone must never unlock a
    # second placement call for an unrelated rejection.
    assert not _is_type_or_grouping_rejection(
        HyperliquidOrderError('Insufficient margin; raw_response={"response":{"type":"order"}}')
    )


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
