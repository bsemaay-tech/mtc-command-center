from __future__ import annotations

import dataclasses
import math
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class RunnerWarning:
    code: str
    message: str


@dataclass(frozen=True)
class TradeRecord:
    trade_id: str
    side: str | None
    entry_time: datetime | None
    exit_time: datetime | None
    entry_price: float | None
    exit_price: float | None
    qty: float
    pnl: float
    pnl_pct: float | None
    exit_reason: str | None
    bars_held: int | None


@dataclass(frozen=True)
class EquityPoint:
    bar_index: int | None
    timestamp: datetime | None
    equity: float


@dataclass(frozen=True)
class MetricsSummary:
    net_profit: float
    net_profit_pct: float
    gross_profit: float
    gross_loss: float
    profit_factor: float | None
    max_drawdown: float
    max_drawdown_pct: float
    win_rate: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    avg_trade: float | None
    avg_trade_pct: float | None
    avg_win: float | None
    avg_loss: float | None
    largest_win: float | None
    largest_loss: float | None
    exposure_bars: int | None = None
    warnings: list[RunnerWarning] = field(default_factory=list)

    @classmethod
    def empty(cls) -> "MetricsSummary":
        return cls(
            net_profit=0.0,
            net_profit_pct=0.0,
            gross_profit=0.0,
            gross_loss=0.0,
            profit_factor=None,
            max_drawdown=0.0,
            max_drawdown_pct=0.0,
            win_rate=0.0,
            total_trades=0,
            winning_trades=0,
            losing_trades=0,
            avg_trade=None,
            avg_trade_pct=None,
            avg_win=None,
            avg_loss=None,
            largest_win=None,
            largest_loss=None,
            exposure_bars=None,
            warnings=[RunnerWarning("NO_TRADES", "No closed trades were available for metric calculation.")],
        )


@dataclass(frozen=True)
class BacktestResult:
    metrics: MetricsSummary
    trades: list[TradeRecord]
    equity_curve: list[EquityPoint]
    config_hash: str
    dataset_hash: str | None
    dataset_id: str | None
    run_id: str | None
    warnings: list[RunnerWarning]
    raw_artifact_paths: dict[str, str]

    def to_optimizer_row(self) -> dict[str, Any]:
        row = dataclasses.asdict(self.metrics)
        row.pop("warnings", None)
        row.update(
            {
                "config_hash": self.config_hash,
                "dataset_hash": self.dataset_hash,
                "dataset_id": self.dataset_id,
                "run_id": self.run_id,
                "warning_codes": "|".join(warning.code for warning in self.warnings),
            }
        )
        return row


def calculate_max_drawdown(equity_values: list[float]) -> tuple[float, float]:
    if not equity_values:
        return 0.0, 0.0
    peak = equity_values[0]
    max_drawdown = 0.0
    max_drawdown_pct = 0.0
    for value in equity_values:
        peak = max(peak, value)
        drawdown = peak - value
        if drawdown > max_drawdown:
            max_drawdown = drawdown
            max_drawdown_pct = (drawdown / peak * 100.0) if peak else 0.0
    return max_drawdown, max_drawdown_pct


def _mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def metrics_from_trades(
    trades: list[TradeRecord],
    equity_values: list[float],
    *,
    initial_capital: float,
    exposure_bars: int | None = None,
) -> MetricsSummary:
    warnings: list[RunnerWarning] = []
    if not trades:
        metrics = MetricsSummary.empty()
        final_equity = equity_values[-1] if equity_values else initial_capital
        drawdown, drawdown_pct = calculate_max_drawdown(equity_values or [initial_capital])
        return dataclasses.replace(
            metrics,
            net_profit=final_equity - initial_capital,
            net_profit_pct=((final_equity - initial_capital) / initial_capital * 100.0) if initial_capital else 0.0,
            max_drawdown=drawdown,
            max_drawdown_pct=drawdown_pct,
        )

    pnl_values = [float(trade.pnl) for trade in trades if math.isfinite(float(trade.pnl))]
    pct_values = [float(trade.pnl_pct) for trade in trades if trade.pnl_pct is not None and math.isfinite(float(trade.pnl_pct))]
    gross_profit = sum(value for value in pnl_values if value > 0)
    gross_loss = abs(sum(value for value in pnl_values if value < 0))
    profit_factor: float | None
    if gross_loss > 0:
        profit_factor = gross_profit / gross_loss
    else:
        profit_factor = None
        warnings.append(RunnerWarning("ZERO_GROSS_LOSS", "Profit factor is unavailable because gross loss is zero."))
    winning = [value for value in pnl_values if value > 0]
    losing = [value for value in pnl_values if value < 0]
    final_equity = equity_values[-1] if equity_values else initial_capital + sum(pnl_values)
    drawdown, drawdown_pct = calculate_max_drawdown(equity_values or [initial_capital, final_equity])
    return MetricsSummary(
        net_profit=final_equity - initial_capital,
        net_profit_pct=((final_equity - initial_capital) / initial_capital * 100.0) if initial_capital else 0.0,
        gross_profit=gross_profit,
        gross_loss=gross_loss,
        profit_factor=profit_factor,
        max_drawdown=drawdown,
        max_drawdown_pct=drawdown_pct,
        win_rate=(len(winning) / len(pnl_values) * 100.0) if pnl_values else 0.0,
        total_trades=len(pnl_values),
        winning_trades=len(winning),
        losing_trades=len(losing),
        avg_trade=_mean(pnl_values),
        avg_trade_pct=_mean(pct_values),
        avg_win=_mean(winning),
        avg_loss=_mean(losing),
        largest_win=max(winning) if winning else None,
        largest_loss=min(losing) if losing else None,
        exposure_bars=exposure_bars,
        warnings=warnings,
    )
