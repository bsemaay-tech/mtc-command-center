"""Fixture tests for the P0-12 funding intake adapter (offline; no network; no key)."""

from __future__ import annotations

import json
import re
from pathlib import Path
from types import SimpleNamespace

import pytest

from tools import funding_intake_adapter as adapter

ADDRESS = "0x" + "1e26" + "0" * 32 + "ac49"
SHA_A = "a" * 64
SHA_B = "b" * 64
TOOL_SHA = "c" * 64


def _manifest(window_start=1789398000000, window_end=1789412400000, pass2_sha=SHA_A):
    return {
        "kind": "P012_PATH1_OWN_ACCOUNT_CAPTURE_MANIFEST_V1",
        "address": ADDRESS,
        "coin": "BTC",
        "network": "mainnet",
        "run_id": "p012-path1-test-r1",
        "ownership_evidence": {"recovered_address": ADDRESS, "status": "VERIFIED"},
        "window": {
            "start": "2026-09-14T15:00:00Z",
            "end": "2026-09-14T19:00:00Z",
            "start_ms": window_start,
            "end_ms": window_end,
            "semantics": "half_open_start_inclusive_end_exclusive_ms",
        },
        "responses": [
            {
                "file": "fills_pass1_page001.json",
                "response_sha256": SHA_B,
                "tool_sha256": TOOL_SHA,
            },
            {
                "file": "funding_pass1_page001.json",
                "response_sha256": SHA_A,
                "tool_sha256": TOOL_SHA,
            },
            {
                "file": "funding_pass2_page001.json",
                "response_sha256": pass2_sha,
                "tool_sha256": TOOL_SHA,
            },
        ],
    }


def _derived():
    return {
        "label": "DERIVED_VIEW_NOT_ORIGINAL_BYTES",
        "fills": [
            {
                "kind": "DERIVED_FILL",
                "coin": "BTC",
                "time": 1789401810942,
                "capture_sha256": SHA_B,
                "json_pointer": "/0",
            }
        ],
        "funding": [
            {
                "kind": "DERIVED_FUNDING",
                "hash": "0x" + "0" * 64,
                "time": 1789405200041,
                "coin": "BTC",
                "usdc": "-0.000571",
                "fundingRate": "0.0000125",
                "szi": "0.00058",
                "capture_sha256": SHA_A,
                "json_pointer": "/0",
            },
            {
                "kind": "DERIVED_FUNDING",
                "hash": "0x" + "0" * 64,
                "time": 1789408800060,
                "coin": "BTC",
                "usdc": "-0.000572",
                "fundingRate": "0.0000125",
                "szi": "0.00058",
                "capture_sha256": SHA_A,
                "json_pointer": "/1",
            },
        ],
    }


def _write_run(root: Path, manifest=None, derived=None) -> Path:
    run = root / "r1"
    run.mkdir(parents=True)
    (run / "CAPTURE_MANIFEST.json").write_text(
        json.dumps(manifest or _manifest()), encoding="utf-8"
    )
    (run / "DERIVED_EXTRACTION.json").write_text(
        json.dumps(derived or _derived()), encoding="utf-8"
    )
    return run


def test_build_fills_only_what_the_bytes_supply_and_labels_the_rest():
    intake = adapter.build_intake(_manifest(), _derived())
    packet = intake["packet"]
    assert packet["label"] == adapter.DRAFT_LABEL
    assert len(packet["bindings"]) == 2
    first = packet["bindings"][0]
    assert first["event_timestamp"] == "2026-09-14T17:00:00.041Z"
    assert first["raw_rate"] == "0.0000125"
    assert first["funding_event_id"] == "hl-funding:0x1e26…ac49:BTC:1789405200041"
    assert first["oracle_price"] == "UNRESOLVED:D-4"
    assert first["oracle_price_source"] == "UNRESOLVED:D-4"
    assert first["source_event_digest"] == "UNRESOLVED:D-1"
    assert first["positive_rate_payer"] == "LONG"
    assert first["provenance"]["source_locator"] == "funding_pass1_page001.json#/0"
    assert first["provenance"]["source_sha256"] == SHA_A
    assert first["provenance"]["evidence_kind_status"] == adapter.D5_RESOLVED_NOTE
    assert ADDRESS not in json.dumps(intake)  # only the short form leaves the adapter
    assert (
        intake["retained_rows"]["rows"][0]["payload_digest"]
        == adapter.BRIDGE_DIGEST_UNAVAILABLE
    )
    assert intake["retained_rows"]["rows"][0]["payload"] == {
        "coin": "BTC",
        "fundingRate": "0.0000125",
        "szi": "0.00058",
        "usdc": "-0.000571",
    }
    # the draft packet declares evidence_kind REAL_CAPTURE_READ_ONLY inside a
    # SYNTHETIC_FUNDING_BINDING_PACKET_V1 packet: the export tool's default
    # (SYNTHETIC) profile actually refuses this as a kind mismatch, not as a
    # missing production contract; this outcome is computed by calling the
    # tool, never declared (lane-8 exact-Opus review of a871e429, NIT-A)
    assert (
        intake["gap_report"]["export_tool_outcome_today"]["refusal_code"]
        == exporter.CANDIDATE_EVIDENCE_KIND_MISMATCH
    )


def test_export_tool_outcome_today_computes_the_outcome_by_calling_the_exporter(
    monkeypatch,
):
    """NIT-3 (Sol T0 review of `8cbf4f1a`): the assertion above only checks the
    resulting code, so a mutant that hardcoded
    ``CANDIDATE_EVIDENCE_KIND_MISMATCH`` without ever calling
    ``build_funding_candidate`` still passed it. Monkeypatch the exporter entry
    point to a sentinel refusal no real packet could produce and assert both
    the sentinel value and the exact call arguments reach the gap report."""
    calls: list[dict[str, object]] = []

    def _fake_build_funding_candidate(
        retained_rows,
        approved_event_bindings,
        coverage,
        schedule_id,
        start_inclusive,
        end_exclusive,
        **kwargs,
    ):
        calls.append(
            {
                "retained_rows": retained_rows,
                "approved_event_bindings": approved_event_bindings,
                "coverage": coverage,
                "schedule_id": schedule_id,
                "start_inclusive": start_inclusive,
                "end_exclusive": end_exclusive,
                "kwargs": kwargs,
            }
        )
        return SimpleNamespace(
            accepted=False,
            reason_code="SENTINEL_NIT3_REFUSAL",
            report={"reason_detail": "sentinel refusal, never produced by the real tool"},
        )

    monkeypatch.setattr(
        adapter.exporter, "build_funding_candidate", _fake_build_funding_candidate
    )

    intake = adapter.build_intake(_manifest(), _derived())

    assert len(calls) == 1
    outcome = intake["gap_report"]["export_tool_outcome_today"]
    assert outcome["refusal_code"] == "SENTINEL_NIT3_REFUSAL"
    assert outcome["reason"] == "sentinel refusal, never produced by the real tool"
    call = calls[0]
    coverage = intake["packet"]["coverage"]
    assert call["retained_rows"] == []
    assert call["approved_event_bindings"] == []
    assert call["coverage"] == coverage
    assert call["schedule_id"] == "P012_INTAKE_ADAPTER_PROBE"
    assert call["start_inclusive"] == coverage["interval_start_inclusive"]
    assert call["end_exclusive"] == coverage["interval_end_exclusive"]
    assert call["kwargs"] == {}


def test_unresolved_fields_are_never_fabricated():
    intake = adapter.build_intake(_manifest(), _derived())
    text = json.dumps(intake)
    for binding in intake["packet"]["bindings"]:
        for field in ("oracle_price", "oracle_price_source", "source_event_digest"):
            assert binding[field].startswith("UNRESOLVED:D-"), field
    for row in intake["retained_rows"]["rows"]:
        assert row["payload_digest"] == adapter.BRIDGE_DIGEST_UNAVAILABLE
    # the back-derived oracle price (usdc / (szi * rate) ~ 78758.6) must appear nowhere
    assert "78758" not in text and "78759" not in text


def test_completeness_rule_hour_alignment_and_identical_passes():
    complete = adapter.completeness(_manifest())
    assert complete["complete"] is True and complete["reasons"] == []
    unaligned = adapter.completeness(_manifest(window_start=1789398000000 + 1))
    assert unaligned["complete"] is False and "aligned" in unaligned["reasons"][0]
    # Gemini NIT-02 (counted detection, 2026-09-15 20:14Z): the END bound is held to the same rule
    unaligned_end = adapter.completeness(_manifest(window_end=1789412400000 + 41))
    assert (
        unaligned_end["complete"] is False and "aligned" in unaligned_end["reasons"][0]
    )
    differing = adapter.completeness(_manifest(pass2_sha=SHA_B))
    assert (
        differing["complete"] is False and "byte-identical" in differing["reasons"][0]
    )
    packet = adapter.build_intake(_manifest(pass2_sha=SHA_B), _derived())["packet"]
    assert packet["coverage"]["complete"] is False


def test_refuses_foreign_coin_malformed_rows_and_bad_labels():
    derived = _derived()
    derived["funding"][0]["coin"] = "ETH"
    with pytest.raises(adapter.IntakeRefused, match="not the run coin"):
        adapter.build_intake(_manifest(), derived)
    derived = _derived()
    derived["funding"][1]["time"] = "1789408800060"
    with pytest.raises(adapter.IntakeRefused, match="must be an integer"):
        adapter.build_intake(_manifest(), derived)
    derived = _derived()
    derived["funding"][0]["kind"] = "DERIVED_FILL"
    with pytest.raises(adapter.IntakeRefused, match="DERIVED_FUNDING"):
        adapter.build_intake(_manifest(), derived)


def test_load_refuses_wrong_kinds_and_duplicate_keys(tmp_path: Path):
    run = _write_run(tmp_path)
    manifest, derived, raw, manifest_sha = adapter.load_capture(run)
    assert manifest["run_id"] == "p012-path1-test-r1" and len(derived["funding"]) == 2
    assert raw == {} and len(manifest_sha) == 64
    bad = _write_run(tmp_path / "bad", manifest={**_manifest(), "kind": "OTHER"})
    with pytest.raises(adapter.IntakeRefused, match="manifest kind"):
        adapter.load_capture(bad)
    dup = _write_run(tmp_path / "dup")
    (dup / "DERIVED_EXTRACTION.json").write_text(
        '{"label":"DERIVED_VIEW_NOT_ORIGINAL_BYTES","label":"x","fills":[],"funding":[]}',
        encoding="utf-8",
    )
    with pytest.raises(adapter.IntakeRefused, match="duplicate JSON member"):
        adapter.load_capture(dup)


def test_outputs_are_deterministic_write_once_and_clock_free(tmp_path: Path):
    intake = adapter.build_intake(_manifest(), _derived())
    d1 = adapter.write_outputs(tmp_path / "one", intake)
    d2 = adapter.write_outputs(tmp_path / "two", intake)
    assert d1 == d2
    with pytest.raises(adapter.IntakeRefused, match="write-once"):
        adapter.write_outputs(tmp_path / "one", intake)
    for name in d1:
        raw = (tmp_path / "one" / name).read_bytes()
        assert (tmp_path / "two" / name).read_bytes() == raw
        assert (tmp_path / "one" / (name + ".sha256")).read_text().strip() == d1[name]
        # no wall clock in any output: every timestamp prefix is the capture window's own day (venue stamps)
        assert set(re.findall(rb"\d{4}-\d{2}-\d{2}T", raw)) <= {b"2026-09-14T"}, name


def test_main_end_to_end(tmp_path: Path, capsys):
    run = _write_run(tmp_path)
    assert adapter.main(["--run-dir", str(run), "--out", str(tmp_path / "out")]) == 0
    out = capsys.readouterr().out
    assert "NONACCEPTING_INTAKE_DRAFT events=2 fills=1 complete=True" in out
    assert adapter.main(["--run-dir", str(run), "--out", str(tmp_path / "out")]) == 3
    assert "INTAKE_OUTPUT_EXISTS" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# Slice 4 — the accepting shape, built from the exact captured bytes and read
# back by export_mtc_funding.py under the REAL_CAPTURE_READ_ONLY profile
# ---------------------------------------------------------------------------

import hashlib
from datetime import UTC, datetime

from bridge.engine.types import FundingAttribution, FundingEventRecord
from tools import export_mtc_funding as exporter

# the exact 433-byte userFunding response of capture r1 (zero hash, no address)
FUNDING_PASS = (
    b'[{"time":1789405200041,"hash":"0x'
    + b"0" * 64
    + b'","delta":{"type":"funding","coin":"BTC","usdc":"-0.000571","szi":"0.00058",'
    b'"fundingRate":"0.0000125","nSamples":null}},{"time":1789408800060,"hash":"0x'
    + b"0"
    * 64
    + b'","delta":{"type":"funding","coin":"BTC","usdc":"-0.000572","szi":"0.00058",'
    b'"fundingRate":"0.0000125","nSamples":null}}]'
)


def _fill(px, sz, side, time_ms, start, direction, seed):
    tx = "0x" + hashlib.sha256(f"fixture-fill-{seed}".encode()).hexdigest()
    return (
        f'{{"coin":"BTC","px":"{px}","sz":"{sz}","side":"{side}","time":{time_ms},'
        f'"startPosition":"{start}","dir":"{direction}","closedPnl":"0.0","hash":"{tx}",'
        f'"oid":{544824403105 + seed},"crossed":true,"fee":"0.005423","tid":{261929593852405 + seed},'
        f'"feeToken":"USDC","twapId":null}}'
    )


FILLS_PASS = (
    "["
    + ",".join(
        [
            _fill("78462.0", "0.00016", "B", 1789401810942, "0.0", "Open Long", 1),
            _fill("78451.0", "0.00013", "B", 1789401915271, "0.00016", "Open Long", 2),
            _fill("78438.0", "0.00013", "B", 1789401971269, "0.00029", "Open Long", 3),
            _fill("78410.0", "0.00016", "B", 1789402474869, "0.00042", "Open Long", 4),
            _fill("78993.0", "0.00058", "A", 1789409323372, "0.00058", "Close Long", 5),
        ]
    )
    + "]"
).encode()
FUNDING_SHA = hashlib.sha256(FUNDING_PASS).hexdigest()
FILLS_SHA = hashlib.sha256(FILLS_PASS).hexdigest()


def _real_manifest():
    manifest = _manifest(pass2_sha=FUNDING_SHA)
    manifest["ownership_evidence"] = {
        "recovered_address": ADDRESS,
        "status": "OWNERSHIP_EVIDENCE: VERIFIED",
    }
    for response in manifest["responses"]:
        response["response_sha256"] = (
            FILLS_SHA if response["file"].startswith("fills") else FUNDING_SHA
        )
    return manifest


def _real_derived():
    derived = _derived()
    for row in derived["funding"]:
        row["capture_sha256"] = FUNDING_SHA
    derived["fills"][0]["capture_sha256"] = FILLS_SHA
    return derived


def _write_real_run(root: Path, funding: bytes = FUNDING_PASS) -> Path:
    run = _write_run(root, manifest=_real_manifest(), derived=_real_derived())
    (run / "funding_pass1_page001.json").write_bytes(funding)
    (run / "funding_pass2_page001.json").write_bytes(funding)
    (run / "fills_pass1_page001.json").write_bytes(FILLS_PASS)
    return run


def _fixture_rows(packet):
    """FIXTURE retained rows: what a schema-v10 store would carry (none has)."""
    rows = []
    for binding, amount in zip(packet["bindings"], (-0.000571, -0.000572)):
        stamp = datetime.strptime(
            binding["event_timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ).replace(tzinfo=UTC)
        record = FundingEventRecord(
            event_id=binding["funding_event_id"],
            symbol="BTC",
            amount_usdc=amount,
            effective_ts=stamp,
            source="HL_USER_FUNDING",
            attribution=FundingAttribution.ATTRIBUTED,
            funding_rate=0.0000125,
            position_szi=0.00058,
            n_samples=None,
        )
        rows.append(
            {
                "attribution": "ATTRIBUTED",
                "event_id": record.event_id,
                "ledger_effective_ts": stamp.isoformat(),
                "payload": record.authoritative(),
                "payload_digest": record.digest,
                "payload_reason": exporter.PAYLOAD_RETAINED,
                "symbol": "BTC",
            }
        )
    return rows


def test_real_packet_is_built_from_the_captured_bytes_under_the_ruled_shape(
    tmp_path: Path,
):
    run = _write_real_run(tmp_path)
    manifest, derived, raw, manifest_sha = adapter.load_capture(run)

    intake = adapter.build_intake(manifest, derived, raw, manifest_sha)
    packet = intake["real_packet"]

    assert packet is not None
    assert set(packet) == {"bindings", "coverage", "packet_version"}
    assert packet["packet_version"] == exporter.REAL_CAPTURE_PACKET_VERSION
    first = packet["bindings"][0]
    assert set(first) == set(exporter.REAL_BINDING_KEYS)
    assert first["funding_event_id"] == "hl-funding:0x1e26…ac49:BTC:1789405200041"
    assert first["event_timestamp"] == "2026-09-14T17:00:00.041Z"
    assert first["interval_hour_utc"] == "2026-09-14T17:00:00Z"
    row0 = FUNDING_PASS[1:216]
    assert first["source_event_digest"] == (
        f"HL_USERFUNDING_ROW_V1:{hashlib.sha256(row0).hexdigest()}"
    )
    assert first["oracle_price"] == "UNRESOLVED:D-4"
    assert first["provenance"]["source_sha256"] == FUNDING_SHA
    cover = packet["coverage"]
    assert set(cover) == set(exporter.REAL_COVERAGE_KEYS)
    assert cover["source_witnesses"][first["funding_event_id"]] == row0.hex()
    assert cover["funding_witness_passes"] == [FUNDING_PASS.hex()] * 2
    assert cover["fills_witness"] == FILLS_PASS.hex()
    assert f"manifest_sha256={manifest_sha}" in cover["witness_identity"]
    assert (
        "ownership OWNERSHIP_EVIDENCE: VERIFIED 0x1e26…ac49"
        in cover["witness_identity"]
    )
    assert ADDRESS not in json.dumps(intake)
    assert intake["gap_report"]["real_capture_packet"]["status"] == "BUILT"
    assert "78758" not in json.dumps(packet)


def test_real_packet_refuses_under_d4_then_validates_once_an_oracle_capture_is_named(
    tmp_path: Path,
):
    run = _write_real_run(tmp_path)
    manifest, derived, raw, manifest_sha = adapter.load_capture(run)
    packet = adapter.build_intake(manifest, derived, raw, manifest_sha)["real_packet"]
    rows = _fixture_rows(packet)
    start, end = "2026-09-14T15:00:00Z", "2026-09-14T19:00:00Z"

    refused = exporter.build_funding_candidate(
        rows,
        packet["bindings"],
        packet["coverage"],
        "S4-TEST",
        start,
        end,
        evidence_kind=exporter.REAL_CAPTURE_EVIDENCE_KIND,
    )
    assert refused.accepted is False
    assert refused.reason_code == exporter.CANDIDATE_ORACLE_EVIDENCE_UNAVAILABLE

    # a FIXTURE oracle capture locator stands in for the capture r1 never made
    locator = hashlib.sha256(b"fixture-oracle-capture").hexdigest() + "#/1/0/oraclePx"
    for binding in packet["bindings"]:
        binding["oracle_price"] = "78758.6"
        binding["oracle_price_source"] = locator
    accepted = exporter.build_funding_candidate(
        rows,
        packet["bindings"],
        packet["coverage"],
        "S4-TEST",
        start,
        end,
        evidence_kind=exporter.REAL_CAPTURE_EVIDENCE_KIND,
    )
    assert accepted.accepted is True, accepted.report["reason_detail"]
    assert accepted.reason_code == exporter.REAL_CAPTURE_CANDIDATE_BUILT

    # and the same packet under the default profile is a kind mismatch, never a pass
    default = exporter.build_funding_candidate(
        rows, packet["bindings"], packet["coverage"], "S4-TEST", start, end
    )
    assert default.accepted is False
    assert default.reason_code == exporter.CANDIDATE_EVIDENCE_KIND_MISMATCH


def test_real_packet_is_absent_without_raw_bytes_and_refuses_tampered_bytes(
    tmp_path: Path,
):
    intake = adapter.build_intake(_manifest(), _derived())
    assert intake["real_packet"] is None
    assert intake["gap_report"]["real_capture_packet"]["status"] == "NOT_BUILT"

    run = _write_run(
        tmp_path / "plain", manifest=_real_manifest(), derived=_real_derived()
    )
    manifest, derived, raw, manifest_sha = adapter.load_capture(run)
    assert raw == {}
    assert (
        adapter.build_intake(manifest, derived, raw, manifest_sha)["real_packet"]
        is None
    )

    tampered = _write_real_run(
        tmp_path / "tampered", funding=FUNDING_PASS.replace(b"0.000571", b"0.000570")
    )
    with pytest.raises(adapter.IntakeRefused, match="response_sha256"):
        adapter.load_capture(tampered)


def test_real_packet_outputs_are_written_deterministically(tmp_path: Path, capsys):
    run = _write_real_run(tmp_path)
    assert adapter.main(["--run-dir", str(run), "--out", str(tmp_path / "out")]) == 0
    out = capsys.readouterr().out
    assert (
        "real_packet=BUILT real_packet_tool_outcome_expected="
        "CANDIDATE_ORACLE_EVIDENCE_UNAVAILABLE"
    ) in out
    written = (tmp_path / "out" / adapter.REAL_PACKET_FILENAME).read_bytes()
    assert (
        hashlib.sha256(written).hexdigest()
        == (tmp_path / "out" / (adapter.REAL_PACKET_FILENAME + ".sha256"))
        .read_text()
        .strip()
    )
    assert set(re.findall(rb"\d{4}-\d{2}-\d{2}T", written)) <= {b"2026-09-14T"}
