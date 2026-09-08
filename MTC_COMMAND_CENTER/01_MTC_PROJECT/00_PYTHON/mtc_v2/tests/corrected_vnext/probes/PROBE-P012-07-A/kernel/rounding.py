from __future__ import annotations

from decimal import Decimal, ROUND_CEILING, ROUND_DOWN, ROUND_FLOOR, ROUND_HALF_UP


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
