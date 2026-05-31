# Start Here For Codex

Read these files in this order before making changes:

1. `03_DOCS/CLAUDE_CODE_HANDOFF_2026-05-29.md`
2. `03_DOCS/HANDOFF.md`
3. `03_DOCS/MTC_V2_ARCHITECTURE.md`
4. `03_DOCS/DEV_LOOP.md`
5. `03_DOCS/RUNBOOK.md`
6. `docs/CODEX_GENERIC_FEATURE_CHANGE_WORKFLOW.md`
7. `docs/INDEPENDENT_REFERENCE_ORACLE_POLICY.md`
8. `docs/PORTABLE_HANDOFF_PACKAGE_SCOPE.md`

## Current State - 2026-05-29

- Portable package is tracked source content and was refreshed after `b55068e9`.
- Factory regression hardening from `096c35c9` is included.
- Range Filter optimization POC from `4af32d71` is included.
- L22 `case_163` is documented as a manual TradingView export task; XLSX audit archives are not included in this main package.
- Legacy `tv_manual_inputs` paths are historical, not live data.

## Hard Rules

- Do not bypass parity gates.
- Do not claim TradingView release parity from local feature parity alone.
- Do not include generated outputs, caches, venvs, node_modules, or TradingView XLSX audit archives in the main portable package.
- If the package becomes stale, refresh it intentionally from the active repo root.
