from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class AlignmentEvent:
    tv_seq: int
    py_seq: int
    mode: str


def _row_matches(
    tv_row: pd.Series,
    py_row: pd.Series,
    *,
    tolerance_min: int = 15,
) -> bool:
    tol_sec = int(tolerance_min) * 60
    return (
        str(tv_row["side"]) == str(py_row["side"])
        and str(tv_row["reason"]) == str(py_row["reason"])
        and abs((tv_row["entry_time"] - py_row["entry_time"]).total_seconds()) <= tol_sec
        and abs((tv_row["exit_time"] - py_row["exit_time"]).total_seconds()) <= tol_sec
    )


def greedy_prefix_alignment(
    tv: pd.DataFrame,
    py: pd.DataFrame,
    *,
    tolerance_min: int = 15,
) -> dict[str, Any]:
    """
    Greedy prefix alignment with single-row skip support.

    This is diagnostic-only. It does not redefine canonical parity. It answers:
    "How far do the two sequences align if we allow one local skip on either
    side when the first divergence occurs?"
    """

    tv = tv.reset_index(drop=True).copy()
    py = py.reset_index(drop=True).copy()

    events: list[AlignmentEvent] = []
    i = 0
    j = 0

    while i < len(tv) and j < len(py):
        tv_row = tv.iloc[i]
        py_row = py.iloc[j]

        if _row_matches(tv_row, py_row, tolerance_min=tolerance_min):
            events.append(AlignmentEvent(tv_seq=i + 1, py_seq=j + 1, mode="direct"))
            i += 1
            j += 1
            continue

        if j + 1 < len(py) and _row_matches(tv_row, py.iloc[j + 1], tolerance_min=tolerance_min):
            events.append(AlignmentEvent(tv_seq=i + 1, py_seq=j + 2, mode="skip_py_1"))
            i += 1
            j += 2
            continue

        if i + 1 < len(tv) and _row_matches(tv.iloc[i + 1], py_row, tolerance_min=tolerance_min):
            events.append(AlignmentEvent(tv_seq=i + 2, py_seq=j + 1, mode="skip_tv_1"))
            i += 2
            j += 1
            continue

        break

    result: dict[str, Any] = {
        "matched_prefix_len": len(events),
        "events": [event.__dict__ for event in events],
        "break_tv_seq": i + 1 if i < len(tv) else None,
        "break_py_seq": j + 1 if j < len(py) else None,
        "tv_total": len(tv),
        "py_total": len(py),
    }

    if i < len(tv):
        result["break_tv"] = {
            "seq": int(i + 1),
            "side": str(tv.iloc[i]["side"]),
            "entry_time": str(tv.iloc[i]["entry_time"]),
            "exit_time": str(tv.iloc[i]["exit_time"]),
            "reason": str(tv.iloc[i]["reason"]),
        }
    else:
        result["break_tv"] = None

    if j < len(py):
        result["break_py"] = {
            "seq": int(j + 1),
            "side": str(py.iloc[j]["side"]),
            "entry_time": str(py.iloc[j]["entry_time"]),
            "exit_time": str(py.iloc[j]["exit_time"]),
            "reason": str(py.iloc[j]["reason"]),
        }
    else:
        result["break_py"] = None

    return result
