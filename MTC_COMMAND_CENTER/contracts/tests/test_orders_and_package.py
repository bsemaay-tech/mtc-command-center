from datetime import UTC, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from mtc_contracts import (
    AccountSnapshot,
    Authorization,
    ExitIntent,
    InstrumentMetadata,
    OrderIntent,
    StrategyPackage,
    TakeProfitLeg,
)


def valid_order(**changes):
    payload = {
        "intent_id": "intent-1",
        "candidate_id": "QLC-20260824-1234abcd",
        "package_hash": "1" * 64,
        "deployment_identity_hash": "2" * 64,
        "worker_id": "worker-1",
        "revision": 0,
        "decision_bar_ts": datetime(2026, 8, 24, tzinfo=UTC),
        "emitted_at": datetime(2026, 8, 24, 0, 0, 1, tzinfo=UTC),
        "valid_until_bar_ts": datetime(2026, 8, 24, 1, tzinfo=UTC),
        "action": "OPEN",
        "direction": "LONG",
        "authorized_qty": Decimal(2),
        "qty_semantics": "DELTA",
        "qty_unit": "base",
        "authorization": "AUTHORIZED_AS_REQUESTED",
        "allocation_policy_version": "allocation-v1",
        "snapshot_id": "3" * 64,
        "stop_price": Decimal(95),
        "stop_semantics": "STRATEGY_NATIVE",
        "tp_legs": [
            TakeProfitLeg(
                leg_id="tp1",
                price=Decimal(110),
                qty_fraction=Decimal(1),
                activation="IMMEDIATE",
                oco_group="oco-1",
            )
        ],
        "entry_reason": "breakout",
        "blocked_by": [],
    }
    payload.update(changes)
    return payload


def test_authorized_order_has_exact_quantity_and_no_resize_state():
    order = OrderIntent.model_validate(valid_order())
    assert order.authorization is Authorization.AUTHORIZED_AS_REQUESTED
    assert order.authorized_qty == Decimal(2)
    with pytest.raises(ValidationError):
        OrderIntent.model_validate(valid_order(authorization="RESIZED"))


def test_rejected_order_has_reason_and_no_executable_quantity():
    order = OrderIntent.model_validate(
        valid_order(
            authorization="REJECTED",
            authorized_qty=None,
            rejection_reason="BUCKET_LIMIT",
        )
    )
    assert order.authorized_qty is None
    with pytest.raises(ValidationError):
        OrderIntent.model_validate(valid_order(authorization="REJECTED"))


def test_exit_intent_is_explicitly_reduce_only():
    intent = ExitIntent(
        intent_id="exit-1",
        candidate_id="QLC-20260824-1234abcd",
        package_hash="1" * 64,
        deployment_identity_hash="2" * 64,
        worker_id="worker-1",
        revision=0,
        decision_bar_ts=datetime(2026, 8, 24, tzinfo=UTC),
        emitted_at=datetime(2026, 8, 24, tzinfo=UTC),
        valid_until_bar_ts=datetime(2026, 8, 24, 1, tzinfo=UTC),
        action="MODIFY_STOP",
        direction="LONG",
        requested_price=Decimal(98),
        requested_qty=None,
        qty_semantics="TARGET_TOTAL",
        reduce_only=True,
        reason="tighten break-even",
    )
    assert intent.reduce_only is True
    with pytest.raises(ValidationError):
        ExitIntent.model_validate({**intent.model_dump(), "reduce_only": False})


def test_strategy_package_and_account_snapshot_are_frozen_identity_bound_shapes():
    metadata = InstrumentMetadata(
        symbol="BTCUSDT",
        tick_size=Decimal("0.10"),
        lot_size=Decimal("0.001"),
        min_qty=Decimal("0.001"),
        min_notional=Decimal(5),
        contract_multiplier=Decimal(1),
    )
    package = StrategyPackage(
        candidate_id="QLC-20260824-1234abcd",
        family_id="FAM-1234abcd1234abcd",
        package_hash="1" * 64,
        kernel_version="kernel-v1",
        kernel_code_sha="2" * 64,
        spec={},
        exact_params={},
        modules_enabled=["stop"],
        substitute_catalogue_versions={},
        instrument_metadata=metadata,
        bar_close_only=True,
        degraded_policy=None,
    )
    snapshot = AccountSnapshot(
        snapshot_id="3" * 64,
        taken_at=datetime(2026, 8, 24, tzinfo=UTC),
        account_id="paper-1",
        equity=Decimal(10000),
        available_margin=Decimal(8000),
        bucket_capital={"bucket-1": Decimal(5000)},
        open_exposure=Decimal(1000),
        margin_used=Decimal(200),
    )
    assert package.instrument_metadata.symbol == "BTCUSDT"
    assert snapshot.snapshot_id == "3" * 64
    with pytest.raises(ValidationError):
        package.package_hash = "4" * 64
