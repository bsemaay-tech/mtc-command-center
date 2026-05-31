"""Manual override support for the regime calendar."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


class ManualOverride:
    """
    Load and apply manual regime overrides on top of auto-labeled windows.

    Override file format (JSON array)::

        [
          {"start": "2020-01-01", "end": "2020-06-30", "label": "TREND_BULL"},
          {"start": "2022-11-01", "end": "2023-01-15", "label": "TREND_BEAR"}
        ]

    Any auto window that overlaps an override is split / replaced by the override.
    The ``source`` field of overridden windows is set to ``"manual"``.
    """

    def __init__(self, overrides: list[dict]) -> None:
        self._overrides = overrides

    @classmethod
    def load(cls, filepath: str | Path) -> "ManualOverride":
        data = json.loads(Path(filepath).read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("Override file must be a JSON array of window objects.")
        return cls(data)

    @classmethod
    def empty(cls) -> "ManualOverride":
        return cls([])

    # ------------------------------------------------------------------
    def apply(self, windows: list[dict]) -> list[dict]:
        """
        Merge overrides into *windows*.

        Returns
        -------
        list[dict]
            Merged and sorted windows. Overridden windows have ``"source": "manual"``.
        """
        if not self._overrides:
            return windows

        # Parse override boundaries
        parsed_overrides = []
        for ov in self._overrides:
            s = pd.Timestamp(ov["start"], tz="UTC")
            e = pd.Timestamp(ov["end"], tz="UTC")
            parsed_overrides.append({"start": s, "end": e, "label": ov["label"]})

        result: list[dict] = []

        for win in windows:
            ws = pd.Timestamp(win["start"])
            we = pd.Timestamp(win["end"])
            if ws.tzinfo is None:
                ws = ws.tz_localize("UTC")
                we = we.tz_localize("UTC")

            # Collect overrides that overlap this window
            applicable = [
                ov for ov in parsed_overrides
                if ov["start"] <= we and ov["end"] >= ws
            ]

            if not applicable:
                result.append(win)
                continue

            # Split the window around overlapping overrides
            # Sort overrides by start
            applicable = sorted(applicable, key=lambda x: x["start"])

            cur = ws
            for ov in applicable:
                ov_s = max(ov["start"], ws)
                ov_e = min(ov["end"], we)

                if cur < ov_s:
                    # Auto portion before the override
                    result.append(_build(cur, ov_s - pd.Timedelta(seconds=1), win["label"], "auto"))
                # Override portion
                result.append(_build(ov_s, ov_e, ov["label"], "manual"))
                cur = ov_e + pd.Timedelta(seconds=1)

            if cur <= we:
                result.append(_build(cur, we, win["label"], "auto"))

        # Sort final list
        result.sort(key=lambda w: w["start"])
        return result


# ---------------------------------------------------------------------------
def _build(start: pd.Timestamp, end: pd.Timestamp, label: str, source: str) -> dict:
    from .labeler import LABEL_DISPLAY
    return {
        "start": start.isoformat(),
        "end": end.isoformat(),
        "label": label,
        "label_display": LABEL_DISPLAY.get(label, label),
        "bars": None,   # not recalculated for split windows (cosmetic only)
        "source": source,
    }
