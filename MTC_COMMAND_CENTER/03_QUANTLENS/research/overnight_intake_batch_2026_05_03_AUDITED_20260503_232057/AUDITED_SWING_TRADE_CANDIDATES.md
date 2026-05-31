# Audited Swing-Trade Candidates

Swing tests run on 1D resampled crypto futures across 10 assets.
Drawdowns over 70% in most cases — Stage 2 robustness (regime filter, drawdown-cap, walk-forward) required before any further promotion.

| rank | cand | family | data | assets | PF_b | PF_2x | PF_3x | DD% | class | next action |
|-----:|------|--------|------|-------:|-----:|------:|------:|----:|-------|-------------|
| 1 | CANDIDATE_001 | Kell Wedge Pop / EMA Crossback | 5M_PROXY | 10 | 1.7481 | 1.6786 | 1.6132 | -46.3269 | PASS_STAGE2 | Stage 2 robustness (parameter perturbation, regime split, wa |
| 2 | CANDIDATE_003 | Slingshot EMA(high,4) Pullback | 5M_PROXY | 10 | 1.4581 | 1.3872 | 1.3207 | -86.417 | WEAK_CANDIDATE | Stage 2 only after drawdown reduction / regime filter / nati |
| 3 | CANDIDATE_005 | BigBeluga RSI/CHoCH/ATR | 5M_PROXY | 10 | 1.4516 | 1.4236 | 1.3962 | -79.8493 | WEAK_CANDIDATE | Stage 2 only after drawdown reduction / regime filter / nati |
| 4 | CANDIDATE_002 | Martin Luke Pullback AVWAP | DAILY_PROXY | 10 | 1.4435 | 1.4078 | 1.3733 | -91.7686 | WEAK_CANDIDATE | Stage 2 only after drawdown reduction / regime filter / nati |
| 5 | CANDIDATE_007 | Linda 5SMA RS Pullback | 5M_PROXY | 10 | 1.3096 | 1.2609 | 1.2138 | -85.9357 | WEAK_CANDIDATE | Stage 2 only after drawdown reduction / regime filter / nati |
| 6 | CANDIDATE_004 | Crabel Range Expansion | 5M_PROXY | 10 | 1.251 | 1.1866 | 1.126 | -98.442 | WEAK_CANDIDATE | Stage 2 only after drawdown reduction / regime filter / nati |
| 8 | CANDIDATE_012 | EMA20/50 Two-Retest Baseline | 5M_PROXY | 10 | 1.8741 | 1.8376 | 1.8023 | -82.1442 | BASELINE_ONLY | use as benchmark only |