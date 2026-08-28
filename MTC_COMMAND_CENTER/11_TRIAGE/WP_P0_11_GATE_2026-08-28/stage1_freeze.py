from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any


GATE_VERSION = "P011-LC-GATE-v2"
SOURCE_COMMIT = "5c5603065c994d545c0eaa8c137fa9edd5cdfc28"
A_TREE_OID = "7aa6f867d821df08a00358adf2dd4400b9c719e8"
PINE_FREEZE_COMMIT = "77a10e6573d93f8aaf777010ea507bbec0a7668b"
B_FREEZE_COMMIT = "b5ed1afadcff09b69e36b72affeb23de51d84c14"
P009_AUTHORITY_COMMIT = "85c3e17f97efa1ba83ef9c679de319a50ad3be04"
P009_BLOB_OID = "1c39ab939dfcf5589e5ec8fba4af8966947a67fc"
P009_SHA256 = "7d48871a3e45dab118e97969d701912edb5d7c16a4d822d816beca1d03a42249"
FIXTURE_SHA256 = "3a3a4939fc8e1b725112115971e2663ddbcc1ea5981c37aa1d02d8bc3674a7bb"
UPSTREAM_MANIFEST_SHA256 = "b4daced1367fabc107a692be03f234af11f0c908bfd2b60d6c65ed23c4de5ea6"
UPSTREAM_NORMALIZED_SHA256 = "521d30ca5cf340ab3ed37a738fe76e1c4651781d91b797c791ea67f92d89cbac"
V1_ANCHOR_SHA256 = "eb6a600ff9609789465118a217845c7cac6f8b09f7ecaee2a93242f1f16ec15c"
OWNER_AUTHORIZATION_SHA256 = "d5da5c81df38de31b629605cd972ce3d9df19185573f6d4018782cae8f2b2ef3"

GATE_DIR = Path(__file__).resolve().parent
REPO_ROOT = GATE_DIR.parents[2]
PROFILE_DIR = GATE_DIR / "profiles"
ANCHOR_PATH = Path(r"C:\LAB\P011_TRUST_ANCHORS\P011-LC-GATE-v2.owner-signed.json")
V1_ANCHOR_PATH = Path(r"C:\LAB\P011_TRUST_ANCHORS\P011-LC-GATE-v1.owner-signed.json")
FIXTURE_PATH = REPO_ROOT / "IBKR_PAPER_BRIDGE" / "tests" / "fixtures" / "BTC_1h_real.csv"
P009_PATH = (
    REPO_ROOT
    / "MTC_COMMAND_CENTER"
    / "11_TRIAGE"
    / "WP_P0_09_CAPABILITY_TABLE_2026-08-25"
    / "CAPABILITY_CANONICALIZATION_TABLE.md"
)
OWNER_AUTHORIZATION_PATH = Path(r"C:\tmp\LANE_PROMPTS_20260828\OWNER_AUTH_P011_GATE_V2.md")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        errors="strict",
        capture_output=True,
        check=True,
    )
    return completed.stdout.strip()


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def verify_fixed_inputs() -> dict[str, Any]:
    if git("rev-parse", "5c560306:MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2") != A_TREE_OID:
        raise SystemExit("STOP: implementation A tree OID mismatch")
    if git("rev-parse", "HEAD:MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2") != A_TREE_OID:
        raise SystemExit("STOP: implementation A HEAD tree differs from the frozen source")
    if git("diff", "--name-only", "--", "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2"):
        raise SystemExit("STOP: implementation A has worktree edits")
    if git("rev-parse", "legacy/pine-controller/2026-08-25^{commit}") != PINE_FREEZE_COMMIT:
        raise SystemExit("STOP: controller freeze tag mismatch")
    if git("rev-parse", "legacy/02-mtc-backtest/2026-08-25^{commit}") != B_FREEZE_COMMIT:
        raise SystemExit("STOP: B freeze tag mismatch")
    p009_rel = "MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/CAPABILITY_CANONICALIZATION_TABLE.md"
    if git("rev-parse", f"{P009_AUTHORITY_COMMIT}:{p009_rel}") != P009_BLOB_OID:
        raise SystemExit("STOP: P0-09 authority blob mismatch")
    if git("rev-parse", f"master:{p009_rel}") != P009_BLOB_OID:
        raise SystemExit("STOP: current master P0-09 authority blob mismatch")
    if sha256_file(P009_PATH) != P009_SHA256:
        raise SystemExit("STOP: P0-09 worktree bytes mismatch")
    if not V1_ANCHOR_PATH.is_file() or sha256_file(V1_ANCHOR_PATH) != V1_ANCHOR_SHA256:
        raise SystemExit("STOP: retained v1 external anchor differs")
    if not OWNER_AUTHORIZATION_PATH.is_file() or sha256_file(OWNER_AUTHORIZATION_PATH) != OWNER_AUTHORIZATION_SHA256:
        raise SystemExit("STOP: v2 owner authorization basis differs")
    if sha256_file(FIXTURE_PATH) != FIXTURE_SHA256:
        raise SystemExit("STOP: BTC fixture SHA-256 mismatch")

    with FIXTURE_PATH.open("r", encoding="utf-8", newline="") as handle:
        header = handle.readline().rstrip("\r\n")
        first = handle.readline().rstrip("\r\n")
        count = 1
        last = first
        for line in handle:
            count += 1
            last = line.rstrip("\r\n")
    if header != "ts,open,high,low,close,volume":
        raise SystemExit("STOP: BTC fixture header mismatch")
    if count != 48077:
        raise SystemExit(f"STOP: BTC fixture row count mismatch: {count}")
    if not first.startswith("2021-01-01T06:00:00+00:00,"):
        raise SystemExit("STOP: BTC fixture first timestamp mismatch")
    if not last.startswith("2026-06-28T00:00:00+00:00,"):
        raise SystemExit("STOP: BTC fixture last timestamp mismatch")
    return {"header": header, "row_count": count, "first_row": first, "last_row": last}


def build_profiles() -> list[dict[str, Any]]:
    source_root = REPO_ROOT / "MTC_COMMAND_CENTER" / "01_MTC_PROJECT" / "00_PYTHON"
    sys.path.insert(0, str(source_root))
    from mtc_v2.core.config import resolve_config

    definitions = [
        ("mtc_v2_legacy_supertrend_default_v1", "Supertrend"),
        ("mtc_v2_legacy_range_filter_default_v1", "Range Filter"),
    ]
    results: list[dict[str, Any]] = []
    for profile_id, signal_mode in definitions:
        resolved = resolve_config(
            {
                "instrument_symbol": "BTCUSD",
                "signal_mode": signal_mode,
                "execution_profile_id": "close_only_deterministic_v2",
            }
        )
        snapshot = {
            "profile_schema_version": "P011_RESOLVED_CONFIG_v1",
            "profile_id": profile_id,
            "producer": "A_MTC_V2_RUNNER",
            "source_commit": SOURCE_COMMIT,
            "source_tree_oid": A_TREE_OID,
            "resolution_function": "mtc_v2.core.config.resolve_config(validate=True)",
            "explicit_inputs": {
                "instrument_symbol": "BTCUSD",
                "signal_mode": signal_mode,
                "execution_profile_id": "close_only_deterministic_v2",
            },
            "resolved_config": resolved,
            "claim_limit": "deterministic capture profile; not an instrument-faithful BTC profile",
        }
        path = PROFILE_DIR / f"{profile_id}.json"
        write_json(path, snapshot)
        results.append(
            {
                "profile_id": profile_id,
                "path": path.relative_to(REPO_ROOT).as_posix(),
                "sha256": sha256_file(path),
                "resolved_key_count": len(resolved),
            }
        )
    return results


def field(path: str, kind: str, nullable: bool, encoding: str, owner: str, ordering: str = "n/a") -> dict[str, Any]:
    return {
        "path": path,
        "type": kind,
        "nullable": nullable,
        "encoding": encoding,
        "owning_record": owner,
        "ordering": ordering,
    }


def build_schema() -> dict[str, Any]:
    fields: list[dict[str, Any]] = [
        field("schema_version", "string", False, "UTF-8 exact literal P011_OBSERVATION_SCHEMA_v1", "observation"),
        field("profile_id", "string", False, "UTF-8 exact", "observation"),
        field("bar_index", "integer", False, "JSON base-10 integer", "observation"),
        field("timestamp", "string", False, "ISO-8601 with explicit UTC offset", "observation"),
    ]
    for name in ("open", "high", "low", "close", "volume"):
        fields.append(field(f"input.{name}", "float", False, "Python float.hex() string", "input"))
    for signal_owner in ("raw_signal", "gated_signal"):
        fields.extend(
            [
                field(f"{signal_owner}.long", "boolean", False, "JSON boolean", signal_owner),
                field(f"{signal_owner}.short", "boolean", False, "JSON boolean", signal_owner),
                field(f"{signal_owner}.reason", "string", True, "UTF-8 exact or null", signal_owner),
                field(f"{signal_owner}.direction", "integer", True, "JSON base-10 integer or null", signal_owner),
                field(f"{signal_owner}.line", "float", True, "Python float.hex() string or null", signal_owner),
            ]
        )
    event_types = {
        "event_ordinal": ("integer", False, "JSON base-10 integer"),
        "event_kind": ("string", False, "UTF-8 exact ENTRY or EXIT"),
        "side": ("string", False, "UTF-8 exact long or short"),
        "reason": ("string", True, "UTF-8 exact or null"),
        "price": ("float", False, "Python float.hex() string"),
        "qty": ("float", False, "Python float.hex() string"),
        "lifecycle_id": ("integer", False, "JSON base-10 integer"),
        "exit_id": ("string", True, "UTF-8 exact or null"),
        "realized_pnl": ("float", True, "Python float.hex() string or null"),
        "was_partial": ("boolean", False, "JSON boolean"),
        "was_pessimistic": ("boolean", False, "JSON boolean"),
    }
    for name, (kind, nullable, encoding) in event_types.items():
        fields.append(field(f"events[*].{name}", kind, nullable, encoding, "event", "event_ordinal ascending"))
    position_types = {
        "present": ("boolean", False),
        "lifecycle_id": ("integer", True),
        "side": ("string", True),
        "entry_price": ("float", True),
        "avg_entry_price": ("float", True),
        "qty": ("float", True),
        "entry_bar": ("integer", True),
        "initial_qty": ("float", True),
        "active_stop_price": ("float", True),
        "active_tp_price": ("float", True),
        "active_stop_owner": ("string", True),
        "be_active": ("boolean", False),
        "trail_active": ("boolean", False),
        "trail_price": ("float", True),
        "initial_risk_per_unit": ("float", True),
        "working_exit_reference_qty": ("float", True),
        "working_exit_book_version": ("integer", True),
    }
    for name, (kind, nullable) in position_types.items():
        encoding = "Python float.hex() string or null" if kind == "float" else (
            "JSON base-10 integer or null" if kind == "integer" else "JSON boolean" if kind == "boolean" else "UTF-8 exact or null"
        )
        fields.append(field(f"position.{name}", kind, nullable, encoding, "position"))
    for name, kind in (("entry_price", "float"), ("qty", "float"), ("entry_bar", "integer")):
        fields.append(field(f"position.entry_legs[*].{name}", kind, False, "Python float.hex() string" if kind == "float" else "JSON base-10 integer", "entry_leg", "source list order"))
    for name, kind, nullable in (
        ("exit_id", "string", False),
        ("kind", "string", False),
        ("target_price", "float", True),
        ("stop_price", "float", True),
        ("qty_fraction", "float", False),
        ("book_version", "integer", False),
        ("active", "boolean", False),
    ):
        encoding = "Python float.hex() string" + (" or null" if nullable else "") if kind == "float" else (
            "JSON base-10 integer" if kind == "integer" else "JSON boolean" if kind == "boolean" else "UTF-8 exact"
        )
        fields.append(field(f"position.working_exits[*].{name}", kind, nullable, encoding, "working_exit", "source list order"))
    fields.append(field("position.completed_exit_ids[*]", "string", False, "UTF-8 exact", "position", "lexicographically sorted"))
    for name, kind, nullable in (
        ("warmup_bars", "integer", False),
        ("block_new_entries_this_bar", "boolean", False),
        ("opened_this_bar_reason", "string", True),
        ("closed_this_bar_reason", "string", True),
        ("gated_long", "boolean", False),
        ("gated_short", "boolean", False),
    ):
        encoding = "JSON base-10 integer" if kind == "integer" else "JSON boolean" if kind == "boolean" else "UTF-8 exact or null"
        fields.append(field(f"gate_readiness.{name}", kind, nullable, encoding, "gate_readiness"))
    for name, kind, nullable in (
        ("gate_name", "string", False),
        ("long_ok", "boolean", False),
        ("short_ok", "boolean", False),
        ("value", "float", True),
        ("category", "string", False),
    ):
        encoding = "Python float.hex() string or null" if kind == "float" else "JSON boolean" if kind == "boolean" else "UTF-8 exact"
        fields.append(field(f"gate_readiness.gate_results[*].{name}", kind, nullable, encoding, "gate_result", "gate_name ascending"))
    for name, kind in (
        ("equity", "float"),
        ("realized_equity", "float"),
        ("unrealized_pnl", "float"),
        ("last_sizing_equity_snapshot", "float"),
        ("total_entries", "integer"),
        ("total_exits", "integer"),
    ):
        fields.append(field(f"account.{name}", kind, False, "Python float.hex() string" if kind == "float" else "JSON base-10 integer", "account"))
    fields.append(field("state_digest", "string", False, "lowercase SHA-256 hex over the canonical state preimage", "observation"))

    state_components = [
        item["path"]
        for item in fields
        if item["path"].startswith(("events[*].", "position.", "gate_readiness.", "account."))
    ]
    return {
        "schema_version": "P011_OBSERVATION_SCHEMA_v1",
        "closed": True,
        "unknown_field_policy": "STOP",
        "top_level_paths": [
            "schema_version",
            "profile_id",
            "bar_index",
            "timestamp",
            "input",
            "raw_signal",
            "gated_signal",
            "events",
            "position",
            "gate_readiness",
            "account",
            "state_digest",
        ],
        "csv_binding": {
            "exact_header": "ts,open,high,low,close,volume",
            "timestamp_source": "ts",
            "numeric_sources": ["open", "high", "low", "close", "volume"],
            "bar_index_derivation": "zero-based physical data-row ordinal after the header",
            "rejects": ["supplied index column", "skipped ordinal", "timestamp/index disagreement", "duplicate observation identity"],
        },
        "float_contract": "Every IEEE-754 value is encoded with Python float.hex(); comparison is exact and has no tolerance.",
        "array_contracts": {
            "events": "ordered by event_ordinal; duplicate ordinals are invalid",
            "entry_legs": "producer order",
            "working_exits": "producer order",
            "completed_exit_ids": "lexicographically sorted",
            "gate_results": "gate_name ascending",
        },
        "field_catalog": fields,
        "digest_catalog": {
            "state_digest_algorithm": "sha256(canonical_json({events,position,gate_readiness,account}))",
            "canonical_json": "UTF-8, sort_keys=true, separators=(',', ':'), ensure_ascii=false, allow_nan=false",
            "state_digest_components": state_components,
            "event_component_paths": [item for item in state_components if item.startswith("events[*].")],
        },
        "excluded_fields": [
            {"path": "Bar.indicators", "reason": "caller-supplied auxiliary map; not used by the two frozen profiles"},
            {"path": "Bar.htf", "reason": "legacy compatibility alias map; the frozen profiles do not provide HTF data"},
            {"path": "PortfolioState.current_bar_index", "reason": "duplicate of observation.bar_index"},
            {"path": "PortfolioState.last_entry_bar_index", "reason": "derivable lifecycle diagnostic not declared in v1"},
            {"path": "PortfolioState.last_exit_bar_index", "reason": "derivable from ordered events"},
            {"path": "PortfolioState.last_exit_price/qty/id/reason flags", "reason": "represented losslessly in ordered events"},
            {"path": "PortfolioState.initial_capital", "reason": "pinned in the full resolved config snapshot"},
            {"path": "PortfolioState.execution_profile_id", "reason": "pinned by profile_id and resolved config"},
            {"path": "PortfolioState.instrument", "reason": "pinned in the full resolved config snapshot"},
            {"path": "PortfolioState.indicator_snapshot", "reason": "internal calculation state; raw and gated producer outputs are observed instead"},
            {"path": "PortfolioState.regime_lock_side", "reason": "undeclared internal control state in schema v1"},
            {"path": "PortfolioState.next_position_lifecycle_id", "reason": "next-id allocator internal; active/event lifecycle IDs are observed"},
            {"path": "Runner private trackers and histories", "reason": "undeclared implementation internals"},
            {"path": "Runner debug metadata", "reason": "debug-only and configuration-redundant"},
            {"path": "arbitrary repr/object address/unordered set iteration", "reason": "non-canonical and forbidden"},
        ],
    }


ROW_TITLES = [
    "Raw signal production, conflict, direction",
    "Entry gates, readiness, signal filters",
    "N-bar confirmation transform and refresh",
    "Level retest confirmation",
    "Direction, regime lock, opposite signal, flip",
    "Pyramiding, adds, entry spacing, exit cooldown",
    "Sizing request and quantity ownership",
    "Contract multiplier",
    "Tick/quantity rounding and minimums",
    "Leverage and margin/liquidation",
    "Fixed/ATR/swing stops",
    "Percent/ATR/R targets",
    "MultiTP",
    "Break-even",
    "Trailing stop",
    "Opposite/filter exits",
    "Bar/time/PnL exits",
    "Session/day limits, guards, recovery",
    "Same-bar stop/target collision",
    "Fill assumptions and gaps",
    "Same-bar re-entry after any exit",
    "Fees, slippage, funding",
    "Warm-up, evaluation boundary, terminal handling",
    "Invalid values, boundary equality, short symmetry",
    "Timestamp discipline",
    "Duplicate/reordered bars, revisions, idempotence",
    "Restart and missed-decision recovery",
    "WunderTrading route-code inputs",
    "WunderTrading order-payload inputs",
    "WunderTrading protective flags",
    "tw_audit_semantics_mode",
    "tw_reversal_reentry_mode",
    "tw_reversal_reentry_delay_bars",
    "tw_margin_call_mode",
    "tw_margin_call_split_entries",
    "tw_be_semantics_mode",
    "tw_trailing_semantics_mode",
    "Swing-break/pivot confirmation state machine",
    "Entry-event mode and first-eval-bar edge requirement",
    "Higher-timeframe series construction and alignment",
    "Indicator readiness substitution and MA/MACD equation authority",
    "Signal-producer equation authority",
]

ROW_STARTS = [131, 149, 167, 204, 227, 245, 289, 324, 342, 360, 411, 429, 447, 465, 483, 501, 519, 537, 555, 575, 606, 624, 642, 660, 678, 696, 714, 746, 766, 790, 810, 830, 871, 894, 918, 938, 972, 995, 1077, 1097, 1147, 1207]


ROW_SCENARIOS: dict[int, dict[str, Any]] = {
    1: {"op": "A.runner_candidate_side", "inputs": {"long": True, "short": True, "reason": "fixture_conflict", "direction": 1, "line": 100.0}, "expected": {"candidate_side": None, "gated_long": False, "gated_short": False, "reason": "signal_conflict"}, "final": {"position_present": False}},
    2: {"op": "A.gates_legacy_fail_open", "inputs": {"ma_close": 100.0, "ma_line": None, "htf_ready": False, "htf_close": None}, "expected": {"ma_long_ok": True, "ma_short_ok": True, "htf_long_ok": True, "htf_short_ok": True}, "final": {"gate_evaluation": "legacy_fail_open"}},
    3: {"op": "A.runner_confirmation_refresh", "inputs": {"confirm_bars": 2, "refresh_on_new_raw": True, "raw_directions": [1, 1]}, "expected": {"confirm_count_after_new_pulse": 0, "confirm_count_after_hold": 1, "fired": False}, "final": {"confirm_direction": 1}},
    4: {"op": "A.runner_level_retest", "inputs": {"break_level": 100.0, "buffer_pct": 0.1, "bar": {"open": 100.05, "high": 100.06, "low": 100.04, "close": 100.05}}, "expected": {"distance_pct": 0.05, "retest_fires": True, "touch_or_cross_required": False, "close_back_required": False}, "final": {"waiting": False}},
    5: {"op": "A.runner_opposite_signal", "inputs": {"allow_flip": False, "initial_side": "long", "opposite_raw_side": "short"}, "expected": {"ordered_exit_reasons": ["opp_signal"], "same_bar_short_entry": False, "deferred_side": "short"}, "final": {"position_present": False}},
    6: {"op": "A.position_manager_spacing", "inputs": {"max_entries": 2, "cooldown_bars": 2, "entry_bar_indices": [10, 11, 12], "side": "long"}, "expected": {"can_open": [True, False, True], "active_entry_legs": 2}, "final": {"position_side": "long"}},
    7: {"op": "A.position_sizer_fixed", "inputs": {"entry_price": 100.0, "stop_price": 90.0, "sizing_equity": 1000.0, "fixed_qty": 1.0, "qty_step": 1.0}, "expected": {"qty": 1.0, "owner": "legacy_kernel"}, "final": {"sizing_snapshot": 1000.0}},
    8: {"op": "A.position_manager_multiplier_pnl", "inputs": {"side": "long", "entry_price": 100.0, "exit_price": 110.0, "qty": 3.0, "contract_multiplier": 2.0}, "expected": {"realized_pnl": 60.0}, "final": {"realized_equity_delta": 60.0}},
    9: {"op": "A.rounding", "inputs": {"price_tick": 0.01, "long_stop": 99.999, "long_target": 100.005, "raw_qty": 1.999, "qty_step": 0.1}, "expected": {"rounded_long_stop": 99.99, "rounded_long_target": 100.01, "floored_qty": 1.9}, "final": {"below_minimum_rejected": True}},
    10: {"op": "A.runner_capital_block", "inputs": {"entry_price": 100.0, "qty": 11.0, "sizing_equity": 1000.0, "max_leverage_cap": 1.0}, "expected": {"notional": 1100.0, "limit": 1000.0, "blocked": True}, "final": {"position_present": False}},
    11: {"op": "A.exits_stop_gap", "inputs": {"side": "long", "entry_price": 100.0, "active_stop_price": 95.0, "bar": {"open": 90.0, "high": 101.0, "low": 89.0, "close": 92.0}}, "expected": {"hit": True, "reason": "stop_loss", "fill_price": 90.0}, "final": {"position_present": False}},
    12: {"op": "A.exits_target_gap", "inputs": {"side": "long", "entry_price": 100.0, "active_tp_price": 105.0, "bar": {"open": 110.0, "high": 112.0, "low": 109.0, "close": 111.0}}, "expected": {"hit": True, "reason": "take_profit", "fill_price": 110.0}, "final": {"position_present": False}},
    13: {"op": "A.exits_multitp", "inputs": {"side": "long", "entry_price": 100.0, "qty": 10.0, "targets": [{"id": "TP1", "price": 105.0, "fraction": 0.5}, {"id": "TP2", "price": 110.0, "fraction": 1.0}], "bar_high": 111.0}, "expected": {"ordered_exit_ids": ["TP1", "TP2"], "exit_qtys": [5.0, 5.0], "realized_pnls": [25.0, 50.0]}, "final": {"position_present": False, "realized_equity_delta": 75.0}},
    14: {"op": "A.exits_break_even_legacy", "inputs": {"side": "long", "entry_price": 100.0, "initial_stop": 90.0, "trigger_r": 1.0, "buffer_r": 0.1, "bar_close": 111.0, "tw_mode": "local"}, "expected": {"be_active": True, "active_stop_price": 101.0, "active_stop_owner": "break_even"}, "final": {"position_present": True}},
    15: {"op": "A.exits_trailing_legacy", "inputs": {"side": "long", "entry_price": 100.0, "initial_stop": 90.0, "trail_atr": 2.0, "trail_distance_atr_mult": 1.0, "bar_close": 110.0}, "expected": {"trail_active": True, "trail_price": 108.0, "active_stop_owner": "trailing"}, "final": {"position_present": True}},
    16: {"op": "A.runner_exit_order", "inputs": {"position_side": "long", "active_stop": 95.0, "bar_low": 94.0, "raw_side": "short", "filter_blocked": True}, "expected": {"first_exit_reason": "stop_loss", "opposite_exit_count": 0, "filter_exit_count": 0}, "final": {"position_present": False}},
    17: {"op": "A.runner_time_exit", "inputs": {"entry_bar": 0, "current_bar": 2, "time_stop_bars": 2, "time_stop_condition": "Always", "close": 101.0}, "expected": {"exit_reason": "time_stop", "exit_price": 101.0}, "final": {"position_present": False}},
    18: {"op": "A.runner_local_guard", "inputs": {"use_max_trades_per_day": True, "max_trades_per_day": 1, "trades_today": 1, "candidate_side": "long"}, "expected": {"guard_blocked": True, "entry_opened": False}, "final": {"position_present": False, "trades_today": 1}},
    19: {"op": "A.exits_collision", "inputs": {"side": "long", "stop_price": 95.0, "target_price": 105.0, "bar": {"open": 100.0, "high": 106.0, "low": 94.0, "close": 101.0}}, "expected": {"exit_reason": "stop_loss", "policy_observed": "STOP_FIRST"}, "final": {"position_present": False}},
    20: {"op": "A.runner_close_only_fill", "inputs": {"execution_profile_id": "close_only_deterministic_v2", "candidate_side": "long", "bar_close": 100.0}, "expected": {"entry_fill_price": 100.0, "fill_policy_id": "decision_bar_close"}, "final": {"position_side": "long"}},
    21: {"op": "A.runner_protective_reentry", "inputs": {"tw_audit_semantics_mode": "off", "position_side": "long", "stop_hit": True, "same_bar_candidate": "short"}, "expected": {"protective_exit_count": 1, "same_bar_entry_count": 0}, "final": {"position_present": False}},
    22: {"op": "A.position_manager_legacy_cost_absence", "inputs": {"side": "long", "entry_price": 100.0, "exit_price": 110.0, "qty": 1.0, "fee": 0.0, "slippage": 0.0, "funding": 0.0}, "expected": {"gross_pnl": 10.0, "realized_pnl": 10.0}, "final": {"unmodeled_costs": ["fee", "slippage", "funding"]}},
    23: {"op": "A.runner_warmup_terminal", "inputs": {"signal_mode": "Supertrend", "bars": 20, "st_atr_len": 21, "terminal_flatten": False}, "expected": {"observations": 20, "entries": 0, "implicit_terminal_exit": False}, "final": {"position_preserved_at_end": True}},
    24: {"op": "A.runner_invalid_bar", "inputs": {"bar": {"open": 100.0, "high": 101.0, "low": 99.0, "close": "NaN", "volume": 1.0}, "side_mirror": ["long", "short"]}, "expected": {"bar_valid": False, "entry_opened": False, "boundary_rule": "legacy_exact_comparisons"}, "final": {"position_present": False}},
    26: {"op": "A.runner_duplicate_bar_legacy", "inputs": {"bars": [{"bar_index": 7, "timestamp": "2026-01-01T00:00:00+00:00"}, {"bar_index": 7, "timestamp": "2026-01-01T00:00:00+00:00"}]}, "expected": {"producer_outputs": 2, "duplicate_rejected_by_legacy_runner": False}, "final": {"last_current_bar_index": 7}},
    28: {"op": "A_FREEZE.resolve_config_route_keys", "inputs": {"wt_enter_long_code": "EL", "wt_exit_long_code": "XL", "wt_enter_short_code": "ES", "wt_exit_short_code": "XS", "wt_exit_all_code": "XA"}, "expected": {"preserved_values": ["EL", "XL", "ES", "XS", "XA"]}, "final": {"route_key_count": 5}},
    29: {"op": "A_FREEZE.resolve_config_payload_keys", "inputs": {"wt_order_type": "limit", "wt_amount_type": "base", "wt_amount": 2.5, "wt_leverage": 3}, "expected": {"order_type": "limit", "amount_type": "base", "amount": 2.5, "leverage": 3}, "final": {"payload_key_count": 4}},
    30: {"op": "A_FREEZE.resolve_config_protective_keys", "inputs": {"use_tp": True, "use_sl": True, "wt_use_tp": True, "wt_use_sl": True, "wt_reduce_only": True, "wt_place_cond_orders": True}, "expected": {"wt_use_tp": True, "wt_use_sl": True, "wt_reduce_only": True, "wt_place_cond_orders": True}, "final": {"protective_key_count": 4, "cross_validation": "PASS"}},
    31: {"op": "A.runner_tw_master_switch", "inputs": {"modes": ["off", "research"], "protective_exit": True}, "expected": {"off_pending_reentry": None, "research_branch_reachable": True}, "final": {"mode_count": 2}},
    32: {"op": "A.resolve_config_reentry_enum", "inputs": {"accepted_values": ["local", "carry_to_next_bar_after_protective_exit", "next_bar_open", "next_bar_close"]}, "expected": {"all_values_validate": True}, "final": {"enum_count": 4}},
    33: {"op": "A.runner_reentry_delay", "inputs": {"delay_bars": 2, "protective_exit_bar": 10, "candidate_bars": [10, 11, 12]}, "expected": {"reentry_allowed": [False, False, True]}, "final": {"first_allowed_bar": 12}},
    34: {"op": "A.runner_margin_call", "inputs": {"tw_audit_semantics_mode": "research", "tw_margin_call_mode": "tradingview", "side": "long", "entry_price": 100.0, "mark_price": 40.0, "qty": 10.0, "margin_long_pct": 100.0}, "expected": {"margin_call_branch_reached": True, "exit_reason": "margin_call"}, "final": {"total_exits": 1}},
    35: {"op": "A.runner_split_entries_stamp", "inputs": {"tw_margin_call_split_entries": True, "debug_mode": True}, "expected": {"debug_metadata_value": True, "economic_branch_count": 0}, "final": {"position_change_from_flag_only": False}},
    36: {"op": "A.runner_be_mode", "inputs": {"tw_audit_semantics_mode": "research", "tw_be_semantics_mode": "tradingview", "trigger_reached": True}, "expected": {"tradingview_be_branch_reached": True}, "final": {"be_active": True}},
    37: {"op": "A.runner_trailing_mode", "inputs": {"tw_audit_semantics_mode": "research", "tw_trailing_semantics_mode": "tradingview", "trigger_reached": True}, "expected": {"tradingview_trailing_branch_reached": True}, "final": {"trail_active": True}},
    38: {"op": "B_FREEZE.pivot_fsm", "inputs": {"wait_long": True, "wait_long_start_bar": 0, "bar_index": 1, "long_level": 100.0, "mintick": 1.0, "break_buffer_ticks": 1, "close": 102.0, "high": 102.0, "min_wait_bars": 1, "require_close_beyond": True}, "expected": {"long_break_level": 101.0, "long_age_ok": True, "long_pulse": True}, "final": {"waits_reset": True}},
    39: {"op": "B_FREEZE.entry_event_mode", "inputs": {"raw_long": [True, True], "entry_modes": ["Edge", "Signal"], "first_bar_requires_edge": True}, "expected": {"edge_long": [True, False], "signal_long": [True, True], "first_eval_bar_blocked_without_edge": True}, "final": {"mode_count": 2}},
    40: {"op": "A.htf_prior_closed_lookup", "inputs": {"ltf_timestamp": "2026-01-01T10:30:00+00:00", "declared_htf_minutes": 60, "completed_htf_closes": [{"timestamp": "2026-01-01T10:00:00+00:00", "close": 100.0}, {"timestamp": "2026-01-01T11:00:00+00:00", "close": 200.0}]}, "expected": {"selected_close": 100.0, "future_close_used": False}, "final": {"selected_timestamp": "2026-01-01T10:00:00+00:00"}},
    41: {"op": "A.gates_readiness_substitution", "inputs": {"ma_line": None, "close": 100.0, "htf_ready": True, "htf_close": 101.0, "htf_ma_line": None}, "expected": {"missing_ltf_ma_passes": True, "htf_substituted_value": 101.0}, "final": {"legacy_substitution_observed": True}},
    42: {"op": "A.signal_producers", "inputs": {"supertrend": {"st_use_ha": True, "bar_count": 3}, "range_filter": {"rf_range": 1000.0, "prices": [100.0, 101.0, 99.0]}}, "expected": {"supertrend_signals": [{"long": False, "short": False, "reason": "st_ha_not_supported"}, {"long": False, "short": False, "reason": "st_ha_not_supported"}, {"long": False, "short": False, "reason": "st_ha_not_supported"}], "range_filter_event_count": 0}, "final": {"producer_count": 2}},
}


def row_authorities(row_number: int) -> list[dict[str, Any]]:
    if row_number in (28, 29, 30):
        return [
            {
                "name": "A_PINE_CONTROLLER_FREEZE",
                "ref": "legacy/pine-controller/2026-08-25",
                "commit": PINE_FREEZE_COMMIT,
                "paths": [
                    "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py",
                    "MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine",
                ],
                "role": "legacy authority; current master is prohibited for this deleted surface",
            }
        ]
    if row_number == 26:
        return [
            {"name": "A_CURRENT_MASTER", "commit": SOURCE_COMMIT, "tree_oid": A_TREE_OID, "role": "legacy runner duplicate/revision behavior"},
            {"name": "PINE_CONTROLLER_FREEZE", "ref": "legacy/pine-controller/2026-08-25", "commit": PINE_FREEZE_COMMIT, "role": "historical L25 dispatch corroboration only"},
        ]
    if row_number == 38:
        return [
            {"name": "B_BACKTEST_FREEZE", "ref": "legacy/02-mtc-backtest/2026-08-25", "commit": B_FREEZE_COMMIT, "path": "MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/modules/confirmation_layer.py", "role": "pivot FSM legacy authority"},
            {"name": "A_CURRENT_MASTER", "commit": SOURCE_COMMIT, "tree_oid": A_TREE_OID, "role": "inert scaffold preservation only"},
        ]
    if row_number in (39, 41):
        return [
            {"name": "A_CURRENT_MASTER", "commit": SOURCE_COMMIT, "tree_oid": A_TREE_OID, "role": "A legacy behavior"},
            {"name": "B_BACKTEST_FREEZE", "ref": "legacy/02-mtc-backtest/2026-08-25", "commit": B_FREEZE_COMMIT, "role": "B corroboration where carried"},
        ]
    if row_number in (3, 4, 42):
        return [
            {"name": "A_CURRENT_MASTER", "commit": SOURCE_COMMIT, "tree_oid": A_TREE_OID, "role": "executable Python authority"},
            {"name": "PINE_CURRENT_MASTER", "commit": SOURCE_COMMIT, "path": "MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine", "role": "equation/source corroboration only; no TradingView execution credit"},
        ]
    return [{"name": "A_CURRENT_MASTER", "commit": SOURCE_COMMIT, "tree_oid": A_TREE_OID, "role": "legacy executable authority"}]


def build_legacy_manifest() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for number, title in enumerate(ROW_TITLES, start=1):
        row_id = f"C{number:02d}"
        start = ROW_STARTS[number - 1]
        end = ROW_STARTS[number] - 1 if number < len(ROW_STARTS) else 1291
        p009_citation = {
            "path": P009_PATH.relative_to(REPO_ROOT).as_posix(),
            "git_blob_oid": P009_BLOB_OID,
            "sha256": P009_SHA256,
            "section_lines_at_pinned_blob": f"{start}-{end}",
        }
        if number in (25, 27):
            proof = (
                "already-decided venue timestamp policy; no A/B legacy implementation is reproduced"
                if number == 25
                else "ticket-45 freshness policy and P0-09 bounds; no A/B legacy implementation is reproduced"
            )
            rows.append(
                {
                    "row_id": row_id,
                    "title": title,
                    "disposition": "NOT_A_LEGACY_REPRODUCTION_ROW",
                    "p009_citation": p009_citation,
                    "proof": proof,
                    "coverage_credit": "policy consistency only; zero A/B/Pine reproduction credit",
                }
            )
            continue
        spec = ROW_SCENARIOS[number]
        rows.append(
            {
                "row_id": row_id,
                "title": title,
                "disposition": "APPLICABLE",
                "p009_citation": p009_citation,
                "legacy_authorities": row_authorities(number),
                "scenarios": [
                    {
                        "scenario_id": f"{row_id}-LEGACY-001",
                        "producer_adapter": spec["op"],
                        "complete_inputs": spec["inputs"],
                        "literal_expected_observation": spec["expected"],
                        "literal_expected_final_state": spec["final"],
                        "expectation_derivation": {
                            "method": "literal source arithmetic written before subject execution",
                            "source": p009_citation,
                            "producer_output_may_not_rebless_expected": True,
                        },
                        "comparison_rule": "canonical JSON exact equality; floats are compared as IEEE-754 hex in executable evidence",
                        "clean_producer_corroboration": {
                            "status": "FROZEN_PENDING_STAGE2_EXECUTION",
                            "required": True,
                            "authority_names": [item["name"] for item in row_authorities(number)],
                        },
                        "producer_mutation": {
                            "mutation_id": f"{row_id}-GF8-MUT-001",
                            "source_seam": spec["op"],
                            "mutation": "invert or perturb the scenario's primary returned predicate/value in an isolated scratch authority copy",
                            "required_red": f"{row_id}-LEGACY-001 exact comparison fails with one terminal row disposition",
                            "restored_green": "frozen clean authority exactly matches the literal oracle",
                            "status": "FROZEN_PENDING_STAGE2_EXECUTION",
                        },
                    }
                ],
            }
        )
    if len(rows) != 42 or len({item["row_id"] for item in rows}) != 42:
        raise AssertionError("legacy row universe must contain C01-C42 exactly once")
    applicable = sum(item["disposition"] == "APPLICABLE" for item in rows)
    not_rows = sum(item["disposition"] == "NOT_A_LEGACY_REPRODUCTION_ROW" for item in rows)
    return {
        "manifest_schema_version": "P011_LEGACY_MANIFEST_v1",
        "gate_version": GATE_VERSION,
        "dependency_variant": "DIRECT_BUILD",
        "fixture_suite_commit": "NONE_DIRECT_BUILD",
        "frozen_before_subject_run": True,
        "subject_run_count_at_freeze": 0,
        "expected_values_change_policy": "new owner decision, new gate version, new baseline and new external signature",
        "applicable_to_not_row_change_policy": "automatic STOP; never an in-place gate repair",
        "p009_authority": {
            "commit": P009_AUTHORITY_COMMIT,
            "blob_oid": P009_BLOB_OID,
            "sha256": P009_SHA256,
            "citation_resolution": "current-master section ranges plus source symbols; rules, oracles, and expected values are unchanged from v1",
            "citation_refresh_branch_status": "merged on master and owner-authorized as the v2 authority pin",
        },
        "separate_p009_non_decisions": [
            {
                "family": 18,
                "name": "snapshot drift / bucket-capital divergence",
                "disposition": "OUTSIDE_C01_C42_LEGACY_ROW_UNIVERSE_NO_CREDIT",
                "relationship_to_c18": "none",
            },
            {
                "family": 19,
                "name": "allocator / Guardian boundary",
                "disposition": "OUTSIDE_C01_C42_LEGACY_ROW_UNIVERSE_NO_CREDIT",
                "relationship_to_c18": "none",
            },
        ],
        "counts": {"total": 42, "applicable": applicable, "not_a_legacy_reproduction_row": not_rows},
        "rows": rows,
    }


def build_receipt(
    fixture_meta: dict[str, Any],
    profiles: list[dict[str, Any]],
    schema_hash: str,
    legacy_manifest_hash: str,
) -> dict[str, Any]:
    a_runner = "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py"
    return {
        "receipt_schema_version": "P011_GATE_RECEIPT_v1",
        "gate_version": GATE_VERSION,
        "receipt_state": "STAGE1_FROZEN_STAGE2_CANDIDATE_PENDING",
        "accepted_git_commit": SOURCE_COMMIT,
        "accepted_git_tree": git("rev-parse", f"{SOURCE_COMMIT}^{{tree}}"),
        "local_master_observed_at_freeze": git("rev-parse", "master"),
        "dependency_variant": "DIRECT_BUILD",
        "fixture_suite_commit": "NONE_DIRECT_BUILD",
        "source_identities": {
            "implementation_a": {
                "commit": SOURCE_COMMIT,
                "tree_oid": A_TREE_OID,
                "runner_path": a_runner,
                "runner_blob_oid": git("rev-parse", f"{SOURCE_COMMIT}:{a_runner}"),
            },
            "pine_current": {
                "commit": SOURCE_COMMIT,
                "path": "MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine",
                "blob_oid": git("rev-parse", f"{SOURCE_COMMIT}:MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine"),
                "role": "source corroboration only",
            },
            "controller_freeze": {"tag": "legacy/pine-controller/2026-08-25", "commit": PINE_FREEZE_COMMIT},
            "implementation_b_freeze": {"tag": "legacy/02-mtc-backtest/2026-08-25", "commit": B_FREEZE_COMMIT},
            "p009": {"commit": P009_AUTHORITY_COMMIT, "blob_oid": P009_BLOB_OID, "sha256": P009_SHA256},
        },
        "data_identities": {
            "emitted_fixture": {
                "path": FIXTURE_PATH.relative_to(REPO_ROOT).as_posix(),
                "sha256": FIXTURE_SHA256,
                **fixture_meta,
                "symbol": "BTCUSD",
                "timeframe": "1h",
                "timezone": "UTC",
                "market_schedule": "24/7",
            },
            "upstream": {
                "bundle": "native_multiasset_alpaca_2026-06-28",
                "provider": "alpaca_crypto",
                "source_symbol": "BTC/USD",
                "classification": "RESEARCH_ONLY_NOT_PROMOTABLE",
                "ohlcv_validation_status": "PASS",
                "manifest_sha256": UPSTREAM_MANIFEST_SHA256,
                "normalized_file_sha256": UPSTREAM_NORMALIZED_SHA256,
                "serialization_identity_note": "upstream normalized bytes and emitted fixture bytes are intentionally different identities",
            },
        },
        "resolved_profiles": profiles,
        "observation_schema": {
            "path": "MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_11_GATE_2026-08-28/P011_OBSERVATION_SCHEMA_v1.json",
            "sha256": schema_hash,
        },
        "legacy_manifest": {
            "path": "MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_11_GATE_2026-08-28/p011_legacy_manifest.json",
            "sha256": legacy_manifest_hash,
            "frozen_before_subject_run": True,
        },
        "producer_and_adapter_bindings": {
            "baseline_generator": {"path": "p011_gate.py", "sha256": None, "status": "PENDING_STAGE2"},
            "a_observation_adapter": {"path": "p011_gate.py", "sha256": None, "status": "PENDING_STAGE2", "required_call": "mtc_v2.core.runner.Runner.run once per profile"},
            "subject_adapter": {"path": None, "sha256": None, "resolved_import_call_graph": None, "status": "REQUIRED_BEFORE_COMPARE"},
        },
        "baseline_outputs": {
            "status": "PENDING_STAGE2_CANDIDATE_BUILD",
            "expected_artifacts": ["mtc_v2_legacy_sequence.jsonl", "baseline_manifest.json", "row_corroboration.json", "final_states.json"],
            "artifact_sha256": {},
            "double_build": {"run_1": None, "run_2": None, "byte_identical": None},
        },
        "tool_environment": {
            "python_executable": sys.executable,
            "python_version": sys.version,
            "python_implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "stage1_generator": {
                "path": Path(__file__).relative_to(REPO_ROOT).as_posix(),
                "sha256": sha256_file(Path(__file__)),
            },
        },
        "subject": {
            "classification": None,
            "allowed_classifications": ["INDEPENDENT_REIMPLEMENTATION", "WRAP_MOVE_OF_A"],
            "tree_oid": None,
            "import_call_graph": None,
            "status": "NO_SUBJECT_RUN_AUTHORIZED_OR_PERFORMED",
        },
        "independent_reproduction_evidence": {
            "status": "NOT_PERFORMED_IMPLEMENTER_MUST_NOT_SELF_ISSUE",
            "required_actor": "independent flagship other than builder",
            "auditor_checkout": None,
            "commands": [],
            "artifact_hashes": {},
        },
        "external_anchor": {
            "path": str(ANCHOR_PATH),
            "required": True,
            "missing": "STOP",
            "present_but_mismatched": "FAIL",
        },
        "claim_limits": [
            "baseline remains a candidate until independent flagship reproduction",
            "no profitability, safety, instrument-faithfulness, live-trading, or unnamed-case claim",
            "sequence arm has no independent economic credit for WRAP_MOVE_OF_A",
            "Pine source is corroboration only without an exact separately authorized export",
            "P0-10 expected values are not used",
        ],
        "discrepancies": [
            "The accepted design names C:\\WFMERGE54; this authorized isolated worktree is C:\\WPP011_20260825 at the same accepted commit.",
            "P011-LC-GATE-v2 re-pins P0-09 to the current-master citation-resolved blob; no row rule, oracle, or expected value changed from v1.",
            "The upstream normalized-file SHA-256 differs from the emitted fixture SHA-256; both identities are retained.",
            "Current master deleted the wt_* surface; C28-C30 use the controller freeze tag, never current master.",
        ],
    }


def main() -> int:
    fixture_meta = verify_fixed_inputs()
    profiles = build_profiles()
    schema_path = GATE_DIR / "P011_OBSERVATION_SCHEMA_v1.json"
    write_json(schema_path, build_schema())
    schema_hash = sha256_file(schema_path)

    legacy_path = GATE_DIR / "p011_legacy_manifest.json"
    write_json(legacy_path, build_legacy_manifest())
    legacy_hash = sha256_file(legacy_path)

    receipt_path = GATE_DIR / "P011_GATE_RECEIPT.json"
    receipt = build_receipt(fixture_meta, profiles, schema_hash, legacy_hash)
    write_json(receipt_path, receipt)
    receipt_hash = sha256_file(receipt_path)

    ANCHOR_PATH.parent.mkdir(parents=True, exist_ok=True)
    anchor = {
        "anchor_schema_version": "P011_OWNER_SIGNED_ANCHOR_v1",
        "gate_version": GATE_VERSION,
        "receipt_sha256": receipt_hash,
        "legacy_manifest_sha256": legacy_hash,
        "owner_identity": "Barış",
        "signature_date": "2026-08-28",
        "signature_basis": {
            "method": "direct owner authorization for the v2 gate bump",
            "owner_authorization_path": str(OWNER_AUTHORIZATION_PATH),
            "owner_authorization_sha256": sha256_file(OWNER_AUTHORIZATION_PATH),
            "owner_words_verbatim": "Bump to v2 now",
        },
        "supersedes_gate_version": "P011-LC-GATE-v1",
        "retained_v1_anchor": {
            "path": str(V1_ANCHOR_PATH),
            "sha256": sha256_file(V1_ANCHOR_PATH),
            "status": "RETAINED_UNTOUCHED",
        },
        "freeze_state": "STAGE1_FROZEN_STAGE2_CANDIDATE_PENDING",
        "subject_runs_at_signature": 0,
        "automatic_stop_rule": "Any P0-11 repository commit that touches, creates, deletes, renames, or claims to replace this external anchor is an automatic STOP.",
        "location_rule": "Only this external path is authoritative; an in-repository copy is not an anchor.",
    }
    write_json(ANCHOR_PATH, anchor)

    summary = {
        "outcome": "PASS",
        "gate_version": GATE_VERSION,
        "profiles": profiles,
        "schema_sha256": schema_hash,
        "legacy_manifest_sha256": legacy_hash,
        "receipt_sha256": receipt_hash,
        "external_anchor": str(ANCHOR_PATH),
        "subject_runs": 0,
    }
    print(json.dumps(summary, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
