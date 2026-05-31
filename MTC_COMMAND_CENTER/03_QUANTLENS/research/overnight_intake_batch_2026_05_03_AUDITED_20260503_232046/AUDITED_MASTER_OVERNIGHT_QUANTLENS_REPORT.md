# AUDITED MASTER OVERNIGHT QUANTLENS REPORT

## 1. Executive Verdict
The first-run overnight research extracted 87 candidates but failed in priority scoring and had a minor backtest gap fill logic bug. The audit has repaired the extraction, recomputed the priority matrix, and adjusted the day-trade prototype backtest. There are NO Pine-ready or MTC producer-ready strategies yet.

## 2. First-Run Reliability Verdict
**Partially Reliable.** The inventory and data discovery was correct, but extraction of metadata tags (priority/verdict) failed. The backtest was slightly optimistic due to gap assumptions.

## 3. Input Coverage
- Valid Intakes: 74
- Extracted Candidates: 87

## 8. Corrected Strategy Ranking
1. LBR Coil Breakout (Day Trade)
2. Charles Harris 50DMA Pullback (Swing)
3. Stan Weinstein Stage Analysis (Swing)

## 14. Stage 2 Recommendation
Run Stage 2 optimization for `QL_LBR_COIL_BREAKOUT_RANGE_EXPANSION_v0` to test limit entries vs stop entries to mitigate slippage.

## 15. MTC/Pine Recommendation
Do not integrate. Need Stage 2 results first.

## 21. Recommended Next Codex Prompt
"Take QL_LBR_COIL_BREAKOUT_RANGE_EXPANSION_v0, implement a limit-order-only variant for 5m crypto, and run a rigorous Stage 2 fee stress optimization on 17 assets."
