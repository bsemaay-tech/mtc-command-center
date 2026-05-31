from __future__ import annotations

from dataclasses import dataclass

from mtc_v2.core.rounding import ceil_to_grid, floor_qty_to_step, floor_to_grid, round_half_up_to_grid


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
