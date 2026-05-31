# Pine Parity Plan — QL_ALPHA_LTC_RSI_OVERSOLD_1H

> Parity work is **DEFERRED** for this candidate (weak fold consistency 1/3, thin PF 1.23). This plan documents the path for IF/WHEN forward paper-trade improves the profile. **Do not modify production `MTC_V2.pine`.**

## Source of truth
- **Python reference = `tools/mega_walk_forward.py` → `build_signals("GEN_RSI_OVERSOLD_REVERSAL", ...)` + `simulate_slice`.**

## Producer logic to implement in Pine v6 (when un-deferred)
- `rsi5 = ta.rsi(close, 5)`.
- `longEntry = rsi5[1] < 35 and rsi5 >= 45`.
- Entry next bar open. Stop = `ta.lowest(low, 5)`. Target = entry + 2*(entry−stop).
- Exit: target / stop / 96-bar time exit. **No trend filter** (keep parity with engine; do not silently add one).

## Strict bar-close confirmation
- RSI must be computed on **closed bars only**; the `rsi5[1] < 35` condition references the prior closed bar.
- Pine: `calc_on_every_tick=false`, evaluate on `barstate.isconfirmed`. This is critical because fast RSI(5) is volatile intrabar and would repaint if evaluated on live ticks.

## Signal columns to export (Python and Pine)
- `timestamp_utc`, `long_entry(bool)`, `rsi5`, `stop_price`, `target_price`, `exit_flag(target|stop|time)`.

## Timestamp comparison & tolerances
- Align on bar `timestamp_utc` (UTC open time).
- `rsi5` relative tol ≤ 1e-4 (verify Pine `ta.rsi` matches Wilder ewm alpha=1/5).
- Entry-flag agreement ≥ 99%; entry/exit bar index exact (1-bar tolerance on spot-check).

## No-lookahead / HTF
- No HTF / `request.security` → no HTF repaint risk.
- Main risk is **intrabar RSI repaint** → mandatory bar-close confirmation (above).

## Parity acceptance criteria
- ≥ 99% entry-flag agreement over full LTC 1h history AND matching trade list within 1-bar tolerance on spot-check.
- Parity is NOT to be started until this candidate is un-deferred by forward paper-trade results.
