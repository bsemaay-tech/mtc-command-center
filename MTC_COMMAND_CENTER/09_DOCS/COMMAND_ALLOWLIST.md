# Command Allowlist

Dashboard-triggered commands must be named operations, not free-form shell strings.

MVP-0 and MVP-1:

- Allowed: read-only file inspection, JSON parsing, schema validation, folder validation, health checks.
- Forbidden: backtests, package installs, webhooks, broker/exchange calls, shell command text boxes.

MVP-2:

- Allowed: controlled status/task write helpers through the write gate.
- Forbidden: direct arbitrary shell execution from dashboard UI.

MVP-4+:

- Allowed: explicitly configured MTC_v2 backtest commands only, with clean subprocess environment and lineage capture.

Outbound network access requires explicit task permission and report disclosure.
