from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "00_PYTHON"))
sys.path.insert(0, str(ROOT))

from mtc_v2.core.config import DEFAULT_CONFIG, validate_config
from mtc_v2.core.results import BacktestResult, EquityPoint, RunnerWarning, TradeRecord, metrics_from_trades
from mtc_v2.core.runner import Runner
from mtc_v2.core.types import Bar


RUNNER_METRICS_ADAPTER_VERSION = "runner_metrics_adapter_v1"


def stable_hash(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def run_with_result(
    bars: Iterable[Bar],
    *,
    config_overrides: dict[str, Any] | None = None,
    dataset_hash: str | None = None,
    dataset_id: str | None = None,
    run_id: str | None = None,
    raw_artifact_paths: dict[str, str] | None = None,
) -> BacktestResult:
    config = dict(DEFAULT_CONFIG)
    config.update(config_overrides or {})
    validate_config(config)
    runner = Runner(config)
    bar_list = list(bars)
    bar_times = {bar.bar_index: bar.timestamp for bar in bar_list}
    equity_curve = [EquityPoint(bar_index=None, timestamp=None, equity=float(config["initial_capital"]))]
    trades: list[TradeRecord] = []
    exposure_bars = 0
    warnings: list[RunnerWarning] = [
        RunnerWarning(
            "ADAPTER_API",
            "Metrics were collected through tools.runner_metrics_adapter without changing Runner strategy behavior.",
        )
    ]
    for bar in bar_list:
        position_before = runner.state.position
        if position_before is not None:
            exposure_bars += 1
        runner.run([bar])
        for event_index, event in enumerate(runner.state.exit_events_this_bar, start=1):
            entry_price = position_before.avg_entry_price if position_before is not None else None
            entry_bar = position_before.entry_bar if position_before is not None else None
            entry_time = bar_times.get(entry_bar) if entry_bar is not None else None
            pnl_pct = None
            if entry_price and event.exit_qty:
                notional = abs(entry_price * event.exit_qty)
                pnl_pct = (event.realized_pnl / notional) * 100.0 if notional else None
            trades.append(
                TradeRecord(
                    trade_id=f"trade_{len(trades) + 1:06d}_{event_index}",
                    side=position_before.side if position_before is not None else None,
                    entry_time=entry_time,
                    exit_time=bar.timestamp,
                    entry_price=entry_price,
                    exit_price=event.exit_price,
                    qty=event.exit_qty,
                    pnl=event.realized_pnl,
                    pnl_pct=pnl_pct,
                    exit_reason=event.exit_reason,
                    bars_held=(bar.bar_index - entry_bar) if entry_bar is not None else None,
                )
            )
        equity_curve.append(EquityPoint(bar_index=bar.bar_index, timestamp=bar.timestamp, equity=float(runner.state.equity)))

    metrics = metrics_from_trades(
        trades,
        [point.equity for point in equity_curve],
        initial_capital=float(config["initial_capital"]),
        exposure_bars=exposure_bars,
    )
    warnings.extend(metrics.warnings)
    return BacktestResult(
        metrics=metrics,
        trades=trades,
        equity_curve=equity_curve,
        config_hash=stable_hash(config),
        dataset_hash=dataset_hash,
        dataset_id=dataset_id,
        run_id=run_id,
        warnings=warnings,
        raw_artifact_paths=raw_artifact_paths or {},
    )
