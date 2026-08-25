# MTC backtest verification

- Run the smallest relevant unit/integration suite and the exact affected CLI path.
- For validation changes, execute `python -m src.cli.mtc_engine_validate` with explicit profile and
  fixtures; never infer behavior from source alone.
- Verify deterministic input/config identity, row counts, numeric tolerances, and skipped reasons.
- Demonstrate RED/GREEN for defect closure and preserve parity/goldens unless separately authorized.
- Confirm no generated output, secret, local path override, Pine, MTC controller, or unrelated parity
  file is staged.
