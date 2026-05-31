from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from datetime import timedelta

import pandas as pd


def normalize_exchange(exchange: str) -> str:
    return exchange.upper().strip()


def normalize_symbol(symbol: str) -> str:
    s = symbol.upper().strip()
    if ":" in s:
        s = s.split(":", 1)[1]
    for suffix in (".P", ".PERP", "-PERP"):
        if s.endswith(suffix):
            s = s[: -len(suffix)]
    return s


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_expected_sha256(dataset: Path, expected: str | None) -> str:
    digest = sha256_file(dataset)
    if expected and digest.lower() != expected.lower():
        raise ValueError(
            f"Checksum mismatch: expected={expected.lower()} actual={digest.lower()} dataset={dataset}"
        )
    return digest


def parse_timeframe(tf: str) -> timedelta:
    raw = tf.strip().lower()
    if raw.endswith("m"):
        return timedelta(minutes=int(raw[:-1]))
    if raw.endswith("h"):
        return timedelta(hours=int(raw[:-1]))
    if raw.endswith("d"):
        return timedelta(days=int(raw[:-1]))
    raise ValueError(f"Unsupported timeframe format: {tf}")


def load_timestamps(dataset: Path, time_col: str) -> pd.Series:
    suffix = dataset.suffix.lower()
    if suffix == ".parquet":
        df = pd.read_parquet(dataset, columns=[time_col])
    elif suffix in (".csv", ".txt"):
        df = pd.read_csv(dataset, usecols=[time_col])
    else:
        raise ValueError(f"Unsupported dataset format: {dataset.suffix}")
    ts = pd.to_datetime(df[time_col], utc=True, errors="coerce")
    if ts.isna().any():
        raise ValueError(f"Timestamp parse failed for column '{time_col}' in {dataset}")
    return ts.sort_values(ignore_index=True)


def compute_timestamp_quality(ts: pd.Series, expected_step: timedelta | None) -> dict:
    dup_count = int(ts.duplicated().sum())
    gaps: list[dict] = []
    if expected_step is not None and len(ts) > 1:
        expected_seconds = int(expected_step.total_seconds())
        diffs = ts.diff().dt.total_seconds().fillna(expected_seconds)
        bad_idx = diffs[diffs > expected_seconds]
        for idx, gap_sec in bad_idx.items():
            gaps.append(
                {
                    "index": int(idx),
                    "prev_ts": str(ts.iloc[idx - 1]),
                    "next_ts": str(ts.iloc[idx]),
                    "gap_seconds": int(gap_sec),
                }
            )
    return {
        "rows": int(len(ts)),
        "duplicate_timestamps": dup_count,
        "gap_count": len(gaps),
        "gaps": gaps[:20],
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Data parity hardening checks.")
    p.add_argument("--dataset", required=True, help="Dataset file to checksum")
    p.add_argument("--symbol", required=True, help="Symbol to normalize/check")
    p.add_argument("--exchange", required=False, default="BINANCE", help="Exchange to normalize/check")
    p.add_argument("--expect-sha256", required=False, help="Optional expected checksum")
    p.add_argument("--time-col", default="timestamp", help="Timestamp column name")
    p.add_argument("--timeframe", required=False, help="Expected bar interval, e.g. 15m, 1h, 1d")
    p.add_argument("--strict-quality", action="store_true", help="Fail when duplicate/gap quality checks fail")
    p.add_argument("--out", required=False, help="Optional JSON output path")
    args = p.parse_args()

    ds = Path(args.dataset)
    if not ds.exists():
        raise FileNotFoundError(f"Dataset not found: {ds}")
    digest = validate_expected_sha256(ds, args.expect_sha256)
    payload = {
        "dataset": str(ds),
        "sha256": digest,
        "exchange_raw": args.exchange,
        "exchange_normalized": normalize_exchange(args.exchange),
        "symbol_raw": args.symbol,
        "symbol_normalized": normalize_symbol(args.symbol),
    }
    if args.timeframe:
        ts = load_timestamps(ds, args.time_col)
        quality = compute_timestamp_quality(ts, parse_timeframe(args.timeframe))
        payload["quality"] = quality
        if args.strict_quality and (quality["duplicate_timestamps"] > 0 or quality["gap_count"] > 0):
            raise ValueError(
                "Data quality check failed: "
                f"duplicate_timestamps={quality['duplicate_timestamps']} gap_count={quality['gap_count']}"
            )

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"Wrote: {out}")
    else:
        print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
