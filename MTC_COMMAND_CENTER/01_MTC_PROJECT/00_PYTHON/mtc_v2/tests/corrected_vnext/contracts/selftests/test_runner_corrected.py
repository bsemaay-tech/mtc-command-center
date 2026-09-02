from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from datetime import datetime
from pathlib import Path

import pytest

from mtc_v2.core.economics import EconomicsRefusal
from mtc_v2.core.runner import Runner
from mtc_v2.core.types import Bar, EntryLeg, Position, RawSignal


MTC_V2_ROOT = Path(__file__).resolve().parents[4]
INPUT_ROOT = MTC_V2_ROOT / "tests" / "corrected_vnext" / "contracts" / "inputs"


def _scenario(scenario_id: str) -> tuple[dict[str, object], list[Bar]]:
    document = json.loads((INPUT_ROOT / f"{scenario_id}.json").read_text(encoding="utf-8"))
    legacy = document["legacy_arm"]
    corrected = document["corrected_only"]
    economic = corrected["economic_inputs"]
    config = {
        **legacy["config"],
        **corrected["records"],
        "kernel_semantics_version": "2.0.0",
        "same_bar_collision_policy_id": economic.get(
            "same_bar_collision_policy_id", "STOP_FIRST"
        ),
        "slippage_model_id": "BPS_OF_REFERENCE_V1",
    }
    bars = [
        Bar(
            timestamp=datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00")),
            open=float(row["open"]),
            high=float(row["high"]),
            low=float(row["low"]),
            close=float(row["close"]),
            volume=float(row["volume"]),
            bar_index=int(row["bar_index"]),
        )
        for row in legacy["bars"]
    ]
    return config, bars


def _open_long(*, entry_bar: int = 1) -> Position:
    return Position(
        side="long",
        entry_price=100.0,
        avg_entry_price=100.0,
        qty=1.0,
        entry_bar=entry_bar,
        initial_qty=1.0,
        entry_legs=[EntryLeg(100.0, 1.0, entry_bar)],
        lifecycle_id=1,
        working_exit_reference_qty=1.0,
    )


class _StaticSignals:
    warmup_bars_required = 0

    def __init__(self, outputs: list[RawSignal]) -> None:
        self._outputs = iter(outputs)

    def calculate(self, _bar: Bar) -> RawSignal:
        return next(self._outputs)

    @staticmethod
    def indicator_snapshot() -> dict[str, float | int]:
        return {"filter_line": 1.0, "direction": 1}


def test_main_runner_entry_path_uses_corrected_final_fill_and_fee_transition() -> None:
    config, bars = _scenario("RULE2-05-RED")
    runner = Runner.for_corrected_contract(
        config,
        requested_quantity_override=1.0,
    )

    runner.run(bars)

    assert runner.state.position is not None
    assert runner.state.position.entry_price == 101.0
    assert [
        (row.final_fill_price, row.quantity)
        for row in runner.state.fill_events
    ] == [(101.0, 0.0)]
    assert [
        (row.kind, row.signed_delta)
        for row in runner.state.cash_events
    ] == [("FEE", 0.0)]
    assert runner.state.cumulative_fee == 0.0
    assert runner.state.equity == 1000.0


def test_main_runner_round_trip_uses_gross_minus_fees_for_all_open10_guards() -> None:
    config, bars = _scenario("RULE2-07-RED")
    runner = Runner(config)

    runner.run(bars)

    assert runner.state.position is None
    assert len(runner.state.fill_events) == 2
    assert runner.state.last_gross_realized_pnl == 0.0
    assert runner.state.last_closed_guard_pnl == -0.2
    assert runner.state.equity == 999.8
    assert runner._l16_consec_loss_count == 1
    assert runner.corrected_guard_snapshot == {
        "guard_pnl_basis": "GROSS-MINUS-FEES",
        "last_closed_guard_pnl": -0.2,
        "consecutive_loss_count": 1,
        "consec_loss_ok": False,
        "guard_blocked_raw": True,
    }


def test_w276_f01_runner_applies_exit_cash_events_in_order() -> None:
    config, bars = _scenario("RULE2-05-GREEN")
    config["initial_capital"] = 1e16
    runner = Runner(config)
    runner._bind_corrected_instrument(bars[0].timestamp)
    assert runner._corrected_records is not None
    assert runner._corrected_records.cost is not None
    runner._corrected_records = replace(
        runner._corrected_records,
        cost={
            **runner._corrected_records.cost,
            "taker_rate": 0.0,
            "fixed_component": 1e16,
            "minimum_fee": 0.0,
        },
    )
    runner.state.position = _open_long()

    assert runner._apply_corrected_market_exit(
        bar=bars[1],
        reference_price=101.0,
        reason="ordered_cash_probe",
    )

    assert [row.signed_delta for row in runner.state.cash_events] == [-1e16, 1.0]
    assert runner.state.equity == 1.0


def test_w283r_r2_runner_seeds_equity_from_initial_capital() -> None:
    config, _bars = _scenario("RULE2-05-GREEN")
    config["initial_capital"] = 1234.5

    runner = Runner(config)

    assert runner.state.initial_capital == 1234.5
    assert runner.state.realized_equity == 0.0
    assert runner.state.equity == runner.state.initial_capital + runner.state.realized_equity


def test_corrected_green_guard_surface_emits_consecutive_loss_outcome() -> None:
    config, bars = _scenario("RULE2-07-GREEN")
    runner = Runner(config)

    runner.run(bars)

    assert runner.corrected_guard_snapshot["consec_loss_ok"] is True


@pytest.mark.parametrize(
    ("max_daily_loss_pct", "guard_blocked"),
    [(0.005, True), (1.0, False)],
)
def test_open10_daily_loss_red_green_use_gross_minus_fees(
    max_daily_loss_pct: float, guard_blocked: bool
) -> None:
    config, bars = _scenario("RULE2-07-RED")
    config.update(
        use_consecutive_loss_halt=False,
        use_daily_loss_limit=True,
        use_time_stop=False,
        max_daily_loss_pct=max_daily_loss_pct,
    )
    runner = Runner(config)

    runner.run(bars[:1])
    runner._l16_last_trade_day = "20000101"
    runner._l16_day_open_equity = 1000.0
    runner.run(bars[1:])

    assert runner.state.guard_realized_equity == -0.1
    assert runner.corrected_guard_snapshot["guard_blocked_raw"] is guard_blocked


def test_open10_daily_loss_excludes_funding_cash() -> None:
    config, bars = _scenario("RULE2-08-RED")
    config.update(use_daily_loss_limit=True, max_daily_loss_pct=0.005)
    runner = Runner(config)
    runner.state.position = _open_long()
    runner._l16_last_trade_day = "20000101"
    runner._l16_day_open_equity = 1000.0

    runner.run(bars[1:])

    assert runner.state.cumulative_funding == -0.1
    assert runner.state.guard_realized_equity == 0.0
    assert runner.corrected_guard_snapshot["guard_blocked_raw"] is False


@pytest.mark.parametrize(
    ("condition", "closed"),
    [("Loss Only", True), ("Profit Only", False)],
)
def test_open10_time_stop_red_green_classify_last_closed_gross_minus_fees(
    condition: str, closed: bool
) -> None:
    config, bars = _scenario("RULE2-07-RED")
    config.update(
        use_consecutive_loss_halt=False,
        time_stop_condition=condition,
        time_stop_bars=1,
    )
    runner = Runner(config)
    runner.run(bars[:1])
    runner.state.position = _open_long(entry_bar=0)
    runner.state.last_realized_pnl = -0.2

    runner.run(bars[1:2])

    assert (runner.state.position is None) is closed


def test_corrected_runner_normalizes_dynamic_stop_owner_to_stop_exit_id() -> None:
    config, bars = _scenario("RULE2-04-RED")
    runner = Runner(config)

    runner.run(bars)

    stop_fill = [row for row in runner.state.fill_events if row.event_class == "PROTECTIVE_STOP_EXIT"]
    assert len(stop_fill) == 1
    assert stop_fill[0].exit_id == "STOP"
    assert stop_fill[0].fill_trigger == "GAP_OPEN"


def test_target_first_is_test_only_and_production_runner_refuses_it() -> None:
    config, bars = _scenario("RULE2-06-RED")

    with pytest.raises(EconomicsRefusal, match="acceptance-bearing"):
        Runner(config).run(bars)


def test_contract_test_runner_can_exercise_target_first_atomic_fill_order() -> None:
    config, bars = _scenario("RULE2-06-RED")
    runner = Runner.for_corrected_contract(config)

    runner.run(bars)

    exits = [row for row in runner.state.fill_events if row.event_class.endswith("EXIT")]
    assert [row.exit_id for row in exits] == ["TP1", "TP2"]
    assert [row.quantity for row in exits] == [1.0, 1.0]
    assert runner.state.position is None


def test_contract_constructor_builds_equal_price_book_without_production_policy_change() -> None:
    config, bars = _scenario("RULE2-06-EQUAL-PRICE-RED")
    runner = Runner.for_corrected_contract(
        config,
        target_book_overrides={
            "TP1": ("TARGET-NEAR", 105.0, 0.5),
            "TP2": ("TARGET-FAR", 105.0, 0.5),
        },
    )

    runner.run(bars)

    exits = [row for row in runner.state.fill_events if row.event_class.endswith("EXIT")]
    assert [row.exit_id for row in exits] == ["TARGET-FAR", "TARGET-NEAR"]
    assert [row.final_fill_price for row in exits] == [105.0, 105.0]
    assert runner.state.position is None


def test_v283b_f6_same_timestamp_funding_uses_post_bar_position_snapshot() -> None:
    config, bars = _scenario("RULE2-08-RED")
    cost_config, _ = _scenario("RULE2-05-GREEN")
    for field in ("cost_schedule_id", "cost_schedule_sha256"):
        config[field] = cost_config[field]
    event_time = datetime.fromisoformat("2000-01-01T00:00:00+00:00")
    event_bar = replace(bars[2], timestamp=event_time)
    runner = Runner(config)
    runner.signal_producer = _StaticSignals(
        [
            RawSignal(False, False, "none", direction=0, line=100.0),
            RawSignal(True, False, "same_timestamp_entry", direction=1, line=100.0),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run([bars[1], event_bar])

    assert runner.state.position is not None
    assert runner.state.funding_events[0].event_timestamp == event_time
    assert runner.state.funding_events[0].lifecycle_id == runner.state.position.lifecycle_id
    funding_decision = next(
        row for row in runner.state.decision_events if row.decision == "FUNDING_ELIGIBILITY"
    )
    assert dict(funding_decision.details)["eligible"] is True
    assert runner.state.decision_events[-1] is funding_decision


def test_w283r_r4_runner_refuses_ineligible_same_funding_pair() -> None:
    config, bars = _scenario("RULE2-08-RED")
    runner = Runner(config)
    runner.state.position = replace(_open_long(), qty=0.0)
    runner.state.applied_funding_event_keys.add(("TEST-FUND-1", 1))

    with pytest.raises(EconomicsRefusal) as exc_info:
        runner._apply_corrected_funding_between(bars[1], bars[2])

    assert exc_info.value.refusal_code == "REFUSED_DUPLICATE_FUNDING_EVENT"
    assert runner.state.decision_events == []
    assert runner.state.funding_events == []


def test_w276_f02_runner_allows_same_funding_id_for_distinct_lifecycle() -> None:
    config, bars = _scenario("RULE2-08-RED")
    runner = Runner(config)
    runner.state.position = replace(_open_long(), lifecycle_id=2)
    runner.state.applied_funding_event_keys.add(("TEST-FUND-1", 1))

    runner._apply_corrected_funding_between(bars[1], bars[2])

    assert runner.state.applied_funding_event_keys == {
        ("TEST-FUND-1", 1),
        ("TEST-FUND-1", 2),
    }
    assert [row.lifecycle_id for row in runner.state.funding_events] == [2]


def test_v283b_f2_runner_does_not_memoize_funding_id_across_lifecycles() -> None:
    config, bars = _scenario("RULE2-08-RED")
    runner = Runner(config)
    runner.state.position = _open_long()

    runner._apply_corrected_funding_between(bars[1], bars[2])
    runner.state.position = replace(_open_long(), lifecycle_id=2)
    runner._apply_corrected_funding_between(bars[1], bars[2])

    assert runner.state.applied_funding_event_keys == {
        ("TEST-FUND-1", 1),
        ("TEST-FUND-1", 2),
    }
    assert [row.lifecycle_id for row in runner.state.funding_events] == [1, 2]


def test_v283b_f5_reused_runner_evaluates_funding_for_new_lifecycle() -> None:
    config, bars = _scenario("RULE2-08-RED")
    runner = Runner(config)
    runner.state.position = _open_long()

    runner.run(bars[1:])
    runner.state.position = replace(_open_long(), lifecycle_id=2)
    runner.run(bars[1:])

    assert runner.state.applied_funding_event_keys == {
        ("TEST-FUND-1", 1),
        ("TEST-FUND-1", 2),
    }
    assert [row.lifecycle_id for row in runner.state.funding_events] == [1, 2]


def test_v283b_f3_pre_window_funding_is_dispositioned_without_equity_effect() -> None:
    config, bars = _scenario("RULE2-08-RED")
    runner = Runner(config)
    runner.state.position = _open_long()

    runner.run(bars[2:])

    funding_decisions = [
        row for row in runner.state.decision_events if row.decision == "FUNDING_ELIGIBILITY"
    ]
    assert len(funding_decisions) == 1
    assert dict(funding_decisions[0].details)["eligible"] is False
    assert runner.state.funding_events == []
    assert runner.state.cash_events == []
    assert runner.state.equity == 1000.0
    assert runner.corrected_equity_curve == [1000.0]


def test_v283b_f4_post_window_funding_stays_outside_equity_curve() -> None:
    config, bars = _scenario("RULE2-08-RED")
    runner = Runner(config)
    runner.state.position = _open_long()

    runner.run(bars[:2])

    funding_decisions = [
        row for row in runner.state.decision_events if row.decision == "FUNDING_ELIGIBILITY"
    ]
    assert len(funding_decisions) == 1
    assert dict(funding_decisions[0].details)["eligible"] is False
    assert runner.state.funding_events == []
    assert runner.state.cash_events == []
    assert runner.state.equity == 1000.0
    assert runner.corrected_equity_curve[-1] == runner.state.equity


def test_w279_f08_position_snapshot_and_interval_boundary_are_applied() -> None:
    config, bars = _scenario("RULE2-08-RED")
    cost_config, _ = _scenario("RULE2-05-GREEN")
    for field in ("cost_schedule_id", "cost_schedule_sha256"):
        config[field] = cost_config[field]
    event_time = datetime.fromisoformat("2000-01-01T00:00:00+00:00")
    event_bar = replace(bars[2], timestamp=event_time)
    runner = Runner(config)
    runner.signal_producer = _StaticSignals(
        [
            RawSignal(False, False, "none", direction=0, line=100.0),
            RawSignal(True, False, "same_timestamp_entry", direction=1, line=100.0),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run([bars[1], event_bar])

    assert runner.state.position is not None
    assert runner.state.funding_events[0].lifecycle_id == runner.state.position.lifecycle_id

    invalid_boundary_runner = Runner(config)
    assert invalid_boundary_runner._corrected_records is not None
    invalid_boundary_runner._corrected_records = replace(
        invalid_boundary_runner._corrected_records,
        funding={
            **invalid_boundary_runner._corrected_records.funding,
            "interval_boundary_convention": "UNSUPPORTED_BOUNDARY",
        },
    )
    invalid_boundary_runner.state.position = _open_long()
    with pytest.raises(EconomicsRefusal, match="interval_boundary_convention"):
        invalid_boundary_runner._apply_corrected_funding_between(bars[1], event_bar)


def test_v283b_f9_boundary_label_does_not_invent_timestamp_alignment() -> None:
    config, bars = _scenario("RULE2-08-RED")
    runner = Runner(config)
    assert runner._corrected_records is not None
    event_time = datetime.fromisoformat("2000-01-01T00:00:30+00:00")
    event = {
        **runner._corrected_records.funding["events"][0],
        "event_timestamp": "2000-01-01T00:00:30Z",
    }
    runner._corrected_records = replace(
        runner._corrected_records,
        funding={
            **runner._corrected_records.funding,
            "events": (event,),
        },
    )
    runner.state.position = _open_long()

    runner.run(bars[1:])

    assert runner.state.funding_events[0].event_timestamp == event_time
    assert runner.state.applied_funding_event_keys == {("TEST-FUND-1", 1)}


def test_w276_f03_missing_production_funding_events_are_typed_refusal() -> None:
    config, bars = _scenario("RULE2-08-RED")
    record_path = (
        MTC_V2_ROOT
        / "core"
        / "economic_records"
        / "funding"
        / "HYPERLIQUID-BTC-PERP-FUNDING-RULES-V1.json"
    )
    config.update(
        funding_schedule_id="HYPERLIQUID-BTC-PERP-FUNDING-RULES-V1",
        funding_schedule_sha256=hashlib.sha256(record_path.read_bytes()).hexdigest(),
    )
    runner = Runner(config)

    with pytest.raises(EconomicsRefusal) as exc_info:
        runner._apply_corrected_funding_between(bars[1], bars[2])

    assert exc_info.value.refusal_code == "REFUSED_MISSING_FUNDING_EVENT"


def test_v283b_f7_missing_events_precede_schedule_rule_refusals() -> None:
    config, bars = _scenario("RULE2-08-RED")
    runner = Runner(config)
    assert runner._corrected_records is not None
    runner._corrected_records = replace(
        runner._corrected_records,
        funding={
            **runner._corrected_records.funding,
            "events": None,
            "position_snapshot_rule": "UNSUPPORTED_SNAPSHOT",
            "interval_boundary_convention": "UNSUPPORTED_BOUNDARY",
        },
    )

    with pytest.raises(EconomicsRefusal) as exc_info:
        runner._apply_corrected_funding_between(bars[1], bars[2])

    assert exc_info.value.refusal_code == "REFUSED_MISSING_FUNDING_EVENT"


def test_v283b_f1_absent_events_member_is_typed_refusal() -> None:
    config, bars = _scenario("RULE2-08-RED")
    runner = Runner(config)
    assert runner._corrected_records is not None
    funding_without_events = {
        key: value
        for key, value in runner._corrected_records.funding.items()
        if key != "events"
    }
    runner._corrected_records = replace(
        runner._corrected_records,
        funding=funding_without_events,
    )

    with pytest.raises(EconomicsRefusal) as exc_info:
        runner._apply_corrected_funding_between(bars[1], bars[2])

    assert exc_info.value.refusal_code == "REFUSED_MISSING_FUNDING_EVENT"


def test_record_runtime_override_refuses_before_first_economic_intent() -> None:
    config, bars = _scenario("RULE2-03-RED")
    runner = Runner.for_corrected_contract(
        config, instrument_validation_field="price_tick"
    )

    with pytest.raises(ValueError, match="REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION"):
        runner.run(bars)

    refusal = runner.state.decision_events[-1]
    assert refusal.decision == "REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION"
    assert refusal.refusal_code == refusal.decision
    assert dict(refusal.details) == {
        "field": "price_tick",
        "record_value": 0.5,
        "runtime_value": 0.25,
    }


def test_record_runtime_match_emits_core_validation_decision() -> None:
    config, bars = _scenario("RULE2-03-GREEN")
    runner = Runner.for_corrected_contract(
        config, instrument_validation_field="price_tick"
    )

    runner.run(bars)

    validation = runner.state.decision_events[-1]
    assert validation.decision == "INSTRUMENT_RECORD_VALIDATED"
    assert dict(validation.details) == {
        "field": "price_tick",
        "record_value": 0.5,
        "runtime_value": 0.5,
    }


@pytest.mark.parametrize(
    "profile_id", ["raw_close_only_v1", "close_only_deterministic_v2"]
)
def test_p02_corrected_profiles_share_the_same_entry_economics(profile_id: str) -> None:
    config, bars = _scenario("RULE2-05-GREEN")
    config["execution_profile_id"] = profile_id
    runner = Runner(config)

    runner.run(bars)

    assert len(runner.state.fill_events) == 1
    assert runner.state.fill_events[0].reference_price == 100.0
    assert runner.state.fill_events[0].final_fill_price == 100.0


def test_p03_corrected_entry_keeps_decision_close_distinct_from_open() -> None:
    config, bars = _scenario("RULE2-05-GREEN")
    bars[1] = replace(bars[1], open=99.0, low=99.0)
    runner = Runner(config)

    runner.run(bars)

    assert runner.state.fill_events[0].reference_price == 100.0
    assert runner.state.fill_events[0].final_fill_price == 100.0


def test_p05_new_position_is_immune_to_its_opening_bar_extremes() -> None:
    config, bars = _scenario("RULE2-04-RED")
    opening_bar = replace(bars[1], high=115.0, low=85.0)
    runner = Runner(config)

    runner.run([bars[0], opening_bar])

    assert runner.state.position is not None
    assert runner.state.position.active_stop_price == 90.0
    assert not [row for row in runner.state.fill_events if row.event_class.endswith("EXIT")]


def test_p06_existing_stop_wins_and_blocks_same_bar_entry_signal() -> None:
    config, bars = _scenario("RULE2-04-RED")
    collision_bar = replace(bars[2], open=100.0, high=110.0, low=85.0, close=105.0)
    runner = Runner(config)

    runner.run([bars[0], bars[1], collision_bar])

    assert runner.state.position is None
    assert runner.state.fill_events[-1].event_class == "PROTECTIVE_STOP_EXIT"
    assert runner.state.block_new_entries_this_bar is True


def test_p07_research_queue_reenters_from_next_decision_close_final_fill() -> None:
    config, _ = _scenario("RULE2-05-RED")
    config.update(
        allow_flip=True,
        enable_short=True,
        exit_on_opposite_signal=True,
        fallback_size_pct=20.0,
        use_sl=True,
        use_sl_atr=False,
        use_sl_percent=True,
        use_sl_swing_atr=False,
        sl_percent=1.0,
        tw_audit_semantics_mode="research",
        tw_reversal_reentry_mode="carry_to_next_bar_after_protective_exit",
        tw_reversal_reentry_delay_bars=1,
    )
    bars = [
        Bar(datetime.fromisoformat("2000-01-01T00:10:00+00:00"), 100, 100, 100, 100, 0, 0),
        Bar(datetime.fromisoformat("2000-01-01T00:11:00+00:00"), 98, 98, 95, 96, 0, 1),
        Bar(datetime.fromisoformat("2000-01-01T00:12:00+00:00"), 90, 93, 89, 92, 0, 2),
    ]
    runner = Runner(config)
    runner.signal_producer = _StaticSignals(
        [
            RawSignal(True, False, "long", direction=1, line=100.0),
            RawSignal(False, True, "queued_short", direction=-1, line=96.0),
            RawSignal(False, False, "none", direction=0, line=92.0),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is not None
    assert runner.state.position.side == "short"
    assert runner.state.position.entry_bar == 2
    assert runner.state.position.entry_price == 91.08
    assert runner.state.position.active_stop_price == 92.0


def test_p07_nonresearch_green_does_not_queue_protective_exit_signal() -> None:
    config, _ = _scenario("RULE2-05-RED")
    config.update(
        allow_flip=True,
        enable_short=True,
        exit_on_opposite_signal=True,
        fallback_size_pct=20.0,
        use_sl=True,
        use_sl_atr=False,
        use_sl_percent=True,
        use_sl_swing_atr=False,
        sl_percent=1.0,
    )
    bars = [
        Bar(datetime.fromisoformat("2000-01-01T00:10:00+00:00"), 100, 100, 100, 100, 0, 0),
        Bar(datetime.fromisoformat("2000-01-01T00:11:00+00:00"), 98, 98, 95, 96, 0, 1),
        Bar(datetime.fromisoformat("2000-01-01T00:12:00+00:00"), 90, 93, 89, 92, 0, 2),
    ]
    runner = Runner(config)
    runner.signal_producer = _StaticSignals(
        [
            RawSignal(True, False, "long", direction=1, line=100.0),
            RawSignal(False, True, "unqueued_short", direction=-1, line=96.0),
            RawSignal(False, False, "none", direction=0, line=92.0),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is None
    assert runner.state.total_entries == 1


def test_p08_same_side_add_rebooks_from_the_final_fill() -> None:
    config, bars = _scenario("RULE2-05-GREEN")
    config["max_entries"] = 2
    runner = Runner(config)
    runner._bind_corrected_instrument(bars[0].timestamp)

    assert runner._apply_corrected_entry(
        bar=bars[1],
        reference_price=100.0,
        side="long",
        reason="p08_first",
        sizing_equity=1000.0,
    )
    assert runner._apply_corrected_entry(
        bar=replace(bars[1], bar_index=2),
        reference_price=100.0,
        side="long",
        reason="p08_add",
        sizing_equity=1000.0,
    )

    assert runner.state.position is not None
    assert runner.state.position.qty == 2.0
    assert runner.state.position.avg_entry_price == 100.0
    assert runner.state.position.working_exit_book_version == 2


def test_w279_f11_corrected_entry_applies_total_margin_admission() -> None:
    config, bars = _scenario("RULE2-05-GREEN")
    config.update(max_entries=2, max_leverage_cap=1.0, margin_long_pct=100.0)
    runner = Runner.for_corrected_contract(
        config,
        requested_quantity_override=5.0,
    )
    runner._bind_corrected_instrument(bars[0].timestamp)
    runner.state.position = replace(
        _open_long(),
        qty=10.0,
        initial_qty=10.0,
        entry_legs=[EntryLeg(100.0, 10.0, 1)],
        working_exit_reference_qty=10.0,
    )

    opened = runner._apply_corrected_entry(
        bar=bars[1],
        reference_price=100.0,
        side="long",
        reason="margin_probe",
        sizing_equity=1000.0,
    )

    assert opened is False
    assert runner.state.position.qty == 10.0
    assert runner.state.fill_events == []
