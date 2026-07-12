"""Historical warmup, candle finalization, reconnect, and staleness control."""

from __future__ import annotations

import asyncio
import inspect
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Awaitable, Callable

from bridge.broker.base import Broker
from bridge.engine.types import Bar

BarCallback = Callable[[Bar], object]
EventCallback = Callable[[str, str], object]


def timeframe_delta(timeframe: str) -> timedelta:
    units = {"m": "minutes", "h": "hours", "d": "days"}
    suffix = timeframe[-1].lower()
    if suffix not in units:
        raise ValueError(f"unsupported timeframe: {timeframe}")
    value = int(timeframe[:-1])
    return timedelta(**{units[suffix]: value})


@dataclass
class BarFinalizer:
    """Turn incremental Hyperliquid candles into exactly-once closed bars."""

    on_bar_closed: BarCallback
    timeframe: str = "1h"
    already_processed: Callable[[datetime], bool] | None = None
    current: Bar | None = None
    current_close_ts: datetime | None = None
    emitted: set[datetime] = field(default_factory=set)
    last_update: datetime | None = None

    def on_candle(self, message: dict) -> None:
        candle = message.get("data", message)
        opened = datetime.fromtimestamp(int(candle["t"]) / 1000, tz=UTC)
        close_raw = candle.get("T")
        closes = (
            datetime.fromtimestamp(int(close_raw) / 1000, tz=UTC)
            if close_raw is not None
            else opened + timeframe_delta(self.timeframe)
        )
        bar = Bar(
            ts=opened,
            open=float(candle["o"]),
            high=float(candle["h"]),
            low=float(candle["l"]),
            close=float(candle["c"]),
            volume=float(candle["v"]),
        )
        self.last_update = datetime.now(UTC)
        if self.current is not None and opened > self.current.ts:
            self._emit(self.current)
        if self.current is None or opened >= self.current.ts:
            self.current = bar
            self.current_close_ts = closes

    def finalize_due(self, now: datetime | None = None) -> bool:
        now = now or datetime.now(UTC)
        if self.current is None or self.current_close_ts is None or now < self.current_close_ts:
            return False
        return self._emit(self.current)

    def _emit(self, bar: Bar) -> bool:
        if bar.ts in self.emitted:
            return False
        if self.already_processed is not None and self.already_processed(bar.ts):
            self.emitted.add(bar.ts)
            return False
        self.emitted.add(bar.ts)
        result = self.on_bar_closed(bar)
        if inspect.isawaitable(result):
            asyncio.get_running_loop().create_task(result)
        return True


class BarFeed:
    """Broker-neutral feed supervisor used by dry-run and testnet runtimes."""

    def __init__(
        self,
        broker: Broker,
        coin: str,
        timeframe: str,
        on_bar_closed: BarCallback,
        on_event: EventCallback | None = None,
        on_stale: Callable[[], object] | None = None,
        poll_seconds: float = 1.0,
    ) -> None:
        self.broker = broker
        self.coin = coin
        self.timeframe = timeframe
        self.on_bar_closed = on_bar_closed
        self.on_event = on_event
        self.on_stale = on_stale
        self.poll_seconds = poll_seconds
        self.last_bar_update: datetime | None = None
        self.warmup: list[Bar] = []
        self._stop = asyncio.Event()
        self._task: asyncio.Task | None = None
        self._stale_emitted = False

    async def start(self, lookback: int = 300) -> list[Bar]:
        self.warmup = await self.broker.historical_bars(self.coin, self.timeframe, lookback)
        if self.warmup:
            self.last_bar_update = self.warmup[-1].ts
        self.broker.subscribe_bars(self.coin, self.timeframe, self._receive_bar)
        self._task = asyncio.create_task(self._watchdog(), name=f"bar-feed-{self.coin}-{self.timeframe}")
        return list(self.warmup)

    async def stop(self) -> None:
        self._stop.set()
        if self._task is not None:
            self._task.cancel()
            await asyncio.gather(self._task, return_exceptions=True)

    def _receive_bar(self, bar: Bar) -> None:
        if self.last_bar_update is not None and bar.ts <= self.last_bar_update:
            return
        self.last_bar_update = bar.ts
        self._stale_emitted = False
        result = self.on_bar_closed(bar)
        if inspect.isawaitable(result):
            asyncio.get_running_loop().create_task(result)

    async def check_once(self, now: datetime | None = None) -> None:
        now = now or datetime.now(UTC)
        finalize_due = getattr(self.broker, "finalize_due", None)
        if finalize_due is not None:
            finalize_due(now)
        reference = getattr(self.broker, "last_bar_update", None) or self.last_bar_update
        if reference is None:
            return
        if now - reference > 2 * timeframe_delta(self.timeframe) and not self._stale_emitted:
            self._stale_emitted = True
            await self._call(self.on_event, "DATA_STALE", f"last_update={reference.isoformat()}")
            await self._call(self.on_stale)

    async def reconnect(self, attempts: int = 5, base_delay: float = 5.0) -> bool:
        await self._call(self.on_event, "DISCONNECT", "bar feed disconnected")
        for attempt in range(attempts):
            try:
                await self.broker.connect()
                resubscribe = getattr(self.broker, "resubscribe", None)
                if resubscribe is not None:
                    await resubscribe()
                await self._call(self.on_event, "RECONNECT", f"attempt={attempt + 1}")
                return True
            except Exception as exc:
                await self._call(self.on_event, "RECONNECT_RETRY", f"attempt={attempt + 1}; error={type(exc).__name__}")
                if attempt + 1 < attempts:
                    await asyncio.sleep(min(base_delay * (2**attempt), 60.0))
        return False

    async def _watchdog(self) -> None:
        while not self._stop.is_set():
            await self.check_once()
            await asyncio.sleep(self.poll_seconds)

    @staticmethod
    async def _call(callback: Callable | None, *args) -> None:
        if callback is None:
            return
        result = callback(*args)
        if isinstance(result, Awaitable) or inspect.isawaitable(result):
            await result
