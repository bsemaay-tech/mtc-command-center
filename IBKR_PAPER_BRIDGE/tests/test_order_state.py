from __future__ import annotations

import itertools
from datetime import UTC, datetime

import pytest
from pydantic import BaseModel

from bridge.engine.types import (
    AccountSnapshot,
    Bar,
    BrokerEvent,
    BrokerOrder,
    FillEvent,
    IllegalOrderTransitionError,
    OrderPlan,
    OrderState,
    OrderUpdateEvent,
    ORDER_STATE_TRANSITIONS,
    Position,
    RAW_ORDER_STATUS_ALIASES,
    RegimeDirective,
    Rejection,
    Signal,
    TERMINAL_ORDER_STATES,
    UnknownRawOrderStatusError,
    can_transition,
    normalize_raw_order_status,
    validate_order_transition,
)

ALL_STATES = tuple(OrderState)

EXPECTED_TRANSITIONS: dict[OrderState, set[OrderState]] = {
    OrderState.PENDING_NEW: {OrderState.PENDING_NEW, OrderState.SUBMITTING},
    OrderState.SUBMITTING: {
        OrderState.SUBMITTING,
        OrderState.SUBMITTED,
        OrderState.REJECTED,
        OrderState.UNKNOWN_SUBMISSION,
    },
    OrderState.SUBMITTED: {
        OrderState.SUBMITTED,
        OrderState.OPEN,
        OrderState.REJECTED,
        OrderState.FILLED,
        OrderState.PARTIALLY_FILLED,
        OrderState.EXPIRED,
        OrderState.PENDING_CANCEL,
        OrderState.CANCELED,
    },
    OrderState.OPEN: {
        OrderState.OPEN,
        OrderState.PARTIALLY_FILLED,
        OrderState.FILLED,
        OrderState.PENDING_CANCEL,
        OrderState.CANCELED,
        OrderState.EXPIRED,
    },
    OrderState.PARTIALLY_FILLED: {
        OrderState.PARTIALLY_FILLED,
        OrderState.FILLED,
        OrderState.PENDING_CANCEL,
        OrderState.CANCELED,
        OrderState.EXPIRED,
    },
    OrderState.PENDING_CANCEL: {
        OrderState.PENDING_CANCEL,
        OrderState.CANCELED,
        OrderState.FILLED,
        OrderState.PARTIALLY_FILLED,
        OrderState.OPEN,
        OrderState.EXPIRED,
    },
    OrderState.UNKNOWN_SUBMISSION: {
        OrderState.UNKNOWN_SUBMISSION,
        OrderState.SUBMITTED,
        OrderState.OPEN,
        OrderState.PARTIALLY_FILLED,
        OrderState.PENDING_CANCEL,
        OrderState.FILLED,
        OrderState.CANCELED,
        OrderState.REJECTED,
        OrderState.EXPIRED,
    },
    OrderState.FILLED: {OrderState.FILLED},
    OrderState.CANCELED: {OrderState.CANCELED},
    OrderState.REJECTED: {OrderState.REJECTED},
    OrderState.EXPIRED: {OrderState.EXPIRED},
}


class _StatusHolder(BaseModel):
    status: OrderState


def test_all_eleven_states_declared():
    assert len(ALL_STATES) == 11
    assert set(EXPECTED_TRANSITIONS) == set(ALL_STATES)


def test_exhaustive_all_pairs_agree_with_declared_relation():
    for a, b in itertools.product(ALL_STATES, repeat=2):
        expected = b in EXPECTED_TRANSITIONS[a]
        assert can_transition(a, b) is expected, f"{a} -> {b} expected {expected}"


def test_total_legal_transition_count_is_44_including_self_loops():
    total = sum(len(edges) for edges in ORDER_STATE_TRANSITIONS.values())
    assert total == 44
    non_self = sum(
        1 for a, b in itertools.product(ALL_STATES, repeat=2) if a is not b and can_transition(a, b)
    )
    assert non_self == 33


@pytest.mark.parametrize("state", ALL_STATES)
def test_same_state_is_always_legal_idempotent_replay(state):
    assert can_transition(state, state) is True
    assert validate_order_transition(state, state) == state


def test_terminal_state_set_is_exactly_four():
    assert TERMINAL_ORDER_STATES == frozenset(
        {OrderState.FILLED, OrderState.CANCELED, OrderState.REJECTED, OrderState.EXPIRED}
    )


@pytest.mark.parametrize("state", sorted(TERMINAL_ORDER_STATES, key=lambda s: s.value))
def test_terminal_states_forbid_resurrection(state):
    for other in ALL_STATES:
        if other is state:
            continue
        assert can_transition(state, other) is False
        with pytest.raises(IllegalOrderTransitionError):
            validate_order_transition(state, other)


@pytest.mark.parametrize("illegal_target", [OrderState.PENDING_NEW, OrderState.SUBMITTING])
def test_unknown_submission_forbids_blind_retry(illegal_target):
    assert can_transition(OrderState.UNKNOWN_SUBMISSION, illegal_target) is False
    with pytest.raises(IllegalOrderTransitionError):
        validate_order_transition(OrderState.UNKNOWN_SUBMISSION, illegal_target)


def test_unknown_submission_resolves_via_reconciliation_evidence():
    resolvable = {
        OrderState.SUBMITTED,
        OrderState.OPEN,
        OrderState.PARTIALLY_FILLED,
        OrderState.PENDING_CANCEL,
        OrderState.FILLED,
        OrderState.CANCELED,
        OrderState.REJECTED,
        OrderState.EXPIRED,
    }
    for target in resolvable:
        assert can_transition(OrderState.UNKNOWN_SUBMISSION, target) is True


def test_partial_fill_cannot_regress_to_ordinary_lower_progress_state():
    forbidden = {OrderState.PENDING_NEW, OrderState.SUBMITTING, OrderState.SUBMITTED, OrderState.OPEN}
    for target in forbidden:
        assert can_transition(OrderState.PARTIALLY_FILLED, target) is False


def test_pending_cancel_still_receives_authoritative_fill_and_terminal_outcomes():
    assert can_transition(OrderState.PENDING_CANCEL, OrderState.FILLED) is True
    assert can_transition(OrderState.PENDING_CANCEL, OrderState.CANCELED) is True
    assert can_transition(OrderState.PENDING_CANCEL, OrderState.EXPIRED) is True
    assert can_transition(OrderState.PENDING_CANCEL, OrderState.PARTIALLY_FILLED) is True


def test_pending_cancel_race_can_revert_to_open_on_cancel_reject():
    assert can_transition(OrderState.PENDING_CANCEL, OrderState.OPEN) is True


@pytest.mark.parametrize(
    "a,b",
    [
        (OrderState.PENDING_NEW, OrderState.SUBMITTING),
        (OrderState.SUBMITTING, OrderState.SUBMITTED),
        (OrderState.SUBMITTING, OrderState.REJECTED),
        (OrderState.SUBMITTING, OrderState.UNKNOWN_SUBMISSION),
        (OrderState.SUBMITTED, OrderState.OPEN),
        (OrderState.OPEN, OrderState.PARTIALLY_FILLED),
        (OrderState.OPEN, OrderState.CANCELED),
        (OrderState.PARTIALLY_FILLED, OrderState.FILLED),
    ],
)
def test_representative_legal_edges(a, b):
    assert can_transition(a, b) is True
    assert validate_order_transition(a, b) == b


@pytest.mark.parametrize(
    "a,b",
    [
        (OrderState.PENDING_NEW, OrderState.OPEN),
        (OrderState.PENDING_NEW, OrderState.FILLED),
        (OrderState.OPEN, OrderState.PENDING_NEW),
        (OrderState.OPEN, OrderState.SUBMITTING),
        (OrderState.FILLED, OrderState.OPEN),
        (OrderState.CANCELED, OrderState.OPEN),
        (OrderState.REJECTED, OrderState.SUBMITTING),
        (OrderState.EXPIRED, OrderState.FILLED),
    ],
)
def test_representative_illegal_edges(a, b):
    assert can_transition(a, b) is False
    with pytest.raises(IllegalOrderTransitionError):
        validate_order_transition(a, b)


def test_illegal_transition_error_is_structured():
    with pytest.raises(IllegalOrderTransitionError) as exc_info:
        validate_order_transition(OrderState.FILLED, OrderState.OPEN)
    err = exc_info.value
    assert err.from_state is OrderState.FILLED
    assert err.to_state is OrderState.OPEN


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("OPEN", OrderState.OPEN),
        ("SUBMITTED", OrderState.SUBMITTED),
        ("PENDING", OrderState.SUBMITTED),
        ("FILLED", OrderState.FILLED),
        ("CANCELLED_BY_ENGINE", OrderState.CANCELED),
        (" open ", OrderState.OPEN),
        ("open", OrderState.OPEN),
        ("Filled", OrderState.FILLED),
    ],
)
def test_known_raw_status_aliases_normalize(raw, expected):
    assert normalize_raw_order_status(raw) is expected


def test_raw_alias_table_matches_documented_inventory():
    expected = {
        "OPEN": OrderState.OPEN,
        "SUBMITTED": OrderState.SUBMITTED,
        "PENDING": OrderState.SUBMITTED,
        "FILLED": OrderState.FILLED,
        "CANCELLED_BY_ENGINE": OrderState.CANCELED,
    }
    assert dict(RAW_ORDER_STATUS_ALIASES) == expected


@pytest.mark.parametrize("raw", ["BOGUS", "", "  ", "OPENN", "waitingForFill", "WAITING_CHILD"])
def test_unknown_or_malformed_raw_status_fails_closed(raw):
    with pytest.raises(UnknownRawOrderStatusError):
        normalize_raw_order_status(raw)


@pytest.mark.parametrize("raw", [True, False, None, 123, 1.5, b"OPEN", ["OPEN"], {"status": "OPEN"}])
def test_non_string_raw_status_fails_closed_not_bypassed(raw):
    with pytest.raises(UnknownRawOrderStatusError):
        normalize_raw_order_status(raw)


def test_unknown_raw_status_error_is_structured_with_reason_code():
    with pytest.raises(UnknownRawOrderStatusError) as exc_info:
        normalize_raw_order_status("TOTALLY_UNRECOGNIZED")
    err = exc_info.value
    assert err.raw == "TOTALLY_UNRECOGNIZED"
    assert isinstance(err.reason_code, str) and err.reason_code


def test_transition_map_values_are_frozensets_immutable_to_callers():
    edges = ORDER_STATE_TRANSITIONS[OrderState.OPEN]
    assert isinstance(edges, frozenset)
    with pytest.raises(AttributeError):
        edges.add(OrderState.REJECTED)


def test_transition_map_itself_is_read_only():
    with pytest.raises(TypeError):
        ORDER_STATE_TRANSITIONS[OrderState.OPEN] = frozenset()


def test_raw_alias_table_is_read_only():
    with pytest.raises(TypeError):
        RAW_ORDER_STATUS_ALIASES["OPEN"] = OrderState.FILLED


def test_can_transition_and_validate_are_pure_no_mutation():
    before = {state: frozenset(edges) for state, edges in ORDER_STATE_TRANSITIONS.items()}
    for _ in range(3):
        for a, b in itertools.product(ALL_STATES, repeat=2):
            can_transition(a, b)
            try:
                validate_order_transition(a, b)
            except IllegalOrderTransitionError:
                pass
    after = {state: frozenset(edges) for state, edges in ORDER_STATE_TRANSITIONS.items()}
    assert before == after


def test_order_state_string_equality_and_value_roundtrip():
    assert OrderState.OPEN == "OPEN"
    assert OrderState("OPEN") is OrderState.OPEN
    assert OrderState.OPEN.value == "OPEN"


def test_order_state_pydantic_json_roundtrip():
    holder = _StatusHolder(status=OrderState.PARTIALLY_FILLED)
    dumped = holder.model_dump_json()
    assert "PARTIALLY_FILLED" in dumped
    restored = _StatusHolder.model_validate_json(dumped)
    assert restored.status is OrderState.PARTIALLY_FILLED


def test_order_state_accepts_plain_string_in_pydantic_model():
    holder = _StatusHolder.model_validate({"status": "FILLED"})
    assert holder.status is OrderState.FILLED


def test_existing_models_remain_constructible_and_backward_compatible():
    ts = datetime(2026, 7, 20, 12, 0, tzinfo=UTC)
    signal = Signal(ts=ts, symbol="BTC", direction="LONG", reason="test", ref_price=100.0)
    plan = OrderPlan(signal=signal, qty=1.0, entry_type="MKT", stop_loss=90.0)
    assert plan.signal.symbol == "BTC"

    order = BrokerOrder(cloid="c1", coin="BTC", side="BUY", size=1.0)
    assert order.status == "OPEN"

    bar = Bar(ts=ts, open=1.0, high=2.0, low=0.5, close=1.5, volume=10.0)
    assert bar.close == 1.5

    position = Position(symbol="BTC", size=1.0, entry_px=100.0)
    assert position.leverage == 1

    account = AccountSnapshot(equity=1000.0, available_margin=1000.0)
    assert account.withdrawable == 0.0

    fill = FillEvent(fill_id="f1", cloid="c1", coin="BTC", qty=1.0, px=100.0, ts=ts)
    update = OrderUpdateEvent(cloid="c1", status="OPEN", ts=ts)
    event: BrokerEvent = fill
    assert event.event_type == "FILL"
    assert update.event_type == "ORDER"

    rejection = Rejection(stage="RISK", reason="test")
    assert rejection.stage == "RISK"

    regime = RegimeDirective(
        ts=ts, regime="BOTH", confidence=0.9, ttl_minutes=60, sources=["x"], rationale="test"
    )
    assert regime.regime == "BOTH"
