from __future__ import annotations

import pytest

from tools.smoke_p0 import _validate_credentials


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
