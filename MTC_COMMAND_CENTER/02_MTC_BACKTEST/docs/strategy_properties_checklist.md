# Strategy Properties Checklist (TV <-> Python)

Use this checklist before calling a run "parity mismatch".

## Instrument / Data
- Symbol/exchange/contract are identical (example: `BTCUSDT.P` / Binance Perp).
- Timeframe matches exactly (example: `15m`).
- Candle source/type is consistent.
- Time window matches exactly (`start_date`, `end_date`).
- Timezone interpretation is consistent (`Europe/London` for TV export parsing, UTC internally in Python).

## TradingView Strategy Properties
- Initial capital matches Python config.
- Order size / position sizing mode matches.
- Commission percent matches.
- Slippage ticks matches.
- Pyramiding value matches.
- Margin / leverage assumptions match.

## TradingView Backtest Toggles
- Bar Magnifier policy is respected (default parity mode: OFF).
- Deep Backtesting policy is respected (default parity mode: OFF).
- Recalculate toggles (`calc_on_every_tick`, `calc_on_order_fills`) align with parity policy.

## Python / Web Inputs
- `warmup_bars` matches parity case.
- `preroll_days` matches parity case.
- `strategy.pyramiding` matches TV.
- `trade.max_pyramid_positions` matches TV/Pine input.
- `trade.signal_mode_max_entries` matches TV/Pine input.

## Execution / Fill Contract
- Same fill contract mode (`touch` vs `close`).
- Same-bar behavior expectations are aligned with engine contract.
- Partial TP / trailing / BE enablement matches.

## Required Exports for Differential Debug
- TV trades export CSV.
- Python `debug_python_trades_*.csv`.
- Python `debug_python_signals_*.csv`.

## Pass Criteria
- Trade count converges (or differences explained by declared policy).
- First divergence (if any) is attributable to known setting/data policy, not unknown behavior.
