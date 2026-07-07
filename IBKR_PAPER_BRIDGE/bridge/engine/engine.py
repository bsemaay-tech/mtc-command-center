"""Main dry-run loop orchestrator."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass

from bridge.broker.base import Broker
from bridge.engine.llm_gate import NullLLMGate
from bridge.engine.orders import OrderManager
from bridge.engine.risk import RiskEngine
from bridge.engine.strategies.keltner_trail_ema8 import KeltnerTrailEma8
from bridge.engine.types import Bar
from bridge.store.db import Store


@dataclass
class BridgeEngine:
    run_id: str
    broker: Broker
    store: Store
    strategy: KeltnerTrailEma8
    risk_engine: RiskEngine
    order_manager: OrderManager | None = None
    llm_gate: NullLLMGate | None = None
    state: str = "ARMED"

    def __post_init__(self) -> None:
        self.order_manager = self.order_manager or OrderManager(self.store, self.broker, self.run_id)
        self.llm_gate = self.llm_gate or NullLLMGate()

    def disarm(self) -> None:
        self.state = "DISARMED"

    async def run_replay(self, max_bars: int | None = None) -> None:
        self._ensure_run()
        await self.broker.connect()
        if self.state != "ARMED":
            return

        bars: list[Bar] = []
        coin = getattr(self.strategy, "symbol", "BTC")
        self.broker.subscribe_bars(coin, "1h", bars.append)
        if max_bars is not None:
            bars = bars[:max_bars]
        for idx, bar in enumerate(bars):
            self.store.insert_bar(coin, "1h", bar.ts, bar.open, bar.high, bar.low, bar.close, bar.volume)
            if self.state != "ARMED":
                return
            signal = self.strategy.on_bar(bars[: idx + 1], position=None)
            if signal is None:
                continue

            decision_uid = f"{self.run_id}:{signal.symbol}:{signal.ts.isoformat()}:{signal.direction}"
            self.store.insert_decision(self.run_id, decision_uid, signal.ts, signal.symbol, "SIGNAL", signal.model_dump(mode="json"))
            stop_loss = signal.ref_price * (0.95 if signal.direction == "LONG" else 1.05)
            take_profit = signal.ref_price * (1.05 if signal.direction == "LONG" else 0.95)
            risk = self.risk_engine.evaluate(
                signal=signal,
                account=await self.broker.account(),
                stop_loss=stop_loss,
                take_profit=take_profit,
            )
            if not risk.accepted or risk.plan is None:
                self.store.insert_decision(
                    self.run_id,
                    decision_uid,
                    signal.ts,
                    signal.symbol,
                    "RISK_REJECT",
                    {"reason": risk.rejection, "gates": risk.gate_results},
                )
                continue

            self.store.insert_decision(
                self.run_id,
                decision_uid,
                signal.ts,
                signal.symbol,
                "RISK_PASS",
                {"order_plan": risk.plan.model_dump(mode="json"), "gates": risk.gate_results},
            )
            llm = await self.llm_gate.check(risk.plan)
            self.store.insert_decision(
                self.run_id,
                decision_uid,
                signal.ts,
                signal.symbol,
                "LLM_SKIPPED",
                {"reason": llm.reason},
            )
            if self.state != "ARMED":
                return
            result = await self.order_manager.submit_plan(decision_uid, risk.plan)
            if result is not None:
                self.store.insert_decision(self.run_id, decision_uid, signal.ts, signal.symbol, "SUBMITTED", result)

    def _ensure_run(self) -> None:
        try:
            self.store.create_run(self.run_id, "dry_run", "testnet", {"broker": "mock"})
        except sqlite3.IntegrityError:
            return
