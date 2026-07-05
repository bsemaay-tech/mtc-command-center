"""
Patch PLAN case rows in MTC_V2_PARITY_CASES.csv with correct test parameters.
Run once: python patch_plan_cases.py
The CSV may have duplicate rows for the same case_id — all copies are patched.
"""
import csv
from pathlib import Path

CSV_PATH = Path(__file__).parent.parent / "MTC_V2_PARITY_CASES.csv"

# case_id -> {column: value} patches.
# Only columns present in SUPPORTED_PINE_INPUTS of parity_compare.py
# affect parity runs; all other columns are informational.
PATCHES: dict[str, dict[str, str]] = {
    # L17 — regime_lock=True already set in CSV; just unblock
    "AUTO_005": {"status": "PENDING_RUN"},

    # L5 — tp_mode=ATR already set in CSV; unblock
    "PLAN_017": {"status": "PENDING_RUN"},

    # L6a — max_entries=2 already set; unblock
    "PLAN_018": {"status": "PENDING_RUN"},

    # L6b — PriceExitEngine: add TP so book has a target to manage
    "PLAN_019": {"tp_mode": "ATR", "status": "PENDING_RUN"},

    # L7 — Break Even
    "PLAN_020": {
        "use_break_even": "True",
        "be_trigger_r": "1.0",
        "be_buffer_r": "0.1",
        "status": "PENDING_RUN",
    },

    # L8 — Trailing Stop
    "PLAN_021": {
        "use_trailing": "True",
        "trail_start_r": "2.0",
        "trail_distance_atr_mult": "1.0",
        "status": "PENDING_RUN",
    },

    # L9 — Multi-TP (requires SL which is on by default ATR mode)
    "PLAN_022": {
        "tp_mode": "Multi-TP",
        "tp1_r_multiple": "3.0",
        "tp1_close_pct": "50.0",
        "tp2_r_multiple": "5.5",
        "status": "PENDING_RUN",
    },

    # L10 — SL Percent mode
    "PLAN_023": {
        "sl_mode": "Percent",
        "sl_pct": "2.0",
        "status": "PENDING_RUN",
    },

    # L11 — TP Percent mode
    "PLAN_024": {
        "tp_mode": "Percent",
        "tp_percent": "3.0",
        "status": "PENDING_RUN",
    },

    # L12 — MA Filter gate (same as AUTO_017 but is the L12 layer gate case)
    "PLAN_025": {
        "use_ma_filter": "True",
        "ma_type": "EMA",
        "ma_length": "200",
        "status": "PENDING_RUN",
    },

    # L13 — Opposite Signal Exit (exit_on_opposite_signal=True is default)
    "PLAN_026": {
        "exit_on_opposite_signal": "True",
        "status": "PENDING_RUN",
    },

    # L14 — MA Block Exit
    "PLAN_027": {
        "use_ma_filter": "True",
        "ma_length": "200",
        "exit_on_ma_block": "True",
        "status": "PENDING_RUN",
    },

    # L15 — Time Stop
    "PLAN_028": {
        "use_time_stop": "True",
        "time_stop_bars": "50",
        "time_stop_condition": "Always",
        "status": "PENDING_RUN",
    },

    # L16 — Max Drawdown Guard
    "PLAN_029": {
        "use_max_drawdown_guard": "True",
        "max_drawdown_pct": "10.0",
        "status": "PENDING_RUN",
    },

    # L18 — Confirmation Transform
    "PLAN_030": {
        "use_confirm_transform": "True",
        "confirm_bars": "3",
        "confirm_close_crosses": "True",
        "status": "PENDING_RUN",
    },

    # L18b — Advanced Confirmation
    "PLAN_031": {
        "use_confirm_transform": "True",
        "confirm_bars": "3",
        "require_raw_still_true": "True",
        "status": "PENDING_RUN",
    },

    # PLAN_032 (L19) — SKIP — do not touch

    # L20 — Level Proximity Gate
    "PLAN_033": {
        "use_level_proximity_gate": "True",
        "level_proximity_threshold_pct": "0.5",
        "level_proximity_lookback": "50",
        "status": "PENDING_RUN",
    },

    # L21 — Level Retest Transform
    "PLAN_034": {
        "use_level_retest": "True",
        "retest_timeout_bars": "50",
        "retest_buffer_pct": "0.1",
        "status": "PENDING_RUN",
    },

    # L22 — Candle Pattern Gate
    "PLAN_035": {
        "use_candle_pattern_gate": "True",
        "status": "PENDING_RUN",
    },

    # L24 — Debug layer (no trade impact)
    "PLAN_036": {"status": "PENDING_RUN"},

    # L25 — WunderTrading (alert dispatch only, no trade impact)
    "PLAN_037": {"status": "PENDING_RUN"},
}


def patch_csv(csv_path: Path, patches: dict[str, dict[str, str]]) -> None:
    with csv_path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        headers = list(reader.fieldnames or [])

    if not headers and rows:
        headers = list(rows[0].keys())

    patched_count = 0
    for row in rows:
        case_id = row.get("case_id", "").strip()
        if case_id in patches:
            for col, val in patches[case_id].items():
                if col not in headers:
                    print(f"WARNING: column {col!r} not in CSV headers — skipping for {case_id}")
                    continue
                row[col] = val
            patched_count += 1

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Patched {patched_count} row(s) across {len(patches)} target case_ids.")
    print(f"CSV path: {csv_path}")


if __name__ == "__main__":
    patch_csv(CSV_PATH, PATCHES)
