from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, Mapping, Any

STANDARD_FILES = {
    "data": "normalized_data.csv",
    "indicators": "normalized_indicators.csv",
    "signals": "normalized_signals.csv",
    "decisions": "normalized_decisions.csv",
    "trades": "normalized_trades.csv",
    "stats": "normalized_stats.json",
}

COLUMNS = {
    "data": ["timestamp", "open", "high", "low", "close", "volume"],
    "indicators": ["timestamp", "indicator_name", "value"],
    "signals": ["timestamp", "bar_index", "raw_long", "raw_short", "final_long", "final_short", "reason_code"],
    "decisions": ["timestamp", "bar_index", "side", "entry_allowed", "blocked_reason", "position_before", "position_after"],
    "trades": ["trade_id", "timestamp", "bar_index", "event_type", "side", "qty", "price", "reason", "sl", "tp", "commission", "equity_after"],
}

def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def write_csv(path: str | Path, columns: list[str], rows: Iterable[Mapping[str, Any]]) -> None:
    path = Path(path)
    ensure_dir(path.parent)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({c: row.get(c, "") for c in columns})

def write_json(path: str | Path, obj: Any) -> None:
    path = Path(path)
    ensure_dir(path.parent)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")

def read_csv_dicts(path: str | Path) -> list[dict[str, str]]:
    path = Path(path)
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def normalize_bool(value: Any) -> str:
    if isinstance(value, bool):
        return "1" if value else "0"
    s = str(value).strip().lower()
    if s in {"true", "t", "yes", "y", "1", "long"}:
        return "1"
    if s in {"false", "f", "no", "n", "0", "", "nan", "none"}:
        return "0"
    return s
