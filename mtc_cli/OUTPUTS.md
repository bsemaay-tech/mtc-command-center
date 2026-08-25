# MTC CLI outputs

- Minimal command/interface change with stable help, deterministic exit codes, and structured output.
- Validated atomic writes with backup/event evidence when the command mutates canonical state.
- Tests covering success, invalid input, schema/version mismatch, collision/lock, and unevaluable state.
- Current-only state in `HANDOFF.md`; no dashboard business-logic duplication.
