import os
import shutil
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


def _clean_root(path: Path) -> Path:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


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


class StubFillSource:
    def __init__(self, snapshots):
        self.snapshots = snapshots

    def connect(self) -> None:
        pass

    def candles_snapshot(self, symbol: str, interval: str, start_ms: int, end_ms: int):
        rows = self.snapshots.get((symbol, interval), [])
        return [row for row in rows if start_ms <= int(row["t"]) < end_ms]

    def subscribe(self, symbol: str, interval: str, callback) -> None:
        pass

    def wait(self) -> None:
        pass

    def close(self) -> None:
        pass


def _collector(archive_root: Path, source) -> MarketDataCollector:
    return MarketDataCollector(
        source=source,
        archive=MonthlyArchive(archive_root),
        identities=_build_identities(),
        env_lineage_id="d11",
        backfill=BackfillPolicy(batch_size=4, inter_request_seconds=0.0),
        clock_ms=lambda: 20_000_000,
    )


def _raw_bar(open_ms: int, price: str = "105", producer: str = "WS_LIVE") -> dict:
    return {
        "proxy_source": None,
        "venue": "HYPERLIQUID",
        "source_producer": producer,
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
        "close": price,
        "volume": "1",
        "o": "100",
        "h": "110",
        "l": "90",
        "c": price,
        "v": "1",
        "n": 1,
        "venue_seq": 1,
    }


def _lines(root: Path) -> int:
    path = root / "bars" / "HYPERLIQUID" / "BTC" / "1h" / "1970-01.jsonl"
    if not path.exists():
        return 0
    return len(path.read_text(encoding="utf-8").splitlines())


print("D11")

root_i = _clean_root(BASE / "d11" / "restart")
collector1 = _collector(root_i, object())
first = collector1.ingest(_raw_bar(3_600_000), "WS_LIVE")
print(f"case-i-first: status=APPENDED lines={_lines(root_i)}")

collector1_again = _collector(root_i, object())
replay = collector1_again.ingest(_raw_bar(3_600_000), "WS_LIVE")
print(
    f"case-i-replay: status={collector1_again.archive.classify_bar(replay)} "
    f"lines={_lines(root_i)} "
    f"cursor={collector1_again._last_live_open}"
)

print("D11: payload correction refusal case")
try:
    collector1_again.ingest(_raw_bar(3_600_000, price="109"), "WS_LIVE")
    print("case-ii: OK-UNEXPECTED")
except Exception as exc:
    print(f"case-ii: ERROR {type(exc).__name__}: {exc}")

root_iii = _clean_root(BASE / "d11" / "restart_gap")
collector_gap_fill = StubFillSource(
    {
        ("BTC", "1h"): [
            _raw_bar(3_600_000, producer="CANDLE_SNAPSHOT"),
            _raw_bar(7_200_000, producer="CANDLE_SNAPSHOT"),
        ],
    }
)
collector_gap = _collector(root_iii, collector_gap_fill)
collector_gap.ingest(_raw_bar(0), "WS_LIVE")
collector_gap.ingest(_raw_bar(3_600_000, producer="CANDLE_SNAPSHOT"), "CANDLE_SNAPSHOT")
collector_gap.ingest(_raw_bar(7_200_000, producer="CANDLE_SNAPSHOT"), "CANDLE_SNAPSHOT")
collector_gap.ingest(_raw_bar(10_800_000), "WS_LIVE")
print(f"case-iii-base: lines={_lines(root_iii)}")

collector_gap_restart = _collector(root_iii, object())
try:
    collector_gap_restart.ingest(_raw_bar(14_400_000), "WS_LIVE")
    print("case-iii: OK-UNEXPECTED")
except Exception as exc:
    print(f"case-iii: ERROR {type(exc).__name__}: {exc}")
