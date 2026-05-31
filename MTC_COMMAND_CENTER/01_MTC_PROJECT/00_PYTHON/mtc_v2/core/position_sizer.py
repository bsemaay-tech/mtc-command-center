from __future__ import annotations

import math

from mtc_v2.core.instrument import InstrumentMetadata
from mtc_v2.core.types import Position


class PositionSizer:
    """L6 risk-based quantity owner.

    The runner provides a frozen equity snapshot for the current bar. This
    module only converts that snapshot plus the current entry/SL context into a
    broker-rounded quantity. It does not decide entry direction or sequencing.
    """

    def __init__(self, config: dict[str, object]) -> None:
        self.risk_per_long_pct = float(config["risk_per_long_pct"])
        self.risk_per_short_pct = float(config["risk_per_short_pct"])
        self.fallback_size_pct = float(config["fallback_size_pct"])
        self.max_leverage_cap = float(config["max_leverage_cap"])
        self.tw_audit_semantics_mode = str(config.get("tw_audit_semantics_mode", "off"))

    def calc_qty(
        self,
        entry: float,
        sl: float | None,
        equity: float,
        is_long: bool,
        instrument: InstrumentMetadata,
        existing_position: Position | None = None,
    ) -> float:
        del existing_position  # Basket state is owned by PositionManager in L6a.

        if not math.isfinite(entry) or entry <= 0.0:
            return 0.0
        if not math.isfinite(equity) or equity <= 0.0:
            return 0.0

        risk_pct = self.risk_per_long_pct if is_long else self.risk_per_short_pct
        raw_qty = 0.0

        if sl is not None and math.isfinite(sl):
            per_unit_risk = abs(entry - sl)
            if per_unit_risk > 0.0:
                risk_amount = equity * (risk_pct / 100.0)
                raw_qty = risk_amount / per_unit_risk
        else:
            fallback_notional = equity * (self.fallback_size_pct / 100.0)
            raw_qty = fallback_notional / entry

        leverage_cap_qty = (equity * self.max_leverage_cap) / (
            entry * instrument.contract_multiplier
        )
        raw_qty = min(raw_qty, leverage_cap_qty)

        if not math.isfinite(raw_qty) or raw_qty <= 0.0:
            return 0.0

        rounded_qty = instrument.floor_qty(raw_qty)
        if self.tw_audit_semantics_mode == "research":
            rounded_qty = math.floor(raw_qty * 1_000_000.0) / 1_000_000.0
        if rounded_qty < instrument.min_qty:
            return 0.0

        order_notional = rounded_qty * entry * instrument.contract_multiplier
        if order_notional < instrument.min_notional:
            return 0.0

        return rounded_qty
