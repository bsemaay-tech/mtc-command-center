"""In-code draft mtc.signal/v1 validation for the local SYSTEM_TEST_ONLY slice."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from .constants import ALLOWED_ENVIRONMENTS, SCHEMA_ID


REQUIRED_FIELDS = {
    "schema",
    "strategy_id",
    "strategy_version",
    "environment",
    "symbol",
    "exchange",
    "timeframe",
    "signal_id",
    "idempotency_key",
    "timestamp_utc",
    "bar_time_utc",
    "side",
    "action",
    "qty_model",
    "risk_ref",
    "current_position_intent",
    "auth_token",
    "checksum",
}

OPTIONAL_FIELDS = {
    "candidate_id",
    "engine_strategy_id",
    "stop_loss",
    "take_profit",
    "entry_price",
    "exit_price",
    "exit_reason",
    "source_trade_index",
}

ALLOWED_FIELDS = REQUIRED_FIELDS | OPTIONAL_FIELDS
VALID_SIDES = {"LONG", "SHORT", "FLAT"}
VALID_ACTIONS = {"ENTRY", "EXIT", "CANCEL"}
ENTRY_INTENTS = {"FLAT_TO_LONG", "FLAT_TO_SHORT"}
EXIT_INTENTS = {"LONG_TO_FLAT", "SHORT_TO_FLAT"}
HEX_64 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    errors: tuple[str, ...]
    canonical_payload: dict[str, Any] | None = None


def canonicalize_timestamp(value: str) -> str:
    text = str(value).strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    elif text.endswith("+0000"):
        text = text[:-5] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    dt = dt.astimezone(timezone.utc).replace(microsecond=0)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def make_signal_id(
    strategy_id: str,
    symbol: str,
    timeframe: str,
    bar_time_utc: str,
    action: str,
) -> str:
    canonical_bar_time = canonicalize_timestamp(bar_time_utc)
    return "|".join([strategy_id, symbol, timeframe, canonical_bar_time, action])


def make_idempotency_key(signal_id: str, strategy_version: str) -> str:
    return hashlib.sha256(f"{signal_id}|{strategy_version}".encode("utf-8")).hexdigest()


def canonicalize_payload(payload: dict[str, Any]) -> dict[str, Any]:
    canonical = dict(payload)
    for key in ("timestamp_utc", "bar_time_utc"):
        if key in canonical and canonical[key] is not None:
            canonical[key] = canonicalize_timestamp(str(canonical[key]))
    return canonical


def checksum_material(payload: dict[str, Any]) -> str:
    canonical = canonicalize_payload(payload)
    filtered = {
        key: canonical[key]
        for key in sorted(canonical)
        if key not in {"auth_token", "checksum"}
    }
    return json.dumps(filtered, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def compute_checksum(payload: dict[str, Any]) -> str:
    return hashlib.sha256(checksum_material(payload).encode("utf-8")).hexdigest()


def sign_payload(payload: dict[str, Any], auth_token: str) -> dict[str, Any]:
    signed = canonicalize_payload(payload)
    signed["signal_id"] = make_signal_id(
        signed["strategy_id"],
        signed["symbol"],
        signed["timeframe"],
        signed["bar_time_utc"],
        signed["action"],
    )
    signed["idempotency_key"] = make_idempotency_key(
        signed["signal_id"], signed["strategy_version"]
    )
    signed["auth_token"] = auth_token
    signed["checksum"] = compute_checksum(signed)
    return signed


def redact_sensitive_fields(payload: dict[str, Any]) -> dict[str, Any]:
    redacted = dict(payload)
    if "auth_token" in redacted:
        redacted["auth_token"] = "<REDACTED>"
    return redacted


def validate_signal_payload(
    payload: dict[str, Any],
    expected_auth_token: str,
) -> ValidationResult:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ValidationResult(False, ("payload must be an object",), None)

    extra = sorted(set(payload) - ALLOWED_FIELDS)
    if extra:
        errors.append(f"unrecognized fields: {', '.join(extra)}")

    missing = sorted(REQUIRED_FIELDS - set(payload))
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")
        return ValidationResult(False, tuple(errors), None)

    canonical = canonicalize_payload(payload)

    if canonical.get("schema") != SCHEMA_ID:
        errors.append("schema must be mtc.signal/v1")

    environment = canonical.get("environment")
    if environment not in ALLOWED_ENVIRONMENTS:
        errors.append(f"environment {environment!r} is not allowed")

    if canonical.get("auth_token") != expected_auth_token:
        errors.append("auth_token mismatch")

    action = canonical.get("action")
    side = canonical.get("side")
    intent = canonical.get("current_position_intent")
    if action not in VALID_ACTIONS:
        errors.append(f"invalid action: {action!r}")
    if side not in VALID_SIDES:
        errors.append(f"invalid side: {side!r}")
    if action == "ENTRY" and intent not in ENTRY_INTENTS:
        errors.append("ENTRY requires FLAT_TO_LONG or FLAT_TO_SHORT intent")
    if action == "EXIT" and intent not in EXIT_INTENTS:
        errors.append("EXIT requires LONG_TO_FLAT or SHORT_TO_FLAT intent")

    expected_signal_id = make_signal_id(
        str(canonical["strategy_id"]),
        str(canonical["symbol"]),
        str(canonical["timeframe"]),
        str(canonical["bar_time_utc"]),
        str(canonical["action"]),
    )
    if canonical.get("signal_id") != expected_signal_id:
        errors.append("signal_id mismatch")

    expected_idempotency = make_idempotency_key(
        expected_signal_id, str(canonical["strategy_version"])
    )
    if canonical.get("idempotency_key") != expected_idempotency:
        errors.append("idempotency_key mismatch")

    checksum = canonical.get("checksum")
    if not isinstance(checksum, str) or not HEX_64.match(checksum):
        errors.append("checksum malformed")
    elif checksum != compute_checksum(canonical):
        errors.append("checksum mismatch")

    for field in ("entry_price", "exit_price", "stop_loss", "take_profit"):
        value = canonical.get(field)
        if value is None:
            continue
        if not isinstance(value, (int, float)):
            errors.append(f"{field} must be numeric")
        elif value <= 0:
            errors.append(f"{field} must be positive")

    if (
        action == "ENTRY"
        and side == "LONG"
        and canonical.get("entry_price") is not None
        and canonical.get("stop_loss") is not None
        and isinstance(canonical["entry_price"], (int, float))
        and isinstance(canonical["stop_loss"], (int, float))
        and canonical["stop_loss"] >= canonical["entry_price"]
    ):
        errors.append("long ENTRY requires stop_loss below entry_price")

    return ValidationResult(not errors, tuple(errors), canonical)
