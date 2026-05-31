# candidate_contract_verdict — Kell Wedge Pop

## Verdict
**PREVIOUS_BACKTEST_NOT_FAIR** + **CONTRACT_NEEDS_NATIVE_DATA**

(Compatible with `CONTRACT_READY_FOR_CODEX_RETEST` once US equity data + RS rank + earnings calendar acquired.)

## Rationale
- Codex's `signal_kell()` dropped every cycle precondition (flush, snapback, higher-low, contraction-vs-context) and reduced the strategy to a 5-bar Donchian breakout with EMA20 gate.
- Backtest was on BTC/ETH/SOL/BNB/XRP — wrong asset class for an equity-leader strategy.
- Stage-2 weak metrics measure the degraded breakout proxy, NOT Kell's actual edge.
- The contract IS mechanically codable (with proxies for leadership) but is **not testable on current crypto-only bundle**.

## Recommended next action
1. Acquire US equity daily OHLCV + SPY + earnings calendar.
2. Implement the FSM in `CODING_REQUIREMENTS_FOR_CODEX.md`.
3. Walk-forward 5-year windows, with side-by-side baseline.
4. Only after that, decide producer vs filter vs reject.

## Killshot conditions
Reject IF (after fair test):
- Cycle preconditions add no R-expectancy lift over Donchian+EMA baseline on US equity universe.
- Trade count too low to be useful in any walk-forward window.
- Edge concentrated in <3 mega-leaders (survivorship).
