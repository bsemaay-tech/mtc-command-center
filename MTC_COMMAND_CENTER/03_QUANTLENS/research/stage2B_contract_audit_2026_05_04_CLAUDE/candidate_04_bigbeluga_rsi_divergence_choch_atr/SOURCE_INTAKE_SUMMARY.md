# SOURCE_INTAKE_SUMMARY — BigBeluga RSI Divergence + CHoCH + ATR

## Source files
- Canonical (per Codex `run_batch.py`): `06_QUANTLENS_LAB/00_INBOX_REPORTS/3 Mayıs/2026-05-03_XNZ4f-b3ED8_quantlens_intake_indicator_audit.md`
- AUDITED card incorrectly references `2026-05-03_NGyE4YIgGpU_...tito_adhikary_options_momentum_intake_report.md` (Tito = options; no BigBeluga indicator there).
- CLEAN card incorrectly references `-JyH5PAJ4-Y` (Nick Schmidt weekly).
- **Provenance contradiction across previous LLM outputs flagged.**

## Source URL
- https://youtu.be/XNZ4f-b3ED8 (review of "Market Structure Trend Matrix [BigBeluga]" indicator)

## Speaker / context
- Anonymous indicator-review video (UNKNOWN_CHANNEL) reviewing a free TradingView indicator by community publisher BigBeluga.
- The strategy logic is **the indicator's logic**, not a discretionary trader's framework.

## Native market
- TradingView indicator → asset-agnostic. Speaker mentions stocks, crypto, futures interchangeably in review style.

## Native timeframe
- Indicator is timeframe-agnostic. Speaker discusses 4h and 1D in examples.

## Indicator-stated rule (intake §3 + §4)
- Inputs: `msLen=10` (pivot left/right), `atrLength=14`, `atrMult=4.0`, `targetStepMult=2.0`.
- Pivots: `ph = ta.pivothigh(msLen, msLen)`, `pl = ta.pivotlow(msLen, msLen)` — **pivot confirmed only after `msLen=10` bars to the right** (10-bar detection lag).
- Bullish CHoCH: `ta.crossover(close, phVal) and not direction` → flip to bull.
- Bearish CHoCH: `ta.crossunder(close, plVal) and direction` → flip to bear.
- Trade idea: RSI divergence is the *early warning*; CHoCH is the *confirmation*. ATR(14) × 4 is the trailing stop. ATR ladder × 2 spacing is the target ladder.
- Initial stop = "divergence pattern high/low" (per intake summary).

## Intake's own warnings
- Pivot has 10-bar confirmation lag → any Python parity must model this.
- RSI-divergence definition is implementation-dependent in BigBeluga's Pine source (intake notes the indicator's behaviour differs slightly from the verbal explanation).
- No commission, slippage, symbol universe, or timeframe assumptions are given.
- Conditional accept; not ready for live without controlled backtests.
