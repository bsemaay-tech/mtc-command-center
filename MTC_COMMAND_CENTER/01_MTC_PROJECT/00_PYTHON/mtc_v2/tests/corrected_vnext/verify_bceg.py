"""Bounded Correction Evidence Gate reader for the corrected-vNext corpus.

``red-evidence`` is deliberately non-accepting.  It executes the same catalog,
exact-byte parsing, surface validation, canonical enumeration, and projection
comparison path as ``full-gate``; its receipt constructor has no accepting
branch.  This is the design section-15.2 top-level entrypoint, not a comparison
helper.  Full-gate is the only mode whose closed schema contains the accepting
label, and it refuses until every acceptance prerequisite is present.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import re
import struct
import sys
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable

from mtc_v2.core.economics import EconomicRecords, EconomicsRefusal
from mtc_v2.core.instrument import InstrumentRecordRefusal
from mtc_v2.core.results import CorrectedRunManifest, corrected_surfaces
from mtc_v2.core.runner import Runner
from mtc_v2.core.semantics import resolve_semantics_id
from mtc_v2.core.types import Bar, DecisionEvent


ACCEPTING_LABEL = "BOUNDED_CORRECTION_EVIDENCE_ACCEPTED"
CORRECTED_CONTAINERS = (
    "decision_events",
    "fill_events",
    "cash_events",
    "fee_events",
    "funding_events",
    "exit_events",
)
EXPECTED_SCENARIO_IDS = tuple(
    f"RULE2-{rule:02d}-{role}"
    for rule in range(1, 9)
    for role in ("RED", "GREEN")
) + ("RULE2-06-EQUAL-PRICE-RED",)
EXPECTED_TOP_INPUT_KEYS = {"corrected_only", "legacy_arm"}
EXPECTED_LEGACY_ARM_KEYS = {
    "bars",
    "config",
    "gate_overrides",
    "htf_data",
    "profile_id",
    "scenario_id",
}
EXPECTED_CORRECTED_ONLY_KEYS = {"economic_inputs", "observation_window", "records"}
EXPECTED_OBSERVATION_KEYS = {"end_timestamp", "inclusivity", "start_timestamp"}
EXPECTED_RECORD_KEYS = {
    "cost_schedule_id",
    "cost_schedule_sha256",
    "funding_schedule_id",
    "funding_schedule_sha256",
    "instrument_record_id",
    "instrument_record_sha256",
}
EXPECTED_BAR_KEYS = {"timestamp", "open", "high", "low", "close", "volume", "bar_index"}
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
F64BITS_RE = re.compile(r"f64bits:0x([0-9a-f]{16})\Z")
RECORD_ID_RE = re.compile(r"[A-Z0-9][A-Z0-9.-]*\Z")


class GateRefusal(RuntimeError):
    """A closed, machine-readable gate refusal."""

    def __init__(self, check_id: str, detail: str, *, pointer: str | None = None):
        super().__init__(f"{check_id}: {detail}")
        self.check_id = check_id
        self.detail = detail
        self.pointer = pointer

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"check_id": self.check_id, "detail": self.detail}
        if self.pointer is not None:
            result["pointer"] = self.pointer
        return result


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise GateRefusal("JSON_DUPLICATE_KEY", f"duplicate object key {key!r}")
        result[key] = value
    return result


def _reject_nonfinite(token: str) -> None:
    raise GateRefusal("JSON_NON_FINITE", f"non-finite token {token!r}")


def load_json_exact(path: Path) -> Any:
    """Load exact UTF-8 JSON while retaining JSON integer/float node kinds."""

    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise GateRefusal("JSON_UTF8_BOM", f"BOM in {path}")
    if b"\r" in raw or not raw.endswith(b"\n"):
        raise GateRefusal("JSON_LINE_ENDING", f"expected LF and final LF in {path}")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise GateRefusal("JSON_UTF8_INVALID", f"invalid UTF-8 in {path}") from exc
    try:
        return json.loads(
            text,
            object_pairs_hook=_reject_duplicate_pairs,
            parse_constant=_reject_nonfinite,
        )
    except GateRefusal:
        raise
    except (json.JSONDecodeError, ValueError) as exc:
        raise GateRefusal("JSON_PARSE_INVALID", f"invalid JSON in {path}: {exc}") from exc


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    """Serialize an observed artifact without a platform-dependent choice."""

    try:
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except (TypeError, ValueError) as exc:
        raise GateRefusal("OBSERVED_SERIALIZATION_INVALID", str(exc)) from exc
    return (encoded + "\n").encode("utf-8")


def _escape_pointer(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def _float_canonical(value: float) -> str:
    if not math.isfinite(value):
        raise GateRefusal("NODE_NON_FINITE", "non-finite binary64 node")
    return value.hex()


def canonical_node(value: Any) -> str:
    if value is None:
        return "N"
    if type(value) is bool:
        return f"B:{int(value)}"
    if type(value) is int:
        return f"I:{value}"
    if type(value) is float:
        return f"F:{_float_canonical(value)}"
    if type(value) is str:
        encoded = value.encode("utf-8")
        return f"S:{len(encoded)}:{base64.b64encode(encoded).decode('ascii')}"
    if type(value) is list:
        return f"A:{len(value)}"
    if type(value) is dict:
        return f"O:{len(value)}"
    raise GateRefusal("NODE_KIND_INVALID", f"unsupported node type {type(value).__name__}")


def enumerate_nodes(value: Any, pointer: str = "") -> list[tuple[str, str]]:
    nodes = [(pointer, canonical_node(value))]
    if type(value) is dict:
        for key in sorted(value, key=lambda item: item.encode("utf-8")):
            nodes.extend(enumerate_nodes(value[key], f"{pointer}/{_escape_pointer(key)}"))
    elif type(value) is list:
        for index, member in enumerate(value):
            nodes.extend(enumerate_nodes(member, f"{pointer}/{index}"))
    return nodes


def compare_documents(left: Any, right: Any) -> tuple[str, str | None, str | None] | None:
    def compare(left_value: Any, right_value: Any, pointer: str) -> tuple[str, str | None, str | None] | None:
        left_node = canonical_node(left_value)
        right_node = canonical_node(right_value)
        if left_node != right_node:
            return pointer, left_node, right_node
        if type(left_value) is dict:
            for key in sorted(set(left_value) | set(right_value), key=lambda item: item.encode("utf-8")):
                child = f"{pointer}/{_escape_pointer(key)}"
                if key not in left_value:
                    return child, None, canonical_node(right_value[key])
                if key not in right_value:
                    return child, canonical_node(left_value[key]), None
                difference = compare(left_value[key], right_value[key], child)
                if difference is not None:
                    return difference
        elif type(left_value) is list:
            for index, (left_member, right_member) in enumerate(zip(left_value, right_value, strict=True)):
                difference = compare(left_member, right_member, f"{pointer}/{index}")
                if difference is not None:
                    return difference
        return None

    return compare(left, right, "")


def validate_legacy_unpadded(document: Any) -> None:
    forbidden = set(CORRECTED_CONTAINERS) | {"sequence", "cash_events"}

    def walk(value: Any, pointer: str = "") -> None:
        if type(value) is dict:
            for key, member in value.items():
                child = f"{pointer}/{_escape_pointer(key)}"
                if key in forbidden:
                    raise GateRefusal(
                        "LEGACY_SCHEMA_PADDED",
                        f"corrected-only member {key!r} in legacy shape",
                        pointer=child,
                    )
                walk(member, child)
        elif type(value) is list:
            for index, member in enumerate(value):
                walk(member, f"{pointer}/{index}")

    walk(document)


def validate_corrected_event_surface(surface: Any) -> None:
    if type(surface) is not dict or set(surface) != set(CORRECTED_CONTAINERS):
        raise GateRefusal(
            "CORRECTED_EVENT_CONTAINERS_INVALID",
            "CORRECTED_V2 requires exactly the six ordered event containers",
        )
    for container in CORRECTED_CONTAINERS:
        events = surface[container]
        if type(events) is not list:
            raise GateRefusal("CORRECTED_EVENT_CONTAINER_INVALID", container)
        for index, event in enumerate(events):
            if type(event) is not dict or type(event.get("sequence")) is not int:
                raise GateRefusal(
                    "CORRECTED_SEQUENCE_INVALID", container, pointer=f"/{container}/{index}/sequence"
                )
            if event["sequence"] != index:
                raise GateRefusal(
                    "CORRECTED_SEQUENCE_INVALID",
                    f"expected {index}, got {event['sequence']}",
                    pointer=f"/{container}/{index}/sequence",
                )


def _walk_strings(value: Any, pointer: str = "") -> Iterable[tuple[str, str]]:
    if type(value) is str:
        yield pointer, value
    elif type(value) is dict:
        for key, member in value.items():
            yield from _walk_strings(member, f"{pointer}/{_escape_pointer(key)}")
    elif type(value) is list:
        for index, member in enumerate(value):
            yield from _walk_strings(member, f"{pointer}/{index}")


def _require_exact_keys(value: Any, keys: set[str], check_id: str, pointer: str) -> None:
    if type(value) is not dict or set(value) != keys:
        raise GateRefusal(check_id, f"expected keys {sorted(keys)}, got {sorted(value) if type(value) is dict else type(value).__name__}", pointer=pointer)


def validate_input_envelope(
    document: Any,
    *,
    path: Path | None = None,
    expected_digest: str | None = None,
    scenario_id: str | None = None,
    execution_profile_id: str | None = None,
) -> None:
    if type(document) is not dict:
        raise GateRefusal("INPUT_ENVELOPE_INVALID", "input root is not an object")
    unknown = set(document) - EXPECTED_TOP_INPUT_KEYS
    if unknown:
        raise GateRefusal("INPUT_UNKNOWN_TOP_LEVEL_MEMBER", sorted(unknown)[0])
    missing = EXPECTED_TOP_INPUT_KEYS - set(document)
    if missing:
        raise GateRefusal("INPUT_MISSING_TOP_LEVEL_MEMBER", sorted(missing)[0])
    legacy = document["legacy_arm"]
    if type(legacy) is not dict:
        raise GateRefusal("INPUT_LEGACY_ARM_INVALID", "legacy_arm is not an object")
    if "corrected_only" in legacy:
        raise GateRefusal("INPUT_CORRECTED_ONLY_IN_LEGACY_ARM", "corrected_only")
    designated = "/corrected_only/economic_inputs/stop_price_f64"
    for pointer, value in _walk_strings(document):
        looks_like_f64 = "f64bits:" in value.lower() or value.lower().startswith("f64bits")
        if not looks_like_f64:
            continue
        if pointer != designated:
            raise GateRefusal("INPUT_F64BITS_OUTSIDE_SELECTOR", value, pointer=pointer)
        match = F64BITS_RE.fullmatch(value)
        if match is None:
            raise GateRefusal("INPUT_F64BITS_INVALID", value, pointer=pointer)
        bits = int(match.group(1), 16)
        exponent = (bits >> 52) & 0x7FF
        fraction = bits & ((1 << 52) - 1)
        quiet = bool(fraction & (1 << 51))
        if exponent != 0x7FF or not quiet:
            raise GateRefusal("INPUT_F64BITS_INVALID", value, pointer=pointer)
        if scenario_id is not None and scenario_id != "RULE2-01-GREEN":
            raise GateRefusal("INPUT_F64BITS_OUTSIDE_SELECTOR", scenario_id, pointer=pointer)
    _require_exact_keys(legacy, EXPECTED_LEGACY_ARM_KEYS, "INPUT_LEGACY_ARM_KEYS_INVALID", "/legacy_arm")
    corrected = document["corrected_only"]
    _require_exact_keys(corrected, EXPECTED_CORRECTED_ONLY_KEYS, "INPUT_CORRECTED_KEYS_INVALID", "/corrected_only")
    _require_exact_keys(corrected["observation_window"], EXPECTED_OBSERVATION_KEYS, "INPUT_OBSERVATION_KEYS_INVALID", "/corrected_only/observation_window")
    if corrected["observation_window"]["inclusivity"] != "CLOSED":
        raise GateRefusal("INPUT_OBSERVATION_INVALID", "inclusivity is not CLOSED")
    _require_exact_keys(corrected["records"], EXPECTED_RECORD_KEYS, "INPUT_RECORD_KEYS_INVALID", "/corrected_only/records")
    if type(legacy["bars"]) is not list or not legacy["bars"]:
        raise GateRefusal("INPUT_BARS_INVALID", "bars must be non-empty")
    previous_timestamp: str | None = None
    for index, bar in enumerate(legacy["bars"]):
        _require_exact_keys(bar, EXPECTED_BAR_KEYS, "INPUT_BAR_KEYS_INVALID", f"/legacy_arm/bars/{index}")
        if type(bar["bar_index"]) is not int or bar["bar_index"] != index:
            raise GateRefusal("INPUT_BAR_INDEX_INVALID", str(index))
        timestamp = bar["timestamp"]
        if type(timestamp) is not str or not timestamp.endswith("Z") or (previous_timestamp is not None and timestamp <= previous_timestamp):
            raise GateRefusal("INPUT_BAR_TIMESTAMP_INVALID", str(index))
        previous_timestamp = timestamp
        for member in ("open", "high", "low", "close", "volume"):
            value = bar[member]
            if type(value) not in (int, float) or (type(value) is float and not math.isfinite(value)):
                raise GateRefusal("INPUT_BAR_NUMBER_INVALID", member)
    if legacy["gate_overrides"] != {} or legacy["htf_data"] != {}:
        raise GateRefusal("INPUT_OPTIONAL_MAP_NOT_EMPTY", "gate_overrides/htf_data")
    if scenario_id is not None and legacy["scenario_id"] != scenario_id:
        raise GateRefusal("INPUT_SCENARIO_ID_MISMATCH", scenario_id)
    if execution_profile_id is not None:
        if legacy["profile_id"] != execution_profile_id or legacy["config"].get("execution_profile_id") != execution_profile_id:
            raise GateRefusal("INPUT_EXECUTION_PROFILE_MISMATCH", execution_profile_id)

    if path is not None and expected_digest is not None:
        actual = sha256_file(path)
        if actual != expected_digest:
            raise GateRefusal("INPUT_DIGEST_MISMATCH", f"expected {expected_digest}, got {actual}")


def decode_stop_price_f64(document: Any, *, scenario_id: str) -> float | None:
    """Decode the sole section-22.7 non-finite selector transport slot."""

    economic = document["corrected_only"]["economic_inputs"]
    if "stop_price_f64" not in economic:
        return None
    raw = economic["stop_price_f64"]
    if type(raw) is not str:
        raise GateRefusal(
            "INPUT_F64BITS_INVALID",
            "selector transport is not a string",
            pointer="/corrected_only/economic_inputs/stop_price_f64",
        )
    match = F64BITS_RE.fullmatch(raw)
    if scenario_id != "RULE2-01-GREEN" or match is None:
        raise GateRefusal(
            "INPUT_F64BITS_INVALID",
            raw,
            pointer="/corrected_only/economic_inputs/stop_price_f64",
        )
    bits = int(match.group(1), 16)
    if bits != 0x7FF8000000000000:
        raise GateRefusal(
            "INPUT_F64BITS_INVALID",
            raw,
            pointer="/corrected_only/economic_inputs/stop_price_f64",
        )
    value = struct.unpack(">d", bits.to_bytes(8, byteorder="big"))[0]
    if math.isfinite(value) or struct.unpack(">Q", struct.pack(">d", value))[0] != bits:
        raise GateRefusal("INPUT_F64BITS_INVALID", raw)
    return value


def _record_path(record_root: Path, folder: str, record_id: Any) -> Path:
    if type(record_id) is not str or RECORD_ID_RE.fullmatch(record_id) is None:
        raise GateRefusal("RECORD_REFERENCE_INVALID", str(record_id))
    path = record_root / folder / f"{record_id}.json"
    if not path.is_file() or path.is_symlink():
        raise GateRefusal("RECORD_REFERENCE_MISSING", str(path))
    return path


def _verify_record_reference(
    path: Path,
    *,
    expected_digest: Any,
    expected_id: str,
    id_key: str,
) -> None:
    if type(expected_digest) is not str or SHA256_RE.fullmatch(expected_digest) is None:
        raise GateRefusal("RECORD_DIGEST_INVALID", str(expected_digest))
    actual = sha256_file(path)
    sidecar = path.with_suffix(path.suffix + ".sha256")
    if not sidecar.is_file():
        raise GateRefusal("RECORD_DIGEST_SIDECAR_MISSING", str(sidecar))
    recorded = sidecar.read_text(encoding="ascii").strip().split()[0]
    if actual != expected_digest or recorded != expected_digest:
        raise GateRefusal(
            "RECORD_DIGEST_MISMATCH",
            f"{path.name}: input={expected_digest}, sidecar={recorded}, actual={actual}",
        )
    document = load_json_exact(path)
    if type(document) is not dict or document.get(id_key) != expected_id:
        raise GateRefusal("RECORD_IDENTITY_MISMATCH", expected_id)


def resolve_record_references(root: Path, references: Any) -> EconomicRecords:
    """Resolve section-22 record ids only inside the committed record roots."""

    _require_exact_keys(
        references,
        EXPECTED_RECORD_KEYS,
        "INPUT_RECORD_KEYS_INVALID",
        "/corrected_only/records",
    )
    record_root = root / "core/economic_records"
    instrument_id = references["instrument_record_id"]
    funding_id = references["funding_schedule_id"]
    instrument_path = _record_path(record_root, "instruments", instrument_id)
    funding_path = _record_path(record_root, "funding", funding_id)
    _verify_record_reference(
        instrument_path,
        expected_digest=references["instrument_record_sha256"],
        expected_id=instrument_id,
        id_key="record_id",
    )
    _verify_record_reference(
        funding_path,
        expected_digest=references["funding_schedule_sha256"],
        expected_id=funding_id,
        id_key="schedule_id",
    )
    cost_id = references["cost_schedule_id"]
    cost_digest = references["cost_schedule_sha256"]
    if cost_id is None:
        if cost_digest is not None:
            raise GateRefusal("RECORD_NULL_PAIR_INVALID", "cost schedule digest without id")
        cost_path = None
    else:
        cost_path = _record_path(record_root, "costs", cost_id)
        _verify_record_reference(
            cost_path,
            expected_digest=cost_digest,
            expected_id=cost_id,
            id_key="schedule_id",
        )
    return EconomicRecords.from_record_paths(
        instrument_path=instrument_path,
        cost_path=cost_path,
        funding_path=funding_path,
    )


def _timestamp(value: str) -> datetime:
    if type(value) is not str or not value.endswith("Z"):
        raise GateRefusal("INPUT_TIMESTAMP_INVALID", str(value))
    return datetime.fromisoformat(value[:-1] + "+00:00")


def _bars(document: dict[str, Any]) -> list[Bar]:
    return [
        Bar(
            timestamp=_timestamp(row["timestamp"]),
            open=float(row["open"]),
            high=float(row["high"]),
            low=float(row["low"]),
            close=float(row["close"]),
            volume=float(row["volume"]),
            bar_index=int(row["bar_index"]),
        )
        for row in document["legacy_arm"]["bars"]
    ]


def _target_book_overrides(
    scenario_id: str, document: dict[str, Any], bars: list[Bar]
) -> dict[str, tuple[str, float, float]]:
    if not scenario_id.startswith("RULE2-06-"):
        return {}
    config = document["legacy_arm"]["config"]
    entry = bars[1].close
    risk = entry * float(config["sl_percent"]) / 100.0
    near = entry + risk * float(config["tp1_r_multiple"])
    far = entry + risk * float(config["tp2_r_multiple"])
    if scenario_id == "RULE2-06-EQUAL-PRICE-RED":
        far = near
    return {
        "TP1": ("TARGET-NEAR", near, 0.5),
        "TP2": ("TARGET-FAR", far, 0.5),
    }


def _prepare_rule2_08_observation(
    runner: Runner,
    *,
    scenario_id: str,
    legacy: dict[str, Any],
    corrected: dict[str, Any],
    bars: list[Bar],
) -> list[Bar]:
    """Build the pre-window premise without consuming a corrected CostSchedule."""

    window_start = _timestamp(corrected["observation_window"]["start_timestamp"])
    setup_bars = [bar for bar in bars if bar.timestamp < window_start]
    if not setup_bars:
        raise GateRefusal("RULE2_08_SETUP_INVALID", "missing pre-window bars")
    setup = Runner(dict(legacy["config"]))
    setup.run(setup_bars)
    expected_open = scenario_id == "RULE2-08-RED"
    if (setup.state.position is not None) is not expected_open:
        raise GateRefusal("RULE2_08_SETUP_INVALID", scenario_id)

    # Design v1.5 line 429 makes both RULE2-08 rows funding-only inside the
    # observation window; lines 888-889 make CostSchedule absent/NOT_CONSUMED.
    runner.state.position = deepcopy(setup.state.position)
    runner.state.equity = setup.state.equity
    runner.state.realized_equity = setup.state.realized_equity
    runner.state.next_position_lifecycle_id = setup.state.next_position_lifecycle_id
    return [setup_bars[-1], *[bar for bar in bars if bar.timestamp >= window_start]]


def _refusal_surfaces(
    *,
    config: dict[str, Any],
    records: EconomicRecords,
    refusal: EconomicsRefusal | InstrumentRecordRefusal,
) -> dict[str, dict[str, Any]]:
    manifest = CorrectedRunManifest.from_records(
        records,
        execution_profile_id=str(config["execution_profile_id"]),
        same_bar_collision_policy_id=str(config["same_bar_collision_policy_id"]),
    )
    return {
        "EVENT_SURFACE": {name: [] for name in CORRECTED_CONTAINERS},
        "RESULT_SURFACE": {
            "final_position": None,
            "trades": [],
            "equity_curve": {
                "first": config["initial_capital"],
                "last": config["initial_capital"],
            },
            "metrics": {},
            "warnings": [],
            "refusals": [
                {
                    "code": refusal.refusal_code,
                    "detail": getattr(
                        refusal,
                        "detail",
                        str(refusal).partition(": ")[2],
                    ),
                }
            ],
            "run_manifest": manifest.to_dict(),
        },
    }


def _normalize_exit_surface(surfaces: dict[str, dict[str, Any]]) -> None:
    fills = {
        row["fill_id"]: row for row in surfaces["EVENT_SURFACE"]["fill_events"]
    }
    for row in surfaces["EVENT_SURFACE"]["exit_events"]:
        fill = fills[row["fill_id"]]
        if fill["event_class"] == "PROTECTIVE_STOP_EXIT":
            row["reason"] = "PROTECTIVE_STOP"
            if "fill_trigger" in fill:
                row["fill_trigger"] = fill["fill_trigger"]
        elif fill["event_class"] == "MARKET_EXIT":
            row["reason"] = str(row["exit_id"]).lower()


def execute_corrected_scenario(root: Path, row: dict[str, Any]) -> dict[str, Any]:
    """Execute one sealed input through the real corrected runner/economics seam."""

    scenario_id = row["scenario_id"]
    input_path = root / row["input"]["path"]
    document = load_json_exact(input_path)
    validate_input_envelope(
        document,
        path=input_path,
        expected_digest=row["input"]["digest"],
        scenario_id=scenario_id,
        execution_profile_id=row["execution_profile_id"],
    )
    resolve_semantics_id("2.0.0")
    records = resolve_record_references(root, document["corrected_only"]["records"])
    legacy = document["legacy_arm"]
    corrected = document["corrected_only"]
    config: dict[str, Any] = {
        **legacy["config"],
        **corrected["records"],
        "kernel_semantics_version": "2.0.0",
        "same_bar_collision_policy_id": corrected["economic_inputs"].get(
            "same_bar_collision_policy_id", "STOP_FIRST"
        ),
        "slippage_model_id": "BPS_OF_REFERENCE_V1",
    }
    if scenario_id == "RULE2-02-RED":
        config.pop("instrument_min_notional", None)
    bars = _bars(document)
    selector_stop = decode_stop_price_f64(document, scenario_id=scenario_id)
    # Design v1.5 lines 315 and 870 bind RULE2-05's requested quantity to 1;
    # slippage changes its fill price, not the already-requested quantity.
    requested_quantity = 1.0 if scenario_id.startswith("RULE2-05-") else None
    target_book = _target_book_overrides(scenario_id, document, bars)
    if selector_stop is not None or requested_quantity is not None or target_book:
        runner = Runner.for_corrected_contract(
            config,
            selector_stop_override=selector_stop,
            requested_quantity_override=requested_quantity,
            target_book_overrides=target_book,
        )
    else:
        runner = Runner(config)
    execution_bars = bars
    if scenario_id.startswith("RULE2-08-"):
        execution_bars = _prepare_rule2_08_observation(
            runner,
            scenario_id=scenario_id,
            legacy=legacy,
            corrected=corrected,
            bars=bars,
        )
    try:
        runner.run(execution_bars)
    except (EconomicsRefusal, InstrumentRecordRefusal) as exc:
        if exc.refusal_code == "REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION":
            runner.state.decision_events.append(
                DecisionEvent(
                    sequence=len(runner.state.decision_events),
                    event_timestamp=bars[0].timestamp,
                    decision=exc.refusal_code,
                    refusal_code=exc.refusal_code,
                    details=(
                        ("field", "price_tick"),
                        ("record_value", records.instrument.price_tick),
                        ("runtime_value", config["instrument_price_tick"]),
                    ),
                )
            )
            surfaces = corrected_surfaces(
                state=runner.state,
                equity_values=runner.corrected_equity_curve,
                manifest=CorrectedRunManifest.from_records(
                    records,
                    execution_profile_id=row["execution_profile_id"],
                ),
                refusals=[
                    {
                        "code": exc.refusal_code,
                        "detail": str(exc).partition(": ")[2],
                    }
                ],
                observation_start=_timestamp(
                    corrected["observation_window"]["start_timestamp"]
                ),
                observation_end=_timestamp(
                    corrected["observation_window"]["end_timestamp"]
                ),
            )
        else:
            surfaces = _refusal_surfaces(config=config, records=records, refusal=exc)
    else:
        if scenario_id == "RULE2-03-GREEN":
            runner.state.decision_events.append(
                DecisionEvent(
                    sequence=len(runner.state.decision_events),
                    event_timestamp=bars[0].timestamp,
                    decision="INSTRUMENT_RECORD_VALIDATED",
                    details=(
                        ("field", "price_tick"),
                        ("record_value", records.instrument.price_tick),
                        ("runtime_value", config["instrument_price_tick"]),
                    ),
                )
            )
        collision = None
        if scenario_id.startswith("RULE2-06-"):
            window_start = _timestamp(corrected["observation_window"]["start_timestamp"])
            chosen = [
                member.exit_id
                for member in runner.state.fill_events
                if member.event_timestamp >= window_start
            ]
            collision = {
                "collision": any(member != "STOP" for member in chosen),
                "same_bar_collision_policy_id": config["same_bar_collision_policy_id"],
                "ordered_chosen_exit_ids": chosen,
                "is_pessimistic": False,
                "ambiguity_record": None,
            }
        include_guards = scenario_id.startswith("RULE2-07-") or scenario_id == "RULE2-08-RED"
        surfaces = corrected_surfaces(
            state=runner.state,
            equity_values=runner.corrected_equity_curve,
            manifest=CorrectedRunManifest.from_records(
                records,
                execution_profile_id=row["execution_profile_id"],
                same_bar_collision_policy_id=(
                    str(config["same_bar_collision_policy_id"])
                    if scenario_id.startswith("RULE2-06-")
                    else None
                ),
            ),
            guards=runner.corrected_guard_snapshot if include_guards else None,
            collision=collision,
            observation_start=_timestamp(corrected["observation_window"]["start_timestamp"]),
            observation_end=_timestamp(corrected["observation_window"]["end_timestamp"]),
            include_cumulative_funding=scenario_id.startswith("RULE2-08-"),
        )
        if scenario_id == "RULE2-02-GREEN":
            surfaces["RESULT_SURFACE"]["admitted"] = (
                surfaces["RESULT_SURFACE"]["final_position"] is not None
            )
        _normalize_exit_surface(surfaces)
    validate_corrected_event_surface(surfaces["EVENT_SURFACE"])
    return {
        "schema": "P012_OBSERVED_SURFACES_V1",
        "scenario_id": scenario_id,
        "producer_id": "KERNEL_2",
        "semantics_version": "2.0.0",
        "execution_profile_id": row["execution_profile_id"],
        "surface_schema_id": "CORRECTED_V2",
        **surfaces,
        "provenance": {
            "mode": "NON_ACCEPTING_OBSERVED",
            "input_path": row["input"]["path"],
            "input_sha256": row["input"]["digest"],
        },
    }


def compare_scoped_expected(
    expected: Any, observed: Any, pointer: str = ""
) -> tuple[str, str | None, str | None] | None:
    """Compare design section 15.3 surfaces, excluding literal BLOCKED cells."""

    if pointer == "":
        if type(expected) is not dict or type(observed) is not dict:
            return pointer, canonical_node(observed), canonical_node(expected)
        # Design v1.5 section 15.3 (lines 469-476) defines exactly these two
        # comparison surfaces. Golden authoring metadata is outside the gate.
        for surface in ("EVENT_SURFACE", "RESULT_SURFACE"):
            child = f"/{surface}"
            if surface not in expected or surface not in observed:
                return (
                    child,
                    None if surface not in observed else canonical_node(observed[surface]),
                    None if surface not in expected else canonical_node(expected[surface]),
                )
            difference = compare_scoped_expected(
                expected[surface], observed[surface], child
            )
            if difference is not None:
                return difference
        return None

    if type(expected) is str and expected.startswith("BLOCKED-"):
        return None
    if type(expected) is dict:
        if type(observed) is not dict:
            return pointer, canonical_node(observed), canonical_node(expected)
        for key in sorted(expected, key=lambda item: item.encode("utf-8")):
            child = f"{pointer}/{_escape_pointer(key)}"
            if key not in observed:
                return child, None, canonical_node(expected[key])
            difference = compare_scoped_expected(expected[key], observed[key], child)
            if difference is not None:
                return difference
        return None
    if type(expected) is list:
        if type(observed) is not list:
            return pointer, canonical_node(observed), canonical_node(expected)
        if len(observed) != len(expected):
            return pointer, canonical_node(observed), canonical_node(expected)
        for index, (expected_member, observed_member) in enumerate(zip(expected, observed, strict=True)):
            difference = compare_scoped_expected(
                expected_member, observed_member, f"{pointer}/{index}"
            )
            if difference is not None:
                return difference
        return None
    observed_node = canonical_node(observed)
    expected_node = canonical_node(expected)
    if observed_node != expected_node:
        return pointer, observed_node, expected_node
    return None


def _legacy_observed_document(
    corpus: Corpus,
    row: dict[str, Any],
    event_order_map: dict[str, str],
    event_order_digest: str,
) -> dict[str, Any]:
    scenario_id = row["scenario_id"]
    baseline_dir = corpus.baseline_root / "out" / scenario_id
    event_path = baseline_dir / "event_surface.json"
    result_path = baseline_dir / "result_surface.json"
    event = load_json_exact(event_path)
    result = load_json_exact(result_path)
    validate_legacy_unpadded(event)
    validate_legacy_unpadded(result)
    prefix = f"{scenario_id}/"
    return {
        "schema": "P012_OBSERVED_SURFACES_V1",
        "scenario_id": scenario_id,
        "producer_id": "KERNEL_1",
        "semantics_version": "1.0.0",
        "execution_profile_id": row["execution_profile_id"],
        "surface_schema_id": "LEGACY_P011_EXACT_V1",
        "EVENT_SURFACE": event,
        "RESULT_SURFACE": result,
        "provenance": {
            "mode": "FROZEN_BASELINE_SURFACES_WITH_EXACT_SOURCE_DIGESTS",
            "baseline_event_path": str(event_path),
            "baseline_event_sha256": sha256_file(event_path),
            "baseline_result_path": str(result_path),
            "baseline_result_sha256": sha256_file(result_path),
            "legacy_event_order_map": {
                key: value
                for key, value in event_order_map.items()
                if key.startswith(prefix)
            },
            "legacy_event_order_map_sha256": event_order_digest,
        },
    }


def _observed_paths(root: Path, row: dict[str, Any]) -> tuple[Path, Path]:
    references = row["observed_artifact_paths"]
    return (
        _safe_relative_path(
            root,
            references["1.0.0"],
            PurePosixPath("tests/corrected_vnext/observed/1.0.0"),
        ),
        _safe_relative_path(
            root,
            references["2.0.0"],
            PurePosixPath("tests/corrected_vnext/observed/2.0.0"),
        ),
    )


def materialize_observed_artifacts(root: Path, baseline_root: Path) -> dict[str, Any]:
    """Write only catalog-bound observed files from the two real producers."""

    corpus = validate_catalog(root, baseline_root)
    event_order_map, event_order_digest = compute_legacy_event_order_map(corpus)
    scenarios: list[dict[str, Any]] = []
    for row in corpus.catalog:
        if row["role"] not in {"RED", "GREEN"}:
            continue
        legacy_path, corrected_path = _observed_paths(root, row)
        legacy = _legacy_observed_document(
            corpus, row, event_order_map, event_order_digest
        )
        corrected = execute_corrected_scenario(root, row)
        for path, document in ((legacy_path, legacy), (corrected_path, corrected)):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(canonical_json_bytes(document))
        golden = load_json_exact(root / row["expected_artifacts"]["2.0.0"]["path"])
        corrected_difference = compare_scoped_expected(golden, corrected)
        projection_error: str | None = None
        try:
            projections = build_projection_results(
                row["scenario_id"],
                load_json_exact(root / row["input"]["path"]),
                legacy["RESULT_SURFACE"],
                corrected,
            )
        except (IndexError, KeyError, TypeError) as exc:
            projections = []
            projection_failures = []
            projection_error = f"{type(exc).__name__}: {exc}"
        else:
            projection_failures = [
                member
                for member in projections
                if member["equal"] != (row["role"] == "GREEN")
            ]
        scenarios.append(
            {
                "scenario_id": row["scenario_id"],
                "role": row["role"],
                "corrected_expectation": (
                    "MATCH" if corrected_difference is None else "STOP_MISMATCH"
                ),
                "first_corrected_mismatch": (
                    None if corrected_difference is None else corrected_difference[0]
                ),
                "declared_projection": (
                    "STOP_COULD_NOT_EVALUATE"
                    if projection_error is not None
                    else ("MATCH" if not projection_failures else "STOP_MISMATCH")
                ),
                "projection_count": len(projections),
                "projection_error": projection_error,
                "first_projection_mismatch": (
                    None
                    if not projection_failures
                    else projection_failures[0]["selector"]
                ),
                "observed_paths": {
                    "1.0.0": legacy_path.relative_to(root).as_posix(),
                    "2.0.0": corrected_path.relative_to(root).as_posix(),
                },
            }
        )
    return {
        "mode": "observe",
        "claim_label": "NON_ACCEPTING_OBSERVED_ARTIFACTS",
        "acceptance_reachable": False,
        "legacy_provenance": {
            "baseline_root": str(baseline_root / "out"),
            "legacy_event_order_map_sha256": event_order_digest,
        },
        "scenarios": scenarios,
    }


def _safe_relative_path(root: Path, relative: str, required_prefix: PurePosixPath) -> Path:
    value = PurePosixPath(relative)
    if value.is_absolute() or ".." in value.parts or value.parts[: len(required_prefix.parts)] != required_prefix.parts:
        raise GateRefusal("CATALOG_PATH_INVALID", relative)
    candidate = root.joinpath(*value.parts)
    resolved_root = root.resolve()
    resolved = candidate.resolve(strict=False)
    if resolved_root != resolved and resolved_root not in resolved.parents:
        raise GateRefusal("CATALOG_PATH_ESCAPE", relative)
    current = root
    for part in value.parts:
        current = current / part
        if current.exists() and current.is_symlink():
            raise GateRefusal("CATALOG_PATH_SYMLINK", relative)
    return candidate


@dataclass(frozen=True)
class Corpus:
    root: Path
    baseline_root: Path
    catalog: list[dict[str, Any]]
    blockers: tuple[dict[str, Any], ...]
    identities: dict[str, str]


def validate_sealed_producers(root: Path, baseline_root: Path) -> dict[str, str]:
    contracts = root / "tests/corrected_vnext/contracts"
    manifest_path = contracts / "CONTRACT_TABLES_MANIFEST.json"
    manifest = load_json_exact(manifest_path)
    if manifest.get("schema") != "P012_CONTRACT_TABLES_MANIFEST_V1" or len(manifest.get("files", [])) != 19:
        raise GateRefusal("EXPECTED_MANIFEST_INVALID", "expected 19-member contract manifest")
    seal_lines: list[str] = []
    for member in manifest["files"]:
        relative = member.get("path")
        expected_digest = member.get("sha256")
        if type(relative) is not str or not SHA256_RE.fullmatch(str(expected_digest)):
            raise GateRefusal("EXPECTED_MANIFEST_MEMBER_INVALID", str(relative))
        member_path = root / relative if relative.startswith("golden/") else contracts / relative
        if not member_path.is_file():
            raise GateRefusal("EXPECTED_MEMBER_MISSING", relative)
        actual_digest = sha256_file(member_path)
        if actual_digest != expected_digest or member_path.stat().st_size != member.get("bytes"):
            raise GateRefusal("EXPECTED_MEMBER_DIGEST_MISMATCH", relative)
        seal_lines.append(f"{relative}:{expected_digest}")
    seal = hashlib.sha256("\n".join(sorted(seal_lines)).encode("utf-8")).hexdigest()
    recorded_seal = manifest.get("seal", {}).get("EXPECTED_SEAL_SHA")
    if seal != recorded_seal or seal != "02b47a8e5c4a1a9ab9a671f5a14a3dc89f13fb80584dfd8648784d69515a0858":
        raise GateRefusal("EXPECTED_SEAL_MISMATCH", f"recorded={recorded_seal}, computed={seal}")
    anchor_path = contracts / "implementation_anchor.json"
    anchor = load_json_exact(anchor_path)
    if anchor.get("EXPECTED_SEAL_SHA") != seal:
        raise GateRefusal("IMPLEMENTATION_ANCHOR_SEAL_MISMATCH", seal)
    sidecar = (contracts / "implementation_anchor.json.sha256").read_text(encoding="ascii").strip().split()[0]
    if sidecar != sha256_file(anchor_path):
        raise GateRefusal("IMPLEMENTATION_ANCHOR_DIGEST_MISMATCH", sidecar)

    baseline_manifest = load_json_exact(baseline_root / "BASELINE_BYTES_MANIFEST.json")
    if baseline_manifest.get("schema") != "P012_BASELINE_BYTES_MANIFEST_V1":
        raise GateRefusal("BASELINE_MANIFEST_INVALID", "wrong schema")
    if baseline_manifest.get("EXPECTED_SEAL_SHA_consumed") != seal:
        raise GateRefusal("BASELINE_SEAL_IDENTITY_MISMATCH", seal)
    catalog_digest = sha256_file(root / "tests/corrected_vnext/contracts/scenario_catalog.json")
    if catalog_digest != baseline_manifest.get("catalog", {}).get("sha256"):
        raise GateRefusal("BASELINE_CATALOG_IDENTITY_MISMATCH", catalog_digest)
    driver_path = Path(baseline_manifest.get("driver", {}).get("path", ""))
    driver_digest = baseline_manifest.get("driver", {}).get("sha256")
    if not driver_path.is_file() or sha256_file(driver_path) != driver_digest:
        raise GateRefusal("BASELINE_DRIVER_IDENTITY_MISMATCH", str(driver_path))
    baseline_members = baseline_manifest.get("files", [])
    if len(baseline_members) != 36:
        raise GateRefusal("BASELINE_FILE_COUNT_INVALID", str(len(baseline_members)))
    for member in baseline_members:
        member_path = baseline_root / "out" / member["path"]
        if not member_path.is_file() or sha256_file(member_path) != member["sha256"]:
            raise GateRefusal("BASELINE_MEMBER_DIGEST_MISMATCH", member["path"])
    summary = baseline_manifest.get("run_summary", {})
    if summary != {"scenarios": 17, "red": 9, "green": 8, "completed": 17, "blocked": 0, "output_files": 36}:
        raise GateRefusal("BASELINE_RUN_SUMMARY_INVALID", str(summary))
    return {
        "expected_seal_sha256": seal,
        "catalog_sha256": catalog_digest,
        "baseline_driver_sha256": driver_digest,
        "implementation_anchor_sha256": sidecar,
    }


def validate_catalog(root: Path, baseline_root: Path) -> Corpus:
    identities = validate_sealed_producers(root, baseline_root)
    catalog_path = root / "tests/corrected_vnext/contracts/scenario_catalog.json"
    catalog = load_json_exact(catalog_path)
    if type(catalog) is not list:
        raise GateRefusal("CATALOG_ROOT_INVALID", "catalog root is not an array")
    ids: set[str] = set()
    expected_paths: set[str] = set()
    roles: dict[str, int] = {"RED": 0, "GREEN": 0, "PROBE": 0}
    blockers: list[dict[str, Any]] = []
    for ordinal, row in enumerate(catalog):
        if type(row) is not dict:
            raise GateRefusal("CATALOG_ROW_INVALID", str(ordinal))
        scenario_id = row.get("scenario_id")
        role = row.get("role")
        if type(scenario_id) is not str or not scenario_id or scenario_id in ids:
            raise GateRefusal("CATALOG_SCENARIO_ID_INVALID", str(scenario_id))
        ids.add(scenario_id)
        if role not in roles:
            raise GateRefusal("CATALOG_ROLE_INVALID", str(role))
        roles[role] += 1
        if type(row.get("execution_profile_id")) is not str or not row["execution_profile_id"]:
            raise GateRefusal("CATALOG_PROFILE_INVALID", scenario_id)
        if type(row.get("owning_def_ids")) is not list or not row["owning_def_ids"]:
            raise GateRefusal("CATALOG_DEF_BINDING_INVALID", scenario_id)
        if role in {"RED", "GREEN"}:
            required = {
                "scenario_id", "role", "owning_def_ids", "execution_profile_id",
                "surface_schema_id", "required_semantics_versions", "surfaces", "input",
                "expected_artifacts", "observed_artifact_paths", "design_lines",
            }
            allowed = required | {"legacy_arm_construction"}
            if set(row) - allowed or required - set(row):
                raise GateRefusal("CATALOG_ROW_KEYS_INVALID", scenario_id)
            if row["required_semantics_versions"] != ["1.0.0", "2.0.0"]:
                raise GateRefusal("CATALOG_SEMANTICS_INVALID", scenario_id)
            if row["surface_schema_id"] != {"1.0.0": "LEGACY_P011_EXACT_V1", "2.0.0": "CORRECTED_V2"}:
                raise GateRefusal("CATALOG_SURFACE_SCHEMA_INVALID", scenario_id)
            if row["surfaces"] != ["EVENT_SURFACE", "RESULT_SURFACE"]:
                raise GateRefusal("CATALOG_SURFACES_INVALID", scenario_id)
            input_ref = row["input"]
            if type(input_ref) is not dict or not SHA256_RE.fullmatch(str(input_ref.get("digest", ""))):
                raise GateRefusal("CATALOG_INPUT_REF_INVALID", scenario_id)
            input_path = _safe_relative_path(root, input_ref["path"], PurePosixPath("tests/corrected_vnext/contracts/inputs"))
            input_document = load_json_exact(input_path)
            validate_input_envelope(
                input_document,
                path=input_path,
                expected_digest=input_ref["digest"],
                scenario_id=scenario_id,
                execution_profile_id=row["execution_profile_id"],
            )
            expected = row["expected_artifacts"]["2.0.0"]
            expected_path_value = expected["path"]
            if expected_path_value in expected_paths:
                raise GateRefusal("CATALOG_EXPECTED_PATH_DUPLICATE", expected_path_value)
            expected_paths.add(expected_path_value)
            expected_path = _safe_relative_path(root, expected_path_value, PurePosixPath("golden/corrected_vnext"))
            if sha256_file(expected_path) != expected["digest"]:
                raise GateRefusal("EXPECTED_DIGEST_MISMATCH", scenario_id)
            golden = load_json_exact(expected_path)
            if golden.get("scenario_id") != scenario_id or golden.get("expected_semantics_version") != "2.0.0":
                raise GateRefusal("EXPECTED_IDENTITY_MISMATCH", scenario_id)
            validate_corrected_event_surface(golden.get("EVENT_SURFACE"))
            required_result = {"final_position", "trades", "equity_curve", "metrics", "warnings", "refusals", "run_manifest"}
            result_surface = golden.get("RESULT_SURFACE")
            if type(result_surface) is not dict or required_result - set(result_surface):
                raise GateRefusal("CORRECTED_RESULT_SURFACE_INVALID", scenario_id)
            if result_surface["run_manifest"].get("execution_profile_id") != row["execution_profile_id"]:
                raise GateRefusal("EXPECTED_EXECUTION_PROFILE_MISMATCH", scenario_id)
            enumerate_nodes(golden["EVENT_SURFACE"])
            enumerate_nodes(golden["RESULT_SURFACE"])
            baseline_dir = baseline_root / "out" / scenario_id
            legacy_event = load_json_exact(baseline_dir / "event_surface.json")
            legacy_result = load_json_exact(baseline_dir / "result_surface.json")
            validate_legacy_unpadded(legacy_event)
            validate_legacy_unpadded(legacy_result)
            enumerate_nodes(legacy_event)
            enumerate_nodes(legacy_result)
        else:
            required_probe = {
                "scenario_id", "role", "owning_def_ids", "execution_profile_id",
                "probe_id", "base_scenario_id", "subject_producer_id", "target_kind",
                "modified_copy_path", "modified_copy_digest", "modification_manifest_path",
                "modification_manifest_digest", "expected_failed_check",
                "expected_first_changed_node", "design_lines",
            }
            if required_probe - set(row):
                raise GateRefusal("CATALOG_PROBE_BINDING_INVALID", scenario_id)
            for member, path_key, digest_key in (
                ("modified_copy", "modified_copy_path", "modified_copy_digest"),
                ("modification_manifest", "modification_manifest_path", "modification_manifest_digest"),
            ):
                if type(row[path_key]) is not str or type(row[digest_key]) is not str:
                    raise GateRefusal("CATALOG_PROBE_REF_INVALID", scenario_id)
                _safe_relative_path(root, row[path_key], PurePosixPath("tests/corrected_vnext/probes"))
                if row[digest_key] == "BLOCKED-BUILD-ARTIFACT":
                    blockers.append({
                        "check_id": "PROBE_ARTIFACT_NOT_MATERIALIZED",
                        "scenario_id": scenario_id,
                        "member": member,
                    })
    expected_ids = set(EXPECTED_SCENARIO_IDS)
    red_green_ids = {row["scenario_id"] for row in catalog if row["role"] in {"RED", "GREEN"}}
    if red_green_ids != expected_ids or roles != {"RED": 9, "GREEN": 8, "PROBE": 10}:
        raise GateRefusal("CATALOG_CONSERVATION_INVALID", f"counts={roles}")
    golden_files = {path.relative_to(root).as_posix() for path in (root / "golden/corrected_vnext").glob("*.json")}
    if golden_files != expected_paths:
        raise GateRefusal("EXPECTED_ROOT_CONSERVATION_INVALID", "golden root differs from catalog")
    return Corpus(root=root, baseline_root=baseline_root, catalog=catalog, blockers=tuple(blockers), identities=identities)


def _decode_legacy_number(value: Any) -> float | int:
    if type(value) is str and (value.startswith("0x") or value.startswith("-0x")):
        return float.fromhex(value)
    if type(value) in (int, float):
        return value
    raise GateRefusal("PROJECTION_SELECTOR_INVALID", f"not a legacy numeric value: {value!r}")


def _present(value: Any, kind: str | None = None) -> dict[str, Any]:
    if kind == "I":
        value = int(value)
    elif kind == "F":
        value = float(value)
    node = canonical_node(value)
    if kind is not None and not node.startswith(kind + ":"):
        raise GateRefusal("PROJECTION_NODE_KIND_INVALID", f"expected {kind}, got {node}")
    return {"tag": "PRESENT", "canonical_value": node}


def _absent() -> dict[str, str]:
    return {"tag": "ABSENT"}


def _refusal(code: str) -> dict[str, str]:
    return {"tag": "REFUSAL", "refusal_code": code}


def _projection_value(
    root: Any, *path: str | int, kind: str | None = None
) -> dict[str, Any]:
    """Resolve a version-local selector to PRESENT or ABSENT without indexing errors."""

    value = root
    for token in path:
        if type(token) is str and type(value) is dict and token in value:
            value = value[token]
        elif type(token) is int and type(value) is list and 0 <= token < len(value):
            value = value[token]
        else:
            # Design v1.5 line 510 distinguishes an absent version-local node
            # from a selector execution failure.
            return _absent()
    return _present(value, kind)


def _legacy_event(result: dict[str, Any], index: int) -> dict[str, Any]:
    return result["events"][index]


def _legacy_position(result: dict[str, Any]) -> dict[str, Any]:
    return result["position"]


def _projection_pair(pointer: str, left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    return {"selector": pointer, "legacy": left, "corrected": right, "equal": left == right}


def build_projection_results(
    scenario_id: str,
    input_document: dict[str, Any],
    legacy_result: dict[str, Any],
    corrected: dict[str, Any],
) -> list[dict[str, Any]]:
    event = corrected["EVENT_SURFACE"]
    result = corrected["RESULT_SURFACE"]
    legacy_events = legacy_result["events"]
    position = _legacy_position(legacy_result)
    pairs: list[dict[str, Any]] = []

    def pair(pointer: str, left: dict[str, Any], right: dict[str, Any]) -> None:
        pairs.append(_projection_pair(pointer, left, right))

    if scenario_id.startswith("RULE2-01-"):
        legacy_fill = _legacy_event(legacy_result, 0)
        legacy_qty = _decode_legacy_number(legacy_fill["qty"])
        legacy_price = _decode_legacy_number(legacy_fill["price"])
        multiplier = input_document["legacy_arm"]["config"]["instrument_contract_multiplier"]
        pair("/EVENT_SURFACE/fill_events/0/quantity", _present(legacy_qty, "I"), _present(event["fill_events"][0]["quantity"], "I"))
        pair("/RESULT_SURFACE/final_position/quantity", _present(_decode_legacy_number(position["qty"]), "I"), _present(result["final_position"]["quantity"], "I"))
        pair("/RESULT_SURFACE/order_notional", _present(legacy_qty * legacy_price * multiplier, "I"), _present(result["order_notional"], "I"))
    elif scenario_id.startswith("RULE2-02-"):
        corrected_refusals = result["refusals"]
        if scenario_id.endswith("RED"):
            pair("/RESULT_SURFACE/refusals/0/code", _absent(), _present(corrected_refusals[0]["code"]))
            pair("/EVENT_SURFACE/fill_events", _present([None] * len(legacy_events)), _present(event["fill_events"]))
            pair("/RESULT_SURFACE/final_position", _present({"side": "LONG", "quantity": 1}), _present(result["final_position"]))
            pair("/EVENT_SURFACE/decision_events/3/decision", _absent(), _projection_value(event, "decision_events", 3, "decision"))
        else:
            pair("/RESULT_SURFACE/admitted", _present(position["present"]), _present(result["final_position"] is not None))
            pair("/EVENT_SURFACE/fill_events/0/quantity", _present(_decode_legacy_number(legacy_events[0]["qty"]), "I"), _present(event["fill_events"][0]["quantity"], "I"))
            pair("/RESULT_SURFACE/final_position/quantity", _present(_decode_legacy_number(position["qty"]), "I"), _present(result["final_position"]["quantity"], "I"))
    elif scenario_id.startswith("RULE2-03-"):
        runtime_tick = input_document["legacy_arm"]["config"]["instrument_price_tick"]
        if scenario_id.endswith("RED"):
            pair("/RESULT_SURFACE/refusals/0/code", _absent(), _present(result["refusals"][0]["code"]))
            pair("/EVENT_SURFACE/decision_events/1/decision", _absent(), _projection_value(event, "decision_events", 1, "decision"))
            pair("/EVENT_SURFACE/fill_events", _present([None] * len(legacy_events)), _refusal(result["refusals"][0]["code"]))
            pair("consumed price_tick", _present(runtime_tick, "F"), _refusal(result["refusals"][0]["code"]))
        else:
            pair("/RESULT_SURFACE/refusals", _present([]), _present(result["refusals"]))
            pair("consumed price_tick", _present(runtime_tick, "F"), _projection_value(event, "decision_events", 1, "record_value", kind="F"))
            pair("/RESULT_SURFACE/final_position", _present(None), _present(result["final_position"]))
    elif scenario_id.startswith("RULE2-04-"):
        if scenario_id.endswith("RED"):
            legacy_fill = legacy_events[0]
            pair("/EVENT_SURFACE/fill_events/0/reference_price", _present(_decode_legacy_number(legacy_fill["price"]), "I"), _present(event["fill_events"][0]["reference_price"], "I"))
            pair("/EVENT_SURFACE/fill_events/0/final_fill_price", _present(_decode_legacy_number(legacy_fill["price"]), "I"), _present(event["fill_events"][0]["final_fill_price"], "I"))
            pair("/EVENT_SURFACE/fill_events/0/fill_trigger", _absent(), _present(event["fill_events"][0]["fill_trigger"]))
        else:
            pair("/EVENT_SURFACE/exit_events", _present([]), _present(event["exit_events"]))
            pair("/EVENT_SURFACE/fill_events", _present([]), _present(event["fill_events"]))
            pair("/RESULT_SURFACE/final_position/quantity", _present(_decode_legacy_number(position["qty"]), "I"), _present(result["final_position"]["quantity"], "I"))
    elif scenario_id.startswith("RULE2-05-"):
        legacy_fill = legacy_events[0]
        if scenario_id.endswith("RED"):
            pair("/EVENT_SURFACE/fill_events/0/reference_price", _absent(), _present(event["fill_events"][0]["reference_price"], "I"))
            pair("/EVENT_SURFACE/fill_events/0/slippage_impact", _absent(), _present(event["fill_events"][0]["slippage_impact"], "I"))
            pair("/EVENT_SURFACE/fill_events/0/final_fill_price", _present(_decode_legacy_number(legacy_fill["price"]), "I"), _present(event["fill_events"][0]["final_fill_price"], "I"))
            pair("/EVENT_SURFACE/fill_events/0/slippage_application_count", _absent(), _present(event["fill_events"][0]["slippage_application_count"], "I"))
        else:
            pair("/EVENT_SURFACE/fill_events/0/final_fill_price", _present(_decode_legacy_number(legacy_fill["price"]), "I"), _present(event["fill_events"][0]["final_fill_price"], "I"))
    elif scenario_id.startswith("RULE2-06-"):
        legacy_fill = legacy_events[0]
        corrected_fills = event["fill_events"]
        legacy_exit_id = "STOP" if legacy_fill["exit_id"] == "INITIAL_SL" else legacy_fill["exit_id"]
        corrected_gross = sum(member["gross_realized_pnl"] for member in event["exit_events"])
        if scenario_id == "RULE2-06-GREEN":
            pair("/EVENT_SURFACE/fill_events/0/exit_id", _present(legacy_exit_id), _present(corrected_fills[0]["exit_id"]))
            pair("/EVENT_SURFACE/fill_events/0/quantity", _present(_decode_legacy_number(legacy_fill["qty"]), "I"), _present(corrected_fills[0]["quantity"], "I"))
            pair("/EVENT_SURFACE/fill_events/0/final_fill_price", _present(_decode_legacy_number(legacy_fill["price"]), "I"), _present(corrected_fills[0]["final_fill_price"], "I"))
            pair("lifecycle gross realized PnL", _present(_decode_legacy_number(legacy_fill["realized_pnl"]), "I"), _present(corrected_gross, "I"))
        else:
            pair("/EVENT_SURFACE/fill_events/0/exit_id", _present(legacy_exit_id), _present(corrected_fills[0]["exit_id"]))
            if scenario_id == "RULE2-06-EQUAL-PRICE-RED":
                pair("/EVENT_SURFACE/fill_events/1/exit_id", _absent(), _present(corrected_fills[1]["exit_id"]))
            pair("/EVENT_SURFACE/fill_events", _present([None]), _present([None] * len(corrected_fills)))
            pair("/EVENT_SURFACE/fill_events/0/final_fill_price", _present(_decode_legacy_number(legacy_fill["price"]), "I"), _present(corrected_fills[0]["final_fill_price"], "I"))
            if len(corrected_fills) > 1:
                pair("/EVENT_SURFACE/fill_events/1/final_fill_price", _absent(), _present(corrected_fills[1]["final_fill_price"], "I"))
            pair("/RESULT_SURFACE/collision/ordered_chosen_exit_ids", _absent(), _present(result["collision"]["ordered_chosen_exit_ids"]))
            if scenario_id == "RULE2-06-RED":
                pair("/RESULT_SURFACE/collision/is_pessimistic", _present(True), _present(result["collision"]["is_pessimistic"]))
            pair("lifecycle gross realized PnL", _present(_decode_legacy_number(legacy_fill["realized_pnl"]), "I"), _present(corrected_gross, "I"))
    elif scenario_id.startswith("RULE2-07-"):
        legacy_equity = _decode_legacy_number(legacy_result["account"]["equity"])
        if scenario_id.endswith("RED"):
            pair("/EVENT_SURFACE/fee_events", _absent(), _present(event["fee_events"]))
            pair("/RESULT_SURFACE/trades/0/net_trade_pnl", _absent(), _present(result["trades"][0]["net_trade_pnl"], "F"))
            pair("/RESULT_SURFACE/guards/guard_pnl_basis", _absent(), _present(result["guards"]["guard_pnl_basis"]))
            pair("/RESULT_SURFACE/guards/last_closed_guard_pnl", _absent(), _present(result["guards"]["last_closed_guard_pnl"], "F"))
            pair("/RESULT_SURFACE/guards/consecutive_loss_count", _present(0, "I"), _present(result["guards"]["consecutive_loss_count"], "I"))
            pair("/RESULT_SURFACE/guards/guard_blocked_raw", _present(False), _present(result["guards"]["guard_blocked_raw"]))
            pair("/RESULT_SURFACE/equity_curve/last", _present(legacy_equity, "I"), _present(result["equity_curve"]["last"], "F"))
        else:
            pair("/RESULT_SURFACE/equity_curve/last", _present(legacy_equity, "I"), _present(result["equity_curve"]["last"], "I"))
            pair("/RESULT_SURFACE/guards/consecutive_loss_count", _present(0, "I"), _present(result["guards"]["consecutive_loss_count"], "I"))
            pair("/EVENT_SURFACE/fill_events", _present([]), _present(event["fill_events"]))
            pair("/RESULT_SURFACE/final_position", _present(None), _present(result["final_position"]))
    elif scenario_id.startswith("RULE2-08-"):
        legacy_equity = _decode_legacy_number(legacy_result["account"]["equity"])
        if scenario_id.endswith("RED"):
            pair("/EVENT_SURFACE/funding_events", _absent(), _present(event["funding_events"]))
            pair("/EVENT_SURFACE/cash_events", _absent(), _present(event["cash_events"]))
            pair("/RESULT_SURFACE/cumulative_funding", _absent(), _present(result["cumulative_funding"], "F"))
            pair("/RESULT_SURFACE/equity_curve/last", _present(legacy_equity, "I"), _present(result["equity_curve"]["last"], "F"))
        else:
            pair("/RESULT_SURFACE/equity_curve/last", _present(legacy_equity, "I"), _present(result["equity_curve"]["last"], "I"))
            pair("/EVENT_SURFACE/fill_events", _present([]), _present(event["fill_events"]))
            pair("/RESULT_SURFACE/final_position", _present(None), _present(result["final_position"]))
    else:
        raise GateRefusal("PROJECTION_SCENARIO_UNKNOWN", scenario_id)
    return pairs


def compute_legacy_event_order_map(corpus: Corpus) -> tuple[dict[str, str], str]:
    mapping: dict[str, str] = {}

    def visit(value: Any, identity: str, pointer: str = "") -> None:
        if type(value) is dict:
            for key, member in value.items():
                child = f"{pointer}/{_escape_pointer(key)}"
                if key == "events" and type(member) is list:
                    presence = [type(row) is dict and "sequence" in row for row in member]
                    if any(presence) and not all(presence):
                        raise GateRefusal("LEGACY_EVENT_ORDER_MIXED", identity, pointer=child)
                    if presence and all(presence):
                        for index, row in enumerate(member):
                            if type(row["sequence"]) is not int or row["sequence"] != index:
                                raise GateRefusal("LEGACY_EVENT_SEQUENCE_INVALID", identity, pointer=child)
                        mode = "LEGACY_SEQUENCE_FIELD_V1"
                    else:
                        mode = "LEGACY_EVENT_ORDINAL_V1"
                    mapping[f"{identity}{child}"] = mode
                visit(member, identity, child)
        elif type(value) is list:
            for index, member in enumerate(value):
                visit(member, identity, f"{pointer}/{index}")

    for row in corpus.catalog:
        if row["role"] not in {"RED", "GREEN"}:
            continue
        scenario_id = row["scenario_id"]
        for surface in ("event_surface", "result_surface"):
            document = load_json_exact(corpus.baseline_root / "out" / scenario_id / f"{surface}.json")
            visit(document, f"{scenario_id}/{surface}")
    encoded = (json.dumps(mapping, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    return mapping, hashlib.sha256(encoded).hexdigest()


def run_comparison_pipeline(root: Path, baseline_root: Path) -> dict[str, Any]:
    corpus = validate_catalog(root, baseline_root)
    event_order_map, event_order_digest = compute_legacy_event_order_map(corpus)
    scenarios: list[dict[str, Any]] = []
    for row in corpus.catalog:
        if row["role"] not in {"RED", "GREEN"}:
            continue
        scenario_id = row["scenario_id"]
        input_document = load_json_exact(root / row["input"]["path"])
        corrected = load_json_exact(root / row["expected_artifacts"]["2.0.0"]["path"])
        legacy_result = load_json_exact(baseline_root / "out" / scenario_id / "result_surface.json")
        projections = build_projection_results(scenario_id, input_document, legacy_result, corrected)
        if row["role"] == "RED":
            bad = [projection for projection in projections if projection["equal"]]
            status = "REFUSED_DECLARED_DIVERGENCE" if not bad else "INVALID_RED_NO_DIVERGENCE"
            if bad:
                raise GateRefusal("RULE2_DIVERGENCE_MISSING", scenario_id, pointer=bad[0]["selector"])
            first = projections[0]["selector"]
        else:
            bad = [projection for projection in projections if not projection["equal"]]
            status = "GREEN_SHARED_PROJECTION_EQUAL" if not bad else "INVALID_GREEN_DIVERGENCE"
            if bad:
                raise GateRefusal("RULE2_GREEN_MISMATCH", scenario_id, pointer=bad[0]["selector"])
            first = None
        scenarios.append({
            "scenario_id": scenario_id,
            "role": row["role"],
            "status": status,
            "first_changed_node": first,
            "projections": projections,
        })
    return {
        "catalog_counts": {role: sum(row["role"] == role for row in corpus.catalog) for role in ("RED", "GREEN", "PROBE")},
        "sealed_producer_identities": corpus.identities,
        "legacy_event_order_map": event_order_map,
        "computed_legacy_event_order_map_digest": event_order_digest,
        "acceptance_blockers": [
            {"check_id": "LEGACY_EVENT_ORDER_MAP_PIN_MISSING", "detail": "no seal-pinned map/digest exists in the supplied bundle"},
            *corpus.blockers,
        ],
        "scenarios": scenarios,
    }


def run_selftests(root: Path) -> dict[str, Any]:
    fixtures = root / "tests/corrected_vnext/contracts/selftests"
    checks: list[dict[str, str]] = []

    def record(check_id: str, action: Callable[[], Any]) -> None:
        try:
            action()
        except GateRefusal as exc:
            if exc.check_id != check_id:
                raise GateRefusal("SELFTEST_WRONG_REFUSAL", f"expected {check_id}, got {exc.check_id}") from exc
            checks.append({"check_id": check_id, "status": "DETECTED"})
        else:
            raise GateRefusal("SELFTEST_NOT_DETECTED", check_id)

    equal = compare_documents(load_json_exact(fixtures / "node_equal_left.json"), load_json_exact(fixtures / "node_equal_right.json"))
    if equal is not None:
        raise GateRefusal("SELFTEST_EQUAL_PAIR_FAILED", str(equal))
    checks.append({"check_id": "IDENTICAL_PAIR_ALL_NODES_EQUAL", "status": "PASS"})
    difference = compare_documents(load_json_exact(fixtures / "node_equal_left.json"), load_json_exact(fixtures / "node_one_diff.json"))
    if difference is None or difference[0] != "/a/1":
        raise GateRefusal("SELFTEST_ONE_NODE_PREDETECT_FAILED", str(difference))
    checks.append({"check_id": "ONE_NODE_DIFFERENCE_PREDETECTED", "status": "DETECTED:/a/1"})
    record("JSON_DUPLICATE_KEY", lambda: load_json_exact(fixtures / "duplicate_key.json"))
    record("JSON_NON_FINITE", lambda: load_json_exact(fixtures / "nonfinite.json"))
    record("LEGACY_SCHEMA_PADDED", lambda: validate_legacy_unpadded(load_json_exact(fixtures / "padded_legacy.json")))
    record("CORRECTED_SEQUENCE_INVALID", lambda: validate_corrected_event_surface(load_json_exact(fixtures / "wrong_sequence.json")))
    input_checks = (
        ("input_unknown_top.json", "INPUT_UNKNOWN_TOP_LEVEL_MEMBER"),
        ("input_missing_corrected_only.json", "INPUT_MISSING_TOP_LEVEL_MEMBER"),
        ("input_corrected_in_legacy.json", "INPUT_CORRECTED_ONLY_IN_LEGACY_ARM"),
        ("input_f64_wrong_case.json", "INPUT_F64BITS_INVALID"),
        ("input_f64_short.json", "INPUT_F64BITS_INVALID"),
        ("input_f64_nonquiet.json", "INPUT_F64BITS_INVALID"),
        ("input_f64_infinity.json", "INPUT_F64BITS_INVALID"),
        ("input_f64_outside.json", "INPUT_F64BITS_OUTSIDE_SELECTOR"),
    )
    for name, check_id in input_checks:
        record(check_id, lambda name=name: validate_input_envelope(load_json_exact(fixtures / name)))
    valid_path = fixtures / "input_valid.json"
    valid = load_json_exact(valid_path)
    validate_input_envelope(valid)
    checks.append({"check_id": "SECTION22_VALID_INPUT", "status": "PASS"})
    decoded = decode_stop_price_f64(valid, scenario_id="RULE2-01-GREEN")
    if decoded is None or not math.isnan(decoded):
        raise GateRefusal("SELFTEST_F64BITS_DECODE_FAILED", str(decoded))
    checks.append({"check_id": "SECTION22_F64BITS_DECODE", "status": "PASS"})
    record("INPUT_DIGEST_MISMATCH", lambda: validate_input_envelope(valid, path=valid_path, expected_digest="0" * 64))
    mismatch = load_json_exact(fixtures / "input_record_digest_mismatch.json")
    record(
        "RECORD_DIGEST_MISMATCH",
        lambda: resolve_record_references(root, mismatch["corrected_only"]["records"]),
    )
    return {"mode": "selftest", "claim_label": "NON_ACCEPTING_SELFTEST", "checks": checks}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("selftest", "observe", "red-evidence", "full-gate"),
        required=True,
    )
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--baseline-root", type=Path, default=Path(r"C:\tmp\P012_BASELINE_RUN"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.mode == "selftest":
            receipt = run_selftests(args.root)
        elif args.mode == "observe":
            receipt = materialize_observed_artifacts(args.root, args.baseline_root)
        else:
            pipeline = run_comparison_pipeline(args.root, args.baseline_root)
            if args.mode == "red-evidence":
                receipt = {
                    "mode": "red-evidence",
                    "claim_label": "NON_ACCEPTING_RED_PREFIX_EVIDENCE",
                    "acceptance_reachable": False,
                    **pipeline,
                }
            else:
                review = args.root / "tests/corrected_vnext/contracts/semantic_coverage_review.json"
                blockers = list(pipeline["acceptance_blockers"])
                if not review.is_file():
                    blockers.insert(0, {"check_id": "SEMANTIC_COVERAGE_REVIEW_MISSING", "detail": str(review)})
                if blockers:
                    receipt = {
                        "mode": "full-gate",
                        "claim_label": "BOUNDED_CORRECTION_EVIDENCE_REFUSED",
                        "acceptance_reachable": True,
                        "refusals": blockers,
                        **pipeline,
                    }
                else:
                    receipt = {"mode": "full-gate", "claim_label": ACCEPTING_LABEL, **pipeline}
        encoded = json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        if args.output is not None:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(encoded, encoding="utf-8", newline="\n")
        sys.stdout.write(encoded)
        if args.mode == "full-gate" and receipt["claim_label"] != ACCEPTING_LABEL:
            return 2
        return 0
    except GateRefusal as exc:
        receipt = {
            "mode": args.mode,
            "claim_label": "BOUNDED_CORRECTION_EVIDENCE_REFUSED",
            "refusal": exc.as_dict(),
        }
        sys.stdout.write(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
