"""Fixture tests for the P0-12 funding intake adapter (offline; no network; no key)."""

from __future__ import annotations

import json
from pathlib import Path

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
    assert first["provenance"]["evidence_kind_status"] == "UNRESOLVED:D-5"
    assert ADDRESS not in json.dumps(intake)  # only the short form leaves the adapter
    assert intake["retained_rows"]["rows"][0]["payload_digest"] == "UNRESOLVED:D-1"
    assert intake["retained_rows"]["rows"][0]["payload"] == {
        "coin": "BTC",
        "fundingRate": "0.0000125",
        "szi": "0.00058",
        "usdc": "-0.000571",
    }
    assert (
        intake["gap_report"]["export_tool_outcome_today"]["refusal_code"]
        == "CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE"
    )


def test_unresolved_fields_are_never_fabricated():
    intake = adapter.build_intake(_manifest(), _derived())
    text = json.dumps(intake)
    for binding in intake["packet"]["bindings"]:
        for field in ("oracle_price", "oracle_price_source", "source_event_digest"):
            assert binding[field].startswith("UNRESOLVED:D-"), field
    for row in intake["retained_rows"]["rows"]:
        assert row["payload_digest"].startswith("UNRESOLVED:D-")
    # the back-derived oracle price (usdc / (szi * rate) ~ 78758.6) must appear nowhere
    assert "78758" not in text and "78759" not in text


def test_completeness_rule_hour_alignment_and_identical_passes():
    complete = adapter.completeness(_manifest())
    assert complete["complete"] is True and complete["reasons"] == []
    unaligned = adapter.completeness(_manifest(window_start=1789398000000 + 1))
    assert unaligned["complete"] is False and "aligned" in unaligned["reasons"][0]
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
    manifest, derived = adapter.load_capture(run)
    assert manifest["run_id"] == "p012-path1-test-r1" and len(derived["funding"]) == 2
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
        assert (
            b"2026-09-15T" not in raw or name == "binding_packet_draft.json"
        )  # no wall clock; only venue stamps


def test_main_end_to_end(tmp_path: Path, capsys):
    run = _write_run(tmp_path)
    assert adapter.main(["--run-dir", str(run), "--out", str(tmp_path / "out")]) == 0
    out = capsys.readouterr().out
    assert "NONACCEPTING_INTAKE_DRAFT events=2 fills=1 complete=True" in out
    assert adapter.main(["--run-dir", str(run), "--out", str(tmp_path / "out")]) == 3
    assert "INTAKE_OUTPUT_EXISTS" in capsys.readouterr().err
