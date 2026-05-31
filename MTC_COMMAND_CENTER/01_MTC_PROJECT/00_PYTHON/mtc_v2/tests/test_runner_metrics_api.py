from __future__ import annotations

from dataclasses import asdict
from datetime import datetime

import pytest

from mtc_v2.core.results import (
    BacktestResult,
    EquityPoint,
    MetricsSummary,
    RunnerWarning,
    TradeRecord,
    calculate_max_drawdown,
    metrics_from_trades,
)
from mtc_v2.core.types import Bar
from tools.runner_metrics_adapter import run_with_result


def test_backtest_result_object_can_be_created() -> None:
    result = BacktestResult(
        metrics=MetricsSummary.empty(),
        trades=[],
        equity_curve=[],
        config_hash="cfg",
        dataset_hash="data",
        dataset_id="dataset",
        run_id="run",
        warnings=[],
        raw_artifact_paths={},
    )

    assert result.metrics.total_trades == 0
    assert result.dataset_id == "dataset"


def test_metrics_summary_handles_no_trade_cases() -> None:
    metrics = metrics_from_trades([], [1000.0], initial_capital=1000.0)

    assert metrics.total_trades == 0
    assert metrics.net_profit == 0.0
    assert metrics.profit_factor is None
    assert any(w.code == "NO_TRADES" for w in metrics.warnings)


def test_profit_factor_handles_zero_gross_loss() -> None:
    trade = TradeRecord(
        trade_id="t1",
        side="long",
        entry_time=None,
        exit_time=datetime(2025, 1, 2),
        entry_price=None,
        exit_price=110.0,
        qty=1.0,
        pnl=10.0,
        pnl_pct=1.0,
        exit_reason="test",
        bars_held=None,
    )

    metrics = metrics_from_trades([trade], [1000.0, 1010.0], initial_capital=1000.0)

    assert metrics.gross_profit == pytest.approx(10.0)
    assert metrics.gross_loss == pytest.approx(0.0)
    assert metrics.profit_factor is None
    assert any(w.code == "ZERO_GROSS_LOSS" for w in metrics.warnings)


def test_max_drawdown_is_deterministic() -> None:
    drawdown, drawdown_pct = calculate_max_drawdown([100.0, 120.0, 90.0, 110.0, 80.0])

    assert drawdown == pytest.approx(40.0)
    assert drawdown_pct == pytest.approx(33.3333333333)


def test_trade_record_serialization_works() -> None:
    trade = TradeRecord(
        trade_id="t1",
        side="short",
        entry_time=datetime(2025, 1, 1),
        exit_time=datetime(2025, 1, 2),
        entry_price=100.0,
        exit_price=90.0,
        qty=2.0,
        pnl=20.0,
        pnl_pct=2.0,
        exit_reason="tp",
        bars_held=3,
    )

    payload = asdict(trade)

    assert payload["trade_id"] == "t1"
    assert payload["side"] == "short"
    assert payload["bars_held"] == 3


def test_adapter_returns_stable_keys_expected_by_optimizer() -> None:
    bars = [
        Bar(datetime(2025, 1, 1), 100.0, 101.0, 99.0, 100.0, 100.0, 0),
        Bar(datetime(2025, 1, 2), 100.0, 102.0, 99.0, 101.0, 100.0, 1),
        Bar(datetime(2025, 1, 3), 101.0, 103.0, 100.0, 102.0, 100.0, 2),
    ]

    result = run_with_result(
        bars,
        config_overrides={
            "instrument_symbol": "TEST",
            "initial_capital": 1000.0,
            "st_atr_len": 2,
            "st_factor": 1.0,
            "sl_atr_len": 1,
            "tp_atr_len": 1,
            "trail_atr_len": 1,
        },
        dataset_id="dataset",
        dataset_hash="hash",
        run_id="run",
    )
    flat = result.to_optimizer_row()

    for key in [
        "net_profit",
        "net_profit_pct",
        "gross_profit",
        "gross_loss",
        "profit_factor",
        "max_drawdown",
        "max_drawdown_pct",
        "win_rate",
        "total_trades",
        "config_hash",
        "dataset_hash",
        "dataset_id",
        "run_id",
    ]:
        assert key in flat


def test_existing_runner_behavior_not_broken() -> None:
    bars = [Bar(datetime(2025, 1, 1), 100.0, 101.0, 99.0, 100.0, 100.0, 0)]

    result = run_with_result(bars, config_overrides={"instrument_symbol": "TEST"}, dataset_id="dataset")

    assert result.metrics.total_trades >= 0
    assert all(isinstance(point, EquityPoint) for point in result.equity_curve)
    assert all(isinstance(warning, RunnerWarning) for warning in result.warnings)
