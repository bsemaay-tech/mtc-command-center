from __future__ import annotations

import gc
import itertools
import os
import subprocess
import sys
import textwrap
from datetime import UTC, datetime
from pathlib import Path

import pytest
from pydantic import BaseModel

import bridge.engine.types as bridge_types_module
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
    assert err.reason_code == "ILLEGAL_ORDER_TRANSITION"


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
        "PARTIALLY_FILLED": OrderState.PARTIALLY_FILLED,
        "PENDING_CANCEL": OrderState.PENDING_CANCEL,
        "FILLED": OrderState.FILLED,
        "CANCELED": OrderState.CANCELED,
        "CANCELLED": OrderState.CANCELED,
        "CANCELLED_BY_ENGINE": OrderState.CANCELED,
        "REJECTED": OrderState.REJECTED,
        "EXPIRED": OrderState.EXPIRED,
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


class _LeakyRepr:
    def __repr__(self) -> str:
        return "LEAK_TOKEN_9f8e7d"


class _ExplodingRepr:
    def __repr__(self) -> str:
        raise RuntimeError("repr exploded")


def test_leaking_repr_object_fails_closed_without_leaking_into_message():
    with pytest.raises(UnknownRawOrderStatusError) as exc_info:
        normalize_raw_order_status(_LeakyRepr())
    err = exc_info.value
    assert err.reason_code == "NON_STRING_RAW_STATUS"
    assert "LEAK_TOKEN_9f8e7d" not in str(err)


def test_exploding_repr_object_still_raises_dedicated_error_not_a_repr_crash():
    with pytest.raises(UnknownRawOrderStatusError) as exc_info:
        normalize_raw_order_status(_ExplodingRepr())
    assert exc_info.value.reason_code == "NON_STRING_RAW_STATUS"


class _HostileMeta(type):
    def __getattribute__(cls, name):
        if name == "__name__":
            raise RuntimeError("metaclass name exploded")
        return super().__getattribute__(name)


class _Hostile(metaclass=_HostileMeta):
    pass


def test_hostile_metaclass_name_lookup_still_raises_dedicated_error():
    with pytest.raises(UnknownRawOrderStatusError) as exc_info:
        normalize_raw_order_status(_Hostile())
    err = exc_info.value
    assert err.reason_code == "NON_STRING_RAW_STATUS"
    assert "metaclass name exploded" not in str(err)


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


def test_no_module_level_mutable_dict_backs_the_transition_policy():
    for name, value in vars(bridge_types_module).items():
        if isinstance(value, dict) and OrderState.FILLED in value:
            pytest.fail(
                f"module-level mutable dict {name!r} is reachable and backs the "
                "transition policy; MappingProxyType alone does not freeze it"
            )


def test_no_module_level_mutable_dict_backs_the_raw_alias_policy():
    for name, value in vars(bridge_types_module).items():
        if isinstance(value, dict) and value.get("OPEN") is OrderState.OPEN:
            pytest.fail(
                f"module-level mutable dict {name!r} is reachable and backs the "
                "raw-alias policy; MappingProxyType alone does not freeze it"
            )


def test_mutating_a_copy_of_transitions_does_not_affect_can_transition():
    poisoned = dict(ORDER_STATE_TRANSITIONS)
    poisoned[OrderState.FILLED] = frozenset({OrderState.OPEN})
    assert can_transition(OrderState.FILLED, OrderState.OPEN) is False


def test_mutating_a_copy_of_raw_aliases_does_not_affect_normalization():
    poisoned = dict(RAW_ORDER_STATUS_ALIASES)
    poisoned["OPEN"] = OrderState.FILLED
    assert normalize_raw_order_status("OPEN") is OrderState.OPEN


def _transitive_gc_referents(obj, limit=200):
    """BFS over gc.get_referents, skipping type objects (classes) so the
    walk stays scoped to *data* reachable from `obj`, not the surrounding
    class/module machinery. Bounded by `limit` as a runaway-graph guard.
    """
    seen_ids = {id(obj)}
    frontier = [obj]
    collected = []
    while frontier and len(collected) < limit:
        current = frontier.pop()
        for referent in gc.get_referents(current):
            if isinstance(referent, type):
                continue
            marker = id(referent)
            if marker in seen_ids:
                continue
            seen_ids.add(marker)
            collected.append(referent)
            frontier.append(referent)
    return collected


def test_gc_referents_of_transitions_contain_no_mutable_container():
    referents = _transitive_gc_referents(ORDER_STATE_TRANSITIONS)
    mutable = [r for r in referents if isinstance(r, (dict, list, set, bytearray))]
    assert mutable == []


def test_gc_referents_of_transitions_cannot_alter_can_transition():
    before = can_transition(OrderState.FILLED, OrderState.OPEN)
    assert before is False
    for referent in _transitive_gc_referents(ORDER_STATE_TRANSITIONS):
        if isinstance(referent, dict):
            referent[OrderState.FILLED] = frozenset({OrderState.OPEN})
        if isinstance(referent, list):
            referent.append((OrderState.FILLED, frozenset({OrderState.OPEN})))
    after = can_transition(OrderState.FILLED, OrderState.OPEN)
    assert after is False


def test_gc_referents_of_raw_aliases_contain_no_mutable_container():
    referents = _transitive_gc_referents(RAW_ORDER_STATUS_ALIASES)
    mutable = [r for r in referents if isinstance(r, (dict, list, set, bytearray))]
    assert mutable == []


def test_gc_referents_of_raw_aliases_cannot_alter_normalization():
    before = normalize_raw_order_status("OPEN")
    assert before is OrderState.OPEN
    for referent in _transitive_gc_referents(RAW_ORDER_STATUS_ALIASES):
        if isinstance(referent, dict):
            referent["OPEN"] = OrderState.FILLED
        if isinstance(referent, list):
            referent.append(("OPEN", OrderState.FILLED))
    after = normalize_raw_order_status("OPEN")
    assert after is OrderState.OPEN


def test_transitions_holder_rejects_normal_attribute_assignment():
    before = can_transition(OrderState.OPEN, OrderState.FILLED)
    with pytest.raises(AttributeError):
        ORDER_STATE_TRANSITIONS._pairs = ((OrderState.OPEN, frozenset()),)
    assert can_transition(OrderState.OPEN, OrderState.FILLED) is before


def test_transitions_holder_rejects_object_setattr():
    before = can_transition(OrderState.OPEN, OrderState.FILLED)
    with pytest.raises(AttributeError):
        object.__setattr__(ORDER_STATE_TRANSITIONS, "_pairs", ((OrderState.OPEN, frozenset()),))
    assert can_transition(OrderState.OPEN, OrderState.FILLED) is before


def test_raw_aliases_holder_rejects_normal_attribute_assignment():
    before = normalize_raw_order_status("SUBMITTED")
    with pytest.raises(AttributeError):
        RAW_ORDER_STATUS_ALIASES._pairs = (("SUBMITTED", OrderState.FILLED),)
    assert normalize_raw_order_status("SUBMITTED") is before


def test_raw_aliases_holder_rejects_object_setattr():
    before = normalize_raw_order_status("SUBMITTED")
    with pytest.raises(AttributeError):
        object.__setattr__(RAW_ORDER_STATUS_ALIASES, "_pairs", (("SUBMITTED", OrderState.FILLED),))
    assert normalize_raw_order_status("SUBMITTED") is before


_CLASS_ASSIGNMENT_ATTACK = textwrap.dedent(
    """
    import sys

    import bridge.engine.types as bridge_types

    export_name, assignment_mode = sys.argv[1:]
    holder = (
        bridge_types.ORDER_STATE_TRANSITIONS
        if export_name == "transitions"
        else bridge_types.RAW_ORDER_STATUS_ALIASES
    )
    holder_type = type(holder)

    class Alternate(holder_type):
        __slots__ = ()

        def __getitem__(self, key):
            if key is bridge_types.OrderState.FILLED:
                return frozenset({bridge_types.OrderState.OPEN})
            if key == "OPEN":
                return bridge_types.OrderState.FILLED
            return holder_type.__getitem__(self, key)

    def policy_decision():
        if export_name == "transitions":
            return bridge_types.can_transition(
                bridge_types.OrderState.FILLED,
                bridge_types.OrderState.OPEN,
            )
        return bridge_types.normalize_raw_order_status("OPEN")

    before_decision = policy_decision()
    try:
        if assignment_mode == "plain":
            holder.__class__ = Alternate
        else:
            object.__setattr__(holder, "__class__", Alternate)
    except AttributeError:
        pass
    else:
        raise AssertionError("policy holder accepted __class__ replacement")

    assert type(holder) is holder_type
    assert policy_decision() == before_decision
    """
)


@pytest.mark.parametrize("export_name", ["transitions", "aliases"])
@pytest.mark.parametrize("assignment_mode", ["plain", "object_setattr"])
def test_policy_holder_rejects_class_assignment(export_name, assignment_mode):
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, "-c", _CLASS_ASSIGNMENT_ATTACK, export_name, assignment_mode],
        cwd=Path(__file__).resolve().parents[1],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


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


# ===========================================================================
# TS-P1-004 — canonical state wired by quantity, partial-recovery machine
# ===========================================================================

from bridge.engine.types import (  # noqa: E402
    PARTIAL_ACCEPTING_STATES,
    PARTIAL_STATE_TRANSITIONS,
    PARTIAL_TERMINAL_STATES,
    ActionOutcome,
    IllegalPartialTransitionError,
    LotQuantizationError,
    LotUnit,
    PartialActionKind,
    PartialProtectionState,
    Provenance,
    canonical_order_state,
    can_transition_partial,
    quantize_lots,
    validate_partial_transition,
)

ALL_PARTIAL_STATES = tuple(PartialProtectionState)


def test_partial_protection_states_are_the_declared_ten():
    assert len(ALL_PARTIAL_STATES) == 10
    assert {state.value for state in ALL_PARTIAL_STATES} == {
        "PARTIAL_DETECTED", "PROTECTION_PENDING", "PROTECTION_VERIFIED",
        "PROTECTED_PARTIAL", "CANCEL_PENDING", "CANCEL_UNKNOWN",
        "FLATTEN_PENDING", "FLATTEN_UNKNOWN", "SAFE_FLAT", "UNPROTECTED_ABORT",
    }


def test_partial_transition_table_covers_every_state():
    assert set(PARTIAL_STATE_TRANSITIONS) == set(ALL_PARTIAL_STATES)


@pytest.mark.parametrize("state", ALL_PARTIAL_STATES)
def test_partial_self_loop_is_always_legal_idempotent_replay(state):
    assert can_transition_partial(state, state)


def test_partial_terminal_and_accepting_sets():
    assert PARTIAL_ACCEPTING_STATES == frozenset({
        PartialProtectionState.PROTECTED_PARTIAL, PartialProtectionState.SAFE_FLAT
    })
    assert PARTIAL_TERMINAL_STATES == PARTIAL_ACCEPTING_STATES | frozenset({
        PartialProtectionState.UNPROTECTED_ABORT
    })


@pytest.mark.parametrize(
    "state",
    [PartialProtectionState.SAFE_FLAT, PartialProtectionState.UNPROTECTED_ABORT],
)
def test_final_states_forbid_resurrection(state):
    assert PARTIAL_STATE_TRANSITIONS[state] == frozenset({state})


def test_protected_partial_only_reopens_for_a_late_fill():
    assert PARTIAL_STATE_TRANSITIONS[PartialProtectionState.PROTECTED_PARTIAL] == (
        frozenset({
            PartialProtectionState.PROTECTED_PARTIAL,
            PartialProtectionState.PARTIAL_DETECTED,
        })
    )


@pytest.mark.parametrize(
    "source",
    [
        PartialProtectionState.PROTECTION_VERIFIED,
        PartialProtectionState.PROTECTED_PARTIAL,
        PartialProtectionState.CANCEL_PENDING,
        PartialProtectionState.CANCEL_UNKNOWN,
    ],
)
def test_late_fill_can_requantify_from_the_documented_states(source):
    assert can_transition_partial(source, PartialProtectionState.PARTIAL_DETECTED)


@pytest.mark.parametrize(
    ("a", "b"),
    [
        (PartialProtectionState.PARTIAL_DETECTED, PartialProtectionState.PROTECTED_PARTIAL),
        (PartialProtectionState.PARTIAL_DETECTED, PartialProtectionState.SAFE_FLAT),
        (PartialProtectionState.PROTECTION_PENDING, PartialProtectionState.PROTECTED_PARTIAL),
        (PartialProtectionState.FLATTEN_PENDING, PartialProtectionState.PARTIAL_DETECTED),
        (PartialProtectionState.UNPROTECTED_ABORT, PartialProtectionState.SAFE_FLAT),
    ],
)
def test_representative_illegal_partial_edges(a, b):
    assert not can_transition_partial(a, b)
    with pytest.raises(IllegalPartialTransitionError):
        validate_partial_transition(a, b)


def test_illegal_partial_transition_error_is_structured():
    with pytest.raises(IllegalPartialTransitionError) as exc_info:
        validate_partial_transition(
            PartialProtectionState.SAFE_FLAT, PartialProtectionState.PARTIAL_DETECTED
        )
    err = exc_info.value
    assert err.reason_code == "ILLEGAL_PARTIAL_TRANSITION"
    assert err.from_state is PartialProtectionState.SAFE_FLAT
    assert err.to_state is PartialProtectionState.PARTIAL_DETECTED


def test_partial_policy_table_is_immutable():
    with pytest.raises(TypeError):
        PARTIAL_STATE_TRANSITIONS[PartialProtectionState.SAFE_FLAT] = frozenset()


def test_partial_enums_are_closed_vocabularies():
    assert {kind.value for kind in PartialActionKind} == {
        "INSTALL_STOP", "CANCEL_ENTRY", "CANCEL_PROTECTION", "FLATTEN"
    }
    assert {outcome.value for outcome in ActionOutcome} == {
        "APPLIED", "NOT_APPLIED", "UNKNOWN"
    }
    assert {p.value for p in Provenance} == {
        "OWNED", "MIXED", "FOREIGN", "AMBIGUOUS", "UNVERIFIED"
    }


# --- canonical order state derived from durable quantities ----------------


@pytest.mark.parametrize(
    ("raw", "ordered", "filled", "expected"),
    [
        ("OPEN", 2.0, 0.0, OrderState.OPEN),
        ("OPEN", 2.0, 0.5, OrderState.PARTIALLY_FILLED),
        ("OPEN", 2.0, 1.999, OrderState.PARTIALLY_FILLED),
        ("OPEN", 2.0, 2.0, OrderState.FILLED),
        ("SUBMITTED", 2.0, 1.0, OrderState.PARTIALLY_FILLED),
        ("PENDING", 2.0, 1.0, OrderState.PARTIALLY_FILLED),
        ("FILLED", 2.0, 1.0, OrderState.FILLED),
        ("CANCELLED_BY_ENGINE", 2.0, 1.0, OrderState.CANCELED),
    ],
)
def test_canonical_order_state_by_quantity(raw, ordered, filled, expected):
    assert (
        canonical_order_state(
            raw_status=raw, ordered_qty=ordered, filled_qty=filled, lot=LotUnit(3)
        )
        is expected
    )


def test_canonical_order_state_pending_cancel_only_while_live():
    assert (
        canonical_order_state(
            raw_status="OPEN", ordered_qty=2.0, filled_qty=1.0,
            lot=LotUnit(3), cancel_reserved=True,
        )
        is OrderState.PENDING_CANCEL
    )
    assert (
        canonical_order_state(
            raw_status="CANCELLED_BY_ENGINE", ordered_qty=2.0, filled_qty=1.0,
            lot=LotUnit(3), cancel_reserved=True,
        )
        is OrderState.CANCELED
    )


def test_canonical_order_state_fails_closed_on_unknown_raw_status():
    with pytest.raises(UnknownRawOrderStatusError):
        canonical_order_state(raw_status="BOGUS", ordered_qty=2.0, filled_qty=1.0)


def test_canonical_order_state_fails_closed_on_non_lot_quantities():
    with pytest.raises(LotQuantizationError):
        canonical_order_state(
            raw_status="OPEN", ordered_qty=2.0, filled_qty=0.00001, lot=LotUnit(3)
        )


def test_canonical_order_state_rejects_non_positive_order_quantity():
    with pytest.raises(LotQuantizationError):
        canonical_order_state(raw_status="OPEN", ordered_qty=0.0, filled_qty=0.0)


def test_canonical_order_state_agrees_with_the_declared_transition_table():
    """Every derived state must be reachable from its raw base state."""
    for raw, base in RAW_ORDER_STATUS_ALIASES.items():
        if base in TERMINAL_ORDER_STATES:
            continue
        derived = canonical_order_state(
            raw_status=raw, ordered_qty=2.0, filled_qty=1.0, lot=LotUnit(3)
        )
        assert can_transition(base, derived)


def test_partial_fill_edges_exist_in_the_order_state_table():
    assert can_transition(OrderState.OPEN, OrderState.PARTIALLY_FILLED)
    assert can_transition(OrderState.PARTIALLY_FILLED, OrderState.PENDING_CANCEL)
    assert can_transition(OrderState.PENDING_CANCEL, OrderState.FILLED)
    assert not can_transition(OrderState.PARTIALLY_FILLED, OrderState.OPEN)


def test_lot_quantum_is_required_to_be_valid():
    with pytest.raises(LotQuantizationError):
        LotUnit(-1)
    assert quantize_lots(1.5, LotUnit(2)) == 150
