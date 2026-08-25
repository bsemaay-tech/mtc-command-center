# MTC build verification

- Run the exact scoped Python/PineTS/parity case command from the local runbook.
- Show D026 RED on pre-fix/equivalent mutation and GREEN on fixed code for every closure test.
- Verify source versions, export timestamp, oracle identity, tolerance, row counts, and skipped cases.
- Confirm no protected Pine/MTC/parity file outside the Gate-1 whitelist changed.
- Grep for stale values after corrections and ensure generated report/root bridge outputs are not
  staged unintentionally.
- If TradingView evidence is missing or stale, report `MISSING_EXPORT`/not comparable; do not pass.
