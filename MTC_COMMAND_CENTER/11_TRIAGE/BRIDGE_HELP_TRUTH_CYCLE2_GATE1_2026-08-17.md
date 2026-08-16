# Bridge Help truth correction — fresh T1 cycle

**Date:** 2026-08-17  
**Owner authorization:** Barış's overnight instruction to continue all safe work
without waiting, issued after the prior T1-cap report. This is recorded as the
explicit authorization to open a materially fresh, narrowly bounded cycle; it
is not a silent third round of the exhausted cycle.

## Gate 1 classification

- **Audit tier:** T1 — non-economic Help/UI knowledge and tests.
- **Fresh scope:** correct only the two source-truth defects discovered at the
  prior cycle's final review.
- **Writer:** fresh counterpart Claude Max session; no session continuation.
- **Acceptance:** fresh Codex `gpt-5.6-sol` high read-only review, round 1 of this
  new cycle. GLM-5.2 second opinion is attempted because the complete inherited
  Help diff exceeds 300 lines; quota failure remains recorded, never silently
  substituted.

## Allowed files

- `IBKR_PAPER_BRIDGE/bridge/static/help_map.json`
- `IBKR_PAPER_BRIDGE/tests/test_dashboard_static.py`
- `IBKR_PAPER_BRIDGE/docs/31_HELP_SYSTEM_MAP_INDEX.md` only if its maintenance
  guidance needs alignment with the new assertions.

All other files are read-only. The existing Help implementation in
`C:\BRIDGE_HELP_IMPL` must be preserved; no reset, checkout, stash, commit, host,
deployment, credential, runtime, strategy, broker, exchange, or economic action.

## Exact repairs

1. **LLM gate:** describe it as dormant/unwired scaffolding. Runtime constructs
   `NullLLMGate`; YAML switches do not activate it today; logging/directive Store
   relationships are planned, not operational. Preserve the future boundary:
   an enabled gate can suppress/select trades and affect outcomes but cannot
   originate or enlarge orders.
2. **Dashboard V1:** describe six original pages plus Help; next-bar UTC time,
   not a countdown; initial WebSocket snapshot with no automatic reconnect.
   Correct the duplicate readiness statement.

## Success criteria

- New focused tests fail against the inherited wording and pass after repair.
- Existing static Help suite passes.
- JSON structure/targets/sources pass; Node syntax and `git diff --check` pass.
- Complete Bridge suite has no new failures beyond the two reproduced baseline
  failures.
- Fresh T1 reviewer returns PASS or PASS-WITH-NITS before commit/transfer.
