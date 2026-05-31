from __future__ import annotations

from datetime import datetime
from typing import Any


def choose_default_dataset(datasets: list[dict[str, Any]]) -> str | None:
    """
    Pick a deterministic default dataset preferring the widest usable history.
    Priority:
    1) largest date span (end-start)
    2) larger bar_count
    3) filename lexicographic
    """
    if not datasets:
        return None

    def _span_seconds(item: dict[str, Any]) -> float:
        start = item.get("start_date")
        end = item.get("end_date")
        if start is None or end is None:
            return -1.0
        if isinstance(start, datetime) and isinstance(end, datetime):
            return max(0.0, (end - start).total_seconds())
        return -1.0

    ranked = sorted(
        datasets,
        key=lambda d: (
            _span_seconds(d),
            int(d.get("bar_count") or 0),
            str(d.get("filename") or ""),
        ),
        reverse=True,
    )
    return ranked[0].get("filename")
