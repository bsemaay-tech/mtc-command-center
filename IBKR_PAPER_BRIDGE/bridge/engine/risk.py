"""RiskEngine for pure sizing and gate checks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from bridge.engine.types import (
    DAILY_RISK_CHECKPOINT_MISMATCH,
    DAILY_RISK_POLICY_MISMATCH,
    DAILY_RISK_STATE_REQUIRED,
    RISK_SNAPSHOT_REQUIRED,
    AccountSnapshot,
    AuthoritativeRiskSnapshot,
    DailyRiskState,
    DurableRiskPolicy,
    OrderPlan,
    Signal,
)

Direction = Literal["BOTH", "LONG_ONLY", "SHORT_ONLY", "NO_TRADE"]


@dataclass(frozen=True)
class RiskConfig:
    policy_id: str = "ts-p1-007-v1"
    risk_pct_per_trade: float = 0.005
    max_daily_loss_pct: float = 0.02
    max_intraday_drawdown_pct: float = 0.05
    equity_floor_usdc: float = 500.0
    max_position_notional_pct: float = 0.20
    min_stop_distance_pct: float = 0.001
    min_order_usd: float = 10.0
    max_leverage: int = 1
    max_consecutive_losses: int = 3
    coin_enabled: bool = True
    feed_stale: bool = False
    app_armed: bool = True
    direction: Direction = "BOTH"
    size_decimals: int = 6


@dataclass
class RiskResult:
    accepted: bool
    plan: OrderPlan | None = None
    rejection: str | None = None
    gate_results: list[dict[str, Any]] = field(default_factory=list)
    disarm: bool = False
    latch_requests: tuple[str, ...] = ()


class RiskEngine:
    def __init__(self, config: RiskConfig | None = None) -> None:
        self.config = config or RiskConfig()
        self.policy = DurableRiskPolicy.create(
            policy_id=self.config.policy_id,
            max_daily_loss_pct=self.config.max_daily_loss_pct,
            max_intraday_drawdown_pct=self.config.max_intraday_drawdown_pct,
            equity_floor_usdc=self.config.equity_floor_usdc,
        )

    def evaluate_authoritative(
        self,
        signal: Signal,
        snapshot: AuthoritativeRiskSnapshot,
        stop_loss: float,
        take_profit: float | None = None,
        regime: Direction = "BOTH",
        realized_today: float = 0.0,
        consecutive_losses: int = 0,
        leverage: int = 1,
        daily_state: DailyRiskState | None = None,
        require_daily_state: bool = False,
    ) -> RiskResult:
        """The only entry-risk path allowed on an opt-in v6 store (TS-P1-006).

        Equity, available margin and open-position exposure are *derived from
        one immutable checkpoint view*, never from independently timed point
        reads. There is no dictionary or ``AccountSnapshot`` overload here on
        purpose: a caller-supplied mapping is exactly the time-of-check /
        time-of-use hole this path exists to close, so anything that is not a
        typed :class:`AuthoritativeRiskSnapshot` is a fail-closed veto rather
        than a fallback.

        Thresholds, gate order and sizing are unchanged; the snapshot only
        replaces where the inputs come from.
        """
        gates: list[dict[str, Any]] = []
        if not isinstance(snapshot, AuthoritativeRiskSnapshot):
            return self._reject(
                "RISK_SNAPSHOT", RISK_SNAPSHOT_REQUIRED, gates, disarm=True
            )
        gates.append(
            self._gate(
                "RISK_SNAPSHOT",
                {
                    "checkpoint_id": snapshot.checkpoint_id,
                    "attempt_id": snapshot.attempt_id,
                    "canonical_hash": snapshot.canonical_hash,
                    "payload_version": snapshot.payload_version,
                    "accepted_ts": snapshot.accepted_ts.isoformat(),
                    "age_s": snapshot.age_s,
                    "positions": len(snapshot.positions),
                },
            )
        )
        if require_daily_state:
            if not isinstance(daily_state, DailyRiskState):
                return self._reject(
                    "DAILY_RISK_STATE", DAILY_RISK_STATE_REQUIRED, gates, disarm=True
                )
            if (
                daily_state.checkpoint_id != snapshot.checkpoint_id
                or daily_state.attempt_id != snapshot.attempt_id
                or daily_state.run_id != snapshot.run_id
                or daily_state.equity != snapshot.equity
            ):
                return self._reject(
                    "DAILY_RISK_STATE",
                    DAILY_RISK_CHECKPOINT_MISMATCH,
                    gates,
                    disarm=True,
                )
            if daily_state.policy_version != self.policy.version:
                return self._reject(
                    "DAILY_RISK_STATE",
                    DAILY_RISK_POLICY_MISMATCH,
                    gates,
                    disarm=True,
                )
            gates.append(
                self._gate(
                    "DAILY_RISK_STATE",
                    {
                        "checkpoint_id": daily_state.checkpoint_id,
                        "trading_date": daily_state.trading_date,
                        "policy_version": daily_state.policy_version,
                    },
                )
            )
        # Any nonzero reconciled position blocks new entry through the existing
        # NO_OPEN_POSITION gate. Passing None here — as the predecessor did —
        # would authorize a second entry against exposure the accepted capture
        # already proved exists.
        open_positions = snapshot.open_positions
        return self._evaluate(
            signal=signal,
            account=snapshot.account(),
            stop_loss=stop_loss,
            take_profit=take_profit,
            regime=regime,
            open_position=open_positions[0] if open_positions else None,
            realized_today=realized_today,
            consecutive_losses=consecutive_losses,
            leverage=leverage,
            gates=gates,
            daily_state=daily_state if require_daily_state else None,
        )

    def evaluate(
        self,
        signal: Signal,
        account: AccountSnapshot | dict[str, float],
        stop_loss: float,
        take_profit: float | None = None,
        regime: Direction = "BOTH",
        open_position: object | None = None,
        realized_today: float = 0.0,
        consecutive_losses: int = 0,
        leverage: int = 1,
    ) -> RiskResult:
        """Predecessor entry point: unchanged, and default v4 behavior.

        Still accepts a mapping or an ``AccountSnapshot`` because the v4/v5
        path has no checkpoint to derive from. On a v6 store the engine never
        calls this — see ``BridgeEngine.on_bar``.
        """
        return self._evaluate(
            signal=signal,
            account=account,
            stop_loss=stop_loss,
            take_profit=take_profit,
            regime=regime,
            open_position=open_position,
            realized_today=realized_today,
            consecutive_losses=consecutive_losses,
            leverage=leverage,
            gates=[],
            daily_state=None,
        )

    def _evaluate(
        self,
        *,
        signal: Signal,
        account: AccountSnapshot | dict[str, float],
        stop_loss: float,
        take_profit: float | None,
        regime: Direction,
        open_position: object | None,
        realized_today: float,
        consecutive_losses: int,
        leverage: int,
        gates: list[dict[str, Any]],
        daily_state: DailyRiskState | None,
    ) -> RiskResult:
        """The one gate sequence. Order, thresholds and sizing are identical for
        both entry points; only the *provenance* of the inputs differs."""
        if not self.config.app_armed:
            return self._reject("STATE_ARMED", "STATE_NOT_ARMED", gates)
        gates.append(self._gate("STATE_ARMED"))

        if not self.config.coin_enabled or self.config.feed_stale:
            return self._reject("FEED_READY", "FEED_BLOCKED", gates)
        gates.append(self._gate("FEED_READY"))

        if open_position is not None:
            return self._reject("NO_OPEN_POSITION", "POSITION_EXISTS", gates)
        gates.append(self._gate("NO_OPEN_POSITION"))

        effective = self._intersect_direction(self.config.direction, regime)
        if signal.direction not in effective:
            return self._reject("DIRECTION", "DIRECTION_BLOCKED", gates)
        gates.append(self._gate("DIRECTION", {"effective": sorted(effective)}))

        if isinstance(account, AccountSnapshot):
            equity = account.equity
            available = account.available_margin
        else:
            equity = float(account.get("equity", 0.0))
            available = float(account.get("available_margin", 0.0))
        if equity <= 0 or available <= 0:
            return self._reject("ACCOUNT", "ACCOUNT_EQUITY_INVALID", gates)
        gates.append(self._gate("ACCOUNT"))

        if daily_state is not None:
            if daily_state.active_latches:
                return self._reject(
                    "RISK_CONTROL_LATCH",
                    f"RISK_CONTROL_LATCHED:{daily_state.active_latches[0].control}",
                    gates,
                    disarm=True,
                )
            gates.append(self._gate("RISK_CONTROL_LATCH"))

            if daily_state.equity <= self.policy.equity_floor_usdc:
                return self._reject(
                    "EQUITY_STOP", "EQUITY_FLOOR_BREACH", gates, disarm=True
                )
            gates.append(
                self._gate(
                    "EQUITY_STOP",
                    {
                        "equity": daily_state.equity,
                        "threshold": self.policy.equity_floor_usdc,
                    },
                )
            )

            daily_pnl = daily_state.daily_pnl
            daily_threshold = -(
                daily_state.baseline_equity * self.policy.max_daily_loss_pct
            )
            if daily_pnl <= daily_threshold:
                return self._reject(
                    "DAILY_LOSS_AUTH",
                    "DAILY_LOSS_LIMIT_AUTH",
                    gates,
                    disarm=True,
                )
            gates.append(
                self._gate(
                    "DAILY_LOSS_AUTH",
                    {
                        "baseline_equity": daily_state.baseline_equity,
                        "daily_pnl": daily_pnl,
                        "threshold": daily_threshold,
                    },
                )
            )

            drawdown = daily_state.peak_equity - daily_state.equity
            drawdown_threshold = (
                daily_state.peak_equity * self.policy.max_intraday_drawdown_pct
            )
            if drawdown >= drawdown_threshold:
                return self._reject(
                    "MAX_DRAWDOWN", "MAX_DRAWDOWN_LIMIT", gates, disarm=True
                )
            gates.append(
                self._gate(
                    "MAX_DRAWDOWN",
                    {
                        "peak_equity": daily_state.peak_equity,
                        "drawdown": drawdown,
                        "threshold": drawdown_threshold,
                    },
                )
            )
        else:
            if realized_today <= -(equity * self.config.max_daily_loss_pct):
                return self._reject(
                    "DAILY_LOSS", "DAILY_LOSS_LIMIT", gates, disarm=True
                )
            gates.append(self._gate("DAILY_LOSS"))

        if consecutive_losses >= self.config.max_consecutive_losses:
            return self._reject("CONSECUTIVE_LOSS", "CONSECUTIVE_LOSS_LIMIT", gates, disarm=True)
        gates.append(self._gate("CONSECUTIVE_LOSS"))

        if leverage > self.config.max_leverage:
            return self._reject("LEVERAGE", "LEVERAGE_CAP", gates)
        gates.append(self._gate("LEVERAGE"))

        stop_distance = abs(signal.ref_price - stop_loss)
        min_distance = signal.ref_price * self.config.min_stop_distance_pct
        if stop_distance < min_distance:
            return self._reject("STOP_DISTANCE", "STOP_TOO_CLOSE", gates)
        if signal.direction == "LONG" and stop_loss >= signal.ref_price:
            return self._reject("STOP_SIDE", "STOP_WRONG_SIDE", gates)
        if signal.direction == "SHORT" and stop_loss <= signal.ref_price:
            return self._reject("STOP_SIDE", "STOP_WRONG_SIDE", gates)
        gates.append(self._gate("STOP"))

        risk_dollars = equity * self.config.risk_pct_per_trade
        raw_qty = risk_dollars / stop_distance
        qty = round(raw_qty, self.config.size_decimals)
        notional = qty * signal.ref_price

        if notional < self.config.min_order_usd:
            return self._reject("MIN_ORDER", "MIN_ORDER_USD", gates)
        gates.append(self._gate("MIN_ORDER", {"notional": notional}))

        max_notional = equity * self.config.max_position_notional_pct * leverage
        if notional > max_notional:
            return self._reject("NOTIONAL", "NOTIONAL_CAP", gates)
        gates.append(self._gate("NOTIONAL", {"notional": notional, "max_notional": max_notional}))

        if notional / max(leverage, 1) > available * 0.95:
            return self._reject("MARGIN", "MARGIN_CAP", gates)
        gates.append(self._gate("MARGIN"))

        plan = OrderPlan(
            signal=signal,
            qty=qty,
            entry_type="MKT",
            limit_price=None,
            stop_loss=stop_loss,
            take_profit=take_profit,
            leverage=leverage,
            risk_dollars=round(risk_dollars, 8),
            risk_pct=self.config.risk_pct_per_trade,
        )
        return RiskResult(accepted=True, plan=plan, gate_results=gates)

    def _intersect_direction(self, config_direction: Direction, regime: Direction) -> set[str]:
        allowed = {
            "BOTH": {"LONG", "SHORT"},
            "LONG_ONLY": {"LONG"},
            "SHORT_ONLY": {"SHORT"},
            "NO_TRADE": set(),
        }
        return allowed[config_direction] & allowed[regime]

    @staticmethod
    def _gate(name: str, detail: dict[str, Any] | None = None) -> dict[str, Any]:
        return {"name": name, "status": "PASS", "detail": detail or {}}

    @staticmethod
    def _reject(
        gate: str,
        reason: str,
        gates: list[dict[str, Any]],
        disarm: bool = False,
    ) -> RiskResult:
        gates.append({"name": gate, "status": "BLOCK", "reason": reason})
        return RiskResult(False, rejection=reason, gate_results=gates, disarm=disarm)
