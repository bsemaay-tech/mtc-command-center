from __future__ import annotations

import dataclasses
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping

from mtc_v2.core.economics import EconomicRecords
from mtc_v2.core.types import CashEventKind, PortfolioState


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


@dataclass(frozen=True)
class CorrectedTradeRecord:
    """One closed corrected lifecycle, kept separate from the legacy shape."""

    entry_fill_price: float
    quantity: float
    exit_ids: list[str]
    gross_realized_pnl: float
    fee_total: float
    funding_total: float
    net_trade_pnl: float


@dataclass(frozen=True)
class CorrectedRunManifest:
    execution_profile_id: str
    instrument_record_id: str
    instrument_record_digest: str
    instrument_source_document_digest: str
    instrument_effective_interval: dict[str, Any]
    cost_schedule_id: str
    cost_schedule_digest: str | None
    funding_schedule_id: str
    funding_schedule_digest: str
    same_bar_collision_policy_id: str | None = None
    kernel_semantics_version: str = "2.0.0"

    @classmethod
    def from_records(
        cls,
        records: EconomicRecords,
        *,
        execution_profile_id: str,
        same_bar_collision_policy_id: str | None = None,
    ) -> "CorrectedRunManifest":
        provenance = records.instrument.provenance or {}
        effective = records.instrument.effective_interval or {}
        return cls(
            execution_profile_id=execution_profile_id,
            instrument_record_id=records.instrument.record_id,
            instrument_record_digest=records.instrument.digest,
            instrument_source_document_digest=str(provenance.get("source_sha256", "")),
            instrument_effective_interval=dict(effective),
            cost_schedule_id=records.cost_schedule_id or "NOT_CONSUMED",
            cost_schedule_digest=records.cost_digest,
            funding_schedule_id=records.funding_schedule_id,
            funding_schedule_digest=records.funding_digest,
            same_bar_collision_policy_id=same_bar_collision_policy_id,
        )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "kernel_semantics_version": self.kernel_semantics_version,
            "execution_profile_id": self.execution_profile_id,
        }
        if self.same_bar_collision_policy_id is not None:
            result["same_bar_collision_policy_id"] = self.same_bar_collision_policy_id
        result.update(
            {
                "instrument_record_id": self.instrument_record_id,
                "instrument_record_digest": self.instrument_record_digest,
                "instrument_source_document_digest": self.instrument_source_document_digest,
                "instrument_effective_interval": self.instrument_effective_interval,
                "cost_schedule_id": self.cost_schedule_id,
            }
        )
        if self.cost_schedule_digest is not None:
            result["cost_schedule_digest"] = self.cost_schedule_digest
        result.update(
            {
                "funding_schedule_id": self.funding_schedule_id,
                "funding_schedule_digest": self.funding_schedule_digest,
            }
        )
        return result


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


def corrected_metrics_from_trades(
    trades: list[CorrectedTradeRecord],
    equity_values: list[float],
    *,
    initial_capital: float,
    exposure_bars: int | None = None,
) -> MetricsSummary:
    """Calculate corrected metrics from lifecycle net cash, never gross PnL."""

    if not trades:
        metrics = MetricsSummary.empty()
        final_equity = equity_values[-1] if equity_values else initial_capital
        drawdown, drawdown_pct = calculate_max_drawdown(
            equity_values or [initial_capital]
        )
        return dataclasses.replace(
            metrics,
            net_profit=final_equity - initial_capital,
            net_profit_pct=(
                (final_equity - initial_capital) / initial_capital * 100.0
                if initial_capital
                else 0.0
            ),
            max_drawdown=drawdown,
            max_drawdown_pct=drawdown_pct,
        )

    pnl_values = [
        float(trade.net_trade_pnl)
        for trade in trades
        if math.isfinite(float(trade.net_trade_pnl))
    ]
    gross_profit = sum(value for value in pnl_values if value > 0.0)
    gross_loss = abs(sum(value for value in pnl_values if value < 0.0))
    warnings: list[RunnerWarning] = []
    if gross_loss > 0.0:
        profit_factor: float | None = gross_profit / gross_loss
    else:
        profit_factor = None
        warnings.append(
            RunnerWarning(
                "ZERO_GROSS_LOSS",
                "Profit factor is unavailable because gross loss is zero.",
            )
        )
    winning = [value for value in pnl_values if value > 0.0]
    losing = [value for value in pnl_values if value < 0.0]
    final_equity = (
        equity_values[-1]
        if equity_values
        else initial_capital + sum(pnl_values)
    )
    drawdown, drawdown_pct = calculate_max_drawdown(
        equity_values or [initial_capital, final_equity]
    )
    return MetricsSummary(
        net_profit=final_equity - initial_capital,
        net_profit_pct=(
            (final_equity - initial_capital) / initial_capital * 100.0
            if initial_capital
            else 0.0
        ),
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
        avg_trade_pct=None,
        avg_win=_mean(winning),
        avg_loss=_mean(losing),
        largest_win=max(winning) if winning else None,
        largest_loss=min(losing) if losing else None,
        exposure_bars=exposure_bars,
        warnings=warnings,
    )


def _timestamp(value: datetime) -> str:
    if value.tzinfo is None:
        raise ValueError("corrected event timestamps must be timezone-aware")
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _json_number(value: float | int) -> float | int:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("corrected surfaces refuse non-finite numbers")
    if number == 0.0 and math.copysign(1.0, number) < 0.0:
        return -0.0
    if number.is_integer():
        return int(number)
    return number


def _in_window(
    timestamp: datetime,
    start: datetime | None,
    end: datetime | None,
) -> bool:
    return (start is None or timestamp >= start) and (end is None or timestamp <= end)


def _event_rows(
    rows: Iterable[object],
    *,
    start: datetime | None,
    end: datetime | None,
) -> list[object]:
    return [
        row
        for row in rows
        if _in_window(getattr(row, "event_timestamp"), start, end)
    ]


_REMOVED_DECISIONS = {
    "SLIPPAGE_RESOLVED",
    "FEE_SCHEDULE_RESOLVED",
    "GUARD_BASIS_RESOLVED",
    "MARKET_EXIT_SELECTED",
}

_DECISION_MEMBERS = {
    "SEMANTICS_VALIDATED": (set(), set()),
    "SIZING_COMPUTED": ({"selector", "contract_multiplier", "order_notional"}, set()),
    "MIN_NOTIONAL_ADMITTED": ({"order_notional", "required_min_notional"}, set()),
    "REFUSED_MIN_NOTIONAL": ({"order_notional", "required_min_notional"}, set()),
    "INSTRUMENT_RECORD_VALIDATED": ({"field", "record_value", "runtime_value"}, set()),
    "REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION": ({"field", "record_value", "runtime_value"}, set()),
    "PROTECTIVE_STOP_EVALUATED": (
        {"position_side", "stop_price", "predicate"},
        {"reference_source", "reference_price"},
    ),
    "COLLISION_RESOLVED": (
        {
            "collision",
            "same_bar_collision_policy_id",
            "touched_exit_ids",
            "ordered_chosen_exit_ids",
            "reference_quantity",
            "stop_remainder_quantity",
        },
        {"target_ordering_rule", "tie_break_applied"},
    ),
    "FUNDING_ELIGIBILITY": (
        {"funding_event_id", "eligible", "position_snapshot_rule"}, set()
    ),
}

_DECISION_TIMESTAMP_REQUIRED = {
    "SIZING_COMPUTED",
    "MIN_NOTIONAL_ADMITTED",
    "REFUSED_MIN_NOTIONAL",
    "PROTECTIVE_STOP_EVALUATED",
    "COLLISION_RESOLVED",
    "FUNDING_ELIGIBILITY",
}


def _decision_value(value: object) -> Any:
    if type(value) in (int, float):
        return _json_number(value)
    if type(value) is tuple:
        return [_decision_value(member) for member in value]
    if type(value) is list:
        return [_decision_value(member) for member in value]
    return value


def _decision_surface(
    rows: list[object], *, kernel_semantics_version: str
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    semantics_emitted = False
    for row in rows:
        decision = getattr(row, "decision")
        if decision in _REMOVED_DECISIONS:
            continue
        if decision == "SEMANTICS_VALIDATED":
            if semantics_emitted:
                continue
            semantics_emitted = True
        if decision not in _DECISION_MEMBERS:
            raise ValueError(f"unknown corrected decision reason: {decision}")
        details = dict(getattr(row, "details"))
        required, optional = _DECISION_MEMBERS[decision]
        if required - set(details) or set(details) - required - optional:
            raise ValueError(f"invalid corrected decision members: {decision}")
        if decision == "PROTECTIVE_STOP_EVALUATED" and (
            ("reference_source" in details) != ("reference_price" in details)
        ):
            raise ValueError("protective-stop reference members must occur together")
        item: dict[str, Any] = {
            "sequence": len(result),
            "decision": decision,
            "kernel_semantics_version": kernel_semantics_version,
        }
        if decision in _DECISION_TIMESTAMP_REQUIRED:
            item["event_timestamp"] = _timestamp(getattr(row, "event_timestamp"))
        for name, value in details.items():
            item[name] = _decision_value(value)
        result.append(item)
    return result


def _fill_surface(
    rows: list[object], *, kernel_semantics_version: str
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for sequence, row in enumerate(rows):
        event_class = getattr(row, "event_class")
        price_tick_alignment = getattr(row, "price_tick_alignment")
        exit_id = getattr(row, "exit_id")
        fill_trigger = getattr(row, "fill_trigger")
        target_fraction = getattr(row, "target_fraction")
        reference_quantity = getattr(row, "reference_quantity")
        is_exit = event_class.endswith("EXIT")
        is_stop = event_class == "PROTECTIVE_STOP_EXIT"
        is_target = event_class == "TARGET_EXIT"
        if price_tick_alignment is None:
            raise ValueError("corrected fill requires price_tick_alignment")
        if is_exit != (exit_id is not None):
            raise ValueError("corrected exit-class fill requires only exit_id")
        if is_stop != (fill_trigger is not None):
            raise ValueError("corrected protective-stop fill requires only fill_trigger")
        if is_target != (
            target_fraction is not None and reference_quantity is not None
        ):
            raise ValueError("corrected target fill requires only target members")
        if not is_target and (
            target_fraction is not None or reference_quantity is not None
        ):
            raise ValueError("corrected non-target fill has target members")
        item: dict[str, Any] = {
            "sequence": sequence,
            "kernel_semantics_version": kernel_semantics_version,
            "fill_id": getattr(row, "fill_id"),
            "event_class": event_class,
            "side": getattr(row, "side"),
            "reference_price": _json_number(getattr(row, "reference_price")),
            "slippage_model_id": getattr(row, "slippage_model_id"),
            "slippage_bps": _json_number(getattr(row, "slippage_bps")),
            "slippage_impact": _json_number(getattr(row, "slippage_impact")),
            "slippage_application_count": getattr(row, "slippage_application_count"),
            "price_tick_alignment": price_tick_alignment,
            "final_fill_price": _json_number(getattr(row, "final_fill_price")),
            "quantity": _json_number(getattr(row, "quantity")),
            "liquidity_role": getattr(row, "liquidity_role"),
        }
        if is_exit:
            item["exit_id"] = exit_id
        if is_stop:
            item["fill_trigger"] = fill_trigger
        if is_target:
            item["target_fraction"] = _json_number(target_fraction)
            item["reference_quantity"] = _json_number(reference_quantity)
        result.append(item)
    return result


def _cash_surface(
    rows: list[object], *, kernel_semantics_version: str
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for sequence, row in enumerate(rows):
        item: dict[str, Any] = {
            "sequence": sequence,
            "kernel_semantics_version": kernel_semantics_version,
            "cash_event_id": getattr(row, "cash_event_id"),
            "kind": getattr(row, "kind").value,
            "signed_delta": _json_number(getattr(row, "signed_delta")),
        }
        for name in ("fill_id", "funding_event_id"):
            value = getattr(row, name)
            if value is not None:
                item[name] = value
        if getattr(row, "kind") is CashEventKind.FUNDING:
            item["lifecycle_id"] = getattr(row, "lifecycle_id")
        result.append(item)
    return result


def _fee_surface(
    rows: list[object], *, kernel_semantics_version: str
) -> list[dict[str, Any]]:
    numeric = {
        "rate",
        "fixed_component",
        "fee_notional",
        "fee_amount",
        "fee_cash_delta",
    }
    fields = (
        "lifecycle_id",
        "fill_id",
        "event_class",
        "liquidity_role",
        "schedule_id",
        "schedule_digest",
        "rate",
        "fixed_component",
        "fee_notional",
        "fee_amount",
        "fee_cash_delta",
        "settlement_currency",
        "cash_event_id",
    )
    result: list[dict[str, Any]] = []
    for sequence, row in enumerate(rows):
        item: dict[str, Any] = {
            "sequence": sequence,
            "kernel_semantics_version": kernel_semantics_version,
            "event_timestamp": _timestamp(getattr(row, "event_timestamp")),
        }
        for name in fields:
            value = getattr(row, name)
            item[name] = _json_number(value) if name in numeric else value
        result.append(item)
    return result


def _funding_surface(
    rows: list[object], *, kernel_semantics_version: str
) -> list[dict[str, Any]]:
    numeric = {
        "open_qty",
        "contract_multiplier",
        "mark_price",
        "raw_rate",
        "long_cashflow_rate",
        "notional",
        "funding_cash_delta",
        "cumulative_funding",
    }
    fields = (
        "funding_event_id",
        "lifecycle_id",
        "position_side",
        "open_qty",
        "contract_multiplier",
        "mark_price",
        "raw_rate",
        "positive_rate_payer",
        "long_cashflow_rate",
        "notional",
        "funding_cash_delta",
        "cumulative_funding",
        "schedule_id",
        "schedule_digest",
        "source_event_digest",
        "cash_event_id",
    )
    result: list[dict[str, Any]] = []
    for sequence, row in enumerate(rows):
        item: dict[str, Any] = {
            "sequence": sequence,
            "kernel_semantics_version": kernel_semantics_version,
            "event_timestamp": _timestamp(getattr(row, "event_timestamp")),
        }
        for name in fields:
            value = getattr(row, name)
            item[name] = _json_number(value) if name in numeric else value
        result.append(item)
    return result


def _joined_exit_fills(
    fills: list[object],
    cash_rows: Iterable[object],
) -> list[tuple[object, float]]:
    gross_by_fill = {
        getattr(row, "fill_id"): getattr(row, "signed_delta")
        for row in cash_rows
        if getattr(row, "kind") is CashEventKind.GROSS_REALIZATION
    }
    return [
        (row, gross_by_fill[getattr(row, "fill_id")])
        for row in fills
        if getattr(row, "fill_id") in gross_by_fill
    ]


def _exit_surface(
    exit_rows: list[tuple[object, float]],
    *,
    kernel_semantics_version: str,
) -> list[dict[str, Any]]:
    reason_by_class = {
        "PROTECTIVE_STOP_EXIT": "PROTECTIVE_STOP",
        "TARGET_EXIT": "TARGET",
        "MARKET_EXIT": "MARKET_EXIT",
    }
    result: list[dict[str, Any]] = []
    for row, gross_realized_pnl in exit_rows:
        fill_id = getattr(row, "fill_id")
        event_class = getattr(row, "event_class")
        item = {
            "sequence": len(result),
            "kernel_semantics_version": kernel_semantics_version,
            "exit_id": getattr(row, "exit_id") or event_class,
            "reason": reason_by_class.get(event_class, event_class),
            "fill_id": fill_id,
            "quantity": _json_number(getattr(row, "quantity")),
            "final_fill_price": _json_number(getattr(row, "final_fill_price")),
            "gross_realized_pnl": _json_number(gross_realized_pnl),
        }
        if event_class == "PROTECTIVE_STOP_EXIT":
            fill_trigger = getattr(row, "fill_trigger")
            if fill_trigger is None:
                raise ValueError("corrected protective-stop exit requires fill_trigger")
            item["fill_trigger"] = fill_trigger
        result.append(item)
    return result


def _closed_lifecycle_trades(
    state: PortfolioState,
    exit_rows: list[tuple[object, float]] | None = None,
) -> list[CorrectedTradeRecord]:
    entries: dict[int, list[object]] = {}
    exits: dict[int, list[object]] = {}
    for row in state.fill_events:
        if row.event_class.endswith("ENTRY"):
            entries.setdefault(row.lifecycle_id, []).append(row)
    if exit_rows is None:
        exit_rows = _joined_exit_fills(state.fill_events, state.cash_events)
    for row, _gross_realized_pnl in exit_rows:
        exits.setdefault(row.lifecycle_id, []).append(row)
    active_lifecycle = None if state.position is None else state.position.lifecycle_id
    trades: list[CorrectedTradeRecord] = []
    for lifecycle_id, entry_rows in entries.items():
        if lifecycle_id == active_lifecycle:
            continue
        exit_rows = exits.get(lifecycle_id, [])
        entry_qty = sum(float(row.quantity) for row in entry_rows)
        exit_qty = sum(float(row.quantity) for row in exit_rows)
        if not exit_rows or exit_qty < entry_qty:
            continue
        entry_fill_price = sum(
            float(row.final_fill_price) * float(row.quantity) for row in entry_rows
        ) / entry_qty
        gross = state.lifecycle_gross_pnl.get(lifecycle_id, 0.0)
        fee = state.lifecycle_fee_cash.get(lifecycle_id, 0.0)
        funding = state.lifecycle_funding_cash.get(lifecycle_id, 0.0)
        trades.append(
            CorrectedTradeRecord(
                entry_fill_price=entry_fill_price,
                quantity=entry_qty,
                exit_ids=[row.exit_id or row.event_class for row in exit_rows],
                gross_realized_pnl=gross,
                fee_total=fee,
                funding_total=funding,
                net_trade_pnl=gross + fee + funding,
            )
        )
    return trades


def _trade_surface(trades: list[CorrectedTradeRecord]) -> list[dict[str, Any]]:
    return [
        {
            "entry_fill_price": _json_number(trade.entry_fill_price),
            "quantity": _json_number(trade.quantity),
            "exit_ids": list(trade.exit_ids),
            "gross_realized_pnl": _json_number(trade.gross_realized_pnl),
            "fee_total": _json_number(trade.fee_total),
            "funding_total": _json_number(trade.funding_total),
            "net_trade_pnl": _json_number(trade.net_trade_pnl),
        }
        for trade in trades
    ]


def _warning_surface(
    warnings: Iterable[RunnerWarning | Mapping[str, Any]],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for warning in warnings:
        if isinstance(warning, RunnerWarning):
            result.append(dataclasses.asdict(warning))
        else:
            result.append(dict(warning))
    return result


def _detail_number(value: object) -> float | int | str:
    if type(value) in (int, float):
        return _json_number(value)
    if not isinstance(value, str):
        return str(value)
    try:
        number = float(value)
    except ValueError:
        return value
    return _json_number(number)


def _state_refusals(state: PortfolioState) -> list[dict[str, Any]]:
    refusals: list[dict[str, Any]] = []
    for row in state.decision_events:
        if row.refusal_code is None:
            continue
        details = dict(row.details)
        refusal: dict[str, Any] = {"code": row.refusal_code}
        if "order_notional" in details:
            refusal["order_notional"] = _detail_number(
                details["order_notional"]
            )
        if "required_min_notional" in details:
            refusal["required_min_notional"] = _detail_number(
                details["required_min_notional"]
            )
        if row.refusal_code == "REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION":
            required = {"field", "record_value", "runtime_value"}
            if required - set(details):
                raise ValueError("corrected override refusal requires closed detail members")
            refusal.update(
                field=str(details["field"]),
                record_value=_detail_number(details["record_value"]),
                runtime_value=_detail_number(details["runtime_value"]),
                stage="PRE_EVALUATION",
            )
        refusals.append(refusal)
    return refusals


def _guard_surface(guards: Mapping[str, Any]) -> dict[str, Any]:
    required = {
        "guard_pnl_basis",
        "consecutive_loss_count",
        "consec_loss_ok",
        "guard_blocked_raw",
    }
    optional = {"last_closed_guard_pnl"}
    names = set(guards)
    if required - names or names - required - optional:
        raise ValueError("invalid corrected guard members")
    if "last_closed_guard_pnl" in guards and guards["last_closed_guard_pnl"] is None:
        raise ValueError("last_closed_guard_pnl must be absent instead of null")
    return dict(guards)


def _realized_equity_window(
    state: PortfolioState,
    *,
    observation_start: datetime | None,
    observation_end: datetime | None,
) -> tuple[float, float] | None:
    if observation_start is None:
        return None
    first = state.initial_capital
    for row in state.cash_events:
        if row.event_timestamp < observation_start:
            first += float(row.signed_delta)
    last = first
    for row in _event_rows(
        state.cash_events,
        start=observation_start,
        end=observation_end,
    ):
        last += float(row.signed_delta)
    return first, last


def corrected_surfaces(
    *,
    state: PortfolioState,
    equity_values: list[float],
    manifest: CorrectedRunManifest,
    warnings: Iterable[RunnerWarning | Mapping[str, Any]] = (),
    refusals: Iterable[Mapping[str, Any]] | None = None,
    computed_guard_snapshot: Mapping[str, Any] | None = None,
    declared_def_ids: Iterable[str] = (),
    observation_start: datetime | None = None,
    observation_end: datetime | None = None,
    include_cumulative_funding: bool | None = None,
) -> dict[str, dict[str, Any]]:
    """Project corrected state into exact version-shaped event/result surfaces."""

    semantic_validation = next(
        (
            row
            for row in state.decision_events
            if row.decision == "SEMANTICS_VALIDATED"
        ),
        None,
    )
    decision_rows = (
        ([] if semantic_validation is None else [semantic_validation])
        + [
            row
            for row in _event_rows(
                state.decision_events, start=observation_start, end=observation_end
            )
            if row.decision != "SEMANTICS_VALIDATED"
        ]
    )
    fill_rows = _event_rows(
        state.fill_events, start=observation_start, end=observation_end
    )
    cash_rows = _event_rows(
        state.cash_events, start=observation_start, end=observation_end
    )
    fee_rows = _event_rows(
        state.fee_events, start=observation_start, end=observation_end
    )
    funding_rows = _event_rows(
        state.funding_events, start=observation_start, end=observation_end
    )
    exit_rows = _joined_exit_fills(fill_rows, cash_rows)
    event_surface = {
        "decision_events": _decision_surface(
            decision_rows,
            kernel_semantics_version=manifest.kernel_semantics_version,
        ),
        "fill_events": _fill_surface(
            fill_rows,
            kernel_semantics_version=manifest.kernel_semantics_version,
        ),
        "cash_events": _cash_surface(
            cash_rows,
            kernel_semantics_version=manifest.kernel_semantics_version,
        ),
        "fee_events": _fee_surface(
            fee_rows,
            kernel_semantics_version=manifest.kernel_semantics_version,
        ),
        "funding_events": _funding_surface(
            funding_rows,
            kernel_semantics_version=manifest.kernel_semantics_version,
        ),
        "exit_events": _exit_surface(
            exit_rows,
            kernel_semantics_version=manifest.kernel_semantics_version,
        ),
    }

    trades = _closed_lifecycle_trades(state, exit_rows)
    position = state.position
    result_surface: dict[str, Any] = {
        "final_position": (
            None
            if position is None
            else {
                "side": position.side.upper(),
                "quantity": _json_number(position.qty),
                "entry_fill_price": _json_number(position.avg_entry_price),
            }
        )
    }
    declared_defs = frozenset(declared_def_ids)
    if declared_defs.intersection({"DEF-P012-01", "DEF-P012-02", "DEF-P012-05"}):
        entry_fills = [
            row for row in state.fill_events if row.event_class.endswith("ENTRY")
        ]
        if entry_fills:
            last_entry = entry_fills[-1]
            result_surface["order_notional"] = _json_number(
                abs(
                    last_entry.final_fill_price
                    * last_entry.quantity
                    * state.instrument.contract_multiplier
                )
            )
        else:
            for decision in reversed(state.decision_events):
                details = dict(decision.details)
                if "order_notional" in details:
                    result_surface["order_notional"] = _detail_number(
                        details["order_notional"]
                    )
                    break
    realized_equity_window = _realized_equity_window(
        state,
        observation_start=observation_start,
        observation_end=observation_end,
    )
    if realized_equity_window is None:
        equity_first = equity_values[0] if equity_values else state.initial_capital
        equity_last = equity_values[-1] if equity_values else state.equity
    else:
        equity_first, equity_last = realized_equity_window
    result_surface.update(
        {
            "trades": _trade_surface(trades),
            "equity_curve": {
                "first": _json_number(equity_first),
                "last": _json_number(equity_last),
            },
        }
    )
    if include_cumulative_funding is None:
        include_cumulative_funding = bool(state.funding_events)
    if include_cumulative_funding:
        result_surface["cumulative_funding"] = _json_number(
            state.cumulative_funding
        )
    if "DEF-P012-07" in declared_defs:
        if computed_guard_snapshot is None:
            raise ValueError("declared guard projection requires a computed guard snapshot")
        result_surface["guards"] = _guard_surface(computed_guard_snapshot)
    if "DEF-P012-02" in declared_defs and any(
        row.decision == "MIN_NOTIONAL_ADMITTED" for row in state.decision_events
    ):
        result_surface["admitted"] = True
    result_surface.update(
        {
            "metrics": None,
            "warnings": _warning_surface(warnings),
            "refusals": (
                _state_refusals(state)
                if refusals is None
                else [dict(row) for row in refusals]
            ),
            "run_manifest": manifest.to_dict(),
        }
    )
    return {"EVENT_SURFACE": event_surface, "RESULT_SURFACE": result_surface}
