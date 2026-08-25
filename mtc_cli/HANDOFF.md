# MTC CLI handoff

## Current state — 2026-08-25

- WP-P0-05 changes onboarding only; CLI code and behavior are untouched.
- D002 remains the architectural decision: CLI is the agent-native writer surface and dashboards
  wrap it rather than duplicate business logic.
- No CLI implementation, canonical write, migration, host, broker, or live command is authorized by
  this handoff.
