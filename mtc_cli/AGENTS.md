# MTC CLI stage rules

`mtc_cli` is the agent-native programmatic surface selected by D002. Dashboard actions wrap CLI/API
contracts one-for-one; business logic does not belong in the dashboard.

- Preserve a narrow, deterministic interface over canonical repository writers. Never create a
  second source of truth or bypass schema, lock, backup, validation, atomic-write, and event rules.
- File/status/registry writes are explicit and fail closed. Unknown schema/version/path/ownership or
  unevaluable state stops; never guess a default.
- No secrets in arguments, logs, fixtures, or repository files. No broker/host/live command family
  without exact owner authorization and T0 treatment.
- Maintain Windows/UTF-8/path behavior. Resolve configured paths, not the frozen legacy repo.
- CLI implementation is normally T1; any host, credential, network, deploy, broker, trading, or
  destructive action is T0 and separately authorized.
- Defect closure requires D026 RED/GREEN and real CLI execution, not direct-function simulation only.
