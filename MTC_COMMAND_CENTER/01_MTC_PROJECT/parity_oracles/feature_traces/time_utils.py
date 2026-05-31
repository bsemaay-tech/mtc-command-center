from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


def to_iso_utc(value: Any) -> str:
    if isinstance(value, datetime):
        dt = value
    else:
        text = str(value).strip()
        if not text:
            return ""
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            if text.isdigit():
                dt = datetime.fromtimestamp(int(text), tz=UTC)
            else:
                dt = datetime.fromisoformat(text)
        except ValueError:
            return str(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC).isoformat()


def looks_iso_utc(value: str) -> bool:
    if not value or value.isdigit():
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None
