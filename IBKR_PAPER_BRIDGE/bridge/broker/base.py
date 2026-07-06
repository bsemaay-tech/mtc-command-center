"""Broker protocol (abstract interface)."""

from __future__ import annotations

from typing import Protocol


class Broker(Protocol):
    """Abstract broker interface for exchange operations."""

    async def connect(self) -> None:
        ...

    async def account(self) -> dict:
        ...

    async def positions(self) -> list:
        ...

    async def open_orders(self) -> list:
        ...

    async def historical_bars(self, coin: str, tf: str, lookback: int) -> list:
        ...

    def subscribe_bars(self, coin: str, tf: str, on_bar_closed) -> None:
        ...

    async def place_bracket(self, plan) -> dict:
        ...

    async def modify_stop(self, cloid: str, new_stop: float) -> None:
        ...

    async def cancel(self, cloid: str) -> None:
        ...

    async def cancel_all(self) -> None:
        ...

    async def flatten(self, coin: str) -> None:
        ...
