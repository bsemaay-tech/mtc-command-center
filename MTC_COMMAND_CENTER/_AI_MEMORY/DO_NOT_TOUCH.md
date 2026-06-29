# DO_NOT_TOUCH

Cross-check this file before EVERY write. Canonical safety detail:
`00_AGENT_PROTOCOLS/MTC_REPO_GUARD_PROTOCOL.md` + `_AI_MEMORY/AI_RULES.md`.

## Behavior (never change without explicit Barış approval)
- Do not modify Pine logic.
- Do not modify MTC strategy behavior or TradingView parity.
- Do not rewrite hardcoded paths until Barış approves rewrite policy.
- Do not change trading logic, promotion gates, or scoring rules.

## Protected scopes (no edits without explicit Barış approval)
- `MTC_COMMAND_CENTER/02_MTC_BACKTEST`
- `MTC_COMMAND_CENTER/07_ADAPTERS`
- `MTC_COMMAND_CENTER/01_PINE` and any `*.pine`
- `MTC_V2` (anywhere) and parity files
- `MTC_COMMAND_CENTER/06_SCHEMAS` (only via an approved `schema_allow`)
- `.git/`
Hard denylist in the cheap-agent harness (cannot be prompted away): `*.pine`, `parity`, `MTC_V2`, `.git/`.

## No execution without explicit approval
Backtests, optimizations, servers, launchers, artifact generation
(`backtest_profile_result.json`, `top_results.json`), broker/live/paper actions.

## Git hygiene
Never work on `master` (branch `feature/<scope>` first). Stage exact explicit paths only —
never `git add .` / `-A`. No `git reset --hard` / `push --force` / `stash` / `--no-verify`
without explicit approval.
