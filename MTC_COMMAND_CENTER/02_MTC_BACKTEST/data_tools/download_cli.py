"""
Download CLI — fetch OHLCV data from a provider and store as Parquet.

Usage examples
--------------
# Download all BTCUSDT timeframes from 2018-07-01 to today
python mtc_backtest/data_tools/download_cli.py \\
    --provider binance \\
    --symbol BTCUSDT \\
    --start 2018-07-01 \\
    --timeframes 5m,15m,1h,2h,4h,1d \\
    --chunk_days 30 \\
    --out-root 110_/data/processed

# Download from a CSV for a non-crypto symbol
python mtc_backtest/data_tools/download_cli.py \\
    --provider csv \\
    --symbol XAUUSD \\
    --csv-file path/to/gold.csv \\
    --start 2018-01-01 \\
    --timeframes 1d \\
    --out-root 110_/data/processed
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

# Ensure the mtc_backtest package root is on sys.path when run as a script
_HERE = Path(__file__).resolve()
_PKG_ROOT = _HERE.parent.parent
if str(_PKG_ROOT) not in sys.path:
    sys.path.insert(0, str(_PKG_ROOT))

from data_providers import get_provider  # noqa: E402

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
DEFAULT_OUT_ROOT = Path(__file__).resolve().parent.parent.parent / "110_" / "data" / "processed"
DEFAULT_CATALOG = Path(__file__).resolve().parent.parent / "backtest_assets" / "data_catalog.json"

CHUNK_DAYS_LOW_TF = 30    # 5m, 15m
CHUNK_DAYS_HIGH_TF = 365  # 1h, 2h, 4h, 1d

LOW_TF = {"5m", "15m"}


def _chunk_days_for(tf: str, override: int | None) -> int:
    if override is not None:
        return override
    return CHUNK_DAYS_LOW_TF if tf in LOW_TF else CHUNK_DAYS_HIGH_TF


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _load_catalog(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _save_catalog(catalog: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(catalog, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
def download_one(
    *,
    provider_name: str,
    symbol: str,
    timeframe: str,
    start: datetime,
    end: datetime,
    chunk_days: int | None,
    out_root: Path,
    catalog_path: Path,
    sleep_ms: int = 100,
    csv_file: str | None = None,
) -> None:
    """Download one (symbol, timeframe) dataset and update the catalog.

    Resumable: if the output Parquet already exists, reads the last timestamp
    and only downloads data after that point ('top-up' mode).
    """

    # Build provider
    if provider_name == "csv":
        if not csv_file:
            raise ValueError("--csv-file is required when --provider csv")
        provider = get_provider("csv", filepath=csv_file)
    else:
        provider = get_provider(provider_name, sleep_ms=sleep_ms)

    tf_chunk = _chunk_days_for(timeframe, chunk_days)

    # Determine output path
    safe_symbol = symbol.replace("/", "_")
    out_path = out_root / provider_name / safe_symbol / f"{timeframe}.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Check for existing partial data (resume support)
    effective_start = start
    existing_df: pd.DataFrame | None = None
    if out_path.exists():
        existing_df = pd.read_parquet(out_path)
        if len(existing_df) > 0:
            last_ts = existing_df.index[-1]
            # Resume from 1 interval after the last saved bar
            effective_start = last_ts.to_pydatetime().replace(tzinfo=timezone.utc) + timedelta(seconds=1)
            print(
                f"[download_cli] Resuming {symbol}/{timeframe} from {effective_start.date()} "
                f"({len(existing_df):,} bars already saved)"
            )

    if effective_start >= end:
        print(f"[download_cli] {symbol}/{timeframe} already up to date ({len(existing_df or []):,} bars).")
        _update_catalog(symbol, timeframe, out_path, out_root, catalog_path, provider, existing_df)
        return

    # Generate time chunks for the remaining range
    chunks: list[tuple[datetime, datetime]] = []
    cur = effective_start
    while cur < end:
        chunk_end = min(cur + timedelta(days=tf_chunk), end)
        chunks.append((cur, chunk_end))
        cur = chunk_end + timedelta(seconds=1)

    print(
        f"[download_cli] {symbol}/{timeframe} | "
        f"{len(chunks)} chunks x {tf_chunk}d | "
        f"{effective_start.date()} -> {end.date()}"
    )

    # Download chunk by chunk and merge incrementally
    for i, (c_start, c_end) in enumerate(chunks, 1):
        print(f"  chunk {i}/{len(chunks)}  {c_start.date()} -> {c_end.date()}", end="", flush=True)
        df_chunk = provider.fetch_ohlcv(symbol, c_start, c_end, timeframe)
        print(f"  -> {len(df_chunk)} bars")

        # Merge with existing data and write immediately (crash-safe)
        if existing_df is not None and len(existing_df) > 0:
            merged = pd.concat([existing_df, df_chunk])
        else:
            merged = df_chunk
        merged = merged[~merged.index.duplicated(keep="last")].sort_index()
        merged.to_parquet(out_path, engine="pyarrow", index=True)
        existing_df = merged  # update in-memory reference

        if i < len(chunks):
            time.sleep(sleep_ms / 1000.0)

    final_df = existing_df if existing_df is not None else pd.DataFrame()
    bar_count = len(final_df)
    print(
        f"[download_cli] OK {symbol}/{timeframe} "
        f"-> {bar_count} bars total -> {out_path}"
    )

    _update_catalog(symbol, timeframe, out_path, out_root, catalog_path, provider, final_df)


def _update_catalog(
    symbol: str,
    timeframe: str,
    out_path: Path,
    out_root: Path,
    catalog_path: Path,
    provider,
    df: pd.DataFrame | None,
) -> None:
    sha256 = _sha256_file(out_path) if out_path.exists() else ""
    bar_count = len(df) if df is not None else 0
    start_utc = df.index[0].isoformat() if bar_count else ""
    end_utc = df.index[-1].isoformat() if bar_count else ""

    catalog = _load_catalog(catalog_path)
    catalog.setdefault(symbol, {})[timeframe] = {
        "path": str(out_path.relative_to(out_root.parent.parent)).replace("\\", "/"),
        "abs_path": str(out_path).replace("\\", "/"),
        "hash_sha256": sha256,
        "bar_count": bar_count,
        "start_utc": start_utc,
        "end_utc": end_utc,
        "provider": provider.name,
        "is_24_7": provider.is_24_7,
        "last_updated": _now_utc_iso(),
    }
    _save_catalog(catalog, catalog_path)
    print(f"[download_cli] Catalog updated -> {catalog_path}")



# ---------------------------------------------------------------------------
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Download OHLCV data and store as Parquet.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--provider", choices=["binance", "binance_usdm", "csv"], default="binance")
    p.add_argument("--symbol", default="BTCUSDT", help="Ticker symbol (e.g. BTCUSDT, XAUUSD)")
    p.add_argument("--start", default="2018-07-01", help="Start date YYYY-MM-DD (UTC)")
    p.add_argument("--end", default=None, help="End date YYYY-MM-DD (UTC). Default: today")
    p.add_argument(
        "--timeframes",
        default="15m",
        help="Comma-separated timeframes: 5m,15m,1h,2h,4h,1d",
    )
    p.add_argument("--chunk_days", type=int, default=None, help="Override chunk size in days")
    p.add_argument(
        "--out-root",
        default=str(DEFAULT_OUT_ROOT),
        help="Root directory for processed data. Default: 110_/data/processed",
    )
    p.add_argument(
        "--catalog",
        default=str(DEFAULT_CATALOG),
        help="Path to data_catalog.json. Default: mtc_backtest/backtest_assets/data_catalog.json",
    )
    p.add_argument("--sleep_ms", type=int, default=100, help="Sleep ms between requests")
    p.add_argument("--csv-file", default=None, help="Path to CSV/Parquet (required for --provider csv)")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    start = datetime.strptime(args.start, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    if args.end:
        end = datetime.strptime(args.end, "%Y-%m-%d").replace(
            hour=23, minute=59, second=59, tzinfo=timezone.utc
        )
    else:
        end = datetime.now(timezone.utc).replace(hour=23, minute=59, second=59)

    timeframes = [tf.strip() for tf in args.timeframes.split(",") if tf.strip()]
    out_root = Path(args.out_root).resolve()
    catalog_path = Path(args.catalog).resolve()

    for tf in timeframes:
        download_one(
            provider_name=args.provider,
            symbol=args.symbol,
            timeframe=tf,
            start=start,
            end=end,
            chunk_days=args.chunk_days,
            out_root=out_root,
            catalog_path=catalog_path,
            sleep_ms=args.sleep_ms,
            csv_file=args.csv_file,
        )

    print("\n[download_cli] All done.")


if __name__ == "__main__":
    main()
