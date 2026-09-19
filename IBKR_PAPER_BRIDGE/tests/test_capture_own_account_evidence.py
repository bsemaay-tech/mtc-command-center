from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest
from eth_account import Account
from eth_account.messages import encode_defunct

from tools import capture_own_account_evidence as cae

ADDRESS = "0x1111111111111111111111111111111111111111"
START = "2026-09-12T11:00:00Z"
END = "2026-09-12T12:00:00Z"
START_MS = 1789210800000
END_MS = 1789214400000
INSIDE_MS = 1789212000000  # 11:20:00Z, inside [START, END)


def fill_row(**overrides):
    row = {
        "coin": "BTC",
        "fee": "0.01",
        "feeToken": "USDC",
        "time": INSIDE_MS,
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
        "time": INSIDE_MS,
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
    """Test double without ``pop_capture``: the tool labels its bytes as re-serialised."""

    def __init__(self, *, fills=None, funding=None, state=None, raise_on=""):
        self.fills = list(fills or [[fill_row()], [fill_row()]])
        self.funding = list(funding or [[funding_row()], [funding_row()]])
        self.state = state if state is not None else {"assetPositions": []}
        self.raise_on = raise_on
        self.fill_calls = 0
        self.funding_calls = 0
        self.fill_windows = []

    def user_fills_by_time(self, address, start_ms, end_ms):
        if self.raise_on == "fills":
            raise RuntimeError("boom")
        self.fill_windows.append((start_ms, end_ms))
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


class FakeResponse:
    def __init__(self, content: bytes, status_code: int = 200):
        self.content = content
        self.status_code = status_code
        self.text = content.decode("utf-8")
        self.headers = {}


class FakeSession:
    """Stands in for ``requests.Session`` under ``CapturingInfo.post``."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def post(self, url, json=None, timeout=None):
        self.calls.append({"url": url, "json": json, "timeout": timeout})
        return self.responses.pop(0)


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


def patch_info(
    monkeypatch, fake, *, mainnet="https://mainnet", testnet="https://testnet"
):
    monkeypatch.delenv("HL_API_WALLET_KEY", raising=False)
    monkeypatch.setattr(cae, "make_info", lambda base_url: fake)
    monkeypatch.setattr(cae.constants, "MAINNET_API_URL", mainnet)
    monkeypatch.setattr(cae.constants, "TESTNET_API_URL", testnet)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def signed(address_account, run_id: str, tmp_path: Path, name: str = "sig.txt") -> Path:
    message = cae.ownership_message(address_account.address, run_id)
    signature = Account.sign_message(
        encode_defunct(text=message), address_account.key
    ).signature.hex()
    path = tmp_path / name
    path.write_text(signature, encoding="utf-8")
    return path


def test_capture_writes_manifest_sidecars_extraction_and_requery_identities(
    tmp_path, monkeypatch
):
    fake = FakeInfo()
    patch_info(monkeypatch, fake)

    manifest = cae.run_capture(args(tmp_path))

    assert (
        manifest["ownership_evidence"]["status"] == "OWNERSHIP_EVIDENCE: NOT_PROVIDED"
    )
    assert manifest["window"] == {
        "start": START,
        "end": END,
        "start_ms": START_MS,
        "end_ms": END_MS,
        "semantics": cae.WINDOW_SEMANTICS,
    }
    assert {entry["base_url"] for entry in manifest["responses"]} == {"https://testnet"}
    assert len(manifest["responses"]) == 5
    for entry in manifest["responses"]:
        body = (tmp_path / entry["file"]).read_bytes()
        assert cae.sha256_bytes(body) == entry["response_sha256"]
        assert (tmp_path / (entry["file"] + ".sha256")).read_text(
            encoding="utf-8"
        ).strip() == entry["response_sha256"]
        assert entry["raw_bytes_source"] == cae.RAW_SOURCE_TEST_DOUBLE
    derived = read_json(tmp_path / "DERIVED_EXTRACTION.json")
    assert derived["label"] == "DERIVED_VIEW_NOT_ORIGINAL_BYTES"
    assert derived["fills"][0]["fee"] == "0.01"
    assert derived["fills"][0]["capture_sha256"]
    assert derived["funding"][0]["usdc"] == "-0.12"
    assert fake.fill_windows[0] == (START_MS, END_MS)
    cae.verify_sidecars(tmp_path)


def test_truncated_full_page_refuses(tmp_path, monkeypatch):
    monkeypatch.setattr(cae, "HL_FILLS_PAGE_LIMIT", 1)
    fake = FakeInfo(fills=[[fill_row(time=START_MS)]])
    patch_info(monkeypatch, fake)

    with pytest.raises(cae.CaptureRefused) as exc:
        cae.run_capture(args(tmp_path))

    assert exc.value.code == cae.REFUSED_TRUNCATED


def test_multi_page_success_dedups_the_inclusive_boundary(tmp_path, monkeypatch):
    monkeypatch.setattr(cae, "HL_FILLS_PAGE_LIMIT", 2)
    t0, t1, t2 = START_MS, START_MS + 1000, START_MS + 2000
    pages = [
        [
            fill_row(tid=1, time=t0),
            fill_row(tid=2, time=t1),
        ],  # full page -> cursor = t1
        [
            fill_row(tid=2, time=t1),
            fill_row(tid=3, time=t2),
        ],  # inclusive restart repeats tid 2
        [fill_row(tid=3, time=t2)],  # short page ends the pass
    ]
    fake = FakeInfo(fills=pages + pages)
    patch_info(monkeypatch, fake)

    manifest = cae.run_capture(args(tmp_path))

    assert fake.fill_calls == 6
    assert fake.fill_windows[:3] == [(START_MS, END_MS), (t1, END_MS), (t2, END_MS)]
    derived = read_json(tmp_path / "DERIVED_EXTRACTION.json")
    assert [row["tid"] for row in derived["fills"]] == [1, 2, 3]
    fill_pages = [
        e["file"] for e in manifest["responses"] if e["file"].startswith("fills_pass1")
    ]
    assert fill_pages == [
        "fills_pass1_page001.json",
        "fills_pass1_page002.json",
        "fills_pass1_page003.json",
    ]


def test_half_open_window_excludes_row_at_end_but_keeps_inside_rows(
    tmp_path, monkeypatch
):
    fake = FakeInfo(
        fills=[[fill_row(tid=1, time=INSIDE_MS), fill_row(tid=2, time=END_MS)]] * 2
    )
    patch_info(monkeypatch, fake)

    cae.run_capture(args(tmp_path))

    derived = read_json(tmp_path / "DERIVED_EXTRACTION.json")
    assert [row["tid"] for row in derived["fills"]] == [1]
    # the original bytes still hold both rows: exclusion is a derived-view rule, not a byte edit
    stored = read_json(tmp_path / "fills_pass1_page001.json")
    assert [row["tid"] for row in stored] == [1, 2]


def test_row_before_requested_start_refuses(tmp_path, monkeypatch):
    fake = FakeInfo(fills=[[fill_row(time=START_MS - 1)]])
    patch_info(monkeypatch, fake)

    with pytest.raises(cae.CaptureRefused) as exc:
        cae.run_capture(args(tmp_path))

    assert exc.value.code == cae.REFUSED_MALFORMED
    assert "before requested start" in exc.value.detail


def test_row_after_requested_end_refuses(tmp_path, monkeypatch):
    fake = FakeInfo(funding=[[funding_row(time=END_MS + 1)]])
    patch_info(monkeypatch, fake)

    with pytest.raises(cae.CaptureRefused) as exc:
        cae.run_capture(args(tmp_path))

    assert exc.value.code == cae.REFUSED_MALFORMED
    assert "after requested end" in exc.value.detail


def test_requery_identity_mismatch_refuses(tmp_path, monkeypatch):
    fake = FakeInfo(fills=[[fill_row(tid=1)], [fill_row(tid=2)]])
    patch_info(monkeypatch, fake)

    with pytest.raises(cae.CaptureRefused) as exc:
        cae.run_capture(args(tmp_path))

    assert exc.value.code == cae.REFUSED_REQUERY_MISMATCH
    assert "only in one pass" in exc.value.detail


def test_requery_content_mismatch_refuses(tmp_path, monkeypatch):
    fake = FakeInfo(
        fills=[[fill_row(tid=1, px="60000")], [fill_row(tid=1, px="60001")]]
    )
    patch_info(monkeypatch, fake)

    with pytest.raises(cae.CaptureRefused) as exc:
        cae.run_capture(args(tmp_path))

    assert exc.value.code == cae.REFUSED_REQUERY_MISMATCH
    assert "row content differs: tid:1" in exc.value.detail


def test_funding_identity_includes_coin(tmp_path, monkeypatch):
    two_coins = [
        funding_row(
            delta={
                "coin": "BTC",
                "usdc": "-0.12",
                "fundingRate": "0.00001",
                "szi": "0.01",
            }
        ),
        funding_row(
            delta={
                "coin": "ETH",
                "usdc": "-0.05",
                "fundingRate": "0.00001",
                "szi": "0.1",
            }
        ),
    ]
    fake = FakeInfo(funding=[two_coins, two_coins])
    patch_info(monkeypatch, fake)

    cae.run_capture(args(tmp_path))

    derived = read_json(tmp_path / "DERIVED_EXTRACTION.json")
    assert [row["coin"] for row in derived["funding"]] == ["BTC", "ETH"]

    with pytest.raises(cae.CaptureRefused) as exc:
        cae.funding_identity({"hash": "0xfund", "time": INSIDE_MS, "delta": {}})
    assert exc.value.code == cae.REFUSED_MALFORMED
    assert "no coin" in exc.value.detail


FIXTURE_R2 = Path(__file__).parent / "fixtures" / "p012_path1_r2_capture"


def test_verify_covers_derived_view_and_manifest_sidecars(tmp_path, monkeypatch):
    # NIT-1: CAPTURE_VERIFY_OK used to cover the responses only; the derived view and the manifest
    # have sidecars too, and the manifest records the derived digest
    patch_info(monkeypatch, FakeInfo())
    manifest = cae.run_capture(args(tmp_path))
    derived = tmp_path / "DERIVED_EXTRACTION.json"
    assert manifest["derived_extraction_sha256"] == cae.sha256_bytes(derived.read_bytes())
    cae.verify_sidecars(tmp_path)
    good = derived.read_bytes()
    derived.write_bytes(good.replace(b'"0.01"', b'"0.02"', 1))
    with pytest.raises(cae.CaptureRefused) as exc:
        cae.verify_sidecars(tmp_path)
    assert exc.value.code == cae.REFUSED_BAD_SIDECAR
    assert "DERIVED_EXTRACTION.json" in exc.value.detail
    # a re-hashed sidecar does not help: the manifest carries the digest
    (tmp_path / "DERIVED_EXTRACTION.json.sha256").write_text(
        cae.sha256_bytes(derived.read_bytes()) + "\n", encoding="utf-8"
    )
    with pytest.raises(cae.CaptureRefused) as exc:
        cae.verify_sidecars(tmp_path)
    assert "differs from the manifest digest" in exc.value.detail
    derived.write_bytes(good)
    (tmp_path / "DERIVED_EXTRACTION.json.sha256").write_text(
        cae.sha256_bytes(good) + "\n", encoding="utf-8"
    )
    cae.verify_sidecars(tmp_path)
    manifest_path = tmp_path / "CAPTURE_MANIFEST.json"
    manifest_path.write_bytes(manifest_path.read_bytes() + b"\n")
    with pytest.raises(cae.CaptureRefused) as exc:
        cae.verify_sidecars(tmp_path)
    assert exc.value.detail == "CAPTURE_MANIFEST.json"


def test_stray_sidecar_without_its_file_refuses(tmp_path, monkeypatch):
    patch_info(monkeypatch, FakeInfo())
    cae.run_capture(args(tmp_path))
    (tmp_path / "ghost.json.sha256").write_text("00" * 32 + "\n", encoding="utf-8")
    with pytest.raises(cae.CaptureRefused) as exc:
        cae.verify_sidecars(tmp_path)
    assert exc.value.code == cae.REFUSED_BAD_SIDECAR
    assert "ghost.json.sha256 names a missing file" == exc.value.detail


def test_descending_page_refuses_instead_of_truncating(tmp_path, monkeypatch):
    # NIT-2: the cursor arithmetic assumes ascending pages; a descending page is refused
    later = fill_row(tid=2, time=INSIDE_MS + 1000)
    earlier = fill_row(tid=1, time=INSIDE_MS)
    patch_info(monkeypatch, FakeInfo(fills=[[later, earlier], [later, earlier]]))
    with pytest.raises(cae.CaptureRefused) as exc:
        cae.run_capture(args(tmp_path))
    assert exc.value.code == cae.REFUSED_MALFORMED
    assert "not in ascending time order" in exc.value.detail


def test_malformed_account_state_keeps_its_bytes_before_refusing(tmp_path, monkeypatch):
    # NIT-3: account_state bytes are recorded before the shape check, like the paged queries
    patch_info(monkeypatch, FakeInfo(state=["not", "an", "object"]))
    with pytest.raises(cae.CaptureRefused) as exc:
        cae.run_capture(args(tmp_path))
    assert exc.value.code == cae.REFUSED_MALFORMED
    assert "account state is not an object" in exc.value.detail
    assert (tmp_path / "account_state.json").exists()
    assert (tmp_path / "account_state.json.sha256").exists()


def test_fill_without_tid_is_refused_not_guessed():
    # NIT-5: hash+oid+time could merge two identical partial fills; the shape is refused
    with pytest.raises(cae.CaptureRefused) as exc:
        cae.fill_identity(fill_row(tid=None))
    assert exc.value.code == cae.REFUSED_MALFORMED
    assert "without tid" in exc.value.detail
    assert cae.fill_identity(fill_row(tid=7)) == "tid:7"


@pytest.mark.parametrize(
    ("content", "fragment"),
    [
        ("{not json", "not a JSON object"),
        ("0xzz", "not recoverable"),
        ("0x" + "11" * 65, "not recoverable"),
    ],
)
def test_malformed_signature_is_a_named_refusal(tmp_path, monkeypatch, content, fragment):
    # NIT-6: a malformed signature file or signature exits 2 with a named refusal, never a raw
    # exception (exit 1)
    patch_info(monkeypatch, FakeInfo())
    path = tmp_path / "sig.txt"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(cae.CaptureRefused) as exc:
        cae.run_capture(args(tmp_path, ownership_signature=path))
    assert exc.value.code == cae.REFUSED_BAD_SIGNATURE
    assert fragment in exc.value.detail
    assert not (tmp_path / "CAPTURE_MANIFEST.json").exists()


def test_missing_signature_file_and_bad_verify_dir_exit_two(tmp_path, monkeypatch, capsys):
    patch_info(monkeypatch, FakeInfo())
    rc = cae.main(
        [
            "--network", "testnet", "--address", ADDRESS, "--start", START, "--end", END,
            "--out", str(tmp_path / "out"), "--run-id", "run-1",
            "--ownership-signature", str(tmp_path / "absent.txt"),
        ]
    )
    assert rc == 2
    assert cae.REFUSED_BAD_SIGNATURE in capsys.readouterr().err
    rc = cae.main(["--verify-existing", str(tmp_path / "no-such-dir")])
    assert rc == 2
    assert cae.REFUSED_BAD_SIDECAR in capsys.readouterr().err


def test_manifest_carries_the_signed_text_and_signature(tmp_path, monkeypatch):
    # NIT-7: the exact signed text and the signature are stored in the manifest (the message
    # still binds address + run_id only - changing it is the owner's call)
    account = Account.create()
    patch_info(monkeypatch, FakeInfo())
    path = signed(account, "run-7", tmp_path)
    manifest = cae.run_capture(
        args(tmp_path, address=account.address, ownership_signature=path, run_id="run-7")
    )
    evidence = manifest["ownership_evidence"]
    assert evidence["status"] == "OWNERSHIP_EVIDENCE: VERIFIED"
    assert evidence["message"] == cae.ownership_message(account.address, "run-7")
    assert evidence["signature"] == path.read_text(encoding="utf-8").strip()
    assert evidence["binds"] == "address+run_id"
    stored = read_json(tmp_path / "CAPTURE_MANIFEST.json")["ownership_evidence"]
    assert stored == evidence


def test_real_r2_capture_bytes_replay(tmp_path):
    # NIT-4: the stored bytes of the real r2 capture (mainnet, 2026-09-17) verify, and the derived
    # view is reproducible from the stored page bytes with the current identity/derivation code
    cae.verify_sidecars(FIXTURE_R2)
    manifest = read_json(FIXTURE_R2 / "CAPTURE_MANIFEST.json")
    assert manifest["run_id"] == "p012-path1-20260917T0700Z-1100Z-r2"
    assert manifest["network"] == "mainnet"
    assert len(manifest["responses"]) == 5
    derived = read_json(FIXTURE_R2 / "DERIVED_EXTRACTION.json")

    def rows(kind: str, identity):
        digest = next(
            e["response_sha256"] for e in manifest["responses"] if e["file"] == f"{kind}_pass1_page001.json"
        )
        page = read_json(FIXTURE_R2 / f"{kind}_pass1_page001.json")
        return [
            {"identity": identity(row), "row": row, "capture_sha256": digest, "json_pointer": f"/{i}"}
            for i, row in enumerate(page)
        ]

    assert cae.fill_derived(rows("fills", cae.fill_identity)) == derived["fills"]
    assert cae.funding_derived(rows("funding", cae.funding_identity)) == derived["funding"]
    assert len(derived["fills"]) == 2 and len(derived["funding"]) == 3
    # the old manifest (af921d75) has no derived digest; verification tolerates its absence
    assert "derived_extraction_sha256" not in manifest


def test_tampered_stored_bytes_vs_sidecar_refuses(tmp_path, monkeypatch):
    fake = FakeInfo()
    patch_info(monkeypatch, fake)
    cae.run_capture(args(tmp_path))
    (tmp_path / "fills_pass1_page001.json").write_text("tampered\n", encoding="utf-8")

    with pytest.raises(cae.CaptureRefused) as exc:
        cae.verify_sidecars(tmp_path)

    assert exc.value.code == cae.REFUSED_BAD_SIDECAR


def test_write_once_refuses_an_existing_output(tmp_path):
    target = tmp_path / "x.json"
    target.write_bytes(b"old")

    with pytest.raises(cae.CaptureRefused) as exc:
        cae.write_once(target, b"new")

    assert exc.value.code == cae.REFUSED_MALFORMED
    assert "output exists" in exc.value.detail
    assert target.read_bytes() == b"old"
    assert not (tmp_path / "x.json.sha256").exists()


def test_sdk_exception_refuses_query_failed(tmp_path, monkeypatch):
    fake = FakeInfo(raise_on="fills")
    patch_info(monkeypatch, fake)

    with pytest.raises(cae.CaptureRefused) as exc:
        cae.run_capture(args(tmp_path))

    assert exc.value.code == cae.REFUSED_QUERY_FAILED


def test_error_response_bytes_are_kept_before_refusal(tmp_path, monkeypatch):
    class ErrorInfo(FakeInfo):
        def __init__(self):
            super().__init__()
            self._captures = []

        def user_fills_by_time(self, address, start_ms, end_ms):
            self._captures.append(
                cae.RawCapture(
                    "/info", {"type": "userFillsByTime"}, b'{"error":"rate limited"}'
                )
            )
            raise RuntimeError("HTTP 429")

        def pop_capture(self):
            return self._captures.pop()

    patch_info(monkeypatch, ErrorInfo())

    with pytest.raises(cae.CaptureRefused) as exc:
        cae.run_capture(args(tmp_path))

    assert exc.value.code == cae.REFUSED_QUERY_FAILED
    assert "fills_pass1_page001_ERROR.json" in exc.value.detail
    assert (
        tmp_path / "fills_pass1_page001_ERROR.json"
    ).read_bytes() == b'{"error":"rate limited"}'
    assert (tmp_path / "fills_pass1_page001_ERROR.json.sha256").read_text(
        encoding="utf-8"
    ).strip() == cae.sha256_bytes(b'{"error":"rate limited"}')


def test_capturing_info_post_keeps_pre_parse_bytes_and_error_bytes():
    info = cae.CapturingInfo("https://example.invalid")
    ok_bytes = b'[{"tid": 7, "time": 1, "coin": "BTC"}]'
    info.session = FakeSession(
        [
            FakeResponse(ok_bytes),
            FakeResponse(b'{"code":"x","msg":"bad"}', status_code=400),
        ]
    )

    parsed = info.user_fills_by_time(ADDRESS, 1, 2)

    assert parsed == [{"tid": 7, "time": 1, "coin": "BTC"}]
    capture = info.pop_capture()
    assert capture.raw == ok_bytes
    assert capture.source == cae.RAW_SOURCE_HTTP
    assert capture.endpoint == "/info"
    assert capture.body["type"] == "userFillsByTime" and capture.body["user"] == ADDRESS
    assert info.session.calls[0]["url"] == "https://example.invalid/info"
    assert info.session.calls[0]["json"] == capture.body

    with pytest.raises(cae.CaptureRefused) as exc:
        cae.call_info(info, "user_fills_by_time", (ADDRESS, 1, 2), "/info", {})
    assert exc.value.code == cae.REFUSED_QUERY_FAILED
    assert "status=400" in exc.value.detail
    assert exc.value.error_capture is not None
    assert exc.value.error_capture.raw == b'{"code":"x","msg":"bad"}'
    assert exc.value.error_capture.source == cae.RAW_SOURCE_HTTP


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
    patch_info(
        monkeypatch,
        fake,
        mainnet="https://mainnet.example",
        testnet="https://testnet.example",
    )

    manifest = cae.run_capture(args(tmp_path, network="mainnet"))

    assert {entry["base_url"] for entry in manifest["responses"]} == {
        "https://mainnet.example"
    }


def test_ownership_signature_verifies_recovered_address(tmp_path, monkeypatch):
    account = Account.create()
    signature_path = signed(account, "run-1", tmp_path)
    fake = FakeInfo()
    patch_info(monkeypatch, fake)

    manifest = cae.run_capture(
        args(
            tmp_path / "capture",
            address=account.address,
            ownership_signature=signature_path,
        )
    )

    assert manifest["ownership_evidence"]["status"] == "OWNERSHIP_EVIDENCE: VERIFIED"
    assert (
        manifest["ownership_evidence"]["recovered_address"].lower()
        == account.address.lower()
    )
    assert manifest["run_id"] == "run-1"


def test_signature_without_run_id_refuses_before_network_and_writes_nothing(
    tmp_path, monkeypatch
):
    account = Account.create()
    signature_path = signed(account, "run-1", tmp_path)
    fake = FakeInfo()
    patch_info(monkeypatch, fake)
    out = tmp_path / "capture"

    with pytest.raises(cae.CaptureRefused) as exc:
        cae.run_capture(
            args(
                out,
                address=account.address,
                ownership_signature=signature_path,
                run_id=None,
            )
        )

    assert exc.value.code == cae.REFUSED_RUN_ID_REQUIRED
    assert fake.fill_calls == 0
    assert not out.exists()


def test_wrong_ownership_signature_refuses_before_network_and_writes_nothing(
    tmp_path, monkeypatch
):
    owner = Account.create()
    stranger = Account.create()
    signature_path = signed(stranger, "run-1", tmp_path)  # signed by another key
    fake = FakeInfo()
    patch_info(monkeypatch, fake)
    out = tmp_path / "capture"

    with pytest.raises(cae.CaptureRefused) as exc:
        cae.run_capture(
            args(out, address=owner.address, ownership_signature=signature_path)
        )

    assert exc.value.code == cae.REFUSED_BAD_SIGNATURE
    assert fake.fill_calls == 0
    assert not out.exists()

    # a signature over a different run_id is a wrong signature too
    other_run = signed(owner, "run-2", tmp_path, name="sig2.txt")
    with pytest.raises(cae.CaptureRefused) as exc:
        cae.run_capture(
            args(
                out,
                address=owner.address,
                ownership_signature=other_run,
                run_id="run-1",
            )
        )
    assert exc.value.code == cae.REFUSED_BAD_SIGNATURE
    assert fake.fill_calls == 0
    assert not out.exists()


def test_tool_imports_no_write_capable_exchange_client():
    source = Path(cae.__file__).read_text(encoding="utf-8")

    assert "hyperliquid.exchange" not in source
    assert "Exchange" not in source
