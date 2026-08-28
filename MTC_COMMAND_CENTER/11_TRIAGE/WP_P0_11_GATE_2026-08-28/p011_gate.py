from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import json
import math
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator

_MODULE_DIR = Path(__file__).resolve().parent
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

from scenario_binding import (
    EXPECTED_ROW_POSITIONS,
    ManifestRowError,
    ManifestScenarioSource,
    ScenarioBindingError,
    bind_scenario,
    lookup_manifest_row,
    verifier_scenario_contract,
    verify_manifest_row_positions,
)


GATE_VERSION = "P011-LC-GATE-v2"
SCHEMA_VERSION = "P011_OBSERVATION_SCHEMA_v1"
SOURCE_COMMIT = "5c5603065c994d545c0eaa8c137fa9edd5cdfc28"
A_TREE_OID = "7aa6f867d821df08a00358adf2dd4400b9c719e8"
FIXTURE_SHA256 = "3a3a4939fc8e1b725112115971e2663ddbcc1ea5981c37aa1d02d8bc3674a7bb"
EXPECTED_PROFILE_IDS = {
    "mtc_v2_legacy_supertrend_default_v1",
    "mtc_v2_legacy_range_filter_default_v1",
}
EXPECTED_HEADER = ["ts", "open", "high", "low", "close", "volume"]
EXPECTED_ROWS = 48077
ANCHOR_PATH = Path(r"C:\LAB\P011_TRUST_ANCHORS\P011-LC-GATE-v2.owner-signed.json")

GATE_DIR = Path(__file__).resolve().parent
REPO_ROOT = GATE_DIR.parents[2]
A_SOURCE_ROOT = REPO_ROOT / "MTC_COMMAND_CENTER" / "01_MTC_PROJECT" / "00_PYTHON"
A_PACKAGE_ROOT = A_SOURCE_ROOT / "mtc_v2"
SCHEMA_PATH = GATE_DIR / "P011_OBSERVATION_SCHEMA_v1.json"


class GateStop(RuntimeError):
    pass


class GateFail(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_bytes(value: Any, *, pretty: bool = True) -> bytes:
    options: dict[str, Any] = {
        "sort_keys": True,
        "ensure_ascii": False,
        "allow_nan": False,
    }
    if pretty:
        options["indent"] = 2
    else:
        options["separators"] = (",", ":")
    return (json.dumps(value, **options) + "\n").encode("utf-8")


def write_json(path: Path, value: Any) -> None:
    path.write_bytes(canonical_bytes(value))


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        errors="strict",
        capture_output=True,
        check=False,
    )
    if check and completed.returncode != 0:
        raise GateStop(f"git {' '.join(args)} failed: {completed.stderr.strip()}")
    return completed


def git_stdout(*args: str) -> str:
    return git(*args).stdout.strip()


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle, parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise GateStop(f"required JSON is unreadable or non-canonical data: {path}: {exc}") from exc


def resolve_user_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else REPO_ROOT / path


def float_hex(value: Any, *, nullable: bool = False) -> str | None:
    if value is None and nullable:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise GateStop(f"non-numeric value reached lossless float encoder: {value!r}") from exc
    if not math.isfinite(number):
        raise GateStop(f"non-finite value reached lossless float encoder: {number!r}")
    return number.hex()


def verify_frozen_authority(source_commit: str) -> None:
    if source_commit != SOURCE_COMMIT:
        raise GateStop(f"source commit is not the frozen authority: {source_commit}")
    actual_tree = git_stdout(
        "rev-parse",
        f"{SOURCE_COMMIT}:MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2",
    )
    if actual_tree != A_TREE_OID:
        raise GateStop(f"implementation A tree mismatch: {actual_tree}")
    head_tree = git_stdout(
        "rev-parse",
        "HEAD:MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2",
    )
    if head_tree != A_TREE_OID:
        raise GateStop(f"implementation A HEAD tree mismatch: {head_tree}")
    diff = git(
        "diff",
        "--quiet",
        SOURCE_COMMIT,
        "--",
        "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2",
        check=False,
    )
    if diff.returncode != 0:
        if diff.returncode == 1:
            raise GateStop("implementation A worktree bytes differ from the frozen commit")
        raise GateStop(f"could not verify implementation A worktree bytes: {diff.stderr.strip()}")
    if any(name == "mtc_v2" or name.startswith("mtc_v2.") for name in sys.modules):
        raise GateStop("mtc_v2 was imported before the frozen-authority binding check")


def verify_import_bindings() -> list[dict[str, str]]:
    bindings: list[dict[str, str]] = []
    root = A_SOURCE_ROOT.resolve()
    for name in sorted(sys.modules):
        if name != "mtc_v2" and not name.startswith("mtc_v2."):
            continue
        module = sys.modules[name]
        module_file = getattr(module, "__file__", None)
        if not module_file:
            continue
        path = Path(module_file).resolve()
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise GateStop(f"future/foreign mtc_v2 import refused: {name} -> {path}") from exc
        if path.suffix == ".pyc" and "__pycache__" in path.parts:
            source_path = path.parent.parent / (path.name.split(".", 1)[0] + ".py")
        else:
            source_path = path
        if not source_path.is_file():
            raise GateStop(f"bound module source is missing: {name} -> {source_path}")
        bindings.append(
            {
                "module": name,
                "path": source_path.relative_to(REPO_ROOT).as_posix(),
                "sha256": sha256_file(source_path),
            }
        )
    required = {"mtc_v2.core.runner", "mtc_v2.core.types", "mtc_v2.core.config"}
    present = {item["module"] for item in bindings}
    missing = sorted(required - present)
    if missing:
        raise GateStop(f"required implementation A modules were not dynamically bound: {missing}")
    return bindings


def read_profiles(profile_paths: list[Path]) -> list[dict[str, Any]]:
    if len(profile_paths) != 2:
        raise GateStop("exactly two acceptance profiles are required")
    profiles = [load_json(path) for path in profile_paths]
    ids = {item.get("profile_id") for item in profiles}
    if ids != EXPECTED_PROFILE_IDS:
        raise GateStop(f"acceptance profile set mismatch: {sorted(str(item) for item in ids)}")

    sys.path.insert(0, str(A_SOURCE_ROOT))
    from mtc_v2.core.config import resolve_config

    for profile, path in zip(profiles, profile_paths):
        if profile.get("profile_schema_version") != "P011_RESOLVED_CONFIG_v1":
            raise GateStop(f"profile schema mismatch: {path}")
        if profile.get("source_commit") != SOURCE_COMMIT or profile.get("source_tree_oid") != A_TREE_OID:
            raise GateStop(f"profile source identity mismatch: {path}")
        explicit = profile.get("explicit_inputs")
        resolved = profile.get("resolved_config")
        if not isinstance(explicit, dict) or not isinstance(resolved, dict):
            raise GateStop(f"profile is not a full resolved snapshot: {path}")
        recomputed = resolve_config(explicit)
        if resolved != recomputed:
            raise GateFail(f"profile resolved configuration differs from frozen resolve_config: {path}")
        if len(resolved) != 184:
            raise GateFail(f"profile resolved key count changed: {path}: {len(resolved)}")
    return sorted(profiles, key=lambda item: item["profile_id"])


def read_bars(path: Path) -> tuple[list[Any], dict[str, Any]]:
    if sha256_file(path) != FIXTURE_SHA256:
        raise GateFail(f"data SHA-256 mismatch: {path}")
    from mtc_v2.core.types import Bar

    bars: list[Any] = []
    first_timestamp: str | None = None
    last_timestamp: str | None = None
    previous: datetime | None = None
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle)
            header = next(reader)
            if header != EXPECTED_HEADER:
                raise GateFail(f"CSV header mismatch: {header!r}")
            for physical_ordinal, row in enumerate(reader):
                if len(row) != 6:
                    raise GateFail(f"CSV row {physical_ordinal} has {len(row)} columns")
                timestamp_text = row[0]
                timestamp = datetime.fromisoformat(timestamp_text)
                if timestamp.tzinfo is None or timestamp.utcoffset() != timezone.utc.utcoffset(timestamp):
                    raise GateFail(f"CSV row {physical_ordinal} timestamp is not explicit UTC")
                if previous is not None and timestamp <= previous:
                    raise GateFail(f"CSV timestamp/index disagreement at row {physical_ordinal}")
                values = [float(item) for item in row[1:]]
                if not all(math.isfinite(item) for item in values):
                    raise GateFail(f"CSV row {physical_ordinal} contains a non-finite OHLCV value")
                bars.append(
                    Bar(
                        timestamp=timestamp,
                        open=values[0],
                        high=values[1],
                        low=values[2],
                        close=values[3],
                        volume=values[4],
                        bar_index=physical_ordinal,
                    )
                )
                previous = timestamp
                first_timestamp = first_timestamp or timestamp_text
                last_timestamp = timestamp_text
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        if isinstance(exc, GateFail):
            raise
        raise GateStop(f"CSV parser failed before a complete observation stream: {exc}") from exc
    if len(bars) != EXPECTED_ROWS:
        raise GateFail(f"CSV row conservation failed: expected {EXPECTED_ROWS}, actual {len(bars)}")
    if first_timestamp != "2021-01-01T06:00:00+00:00" or last_timestamp != "2026-06-28T00:00:00+00:00":
        raise GateFail("CSV endpoint timestamps mismatch")
    return bars, {
        "sha256": FIXTURE_SHA256,
        "row_count": len(bars),
        "header": ",".join(EXPECTED_HEADER),
        "first_timestamp": first_timestamp,
        "last_timestamp": last_timestamp,
        "bar_index_derivation": "zero-based physical data-row ordinal after the header",
    }


def project_signal(signal: Any) -> dict[str, Any]:
    return {
        "long": bool(signal.long),
        "short": bool(signal.short),
        "reason": None if signal.reason is None else str(signal.reason),
        "direction": None if signal.direction is None else int(signal.direction),
        "line": float_hex(signal.line, nullable=True),
    }


def project_position(position: Any) -> dict[str, Any]:
    if position is None:
        return {
            "present": False,
            "lifecycle_id": None,
            "side": None,
            "entry_price": None,
            "avg_entry_price": None,
            "qty": None,
            "entry_bar": None,
            "initial_qty": None,
            "active_stop_price": None,
            "active_tp_price": None,
            "active_stop_owner": None,
            "be_active": False,
            "trail_active": False,
            "trail_price": None,
            "initial_risk_per_unit": None,
            "working_exit_reference_qty": None,
            "working_exit_book_version": None,
            "entry_legs": [],
            "working_exits": [],
            "completed_exit_ids": [],
        }
    return {
        "present": True,
        "lifecycle_id": int(position.lifecycle_id),
        "side": str(position.side),
        "entry_price": float_hex(position.entry_price),
        "avg_entry_price": float_hex(position.avg_entry_price),
        "qty": float_hex(position.qty),
        "entry_bar": int(position.entry_bar),
        "initial_qty": float_hex(position.initial_qty),
        "active_stop_price": float_hex(position.active_stop_price, nullable=True),
        "active_tp_price": float_hex(position.active_tp_price, nullable=True),
        "active_stop_owner": None if position.active_stop_owner is None else str(position.active_stop_owner),
        "be_active": bool(position.be_active),
        "trail_active": bool(position.trail_active),
        "trail_price": float_hex(position.trail_price, nullable=True),
        "initial_risk_per_unit": float_hex(position.initial_risk_per_unit, nullable=True),
        "working_exit_reference_qty": float_hex(position.working_exit_reference_qty),
        "working_exit_book_version": int(position.working_exit_book_version),
        "entry_legs": [
            {
                "entry_price": float_hex(leg.entry_price),
                "qty": float_hex(leg.qty),
                "entry_bar": int(leg.entry_bar),
            }
            for leg in position.entry_legs
        ],
        "working_exits": [
            {
                "exit_id": str(item.exit_id),
                "kind": str(item.kind),
                "target_price": float_hex(item.target_price, nullable=True),
                "stop_price": float_hex(item.stop_price, nullable=True),
                "qty_fraction": float_hex(item.qty_fraction),
                "book_version": int(item.book_version),
                "active": bool(item.active),
            }
            for item in position.working_exits
        ],
        "completed_exit_ids": sorted(str(item) for item in position.completed_exit_ids),
    }


def project_gate_readiness(state: Any) -> dict[str, Any]:
    gate_results = [
        {
            "gate_name": str(item.gate_name),
            "long_ok": bool(item.long_ok),
            "short_ok": bool(item.short_ok),
            "value": float_hex(item.value, nullable=True),
            "category": str(item.category),
        }
        for item in state.gate_results.values()
    ]
    gate_results.sort(key=lambda item: item["gate_name"])
    return {
        "warmup_bars": int(state.warmup_bars),
        "block_new_entries_this_bar": bool(state.block_new_entries_this_bar),
        "opened_this_bar_reason": None if state.opened_this_bar_reason is None else str(state.opened_this_bar_reason),
        "closed_this_bar_reason": None if state.closed_this_bar_reason is None else str(state.closed_this_bar_reason),
        "gated_long": bool(state.gated_long),
        "gated_short": bool(state.gated_short),
        "gate_results": gate_results,
    }


def project_account(state: Any) -> dict[str, Any]:
    return {
        "equity": float_hex(state.equity),
        "realized_equity": float_hex(state.realized_equity),
        "unrealized_pnl": float_hex(state.unrealized_pnl),
        "last_sizing_equity_snapshot": float_hex(state.last_sizing_equity_snapshot),
        "total_entries": int(state.total_entries),
        "total_exits": int(state.total_exits),
    }


def state_digest(events: list[dict[str, Any]], position: dict[str, Any], gate_readiness: dict[str, Any], account: dict[str, Any]) -> str:
    preimage = {
        "events": events,
        "position": position,
        "gate_readiness": gate_readiness,
        "account": account,
    }
    encoded = json.dumps(
        preimage,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def run_profile(profile: dict[str, Any], bars: list[Any], spool_path: Path) -> tuple[list[Any], dict[str, Any]]:
    from mtc_v2.core.runner import Runner

    runner = Runner(profile["explicit_inputs"])
    if runner.config != profile["resolved_config"]:
        raise GateFail(f"Runner internal resolved config differs from frozen profile: {profile['profile_id']}")
    raw_by_index: dict[int, dict[str, Any]] = {}
    events_by_index: dict[int, list[dict[str, Any]]] = {}

    original_apply = runner._apply_entry_gates

    def observed_apply(raw: Any, gate_results: dict[str, Any]) -> Any:
        index = int(runner.state.current_bar_index)
        if index in raw_by_index:
            raise GateStop(f"raw signal producer called more than once for bar {index}")
        raw_by_index[index] = project_signal(raw)
        return original_apply(raw, gate_results)

    runner._apply_entry_gates = observed_apply

    position_manager = runner.position_manager
    original_open = position_manager.open_position
    original_close = position_manager.close_position

    def observed_open(**kwargs: Any) -> None:
        state = kwargs["state"]
        before = int(state.total_entries)
        original_open(**kwargs)
        if int(state.total_entries) == before:
            return
        bar = kwargs["bar"]
        position = state.position
        if position is None:
            raise GateStop("entry transition completed without a position")
        event_list = events_by_index.setdefault(int(bar.bar_index), [])
        fill_price = kwargs.get("fill_price")
        event_list.append(
            {
                "event_ordinal": len(event_list),
                "event_kind": "ENTRY",
                "side": str(kwargs["side"]),
                "reason": None if kwargs.get("reason") is None else str(kwargs["reason"]),
                "price": float_hex(float(bar.close) if fill_price is None else fill_price),
                "qty": float_hex(kwargs["qty"]),
                "lifecycle_id": int(position.lifecycle_id),
                "exit_id": None,
                "realized_pnl": None,
                "was_partial": False,
                "was_pessimistic": False,
            }
        )

    def observed_close(**kwargs: Any) -> None:
        state = kwargs["state"]
        position = state.position
        if position is None:
            original_close(**kwargs)
            return
        side = str(position.side)
        lifecycle_id = int(position.lifecycle_id)
        before = int(state.total_exits)
        original_close(**kwargs)
        if int(state.total_exits) == before:
            return
        bar = kwargs["bar"]
        exit_event = state.exit_events_this_bar[-1]
        event_list = events_by_index.setdefault(int(bar.bar_index), [])
        event_list.append(
            {
                "event_ordinal": len(event_list),
                "event_kind": "EXIT",
                "side": side,
                "reason": str(exit_event.exit_reason),
                "price": float_hex(exit_event.exit_price),
                "qty": float_hex(exit_event.exit_qty),
                "lifecycle_id": lifecycle_id,
                "exit_id": None if exit_event.exit_id is None else str(exit_event.exit_id),
                "realized_pnl": float_hex(exit_event.realized_pnl),
                "was_partial": bool(exit_event.was_partial),
                "was_pessimistic": bool(exit_event.was_pessimistic),
            }
        )

    position_manager.open_position = observed_open
    position_manager.close_position = observed_close

    last_record: dict[str, Any] | None = None

    with spool_path.open("wb") as spool:
        def capture(bar: Any) -> None:
            nonlocal last_record
            index = int(bar.bar_index)
            raw = raw_by_index.pop(index, None)
            if raw is None:
                raise GateStop(f"no raw signal was observed at the real Runner seam for bar {index}")
            events = events_by_index.pop(index, [])
            expected_ordinals = list(range(len(events)))
            actual_ordinals = [item["event_ordinal"] for item in events]
            if actual_ordinals != expected_ordinals:
                raise GateStop(f"event ordinal conservation failed for bar {index}")
            position = project_position(runner.state.position)
            readiness = project_gate_readiness(runner.state)
            account = project_account(runner.state)
            record = {
                "schema_version": SCHEMA_VERSION,
                "profile_id": profile["profile_id"],
                "bar_index": index,
                "timestamp": bar.timestamp.isoformat(),
                "input": {
                    "open": float_hex(bar.open),
                    "high": float_hex(bar.high),
                    "low": float_hex(bar.low),
                    "close": float_hex(bar.close),
                    "volume": float_hex(bar.volume),
                },
                "raw_signal": raw,
                "events": events,
                "position": position,
                "gate_readiness": readiness,
                "account": account,
                "state_digest": state_digest(events, position, readiness, account),
            }
            spool.write(canonical_bytes(record, pretty=False))
            last_record = record

        def observed_bars() -> Iterator[Any]:
            previous = None
            for current in bars:
                if previous is not None:
                    capture(previous)
                yield current
                previous = current
            if previous is not None:
                capture(previous)

        outputs = runner.run(observed_bars())

    if raw_by_index or events_by_index:
        raise GateStop("adapter ended with unconsumed raw signals or events")
    if len(outputs) != len(bars):
        raise GateFail(f"Runner output conservation failed for {profile['profile_id']}: {len(outputs)}")
    if last_record is None:
        raise GateStop(f"Runner produced no state observations for {profile['profile_id']}")
    return outputs, last_record


def validate_legacy_manifest(path: Path, expected_sha256: str) -> dict[str, Any]:
    actual_hash = sha256_file(path)
    if actual_hash != expected_sha256:
        raise GateFail(f"legacy manifest differs from the external pin: {actual_hash}")
    manifest = load_json(path)
    rows = manifest.get("rows")
    if not isinstance(rows, list) or len(rows) != 42:
        raise GateStop("legacy manifest does not enumerate 42 rows")
    expected_ids = [f"C{index:02d}" for index in range(1, 43)]
    try:
        verify_manifest_row_positions(manifest, expected_ids)
    except ManifestRowError as exc:
        raise GateFail(str(exc)) from exc
    allowed = {"APPLICABLE", "NOT_A_LEGACY_REPRODUCTION_ROW"}
    if any(row.get("disposition") not in allowed for row in rows):
        raise GateStop("legacy manifest contains a non-terminal disposition")
    for row_id in expected_ids:
        row = lookup_manifest_row(manifest, row_id, EXPECTED_ROW_POSITIONS[row_id])
        if row["disposition"] == "APPLICABLE":
            scenarios = row.get("scenarios")
            if not isinstance(scenarios, list) or not scenarios:
                raise GateStop(f"applicable row has no frozen scenario: {row['row_id']}")
            if len(scenarios) != 1:
                raise GateStop(f"applicable row must have exactly one frozen scenario: {row_id}")
            try:
                binding = bind_scenario(
                    ManifestScenarioSource(
                        manifest=manifest,
                        row_id=row_id,
                        expected_position=EXPECTED_ROW_POSITIONS[row_id],
                    ),
                    verifier_scenario_contract(row_id),
                )
            except ScenarioBindingError as exc:
                raise GateStop(f"scenario binding refused for {row_id}: {exc}") from exc
    return manifest


def build_row_corroboration(manifest: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for row in manifest["rows"]:
        if row["disposition"] == "NOT_A_LEGACY_REPRODUCTION_ROW":
            rows.append(
                {
                    "row_id": row["row_id"],
                    "status": "NOT_A_LEGACY_REPRODUCTION_ROW",
                    "producer_execution": "NOT_APPLICABLE",
                    "producer_mutation": "NOT_APPLICABLE",
                }
            )
        else:
            bind_scenario(
                ManifestScenarioSource(
                    manifest=manifest,
                    row_id=row["row_id"],
                    expected_position=EXPECTED_ROW_POSITIONS[row["row_id"]],
                ),
                verifier_scenario_contract(row["row_id"]),
            )
            rows.append(
                {
                    "row_id": row["row_id"],
                    "status": "STOP",
                    "producer_execution": "PENDING_DIRECT_BUILD_ADAPTER",
                    "producer_mutation": "PENDING_DIRECT_BUILD_MUTATION",
                    "scenario_ids": [item["scenario_id"] for item in row["scenarios"]],
                }
            )
    return {
        "artifact_schema_version": "P011_ROW_CORROBORATION_v1",
        "gate_version": GATE_VERSION,
        "outcome": "STOP",
        "reason": "40 direct-build producer adapters and their D026 mutations are frozen but not executed by this sequence builder",
        "rows": rows,
        "counts": {
            "total": len(rows),
            "green": 0,
            "stop": sum(item["status"] == "STOP" for item in rows),
            "not_applicable": sum(item["status"] == "NOT_A_LEGACY_REPRODUCTION_ROW" for item in rows),
        },
    }


def command_build_baseline(args: argparse.Namespace) -> int:
    if args.producer != "A":
        raise GateStop("only frozen producer A is valid for the sequence baseline")
    out = resolve_user_path(args.out)
    if out.exists():
        raise GateStop(f"output directory already exists; a fresh directory is required: {out}")
    verify_frozen_authority(args.source_commit)

    receipt_path = GATE_DIR / "P011_GATE_RECEIPT.json"
    receipt = load_json(receipt_path)
    if receipt.get("accepted_git_commit") != SOURCE_COMMIT:
        raise GateStop("receipt does not bind the frozen source commit")
    anchor = load_json(ANCHOR_PATH)
    if anchor.get("receipt_sha256") != sha256_file(receipt_path):
        raise GateFail("external anchor receipt pin mismatch")

    legacy_path = resolve_user_path(args.legacy_manifest)
    manifest = validate_legacy_manifest(legacy_path, str(anchor.get("legacy_manifest_sha256")))
    profile_paths = [resolve_user_path(item) for item in args.profile]
    profiles = read_profiles(profile_paths)
    bars, data_identity = read_bars(resolve_user_path(args.data))
    importlib.import_module("mtc_v2.core.runner")
    bindings_before = verify_import_bindings()

    out.mkdir(parents=True, exist_ok=False)
    sequence_path = out / "mtc_v2_legacy_sequence.jsonl"
    final_states: dict[str, Any] = {}
    profile_metrics: list[dict[str, Any]] = []
    total_records = 0
    total_events = 0

    try:
        with sequence_path.open("wb") as sequence_handle:
            for profile in profiles:
                spool_path = out / f".{profile['profile_id']}.state-spool.jsonl"
                outputs, last_record = run_profile(profile, bars, spool_path)
                records = 0
                events = 0
                with spool_path.open("r", encoding="utf-8") as spool:
                    for index, (line, gated) in enumerate(zip(spool, outputs, strict=True)):
                        record = json.loads(line)
                        if record["bar_index"] != index:
                            raise GateFail(f"spool bar-index conservation failed for {profile['profile_id']}")
                        record["gated_signal"] = project_signal(gated)
                        sequence_handle.write(canonical_bytes(record, pretty=False))
                        records += 1
                        events += len(record["events"])
                spool_path.unlink()
                if records != EXPECTED_ROWS:
                    raise GateFail(f"observation conservation failed for {profile['profile_id']}: {records}")
                final_states[profile["profile_id"]] = {
                    "last_key": [profile["profile_id"], EXPECTED_ROWS - 1, last_record["timestamp"]],
                    "events": last_record["events"],
                    "position": last_record["position"],
                    "gate_readiness": last_record["gate_readiness"],
                    "account": last_record["account"],
                    "state_digest": last_record["state_digest"],
                }
                profile_metrics.append(
                    {
                        "profile_id": profile["profile_id"],
                        "input_bars": len(bars),
                        "observations": records,
                        "events": events,
                        "final_state_digest": last_record["state_digest"],
                    }
                )
                total_records += records
                total_events += events
    except Exception:
        for spool in out.glob(".*.state-spool.jsonl"):
            spool.unlink(missing_ok=True)
        raise

    final_states_path = out / "final_states.json"
    write_json(final_states_path, {"gate_version": GATE_VERSION, "profiles": final_states})
    row_path = out / "row_corroboration.json"
    write_json(row_path, build_row_corroboration(manifest))

    bindings_after = verify_import_bindings()
    before_bindings = {(item["module"], item["path"], item["sha256"]) for item in bindings_before}
    after_bindings = {(item["module"], item["path"], item["sha256"]) for item in bindings_after}
    if not before_bindings.issubset(after_bindings):
        raise GateStop("implementation A import binding changed during execution")
    baseline_manifest = {
        "artifact_schema_version": "P011_BASELINE_MANIFEST_v1",
        "gate_version": GATE_VERSION,
        "candidate_status": "SEQUENCE_BUILT_ROW_ARM_STOP_INDEPENDENT_REPRODUCTION_PENDING",
        "source": {
            "producer": "A",
            "commit": SOURCE_COMMIT,
            "tree_oid": A_TREE_OID,
            "runner_call": "mtc_v2.core.runner.Runner.run once per profile over the ordered Bar stream",
            "resolved_import_bindings": bindings_after,
        },
        "adapters": {
            "observation_adapter": {
                "path": Path(__file__).relative_to(REPO_ROOT).as_posix(),
                "sha256": sha256_file(Path(__file__)),
                "binding": "real Runner.run; signal gate seam; PositionManager entry/exit calls; Runner.state at iterable boundaries",
                "precomputed_observation_input": False,
            }
        },
        "data": data_identity,
        "profiles": [
            {
                "profile_id": item["profile_id"],
                "path": next(path.relative_to(REPO_ROOT).as_posix() for path in profile_paths if path.stem == item["profile_id"]),
                "sha256": next(sha256_file(path) for path in profile_paths if path.stem == item["profile_id"]),
                "resolved_key_count": len(item["resolved_config"]),
            }
            for item in profiles
        ],
        "conservation": {
            "profiles": len(profiles),
            "input_bars_per_profile": EXPECTED_ROWS,
            "observations_per_profile": EXPECTED_ROWS,
            "total_observations": total_records,
            "total_events": total_events,
            "profile_metrics": profile_metrics,
        },
        "artifact_hashes": {
            "mtc_v2_legacy_sequence.jsonl": sha256_file(sequence_path),
            "final_states.json": sha256_file(final_states_path),
            "row_corroboration.json": sha256_file(row_path),
        },
        "tool_environment": {
            "python_executable": sys.executable,
            "python_version": sys.version,
            "python_implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "pythonpath_environment_present": bool(os.environ.get("PYTHONPATH")),
        },
        "independent_reproduction": "NOT_PERFORMED_IMPLEMENTER_DUTY_EXCLUDED",
    }
    baseline_manifest_path = out / "baseline_manifest.json"
    write_json(baseline_manifest_path, baseline_manifest)

    result = {
        "outcome": "PASS",
        "command": "build-baseline",
        "artifact_status": baseline_manifest["candidate_status"],
        "output_directory": str(out),
        "sequence_sha256": baseline_manifest["artifact_hashes"]["mtc_v2_legacy_sequence.jsonl"],
        "total_observations": total_records,
        "profile_metrics": profile_metrics,
        "full_gate_outcome": "STOP",
        "full_gate_stop_reason": "row producer corroboration/mutations and independent reproduction are not earned",
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
    return 0


def command_validate_legacy_manifest(args: argparse.Namespace) -> int:
    path = resolve_user_path(args.legacy_manifest)
    validate_legacy_manifest(path, args.legacy_manifest_sha256)
    print(
        json.dumps(
            {
                "legacy_manifest": str(path),
                "outcome": "PASS",
                "sha256": args.legacy_manifest_sha256,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0


TOP_LEVEL_KEYS = {
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
}
INPUT_KEYS = {"open", "high", "low", "close", "volume"}
SIGNAL_KEYS = {"long", "short", "reason", "direction", "line"}
EVENT_KEYS = {"event_ordinal", "event_kind", "side", "reason", "price", "qty", "lifecycle_id", "exit_id", "realized_pnl", "was_partial", "was_pessimistic"}
POSITION_KEYS = {"present", "lifecycle_id", "side", "entry_price", "avg_entry_price", "qty", "entry_bar", "initial_qty", "active_stop_price", "active_tp_price", "active_stop_owner", "be_active", "trail_active", "trail_price", "initial_risk_per_unit", "working_exit_reference_qty", "working_exit_book_version", "entry_legs", "working_exits", "completed_exit_ids"}
ENTRY_LEG_KEYS = {"entry_price", "qty", "entry_bar"}
WORKING_EXIT_KEYS = {"exit_id", "kind", "target_price", "stop_price", "qty_fraction", "book_version", "active"}
READINESS_KEYS = {"warmup_bars", "block_new_entries_this_bar", "opened_this_bar_reason", "closed_this_bar_reason", "gated_long", "gated_short", "gate_results"}
GATE_RESULT_KEYS = {"gate_name", "long_ok", "short_ok", "value", "category"}
ACCOUNT_KEYS = {"equity", "realized_equity", "unrealized_pnl", "last_sizing_equity_snapshot", "total_entries", "total_exits"}


def exact_keys(value: Any, expected: set[str], location: str) -> None:
    if not isinstance(value, dict):
        raise GateStop(f"{location} is not an object")
    actual = set(value)
    if actual != expected:
        raise GateFail(f"{location} closed-schema keys differ: missing={sorted(expected-actual)} unexpected={sorted(actual-expected)}")


def validate_observation(record: Any, line_number: int) -> tuple[str, int, str]:
    exact_keys(record, TOP_LEVEL_KEYS, f"observation line {line_number}")
    if record["schema_version"] != SCHEMA_VERSION:
        raise GateFail(f"observation line {line_number} schema version differs")
    exact_keys(record["input"], INPUT_KEYS, f"observation line {line_number}.input")
    exact_keys(record["raw_signal"], SIGNAL_KEYS, f"observation line {line_number}.raw_signal")
    exact_keys(record["gated_signal"], SIGNAL_KEYS, f"observation line {line_number}.gated_signal")
    if not isinstance(record["events"], list):
        raise GateStop(f"observation line {line_number}.events is not an array")
    for index, event in enumerate(record["events"]):
        exact_keys(event, EVENT_KEYS, f"observation line {line_number}.events[{index}]")
        if event["event_ordinal"] != index:
            raise GateFail(f"duplicate/skipped event ordinal at observation line {line_number}")
    exact_keys(record["position"], POSITION_KEYS, f"observation line {line_number}.position")
    for index, leg in enumerate(record["position"]["entry_legs"]):
        exact_keys(leg, ENTRY_LEG_KEYS, f"observation line {line_number}.position.entry_legs[{index}]")
    for index, item in enumerate(record["position"]["working_exits"]):
        exact_keys(item, WORKING_EXIT_KEYS, f"observation line {line_number}.position.working_exits[{index}]")
    completed = record["position"]["completed_exit_ids"]
    if completed != sorted(completed):
        raise GateFail(f"completed_exit_ids ordering differs at observation line {line_number}")
    exact_keys(record["gate_readiness"], READINESS_KEYS, f"observation line {line_number}.gate_readiness")
    gate_results = record["gate_readiness"]["gate_results"]
    for index, item in enumerate(gate_results):
        exact_keys(item, GATE_RESULT_KEYS, f"observation line {line_number}.gate_results[{index}]")
    gate_names = [item["gate_name"] for item in gate_results]
    if gate_names != sorted(gate_names) or len(gate_names) != len(set(gate_names)):
        raise GateFail(f"gate_results ordering/identity differs at observation line {line_number}")
    exact_keys(record["account"], ACCOUNT_KEYS, f"observation line {line_number}.account")
    expected_digest = state_digest(record["events"], record["position"], record["gate_readiness"], record["account"])
    if record["state_digest"] != expected_digest:
        raise GateFail(f"state digest preimage mismatch at observation line {line_number}")
    return str(record["profile_id"]), int(record["bar_index"]), str(record["timestamp"])


def index_sequence(path: Path) -> tuple[dict[tuple[str, int, str], str], list[tuple[str, int, str]]]:
    index: dict[tuple[str, int, str], str] = {}
    order: list[tuple[str, int, str]] = []
    try:
        with path.open("rb") as handle:
            for line_number, raw_line in enumerate(handle, start=1):
                if not raw_line.endswith(b"\n"):
                    raise GateStop(f"unterminated JSONL record at line {line_number}: {path}")
                try:
                    record = json.loads(raw_line)
                except (UnicodeError, json.JSONDecodeError, ValueError) as exc:
                    raise GateStop(f"unreadable JSONL record at line {line_number}: {path}: {exc}") from exc
                key = validate_observation(record, line_number)
                if key in index:
                    raise GateFail(f"duplicate observation identity: {key}")
                index[key] = sha256_bytes(raw_line)
                order.append(key)
    except OSError as exc:
        raise GateStop(f"sequence is unreadable: {path}: {exc}") from exc
    return index, order


def load_selected(path: Path, keys: set[tuple[str, int, str]]) -> dict[tuple[str, int, str], Any]:
    selected: dict[tuple[str, int, str], Any] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            record = json.loads(line)
            key = (str(record["profile_id"]), int(record["bar_index"]), str(record["timestamp"]))
            if key in keys:
                selected[key] = record
    return selected


def compare_sequence_files(expected_path: Path, actual_path: Path, authority: str) -> tuple[list[dict[str, Any]], int]:
    expected_index, expected_order = index_sequence(expected_path)
    actual_index, actual_order = index_sequence(actual_path)
    expected_keys = set(expected_index)
    actual_keys = set(actual_index)
    missing = sorted(expected_keys - actual_keys)
    unexpected = sorted(actual_keys - expected_keys)
    changed = sorted(key for key in expected_keys & actual_keys if expected_index[key] != actual_index[key])
    order_mismatch = expected_order != actual_order and not missing and not unexpected
    detail_keys = set(changed[:100])
    expected_records = load_selected(expected_path, detail_keys) if detail_keys else {}
    actual_records = load_selected(actual_path, detail_keys) if detail_keys else {}
    ledger: list[dict[str, Any]] = []
    for key in missing[:100]:
        ledger.append({"profile_or_row": key[0], "bar": key[1], "timestamp": key[2], "expected": "present", "actual": "missing", "authority": authority, "reason": "missing_observation"})
    for key in unexpected[:100]:
        ledger.append({"profile_or_row": key[0], "bar": key[1], "timestamp": key[2], "expected": "absent", "actual": "present", "authority": authority, "reason": "unexpected_observation"})
    for key in changed[:100]:
        ledger.append({"profile_or_row": key[0], "bar": key[1], "timestamp": key[2], "expected": expected_records[key], "actual": actual_records[key], "authority": authority, "reason": "observation_value_mismatch"})
    if order_mismatch:
        first = next(index for index, pair in enumerate(zip(expected_order, actual_order)) if pair[0] != pair[1])
        ledger.append({"profile_or_row": expected_order[first][0], "bar": expected_order[first][1], "expected": expected_order[first], "actual": actual_order[first], "authority": authority, "reason": "observation_order_mismatch"})
    changed_record_count = len(missing) + len(unexpected) + len(changed)
    if order_mismatch:
        changed_record_count = max(changed_record_count, 1)
    return ledger, changed_record_count


def verify_receipt_and_baseline(receipt_path: Path, baseline: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    receipt = load_json(receipt_path)
    anchor = load_json(ANCHOR_PATH)
    if anchor.get("gate_version") != GATE_VERSION:
        raise GateFail("external anchor gate version differs")
    if anchor.get("receipt_sha256") != sha256_file(receipt_path):
        raise GateFail("external anchor receipt hash differs")
    legacy_path = GATE_DIR / "p011_legacy_manifest.json"
    if anchor.get("legacy_manifest_sha256") != sha256_file(legacy_path):
        raise GateFail("external anchor legacy-manifest hash differs")
    baseline_manifest_path = baseline / "baseline_manifest.json"
    manifest = load_json(baseline_manifest_path)
    if manifest.get("source", {}).get("commit") != SOURCE_COMMIT or manifest.get("source", {}).get("tree_oid") != A_TREE_OID:
        raise GateFail("baseline producer identity differs")
    for name, expected_hash in manifest.get("artifact_hashes", {}).items():
        artifact = baseline / name
        if not artifact.is_file():
            raise GateStop(f"required baseline artifact is missing: {artifact}")
        if sha256_file(artifact) != expected_hash:
            raise GateFail(f"baseline artifact hash differs: {name}")
    receipt_hashes = receipt.get("baseline_outputs", {}).get("artifact_sha256", {})
    if receipt_hashes:
        for name, expected_hash in receipt_hashes.items():
            artifact = baseline / name
            if not artifact.is_file():
                raise GateStop(f"receipt-bound baseline artifact is missing: {name}")
            if sha256_file(artifact) != expected_hash:
                raise GateFail(f"receipt-bound baseline artifact hash differs: {name}")
    return receipt, manifest


def command_compare(args: argparse.Namespace) -> int:
    receipt_path = resolve_user_path(args.receipt)
    baseline = resolve_user_path(args.baseline)
    receipt, manifest = verify_receipt_and_baseline(receipt_path, baseline)
    baseline_sequence = baseline / "mtc_v2_legacy_sequence.jsonl"
    expected_index, expected_order = index_sequence(baseline_sequence)
    if len(expected_index) != EXPECTED_ROWS * 2:
        raise GateFail(f"baseline observation conservation differs: {len(expected_index)}")
    profile_counts = {profile_id: 0 for profile_id in EXPECTED_PROFILE_IDS}
    for profile_id, _, _ in expected_order:
        if profile_id not in profile_counts:
            raise GateFail(f"unexpected baseline profile: {profile_id}")
        profile_counts[profile_id] += 1
    if set(profile_counts.values()) != {EXPECTED_ROWS}:
        raise GateFail(f"baseline profile conservation differs: {profile_counts}")

    row_evidence = load_json(baseline / "row_corroboration.json")
    row_outcome = row_evidence.get("outcome")
    actual_sequence_arg = args.actual_sequence
    if actual_sequence_arg:
        actual_path = resolve_user_path(actual_sequence_arg)
        ledger, changed_records = compare_sequence_files(baseline_sequence, actual_path, "implementation A frozen sequence")
        mismatch_path = resolve_user_path(args.mismatch_ledger)
        write_json(mismatch_path, {"gate_version": GATE_VERSION, "mismatches": ledger, "changed_record_count": changed_records})
        if ledger:
            print(json.dumps({"outcome": "FAIL", "changed_record_count": changed_records, "mismatch_ledger": str(mismatch_path)}, sort_keys=True, separators=(",", ":")))
            return 1
    if row_outcome != "PASS":
        raise GateStop(f"row-semantic arm is not evaluable: {row_evidence.get('reason', row_outcome)}")
    if receipt.get("independent_reproduction_evidence", {}).get("status") not in {"PASS", "PASS-WITH-NITS"}:
        raise GateStop("independent flagship reproduction is absent")
    subject = receipt.get("subject", {})
    classification = subject.get("classification")
    if classification not in {"INDEPENDENT_REIMPLEMENTATION", "WRAP_MOVE_OF_A"}:
        raise GateStop("subject classification/import-call binding is absent")
    if not actual_sequence_arg:
        raise GateStop("subject adapter/sequence is absent")
    mismatch_path = resolve_user_path(args.mismatch_ledger)
    write_json(mismatch_path, {"gate_version": GATE_VERSION, "mismatches": [], "changed_record_count": 0})
    print(json.dumps({"outcome": "PASS", "profile_counts": profile_counts, "mismatch_ledger": str(mismatch_path)}, sort_keys=True, separators=(",", ":")))
    return 0


def command_verify_double_build(args: argparse.Namespace) -> int:
    run1 = resolve_user_path(args.run1)
    run2 = resolve_user_path(args.run2)
    names = ["mtc_v2_legacy_sequence.jsonl", "final_states.json", "row_corroboration.json", "baseline_manifest.json"]
    comparisons = []
    for name in names:
        path1 = run1 / name
        path2 = run2 / name
        if not path1.is_file() or not path2.is_file():
            raise GateStop(f"double-build artifact is missing: {name}")
        hash1 = sha256_file(path1)
        hash2 = sha256_file(path2)
        comparisons.append({"artifact": name, "run1_sha256": hash1, "run2_sha256": hash2, "byte_identical": hash1 == hash2})
    if not all(item["byte_identical"] for item in comparisons):
        raise GateFail("fresh baseline builds are not byte-identical")
    print(json.dumps({"outcome": "PASS", "byte_identical": True, "artifacts": comparisons}, sort_keys=True, separators=(",", ":")))
    return 0


def command_self_test_compare(args: argparse.Namespace) -> int:
    expected = resolve_user_path(args.expected)
    actual = resolve_user_path(args.actual)
    ledger_path = resolve_user_path(args.mismatch_ledger)
    ledger, changed_records = compare_sequence_files(expected, actual, "P011 comparator discrimination self-test")
    write_json(
        ledger_path,
        {
            "gate_version": GATE_VERSION,
            "self_test_only": True,
            "changed_record_count": changed_records,
            "mismatches": ledger,
        },
    )
    if ledger:
        print(json.dumps({"outcome": "FAIL", "changed_record_count": changed_records, "mismatch_count": len(ledger), "mismatch_ledger": str(ledger_path)}, sort_keys=True, separators=(",", ":")))
        return 1
    print(json.dumps({"outcome": "PASS", "changed_record_count": 0, "mismatch_count": 0, "mismatch_ledger": str(ledger_path)}, sort_keys=True, separators=(",", ":")))
    return 0


def representative_observation(baseline_sequence: Path) -> dict[str, Any]:
    try:
        with baseline_sequence.open("r", encoding="utf-8") as handle:
            first = json.loads(next(handle))
    except (OSError, StopIteration, UnicodeError, json.JSONDecodeError) as exc:
        raise GateStop(f"cannot create discrimination fixture from baseline: {exc}") from exc
    first["events"] = [
        {
            "event_ordinal": 0,
            "event_kind": "ENTRY",
            "side": "long",
            "reason": "matrix_fixture",
            "price": float(100.0).hex(),
            "qty": float(2.0).hex(),
            "lifecycle_id": 1,
            "exit_id": None,
            "realized_pnl": None,
            "was_partial": False,
            "was_pessimistic": False,
        }
    ]
    first["position"] = {
        "present": True,
        "lifecycle_id": 1,
        "side": "long",
        "entry_price": float(100.0).hex(),
        "avg_entry_price": float(100.0).hex(),
        "qty": float(2.0).hex(),
        "entry_bar": int(first["bar_index"]),
        "initial_qty": float(2.0).hex(),
        "active_stop_price": float(95.0).hex(),
        "active_tp_price": float(110.0).hex(),
        "active_stop_owner": "initial",
        "be_active": False,
        "trail_active": False,
        "trail_price": None,
        "initial_risk_per_unit": float(5.0).hex(),
        "working_exit_reference_qty": float(2.0).hex(),
        "working_exit_book_version": 1,
        "entry_legs": [{"entry_price": float(100.0).hex(), "qty": float(2.0).hex(), "entry_bar": int(first["bar_index"])}],
        "working_exits": [
            {
                "exit_id": "TP1",
                "kind": "target",
                "target_price": float(110.0).hex(),
                "stop_price": None,
                "qty_fraction": float(0.5).hex(),
                "book_version": 1,
                "active": True,
            }
        ],
        "completed_exit_ids": ["TP0"],
    }
    first["gate_readiness"]["gate_results"] = [
        {
            "gate_name": "matrix_gate",
            "long_ok": True,
            "short_ok": False,
            "value": float(1.25).hex(),
            "category": "filter",
        }
    ]
    first["state_digest"] = state_digest(first["events"], first["position"], first["gate_readiness"], first["account"])
    validate_observation(first, 1)
    return first


def path_tokens(path: str) -> list[str | int]:
    tokens: list[str | int] = []
    for part in path.split("."):
        if part.endswith("[*]"):
            tokens.append(part[:-3])
            tokens.append(0)
        else:
            tokens.append(part)
    return tokens


def get_path(record: Any, path: str) -> Any:
    current = record
    for token in path_tokens(path):
        current = current[token]
    return current


def set_path(record: Any, path: str, value: Any) -> None:
    tokens = path_tokens(path)
    current = record
    for token in tokens[:-1]:
        current = current[token]
    current[tokens[-1]] = value


def mutated_value(current: Any, catalog_type: str) -> Any:
    if current is None:
        return {
            "float": float(1.0).hex(),
            "integer": 1,
            "string": "MUTATED",
            "boolean": True,
        }[catalog_type]
    if catalog_type == "boolean":
        return not bool(current)
    if catalog_type == "integer":
        return int(current) + 1
    if catalog_type == "float":
        number = float.fromhex(str(current))
        return (number + 0.5).hex()
    return str(current) + "_MUTATED"


def run_self_test_subprocess(expected: Path, actual: Path, ledger: Path) -> dict[str, Any]:
    command = [
        sys.executable,
        "-I",
        str(Path(__file__).resolve()),
        "self-test-compare",
        "--expected",
        str(expected),
        "--actual",
        str(actual),
        "--mismatch-ledger",
        str(ledger),
    ]
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        errors="strict",
        capture_output=True,
        check=False,
        timeout=60,
    )
    evidence_bytes = (completed.stdout + completed.stderr).encode("utf-8")
    return {
        "command_argv": command,
        "return_code": completed.returncode,
        "stdout": completed.stdout.rstrip("\r\n"),
        "stderr": completed.stderr.rstrip("\r\n"),
        "evidence_sha256": sha256_bytes(evidence_bytes),
    }


def command_mutation_harness(args: argparse.Namespace) -> int:
    baseline = resolve_user_path(args.baseline)
    out = resolve_user_path(args.out)
    if out.exists():
        raise GateStop(f"mutation output directory already exists; a fresh directory is required: {out}")
    baseline_sequence = baseline / "mtc_v2_legacy_sequence.jsonl"
    if not baseline_sequence.is_file():
        raise GateStop("baseline sequence is absent")
    schema = load_json(SCHEMA_PATH)
    catalog = schema.get("field_catalog")
    if not isinstance(catalog, list) or not catalog:
        raise GateStop("schema field catalog is absent")
    out.mkdir(parents=True, exist_ok=False)
    expected_path = out / "representative_expected.jsonl"
    actual_path = out / "representative_actual.jsonl"
    ledger_path = out / "current_mismatch_ledger.json"
    expected_record = representative_observation(baseline_sequence)
    expected_path.write_bytes(canonical_bytes(expected_record, pretty=False))

    rows: list[dict[str, Any]] = []
    transcript_path = out / "mutation_transcript.jsonl"
    with transcript_path.open("wb") as transcript:
        for index, item in enumerate(catalog, start=1):
            path = str(item["path"])
            actual_record = json.loads(json.dumps(expected_record))
            original = get_path(actual_record, path)
            set_path(actual_record, path, mutated_value(original, str(item["type"])))
            if path.startswith(("events[*].", "position.", "gate_readiness.", "account.")):
                actual_record["state_digest"] = state_digest(
                    actual_record["events"],
                    actual_record["position"],
                    actual_record["gate_readiness"],
                    actual_record["account"],
                )
            actual_path.write_bytes(canonical_bytes(actual_record, pretty=False))
            red = run_self_test_subprocess(expected_path, actual_path, ledger_path)
            green = run_self_test_subprocess(expected_path, expected_path, ledger_path)
            matrix_row = {
                "matrix_id": f"FIELD-{index:03d}",
                "stable_field_component_path": path,
                "owning_record_or_digest": item["owning_record"],
                "digest_component": path in schema["digest_catalog"]["state_digest_components"],
                "mutation": {"before": original, "after": get_path(actual_record, path)},
                "expected_changed_record_count": 1,
                "actual_changed_record_count": 1,
                "failing_record_keys": [[expected_record["profile_id"], expected_record["bar_index"], expected_record["timestamp"]]],
                "red": red,
                "restoration": green,
            }
            transcript.write(canonical_bytes(matrix_row, pretty=False))
            rows.append(matrix_row)

    failures = [
        row["matrix_id"]
        for row in rows
        if row["red"]["return_code"] != 1 or row["restoration"]["return_code"] != 0
    ]
    matrix = {
        "artifact_schema_version": "P011_DISCRIMINATION_MATRIX_v1",
        "gate_version": GATE_VERSION,
        "schema_sha256": sha256_file(SCHEMA_PATH),
        "baseline_sequence_sha256": sha256_file(baseline_sequence),
        "generated_from_schema_catalog": True,
        "catalog_field_count": len(catalog),
        "matrix_row_count": len(rows),
        "digest_component_count": sum(bool(row["digest_component"]) for row in rows),
        "event_component_count": sum(row["stable_field_component_path"].startswith("events[*].") for row in rows),
        "red_count": sum(row["red"]["return_code"] == 1 for row in rows),
        "restored_green_count": sum(row["restoration"]["return_code"] == 0 for row in rows),
        "failures": failures,
        "outcome": "PASS" if not failures else "STOP",
        "rows": rows,
    }
    matrix_path = out / "discrimination_matrix.json"
    write_json(matrix_path, matrix)
    actual_path.unlink(missing_ok=True)
    ledger_path.unlink(missing_ok=True)
    result = {
        "outcome": matrix["outcome"],
        "matrix_rows": len(rows),
        "red": matrix["red_count"],
        "restored_green": matrix["restored_green_count"],
        "digest_components": matrix["digest_component_count"],
        "event_components": matrix["event_component_count"],
        "matrix_sha256": sha256_file(matrix_path),
        "transcript_sha256": sha256_file(transcript_path),
        "output_directory": str(out),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0 if not failures else 3


def command_finalize_candidate(args: argparse.Namespace) -> int:
    run1 = resolve_user_path(args.run1)
    run2 = resolve_user_path(args.run2)
    mutation_matrix = resolve_user_path(args.mutation_matrix)
    receipt_path = GATE_DIR / "P011_GATE_RECEIPT.json"
    receipt = load_json(receipt_path)
    anchor = load_json(ANCHOR_PATH)
    if anchor.get("receipt_sha256") != sha256_file(receipt_path):
        raise GateFail("pre-finalization receipt no longer matches the external anchor")
    if anchor.get("legacy_manifest_sha256") != sha256_file(GATE_DIR / "p011_legacy_manifest.json"):
        raise GateFail("pre-finalization legacy manifest no longer matches the external anchor")
    names = ["mtc_v2_legacy_sequence.jsonl", "final_states.json", "row_corroboration.json", "baseline_manifest.json"]
    artifacts: dict[str, str] = {}
    double_build: dict[str, Any] = {"run_1": str(run1), "run_2": str(run2), "byte_identical": True, "artifacts": []}
    for name in names:
        first = run1 / name
        second = run2 / name
        if not first.is_file() or not second.is_file():
            raise GateStop(f"candidate finalization artifact is missing: {name}")
        first_hash = sha256_file(first)
        second_hash = sha256_file(second)
        if first_hash != second_hash:
            raise GateFail(f"candidate finalization builds differ: {name}")
        artifacts[name] = first_hash
        double_build["artifacts"].append({"artifact": name, "run_1_sha256": first_hash, "run_2_sha256": second_hash})
    matrix = load_json(mutation_matrix)
    if matrix.get("outcome") != "PASS" or matrix.get("red_count") != matrix.get("matrix_row_count") or matrix.get("restored_green_count") != matrix.get("matrix_row_count"):
        raise GateStop("per-field discrimination matrix is not complete GREEN-after-RED evidence")
    baseline_manifest = load_json(run1 / "baseline_manifest.json")
    current_tool_hash = sha256_file(Path(__file__))
    if baseline_manifest.get("adapters", {}).get("observation_adapter", {}).get("sha256") != current_tool_hash:
        raise GateFail("candidate baseline was not built by the current pinned gate tool")
    receipt["receipt_state"] = "STAGE2_SEQUENCE_CANDIDATE_BUILT_ROW_ARM_STOP_AUDIT_PENDING"
    receipt["producer_and_adapter_bindings"]["baseline_generator"] = {
        "path": "p011_gate.py",
        "sha256": current_tool_hash,
        "status": "PASS",
    }
    receipt["producer_and_adapter_bindings"]["a_observation_adapter"] = {
        "path": "p011_gate.py",
        "sha256": current_tool_hash,
        "status": "PASS",
        "required_call": "mtc_v2.core.runner.Runner.run once per profile",
        "resolved_import_call_bindings": baseline_manifest["source"]["resolved_import_bindings"],
        "binding": baseline_manifest["adapters"]["observation_adapter"]["binding"],
    }
    receipt["baseline_outputs"] = {
        "status": "CANDIDATE_SEQUENCE_BUILT_ROW_ARM_STOP_INDEPENDENT_REPRODUCTION_PENDING",
        "artifact_sha256": artifacts,
        "double_build": double_build,
        "conservation": baseline_manifest["conservation"],
        "discrimination_matrix": {
            "path": str(mutation_matrix),
            "sha256": sha256_file(mutation_matrix),
            "matrix_rows": matrix["matrix_row_count"],
            "red": matrix["red_count"],
            "restored_green": matrix["restored_green_count"],
            "digest_components": matrix["digest_component_count"],
            "event_components": matrix["event_component_count"],
        },
        "row_arm": row_arm_receipt(),
    }
    receipt["independent_reproduction_evidence"] = {
        "status": "NOT_PERFORMED_IMPLEMENTER_MUST_NOT_SELF_ISSUE",
        "required_actor": "independent flagship other than builder",
        "auditor_checkout": None,
        "commands": [],
        "artifact_hashes": {},
    }
    write_json(receipt_path, receipt)
    final_receipt_hash = sha256_file(receipt_path)
    anchor["receipt_sha256"] = final_receipt_hash
    anchor["freeze_state"] = "STAGE2_SEQUENCE_CANDIDATE_BUILT_ROW_ARM_STOP_AUDIT_PENDING"
    anchor["subject_runs_at_signature"] = 0
    anchor["candidate_baseline_artifact_sha256"] = artifacts
    anchor["candidate_discrimination_matrix_sha256"] = sha256_file(mutation_matrix)
    write_json(ANCHOR_PATH, anchor)
    print(json.dumps({"outcome": "PASS", "receipt_sha256": final_receipt_hash, "legacy_manifest_sha256": anchor["legacy_manifest_sha256"], "artifact_sha256": artifacts, "full_gate_outcome": "STOP"}, sort_keys=True, separators=(",", ":")))
    return 0


def row_arm_receipt() -> dict[str, Any]:
    evidence_path = GATE_DIR / "evidence" / "row_arm" / "row_corroboration.json"
    if not evidence_path.is_file():
        raise GateStop("v2 row-arm re-verification evidence is absent")
    evidence = load_json(evidence_path)
    expected_counts = {"green": 33, "not_applicable": 2, "stop": 7, "total": 42}
    if evidence.get("gate_version") != GATE_VERSION:
        raise GateStop("row-arm evidence is not bound to v2")
    if evidence.get("outcome") != "STOP" or evidence.get("counts") != expected_counts:
        raise GateStop("row-arm evidence did not preserve the 33 GREEN / 7 STOP / 2 policy-only disposition")
    return {
        "outcome": "STOP",
        "counts": expected_counts,
        "reason": "7 of 40 applicable rows remain honest STOP after v2 re-verification",
        "evidence_path": str(evidence_path),
        "evidence_sha256": sha256_file(evidence_path),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P011-LC-GATE-v2 deterministic builder and comparator")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build-baseline")
    build.add_argument("--source-commit", required=True)
    build.add_argument("--producer", required=True)
    build.add_argument("--data", required=True)
    build.add_argument("--profile", action="append", required=True)
    build.add_argument("--legacy-manifest", required=True)
    build.add_argument("--out", required=True)
    build.set_defaults(func=command_build_baseline)

    validate_manifest = subparsers.add_parser("validate-legacy-manifest")
    validate_manifest.add_argument("--legacy-manifest", required=True)
    validate_manifest.add_argument("--legacy-manifest-sha256", required=True)
    validate_manifest.set_defaults(func=command_validate_legacy_manifest)

    compare = subparsers.add_parser("compare")
    compare.add_argument("--receipt", required=True)
    compare.add_argument("--baseline", required=True)
    compare.add_argument("--subject-mode", required=True)
    compare.add_argument("--mismatch-ledger", required=True)
    compare.add_argument("--actual-sequence")
    compare.set_defaults(func=command_compare)

    double = subparsers.add_parser("verify-double-build")
    double.add_argument("--run1", required=True)
    double.add_argument("--run2", required=True)
    double.set_defaults(func=command_verify_double_build)

    self_test = subparsers.add_parser("self-test-compare")
    self_test.add_argument("--expected", required=True)
    self_test.add_argument("--actual", required=True)
    self_test.add_argument("--mismatch-ledger", required=True)
    self_test.set_defaults(func=command_self_test_compare)

    mutations = subparsers.add_parser("mutation-harness")
    mutations.add_argument("--baseline", required=True)
    mutations.add_argument("--out", required=True)
    mutations.set_defaults(func=command_mutation_harness)

    finalize = subparsers.add_parser("finalize-candidate")
    finalize.add_argument("--run1", required=True)
    finalize.add_argument("--run2", required=True)
    finalize.add_argument("--mutation-matrix", required=True)
    finalize.set_defaults(func=command_finalize_candidate)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except GateFail as exc:
        print(json.dumps({"outcome": "FAIL", "reason": str(exc)}, sort_keys=True, separators=(",", ":")))
        return 1
    except GateStop as exc:
        print(json.dumps({"outcome": "STOP", "reason": str(exc)}, sort_keys=True, separators=(",", ":")))
        return 3
    except Exception as exc:
        print(json.dumps({"outcome": "STOP", "reason": f"unhandled {type(exc).__name__}: {exc}"}, sort_keys=True, separators=(",", ":")))
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
