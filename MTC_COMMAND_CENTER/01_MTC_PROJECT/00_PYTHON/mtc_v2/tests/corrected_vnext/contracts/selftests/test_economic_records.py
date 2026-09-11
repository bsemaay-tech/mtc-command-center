from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from mtc_v2.core.instrument import (
    REFUSED_INCOMPLETE_INSTRUMENT_RECORD,
    REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION,
    REFUSED_INVALID_RECORD_BYTES,
    InstrumentRecordRefusal,
    load_verified_instrument_record,
    load_verified_json_record,
)


MTC_V2_ROOT = Path(__file__).resolve().parents[4]
RECORD_ROOT = MTC_V2_ROOT / "core" / "economic_records"


def test_catalog_pinned_synthetic_instrument_loads_for_evaluation() -> None:
    path = (
        RECORD_ROOT
        / "instruments"
        / "SYNTH-INSTRUMENT-RULE2-01-RED-V1.json"
    )
    record = load_verified_instrument_record(path)

    assert record.digest == "e3612111ca302bc86dfac316efb80d08aac12a8312287e7117b0115f289e1e5d"
    metadata = record.for_evaluation(
        "2000-01-01T00:10:00Z",
        {
            "instrument_symbol": "SYNTH-RULE2-01-RED",
            "instrument_point_value": 1,
            "instrument_price_tick": 1,
            "instrument_qty_step": 1,
            "instrument_min_qty": 0,
            "instrument_min_notional": 0,
            "instrument_contract_multiplier": 2,
        },
    )
    assert metadata.symbol == "SYNTH-RULE2-01-RED"
    assert metadata.contract_multiplier == 2.0


def test_production_candidate_bytes_are_copied_exactly_but_remain_incomplete() -> None:
    path = RECORD_ROOT / "instruments" / "HYPERLIQUID-BTC-PERP-V1.3.json"
    verified = load_verified_json_record(path)
    assert verified.digest == "5abb99abbdb9735e95ad1084c706a3c5326fb6bb134e48a79e9bb0992b68316a"
    provenance = verified.data["provenance"]
    assert {
        Path(source["frozen_file"]).name: source["sha256"]
        for source in provenance["sources"]
    } == {
        "api-info-meta.json": "2bbe9a105808b910a62813b1c3f30ca3149241ab4625a01a825d0165455039c9",
        "contract-specifications.html": "3be3f419b268e9aeac2d85c0a9611eddfd486c510e59b62f44e5547aa5253737",
        "error-responses.html": "a320fd41ad7d9e3ee88a9ae501ba5126dadcd7c63b410629c87a2a874bb43727",
        "order-types.html": "8c65a45d63a554ae54568378ba7e29e505aee6a3f9758b0cdcd298ab95992640",
        "tick-and-lot-size-api.html": "81a865c35bcb77338cb94bf0a09e6294bb772a4d7ddd24af28636c273655d3e4",
    }
    assert provenance["source_sha256"] == (
        "da2bf1fef41adbb4d3429e5abaff070a8fc81814730bf0ee7715b9eb79f097ed"
    )
    assert verified.data["price_tick"] is None
    assert dict(verified.data["price_alignment_policy"]) == {
        "id": "HYPERLIQUID_PX_V1",
        "significant_figures": 5,
        "perp_max_decimals": 6,
        "size_decimals": 5,
        "integer_exception": True,
        "positive_price_required": True,
    }
    assert verified.data["minimum_quantity"] is None
    assert verified.data["provenance"]["human_reviewer"] is None

    record = load_verified_instrument_record(path)
    with pytest.raises(InstrumentRecordRefusal) as exc_info:
        record.for_evaluation("2026-08-31T07:00:53Z", {})
    assert exc_info.value.refusal_code == REFUSED_INCOMPLETE_INSTRUMENT_RECORD


def test_runtime_instrument_override_must_equal_record() -> None:
    path = (
        RECORD_ROOT
        / "instruments"
        / "SYNTH-INSTRUMENT-RULE2-03-RED-V1.json"
    )
    record = load_verified_instrument_record(path)
    with pytest.raises(InstrumentRecordRefusal) as exc_info:
        record.for_evaluation(
            "2000-01-01T00:10:00Z",
            {"instrument_price_tick": 0.25},
        )
    assert exc_info.value.refusal_code == REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION


@pytest.mark.parametrize(
    "raw",
    [
        b'{"record_id":"X","record_id":"Y"}\n',
        b'{"record_id":"X","value":NaN}\n',
        b'{"record_id":"X"}',
        b'\xef\xbb\xbf{"record_id":"X"}\n',
        b'{"record_id":"X"}\r\n',
    ],
)
def test_strict_record_loader_refuses_invalid_json_bytes(tmp_path: Path, raw: bytes) -> None:
    path = tmp_path / "record.json"
    path.write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    path.with_name(path.name + ".sha256").write_bytes((digest + "\n").encode("ascii"))

    with pytest.raises(InstrumentRecordRefusal) as exc_info:
        load_verified_json_record(path)
    assert exc_info.value.refusal_code == REFUSED_INVALID_RECORD_BYTES


def test_detached_digest_is_mandatory_and_exact(tmp_path: Path) -> None:
    path = tmp_path / "record.json"
    path.write_bytes(b'{"record_id":"X"}\n')
    path.with_name(path.name + ".sha256").write_bytes(("0" * 64 + "\n").encode("ascii"))

    with pytest.raises(InstrumentRecordRefusal) as exc_info:
        load_verified_json_record(path)
    assert exc_info.value.refusal_code == REFUSED_INVALID_RECORD_BYTES


def test_every_catalog_record_reference_resolves_to_exact_bytes() -> None:
    input_root = MTC_V2_ROOT / "tests" / "corrected_vnext" / "contracts" / "inputs"
    resolved: set[tuple[str, str]] = set()
    for input_path in sorted(input_root.glob("*.json")):
        document = json.loads(input_path.read_text(encoding="utf-8"))
        refs = document["corrected_only"]["records"]
        for kind, identity_key, digest_key in (
            ("instruments", "instrument_record_id", "instrument_record_sha256"),
            ("costs", "cost_schedule_id", "cost_schedule_sha256"),
            ("funding", "funding_schedule_id", "funding_schedule_sha256"),
        ):
            identity = refs[identity_key]
            digest = refs[digest_key]
            if identity is None:
                assert digest is None
                continue
            record = load_verified_json_record(RECORD_ROOT / kind / f"{identity}.json")
            assert record.digest == digest
            resolved.add((kind, identity))
    assert len(resolved) == 48


def test_production_cost_record_preserves_residual_refusals() -> None:
    record = load_verified_json_record(
        RECORD_ROOT / "costs" / "HYPERLIQUID-BTC-PERP-BASE-TIER0-V1.json"
    ).data
    assert record["maker_rate"] == 0.00015
    assert record["taker_rate"] == 0.00045
    assert record["slippage_model_id"] == "BPS_OF_REFERENCE_V1"
    assert record["slippage_parameters"]["slippage_bps"] == 0
    assert "fixed_component" not in record
    assert "minimum_fee" not in record
    assert "fee_rounding_rule" not in record
    assert record["refused_event_classes"]["MARGIN_CALL_LIQUIDATION"].startswith(
        "CANNOT_MAP"
    )
    absence = record["provenance"]["frozen_source_absence"]
    assert absence["fields"] == (
        "fee_rounding_rule",
        "fixed_component",
        "minimum_fee",
    )
    assert absence["source_locator"] == (
        "https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees"
    )
    assert absence["source_sha256"] == (
        "3c49f9030a427df06f70943f53517204e4bd804bb205dcd05b2d27a75f51ce8b"
    )
    assert absence["owner_decision_ref"] == (
        "HIST-2026-0033 / WP-P012-DECISION1-SOURCED-ABSENCE"
    )
    assert absence["disposition"] == "KEEP_REFUSED"
    assert absence["limitation"] == (
        "Not stated in this frozen source; no zero or rule inferred; not "
        "universal current absence or liquidation evidence."
    )
    assert record["refused_missing_fields"] == (
        "fee_rounding_rule",
        "fixed_component",
        "minimum_fee",
        "tier_account_selection_evidence",
    )
    assert record["admission_status"] == "REFUSED_INCOMPLETE_COST_SCHEDULE"


def test_production_funding_rules_do_not_invent_event_rows() -> None:
    record = load_verified_json_record(
        RECORD_ROOT / "funding" / "HYPERLIQUID-BTC-PERP-FUNDING-RULES-V1.json"
    ).data
    assert record["position_snapshot_rule"] == "END_OF_INTERVAL_INCLUDE_SAME_TIMESTAMP_V1"
    assert record["rate_rules"]["valuation_price_source"] == "SPOT_ORACLE"
    assert record["rate_rules"]["positive_rate_payer"] == "LONG"
    assert record["events"] is None
    assert record["effective_interval"] is None
    assert record["admission_status"] == "REFUSED_MISSING_PRODUCTION_FUNDING_EVENTS"
