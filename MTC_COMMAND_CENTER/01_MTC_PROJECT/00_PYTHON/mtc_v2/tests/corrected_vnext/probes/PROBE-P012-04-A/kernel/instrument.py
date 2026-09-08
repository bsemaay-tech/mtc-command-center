from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import re
from types import MappingProxyType
from typing import Any

from mtc_v2.core.rounding import ceil_to_grid, floor_qty_to_step, floor_to_grid, round_half_up_to_grid


REFUSED_INVALID_RECORD_BYTES = "REFUSED_INVALID_RECORD_BYTES"
REFUSED_INCOMPLETE_INSTRUMENT_RECORD = "REFUSED_INCOMPLETE_INSTRUMENT_RECORD"
REFUSED_INSTRUMENT_RECORD_OUT_OF_RANGE = "REFUSED_INSTRUMENT_RECORD_OUT_OF_RANGE"
REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION = (
    "REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION"
)

_LOWER_SHA256 = re.compile(r"[0-9a-f]{64}")


class InstrumentRecordRefusal(ValueError):
    def __init__(self, refusal_code: str, detail: str) -> None:
        self.refusal_code = refusal_code
        super().__init__(f"{refusal_code}: {detail}")


def _refuse_invalid(detail: str) -> InstrumentRecordRefusal:
    return InstrumentRecordRefusal(REFUSED_INVALID_RECORD_BYTES, detail)


def _duplicate_rejecting_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON token: {token}")


def _reject_nonfinite(value: Any, location: str = "$") -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"non-finite number at {location}")
    if isinstance(value, list):
        for index, item in enumerate(value):
            _reject_nonfinite(item, f"{location}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            _reject_nonfinite(item, f"{location}.{key}")


def _deep_freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _deep_freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_deep_freeze(item) for item in value)
    return value


@dataclass(slots=True, frozen=True)
class VerifiedJsonRecord:
    path: Path
    digest: str
    raw_bytes: bytes
    data: Mapping[str, Any]


def load_verified_json_record(path: str | Path) -> VerifiedJsonRecord:
    """Load one exact-byte JSON record and its mandatory detached digest."""

    record_path = Path(path)
    digest_path = record_path.with_name(record_path.name + ".sha256")
    try:
        raw = record_path.read_bytes()
        detached = digest_path.read_bytes()
    except OSError as exc:
        raise _refuse_invalid(f"record or detached digest unavailable: {exc}") from exc

    if raw.startswith(b"\xef\xbb\xbf"):
        raise _refuse_invalid("UTF-8 BOM is forbidden")
    if b"\r" in raw:
        raise _refuse_invalid("CR byte is forbidden")
    if not raw.endswith(b"\n"):
        raise _refuse_invalid("final LF is required")
    if len(detached) != 65 or not detached.endswith(b"\n"):
        raise _refuse_invalid("detached digest must be 64 lower-case hex bytes plus LF")
    try:
        expected_digest = detached[:-1].decode("ascii")
    except UnicodeDecodeError as exc:
        raise _refuse_invalid("detached digest is not ASCII") from exc
    if _LOWER_SHA256.fullmatch(expected_digest) is None:
        raise _refuse_invalid("detached digest is not lower-case SHA-256")
    actual_digest = hashlib.sha256(raw).hexdigest()
    if actual_digest != expected_digest:
        raise _refuse_invalid(
            f"detached digest mismatch: expected {expected_digest}, actual {actual_digest}"
        )

    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_duplicate_rejecting_object,
            parse_constant=_reject_constant,
        )
        _reject_nonfinite(value)
    except (UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise _refuse_invalid(f"strict JSON refusal: {exc}") from exc
    if not isinstance(value, dict):
        raise _refuse_invalid("record root must be an object")
    return VerifiedJsonRecord(
        path=record_path,
        digest=actual_digest,
        raw_bytes=raw,
        data=_deep_freeze(value),
    )


def _parse_utc(value: str, field_name: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise InstrumentRecordRefusal(
            REFUSED_INCOMPLETE_INSTRUMENT_RECORD,
            f"{field_name} must be an explicit Z timestamp",
        )
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise InstrumentRecordRefusal(
            REFUSED_INCOMPLETE_INSTRUMENT_RECORD,
            f"{field_name} is not an ISO-8601 timestamp",
        ) from exc
    return parsed.astimezone(timezone.utc)


def _required_number(
    value: Any,
    field_name: str,
    *,
    positive: bool,
) -> float:
    if value is None:
        raise InstrumentRecordRefusal(
            REFUSED_INCOMPLETE_INSTRUMENT_RECORD,
            f"{field_name} is absent",
        )
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InstrumentRecordRefusal(
            REFUSED_INCOMPLETE_INSTRUMENT_RECORD,
            f"{field_name} must be numeric",
        )
    number = float(value)
    if not math.isfinite(number) or (positive and number <= 0.0) or (
        not positive and number < 0.0
    ):
        relation = "> 0" if positive else ">= 0"
        raise InstrumentRecordRefusal(
            REFUSED_INCOMPLETE_INSTRUMENT_RECORD,
            f"{field_name} must be finite and {relation}",
        )
    return number


@dataclass(slots=True, frozen=True)
class InstrumentRecord:
    record_id: str
    digest: str
    venue: str | None
    product_type: str | None
    symbol: str | None
    settlement_currency: str | None
    point_value: int | float | None
    price_tick: int | float | None
    quantity_step: int | float | None
    minimum_quantity: int | float | None
    minimum_notional: int | float | None
    contract_multiplier: int | float | None
    effective_interval: Mapping[str, Any] | None
    provenance: Mapping[str, Any] | None
    source_path: Path

    def for_evaluation(
        self,
        evaluation_time: str | datetime,
        runtime_config: Mapping[str, object],
    ) -> "InstrumentMetadata":
        text_fields = {
            "venue": self.venue,
            "product_type": self.product_type,
            "symbol": self.symbol,
            "settlement_currency": self.settlement_currency,
        }
        missing_text = [
            name
            for name, value in text_fields.items()
            if not isinstance(value, str) or not value.strip()
        ]
        if missing_text:
            raise InstrumentRecordRefusal(
                REFUSED_INCOMPLETE_INSTRUMENT_RECORD,
                f"missing text fields: {', '.join(missing_text)}",
            )

        numbers = {
            "point_value": _required_number(self.point_value, "point_value", positive=True),
            "price_tick": _required_number(self.price_tick, "price_tick", positive=True),
            "quantity_step": _required_number(
                self.quantity_step, "quantity_step", positive=True
            ),
            "minimum_quantity": _required_number(
                self.minimum_quantity, "minimum_quantity", positive=False
            ),
            "minimum_notional": _required_number(
                self.minimum_notional, "minimum_notional", positive=False
            ),
            "contract_multiplier": _required_number(
                self.contract_multiplier, "contract_multiplier", positive=True
            ),
        }

        if self.provenance is None or not self.provenance.get("human_reviewer"):
            raise InstrumentRecordRefusal(
                REFUSED_INCOMPLETE_INSTRUMENT_RECORD,
                "provenance.human_reviewer is absent",
            )
        if self.effective_interval is None:
            raise InstrumentRecordRefusal(
                REFUSED_INCOMPLETE_INSTRUMENT_RECORD,
                "effective_interval is absent",
            )
        start_raw = self.effective_interval.get(
            "start_inclusive", self.effective_interval.get("start_utc")
        )
        end_raw = self.effective_interval.get(
            "end_exclusive", self.effective_interval.get("end_utc")
        )
        start = _parse_utc(start_raw, "effective_interval start")
        if isinstance(evaluation_time, str):
            evaluation = _parse_utc(evaluation_time, "evaluation_time")
        elif isinstance(evaluation_time, datetime):
            if evaluation_time.tzinfo is None:
                raise InstrumentRecordRefusal(
                    REFUSED_INCOMPLETE_INSTRUMENT_RECORD,
                    "evaluation_time must be timezone-aware",
                )
            evaluation = evaluation_time.astimezone(timezone.utc)
        else:
            raise InstrumentRecordRefusal(
                REFUSED_INCOMPLETE_INSTRUMENT_RECORD,
                "evaluation_time must be a timestamp string or datetime",
            )
        end = _parse_utc(end_raw, "effective_interval end") if end_raw is not None else None
        if evaluation < start or (end is not None and evaluation >= end):
            raise InstrumentRecordRefusal(
                REFUSED_INSTRUMENT_RECORD_OUT_OF_RANGE,
                "evaluation timestamp is outside the record interval",
            )

        runtime_pairs = {
            "instrument_symbol": self.symbol,
            "instrument_point_value": numbers["point_value"],
            "instrument_price_tick": numbers["price_tick"],
            "instrument_qty_step": numbers["quantity_step"],
            "instrument_min_qty": numbers["minimum_quantity"],
            "instrument_min_notional": numbers["minimum_notional"],
            "instrument_contract_multiplier": numbers["contract_multiplier"],
        }
        for key, record_value in runtime_pairs.items():
            if key not in runtime_config:
                continue
            runtime_value = runtime_config[key]
            if isinstance(record_value, float):
                equal = (
                    not isinstance(runtime_value, bool)
                    and isinstance(runtime_value, (int, float))
                    and math.isfinite(float(runtime_value))
                    and float(runtime_value) == record_value
                )
            else:
                equal = runtime_value == record_value
            if not equal:
                raise InstrumentRecordRefusal(
                    REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION,
                    f"{key} differs from immutable record {self.record_id}",
                )

        return InstrumentMetadata(
            symbol=self.symbol,
            point_value=numbers["point_value"],
            price_tick=numbers["price_tick"],
            qty_step=numbers["quantity_step"],
            min_qty=numbers["minimum_quantity"],
            min_notional=numbers["minimum_notional"],
            contract_multiplier=numbers["contract_multiplier"],
        )


def load_verified_instrument_record(path: str | Path) -> InstrumentRecord:
    verified = load_verified_json_record(path)
    data = verified.data
    effective = data.get("effective_interval")
    provenance = data.get("provenance")
    return InstrumentRecord(
        record_id=str(data.get("record_id", verified.path.stem)),
        digest=verified.digest,
        venue=data.get("venue"),
        product_type=data.get("product_type"),
        symbol=data.get("symbol"),
        settlement_currency=data.get("settlement_currency"),
        point_value=data.get("point_value"),
        price_tick=data.get("price_tick"),
        quantity_step=data.get("quantity_step"),
        minimum_quantity=data.get("minimum_quantity"),
        minimum_notional=data.get("minimum_notional"),
        contract_multiplier=data.get("contract_multiplier"),
        effective_interval=effective if isinstance(effective, Mapping) else None,
        provenance=provenance if isinstance(provenance, Mapping) else None,
        source_path=verified.path,
    )


@dataclass(slots=True, frozen=True)
class InstrumentMetadata:
    symbol: str = "UNKNOWN"
    point_value: float = 1.0
    price_tick: float = 0.01
    qty_step: float = 1.0
    min_qty: float = 0.0
    min_notional: float = 0.0
    contract_multiplier: float = 1.0

    @classmethod
    def from_config(cls, config: dict[str, object]) -> "InstrumentMetadata":
        return cls(
            symbol=str(config["instrument_symbol"]),
            point_value=float(config["instrument_point_value"]),
            price_tick=float(config["instrument_price_tick"]),
            qty_step=float(config["instrument_qty_step"]),
            min_qty=float(config["instrument_min_qty"]),
            min_notional=float(config["instrument_min_notional"]),
            contract_multiplier=float(config["instrument_contract_multiplier"]),
        )

    def round_price(self, value: float) -> float:
        return round_half_up_to_grid(value, self.price_tick)

    def floor_price(self, value: float) -> float:
        return floor_to_grid(value, self.price_tick)

    def ceil_price(self, value: float) -> float:
        return ceil_to_grid(value, self.price_tick)

    def floor_qty(self, value: float) -> float:
        return floor_qty_to_step(value, self.qty_step)
