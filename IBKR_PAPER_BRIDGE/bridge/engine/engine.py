"""Continuous bridge engine plus deterministic replay entry point."""

from __future__ import annotations

import asyncio
import inspect
import sqlite3
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Callable

from bridge.broker.base import Broker
from bridge.engine.bars import BarFeed
from bridge.engine.llm_gate import NullLLMGate
from bridge.engine.orders import OrderManager
from bridge.engine.risk import RiskEngine
from bridge.engine.strategies.keltner_trail_ema8 import KeltnerTrailEma8
from bridge.engine.types import Bar, Position
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
    state: str = "DISARMED"
    coin: str = "BTC"
    timeframe: str = "1h"
    mode: str = "dry_run"
    on_update: Callable[[str, object], object] | None = None
    reconcile_interval_s: float = 60.0
    bars: list[Bar] = field(default_factory=list)
    reconcile_ready: bool = False
    _feed: BarFeed | None = field(default=None, init=False)
    _tasks: list[asyncio.Task] = field(default_factory=list, init=False)
    _kill_requested: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        self.order_manager = self.order_manager or OrderManager(self.store, self.broker, self.run_id)
        self.llm_gate = self.llm_gate or NullLLMGate()
        persisted = self.store.get_meta("app_state")
        if persisted is None:
            self.store.set_meta("app_state", self.state)
        else:
            self.state = persisted

    async def start(self, lookback: int = 300) -> None:
        self._ensure_run(mode=self.mode)
        await self.broker.connect()
        await self.order_manager.reconcile()
        self.reconcile_ready = True
        await self._publish("status", self.status())
        self._feed = BarFeed(
            broker=self.broker,
            coin=self.coin,
            timeframe=self.timeframe,
            on_bar_closed=self.on_bar,
            on_event=self._feed_event,
            on_stale=self._stale_disarm,
        )
        self.bars = await self._feed.start(lookback=lookback)
        stream = getattr(self.broker, "start_stream", None)
        if stream is not None:
            self._tasks.append(asyncio.create_task(stream(), name="mock-broker-stream"))
        self._tasks.append(asyncio.create_task(self._reconcile_loop(), name="bridge-reconciler"))

    async def stop(self) -> None:
        if self._feed is not None:
            await self._feed.stop()
        for task in self._tasks:
            task.cancel()
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()

    async def arm(self) -> None:
        if self._app_state() == "KILLED":
            raise RuntimeError("KILLED requires operator acknowledgement")
        if not self.reconcile_ready:
            raise RuntimeError("startup reconcile incomplete")
        self._kill_requested = False
        self._set_state("ARMED")
        await self._publish("status", self.status())

    def disarm(self) -> None:
        self._set_state("DISARMED")

    async def disarm_runtime(self) -> None:
        self.disarm()
        for order in await self.broker.open_orders():
            if order.role == "ENTRY":
                await self.broker.cancel(order.cloid)
        await self.order_manager.reconcile()
        await self._publish("status", self.status())

    async def kill(self, flatten: bool = False) -> None:
        self._kill_requested = True
        self._set_state("KILLED")
        await self.broker.cancel_all()
        if flatten:
            await self.broker.flatten(self.coin)
        await self._publish("status", self.status())

    async def acknowledge_kill(self) -> None:
        if self._app_state() != "KILLED":
            return
        self._kill_requested = False
        self._set_state("DISARMED")
        self.reconcile_ready = False
        await self.order_manager.reconcile()
        self.reconcile_ready = True
        await self._publish("status", self.status())

    async def run_replay(self, max_bars: int | None = None) -> None:
        self._ensure_run(mode="dry_run")
        await self.broker.connect()
        if self._app_state() != "ARMED":
            return
        replay: list[Bar] = []
        self.broker.subscribe_bars(self.coin, self.timeframe, replay.append)
        if max_bars is not None:
            replay = replay[:max_bars]
        for bar in replay:
            await self.on_bar(bar, process_broker_bar=True)

    async def on_bar(self, bar: Bar, process_broker_bar: bool = False) -> None:
        if not self.bars or bar.ts > self.bars[-1].ts:
            self.bars.append(bar)
        self.store.insert_bar(self.coin, self.timeframe, bar.ts, bar.open, bar.high, bar.low, bar.close, bar.volume)
        if process_broker_bar:
            process_bar = getattr(self.broker, "process_bar", None)
            if process_bar is not None:
                process_bar(bar)
        await self.order_manager.sync_broker_state()
        position = self._position_for(self.coin, await self.broker.positions())

        if position is not None:
            trail = self.strategy.trail_level(self.bars, position)
            if trail is not None:
                await self.order_manager.trail_position(position, trail)
            signal = self.strategy.on_bar(self.bars, position=position)
            if signal is not None and self._is_opposite(position, signal.direction):
                await self.order_manager.close_position(position)
                self.store.insert_decision(
                    self.run_id,
                    f"{self.run_id}:{signal.symbol}:{signal.ts.isoformat()}:CLOSE",
                    signal.ts,
                    signal.symbol,
                    "CLOSE_ONLY_SUBMITTED",
                    {"reason": "opposite_signal_flip_disabled"},
                )
            await self._publish("bar", bar.model_dump(mode="json"))
            return

        if self._app_state() != "ARMED" or self._kill_requested:
            await self._publish("bar", bar.model_dump(mode="json"))
            return
        signal = self.strategy.on_bar(self.bars, position=None)
        if signal is None:
            await self._publish("bar", bar.model_dump(mode="json"))
            return

        decision_uid = f"{self.run_id}:{signal.symbol}:{signal.ts.isoformat()}:{signal.direction}"
        self.store.insert_decision(self.run_id, decision_uid, signal.ts, signal.symbol, "SIGNAL", signal.model_dump(mode="json"))
        if signal.stop_loss is None:
            self.store.insert_decision(
                self.run_id,
                decision_uid,
                signal.ts,
                signal.symbol,
                "RISK_REJECT",
                {"reason": "STRATEGY_STOP_MISSING", "gates": []},
            )
            return
        risk = self.risk_engine.evaluate(
            signal=signal,
            account=await self.broker.account(),
            stop_loss=signal.stop_loss,
            take_profit=signal.take_profit,
            open_position=None,
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
            if risk.disarm:
                self.disarm()
                self.store.insert_event(self.run_id, datetime.now(UTC), "WARN", "RISK_AUTO_DISARM", str(risk.rejection))
            return
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
        if self._app_state() != "ARMED" or self._kill_requested:
            return
        if self._position_for(self.coin, await self.broker.positions()) is not None:
            return
        result = await self.order_manager.submit_plan(decision_uid, risk.plan)
        if result is not None:
            self.store.insert_decision(self.run_id, decision_uid, signal.ts, signal.symbol, "SUBMITTED", result)
        await self._publish("decision", {"decision_uid": decision_uid})

    def status(self) -> dict[str, object]:
        return {
            "state": self._app_state(),
            "reconcile_ready": self.reconcile_ready,
            "run_id": self.run_id,
            "coin": self.coin,
            "timeframe": self.timeframe,
        }

    async def _reconcile_loop(self) -> None:
        while True:
            await asyncio.sleep(self.reconcile_interval_s)
            await self.order_manager.reconcile()
            await self._publish("equity", {"run_id": self.run_id})

    async def _feed_event(self, code: str, detail: str) -> None:
        severity = "WARN" if code in {"DATA_STALE", "DISCONNECT", "RECONNECT_RETRY"} else "INFO"
        self.store.insert_event(self.run_id, datetime.now(UTC), severity, code, detail)
        await self._publish("event", {"code": code, "detail": detail})

    async def _stale_disarm(self) -> None:
        self.disarm()
        await self._publish("status", self.status())

    async def _publish(self, topic: str, data: object) -> None:
        if self.on_update is None:
            return
        result = self.on_update(topic, data)
        if inspect.isawaitable(result):
            await result

    def _ensure_run(self, mode: str) -> None:
        try:
            self.store.create_run(self.run_id, mode, "testnet", {"broker": type(self.broker).__name__})
        except sqlite3.IntegrityError:
            return

    def _app_state(self) -> str:
        persisted = self.store.get_meta("app_state")
        if persisted is not None:
            self.state = persisted
        return self.state

    def _set_state(self, state: str) -> None:
        self.state = state
        self.store.set_meta("app_state", state)

    @staticmethod
    def _position_for(coin: str, positions: list[Position]) -> Position | None:
        return next((position for position in positions if position.symbol == coin and position.size != 0), None)

    @staticmethod
    def _is_opposite(position: Position, direction: str) -> bool:
        return (position.size > 0 and direction == "SHORT") or (position.size < 0 and direction == "LONG")
