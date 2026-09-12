"""One local-only check for monthly archives, gap repair, and start refusal.

D026 sensitivity: in-memory mutants restore the removed aa602e9c hunks (packet interpretation,
durable GAP writer, concrete SDK backend; the permission validator is restored only up to the seam)
into a copy of the fixed module text, plus text-only token, interval-step, lifecycle, refusal-text,
and forming-bar deviants. Each mutant must fail on exactly the assertion it was built to break.
Changed carried fences include old-vs-new discriminating-power proofs. No mutant touches disk.
"""

from __future__ import annotations

import ast
import dataclasses
import hashlib
import json
import socket
import sys
import tempfile
import types
from contextlib import ExitStack, redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from types import SimpleNamespace
from typing import Callable
from unittest.mock import patch

import market_data_collector as subject


EXPECTED_INTERVAL_MS = {
    "15m": 15 * 60 * 1000,
    "4h": 4 * 60 * 60 * 1000,
    "1h": 60 * 60 * 1000,
    "1d": 24 * 60 * 60 * 1000,
}
EXPECTED_INTERVALS = ("15m", "1h", "4h", "1d")
STEP = EXPECTED_INTERVAL_MS["15m"]
assert subject.INTERVAL_MS == EXPECTED_INTERVAL_MS
assert subject.INITIAL_INTERVALS == EXPECTED_INTERVALS
FEBRUARY_START = 1769904000000  # Fixture-only: 2026-02-01 00:00 UTC.
JANUARY_LAST_BAR = 1769903100000  # Fixture-only: 2026-01-31 23:45 UTC.
PERSISTED_ORDER_BASE = FEBRUARY_START + 2 * STEP  # Keep physical order fixtures in one file.
EXPECTED_OPEN_QUESTIONS = {
    "OPEN-F3",
    "OPEN-F4",
    "OPEN-N2",
    "OPEN-N3",
    "OPEN-N4",
    "OPEN-N5",
    "OPEN-N6",
    "OPEN-N7",
    "OPEN-N8",
    "OPEN-N10",
    "OPEN-N11",
    "OPEN-N12",
    "OPEN-N13",
    "OPEN-N14",
    "OPEN-N17",
    "OPEN-N18",
    "OPEN-N19",
}
REFUSAL_SUFFIX = "future owner-ratified permission protocol and backend"
REFUSAL_TEXT = (
    "REFUSED: Decision 187 authorizes building only; collector runtime requires a "
    f"{REFUSAL_SUFFIX}\n"
)


def contract(*fields: str) -> subject.HashContract:
    # Fixture values exercise the configurable contract; they are not runtime defaults.
    return subject.HashContract(tuple(fields), "sha256", "utf-8", "json-array-compact")


def identities_for(module: types.ModuleType):
    """Build the fixture identity policy for the given module (fixed or mutant)."""
    hash_contract = module.HashContract

    def make(*fields: str):
        return hash_contract(tuple(fields), "sha256", "utf-8", "json-array-compact")

    kwargs = {
        "payload": make("t", "s", "i", "o", "h", "l", "c", "v"),
        "observation": make(
            "t", "s", "i", "venue", "track", "source_producer", "producer_payload_hash"
        ),
    }
    if "event" in {field.name for field in dataclasses.fields(module.IdentityPolicy)}:
        # Only the durable-GAP-writer mutant carries the removed event contract.
        kwargs["event"] = make(
            "record_type", "venue", "symbol", "interval", "window_start", "window_end", "detected_at"
        )
    return module.IdentityPolicy(**kwargs)


IDENTITIES = identities_for(subject)


def raw_bar(open_time: int, interval: str = "15m") -> dict[str, object]:
    step = EXPECTED_INTERVAL_MS[interval]
    offset = (open_time - (FEBRUARY_START - step)) // step
    price = 100 + offset
    return {
        "t": open_time,
        "T": open_time + step,
        "s": "BTC",
        "i": interval,
        "o": str(price),
        "h": str(price + 2),
        "l": str(price - 1),
        "c": str(price + 1),
        "v": str(10 + offset),
    }


class FakePublicSource:
    def __init__(
        self,
        snapshot_rows: list[dict[str, object]],
        *,
        lifecycle: bool = False,
        wait_error: Exception | None = None,
    ) -> None:
        self.snapshot_rows = snapshot_rows
        self.snapshot_calls: list[tuple[str, str, int, int]] = []
        self.lifecycle = lifecycle
        self.wait_error = wait_error
        self.calls: list[str] = []
        self.subscriptions: list[tuple[str, str]] = []

    def connect(self) -> None:
        if not self.lifecycle:
            raise AssertionError("the local check must never connect")
        self.calls.append("connect")

    def candles_snapshot(self, symbol: str, interval: str, start_ms: int, end_ms: int):
        self.snapshot_calls.append((symbol, interval, start_ms, end_ms))
        return [row for row in self.snapshot_rows if start_ms <= int(row["t"]) < end_ms]

    def subscribe(self, symbol, interval, callback) -> None:
        if not self.lifecycle:
            raise AssertionError("the local check must never subscribe")
        self.calls.append("subscribe")
        self.subscriptions.append((symbol, interval))

    def wait(self) -> None:
        if not self.lifecycle:
            raise AssertionError("the local check must never wait on a socket")
        self.calls.append("wait")
        if self.wait_error is not None:
            raise self.wait_error

    def close(self) -> None:
        if not self.lifecycle:
            raise AssertionError("the local check must never close a socket")
        self.calls.append("close")


def durable_files(root: Path) -> list[tuple[str, int]]:
    return sorted((path.relative_to(root).as_posix(), path.stat().st_size) for path in root.rglob("*") if path.is_file())


def archive_check(gap_detector=None, module: types.ModuleType = subject) -> None:
    detector = module.detect_gap if gap_detector is None else gap_detector
    missing = [raw_bar(JANUARY_LAST_BAR + STEP), raw_bar(JANUARY_LAST_BAR + 2 * STEP)]
    missing_before = [dict(row) for row in missing]
    source = FakePublicSource(missing)
    now = JANUARY_LAST_BAR + 5 * STEP
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        archive = module.MonthlyArchive(root)
        collector = module.MarketDataCollector(
            source=source,
            archive=archive,
            identities=identities_for(module),
            env_lineage_id="fixture-lineage",
            backfill=module.BackfillPolicy(batch_size=2, inter_request_seconds=0),
            clock_ms=lambda: now,
            gap_detector=detector,
        )
        first = collector.ingest(raw_bar(JANUARY_LAST_BAR), "WS_LIVE")
        collector.ingest(raw_bar(JANUARY_LAST_BAR + 3 * STEP), "WS_LIVE")

        bars = archive.bars("BTC", "15m")
        recovered = [int(bar["bar_open_time"]) for bar in bars]
        assert recovered == [
            JANUARY_LAST_BAR,
            JANUARY_LAST_BAR + STEP,
            JANUARY_LAST_BAR + 2 * STEP,
            JANUARY_LAST_BAR + 3 * STEP,
        ], ("recovered_bar_open_times", recovered)
        assert {bar["venue"] for bar in bars} == {"HYPERLIQUID"}
        assert {bar["track"] for bar in bars} == {"NATIVE"}
        assert {bar["source_producer"] for bar in bars} == {"WS_LIVE", "CANDLE_SNAPSHOT"}
        assert (root / "bars" / "HYPERLIQUID" / "BTC" / "15m" / "2026-01.jsonl").is_file()
        assert (root / "bars" / "HYPERLIQUID" / "BTC" / "15m" / "2026-02.jsonl").is_file()
        # The only durable output family is bars/: nothing else may exist under the root.
        durable_families = sorted(child.name for child in root.iterdir())
        assert durable_families == ["bars"], ("durable_output_families", durable_families)
        assert missing == missing_before
        assert first is not None
        assert archive.append_bar(first) == "IDENTICAL_REPLAY_NOOP"
        # Same-slot conflict controls (both production refusal paths), nothing appended either way.
        same_id_different_bytes = dataclasses.replace(first, close=str(int(first.close) + 1), producer_payload_hash="0" * 64)
        different_id_same_slot = dataclasses.replace(same_id_different_bytes, observation_id="1" * 64)
        for conflicting, expected in (
            (same_id_different_bytes, "same observation_id has different producer bytes"),
            (different_id_same_slot, "differing same-producer bar requires an approved correction contract"),
        ):
            try:
                archive.append_bar(conflicting)
            except module.CollectionRefused as error:
                assert str(error) == expected, str(error)
            else:
                raise AssertionError(f"conflicting same-slot bar was appended: {expected}")
        assert [int(bar["bar_open_time"]) for bar in archive.bars("BTC", "15m")] == [
            JANUARY_LAST_BAR, JANUARY_LAST_BAR + STEP, JANUARY_LAST_BAR + 2 * STEP, JANUARY_LAST_BAR + 3 * STEP
        ]
        # Forming bar through the approved ingest seam: an interval-aligned bar that closes after
        # `now` must be neither normalized nor written anywhere under the archive root.
        durable_before = durable_files(root)
        forming = raw_bar(JANUARY_LAST_BAR + 5 * STEP)
        assert collector.ingest(forming, "WS_LIVE") is None
        durable_after = durable_files(root)
        assert durable_after == durable_before, ("durable_files_changed", durable_before, durable_after)
        assert source.snapshot_calls == [
            ("BTC", "15m", JANUARY_LAST_BAR + STEP, JANUARY_LAST_BAR + 3 * STEP)
        ]


def replay_and_gap_atomicity_check(module: types.ModuleType = subject) -> None:
    """Fixture-only ingest replay and failed-gap state transition checks."""
    clock = [JANUARY_LAST_BAR + 10 * STEP]
    with tempfile.TemporaryDirectory() as temporary:
        archive = module.MonthlyArchive(Path(temporary))
        source = FakePublicSource([])
        collector = module.MarketDataCollector(
            source=source,
            archive=archive,
            identities=identities_for(module),
            env_lineage_id="fixture-lineage",
            backfill=module.BackfillPolicy(batch_size=2, inter_request_seconds=0),
            clock_ms=lambda: clock[0],
        )
        first = collector.ingest(raw_bar(JANUARY_LAST_BAR), "WS_LIVE")
        assert first is not None
        stored_path = archive.bar_path(first)
        stored_before = stored_path.read_bytes()
        clock[0] += STEP
        replay = collector.ingest(raw_bar(JANUARY_LAST_BAR), "WS_LIVE")
        assert replay is not None and replay.ingest_time == clock[0]
        assert stored_path.read_bytes() == stored_before
        assert [int(bar["bar_open_time"]) for bar in archive.bars("BTC", "15m")] == [
            JANUARY_LAST_BAR
        ]

        conflict = raw_bar(JANUARY_LAST_BAR)
        conflict["c"] = str(int(conflict["c"]) + 1)
        try:
            collector.ingest(conflict, "WS_LIVE")
        except module.CollectionRefused as error:
            assert str(error) == (
                "differing same-producer bar requires an approved correction contract"
            )
        else:
            raise AssertionError("conflicting ingest replay was accepted")

        collector.ingest(raw_bar(JANUARY_LAST_BAR + STEP), "WS_LIVE")
        older_replay = collector.ingest(raw_bar(JANUARY_LAST_BAR), "WS_LIVE")
        assert older_replay is not None and older_replay.observation_id == first.observation_id
        collector.ingest(raw_bar(JANUARY_LAST_BAR + 2 * STEP), "WS_LIVE")
        assert source.snapshot_calls == [], ("older_replay_rewound_cursor", source.snapshot_calls)

    with tempfile.TemporaryDirectory() as temporary:
        archive = module.MonthlyArchive(Path(temporary))
        source = FakePublicSource([])
        collector = module.MarketDataCollector(
            source=source,
            archive=archive,
            identities=identities_for(module),
            env_lineage_id="fixture-lineage",
            backfill=module.BackfillPolicy(batch_size=2, inter_request_seconds=0),
            clock_ms=lambda: clock[0],
        )
        collector.ingest(raw_bar(JANUARY_LAST_BAR), "WS_LIVE")
        try:
            collector.ingest(raw_bar(JANUARY_LAST_BAR + 3 * STEP), "WS_LIVE")
        except module.CollectionRefused as error:
            assert str(error) == f"snapshot did not fill gap starting at {JANUARY_LAST_BAR + STEP}"
        else:
            raise AssertionError("empty gap snapshot was accepted")
        failed_rows = [
            int(bar["bar_open_time"]) for bar in archive.bars("BTC", "15m")
        ]
        assert failed_rows == [JANUARY_LAST_BAR], ("failed_gap_rows", failed_rows)

        collector.ingest(raw_bar(JANUARY_LAST_BAR + STEP), "WS_LIVE")
        assert [int(bar["bar_open_time"]) for bar in archive.bars("BTC", "15m")] == [
            JANUARY_LAST_BAR,
            JANUARY_LAST_BAR + STEP,
        ]
    print("INGEST REPLAY/GAP ATOMICITY (fixture transport): PASS")


def restart_replay_seeds_live_cursor_check(module: types.ModuleType = subject) -> None:
    """A restart whose first live frame is an identical replay must still hold the live cursor."""
    now = JANUARY_LAST_BAR + 10 * STEP

    def build(archive, source):
        return module.MarketDataCollector(
            source=source,
            archive=archive,
            identities=identities_for(module),
            env_lineage_id="fixture-lineage",
            backfill=module.BackfillPolicy(batch_size=2, inter_request_seconds=0),
            clock_ms=lambda: now,
        )

    with tempfile.TemporaryDirectory() as temporary:
        archive = module.MonthlyArchive(Path(temporary))
        source = FakePublicSource([])
        assert build(archive, source).ingest(raw_bar(JANUARY_LAST_BAR), "WS_LIVE") is not None
        # Fresh collector over the same archive: its first live frame replays the stored last bar,
        # so the two-bar hole before the next live bar must still be detected and refused.
        restarted = build(archive, source)
        replay = restarted.ingest(raw_bar(JANUARY_LAST_BAR), "WS_LIVE")
        assert replay is not None and replay.bar_open_time == JANUARY_LAST_BAR
        try:
            restarted.ingest(raw_bar(JANUARY_LAST_BAR + 3 * STEP), "WS_LIVE")
            refusal = None
        except module.CollectionRefused as error:
            refusal = str(error)
        stored = [int(bar["bar_open_time"]) for bar in archive.bars("BTC", "15m")]
        observed = (refusal, stored, len(source.snapshot_calls))
        assert observed == (
            f"snapshot did not fill gap starting at {JANUARY_LAST_BAR + STEP}",
            [JANUARY_LAST_BAR],
            1,
        ), ("restart_replay_cursor", observed)

    # Seeding must never rewind: an older identical replay after newer live bars leaves the cursor
    # at the newest bar, so the next contiguous live bar still needs no snapshot.
    with tempfile.TemporaryDirectory() as temporary:
        archive = module.MonthlyArchive(Path(temporary))
        source = FakePublicSource([])
        collector = build(archive, source)
        collector.ingest(raw_bar(JANUARY_LAST_BAR), "WS_LIVE")
        collector.ingest(raw_bar(JANUARY_LAST_BAR + STEP), "WS_LIVE")
        collector.ingest(raw_bar(JANUARY_LAST_BAR), "WS_LIVE")
        collector.ingest(raw_bar(JANUARY_LAST_BAR + 2 * STEP), "WS_LIVE")
        assert source.snapshot_calls == [], (
            "older_replay_rewound_seeded_cursor", source.snapshot_calls
        )
        assert [int(bar["bar_open_time"]) for bar in archive.bars("BTC", "15m")] == [
            JANUARY_LAST_BAR,
            JANUARY_LAST_BAR + STEP,
            JANUARY_LAST_BAR + 2 * STEP,
        ]
    print("RESTART REPLAY SEEDS LIVE CURSOR: PASS")


def restart_persisted_latest_cursor_check(module: types.ModuleType = subject) -> None:
    """A fresh collector must use the newest persisted live bar, not the first frame it sees."""
    now = JANUARY_LAST_BAR + 10 * STEP

    def build(archive, source):
        return module.MarketDataCollector(
            source=source,
            archive=archive,
            identities=identities_for(module),
            env_lineage_id="fixture-lineage",
            backfill=module.BackfillPolicy(batch_size=2, inter_request_seconds=0),
            clock_ms=lambda: now,
        )

    with tempfile.TemporaryDirectory() as temporary:
        archive = module.MonthlyArchive(Path(temporary))
        seed = build(archive, FakePublicSource([]))
        for offset in (0, 1, 2):
            assert seed.ingest(raw_bar(JANUARY_LAST_BAR + offset * STEP), "WS_LIVE") is not None

        source = FakePublicSource([])
        restarted = build(archive, source)
        try:
            restarted.ingest(raw_bar(JANUARY_LAST_BAR + 5 * STEP), "WS_LIVE")
            refusal = None
        except module.CollectionRefused as error:
            refusal = str(error)
        observed = (
            refusal,
            [int(bar["bar_open_time"]) for bar in archive.bars("BTC", "15m")],
            len(source.snapshot_calls),
        )
        assert observed == (
            f"snapshot did not fill gap starting at {JANUARY_LAST_BAR + 3 * STEP}",
            [JANUARY_LAST_BAR, JANUARY_LAST_BAR + STEP, JANUARY_LAST_BAR + 2 * STEP],
            1,
        ), ("restart_persisted_latest_gap", observed)

    with tempfile.TemporaryDirectory() as temporary:
        archive = module.MonthlyArchive(Path(temporary))
        seed = build(archive, FakePublicSource([]))
        for offset in (0, 1, 2):
            assert seed.ingest(raw_bar(JANUARY_LAST_BAR + offset * STEP), "WS_LIVE") is not None

        source = FakePublicSource([])
        restarted = build(archive, source)
        assert restarted.ingest(raw_bar(JANUARY_LAST_BAR), "WS_LIVE") is not None
        assert restarted.ingest(raw_bar(JANUARY_LAST_BAR + 3 * STEP), "WS_LIVE") is not None
        observed = (
            [int(bar["bar_open_time"]) for bar in archive.bars("BTC", "15m")],
            len(source.snapshot_calls),
        )
        assert observed == (
            [
                JANUARY_LAST_BAR,
                JANUARY_LAST_BAR + STEP,
                JANUARY_LAST_BAR + 2 * STEP,
                JANUARY_LAST_BAR + 3 * STEP,
            ],
            0,
        ), ("restart_persisted_latest_replay", observed)
    print("RESTART PERSISTED LATEST CURSOR: PASS")


def restart_persisted_gap_refusal_check(module: types.ModuleType = subject) -> None:
    """A persisted WS_LIVE hole must be refused, even when a snapshot row fills one timestamp."""
    now = JANUARY_LAST_BAR + 10 * STEP

    with tempfile.TemporaryDirectory() as temporary:
        archive = module.MonthlyArchive(Path(temporary))
        for offset, producer in ((0, "WS_LIVE"), (1, "CANDLE_SNAPSHOT"), (5, "WS_LIVE")):
            bar = module.normalize_bar(
                raw_bar(JANUARY_LAST_BAR + offset * STEP),
                source_producer=producer,
                ingest_time=now,
                env_lineage_id="fixture-lineage",
                identities=identities_for(module),
            )
            assert bar is not None
            assert archive.append_bar(bar) == "APPENDED"

        source = FakePublicSource([])
        restarted = module.MarketDataCollector(
            source=source,
            archive=archive,
            identities=identities_for(module),
            env_lineage_id="fixture-lineage",
            backfill=module.BackfillPolicy(batch_size=2, inter_request_seconds=0),
            clock_ms=lambda: now,
        )
        try:
            restarted.ingest(raw_bar(JANUARY_LAST_BAR + 6 * STEP), "WS_LIVE")
            refusal = None
        except module.CollectionRefused as error:
            refusal = str(error)
        observed = (
            refusal,
            [int(bar["bar_open_time"]) for bar in archive.bars("BTC", "15m")],
            len(source.snapshot_calls),
        )
        assert observed == (
            "persisted WS_LIVE sequence has a gap at 2026-02-01T00:00:00Z",
            [JANUARY_LAST_BAR, JANUARY_LAST_BAR + STEP, JANUARY_LAST_BAR + 5 * STEP],
            0,
        ), ("restart_persisted_gap", observed)
    print("RESTART PERSISTED GAP REFUSED: PASS")


def restart_persisted_order_refusal_check(module: types.ModuleType = subject) -> None:
    """Persisted reverse and duplicate order must be refused without side effects."""
    now = JANUARY_LAST_BAR + 10 * STEP

    for label, offsets in (
        ("persisted_reverse_order", (0, 1, 0)),
        ("persisted_duplicate_order", (0, 1, 1)),
    ):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = module.MonthlyArchive(root)
            for offset in offsets:
                bar = module.normalize_bar(
                    raw_bar(PERSISTED_ORDER_BASE + offset * STEP),
                    source_producer="WS_LIVE",
                    ingest_time=now,
                    env_lineage_id="fixture-lineage",
                    identities=identities_for(module),
                )
                assert bar is not None
                archive._append(archive.bar_path(bar), dataclasses.asdict(bar))

            source = FakePublicSource([])
            before = durable_bytes(root)
            restarted = module.MarketDataCollector(
                source=source,
                archive=archive,
                identities=identities_for(module),
                env_lineage_id="fixture-lineage",
                backfill=module.BackfillPolicy(batch_size=2, inter_request_seconds=0),
                clock_ms=lambda: now,
            )
            try:
                restarted.ingest(raw_bar(PERSISTED_ORDER_BASE + 3 * STEP), "WS_LIVE")
            except module.CollectionRefused:
                pass
            else:
                raise AssertionError((label, "accepted"))
            assert durable_bytes(root) == before, (label, "archive_changed")
            assert source.snapshot_calls == [], (label, "snapshot_called")
    print("RESTART PERSISTED ORDER (reverse 0,1,0 + duplicate 0,1,1) REFUSED: PASS")


def restart_persisted_sorting_counterexample_check(module: types.ModuleType = subject) -> None:
    """The sorting mutant must still be distinguishable on a non-monotonic 0,2,1 history."""
    now = JANUARY_LAST_BAR + 10 * STEP
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        archive = module.MonthlyArchive(root)
        for offset in (0, 2, 1):
            bar = module.normalize_bar(
                raw_bar(PERSISTED_ORDER_BASE + offset * STEP),
                source_producer="WS_LIVE",
                ingest_time=now,
                env_lineage_id="fixture-lineage",
                identities=identities_for(module),
            )
            assert bar is not None
            archive._append(archive.bar_path(bar), dataclasses.asdict(bar))
        source = FakePublicSource([])
        restarted = module.MarketDataCollector(
            source=source,
            archive=archive,
            identities=identities_for(module),
            env_lineage_id="fixture-lineage",
            backfill=module.BackfillPolicy(batch_size=2, inter_request_seconds=0),
            clock_ms=lambda: now,
        )
        try:
            restarted.ingest(raw_bar(PERSISTED_ORDER_BASE + 3 * STEP), "WS_LIVE")
        except module.CollectionRefused:
            pass
        else:
            raise AssertionError(("persisted_sorted_order", "accepted"))
    print("RESTART PERSISTED SORTING COUNTEREXAMPLE REFUSED: PASS")


def persisted_interval_identity_refusal_check(module: types.ModuleType = subject) -> None:
    """Selected archives must reject WS_LIVE records whose persisted interval disagrees."""
    now = JANUARY_LAST_BAR + 10 * STEP
    for label, persisted_interval in (("mismatching", "1h"), ("unsupported", "5m")):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = module.MonthlyArchive(root)
            valid = module.normalize_bar(
                raw_bar(JANUARY_LAST_BAR),
                source_producer="WS_LIVE",
                ingest_time=now,
                env_lineage_id="fixture-lineage",
                identities=identities_for(module),
            )
            assert valid is not None
            record = dataclasses.asdict(valid)
            record["interval"] = persisted_interval
            archive._append(archive.bar_path(valid), record)
            before = durable_bytes(root)
            source = FakePublicSource([])
            restarted = module.MarketDataCollector(
                source=source,
                archive=archive,
                identities=identities_for(module),
                env_lineage_id="fixture-lineage",
                backfill=module.BackfillPolicy(batch_size=2, inter_request_seconds=0),
                clock_ms=lambda: now,
            )
            try:
                restarted.ingest(raw_bar(JANUARY_LAST_BAR + STEP), "WS_LIVE")
            except module.CollectionRefused:
                pass
            else:
                raise AssertionError(("persisted_interval", label, "accepted"))
            assert durable_bytes(root) == before, ("persisted_interval", label, "archive_changed")
            assert source.snapshot_calls == [], ("persisted_interval", label, "snapshot_called")
    print("PERSISTED WS_LIVE INTERVAL IDENTITY (mismatching/unsupported) REFUSED: PASS")


def forming_first_frame_reconstructs_history_check(module: types.ModuleType = subject) -> None:
    """A first forming frame validates persisted history but remains non-durable."""
    now = JANUARY_LAST_BAR + 10 * STEP
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        archive = module.MonthlyArchive(root)
        for offset in (0, 1):
            bar = module.normalize_bar(
                raw_bar(JANUARY_LAST_BAR + offset * STEP),
                source_producer="WS_LIVE",
                ingest_time=now,
                env_lineage_id="fixture-lineage",
                identities=identities_for(module),
            )
            assert bar is not None
            archive._append(archive.bar_path(bar), dataclasses.asdict(bar))
        detector_calls: list[tuple[int, int, str, str]] = []

        def detector(previous, next_open, symbol, interval):
            detector_calls.append((previous, next_open, symbol, interval))
            return None

        source = FakePublicSource([])
        collector = module.MarketDataCollector(
            source=source,
            archive=archive,
            identities=identities_for(module),
            env_lineage_id="fixture-lineage",
            backfill=module.BackfillPolicy(batch_size=2, inter_request_seconds=0),
            clock_ms=lambda: now,
            gap_detector=detector,
        )
        before = durable_bytes(root)
        assert collector.ingest(raw_bar(now), "WS_LIVE") is None
        assert detector_calls == [
            (JANUARY_LAST_BAR, JANUARY_LAST_BAR + STEP, "BTC", "15m")
        ], ("forming_history", detector_calls)
        assert durable_bytes(root) == before, ("forming_first_frame", "archive_changed")
        assert source.snapshot_calls == [], ("forming_first_frame", "snapshot_called")

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        archive = module.MonthlyArchive(root)
        for offset in (0, 2):
            bar = module.normalize_bar(
                raw_bar(JANUARY_LAST_BAR + offset * STEP),
                source_producer="WS_LIVE",
                ingest_time=now,
                env_lineage_id="fixture-lineage",
                identities=identities_for(module),
            )
            assert bar is not None
            archive._append(archive.bar_path(bar), dataclasses.asdict(bar))
        source = FakePublicSource([])
        collector = module.MarketDataCollector(
            source=source,
            archive=archive,
            identities=identities_for(module),
            env_lineage_id="fixture-lineage",
            backfill=module.BackfillPolicy(batch_size=2, inter_request_seconds=0),
            clock_ms=lambda: now,
        )
        before = durable_bytes(root)
        try:
            collector.ingest(raw_bar(now), "WS_LIVE")
        except module.CollectionRefused:
            pass
        else:
            raise AssertionError(("forming_persisted_gap", "accepted"))
        assert durable_bytes(root) == before, ("forming_persisted_gap", "archive_changed")
        assert source.snapshot_calls == [], ("forming_persisted_gap", "snapshot_called")
    print("FIRST FORMING FRAME RECONSTRUCTS/VALIDATES HISTORY WITHOUT WRITE: PASS")


def persisted_huge_timestamp_gap_refusal_check(module: types.ModuleType = subject) -> None:
    """Huge exact persisted timestamps must not leak diagnostic conversion errors."""
    now = JANUARY_LAST_BAR + 10 * STEP
    huge = (10**1000 // STEP) * STEP
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        archive = module.MonthlyArchive(root)
        for offset, persisted_open in ((0, huge), (2, huge + 2 * STEP)):
            bar = module.normalize_bar(
                raw_bar(JANUARY_LAST_BAR + offset * STEP),
                source_producer="WS_LIVE",
                ingest_time=now,
                env_lineage_id="fixture-lineage",
                identities=identities_for(module),
            )
            assert bar is not None
            record = dataclasses.asdict(bar)
            record["bar_open_time"] = persisted_open
            archive._append(archive.bar_path(bar), record)
        source = FakePublicSource([])
        restarted = module.MarketDataCollector(
            source=source,
            archive=archive,
            identities=identities_for(module),
            env_lineage_id="fixture-lineage",
            backfill=module.BackfillPolicy(batch_size=2, inter_request_seconds=0),
            clock_ms=lambda: now,
        )
        before = durable_bytes(root)
        try:
            restarted.ingest(raw_bar(JANUARY_LAST_BAR + 3 * STEP), "WS_LIVE")
        except module.CollectionRefused:
            pass
        except BaseException as error:
            raise AssertionError(("persisted_huge_timestamp", type(error).__name__)) from error
        else:
            raise AssertionError(("persisted_huge_timestamp", "accepted"))
        assert durable_bytes(root) == before, ("persisted_huge_timestamp", "archive_changed")
        assert source.snapshot_calls == [], ("persisted_huge_timestamp", "snapshot_called")
    print("PERSISTED HUGE TIMESTAMP GAP DIAGNOSTIC FAILS CLOSED: PASS")


def persisted_huge_timestamp_public_ingest_check(module: types.ModuleType = subject) -> None:
    """Every enormous persisted WS_LIVE timestamp must fail before cursor reconstruction."""
    now = JANUARY_LAST_BAR + 10 * STEP
    huge = (10**1000 // STEP) * STEP
    for label, persisted_opens in (("single", (huge,)), ("contiguous", (huge, huge + STEP))):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = module.MonthlyArchive(root)
            for persisted_open in persisted_opens:
                bar = module.normalize_bar(
                    raw_bar(JANUARY_LAST_BAR),
                    source_producer="WS_LIVE",
                    ingest_time=now,
                    env_lineage_id="fixture-lineage",
                    identities=identities_for(module),
                )
                assert bar is not None
                record = dataclasses.asdict(bar)
                record["bar_open_time"] = persisted_open
                archive._append(archive.bar_path(bar), record)
            source = FakePublicSource([])
            restarted = module.MarketDataCollector(
                source=source,
                archive=archive,
                identities=identities_for(module),
                env_lineage_id="fixture-lineage",
                backfill=module.BackfillPolicy(batch_size=2, inter_request_seconds=0),
                clock_ms=lambda: now,
            )
            before = durable_bytes(root)
            try:
                restarted.ingest(raw_bar(JANUARY_LAST_BAR + STEP), "WS_LIVE")
            except module.CollectionRefused as error:
                assert str(error) == "persisted WS_LIVE bar_open_time is not UTC-renderable", (
                    label,
                    str(error),
                )
            except BaseException as error:
                raise AssertionError(("persisted_huge_timestamp_public", label, type(error).__name__)) from error
            else:
                raise AssertionError(("persisted_huge_timestamp_public", label, "accepted"))
            assert durable_bytes(root) == before, (label, "archive_changed")
            assert source.snapshot_calls == [], (label, "snapshot_called")
    print("PERSISTED HUGE TIMESTAMP PUBLIC INGEST (single/contiguous) REFUSED: PASS")


def durable_bytes(root: Path) -> list[tuple[str, bytes]]:
    return sorted(
        (path.relative_to(root).as_posix(), path.read_bytes())
        for path in root.rglob("*")
        if path.is_file()
    )


def persisted_timestamp_case_check(
    label: str, persisted_value: object, *, missing: bool = False, module: types.ModuleType = subject
) -> None:
    now = JANUARY_LAST_BAR + 10 * STEP
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        archive = module.MonthlyArchive(root)
        valid = module.normalize_bar(
            raw_bar(JANUARY_LAST_BAR),
            source_producer="WS_LIVE",
            ingest_time=now,
            env_lineage_id="fixture-lineage",
            identities=identities_for(module),
        )
        assert valid is not None
        record = dataclasses.asdict(valid)
        if missing:
            record.pop("bar_open_time")
        else:
            record["bar_open_time"] = persisted_value
        archive._append(archive.bar_path(valid), record)
        before = durable_bytes(root)
        source = FakePublicSource([])
        restarted = module.MarketDataCollector(
            source=source,
            archive=archive,
            identities=identities_for(module),
            env_lineage_id="fixture-lineage",
            backfill=module.BackfillPolicy(batch_size=2, inter_request_seconds=0),
            clock_ms=lambda: now,
        )
        try:
            restarted.ingest(raw_bar(JANUARY_LAST_BAR + STEP), "WS_LIVE")
        except module.CollectionRefused:
            outcome = "refused"
        except BaseException as error:
            outcome = type(error).__name__
        else:
            outcome = "accepted"
        changed = durable_bytes(root) != before
        snapshots = len(source.snapshot_calls)
        assert (outcome, changed, snapshots) == ("refused", False, 0), (
            "persisted_timestamp",
            label,
            outcome,
            changed,
            snapshots,
        )


def persisted_timestamp_type_refusal_check(module: types.ModuleType = subject) -> None:
    cases = (
        ("numeric string", str(JANUARY_LAST_BAR), False),
        ("fractional float", JANUARY_LAST_BAR + 0.5, False),
        ("bool", True, False),
        ("null", None, False),
        ("missing", None, True),
    )
    failures: list[object] = []
    for label, value, missing in cases:
        try:
            persisted_timestamp_case_check(label, value, missing=missing, module=module)
        except AssertionError as error:
            failures.append(error.args[0] if error.args else None)
    assert failures == [], ("persisted_timestamp_fences", failures)
    print("PERSISTED TIMESTAMP TYPE FENCES (string/float/bool/null/missing): PASS")


def persisted_off_grid_refusal_check(module: types.ModuleType = subject) -> None:
    """Consistently shifted integer live opens must still fail absolute-grid validation."""
    now = JANUARY_LAST_BAR + 10 * STEP
    shifted = (JANUARY_LAST_BAR + 1, JANUARY_LAST_BAR + STEP + 1)

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        archive = module.MonthlyArchive(root)
        for open_time in shifted:
            bar = module.normalize_bar(
                raw_bar(open_time),
                source_producer="WS_LIVE",
                ingest_time=now,
                env_lineage_id="fixture-lineage",
                identities=identities_for(module),
            )
            assert bar is not None
            assert archive.append_bar(bar) == "APPENDED"

        source = FakePublicSource([])
        before = durable_bytes(root)
        restarted = module.MarketDataCollector(
            source=source,
            archive=archive,
            identities=identities_for(module),
            env_lineage_id="fixture-lineage",
            backfill=module.BackfillPolicy(batch_size=2, inter_request_seconds=0),
            clock_ms=lambda: now,
        )
        try:
            restarted.ingest(raw_bar(JANUARY_LAST_BAR + 2 * STEP + 1), "WS_LIVE")
        except module.CollectionRefused:
            pass
        else:
            raise AssertionError(("persisted_off_grid", "accepted"))
        assert durable_bytes(root) == before, ("persisted_off_grid", "archive_changed")
        assert source.snapshot_calls == [], ("persisted_off_grid", "snapshot_called")
    print("PERSISTED INTEGER OFF-GRID OPENS REFUSED: PASS")


def synthetic_same_id_conflict_check(module: types.ModuleType = subject) -> None:
    """A fixture-only observation contract forces changed producer bytes onto one ID."""
    identities = module.IdentityPolicy(
        payload=module.HashContract(
            ("t", "s", "i", "o", "h", "l", "c", "v"),
            "sha256",
            "utf-8",
            "json-array-compact",
        ),
        observation=module.HashContract(
            ("t", "s", "i", "venue", "track", "source_producer"),
            "sha256",
            "utf-8",
            "json-array-compact",
        ),
    )
    now = JANUARY_LAST_BAR + 10 * STEP
    changed = raw_bar(JANUARY_LAST_BAR)
    changed["c"] = str(int(changed["c"]) + 1)
    first_bar = module.normalize_bar(
        raw_bar(JANUARY_LAST_BAR),
        source_producer="WS_LIVE",
        ingest_time=now,
        env_lineage_id="fixture-lineage",
        identities=identities,
    )
    changed_bar = module.normalize_bar(
        changed,
        source_producer="WS_LIVE",
        ingest_time=now,
        env_lineage_id="fixture-lineage",
        identities=identities,
    )
    assert first_bar is not None and changed_bar is not None
    assert first_bar.observation_id == changed_bar.observation_id
    assert first_bar.producer_payload_hash != changed_bar.producer_payload_hash

    with tempfile.TemporaryDirectory() as temporary:
        archive = module.MonthlyArchive(Path(temporary))
        collector = module.MarketDataCollector(
            source=FakePublicSource([]),
            archive=archive,
            identities=identities,
            env_lineage_id="fixture-lineage",
            backfill=module.BackfillPolicy(batch_size=2, inter_request_seconds=0),
            clock_ms=lambda: now,
        )
        collector.ingest(raw_bar(JANUARY_LAST_BAR), "WS_LIVE")
        try:
            collector.ingest(changed, "WS_LIVE")
        except module.CollectionRefused as error:
            assert str(error) == "same observation_id has different producer bytes"
        else:
            raise AssertionError("same-id changed producer bytes were accepted")
        assert len(archive.bars("BTC", "15m")) == 1
    print("SYNTHETIC SAME-ID CONFLICT THROUGH INGEST: PASS")


def append_failure_cursor_check(module: types.ModuleType = subject) -> None:
    """A failed first-seen append must leave the live cursor at the prior stored bar."""
    now = JANUARY_LAST_BAR + 10 * STEP
    with tempfile.TemporaryDirectory() as temporary:
        archive = module.MonthlyArchive(Path(temporary))
        source = FakePublicSource([])
        collector = module.MarketDataCollector(
            source=source,
            archive=archive,
            identities=identities_for(module),
            env_lineage_id="fixture-lineage",
            backfill=module.BackfillPolicy(batch_size=2, inter_request_seconds=0),
            clock_ms=lambda: now,
        )
        collector.ingest(raw_bar(JANUARY_LAST_BAR), "WS_LIVE")
        with patch.object(
            archive,
            "append_bar",
            side_effect=module.CollectionRefused("fixture append failure"),
        ):
            try:
                collector.ingest(raw_bar(JANUARY_LAST_BAR + STEP), "WS_LIVE")
            except module.CollectionRefused as error:
                assert str(error) == "fixture append failure"
            else:
                raise AssertionError("injected append failure was accepted")
        collector.ingest(raw_bar(JANUARY_LAST_BAR + STEP), "WS_LIVE")
        collector.ingest(raw_bar(JANUARY_LAST_BAR + 2 * STEP), "WS_LIVE")
        assert source.snapshot_calls == [], ("append_failure_advanced_cursor", source.snapshot_calls)
        assert [int(bar["bar_open_time"]) for bar in archive.bars("BTC", "15m")] == [
            JANUARY_LAST_BAR,
            JANUARY_LAST_BAR + STEP,
            JANUARY_LAST_BAR + 2 * STEP,
        ]
    print("APPEND FAILURE LEAVES LIVE CURSOR RETRYABLE: PASS")


def persisted_record_check() -> None:
    """Expected values come from fixture inputs/constants, never the stored record."""
    now = FEBRUARY_START + 10 * STEP
    with tempfile.TemporaryDirectory() as temporary:
        archive = subject.MonthlyArchive(Path(temporary))
        expected_records = []
        for index, producer in enumerate(("WS_LIVE", "CANDLE_SNAPSHOT")):
            raw = raw_bar(FEBRUARY_START + index * STEP)
            raw["n"] = 11 + index
            # Independent fixture contract, not the production digest implementation.
            def digest(values):
                encoded = json.dumps(values, ensure_ascii=False, allow_nan=False,
                                     separators=(",", ":")).encode("utf-8")
                return hashlib.sha256(encoded).hexdigest()

            payload_hash = digest([raw[key] for key in ("t", "s", "i", "o", "h", "l", "c", "v")])
            expected_records.append({
                "observation_id": digest([raw["t"], "BTC", "15m", "HYPERLIQUID", "NATIVE", producer, payload_hash]),
                "producer_payload_hash": payload_hash,
                "symbol": "BTC",
                "interval": "15m",
                "bar_open_time": raw["t"],
                "bar_close_time": raw["t"] + STEP,
                "open": raw["o"],
                "high": raw["h"],
                "low": raw["l"],
                "close": raw["c"],
                "volume": raw["v"],
                "venue": "HYPERLIQUID",
                "track": "NATIVE",
                "proxy_source": None,
                "source_producer": producer,
                "observation_type": "INITIAL",
                "supersedes_observation_id": None,
                "ingest_time": now,
                "venue_seq": 11 + index,
                "env_lineage_id": "fixture-lineage",
                "schema_version": "0.1.0",
            })
            bar = subject.normalize_bar(raw, source_producer=producer, ingest_time=now,
                                        env_lineage_id="fixture-lineage", identities=IDENTITIES)
            assert bar is not None
            assert archive.append_bar(bar) == "APPENDED"
        # Read the actual monthly bytes, independently of the archive reader.
        path = Path(temporary) / "bars" / "HYPERLIQUID" / "BTC" / "15m" / "2026-02.jsonl"
        records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        assert len(records) == 2, ("persisted_record_count", len(records))
        for index, (record, expected) in enumerate(zip(records, expected_records)):
            assert set(record) == set(expected), ("persisted_field_inventory", index, sorted(record))
            for field, value in expected.items():
                assert record[field] == value, ("persisted_field", index, field, record[field], value)
    print("COMPLETE PERSISTED RECORDS (21 fields, two bars): PASS")


def persisted_record_mutant_check() -> None:
    original = subject.MonthlyArchive._append
    for field in ("open", "env_lineage_id"):
        def corrupt(path, record):
            value = record["close"] if field == "open" else "CORRUPTED"
            return original(path, {**record, field: value})

        with patch.object(subject.MonthlyArchive, "_append", staticmethod(corrupt)):
            archive_check()  # The unchanged inherited fence accepts this same deviant.
            try:
                persisted_record_check()
            except AssertionError as error:
                assert error.args and error.args[0][:3] == ("persisted_field", 0, field), error.args
            else:
                raise AssertionError(f"persisted {field} corruption was accepted")
        print(f"PERSISTED FENCE PROOF ({field}): OLD_FENCE_ACCEPTS_DEVIANT; NEW_FENCE_REJECTS_DEVIANT")
        print(f"REINTRODUCTION MUTANT (persisted {field} corrupted): DETECTED")


def interval_matrix_check(module: types.ModuleType = subject) -> None:
    assert set(module.INTERVAL_MS) == set(EXPECTED_INTERVAL_MS)
    for interval, step in EXPECTED_INTERVAL_MS.items():
        first_open = FEBRUARY_START - step
        complete_gap = module.detect_gap(first_open, first_open + step, "BTC", interval)
        assert complete_gap is None, ("interval_complete_gap", interval, complete_gap)
        assert module.detect_gap(
            first_open, first_open + 3 * step, "BTC", interval
        ) == module.Gap("BTC", interval, first_open + step, first_open + 3 * step, 2)

        source = FakePublicSource(
            [raw_bar(first_open + step, interval), raw_bar(first_open + 2 * step, interval)]
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = module.MonthlyArchive(root)
            collector = module.MarketDataCollector(
                source=source,
                archive=archive,
                identities=identities_for(module),
                env_lineage_id="fixture-lineage",
                backfill=module.BackfillPolicy(batch_size=2, inter_request_seconds=0),
                clock_ms=lambda: first_open + 5 * step,
            )
            collector.ingest(raw_bar(first_open, interval), "WS_LIVE")
            collector.ingest(raw_bar(first_open + 3 * step, interval), "WS_LIVE")
            recovered = [int(bar["bar_open_time"]) for bar in archive.bars("BTC", interval)]
            assert recovered == [first_open + offset * step for offset in range(4)], (
                "interval_recovered_bar_open_times",
                interval,
                recovered,
            )
            directory = root / "bars" / "HYPERLIQUID" / "BTC" / interval
            assert (directory / "2026-01.jsonl").is_file()
            assert (directory / "2026-02.jsonl").is_file()
            assert source.snapshot_calls == [
                ("BTC", interval, first_open + step, first_open + 3 * step)
            ]
    print("FOUR-INTERVAL ARCHIVE/GAP/ROLLOVER MATRIX: PASS")


def old_forming_bar_fence(module: types.ModuleType) -> None:
    """The fence carried through round 4: a direct normalize_bar call. Kept ONLY as the comparison
    arm of the carried-fence discriminating-power proof (TESTS.md); no longer a closure check."""
    assert module.normalize_bar(
        raw_bar(JANUARY_LAST_BAR),
        source_producer="WS_LIVE",
        ingest_time=JANUARY_LAST_BAR + STEP - 1,
        env_lineage_id="fixture-lineage",
        identities=identities_for(module),
    ) is None


def gap_report_check() -> None:
    assert subject.detect_gap(
        JANUARY_LAST_BAR, JANUARY_LAST_BAR + 3 * STEP, "BTC", "15m"
    ) == subject.Gap(
        "BTC", "15m", JANUARY_LAST_BAR + STEP, JANUARY_LAST_BAR + 3 * STEP, 2
    )
    assert subject.detect_gap(
        JANUARY_LAST_BAR, JANUARY_LAST_BAR + STEP, "BTC", "15m"
    ) is None


def gap_report_cli_check() -> None:
    expected_gaps = (
        "GAP symbol=BTC interval=15m first_missing=2026-02-01T00:00:00Z last_missing=2026-02-01T00:15:00Z",
        "GAP symbol=BTC interval=1h first_missing=2026-02-01T00:00:00Z last_missing=2026-02-01T01:00:00Z",
        "GAP symbol=BTC interval=4h first_missing=2026-02-01T00:00:00Z last_missing=2026-02-01T04:00:00Z",
        "GAP symbol=BTC interval=1d first_missing=2026-02-01T00:00:00Z last_missing=2026-02-02T00:00:00Z",
    )
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        incomplete = subject.MonthlyArchive(root / "incomplete")
        complete = subject.MonthlyArchive(root / "complete")
        for interval in EXPECTED_INTERVALS:
            step = EXPECTED_INTERVAL_MS[interval]
            first_open = FEBRUARY_START - step
            for offset in range(4):
                open_time = first_open + offset * step
                bar = subject.normalize_bar(
                    raw_bar(open_time, interval),
                    source_producer="FIXTURE",
                    ingest_time=open_time + step,
                    env_lineage_id="fixture-lineage",
                    identities=IDENTITIES,
                )
                assert bar is not None
                complete.append_bar(bar)
                if offset in (0, 3):
                    incomplete.append_bar(bar)

        output = StringIO()
        with redirect_stdout(output):
            assert subject.main(["gap-report", "--archive", str(incomplete.root)]) == 0
        assert output.getvalue().splitlines() == [*expected_gaps, "GAPS: 4"]

        output = StringIO()
        with redirect_stdout(output):
            assert subject.main(["gap-report", "--archive", str(complete.root)]) == 0
        assert output.getvalue().splitlines() == ["GAPS: 0"]
    print("GAP-REPORT CLI (gap + complete): PASS")


def lifecycle_check(module: types.ModuleType = subject) -> None:
    subscriptions = [
        (symbol, interval)
        for symbol in module.INITIAL_SYMBOLS
        for interval in module.INITIAL_INTERVALS
    ]
    expected_order = ["connect", *("subscribe" for _pair in subscriptions), "wait", "close"]
    for wait_error in (None, RuntimeError("fixture wait failure")):
        source = FakePublicSource([], lifecycle=True, wait_error=wait_error)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            collector = module.MarketDataCollector(
                source=source,
                archive=module.MonthlyArchive(root),
                identities=identities_for(module),
                env_lineage_id="fixture-lineage",
                backfill=module.BackfillPolicy(batch_size=2, inter_request_seconds=0),
            )
            if wait_error is None:
                collector.run(module.INITIAL_SYMBOLS, module.INITIAL_INTERVALS)
            else:
                try:
                    collector.run(module.INITIAL_SYMBOLS, module.INITIAL_INTERVALS)
                except RuntimeError as error:
                    assert error is wait_error
                else:
                    raise AssertionError("lifecycle wait error did not propagate")
            label = "lifecycle_error_order" if wait_error is not None else "lifecycle_order"
            assert source.calls == expected_order, (label, source.calls)
            assert source.subscriptions == subscriptions
            assert durable_files(root) == []
    print("OFFLINE COLLECTOR LIFECYCLE (success + wait error): PASS")


def runtime_start_refusal_check(
    socket_attempts: list[object], module: types.ModuleType = subject
) -> None:
    calls = {"loader": 0, "interpreter": 0, "backend": 0, "collector": 0}
    synthetic_packet: dict[str, object] = {}

    def fake_loader(_path: Path) -> dict[str, object]:
        calls["loader"] += 1
        return synthetic_packet

    def fake_interpreter(_packet: object) -> SimpleNamespace:
        calls["interpreter"] += 1
        return SimpleNamespace(
            decision_number=188,
            numeric_settings={},
            archive_root=Path("fixture-only"),
            identities=IDENTITIES,
            env_lineage_id="fixture-only",
            symbols=(),
            intervals=(),
        )

    def fake_backend() -> object:
        calls["backend"] += 1
        return object()

    def fake_collector(**_kwargs: object) -> object:
        calls["collector"] += 1
        raise module.CollectionRefused("collector construction tripwire")

    # Tripwires are created on the module under test whether or not the names exist there:
    # on the fixed module every counter must stay 0; on the packet-interpretation mutant the
    # restored main() body reaches the loader and the counter becomes 1.
    with ExitStack() as stack:
        stack.enter_context(patch.object(module, "load_permission_packet", fake_loader, create=True))
        stack.enter_context(
            patch.object(module, "validate_permission_packet", fake_interpreter, create=True)
        )
        stack.enter_context(
            patch.object(module, "_require_single_connection_selection", lambda _value: None, create=True)
        )
        stack.enter_context(
            patch.object(module, "_backfill_policy", lambda _value: object(), create=True)
        )
        stack.enter_context(
            patch.object(module, "HyperliquidPublicSource", fake_backend, create=True)
        )
        stack.enter_context(patch.object(module, "MarketDataCollector", fake_collector))
        errors = StringIO()
        with redirect_stderr(errors):
            for decision, packet in ((187, {}), (188, {"synthetic": "content"})):
                synthetic_packet = packet
                try:
                    module.main(
                        [
                            "run",
                            "--permission-packet",
                            "fixture-only.json",
                            "--owner-approved-start-decision",
                            str(decision),
                        ]
                    )
                except SystemExit as error:
                    assert error.code == 2
                else:
                    raise AssertionError("collector start was accepted")

    assert calls == {"loader": 0, "interpreter": 0, "backend": 0, "collector": 0}, ("forbidden_effect_counters", calls)
    assert socket_attempts == []
    assert set(module.UNSET_NUMERIC_QUESTIONS) == EXPECTED_OPEN_QUESTIONS
    assert errors.getvalue() == REFUSAL_TEXT * 2


def static_boundary_check(
    module: types.ModuleType = subject, source_text: str | None = None
) -> None:
    """Collect every boundary violation, then assert once, so a mutant covers each rule it breaks."""
    text = source_text if source_text is not None else Path(subject.__file__).read_text(encoding="utf-8")
    tree = ast.parse(text)
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add(node.module or "")
    violations: list[str] = []
    if any(name == "hyperliquid" or name.startswith("hyperliquid.") for name in imported):
        violations.append("import:hyperliquid")
    if "eth_account" in imported:
        violations.append("import:eth_account")
    for attribute in ("HyperliquidPublicSource", "load_permission_packet", "validate_permission_packet", "RuntimePermission"):
        if hasattr(module, attribute):
            violations.append(f"attribute:{attribute}")
    for reserved_field in ("archive_format", "collector_start_authorized", "identity_contracts"):
        if reserved_field in text:
            violations.append(f"reserved_field:{reserved_field}")
    for forbidden in ("os.environ", ".order("):
        if forbidden in text:
            violations.append(f"text:{forbidden}")
    assert violations == [], ("boundary_violations", violations)


# --- D026 mutants: exact aa602e9c hunks re-inserted into the fixed module text -------------------

FIXED_MAIN_TAIL = '''    args = parser.parse_args(argv)
    if args.command == "gap-report":
        return _print_gap_report(args.archive, args.symbol, args.interval)
    parser.exit(
        2,
        "REFUSED: Decision 187 authorizes building only; collector runtime requires "
        "a future owner-ratified permission protocol and backend\\n",
    )
'''

BASE_MAIN_TAIL = '''    args = parser.parse_args(argv)

    try:
        permission = validate_permission_packet(load_permission_packet(args.permission_packet))
        if args.owner_approved_start_decision != permission.decision_number:
            raise CollectionRefused(
                "explicit start decision does not match the permission packet"
            )
        _require_single_connection_selection(permission.numeric_settings)
        collector = MarketDataCollector(
            source=HyperliquidPublicSource(),
            archive=MonthlyArchive(permission.archive_root),
            identities=permission.identities,
            env_lineage_id=permission.env_lineage_id,
            backfill=_backfill_policy(permission.numeric_settings),
        )
        collector.run(permission.symbols, permission.intervals)
    except CollectionRefused as error:
        parser.exit(2, f"REFUSED: {error}\\n")
    return 0
'''

BASE_PERMISSION_FAMILY = '''_FORBIDDEN_PERMISSION_KEYS = ("account", "credential", "private_key", "secret", "wallet")
_REQUIRED_NEVER_ACTIONS = {"accounts", "credentials", "orders", "positions", "broker"}
_PERMISSION_KEYS = {
    "collector_start_decision",
    "collector_start_authorized",
    "scope",
    "machine",
    "archive_root",
    "archive_format",
    "writes",
    "symbols",
    "intervals",
    "stop_notification",
    "never",
    "env_lineage_id",
    "numeric_settings",
    "identity_contracts",
}


@dataclass(frozen=True)
class RuntimePermission:
    decision_number: int
    machine: str
    archive_root: Path
    symbols: tuple[str, ...]
    intervals: tuple[str, ...]
    stop_notification: str
    env_lineage_id: str
    numeric_settings: Mapping[str, object]
    identities: IdentityPolicy


def _strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise CollectionRefused(f"duplicate permission-packet key: {key}")
        result[key] = value
    return result


def load_permission_packet(path: Path) -> Mapping[str, object]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(
                handle,
                object_pairs_hook=_strict_object,
                parse_constant=lambda token: (_ for _ in ()).throw(
                    CollectionRefused(f"non-JSON number in permission packet: {token}")
                ),
            )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise CollectionRefused(f"cannot read permission packet: {path}") from error
    if not isinstance(value, Mapping):
        raise CollectionRefused("permission packet must be one JSON object")
    return value


def _walk_keys(value: object) -> list[str]:
    if isinstance(value, Mapping):
        keys = [str(key).lower() for key in value]
        for child in value.values():
            keys.extend(_walk_keys(child))
        return keys
    if isinstance(value, list):
        return [key for child in value for key in _walk_keys(child)]
    return []


def _unset(value: object) -> bool:
    return value is None or value == "" or value == [] or value == {}


def validate_permission_packet(packet: Mapping[str, object]) -> RuntimePermission:
    """Validate the technical interlock; this does not itself grant authority."""

    unknown_packet_keys = sorted(set(packet) - _PERMISSION_KEYS)
    if unknown_packet_keys:
        raise CollectionRefused(
            f"unknown permission-packet field(s): {', '.join(unknown_packet_keys)}"
        )
    forbidden_keys = sorted(
        key
        for key in _walk_keys(packet)
        if any(token in key for token in _FORBIDDEN_PERMISSION_KEYS)
    )
    if forbidden_keys:
        raise CollectionRefused(
            f"credential/account fields are forbidden: {', '.join(forbidden_keys)}"
        )
    decision = packet.get("collector_start_decision")
    if isinstance(decision, bool) or not isinstance(decision, int):
        raise CollectionRefused("missing collector_start_decision from a separate owner permission packet")
    if decision == 187:
        raise CollectionRefused("decision 187 authorizes building only, not starting the collector")
    if packet.get("collector_start_authorized") is not True:
        raise CollectionRefused("collector_start_authorized is not true in the separate permission packet")
    if packet.get("scope") != "public_market_data_only":
        raise CollectionRefused("permission scope must be public_market_data_only")
    raise CollectionRefused("mutant: remainder of the removed validator is not needed to reach the seam")


'''

BASE_EVENT_PATH = '''    def event_path(self, event: Mapping[str, object]) -> Path:
        return (
            self.root
            / "events"
            / _safe_part(str(event["venue"]), "venue")
            / _safe_part(str(event["symbol"]), "symbol")
            / _safe_part(str(event["interval"]), "interval")
            / f"{_month(int(event['detected_at']))}.jsonl"
        )

'''

BASE_APPEND_EVENT = '''
    def append_event(self, event: Mapping[str, object]) -> None:
        path = self.event_path(event)
        if any(existing.get("event_id") == event.get("event_id") for existing in self._records(path)):
            raise CollectionRefused("duplicate event_id")
        self._append(path, event)
'''

BASE_RECORD_GAP = '''    def _record_gap(self, gap: Gap, detected_at: int) -> None:
        event: dict[str, object] = {
            "record_type": "GAP",
            "venue": "HYPERLIQUID",
            "symbol": gap.symbol,
            "interval": gap.interval,
            "window_start": gap.window_start,
            "window_end": gap.window_end,
            "detected_at": detected_at,
            "detail": {"missing_bars": gap.missing_bars},
            "producer": "WS_LIVE",
            "env_lineage_id": self.env_lineage_id,
        }
        event["event_id"] = self.identities.event.digest(event)
        self.archive.append_event(event)

'''

BASE_SDK_BACKEND = '''class HyperliquidPublicSource:
    """Lazy, public-info-only SDK adapter.  Construction performs no I/O."""

    def __init__(self) -> None:
        self._info: object | None = None

    def connect(self) -> None:
        from hyperliquid.info import Info
        from hyperliquid.utils import constants

        self._info = Info(constants.MAINNET_API_URL, skip_ws=False)

    def _client(self) -> object:
        if self._info is None:
            raise CollectionRefused("public market source is not connected")
        return self._info

    def candles_snapshot(
        self, symbol: str, interval: str, start_ms: int, end_ms: int
    ) -> Sequence[Mapping[str, object]]:
        client = self._client()
        return client.candles_snapshot(symbol, interval, start_ms, end_ms)  # type: ignore[attr-defined,no-any-return]

    def subscribe(
        self,
        symbol: str,
        interval: str,
        callback: Callable[[Mapping[str, object]], None],
    ) -> None:
        client = self._client()

        def receive(message: Mapping[str, object]) -> None:
            data = message.get("data")
            if not isinstance(data, Mapping):
                raise CollectionRefused("unexpected public candle message")
            callback(data)

        client.subscribe(  # type: ignore[attr-defined]
            {"type": "candle", "coin": symbol, "interval": interval}, receive
        )

    def wait(self) -> None:
        manager = getattr(self._client(), "ws_manager", None)
        if manager is None:
            raise CollectionRefused("public WebSocket manager is unavailable")
        manager.join()

    def close(self) -> None:
        if self._info is not None:
            self._info.disconnect_websocket()  # type: ignore[attr-defined]


'''


def _splice(text: str, anchor: str, replacement: str) -> str:
    if text.count(anchor) != 1:
        raise AssertionError(f"mutant anchor not unique/present: {anchor[:60]!r}")
    return text.replace(anchor, replacement)


def mutant_text(label: str) -> str:
    fixed = Path(subject.__file__).read_text(encoding="utf-8")
    if label == "refusal prefix changed":
        return _splice(
            fixed,
            '        "REFUSED: Decision 187 authorizes building only; collector runtime requires "\n',
            '        "REFUSED: MUTANT run boundary; collector runtime requires "\n',
        )
    if label == "broken lifecycle":
        return _splice(
            fixed,
            "            self.source.wait()\n        finally:\n            self.source.close()\n",
            "            self.source.wait()\n        except BaseException:\n            raise\n        self.source.close()\n",
        )
    if label == "swapped interval steps":
        return _splice(
            fixed,
            '    "1h": 60 * 60 * 1000,\n    "4h": 4 * 60 * 60 * 1000,\n',
            '    "1h": 4 * 60 * 60 * 1000,\n    "4h": 60 * 60 * 1000,\n',
        )
    if label in ("packet interpretation", "packet interpretation (static boundary)"):
        text = _splice(fixed, FIXED_MAIN_TAIL, BASE_MAIN_TAIL)
        return _splice(text, "def _safe_part(value: str, label: str) -> str:\n",
                       BASE_PERMISSION_FAMILY + "def _safe_part(value: str, label: str) -> str:\n")
    if label == "durable gap event":
        text = _splice(fixed, "class IdentityPolicy:\n    payload: HashContract\n    observation: HashContract\n",
                       "class IdentityPolicy:\n    payload: HashContract\n    observation: HashContract\n    event: HashContract\n")
        text = _splice(text, '            / f"{_month(bar.bar_open_time)}.jsonl"\n        )\n\n',
                       '            / f"{_month(bar.bar_open_time)}.jsonl"\n        )\n\n' + BASE_EVENT_PATH)
        text = _splice(text, '        self._append(path, asdict(bar))\n        return "APPENDED"\n',
                       '        self._append(path, asdict(bar))\n        return "APPENDED"\n' + BASE_APPEND_EVENT)
        text = _splice(text, "                if gap is not None:\n                    self._fill_gap(gap)\n",
                       "                if gap is not None:\n                    self._record_gap(gap, now)\n                    self._fill_gap(gap)\n")
        return _splice(text, "    def _fill_gap(self, gap: Gap) -> None:\n",
                       BASE_RECORD_GAP + "    def _fill_gap(self, gap: Gap) -> None:\n")
    if label == "concrete SDK import":
        return _splice(fixed, "def main(argv: Sequence[str] | None = None) -> int:\n",
                       BASE_SDK_BACKEND + "def main(argv: Sequence[str] | None = None) -> int:\n")
    if label == "forming bar written":
        # Deviant: normalize_bar still returns None for a forming bar, but ingest persists it anyway.
        return _splice(fixed, "        if bar is None:\n            return None\n",
                       "        if bar is None:\n"
                       "            self.archive._append(self.archive.root / \"bars\" / \"FORMING.jsonl\", dict(raw))  # mutant\n"
                       "            return None\n")
    if label == "append before gap":
        return _splice(
            fixed,
            '        if source_producer == "WS_LIVE":\n'
            '            key = (bar.symbol, bar.interval)\n'
            '            previous = self._last_live_open.get(key)\n',
            '        if source_producer == "WS_LIVE":\n'
            '            self.archive.append_bar(bar)  # mutant: incoming bar persisted before gap validation\n'
            '            key = (bar.symbol, bar.interval)\n'
            '            previous = self._last_live_open.get(key)\n',
        )
    if label == "replay does not seed cursor":
        # Deviant: restores the complete pre-fix restart path, with no archive rehydration and no
        # replay seeding, so the next live bar is admitted with no gap check.
        text = _splice(
            fixed,
            '        if self.archive.classify_bar(bar) == "IDENTICAL_REPLAY_NOOP":\n'
            '            if source_producer == "WS_LIVE":\n'
            '                # A restarted collector can meet an identical replay of the stored last bar as its\n'
            '                # first live frame; seed the cursor here, and never rewind it on an older replay.\n'
            '                key = (bar.symbol, bar.interval)\n'
            '                previous = self._last_live_open.get(key)\n'
            '                self._last_live_open[key] = (\n'
            '                    bar.bar_open_time if previous is None else max(previous, bar.bar_open_time)\n'
            '                )\n'
            '            return bar\n',
            '        if self.archive.classify_bar(bar) == "IDENTICAL_REPLAY_NOOP":\n'
            '            return bar  # mutant: identical replay never seeds the live cursor\n',
        )
        return _splice(
            text,
            '            if key not in self._last_live_open:\n',
            '            if False:  # mutant: restart does not rehydrate the live cursor\n',
        )
    if label == "restart does not rehydrate cursor":
        return _splice(
            fixed,
            '            if key not in self._last_live_open:\n',
            '            if False:  # mutant: restart does not rehydrate the live cursor\n',
        )
    if label == "persisted order sorted":
        return _splice(
            fixed,
            "                for previous_open, next_open in zip(persisted_live_opens, persisted_live_opens[1:]):\n",
            "                persisted_live_opens = sorted(persisted_live_opens)  # mutant\n"
            "                for previous_open, next_open in zip(persisted_live_opens, persisted_live_opens[1:]):\n",
        )
    if label == "persisted interval filtered":
        return _splice(
            fixed,
            '                    if record.get("source_producer") != "WS_LIVE":\n'
            '                        continue\n'
            '                    if record.get("symbol") != symbol or record.get("interval") != interval:\n'
            '                        raise CollectionRefused(\n'
            '                            "persisted WS_LIVE identity does not match selected archive"\n'
            '                        )\n',
            '                    if (\n'
            '                        record.get("symbol") != symbol\n'
            '                        or record.get("interval") != interval\n'
            '                        or record.get("source_producer") != "WS_LIVE"\n'
            '                    ):\n'
            '                        continue\n',
        )
    if label == "forming history not reconstructed":
        return _splice(
            fixed,
            '        if source_producer == "WS_LIVE":\n'
            '            symbol = bar.symbol if bar is not None else str(raw["s"])\n',
            '        if bar is None:\n'
            '            return None\n'
            '        if source_producer == "WS_LIVE":\n'
            '            symbol = bar.symbol if bar is not None else str(raw["s"])\n',
        )
    if label == "persisted timestamp diagnostic leaked":
        text = _splice(
            fixed,
            "                    try:\n"
            "                        _iso_utc(persisted_open)\n"
            "                    except (OSError, OverflowError, ValueError) as error:\n"
            "                        raise CollectionRefused(\n"
            "                            \"persisted WS_LIVE bar_open_time is not UTC-renderable\"\n"
            "                        ) from error\n",
            "",
        )
        return _splice(
            text,
            '                        try:\n'
            '                            gap_at = _iso_utc(gap.window_start)\n'
            '                        except (OSError, OverflowError, ValueError) as error:\n'
            '                            raise CollectionRefused(\n'
            '                                "persisted WS_LIVE sequence has an invalid timestamp"\n'
            '                            ) from error\n'
            '                        raise CollectionRefused(f"persisted WS_LIVE sequence has a gap at {gap_at}")\n',
            '                        gap_at = _iso_utc(gap.window_start)\n'
            '                        raise CollectionRefused(f"persisted WS_LIVE sequence has a gap at {gap_at}")\n',
        )
    if label == "persisted timestamp representability removed":
        return _splice(
            fixed,
            "                    try:\n"
            "                        _iso_utc(persisted_open)\n"
            "                    except (OSError, OverflowError, ValueError) as error:\n"
            "                        raise CollectionRefused(\n"
            "                            \"persisted WS_LIVE bar_open_time is not UTC-renderable\"\n"
            "                        ) from error\n",
            "",
        )
    if label == "persisted timestamp coerced":
        return _splice(
            fixed,
            "                    persisted_open = record.get(\"bar_open_time\")\n"
            "                    if type(persisted_open) is not int:\n"
            "                        raise CollectionRefused(\n"
            "                            \"persisted WS_LIVE bar_open_time must be an integer\"\n"
            "                        )\n"
            "                    if persisted_open % step:\n"
            "                        raise CollectionRefused(\n"
            "                            \"persisted WS_LIVE bar_open_time is off interval\"\n"
            "                        )\n",
            "                    persisted_open = int(record[\"bar_open_time\"])  # mutant\n",
        )
    if label == "persisted grid validation removed":
        return _splice(
            fixed,
            "                    if persisted_open % step:\n"
            "                        raise CollectionRefused(\n"
            "                            \"persisted WS_LIVE bar_open_time is off interval\"\n"
            "                        )\n",
            "",
        )
    if label == "persisted gap validation removed":
        return _splice(
            fixed,
            '                for previous_open, next_open in zip(persisted_live_opens, persisted_live_opens[1:]):\n'
            '                    gap = self.gap_detector(\n'
            '                        previous_open, next_open, symbol, interval\n'
            '                    )\n'
            '                    if gap is not None:\n'
            '                        try:\n'
            '                            gap_at = _iso_utc(gap.window_start)\n'
            '                        except (OSError, OverflowError, ValueError) as error:\n'
            '                            raise CollectionRefused(\n'
            '                                "persisted WS_LIVE sequence has an invalid timestamp"\n'
            '                            ) from error\n'
            '                        raise CollectionRefused(f"persisted WS_LIVE sequence has a gap at {gap_at}")\n',
            '',
        )
    if label in TOKEN_MUTANTS:
        # Text-only mutants for the speculative guard rules (no such token exists at aa602e9c);
        # they are scanned, never executed.
        return _splice(fixed, "def main(argv: Sequence[str] | None = None) -> int:\n",
                       TOKEN_MUTANTS[label] + "\n\n\ndef main(argv: Sequence[str] | None = None) -> int:\n")
    raise AssertionError(f"unknown mutant: {label}")


TOKEN_MUTANTS = {
    "eth_account import": "import eth_account  # mutant: a signing library must never enter this module",
    "os.environ read": 'MUTANT_ENV = os.environ.get("HYPERLIQUID_KEY")  # mutant: no environment/credential reads',
    "order call": 'def mutant_order(client):\n    return client.order("BTC", 1)  # mutant: no order placement',
}


def build_mutant(label: str) -> tuple[types.ModuleType, str]:
    text = mutant_text(label)
    module = types.ModuleType(f"market_data_collector_mutant_{label.replace(' ', '_')}")
    module.__file__ = f"<mutant:{label}>"
    # dataclass processing resolves annotations through sys.modules[cls.__module__];
    # the entry is removed again by mutation_checks. In-memory only; never written to disk.
    sys.modules[module.__name__] = module
    exec(compile(text, module.__file__, "exec"), module.__dict__)
    return module, text


def interval_step_mutant_check() -> None:
    module, _text = build_mutant("swapped interval steps")
    try:
        try:
            interval_matrix_check(module=module)
        except AssertionError as error:
            assert error.args and error.args[0][0] == "interval_complete_gap", error.args
            print("INTERVAL-STEP MUTANT (1h/4h swapped): DETECTED")
        else:
            raise AssertionError("swapped interval-step mutant was not detected")
    finally:
        sys.modules.pop(module.__name__, None)


def lifecycle_mutant_check() -> None:
    module, _text = build_mutant("broken lifecycle")
    try:
        try:
            lifecycle_check(module=module)
        except AssertionError as error:
            assert error.args and error.args[0][0] == "lifecycle_error_order", error.args
            print("LIFECYCLE MUTANT (close skipped after wait error): DETECTED")
        else:
            raise AssertionError("broken lifecycle mutant was accepted")
    finally:
        sys.modules.pop(module.__name__, None)


def refusal_fence_proof(socket_attempts: list[object]) -> None:
    module, _text = build_mutant("refusal prefix changed")
    try:
        errors = StringIO()
        with redirect_stderr(errors):
            for decision in (187, 188):
                try:
                    module.main(
                        [
                            "run",
                            "--permission-packet",
                            "fixture-only.json",
                            "--owner-approved-start-decision",
                            str(decision),
                        ]
                    )
                except SystemExit as error:
                    assert error.code == 2
                else:
                    raise AssertionError("refusal-text mutant accepted collector start")
        assert errors.getvalue().count(REFUSAL_SUFFIX) == 2
        old_outcome = "OLD_FENCE_ACCEPTS_DEVIANT"
        try:
            assert errors.getvalue() == REFUSAL_TEXT * 2
        except AssertionError:
            new_outcome = "NEW_FENCE_REJECTS_DEVIANT"
        else:
            raise AssertionError("exact refusal fence accepted the deviant")
        print(f"CARRIED FENCE PROOF (refusal): {old_outcome}; {new_outcome}")
    finally:
        sys.modules.pop(module.__name__, None)
    assert socket_attempts == []


def carried_fence_proof(socket_attempts: list[object]) -> None:
    """TESTS.md carried-fence rule: the forming-bar fence changed in round 5, so show one exact
    deviant that the OLD assertion (direct normalize_bar) accepts and the NEW assertion
    (collector.ingest + durable files unchanged) rejects, recording both outcomes."""
    module, _text = build_mutant("forming bar written")
    try:
        old_forming_bar_fence(module)  # OLD fence: passes on the deviant (normalize_bar is untouched)
        old_outcome = "OLD_FENCE_ACCEPTS_DEVIANT"
        try:
            archive_check(module=module)
        except AssertionError as error:
            assert error.args and error.args[0][0] == "durable_files_changed", error.args
            new_outcome = "NEW_FENCE_REJECTS_DEVIANT"
        else:
            raise AssertionError("new forming-bar fence accepted the deviant")
        print(f"CARRIED FENCE PROOF (forming bar): {old_outcome}; {new_outcome}")
    finally:
        sys.modules.pop(module.__name__, None)
    assert socket_attempts == []


def mutation_checks(socket_attempts: list[object]) -> None:
    fixed_text = Path(subject.__file__).read_text(encoding="utf-8")
    cases = (
        ("packet interpretation", True,
         lambda module, _text: runtime_start_refusal_check(socket_attempts, module=module),
         ("forbidden_effect_counters", {"loader": 2, "interpreter": 2, "backend": 1, "collector": 1})),
        ("packet interpretation (static boundary)", True,
         lambda module, text: static_boundary_check(module=module, source_text=text),
         ("boundary_violations", ["attribute:load_permission_packet", "attribute:validate_permission_packet",
                                  "attribute:RuntimePermission", "reserved_field:archive_format",
                                  "reserved_field:collector_start_authorized", "reserved_field:identity_contracts"])),
        ("durable gap event", True, lambda module, _text: archive_check(module=module),
         ("durable_output_families", ["bars", "events"])),
        ("concrete SDK import", True,
         lambda module, text: static_boundary_check(module=module, source_text=text),
         ("boundary_violations", ["import:hyperliquid", "attribute:HyperliquidPublicSource"])),
        ("forming bar written", True, lambda module, _text: archive_check(module=module),
         "durable_files_changed"),
        ("append before gap", True,
         lambda module, _text: replay_and_gap_atomicity_check(module=module),
         ("failed_gap_rows", [JANUARY_LAST_BAR, JANUARY_LAST_BAR + 3 * STEP])),
        ("replay does not seed cursor", True,
         lambda module, _text: restart_replay_seeds_live_cursor_check(module=module),
         ("restart_replay_cursor", (None, [JANUARY_LAST_BAR, JANUARY_LAST_BAR + 3 * STEP], 0))),
        ("restart does not rehydrate cursor", True,
         lambda module, _text: restart_persisted_latest_cursor_check(module=module),
         ("restart_persisted_latest_gap", (None,
          [JANUARY_LAST_BAR, JANUARY_LAST_BAR + STEP, JANUARY_LAST_BAR + 2 * STEP,
          JANUARY_LAST_BAR + 5 * STEP], 0))),
        ("persisted gap validation removed", True,
         lambda module, _text: restart_persisted_gap_refusal_check(module=module),
         ("restart_persisted_gap", (None,
          [JANUARY_LAST_BAR, JANUARY_LAST_BAR + STEP, JANUARY_LAST_BAR + 5 * STEP,
          JANUARY_LAST_BAR + 6 * STEP], 0))),
        ("persisted order sorted", True,
         lambda module, _text: restart_persisted_sorting_counterexample_check(module=module),
         ("persisted_sorted_order", "accepted")),
        ("persisted interval filtered", True,
         lambda module, _text: persisted_interval_identity_refusal_check(module=module),
         ("persisted_interval", "mismatching", "accepted")),
        ("forming history not reconstructed", True,
         lambda module, _text: forming_first_frame_reconstructs_history_check(module=module),
         ("forming_history", [])),
        ("persisted timestamp diagnostic leaked", True,
         lambda module, _text: persisted_huge_timestamp_gap_refusal_check(module=module),
         ("persisted_huge_timestamp", "OverflowError")),
        ("persisted timestamp representability removed", True,
         lambda module, _text: persisted_huge_timestamp_public_ingest_check(module=module),
         ("single", "bar sequence is non-increasing or off interval")),
        ("persisted timestamp coerced", True,
         lambda module, _text: persisted_timestamp_case_check(
             "numeric string", str(JANUARY_LAST_BAR), module=module
         ),
         ("persisted_timestamp", "numeric string", "accepted", True, 0)),
        ("persisted grid validation removed", True,
         lambda module, _text: persisted_off_grid_refusal_check(module=module),
         ("persisted_off_grid", "accepted")),
        ("eth_account import", False,
         lambda _module, text: static_boundary_check(module=subject, source_text=text),
         ("boundary_violations", ["import:eth_account"])),
        ("os.environ read", False,
         lambda _module, text: static_boundary_check(module=subject, source_text=text),
         ("boundary_violations", ["text:os.environ"])),
        ("order call", False,
         lambda _module, text: static_boundary_check(module=subject, source_text=text),
         ("boundary_violations", ["text:.order("])),
    )
    carried_fence_proof(socket_attempts)
    refusal_fence_proof(socket_attempts)
    for label, execute, check, expected in cases:
        module, text = build_mutant(label) if execute else (None, mutant_text(label))
        try:
            assert text != fixed_text
            try:
                check(module, text)
            except AssertionError as error:
                # The mutant must fail on exactly the assertion it was built to break, with the expected payload
                # (for the durable-files fence the payload carries the before/after listings; match its label).
                observed = error.args[0] if error.args else None
                if isinstance(expected, str):
                    assert isinstance(observed, tuple) and observed[0] == expected, (label, error.args, expected)
                else:
                    assert observed == expected, (label, error.args, expected)
                print(f"REINTRODUCTION MUTANT ({label}): DETECTED")
            else:
                raise AssertionError(f"reintroduction mutant was accepted: {label}")
        finally:
            if module is not None:
                sys.modules.pop(module.__name__, None)
    assert sys.modules["market_data_collector"] is subject
    assert socket_attempts == []


def main() -> None:
    attempts: list[object] = []

    def blocked_network(*args, **kwargs):
        attempts.append((args, kwargs))
        raise AssertionError("network access attempted by local check")

    # Socket tripwires stay armed for every check, including the modified copy and the mutants.
    with ExitStack() as stack:
        stack.enter_context(patch.object(socket.socket, "connect", blocked_network))
        stack.enter_context(patch.object(socket, "create_connection", blocked_network))
        archive_check()
        replay_and_gap_atomicity_check()
        restart_replay_seeds_live_cursor_check()
        restart_persisted_latest_cursor_check()
        restart_persisted_gap_refusal_check()
        restart_persisted_order_refusal_check()
        restart_persisted_sorting_counterexample_check()
        persisted_interval_identity_refusal_check()
        forming_first_frame_reconstructs_history_check()
        persisted_huge_timestamp_gap_refusal_check()
        persisted_huge_timestamp_public_ingest_check()
        persisted_timestamp_type_refusal_check()
        persisted_off_grid_refusal_check()
        synthetic_same_id_conflict_check()
        append_failure_cursor_check()
        persisted_record_check()
        persisted_record_mutant_check()
        interval_matrix_check()
        interval_step_mutant_check()
        gap_report_check()
        gap_report_cli_check()
        lifecycle_check()
        lifecycle_mutant_check()
        runtime_start_refusal_check(attempts)
        static_boundary_check()

        try:
            archive_check(lambda previous, next_open, symbol, interval: None)
        except AssertionError as error:
            assert error.args and error.args[0] == (
                "recovered_bar_open_times", [JANUARY_LAST_BAR, JANUARY_LAST_BAR + 3 * STEP]
            ), error.args
            print("MODIFIED COPY (gap detection removed): DETECTED")
        else:
            raise AssertionError("modified copy without gap detection was accepted")
        mutation_checks(attempts)
        assert attempts == []
    print("NETWORK ATTEMPTS: 0")
    print("MARKET DATA COLLECTOR CHECK: PASS")


if __name__ == "__main__":
    main()
