# Bug and Repair Report

1. **Candidate Extraction Bug**: First run failed to extract verdicts properly due to YAML dictionary flattening. Fixed in audit script.
2. **Backtest Logic Bug**: First run `strategy_LBR_COIL` assumed fills at trigger price even if price gapped above. Fixed in `audit_phase4_to_8.py`.
3. **Classification Bug**: First run ranked everything as Tier C. Recomputed correctly.
