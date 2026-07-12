from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta

from bridge.engine.bars import BarFeed, BarFinalizer
from bridge.engine.types import AccountSnapshot, Bar


def test_wall_clock_timer_finalizes_quiet_candle_once():
    emitted: list[Bar] = []
    finalizer = BarFinalizer(on_bar_closed=emitted.append, timeframe="1h")
    opened = datetime(2026, 7, 12, 10, tzinfo=UTC)
    finalizer.on_candle(_candle(opened, opened + timedelta(hours=1)))

    assert finalizer.finalize_due(opened + timedelta(minutes=59)) is False
    assert finalizer.finalize_due(opened + timedelta(hours=1)) is True
    assert finalizer.finalize_due(opened + timedelta(hours=2)) is False
    assert [bar.ts for bar in emitted] == [opened]


def test_reconnect_duplicate_is_deduped_by_feed():
    asyncio.run(_reconnect_duplicate_is_deduped())


def test_data_stale_emits_and_disarms_once():
    asyncio.run(_data_stale_emits_and_disarms_once())


async def _reconnect_duplicate_is_deduped() -> None:
    base = datetime(2026, 7, 12, 10, tzinfo=UTC)
    broker = FeedBroker([_bar(base)])
    emitted: list[Bar] = []
    events: list[tuple[str, str]] = []
    feed = BarFeed(broker, "BTC", "1h", emitted.append, lambda code, detail: events.append((code, detail)))
    await feed.start(lookback=1)
    broker.emit(_bar(base))
    broker.emit(_bar(base + timedelta(hours=1)))
    assert await feed.reconnect(attempts=1, base_delay=0) is True
    broker.emit(_bar(base + timedelta(hours=1)))
    broker.emit(_bar(base + timedelta(hours=2)))
    await feed.stop()

    assert [bar.ts for bar in emitted] == [base + timedelta(hours=1), base + timedelta(hours=2)]
    assert broker.resubscribe_count == 1
    assert [code for code, _ in events] == ["DISCONNECT", "RECONNECT"]


async def _data_stale_emits_and_disarms_once() -> None:
    base = datetime(2026, 7, 12, 10, tzinfo=UTC)
    broker = FeedBroker([_bar(base)])
    events: list[tuple[str, str]] = []
    disarms: list[bool] = []
    feed = BarFeed(
        broker,
        "BTC",
        "1h",
        lambda bar: None,
        lambda code, detail: events.append((code, detail)),
        lambda: disarms.append(True),
    )
    feed.last_bar_update = base
    await feed.check_once(base + timedelta(hours=2, seconds=1))
    await feed.check_once(base + timedelta(hours=3))

    assert [code for code, _ in events] == ["DATA_STALE"]
    assert disarms == [True]


def _bar(ts: datetime) -> Bar:
    return Bar(ts=ts, open=100, high=101, low=99, close=100, volume=1)


def _candle(opened: datetime, closed: datetime) -> dict:
    return {
        "t": int(opened.timestamp() * 1000),
        "T": int(closed.timestamp() * 1000),
        "o": "100",
        "h": "101",
        "l": "99",
        "c": "100",
        "v": "1",
    }


class FeedBroker:
    def __init__(self, historical: list[Bar]) -> None:
        self.historical = historical
        self.callback = None
        self.resubscribe_count = 0
        self.connected = False
        self.last_bar_update = historical[-1].ts if historical else None

    async def connect(self) -> None:
        self.connected = True

    async def account(self) -> AccountSnapshot:
        return AccountSnapshot(equity=1000, available_margin=1000)

    async def positions(self):
        return []

    async def open_orders(self):
        return []

    async def historical_bars(self, coin, tf, lookback):
        return self.historical[-lookback:]

    def subscribe_bars(self, coin, tf, on_bar_closed):
        self.callback = on_bar_closed

    async def place_bracket(self, plan):
        return {}

    async def modify_stop(self, cloid, new_stop):
        return None

    async def cancel(self, cloid):
        return None

    async def cancel_all(self):
        return None

    async def flatten(self, coin):
        return None

    async def resubscribe(self):
        self.resubscribe_count += 1

    def emit(self, bar: Bar) -> None:
        assert self.callback is not None
        self.last_bar_update = bar.ts
        self.callback(bar)
