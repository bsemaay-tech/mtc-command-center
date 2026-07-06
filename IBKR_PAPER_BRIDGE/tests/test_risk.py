from __future__ import annotations

from datetime import UTC, datetime

from bridge.engine.risk import RiskConfig, RiskEngine
from bridge.engine.types import Signal


def _signal(direction: str = "LONG", ref_price: float = 100.0) -> Signal:
    return Signal(
        ts=datetime(2026, 7, 6, tzinfo=UTC),
        symbol="BTC",
        direction=direction,
        reason="test",
        ref_price=ref_price,
    )


def test_risk_engine_sizes_with_stop_distance_and_rounding():
    engine = RiskEngine(RiskConfig(risk_pct_per_trade=0.01, min_order_usd=10))

    result = engine.evaluate(
        signal=_signal(),
        account={"equity": 1000.0, "available_margin": 1000.0},
        stop_loss=95.0,
        take_profit=110.0,
    )

    assert result.accepted is True
    assert result.plan is not None
    assert result.plan.qty == 2.0
    assert result.plan.risk_dollars == 10.0
    assert [gate["status"] for gate in result.gate_results] == ["PASS"] * len(result.gate_results)


def test_risk_engine_rejects_daily_loss_and_no_trade_regime():
    engine = RiskEngine(RiskConfig(max_daily_loss_pct=0.02))

    daily_loss = engine.evaluate(
        signal=_signal(),
        account={"equity": 1000.0, "available_margin": 1000.0},
        stop_loss=95.0,
        realized_today=-25.0,
    )
    assert daily_loss.accepted is False
    assert daily_loss.rejection == "DAILY_LOSS_LIMIT"

    no_trade = engine.evaluate(
        signal=_signal(),
        account={"equity": 1000.0, "available_margin": 1000.0},
        stop_loss=95.0,
        regime="NO_TRADE",
    )
    assert no_trade.accepted is False
    assert no_trade.rejection == "DIRECTION_BLOCKED"


def test_risk_engine_rejects_leverage_notional_and_bad_stop():
    engine = RiskEngine(
        RiskConfig(
            risk_pct_per_trade=0.01,
            max_position_notional_pct=0.20,
            max_leverage=1,
            min_stop_distance_pct=0.001,
            min_order_usd=10,
        )
    )

    bad_stop = engine.evaluate(
        signal=_signal(),
        account={"equity": 1000.0, "available_margin": 1000.0},
        stop_loss=99.99,
    )
    assert bad_stop.accepted is False
    assert bad_stop.rejection == "STOP_TOO_CLOSE"

    bad_leverage = engine.evaluate(
        signal=_signal(),
        account={"equity": 1000.0, "available_margin": 1000.0},
        stop_loss=95.0,
        leverage=2,
    )
    assert bad_leverage.accepted is False
    assert bad_leverage.rejection == "LEVERAGE_CAP"

    notional = engine.evaluate(
        signal=_signal(),
        account={"equity": 1000.0, "available_margin": 1000.0},
        stop_loss=99.0,
    )
    assert notional.accepted is False
    assert notional.rejection == "NOTIONAL_CAP"
