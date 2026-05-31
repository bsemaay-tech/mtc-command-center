# MTC V2 Readiness Audit

Mapping each audited candidate to its MTC role. **No candidate is ready for direct MTC integration tonight.**

| candidate | audit_class | MTC role | required Stage 2 / pre-integration tests |
|-----------|-------------|----------|------------------------------------------|
| CANDIDATE_001 | PASS_STAGE2 | MTC_SIGNAL_PRODUCER_POSSIBLE_LATER | walk-forward, parameter perturbation, regime split, MTC SL/TP/trailing harness, parity vs Pine |
| CANDIDATE_003 | WEAK_CANDIDATE | MTC_SIGNAL_PRODUCER_NOT_READY | drawdown reduction, regime filter, native data acquisition, then full Stage 2 |
| CANDIDATE_005 | WEAK_CANDIDATE | MTC_SIGNAL_PRODUCER_NOT_READY | drawdown reduction, regime filter, native data acquisition, then full Stage 2 |
| CANDIDATE_002 | WEAK_CANDIDATE | MTC_SIGNAL_PRODUCER_NOT_READY | drawdown reduction, regime filter, native data acquisition, then full Stage 2 |
| CANDIDATE_007 | WEAK_CANDIDATE | MTC_SIGNAL_PRODUCER_NOT_READY | drawdown reduction, regime filter, native data acquisition, then full Stage 2 |
| CANDIDATE_004 | WEAK_CANDIDATE | MTC_SIGNAL_PRODUCER_NOT_READY | drawdown reduction, regime filter, native data acquisition, then full Stage 2 |
| CANDIDATE_009 | WEAK_CANDIDATE | MTC_SIGNAL_PRODUCER_NOT_READY | drawdown reduction, regime filter, native data acquisition, then full Stage 2 |
| CANDIDATE_012 | BASELINE_ONLY | NOT_MTC_RELEVANT (benchmark only) | treat as benchmark, do not promote |
| CANDIDATE_008 | REJECT_NO_EDGE | NOT_MTC_RELEVANT | do not retest |
| CANDIDATE_011 | REJECT_NO_EDGE | MTC_FILTER_ONLY (currently rejected as standalone — re-test as filter overlay only) | apply over an existing producer's trade set; check whether DD reduces without killing edge |
| CANDIDATE_006 | DATA_BLOCKED | MTC_POSITION_TRADING_OUTSIDE_CORE | acquire native data first; do not run on proxy |
| CANDIDATE_010 | DATA_BLOCKED | MTC_POSITION_TRADING_OUTSIDE_CORE | acquire native data first; do not run on proxy |