from __future__ import annotations

import argparse
import csv
import json
import shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RESEARCH_WARNING = "Research seed only; not Pine default; not production parameter."
REQUIRED_COLUMNS = {
    "strategy_id",
    "producer_id",
    "asset",
    "symbol",
    "timeframe",
    "rank",
    "parameter_set_id",
    "parameter_hash",
    "source_run_id",
    "source_output_path",
    "st_factor",
    "global_atr_length",
    "sl_atr_mult",
    "tp_mode",
    "tp_r_multiple",
    "risk_long",
    "risk_short",
    "status",
    "confidence",
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def read_csv(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row.keys()}) if rows else ["status"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def backup(path: Path) -> Path | None:
    if not path.exists():
        return None
    backup_path = path.with_name(f"{path.stem}.backup_{utc_stamp()}{path.suffix}")
    shutil.copy2(path, backup_path)
    return backup_path


def numeric_values(rows: list[dict[str, Any]], key: str) -> list[float]:
    values = []
    for row in rows:
        try:
            value = row.get(key)
            if value not in ("", None):
                values.append(float(value))
        except (TypeError, ValueError):
            pass
    return values


def yaml_scalar(value: Any) -> str:
    if value in ("", None):
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value))


def write_seed_regions(path: Path, rows: list[dict[str, Any]], producer: str) -> None:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if str(row.get("seed_source_type")) == "SMOKE_ASSET_TIMEFRAME_SEED":
            grouped[(str(row.get("asset")), str(row.get("timeframe")))].append(row)

    lines = [
        "# Supertrend Seed Regions",
        RESEARCH_WARNING,
        "",
        "regions:",
    ]
    if not grouped:
        lines += [
            "  - region_id: no_asset_timeframe_smoke_regions",
            "    accepted_for_next_stage: false",
            "    rejected_reason: NO_GRANULAR_ROWS",
            "    warnings:",
            f"      - {RESEARCH_WARNING}",
        ]
    for (asset, timeframe), group_rows in sorted(grouped.items()):
        region_id = f"{producer.lower()}_{asset}_{timeframe}_smoke_region_v1".replace("/", "_")
        lines += [
            f"  - region_id: {region_id}",
            "    strategy_id: MTC_V2",
            f"    producer_id: {producer}",
            f"    asset: {asset}",
            f"    timeframe: {timeframe}",
            "    confidence: LOW",
            f"    evidence_count: {len(group_rows)}",
            "    accepted_for_next_stage: true",
            "    seed_source_type: SMOKE_ASSET_TIMEFRAME_SEED",
            f"    warning: {RESEARCH_WARNING}",
            "    parameter_ranges:",
        ]
        for key in ["st_factor", "global_atr_length", "sl_atr_mult", "tp_r_multiple", "risk_long", "risk_short"]:
            values = numeric_values(group_rows, key)
            if values:
                lines += [
                    f"      {key}:",
                    f"        observed_values: {sorted(set(values))}",
                    f"        min: {min(values)}",
                    f"        max: {max(values)}",
                ]
        modes = sorted({str(row.get("tp_mode")) for row in group_rows if row.get("tp_mode")})
        lines += ["      tp_mode:", f"        observed_values: {modes}", "    center_params:"]
        top = sorted(group_rows, key=lambda row: int(float(row.get("rank") or 999)))[0]
        for key in ["st_factor", "global_atr_length", "sl_atr_mult", "tp_mode", "tp_r_multiple", "risk_long", "risk_short"]:
            lines.append(f"      {key}: {yaml_scalar(top.get(key))}")
        lines += [
            "    warnings:",
            f"      - {RESEARCH_WARNING}",
            "      - Smoke seeds prove schema/pipeline only; not final optimization conclusions.",
        ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_rejected(path: Path, rows: list[dict[str, Any]]) -> None:
    rejected = [row for row in rows if str(row.get("status")) in {"REJECTED", "INSUFFICIENT_DATA"}]
    lines = [
        "# Supertrend Rejected Regions",
        RESEARCH_WARNING,
        "",
        "rejected_or_caution_regions:",
        "  - region_id: smoke_schema_only_warning",
        "    type: caution",
        "    reason: Smoke-derived rows validate pipeline/schema only and are not final parameter conclusions.",
        "    action: Run real producer-only staged optimization before exit/filter refinement.",
    ]
    for row in rejected[:20]:
        lines += [
            f"  - region_id: rejected_{row.get('symbol')}_{row.get('timeframe')}_{row.get('parameter_hash')}",
            "    type: rejected_smoke_seed",
            f"    reason: {row.get('status')}",
            f"    asset: {row.get('asset')}",
            f"    timeframe: {row.get('timeframe')}",
        ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(path: Path, rows: list[dict[str, Any]], backups: list[Path], input_path: Path, producer: str) -> None:
    by_type = Counter(str(row.get("seed_source_type")) for row in rows)
    asset_timeframes = sorted({f"{row.get('asset')}:{row.get('timeframe')}" for row in rows if row.get("seed_source_type") == "SMOKE_ASSET_TIMEFRAME_SEED"})
    lines = [
        "# Supertrend Extraction Report",
        "",
        RESEARCH_WARNING,
        "",
        "## Source",
        "",
        f"- Input granular seed file: `{input_path}`",
        f"- Producer: `{producer}`",
        "",
        "## Backup Files",
        "",
    ]
    lines += [f"- `{item}`" for item in backups] if backups else ["- None needed."]
    lines += [
        "",
        "## Seed Source Types",
        "",
    ]
    lines += [f"- `{key}`: `{value}`" for key, value in sorted(by_type.items())]
    lines += [
        "",
        "## Asset/Timeframe Rows",
        "",
    ]
    lines += [f"- `{value}`" for value in asset_timeframes] if asset_timeframes else ["- None."]
    lines += [
        "",
        "## Warnings",
        "",
        "- Smoke-derived rows are `SMOKE_ASSET_TIMEFRAME_SEED` and confidence LOW.",
        "- Aggregate big-run rows are preserved as `AGGREGATE_MEDIUM_SEED`.",
        "- No row is a Pine default or production parameter.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--producer", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--top-n", type=int, default=5)
    args = parser.parse_args()

    input_path = Path(args.input)
    out = Path(args.out)
    rows = read_csv(input_path)
    if not rows:
        raise SystemExit(f"input has no rows: {input_path}")
    missing = sorted(REQUIRED_COLUMNS - set(rows[0].keys()))
    if missing:
        raise SystemExit(f"missing required columns: {missing}")

    best_path = out / f"{args.producer.lower()}_best_by_asset_timeframe.csv"
    region_path = out / f"{args.producer.lower()}_seed_regions.yml"
    rejected_path = out / f"{args.producer.lower()}_rejected_regions.yml"
    report_path = out / f"{args.producer.lower()}_extraction_report.md"
    backups = [item for item in [backup(best_path), backup(region_path), backup(rejected_path), backup(report_path)] if item]

    existing = read_csv(best_path)
    for row in existing:
        row.setdefault("seed_source_type", "AGGREGATE_MEDIUM_SEED")
        row.setdefault("status", row.get("status") or "RESEARCH_SEED_ONLY_NOT_PRODUCTION_DEFAULT")
        row.setdefault("notes", RESEARCH_WARNING)

    granular: list[dict[str, Any]] = []
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row.get("asset")), str(row.get("timeframe")))].append(row)
    for (_asset, _timeframe), group_rows in sorted(grouped.items()):
        group_rows.sort(key=lambda item: int(float(item.get("rank") or 999)))
        for row in group_rows[: args.top_n]:
            item = dict(row)
            item["seed_source_type"] = "SMOKE_ASSET_TIMEFRAME_SEED"
            item["granularity_status"] = "ASSET_TIMEFRAME_AVAILABLE"
            item["status"] = "SMOKE_RESEARCH_SEED"
            item["notes"] = f"{RESEARCH_WARNING} Smoke seeds prove pipeline/schema only; not final optimization results."
            granular.append(item)

    combined = existing + granular
    write_csv(best_path, combined)
    write_seed_regions(region_path, combined, args.producer)
    write_rejected(rejected_path, rows)
    write_report(report_path, combined, backups, input_path, args.producer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
