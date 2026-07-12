"""Broker protocol (abstract interface)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Protocol

from bridge.engine.types import AccountSnapshot, Bar, BrokerEvent, BrokerOrder, OrderPlan, Position


class Broker(Protocol):
    """Abstract broker interface for exchange operations."""

    async def connect(self) -> None:
        ...

    async def account(self) -> AccountSnapshot:
        ...

    async def positions(self) -> list[Position]:
        ...

    async def open_orders(self) -> list[BrokerOrder]:
        ...

    async def historical_bars(self, coin: str, tf: str, lookback: int) -> list[Bar]:
        ...

    def subscribe_bars(self, coin: str, tf: str, on_bar_closed: Callable[[Bar], None]) -> None:
        ...

    def subscribe_user_events(self, on_event: Callable[[BrokerEvent], None]) -> None:
        ...

    async def place_bracket(self, plan: OrderPlan) -> dict[str, Any]:
        ...

    async def modify_stop(self, cloid: str, new_stop: float) -> None:
        ...

    async def cancel(self, cloid: str) -> None:
        ...

    async def cancel_all(self) -> None:
        ...

    async def flatten(self, coin: str) -> None:
        ...

    async def reprotect_position(
        self,
        position: Position,
        stop_loss: float,
        take_profit: float | None,
        decision_uid: str,
    ) -> dict[str, Any] | None:
        ...
