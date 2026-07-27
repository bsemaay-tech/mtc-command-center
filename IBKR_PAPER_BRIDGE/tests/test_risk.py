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


# ---------------------------------------------------------------------------
# TS-P1-007 — pure durable-control gates
#
# These are unit tests of the *arithmetic and gate order* given an already
# proven daily-risk state. Derivation, persistence, exactly-once latching and
# restart reconstruction are proven against real evidence in test_store.py,
# test_reconciliation.py and test_engine_dryrun.py.
# ---------------------------------------------------------------------------

DAY_DATE = "2026-07-26"


def _durable_config(**overrides):
    values = {
        "risk_pct_per_trade": 0.01,
        "min_order_usd": 10,
        "max_daily_loss_pct": 0.02,
        "max_intraday_drawdown_pct": 0.05,
        "equity_floor_usdc": 500.0,
    }
    values.update(overrides)
    return RiskConfig(**values)


def _daily(
    *,
    equity: float,
    baseline: float,
    peak: float | None = None,
    latches: tuple = (),
    checkpoint_id: str | None = None,
    policy_version: str | None = None,
    realized_local: float = 0.0,
    funding: float = 0.0,
):
    from bridge.engine.types import DailyRiskState

    peak = max(baseline, equity) if peak is None else peak
    snapshot = _snapshot()
    return DailyRiskState(
        mode="paper",
        network="testnet",
        trading_date=DAY_DATE,
        checkpoint_id=checkpoint_id or snapshot.checkpoint_id,
        attempt_id=snapshot.attempt_id,
        run_id=snapshot.run_id,
        accepted_ts=SNAP_TS,
        loaded_ts=SNAP_TS + timedelta(seconds=3),
        baseline_checkpoint_id="ckpt-v1:" + "d" * 64,
        baseline_ts=SNAP_TS - timedelta(hours=12),
        baseline_equity=float(baseline),
        peak_equity=float(peak),
        equity=float(equity),
        realized_pnl_local=float(realized_local),
        funding_attributed_usdc=float(funding),
        policy_version=policy_version or _durable_policy().version,
        active_latches=tuple(latches),
    )


def _durable_policy(**overrides):
    from bridge.engine.types import DurableRiskPolicy

    values = {
        "policy_id": "ts-p1-007-v1",
        "max_daily_loss_pct": 0.02,
        "max_intraday_drawdown_pct": 0.05,
        "equity_floor_usdc": 500.0,
    }
    values.update(overrides)
    return DurableRiskPolicy.create(**values)


def _latch(control: str, *, threshold: float = 0.0, observed: float = 0.0):
    from bridge.engine.types import RiskControlLatch

    return RiskControlLatch(
        latch_row_id=1,
        control=control,
        scope_key=DAY_DATE,
        trading_date=DAY_DATE,
        checkpoint_id="ckpt-v1:" + "a" * 64,
        generation=1,
        observed_value=observed,
        threshold_value=threshold,
        equity=900.0,
        reason_code=f"{control}_LIMIT",
        policy_version=_durable_policy().version,
        latched_ts=SNAP_TS,
    )


def _durable_result(daily, *, equity=1000.0, engine=None, **kwargs):
    engine = engine or RiskEngine(_durable_config())
    return engine.evaluate_authoritative(
        signal=_signal(),
        snapshot=_snapshot(equity=equity, available=equity),
        stop_loss=95.0,
        daily_state=daily,
        require_daily_state=True,
        **kwargs,
    )


def test_durable_policy_refuses_non_finite_negative_and_absurd_values():
    from bridge.engine.types import RiskPolicyInvalid

    for field, value in (
        ("max_daily_loss_pct", float("nan")),
        ("max_daily_loss_pct", float("inf")),
        ("max_daily_loss_pct", 0.0),
        ("max_daily_loss_pct", -0.01),
        ("max_daily_loss_pct", 1.01),
        ("max_intraday_drawdown_pct", float("nan")),
        ("max_intraday_drawdown_pct", -0.05),
        ("max_intraday_drawdown_pct", 0.0),
        ("equity_floor_usdc", float("inf")),
        ("equity_floor_usdc", -1.0),
        ("equity_floor_usdc", float("nan")),
        ("policy_id", ""),
        ("max_daily_loss_pct", True),
    ):
        with pytest.raises(RiskPolicyInvalid):
            _durable_policy(**{field: value})

    # A silent config change must produce a different, persisted version.
    assert _durable_policy().version != _durable_policy(equity_floor_usdc=501.0).version
    assert _durable_policy().version == _durable_policy().version
    assert _durable_policy().version.startswith("rpol-v1:")


def test_risk_engine_refuses_to_start_with_an_invalid_durable_policy():
    from bridge.engine.types import RiskPolicyInvalid

    with pytest.raises(RiskPolicyInvalid):
        RiskEngine(_durable_config(max_intraday_drawdown_pct=float("nan")))
    with pytest.raises(RiskPolicyInvalid):
        RiskEngine(_durable_config(equity_floor_usdc=-1.0))
    engine = RiskEngine(_durable_config())
    assert engine.policy.max_daily_loss_pct == 0.02
    assert engine.policy.max_intraday_drawdown_pct == 0.05
    assert engine.policy.equity_floor_usdc == 500.0


def test_daily_loss_gate_uses_day_start_equity_and_blocks_on_the_exact_boundary():
    inside = _durable_result(_daily(equity=9_801.0, baseline=10_000.0), equity=9_801.0)
    assert inside.accepted is True

    exact = _durable_result(_daily(equity=9_800.0, baseline=10_000.0), equity=9_800.0)
    assert exact.accepted is False
    assert exact.rejection == "DAILY_LOSS_LIMIT_AUTH"
    assert exact.disarm is True

    outside = _durable_result(_daily(equity=9_799.0, baseline=10_000.0), equity=9_799.0)
    assert outside.rejection == "DAILY_LOSS_LIMIT_AUTH"

    # Current equity is NOT the denominator: 199 of loss is inside the day-start
    # budget of 200 but outside 2% of the current 9,801.
    assert 199.0 > 0.02 * 9_801.0
    assert inside.accepted is True


def test_max_drawdown_gate_measures_from_the_monotonic_peak():
    inside = _durable_result(
        _daily(equity=11_401.0, baseline=10_000.0, peak=12_000.0), equity=11_401.0
    )
    assert inside.accepted is True

    exact = _durable_result(
        _daily(equity=11_400.0, baseline=10_000.0, peak=12_000.0), equity=11_400.0
    )
    assert exact.accepted is False
    assert exact.rejection == "MAX_DRAWDOWN_LIMIT"
    assert exact.disarm is True

    outside = _durable_result(
        _daily(equity=11_399.0, baseline=10_000.0, peak=12_000.0), equity=11_399.0
    )
    assert outside.rejection == "MAX_DRAWDOWN_LIMIT"


def test_equity_floor_gate_blocks_at_and_below_the_absolute_floor():
    inside = _durable_result(_daily(equity=501.0, baseline=10_000.0), equity=501.0)
    # The absolute floor is not crossed at 501. The independent daily-loss
    # veto still blocks this separate, very large day loss.
    assert inside.rejection == "DAILY_LOSS_LIMIT_AUTH"

    inside_safe = _durable_result(_daily(equity=501.0, baseline=505.0), equity=501.0)
    assert inside_safe.accepted is True

    exact = _durable_result(_daily(equity=500.0, baseline=505.0), equity=500.0)
    assert exact.accepted is False
    assert exact.rejection == "EQUITY_FLOOR_BREACH"
    assert exact.disarm is True

    outside = _durable_result(_daily(equity=499.0, baseline=505.0), equity=499.0)
    assert outside.rejection == "EQUITY_FLOOR_BREACH"


def test_an_active_latch_vetoes_before_any_threshold_is_re_evaluated():
    from bridge.engine.types import RISK_CONTROL_DAILY_LOSS

    # Equity has fully recovered; the sticky latch still blocks.
    result = _durable_result(
        _daily(
            equity=10_500.0,
            baseline=10_000.0,
            peak=10_500.0,
            latches=(_latch(RISK_CONTROL_DAILY_LOSS),),
        ),
        equity=10_500.0,
    )
    assert result.accepted is False
    assert result.rejection == f"RISK_CONTROL_LATCHED:{RISK_CONTROL_DAILY_LOSS}"
    assert result.disarm is True
    blocked = [gate for gate in result.gate_results if gate["status"] == "BLOCK"]
    assert [gate["name"] for gate in blocked] == ["RISK_CONTROL_LATCH"]


def test_missing_or_mismatched_daily_state_fails_closed():
    from bridge.engine.types import (
        DAILY_RISK_CHECKPOINT_MISMATCH,
        DAILY_RISK_POLICY_MISMATCH,
        DAILY_RISK_STATE_REQUIRED,
    )

    engine = RiskEngine(_durable_config())

    missing = engine.evaluate_authoritative(
        signal=_signal(),
        snapshot=_snapshot(),
        stop_loss=95.0,
        daily_state=None,
        require_daily_state=True,
    )
    assert missing.accepted is False
    assert missing.rejection == DAILY_RISK_STATE_REQUIRED
    assert missing.disarm is True

    for bad in ({"equity": 1000.0}, object(), 1000.0):
        wrong_type = engine.evaluate_authoritative(
            signal=_signal(),
            snapshot=_snapshot(),
            stop_loss=95.0,
            daily_state=bad,
            require_daily_state=True,
        )
        assert wrong_type.rejection == DAILY_RISK_STATE_REQUIRED
        assert wrong_type.disarm is True

    other_checkpoint = _durable_result(
        _daily(
            equity=1000.0,
            baseline=1000.0,
            checkpoint_id="ckpt-v1:" + "e" * 64,
        )
    )
    assert other_checkpoint.rejection == DAILY_RISK_CHECKPOINT_MISMATCH
    assert other_checkpoint.disarm is True

    # Same checkpoint, different equity: two epochs mixed into one decision.
    mixed_equity = _durable_result(_daily(equity=999.0, baseline=1000.0), equity=1000.0)
    assert mixed_equity.rejection == DAILY_RISK_CHECKPOINT_MISMATCH

    stale_policy = _durable_result(
        _daily(
            equity=1000.0,
            baseline=1000.0,
            policy_version=_durable_policy(equity_floor_usdc=1.0).version,
        )
    )
    assert stale_policy.rejection == DAILY_RISK_POLICY_MISMATCH
    assert stale_policy.disarm is True


def test_v6_authoritative_path_is_byte_for_byte_unchanged_without_daily_state():
    engine = RiskEngine(_durable_config())
    baseline = engine.evaluate_authoritative(
        signal=_signal(), snapshot=_snapshot(), stop_loss=95.0
    )
    assert baseline.accepted is True
    names = [gate["name"] for gate in baseline.gate_results]
    assert "DAILY_RISK_STATE" not in names
    assert "EQUITY_STOP" not in names
    assert "MAX_DRAWDOWN" not in names
    assert "RISK_CONTROL_LATCH" not in names
    assert names[0] == "RISK_SNAPSHOT"


def test_durable_gates_run_before_sizing_and_emit_ordered_evidence():
    result = _durable_result(
        _daily(equity=9_900.0, baseline=10_000.0, peak=10_100.0), equity=9_900.0
    )
    assert result.accepted is True
    names = [gate["name"] for gate in result.gate_results]
    assert names.index("DAILY_RISK_STATE") < names.index("ACCOUNT")
    for control in ("RISK_CONTROL_LATCH", "EQUITY_STOP", "DAILY_LOSS_AUTH", "MAX_DRAWDOWN"):
        assert names.index("ACCOUNT") < names.index(control) < names.index("MIN_ORDER")
    detail = next(
        gate["detail"] for gate in result.gate_results if gate["name"] == "DAILY_LOSS_AUTH"
    )
    assert detail["baseline_equity"] == 10_000.0
    assert detail["daily_pnl"] == -100.0
    assert detail["threshold"] == -200.0
