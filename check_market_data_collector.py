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
