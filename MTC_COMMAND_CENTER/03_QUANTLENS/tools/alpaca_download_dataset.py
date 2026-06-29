"""
Alpaca multi-asset, multi-timeframe dataset builder (QuantLens).

Builds ONE consolidated native bundle covering everything Alpaca can serve:
US stocks + ETFs (incl. commodity/index/bond/sector proxies) and crypto, across
several timeframes. Writes normalized CSVs + a single dataset_manifest.json the
engine consumes via MEGA_BUNDLE_MANIFEST.

Scope reality (Alpaca):
- Equities/ETFs: IEX feed (free), intraday history from ~2020, daily deeper.
  Commodities/indices/bonds are covered via liquid ETF proxies (GLD, USO, TLT, ...).
- Crypto: Alpaca crypto endpoint, 24/7.
- NO spot forex, NO real CME futures here (need other providers).

Safe-by-default: reads API key from env, commits no secrets, touches no engine /
Pine / MTC_V2 / parity / protected scope, runs no backtest. SKIPS files that
already exist so an interrupted overnight run resumes cleanly.

Usage:
    $env:APCA_API_KEY_ID="..."; $env:APCA_API_SECRET_KEY="..."
    python alpaca_download_dataset.py --timeframes 10m 15m 30m 1h 2h 4h 1d --start 2016-01-01
"""
from __future__ import annotations
import argparse, csv, datetime as dt, hashlib, json, os, sys, time
import urllib.parse, urllib.request
from pathlib import Path

STOCK_URL = "https://data.alpaca.markets/v2/stocks/bars"
CRYPTO_URL = "https://data.alpaca.markets/v1beta3/crypto/us/bars"

try:
    from zoneinfo import ZoneInfo
    _ET = ZoneInfo("America/New_York")
except Exception:
    _ET = None

# Alpaca timeframe string per normalized label
TF_MAP = {"10m": "10Min", "15m": "15Min", "30m": "30Min",
          "1h": "1Hour", "2h": "2Hour", "4h": "4Hour", "1d": "1Day"}
INTRADAY = {"10m", "15m", "30m", "1h", "2h", "4h"}

# --- Universe (Alpaca-coverable, liquid, tradeable) ---
EQUITY_UNIVERSE = {
    # Index ETFs
    "SPY": "index_sp500", "QQQ": "index_nasdaq100", "DIA": "index_dow", "IWM": "index_russell2000",
    # Mega-cap stocks
    "AAPL": "stock", "MSFT": "stock", "NVDA": "stock", "AMZN": "stock", "TSLA": "stock",
    "GOOGL": "stock", "META": "stock", "NFLX": "stock", "AMD": "stock",
    # Commodities (ETF proxies)
    "GLD": "commodity_gold", "SLV": "commodity_silver", "USO": "commodity_oil_wti",
    "BNO": "commodity_oil_brent", "UNG": "commodity_natgas", "DBC": "commodity_broad", "CPER": "commodity_copper",
    # Bonds
    "TLT": "bond_20y", "IEF": "bond_7_10y", "HYG": "bond_highyield", "LQD": "bond_ig",
    # Sectors
    "XLF": "sector_financials", "XLE": "sector_energy", "XLK": "sector_tech", "XLV": "sector_health",
    "XLI": "sector_industrials", "XLY": "sector_discretionary", "XLP": "sector_staples",
    "XLU": "sector_utilities", "XLB": "sector_materials", "XLRE": "sector_realestate", "XLC": "sector_comm",
    # Volatility + international
    "VXX": "volatility_vix", "EEM": "intl_em", "EFA": "intl_dev", "FXI": "intl_china",
}
CRYPTO_UNIVERSE = ["BTC/USD", "ETH/USD", "SOL/USD", "LTC/USD", "BCH/USD", "LINK/USD",
                   "UNI/USD", "AAVE/USD", "DOGE/USD", "AVAX/USD", "DOT/USD", "SHIB/USD"]


def _headers():
    kid = os.environ.get("APCA_API_KEY_ID"); sec = os.environ.get("APCA_API_SECRET_KEY")
    if not kid or not sec:
        sys.exit("ERROR: set APCA_API_KEY_ID and APCA_API_SECRET_KEY env vars first.")
    return {"APCA-API-KEY-ID": kid, "APCA-API-SECRET-KEY": sec}


def _get(url, params, headers):
    for attempt in range(6):
        try:
            req = urllib.request.Request(url + "?" + urllib.parse.urlencode(params), headers=headers)
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except Exception as e:
            if attempt == 5:
                raise
            time.sleep(2 * (attempt + 1))


def fetch(symbol, is_crypto, tf_alpaca, start, end, feed, adjustment, headers):
    url = CRYPTO_URL if is_crypto else STOCK_URL
    token = None
    while True:
        params = {"symbols": symbol, "timeframe": tf_alpaca, "start": start, "end": end,
                  "limit": "10000", "sort": "asc"}
        if not is_crypto:
            params["feed"] = feed; params["adjustment"] = adjustment
        if token:
            params["page_token"] = token
        payload = _get(url, params, headers)
        for b in (payload.get("bars") or {}).get(symbol, []) or []:
            yield b
        token = payload.get("next_page_token")
        if not token:
            break


def in_rth(ts_utc):
    if _ET is None:
        return True
    et = ts_utc.astimezone(_ET)
    if et.weekday() > 4:
        return False
    m = et.hour * 60 + et.minute
    return (9 * 60 + 30) <= m < (16 * 60)


def sha256(p: Path):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def write_symbol_tf(rows, out_path, with_volume):
    cols = ["timestamp_utc", "open", "high", "low", "close"] + (["volume"] if with_volume else [])
    with open(out_path, "w", newline="") as f:
        w = csv.writer(f); w.writerow(cols); w.writerows(rows)


def validate(rows):
    times = [r[0] for r in rows]
    dups = len(times) - len(set(times))
    mono = all(times[i] <= times[i+1] for i in range(len(times)-1))
    bad = 0
    for r in rows:
        o, h, l, c = float(r[1]), float(r[2]), float(r[3]), float(r[4])
        if h < max(o, c) - 1e-9 or l > min(o, c) + 1e-9 or h < l:
            bad += 1
    status = "PASS" if (dups == 0 and mono and bad == 0) else "FAIL"
    return status, dups, mono, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeframes", nargs="+", default=["10m", "15m", "30m", "1h", "2h", "4h", "1d"])
    ap.add_argument("--start", default="2016-01-01")
    ap.add_argument("--end", default=dt.date.today().isoformat())
    ap.add_argument("--feed", default="iex", choices=["iex", "sip"])
    ap.add_argument("--adjustment", default="all", choices=["raw", "split", "dividend", "all"])
    ap.add_argument("--out-root", default=str(Path(__file__).resolve().parents[1] / "data"))
    ap.add_argument("--bundle-name", default=f"native_multiasset_alpaca_{dt.date.today().isoformat()}")
    args = ap.parse_args()

    headers = _headers()
    bundle = Path(args.out_root) / args.bundle_name
    norm = bundle / "normalized"; mans = bundle / "manifests"
    norm.mkdir(parents=True, exist_ok=True); mans.mkdir(parents=True, exist_ok=True)
    man_path = mans / "dataset_manifest.json"

    universe = [(s, False, ac) for s, ac in EQUITY_UNIVERSE.items()] + \
               [(s, True, "crypto") for s in CRYPTO_UNIVERSE]
    datasets = []
    t0 = time.time()
    total = len(universe) * len(args.timeframes)
    done = 0
    for symbol, is_crypto, asset_class in universe:
        norm_sym = symbol.replace("/", "")
        for tf in args.timeframes:
            done += 1
            tf_alpaca = TF_MAP[tf]
            out_path = norm / f"{norm_sym}_{tf}.csv"
            with_volume = True
            if out_path.exists():
                # resume: reuse existing file, just (re)register in manifest
                try:
                    with open(out_path) as f:
                        rdr = csv.reader(f); hdr = next(rdr); first = next(rdr, None)
                        cnt = 1 + sum(1 for _ in rdr) if first else 0
                    print(f"[{done}/{total}] SKIP exists {norm_sym} {tf} ({cnt} rows)")
                except Exception:
                    cnt = 0
                _register(datasets, symbol, norm_sym, asset_class, is_crypto, tf, out_path, args)
                _write_manifest(man_path, bundle, datasets, args)
                continue
            rth = (not is_crypto) and (tf in INTRADAY)
            rows = []
            try:
                for b in fetch(symbol, is_crypto, tf_alpaca, args.start, args.end,
                               args.feed, args.adjustment, headers):
                    ts = dt.datetime.fromisoformat(b["t"].replace("Z", "+00:00"))
                    if rth and not in_rth(ts):
                        continue
                    rows.append((ts.strftime("%Y-%m-%d %H:%M:%S+00:00"),
                                 b["o"], b["h"], b["l"], b["c"], b.get("v", 0)))
            except Exception as e:
                print(f"[{done}/{total}] ERROR {norm_sym} {tf}: {e}")
                continue
            if not rows:
                print(f"[{done}/{total}] EMPTY {norm_sym} {tf} (not available on this feed)")
                continue
            rows.sort(key=lambda r: r[0])
            write_symbol_tf(rows, out_path, with_volume)
            _register(datasets, symbol, norm_sym, asset_class, is_crypto, tf, out_path, args)
            _write_manifest(man_path, bundle, datasets, args)
            el = time.time() - t0
            print(f"[{done}/{total}] {norm_sym} {tf}: {len(rows)} rows  {rows[0][0]}..{rows[-1][0]}  ({el:.0f}s)")

    _write_manifest(man_path, bundle, datasets, args)
    print(f"\nDONE. bundle={bundle}  datasets={len(datasets)}  elapsed={time.time()-t0:.0f}s")


def _register(datasets, symbol, norm_sym, asset_class, is_crypto, tf, out_path, args):
    rows = _read_rows(out_path)
    status, dups, mono, bad = validate(rows)
    ds = {
        "symbol": norm_sym, "source_symbol": symbol,
        "exchange": "CRYPTO" if is_crypto else "ALPACA_" + args.feed.upper(),
        "asset_class": asset_class, "timeframe_normalized": tf,
        "normalized_path": f"normalized/{out_path.name}",
        "ohlcv_validation_status": status,
        "bar_count": len(rows),
        "first_timestamp_utc": rows[0][0] if rows else None,
        "last_timestamp_utc": rows[-1][0] if rows else None,
        "provider": "alpaca_crypto" if is_crypto else f"alpaca_{args.feed}",
        "is_24_7": bool(is_crypto),
        "volume_available": True,
        "adjustment_policy": "crypto_raw" if is_crypto else f"alpaca_{args.adjustment}",
        "session_policy_inferred": "CRYPTO_24_7" if is_crypto else
            ("RTH_ONLY_09_30_to_16_00_ET" if tf in INTRADAY else "DAILY_SESSION"),
        "normalized_sha256": sha256(out_path),
    }
    # de-dup: replace any existing entry for same (symbol, tf)
    for i, d in enumerate(datasets):
        if d["symbol"] == norm_sym and d["timeframe_normalized"] == tf:
            datasets[i] = ds
            return
    datasets.append(ds)


def _read_rows(out_path):
    with open(out_path, newline="") as f:
        r = csv.reader(f); next(r)
        return [tuple(x) for x in r]


def _write_manifest(man_path, bundle, datasets, args):
    manifest = {
        "bundle_id": bundle.name,
        "created_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "provider": f"alpaca_{args.feed}+alpaca_crypto",
        "classification": "RESEARCH_ONLY_NOT_PROMOTABLE",
        "timeframes": args.timeframes,
        "datasets": datasets,
    }
    tmp = man_path.with_suffix(".json.tmp")
    with open(tmp, "w") as f:
        json.dump(manifest, f, indent=2)
    tmp.replace(man_path)


if __name__ == "__main__":
    main()
