from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from bridge.engine.risk import RiskConfig, RiskEngine
from bridge.engine.types import (
    RISK_SNAPSHOT_REQUIRED,
    SNAPSHOT_PAYLOAD_VERSION_V2,
    AccountSnapshot,
    AuthoritativeRiskSnapshot,
    RiskPositionRow,
    Signal,
)

SNAP_TS = datetime(2026, 7, 26, 12, 0, tzinfo=UTC)


def _snapshot(
    *,
    equity: float = 1000.0,
    available: float = 1000.0,
    withdrawable: float = 1000.0,
    margin_used: float = 0.0,
    positions: tuple[RiskPositionRow, ...] = (),
) -> AuthoritativeRiskSnapshot:
    """A typed view shaped exactly like the loader's output.

    Constructed directly on purpose: these are unit tests of the *gate* logic
    given a snapshot. Provenance, hashing, freshness and pointer authority are
    proven end-to-end in test_store.py and test_reconciliation.py.
    """
    return AuthoritativeRiskSnapshot(
        payload_version=SNAPSHOT_PAYLOAD_VERSION_V2,
        checkpoint_id="ckpt-v1:" + "a" * 64,
        attempt_id="attempt-v1:" + "b" * 64,
        run_id="run-risk",
        canonical_hash="c" * 64,
        accepted_ts=SNAP_TS,
        loaded_ts=SNAP_TS + timedelta(seconds=3),
        observed_from_ts=SNAP_TS,
        observed_to_ts=SNAP_TS,
        coverage_start_ms=0,
        coverage_end_ms=1,
        positions=positions,
        equity=equity,
        withdrawable=withdrawable,
        margin_used=margin_used,
        available_margin=available,
    )


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


# ---------------------------------------------------------------------------
# TS-P1-006 — the authoritative snapshot is the only v6 risk input
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bogus",
    [
        None,
        {"equity": 1_000_000.0, "available_margin": 1_000_000.0},
        AccountSnapshot(equity=1_000_000.0, available_margin=1_000_000.0),
        ("ckpt", 1_000_000.0),
        object(),
    ],
)
def test_authoritative_path_refuses_every_non_snapshot_input(bogus):
    """A mapping is exactly the TOCTOU hole this path closes — never a fallback."""
    engine = RiskEngine(RiskConfig(risk_pct_per_trade=0.01, min_order_usd=10))

    result = engine.evaluate_authoritative(
        signal=_signal(), snapshot=bogus, stop_loss=95.0
    )

    assert result.accepted is False
    assert result.plan is None
    assert result.rejection == RISK_SNAPSHOT_REQUIRED
    assert result.disarm is True
    assert [gate["status"] for gate in result.gate_results] == ["BLOCK"]


def test_authoritative_sizing_is_identical_to_the_predecessor_for_equal_inputs():
    """Thresholds, gate order and sizing are unchanged; only provenance moves."""
    engine = RiskEngine(RiskConfig(risk_pct_per_trade=0.01, min_order_usd=10))

    legacy = engine.evaluate(
        signal=_signal(),
        account={"equity": 1000.0, "available_margin": 1000.0},
        stop_loss=95.0,
        take_profit=110.0,
    )
    authoritative = engine.evaluate_authoritative(
        signal=_signal(),
        snapshot=_snapshot(equity=1000.0, available=1000.0),
        stop_loss=95.0,
        take_profit=110.0,
    )

    assert authoritative.accepted is legacy.accepted is True
    assert authoritative.plan.qty == legacy.plan.qty == 2.0
    assert authoritative.plan.risk_dollars == legacy.plan.risk_dollars == 10.0
    assert authoritative.plan.model_dump() == legacy.plan.model_dump()
    # One leading authority gate, then the accepted sequence, byte for byte.
    legacy_names = [gate["name"] for gate in legacy.gate_results]
    authoritative_names = [gate["name"] for gate in authoritative.gate_results]
    assert authoritative_names == ["RISK_SNAPSHOT"] + legacy_names
    assert all(gate["status"] == "PASS" for gate in authoritative.gate_results)
    # The checkpoint identity that authorized the size is recorded as evidence.
    detail = authoritative.gate_results[0]["detail"]
    assert detail["checkpoint_id"] == "ckpt-v1:" + "a" * 64
    assert detail["canonical_hash"] == "c" * 64
    assert detail["payload_version"] == SNAPSHOT_PAYLOAD_VERSION_V2
    assert detail["age_s"] == 3.0


def test_authoritative_sizing_uses_snapshot_equity_not_a_larger_point_read():
    engine = RiskEngine(RiskConfig(risk_pct_per_trade=0.01, min_order_usd=10))

    result = engine.evaluate_authoritative(
        signal=_signal(),
        snapshot=_snapshot(equity=1000.0, available=1000.0),
        stop_loss=95.0,
    )

    # 1000 * 0.01 / 5 == 2.0. A 1,000,000 point read would have sized 2000.
    assert result.accepted is True
    assert result.plan.qty == 2.0


@pytest.mark.parametrize("size", [0.5, -0.5, 1e-9])
def test_any_nonzero_reconciled_position_blocks_a_new_entry(size):
    """The predecessor passed open_position=None regardless of real exposure."""
    engine = RiskEngine(RiskConfig(risk_pct_per_trade=0.01, min_order_usd=10))

    result = engine.evaluate_authoritative(
        signal=_signal(),
        snapshot=_snapshot(positions=(RiskPositionRow("ETH", size),)),
        stop_loss=95.0,
    )

    assert result.accepted is False
    assert result.plan is None
    assert result.rejection == "POSITION_EXISTS"
    # Blocked at the accepted gate, in the accepted position.
    assert [gate["name"] for gate in result.gate_results] == [
        "RISK_SNAPSHOT",
        "STATE_ARMED",
        "FEED_READY",
        "NO_OPEN_POSITION",
    ]


def test_canonical_flat_positions_behave_exactly_as_before():
    """Explicit zero rows are evidence of flatness, never of an open position."""
    engine = RiskEngine(RiskConfig(risk_pct_per_trade=0.01, min_order_usd=10))

    result = engine.evaluate_authoritative(
        signal=_signal(),
        snapshot=_snapshot(
            positions=(RiskPositionRow("BTC", 0.0), RiskPositionRow("ETH", 0.0))
        ),
        stop_loss=95.0,
    )

    assert result.accepted is True
    assert result.plan.qty == 2.0


def test_authoritative_path_preserves_the_interim_pnl_gates():
    """Daily-loss and consecutive-loss semantics and thresholds are untouched."""
    engine = RiskEngine(RiskConfig(max_daily_loss_pct=0.02, max_consecutive_losses=3))

    boundary = engine.evaluate_authoritative(
        signal=_signal(),
        snapshot=_snapshot(equity=1000.0, available=1000.0),
        stop_loss=95.0,
        realized_today=-20.0,
    )
    assert boundary.accepted is False
    assert boundary.rejection == "DAILY_LOSS_LIMIT"
    assert boundary.disarm is True

    inside = engine.evaluate_authoritative(
        signal=_signal(),
        snapshot=_snapshot(equity=1000.0, available=1000.0),
        stop_loss=95.0,
        realized_today=-19.99,
    )
    assert inside.accepted is True

    streak = engine.evaluate_authoritative(
        signal=_signal(),
        snapshot=_snapshot(equity=1000.0, available=1000.0),
        stop_loss=95.0,
        consecutive_losses=3,
    )
    assert streak.accepted is False
    assert streak.rejection == "CONSECUTIVE_LOSS_LIMIT"
    assert streak.disarm is True


def test_snapshot_account_derivation_cannot_be_widened_by_a_caller():
    """`account()` is derived from the frozen view; there is no setter to abuse."""
    snapshot = _snapshot(equity=1000.0, available=1000.0)

    first = snapshot.account()
    first.equity = 1_000_000.0  # a mutable pydantic copy, not the snapshot

    assert snapshot.equity == 1000.0
    assert snapshot.account().equity == 1000.0
    engine = RiskEngine(RiskConfig(risk_pct_per_trade=0.01, min_order_usd=10))
    assert (
        engine.evaluate_authoritative(
            signal=_signal(), snapshot=snapshot, stop_loss=95.0
        ).plan.qty
        == 2.0
    )
