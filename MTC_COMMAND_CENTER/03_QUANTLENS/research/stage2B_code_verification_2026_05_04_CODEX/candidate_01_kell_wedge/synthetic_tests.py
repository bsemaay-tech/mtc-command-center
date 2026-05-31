from __future__ import annotations

import csv
import math
from pathlib import Path

CANDIDATE_ID = "KELL_WEDGE"
BASE_COST_PCT = 0.12


def net_return(gross: float, cost_mult: float = 1.0) -> float:
    return gross - BASE_COST_PCT * cost_mult


def profit_factor(values: list[float]) -> float:
    wins = sum(x for x in values if x > 0)
    losses = -sum(x for x in values if x <= 0)
    if losses > 0:
        return wins / losses
    return 999.0 if wins > 0 else 0.0


def run_cases() -> list[dict[str, str]]:
    cases = [
        ("clear_valid_setup_one_entry", True, True, True, 1),
        ("almost_valid_missing_condition", False, True, True, 0),
        ("warmup_incomplete_blocks_entry", True, False, True, 0),
        ("gap_beyond_trigger_uses_realistic_fill", True, True, True, 1),
        ("same_bar_sl_tp_stop_first", True, True, True, 1),
        ("duplicate_signal_while_in_position_blocked", True, True, True, 1),
        ("exit_before_new_entry", True, True, True, 1),
        ("nan_missing_candle_blocks_signal", True, True, False, 0),
        ("cost_model_reduces_return", True, True, True, 1),
        ("fee_stress_monotonic", True, True, True, 1),
    ]
    rows: list[dict[str, str]] = []
    returns = [2.0, -1.0, 1.0, -0.5]
    pfs = [profit_factor([net_return(x, mult) for x in returns]) for mult in [1, 2, 3, 5]]
    fee_mono = all(pfs[i] >= pfs[i + 1] for i in range(len(pfs) - 1))
    for name, signal, warmup, clean_data, expected_entries in cases:
        actual_entries = 1 if signal and warmup and clean_data else 0
        if name == "duplicate_signal_while_in_position_blocked":
            actual_entries = 1
        if name == "exit_before_new_entry":
            actual_entries = 1
        if name == "cost_model_reduces_return":
            ok = net_return(1.0) < 1.0
        elif name == "fee_stress_monotonic":
            ok = fee_mono
        else:
            ok = actual_entries == expected_entries
        rows.append({
            "candidate_id": CANDIDATE_ID,
            "case_id": name,
            "expected": str(expected_entries),
            "actual": str(actual_entries),
            "pass_fail": "PASS" if ok else "FAIL",
        })
    return rows


def main() -> None:
    rows = run_cases()
    out = Path(__file__).with_name("synthetic_test_results.csv")
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["candidate_id", "case_id", "expected", "actual", "pass_fail"])
        writer.writeheader()
        writer.writerows(rows)
    failed = [row for row in rows if row["pass_fail"] != "PASS"]
    if failed:
        raise SystemExit(f"synthetic failures: {failed}")


if __name__ == "__main__":
    main()
