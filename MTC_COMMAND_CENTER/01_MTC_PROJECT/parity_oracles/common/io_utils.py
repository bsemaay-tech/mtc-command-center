from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]


NORMALIZED_FILES = {
    "data": ("normalized_data.csv", ["timestamp", "open", "high", "low", "close", "volume"]),
    "indicators": ("normalized_indicators.csv", ["timestamp", "indicator_name", "value"]),
    "signals": (
        "normalized_signals.csv",
        ["timestamp", "bar_index", "raw_long", "raw_short", "final_long", "final_short", "reason_code"],
    ),
    "decisions": (
        "normalized_decisions.csv",
        ["timestamp", "bar_index", "side", "entry_allowed", "blocked_reason", "position_before", "position_after"],
    ),
    "trades": (
        "normalized_trades.csv",
        ["trade_id", "timestamp", "bar_index", "event_type", "side", "qty", "price", "reason", "sl", "tp", "commission", "equity_after"],
    ),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> None:
    ensure_dir(path.parent)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def sha256_file(path: Path | None) -> str:
    if path is None or not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_json(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def git_code_hash(root: Path = ROOT) -> str:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode == 0:
            return completed.stdout.strip()
    except OSError:
        pass
    return ""


def empty_normalized_set(out_dir: Path) -> dict[str, str]:
    outputs: dict[str, str] = {}
    for name, (filename, columns) in NORMALIZED_FILES.items():
        target = out_dir / filename
        write_csv(target, columns, [])
        outputs[name] = str(target)
    stats = out_dir / "normalized_stats.json"
    write_json(stats, {})
    outputs["stats"] = str(stats)
    return outputs


def result_payload(
    engine_name: str,
    command: str,
    status: str,
    case: dict[str, Any],
    output_files: dict[str, str],
    started_at: str,
    errors: list[str] | None = None,
    warnings: list[str] | None = None,
    engine_version: str = "unknown",
) -> dict[str, Any]:
    data_file = ROOT / str(case.get("data_file", ""))
    return {
        "engine_name": engine_name,
        "engine_version": engine_version,
        "command": command,
        "status": status,
        "data_hash": sha256_file(data_file),
        "config_hash": sha256_json(case.get("mtc_config", {})),
        "code_hash": git_code_hash(),
        "run_started_at": started_at,
        "run_finished_at": utc_now(),
        "output_files": output_files,
        "errors": errors or [],
        "warnings": warnings or [],
    }
