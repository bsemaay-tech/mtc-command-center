from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from mtc_v2.core.instrument import (
    REFUSED_INCOMPLETE_INSTRUMENT_RECORD,
    InstrumentMetadata,
    InstrumentRecordRefusal,
    load_verified_instrument_record,
)
from mtc_v2.core.economics import _fill_price
from mtc_v2.core.exits import (
    build_working_exit_book,
    calc_sl,
    update_protective_stop_owner,
)
from mtc_v2.core.rounding import (
    PriceAlignmentPolicy,
    align_price_to_policy,
    is_valid_price,
)
from mtc_v2.core.types import Bar, Position


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
        (1000.05, 1000, 1000.1, 1000.1),
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


@pytest.mark.parametrize(
    "value",
    [True, 0.0, -1.0, float("inf"), float("-inf"), float("nan")],
)
def test_policy_alignment_refuses_invalid_nonpositive_or_nonfinite_input(
    value: object,
) -> None:
    assert is_valid_price(value, POLICY) is False  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        align_price_to_policy(value, POLICY, "HALF_UP")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "updates",
    [
        {"id": 1},
        {"id": "UNKNOWN"},
        {"significant_figures": True},
        {"significant_figures": 4},
        {"perp_max_decimals": 6.0},
        {"size_decimals": False},
        {"integer_exception": 1},
        {"positive_price_required": 1},
    ],
)
def test_direct_policy_constructor_refuses_invalid_field_types(
    updates: dict[str, object],
) -> None:
    values: dict[str, object] = {
        "id": "HYPERLIQUID_PX_V1",
        "significant_figures": 5,
        "perp_max_decimals": 6,
        "size_decimals": 5,
        "integer_exception": True,
        "positive_price_required": True,
    }
    values.update(updates)
    with pytest.raises(ValueError):
        PriceAlignmentPolicy(**values)  # type: ignore[arg-type]


def test_policy_mapping_refuses_extra_fields() -> None:
    raw: dict[str, object] = {
        "id": "HYPERLIQUID_PX_V1",
        "significant_figures": 5,
        "perp_max_decimals": 6,
        "size_decimals": 5,
        "integer_exception": True,
        "positive_price_required": True,
        "extra": "forbidden",
    }
    with pytest.raises(ValueError):
        PriceAlignmentPolicy.from_mapping(raw)


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


def test_corrected_fill_stop_and_target_dispatch_policy() -> None:
    metadata = InstrumentMetadata(price_tick=None, price_alignment_policy=POLICY)
    fill, _bps, _impact, alignment = _fill_price(
        reference=12345.6,
        action_side="BUY",
        instrument=metadata,
        cost={
            "slippage_model_id": "BPS_OF_REFERENCE_V1",
            "slippage_parameters": {"slippage_bps": 0},
        },
    )
    assert (fill, alignment) == (12346, "CEIL")

    stop = calc_sl(
        {"use_sl": True, "use_sl_atr": True, "sl_atr_mult": 1},
        bar=Bar(
            timestamp=datetime(2000, 1, 1, tzinfo=timezone.utc),
            open=12350.6,
            high=12350.6,
            low=12345.6,
            close=12350.6,
            volume=1,
            bar_index=0,
        ),
        entry_price=12350.6,
        is_long=True,
        price_tick=None,
        price_alignment_policy=POLICY,
        atr_value=5,
    )
    assert stop == 12345

    target, exits = build_working_exit_book(
        {"tp_mode": "ATR", "tp_atr_mult": 1},
        entry_price=12340,
        is_long=True,
        price_tick=None,
        price_alignment_policy=POLICY,
        atr_value=5.6,
        book_version=1,
    )
    assert target == 12346
    assert exits[0].target_price == 12346


@pytest.mark.parametrize("owner", ["trail", "break_even"])
def test_trailing_and_break_even_dispatch_policy(owner: str) -> None:
    position = Position(
        side="long",
        entry_price=12345.6,
        avg_entry_price=12345.6,
        qty=1,
        entry_bar=0,
        active_stop_price=12000,
        initial_risk_per_unit=1,
    )
    config: dict[str, object] = {
        "execution_profile_id": "",
        "use_trailing": owner == "trail",
        "trail_start_r": 0,
        "trail_distance_atr_mult": 0,
        "use_break_even": owner == "break_even",
        "be_trigger_r": 0,
        "be_buffer_r": 0,
    }
    update_protective_stop_owner(
        config,
        position=position,
        bar=Bar(
            timestamp=datetime(2000, 1, 1, tzinfo=timezone.utc),
            open=12345.6,
            high=12345.6,
            low=12345.6,
            close=12345.6,
            volume=1,
            bar_index=0,
        ),
        price_tick=None,
        price_alignment_policy=POLICY,
        trail_atr=1,
    )
    assert position.active_stop_price == 12345


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
    ("updates", "expected_field"),
    [
        ({"minimum_quantity": None}, "minimum_quantity"),
        ({"provenance": {"human_reviewer": None}}, "provenance.human_reviewer"),
    ],
    ids=["minimum-quantity", "human-review"],
)
def test_policy_does_not_admit_other_incomplete_production_facts(
    tmp_path: Path,
    updates: dict[str, object],
    expected_field: str,
) -> None:
    record = load_verified_instrument_record(_write_record(tmp_path, **updates))
    with pytest.raises(InstrumentRecordRefusal) as exc_info:
        record.for_evaluation("2000-01-01T00:10:00Z", {})
    assert exc_info.value.refusal_code == REFUSED_INCOMPLETE_INSTRUMENT_RECORD
    assert expected_field in str(exc_info.value)


def test_complete_policy_record_preserves_ten_dollar_notional(tmp_path: Path) -> None:
    record = load_verified_instrument_record(_write_record(tmp_path))
    metadata = record.for_evaluation("2000-01-01T00:10:00Z", {})
    assert metadata.min_notional == 10
    assert metadata.price_alignment_policy == POLICY
