from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_SYMBOLS = [
    "ETHUSDT",
    "SOLUSDT",
    "BNBUSDT",
    "XRPUSDT",
    "ADAUSDT",
    "AVAXUSDT",
    "DOGEUSDT",
    "LINKUSDT",
    "DOTUSDT",
    "POLUSDT",
    "LTCUSDT",
    "TRXUSDT",
    "NEARUSDT",
    "APTUSDT",
    "ARBUSDT",
    "OPUSDT",
]

INTERVALS = {
    "15m": "15",
    "1h": "60",
    "2h": "120",
    "4h": "240",
    "1d": "1D",
}


def utc_ms(value: str) -> int:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)


def get_json(url: str) -> Any:
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_klines(symbol: str, interval: str, start_ms: int, end_ms: int, pause_seconds: float) -> list[list[Any]]:
    rows: list[list[Any]] = []
    cursor = start_ms
    while cursor < end_ms:
        params = urllib.parse.urlencode(
            {
                "symbol": symbol,
                "interval": interval,
                "startTime": cursor,
                "endTime": end_ms,
                "limit": 1500,
            }
        )
        url = f"https://fapi.binance.com/fapi/v1/klines?{params}"
        batch = get_json(url)
        if not batch:
            break
        rows.extend(batch)
        next_cursor = int(batch[-1][0]) + 1
        if next_cursor <= cursor:
            break
        cursor = next_cursor
        time.sleep(pause_seconds)
    dedup: dict[int, list[Any]] = {}
    for row in rows:
        open_time = int(row[0])
        if start_ms <= open_time <= end_ms:
            dedup[open_time] = row
    return [dedup[key] for key in sorted(dedup)]


def write_chart_csv(path: Path, klines: list[list[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(["time", "open", "high", "low", "close"])
        for row in klines:
            writer.writerow([int(row[0]) // 1000, row[1], row[2], row[3], row[4]])


def detect_gaps(path: Path) -> dict[str, Any]:
    times: list[int] = []
    with path.open("r", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            times.append(int(row["time"]))
    if len(times) < 3:
        return {"base_interval_seconds": None, "gap_count": 0, "first_20_gaps": []}
    deltas = [times[idx] - times[idx - 1] for idx in range(1, len(times)) if times[idx] > times[idx - 1]]
    base = min(deltas) if deltas else None
    gaps = []
    if base:
        for idx in range(1, len(times)):
            delta = times[idx] - times[idx - 1]
            if delta > base * 1.5:
                gaps.append(
                    {
                        "prev": times[idx - 1],
                        "next": times[idx],
                        "delta_seconds": delta,
                        "missing_intervals_est": int(delta / base) - 1,
                    }
                )
    return {"base_interval_seconds": base, "gap_count": len(gaps), "first_20_gaps": gaps[:20]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--report-dir", required=True)
    parser.add_argument("--symbols", nargs="*", default=DEFAULT_SYMBOLS)
    parser.add_argument("--intervals", nargs="*", default=list(INTERVALS.keys()))
    parser.add_argument("--start", default="2025-09-01T00:00:00+00:00")
    parser.add_argument("--end", default=datetime.now(timezone.utc).isoformat())
    parser.add_argument("--pause-seconds", type=float, default=0.08)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    report_dir = Path(args.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    start_ms = utc_ms(args.start)
    end_ms = utc_ms(args.end)
    results = []
    failures = []
    for symbol in args.symbols:
        for interval in args.intervals:
            if interval not in INTERVALS:
                failures.append({"symbol": symbol, "interval": interval, "error": "unsupported_interval"})
                continue
            tv_tf = INTERVALS[interval]
            out_path = out_dir / f"BINANCE_{symbol}.P, {tv_tf}_binance_public.csv"
            try:
                klines = fetch_klines(symbol, interval, start_ms, end_ms, args.pause_seconds)
                write_chart_csv(out_path, klines)
                gap_info = detect_gaps(out_path)
                results.append(
                    {
                        "symbol": symbol,
                        "tradingview_symbol": f"{symbol}.P",
                        "exchange": "BINANCE",
                        "interval": interval,
                        "timeframe": tv_tf,
                        "source": "binance_futures_public_klines",
                        "path": str(out_path),
                        "rows": len(klines),
                        "first_time": int(klines[0][0]) // 1000 if klines else None,
                        "last_time": int(klines[-1][0]) // 1000 if klines else None,
                        "sha256": sha256_file(out_path),
                        "bytes": out_path.stat().st_size,
                        **gap_info,
                    }
                )
                print(f"ok {symbol} {interval} rows={len(klines)}")
            except Exception as exc:
                failures.append({"symbol": symbol, "interval": interval, "error": str(exc)})
                print(f"fail {symbol} {interval}: {exc}")
    payload = {
        "started_at": args.start,
        "ended_at": args.end,
        "output_dir": str(out_dir),
        "results": results,
        "failures": failures,
    }
    (report_dir / "binance_futures_public_download_report.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    with (report_dir / "binance_futures_public_download_summary.csv").open("w", encoding="utf-8", newline="") as fh:
        fieldnames = sorted({key for item in results for key in item.keys()})
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
