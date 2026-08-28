# MTC build inputs

- `03_DOCS/MTC_V2_ARCHITECTURE.md` — architecture source of truth.
- `03_DOCS/MTC_V2_INPUT_UI_SPEC.md` — Pine input-surface source of truth.
- `03_DOCS/RUNBOOK.md` — scoped operational procedure.
- Exact Pine/Python case, source versions, TradingView export identity/date, oracle, tolerance, and
  expected comparison mode.
- Relevant feature contract, parity oracle, and case fixture only; do not load whole evidence trees.
- Root `DECISIONS.md`, especially D003 and any explicit later authorization governing the task.

TradingView exports supplied by the user must retain provenance. Stale or missing exports are a
blocker to claims about TradingView parity, not permission to infer a result.
