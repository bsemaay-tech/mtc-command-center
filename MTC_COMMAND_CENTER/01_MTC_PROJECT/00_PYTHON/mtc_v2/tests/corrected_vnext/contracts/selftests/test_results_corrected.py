from __future__ import annotations

import dataclasses
import json
from datetime import datetime
from pathlib import Path

import pytest

from mtc_v2.core.economics import EconomicRecords
from mtc_v2.core.results import (
    CorrectedRunManifest,
    TradeRecord,
    corrected_surfaces,
)
from mtc_v2.core.runner import Runner
from mtc_v2.core.types import Bar


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
        guards=runner.corrected_guard_snapshot,
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
    assert result["metrics"]["net_profit"] == pytest.approx(-0.2)
    assert result["metrics"]["gross_loss"] == 0.2
    assert result["run_manifest"]["kernel_semantics_version"] == "2.0.0"
    assert result["run_manifest"]["instrument_record_digest"] == records.instrument.digest


def test_corrected_manifest_marks_an_unconsumed_cost_schedule_without_padding_digest() -> None:
    config, _bars = _scenario("RULE2-08-RED")

    manifest = CorrectedRunManifest.from_records(
        _records(config), execution_profile_id=str(config["execution_profile_id"])
    ).to_dict()

    assert manifest["cost_schedule_id"] == "NOT_CONSUMED"
    assert "cost_schedule_digest" not in manifest
    assert manifest["funding_schedule_id"] == "SYNTH-FUNDING-RULE2-08-V1"


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
    )["RESULT_SURFACE"]

    assert result["final_position"] is None
    assert result["order_notional"] == 100
    assert result["refusals"] == [
        {
            "code": "REFUSED_MIN_NOTIONAL",
            "observed_notional": 100,
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
