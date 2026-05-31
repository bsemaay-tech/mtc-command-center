# Metric Recompute Audit

Independent recomputation from each strategy's raw trades.csv.
Status meanings: MATCH (≤rounding), MINOR_ROUNDING_DIFF, MAJOR_MISMATCH.

| cand | trades_match | pf_first | pf_audit | pf | net_first | net_audit | net | dd_first | dd_audit | dd | wr_first | wr_audit | fee2_first | fee2_audit | fee3_first | fee3_audit | mono_first | mono_audit |
|------|--------------|---------:|---------:|----|----------:|----------:|----|---------:|---------:|----|---------:|---------:|-----------:|-----------:|-----------:|-----------:|------------|------------|
| CANDIDATE_001 | True | 1.7481 | 1.7481 | MINOR_ROUNDING_DIFF | 331.7517 | 331.7517 | MINOR_ROUNDING_DIFF | -46.3269 | -46.3269 | MATCH | 31.53 | 31.53 | 1.6786 | 1.6786 | 1.6132 | 1.6132 | True | True |
| CANDIDATE_002 | True | 1.4435 | 1.4435 | MINOR_ROUNDING_DIFF | 17034.8144 | 17034.8144 | MINOR_ROUNDING_DIFF | -91.7686 | -91.7686 | MATCH | 31.85 | 31.85 | 1.4078 | 1.4078 | 1.3733 | 1.3733 | True | True |
| CANDIDATE_003 | True | 1.4581 | 1.4581 | MINOR_ROUNDING_DIFF | 292669.9798 | 292669.9798 | MINOR_ROUNDING_DIFF | -86.417 | -86.417 | MATCH | 38.11 | 38.11 | 1.3872 | 1.3872 | 1.3207 | 1.3207 | True | True |
| CANDIDATE_004 | True | 1.251 | 1.251 | MINOR_ROUNDING_DIFF | 7179649232.748 | 7179649232.748 | MINOR_ROUNDING_DIFF | -98.442 | -98.442 | MATCH | 47.45 | 47.45 | 1.1866 | 1.1866 | 1.126 | 1.126 | True | True |
| CANDIDATE_005 | True | 1.4516 | 1.4516 | MINOR_ROUNDING_DIFF | 3955.225 | 3955.225 | MINOR_ROUNDING_DIFF | -79.8493 | -79.8493 | MATCH | 46.67 | 46.67 | 1.4236 | 1.4236 | 1.3962 | 1.3962 | True | True |
| CANDIDATE_007 | True | 1.3096 | 1.3096 | MINOR_ROUNDING_DIFF | 1206.3069 | 1206.3069 | MINOR_ROUNDING_DIFF | -85.9357 | -85.9357 | MATCH | 63.03 | 63.03 | 1.2609 | 1.2609 | 1.2138 | 1.2138 | True | True |
| CANDIDATE_008 | True | 0.5383 | 0.5383 | MINOR_ROUNDING_DIFF | -99.4805 | -99.4805 | MINOR_ROUNDING_DIFF | -99.4799 | -99.4799 | MATCH | 34.14 | 34.14 | 0.3067 | 0.3067 | 0.1848 | 0.1848 | True | True |
| CANDIDATE_009 | True | 1.0861 | 1.0861 | MINOR_ROUNDING_DIFF | 3.0885 | 3.0885 | MINOR_ROUNDING_DIFF | -7.1457 | -7.1457 | MATCH | 49.01 | 49.01 | 0.716 | 0.716 | 0.4825 | 0.4825 | True | True |
| CANDIDATE_011 | True | 0.5201 | 0.5201 | MINOR_ROUNDING_DIFF | -96.8928 | -96.8928 | MINOR_ROUNDING_DIFF | -98.614 | -98.614 | MATCH | 43.24 | 43.24 | 0.5031 | 0.5031 | 0.4865 | 0.4865 | True | True |
| CANDIDATE_012 | True | 1.8741 | 1.8741 | MINOR_ROUNDING_DIFF | 738.7124 | 738.7124 | MINOR_ROUNDING_DIFF | -82.1442 | -82.1442 | MATCH | 23.7 | 23.7 | 1.8376 | 1.8376 | 1.8023 | 1.8023 | True | True |