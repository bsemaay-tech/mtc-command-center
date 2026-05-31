# Pine MCP Usage Rules

pine-mcp is a reference idea for future Pine tooling boundaries. In MCC foundation, it is not wired into the project.

## Rules

- Treat Pine tooling as advisory unless explicitly connected.
- Never send secrets through Pine tooling.
- Do not modify production Pine files directly.
- Record compile attempts and user-observed results in reports.
- Keep draft, review, and promotion stages separate.

## Future Contract

A future Pine tool adapter may expose compile checks, syntax diagnostics, and draft metadata. Until then, user-observed TradingView results are the source of truth.
