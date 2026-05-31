# Parity Reproducibility Policy

This document defines reproducible TradingView <-> Python parity conditions.

## Scope
- Engine behavior is lock-governed by `06_ENGINE_LOCK_PROTOCOL.md`.
- This policy only defines settings and comparison workflow.

## Required Run Profile
- Use a `parity_profile_<name>.json` file under `configs/cases/`.
- Use matching dataset, timeframe, date window, and strategy properties.

## TV Backtesting Policy
- Bar Magnifier: **OFF** (default parity mode).
- Deep Backtesting: **OFF** (default parity mode).
- Recalculate on every tick/order fills: **OFF** unless explicitly tested with equivalent Python policy.

Reason:
- Python engine runs deterministic bar-level logic in parity mode.
- Intrabar emulation differences can introduce non-contract mismatches.

## Differential Debug Workflow
1. Export TV trades CSV.
2. Run Python with debug export enabled.
3. Compare:
   - `python -m src.parity.compare_tv_trades --tv <tv.csv> --py <debug_python_trades.csv> --tv-tz Europe/London --out <report.csv>`
4. Find first mismatch:
   - `python scripts/first_divergence_finder.py --report <report.csv>`

## Interpretation Rules
- If first mismatch occurs before Python eval window start: treat as run-window/config mismatch.
- If mismatch appears after window alignment and profile lock: investigate known limitations and data-feed differences first.
- Only escalate as engine issue if profile and policy are fully matched and divergence remains unexplained.
