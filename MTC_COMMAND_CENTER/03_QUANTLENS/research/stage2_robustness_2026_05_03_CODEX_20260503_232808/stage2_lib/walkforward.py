from __future__ import annotations

import pandas as pd


def chronological_splits(trades: pd.DataFrame) -> dict[str, pd.DataFrame]:
    if trades.empty:
        return {"train": trades, "validation": trades, "test": trades}
    data = trades.sort_values("entry_time").reset_index(drop=True)
    n = len(data)
    return {
        "train": data.iloc[: int(n * 0.6)].copy(),
        "validation": data.iloc[int(n * 0.6) : int(n * 0.8)].copy(),
        "test": data.iloc[int(n * 0.8) :].copy(),
    }
