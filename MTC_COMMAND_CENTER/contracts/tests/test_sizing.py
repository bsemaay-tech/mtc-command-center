from datetime import UTC, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from mtc_contracts import (
    BoundSizingIntent,
    SizingMethod,
    SizingRequest,
    SizingSourceClass,
    VolatilityTargetParams,
)

BASE = {
    "instrument_metadata_hash": "1" * 64,
    "kernel_version": "kernel-0.1.0",
    "package_hash": "2" * 64,
    "decision_bar_ts": datetime(2026, 8, 24, tzinfo=UTC),
    "entry_reference_price": Decimal(100),
    "direction": "LONG",
    "sizing_source_class": SizingSourceClass.NATIVE_DECLARED,
}


@pytest.mark.parametrize(
    ("method", "field", "value"),
    [
        (SizingMethod.RISK_AT_STOP, "requested_risk_fraction", Decimal("0.01")),
        (SizingMethod.FIXED_QTY, "requested_fixed_qty", Decimal(2)),
        (SizingMethod.FIXED_NOTIONAL, "requested_fixed_notional", Decimal(250)),
        (
            SizingMethod.VOLATILITY_TARGET,
            "vol_target_params",
            VolatilityTargetParams(
                target_volatility=Decimal("0.10"), estimator_id="ewma-20"
            ),
        ),
    ],
)
def test_each_normalized_method_accepts_exactly_its_request_constant(
    method, field, value
):
    payload = {**BASE, "sizing_method": method, field: value}
    if method is SizingMethod.RISK_AT_STOP:
        payload["stop_price"] = Decimal(95)
    request = SizingRequest.model_validate(payload)
    assert getattr(request, field) == value


def test_sizing_method_is_exactly_the_four_normalized_values():
    assert {item.value for item in SizingMethod} == {
        "RISK_AT_STOP",
        "FIXED_QTY",
        "FIXED_NOTIONAL",
        "VOLATILITY_TARGET",
    }
    with pytest.raises(ValidationError):
        SizingRequest.model_validate(
            {**BASE, "sizing_method": "SOURCE_DEFINED", "source_defined_request": {}}
        )


@pytest.mark.parametrize(
    "forbidden",
    [
        "snapshot_id",
        "allocation_policy_version",
        "account_equity",
        "bucket_capital",
        "proposed_qty",
        "authorized_qty",
        "final_qty",
        "notional_result",
    ],
)
def test_snapshot_account_and_result_fields_are_rejected(forbidden):
    payload = {
        **BASE,
        "sizing_method": "FIXED_QTY",
        "requested_fixed_qty": Decimal(2),
        forbidden: "forbidden",
    }
    with pytest.raises(ValidationError):
        SizingRequest.model_validate(payload)


def test_request_field_must_match_method_and_be_the_only_request_value():
    with pytest.raises(ValidationError):
        SizingRequest.model_validate(
            {
                **BASE,
                "sizing_method": "FIXED_QTY",
                "requested_fixed_notional": Decimal(100),
            }
        )
    with pytest.raises(ValidationError):
        SizingRequest.model_validate(
            {
                **BASE,
                "sizing_method": "FIXED_QTY",
                "requested_fixed_qty": Decimal(1),
                "requested_fixed_notional": Decimal(100),
            }
        )


def test_source_defined_is_provenance_only_on_a_compiled_native_request():
    request = SizingRequest.model_validate(
        {
            **BASE,
            "sizing_source_class": "SOURCE_DEFINED",
            "source_rule_id": "source-rule-7",
            "source_rule_provenance": "video-transcript:sha256:abc",
            "sizing_method": "FIXED_QTY",
            "requested_fixed_qty": Decimal(2),
        }
    )
    assert request.sizing_method is SizingMethod.FIXED_QTY
    assert request.sizing_source_class is SizingSourceClass.SOURCE_DEFINED
    assert "substitute" not in request.model_dump()


def test_bound_intent_preserves_the_complete_request_and_only_binds_identity():
    request = SizingRequest.model_validate(
        {**BASE, "sizing_method": "FIXED_QTY", "requested_fixed_qty": Decimal(2)}
    )
    bound = BoundSizingIntent(
        request=request,
        snapshot_id="3" * 64,
        snapshot_taken_at=datetime(2026, 8, 24, tzinfo=UTC),
        snapshot_deadline_ms=None,
        allocation_policy_version="allocation-0.1.0",
        bucket_id="bucket-1",
        deployment_identity_hash="4" * 64,
    )
    assert bound.request == request
    assert bound.snapshot_deadline_ms is None
    assert "fail-closed" in (BoundSizingIntent.__doc__ or "").lower()
