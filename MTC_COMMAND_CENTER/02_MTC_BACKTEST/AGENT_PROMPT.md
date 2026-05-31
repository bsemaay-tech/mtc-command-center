# MTC Backtester — Agent Workflow Guide

## Quick Start (2 commands)

```bash
cd C:\LAB\tradingview-lab\mtc_backtest

# 1. Run backtest
python scripts/run_case.py configs/cases/dec2025_parity.json

# 2. Compare with TradingView
python scripts/compare_tv.py configs/cases/dec2025_parity.json
```

## What This Does

- `run_case.py` reads a JSON config, runs the Python backtest engine, prints metrics + exports debug CSVs.
- `compare_tv.py` auto-detects the latest Python debug CSV and compares it trade-by-trade against the TradingView CSV.

## Agent Rules

1. **Create a new git branch** before making changes: `git checkout -b parity/<short_desc>`
2. **Only edit** code under `src/` and configs under `configs/cases/`.
3. **Never edit** data files or TV CSVs.
4. After every code change: `git diff` to show what changed.
5. Run the 2-command pipeline and paste the comparison output.
6. Stop when mismatches reduce; summarize root cause + next patch.

## Current Status

- **TradingView**: 60 closed + 1 open = 61 trades
- **Python**: 46 trades (24 unique entries x ~2 pyramid legs)
- **Gap**: 15 trades missing in Python
- **Main issues**: Entry timing differs by 15-75min on early December trades due to Supertrend band convergence differences

## File Structure

```
mtc_backtest/
  configs/cases/           <- JSON case files (agent edits these)
    dec2025_parity.json    <- Dec 2025 BTCUSDT parity case
  scripts/
    run_case.py            <- CLI backtest runner
    compare_tv.py          <- TV vs Python parity comparison
  src/
    config/defaults.py     <- MTCConfig Pydantic model
    engine/mtc_runner.py   <- Main backtest engine (bar-by-bar loop)
    engine/mtc_state.py    <- Position/trade state management
    engine/indicators.py   <- ATR, RMA, Supertrend calculations
    modules/signals/       <- Signal plugins (Supertrend)
    modules/filters/       <- Filter chain (MA, Volume, ATR Vol)
    modules/risk/          <- Position sizing, SL/TP calculators
  data/                    <- Parquet/CSV datasets (DO NOT EDIT)
  debug/                   <- Debug CSV output directory
```

## Key Config Parameters (dec2025_parity.json)

| Parameter | Value | Purpose |
|-----------|-------|---------|
| preroll_days | 90 | Indicator warmup before trading starts |
| warmup_bars | 200 | Minimum bars before any signal processing |
| pyramiding | 2 | Max concurrent positions per direction |
| fill_contract | touch | OHLC touch-based exit detection |
| close_open_at_end | false | Leave open positions open (TV parity) |

## Parity Debug Columns (debug_python_signals CSV)

New columns added for debugging:
- `pos_side`: LONG / SHORT / FLAT
- `open_legs`: Number of open pyramid legs
- `entry_price`: Current position entry price
- `sl_price`: Current stop loss price
- `be_triggered`: Whether break-even has been triggered
- `trailing_active`: Whether trailing stop is active
- `can_trade`: Whether trade_start gate allows trading (false during preroll)
