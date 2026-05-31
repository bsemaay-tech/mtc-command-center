# Pine Parity Plan — QL_ALPHA_ADA_TWO_CANDLE_SR_1H

> REVIEW-only Pine v6 that reproduces the Python reference. **Do not modify production `MTC_V2.pine`.**

## Source of truth
- **Python reference = `tools/mega_walk_forward.py` → `build_signals("QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR", ...)` + `simulate_slice`.**
- Match this reference, not the original video, until source fidelity confirmed.

## Producer logic to implement in Pine v6
- `highBreak = ta.highest(high, 200)[1]`.
- `pos = (close - low) / (high - low)`.
- `longEntry = pos >= 0.6 and close > high[1] and close > highBreak` (break_buf = 0).
- Entry next bar open. Stop = `ta.lowest(low, 2)` at signal bar. Target = entry + 2*(entry−stop).
- Exit: target hit (intrabar high ≥ target), or stop (intrabar low ≤ stop), or 96-bar time exit.

## Special focus — candle confirmation & no-repaint
- The breakout level uses `[1]` (excludes current bar) → the resistance is fixed at bar close, **no repaint**.
- `pos` uses only the current closed bar's OHLC → deterministic at close.
- Confirm Pine evaluates on confirmed bars; `calc_on_every_tick=false` for parity runs.

## Signal columns to export (Python and Pine)
- `timestamp_utc`, `long_entry(bool)`, `stop_price`, `target_price`, `exit_flag(target|stop|time)`, `high_break`, `pos`.

## Timestamp comparison & tolerances
- Align on bar `timestamp_utc` (UTC open time).
- Indicators (high_break, pos): relative tol ≤ 1e-4.
- Entry-flag agreement ≥ 99%; entry/exit bar index exact (1-bar tolerance on spot-check).

## No-lookahead / HTF
- No HTF / `request.security` → no HTF repaint risk.
- No intrabar/tick dependency for the signal.

## Parity acceptance criteria
- ≥ 99% entry-flag agreement over full ADA 1h history AND matching trade list within 1-bar tolerance on a spot-check window.
- Until met: status stays `PROMOTE_TO_PARITY_CANDIDATE` (parity NOT complete).

## Acceptance log
- 2026-05-30: **Pine v6 server compile = PASS** (0 errors / 0 warnings via TradingView `pine_check`). Python reference VERIFIED.
  Chart-based trade parity PENDING — TradingView Desktop not installed in this environment (see `../PARITY_RESULTS.md`).
