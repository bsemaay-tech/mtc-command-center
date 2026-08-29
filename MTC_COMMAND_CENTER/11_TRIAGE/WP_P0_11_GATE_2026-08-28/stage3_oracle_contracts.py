from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


EXECUTION_OBSERVATION = "EXECUTION_OBSERVATION"
SOURCE_CORROBORATION = "SOURCE_CORROBORATION"
COMPARISON_RULE_ID = "RECURSIVE_EXACT_IEEE754_HEX_V1"
EXPECTATION_METHOD_ID = "P009_LITERAL_SOURCE_ARITHMETIC_V1"
CORROBORATION_STATUS = "REQUIRED_TERMINAL_AUTHORITY_EVIDENCE"
MUTATION_STATUS = "REQUIRED_RED_THEN_GREEN"
MUTATION_RESTORED_GREEN = "RECURSIVE_EXACT_IEEE754_HEX_V1_MATCH"
P009_PATH = (
    "MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/"
    "CAPABILITY_CANONICALIZATION_TABLE.md"
)
P009_BLOB_OID = "1c39ab939dfcf5589e5ec8fba4af8966947a67fc"
P009_SHA256 = "7d48871a3e45dab118e97969d701912edb5d7c16a4d822d816beca1d03a42249"

C32_VALUES = (
    "local",
    "delay_after_protective_exit",
    "carry_to_next_bar_after_protective_exit",
    "next_bar_open_after_protective_exit_signal",
    "next_bar_close_after_protective_exit_signal",
)
C32_INVALID_CONTROL = "next_bar_open"
C32_INVALID_ERROR = (
    "tw_reversal_reentry_mode must be one of: local, delay_after_protective_exit, "
    "carry_to_next_bar_after_protective_exit, next_bar_open_after_protective_exit_signal, "
    "next_bar_close_after_protective_exit_signal"
)


def _provenance(lines: str) -> dict[str, Any]:
    return {
        "method": EXPECTATION_METHOD_ID,
        "source": {
            "path": P009_PATH,
            "git_blob_oid": P009_BLOB_OID,
            "sha256": P009_SHA256,
            "section_lines_at_pinned_blob": lines,
        },
        "producer_output_may_not_rebless_expected": True,
    }


def _authority(*requirements: tuple[str, str]) -> dict[str, Any]:
    return {
        "status": CORROBORATION_STATUS,
        "required": True,
        "authority_requirements": [
            {"name": name, "evidence_mode": evidence_mode}
            for name, evidence_mode in requirements
        ],
    }


def _mutation(
    row_id: str,
    source_seam: str,
    old_sha256: str,
    new_sha256: str,
    required_path: str,
) -> dict[str, str]:
    return {
        "mutation_id": f"{row_id}-STAGE3-MUT-001",
        "source_seam": source_seam,
        "mutation": (
            "EXACT_TEXT_REPLACE_ONCE_V1:"
            f"old_sha256={old_sha256}:new_sha256={new_sha256}"
        ),
        "required_red": f"MISMATCH_PATH_PRESENT_V1:{required_path}",
        "restored_green": MUTATION_RESTORED_GREEN,
        "status": MUTATION_STATUS,
    }


C32_BARS = [
    {"bar_index": 0, "timestamp": "2026-01-01T00:00:00+00:00", "open": 100.0, "high": 100.0, "low": 100.0, "close": 100.0, "volume": 1.0, "raw_long": True, "raw_short": False},
    {"bar_index": 1, "timestamp": "2026-01-01T00:01:00+00:00", "open": 99.0, "high": 99.0, "low": 94.0, "close": 94.0, "volume": 1.0, "raw_long": True, "raw_short": False},
    {"bar_index": 2, "timestamp": "2026-01-01T00:02:00+00:00", "open": 94.0, "high": 100.0, "low": 94.0, "close": 100.0, "volume": 1.0, "raw_long": True, "raw_short": False},
    {"bar_index": 3, "timestamp": "2026-01-01T00:03:00+00:00", "open": 99.0, "high": 100.0, "low": 99.0, "close": 100.0, "volume": 1.0, "raw_long": False, "raw_short": False},
    {"bar_index": 4, "timestamp": "2026-01-01T00:04:00+00:00", "open": 100.0, "high": 100.0, "low": 99.0, "close": 100.0, "volume": 1.0, "raw_long": False, "raw_short": False},
    {"bar_index": 5, "timestamp": "2026-01-01T00:05:00+00:00", "open": 100.0, "high": 100.0, "low": 99.0, "close": 100.0, "volume": 1.0, "raw_long": True, "raw_short": False},
]


def _c32_run(value: str, bar_index: int, price: float, quantity: float) -> dict[str, Any]:
    return {
        "value": value,
        "events": [
            {"bar_index": 0, "event": "ENTER_LONG", "price": 100.0, "quantity": 1.0, "reason": "c32_fixture_signal"},
            {"bar_index": 1, "event": "EXIT_LONG", "price": 94.0, "quantity": 1.0, "reason": "sl_percent_hit", "realized_pnl": -6.0},
            {"bar_index": bar_index, "event": "ENTER_LONG", "price": price, "quantity": quantity, "reason": "c32_fixture_signal"},
        ],
        "reentry": {"bar_index": bar_index, "price": price, "quantity": quantity},
    }


C32_RUNS = [
    _c32_run(C32_VALUES[0], 2, 100.0, 0.994),
    _c32_run(C32_VALUES[1], 5, 100.0, 0.994),
    _c32_run(C32_VALUES[2], 3, 100.0, 0.994),
    _c32_run(C32_VALUES[3], 3, 99.0, 1.00404),
    _c32_run(C32_VALUES[4], 4, 100.0, 0.994),
]

C32_FINAL_RUNS = [
    {
        "value": item["value"],
        "position": {
            "side": "long",
            "entry_bar": item["reentry"]["bar_index"],
            "entry_price": item["reentry"]["price"],
            "quantity": item["reentry"]["quantity"],
        },
        "realized_pnl": -6.0,
        "total_entries": 2,
        "total_exits": 1,
    }
    for item in C32_RUNS
]

C34_BARS = [
    {"bar_index": 0, "timestamp": "2026-01-01T00:00:00+00:00", "open": 100.0, "high": 100.0, "low": 100.0, "close": 100.0, "volume": 10.0, "raw_long": True, "raw_short": False},
    {"bar_index": 1, "timestamp": "2026-01-01T00:01:00+00:00", "open": 98.0, "high": 98.0, "low": 94.0, "close": 95.0, "volume": 10.0, "raw_long": False, "raw_short": False},
    {"bar_index": 2, "timestamp": "2026-01-01T00:02:00+00:00", "open": 94.0, "high": 94.0, "low": 88.0, "close": 89.0, "volume": 10.0, "raw_long": False, "raw_short": False},
    {"bar_index": 3, "timestamp": "2026-01-01T00:03:00+00:00", "open": 88.0, "high": 88.0, "low": 84.0, "close": 85.0, "volume": 10.0, "raw_long": False, "raw_short": False},
]

C34_L1 = {
    "checkpoints": [],
    "events": [
        {"bar_index": 0, "event": "ENTER_LONG", "price": 100.0, "quantity": 40.0, "reason": "c34_fixture_signal"}
    ],
}
C34_L2 = {
    "checkpoints": [
        {"mark": 98.0, "required_margin": 784.0, "equity": 920.0, "deficit": -136.0, "exit_fraction": 0.0},
        {"mark": 94.0, "required_margin": 752.0, "equity": 760.0, "deficit": -8.0, "exit_fraction": 0.0},
        {"mark": 94.0, "required_margin": 752.0, "equity": 760.0, "deficit": -8.0, "exit_fraction": 0.0},
        {"mark": 88.0, "required_margin": 704.0, "equity": 520.0, "deficit": 184.0, "exit_fraction": 1.0},
    ],
    "events": [
        {"bar_index": 0, "event": "ENTER_LONG", "price": 100.0, "quantity": 40.0, "reason": "c34_fixture_signal"},
        {"bar_index": 2, "event": "EXIT_LONG", "price": 88.0, "quantity": 40.0, "reason": "margin_call", "realized_pnl": -480.0},
    ],
}
C34_FINAL_OPEN = {
    "position": {"side": "long", "entry_bar": 0, "entry_price": 100.0, "quantity": 40.0},
    "realized_pnl": 0.0,
    "equity_at_final_close": 400.0,
    "total_entries": 1,
    "total_exits": 0,
}
C34_FINAL_L2 = {
    "position": None,
    "realized_pnl": -480.0,
    "equity_at_final_close": 520.0,
    "total_entries": 1,
    "total_exits": 1,
}

C42_COMMON_BARS = [
    {"bar_index": 0, "timestamp": "2026-01-01T00:00:00+00:00", "open": 100.0, "high": 102.0, "low": 98.0, "close": 100.0, "volume": 1.0},
    {"bar_index": 1, "timestamp": "2026-01-01T00:01:00+00:00", "open": 100.0, "high": 102.0, "low": 98.0, "close": 100.0, "volume": 1.0},
    {"bar_index": 2, "timestamp": "2026-01-01T00:02:00+00:00", "open": 100.0, "high": 102.0, "low": 90.0, "close": 95.0, "volume": 1.0},
    {"bar_index": 3, "timestamp": "2026-01-01T00:03:00+00:00", "open": 95.0, "high": 110.0, "low": 95.0, "close": 109.0, "volume": 1.0},
    {"bar_index": 4, "timestamp": "2026-01-01T00:04:00+00:00", "open": 109.0, "high": 110.0, "low": 108.0, "close": 109.0, "volume": 1.0},
]
C42_F3_WICK_BARS = [
    C42_COMMON_BARS[0],
    {"bar_index": 1, "timestamp": "2026-01-01T00:01:00+00:00", "open": 100.0, "high": 102.0, "low": 94.0, "close": 100.0, "volume": 1.0},
]
C42_F4_BARS = [
    {"bar_index": 0, "timestamp": "2026-01-01T00:00:00+00:00", "open": 100.0, "high": 100.0, "low": 100.0, "close": 100.0, "volume": 1.0},
    {"bar_index": 1, "timestamp": "2026-01-01T00:01:00+00:00", "open": 115.0, "high": 115.0, "low": 115.0, "close": 115.0, "volume": 1.0},
    {"bar_index": 2, "timestamp": "2026-01-01T00:02:00+00:00", "open": 104.0, "high": 104.0, "low": 104.0, "close": 104.0, "volume": 1.0},
]


def _raw(long: bool, short: bool, reason: str, direction: int | None, line: float | None) -> dict[str, Any]:
    return {"long": long, "short": short, "reason": reason, "direction": direction, "line": line}


C42_EXPECTED_ARMS = {
    "F1": {
        "raw_signals": [_raw(False, False, "st_ha_not_supported", None, None) for _ in range(5)],
        "fills": [],
    },
    "F2": {
        "raw_signals": [
            _raw(False, False, "st_direction_init", 1, 96.0),
            _raw(False, False, "st_hold_long", 1, 96.0),
            _raw(False, True, "st_flip_short", -1, 104.0),
            _raw(True, False, "st_flip_long", 1, 87.5),
            _raw(False, False, "st_hold_long", 1, 107.0),
        ],
        "fills": [
            {"bar_index": 2, "event": "ENTER_SHORT", "price": 95.0, "quantity": 1.0, "reason": "st_flip_short"},
            {"bar_index": 3, "event": "EXIT_SHORT", "price": 109.0, "quantity": 1.0, "reason": "opp_signal", "realized_pnl": -14.0},
            {"bar_index": 3, "event": "ENTER_LONG", "price": 109.0, "quantity": 1.0, "reason": "st_flip_long"},
        ],
    },
    "F3_CLOSE": {
        "raw_signals": [
            _raw(False, False, "st_direction_init", 1, 96.0),
            _raw(False, False, "st_hold_long", 1, 96.0),
        ],
        "fills": [],
    },
    "F3_WICK": {
        "raw_signals": [
            _raw(False, False, "st_direction_init", 1, 96.0),
            _raw(False, True, "st_flip_short", -1, 104.0),
        ],
        "fills": [
            {"bar_index": 1, "event": "ENTER_SHORT", "price": 100.0, "quantity": 1.0, "reason": "st_flip_short"}
        ],
    },
    "F4": {
        "raw_signals": [
            _raw(False, False, "rf_init", 0, 100.0),
            _raw(True, False, "rf_flip_long", 1, 105.0),
            _raw(False, True, "rf_flip_short", -1, 114.0),
        ],
        "fills": [
            {"bar_index": 1, "event": "ENTER_LONG", "price": 115.0, "quantity": 1.0, "reason": "rf_flip_long"},
            {"bar_index": 2, "event": "EXIT_LONG", "price": 104.0, "quantity": 1.0, "reason": "opp_signal", "realized_pnl": -11.0},
            {"bar_index": 2, "event": "ENTER_SHORT", "price": 104.0, "quantity": 1.0, "reason": "rf_flip_short"},
        ],
    },
}

C42_FINAL_ARMS = {
    "F1": {"position": None, "realized_pnl": 0.0, "total_entries": 0, "total_exits": 0},
    "F2": {"position": {"side": "long", "entry_bar": 3, "entry_price": 109.0, "quantity": 1.0}, "realized_pnl": -14.0, "total_entries": 2, "total_exits": 1},
    "F3_CLOSE": {"position": None, "realized_pnl": 0.0, "total_entries": 0, "total_exits": 0},
    "F3_WICK": {"position": {"side": "short", "entry_bar": 1, "entry_price": 100.0, "quantity": 1.0}, "realized_pnl": 0.0, "total_entries": 1, "total_exits": 0},
    "F4": {"position": {"side": "short", "entry_bar": 2, "entry_price": 104.0, "quantity": 1.0}, "realized_pnl": -11.0, "total_entries": 2, "total_exits": 1},
}


_CONTRACTS: Mapping[str, Mapping[str, Any]] = {
    "C32": {
        "scenario_id": "C32-LEGACY-001",
        "producer_adapter": "A.runner_reentry_enum_stage3",
        "complete_inputs": {
            "accepted_values": list(C32_VALUES),
            "invalid_control": C32_INVALID_CONTROL,
            "config": {
                "tw_audit_semantics_mode": "research",
                "tw_reversal_reentry_delay_bars": 2,
                "use_sl": True,
                "use_sl_percent": True,
                "sl_percent": 5.0,
                "tp_mode": "None",
                "exit_on_opposite_signal": True,
                "allow_flip": True,
                "execution_profile_id": "close_only_deterministic_v2",
                "initial_capital": 1000.0,
                "risk_per_long_pct": 0.5,
                "risk_per_short_pct": 0.5,
                "max_leverage_cap": 1.0,
                "cooldown_bars": 0,
                "max_entries": 1,
                "regime_lock": False,
                "instrument_price_tick": 0.01,
                "instrument_qty_step": 0.000001,
                "instrument_min_qty": 0.0,
                "instrument_min_notional": 0.0,
                "instrument_contract_multiplier": 1.0,
            },
            "bars": C32_BARS,
        },
        "literal_expected_observation": {
            "runs": C32_RUNS,
            "invalid_control": {
                "accepted": False,
                "accepted_values": list(C32_VALUES),
                "error_type": "ValueError",
                "error": C32_INVALID_ERROR,
                "value": C32_INVALID_CONTROL,
            },
        },
        "literal_expected_final_state": {"runs": C32_FINAL_RUNS},
        "expectation_derivation": _provenance("830-870"),
        "comparison_rule": COMPARISON_RULE_ID,
        "clean_producer_corroboration": _authority(
            ("A_CURRENT_MASTER", EXECUTION_OBSERVATION)
        ),
        "producer_mutation": _mutation(
            "C32",
            "mtc_v2/core/runner.py",
            "ac9f7cc57e54c82dc623ffd5e1657fba46a2dd6a9eb90df08ed49ac6bd8fadf4",
            "0dac5019f5ece8803bb4f169f714e46e15d844a5cdfce94e0876e554f135a9cb",
            "$.observation.runs[2].reentry.bar_index",
        ),
    },
    "C34": {
        "scenario_id": "C34-LEGACY-001",
        "producer_adapter": "A.runner_margin_call_stage3",
        "complete_inputs": {
            "arms": [
                {"arm": "L1", "tw_audit_semantics_mode": "off", "tw_margin_call_mode": "off"},
                {"arm": "L2", "tw_audit_semantics_mode": "research", "tw_margin_call_mode": "tradingview"},
                {"arm": "L3", "tw_audit_semantics_mode": "off", "tw_margin_call_mode": "tradingview"},
            ],
            "config": {
                "initial_capital": 1000.0,
                "max_leverage_cap": 5.0,
                "margin_long_pct": 20.0,
                "margin_short_pct": 20.0,
                "use_sl": False,
                "use_sl_percent": False,
                "use_sl_atr": False,
                "use_sl_swing_atr": False,
                "tp_mode": "None",
                "fallback_size_pct": 400.0,
                "cooldown_bars": 0,
                "max_entries": 1,
                "instrument_price_tick": 0.01,
                "instrument_qty_step": 1.0,
                "instrument_min_qty": 0.0,
                "instrument_min_notional": 0.0,
                "instrument_contract_multiplier": 1.0,
            },
            "bars": C34_BARS,
        },
        "literal_expected_observation": {
            "arms": {"L1": C34_L1, "L2": C34_L2, "L3": C34_L1},
            "l1_l3_field_identical": True,
        },
        "literal_expected_final_state": {
            "arms": {"L1": C34_FINAL_OPEN, "L2": C34_FINAL_L2, "L3": C34_FINAL_OPEN}
        },
        "expectation_derivation": _provenance("894-917"),
        "comparison_rule": COMPARISON_RULE_ID,
        "clean_producer_corroboration": _authority(
            ("A_CURRENT_MASTER", EXECUTION_OBSERVATION)
        ),
        "producer_mutation": _mutation(
            "C34",
            "mtc_v2/core/runner.py",
            "fbd4d97a7f39a4c69c3c8163e47618f6c36f574ed59f7284e33225cfc6401eed",
            "548b0ed866501ecb61bd61a68a1e166a7d10cfb1708abd2acaeeacc239edf565",
            "$.final_state.arms.L2.position",
        ),
    },
    "C42": {
        "scenario_id": "C42-LEGACY-001",
        "producer_adapter": "A.signal_producers_stage3",
        "complete_inputs": {
            "common_config": {
                "use_confirm_transform": False,
                "use_level_retest": False,
                "use_l18b_confirmation": False,
                "use_sl": False,
                "use_sl_percent": False,
                "use_sl_atr": False,
                "use_sl_swing_atr": False,
                "tp_mode": "None",
                "max_entries": 1,
                "exit_on_opposite_signal": True,
                "allow_flip": True,
                "cooldown_bars": 0,
                "regime_lock": False,
                "initial_capital": 1000.0,
                "fallback_size_pct": 11.5,
                "instrument_price_tick": 0.01,
                "instrument_qty_step": 1.0,
                "instrument_min_qty": 0.0,
                "instrument_min_notional": 0.0,
                "instrument_contract_multiplier": 1.0,
            },
            "arms": {
                "F1": {"config": {"signal_mode": "Supertrend", "st_atr_len": 1, "st_factor": 1.0, "st_use_wicks": False, "st_use_ha": True}, "bars": C42_COMMON_BARS},
                "F2": {"config": {"signal_mode": "Supertrend", "st_atr_len": 1, "st_factor": 1.0, "st_use_wicks": False, "st_use_ha": False}, "bars": C42_COMMON_BARS},
                "F3_CLOSE": {"config": {"signal_mode": "Supertrend", "st_atr_len": 1, "st_factor": 1.0, "st_use_wicks": False, "st_use_ha": False}, "bars": C42_COMMON_BARS[:2]},
                "F3_WICK": {"config": {"signal_mode": "Supertrend", "st_atr_len": 1, "st_factor": 1.0, "st_use_wicks": True, "st_use_ha": False}, "bars": C42_F3_WICK_BARS},
                "F4": {"config": {"signal_mode": "Range Filter", "rf_range": 10.0}, "bars": C42_F4_BARS},
            },
        },
        "literal_expected_observation": {"arms": C42_EXPECTED_ARMS},
        "literal_expected_final_state": {"arms": C42_FINAL_ARMS},
        "expectation_derivation": _provenance("1231-1276"),
        "comparison_rule": COMPARISON_RULE_ID,
        "clean_producer_corroboration": _authority(
            ("A_CURRENT_MASTER", EXECUTION_OBSERVATION),
            ("PINE_CURRENT_MASTER", SOURCE_CORROBORATION),
        ),
        "producer_mutation": _mutation(
            "C42",
            "mtc_v2/signals/range_filter.py",
            "75d752d8f6a0d251cd99f55adc71c46dc63cc4259beda48c407e7de2326cb197",
            "716cd0bddc28df03c85f493f80fa071375bbb362a598d762de41c7662f568c15",
            "$.observation.arms.F4.raw_signals[2].short",
        ),
    },
}


def stage3_oracle_mappings() -> dict[str, dict[str, Any]]:
    return deepcopy(dict(_CONTRACTS))


def stage3_oracle_mapping(row_id: str) -> dict[str, Any]:
    try:
        return deepcopy(dict(_CONTRACTS[row_id]))
    except KeyError as exc:
        raise KeyError(f"stage-3 oracle is absent: {row_id}") from exc


def stage3_required_authority_modes(row_id: str) -> tuple[tuple[str, str], ...]:
    contract = stage3_oracle_mapping(row_id)
    return tuple(
        (item["name"], item["evidence_mode"])
        for item in contract["clean_producer_corroboration"]["authority_requirements"]
    )
