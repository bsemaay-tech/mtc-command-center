from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
import urllib.parse
import urllib.request
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
BUNDLE_ROOT = ROOT.parent / "MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427"
OUTPUT_ROOT = ROOT / "06_QUANTLENS_LAB" / "research" / "data_acquisition_5m_2026_05_03"
DATA_ROOT = OUTPUT_ROOT / "normalized" / "binance_futures"
MANIFEST_PATH = OUTPUT_ROOT / "manifest_5m_research.json"
QUALITY_PATH = OUTPUT_ROOT / "DATA_QUALITY_REPORT.csv"
DOWNLOAD_REPORT_PATH = OUTPUT_ROOT / "DATA_DOWNLOAD_REPORT.md"
README_PATH = OUTPUT_ROOT / "README.md"

BINANCE_FAPI_KLINES = "https://fapi.binance.com/fapi/v1/klines"
INTERVAL = "5m"
INTERVAL_MS = 5 * 60 * 1000
API_LIMIT = 1500
MINIMUM_SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]


def utc_ms(value: str) -> int:
    return int(pd.Timestamp(value, tz="UTC").timestamp() * 1000)


def now_last_closed_open_ms() -> int:
    now = datetime.now(UTC)
    floored = now - timedelta(
        minutes=now.minute % 5,
        seconds=now.second,
        microseconds=now.microsecond,
    )
    return int((floored - timedelta(minutes=5)).timestamp() * 1000)


def bundle_symbols() -> list[str]:
    manifest = json.loads((BUNDLE_ROOT / "manifests" / "dataset_manifest.json").read_text(encoding="utf-8"))
    return sorted({row["symbol"] for row in manifest["datasets"] if row.get("exchange") == "BINANCE"})


def request_klines(symbol: str, start_ms: int, end_ms: int, retries: int = 4) -> list[list[Any]]:
    query = urllib.parse.urlencode(
        {
            "symbol": symbol,
            "interval": INTERVAL,
            "startTime": start_ms,
            "endTime": end_ms,
            "limit": API_LIMIT,
        }
    )
    url = f"{BINANCE_FAPI_KLINES}?{query}"
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Binance request failed for {symbol} at {start_ms}: {last_error}")


def normalize_klines(rows: list[list[Any]]) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])
    frame = pd.DataFrame(
        rows,
        columns=[
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_volume",
            "trade_count",
            "taker_buy_base_volume",
            "taker_buy_quote_volume",
            "ignore",
        ],
    )
    frame = frame[["open_time", "open", "high", "low", "close", "volume"]].copy()
    frame["timestamp"] = pd.to_datetime(frame["open_time"], unit="ms", utc=True).dt.strftime("%Y-%m-%dT%H:%M:%S%z")
    frame["timestamp"] = frame["timestamp"].str.replace(r"(\+0000)$", "+00:00", regex=True)
    for column in ["open", "high", "low", "close", "volume"]:
        frame[column] = pd.to_numeric(frame[column], errors="raise")
    return frame[["timestamp", "open", "high", "low", "close", "volume"]]


def download_symbol(symbol: str, start_ms: int, end_ms: int, sleep_seconds: float) -> pd.DataFrame:
    chunks: list[pd.DataFrame] = []
    cursor = start_ms
    while cursor <= end_ms:
        rows = request_klines(symbol, cursor, end_ms)
        if not rows:
            break
        chunk = normalize_klines(rows)
        chunks.append(chunk)
        last_open = int(rows[-1][0])
        next_cursor = last_open + INTERVAL_MS
        if next_cursor <= cursor:
            break
        cursor = next_cursor
        if len(rows) < API_LIMIT:
            break
        time.sleep(sleep_seconds)
    if not chunks:
        return normalize_klines([])
    frame = pd.concat(chunks, ignore_index=True)
    frame = frame.drop_duplicates("timestamp").sort_values("timestamp").reset_index(drop=True)
    return frame


def quality_row(symbol: str, path: Path, frame: pd.DataFrame, start_ms: int, end_ms: int) -> dict[str, Any]:
    duplicate_count = int(frame["timestamp"].duplicated().sum()) if not frame.empty else 0
    expected_index = pd.date_range(
        pd.to_datetime(start_ms, unit="ms", utc=True),
        pd.to_datetime(end_ms, unit="ms", utc=True),
        freq="5min",
    )
    observed = pd.to_datetime(frame["timestamp"], utc=True) if not frame.empty else pd.DatetimeIndex([])
    missing_count = int(len(expected_index.difference(observed)))
    sha256 = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""
    return {
        "symbol": symbol,
        "timeframe": INTERVAL,
        "path": str(path.relative_to(OUTPUT_ROOT)),
        "bar_count": int(len(frame)),
        "first_ts": frame["timestamp"].iloc[0] if not frame.empty else "",
        "last_ts": frame["timestamp"].iloc[-1] if not frame.empty else "",
        "duplicate_bar_count": duplicate_count,
        "missing_candle_count": missing_count,
        "expected_bar_count": int(len(expected_index)),
        "sha256": sha256,
        "status": "FAIL" if len(frame) == 0 or duplicate_count > 0 else ("WARN_MISSING_CANDLES" if missing_count > 0 else "PASS"),
    }


def write_outputs(rows: list[dict[str, Any]], start: str, end_iso: str, mode: str) -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    with QUALITY_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()) if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(rows)
    manifest = {
        "created_at": datetime.now(UTC).isoformat(),
        "source": "binance_futures_fapi_klines",
        "research_only": True,
        "production_manifest_modified": False,
        "timeframe": INTERVAL,
        "start": start,
        "end_last_closed_bar": end_iso,
        "datasets": rows,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    README_PATH.write_text(
        "\n".join(
            [
                "# QuantLens 5m Binance Futures Research Data",
                "",
                "Research-only 5m OHLCV acquisition for blocked intraday strategy proxy tests.",
                "",
                "Run:",
                "`python 06_QUANTLENS_LAB/research/data_acquisition_5m_2026_05_03/download_binance_futures_5m.py --symbols minimum`",
                "",
                "The production data bundle manifest is not modified.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    total_bars = sum(int(row["bar_count"]) for row in rows)
    DOWNLOAD_REPORT_PATH.write_text(
        "\n".join(
            [
                "# DATA DOWNLOAD REPORT",
                "",
                f"- Mode: `{mode}`.",
                f"- Timeframe: `{INTERVAL}`.",
                f"- Start: `{start}`.",
                f"- End last closed bar: `{end_iso}`.",
                f"- Symbols downloaded: `{len(rows)}`.",
                f"- Total bars: `{total_bars}`.",
                "- Production bundle manifest modified: `false`.",
                "- Timezone: UTC storage; New York session conversion is handled in rerun script.",
                "",
                "## Data Quality",
                "- See `DATA_QUALITY_REPORT.csv`.",
                "- Missing candle count is calculated against continuous 5-minute UTC grid between requested start and last closed bar.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbols", choices=["minimum", "all"], default="all")
    parser.add_argument("--start", default="2024-01-01T00:00:00+00:00")
    parser.add_argument("--end", default="")
    parser.add_argument("--sleep", type=float, default=0.08)
    args = parser.parse_args()

    symbols = MINIMUM_SYMBOLS if args.symbols == "minimum" else bundle_symbols()
    start_ms = utc_ms(args.start)
    end_ms = utc_ms(args.end) if args.end else now_last_closed_open_ms()
    end_iso = pd.to_datetime(end_ms, unit="ms", utc=True).isoformat()
    rows: list[dict[str, Any]] = []
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    for symbol in symbols:
        symbol_dir = DATA_ROOT / symbol / INTERVAL
        symbol_dir.mkdir(parents=True, exist_ok=True)
        output_path = symbol_dir / f"BINANCE_FUTURES_{symbol}_{INTERVAL}_20240101_RESEARCH.csv"
        frame = download_symbol(symbol, start_ms, end_ms, args.sleep)
        frame.to_csv(output_path, index=False)
        row = quality_row(symbol, output_path, frame, start_ms, end_ms)
        rows.append(row)
        print(f"{symbol} bars={row['bar_count']} missing={row['missing_candle_count']} path={output_path}")
    write_outputs(rows, args.start, end_iso, args.symbols)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
