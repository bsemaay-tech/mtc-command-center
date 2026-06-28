"""
Alpaca → native US-equities 10m bundle downloader (QuantLens).

Pulls 10-minute OHLCV bars from Alpaca Market Data v2 for a frozen symbol list,
filters to Regular Trading Hours (RTH), validates, and writes a QuantLens bundle
(normalized CSVs + dataset_manifest.json) the engine can consume via
MEGA_BUNDLE_MANIFEST. Does NOT touch protected scope (02_MTC_BACKTEST), the
engine, Pine, MTC_V2, or parity. Does NOT run a backtest or generate result
artifacts.

Credentials (never hard-coded, never committed) — set before running:
    $env:APCA_API_KEY_ID     = "..."
    $env:APCA_API_SECRET_KEY = "..."

Usage:
    python alpaca_download_us_equities_10m.py \
        --symbols SPY QQQ AAPL MSFT NVDA AMZN TSLA \
        --start 2016-01-01 --feed iex --adjustment all

Notes:
- Alpaca free tier = IEX feed (history back to ~2016). SIP needs a paid plan
  (pass --feed sip if you have it).
- adjustment=all → split + dividend adjusted (REQUIRED for NVDA/AMZN/TSLA splits).
- 10Min is a native Alpaca timeframe; no resampling needed.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

BARS_URL = "https://data.alpaca.markets/v2/stocks/bars"

# RTH in US/Eastern → fixed UTC windows per DST regime. Alpaca timestamps are UTC.
# We keep bars whose START is within [09:30, 16:00) ET. Use a tz-aware check.
try:
    from zoneinfo import ZoneInfo
    _ET = ZoneInfo("America/New_York")
except Exception:  # pragma: no cover
    _ET = None


def _headers():
    kid = os.environ.get("APCA_API_KEY_ID")
    sec = os.environ.get("APCA_API_SECRET_KEY")
    if not kid or not sec:
        sys.exit("ERROR: set APCA_API_KEY_ID and APCA_API_SECRET_KEY env vars first.")
    return {"APCA-API-KEY-ID": kid, "APCA-API-SECRET-KEY": sec}


def fetch_symbol(symbol, start, end, feed, adjustment, headers):
    """Yield bar dicts for one symbol, following pagination."""
    page_token = None
    while True:
        params = {
            "symbols": symbol,
            "timeframe": "10Min",
            "start": start,
            "end": end,
            "limit": "10000",
            "feed": feed,
            "adjustment": adjustment,
            "sort": "asc",
        }
        if page_token:
            params["page_token"] = page_token
        url = BARS_URL + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers=headers)
        for attempt in range(5):
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    payload = json.load(r)
                break
            except Exception as e:
                if attempt == 4:
                    raise
                time.sleep(2 * (attempt + 1))  # backoff on rate limit / transient
        bars = (payload.get("bars") or {}).get(symbol) or []
        for b in bars:
            yield b
        page_token = payload.get("next_page_token")
        if not page_token:
            break


def in_rth(ts_utc):
    """ts_utc: aware UTC datetime. True if bar start is within 09:30–16:00 ET, Mon–Fri."""
    if _ET is None:
        return True
    et = ts_utc.astimezone(_ET)
    if et.weekday() > 4:
        return False
    minutes = et.hour * 60 + et.minute
    return (9 * 60 + 30) <= minutes < (16 * 60)


def validate(rows):
    """rows: list of (ts_utc_str, o,h,l,c,v). Return dict of checks."""
    times = [r[0] for r in rows]
    dups = len(times) - len(set(times))
    mono = all(times[i] <= times[i + 1] for i in range(len(times) - 1))
    ohlc_fail = 0
    for _, o, h, l, c, _v in rows:
        o, h, l, c = float(o), float(h), float(l), float(c)
        if h < max(o, c) - 1e-9 or l > min(o, c) + 1e-9 or h < l:
            ohlc_fail += 1
    return {
        "bar_count": len(rows),
        "duplicate_timestamps": dups,
        "monotonic": mono,
        "ohlc_sanity_failures": ohlc_fail,
        "first_timestamp_utc": rows[0][0] if rows else None,
        "last_timestamp_utc": rows[-1][0] if rows else None,
    }


def sha256(p: Path):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", nargs="+",
                    default=["SPY", "QQQ", "AAPL", "MSFT", "NVDA", "AMZN", "TSLA"])
    ap.add_argument("--start", default="2016-01-01")
    ap.add_argument("--end", default=dt.date.today().isoformat())
    ap.add_argument("--feed", default="iex", choices=["iex", "sip"])
    ap.add_argument("--adjustment", default="all",
                    choices=["raw", "split", "dividend", "all"])
    ap.add_argument("--rth-only", action="store_true", default=True)
    ap.add_argument("--out-root",
                    default=str(Path(__file__).resolve().parents[1] / "data"))
    args = ap.parse_args()

    headers = _headers()
    stamp = dt.date.today().isoformat()
    bundle = Path(args.out_root) / f"native_us_equities_10m_alpaca_{stamp}"
    norm_dir = bundle / "normalized"
    man_dir = bundle / "manifests"
    norm_dir.mkdir(parents=True, exist_ok=True)
    man_dir.mkdir(parents=True, exist_ok=True)

    datasets = []
    for sym in args.symbols:
        print(f"[{sym}] downloading 10Min {args.start}->{args.end} feed={args.feed} adj={args.adjustment} ...")
        rows = []
        for b in fetch_symbol(sym, args.start, args.end, args.feed, args.adjustment, headers):
            ts = dt.datetime.fromisoformat(b["t"].replace("Z", "+00:00"))
            if args.rth_only and not in_rth(ts):
                continue
            rows.append((
                ts.strftime("%Y-%m-%d %H:%M:%S+00:00"),
                b["o"], b["h"], b["l"], b["c"], b.get("v", 0),
            ))
        if not rows:
            print(f"[{sym}] WARNING: 0 bars (check feed/entitlement/date range). Skipping.")
            continue
        rows.sort(key=lambda r: r[0])
        checks = validate(rows)
        status = "PASS" if (checks["duplicate_timestamps"] == 0 and checks["monotonic"]
                            and checks["ohlc_sanity_failures"] == 0) else "FAIL"
        out = norm_dir / f"{sym}_10m.csv"
        with open(out, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["timestamp_utc", "open", "high", "low", "close", "volume"])
            w.writerows(rows)
        ds = {
            "symbol": sym, "source_symbol": sym, "exchange": "ALPACA_" + args.feed.upper(),
            "asset_class": "US_EQUITY", "timeframe_normalized": "10m",
            "normalized_path": f"normalized/{sym}_10m.csv",
            "ohlcv_validation_status": status,
            "provider": f"alpaca_{args.feed}", "is_24_7": False,
            "first_timestamp_utc": checks["first_timestamp_utc"],
            "last_timestamp_utc": checks["last_timestamp_utc"],
            "bar_count": checks["bar_count"],
            "volume_available": True,
            "adjustment_policy": f"alpaca_{args.adjustment}",
            "session_policy_inferred": "RTH_ONLY_09_30_to_16_00_ET" if args.rth_only else "ALL_HOURS",
            "normalized_sha256": sha256(out),
        }
        datasets.append(ds)
        print(f"[{sym}] {checks['bar_count']} bars  {checks['first_timestamp_utc']} -> {checks['last_timestamp_utc']}  status={status}")

    manifest = {
        "bundle_id": bundle.name,
        "created_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "provider": f"alpaca_{args.feed}",
        "adjustment_policy": f"alpaca_{args.adjustment}",
        "classification": "RESEARCH_ONLY_NOT_PROMOTABLE",
        "universe": [d["symbol"] for d in datasets],
        "datasets": datasets,
    }
    man_path = man_dir / "dataset_manifest.json"
    with open(man_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nBundle: {bundle}")
    print(f"Manifest: {man_path}")
    print(f"Symbols written: {len(datasets)} / {len(args.symbols)}")
    print("Next: set MEGA_BUNDLE_MANIFEST to the manifest and run mega_walk_forward.py with --symbol/--tf 10m.")


if __name__ == "__main__":
    main()
