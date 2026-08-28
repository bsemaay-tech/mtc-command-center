# Bridge inputs

- Exact Gate-1 contract: protected/unprotected classification, allowed paths, runtime/host boundary,
  acceptance evidence, and rollback.
- Relevant contract under `docs/` (order state through KILL-evidence epoch) and exact schema target.
- Root `DECISIONS.md`; open a linked full decision only when it directly governs this work.
- For executable safety checks: `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md`.
- Frozen candidate identity, deployed identity if in scope, database/schema version, config, and
  dependency lock. Never ingest `.env`, keys, wallet/broker secrets, or unredacted credentials.
- Host/deploy work additionally requires exact host, command, backup, rollback, stop conditions, and
  a T0 two-flagship audit contract before execution.
