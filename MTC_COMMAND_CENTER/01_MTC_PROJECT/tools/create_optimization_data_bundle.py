from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import shutil
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EXPECTED_SYMBOLS = [
    "BTCUSDT",
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
EXPECTED_TIMEFRAMES = ["15m", "1h", "2h", "4h", "1D"]
TIMEFRAME_ALIASES = {
    "15": "15m",
    "15m": "15m",
    "60": "1h",
    "1h": "1h",
    "120": "2h",
    "2h": "2h",
    "240": "4h",
    "4h": "4h",
    "D": "1D",
    "1D": "1D",
    "1d": "1D",
    "1440": "1D",
}
TIMEFRAME_SECONDS = {"15m": 900, "1h": 3600, "2h": 7200, "4h": 14400, "1D": 86400}
METHOD_VERSION = "rule_based_market_regime_v1"


@dataclass(frozen=True)
class SourceFile:
    source_path: Path
    symbol: str
    exchange: str
    timeframe: str
    source_type: str
    row_count: int
    first_timestamp: str | None
    last_timestamp: str | None
    columns: list[str]
    sha256: str
    size_bytes: int
    include_candidate: bool
    skip_reason: str


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_time(value: str) -> datetime | None:
    value = str(value).strip()
    if not value:
        return None
    try:
        if value.isdigit():
            raw = int(value)
            if raw > 10_000_000_000:
                raw //= 1000
            return datetime.fromtimestamp(raw, timezone.utc)
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except ValueError:
        return None


def iso(dt: datetime | None) -> str | None:
    return dt.astimezone(timezone.utc).isoformat() if dt else None


def date_token(value: str | None) -> str:
    if not value:
        return "UNKNOWN"
    return value[:10].replace("-", "")


def infer_from_name(path: Path) -> tuple[str, str, str]:
    name = path.stem
    exchange = "UNKNOWN"
    symbol = "UNKNOWN"
    timeframe = "UNKNOWN"
    if name.upper().startswith("BINANCE_"):
        exchange = "BINANCE"
        rest = name[len("BINANCE_") :]
        if "," in rest:
            symbol_part, tf_part = rest.split(",", 1)
            symbol = symbol_part.strip().replace(".P", "")
            tf_token = tf_part.strip().split("_", 1)[0].strip()
            timeframe = TIMEFRAME_ALIASES.get(tf_token, tf_token)
    return exchange, symbol, timeframe


def classify_source_type(path: Path, columns: list[str]) -> str:
    lower = path.name.lower()
    normalized_columns = {column.lower().strip() for column in columns}
    chart_like = {"open", "high", "low", "close"}.issubset(normalized_columns) and (
        "time" in normalized_columns or "timestamp" in normalized_columns or "datetime" in normalized_columns
    )
    if not chart_like:
        return "not_chart_data"
    if lower.endswith("_binance_public.csv"):
        return "binance_public_futures_klines"
    if lower.startswith("binance_"):
        return "tradingview_chart_csv_binance"
    return "unknown_csv"


def read_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            if not reader.fieldnames:
                return [], []
            return list(reader), list(reader.fieldnames)
    except UnicodeDecodeError:
        with path.open("r", encoding="latin-1", newline="") as fh:
            reader = csv.DictReader(fh)
            if not reader.fieldnames:
                return [], []
            return list(reader), list(reader.fieldnames)


def inspect_source_file(path: Path) -> SourceFile:
    rows, columns = read_rows(path)
    exchange, symbol, timeframe = infer_from_name(path)
    source_type = classify_source_type(path, columns)
    normalized_columns = {column.lower().strip(): column for column in columns}
    time_column = normalized_columns.get("time") or normalized_columns.get("timestamp") or normalized_columns.get("datetime")
    timestamps: list[datetime] = []
    if time_column:
        for row in rows:
            parsed = parse_time(row.get(time_column, ""))
            if parsed:
                timestamps.append(parsed)
    skip_reason = ""
    include_candidate = True
    if source_type in {"not_chart_data", "unknown_csv"}:
        include_candidate = False
        skip_reason = source_type
    elif symbol == "UNKNOWN" or timeframe == "UNKNOWN":
        include_candidate = False
        skip_reason = "symbol_or_timeframe_unknown"
    elif not rows:
        include_candidate = False
        skip_reason = "empty_csv"
    elif len(timestamps) == 0:
        include_candidate = False
        skip_reason = "timestamp_parse_failed"
    return SourceFile(
        source_path=path,
        symbol=symbol,
        exchange=exchange,
        timeframe=timeframe,
        source_type=source_type,
        row_count=len(rows),
        first_timestamp=iso(min(timestamps)) if timestamps else None,
        last_timestamp=iso(max(timestamps)) if timestamps else None,
        columns=columns,
        sha256=sha256_file(path),
        size_bytes=path.stat().st_size,
        include_candidate=include_candidate,
        skip_reason=skip_reason,
    )


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str), encoding="utf-8")


def yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value).replace("\\", "/").replace('"', '\\"')
    return f'"{text}"'


def write_simple_yaml(path: Path, payload: dict[str, Any]) -> None:
    lines: list[str] = []
    for key, value in payload.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                if isinstance(item, dict):
                    lines.append("  -")
                    for item_key, item_value in item.items():
                        if isinstance(item_value, list):
                            lines.append(f"    {item_key}:")
                            for sub in item_value:
                                lines.append(f"      - {yaml_scalar(sub)}")
                        else:
                            lines.append(f"    {item_key}: {yaml_scalar(item_value)}")
                else:
                    lines.append(f"  - {yaml_scalar(item)}")
        else:
            lines.append(f"{key}: {yaml_scalar(value)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def normalize_rows(rows: list[dict[str, str]], columns: list[str]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    normalized_columns = {column.lower().strip(): column for column in columns}
    time_column = normalized_columns.get("time") or normalized_columns.get("timestamp") or normalized_columns.get("datetime")
    volume_column = normalized_columns.get("volume")
    result = []
    for row in rows:
        parsed = parse_time(row.get(time_column, "") if time_column else "")
        if not parsed:
            continue
        item: dict[str, Any] = {
            "timestamp_utc": parsed.isoformat(),
            "open": row[normalized_columns["open"]],
            "high": row[normalized_columns["high"]],
            "low": row[normalized_columns["low"]],
            "close": row[normalized_columns["close"]],
        }
        if volume_column:
            item["volume"] = row.get(volume_column, "")
        result.append(item)
    result.sort(key=lambda item: str(item["timestamp_utc"]))
    notes = {"volume": "present" if volume_column else "missing_in_source"}
    return result, notes


def dataset_id_for(source: SourceFile, used_ids: set[str]) -> str:
    base = f"BINANCE_FUTURES_{source.symbol}_{source.timeframe}_{date_token(source.first_timestamp)}_{date_token(source.last_timestamp)}"
    base = base.replace(".", "").replace("/", "_")
    dataset_id = base
    if dataset_id in used_ids:
        dataset_id = f"{base}_{source.sha256[:8]}"
    used_ids.add(dataset_id)
    return dataset_id


def validate_quality(dataset_id: str, rows: list[dict[str, Any]], timeframe: str, bundle_root: Path) -> dict[str, Any]:
    times: list[datetime] = []
    invalid_rows: list[dict[str, Any]] = []
    duplicates: list[dict[str, Any]] = []
    gaps: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, row in enumerate(rows, start=1):
        ts = parse_time(str(row["timestamp_utc"]))
        if not ts:
            invalid_rows.append({"row": index, "reason": "timestamp_parse_failed"})
            continue
        key = ts.isoformat()
        if key in seen:
            duplicates.append({"row": index, "timestamp_utc": key})
        seen.add(key)
        times.append(ts)
        try:
            open_price = float(row["open"])
            high = float(row["high"])
            low = float(row["low"])
            close = float(row["close"])
            if high < low:
                invalid_rows.append({"row": index, "timestamp_utc": key, "reason": "high_below_low"})
            if open_price < low or open_price > high:
                invalid_rows.append({"row": index, "timestamp_utc": key, "reason": "open_outside_high_low"})
            if close < low or close > high:
                invalid_rows.append({"row": index, "timestamp_utc": key, "reason": "close_outside_high_low"})
            if min(open_price, high, low, close) < 0:
                invalid_rows.append({"row": index, "timestamp_utc": key, "reason": "negative_ohlc"})
            if close <= 0:
                invalid_rows.append({"row": index, "timestamp_utc": key, "reason": "zero_or_negative_close"})
        except (TypeError, ValueError):
            invalid_rows.append({"row": index, "timestamp_utc": key, "reason": "ohlc_parse_failed"})
    times = sorted(times)
    expected_step = TIMEFRAME_SECONDS.get(timeframe)
    if expected_step and len(times) > 1:
        for prev, current in zip(times, times[1:]):
            delta = int((current - prev).total_seconds())
            if delta > expected_step * 1.5:
                gaps.append(
                    {
                        "prev_timestamp_utc": prev.isoformat(),
                        "next_timestamp_utc": current.isoformat(),
                        "delta_seconds": delta,
                        "missing_bars_estimate": int(delta / expected_step) - 1,
                    }
                )
    gap_path = bundle_root / "quality" / "gap_reports" / f"{dataset_id}_gaps.csv"
    duplicate_path = bundle_root / "quality" / "duplicate_timestamp_reports" / f"{dataset_id}_duplicates.csv"
    ohlcv_path = bundle_root / "quality" / "ohlcv_validation_reports" / f"{dataset_id}_ohlcv.md"
    write_csv(gap_path, gaps, ["prev_timestamp_utc", "next_timestamp_utc", "delta_seconds", "missing_bars_estimate"])
    write_csv(duplicate_path, duplicates, ["row", "timestamp_utc"])
    ohlcv_path.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if not invalid_rows else "FAIL"
    ohlcv_path.write_text(
        "\n".join(
            [
                f"# OHLCV Validation - {dataset_id}",
                "",
                f"- Status: `{status}`",
                f"- Invalid rows: `{len(invalid_rows)}`",
                f"- Duplicate timestamps: `{len(duplicates)}`",
                f"- Gaps: `{len(gaps)}`",
                "",
                "## First Invalid Rows",
                "",
                json.dumps(invalid_rows[:50], indent=2, sort_keys=True),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    expected_bars = None
    if expected_step and len(times) > 1:
        expected_bars = int((times[-1] - times[0]).total_seconds() / expected_step) + 1
    return {
        "has_gaps": bool(gaps),
        "gap_count": len(gaps),
        "gap_report_path": str(gap_path.relative_to(bundle_root)),
        "duplicate_timestamp_count": len(duplicates),
        "duplicate_report_path": str(duplicate_path.relative_to(bundle_root)),
        "ohlcv_validation_status": status,
        "ohlcv_report_path": str(ohlcv_path.relative_to(bundle_root)),
        "invalid_ohlcv_count": len(invalid_rows),
        "expected_bars": expected_bars,
    }


def regime_lookback(timeframe: str) -> int:
    return {"15m": 96, "1h": 72, "2h": 60, "4h": 42, "1D": 30}.get(timeframe, 50)


def classify_regimes(dataset_id: str, symbol: str, timeframe: str, rows: list[dict[str, Any]], output_path: Path) -> dict[str, Any]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lookback = regime_lookback(timeframe)
    closes = [float(row["close"]) for row in rows]
    highs = [float(row["high"]) for row in rows]
    lows = [float(row["low"]) for row in rows]
    regime_rows: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    for index, row in enumerate(rows):
        start = max(0, index - lookback + 1)
        close_window = closes[start : index + 1]
        high_window = highs[start : index + 1]
        low_window = lows[start : index + 1]
        if len(close_window) < max(5, min(lookback, 10)):
            regime = "CONSOLIDATING"
            rolling_volatility = 0.0
            trend_strength = 0.0
            range_compression = 1.0
            choppiness_score = 0.5
            confidence = 0.25
        else:
            returns = [
                (close_window[i] - close_window[i - 1]) / close_window[i - 1]
                for i in range(1, len(close_window))
                if close_window[i - 1] != 0
            ]
            mean_close = sum(close_window) / len(close_window)
            rolling_volatility = math.sqrt(sum((ret - (sum(returns) / len(returns))) ** 2 for ret in returns) / len(returns)) if returns else 0.0
            net_move = abs(close_window[-1] - close_window[0])
            path_move = sum(abs(close_window[i] - close_window[i - 1]) for i in range(1, len(close_window)))
            trend_strength = net_move / path_move if path_move else 0.0
            window_range = max(high_window) - min(low_window)
            range_compression = window_range / mean_close if mean_close else 0.0
            choppiness_score = 1.0 - trend_strength
            if trend_strength >= 0.42 and range_compression >= 0.025:
                regime = "TRENDING"
                confidence = min(1.0, trend_strength)
            elif range_compression <= 0.018 and rolling_volatility <= 0.006:
                regime = "CONSOLIDATING"
                confidence = min(1.0, 1.0 - range_compression)
            elif choppiness_score >= 0.82 and rolling_volatility >= 0.006:
                regime = "CHOPPY"
                confidence = min(1.0, choppiness_score)
            else:
                regime = "RANGING"
                confidence = max(0.35, min(0.85, choppiness_score))
        counts[regime] += 1
        regime_rows.append(
            {
                "timestamp_utc": row["timestamp_utc"],
                "dataset_id": dataset_id,
                "symbol": symbol,
                "timeframe": timeframe,
                "regime": regime,
                "confidence": round(confidence, 6),
                "rolling_volatility": round(rolling_volatility, 10),
                "trend_strength": round(trend_strength, 10),
                "range_compression": round(range_compression, 10),
                "choppiness_score": round(choppiness_score, 10),
                "method_version": METHOD_VERSION,
            }
        )
    write_csv(
        output_path,
        regime_rows,
        [
            "timestamp_utc",
            "dataset_id",
            "symbol",
            "timeframe",
            "regime",
            "confidence",
            "rolling_volatility",
            "trend_strength",
            "range_compression",
            "choppiness_score",
            "method_version",
        ],
    )
    return {"regime_file": str(output_path), "counts": dict(counts), "rows": len(regime_rows)}


def safe_copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def build_bundle(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root)
    parent_root = Path(args.bundle_parent)
    bundle_name = f"MTC_V2_OPTIMIZATION_DATA_BUNDLE_{args.date_token}"
    bundle_root = parent_root / bundle_name
    if bundle_root.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        bundle_root.rename(parent_root / f"{bundle_name}_previous_{timestamp}")
    zip_path = parent_root / f"{bundle_name}.zip"
    if zip_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_path.rename(parent_root / f"{bundle_name}_previous_{timestamp}.zip")
    sha_path = parent_root / f"{bundle_name}.zip.sha256"
    if sha_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sha_path.rename(parent_root / f"{bundle_name}_previous_{timestamp}.zip.sha256")
    for sub in [
        "raw/binance_futures",
        "normalized/binance_futures",
        "manifests",
        "regimes/per_dataset",
        "quality/gap_reports",
        "quality/duplicate_timestamp_reports",
        "quality/ohlcv_validation_reports",
        "docs",
    ]:
        (bundle_root / sub).mkdir(parents=True, exist_ok=True)

    discovery_roots = [Path(args.archive_root), Path(args.datasets_root), repo_root / "reports" / "data_downloads"]
    csv_files: list[Path] = []
    for root in discovery_roots:
        if root.exists():
            csv_files.extend(sorted(root.rglob("*.csv")))
    source_files = [inspect_source_file(path) for path in sorted(set(csv_files))]
    discovery_rows = [
        {
            "source_path": str(item.source_path),
            "symbol": item.symbol,
            "exchange": item.exchange,
            "timeframe": item.timeframe,
            "source_type": item.source_type,
            "row_count": item.row_count,
            "first_timestamp": item.first_timestamp,
            "last_timestamp": item.last_timestamp,
            "columns": "|".join(item.columns),
            "sha256": item.sha256,
            "size_bytes": item.size_bytes,
            "include_candidate": item.include_candidate,
            "skip_reason": item.skip_reason,
        }
        for item in source_files
    ]
    report_root = repo_root / "reports" / "optimization_data_bundle"
    report_root.mkdir(parents=True, exist_ok=True)
    write_csv(report_root / "source_file_discovery.csv", discovery_rows)

    included = [item for item in source_files if item.include_candidate]
    used_ids: set[str] = set()
    manifests: list[dict[str, Any]] = []
    source_index: list[dict[str, Any]] = []
    quality_summaries: list[dict[str, Any]] = []
    regime_registry: list[dict[str, Any]] = []
    total_rows = 0
    for source in included:
        dataset_id = dataset_id_for(source, used_ids)
        raw_dst = bundle_root / "raw" / "binance_futures" / source.symbol / source.timeframe / source.source_path.name
        safe_copy(source.source_path, raw_dst)
        rows, columns = read_rows(source.source_path)
        normalized_rows, normalize_notes = normalize_rows(rows, columns)
        normalized_dst = bundle_root / "normalized" / "binance_futures" / source.symbol / source.timeframe / f"{dataset_id}.csv"
        normalized_fields = ["timestamp_utc", "open", "high", "low", "close"]
        if normalize_notes["volume"] == "present":
            normalized_fields.append("volume")
        write_csv(normalized_dst, normalized_rows, normalized_fields)
        quality = validate_quality(dataset_id, normalized_rows, source.timeframe, bundle_root)
        regime_rel = Path("regimes") / "per_dataset" / f"{dataset_id}_regimes.csv"
        regime = classify_regimes(dataset_id, source.symbol, source.timeframe, normalized_rows, bundle_root / regime_rel)
        total_rows += len(normalized_rows)
        manifest = {
            "dataset_id": dataset_id,
            "symbol": source.symbol,
            "exchange": source.exchange,
            "timeframe": source.timeframe,
            "timeframe_normalized": source.timeframe,
            "source_type": source.source_type,
            "raw_path": str(raw_dst.relative_to(bundle_root)),
            "normalized_path": str(normalized_dst.relative_to(bundle_root)),
            "start": source.first_timestamp,
            "end": source.last_timestamp,
            "timezone": "UTC",
            "row_count": len(normalized_rows),
            "sha256_raw": sha256_file(raw_dst),
            "sha256_normalized": sha256_file(normalized_dst),
            "file_size_bytes": raw_dst.stat().st_size,
            "has_gaps": quality["has_gaps"],
            "gap_report_path": quality["gap_report_path"],
            "duplicate_timestamp_count": quality["duplicate_timestamp_count"],
            "ohlcv_validation_status": quality["ohlcv_validation_status"],
            "regime_file": str(regime_rel).replace("\\", "/"),
            "notes": f"volume={normalize_notes['volume']}; expected_bars={quality['expected_bars']}",
        }
        manifests.append(manifest)
        quality_summaries.append({**quality, "dataset_id": dataset_id, "symbol": source.symbol, "timeframe": source.timeframe, "row_count": len(normalized_rows)})
        regime_registry.append({"dataset_id": dataset_id, "symbol": source.symbol, "timeframe": source.timeframe, "regime_file": str(regime_rel).replace("\\", "/"), **regime})
        source_index.append(
            {
                "dataset_id": dataset_id,
                "source_path": str(source.source_path),
                "raw_path": manifest["raw_path"],
                "normalized_path": manifest["normalized_path"],
                "source_type": source.source_type,
                "sha256_raw": manifest["sha256_raw"],
                "sha256_normalized": manifest["sha256_normalized"],
            }
        )

    manifest_payload = {"created_at": datetime.now(timezone.utc).isoformat(), "datasets": manifests}
    write_json(bundle_root / "manifests" / "dataset_manifest.json", manifest_payload)
    write_simple_yaml(bundle_root / "manifests" / "dataset_manifest.yml", manifest_payload)
    write_json(bundle_root / "DATA_BUNDLE_MANIFEST.json", manifest_payload)
    write_simple_yaml(bundle_root / "DATA_BUNDLE_MANIFEST.yml", manifest_payload)
    write_csv(bundle_root / "manifests" / "source_file_index.csv", source_index)
    (bundle_root / "manifests" / "selected_dataset_ids.txt").write_text("\n".join(item["dataset_id"] for item in manifests) + "\n", encoding="utf-8")
    regime_payload = {"method_version": METHOD_VERSION, "datasets": regime_registry}
    write_json(bundle_root / "regimes" / "regime_registry.json", regime_payload)
    write_simple_yaml(bundle_root / "regimes" / "regime_registry.yml", regime_payload)
    write_json(bundle_root / "quality" / "DATA_QUALITY_SUMMARY.json", {"datasets": quality_summaries})

    source_counts = Counter(item.source_type for item in included)
    symbols_included = sorted({item["symbol"] for item in manifests})
    timeframes_included = sorted({item["timeframe"] for item in manifests}, key=lambda tf: EXPECTED_TIMEFRAMES.index(tf) if tf in EXPECTED_TIMEFRAMES else 99)
    missing = [
        {"symbol": symbol, "timeframe": timeframe}
        for symbol in EXPECTED_SYMBOLS
        for timeframe in EXPECTED_TIMEFRAMES
        if not any(item["symbol"] == symbol and item["timeframe"] == timeframe for item in manifests)
    ]
    quality_lines = [
        "# Data Quality Summary",
        "",
        f"- Dataset count: `{len(manifests)}`",
        f"- Total normalized rows: `{total_rows}`",
        f"- Datasets with gaps: `{sum(1 for item in quality_summaries if item['has_gaps'])}`",
        f"- Datasets with duplicate timestamps: `{sum(1 for item in quality_summaries if item['duplicate_timestamp_count'])}`",
        f"- Datasets with OHLCV validation failure: `{sum(1 for item in quality_summaries if item['ohlcv_validation_status'] != 'PASS')}`",
    ]
    (bundle_root / "quality" / "DATA_QUALITY_SUMMARY.md").write_text("\n".join(quality_lines) + "\n", encoding="utf-8")
    (bundle_root / "README_DATASET_USAGE.md").write_text(readme_text(bundle_name), encoding="utf-8")
    (bundle_root / "docs" / "DATA_SOURCE_RULES.md").write_text(data_source_rules_text(), encoding="utf-8")
    (bundle_root / "docs" / "OPTIMIZER_DATA_USAGE_RULES.md").write_text(optimizer_rules_text(), encoding="utf-8")
    (bundle_root / "docs" / "REGIME_CLASSIFICATION_METHOD.md").write_text(regime_method_text(), encoding="utf-8")
    (bundle_root / "BUNDLE_CREATION_REPORT.md").write_text(bundle_report_text(bundle_root, zip_path, manifests, source_files, missing, total_rows, source_counts), encoding="utf-8")
    discovery_report = discovery_report_text(source_files)
    (report_root / "DATA_SOURCE_DISCOVERY_REPORT.md").write_text(discovery_report, encoding="utf-8")

    write_hashes(bundle_root)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
        for path in sorted(bundle_root.rglob("*")):
            if path.is_file():
                zipf.write(path, arcname=str(Path(bundle_name) / path.relative_to(bundle_root)))
    zip_sha = sha256_file(zip_path)
    sha_path.write_text(f"{zip_sha}  {zip_path.name}\n", encoding="utf-8")
    forbidden = verify_zip_forbidden(zip_path)
    final_payload = {
        "bundle_root": str(bundle_root),
        "zip_path": str(zip_path),
        "zip_sha256": zip_sha,
        "symbols": symbols_included,
        "timeframes": timeframes_included,
        "dataset_count": len(manifests),
        "total_rows": total_rows,
        "total_size_bytes": sum(path.stat().st_size for path in bundle_root.rglob("*") if path.is_file()),
        "source_types": dict(source_counts),
        "missing": missing,
        "forbidden_zip_entries": forbidden,
        "verdict": "OPTIMIZATION_DATA_BUNDLE_READY" if not forbidden and manifests else "OPTIMIZATION_DATA_BUNDLE_READY_WITH_WARNINGS",
    }
    final_report = final_report_text(final_payload, source_files, quality_summaries, regime_registry)
    (report_root / "OPTIMIZATION_DATA_BUNDLE_CREATION_REPORT.md").write_text(final_report, encoding="utf-8")
    write_json(report_root / "OPTIMIZATION_DATA_BUNDLE_CREATION_REPORT.json", final_payload)
    return final_payload


def readme_text(bundle_name: str) -> str:
    return f"""# MTC V2 Optimization Data Bundle

Bundle: `{bundle_name}`

This bundle is for broad optimization and cross-market validation only. It is not a final TradingView parity/audit dataset.

Use `manifests/dataset_manifest.json` or `manifests/dataset_manifest.yml` and reference data by `dataset_id`. Do not hardcode CSV paths in optimizer jobs.

Always verify `sha256_raw` and `sha256_normalized` before running optimization.

Regime files under `regimes/per_dataset/` can be joined by `dataset_id` and `timestamp_utc` to evaluate strategy behavior in `TRENDING`, `RANGING`, `CONSOLIDATING`, and `CHOPPY` conditions.

To add future symbols or timeframes, add source CSVs under the archive/data source folder, rerun the bundle builder, and consume the new manifest.

Source type meanings:
- `binance_public_futures_klines`: Binance USD-M Futures public kline API data.
- `tradingview_chart_csv_binance`: TradingView chart CSV data for Binance symbols.
- `unknown_csv` / `not_chart_data`: discovered but skipped.
"""


def data_source_rules_text() -> str:
    return """# Data Source Rules

- Do not mix sources without preserving `source_type`.
- Binance public futures klines are acceptable for broad optimization research.
- TradingView chart CSVs are acceptable for chart-data experiments but are not Strategy Tester audit workbooks.
- TradingView Strategy Tester XLSX files must not be included in this bundle.
- This bundle must not contain API keys, `.env` files, `.git`, virtual environments, or generated optimization result folders.
"""


def optimizer_rules_text() -> str:
    return """# Optimizer Data Usage Rules

- Load datasets through the manifest, not hardcoded paths.
- Verify SHA256 before each run.
- Preserve `dataset_id`, `source_type`, `symbol`, `timeframe`, and `sha256` in every result row.
- Treat this bundle as research data only.
- Do not claim live profitability or final TradingView parity from these files.
"""


def regime_method_text() -> str:
    return f"""# Regime Classification Method

Method version: `{METHOD_VERSION}`

The classifier is deterministic and rule-based. It uses only historical rolling windows ending at the current bar, so it does not use future leakage.

Features:
- rolling return path efficiency as `trend_strength`
- rolling return volatility
- rolling high/low range compression
- choppiness proxy as `1 - trend_strength`

Regimes:
- `TRENDING`: strong directional movement over the rolling window.
- `RANGING`: moderate choppiness without compressed range.
- `CONSOLIDATING`: compressed range and low rolling volatility.
- `CHOPPY`: high choppiness with elevated volatility.

Limitations:
- This is an initial research label, not market truth.
- Thresholds should be calibrated after joining backtest results by regime.
- Labels are intended for robustness diagnostics, not signal generation.
"""


def write_hashes(bundle_root: Path) -> None:
    hash_path = bundle_root / "FILE_HASHES.sha256"
    rows = []
    for path in sorted(bundle_root.rglob("*")):
        if path.is_file() and path.name != "FILE_HASHES.sha256":
            rows.append(f"{sha256_file(path)}  {path.relative_to(bundle_root).as_posix()}")
    hash_path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def verify_zip_forbidden(zip_path: Path) -> list[str]:
    forbidden_fragments = [".git/", ".venv/", "node_modules/", "__pycache__/", ".pytest_cache/", "reports/optimization"]
    forbidden_suffixes = [".xlsx", ".env"]
    bad: list[str] = []
    with zipfile.ZipFile(zip_path, "r") as zipf:
        for name in zipf.namelist():
            normalized = name.replace("\\", "/")
            lower = normalized.lower()
            if any(fragment in lower for fragment in forbidden_fragments) or any(lower.endswith(suffix) for suffix in forbidden_suffixes):
                bad.append(normalized)
    return bad


def discovery_report_text(source_files: list[SourceFile]) -> str:
    included = [item for item in source_files if item.include_candidate]
    skipped = [item for item in source_files if not item.include_candidate]
    lines = [
        "# Data Source Discovery Report",
        "",
        f"- CSV files discovered: `{len(source_files)}`",
        f"- Included candidates: `{len(included)}`",
        f"- Skipped files: `{len(skipped)}`",
        "",
        "## Skipped Files",
        "",
    ]
    for item in skipped[:200]:
        lines.append(f"- `{item.source_path}`: `{item.skip_reason}`")
    return "\n".join(lines) + "\n"


def bundle_report_text(bundle_root: Path, zip_path: Path, manifests: list[dict[str, Any]], source_files: list[SourceFile], missing: list[dict[str, str]], total_rows: int, source_counts: Counter[str]) -> str:
    symbols = sorted({item["symbol"] for item in manifests})
    timeframes = sorted({item["timeframe"] for item in manifests}, key=lambda tf: EXPECTED_TIMEFRAMES.index(tf) if tf in EXPECTED_TIMEFRAMES else 99)
    return "\n".join(
        [
            "# Bundle Creation Report",
            "",
            f"- Bundle folder: `{bundle_root}`",
            f"- Zip path: `{zip_path}`",
            f"- Dataset count: `{len(manifests)}`",
            f"- Total rows: `{total_rows}`",
            f"- Symbols: `{', '.join(symbols)}`",
            f"- Timeframes: `{', '.join(timeframes)}`",
            f"- Source types: `{dict(source_counts)}`",
            f"- Missing expected symbol/timeframe pairs: `{len(missing)}`",
            f"- Discovered CSV files: `{len(source_files)}`",
        ]
    ) + "\n"


def final_report_text(payload: dict[str, Any], source_files: list[SourceFile], quality_summaries: list[dict[str, Any]], regime_registry: list[dict[str, Any]]) -> str:
    skipped = [item for item in source_files if not item.include_candidate]
    gap_count = sum(1 for item in quality_summaries if item["has_gaps"])
    duplicate_count = sum(1 for item in quality_summaries if item["duplicate_timestamp_count"])
    ohlcv_fail_count = sum(1 for item in quality_summaries if item["ohlcv_validation_status"] != "PASS")
    regime_counts: Counter[str] = Counter()
    for item in regime_registry:
        regime_counts.update(item.get("counts", {}))
    lines = [
        "# Optimization Data Bundle Creation Report",
        "",
        f"## A. Executive summary\nVerdict: `{payload['verdict']}`. Bundle created for optimization research and cross-market validation.",
        f"## B. Bundle folder path\n`{payload['bundle_root']}`",
        f"## C. Zip path\n`{payload['zip_path']}`",
        f"## D. Zip SHA256\n`{payload['zip_sha256']}`",
        f"## E. Symbols included\n`{', '.join(payload['symbols'])}`",
        f"## F. Timeframes included\n`{', '.join(payload['timeframes'])}`",
        f"## G. Missing expected symbols/timeframes\n`{len(payload['missing'])}` missing pairs. See JSON report for full list.",
        f"## H. Dataset count\n`{payload['dataset_count']}`",
        f"## I. Total row count\n`{payload['total_rows']}`",
        f"## J. Total size\n`{payload['total_size_bytes']}` bytes inside bundle folder.",
        f"## K. Data source types\n`{payload['source_types']}`",
        f"## L. Quality check summary\nDatasets with gaps: `{gap_count}`. Datasets with duplicates: `{duplicate_count}`. OHLCV failures: `{ohlcv_fail_count}`.",
        f"## M. Regime classification summary\n`{dict(regime_counts)}`",
        f"## N. Skipped files\n`{len(skipped)}` skipped. See `source_file_discovery.csv`.",
        f"## O. Warnings\nForbidden zip entries: `{len(payload['forbidden_zip_entries'])}`. Single-source limitations remain source-labeled.",
        "## P. How optimizer should use this bundle\nUse manifest dataset IDs, verify SHA256, preserve source_type in results, and join regime CSVs by timestamp for robustness diagnostics.",
        "## Q. Next prompt recommendation\n`Use MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427/manifests/dataset_manifest.json to run a 5-evaluation resume smoke, then run a small multi-asset walk-forward pilot with coverage-aware scoring.`",
    ]
    return "\n\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2")
    parser.add_argument("--bundle-parent", default=r"C:\LAB\tradingview-lab")
    parser.add_argument("--archive-root", default=r"C:\LAB\tradingview-lab\mtc_backtest\parity_suite_350\tv_manual_inputs\raw_tv_exports\ARŞİV")
    parser.add_argument("--datasets-root", default=r"C:\LAB\tradingview-lab\mtc_backtest\datasets")
    parser.add_argument("--date-token", default="20260427")
    args = parser.parse_args()
    payload = build_bundle(args)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
