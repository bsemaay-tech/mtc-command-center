# Contract Used By Code - BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR

This is the mechanical contract audited by Codex Stage-2B. It is derived from the previous local reports and the previous Python implementation, not from TradingView or Pine.

## Rules
- 1. RSI divergence
- 2. CHoCH structure break
- 3. ATR stop
- 4. pivot delay
- 5. long/short reversal support

## Execution Contract Used For Repair
- Signals are confirmed on completed bars.
- Entry is next-bar open unless the original contract explicitly defines a stop-trigger fill.
- Exit-first ordering is required when a position exists.
- Same-bar SL/TP conflict is deterministic stop-first in this verification harness.
- Costs are explicit and net return is recomputed from trade_trace.csv.
- Crypto proxy rows are never treated as native US equity proof.
