"""Offline public market-bar collector core with monthly append-only archives.

Importing this module is inert. Runtime startup remains unconditionally refused
until the owner ratifies both a permission protocol and a concrete backend.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Callable, Mapping, Protocol, Sequence


INTERVAL_MS = {
    "15m": 15 * 60 * 1000,
    "1h": 60 * 60 * 1000,
    "4h": 4 * 60 * 60 * 1000,
    "1d": 24 * 60 * 60 * 1000,
}
INITIAL_SYMBOLS = ("BTC",)
INITIAL_INTERVALS = tuple(INTERVAL_MS)

# These are questions, not defaults.  The accepted design says exactly these
# seventeen tags remain open after decisions 104-109.
UNSET_NUMERIC_QUESTIONS = {
    "OPEN-F3": "Should any interval override the decided aging and stale offsets, and if so by how much?",
    "OPEN-F4": "How long may RECOVERING last before escalation?",
    "OPEN-N2": "How many WebSocket connections should be active, and how should subscriptions be split among them?",
    "OPEN-N3": "What reconnect-backoff base, ceiling, and jitter should be used?",
    "OPEN-N4": "After how many consecutive reconnect failures may DEGRADED snapshot polling begin?",
    "OPEN-N5": "Should the canonical bar key use the bar-open time or the bar-close time?",
    "OPEN-N6": "What host-versus-venue clock skew should raise the alarm?",
    "OPEN-N7": "What snapshot batch size and inter-request pacing should be used?",
    "OPEN-N8": "What OHLCV difference tolerance should mark native producers as divergent?",
    "OPEN-N10": "How much native/proxy overlap is enough to trigger the one-time divergence study?",
    "OPEN-N11": "For 1h, 4h, and 1d data, how near the retention edge should DEGRADED be raised?",
    "OPEN-N12": "Which still-unset WP-P0-21 data-quality thresholds should this collector inherit?",
    "OPEN-N13": "What backtest-versus-forward divergence tolerance should WP-P0-21 use?",
    "OPEN-N14": "What is the maximum allowed time from collector failure detection to owner notification delivery?",
    "OPEN-N17": "What minimum admissible price and volume bounds should be enforced?",
    "OPEN-N18": "How often may snapshot polling run while the feed is DEGRADED?",
    "OPEN-N19": "How many consecutive beyond-tolerance reconciliations are required before DRIFT?",
}

_SAFE_PART = re.compile(r"^[A-Za-z0-9._-]+$")
class CollectionRefused(RuntimeError):
    """Collection could not proceed without guessing or crossing authority."""


@dataclass(frozen=True)
class HashContract:
    fields: tuple[str, ...]
    algorithm: str
    encoding: str
    serialization: str

    def digest(self, record: Mapping[str, object]) -> str:
        missing = [field for field in self.fields if field not in record]
        if missing:
            raise CollectionRefused(
                f"identity contract field(s) missing: {', '.join(missing)}"
            )
        payload = json.dumps(
            [record[field] for field in self.fields],
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        ).encode(self.encoding)
        digest = hashlib.new(self.algorithm)
        digest.update(payload)
        return digest.hexdigest()


@dataclass(frozen=True)
class IdentityPolicy:
    payload: HashContract
    observation: HashContract


@dataclass(frozen=True)
class MarketBar:
    observation_id: str
    producer_payload_hash: str
    symbol: str
    interval: str
    bar_open_time: int
    bar_close_time: int
    open: str
    high: str
    low: str
    close: str
    volume: str
    venue: str
    track: str
    proxy_source: None
    source_producer: str
    observation_type: str
    supersedes_observation_id: None
    ingest_time: int
    venue_seq: int | None
    env_lineage_id: str
    schema_version: str


@dataclass(frozen=True)
class Gap:
    symbol: str
    interval: str
    window_start: int
    window_end: int
    missing_bars: int


@dataclass(frozen=True)
class BackfillPolicy:
    batch_size: int
    inter_request_seconds: float

    def __post_init__(self) -> None:
        if isinstance(self.batch_size, bool) or self.batch_size <= 0:
            raise CollectionRefused("OPEN-N7 batch_size must be greater than zero")
        if (
            isinstance(self.inter_request_seconds, bool)
            or not math.isfinite(self.inter_request_seconds)
            or self.inter_request_seconds < 0
        ):
            raise CollectionRefused("OPEN-N7 inter_request_seconds must be finite and non-negative")


class PublicMarketSource(Protocol):
    def connect(self) -> None: ...

    def candles_snapshot(
        self, symbol: str, interval: str, start_ms: int, end_ms: int
    ) -> Sequence[Mapping[str, object]]: ...

    def subscribe(
        self,
        symbol: str,
        interval: str,
        callback: Callable[[Mapping[str, object]], None],
    ) -> None: ...

    def wait(self) -> None: ...

    def close(self) -> None: ...


def _safe_part(value: str, label: str) -> str:
    if not _SAFE_PART.fullmatch(value):
        raise CollectionRefused(f"unsafe {label}: {value!r}")
    return value


def _month(epoch_ms: int) -> str:
    return datetime.fromtimestamp(epoch_ms / 1000, tz=UTC).strftime("%Y-%m")


def _iso_utc(epoch_ms: int) -> str:
    return datetime.fromtimestamp(epoch_ms / 1000, tz=UTC).isoformat().replace("+00:00", "Z")


def _decimal(name: str, value: object) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise CollectionRefused(f"bar {name} is not numeric")
    try:
        number = Decimal(str(value))
    except InvalidOperation as error:
        raise CollectionRefused(f"bar {name} is not numeric") from error
    if not number.is_finite():
        raise CollectionRefused(f"bar {name} is not finite")
    return number


def normalize_bar(
    raw: Mapping[str, object],
    *,
    source_producer: str,
    ingest_time: int,
    env_lineage_id: str,
    identities: IdentityPolicy,
) -> MarketBar | None:
    required = ("t", "s", "i", "o", "h", "l", "c", "v")
    missing = [field for field in required if field not in raw]
    if missing:
        raise CollectionRefused(f"bar field(s) missing: {', '.join(missing)}")
    symbol = str(raw["s"])
    interval = str(raw["i"])
    if symbol not in INITIAL_SYMBOLS or interval not in INTERVAL_MS:
        raise CollectionRefused(f"bar outside approved initial universe: {symbol} {interval}")
    if isinstance(raw["t"], bool) or not isinstance(raw["t"], int):
        raise CollectionRefused("bar t must be an integer")
    open_time = raw["t"]
    close_time = open_time + INTERVAL_MS[interval]
    if close_time > ingest_time:
        return None

    values = {name: _decimal(name, raw[wire]) for name, wire in (
        ("open", "o"), ("high", "h"), ("low", "l"), ("close", "c"), ("volume", "v")
    )}
    if values["high"] < max(values["open"], values["close"], values["low"]):
        raise CollectionRefused("bar high is inconsistent with OHLC")
    if values["low"] > min(values["open"], values["close"], values["high"]):
        raise CollectionRefused("bar low is inconsistent with OHLC")

    payload_hash = identities.payload.digest(raw)
    observation_fields: dict[str, object] = {
        **raw,
        "venue": "HYPERLIQUID",
        "track": "NATIVE",
        "source_producer": source_producer,
        "producer_payload_hash": payload_hash,
    }
    observation_id = identities.observation.digest(observation_fields)
    venue_seq = raw.get("n")
    if venue_seq is not None and (isinstance(venue_seq, bool) or not isinstance(venue_seq, int)):
        raise CollectionRefused("bar venue sequence must be an integer when present")
    return MarketBar(
        observation_id=observation_id,
        producer_payload_hash=payload_hash,
        symbol=symbol,
        interval=interval,
        bar_open_time=open_time,
        bar_close_time=close_time,
        open=str(raw["o"]),
        high=str(raw["h"]),
        low=str(raw["l"]),
        close=str(raw["c"]),
        volume=str(raw["v"]),
        venue="HYPERLIQUID",
        track="NATIVE",
        proxy_source=None,
        source_producer=source_producer,
        observation_type="INITIAL",
        supersedes_observation_id=None,
        ingest_time=ingest_time,
        venue_seq=venue_seq,
        env_lineage_id=env_lineage_id,
        schema_version="0.1.0",
    )


def detect_gap(previous_open: int, next_open: int, symbol: str, interval: str) -> Gap | None:
    step = INTERVAL_MS.get(interval)
    if step is None:
        raise CollectionRefused(f"unsupported interval: {interval}")
    distance = next_open - previous_open
    if distance <= 0 or distance % step:
        raise CollectionRefused("bar sequence is non-increasing or off interval")
    if distance == step:
        return None
    return Gap(symbol, interval, previous_open + step, next_open, distance // step - 1)


class MonthlyArchive:
    def __init__(self, root: Path) -> None:
        self.root = root

    def bar_path(self, bar: MarketBar) -> Path:
        return (
            self.root
            / "bars"
            / _safe_part(bar.venue, "venue")
            / _safe_part(bar.symbol, "symbol")
            / _safe_part(bar.interval, "interval")
            / f"{_month(bar.bar_open_time)}.jsonl"
        )

    @staticmethod
    def _records(path: Path) -> list[Mapping[str, object]]:
        if not path.exists():
            return []
        records: list[Mapping[str, object]] = []
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                try:
                    value = json.loads(line)
                except json.JSONDecodeError as error:
                    raise CollectionRefused(f"invalid archive JSON at {path}:{line_number}") from error
                if not isinstance(value, Mapping):
                    raise CollectionRefused(f"invalid archive record at {path}:{line_number}")
                records.append(value)
        return records

    @staticmethod
    def _append(path: Path, record: Mapping[str, object]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = (
            json.dumps(record, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
            + "\n"
        ).encode("utf-8")
        descriptor = os.open(path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600)
        try:
            os.write(descriptor, payload)
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    def append_bar(self, bar: MarketBar) -> str:
        path = self.bar_path(bar)
        for existing in self._records(path):
            if existing.get("observation_id") == bar.observation_id:
                if existing.get("producer_payload_hash") == bar.producer_payload_hash:
                    return "IDENTICAL_REPLAY_NOOP"
                raise CollectionRefused("same observation_id has different producer bytes")
            same_producer_slot = all(
                existing.get(field) == getattr(bar, field)
                for field in ("source_producer", "symbol", "interval", "bar_open_time")
            )
            if same_producer_slot:
                raise CollectionRefused(
                    "differing same-producer bar requires an approved correction contract"
                )
        self._append(path, asdict(bar))
        return "APPENDED"

    def bars(self, symbol: str, interval: str) -> list[Mapping[str, object]]:
        directory = self.root / "bars" / "HYPERLIQUID" / symbol / interval
        return [record for path in sorted(directory.glob("*.jsonl")) for record in self._records(path)]


class MarketDataCollector:
    def __init__(
        self,
        *,
        source: PublicMarketSource,
        archive: MonthlyArchive,
        identities: IdentityPolicy,
        env_lineage_id: str,
        backfill: BackfillPolicy,
        clock_ms: Callable[[], int] = lambda: time.time_ns() // 1_000_000,
        gap_detector: Callable[[int, int, str, str], Gap | None] = detect_gap,
    ) -> None:
        if not env_lineage_id:
            raise CollectionRefused("missing env_lineage_id")
        self.source = source
        self.archive = archive
        self.identities = identities
        self.env_lineage_id = env_lineage_id
        self.backfill = backfill
        self.clock_ms = clock_ms
        self.gap_detector = gap_detector
        self._last_live_open: dict[tuple[str, str], int] = {}

    def ingest(self, raw: Mapping[str, object], source_producer: str) -> MarketBar | None:
        now = self.clock_ms()
        bar = normalize_bar(
            raw,
            source_producer=source_producer,
            ingest_time=now,
            env_lineage_id=self.env_lineage_id,
            identities=self.identities,
        )
        if bar is None:
            return None
        if source_producer == "WS_LIVE":
            key = (bar.symbol, bar.interval)
            previous = self._last_live_open.get(key)
            if previous is not None:
                gap = self.gap_detector(previous, bar.bar_open_time, bar.symbol, bar.interval)
                if gap is not None:
                    self._fill_gap(gap)
            self._last_live_open[key] = bar.bar_open_time
        self.archive.append_bar(bar)
        return bar

    def _fill_gap(self, gap: Gap) -> None:
        step = INTERVAL_MS[gap.interval]
        cursor = gap.window_start
        while cursor < gap.window_end:
            page_end = min(
                gap.window_end, cursor + self.backfill.batch_size * step
            )
            rows = self.source.candles_snapshot(
                gap.symbol, gap.interval, cursor, page_end
            )
            if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes)):
                raise CollectionRefused("snapshot response must be a row sequence")
            if not all(isinstance(row, Mapping) for row in rows):
                raise CollectionRefused("snapshot response contains a non-object row")
            eligible = sorted(
                (
                    row
                    for row in rows
                    if cursor <= int(row.get("t", -1)) < page_end
                ),
                key=lambda row: int(row["t"]),
            )
            for row in eligible:
                self.ingest(row, "CANDLE_SNAPSHOT")
            if not eligible:
                raise CollectionRefused(
                    f"snapshot did not fill gap starting at {cursor}"
                )
            next_cursor = int(eligible[-1]["t"]) + step
            if next_cursor <= cursor:
                raise CollectionRefused("snapshot cursor made no progress")
            cursor = next_cursor
            if cursor < gap.window_end and self.backfill.inter_request_seconds:
                time.sleep(self.backfill.inter_request_seconds)
        stored = {int(row["bar_open_time"]) for row in self.archive.bars(gap.symbol, gap.interval)}
        missing = [
            timestamp
            for timestamp in range(gap.window_start, gap.window_end, step)
            if timestamp not in stored
        ]
        if missing:
            raise CollectionRefused(f"snapshot left {len(missing)} bar(s) missing")

    def run(self, symbols: Sequence[str], intervals: Sequence[str]) -> None:
        self.source.connect()
        try:
            for symbol in symbols:
                for interval in intervals:
                    self.source.subscribe(
                        symbol,
                        interval,
                        lambda row, producer="WS_LIVE": self.ingest(row, producer),
                    )
            self.source.wait()
        finally:
            self.source.close()


def _print_gap_report(archive_root: Path, symbol: str, interval: str | None) -> int:
    archive = MonthlyArchive(archive_root)
    intervals = (interval,) if interval else INITIAL_INTERVALS
    gaps = 0
    for selected_interval in intervals:
        records = archive.bars(symbol, selected_interval)
        for previous, next_record in zip(records, records[1:]):
            gap = detect_gap(
                int(previous["bar_open_time"]),
                int(next_record["bar_open_time"]),
                symbol,
                selected_interval,
            )
            if gap is None:
                continue
            print(
                f"GAP symbol={gap.symbol} interval={gap.interval} "
                f"first_missing={_iso_utc(gap.window_start)} "
                f"last_missing={_iso_utc(gap.window_end - INTERVAL_MS[selected_interval])}"
            )
            gaps += 1
    print(f"GAPS: {gaps}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Offline market-bar collector core")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run", help="refused until a future owner-ratified runtime step")
    run_parser.add_argument("--permission-packet", required=True, type=Path)
    run_parser.add_argument("--owner-approved-start-decision", required=True, type=int)
    report_parser = subparsers.add_parser("gap-report", help="report archive gaps without venue contact")
    report_parser.add_argument("--archive", required=True, type=Path)
    report_parser.add_argument("--symbol", choices=INITIAL_SYMBOLS, default="BTC")
    report_parser.add_argument("--interval", choices=INITIAL_INTERVALS)
    args = parser.parse_args(argv)
    if args.command == "gap-report":
        return _print_gap_report(args.archive, args.symbol, args.interval)
    parser.exit(
        2,
        "REFUSED: Decision 187 authorizes building only; collector runtime requires "
        "a future owner-ratified permission protocol and backend\n",
    )


if __name__ == "__main__":
    raise SystemExit(main())
