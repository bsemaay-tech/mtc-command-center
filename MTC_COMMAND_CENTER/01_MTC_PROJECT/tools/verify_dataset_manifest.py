from __future__ import annotations

import argparse
import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_simple_yaml(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        data[key.strip()] = value
    return data


def write_simple_yaml(path: Path, data: dict[str, Any]) -> None:
    lines = []
    for key, value in data.items():
        if value is None:
            rendered = "UNKNOWN"
        elif isinstance(value, (int, float)):
            rendered = str(value)
        else:
            rendered = '"' + str(value).replace('"', '\\"') + '"'
        lines.append(f"{key}: {rendered}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _parse_time(value: str) -> datetime | None:
    value = value.strip()
    if not value:
        return None
    try:
        if value.isdigit():
            return datetime.fromtimestamp(int(value), tz=timezone.utc)
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def inspect_csv(path: Path) -> dict[str, Any]:
    row_count = 0
    first_time: str | None = None
    last_time: str | None = None
    timestamps: list[datetime] = []
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            row_count += 1
            time_value = str(row.get("time") or row.get("timestamp") or row.get("datetime") or "")
            if first_time is None:
                first_time = time_value
            last_time = time_value
            parsed = _parse_time(time_value)
            if parsed is not None:
                timestamps.append(parsed)
    has_gaps: str = "UNKNOWN"
    if len(timestamps) > 3:
        deltas = [(timestamps[idx] - timestamps[idx - 1]).total_seconds() for idx in range(1, len(timestamps))]
        positive = [delta for delta in deltas if delta > 0]
        if positive:
            base = min(positive)
            has_gaps = "true" if any(delta > base * 1.5 for delta in positive) else "false"
    return {
        "row_count": row_count,
        "start": first_time or "UNKNOWN",
        "end": last_time or "UNKNOWN",
        "has_gaps": has_gaps,
    }


def build_manifest(source_path: Path) -> dict[str, Any]:
    inspected = inspect_csv(source_path)
    name = source_path.name
    return {
        "dataset_id": "binance_btcusdtp_60_consolidated_stable",
        "symbol": "BTCUSDT.P",
        "exchange": "BINANCE",
        "timeframe": "60",
        "source_type": "local_csv",
        "source_path": str(source_path).replace("\\", "/"),
        "row_count": inspected["row_count"],
        "start": inspected["start"],
        "end": inspected["end"],
        "timezone": "UTC_or_exchange_export_UNKNOWN",
        "sha256": sha256_file(source_path),
        "file_size_bytes": source_path.stat().st_size,
        "has_gaps": inspected["has_gaps"],
        "notes": f"Generated from available local chart CSV: {name}",
    }


def verify_manifest(path: Path) -> tuple[bool, str]:
    manifest = read_simple_yaml(path)
    source_path = Path(str(manifest["source_path"]))
    if not source_path.is_absolute():
        source_path = Path.cwd() / source_path
    actual_hash = sha256_file(source_path)
    expected_hash = str(manifest.get("sha256", ""))
    if actual_hash != expected_hash:
        return False, f"dataset hash mismatch: expected={expected_hash} actual={actual_hash}"
    return True, f"dataset hash ok: {actual_hash}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--source")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    manifest_path = Path(args.manifest)
    if args.write:
        if not args.source:
            parser.error("--source is required with --write")
        write_simple_yaml(manifest_path, build_manifest(Path(args.source)))
    ok, message = verify_manifest(manifest_path)
    print(message)
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
