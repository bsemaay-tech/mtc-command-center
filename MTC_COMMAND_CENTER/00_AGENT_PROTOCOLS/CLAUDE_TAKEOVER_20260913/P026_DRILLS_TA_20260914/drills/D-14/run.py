import os
import sys
from pathlib import Path

LANE = Path(r"C:/tmp/P026_DRILLS_TA_20260914")
_TMP = LANE / "tmp"
_TMP.mkdir(parents=True, exist_ok=True)
os.environ["TEMP"] = str(_TMP)
os.environ["TMP"] = str(_TMP)
os.environ["PYTHONUTF8"] = "1"

sys.path.insert(0, str((LANE / "wt").resolve()))

from market_data_collector import BackfillPolicy, HashContract, IdentityPolicy, MarketDataCollector, MonthlyArchive

BASE = LANE / "fixtures"


class SnapshotSource:
    """Stub PublicMarketSource. Returns rows unfiltered so collector checks fire."""

    def __init__(self, snapshot_rows):
        self.snapshot_rows = snapshot_rows
        self.connect_count = 0

    def connect(self) -> None:
        self.connect_count += 1

    def candles_snapshot(self, symbol: str, interval: str, start_ms: int, end_ms: int):
        rows = self.snapshot_rows.get((symbol, interval), [])
        if callable(rows):
            rows = rows(start_ms, end_ms)
        return rows

    def subscribe(self, symbol: str, interval: str, callback) -> None:
        pass

    def wait(self) -> None:
        pass

    def close(self) -> None:
        pass


class CursorStuckRow(dict):
    """Eligible via .get('t') (in-range) but ['t'] does not advance the cursor."""

    def get(self, key, default=None):
        if key == "t":
            return 3_600_000
        return super().get(key, default)


def _build_identities() -> IdentityPolicy:
    return IdentityPolicy(
        payload=HashContract(
            fields=(
                "venue",
                "source_producer",
                "symbol",
                "interval",
                "bar_open_time",
                "bar_close_time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "venue_seq",
            ),
            algorithm="sha256",
            encoding="utf-8",
            serialization="json",
        ),
        observation=HashContract(
            fields=(
                "venue",
                "track",
                "proxy_source",
                "source_producer",
                "symbol",
                "interval",
                "bar_open_time",
                "producer_payload_hash",
            ),
            algorithm="sha256",
            encoding="utf-8",
            serialization="json",
        ),
    )


def _collector(root: Path, source: SnapshotSource) -> MarketDataCollector:
    return MarketDataCollector(
        source=source,
        archive=MonthlyArchive(root),
        identities=_build_identities(),
        env_lineage_id="d14",
        backfill=BackfillPolicy(batch_size=4, inter_request_seconds=0.0),
        clock_ms=lambda: 20_000_000,
    )


def _bar(open_ms: int, close: str = "105") -> dict:
    return {
        "proxy_source": None,
        "venue": "HYPERLIQUID",
        "source_producer": "CANDLE_SNAPSHOT",
        "s": "BTC",
        "symbol": "BTC",
        "i": "1h",
        "interval": "1h",
        "t": open_ms,
        "bar_open_time": open_ms,
        "bar_close_time": open_ms + 3_600_000,
        "open": "100",
        "high": "110",
        "low": "90",
        "close": close,
        "volume": "1",
        "o": "100",
        "h": "110",
        "l": "90",
        "c": close,
        "v": "1",
        "n": 1,
        "venue_seq": 1,
    }


def _run_case(label: str, source: SnapshotSource) -> None:
    archive_root = BASE / "d14" / label
    if archive_root.exists():
        for child in sorted(archive_root.rglob("*"), reverse=True):
            if child.is_file():
                child.unlink()
            elif child.is_dir():
                try:
                    child.rmdir()
                except OSError:
                    pass
    archive_root.mkdir(parents=True, exist_ok=True)

    collector = _collector(archive_root, source)
    collector.ingest(_bar(0), "WS_LIVE")
    try:
        collector.ingest(_bar(10_800_000), "WS_LIVE")
        count_path = archive_root / "bars" / "HYPERLIQUID" / "BTC" / "1h" / "1970-01.jsonl"
        print(
            f"{label}: OK lines={0 if not count_path.exists() else len(count_path.read_text(encoding='utf-8').splitlines())}"
        )
    except Exception as exc:
        print(f"{label}: ERROR {type(exc).__name__}: {exc}")


def _snapshot_mode_ok(start_ms: int, end_ms: int):
    return [
        _bar(3_600_000),
        _bar(7_200_000, close="106"),
    ]


def _snapshot_mode_none(start_ms: int, end_ms: int):
    return []


def _snapshot_mode_no_progress(start_ms: int, end_ms: int):
    # Collector eligible-filter uses row.get("t"); cursor math uses row["t"] + step.
    return [CursorStuckRow(_bar(0))]


def _snapshot_mode_residual(start_ms: int, end_ms: int):
    # Skip 3_600_000 so the page advances past a hole; completeness check fires.
    return [_bar(7_200_000, close="106")]


print("D14")
_run_case("forced_disconn_ok", SnapshotSource({("BTC", "1h"): _snapshot_mode_ok}))
_run_case("forced_disconn_no_snapshot", SnapshotSource({("BTC", "1h"): _snapshot_mode_none}))
_run_case("forced_disconn_no_progress", SnapshotSource({("BTC", "1h"): _snapshot_mode_no_progress}))
_run_case("forced_disconn_residual", SnapshotSource({("BTC", "1h"): _snapshot_mode_residual}))
