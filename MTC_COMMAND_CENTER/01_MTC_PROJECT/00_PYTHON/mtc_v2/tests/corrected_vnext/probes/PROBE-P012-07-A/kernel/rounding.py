from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal, ROUND_CEILING, ROUND_DOWN, ROUND_FLOOR, ROUND_HALF_UP
from typing import Literal


PriceAlignmentDirection = Literal["FLOOR", "CEIL", "HALF_UP"]


@dataclass(frozen=True, slots=True)
class PriceAlignmentPolicy:
    id: str
    significant_figures: int
    perp_max_decimals: int
    size_decimals: int
    integer_exception: bool
    positive_price_required: bool

    def __post_init__(self) -> None:
        expected = {
            "id": "HYPERLIQUID_PX_V1",
            "significant_figures": 5,
            "perp_max_decimals": 6,
            "size_decimals": 5,
            "integer_exception": True,
            "positive_price_required": True,
        }
        for field_name, expected_value in expected.items():
            actual = getattr(self, field_name)
            if type(actual) is not type(expected_value) or actual != expected_value:
                raise ValueError(f"unsupported price alignment policy field {field_name}")

    @classmethod
    def from_mapping(cls, raw: Mapping[str, object]) -> "PriceAlignmentPolicy":
        fields = {
            "id",
            "significant_figures",
            "perp_max_decimals",
            "size_decimals",
            "integer_exception",
            "positive_price_required",
        }
        if not isinstance(raw, Mapping) or set(raw) != fields:
            raise ValueError("price alignment policy requires exactly six supported fields")
        return cls(
            id=raw["id"],  # type: ignore[arg-type]
            significant_figures=raw["significant_figures"],  # type: ignore[arg-type]
            perp_max_decimals=raw["perp_max_decimals"],  # type: ignore[arg-type]
            size_decimals=raw["size_decimals"],  # type: ignore[arg-type]
            integer_exception=raw["integer_exception"],  # type: ignore[arg-type]
            positive_price_required=raw["positive_price_required"],  # type: ignore[arg-type]
        )


def _policy_decimal(value: int | float) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("price must be numeric and not boolean")
    decimal_value = Decimal(str(value))
    if not decimal_value.is_finite() or decimal_value <= 0:
        raise ValueError("price must be finite and > 0")
    return decimal_value


def is_valid_price(value: int | float, policy: PriceAlignmentPolicy) -> bool:
    if not isinstance(policy, PriceAlignmentPolicy):
        return False
    if isinstance(value, int) and not isinstance(value, bool):
        return value > 0
    try:
        decimal_value = _policy_decimal(value)
    except (ValueError, ArithmeticError):
        return False
    if decimal_value == decimal_value.to_integral_value():
        return True
    return (
        decimal_value <= Decimal("9999.9")
        and decimal_value * 10 == (decimal_value * 10).to_integral_value()
    )


def align_price_to_policy(
    value: int | float,
    policy: PriceAlignmentPolicy,
    direction: PriceAlignmentDirection,
) -> int | float:
    if not isinstance(policy, PriceAlignmentPolicy):
        raise ValueError("unsupported price alignment policy")
    if direction not in {"FLOOR", "CEIL", "HALF_UP"}:
        raise ValueError(f"unsupported price alignment direction {direction!r}")
    if isinstance(value, int) and not isinstance(value, bool):
        if value <= 0:
            raise ValueError("price must be finite and > 0")
        return value
    decimal_value = _policy_decimal(value)
    if decimal_value < Decimal("10000"):
        scaled = decimal_value * 10
        lower_units = scaled.to_integral_value(rounding=ROUND_FLOOR)
        upper_units = scaled.to_integral_value(rounding=ROUND_CEILING)
        lower = lower_units / 10 if lower_units >= 1 else None
        upper = upper_units / 10
    else:
        lower = decimal_value.to_integral_value(rounding=ROUND_FLOOR)
        upper = decimal_value.to_integral_value(rounding=ROUND_CEILING)

    if direction == "FLOOR":
        if lower is None:
            raise ValueError("price has no positive valid floor")
        return float(lower)
    if direction == "CEIL":
        return float(upper)
    if lower is None or decimal_value - lower >= upper - decimal_value:
        return float(upper)
    return float(lower)


def round_half_up_to_grid(value: float, tick: float) -> float:
    tick_decimal = _positive_decimal(tick, "tick")
    value_decimal = Decimal(str(value))
    units = (value_decimal / tick_decimal).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return float(units * tick_decimal)


def floor_to_grid(value: float, tick: float) -> float:
    tick_decimal = _positive_decimal(tick, "tick")
    value_decimal = Decimal(str(value))
    units = (value_decimal / tick_decimal).quantize(Decimal("1"), rounding=ROUND_FLOOR)
    return float(units * tick_decimal)


def ceil_to_grid(value: float, tick: float) -> float:
    tick_decimal = _positive_decimal(tick, "tick")
    value_decimal = Decimal(str(value))
    units = (value_decimal / tick_decimal).quantize(Decimal("1"), rounding=ROUND_CEILING)
    return float(units * tick_decimal)


def floor_qty_to_step(value: float, qty_step: float) -> float:
    step_decimal = _positive_decimal(qty_step, "qty_step")
    value_decimal = Decimal(str(value))
    if value_decimal <= 0:
        return 0.0
    units = (value_decimal / step_decimal).quantize(Decimal("1"), rounding=ROUND_DOWN)
    return float(units * step_decimal)


def _positive_decimal(value: float, label: str) -> Decimal:
    decimal_value = Decimal(str(value))
    if decimal_value <= 0:
        raise ValueError(f"{label} must be > 0")
    return decimal_value
