from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TARGET_TIMEFRAMES = {"15": "15m", "60": "1h", "120": "2h", "240": "4h", "1D": "1D"}


@dataclass(frozen=True)
class Bar:
    time: int
    open: float
    high: float
    low: float
    close: float


@dataclass(frozen=True)
class SegmentMetrics:
    dataset_id: str
    source_path: str
    symbol: str
    timeframe: str
    segment_id: str
    start_time: int
    end_time: int
    row_count: int
    return_pct: float
    abs_return_pct: float
    atr_pct: float
    range_pct: float
    efficiency_ratio: float
    choppiness_index: float
    label: str
    trend_direction: str
    classification_reason: str


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def iso_utc(epoch_seconds: int) -> str:
    return datetime.fromtimestamp(epoch_seconds, timezone.utc).isoformat()


def infer_symbol_timeframe(path: Path) -> tuple[str, str]:
    name = path.stem
    symbol = "UNKNOWN"
    timeframe = "UNKNOWN"
    if name.startswith("BINANCE_"):
        after_exchange = name[len("BINANCE_") :]
        if "," in after_exchange:
            symbol_part, tf_part = after_exchange.split(",", 1)
            symbol = symbol_part.strip()
            tf_token = tf_part.strip().split("_", 1)[0].strip()
            timeframe = TARGET_TIMEFRAMES.get(tf_token, tf_token)
    return symbol, timeframe


def dataset_id_for(path: Path) -> str:
    digest = hashlib.sha1(str(path).encode("utf-8")).hexdigest()[:10]
    symbol, timeframe = infer_symbol_timeframe(path)
    safe_symbol = symbol.replace(".", "_").replace("/", "_")
    safe_tf = timeframe.replace("/", "_")
    return f"{safe_symbol}_{safe_tf}_{digest}"


def parse_time(value: str) -> int:
    value = value.strip()
    if value.isdigit():
        raw = int(value)
        return raw // 1000 if raw > 10_000_000_000 else raw
    normalized = value.replace("Z", "+00:00")
    return int(datetime.fromisoformat(normalized).timestamp())


def read_bars(path: Path) -> list[Bar]:
    bars: list[Bar] = []
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            return bars
        columns = {name.lower().strip(): name for name in reader.fieldnames}
        required = ["time", "open", "high", "low", "close"]
        if not all(column in columns for column in required):
            return bars
        for row in reader:
            try:
                bars.append(
                    Bar(
                        time=parse_time(row[columns["time"]]),
                        open=float(row[columns["open"]]),
                        high=float(row[columns["high"]]),
                        low=float(row[columns["low"]]),
                        close=float(row[columns["close"]]),
                    )
                )
            except (TypeError, ValueError):
                continue
    dedup = {bar.time: bar for bar in bars if bar.high >= bar.low and bar.close > 0}
    return [dedup[key] for key in sorted(dedup)]


def true_ranges(bars: list[Bar]) -> list[float]:
    ranges: list[float] = []
    previous_close = bars[0].close
    for bar in bars:
        ranges.append(max(bar.high - bar.low, abs(bar.high - previous_close), abs(bar.low - previous_close)))
        previous_close = bar.close
    return ranges


def quantile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = min(len(ordered) - 1, max(0, int(round((len(ordered) - 1) * q))))
    return ordered[idx]


def compute_segment_metrics(
    dataset_id: str,
    source_path: Path,
    symbol: str,
    timeframe: str,
    segment_index: int,
    bars: list[Bar],
) -> dict[str, Any]:
    closes = [bar.close for bar in bars]
    highs = [bar.high for bar in bars]
    lows = [bar.low for bar in bars]
    trs = true_ranges(bars)
    mean_close = statistics.fmean(closes)
    total_path = sum(abs(closes[idx] - closes[idx - 1]) for idx in range(1, len(closes)))
    net_move = closes[-1] - closes[0]
    price_range = max(highs) - min(lows)
    atr = statistics.fmean(trs)
    efficiency = abs(net_move) / total_path if total_path > 0 else 0.0
    choppiness = 100.0
    if price_range > 0 and len(bars) > 1:
        choppiness = 100.0 * math.log10(max(sum(trs), 1e-12) / price_range) / math.log10(len(bars))
    return {
        "dataset_id": dataset_id,
        "source_path": str(source_path),
        "symbol": symbol,
        "timeframe": timeframe,
        "segment_id": f"{dataset_id}_seg_{segment_index:05d}",
        "start_time": bars[0].time,
        "end_time": bars[-1].time,
        "row_count": len(bars),
        "return_pct": (net_move / bars[0].close) * 100.0 if bars[0].close else 0.0,
        "abs_return_pct": abs(net_move / bars[0].close) * 100.0 if bars[0].close else 0.0,
        "atr_pct": (atr / mean_close) * 100.0 if mean_close else 0.0,
        "range_pct": (price_range / mean_close) * 100.0 if mean_close else 0.0,
        "efficiency_ratio": efficiency,
        "choppiness_index": choppiness,
    }


def label_segments(raw_segments: list[dict[str, Any]]) -> list[SegmentMetrics]:
    atr_values = [float(row["atr_pct"]) for row in raw_segments]
    range_values = [float(row["range_pct"]) for row in raw_segments]
    abs_return_values = [float(row["abs_return_pct"]) for row in raw_segments]
    atr_low = quantile(atr_values, 0.33)
    atr_high = quantile(atr_values, 0.66)
    range_low = quantile(range_values, 0.33)
    abs_return_high = quantile(abs_return_values, 0.66)
    labeled = []
    for row in raw_segments:
        efficiency = float(row["efficiency_ratio"])
        choppiness = float(row["choppiness_index"])
        atr_pct = float(row["atr_pct"])
        range_pct = float(row["range_pct"])
        abs_return_pct = float(row["abs_return_pct"])
        return_pct = float(row["return_pct"])
        direction = "UP" if return_pct > 0 else "DOWN" if return_pct < 0 else "FLAT"
        if efficiency >= 0.32 and abs_return_pct >= abs_return_high and choppiness <= 58.0:
            label = "TRENDING"
            reason = "high_efficiency_high_net_move"
        elif atr_pct <= atr_low and range_pct <= range_low:
            label = "CONSOLIDATING"
            reason = "low_atr_low_range"
        elif efficiency <= 0.16 and choppiness >= 61.8 and atr_pct >= atr_high:
            label = "CHOPPY"
            reason = "low_efficiency_high_choppiness_high_atr"
        elif efficiency <= 0.22 and abs_return_pct < abs_return_high:
            label = "RANGING_SIDEWAYS"
            reason = "low_efficiency_limited_net_move"
        else:
            label = "MIXED_TRANSITION"
            reason = "thresholds_mixed"
        labeled.append(
            SegmentMetrics(
                dataset_id=str(row["dataset_id"]),
                source_path=str(row["source_path"]),
                symbol=str(row["symbol"]),
                timeframe=str(row["timeframe"]),
                segment_id=str(row["segment_id"]),
                start_time=int(row["start_time"]),
                end_time=int(row["end_time"]),
                row_count=int(row["row_count"]),
                return_pct=return_pct,
                abs_return_pct=abs_return_pct,
                atr_pct=atr_pct,
                range_pct=range_pct,
                efficiency_ratio=efficiency,
                choppiness_index=choppiness,
                label=label,
                trend_direction=direction,
                classification_reason=reason,
            )
        )
    return labeled


def segment_size_for(timeframe: str) -> int:
    if timeframe == "15m":
        return 672
    if timeframe == "1h":
        return 336
    if timeframe == "2h":
        return 252
    if timeframe == "4h":
        return 168
    if timeframe == "1D":
        return 90
    return 250


def classify_file(path: Path) -> tuple[dict[str, Any], list[SegmentMetrics]]:
    dataset_id = dataset_id_for(path)
    symbol, timeframe = infer_symbol_timeframe(path)
    bars = read_bars(path)
    file_summary: dict[str, Any] = {
        "dataset_id": dataset_id,
        "source_path": str(path),
        "symbol": symbol,
        "timeframe": timeframe,
        "row_count": len(bars),
        "sha256": sha256_file(path),
        "start": iso_utc(bars[0].time) if bars else None,
        "end": iso_utc(bars[-1].time) if bars else None,
        "usable": len(bars) >= 200,
        "skip_reason": "" if len(bars) >= 200 else "too_few_rows_or_bad_columns",
    }
    if len(bars) < 200:
        return file_summary, []
    segment_size = segment_size_for(timeframe)
    step = max(50, segment_size // 2)
    raw_segments = []
    segment_index = 1
    for start in range(0, max(1, len(bars) - segment_size + 1), step):
        window = bars[start : start + segment_size]
        if len(window) < max(80, segment_size // 2):
            continue
        raw_segments.append(compute_segment_metrics(dataset_id, path, symbol, timeframe, segment_index, window))
        segment_index += 1
    segments = label_segments(raw_segments)
    counts = Counter(segment.label for segment in segments)
    file_summary.update(
        {
            "segment_count": len(segments),
            "trending_segments": counts.get("TRENDING", 0),
            "ranging_sideways_segments": counts.get("RANGING_SIDEWAYS", 0),
            "consolidating_segments": counts.get("CONSOLIDATING", 0),
            "choppy_segments": counts.get("CHOPPY", 0),
            "mixed_transition_segments": counts.get("MIXED_TRANSITION", 0),
        }
    )
    return file_summary, segments


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--pattern", default="BINANCE_*.csv")
    args = parser.parse_args()

    archive_dir = Path(args.archive_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    file_summaries: list[dict[str, Any]] = []
    all_segments: list[SegmentMetrics] = []
    failures: list[dict[str, Any]] = []
    for path in sorted(archive_dir.glob(args.pattern)):
        try:
            summary, segments = classify_file(path)
            file_summaries.append(summary)
            all_segments.extend(segments)
            print(f"ok {path.name} segments={len(segments)}")
        except Exception as exc:
            failures.append({"source_path": str(path), "error": str(exc)})
            print(f"fail {path.name}: {exc}")

    segment_rows = [
        {
            **segment.__dict__,
            "start": iso_utc(segment.start_time),
            "end": iso_utc(segment.end_time),
        }
        for segment in all_segments
    ]
    segment_fields = [
        "dataset_id",
        "source_path",
        "symbol",
        "timeframe",
        "segment_id",
        "start_time",
        "end_time",
        "start",
        "end",
        "row_count",
        "return_pct",
        "abs_return_pct",
        "atr_pct",
        "range_pct",
        "efficiency_ratio",
        "choppiness_index",
        "label",
        "trend_direction",
        "classification_reason",
    ]
    summary_fields = [
        "dataset_id",
        "source_path",
        "symbol",
        "timeframe",
        "row_count",
        "start",
        "end",
        "sha256",
        "usable",
        "skip_reason",
        "segment_count",
        "trending_segments",
        "ranging_sideways_segments",
        "consolidating_segments",
        "choppy_segments",
        "mixed_transition_segments",
    ]
    write_csv(out_dir / "market_regime_segments.csv", segment_rows, segment_fields)
    write_csv(out_dir / "per_dataset_regime_summary.csv", file_summaries, summary_fields)

    label_counts = Counter(segment.label for segment in all_segments)
    by_timeframe: dict[str, Counter[str]] = defaultdict(Counter)
    by_symbol: dict[str, Counter[str]] = defaultdict(Counter)
    for segment in all_segments:
        by_timeframe[segment.timeframe][segment.label] += 1
        by_symbol[segment.symbol][segment.label] += 1
    payload = {
        "archive_dir": str(archive_dir),
        "file_count": len(file_summaries),
        "segment_count": len(all_segments),
        "label_counts": dict(label_counts),
        "by_timeframe": {key: dict(value) for key, value in sorted(by_timeframe.items())},
        "by_symbol": {key: dict(value) for key, value in sorted(by_symbol.items())},
        "failures": failures,
    }
    (out_dir / "market_regime_summary.json").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    lines = [
        "# Market Regime Classification Report",
        "",
        f"- Archive: `{archive_dir}`",
        f"- Files classified: {len(file_summaries)}",
        f"- Segments classified: {len(all_segments)}",
        f"- Failures: {len(failures)}",
        "",
        "## Labels",
        "",
        "- `TRENDING`: high directional efficiency and high net movement.",
        "- `RANGING_SIDEWAYS`: low directional efficiency with limited net movement.",
        "- `CONSOLIDATING`: low ATR and low price range versus that dataset's own segments.",
        "- `CHOPPY`: low efficiency, high choppiness, high ATR.",
        "- `MIXED_TRANSITION`: no strong regime match; transition/noisy hybrid.",
        "",
        "## Label Counts",
        "",
    ]
    for label, count in sorted(label_counts.items()):
        lines.append(f"- {label}: {count}")
    lines.extend(["", "## Use In Backtests", ""])
    lines.append(
        "Backtest trade rows can be joined to `market_regime_segments.csv` by `symbol`, `timeframe`, "
        "and entry/exit timestamp to summarize PnL, win rate, drawdown, and trade count per regime."
    )
    if failures:
        lines.extend(["", "## Failures", ""])
        for failure in failures:
            lines.append(f"- `{failure['source_path']}`: {failure['error']}")
    (out_dir / "MARKET_REGIME_CLASSIFICATION_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
