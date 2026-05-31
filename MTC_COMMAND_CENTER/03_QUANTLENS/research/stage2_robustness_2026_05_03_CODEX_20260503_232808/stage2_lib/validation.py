from __future__ import annotations

import pandas as pd


def fee_monotonic_ok(fee_rows: pd.DataFrame) -> bool:
    for _, group in fee_rows.groupby("candidate_id"):
        ordered = group.sort_values("cost_mult")
        values = list(pd.to_numeric(ordered["profit_factor"], errors="coerce").fillna(0))
        if any(values[i] < values[i + 1] for i in range(len(values) - 1)):
            return False
    return True
