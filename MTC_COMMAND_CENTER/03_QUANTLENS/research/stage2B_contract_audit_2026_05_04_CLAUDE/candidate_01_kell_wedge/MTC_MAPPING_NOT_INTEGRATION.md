# MTC_MAPPING_NOT_INTEGRATION — Kell Wedge Pop

## MTC role
**SIGNAL_PRODUCER_POSSIBLE** (with caveats).

## Producer raw signal definition (research-only)
`raw_kell_wedge_pop_long = preflush_in_30bars AND snapback_seen AND higher_low_confirmed AND contraction_5_30 AND close>EMA10 AND close>EMA20 AND close>mini_base_high`

## Non-repaint requirements
- `pre_flush`, `snapback`, `higher_low` all evaluated only with right-side confirmed pivots → use `shift(right_bars)` so the producer never references future bars.
- Trigger evaluated on bar close; entry next bar open.

## Timeframe requirements
- Native trade idea TF: **1D**.
- Context gate TF: **1W** (weekly EMA10 slope) — MTC must have working HTF gate.
- Execution refinement TF: optional 30m / 65m.

## Stateful transform needed
- `flush_active` flag (latched until snapback OR expired after 30 bars).
- `snapback_seen` flag (latched until higher_low OR expired).
- `higher_low_confirmed` flag (latched for contraction window).
- `contraction_window_bars_remaining` counter.
This is a 4-state FSM — NOT a stateless rule.

## Filters needed (on top of producer)
- RS-rank gate (top decile vs SPY 60d).
- Macro gate (SPY > EMA200).
- Earnings blackout.

## MTC SL/TP compatibility
- Initial SL = price level (mini_base_low / higher_low − 0.25 ATR). Direct fit for MTC stop owner.
- TP = none fixed; uses **trailing exit on EMA**. MTC must support MA-trail with switching trail-MA mid-trade.
- Time stop = 5-bar exit if no follow-through. Compatible.

## Likely UI complexity
- High. FSM state visible in pane; trail-MA switch needs tooltip; theme-leader filter needs external table.

## Parity risks
- Strategy is multi-step pivot-state machine. Pine implementation must replay the FSM identically to Python; off-by-one on swing pivot confirmation is the main parity bug to expect.
- DO NOT integrate to MTC_V2.pine until Python prototype has clean US-equity walk-forward proof.
