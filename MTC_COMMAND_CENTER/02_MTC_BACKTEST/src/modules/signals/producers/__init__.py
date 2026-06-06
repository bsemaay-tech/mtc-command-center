"""Manual producer adapters for MTC-Engine Validation."""

from __future__ import annotations

from typing import Any

from src.modules.signals.base import SignalPlugin

from .quantlens_momentum_continuation_producer import QuantLensMomentumContinuationProducerAdapter
from .supertrend_producer import SupertrendProducerAdapter


PRODUCER_REGISTRY = {
    "supertrend": SupertrendProducerAdapter,
    "producer_supertrend": SupertrendProducerAdapter,
    "ql_fam_momentum_continuation": QuantLensMomentumContinuationProducerAdapter,
    "producer_ql_fam_momentum_continuation": QuantLensMomentumContinuationProducerAdapter,
    "momentum_continuation": QuantLensMomentumContinuationProducerAdapter,
}


def create_producer(name: str, params: dict[str, Any] | None = None) -> SignalPlugin:
    key = name.strip().lower()
    try:
        cls = PRODUCER_REGISTRY[key]
    except KeyError as exc:
        known = ", ".join(sorted(PRODUCER_REGISTRY))
        raise ValueError(f"Unknown producer {name!r}. Known producers: {known}") from exc
    return cls(**(params or {}))


__all__ = [
    "PRODUCER_REGISTRY",
    "QuantLensMomentumContinuationProducerAdapter",
    "SupertrendProducerAdapter",
    "create_producer",
]
