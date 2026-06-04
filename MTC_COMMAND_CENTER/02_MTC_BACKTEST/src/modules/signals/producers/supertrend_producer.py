"""Golden producer adapter wrapping the existing Supertrend signal plugin."""

from __future__ import annotations

from src.modules.signals.supertrend import SupertrendSignal


class SupertrendProducerAdapter(SupertrendSignal):
    """Manual producer adapter for Supertrend raw long/short signals.

    This adapter intentionally delegates to the existing SupertrendSignal
    implementation and does not add filters, exits, risk, or lifecycle logic.
    """

    def __init__(
        self,
        atr_len: int = 21,
        factor: float = 4.0,
        use_wicks: bool = True,
        use_ha: bool = True,
    ) -> None:
        super().__init__(
            atr_len=atr_len,
            factor=factor,
            use_wicks=use_wicks,
            use_ha=use_ha,
        )
        self.name = "producer_supertrend"
