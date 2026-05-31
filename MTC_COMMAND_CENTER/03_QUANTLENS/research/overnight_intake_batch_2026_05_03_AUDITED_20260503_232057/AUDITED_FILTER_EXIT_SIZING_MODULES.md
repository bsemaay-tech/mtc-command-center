# Audited Filter / Exit / Sizing Modules

## Filter candidates
- **CANDIDATE_011 Daily Extension Anti-Chase Filter** — rejected as standalone (PF 0.52, DD 99%) but has plausible *filter* utility. Recommended next test: apply as a veto over CANDIDATE_001's trade set and measure DD/PF delta.

## Exit / SL / TP / trailing modules
- No standalone exit module is promoted tonight. ATR/time-stop logic in CANDIDATE_001/003/005 should be parameterized and tested in a shared exit harness during Stage 2.

## Sizing modules
- Progressive Exposure (mentioned across Minervini/poker-trader intakes) is a **risk module concept** — needs an isolated Python implementation that takes a base trade stream and rescales risk by recent equity slope. Not tested here; document as Stage-2 follow-up.
