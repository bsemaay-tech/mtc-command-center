"""RiskEngine for pure sizing and gate checks."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Literal

from bridge.engine.types import (
    DAILY_RISK_CHECKPOINT_MISMATCH,
    DAILY_RISK_POLICY_MISMATCH,
    DAILY_RISK_STATE_REQUIRED,
    EXPOSURE_EVIDENCE_INVALID,
    ExposureRiskPolicy,
    LIQ_DISTANCE_BREACH,
    LEVERAGE_EFFECTIVE_BREACH,
    LEVERAGE_REPORTED_BREACH,
    PORTFOLIO_GROSS_BREACH,
    RISK_SNAPSHOT_REQUIRED,
    SNAPSHOT_PAYLOAD_VERSION_V3,
    SYMBOL_GROSS_BREACH,
    WALLET_UTIL_BREACH,
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
    # TS-P1-008 owner-approved (2026-07-27) exposure / leverage / liquidation
    # policy. Versioned configuration values, not permanent constants: a later
    # owner-approved change creates a new immutable ExposureRiskPolicy version.
    # Inert on v4-v7 stores; the gates run only on a v3 snapshot.
    exposure_policy_id: str = "ts-p1-008-v1"
    max_symbol_gross_pct: float = 0.20
    max_portfolio_gross_pct: float = 0.40
    max_wallet_margin_util_pct: float = 0.25
    max_effective_leverage: float = 1.0
    min_liquidation_distance_pct: float = 0.15


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
        self.exposure_policy = ExposureRiskPolicy.create(
            policy_id=self.config.exposure_policy_id,
            max_symbol_gross_pct=self.config.max_symbol_gross_pct,
            max_portfolio_gross_pct=self.config.max_portfolio_gross_pct,
            max_wallet_margin_util_pct=self.config.max_wallet_margin_util_pct,
            max_effective_leverage=self.config.max_effective_leverage,
            min_liquidation_distance_pct=self.config.min_liquidation_distance_pct,
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
        #
        # TS-P1-008: on a v3 snapshot the five exposure / leverage / liquidation
        # gates run here — after authority + policy validation and BEFORE the
        # existing NO_OPEN_POSITION gate (precedence §5: gates 4-8 precede 9).
        # They veto and DISARM on the first breach, with no broker mutation. A
        # v2 snapshot (v4-v7 stores) skips them, so predecessor behavior is
        # byte-for-byte unchanged.
        if snapshot.payload_version == SNAPSHOT_PAYLOAD_VERSION_V3:
            if snapshot.exposure_policy_version != self.exposure_policy.version:
                return RiskResult(
                    accepted=False,
                    rejection="EXPOSURE_POLICY_MISMATCH",
                    gate_results=gates,
                    disarm=True,
                )
            exposure_rejection = self._evaluate_exposure(
                snapshot=snapshot, signal=signal, stop_loss=stop_loss, gates=gates
            )
            if exposure_rejection is not None:
                return RiskResult(
                    accepted=False,
                    rejection=exposure_rejection,
                    gate_results=gates,
                    disarm=True,
                )
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

    # ------------------------------------------------------------------
    # TS-P1-008 exposure / leverage / liquidation gates (v3 snapshot only)
    # ------------------------------------------------------------------

    def _evaluate_exposure(
        self,
        *,
        snapshot: AuthoritativeRiskSnapshot,
        signal: Signal,
        stop_loss: float,
        gates: list[dict[str, Any]],
    ) -> str | None:
        """Run the five deterministic fail-closed gates for a v3 snapshot.

        Precedence (§5): evidence validity -> liquidation distance -> reported
        then effective leverage -> symbol gross -> portfolio gross -> wallet
        utilization. The projected order is included exactly once. Every gate
        is fail-closed at its exact boundary. Appends one PASS gate per cleared
        check, or one BLOCK gate (with secret-safe detail) on the first breach,
        and returns that breach's reason code; returns ``None`` when all pass.
        """
        policy = self.exposure_policy
        equity = snapshot.equity
        checkpoint_id = snapshot.checkpoint_id

        def block(name: str, reason: str, detail: dict[str, Any]) -> str:
            gates.append(
                {"name": name, "status": "BLOCK", "reason": reason, "detail": detail}
            )
            return reason

        # Gate 3: account + position evidence validity.
        if not math.isfinite(equity) or equity <= 0.0:
            return block(
                "EXPOSURE_EVIDENCE",
                EXPOSURE_EVIDENCE_INVALID,
                {"scope": "EQUITY", "equity": equity, "checkpoint_id": checkpoint_id},
            )
        for row in snapshot.positions:
            if row.size == 0.0:
                # A flat row carries no exposure; its v3 valuation fields are
                # optional and it contributes nothing to any gate below.
                continue
            sub_reason = self._validate_v3_row(row)
            if sub_reason is not None:
                return block(
                    "EXPOSURE_EVIDENCE",
                    EXPOSURE_EVIDENCE_INVALID,
                    {
                        "scope": "POSITION",
                        "symbol": row.symbol,
                        "reason": sub_reason,
                        "checkpoint_id": checkpoint_id,
                        "policy_version": policy.version,
                    },
                )
        gates.append(
            self._gate(
                "EXPOSURE_EVIDENCE",
                {
                    "equity": equity,
                    "positions": len(snapshot.positions),
                    "checkpoint_id": checkpoint_id,
                    "policy_version": policy.version,
                },
            )
        )

        nonzero = [row for row in snapshot.positions if row.size != 0.0]
        projected = self._projected_notional(equity, signal.ref_price, stop_loss)

        # Gate 4: directional liquidation distance (existing positions only).
        for row in nonzero:
            mark = row.mark_price  # type: ignore[assignment]
            liq = row.liquidation_px
            assert mark is not None and liq is not None  # validated above
            distance = (mark - liq) / mark if row.size > 0 else (liq - mark) / mark
            detail = {
                "symbol": row.symbol,
                "side": "LONG" if row.size > 0 else "SHORT",
                "mark": mark,
                "liquidation_px": liq,
                "distance": distance,
                "minimum": policy.min_liquidation_distance_pct,
                "checkpoint_id": checkpoint_id,
                "policy_version": policy.version,
            }
            # Exact minimum blocks: at or below the floor fails closed.
            if distance <= policy.min_liquidation_distance_pct:
                return block("LIQUIDATION_DISTANCE", LIQ_DISTANCE_BREACH, detail)
        gates.append(
            self._gate(
                "LIQUIDATION_DISTANCE",
                {
                    "positions": len(nonzero),
                    "minimum": policy.min_liquidation_distance_pct,
                    "policy_version": policy.version,
                },
            )
        )

        # Gate 5a: reported exchange leverage per nonzero position.
        for row in nonzero:
            if row.leverage > policy.max_effective_leverage:
                return block(
                    "LEVERAGE",
                    LEVERAGE_REPORTED_BREACH,
                    {
                        "symbol": row.symbol,
                        "reported_leverage": row.leverage,
                        "maximum": policy.max_effective_leverage,
                        "checkpoint_id": checkpoint_id,
                        "policy_version": policy.version,
                    },
                )

        # Gate 5b: effective wallet leverage (portfolio gross / equity).
        existing_gross = sum(row.position_value for row in nonzero)
        portfolio_gross = existing_gross + projected
        effective = portfolio_gross / equity
        if effective > policy.max_effective_leverage:
            return block(
                "EFFECTIVE_LEVERAGE",
                LEVERAGE_EFFECTIVE_BREACH,
                {
                    "portfolio_gross": portfolio_gross,
                    "equity": equity,
                    "effective_leverage": effective,
                    "maximum": policy.max_effective_leverage,
                    "checkpoint_id": checkpoint_id,
                    "policy_version": policy.version,
                },
            )
        gates.append(
            self._gate(
                "EFFECTIVE_LEVERAGE",
                {
                    "effective_leverage": effective,
                    "maximum": policy.max_effective_leverage,
                    "policy_version": policy.version,
                },
            )
        )

        # Gate 6: per-symbol gross exposure (existing same-symbol + projected).
        symbol_cap = equity * policy.max_symbol_gross_pct
        per_symbol: dict[str, float] = {}
        for row in nonzero:
            symbol = row.symbol.strip().upper()
            per_symbol[symbol] = per_symbol.get(symbol, 0.0) + row.position_value
        signal_symbol = signal.symbol.strip().upper()
        if signal_symbol:
            per_symbol[signal_symbol] = per_symbol.get(signal_symbol, 0.0) + projected
        breached_symbol = next(
            (
                (symbol, gross)
                for symbol, gross in sorted(per_symbol.items())
                if gross >= symbol_cap
            ),
            None,
        )
        detail_symbol = breached_symbol[0] if breached_symbol else signal_symbol
        symbol_gross = (
            breached_symbol[1]
            if breached_symbol
            else per_symbol.get(signal_symbol, 0.0)
        )
        symbol_detail = {
            "symbol": detail_symbol,
            "symbol_gross": symbol_gross,
            "cap": symbol_cap,
            "existing": sum(
                row.position_value
                for row in nonzero
                if row.symbol.strip().upper() == detail_symbol
            ),
            "projected": projected if detail_symbol == signal_symbol else 0.0,
            "checkpoint_id": checkpoint_id,
            "policy_version": policy.version,
        }
        # Exact cap blocks: at or above the cap fails closed.
        if breached_symbol is not None:
            return block("SYMBOL_GROSS", SYMBOL_GROSS_BREACH, symbol_detail)
        gates.append(self._gate("SYMBOL_GROSS", symbol_detail))

        # Gate 7: portfolio gross exposure (whole wallet, no netting).
        portfolio_cap = equity * policy.max_portfolio_gross_pct
        portfolio_detail = {
            "portfolio_gross": portfolio_gross,
            "cap": portfolio_cap,
            "existing": existing_gross,
            "projected": projected,
            "checkpoint_id": checkpoint_id,
            "policy_version": policy.version,
        }
        if portfolio_gross >= portfolio_cap:
            return block("PORTFOLIO_GROSS", PORTFOLIO_GROSS_BREACH, portfolio_detail)
        gates.append(self._gate("PORTFOLIO_GROSS", portfolio_detail))

        # Gate 8: wallet margin utilization (same-checkpoint margin_used / equity).
        utilization = snapshot.margin_used / equity
        util_detail = {
            "margin_used": snapshot.margin_used,
            "equity": equity,
            "utilization": utilization,
            "cap": policy.max_wallet_margin_util_pct,
            "checkpoint_id": checkpoint_id,
            "policy_version": policy.version,
        }
        if utilization >= policy.max_wallet_margin_util_pct:
            return block("WALLET_UTILIZATION", WALLET_UTIL_BREACH, util_detail)
        gates.append(self._gate("WALLET_UTILIZATION", util_detail))

        return None

    def evaluate_snapshot_exposure(
        self, snapshot: AuthoritativeRiskSnapshot
    ) -> str | None:
        """Validate current v3 wallet risk for ARM/restart, without a new order."""
        if snapshot.payload_version != SNAPSHOT_PAYLOAD_VERSION_V3:
            return None
        if snapshot.exposure_policy_version != self.exposure_policy.version:
            return "EXPOSURE_POLICY_MISMATCH"
        gates: list[dict[str, Any]] = []
        return self._evaluate_exposure(
            snapshot=snapshot,
            signal=Signal(
                ts=snapshot.loaded_ts,
                symbol="",
                direction="FLAT",
                reason="ARM_SNAPSHOT_VALIDATION",
                ref_price=0.0,
                stop_loss=0.0,
            ),
            stop_loss=0.0,
            gates=gates,
        )

    @staticmethod
    def _validate_v3_row(row: object) -> str | None:
        """Return a secret-free sub-reason if a nonzero v3 row's evidence is
        missing, non-finite, negative, incoherent, or wrong-sided; else None."""
        position_value = getattr(row, "position_value", None)
        size = getattr(row, "size", 0.0)
        leverage = getattr(row, "leverage", None)
        liquidation_px = getattr(row, "liquidation_px", None)
        if position_value is None:
            return "V3_FIELDS_REQUIRED"
        if not isinstance(position_value, (int, float)) or not math.isfinite(
            float(position_value)
        ):
            return "POSITION_VALUE_NONFINITE"
        if float(position_value) < 0.0:
            return "POSITION_VALUE_NEGATIVE"
        if size != 0.0 and float(position_value) <= 0.0:
            return "POSITION_VALUE_ZERO_FOR_NONZERO_SIZE"
        mark = getattr(row, "mark_price", None)
        if size != 0.0 and (
            mark is None
            or not isinstance(mark, (int, float))
            or not math.isfinite(float(mark))
            or float(mark) <= 0.0
        ):
            return "MARK_INCOHERENT"
        if leverage is None or not isinstance(leverage, (int, float)) or not math.isfinite(
            float(leverage)
        ):
            return "LEVERAGE_INVALID"
        if float(leverage) <= 0.0:
            return "LEVERAGE_INVALID"
        if size != 0.0:
            if liquidation_px is None or not isinstance(
                liquidation_px, (int, float)
            ) or not math.isfinite(float(liquidation_px)):
                return "LIQUIDATION_MISSING"
            if float(liquidation_px) <= 0.0:
                return "LIQUIDATION_MISSING"
            if mark is None:
                return "MARK_INCOHERENT"
            if size > 0 and float(liquidation_px) >= float(mark):
                return "LIQUIDATION_WRONG_SIDE"
            if size < 0 and float(liquidation_px) <= float(mark):
                return "LIQUIDATION_WRONG_SIDE"
        return None

    def _projected_notional(
        self, equity: float, ref_price: float, stop_loss: float
    ) -> float:
        """Gross notional of the one projected order, using the exact sizing
        formula the NOTIONAL gate uses. A degenerate stop cannot size an order,
        so it projects zero; the STOP gate rejects later. Counted exactly once
        because the sizing is deterministic in the snapshot equity and signal."""
        stop_distance = abs(ref_price - stop_loss)
        if not math.isfinite(stop_distance) or stop_distance <= 0.0:
            return 0.0
        risk_dollars = equity * self.config.risk_pct_per_trade
        qty = round(risk_dollars / stop_distance, self.config.size_decimals)
        return qty * ref_price

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
