from __future__ import annotations

import dataclasses
import json
from datetime import datetime
from pathlib import Path

from mtc_v2.core.economics import EconomicRecords
from mtc_v2.core.results import (
    CorrectedRunManifest,
    TradeRecord,
    _realized_equity_window,
    corrected_surfaces,
)
from mtc_v2.core.runner import Runner
from mtc_v2.core.types import Bar, CashEvent, CashEventKind, PortfolioState


MTC_V2_ROOT = Path(__file__).resolve().parents[4]
INPUT_ROOT = MTC_V2_ROOT / "tests" / "corrected_vnext" / "contracts" / "inputs"
RECORD_ROOT = MTC_V2_ROOT / "core" / "economic_records"


def _scenario(scenario_id: str) -> tuple[dict[str, object], list[Bar]]:
    document = json.loads((INPUT_ROOT / f"{scenario_id}.json").read_text(encoding="utf-8"))
    legacy = document["legacy_arm"]
    corrected = document["corrected_only"]
    config = {
        **legacy["config"],
        **corrected["records"],
        "kernel_semantics_version": "2.0.0",
        "same_bar_collision_policy_id": corrected["economic_inputs"].get(
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


def _records(config: dict[str, object]) -> EconomicRecords:
    cost_id = config["cost_schedule_id"]
    return EconomicRecords.from_record_paths(
        instrument_path=RECORD_ROOT / "instruments" / f"{config['instrument_record_id']}.json",
        cost_path=None if cost_id is None else RECORD_ROOT / "costs" / f"{cost_id}.json",
        funding_path=RECORD_ROOT / "funding" / f"{config['funding_schedule_id']}.json",
    )


def test_corrected_result_is_version_shaped_and_net_cash_based() -> None:
    config, bars = _scenario("RULE2-07-RED")
    runner = Runner(config)
    runner.run(bars)
    records = _records(config)

    surfaces = corrected_surfaces(
        state=runner.state,
        equity_values=runner.corrected_equity_curve,
        manifest=CorrectedRunManifest.from_records(
            records, execution_profile_id=str(config["execution_profile_id"])
        ),
        computed_guard_snapshot=runner.corrected_guard_snapshot,
        declared_def_ids=("DEF-P012-07",),
    )

    event = surfaces["EVENT_SURFACE"]
    assert list(event) == [
        "decision_events",
        "fill_events",
        "cash_events",
        "fee_events",
        "funding_events",
        "exit_events",
    ]
    for rows in event.values():
        assert [row["sequence"] for row in rows] == list(range(len(rows)))
    assert len(event["fee_events"]) == 2
    assert set(event["fee_events"][0]) == {
        "sequence",
        "kernel_semantics_version",
        "event_timestamp",
        "lifecycle_id",
        "fill_id",
        "event_class",
        "liquidity_role",
        "schedule_id",
        "schedule_digest",
        "rate",
        "fixed_component",
        "fee_notional",
        "fee_amount",
        "fee_cash_delta",
        "settlement_currency",
        "cash_event_id",
    }
    cash_by_id = {row["cash_event_id"]: row for row in event["cash_events"]}
    for fee in event["fee_events"]:
        assert fee["fee_cash_delta"] == cash_by_id[fee["cash_event_id"]]["signed_delta"]

    result = surfaces["RESULT_SURFACE"]
    assert result["final_position"] is None
    assert result["trades"] == [
        {
            "entry_fill_price": 100.0,
            "quantity": 1.0,
            "exit_ids": ["TIME_STOP"],
            "gross_realized_pnl": 0.0,
            "fee_total": -0.2,
            "funding_total": 0.0,
            "net_trade_pnl": -0.2,
        }
    ]
    assert result["equity_curve"] == {"first": 1000.0, "last": 999.8}
    assert result["metrics"] is None
    assert result["guards"] == {
        "guard_pnl_basis": "GROSS-MINUS-FEES",
        "last_closed_guard_pnl": -0.2,
        "consecutive_loss_count": 1,
        "consec_loss_ok": False,
        "guard_blocked_raw": True,
    }
    assert result["run_manifest"]["kernel_semantics_version"] == "2.0.0"
    assert result["run_manifest"]["instrument_record_digest"] == records.instrument.digest
    assert set(result["run_manifest"]) == {
        "kernel_semantics_version",
        "execution_profile_id",
        "instrument_record_id",
        "instrument_record_digest",
        "instrument_source_document_digest",
        "instrument_effective_interval",
        "cost_schedule_id",
        "cost_schedule_digest",
        "funding_schedule_id",
        "funding_schedule_digest",
    }


def test_corrected_manifest_carries_the_consumed_cost_schedule_and_digest() -> None:
    config, _bars = _scenario("RULE2-08-RED")

    manifest = CorrectedRunManifest.from_records(
        _records(config), execution_profile_id=str(config["execution_profile_id"])
    ).to_dict()

    # Owner decision 144; design P012_FRESH_DESIGN_V1.md:932 binds the RED cost record id and digest.
    assert manifest["cost_schedule_id"] == "SYNTH-COST-RULE2-07-RED-V1"
    assert manifest["cost_schedule_digest"] == (
        "806e98512a3eb336538c8b68a52cef3ed80897cd2a87d9f270900c7ba094f29b"
    )
    assert manifest["funding_schedule_id"] == "SYNTH-FUNDING-RULE2-08-V1"


def test_def_p012_08_result_includes_zero_cumulative_funding_without_events() -> None:
    config, _bars = _scenario("RULE2-08-GREEN")
    state = PortfolioState(
        initial_capital=1000.0,
        equity=1000.0,
        realized_equity=1000.0,
    )
    assert state.funding_events == []

    result = corrected_surfaces(
        state=state,
        equity_values=[],
        manifest=CorrectedRunManifest.from_records(
            _records(config), execution_profile_id=str(config["execution_profile_id"])
        ),
        declared_def_ids=("DEF-P012-08",),
    )["RESULT_SURFACE"]

    assert result["cumulative_funding"] == 0


def test_realized_equity_window_adds_in_window_deltas_in_array_order() -> None:
    observation_start = datetime.fromisoformat("2000-01-01T00:00:00+00:00")
    deltas = [1e16, 1.0, -1e16]
    state = PortfolioState(initial_capital=1.0)
    state.cash_events = [
        CashEvent(
            sequence=sequence,
            cash_event_id=f"CASH-{sequence}",
            event_timestamp=observation_start,
            lifecycle_id=1,
            kind=CashEventKind.GROSS_REALIZATION,
            signed_delta=delta,
            settlement_currency="USD",
        )
        for sequence, delta in enumerate(deltas)
    ]

    grouped_delta = sum(deltas)
    ordered_delta = 0.0
    for delta in deltas:
        ordered_delta += delta
    assert grouped_delta.hex() != ordered_delta.hex()

    expected_last = state.initial_capital
    for delta in deltas:
        expected_last += delta
    first, last = _realized_equity_window(
        state,
        observation_start=observation_start,
        observation_end=observation_start,
    )

    assert first.hex() == state.initial_capital.hex()
    assert last.hex() == expected_last.hex()


def test_corrected_min_notional_refusal_retains_nonblocked_result_facts() -> None:
    config, bars = _scenario("RULE2-02-RED")
    # The differing value belongs only to the sealed legacy arm. Corrected
    # execution consumes the immutable record and therefore supplies no runtime override.
    config.pop("instrument_min_notional")
    runner = Runner(config)
    runner.run(bars)

    result = corrected_surfaces(
        state=runner.state,
        equity_values=runner.corrected_equity_curve,
        manifest=CorrectedRunManifest.from_records(
            _records(config), execution_profile_id=str(config["execution_profile_id"])
        ),
        declared_def_ids=("DEF-P012-02",),
    )["RESULT_SURFACE"]

    assert result["final_position"] is None
    assert result["order_notional"] == 100
    assert result["refusals"] == [
        {
            "code": "REFUSED_MIN_NOTIONAL",
            "order_notional": 100,
            "required_min_notional": 101,
        }
    ]


def test_legacy_trade_record_shape_is_not_padded_with_corrected_fields() -> None:
    legacy = TradeRecord(
        trade_id="T1",
        side="long",
        entry_time=None,
        exit_time=None,
        entry_price=100.0,
        exit_price=101.0,
        qty=1.0,
        pnl=1.0,
        pnl_pct=1.0,
        exit_reason="target",
        bars_held=1,
    )

    assert set(dataclasses.asdict(legacy)) == {
        "trade_id",
        "side",
        "entry_time",
        "exit_time",
        "entry_price",
        "exit_price",
        "qty",
        "pnl",
        "pnl_pct",
        "exit_reason",
        "bars_held",
    }
