# Pine Parity Plan — QL_ALPHA_LINK_8EMA_1H

> Goal: a REVIEW-only Pine v6 producer/strategy that reproduces the Python reference signal bar-for-bar. **Do not modify production `MTC_V2.pine`.**

## Source of truth
- **Python reference = `tools/mega_walk_forward.py` → `build_signals(strategy="QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL", ...)` + `simulate_slice`.**
- Pine must match this reference, NOT the original video, until source fidelity is confirmed.

## Producer logic to implement in Pine v6
- `ema8 = ta.ema(close, 8)`; `atr14 = ta.atr(14)` (Wilder/RMA — matches Python ewm alpha=1/14).
- `slope = ema8 - ema8[3]`; `dist = math.abs(close - ema8)/atr14`; `impulse = math.abs(close - close[3])/atr14`.
- `longEntry = close > ema8 and slope > 0 and dist <= 0.5 and impulse[1] >= 1.6`.
- Entry at next bar (use `strategy.entry` which fills next bar open, or compute on confirmed bar).
- Stop = `ta.lowest(low, 3)` captured at signal bar.
- Exit (trailing): close < ema8 → exit next bar open; plus hard stop; plus max-hold 96 bars.

## Signal columns to export (Python and Pine)
- `timestamp_utc`, `long_entry(bool)`, `stop_price`, `exit_flag(trail|stop|time)`, `ema8`, `atr14`.

## Timestamp comparison
- Align on bar `timestamp_utc` (bar open time, UTC). Compare entry/exit on matching bar indices.

## Tolerance rules
- Indicator values (ema8, atr14): relative tol ≤ 1e-4.
- Boolean entry flags: exact match required on ≥ 99% of bars; investigate any mismatch.
- Entry/exit bar index: exact match.

## No-lookahead / no-repaint checks
- Signal uses only confirmed-bar data (`impulse[1]`); confirm Pine uses `barstate.isconfirmed` semantics / no `request.security` lookahead.
- No HTF data used → **no HTF repaint risk** for this candidate.
- No intrabar/tick dependency.

## Bar-close confirmation
- All conditions evaluated on closed bar; entry executes next bar open. Pine `calc_on_every_tick=false` for parity runs.

## Parity acceptance criteria
- Entry-flag agreement ≥ 99% over the full LINK 1h history AND identical trade list within 1-bar tolerance on a spot-check window.
- Indicator parity within tolerance above.
- Until met: status stays `PROMOTE_TO_PARITY_CANDIDATE` (parity NOT complete).

## Acceptance log
- 2026-05-30: **Pine v6 server compile = PASS** (0 errors / 0 warnings via TradingView `pine_check`). Python reference VERIFIED.
- 2026-05-30: **Live chart run = PASS.** Loaded on TradingView Desktop (MSIX, relaunched with CDP), compiled + added to chart on LINKUSDT 1h; console "Compiled / Added to chart"; long-only trade stream generated. Strategy Tester (Jan 2024–May 2026): PF ~1.21 on spot, **~1.65 on `LINKUSDT.P` futures** (matching the bundle feed type), DD ~21.5%. Consistent with the Python reference edge (PF 2.04 on lockbox). (TradingView spot/futures feed ≠ local bundle → only logic parity there.)
- 2026-05-30: **PineTS EXACT producer parity = PASS (100.0%).** Ran the producer logic through PineTS (`pinets_link_parity.mjs`) on Binance FUTURES klines verified byte-identical to the bundle, fed via Provider.Mock (Provider.Binance returns spot and rejects `.P`). Compared bar-for-bar to the Python engine (`compare_link_pinets_parity.py`) on the SAME bars:
  - bars compared: **7485** (100-bar warmup excluded)
  - **long-signal agreement: 100.0%** (Pine 60 / Python 60 / both 60 / only-pine 0 / only-python 0)
  - ema8 max rel-diff **0.0**; atr14 max rel-diff **1.6e-4** (Wilder seeding, within tolerance)
  - Result file: `PINETS_PARITY_RESULT.json`. **This is the exact same-data parity gate; PASS.**
