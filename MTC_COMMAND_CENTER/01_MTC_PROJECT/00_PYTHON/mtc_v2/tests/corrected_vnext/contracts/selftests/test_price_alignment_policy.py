from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from mtc_v2.core.instrument import (
    REFUSED_INCOMPLETE_INSTRUMENT_RECORD,
    InstrumentMetadata,
    InstrumentRecordRefusal,
    load_verified_instrument_record,
)
from mtc_v2.core.rounding import (
    PriceAlignmentPolicy,
    align_price_to_policy,
    is_valid_price,
)


POLICY = PriceAlignmentPolicy(
    id="HYPERLIQUID_PX_V1",
    significant_figures=5,
    perp_max_decimals=6,
    size_decimals=5,
    integer_exception=True,
    positive_price_required=True,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0.1, True),
        (9999.9, True),
        (10000, True),
        (100001, True),
        (123456, True),
        (0.01, False),
        (9999.95, False),
        (10000.1, False),
        (0.0, False),
        (-0.1, False),
        (float("inf"), False),
        (float("nan"), False),
    ],
)
def test_hyperliquid_policy_membership(value: float, expected: bool) -> None:
    assert is_valid_price(value, POLICY) is expected


@pytest.mark.parametrize(
    ("value", "floor", "ceil", "nearest"),
    [
        (12345.6, 12345, 12346, 12346),
        (100000.1, 100000, 100001, 100000),
        (1234.55, 1234.5, 1234.6, 1234.6),
        (9999.95, 9999.9, 10000, 10000),
        (42.04, 42.0, 42.1, 42.0),
        (123456, 123456, 123456, 123456),
        (100001, 100001, 100001, 100001),
    ],
)
def test_policy_neighbors_and_direction(
    value: float,
    floor: float,
    ceil: float,
    nearest: float,
) -> None:
    assert align_price_to_policy(value, POLICY, "FLOOR") == floor
    assert align_price_to_policy(value, POLICY, "CEIL") == ceil
    assert align_price_to_policy(value, POLICY, "HALF_UP") == nearest


def test_no_positive_floor_neighbor_refuses_but_ceil_and_nearest_use_point_one() -> None:
    with pytest.raises(ValueError):
        align_price_to_policy(0.01, POLICY, "FLOOR")
    assert align_price_to_policy(0.01, POLICY, "CEIL") == 0.1
    assert align_price_to_policy(0.01, POLICY, "HALF_UP") == 0.1


@pytest.mark.parametrize("value", [0.0, -1.0, float("inf"), float("-inf"), float("nan")])
def test_policy_alignment_refuses_nonpositive_or_nonfinite_input(value: float) -> None:
    with pytest.raises(ValueError):
        align_price_to_policy(value, POLICY, "HALF_UP")


def test_metadata_dispatches_policy_without_changing_public_rounding_methods() -> None:
    metadata = InstrumentMetadata(price_tick=None, price_alignment_policy=POLICY)
    assert metadata.floor_price(12345.6) == 12345
    assert metadata.ceil_price(12345.6) == 12346
    assert metadata.round_price(1234.55) == 1234.6


def test_legacy_scalar_rounding_is_unchanged() -> None:
    metadata = InstrumentMetadata(price_tick=0.25)
    assert metadata.floor_price(1.125) == 1.0
    assert metadata.ceil_price(1.125) == 1.25
    assert metadata.round_price(1.125) == 1.25


def _write_record(tmp_path: Path, **updates: object) -> Path:
    record: dict[str, object] = {
        "record_id": "TEST-POLICY-V1",
        "venue": "SYNTHETIC",
        "product_type": "LINEAR_TEST_CONTRACT",
        "symbol": "TEST-POLICY",
        "settlement_currency": "TEST-USD",
        "point_value": 1,
        "price_tick": None,
        "price_alignment_policy": {
            "id": "HYPERLIQUID_PX_V1",
            "significant_figures": 5,
            "perp_max_decimals": 6,
            "size_decimals": 5,
            "integer_exception": True,
            "positive_price_required": True,
        },
        "quantity_step": 1,
        "minimum_quantity": 0,
        "minimum_notional": 10,
        "contract_multiplier": 1,
        "effective_interval": {
            "start_inclusive": "2000-01-01T00:00:00Z",
            "end_exclusive": "2000-01-02T00:00:00Z",
        },
        "provenance": {"human_reviewer": "test reviewer"},
    }
    record.update(updates)
    raw = (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    path = tmp_path / "instrument.json"
    path.write_bytes(raw)
    path.with_name(path.name + ".sha256").write_text(
        hashlib.sha256(raw).hexdigest() + "\n",
        encoding="ascii",
        newline="\n",
    )
    return path


@pytest.mark.parametrize(
    "updates",
    [
        {"price_alignment_policy": {"id": "UNKNOWN"}},
        {
            "price_alignment_policy": {
                "id": "HYPERLIQUID_PX_V1",
                "significant_figures": 5,
                "perp_max_decimals": 6,
                "size_decimals": 5,
                "integer_exception": True,
            }
        },
        {"price_tick": 0.1},
    ],
    ids=["unknown", "malformed", "scalar-policy-conflict"],
)
def test_loader_refuses_unknown_malformed_or_conflicting_policy(
    tmp_path: Path,
    updates: dict[str, object],
) -> None:
    with pytest.raises(InstrumentRecordRefusal) as exc_info:
        load_verified_instrument_record(_write_record(tmp_path, **updates))
    assert exc_info.value.refusal_code == REFUSED_INCOMPLETE_INSTRUMENT_RECORD


@pytest.mark.parametrize(
    "updates",
    [
        {"minimum_quantity": None},
        {"provenance": {"human_reviewer": None}},
    ],
    ids=["minimum-quantity", "human-review"],
)
def test_policy_does_not_admit_other_incomplete_production_facts(
    tmp_path: Path,
    updates: dict[str, object],
) -> None:
    record = load_verified_instrument_record(_write_record(tmp_path, **updates))
    with pytest.raises(InstrumentRecordRefusal) as exc_info:
        record.for_evaluation("2000-01-01T00:10:00Z", {})
    assert exc_info.value.refusal_code == REFUSED_INCOMPLETE_INSTRUMENT_RECORD


def test_complete_policy_record_preserves_ten_dollar_notional(tmp_path: Path) -> None:
    record = load_verified_instrument_record(_write_record(tmp_path))
    metadata = record.for_evaluation("2000-01-01T00:10:00Z", {})
    assert metadata.min_notional == 10
    assert metadata.price_alignment_policy == POLICY
