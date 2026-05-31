# Rerun Plan

Audit found **no metric corruption** requiring rerun. All 10 strategies' trades reproduce reported metrics within rounding.
Therefore no rerun was performed in this audit pass. Stage 2 robustness reruns are deferred to the next prompt.

If first-run had been corrupted, the rerun targets would have been (in order):
1. CANDIDATE_001 Kell Wedge — top PASS_STAGE2 candidate.
2. CANDIDATE_005 BigBeluga RSI — best fee-stress profile among WEAKs (3x PF still 1.40).
3. CANDIDATE_004 Crabel — to verify the 98% DD is reproducible under audited cost model.
