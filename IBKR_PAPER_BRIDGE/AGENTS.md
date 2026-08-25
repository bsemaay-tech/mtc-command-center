# Bridge execution stage rules

Despite its legacy name, this is the Hyperliquid paper/TESTNET execution Bridge. Any Bridge task not
explicitly proven unprotected at Gate 1 defaults protected. Risk, order behavior, persistence,
concurrency, broker/exchange, credentials, ARM, host/deploy, teardown, or live-facing work is T0.

- No host contact, deployment, secret handling, TESTNET/mainnet, ARM, order, threshold, runtime, or
  live action without exact owner authorization. Never recommend live trading.
- Startup is fail-closed: every start forces `DISARMED` unless state is `KILLED`; ARM is explicit.
- Execution accepts only frozen, hash-verified packages. Research labels and system tests grant no
  execution authority. `MTC_COMMAND_CENTER/_AI_MEMORY/LIVE_TRADING_GATE.md` remains unsigned unless
  the owner explicitly changes it.
- Preserve transaction, idempotency, order-state, risk, KILL, evidence, and migration contracts.
  Unknown or unevaluable state stops. No schema downgrade or silent historical deletion.
- Bridge implementation on protected core/runtime stays with a flagship implementer. Cheap models
  may not implement it. Audits use the root tier policy and exact roster.
- Any regression test offered as closure evidence shows real RED on pre-fix/equivalent mutation and
  GREEN with the fix. Check durable encoding/clock domains, not only parsed objects.
- Before designing or auditing an executable check/block/preregistration, read
  `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md`.

Run the suite from `IBKR_PAPER_BRIDGE` and ignore the ACL-locked collection directory exactly as
shown in `TESTS.md`. The two documented baseline failures are not permission to ignore new failures.
