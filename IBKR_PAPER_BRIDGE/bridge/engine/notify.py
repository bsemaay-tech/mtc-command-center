"""Fail-silent Telegram notifier (architecture §6.7).

Both env vars unset => disabled, no error. A notification failure NEVER
blocks or raises into the trading path. 5 s hard timeout, fire-and-forget.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Awaitable, Callable

import httpx

from bridge.settings import resolve_telegram_credentials

Sender = Callable[[dict], None | Awaitable[None]]


@dataclass
class TelegramNotifier:
    enabled: bool = False
    sender: Sender | None = None

    async def send(self, severity: str, message: str) -> None:
        if not self.enabled or self.sender is None:
            return
        payload = {"text": f"[{severity}] {message}"}
        try:
            result = self.sender(payload)
            if asyncio.iscoroutine(result):
                await asyncio.wait_for(result, timeout=5)
        except Exception:  # noqa: BLE001 - notifications must never raise
            return

    async def heartbeat(self, position: str, equity: str, last_bar: str) -> None:
        await self.send("INFO", f"bridge alive | position={position} equity={equity} last_bar={last_bar}")


def _http_sender(bot_token: str, chat_id: str) -> Sender:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    async def send(payload: dict) -> None:
        async with httpx.AsyncClient(timeout=5) as client:
            await client.post(url, json={"chat_id": chat_id, "text": payload["text"]})

    return send


def build_notifier(enabled: bool = True) -> TelegramNotifier:
    """Factory: resolves creds via process env then user registry (E1
    pattern). Missing creds => disabled notifier, no error, nothing logged."""
    if not enabled:
        return TelegramNotifier(enabled=False)
    token, chat_id = resolve_telegram_credentials()
    if not token or not chat_id:
        return TelegramNotifier(enabled=False)
    return TelegramNotifier(enabled=True, sender=_http_sender(token, chat_id))
