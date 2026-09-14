from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import pytest
from eth_account import Account
from eth_account.messages import encode_defunct

from tools import capture_own_account_evidence as cae

ADDRESS = "0x1111111111111111111111111111111111111111"
START = "2026-09-12T11:00:00Z"
END = "2026-09-12T12:00:00Z"


def fill_row(**overrides):
    row = {
        "coin": "BTC",
        "fee": "0.01",
        "feeToken": "USDC",
        "time": 1799742000000,
        "tid": 123,
        "hash": "0xfill",
        "oid": 456,
        "closedPnl": "0.00",
        "crossed": True,
        "side": "B",
        "px": "60000",
        "sz": "0.001",
    }
    row.update(overrides)
    return row


def funding_row(**overrides):
    row = {
        "hash": "0xfund",
        "time": 1799742000000,
        "delta": {
            "coin": "BTC",
            "usdc": "-0.12",
            "fundingRate": "0.00001",
            "szi": "0.01",
        },
    }
    row.update(overrides)
    return row


class FakeInfo:
    def __init__(self, *, fills=None, funding=None, state=None, raise_on=""):
        self.fills = list(fills or [[fill_row()], [fill_row()]])
        self.funding = list(funding or [[funding_row()], [funding_row()]])
        self.state = state if state is not None else {"assetPositions": []}
        self.raise_on = raise_on
        self.fill_calls = 0
        self.funding_calls = 0

    def user_fills_by_time(self, address, start_ms, end_ms):
        if self.raise_on == "fills":
            raise RuntimeError("boom")
        row = self.fills[min(self.fill_calls, len(self.fills) - 1)]
        self.fill_calls += 1
        return row

    def user_funding_history(self, address, start_ms, end_ms):
        if self.raise_on == "funding":
            raise RuntimeError("boom")
        row = self.funding[min(self.funding_calls, len(self.funding) - 1)]
        self.funding_calls += 1
        return row

    def user_state(self, address):
        if self.raise_on == "state":
            raise RuntimeError("boom")
        return self.state


def args(tmp_path, **overrides):
    values = {
        "network": "testnet",
        "address": ADDRESS,
        "coin": "BTC",
        "start": START,
        "end": END,
        "out": tmp_path,
        "ownership_signature": None,
        "run_id": "run-1",
    }
    values.update(overrides)
    return argparse.Namespace(**values)


def patch_info(monkeypatch, fake, *, mainnet="https://mainnet", testnet="https://testnet"):
    monkeypatch.delenv("HL_API_WALLET_KEY", raising=False)
    monkeypatch.setattr(cae, "make_info", lambda base_url: fake)
    monkeypatch.setattr(cae.constants, "MAINNET_API_URL", mainnet)
    monkeypatch.setattr(cae.constants, "TESTNET_API_URL", testnet)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_capture_writes_manifest_sidecars_extraction_and_requery_identities(tmp_path, monkeypatch):
    fake = FakeInfo()
    patch_info(monkeypatch, fake)

    manifest = cae.run_capture(args(tmp_path))

    assert manifest["ownership_evidence"]["status"] == "OWNERSHIP_EVIDENCE: NOT_PROVIDED"
    assert {entry["base_url"] for entry in manifest["responses"]} == {"https://testnet"}
    assert len(manifest["responses"]) == 5
    for entry in manifest["responses"]:
        body = (tmp_path / entry["file"]).read_bytes()
        assert cae.sha256_bytes(body) == entry["response_sha256"]
        assert (tmp_path / (entry["file"] + ".sha256")).read_text(encoding="utf-8").strip() == entry["response_sha256"]
    derived = read_json(tmp_path / "DERIVED_EXTRACTION.json")
    assert derived["label"] == "DERIVED_VIEW_NOT_ORIGINAL_BYTES"
    assert derived["fills"][0]["fee"] == "0.01"
    assert derived["fills"][0]["capture_sha256"]
    assert derived["funding"][0]["usdc"] == "-0.12"
    cae.verify_sidecars(tmp_path)


def test_truncated_full_page_refuses(tmp_path, monkeypatch):
    monkeypatch.setattr(cae, "HL_FILLS_PAGE_LIMIT", 1)
    fake = FakeInfo(fills=[[fill_row(time=cae.ms(cae.parse_utc(START)))]])
    patch_info(monkeypatch, fake)

    with pytest.raises(cae.CaptureRefused) as exc:
        cae.run_capture(args(tmp_path))

    assert exc.value.code == cae.REFUSED_TRUNCATED


def test_requery_identity_mismatch_refuses(tmp_path, monkeypatch):
    fake = FakeInfo(fills=[[fill_row(tid=1)], [fill_row(tid=2)]])
    patch_info(monkeypatch, fake)

    with pytest.raises(cae.CaptureRefused) as exc:
        cae.run_capture(args(tmp_path))

    assert exc.value.code == cae.REFUSED_REQUERY_MISMATCH


def test_tampered_stored_bytes_vs_sidecar_refuses(tmp_path, monkeypatch):
    fake = FakeInfo()
    patch_info(monkeypatch, fake)
    cae.run_capture(args(tmp_path))
    (tmp_path / "fills_pass1_page001.json").write_text("tampered\n", encoding="utf-8")

    with pytest.raises(cae.CaptureRefused) as exc:
        cae.verify_sidecars(tmp_path)

    assert exc.value.code == cae.REFUSED_BAD_SIDECAR


def test_sdk_exception_refuses_query_failed(tmp_path, monkeypatch):
    fake = FakeInfo(raise_on="fills")
    patch_info(monkeypatch, fake)

    with pytest.raises(cae.CaptureRefused) as exc:
        cae.run_capture(args(tmp_path))

    assert exc.value.code == cae.REFUSED_QUERY_FAILED


def test_malformed_address_refuses_before_sdk(tmp_path, monkeypatch):
    fake = FakeInfo()
    patch_info(monkeypatch, fake)

    with pytest.raises(cae.CaptureRefused) as exc:
        cae.run_capture(args(tmp_path, address="not-an-address"))

    assert exc.value.code == cae.REFUSED_BAD_ADDRESS
    assert fake.fill_calls == 0


def test_wallet_key_environment_refuses_before_sdk(tmp_path, monkeypatch):
    fake = FakeInfo()
    patch_info(monkeypatch, fake)
    monkeypatch.setenv("HL_API_WALLET_KEY", "secret")

    with pytest.raises(cae.CaptureRefused) as exc:
        cae.run_capture(args(tmp_path))

    assert exc.value.code == cae.REFUSED_KEY_PRESENT
    assert fake.fill_calls == 0


def test_requested_network_records_matching_sdk_constant(tmp_path, monkeypatch):
    fake = FakeInfo()
    patch_info(monkeypatch, fake, mainnet="https://mainnet.example", testnet="https://testnet.example")

    manifest = cae.run_capture(args(tmp_path, network="mainnet"))

    assert {entry["base_url"] for entry in manifest["responses"]} == {"https://mainnet.example"}


def test_ownership_signature_verifies_recovered_address(tmp_path, monkeypatch):
    account = Account.create()
    address = account.address
    message = cae.ownership_message(address, "run-1")
    signature = Account.sign_message(encode_defunct(text=message), account.key).signature.hex()
    signature_path = tmp_path / "sig.txt"
    signature_path.write_text(signature, encoding="utf-8")
    fake = FakeInfo()
    patch_info(monkeypatch, fake)

    manifest = cae.run_capture(args(tmp_path / "capture", address=address, ownership_signature=signature_path))

    assert manifest["ownership_evidence"]["status"] == "OWNERSHIP_EVIDENCE: VERIFIED"
    assert manifest["ownership_evidence"]["recovered_address"].lower() == address.lower()


def test_tool_imports_no_write_capable_exchange_client():
    source = Path(cae.__file__).read_text(encoding="utf-8")

    assert "hyperliquid.exchange" not in source
    assert "Exchange" not in source
