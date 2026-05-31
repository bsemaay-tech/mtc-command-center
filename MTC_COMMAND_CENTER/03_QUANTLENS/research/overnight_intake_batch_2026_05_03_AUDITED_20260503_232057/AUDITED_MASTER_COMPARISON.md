# Audited Master Comparison

Independently audited from raw trades. PF/net/DD recomputed; first-run figures verified.

| rank | cand | family | horizon | TF | data | assets | trades | net% | PF_b | PF_2x | PF_3x | DD% | win% | top_share | flags | class | next |
|-----:|------|--------|---------|----|------|-------:|-------:|-----:|-----:|------:|------:|----:|----:|----------:|-------|-------|------|
| 1 | CANDIDATE_001 | Kell Wedge Pop / EMA Crossback | SWING | 1D | 5M_PROXY | 10 | 111 | 331.7517 | 1.7481 | 1.6786 | 1.6132 | -46.3269 | 31.53 | 0.324 | proxy | PASS_STAGE2 | Stage 2 robustness (parameter perturbation, regime |
| 2 | CANDIDATE_003 | Slingshot EMA(high,4) Pullback | SWING | 1D | 5M_PROXY | 10 | 1388 | 292669.9798 | 1.4581 | 1.3872 | 1.3207 | -86.417 | 38.11 | 0.13 | DD,proxy | WEAK_CANDIDATE | Stage 2 only after drawdown reduction / regime fil |
| 3 | CANDIDATE_005 | BigBeluga RSI/CHoCH/ATR | SWING | 1D | 5M_PROXY | 10 | 465 | 3955.225 | 1.4516 | 1.4236 | 1.3962 | -79.8493 | 46.67 | 0.112 | DD,proxy | WEAK_CANDIDATE | Stage 2 only after drawdown reduction / regime fil |
| 4 | CANDIDATE_002 | Martin Luke Pullback AVWAP | SWING | 1D | DAILY_PROXY | 10 | 584 | 17034.8144 | 1.4435 | 1.4078 | 1.3733 | -91.7686 | 31.85 | 0.137 | DD,proxy | WEAK_CANDIDATE | Stage 2 only after drawdown reduction / regime fil |
| 5 | CANDIDATE_007 | Linda 5SMA RS Pullback | SWING | 1D | 5M_PROXY | 10 | 687 | 1206.3069 | 1.3096 | 1.2609 | 1.2138 | -85.9357 | 63.03 | 0.138 | DD,proxy | WEAK_CANDIDATE | Stage 2 only after drawdown reduction / regime fil |
| 6 | CANDIDATE_004 | Crabel Range Expansion | SWING | 1D | 5M_PROXY | 10 | 8105 | 7179649232.748 | 1.251 | 1.1866 | 1.126 | -98.442 | 47.45 | 0.118 | DD,proxy | WEAK_CANDIDATE | Stage 2 only after drawdown reduction / regime fil |
| 7 | CANDIDATE_009 | HighBeta Opening-Bar Gap-and-G | DAY_TRADE | 5m | 5M_PROXY | 5 | 151 | 3.0885 | 1.0861 | 0.716 | 0.4825 | -7.1457 | 49.01 | 0.232 | cost,proxy | WEAK_CANDIDATE | Stage 2 only after drawdown reduction / regime fil |
| 8 | CANDIDATE_012 | EMA20/50 Two-Retest Baseline | SWING | 1D | 5M_PROXY | 10 | 135 | 738.7124 | 1.8741 | 1.8376 | 1.8023 | -82.1442 | 23.7 | 0.17 | DD,proxy | BASELINE_ONLY | use as benchmark only |
| 9 | CANDIDATE_008 | 8AM ET Opening Range Breakout | DAY_TRADE | 5m | 5M_PROXY | 5 | 4259 | -99.4805 | 0.5383 | 0.3067 | 0.1848 | -99.4799 | 34.14 | 0.2 | DD,cost,proxy | REJECT_NO_EDGE | do not test further — reject |
| 10 | CANDIDATE_011 | Daily Extension Anti-Chase Fil | FILTER | 1D | 5M_PROXY | 10 | 111 | -96.8928 | 0.5201 | 0.5031 | 0.4865 | -98.614 | 43.24 | 0.144 | DD,cost,proxy | REJECT_NO_EDGE | do not test further — reject |
| 11 | CANDIDATE_006 | CANSLIM Shakeout +3 | POSITION | 1D | DATA_BLOCKED | 0 | 0 |  |  |  |  |  |  |  | - | DATA_BLOCKED | acquire native data (US equity / microcap) |
| 12 | CANDIDATE_010 | Ty Rajnus Microcap Short | DAY_TRADE | 1m | DATA_BLOCKED | 0 | 0 |  |  |  |  |  |  |  | - | DATA_BLOCKED | acquire native data (US equity / microcap) |