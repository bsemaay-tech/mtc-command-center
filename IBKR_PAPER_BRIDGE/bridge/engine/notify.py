"""Fail-silent Telegram notifier."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Awaitable, Callable

Sender = Callable[[dict], None | Awaitable[None]]


@dataclass
class TelegramNotifier:
    enabled: bool = False
    sender: Sender | None = None

    async def send(self, severity: str, message: str) -> None:
        if not self.enabled:
            return
        payload = {"text": f"[{severity}] {message}"}
        try:
            if self.sender is None:
                return
            result = self.sender(payload)
            if asyncio.iscoroutine(result):
                await asyncio.wait_for(result, timeout=5)
        except Exception:
            return

    async def heartbeat(self, position: str, equity: str, last_bar: str) -> None:
        await self.send("INFO", f"bridge alive | position={position} equity={equity} last_bar={last_bar}")
