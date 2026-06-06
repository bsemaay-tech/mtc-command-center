# Strategy Code Review Checklist (permanent)

Run before marking any strategy/variant `code_safety_status: PASS`. Covers Python
backtest code and Pine⇄Python conversions. Record PASS/FAIL + notes in the
variant log and final report.

## Repaint / lookahead / leakage
- [ ] **Repaint**: signals computed on the **closed** bar; no use of the forming bar.
- [ ] **Lookahead**: rolling windows shifted (`[1]`) so the level excludes the
      current bar; no `max/min` over a window that includes the signal bar.
- [ ] **Future data leakage**: no train/test contamination; OOS truly out-of-sample;
      no normalization/scaling fit on the full series.
- [ ] **HTF data**: higher-timeframe values are only available after the HTF bar
      closes (no intrabar HTF peeking); align HTF→LTF with proper shift.

## Execution assumptions
- [ ] **Candle close**: entries/exits decided on bar close.
- [ ] **Order execution**: filled at **next bar open** (not signal-bar close).
- [ ] **Same-bar entry/exit**: avoided, or modeled conservatively if unavoidable.
- [ ] **Commission**: applied per round trip, realistic bps.
- [ ] **Slippage**: modeled (ticks or %), not zero.

## Position & risk modules
- [ ] **Position sizing**: capital math correct; no >100% exposure unless intended.
- [ ] **Stop-loss**: placed and triggered correctly (intrabar vs close).
- [ ] **Take-profit**: target math correct (R multiples, levels).
- [ ] **Trailing stop**: ratchets monotonically; no look-back tightening cheat.
- [ ] **Portfolio allocation**: weights sum correctly; no double-counting capital.

## TradingView parity
- [ ] **TV mismatch risk**: indicator implementations match Pine (RMA/Wilder vs SMA, etc.).
- [ ] **Python→Pine** conversion: series indexing, `na` handling, `barstate` semantics.
- [ ] **Pine→Python** conversion: `[1]` offsets, `request.security` lookahead flags,
      session/timezone handling for intraday.

## Sanity
- [ ] Trade count is large enough to be meaningful (small-sample caveat noted).
- [ ] Results reproduce on re-run (deterministic seed / no hidden state).
- [ ] B&H baseline + alpha reported (per backtest rules).

See also: `_AI_MEMORY/REVIEW_CHECKLIST.md` (general code review).
