from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GATE_VERSION = "P011-LC-GATE-v2"
STAGE3_GATE_VERSION = "P011-LC-GATE-v3"
EXECUTION_OBSERVATION = "EXECUTION_OBSERVATION"
SOURCE_CORROBORATION = "SOURCE_CORROBORATION"
BLOCKED_BY_DESIGN = "BLOCKED_BY_DESIGN"
SOURCE_COMMIT = "5c5603065c994d545c0eaa8c137fa9edd5cdfc28"
A_TREE_OID = "7aa6f867d821df08a00358adf2dd4400b9c719e8"
PINE_FREEZE_COMMIT = "77a10e6573d93f8aaf777010ea507bbec0a7668b"
B_FREEZE_COMMIT = "b5ed1afadcff09b69e36b72affeb23de51d84c14"
P009_AUTHORITY_COMMIT = "85c3e17f97efa1ba83ef9c679de319a50ad3be04"
P009_BLOB_OID = "1c39ab939dfcf5589e5ec8fba4af8966947a67fc"
P009_SHA256 = "7d48871a3e45dab118e97969d701912edb5d7c16a4d822d816beca1d03a42249"
COMPARISON_RULE_ID = "RECURSIVE_EXACT_IEEE754_HEX_V1"
EXPECTATION_METHOD_ID = "P009_LITERAL_SOURCE_ARITHMETIC_V1"
CORROBORATION_STATUS = "REQUIRED_EXACT_AUTHORITY_SET"
MUTATION_STATUS = "REQUIRED_RED_THEN_GREEN"
MUTATION_RESTORED_GREEN = "RECURSIVE_EXACT_IEEE754_HEX_V1_MATCH"
UNRESOLVED_MUTATION_OPERATION = "NOT_EXECUTED_UNRESOLVED_ROW_V1"
UNRESOLVED_MUTATION_REQUIRED_RED = "TERMINAL_STOP_REQUIRED_V1"
UNRESOLVED_MUTATION_RESTORATION = "NOT_ESTABLISHED_V1"
UNRESOLVED_MUTATION_STATUS = "UNRESOLVED_EXECUTION"
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
STAGE3_AUTHORIZATION_FILE_PATH = Path(
    r"C:\tmp\LANE_PROMPTS_20260828\OWNER_AUTH_P011_GATE_V3.md"
)
STAGE3_ANCHOR_PATH = Path(
    r"C:\LAB\P011_TRUST_ANCHORS\P011-LC-GATE-v3.owner-signed.json"
)
V3_PUBLICATION_RECEIPT_PATH = GATE_DIR / "P011_V3_PUBLICATION_RECEIPT.json"
V3_SIGNATURE_REFERENCE = {
    "kind": "REFERENCE_ONLY_NO_CODE_SIGNATURE",
    "owner_decision_file": "MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-29_EVENING.md",
    "branch": "docs/session-20260829-status",
    "commit": "3ffff7bc5d05675f6f7ed49449295bfcd99d93a9",
    "addendum": 5,
    "recorded_owner_ruling": "Sign with caveat recorded",
}
V3_SIGNATURE_CAVEAT = (
    "stage-4 design v2f's A-N recipe carries one step not yet literally executable by a "
    "stranger — wording, not evidence; parking record `AUDIT_N66E_V2F.md`"
)


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
    28: {"op": "A_FREEZE.resolve_config_route_keys", "inputs": {"wt_enter_long_code": "EL", "wt_exit_long_code": "XL", "wt_enter_short_code": "ES", "wt_exit_short_code": "XS", "wt_exit_all_code": "XA"}, "expected": {"declared_config_values": ["EL", "XL", "ES", "XS", "XA"]}, "final": {"route_key_count": 5}},
    29: {"op": "A_FREEZE.resolve_config_payload_keys", "inputs": {"wt_order_type": "limit", "wt_amount_type": "base", "wt_amount": 2.5, "wt_leverage": 3}, "expected": {"order_type": "limit", "amount_type": "base", "amount": 2.5, "leverage": 3}, "final": {"payload_key_count": 4}},
    30: {"op": "A_FREEZE.resolve_config_protective_keys", "inputs": {"use_tp": True, "use_sl": True, "wt_use_tp": True, "wt_use_sl": True, "wt_reduce_only": True, "wt_place_cond_orders": True}, "expected": {"wt_use_tp": True, "wt_use_sl": True, "wt_reduce_only": True, "wt_place_cond_orders": True}, "final": {"protective_key_count": 4, "cross_validation": "PASS"}},
    31: {"op": "A.runner_tw_master_switch", "inputs": {"modes": ["off", "research"], "protective_exit": True}, "expected": {"off_pending_reentry": None, "research_branch_reachable": True}, "final": {"mode_count": 2}},
    32: {"op": "A.resolve_config_reentry_enum", "inputs": {"accepted_values": ["local", "carry_to_next_bar_after_protective_exit", "next_bar_open", "next_bar_close"]}, "expected": {"all_values_validate": True}, "final": {"enum_count": 4}},
    33: {"op": "A.runner_reentry_delay", "inputs": {"delay_bars": 2, "protective_exit_bar": 10, "candidate_bars": [10, 11, 12]}, "expected": {"reentry_allowed": [False, False, True]}, "final": {"first_allowed_bar": 12}},
    34: {"op": "A.runner_margin_call", "inputs": {"tw_audit_semantics_mode": "research", "tw_margin_call_mode": "tradingview", "side": "long", "entry_price": 100.0, "mark_price": 40.0, "qty": 10.0, "margin_long_pct": 100.0, "initial_capital": 1000.0}, "expected": {"margin_call_branch_reached": True, "exit_reason": "margin_call"}, "final": {"total_exits": 1}},
    35: {"op": "A.runner_split_entries_stamp", "inputs": {"tw_margin_call_split_entries": True, "debug_mode": True}, "expected": {"debug_metadata_value": True, "economic_branch_count": 0}, "final": {"position_change_from_flag_only": False}},
    36: {"op": "A.runner_be_mode", "inputs": {"tw_audit_semantics_mode": "research", "tw_be_semantics_mode": "tradingview", "trigger_reached": True}, "expected": {"tradingview_be_branch_reached": True}, "final": {"be_active": True}},
    37: {"op": "A.runner_trailing_mode", "inputs": {"tw_audit_semantics_mode": "research", "tw_trailing_semantics_mode": "tradingview", "trigger_reached": True}, "expected": {"tradingview_trailing_branch_reached": True}, "final": {"trail_active": True}},
    38: {"op": "B_FREEZE.pivot_fsm", "inputs": {"wait_long": True, "wait_long_start_bar": 0, "bar_index": 1, "long_level": 100.0, "mintick": 1.0, "break_buffer_ticks": 1, "close": 102.0, "high": 102.0, "min_wait_bars": 1, "require_close_beyond": True}, "expected": {"long_break_level": 101.0, "long_age_ok": True, "long_pulse": True}, "final": {"waits_reset": True}},
    39: {"op": "B_FREEZE.entry_event_mode", "inputs": {"raw_long": [True, True], "entry_modes": ["Edge", "Signal"], "first_bar_requires_edge": True}, "expected": {"edge_long": [True, False], "signal_long": [True, True], "first_eval_bar_blocked_without_edge": True}, "final": {"mode_count": 2}},
    40: {"op": "A.htf_prior_closed_lookup", "inputs": {"ltf_timestamp": "2026-01-01T10:30:00+00:00", "declared_htf_minutes": 60, "completed_htf_closes": [{"timestamp": "2026-01-01T10:00:00+00:00", "close": 100.0}, {"timestamp": "2026-01-01T11:00:00+00:00", "close": 200.0}]}, "expected": {"selected_close": 100.0, "future_close_used": False}, "final": {"selected_timestamp": "2026-01-01T10:00:00+00:00"}},
    41: {"op": "A.gates_readiness_substitution", "inputs": {"ma_line": None, "close": 100.0, "htf_ready": True, "htf_close": 101.0, "htf_ma_line": None}, "expected": {"missing_ltf_ma_passes": True, "htf_substituted_value": 101.0}, "final": {"legacy_substitution_observed": True}},
    42: {"op": "A.signal_producers", "inputs": {"supertrend": {"st_use_ha": True, "bar_count": 3}, "range_filter": {"rf_range": 1000.0, "prices": [100.0, 101.0, 99.0]}}, "expected": {"supertrend_signals": [{"long": False, "short": False, "reason": "st_ha_not_supported"}, {"long": False, "short": False, "reason": "st_ha_not_supported"}, {"long": False, "short": False, "reason": "st_ha_not_supported"}], "range_filter_event_count": 0}, "final": {"producer_count": 2}},
}


def _stage3_generator_scenarios() -> dict[int, dict[str, Any]]:
    c32_values = [
        "local",
        "delay_after_protective_exit",
        "carry_to_next_bar_after_protective_exit",
        "next_bar_open_after_protective_exit_signal",
        "next_bar_close_after_protective_exit_signal",
    ]
    c32_bars = [
        {"bar_index": 0, "timestamp": "2026-01-01T00:00:00+00:00", "open": 100.0, "high": 100.0, "low": 100.0, "close": 100.0, "volume": 1.0, "raw_long": True, "raw_short": False},
        {"bar_index": 1, "timestamp": "2026-01-01T00:01:00+00:00", "open": 99.0, "high": 99.0, "low": 94.0, "close": 94.0, "volume": 1.0, "raw_long": True, "raw_short": False},
        {"bar_index": 2, "timestamp": "2026-01-01T00:02:00+00:00", "open": 94.0, "high": 100.0, "low": 94.0, "close": 100.0, "volume": 1.0, "raw_long": True, "raw_short": False},
        {"bar_index": 3, "timestamp": "2026-01-01T00:03:00+00:00", "open": 99.0, "high": 100.0, "low": 99.0, "close": 100.0, "volume": 1.0, "raw_long": False, "raw_short": False},
        {"bar_index": 4, "timestamp": "2026-01-01T00:04:00+00:00", "open": 100.0, "high": 100.0, "low": 99.0, "close": 100.0, "volume": 1.0, "raw_long": False, "raw_short": False},
        {"bar_index": 5, "timestamp": "2026-01-01T00:05:00+00:00", "open": 100.0, "high": 100.0, "low": 99.0, "close": 100.0, "volume": 1.0, "raw_long": True, "raw_short": False},
    ]
    c32_reentries = [
        (c32_values[0], 2, 100.0, 0.994),
        (c32_values[1], 5, 100.0, 0.994),
        (c32_values[2], 3, 100.0, 0.994),
        (c32_values[3], 3, 99.0, 1.00404),
        (c32_values[4], 4, 100.0, 0.994),
    ]
    c32_runs = []
    c32_final = []
    for value, bar_index, price, quantity in c32_reentries:
        c32_runs.append(
            {
                "value": value,
                "events": [
                    {"bar_index": 0, "event": "ENTER_LONG", "price": 100.0, "quantity": 1.0, "reason": "c32_fixture_signal"},
                    {"bar_index": 1, "event": "EXIT_LONG", "price": 94.0, "quantity": 1.0, "reason": "sl_percent_hit", "realized_pnl": -6.0},
                    {"bar_index": bar_index, "event": "ENTER_LONG", "price": price, "quantity": quantity, "reason": "c32_fixture_signal"},
                ],
                "reentry": {"bar_index": bar_index, "price": price, "quantity": quantity},
            }
        )
        c32_final.append(
            {
                "value": value,
                "position": {"side": "long", "entry_bar": bar_index, "entry_price": price, "quantity": quantity},
                "realized_pnl": -6.0,
                "total_entries": 2,
                "total_exits": 1,
            }
        )

    c34_bars = [
        {"bar_index": 0, "timestamp": "2026-01-01T00:00:00+00:00", "open": 100.0, "high": 100.0, "low": 100.0, "close": 100.0, "volume": 10.0, "raw_long": True, "raw_short": False},
        {"bar_index": 1, "timestamp": "2026-01-01T00:01:00+00:00", "open": 98.0, "high": 98.0, "low": 94.0, "close": 95.0, "volume": 10.0, "raw_long": False, "raw_short": False},
        {"bar_index": 2, "timestamp": "2026-01-01T00:02:00+00:00", "open": 94.0, "high": 94.0, "low": 88.0, "close": 89.0, "volume": 10.0, "raw_long": False, "raw_short": False},
        {"bar_index": 3, "timestamp": "2026-01-01T00:03:00+00:00", "open": 88.0, "high": 88.0, "low": 84.0, "close": 85.0, "volume": 10.0, "raw_long": False, "raw_short": False},
    ]
    c34_l1 = {"checkpoints": [], "events": [{"bar_index": 0, "event": "ENTER_LONG", "price": 100.0, "quantity": 40.0, "reason": "c34_fixture_signal"}]}
    c34_l2 = {
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
    c34_open = {"position": {"side": "long", "entry_bar": 0, "entry_price": 100.0, "quantity": 40.0}, "realized_pnl": 0.0, "equity_at_final_close": 400.0, "total_entries": 1, "total_exits": 0}
    c34_flat = {"position": None, "realized_pnl": -480.0, "equity_at_final_close": 520.0, "total_entries": 1, "total_exits": 1}

    c42_common = [
        {"bar_index": 0, "timestamp": "2026-01-01T00:00:00+00:00", "open": 100.0, "high": 102.0, "low": 98.0, "close": 100.0, "volume": 1.0},
        {"bar_index": 1, "timestamp": "2026-01-01T00:01:00+00:00", "open": 100.0, "high": 102.0, "low": 98.0, "close": 100.0, "volume": 1.0},
        {"bar_index": 2, "timestamp": "2026-01-01T00:02:00+00:00", "open": 100.0, "high": 102.0, "low": 90.0, "close": 95.0, "volume": 1.0},
        {"bar_index": 3, "timestamp": "2026-01-01T00:03:00+00:00", "open": 95.0, "high": 110.0, "low": 95.0, "close": 109.0, "volume": 1.0},
        {"bar_index": 4, "timestamp": "2026-01-01T00:04:00+00:00", "open": 109.0, "high": 110.0, "low": 108.0, "close": 109.0, "volume": 1.0},
    ]
    c42_f3_wick = [
        c42_common[0],
        {"bar_index": 1, "timestamp": "2026-01-01T00:01:00+00:00", "open": 100.0, "high": 102.0, "low": 94.0, "close": 100.0, "volume": 1.0},
    ]
    c42_f4 = [
        {"bar_index": 0, "timestamp": "2026-01-01T00:00:00+00:00", "open": 100.0, "high": 100.0, "low": 100.0, "close": 100.0, "volume": 1.0},
        {"bar_index": 1, "timestamp": "2026-01-01T00:01:00+00:00", "open": 115.0, "high": 115.0, "low": 115.0, "close": 115.0, "volume": 1.0},
        {"bar_index": 2, "timestamp": "2026-01-01T00:02:00+00:00", "open": 104.0, "high": 104.0, "low": 104.0, "close": 104.0, "volume": 1.0},
    ]

    def raw(long: bool, short: bool, reason: str, direction: int | None, line: float | None) -> dict[str, Any]:
        return {"long": long, "short": short, "reason": reason, "direction": direction, "line": line}

    c42_observed = {
        "F1": {"raw_signals": [raw(False, False, "st_ha_not_supported", None, None) for _ in range(5)], "fills": []},
        "F2": {
            "raw_signals": [raw(False, False, "st_direction_init", 1, 96.0), raw(False, False, "st_hold_long", 1, 96.0), raw(False, True, "st_flip_short", -1, 104.0), raw(True, False, "st_flip_long", 1, 87.5), raw(False, False, "st_hold_long", 1, 107.0)],
            "fills": [
                {"bar_index": 2, "event": "ENTER_SHORT", "price": 95.0, "quantity": 1.0, "reason": "st_flip_short"},
                {"bar_index": 3, "event": "EXIT_SHORT", "price": 109.0, "quantity": 1.0, "reason": "opp_signal", "realized_pnl": -14.0},
                {"bar_index": 3, "event": "ENTER_LONG", "price": 109.0, "quantity": 1.0, "reason": "st_flip_long"},
            ],
        },
        "F3_CLOSE": {"raw_signals": [raw(False, False, "st_direction_init", 1, 96.0), raw(False, False, "st_hold_long", 1, 96.0)], "fills": []},
        "F3_WICK": {"raw_signals": [raw(False, False, "st_direction_init", 1, 96.0), raw(False, True, "st_flip_short", -1, 104.0)], "fills": [{"bar_index": 1, "event": "ENTER_SHORT", "price": 100.0, "quantity": 1.0, "reason": "st_flip_short"}]},
        "F4": {
            "raw_signals": [raw(False, False, "rf_init", 0, 100.0), raw(True, False, "rf_flip_long", 1, 105.0), raw(False, True, "rf_flip_short", -1, 114.0)],
            "fills": [
                {"bar_index": 1, "event": "ENTER_LONG", "price": 115.0, "quantity": 1.0, "reason": "rf_flip_long"},
                {"bar_index": 2, "event": "EXIT_LONG", "price": 104.0, "quantity": 1.0, "reason": "opp_signal", "realized_pnl": -11.0},
                {"bar_index": 2, "event": "ENTER_SHORT", "price": 104.0, "quantity": 1.0, "reason": "rf_flip_short"},
            ],
        },
    }
    c42_final = {
        "F1": {"position": None, "realized_pnl": 0.0, "total_entries": 0, "total_exits": 0},
        "F2": {"position": {"side": "long", "entry_bar": 3, "entry_price": 109.0, "quantity": 1.0}, "realized_pnl": -14.0, "total_entries": 2, "total_exits": 1},
        "F3_CLOSE": {"position": None, "realized_pnl": 0.0, "total_entries": 0, "total_exits": 0},
        "F3_WICK": {"position": {"side": "short", "entry_bar": 1, "entry_price": 100.0, "quantity": 1.0}, "realized_pnl": 0.0, "total_entries": 1, "total_exits": 0},
        "F4": {"position": {"side": "short", "entry_bar": 2, "entry_price": 104.0, "quantity": 1.0}, "realized_pnl": -11.0, "total_entries": 2, "total_exits": 1},
    }
    return {
        32: {
            "op": "A.runner_reentry_enum_stage3",
            "inputs": {
                "accepted_values": c32_values,
                "invalid_control": "next_bar_open",
                "config": {"tw_audit_semantics_mode": "research", "tw_reversal_reentry_delay_bars": 2, "use_sl": True, "use_sl_percent": True, "sl_percent": 5.0, "tp_mode": "None", "exit_on_opposite_signal": True, "allow_flip": True, "execution_profile_id": "close_only_deterministic_v2", "initial_capital": 1000.0, "risk_per_long_pct": 0.5, "risk_per_short_pct": 0.5, "max_leverage_cap": 1.0, "cooldown_bars": 0, "max_entries": 1, "regime_lock": False, "instrument_price_tick": 0.01, "instrument_qty_step": 0.000001, "instrument_min_qty": 0.0, "instrument_min_notional": 0.0, "instrument_contract_multiplier": 1.0},
                "bars": c32_bars,
            },
            "expected": {"runs": c32_runs, "invalid_control": {"accepted": False, "accepted_values": c32_values, "error_type": "ValueError", "error": "tw_reversal_reentry_mode must be one of: local, delay_after_protective_exit, carry_to_next_bar_after_protective_exit, next_bar_open_after_protective_exit_signal, next_bar_close_after_protective_exit_signal", "value": "next_bar_open"}},
            "final": {"runs": c32_final},
        },
        34: {
            "op": "A.runner_margin_call_stage3",
            "inputs": {
                "arms": [{"arm": "L1", "tw_audit_semantics_mode": "off", "tw_margin_call_mode": "off"}, {"arm": "L2", "tw_audit_semantics_mode": "research", "tw_margin_call_mode": "tradingview"}, {"arm": "L3", "tw_audit_semantics_mode": "off", "tw_margin_call_mode": "tradingview"}],
                "config": {"initial_capital": 1000.0, "max_leverage_cap": 5.0, "margin_long_pct": 20.0, "margin_short_pct": 20.0, "use_sl": False, "use_sl_percent": False, "use_sl_atr": False, "use_sl_swing_atr": False, "tp_mode": "None", "fallback_size_pct": 400.0, "cooldown_bars": 0, "max_entries": 1, "instrument_price_tick": 0.01, "instrument_qty_step": 1.0, "instrument_min_qty": 0.0, "instrument_min_notional": 0.0, "instrument_contract_multiplier": 1.0},
                "bars": c34_bars,
            },
            "expected": {"arms": {"L1": c34_l1, "L2": c34_l2, "L3": c34_l1}, "l1_l3_field_identical": True},
            "final": {"arms": {"L1": c34_open, "L2": c34_flat, "L3": c34_open}},
        },
        42: {
            "op": "A.signal_producers_stage3",
            "inputs": {
                "common_config": {"use_confirm_transform": False, "use_level_retest": False, "use_l18b_confirmation": False, "use_sl": False, "use_sl_percent": False, "use_sl_atr": False, "use_sl_swing_atr": False, "tp_mode": "None", "max_entries": 1, "exit_on_opposite_signal": True, "allow_flip": True, "cooldown_bars": 0, "regime_lock": False, "initial_capital": 1000.0, "fallback_size_pct": 11.5, "instrument_price_tick": 0.01, "instrument_qty_step": 1.0, "instrument_min_qty": 0.0, "instrument_min_notional": 0.0, "instrument_contract_multiplier": 1.0},
                "arms": {
                    "F1": {"config": {"signal_mode": "Supertrend", "st_atr_len": 1, "st_factor": 1.0, "st_use_wicks": False, "st_use_ha": True}, "bars": c42_common},
                    "F2": {"config": {"signal_mode": "Supertrend", "st_atr_len": 1, "st_factor": 1.0, "st_use_wicks": False, "st_use_ha": False}, "bars": c42_common},
                    "F3_CLOSE": {"config": {"signal_mode": "Supertrend", "st_atr_len": 1, "st_factor": 1.0, "st_use_wicks": False, "st_use_ha": False}, "bars": c42_common[:2]},
                    "F3_WICK": {"config": {"signal_mode": "Supertrend", "st_atr_len": 1, "st_factor": 1.0, "st_use_wicks": True, "st_use_ha": False}, "bars": c42_f3_wick},
                    "F4": {"config": {"signal_mode": "Range Filter", "rf_range": 10.0}, "bars": c42_f4},
                },
            },
            "expected": {"arms": c42_observed},
            "final": {"arms": c42_final},
        },
    }


ROW_MUTATION_EXECUTION: dict[int, tuple[str, str, str, str]] = {
    1: ("mtc_v2/core/runner.py", "ad95a5b021a764a326f74b6db2a5fc5b9f82335d19624e4ddaf853e49a2dad83", "b3adfb6bd97664a9c4e7312c206dd1311dae1091c9bd59feac747309754e4053", "$.observation.gated_long"),
    2: ("mtc_v2/core/gates.py", "c52bba18466bae57fce418e53999b6885e5ea3449db7068a89bb58b87a6fb8f5", "6b04be3a27f98fa0653b107803512f7db24b624b54f82f906daa88e44afdd17a", "$.final_state.gate_evaluation"),
    3: ("mtc_v2/core/runner.py", "a2ecd934e15187cff0bd6b24f702dc07c8731deee8bb1b6bd602a14b47f35ddb", "4fbd5a93c017a083a3db00b5244c54110258103e1226e5ae95cfd9cf8d00b6ad", "$.final_state.confirm_direction"),
    4: ("mtc_v2/core/runner.py", "0deefc1645c6752e620773ddb71ac3ea49d403b44a922cb13ecd0d513590cb16", "9cad46b8e28073b77c04bbafc7707ac1db7ccf6bde21a6d961a939823023b812", "$.final_state.waiting"),
    5: ("mtc_v2/core/runner.py", "9d0946df2923338f6604adfd543c3f302c9319cfc331c49415488dd3c38d879a", "a47a40ece28de06a4319b2ffe3968c5ff3b3e66e9605b1355fecc2a12e9db66a", "$.final_state.position_present"),
    6: ("mtc_v2/core/position_manager.py", "2130c27d24f8292c2ae3fad396ee0d7542f6c797aff4e1d94e3bca84f2f26a1d", "58c59acc885ecc277bc0b316fb64e961af07539b91ce499d6880e489f3e7e181", "$.observation.active_entry_legs"),
    7: ("mtc_v2/core/position_sizer.py", "1ae7dab7b506d611ef802f9652808df9926ab8e862553a348d177931221fd7ad", "5d842be7bd1f9425ea820fc5261fedfed31386fe6c0824922fac1059498350b1", "$.observation.qty.__float_hex__"),
    8: ("mtc_v2/core/position_manager.py", "3c978f26dfe67a023085e1df7ddafa71edeb3f2db31c1769c199755aff7e230d", "fcd61ceb8b4d64e69ac44dec550fc75b53c5d726f91d4ab6b05710af1a0b5eec", "$.final_state.realized_equity_delta.__float_hex__"),
    9: ("mtc_v2/core/rounding.py", "c027c7be7f21b9ba97bc4dd2c32183dd7b9192d338fc04e54a7498df3cf32a60", "45975d63f57f5834bd8876bf235a5e485ec2d32e5bb74964bbf6bf4a9484966b", "$.final_state.below_minimum_rejected"),
    10: ("mtc_v2/core/runner.py", "013ee9cc28f61de6af47bdad04884c5689f33cd83fef0dffcd0bfab7cd62d4f4", "9c05bf2ad8a286947af7222c9f35a923466f07baf3ec8e0b6b24f0c11d1072ba", "$.observation.blocked"),
    11: ("mtc_v2/core/exits.py", "3ea1281688b1c913b26774741a0267586754406cb0a7e15611b8fd34050d6e31", "e8b7dab6b105da04f9822825b12aad26f9a0518425e709c387d118dbdc3a3c57", "$.observation.fill_price.__float_hex__"),
    12: ("mtc_v2/core/exits.py", "a0ddf453f0f127fde3815bfb011d335d5bf7c108dc25e66c16c9dc3812141d83", "109bc8c728dd3ef445489722f64d8eb8177f09eeb4c7a6f7ef139d687fd7c448", "$.observation.fill_price.__float_hex__"),
    13: ("mtc_v2/core/exits.py", "4f6ae95933a45975077819d7a73447685492a68e749a96613bf5ed938b37de6c", "14ec1653e8635823c80e5324b3632a53250d99aa395c06450636071b329b9278", "$.final_state.position_present"),
    14: ("mtc_v2/core/exits.py", "c08a62e4c26d2902b7081f3bcf54855d0da62f124209724bc9c89962f161f522", "27227b7b51580513b97a93e82929e65b0b2c1f9f7d75bff9dbfe52442c20c77d", "$.observation.active_stop_price.__float_hex__"),
    15: ("mtc_v2/core/exits.py", "e8b8fa8645ef8a6618c105b29921e2f0af5db5d2031f4c4658aa6bdf8c5ad979", "42c1bbbcb35e05905f2a28d52abe357b51adf758cf4345a3b6a08510a504e6c2", "$.observation.trail_price.__float_hex__"),
    16: ("mtc_v2/core/runner.py", "5e8445da1a8f1c6d74eb4266aa446157b9b6f30cd5ae43783b148861c2aaa860", "a4a9fb7c943b52adf54e9414151a7592f4c4c17b877a606702316f966ade9b53", "$.final_state.position_present"),
    17: ("mtc_v2/core/runner.py", "002e491ab4e31ed54310a1fa09cff0f15ead17876bb8c272845d78f1d71d78bd", "758e73f3abf2788f08513afd2706a0e04fd0d37782cb4b2023519a446dcc0197", "$.final_state.position_present"),
    18: ("mtc_v2/core/runner.py", "74762216379c0f91c7d5ebe2d36545f07ad84eed6ac0979f5d150d0638ea25e5", "aa96326b0eb02e78245ca196fd0590ded80e9c6c17b27d937860e632c2543bbe", "$.final_state.position_present"),
    19: ("mtc_v2/core/exits.py", "c891ac7ddd3dbff9427dfeba2beeafc16f1a0687cb460a70c84246245a25f937", "8793b52d8994c0e41a7dd32455d9826c4d12640c4e554b2b8e3b401781f852c0", "$.observation.exit_reason"),
    20: ("mtc_v2/core/position_manager.py", "a60314232b6517679754f2dfd91a0cacf903cf60aa523ad94718c93904503f04", "3f8cd407e6e1118a0181f50ef8b630c74ac7593b12b1ac606394e2c903210d41", "$.observation.entry_fill_price.__float_hex__"),
    21: ("mtc_v2/core/runner.py", "db570eed9b03719611af710215ad7ed9785374043250bd70106d503ea0a842b4", "94e573d42e0043e2e59dae9e9a78502888630ca5b96a05fc2814e07a3258e6fc", "$.final_state.position_present"),
    22: ("mtc_v2/core/position_manager.py", "3c978f26dfe67a023085e1df7ddafa71edeb3f2db31c1769c199755aff7e230d", "27f6e73bbfb1666dc99bf4c12df891eba7f540951f4a5004360758207359da9b", "$.observation.gross_pnl.__float_hex__"),
    23: ("mtc_v2/core/runner.py", "79b679d9f4ac55863d8c6aad7ba51cecc9081c68a1ad01f341c8fd9cdc850d52", "bf6ad2bc42ecaa2f19d743a55e80f125e7daead938798eb4f519011d286ae7d2", "$.final_state.position_preserved_at_end"),
    24: ("mtc_v2/core/runner.py", "865c36057f21a770817725961296b5014a5089dd103e7f81c58b7422d50ee010", "18a0909bb93e7a9d12517b6e143a077a3e5e20d09f39ef9e42dfcd4143f3539b", "$.observation.bar_valid"),
    26: ("mtc_v2/core/runner.py", "323090b1241b3a3c3ca58932ebbd3152b876515a9ef3f76397f019af842fdd6d", "b55b612b69d0700fdd746128a32b8993b6e9bdcdf37df8a6c705141fde94c9a2", "$.observation.duplicate_rejected_by_legacy_runner"),
    31: ("mtc_v2/core/runner.py", "4b4c086b080974455fd423d6360aa05ad7ee4eca6a8d22529ac134495d8f9227", "2b9674feade1b145587d4a309a96219a09419e1cac16bef0ac1a511b007d1c51", "$.observation.research_branch_reachable"),
    33: ("mtc_v2/core/runner.py", "ac9f7cc57e54c82dc623ffd5e1657fba46a2dd6a9eb90df08ed49ac6bd8fadf4", "0dac5019f5ece8803bb4f169f714e46e15d844a5cdfce94e0876e554f135a9cb", "$.final_state.first_allowed_bar"),
    36: ("mtc_v2/core/exits.py", "c6a07a9a739340ff30027689aa3e6c5fe4b1484541c60a69e2580c26c0ebed64", "e9a86c7cb991f36794b98fbd3bd8bcc7e012ccec2aded82612b044286cd982c8", "$.final_state.be_active"),
    37: ("mtc_v2/core/exits.py", "18c81d7380bad828aaf516b37ff8c584d08197028d9457e42e24bdba3025ea73", "981922c97e4143e6813b86f595eee4a827c8e66192f1c6bdd8426776a40e8c36", "$.final_state.trail_active"),
    38: ("src/modules/confirmation_layer.py", "d05d808cd34c7befe607d8025b24ad646dcfe700bdcb17c2af6d2b5f2ef59bae", "69849df8168bc57ca0d321877b772a98efcaba81029238868db6b9178413726a", "$.final_state.waits_reset"),
    39: ("src/engine/mtc_runner.py", "6c8c9f966a1ca9fdebbb9b25c3289877218277775cfbc2863890659d66e932e6", "2d78292df2d3f886d1c662c527e5d1d4e028e8becca6030c252c517eff09be32", "$.observation.edge_long[1]"),
    40: ("mtc_v2/core/htf.py", "b7c15e2847b776e366b698fd9b5500289a619360a29a516e75693f501d5ae35c", "05686dd77c4ff7234d391eb6cd7016dca7b4522ef0ff5cca788266bc441d628d", "$.final_state.selected_timestamp"),
    41: ("mtc_v2/core/gates.py", "cc3b3711483c40ed79559f9106060feaaa8028f33997743a9d0a4fe10554db41", "11a4ab9b7098939089c202977551ad71582f48ae7300252357ff4a6b610c2c70", "$.final_state.legacy_substitution_observed"),
}


def row_authorities(row_number: int, *, stage3: bool = False) -> list[dict[str, Any]]:
    if row_number in (28, 29, 30):
        authorities = [
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
    elif row_number == 26:
        authorities = [
            {"name": "A_CURRENT_MASTER", "commit": SOURCE_COMMIT, "tree_oid": A_TREE_OID, "role": "legacy runner duplicate/revision behavior"},
            {"name": "PINE_CONTROLLER_FREEZE", "ref": "legacy/pine-controller/2026-08-25", "commit": PINE_FREEZE_COMMIT, "role": "historical L25 dispatch corroboration only"},
        ]
    elif row_number == 38:
        authorities = [
            {"name": "B_BACKTEST_FREEZE", "ref": "legacy/02-mtc-backtest/2026-08-25", "commit": B_FREEZE_COMMIT, "path": "MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/modules/confirmation_layer.py", "role": "pivot FSM legacy authority"},
            {"name": "A_CURRENT_MASTER", "commit": SOURCE_COMMIT, "tree_oid": A_TREE_OID, "role": "inert scaffold preservation only"},
        ]
    elif row_number in (39, 41):
        authorities = [
            {"name": "A_CURRENT_MASTER", "commit": SOURCE_COMMIT, "tree_oid": A_TREE_OID, "role": "A legacy behavior"},
            {"name": "B_BACKTEST_FREEZE", "ref": "legacy/02-mtc-backtest/2026-08-25", "commit": B_FREEZE_COMMIT, "role": "B corroboration where carried"},
        ]
    elif row_number in (3, 4, 42):
        authorities = [
            {"name": "A_CURRENT_MASTER", "commit": SOURCE_COMMIT, "tree_oid": A_TREE_OID, "role": "executable Python authority"},
            {"name": "PINE_CURRENT_MASTER", "commit": SOURCE_COMMIT, "path": "MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine", "role": "equation/source corroboration only; no TradingView execution credit"},
        ]
    else:
        authorities = [{"name": "A_CURRENT_MASTER", "commit": SOURCE_COMMIT, "tree_oid": A_TREE_OID, "role": "legacy executable authority"}]
    if not stage3:
        return authorities
    modes_by_row: dict[int, dict[str, str]] = {
        3: {"A_CURRENT_MASTER": EXECUTION_OBSERVATION, "PINE_CURRENT_MASTER": SOURCE_CORROBORATION},
        4: {"A_CURRENT_MASTER": EXECUTION_OBSERVATION, "PINE_CURRENT_MASTER": SOURCE_CORROBORATION},
        26: {"A_CURRENT_MASTER": EXECUTION_OBSERVATION, "PINE_CONTROLLER_FREEZE": SOURCE_CORROBORATION},
        28: {"A_PINE_CONTROLLER_FREEZE": BLOCKED_BY_DESIGN},
        29: {"A_PINE_CONTROLLER_FREEZE": BLOCKED_BY_DESIGN},
        30: {"A_PINE_CONTROLLER_FREEZE": BLOCKED_BY_DESIGN},
        38: {"B_BACKTEST_FREEZE": EXECUTION_OBSERVATION, "A_CURRENT_MASTER": SOURCE_CORROBORATION},
        39: {"A_CURRENT_MASTER": SOURCE_CORROBORATION, "B_BACKTEST_FREEZE": EXECUTION_OBSERVATION},
        41: {"A_CURRENT_MASTER": EXECUTION_OBSERVATION, "B_BACKTEST_FREEZE": SOURCE_CORROBORATION},
        42: {"A_CURRENT_MASTER": EXECUTION_OBSERVATION, "PINE_CURRENT_MASTER": SOURCE_CORROBORATION},
    }
    explicit_modes = modes_by_row.get(row_number, {"A_CURRENT_MASTER": EXECUTION_OBSERVATION})
    typed: list[dict[str, Any]] = []
    for authority in authorities:
        item = dict(authority)
        item["evidence_mode"] = explicit_modes[item["name"]]
        typed.append(item)
    return typed


STAGE3_MUTATIONS: dict[int, tuple[str, str, str, str]] = {
    32: (
        "mtc_v2/core/runner.py",
        "ac9f7cc57e54c82dc623ffd5e1657fba46a2dd6a9eb90df08ed49ac6bd8fadf4",
        "0dac5019f5ece8803bb4f169f714e46e15d844a5cdfce94e0876e554f135a9cb",
        "$.observation.runs[2].reentry.bar_index",
    ),
    34: (
        "mtc_v2/core/runner.py",
        "fbd4d97a7f39a4c69c3c8163e47618f6c36f574ed59f7284e33225cfc6401eed",
        "548b0ed866501ecb61bd61a68a1e166a7d10cfb1708abd2acaeeacc239edf565",
        "$.final_state.arms.L2.position",
    ),
    42: (
        "mtc_v2/signals/range_filter.py",
        "75d752d8f6a0d251cd99f55adc71c46dc63cc4259beda48c407e7de2326cb197",
        "716cd0bddc28df03c85f493f80fa071375bbb362a598d762de41c7662f568c15",
        "$.observation.arms.F4.raw_signals[2].short",
    ),
}


def row_mutation_contract(
    row_number: int, row_id: str, spec: dict[str, Any], *, stage3: bool = False
) -> dict[str, str]:
    mutation_prefix = "STAGE3" if stage3 and row_number in STAGE3_MUTATIONS else "GF8"
    execution = (
        STAGE3_MUTATIONS.get(row_number)
        if stage3 and row_number in STAGE3_MUTATIONS
        else ROW_MUTATION_EXECUTION.get(row_number)
    )
    if execution is None:
        return {
            "mutation_id": f"{row_id}-{mutation_prefix}-MUT-001",
            "source_seam": spec["op"],
            "mutation": UNRESOLVED_MUTATION_OPERATION,
            "required_red": UNRESOLVED_MUTATION_REQUIRED_RED,
            "restored_green": UNRESOLVED_MUTATION_RESTORATION,
            "status": UNRESOLVED_MUTATION_STATUS,
        }
    source_seam, old_sha256, new_sha256, required_red_path = execution
    return {
        "mutation_id": f"{row_id}-{mutation_prefix}-MUT-001",
        "source_seam": source_seam,
        "mutation": (
            f"EXACT_TEXT_REPLACE_ONCE_V1:old_sha256={old_sha256}:"
            f"new_sha256={new_sha256}"
        ),
        "required_red": f"MISMATCH_PATH_PRESENT_V1:{required_red_path}",
        "restored_green": MUTATION_RESTORED_GREEN,
        "status": MUTATION_STATUS,
    }


def build_legacy_manifest(*, stage3: bool = False) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    stage3_scenarios = _stage3_generator_scenarios() if stage3 else {}
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
        if stage3 and number == 42:
            p009_citation["section_lines_at_pinned_blob"] = "1231-1276"
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
        spec = stage3_scenarios.get(number, ROW_SCENARIOS[number])
        authorities = row_authorities(number, stage3=stage3)
        rows.append(
            {
                "row_id": row_id,
                "title": title,
                "disposition": "APPLICABLE",
                "p009_citation": p009_citation,
                "legacy_authorities": authorities,
                "scenarios": [
                    {
                        "scenario_id": f"{row_id}-LEGACY-001",
                        "producer_adapter": spec["op"],
                        "complete_inputs": spec["inputs"],
                        "literal_expected_observation": spec["expected"],
                        "literal_expected_final_state": spec["final"],
                        "expectation_derivation": {
                            "method": EXPECTATION_METHOD_ID,
                            "source": p009_citation,
                            "producer_output_may_not_rebless_expected": True,
                        },
                        "comparison_rule": COMPARISON_RULE_ID,
                        "clean_producer_corroboration": (
                            {
                                "status": "REQUIRED_TERMINAL_AUTHORITY_EVIDENCE",
                                "required": True,
                                "authority_requirements": [
                                    {
                                        "name": item["name"],
                                        "evidence_mode": item["evidence_mode"],
                                    }
                                    for item in authorities
                                ],
                            }
                            if stage3
                            else {
                                "status": CORROBORATION_STATUS,
                                "required": True,
                                "authority_names": [item["name"] for item in authorities],
                            }
                        ),
                        "producer_mutation": row_mutation_contract(
                            number, row_id, spec, stage3=stage3
                        ),
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
        "gate_version": STAGE3_GATE_VERSION if stage3 else GATE_VERSION,
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


def _contains_exact_key(value: Any, target: str) -> bool:
    if isinstance(value, dict):
        return target in value or any(
            _contains_exact_key(child, target) for child in value.values()
        )
    if isinstance(value, list):
        return any(_contains_exact_key(child, target) for child in value)
    return False


def validate_v3_publication_receipt(
    path: Path = V3_PUBLICATION_RECEIPT_PATH,
) -> dict[str, Any]:
    receipt = json.loads(path.read_text(encoding="utf-8"))
    if receipt.get("receipt_schema_version") != "P011_V3_PUBLICATION_RECEIPT_v1":
        raise SystemExit("STOP_V3_PUBLICATION_RECEIPT_SCHEMA_MISMATCH")
    if receipt.get("gate_version") != STAGE3_GATE_VERSION:
        raise SystemExit("STOP_V3_PUBLICATION_RECEIPT_GATE_VERSION_MISMATCH")
    if receipt.get("gate_outcome") != "STOP":
        raise SystemExit("STOP_V3_GATE_OUTCOME_NOT_STOP")
    if _contains_exact_key(receipt, "signature"):
        raise SystemExit("STOP_V3_CODE_SIGNATURE_FIELD_REFUSED")
    if receipt.get("signature_act_of_record") != V3_SIGNATURE_REFERENCE:
        raise SystemExit("STOP_V3_SIGNATURE_REFERENCE_MISMATCH")
    caveat = receipt.get("publication_caveat") or {}
    if caveat.get("verbatim") != V3_SIGNATURE_CAVEAT:
        raise SystemExit("STOP_V3_CAVEAT_MISMATCH")
    measured = (receipt.get("independent_reproduction_evidence") or {}).get(
        "measured_identity_matches"
    )
    if measured != {
        "deciding_text_input_blob_oids": 4,
        "tool_blob_oids": 6,
        "package_file_sha256": 13,
        "source_commit": 1,
        "source_tree": 1,
    }:
        raise SystemExit("STOP_V3_SECOND_ACTOR_MEASUREMENTS_MISMATCH")
    hashed_baseline = (receipt.get("identity_contract") or {}).get(
        "hashed_baseline", {}
    )
    for machine_key in (
        "platform",
        "python_executable",
        "python_implementation",
        "python_version",
    ):
        if machine_key in hashed_baseline:
            raise SystemExit("STOP_V3_MACHINE_STRING_IN_HASHED_BASELINE")
    if hashed_baseline.get("machine_strings") != "EXCLUDED":
        raise SystemExit("STOP_V3_MACHINE_STRING_POLICY_MISMATCH")
    steps = receipt.get("design_step_execution")
    if not isinstance(steps, list) or [item.get("step") for item in steps] != list(
        "ABCDEFGHIJKLMN"
    ):
        raise SystemExit("STOP_V3_DESIGN_STEP_MAP_MISMATCH")
    if any(
        not isinstance(item.get("status"), str)
        or not item["status"].startswith(("DONE_", "STOP_"))
        for item in steps
    ):
        raise SystemExit("STOP_V3_UNMEASURED_STEP_LABEL_REFUSED")
    return receipt


def _refuse_protected_publication_target(path: Path) -> None:
    resolved = path.resolve()
    protected = {
        (GATE_DIR / "P011_GATE_RECEIPT.json").resolve(),
        (GATE_DIR / "p011_legacy_manifest.json").resolve(),
        V3_PUBLICATION_RECEIPT_PATH.resolve(),
        V1_ANCHOR_PATH.resolve(),
        ANCHOR_PATH.resolve(),
        STAGE3_ANCHOR_PATH.resolve(),
    }
    if resolved in protected and not (
        "P011-LC-GATE-v1" in resolved.name
        or "P011-LC-GATE-v2" in resolved.name
    ):
        raise SystemExit("STOP_PROTECTED_PUBLICATION_TARGET_REFUSED")
    if (
        "P011-LC-GATE-v1" in resolved.name
        or "P011-LC-GATE-v2" in resolved.name
    ):
        raise SystemExit("STOP_V1_V2_PUBLICATION_TARGET_REFUSED")


def _require_stage3_scratch(path: Path, scratch_root: Path) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(scratch_root.resolve())
    except ValueError as exc:
        raise SystemExit("STOP_CANDIDATE_PATH_OUTSIDE_STAGE3_SCRATCH") from exc
    _refuse_protected_publication_target(resolved)
    return resolved


def command_candidate_manifest(args: argparse.Namespace) -> int:
    output = _require_stage3_scratch(Path(args.out), Path(args.scratch_root))
    write_json(output, build_legacy_manifest(stage3=True))
    print(
        json.dumps(
            {
                "command": "candidate-manifest",
                "gate_version": STAGE3_GATE_VERSION,
                "manifest_sha256": sha256_file(output),
                "outcome": "CANDIDATE_ONLY_NOT_CANONICAL",
                "path": str(output),
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0


def validate_stage3_publication_prerequisites(
    *,
    manifest_path: Path,
    receipt_path: Path,
    authorization_file_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    _refuse_protected_publication_target(output_path)
    if not authorization_file_path.is_file():
        raise SystemExit("STOP_V3_ANCHOR_AUTHORITY_ABSENT")
    if not manifest_path.is_file() or not receipt_path.is_file():
        raise SystemExit("STOP_V3_PREREQUISITE_FILE_ABSENT")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    manifest_sha256 = sha256_file(manifest_path)
    receipt_manifest_sha256 = (receipt.get("legacy_manifest") or {}).get("sha256")
    if manifest.get("gate_version") != STAGE3_GATE_VERSION:
        raise SystemExit("STOP_V3_MANIFEST_GATE_VERSION_MISMATCH")
    if receipt.get("gate_version") != STAGE3_GATE_VERSION:
        raise SystemExit("STOP_V3_RECEIPT_GATE_VERSION_MISMATCH")
    if receipt_manifest_sha256 != manifest_sha256:
        raise SystemExit("STOP_V3_MANIFEST_RECEIPT_HASH_MISMATCH")
    return {
        "anchor_schema_version": "P011_V3_PREREQUISITE_FILE_PRESENCE_v1",
        "gate_version": STAGE3_GATE_VERSION,
        "legacy_manifest_sha256": manifest_sha256,
        "receipt_sha256": sha256_file(receipt_path),
        "authorization_file_presence": {
            "method": "FILE_EXISTS_AND_SHA256_ONLY_NO_SIGNATURE_VERIFICATION",
            "path": str(authorization_file_path.resolve()),
            "sha256": sha256_file(authorization_file_path),
        },
        "references_gate_version": GATE_VERSION,
    }


def command_publish_stage3_prerequisite(args: argparse.Namespace) -> int:
    output = Path(args.out).resolve()
    anchor = validate_stage3_publication_prerequisites(
        manifest_path=Path(args.manifest).resolve(),
        receipt_path=Path(args.receipt).resolve(),
        authorization_file_path=Path(args.authorization_file).resolve(),
        output_path=output,
    )
    write_json(output, anchor)
    print(
        json.dumps(
            {
                "command": "publish-v3-prerequisite",
                "gate_version": STAGE3_GATE_VERSION,
                "outcome": "PUBLISHED_V3_PREREQUISITE_FILE_PRESENCE_RECORD",
                "path": str(output),
                "sha256": sha256_file(output),
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0


def _retired_combined_v2_freeze() -> int:
    raise SystemExit("STOP_RETIRED_COMBINED_GENERATOR_REFUSED")


def build_parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="P0-11 freeze/candidate boundary")
    sub = root.add_subparsers(dest="command", required=True)
    candidate = sub.add_parser("candidate-manifest")
    candidate.add_argument("--out", required=True)
    candidate.add_argument("--scratch-root", required=True)
    candidate.set_defaults(handler=command_candidate_manifest)
    publish = sub.add_parser("publish-v3-prerequisite")
    publish.add_argument("--manifest", required=True)
    publish.add_argument("--receipt", required=True)
    publish.add_argument("--authorization-file", required=True)
    publish.add_argument("--out", required=True)
    publish.set_defaults(handler=command_publish_stage3_prerequisite)
    return root


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
